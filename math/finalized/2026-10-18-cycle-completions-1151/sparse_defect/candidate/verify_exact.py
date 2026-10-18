#!/usr/bin/env python3
"""Exact controls for the M-SPARSE-DEFECT candidate; newly authored, no historical imports."""
from itertools import permutations
from pathlib import Path
from collections import Counter
import hashlib
import json
import sympy as sp

BASE = Path(__file__).resolve().parent
x = sp.Symbol('x')


def retained(n):
    if n < 2 or n % 2:
        raise ValueError('Half-density constructor requires even N >= 2')
    m = n // 2
    return [[(i < m and j % 2 == 0) or (i >= m and j % 2 == 1)
             for j in range(n)] for i in range(n)]


def ring_gram(n, mask, column=False, corruption=None):
    """Return exact cyclotomic remainder entries of H H* or H* H.

    H_ij = mask_ij * x^(ij); conjugation x -> x^(-1).
    Optional corruption multiplies one coefficient by a rational integer.
    """
    phi = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.QQ)
    basis = [sp.rem(sp.Poly(x**e, x), phi) for e in range(n)]
    out = []
    for i in range(n):
        row = []
        for j in range(n):
            coeffs = Counter()
            for k in range(n):
                ia, ib = ((k, i), (k, j)) if column else ((i, k), (j, k))
                if mask[ia[0]][ia[1]] and mask[ib[0]][ib[1]]:
                    ca = corruption[2] if corruption and ia == corruption[:2] else 1
                    cb = corruption[2] if corruption and ib == corruption[:2] else 1
                    exponent = ((j - i) * k if column else (i - j) * k) % n
                    coeffs[exponent] += ca * cb
            value = sp.Poly(0, x, domain=sp.QQ)
            for e, c in coeffs.items():
                value += c * basis[e]
            row.append(sp.rem(value, phi))
        out.append(row)
    return out


def gram_is_scalar(g, scalar):
    return all(g[i][j] == sp.Poly(scalar if i == j else 0, x, domain=sp.QQ)
               for i in range(len(g)) for j in range(len(g)))


def half_controls():
    rows = []
    for n in range(2, 33, 2):
        h = retained(n)
        e = [[not v for v in row] for row in h]
        checks = {
            'retained_row_support': all(sum(row) == n//2 for row in h),
            'retained_column_support': all(sum(h[i][j] for i in range(n)) == n//2 for j in range(n)),
            'retained_HHstar': gram_is_scalar(ring_gram(n, h), n//2),
            'retained_HstarH': gram_is_scalar(ring_gram(n, h, column=True), n//2),
            'residual_EEstar': gram_is_scalar(ring_gram(n, e), n//2),
            'residual_EstarE': gram_is_scalar(ring_gram(n, e, column=True), n//2),
        }
        assert all(checks.values()), (n, checks)
        # Since normalized M=H/sqrt(N) and H H*=m I,
        # M^-1=(sqrt(N)/m)H*. Its support counts are the transposed H counts.
        rows.append({'N': n, 's': n//2, 'checks': checks,
                     'normalized_MMstar': 'I/2', 'normalized_error_gram': 'I/2',
                     'inverse_support_per_row_and_column': n//2})
    return rows


def singleton_controls():
    rows = []
    for n in range(2, 9):
        tested = passing = 0
        for sigma in permutations(range(n)):
            tested += 1
            ok = n % 2 == 0 and all(
                ((k-l)*(sigma[k]-sigma[l])) % n == n//2
                for k in range(n) for l in range(k)
            )
            passing += bool(ok)
        assert passing == (2 if n == 2 else 0)
        rows.append({'N': n, 'support_permutations_tested': tested,
                     'passing_necessary_equality_congruences': passing})
    return rows


def three_controls():
    w = -sp.Rational(1,2) - sp.I*sp.sqrt(3)/2
    F = sp.Matrix(3, 3, lambda i,j: sp.simplify(w**(i*j)/sp.sqrt(3)))
    D = sp.diag(1,w,w)
    C = sp.simplify(D*F*D)
    expected = ((1-w)*sp.eye(3)+w*sp.ones(3))/sp.sqrt(3)
    l0 = -sp.I
    l1 = sp.sqrt(3)/2 + sp.I/2
    c = (l0+l1)/2
    M = c*D
    E = sp.simplify(F-M)
    checks = {
        'circulant_identity': sp.simplify(C-expected) == sp.zeros(3),
        'lambda0': sp.simplify((1+2*w)/sp.sqrt(3)-l0) == 0,
        'lambda1': sp.simplify((1-w)/sp.sqrt(3)-l1) == 0,
        'squared_eigenvalue_distance': sp.simplify((l0-l1)*sp.conjugate(l0-l1)) == 3,
        'midpoint_nonzero': sp.simplify(c*sp.conjugate(c)) == sp.Rational(1,4),
        'witness_error_gram': sp.simplify(E*E.conjugate().T) == sp.Rational(3,4)*sp.eye(3),
        'witness_condition_one': sp.simplify(M*M.conjugate().T) == sp.Rational(1,4)*sp.eye(3),
        'six_affine_permutations': len({tuple((a*i+b)%3 for i in range(3)) for a in [1,2] for b in range(3)}) == 6,
    }
    assert all(checks.values()), checks
    return checks


def negative_controls():
    rejected = []
    for n in [0,1,3,5,9]:
        try:
            retained(n)
        except ValueError:
            rejected.append(n)
    assert rejected == [0,1,3,5,9]
    n=8
    h=retained(n)
    corrupted = not gram_is_scalar(ring_gram(n,h,corruption=(0,0,2)), n//2)
    singular = [[j%2==0 for j in range(n)] for i in range(n)]
    singular_fails = not gram_is_scalar(ring_gram(n,singular), n//2)
    # Its odd columns vanish, an independent exact singularity certificate.
    singular_zero_columns = [j for j in range(n) if not any(singular[i][j] for i in range(n))]
    assert corrupted and singular_fails and singular_zero_columns == [1,3,5,7]
    return {'invalid_half_lengths_rejected':rejected,
            'corrupted_entry_rejected':corrupted,
            'repeated_column_mask_rejected':singular_fails,
            'repeated_column_mask_zero_columns':singular_zero_columns}


def main():
    result = {'stable_id':'M-SPARSE-DEFECT',
              'proof_scope':'Half-density all even N; singleton strict nonsharpness all N>=3; exact singleton N=3',
              'method':'Exact arithmetic in Q[x]/Phi_N(x), integer congruences, symbolic Q(sqrt(3),i)',
              'half_density':half_controls(),
              'singleton':singleton_controls(),
              'exact_three':three_controls(),
              'negative_controls':negative_controls()}
    result['all_passed'] = True
    result['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (BASE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_passed':True,
                      'even_lengths':[r['N'] for r in result['half_density']],
                      'singleton_permutations':sum(r['support_permutations_tested'] for r in result['singleton']),
                      'output':str(BASE/'RESULTS.json')}))

if __name__ == '__main__':
    main()
