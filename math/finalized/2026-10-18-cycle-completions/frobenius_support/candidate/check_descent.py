#!/usr/bin/env python3
"""Fresh, standard-library controls for the N13 stable-support descent theorem.

No inherited scientific program is imported or executed. Gaussian coefficients
are constructed by their additive Pascal recurrence. The finite census is a
regression of an accepted premise, not claimed as new research completion.
"""
import hashlib
import json
from collections import Counter
from functools import cache
from pathlib import Path

P, Q, N = 53, 16, 13
ROOT = Path(__file__).resolve().parent


def binomial(n, k, omega):
    row = [1]
    for m in range(1, n + 1):
        row = [1] + [
            ((row[j] if j < len(row) else 0)
             + pow(omega, m-j, P) * row[j-1]) % P
            for j in range(1, m)
        ] + [1]
    return row[k]


@cache
def gaussian(epsilon, delta, a, b):
    r, ell = epsilon*a % N, delta*b % N
    if r + ell >= N:
        return 0
    return binomial(r+ell, ell, pow(Q, epsilon*delta % N, P))


@cache
def moment_coefficients(a, b):
    denominator = gaussian(1, 1, a, b)
    isolated = gaussian(-1, 1, N-b, b)
    assert denominator and isolated
    u = pow(Q, 10*(a+b)**2 % N, P) * pow(denominator, -1, P) % P
    v = gaussian(-1, 1, a, b) * pow(denominator*isolated % P, -1, P) % P
    return u, v, N-a-b


def moment(a, b, y):
    u, v, exponent = moment_coefficients(a, b)
    return (u - v*pow(y, exponent, P)) % P


def solve_square(matrix, rhs):
    size = len(matrix)
    rows = [list(row)+[value] for row, value in zip(matrix, rhs)]
    for j in range(size):
        pivot = next((i for i in range(j, size) if rows[i][j]), None)
        assert pivot is not None, (j, rows)
        rows[j], rows[pivot] = rows[pivot], rows[j]
        inv = pow(rows[j][j], -1, P)
        rows[j] = [x*inv % P for x in rows[j]]
        for i in range(size):
            if i != j:
                factor = rows[i][j]
                rows[i] = [(x-factor*y) % P for x, y in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def evaluate(coefficients, value):
    out = 0
    for coefficient in reversed(coefficients):
        out = (out*value+coefficient) % P
    return out


def main():
    assert pow(Q, N, P) == 1 and Q != 1
    gaussian_table = {
        (e, d, a, b): gaussian(e, d, a, b)
        for e in (1, -1) for d in (1, -1)
        for a in range(N) for b in range(N)
    }
    reflection_checks = 0
    for (e, d, a, b), value in gaussian_table.items():
        assert value == gaussian_table[-e, -d, -a % N, -b % N]
        assert pow(Q, 10*(a+b)**2 % N, P) == pow(Q, 10*((-a % N)+(-b % N))**2 % N, P)
        reflection_checks += 1

    # Coefficientwise last-window identity: P_h(Y)=sum u_j h_j
    # - sum v_j h_j Y^(8-j), for j=0,...,7 and h_7=1.
    terms = [moment_coefficients(a, 1) for a in range(4, 12)]
    u, v, degrees = [list(x) for x in zip(*terms)]
    assert degrees == list(range(8, 0, -1))
    assert all(v)
    leading_factor = -v[0] % P
    # Every legal nonzero constant coefficient has a nonzero leading term.
    assert all(leading_factor*h0 % P for h0 in range(1, P))

    windows = [(1,1), (1,2), (1,3), (1,4), (2,2), (2,3)]
    census, histogram = [], Counter()
    polynomial_identity_checks = 0
    for y in range(1, P):
        rows = [[moment(a+j, b, y) for j in range(8)] for b, a in windows]
        first_six = [row[:6] for row in rows]
        particular = solve_square(first_six, [-row[7] % P for row in rows])
        direction = solve_square(first_six, [-row[6] % P for row in rows])
        for lam in range(P):
            h = [(a+lam*b) % P for a, b in zip(particular, direction)] + [lam, 1]
            assert all(sum(x*z for x, z in zip(row, h)) % P == 0 for row in rows)
            polynomial = [0]*9
            polynomial[0] = sum(a*b for a, b in zip(u, h)) % P
            for j in range(8):
                polynomial[8-j] = -v[j]*h[j] % P
            for test_y in range(P):
                direct = sum(h[j]*moment(4+j, 1, test_y) for j in range(8)) % P
                assert evaluate(polynomial, test_y) == direct
                polynomial_identity_checks += 1
            assert evaluate(polynomial, y) == 0
            if h[0]:
                assert polynomial[8] != 0
            roots = [x for x in range(1, P) if evaluate(h, x) == 0]
            histogram[len(roots)] += 1
            assert len(roots) <= 6
            census.append({"y": y, "lambda": lam, "H": h, "nonzero_roots": roots})

    # A mutation h0=0 really destroys the degree-eight certificate: the
    # hypothesis is necessary and not silently supplied by the checker.
    mutant_h = [0, 1, 0, 0, 0, 0, 0, 1]
    mutant = [0]*9
    mutant[0] = sum(a*b for a, b in zip(u, mutant_h)) % P
    for j in range(8):
        mutant[8-j] = -v[j]*mutant_h[j] % P
    assert mutant[8] == 0 and mutant[7] != 0

    receipt = {
        "status": "PASS",
        "source_execution": "Fresh checker only; inherited programs not executed or imported",
        "new_gate": "One-sided prime-Frobenius-stable degree-seven support obstruction for gcd(d,210)=1",
        "last_b1_window": {"a": [4,11], "u": u, "v": v, "Y_degrees": degrees,
                           "leading_coefficient": f"{leading_factor}*h0 modulo 53"},
        "reflection_identities": reflection_checks,
        "accepted_base_field_premise_regression": {
            "y_values": 52, "lambda_values": 53, "polynomials": len(census),
            "nonzero_root_evaluations": len(census)*52,
            "root_count_histogram": dict(sorted(histogram.items())),
            "maximum_distinct_nonzero_roots": max(histogram),
            "new_completion_credit": False,
        },
        "last_window_scalar_identity_controls": polynomial_identity_checks,
        "zero_constant_mutation": "Detected; degree drops from eight to seven",
        "all_degree_claim": "Proved in REPORT.md by orbit length and finite-field degree; not inferred from a finite degree census",
        "failures": 0,
    }
    (ROOT/'BASEFIELD_PREMISE_REGRESSION.json').write_text(json.dumps(census, indent=2)+'\n')
    (ROOT/'CHECK_RESULT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
