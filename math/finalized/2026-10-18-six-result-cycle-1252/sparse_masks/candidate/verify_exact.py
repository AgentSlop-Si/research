#!/usr/bin/env python3
"""Fresh exact controls for the simultaneous Fourier-mask equality criterion.

No historical checker is imported. Requires Python 3 and SymPy. No floating point.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import math
import sympy as sp
from sympy.polys.domains import QQ

BASE = Path(__file__).resolve().parent
x = sp.Symbol('x')


@lru_cache(None)
def roots(n):
    phi = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.ZZ)
    deg = phi.degree()
    out = []
    for e in range(n):
        rem = sp.rem(sp.Poly(x**e, x, domain=sp.ZZ), phi)
        out.append(tuple(int(rem.nth(k)) for k in range(deg)))
    return tuple(out)


def zero_sum(n, exponents):
    basis = roots(n)
    result = [0] * len(basis[0])
    for e, multiplicity in Counter(e % n for e in exponents).items():
        for k, v in enumerate(basis[e]):
            result[k] += multiplicity * v
    return not any(result)


def mask_for_divisor(n, d):
    if n < 2 or d < 1 or d >= n or n % d:
        raise ValueError('Require N>=2 and a positive proper divisor d of N')
    m = n // d
    return [[i // d == j % m for j in range(n)] for i in range(n)]


def exact_gram(n, left, right=None, column=True):
    """Gram or mixed product for entries coefficient_ij * z^(ij).

    column=True returns left* right; otherwise left right*.
    Coefficients are real integers and can encode corruptions.
    """
    right = left if right is None else right
    basis = roots(n)
    deg = len(basis[0])
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            count = Counter()
            for k in range(n):
                if column:
                    coefficient = int(left[k][i]) * int(right[k][j])
                    exponent = (k * (j-i)) % n
                else:
                    coefficient = int(left[i][k]) * int(right[j][k])
                    exponent = (k * (i-j)) % n
                if coefficient:
                    count[exponent] += coefficient
            value = [0] * deg
            for e, c in count.items():
                for h, v in enumerate(basis[e]):
                    value[h] += c*v
            row.append(tuple(value))
        out.append(row)
    return out


def scalar_gram(g, scalar):
    n = len(g)
    return all(v == ((scalar if i == j else 0),) + (0,)*(len(v)-1)
               for i, row in enumerate(g) for j, v in enumerate(row))


def support_counts(mask):
    n = len(mask)
    return ([sum(bool(v) for v in row) for row in mask],
            [sum(bool(mask[i][j]) for i in range(n)) for j in range(n)])


def divisor_controls():
    tested = []
    dimensions = list(range(2, 37)) + [40, 42, 48, 50, 60, 64]
    for n in dimensions:
        full = [[True]*n for _ in range(n)]
        for d in range(1, n):
            if n % d:
                continue
            c = mask_for_divisor(n, d)
            a = [[not v for v in row] for row in c]
            rows, cols = support_counts(c)
            arows, acols = support_counts(a)
            checks = {
                'omitted_row_support': rows == [d]*n,
                'omitted_column_support': cols == [d]*n,
                'inverse_row_support': acols == [n-d]*n,
                'inverse_column_support': arows == [n-d]*n,
                'omitted_CstarC': scalar_gram(exact_gram(n,c), d),
                'omitted_CCstar': scalar_gram(exact_gram(n,c,column=False), d),
            }
            # In the unnormalized notation W=sqrt(N)F and H=sqrt(N)A:
            # sI - H*W - W*H + H*H = 0.
            aw = exact_gram(n,a,full)
            wa = exact_gram(n,full,a)
            aa = exact_gram(n,a)
            identity = True
            for i in range(n):
                for j in range(n):
                    for k in range(len(roots(n)[0])):
                        value = -aw[i][j][k]-wa[i][j][k]+aa[i][j][k]
                        if k == 0 and i == j:
                            value += n-d
                        identity &= value == 0
            checks['retained_equality_identity'] = identity
            assert all(checks.values()), (n,d,checks)
            tested.append({'N':n,'d':d,'s':n-d,'squared_optimum':f'{d}/{n}',
                           'checks':checks})
    return tested


def field_matrix_inverse(a, K):
    n = len(a)
    work = [list(row)+[K.one if i == j else K.zero for j in range(n)]
            for i,row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j,n) if work[i][j] != K.zero),None)
        if pivot is None:
            raise ValueError('Singular exact matrix')
        work[j], work[pivot] = work[pivot], work[j]
        value = work[j][j]
        work[j] = [v/value for v in work[j]]
        for i in range(n):
            if i != j and work[i][j] != K.zero:
                factor = work[i][j]
                work[i] = [v-factor*w for v,w in zip(work[i],work[j])]
    return [row[n:] for row in work]


def multiply(a,b,K):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),K.zero)
             for j in range(len(b[0]))] for i in range(len(a))]


def scalar_matrix(a,c,K):
    return all(a[i][j] == (K.convert(c) if i == j else K.zero)
               for i in range(len(a)) for j in range(len(a)))


def field_witness(n,d,negative=False):
    # Any primitive root realizes the same algebraic identities. Complex
    # conjugation is represented exactly by z -> z^(-1), independent of which
    # conjugate CRootOf uses as its embedding.
    alpha = sp.CRootOf(sp.cyclotomic_poly(n,x),0)
    K = QQ.algebraic_field(alpha)
    z = K.convert(alpha)
    basis = [z**e for e in range(n)]
    zbar = basis[-1]

    def conjugate(v):
        out = K.zero
        for coefficient in v.to_list():
            out = out*zbar + K.convert(coefficient)
        return out

    def adjoint(a):
        return [[conjugate(a[j][i]) for j in range(len(a))]
                for i in range(len(a[0]))]

    mask = mask_for_divisor(n,d)
    W = [[basis[(i*j)%n] for j in range(n)] for i in range(n)]
    H = [[K.zero if mask[i][j] else W[i][j] for j in range(n)] for i in range(n)]
    Hstar = adjoint(H)
    s = n-d
    inverse = field_matrix_inverse(Hstar,K)
    Z = [[s*v for v in row] for row in inverse]  # Z = sqrt(N) M.
    error = [[Z[i][j]-W[i][j] for j in range(n)] for i in range(n)]
    checks = {
        'Z_Hstar_equals_sI':scalar_matrix(multiply(Z,Hstar,K),s,K),
        'Hstar_Z_equals_sI':scalar_matrix(multiply(Hstar,Z,K),s,K),
        'error_left_gram_equals_dI':scalar_matrix(multiply(error,adjoint(error),K),d,K),
        'error_right_gram_equals_dI':scalar_matrix(multiply(adjoint(error),error,K),d,K),
        'inverse_row_support':all(sum(v != K.zero for v in row)==s for row in Hstar),
        'inverse_column_support':all(sum(Hstar[i][j] != K.zero for i in range(n))==s for j in range(n)),
    }
    assert all(checks.values()),(n,d,checks)
    out = {'N':n,'d':d,'s':s,'checks':checks}
    if negative:
        assert (n,d)==(3,1)
        # M=A has the right error, but its inverse is dense: this must NOT
        # be accepted merely because the retained mask itself is sparse.
        naive_inverse = field_matrix_inverse(H,K)
        inverse_counts = [sum(v != K.zero for v in row) for row in naive_inverse]
        wrong_error = [[2*Z[i][j]-W[i][j] for j in range(n)] for i in range(n)]
        wrong_scale_rejected = not scalar_matrix(multiply(wrong_error,adjoint(wrong_error),K),d,K)
        assert inverse_counts == [3]*3 and wrong_scale_rejected
        out['negative_controls'] = {
            'naive_retained_mask_inverse_counts':inverse_counts,
            'naive_retained_mask_rejected_by_simultaneous_inverse_budget':True,
            'wrong_witness_gain_rejected':wrong_scale_rejected,
        }
    return out


def exhaustive_small_masks():
    out = []
    for n in range(2,6):
        for w in range(1,n):
            subsets = list(combinations(range(n),w))
            total = regular = passing = 0
            for column_supports in product(subsets,repeat=n):
                total += 1
                rowcounts = [0]*n
                for support in column_supports:
                    for i in support:
                        rowcounts[i] += 1
                if rowcounts != [w]*n:
                    continue
                regular += 1
                valid = True
                for j in range(n):
                    for k in range(j):
                        overlap = set(column_supports[j]) & set(column_supports[k])
                        if not zero_sum(n, [r*(j-k) for r in overlap]):
                            valid = False
                            break
                    if not valid:
                        break
                passing += valid
            if w == 1:
                assert passing == math.factorial(n)
            elif n in [3,5] or (n==4 and w==3):
                assert passing == 0
            else:
                assert (n,w)==(4,2) and passing>0
            out.append({'N':n,'omitted_weight':w,'s':n-w,
                        'all_fixed_column_weight_masks':total,
                        'also_row_regular_masks':regular,
                        'passing_exact_criterion':passing})
    return out


def root_sum_controls():
    primes = []
    for p in [2,3,5,7,11,13]:
        examined = vanished = 0
        for weight in range(1,p):
            for support in combinations(range(p),weight):
                examined += 1
                vanished += zero_sum(p,support)
        assert vanished == 0
        primes.append({'p':p,'proper_nonempty_subsets':examined,'vanishing':vanished})
    odds = []
    for n in range(3,62,2):
        pairs = list(combinations(range(n),2))
        vanished = sum(zero_sum(n,pair) for pair in pairs)
        assert vanished == 0
        odds.append({'N':n,'two_root_subsets':len(pairs),'vanishing':vanished})
    return {'prime_subset_sums':primes,'odd_two_root_sums':odds}


def negative_controls():
    bad = [(1,1),(2,0),(2,2),(5,2),(6,4),(0,1),(-1,1)]
    for n,d in bad:
        try:
            mask_for_divisor(n,d)
        except ValueError:
            continue
        raise AssertionError(('invalid_divisor_accepted',n,d))
    n,d=6,2
    c = mask_for_divisor(n,d)
    corrupted = [[int(v) for v in row] for row in c]
    corrupted[0][0]=2
    corrupted_rejected = not scalar_gram(exact_gram(n,corrupted),d)
    repeated_row = [[i==0 for _ in range(5)] for i in range(5)]
    row_norm_only_rejected = not scalar_gram(exact_gram(5,repeated_row),1)
    assert corrupted_rejected and row_norm_only_rejected
    return {'invalid_divisor_inputs_rejected':bad,
            'corrupted_phase_coefficient_rejected':corrupted_rejected,
            'right_column_norms_wrong_cross_gram_rejected':row_norm_only_rejected}


def source_checks():
    binding = json.loads((BASE/'SOURCE_BINDINGS.json').read_text())
    for item in binding['copied_sources']:
        path = BASE/item['copy']
        data = path.read_bytes()
        assert len(data)==item['bytes']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
    return {'copied_source_count':len(binding['copied_sources']),'all_hashes_match':True}


def main():
    result = {
        'stable_id':'M-SPARSE-DEFECT',
        'method':'Exact cyclotomic quotient arithmetic and exact algebraic-field inverses; no floats',
        'source_checks_before':source_checks(),
        'divisor_masks':divisor_controls(),
        'explicit_inverse_witnesses':[field_witness(n,d,negative=(n,d)==(3,1))
            for n,d in [(2,1),(3,1),(4,1),(4,2),(5,1),(6,1),(6,2),(6,3),
                        (8,1),(8,2),(8,4),(9,3),(10,2),(12,3),(12,4)]],
        'exhaustive_small_masks':exhaustive_small_masks(),
        'root_sum_controls':root_sum_controls(),
        'negative_controls':negative_controls(),
        'source_checks_after':source_checks(),
    }
    result['all_passed']=True
    result['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (BASE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_passed':True,'divisor_cases':len(result['divisor_masks']),
                      'explicit_inverse_cases':len(result['explicit_inverse_witnesses']),
                      'exhaustive_masks':sum(r['all_fixed_column_weight_masks'] for r in result['exhaustive_small_masks']),
                      'exact_mask_pass_counts':[(r['N'],r['omitted_weight'],r['passing_exact_criterion']) for r in result['exhaustive_small_masks']],
                      'output':str(BASE/'RESULTS.json')}))


if __name__=='__main__':
    main()
