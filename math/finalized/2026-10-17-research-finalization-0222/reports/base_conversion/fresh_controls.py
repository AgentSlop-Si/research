#!/usr/bin/env python3
"""Fresh exact-oracle controls; no imports from historical/candidate programs.

This is not a bit-cost benchmark or a proof of asymptotic bounds.
"""
from fractions import Fraction
from itertools import product
from math import factorial, comb, log2
from random import Random
import hashlib
import json
from pathlib import Path


def ceil_log2(n):
    assert n >= 1
    return (n - 1).bit_length()


def poly_linear(a, root):
    out = [0] * (len(a) + 1)
    for i, value in enumerate(a):
        out[i] -= root * value
        out[i + 1] += value
    return out


def prepare(M):
    r = 2 * M - 1
    ell = ceil_log2(r)
    K = (r - 1) * (ell + 1) + 1
    D = factorial(r - 1)
    columns = []
    for t in range(r):
        a = [1]
        for j in range(r):
            if j != t:
                a = poly_linear(a, j)
        scale = (-1) ** (r - 1 - t) * comb(r - 1, t)
        a = [scale * value for value in a]
        assert all(abs(value) < 1 << K for value in a)
        # Independently evaluate the claimed scaled Lagrange polynomial.
        for s in range(r):
            assert sum(value * s ** k for k, value in enumerate(a)) == (D if s == t else 0)
        columns.append(a)
    assert D.bit_length() <= K
    return r, ell, K, D, columns


def convolution(x, y):
    out = [0] * (len(x) + len(y) - 1)
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            out[i + j] += a * b
    return out


