"""Independent exact checks that do not import the primary Weyl-packet module."""
from __future__ import annotations

import json
from finite_field import field_for_length, inv, mat_identity, matrix_inverse, mat_vec


def dense_green(n, p, omega, alpha, r, h):
    a = mat_identity(n)
    for j in range(n):
        i = (j + h) % n
        a[i][j] = (a[i][j] - alpha * pow(omega, r * j, p)) % p
    return matrix_inverse(a, p)


def packet_literal(n, p, omega, alpha, s, h, x):
    out = [0] * n
    invn = inv(n, p)
    for r in range(n):
        g = dense_green(n, p, omega, alpha, r, h)
        y = mat_vec(g, x, p)
        w = invn * pow(omega, (-r * s) % n, p) % p
        for i in range(n):
            out[i] = (out[i] + w * y[i]) % p
    return out


def packet_sparse(n, p, omega, alpha, s, h, x):
    out = [0] * n
    den = inv((1 - pow(alpha, n, p)) % p, p)
    if s == 0:
        out = x[:]
    ap = alpha % p
    for m in range(1, n):
        j = ((s - h * m * (m - 1) // 2) * pow(m, -1, n)) % n
        i = (j + h * m) % n
        out[i] = (out[i] + ap * x[j]) % p
        ap = ap * alpha % p
    return [v * den % p for v in out]


def run():
    checked = 0
    max_nonzeros = 0
    for n in (5, 7, 11, 13):
        p, omega = field_for_length(n)
        alpha = 2
        while pow(alpha, n, p) == 1:
            alpha += 1
        x = [(j * j + 7 * j + 4) % p for j in range(n)]
        for h in (1, 2):
            for s in range(n):
                a = packet_literal(n, p, omega, alpha, s, h, x)
                b = packet_sparse(n, p, omega, alpha, s, h, x)
                assert a == b
                checked += 1
                # Independently materialize columns to count support.
                nnz = 0
                for j in range(n):
                    e = [0] * n
                    e[j] = 1
                    col = packet_sparse(n, p, omega, alpha, s, h, e)
                    nnz += sum(v != 0 for v in col)
                expected = 2 * n - 1 if s == 0 else n - 1
                assert nnz == expected
                max_nonzeros = max(max_nonzeros, nnz)
    result = {"independent_packet_cases": checked, "max_packet_nonzeros": max_nonzeros}
    with open("independent_results.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    run()
