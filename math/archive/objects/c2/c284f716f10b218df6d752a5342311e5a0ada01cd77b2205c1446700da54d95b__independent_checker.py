#!/usr/bin/env python3
"""Independent exact audits. No uploaded module is imported or executed."""
import itertools
import json
import random
from pathlib import Path

RNG = random.Random(20261009)


def rank(a, p):
    a = [[x % p for x in row] for row in a]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        z = pow(a[r][c], -1, p)
        a[r] = [(x * z) % p for x in a[r]]
        for i in range(r + 1, len(a)):
            z = a[i][c]
            a[i] = [(x - z * y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def inverse(a, p):
    n = len(a)
    b = [[x % p for x in row] + [int(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for c in range(n):
        pivot = next((i for i in range(c, n) if b[i][c]), None)
        if pivot is None:
            return None
        b[c], b[pivot] = b[pivot], b[c]
        z = pow(b[c][c], -1, p)
        b[c] = [(x * z) % p for x in b[c]]
        for i in range(n):
            if i != c:
                z = b[i][c]
                b[i] = [(x - z * y) % p for x, y in zip(b[i], b[c])]
    return [row[n:] for row in b]


def sub(a, rows, cols):
    return [[a[i][j] for j in cols] for i in rows]


def matmul(a, b, p):
    return [[sum(x * y for x, y in zip(row, col)) % p
             for col in zip(*b)] for row in a]


def prime(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def field_and_root(n):
    k = max(1, 1000 // n)
    while not prime(k * n + 1):
        k += 1
    p = k * n + 1
    divisors = [d for d in range(1, n) if n % d == 0]
    for g in range(2, p):
        w = pow(g, k, p)
        if pow(w, n, p) == 1 and all(pow(w, d, p) != 1 for d in divisors):
            return p, w
    raise AssertionError("Primitive root not found")


def qs(n, r, p, arbitrary_lower=False):
    u = [[RNG.randrange(p) for _ in range(n)] for _ in range(r)]
    v = [[RNG.randrange(p) for _ in range(n)] for _ in range(r)]
    x = [[RNG.randrange(p) for _ in range(n)] for _ in range(r)]
    y = [[RNG.randrange(p) for _ in range(n)] for _ in range(r)]
    return [[RNG.randrange(p) if i == j or (i > j and arbitrary_lower)
             else sum(u[t][i] * v[t][j] if i < j else x[t][i] * y[t][j]
                      for t in range(r)) % p
             for j in range(n)] for i in range(n)]


def cut_ranks(a, p):
    n = len(a)
    return (max(rank(sub(a, range(k), range(k, n)), p) for k in range(1, n)),
            max(rank(sub(a, range(k, n), range(k)), p) for k in range(1, n)))


def main():
    counts = dict(halfcut_products=0, one_endpoint_minor_checks=0,
                  monomial_distance_witnesses=0, inverse_cut_identities=0,
                  tridiagonal_inverse_cuts=0, three_stage_control_blocks=0)
    fields = {}
    for n in list(range(2, 18)) + [32]:
        p, w = field_and_root(n)
        fields[str(n)] = {"prime": p, "root": w}
        m = n // 2
        left, right = list(range(m)), list(range(n - m, n))
        f = [[pow(w, i * j, p) for j in range(n)] for i in range(n)]
        permutations = list(itertools.permutations(range(n))) if n <= 6 else []
        if not permutations:
            for _ in range(30):
                perm = list(range(n))
                RNG.shuffle(perm)
                permutations.append(perm)
        # Reuse independently generated stage pairs while varying every small permutation.
        stages = [(qs(n, r, p, True), qs(n, r, p)) for r in range(4)]
        for number, perm in enumerate(permutations):
            a, b = stages[number % len(stages)]
            au, _ = cut_ranks(a, p)
            bu, bl = cut_ranks(b, p)
            gains = [RNG.randrange(1, p) for _ in range(n)]
            pb = [[gains[k] * b[perm[k]][j] % p for j in range(n)]
                  for k in range(n)]
            product = matmul(a, pb, p)
            cl = sum(perm[k] < m for k in left)
            cr = sum(perm[k] >= n - m for k in left)
            assert cl + cr <= m
            assert rank(sub(product, left, left), p) <= cl + au + bl
            assert rank(sub(product, left, right), p) <= cr + au + bu
            counts["halfcut_products"] += 1
            # Either endpoint permutation separately preserves the required full minors.
            assert rank(sub(f, perm[:m], left), p) == m
            assert rank(sub(f, perm[:m], right), p) == m
            assert rank(sub(f, left, perm[:m]), p) == m
            assert rank(sub(f, left, perm[n - m:]), p) == m
            counts["one_endpoint_minor_checks"] += 4
            # A full minor of F-M outside the monomial support gives rank >= floor(N/2).
            difference = [row[:] for row in f]
            for i in range(n):
                difference[i][perm[i]] = (difference[i][perm[i]] - gains[i]) % p
            zero_cols = [j for j in range(n) if j not in set(perm[:m])][:m]
            assert rank(sub(difference, left, zero_cols), p) == m
            assert rank(difference, p) >= m
            counts["monomial_distance_witnesses"] += 1
        for _ in range(3):
            while True:
                a = [[RNG.randrange(p) for _ in range(n)] for _ in range(n)]
                ainv = inverse(a, p)
                if ainv is not None:
                    break
            while True:
                t = [[RNG.randrange(p) if abs(i - j) <= 1 else 0
                      for j in range(n)] for i in range(n)]
                tinv = inverse(t, p)
                if tinv is not None:
                    break
            for k in range(1, n):
                l, r = range(k), range(k, n)
                for i, j in [(l, r), (r, l)]:
                    assert rank(sub(a, i, j), p) == rank(sub(ainv, i, j), p)
                    assert rank(sub(tinv, i, j), p) == rank(sub(t, i, j), p) <= 1
                    counts["inverse_cut_identities"] += 1
                    counts["tridiagonal_inverse_cuts"] += 1
        if n % 2 == 0:
            b = [[0 for _ in range(n)] for _ in range(n)]
            for k in range(0, n, 2):
                b[k][k], b[k][k + 1], b[k + 1][k], b[k + 1][k + 1] = 1, 1, 1, 2
            assert cut_ranks(b, p) == (1, 1)
            e, o = range(0, n, 2), range(1, n, 2)
            for i, j in [(e, e), (e, o), (o, e), (o, o)]:
                assert rank(sub(b, i, j), p) == m
                counts["three_stage_control_blocks"] += 1
    # Both endpoint permutations can destroy the full-minor premise, already at N=4.
    p, w = field_and_root(4)
    f = [[pow(w, i * j, p) for j in range(4)] for i in range(4)]
    assert rank(sub(f, [0, 2], [0, 2]), p) == 1
    # The stated odd-N bound does not exclude rank-2 plus rank-2 at N=17.
    assert 2 + 2 == (17 // 2) / 2
    output = {"status": "PASS", "seed": 20261009, "counts": counts,
              "fields": fields, "scope": "Finite exact audits, not universal proofs."}
    path = Path(__file__).with_name("independent_results.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