def kernel(x, y, R, prepared):
    M = len(x)
    r, ell, K, D, columns = prepared
    h = (R - 1).bit_length()
    H = h + ceil_log2(M) + (M - 1) * ell + 1
    B = 2 * H + K + ceil_log2(r) + 2
    u = [sum(a * t ** i for i, a in enumerate(x)) for t in range(r)]
    v = [sum(a * t ** i for i, a in enumerate(y)) for t in range(r)]
    assert all(0 <= z < 1 << H for z in u + v)
    z = [a * b for a, b in zip(u, v)]
    b = [sum(columns[t][k] * z[t] for t in range(r)) for k in range(r)]
    assert all(abs(value) < 1 << B for value in b)
    assert all(value % D == 0 for value in b)
    result = [value // D for value in b]
    assert result == convolution(x, y)
    assert all(0 <= a <= M * (R - 1) ** 2 for a in result)
    return result, H, B


def rank(a):
    a = [[Fraction(v) for v in row] for row in a]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        scale = a[row][col]
        a[row] = [v / scale for v in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                scale = a[i][col]
                a[i] = [v - scale * w for v, w in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def digit_oracle(value, base, length):
    result = []
    for _ in range(length):
        value, digit = divmod(value, base)
        result.append(digit)
    assert value == 0
    return result


def reconstruct_p(digits, m, d):
    out = 0
    for digit in reversed(digits):
        for _ in range(d):
            out = (out << m) - out
        out += digit
    return out


def pipeline(X, Y, m, d, M, prepared):
    p = (1 << m) - 1
    Q = p ** d
    R = Q ** M
    xq = digit_oracle(X, Q, M * M)
    yq = digit_oracle(Y, Q, M * M)
    assert reconstruct_p(xq, m, d) == X
    assert reconstruct_p(yq, m, d) == Y
    xb = [reconstruct_p(xq[i * M:(i + 1) * M], m, d) for i in range(M)]
    yb = [reconstruct_p(yq[i * M:(i + 1) * M], m, d) for i in range(M)]
    s, H, B = kernel(xb, yb, R, prepared)
    result = reconstruct_p(s, m, d * M)
    assert result == X * Y
    assert result.bit_length() <= 2 * d * m * M * M
    # This equality shows that a scalar-output bilinear map has rank one.
    assert sum(a * R ** i for i, a in enumerate(xb)) * sum(b * R ** j for j, b in enumerate(yb)) == result
    return H, B


def main():
    rng = Random(202610170216)
    counts = {"flattening_rank_checks": 0, "interpolation_table_checks": 0,
              "exhaustive_pipelines": 0, "boundary_random_pipelines": 0,
              "parameter_bounds": 0, "capacity_wrappers": 0, "negative_controls": 0}
    rank_rows = []
    for M in range(2, 17):
        r, ell, K, D, columns = prepare(M)
        mat = [[int(i + j == k) for i in range(M) for j in range(M)] for k in range(r)]
        actual = rank(mat)
        assert actual == r
        counts["flattening_rank_checks"] += 1
        counts["interpolation_table_checks"] += 1
        rank_rows.append({"M": M, "full_coefficient_rank": actual, "scalar_output_rank": 1})

    m, d, M = 2, 1, 2
    prep = prepare(M)
    capacity = ((1 << m) - 1) ** (d * M * M)
    for X, Y in product(range(capacity), repeat=2):
        pipeline(X, Y, m, d, M, prep)
        counts["exhaustive_pipelines"] += 1

    parameter_rows = []
    for m, d, M in product([2, 3, 4, 5, 7], [1, 2, 3], [2, 3, 4, 5, 8]):
        p = (1 << m) - 1
        Q = p ** d
        R = Q ** M
        cap = R ** M
        prep = prepare(M)
        cases = [(0, 0), (0, cap - 1), (1, cap - 1), (cap - 1, cap - 1),
                 (Q - 1, Q), (R - 1, R), (cap // 2, cap // 3)]
        cases += [(rng.randrange(cap), rng.randrange(cap)) for _ in range(12)]
        for X, Y in cases:
            H, B = pipeline(X, Y, m, d, M, prep)
            counts["boundary_random_pipelines"] += 1
        # Exact integer guards behind the real-log analysis.
        C = d * m * M * M
        assert 1 << (d * (m - 1) * M * M) <= cap < 1 << C
        assert (R - 1).bit_length() >= M
        assert C * C // m == C * d * M * M
        n = M * M * d * log2(p)
        h0 = n / M
        rho0 = (2 - 1 / M) * log2(h0) / log2(n)
        assert rho0 + 1e-12 >= 1 - 1 / (2 * M)
        counts["parameter_bounds"] += 1
        parameter_rows.append({"m": m, "d": d, "M": M, "N": (cap - 1).bit_length(),
                               "h": (R - 1).bit_length(), "H": H, "B": B,
                               "rho0_diagnostic_only": rho0})

    for m in range(2, 10):
        for d in range(1, 5):
            for A in range(d * m, 257, 11):
                required = (A + d * (m - 1) - 1) // (d * (m - 1))
                M = 2
                while M * M < required:
                    M *= 2
                assert M * M < 4 * required
                assert ((1 << m) - 1) ** (d * M * M) >= 1 << A
                counts["capacity_wrappers"] += 1

    # Missing exact division gives wrong coefficients.
    r, ell, K, D, cols = prepare(3)
    x = [1, 2, 3]
    y = [4, 5, 6]
    values = [sum(a * t ** i for i, a in enumerate(x)) * sum(b * t ** j for j, b in enumerate(y)) for t in range(r)]
    scaled = [sum(cols[t][k] * values[t] for t in range(r)) for k in range(r)]
    assert scaled != convolution(x, y) and [a // D for a in scaled] == convolution(x, y)
    counts["negative_controls"] += 1
    # One fewer generic evaluation point does not determine all coefficients.
    vanishing = [1]
    for t in range(r - 1):
        vanishing = poly_linear(vanishing, t)
    assert any(vanishing)
    assert all(sum(a * t ** i for i, a in enumerate(vanishing)) == 0 for t in range(r - 1))
    counts["negative_controls"] += 1
    # An output-rank-one scalar target cannot inherit the 2M-1 output-span bound.
    M, R = 4, 81
    scalar = [[R ** (i + j) for i in range(M) for j in range(M)]]
    assert rank(scalar) == 1
    assert (R ** M - 1).bit_length() > (R - 1).bit_length()
    counts["negative_controls"] += 1
    # Substituting the all-ones word for p^d changes the target base.
    assert ((1 << 3) - 1) ** 2 == 49 != (1 << 6) - 1
    counts["negative_controls"] += 1

    result = {"status": "PASS", "counts": counts, "rank_rows": rank_rows,
              "parameter_rows": parameter_rows,
              "scope": "Fresh exact arithmetic controls; no historical programs, runtime benchmark, or numerical proof of asymptotics.",
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name("CONTROL_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "counts": counts}, indent=2))


if __name__ == "__main__":
    main()
