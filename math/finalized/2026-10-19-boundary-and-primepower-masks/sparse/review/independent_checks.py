#!/usr/bin/env python3
"""Fresh independent exact controls. No imported or executed research checker."""
import hashlib
import itertools
import json
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
COUNTS = Counter()


def polynomial_remainder(coefficients, p, a):
    """Long division by 1+X^n+...+X^((p-1)n), not fiber matching."""
    if a == 0:
        return (sum(coefficients),)
    L, n = p**a, p**(a-1)
    degree = L-n
    c = list(coefficients) + [0]*max(0, L-len(coefficients))
    for high in range(len(c)-1, degree-1, -1):
        q = c[high]
        if q:
            offset = high-degree
            for t in range(p):
                c[offset+t*n] -= q
    return tuple(c[:degree])


def root_sum(terms, p, a):
    L = p**a
    c = [0]*L
    for exponent, coefficient in terms:
        c[exponent % L] += coefficient
    return polynomial_remainder(c, p, a)


def is_zero(v):
    return not any(v)


@dataclass
class Matrix:
    p: int
    a: int
    d: int
    x: list
    y: list
    k: list
    supports: list
    name: str

    def record(self):
        return dict(p=self.p, a=self.a, d=self.d, x=self.x, y=self.y,
                    k=self.k, supports=[sorted(s) for s in self.supports], name=self.name)


def validate(A):
    m, p, a = len(A.x), A.p, A.a
    assert m > 0 and len(A.y) == len(A.k) == len(A.supports) == m
    assert A.d > 0 and a >= 0
    L = p**a
    assert all(0 <= x < L for x in A.x+A.y)
    assert all(isinstance(k, int) and k >= 0 for k in A.k)
    assert all(s and s <= set(range(m)) for s in A.supports)
    weights = [p**k for k in A.k]
    # Row Gram: off-diagonal common amplitude is positive and factored out.
    for i in range(m):
        assert weights[i]*len(A.supports[i]) == A.d, ('row diagonal', A.name, i)
        for h in range(m):
            if h != i:
                terms = [((A.x[i]-A.x[h])*A.y[j], 1)
                         for j in A.supports[i] & A.supports[h]]
                assert is_zero(root_sum(terms, p, a)), ('row Gram', A.name, i, h)
            COUNTS['row_gram_entries'] += 1
    # Column Gram: row weights must remain inside the sum.
    for j in range(m):
        for l in range(m):
            terms = [(A.x[i]*(A.y[l]-A.y[j]), weights[i]) for i in range(m)
                     if j in A.supports[i] and l in A.supports[i]]
            got = root_sum(terms, p, a)
            target = (A.d if j == l else 0,) + (0,)*(len(got)-1)
            assert got == target, ('column Gram', A.name, j, l)
            COUNTS['column_gram_entries'] += 1
    COUNTS['validated_matrices'] += 1


