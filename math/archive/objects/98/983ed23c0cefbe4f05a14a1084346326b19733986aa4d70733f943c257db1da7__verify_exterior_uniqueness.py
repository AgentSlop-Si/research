#!/usr/bin/env python3
"""Independently authored fixed-interface linear-system controls."""
import json
from pathlib import Path

FIELD = 65537


def zero(n, m=None):
    return [[0] * (n if m is None else m) for _ in range(n)]


def eye(n):
    z = zero(n)
    for i in range(n):
        z[i][i] = 1
    return z


def mul(a, b):
    out = zero(len(a), len(b[0]))
    sparse_b = [[(j, x) for j, x in enumerate(row) if x] for row in b]
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in sparse_b[k]:
                    out[i][j] += x * y
        out[i] = [x % FIELD for x in out[i]]
    return out


def rank(a):
    z = [row[:] for row in a]
    r = 0
    width = len(z[0])
    for j in range(width):
        pivot = next((i for i in range(r, len(z)) if z[i][j]), None)
        if pivot is None:
            continue
        z[r], z[pivot] = z[pivot], z[r]
        iv = pow(z[r][j], -1, FIELD)
        z[r][j:] = [v * iv % FIELD for v in z[r][j:]]
        for i in range(r + 1, len(z)):
            c = z[i][j]
            if c:
                z[i][j:] = [(v - c * w) % FIELD for v, w in zip(z[i][j:], z[r][j:])]
        r += 1
        if r == len(z):
            break
    return r


def root(n):
    w = pow(3, (FIELD - 1) // n, FIELD)
    assert pow(w, n, FIELD) == 1 and pow(w, n // 2, FIELD) != 1
    return w


def fourier(n, w):
    return [[pow(w, i * j, FIELD) for j in range(n)] for i in range(n)]


def bank(m, q, active, inverse=False):
    eta = root(m)
    if inverse:
        eta = pow(eta, -1, FIELD)
    f = fourier(m, eta)
    if inverse:
        im = pow(m, -1, FIELD)
        f = [[v * im % FIELD for v in row] for row in f]
    out = zero(m * q)
    for r in range(q):
        block = f if r in active else eye(m)
        for i in range(m):
            for j in range(m):
                out[r * m + i][r * m + j] = block[i][j]
    return out


def intertwiner_equations(a, y):
    """Coefficient rows for P A - Y P = 0, row-major vec(P)."""
    n = len(a)
    equations = []
    for i in range(n):
        for j in range(n):
            row = [0] * (n * n)
            for k in range(n):
                row[i * n + k] = (row[i * n + k] + a[k][j]) % FIELD
                row[k * n + j] = (row[k * n + j] - y[i][k]) % FIELD
            equations.append(row)
    return equations


def check(m, q, active):
    n = m * q
    omega, eta = root(n), root(m)
    omega_q = pow(omega, m, FIELD)
    f = fourier(n, omega)
    r = zero(n)
    for b in range(q):
        for s in range(m):
            r[b * m + s][b + q * s] = 1
    rt = [list(row) for row in zip(*r)]
    b, bi = bank(m, q, active), bank(m, q, active, True)
    v, vi = mul(b, r), mul(rt, bi)
    s, si, d = zero(n), zero(n), zero(n)
    for j in range(n):
        s[(j + 1) % n][j] = 1
        si[(j - 1) % n][j] = 1
        d[j][j] = pow(omega, j, FIELD)
    a1, a2 = mul(mul(v, s), vi), mul(mul(v, d), vi)
    p0 = zero(n)
    for u in range(q):
        for t in range(m):
            for bank_index in range(q):
                common = pow(omega_q, u * bank_index, FIELD) * pow(omega, bank_index * t, FIELD) % FIELD
                for h in range(m):
                    factor = int(t == h) if bank_index in active else pow(eta, t * h, FIELD)
                    p0[m * u + t][m * bank_index + h] = common * factor % FIELD
    assert mul(p0, v) == f
    assert mul(p0, a1) == mul(d, p0)
    assert mul(p0, a2) == mul(si, p0)
    expected_nnz = n * (len(active) + (q - len(active)) * m)
    actual_nnz = sum(bool(x) for row in p0 for x in row)
    assert actual_nnz == expected_nnz
    e1, e2 = intertwiner_equations(a1, d), intertwiner_equations(a2, si)
    r1, rboth = rank(e1), rank(e1 + e2)
    calibration = [0] * (n * n)
    for k in range(n):
        calibration[k] = v[k][0]
    calibrated = rank(e1 + e2 + [calibration])
    assert r1 == n * n - n
    assert rboth == n * n - 1
    assert calibrated == n * n
    flat_p = [x for row in p0 for x in row]
    assert sum(x * y for x, y in zip(calibration, flat_p)) % FIELD == 1
    return {'N': n, 'm': m, 'q': q, 'active': sorted(active), 'P_nnz': actual_nnz,
            'unknowns': n * n, 'one_generator_rank': r1,
            'two_generator_rank': rboth, 'calibrated_rank': calibrated}


def main():
    cases = []
    for m, q, choices in (
        (2, 2, (set(), {0}, {1}, {0, 1})),
        (2, 4, (set(), {0}, {0, 1}, set(range(4)))),
        (4, 2, (set(), {0}, {0, 1})),
        (4, 4, ({0, 1},)),
    ):
        for active in choices:
            cases.append(check(m, q, active))
    result = {'field': FIELD, 'cases': cases, 'case_count': len(cases),
              'all_exact_assertions_passed': True,
              'scope': 'Unique exterior operator verified; no paired-Green factorization constructed.'}
    Path(__file__).with_name('EXTERIOR_UNIQUENESS_CONTROLS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
