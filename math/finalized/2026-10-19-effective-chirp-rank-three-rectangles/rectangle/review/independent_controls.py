#!/usr/bin/env python3
"""Fresh, characteristic-zero controls; no historical checker is imported/executed."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import random
import time
import sympy as sp

OUT = Path(__file__).resolve().parent
RNG = random.Random(202610191202)
X = sp.Symbol('x')
COUNTS = Counter()
CERTIFICATES = []
START = time.monotonic()


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Cyclotomic:
    def __init__(self, n):
        self.n = n
        self.poly = sp.Poly(sp.cyclotomic_poly(n, X), X)
        self.degree = self.poly.degree()
        self.lower = [(int(e[0]), -int(c)) for e, c in self.poly.terms()
                      if e[0] != self.degree]

    @lru_cache(None)
    def monomial(self, exponent):
        exponent %= self.n
        if exponent < self.degree:
            return ((exponent, 1),)
        out = Counter()
        for lower, coefficient in self.lower:
            for e, c in self.monomial(exponent - self.degree + lower):
                out[e] += coefficient * c
        return tuple(sorted((e, c) for e, c in out.items() if c))

    def reduce(self, expression):
        out = Counter()
        for exponent, coefficient in expression.items():
            if coefficient:
                for e, c in self.monomial(exponent):
                    out[e] += coefficient * c
        return tuple(sorted((e, c) for e, c in out.items() if c))

    def determinant(self, rows, cols):
        COUNTS['exact_determinant_calls'] += 1
        return self.reduce(det_expression(self.n, rows, cols))


@lru_cache(None)
def field(n):
    return Cyclotomic(n)


@lru_cache(None)
def signed_permutations(k):
    result = []
    for perm in permutations(range(k)):
        inversions = sum(perm[i] > perm[j] for i in range(k) for j in range(i+1, k))
        result.append((perm, -1 if inversions % 2 else 1))
    return result


def det_expression(n, rows, cols):
    assert len(rows) == len(cols)
    result = Counter()
    for perm, sign in signed_permutations(len(rows)):
        result[sum(rows[i] * cols[perm[i]] for i in range(len(rows))) % n] += sign
    return {e: c for e, c in result.items() if c}


def independent_sympy_check(n, rows, cols):
    # Expand the determinant in SymPy directly, rather than use our permutation routine.
    z = sp.Matrix([[X ** ((r*c) % n) for c in cols] for r in rows])
    raw = sp.Poly(z.det(method='domain-ge'), X)
    actual = raw.rem(field(n).poly)
    actual_dict = tuple(sorted((int(e[0]), int(c)) for e, c in actual.terms() if c))
    assert field(n).determinant(rows, cols) == actual_dict
    COUNTS['direct_sympy_determinant_crosschecks'] += 1


def find_minor(n, rows, cols):
    k = len(cols)
    for _ in range(24):
        selected = RNG.sample(rows, k)
        if field(n).determinant(selected, cols):
            return selected
    for selected in combinations(rows, k):
        if field(n).determinant(selected, cols):
            return list(selected)
    raise AssertionError(('no nonzero minor', n, rows, cols))


PAIRS = [(5,7), (7,5), (5,11), (11,5), (7,13), (13,7),
         (11,13), (13,11), (13,17), (17,13), (17,19), (19,17)]

# 1. Projection from the actual mixed-order Fourier phases, in both prime orders.
for p, q in PAIRS:
    n = p*p*q
    for iteration in range(100):
        base = RNG.randrange(q)
        u = RNG.sample(range(p*p), 4)
        rows = [base+q*t for t in u]
        residues = RNG.sample(range(p), 4)
        cols = [v + p*RNG.randrange(p*q) for v in residues]
        actual = field(n).determinant(rows, cols)
        assert actual
        lower_expr = det_expression(p*p, u, [c % (p*p) for c in cols])
        expected = Counter()
        for e, coefficient in lower_expr.items():
            expected[(base*sum(cols)+q*e) % n] += coefficient
        assert actual == field(n).reduce(expected)
        assert field(p*p).determinant(u, [c % (p*p) for c in cols])
        COUNTS['actual_phase_projection_controls'] += 1
        if iteration == 0:
            independent_sympy_check(n, rows, cols)

# 2. Short-support lemma at the correct threshold, with either prime repeated.
for p, q in PAIRS:
    m, maximum = p*q, max(p,q)
    for k in (2,3,4):
        size = (k-1)*maximum+1
        for iteration in range(60):
            cols = RNG.sample(range(m), k)
            if iteration % 3 == 0:
                # Residue-concentrated row ordering, not just random subsets.
                order = [a+p*b for a in RNG.sample(range(p),p) for b in range(q)]
                rows = order[:size]
            elif iteration % 3 == 1:
                order = [a+q*b for a in RNG.sample(range(q),q) for b in range(p)]
                rows = order[:size]
            else:
                rows = RNG.sample(range(m), size)
            chosen = find_minor(m, rows, cols)
            assert len(set(chosen)) == k
            COUNTS['semiprime_short_support_rank_controls'] += 1
            if iteration == 0:
                independent_sympy_check(m, chosen, cols)
    # Arithmetic bound for every composition of k' through four terms.
    for kp in range(1,5):
        def compositions(total, length):
            if length == 1:
                yield (total,)
            else:
                for head in range(1,total-length+2):
                    for tail in compositions(total-head,length-1):
                        yield (head,)+tail
        for t in range(1,kp+1):
            for sizes in compositions(kp,t):
                for z0 in range(min(sizes)):
                    bound = min(p,q)*(t-1)+(maximum-t+1)*z0
                    assert bound <= maximum*(kp-1)
                    COUNTS['support_zero_envelopes'] += 1

# 3. Full target one-residue rectangles, with 79 rows and columns.
p, q, n = 13, 17, 2873
for iteration in range(150):
    y = RNG.randrange(p)
    A = RNG.sample(range(p*q),79)
    rows = [y+p*a for a in A]
    cols = RNG.sample(range(n),79)
    representatives = {}
    for c in cols:
        representatives.setdefault(c % (p*q),c)
    selected_cols = list(representatives.values())[:4]
    reduced_cols = [c % (p*q) for c in selected_cols]
    selected_a = find_minor(p*q,A,reduced_cols)
    selected_rows = [y+p*a for a in selected_a]
    assert field(n).determinant(selected_rows,selected_cols)
    COUNTS['target_one_row_residue_four_minors'] += 1

# 4. Explicit four-minor formula for the formerly difficult s=2 and s=3 cases.
for p,q in PAIRS:
    n=p*p*q
    for iteration in range(150):
        r0=RNG.randrange(p*p)
        w=RNG.sample(range(q),3)
        rows=[r0+p*p*t for t in w]
        rstar=RNG.randrange(n)
        while (rstar-r0)%p == 0:
            rstar=RNG.randrange(n)
        rows.append(rstar)
        v=RNG.sample(range(q),3)
        c1=v[0]+q*RNG.randrange(p*p)
        c4=(c1+q*RNG.randrange(1,p*p))%n
        c2=v[1]+q*RNG.randrange(p*p)
        c3=v[2]+q*RNG.randrange(p*p)
        cols=[c1,c2,c3,c4]
        top=det_expression(n,rows[:3],cols[:3])
        expected=Counter()
        for e, coefficient in top.items():
            expected[(e+rstar*c4)%n] += coefficient
            expected[(e+r0*(c4-c1)+rstar*c1)%n] -= coefficient
        actual=field(n).determinant(rows,cols)
        assert actual and actual==field(n).reduce(expected)
        assert ((rstar-r0)*(c4-c1))%n != 0
        assert field(q).determinant(w,v)
        COUNTS['explicit_four_minor_factorizations'] += 1
        if (p,q)==(13,17):
            CERTIFICATES.append({'N':n,'rows':rows,'columns':cols,
                                 'r0':r0,'row_lifts':w,
                                 'remainder_sha256':hashlib.sha256(repr(actual).encode()).hexdigest()})
        if iteration==0:
            independent_sympy_check(n,rows,cols)

# 5. Two-residue direct-sum lemma at N=2873, checked separately although not needed
# in the simplified proof. Two rich lifts give supported block vectors; certify a
# genuine 4-minor in the whole 40-row by 6-column matrix.
p,q,n=13,17,2873
for iteration in range(150):
    y=RNG.sample(range(p),2)
    A=RNG.sample(range(p*q),35)
    B=RNG.sample(range(p*q),5)
    rows=[y[0]+p*a for a in A]+[y[1]+p*b for b in B]
    T=RNG.sample(range(p*q),3)
    cols=[t+p*q*w for t in T for w in RNG.sample(range(p),2)]
    # Independent search for four rows/columns; exact characteristic-zero certificate.
    for trial in range(100):
        rr=RNG.sample(rows,4); cc=RNG.sample(cols,4)
        if field(n).determinant(rr,cc):
            break
    else:
        raise AssertionError('direct-sum certificate search failed')
    COUNTS['two_residue_direct_sum_certificates'] += 1

# 6. Boundary examples: actual rank-three rectangles, not scalar shapes alone.
for p,q in PAIRS:
    n=p*p*q
    for d in (p,q,p*p,p*q):
        # Three cosets of a subgroup of size d, paired with its annihilator.
        spacing=n//d
        if spacing<3:
            continue
        rows=[j+spacing*k for j in range(3) for k in range(d)]
        cols=[d*k for k in range(spacing)]
        assert len(set(rows))==3*d and len(set(cols))==spacing
        chosen=find_minor(n,rows,cols[:3])
        assert field(n).determinant(chosen,cols[:3])
        for _ in range(15):
            if len(cols)>=4:
                assert not field(n).determinant(RNG.sample(rows,4),RNG.sample(cols,4))
                COUNTS['genuine_rank_three_zero_four_minors'] += 1
        # Exact rank≤3 from rows differing by spacing within each coset.
        assert all((spacing*c)%n==0 for c in cols)
        assert min(len(rows),len(cols))<=max(6*p,3*q)
        COUNTS['genuine_rank_three_examples'] += 1

# 7. Exhaust the relevant occupancy capacities and all target scalar shapes.
p,q,n=13,17,2873
B=max(6*p,3*q)
assert B==78
for s in range(1,4):
    assert 2*s*p<=B
    for t in range(1,4):
        assert 2*t*p<=B
        COUNTS['occupancy_count_pairs'] += 1
assert 2*13+(3*17-2)==75
assert 3*17==51 and 3*13==39
scalar_min=None; scalar_argmin=[]
for a in range(1,79):
    for b in range(a,min(n,3*n//a)+1):
        density=Fraction(3,a)+Fraction(3,b)
        assert density>=Fraction(29,442)>Fraction(186,n)
        COUNTS['target_scalar_shapes'] += 1
        if scalar_min is None or density<scalar_min:
            scalar_min=density; scalar_argmin=[(a,b)]
        elif density==scalar_min:
            scalar_argmin.append((a,b))
divisors=[d for d in range(1,n+1) if n%d==0]
D=min(d+n//d for d in divisors)
E2=min(2*d+n//d for d in divisors if d<n)
assert (D,E2)==(186,203)
assert {tuple(sorted((d,n//d))) for d in divisors if d+n//d==D}=={(17,169)}
assert Fraction(29,442)-Fraction(D,n)==Fraction(5,5746)
assert Fraction(E2,n)>Fraction(29,442)
assert 16*442*442>29*29*n
assert n*D==534378

# 8. Every entry in an explicit optimal tiling, with exact difference identities.
coverage=bytearray(n*n)
cost=0; tile_count=0
for u in range(169):
    rows=[u+169*k for k in range(17)]
    for v in range(17):
        cols=[v+17*l for l in range(169)]
        for r in rows:
            for c in cols:
                assert ((r-rows[0])*(c-cols[0]))%n==0
                index=r*n+c
                assert coverage[index]==0
                coverage[index]=1
        cost+=len(rows)+len(cols)
        tile_count+=1
assert tile_count==n and cost==534378 and all(coverage)
COUNTS['tiling_entries_covered_exactly_once']=len(coverage)
COUNTS['rank_one_tiles']=tile_count

dump('TARGET_EXACT_CERTIFICATES.json',CERTIFICATES)
dump('RESULTS.json',{
    'status':'PASS', 'counts':dict(COUNTS), 'seconds':round(time.monotonic()-START,3),
    'ordered_prime_pairs':PAIRS, 'target':{'N':n,'D':D,'E2':E2,'side_cutoff':B,
       'density_floor':'29/442','higher_rank_area_penalty':'5/5746','optimum':cost,
       'scalar_relaxation_minimum':str(scalar_min),'scalar_relaxation_minimizers':scalar_argmin},
    'method':'New integer cyclotomic remainder evaluator in characteristic zero; direct SymPy determinant crosschecks.',
    'historical_checkers_imported_or_executed':False,'external_writes':False,
    'finite_controls_are_not_a_universal_proof':True,
})
print((OUT/'RESULTS.json').read_text())
