#!/usr/bin/env python3
"""Independent finite-field controls and symbolic boundary factorization.

Only inert JSON certificate data is read. No uploaded source is executed.
The rank inequalities are proved in the report; finite tests are controls.
"""
from pathlib import Path
from itertools import combinations
from random import Random
import json, math, time

HERE = Path(__file__).resolve().parent
started = time.monotonic()
rng = Random(10101827)


def rank(A, p):
    if not A:
        return 0
    M = [[x % p for x in row] for row in A]
    r = 0
    for c in range(len(M[0])):
        pivot = next((i for i in range(r, len(M)) if M[i][c]), None)
        if pivot is None:
            continue
        M[r], M[pivot] = M[pivot], M[r]
        inv = pow(M[r][c], -1, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(r + 1, len(M)):
            f = M[i][c]
            if f:
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def det(A, p):
    M = [[x % p for x in row] for row in A]
    result = 1
    for c in range(len(M)):
        pivot = next((i for i in range(c, len(M)) if M[i][c]), None)
        if pivot is None:
            return 0
        if pivot != c:
            M[c], M[pivot] = M[pivot], M[c]
            result = -result
        value = M[c][c]
        result = result * value % p
        inv = pow(value, -1, p)
        for i in range(c + 1, len(M)):
            f = M[i][c] * inv % p
            if f:
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[c])]
    return result % p


def multiply(A, B, p):
    columns = list(zip(*B))
    return [[sum(x * y for x, y in zip(row, col)) % p for col in columns] for row in A]


def is_prime(p):
    return p >= 2 and all(p % d for d in range(2, math.isqrt(p) + 1))