def descend(A, records):
    validate(A)
    p, a, m = A.p, A.a, len(A.x)
    records.append(A.record())
    if a == 0:
        assert all(len(s) == 1 for s in A.supports)
        assert len(set(next(iter(s)) for s in A.supports)) == m
        assert all(p**k == A.d for k in A.k)
        COUNTS['terminal_matrices'] += 1
        COUNTS['terminal_rows'] += m
        return list(A.k)
    L, n = p**a, p**(a-1)
    residues = [{A.y[j] % p for j in s} for s in A.supports]
    mixed = {i for i, t in enumerate(residues) if len(t) > 1}
    done = set()
    output = []
    for i in range(m):
        if i in done:
            continue
        if i not in mixed:
            t = next(iter(residues[i]))
            output.append((A.x[i] % n, A.k[i], A.supports[i], t, A.x[i]))
            done.add(i)
            COUNTS['pure_rows'] += 1
            continue
        S = A.supports[i]
        j0 = min(S)
        j1 = min(j for j in S if A.y[j] % p != A.y[j0] % p)
        u = A.x[i] % n
        siblings = []
        # Find from anchor pair only; do not assume matching supports or weights.
        for q in range(p):
            hits = [h for h in range(m) if A.x[h] == u+q*n
                    and j0 in A.supports[h] and j1 in A.supports[h]]
            assert len(hits) == 1
            h = hits[0]
            assert h not in done and A.supports[h] == S and A.k[h] == A.k[i]
            siblings.append(h)
        assert len(set(siblings)) == p
        counts = Counter(A.y[j] % p for j in S)
        assert len(counts) == p and len(set(counts.values())) == 1
        done.update(siblings)
        COUNTS['matched_tuples'] += 1
        for t in range(p):
            restricted = {j for j in S if A.y[j] % p == t}
            assert restricted
            # Independently verify every entry of the actual Fourier row sum.
            # Clearing 1/sqrt(p) leaves p*zeta^(u*y) on the matching residue.
            for j in range(m):
                terms = []
                if j in S:
                    terms = [((u+q*n)*A.y[j]-t*q*n, 1) for q in range(p)]
                if j in restricted:
                    terms.append((u*A.y[j], -p))
                assert is_zero(root_sum(terms, p, a))
                COUNTS['row_fourier_entry_checks'] += 1
            output.append((u, A.k[i]+1, restricted, t, u))
    assert done == set(range(m)) and len(output) == m
    answer = []
    for t in range(p):
        J = [j for j in range(m) if A.y[j] % p == t]
        I = [o for o in output if o[3] == t]
        assert len(I) == len(J), ('block dimension', A.name, t)
        if not J:
            continue
        mapping = {old: new for new, old in enumerate(J)}
        for x, k, S, _, oldx in I:
            for j in J:
                yprime = (A.y[j]-t)//p
                # Exact exponent congruence for diagonal row dephasing.
                assert (oldx*A.y[j]-oldx*t-p*x*yprime) % L == 0
                COUNTS['dephasing_entry_checks'] += 1
        B = Matrix(p, a-1, A.d, [o[0] for o in I],
                   [(A.y[j]-t)//p for j in J], [o[1] for o in I],
                   [{mapping[j] for j in o[2]} for o in I], A.name+f'/{t}')
        answer += descend(B, records)
    assert len(answer) == m
    return answer


CONNECTED = [
    [0,0,1,1,0,0,1,1], [0,1,0,1,0,1,0,1],
    [1,1,0,0,1,1,0,0], [1,0,1,0,1,0,1,0],
    [0,0,1,1,0,0,1,1], [1,0,1,0,1,0,1,0],
    [1,1,0,0,1,1,0,0], [0,1,0,1,0,1,0,1]]


def divisor_case(p, a, b):
    N, d = p**a, p**b
    m = N//d
    supports = [{t+l*m for l in range(d)} for t in range(m) for _ in range(d)]
    return Matrix(p, a, d, list(range(N)), list(range(N)), [0]*N, supports,
                  f'divisor_p{p}_a{a}_b{b}')


def weighted_stress(p, a):
    """Direct sum of differently sized, differently weighted Fourier blocks."""
    L, x, y, k, supports = p**a, [], [], [], []
    for j in range(a+1):
        for orientation in (0, 1):
            q, offset = p**j, len(x)
            x += [r*(L//q if orientation == 0 else 1) for r in range(q)]
            y += [c*(1 if orientation == 0 else L//q) for c in range(q)]
            k += [a-j]*q
            supports += [set(range(offset, offset+q)) for _ in range(q)]
    assert len(set(x)) < len(x) and len(set(y)) < len(y)
    assert len(set(k)) > 1 and len(x) != L
    return Matrix(p, a, L, x, y, k, supports, f'weighted_stress_p{p}_a{a}')


def rejection_control(A, label):
    try:
        validate(A)
    except AssertionError as e:
        return {'control': label, 'rejected': True, 'reason': str(e)}
    raise AssertionError(('bad control unexpectedly passed', label))


def small_census():
    out = {}
    for p, a in [(2, 1), (3, 1), (2, 2)]:
        N, counts, tested = p**a, Counter(), 0
        for bits in itertools.product((0, 1), repeat=N*N):
            tested += 1
            supports = [{j for j in range(N) if bits[i*N+j]} for i in range(N)]
            d = len(supports[0])
            if d == 0 or any(len(s) != d for s in supports):
                continue
            if any(sum(j in s for s in supports) != d for j in range(N)):
                continue
            if any(not is_zero(root_sum([((i-h)*j, 1) for j in supports[i]&supports[h]], p, a))
                   for i in range(N) for h in range(i)):
                continue
            A = Matrix(p, a, d, list(range(N)), list(range(N)), [0]*N,
                       supports, f'census_N{N}_{tested}')
            validate(A)
            counts[d] += 1
        assert set(counts) == {p**b for b in range(a+1)}
        out[str(N)] = dict(binary_masks_tested=tested, accepted_by_d=dict(counts))
    return out


def cyclotomic_controls():
    out = []
    # Exhaust every coefficient vector over {-1,0,1} for L <= 9.
    for p, a in [(2,1), (2,2), (2,3), (3,1), (3,2), (5,1), (7,1)]:
        L, n = p**a, p**(a-1)
        tested = 0
        for coeff in itertools.product((-1,0,1), repeat=L):
            expected = all(len({coeff[u+q*n] for q in range(p)}) == 1 for u in range(n))
            assert is_zero(polynomial_remainder(coeff, p, a)) == expected
            # All units at small orders explicitly test the h dependence.
            for h in range(1,L):
                if h % p:
                    got = root_sum([(h*x, coeff[x]) for x in range(L)], p, a)
                    assert is_zero(got) == expected
            tested += 1
        # Rational coefficients are also checked, independent of p-power weights.
        base = [Fraction((-1)**u*(u+1), u+2) for u in range(n)]
        coeff = [base[x % n] for x in range(L)]
        assert is_zero(polynomial_remainder(coeff, p, a))
        coeff[-1] += Fraction(1,11)
        assert not is_zero(polynomial_remainder(coeff, p, a))
        out.append(dict(p=p, a=a, signed_coefficient_vectors=tested,
                        unit_multipliers='all', rational_controls=2))
    return out


class Qz8:
    """Independent exact field arithmetic, z^4=-1."""
    def __init__(self, value=0):
        if isinstance(value, Qz8):
            self.c = value.c
        elif isinstance(value, (int, Fraction)):
            self.c = (Fraction(value), Fraction(0), Fraction(0), Fraction(0))
        else:
            self.c = tuple(Fraction(v) for v in value)
            assert len(self.c) == 4
    def __add__(self, other):
        o = Qz8(other)
        return Qz8([a+b for a,b in zip(self.c,o.c)])
    __radd__ = __add__
    def __neg__(self): return Qz8([-a for a in self.c])
    def __sub__(self, other): return self+-Qz8(other)
    def __rsub__(self, other): return Qz8(other)+-self
    def __mul__(self, other):
        o, c = Qz8(other), [Fraction(0)]*4
        for i,a in enumerate(self.c):
            for j,b in enumerate(o.c):
                c[(i+j)%4] += a*b*(1 if i+j < 4 else -1)
        return Qz8(c)
    __rmul__ = __mul__
    def __bool__(self): return any(self.c)
    def __eq__(self, other): return self.c == Qz8(other).c
    def conjugate(self):
        return sum((a*root8(-i) for i,a in enumerate(self.c)), Qz8())
    def inverse(self):
        # Solve multiplication-by-self over Q, rather than importing algebra code.
        columns = [(self*root8(j)).c for j in range(4)]
        rows = [[columns[j][i] for j in range(4)] + [Fraction(i == 0)] for i in range(4)]
        for j in range(4):
            pivot = next(i for i in range(j,4) if rows[i][j])
            rows[j],rows[pivot] = rows[pivot],rows[j]
            q = rows[j][j]
            rows[j] = [v/q for v in rows[j]]
            for i in range(4):
                if i != j:
                    q = rows[i][j]
                    rows[i] = [v-q*w for v,w in zip(rows[i],rows[j])]
        result = Qz8([rows[i][-1] for i in range(4)])
        assert self*result == 1
        return result
    def data(self): return [str(v) for v in self.c]


def root8(t):
    t %= 8
    v = [0]*4
    v[t%4] = 1 if t < 4 else -1
    return Qz8(v)


def adjoint(A): return [[A[i][j].conjugate() for i in range(len(A))] for j in range(len(A[0]))]
def multiply(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))), Qz8())
             for j in range(len(B[0]))] for i in range(len(A))]
