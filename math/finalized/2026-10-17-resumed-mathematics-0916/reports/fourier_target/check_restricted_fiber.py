#!/usr/bin/env python3
"""Fresh exact checks for the inverse-cyclic-tridiagonal Fourier obstruction.

Uses only Python's standard library. Historical programs are not imported.
The general-N result is proved in REPORT.md; this program verifies the pinned
F8 certificate, all 70 four-frequency choices, and a nonvacuity witness.
"""
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
import json

ZERO = (Fraction(0),) * 4
ONE = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
Z = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))

def const(n):
    return (Fraction(n), Fraction(0), Fraction(0), Fraction(0))

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def neg(a):
    return tuple(-x for x in a)

def sub(a, b):
    return add(a, neg(b))

def mul(a, b):
    c = [Fraction(0)] * 7
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i + j] += ai * bj
    for k in range(6, 3, -1):
        c[k - 4] -= c[k]
    return tuple(c[:4])

def prod(xs):
    out = ONE
    for x in xs:
        out = mul(out, x)
    return out

def power(a, n):
    out = ONE
    for _ in range(n):
        out = mul(out, a)
    return out

def det(M):
    n = len(M)
    out = ZERO
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = prod(M[i][p[i]] for i in range(n))
        out = add(out, neg(term) if inversions % 2 else term)
    return out

def polynomial_with_roots(roots):
    coefficients = [ONE]
    for root in roots:
        nxt = [ZERO] * (len(coefficients) + 1)
        for j, coefficient in enumerate(coefficients):
            nxt[j] = sub(nxt[j], mul(root, coefficient))
            nxt[j + 1] = add(nxt[j + 1], coefficient)
        coefficients = nxt
    return coefficients

def encode(a):
    return [str(v) for v in a]

def main():
    z = [power(Z, k) for k in range(8)]
    assert power(Z, 4) == neg(ONE) and power(Z, 8) == ONE
    assert all(z[i] != z[j] for i in range(8) for j in range(i))
    a = add(add(ONE, z[1]), z[7])
    assert a != ZERO
    Q = []
    null_checks = 0
    for k in range(8):
        support = [(k - 1) % 8, k, (k + 1) % 8]
        q = polynomial_with_roots([z[s] for s in support])
        translated = [neg(z[(3 * k) % 8]), mul(a, z[(2 * k) % 8]), neg(mul(a, z[k])), ONE]
        assert q == translated
        Q.append(q)
        for s in support:
            dot = ZERO
            for r in range(4):
                dot = add(dot, mul(q[r], z[((4 + r) * s) % 8]))
            assert dot == ZERO
            null_checks += 1
        # Consecutive first three rows of the four-row restriction already inject.
        minor = [[z[(r * s) % 8] for s in support] for r in [4, 5, 6]]
        assert det(minor) != ZERO

    four_frequency_checks = []
    for ks in combinations(range(8), 4):
        determinant = det([Q[k] for k in ks])
        vandermonde = prod(sub(z[ks[j]], z[ks[i]]) for i in range(4) for j in range(i + 1, 4))
        assert determinant == mul(mul(a, a), vandermonde)
        assert determinant != ZERO
        four_frequency_checks.append({'frequencies': list(ks), 'determinant': encode(determinant)})

    p = [7, 0, 6, 3, 4, 1, 2, 5]
    inverse_p = [p.index(j) for j in range(8)]
    ks = inverse_p[:4]
    assert ks == [1, 5, 6, 3]
    pinned_Q = [Q[k] for k in ks]
    pinned_det = det(pinned_Q)
    expected = tuple(map(Fraction, [-12, 12, 28, 28]))
    assert pinned_det == expected
    inverse_certificate = tuple(map(Fraction, ['-5/8', '1/4', '1/4', '-5/8']))
    assert mul(pinned_det, inverse_certificate) == ONE
    # Field norm from the rational matrix of multiplication by pinned_det.
    basis = [power(Z, j) for j in range(4)]
    multiplication_matrix = [[const(mul(pinned_det, basis[j])[i]) for j in range(4)] for i in range(4)]
    assert det(multiplication_matrix) == const(2048)

    # A genuine separated-generator stage with an invertible tridiagonal inverse.
    C = [[Fraction(2 if i == j else -1 if abs(i - j) == 1 else 0) for j in range(8)] for i in range(8)]
    A = [[Fraction((min(i, j) + 1) * (8 - max(i, j)), 9) for j in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            assert sum(C[i][k] * A[k][j] for k in range(8)) == (i == j)
            if i > j:
                assert A[i][j] == Fraction(8 - i, 9) * (j + 1)
            elif i < j:
                assert A[i][j] == Fraction(i + 1, 9) * (8 - j)

    # The inverse-tridiagonal restriction is not implied by the source chart.
    A_general = [[Fraction(1 + (i == j)) for j in range(8)] for i in range(8)]
    C_general = [[Fraction(i == j) - Fraction(1, 9) for j in range(8)] for i in range(8)]
    for i in range(8):
        for j in range(8):
            assert sum(A_general[i][k] * C_general[k][j] for k in range(8)) == (i == j)
    assert C_general[0][2] == -Fraction(1, 9)

    results = {
        'status': 'PASS: restricted inverse-cyclic-tridiagonal obstruction only',
        'unrestricted_target_fiber': 'UNSOLVED',
        'field': 'Q[z]/(z^4+1)',
        'coefficient_encoding': 'ascending powers [1,z,z^2,z^3], exact rational strings',
        'permutation': p,
        'selected_inverse_columns': ks,
        'selected_supports': [[(k - 1) % 8, k, (k + 1) % 8] for k in ks],
        'annihilator_rows': [[encode(v) for v in row] for row in pinned_Q],
        'annihilator_determinant': encode(pinned_det),
        'determinant_inverse_certificate': encode(inverse_certificate),
        'determinant_norm': 2048,
        'annihilator_dot_checks': null_checks,
        'injective_four_by_three_maps_checked': 8,
        'four_frequency_choices_checked': len(four_frequency_checks),
        'all_four_frequency_determinants': four_frequency_checks,
        'nonvacuity_witness': 'C=tridiag(-1,2,-1), A_ij=(min(i,j)+1)(8-max(i,j))/9; CA=I exactly',
        'restriction_is_strict_witness': 'A=I+J belongs to the source chart; A^-1=I-J/9 has nonzero (0,2) entry and is not cyclic tridiagonal',
        'historical_programs_run': False,
        'numerical_fitting_used': False,
    }
    out = Path(__file__).with_name('RESULTS.json')
    out.write_text(json.dumps(results, indent=2) + '\n')
    print('PASS: exact pinned determinant, inverse and norm; 70 Vandermonde cases; 8 injection checks; nonvacuity witness.')
    print('Restricted theorem only. The unrestricted F8 target-fiber ideal remains undecided.')

if __name__ == '__main__':
    main()
