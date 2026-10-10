from __future__ import annotations

"""Independent finite-field verifier for the saved v18 cases.

This file intentionally does not import green_bank_gate.py.  It reconstructs the
same deterministic certificates using separately written permutation, separation,
Green-kernel, and modular-elimination routines.
"""

import json
import random
from pathlib import Path

CASES = {2: (13, 53), 3: (37, 149), 4: (83, 167), 5: (193, 773),
         6: (449, 3593), 7: (1031, 2063), 8: (2309, 32327)}


def inv(a, p):
    return pow(a % p, p - 2, p)


def primitive_root(p):
    n = p - 1
    fac = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError


def rank(a, p):
    a = [[x % p for x in row] for row in a]
    if not a: return 0
    m, n = len(a), len(a[0]); r = 0
    for c in range(n):
        z = None
        for i in range(r, m):
            if a[i][c]: z = i; break
        if z is None: continue
        a[r], a[z] = a[z], a[r]
        q = inv(a[r][c], p)
        for j in range(c, n): a[r][j] = a[r][j] * q % p
        for i in range(r + 1, m):
            q = a[i][c]
            if q:
                for j in range(c, n): a[i][j] = (a[i][j] - q * a[r][j]) % p
        r += 1
        if r == m: break
    return r


def det(a, p):
    a = [[x % p for x in row] for row in a]
    n = len(a); ans = 1
    for c in range(n):
        z = None
        for i in range(c, n):
            if a[i][c]: z = i; break
        if z is None: return 0
        if z != c:
            a[c], a[z] = a[z], a[c]
            ans = -ans
        pv = a[c][c]
        ans = ans * pv % p
        ip = inv(pv, p)
        for i in range(c + 1, n):
            q = a[i][c] * ip % p
            for j in range(c, n): a[i][j] = (a[i][j] - q * a[c][j]) % p
    return ans % p


def make_cycle(n, rng):
    q = list(range(n)); rng.shuffle(q)
    perm = [0] * n
    for i, x in enumerate(q): perm[x] = q[(i + 1) % n]
    return perm


def positions(perm):
    n = len(perm); out = [None] * n
    x = 0
    for k in range(n):
        out[x] = k; x = perm[x]
    assert x == 0 and all(v is not None for v in out)
    return out


def separated(orders):
    n = len(orders[0])
    q = sorted(range(n), key=lambda x: orders[0][x])
    m = n // 2
    A, B = q[:m], q[-m:]
    for o in orders[1:]:
        m = len(A)
        q = sorted(A + B, key=lambda x: o[x])
        low = set(q[:m])
        x1 = [x for x in A if x in low]
        y1 = [x for x in B if x not in low]
        x2 = [x for x in B if x in low]
        y2 = [x for x in A if x not in low]
        if len(x1) >= len(x2): A, B = x1, y1
        else: A, B = x2, y2
    return A, B


def green_rect(pos, alpha, left, right, A, B, p):
    n = len(pos); den = inv(1 - pow(alpha, n, p), p)
    return [[left[i] * pow(alpha, (pos[i] - pos[j]) % n, p) % p * right[j] % p * den % p
             for j in B] for i in A]


def verify_case(t, n, p):
    rng = random.Random(1800 + 1009 * t + n)
    perms = [make_cycle(n, rng) for _ in range(t)]
    pos = [positions(q) for q in perms]
    A, B = separated(pos)
    g = primitive_root(p)
    w = pow(g, (p - 1) // n, p)
    total = [[0] * len(B) for _ in A]
    term_ranks = []
    for r in range(t):
        while True:
            alpha = rng.randrange(0, p)
            if pow(alpha, n, p) != 1: break
        left = [rng.randrange(1, p) for _ in range(n)]
        right = [rng.randrange(1, p) for _ in range(n)]
        G = green_rect(pos[r], alpha, left, right, A, B, p)
        term_ranks.append(rank(G, p))
        for i in range(len(A)):
            for j in range(len(B)): total[i][j] = (total[i][j] + G[i][j]) % p
    F = [[pow(w, i * j, p) for j in B] for i in A]
    return {
        't': t, 'n': n, 'field': p, 'size': len(A),
        'term_ranks': term_ranks, 'sum_rank': rank(total, p),
        'fourier_rank': rank(F, p), 'fourier_det': det(F, p),
    }


def main():
    rows = [verify_case(t, *CASES[t]) for t in sorted(CASES)]
    for row in rows:
        assert row['size'] > row['t']
        assert max(row['term_ranks']) <= 1
        assert row['sum_rank'] <= row['t']
        assert row['fourier_rank'] == row['size']
        assert row['fourier_det'] != 0
    target = Path(__file__).with_name('independent_results.json')
    target.write_text(json.dumps(rows, indent=2, sort_keys=True) + '\n')
    print(json.dumps(rows, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