def scalar_identity(A,s):
    return all(A[i][j] == (s if i == j else 0) for i in range(len(A)) for j in range(len(A)))


def connected_original_model():
    N = 8
    H = [[root8(i*j) for j in range(N)] for i in range(N)]
    D = [[CONNECTED[i][j]*H[i][j] for j in range(N)] for i in range(N)]
    A = [[H[i][j]-D[i][j] for j in range(N)] for i in range(N)]
    B = [[Fraction(1,4)*v for v in row] for row in adjoint(A)]
    augmented = [B[i][:]+[Qz8(int(i==j)) for j in range(N)] for i in range(N)]
    for j in range(N):
        pivot = next(i for i in range(j,N) if augmented[i][j])
        augmented[j],augmented[pivot] = augmented[pivot],augmented[j]
        inverse = augmented[j][j].inverse()
        augmented[j] = [v*inverse for v in augmented[j]]
        for i in range(N):
            if i != j:
                q = augmented[i][j]
                augmented[i] = [v-q*w for v,w in zip(augmented[i],augmented[j])]
    M = [row[N:] for row in augmented]
    assert scalar_identity(multiply(M,B),1) and scalar_identity(multiply(B,M),1)
    assert all(sum(bool(v) for v in row) == 4 for row in B)
    assert all(sum(bool(B[i][j]) for i in range(N)) == 4 for j in range(N))
    E = [[M[i][j]-H[i][j] for j in range(N)] for i in range(N)]
    grams = dict(DstarD=multiply(adjoint(D),D), DDstar=multiply(D,adjoint(D)),
                 EstarE=multiply(adjoint(E),E), EEstar=multiply(E,adjoint(E)))
    assert all(scalar_identity(G,4) for G in grams.values())
    seen, todo = {('r',0)}, [('r',0)]
    while todo:
        side,i = todo.pop()
        neighbors = [('c',j) for j in range(N) if CONNECTED[i][j]] if side == 'r' else [('r',j) for j in range(N) if CONNECTED[j][i]]
        for node in neighbors:
            if node not in seen:
                seen.add(node); todo.append(node)
    assert len(seen) == 2*N
    data = dict(N=8,d=4,connected_vertices=len(seen),normalization='M_original=M_tilde/sqrt(8); inverse=sqrt(8)*B_tilde',
                M_tilde=[[v.data() for v in row] for row in M],
                B_tilde=[[v.data() for v in row] for row in B],
                grams={name:[[v.data() for v in row] for row in G] for name,G in grams.items()})
    return data