def primitive_root_of_order(n, p):
    assert is_prime(p) and (p - 1) % n == 0
    for a in range(2, p):
        z = pow(a, (p - 1) // n, p)
        if pow(z, n, p) == 1 and all(pow(z, d, p) != 1 for d in range(1, n) if n % d == 0):
            return z
    raise AssertionError((n, p))


def field_for(n):
    k = (1000 + n - 1) // n
    while not is_prime(k * n + 1):
        k += 1
    p = k * n + 1
    return p, primitive_root_of_order(n, p)


def transpose(A):
    return [list(row) for row in zip(*A)]


results = []
counts = {'kernel_annihilation': 0, 'kernel_restriction_ranks': 0,
          'fullrank_space_inequalities': 0, 'spectral_complement_identities': 0,
          'spectral_tail_map_invertibility': 0, 'spectral_space_ranks': 0}
for n in list(range(2, 19)) + [24, 32, 64]:
    p, z = field_for(n)
    F = [[pow(z, i * k, p) for k in range(n)] for i in range(n)]
    ts = list(range(1, n)) if n <= 18 else sorted({1, 2, 3, 4, n // 2, n - 2, n - 1})
    for t in ts:
        high = [[pow(z, r * k, p) for r in range(1, t + 1)] for k in range(n)]
        low = [[pow(z, (-r * k) % n, p) for r in range(t)] for k in range(n)]
        assert not any(any(row) for row in multiply(F[:n - t], high, p))
        assert not any(any(row) for row in multiply(F[t:], low, p))
        counts['kernel_annihilation'] += 2
        for a in range(n):
            assert rank(high[a + 1:], p) == min(t, n - 1 - a)
            assert rank(low[:a], p) == min(t, a)
            counts['kernel_restriction_ranks'] += 2
        for rep in range(4):
            X = [[rng.randrange(p) for _ in range(t)] for _ in range(n)]
            if rank(X, p) < t:
                continue
            a = rng.randrange(n)
            assert rank(multiply(F[:n - t], X, p), p) + rank(X[a + 1:], p) >= min(t, n - 1 - a)
            assert rank(multiply(F[t:], X, p), p) + rank(X[:a], p) >= min(t, a)
            counts['fullrank_space_inequalities'] += 2
    bs = list(range(1, n // 2 + 1)) if n <= 18 else sorted({1, 2, 3, n // 2})
    for b in bs:
        # The tail -> initial-output map is square. Check its invertibility.
        square = [row[b:] for row in F[:n - b]]
        assert rank(square, p) == n - b
        counts['spectral_tail_map_invertibility'] += 1
        tail_exp = [[pow(z, r * k, p) for r in range(1, b + 1)] for k in range(b, n)]
        low_chars = [[pow(z, i * j, p) for j in range(b)] for i in range(n - b)]
        coeffs = [[-pow(z, r * j, p) % p for r in range(1, b + 1)] for j in range(b)]
        assert multiply(square, tail_exp, p) == multiply(low_chars, coeffs, p)
        assert rank(tail_exp, p) == rank(low_chars, p) == rank(coeffs, p) == b
        counts['spectral_complement_identities'] += 1
        counts['spectral_space_ranks'] += 3
    results.append({'N': n, 'prime': p, 'root': z, 't_values': ts, 'b_values': bs})
print('All-length Fourier rank and spectral-complement controls passed.', flush=True)

# Independent all-length boundary-lock controls, including N=9 (first valid
# six-row case), non-power-of-two lengths and deliberate zero branches.
boundary_cases = []
for n in (8, 9, 10, 11, 12, 15, 16, 24, 32, 64):
    p, z = field_for(n)
    counts_here = {'rank_equivalences': 0, 'determinant_factorizations': 0,
                   'zero_boundary_cases': 0, 'N8_exceptions': 0}
    ratios = set()
    for rep in range(40):
        alpha = [rng.randrange(p) for _ in range(3)]
        U = [rng.randrange(p) for _ in range(n)]
        L = [sum(alpha[r - 1] * pow(z, r * k, p) for r in (1, 2, 3)) % p for k in range(n)]
        if rep % 4 == 0:
            alpha = [0, 0, 0]
            L = [0] * n
            U[3] = U[4] = 0
        elif rep % 4 == 1:
            scale = rng.randrange(p)
            U[3], U[4] = scale * L[3] % p, scale * L[4] % p
        M = [[1, pow(z, i, p), pow(z, 2 * i, p), pow(z, 5 * i, p),
              sum(U[k] * pow(z, i * k, p) for k in range(5)) % p,
              sum(L[k] * pow(z, i * k, p) for k in range(6, n)) % p]
             for i in range(n - 3)]
        D = (U[3] * L[4] - U[4] * L[3]) % p
        if n >= 9:
            boundary_rank = rank([[U[3], -L[3]], [U[4], -L[4]]], p)
            assert rank(M, p) == 4 + boundary_rank
            assert (rank(M, p) <= 5) == (D == 0)
            vand = math.prod((pow(z, j, p) - pow(z, i, p)) % p for i, j in combinations(range(6), 2)) % p
            assert vand
            assert det(M[:6], p) == -D * vand % p
            counts_here['rank_equivalences'] += 1
            counts_here['determinant_factorizations'] += 1
            if D:
                ratios.add(det(M[:6], p) * pow(D, -1, p) % p)
            else:
                counts_here['zero_boundary_cases'] += 1
        else:
            assert rank(M, p) <= 5
            if D:
                assert rank(M, p) == 5
                counts_here['N8_exceptions'] += 1
    boundary_cases.append({'N': n, 'prime': p, 'root': z, **counts_here, 'nonzero_ratios': sorted(ratios)})

# Reproduce every numerical constant in the supplied boundary certificate
# without recreating its random sample stream.
original_boundary = json.loads((HERE / 'input_data' / 'BOUNDARY_LOCK_TESTS.json').read_text())
source_ratios = []
for row in original_boundary:
    n, p, z = row['n'], row['p'], row['z']
    assert pow(z, n, p) == 1 and all(pow(z, d, p) != 1 for d in range(1, n) if n % d == 0)
    if n >= 9:
        ratio = -math.prod((pow(z, j, p) - pow(z, i, p)) % p for i, j in combinations(range(6), 2)) % p
        assert ratio == row['determinant_ratio']
        source_ratios.append({'N': n, 'prime': p, 'root': z, 'ratio': ratio})

tail_witnesses = []
for n, p, z, expected in [(16, 12289, 4134, 1099), (16, 65537, 64, 121),
                           (32, 12289, 5860, 2858), (64, 12289, 7311, 4461)]:
    value = det([[pow(z, r * k, p) for r in (1, 2, 3)] for k in (6, 7, 8)], p)
    assert value == expected
    tail_witnesses.append({'N': n, 'prime': p, 'root': z, 'determinant': value})

# Exact symbolic N=8 exception: alpha=(1,0,0), U3=1,U4=0 gives D=z^4=-1.
# Verify it over a fresh finite field as a control of the general proof.
p, z = 17, 9
L = [pow(z, k, p) for k in range(8)]
M = [[1, pow(z, i, p), pow(z, 2*i, p), pow(z, 5*i, p), pow(z, 3*i, p),
      sum(L[k] * pow(z, i*k, p) for k in range(6, 8)) % p] for i in range(5)]
assert L[4] == p - 1 and rank(M, p) == 5
print('Boundary identity and rank criterion passed, with explicit N=8 exception.', flush=True)

out = {'uploaded_code_executed': False, 'seed': 10101827, 'rank_and_spectral_checks': counts,
       'rank_and_spectral_fields': results, 'boundary_checks': boundary_cases,
       'source_boundary_ratios_reproduced': source_ratios,
       'source_tail_determinants_reproduced': tail_witnesses,
       'explicit_N8_exception': {'prime': 17, 'root': 9, 'alpha': [1, 0, 0],
                                'U3': 1, 'U4': 0, 'D': 16, 'rank': 5},
       'elapsed_seconds': round(time.monotonic() - started, 3)}
(HERE / 'modular_results.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'counts': counts, 'elapsed_seconds': out['elapsed_seconds']}, indent=2), flush=True)
