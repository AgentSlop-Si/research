"""Exact modular witnesses for the *all-permutation* two-stage cut-rank theorem.

No proof is inferred from sampling; the corresponding proof is in THEOREM.md.
Everything below is ordinary integer arithmetic modulo 998244353.
"""
from math import isqrt
from random import Random
import json

MOD = 998244353
PRIMITIVE_ROOT = 3


def rank_mod(A, p=MOD):
    if not A:
        return 0
    w = [list(map(lambda v: v % p, row)) for row in A]
    h, n = len(w), len(w[0])
    r = 0
    for col in range(n):
        pivot = next((i for i in range(r, h) if w[i][col]), None)
        if pivot is None:
            continue
        w[r], w[pivot] = w[pivot], w[r]
        inv = pow(w[r][col], p - 2, p)
        for i in range(r + 1, h):
            if w[i][col]:
                factor = w[i][col] * inv % p
                for j in range(col, n):
                    w[i][j] = (w[i][j] - factor * w[r][j]) % p
        r += 1
        if r == h:
            break
    return r


def stage(n, r, seed):
    """Generate an n*n exact quasiseparable stage, both cut ranks <=r."""
    g = Random(seed)
    def rows():
        return [[g.randrange(1, MOD) for _ in range(r)] for _ in range(n)]
    low_p, low_q, up_u, up_v = rows(), rows(), rows(), rows()
    d = [g.randrange(1, MOD) for _ in range(n)]
    return [[d[i] if i == j else
            sum(low_p[i][t] * low_q[j][t] for t in range(r)) % MOD if i > j else
            sum(up_u[i][t] * up_v[j][t] for t in range(r)) % MOD
            for j in range(n)] for i in range(n)]


def cut_bound(A, r):
    n = len(A)
    for k in range(1, n):
        assert rank_mod([row[k:] for row in A[:k]]) <= r
        assert rank_mod([row[:k] for row in A[k:]]) <= r


def permutation(n, kind, seed=777):
    if kind == 'identity':
        return list(range(n))
    if kind == 'reverse':
        return list(range(n - 1, -1, -1))
    if kind == 'bitrev':
        assert n & (n - 1) == 0
        b = n.bit_length() - 1
        return [int(f'{i:0{b}b}'[::-1], 2) for i in range(n)]
    if kind == 'random':
        p = list(range(n))
        Random(seed).shuffle(p)
        return p
    raise ValueError(kind)


def chosen_interval(perm):
    """Pick one of m disjoint m-wide column intervals with <=1 overlap."""
    n = len(perm)
    m = isqrt(n)
    counts = [0] * m
    for k in range(m):
        if perm[k] < m * m:
            counts[perm[k] // m] += 1
    t = min(range(m), key=counts.__getitem__)
    assert counts[t] <= 1, (counts, n)
    return m, t * m, counts[t]


def rectangular_product(A, B, perm, m, start, filter_k, weights=None):
    n = len(perm)
    out = [[0] * m for _ in range(m)]
    for k in range(n):
        if not filter_k(k):
            continue
        bk = B[perm[k]]
        for i in range(m):
            a = A[i][k] if weights is None else A[i][k] * weights[k] % MOD
            for j in range(m):
                out[i][j] = (out[i][j] + a * bk[start + j]) % MOD
    return out


def fourier_minor(n, m, start):
    assert (MOD - 1) % n == 0
    w = pow(PRIMITIVE_ROOT, (MOD - 1) // n, MOD)
    assert pow(w, n, MOD) == 1
    if n > 1:
        assert pow(w, n // 2, MOD) != 1
    return [[pow(w, i * (start + j), MOD) for j in range(m)] for i in range(m)]


def run_case(n=64, r1=2, r2=2, shuffle='random', seed=1009, weighted=False):
    """Matrix M=S2 P S1; r2 is the LEFT stage order, r1 right."""
    assert (MOD - 1) % n == 0, 'n must divide MOD-1'
    B = stage(n, r1, seed)
    A = stage(n, r2, seed + 17)
    # Underlying generators guarantee the cut ranks for every k; additionally
    # audit the actual ranks at small and medium sizes.
    if n <= 128:
        cut_bound(A, r2)
        cut_bound(B, r1)
    pi = permutation(n, shuffle, seed + 123)
    rng = Random(seed+2048)
    weights = [rng.randrange(1,MOD) for _ in range(n)] if weighted else None
    if weighted: assert len(set(weights)) > 1
    m, s, c = chosen_interval(pi)
    parts = [
        rectangular_product(A, B, pi, m, s, lambda k: k >= m, weights),
        rectangular_product(A, B, pi, m, s, lambda k: k < m and pi[k] < s, weights),
        rectangular_product(A, B, pi, m, s, lambda k: k < m and pi[k] >= s + m, weights),
        rectangular_product(A, B, pi, m, s, lambda k: k < m and s <= pi[k] < s + m, weights),
    ]
    part_ranks = [rank_mod(q) for q in parts]
    assert part_ranks[0] <= r2
    assert part_ranks[1] <= r1
    assert part_ranks[2] <= r1
    assert part_ranks[3] <= c
    M = [[sum(parts[t][i][j] for t in range(4)) % MOD
          for j in range(m)] for i in range(m)]
    rank_M = rank_mod(M)
    assert rank_M <= r2 + 2 * r1 + c
    F = fourier_minor(n, m, s)
    rank_F = rank_mod(F)
    assert rank_F == m
    forbidden = m > r2 + 2 * r1 + 1
    if forbidden:
        assert rank_M < rank_F
        assert M != F
    return {
        'N': n, 'r_left': r2, 'r_right': r1,
        'permutation': shuffle, 'monomial_weights': bool(weighted), 'm': m, 'column_interval': [s, s + m],
        'intersection_count': c, 'component_ranks': part_ranks,
        'rank_composed_minor': rank_M, 'rank_fourier_minor': rank_F,
        'universal_bound': r2 + 2 * r1 + 1,
        'theorem_rejects_all_permutations': forbidden,
        'local_certificate_passed': True,
    }


def run():
    cases=[]
    for n,r in [(32,1),(64,2),(128,3),(256,4)]:
        for kind in ['identity','reverse','bitrev','random']:
            cases.append(run_case(n,r,r,kind))
    return cases


if __name__=='__main__':
    results = run()
    print(json.dumps(results, indent=2))