def main():
    records, cases = [], []
    for p, maxa in [(2,6),(3,3),(5,2),(7,2)]:
        for a in range(1,maxa+1):
            for b in range(a+1):
                A = divisor_case(p,a,b)
                terminal = descend(A,records)
                assert set(terminal) == {b}
                cases.append(A.name)
    connected = Matrix(2,3,4,list(range(8)),list(range(8)),[0]*8,
                       [{j for j,v in enumerate(row) if v} for row in CONNECTED], 'connected_8_4')
    assert set(descend(connected,records)) == {2}
    cases.append(connected.name)
    for p,a in [(2,3),(3,2),(5,1)]:
        A = weighted_stress(p,a)
        assert set(descend(A,records)) == {a}
        cases.append(A.name)
    for p,b in [(2,0),(2,4),(3,2)]:
        A = Matrix(p,0,p**b,[0]*3,[0]*3,[b]*3,[{0},{1},{2}],f'order1_p{p}_k{b}')
        assert set(descend(A,records)) == {b}
        cases.append(A.name)
    descent_counters = dict(COUNTS)
    negatives = []
    switched = [set(s) for s in connected.supports]
    # Degree-preserving 2x2 switch: rows 0,1 and columns 1,2.
    switched[0].remove(2); switched[0].add(1)
    switched[1].remove(1); switched[1].add(2)
    assert all(len(s)==4 for s in switched)
    assert all(sum(j in s for s in switched)==4 for j in range(8))
    negatives.append(rejection_control(Matrix(2,3,4,list(range(8)),list(range(8)),[0]*8,switched,'switched'), 'degree-preserving switch'))
    bad_k = connected.k[:]; bad_k[0] = 1
    negatives.append(rejection_control(Matrix(2,3,4,connected.x,connected.y,bad_k,connected.supports,'bad_weight'), 'corrupt row weight'))
    negatives.append(rejection_control(Matrix(2,0,3,[0],[0],[0],[{0}],'bad_base'), 'non-power base d'))
    negatives.append(rejection_control(Matrix(2,0,1,[],[],[],[],'empty'), 'empty matrix'))
    # Columns alone permit aggregation of several same-label rows: 3x2 countercontrol.
    rectangular_columns = [root_sum([(0,2),(1,1),(1,1)],2,1), root_sum([(0,4)],2,1)]
    assert rectangular_columns == [(0,), (4,)]
    assert root_sum([(0,1),(0,1)],2,1) == (2,)  # duplicate-row Gram is nonzero
    negatives.append(dict(control='column-only rectangular matching counterexample',
                          rows=[dict(x=0,k=1),dict(x=1,k=0),dict(x=1,k=0)],
                          y=[0,1],supports=[[0,1]]*3,column_gram='4 I_2',
                          equal_weight_matching_exists=False, rejected_by_full_class=True))
    result = dict(status='PASS',positive_cases=cases,positive_case_count=len(cases),
                  descent_counters=descent_counters,counters=dict(COUNTS),small_census=small_census(),
                  cyclotomic_controls=cyclotomic_controls(),negative_controls=negatives)
    original = connected_original_model()
    result['counters'] = dict(COUNTS)
    result['original_model_control'] = dict(both_inverse_products=True,both_error_grams=True,
                                          every_inverse_row_and_column_support=4,connected_vertices=16)
    (HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'INDEPENDENT_DESCENT_CERTIFICATES.json').write_text(json.dumps(records,indent=2)+'\n')
    (HERE/'INDEPENDENT_ORIGINAL_MODEL.json').write_text(json.dumps(original,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',positive_cases=len(cases),counters=dict(COUNTS)),indent=2))


if __name__ == '__main__':
    main()
