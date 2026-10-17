"""Independent cycle-formula rebuild and rank certification; no research imports."""
from pathlib import Path
from math import isqrt
import hashlib
import json

P = 1_000_000_007
assert all(P % d for d in range(2, isqrt(P) + 1))


def permutation(s, choice):
    p = []
    for j in range(s * s):
        x, y = divmod(j, s)
        if choice < 2:
            x = (x + 2 * y + choice) % s
        else:
            y = (y + 2 * x + choice - 2) % s
        p.append(s * x + y)
    assert sorted(p) == list(range(s * s))
    return p


def cycle_resolvent(perm, numerator):
    n = len(perm)
    g = numerator * pow(101, P - 2, P) % P
    result = [[0] * n for _ in range(n)]
    for j in range(n):
        orbit = [j]
        while perm[orbit[-1]] != j:
            orbit.append(perm[orbit[-1]])
            assert len(orbit) <= n
        denominator = (1 - pow(g, len(orbit), P)) % P
        assert denominator
        reciprocal = pow(denominator, P - 2, P)
        power = 1
        for i in orbit:
            result[i][j] = power * reciprocal % P
            power = power * g % P
    for j in range(n):
        for i in range(n):
            # Explicitly check column j of (I-gP)G=I.
            predecessor = perm.index(i)
            assert (result[i][j] - g * result[predecessor][j]) % P == (i == j)
    return result


def rank(a):
    # Fraction-free elimination: all row multipliers are nonzero field elements.
    a = [row[:] for row in a]
    height, width, r = len(a), len(a[0]), 0
    for c in range(width):
        choices = [i for i in range(r, height) if a[i][c]]
        if not choices:
            continue
        i = choices[-1]
        a[i], a[r] = a[r], a[i]
        pivot = a[r][c]
        for i in range(r + 1, height):
            entry = a[i][c]
            if entry:
                a[i] = [(pivot * a[i][j] - entry * a[r][j]) % P for j in range(width)]
        r += 1
        if r == min(height, width):
            break
    return r


author = json.loads(Path(__file__).with_name('AUTHOR_CUT_CHECK_RESULTS.json').read_text())
checks = []
for s in (2, 3, 4):
    n = s * s
    perms = [permutation(s, q) for q in range(4)]
    gs = [cycle_resolvent(perms[q % 4], q + 1) for q in range(20)]
    x = [[sum(gs[q][i][j] for q in range(10)) % P for j in range(n)] for i in range(n)]
    y = [[sum(gs[q][i][j] for q in range(10, 20)) % P for j in range(n)] for i in range(n)]
    t = [[sum(y[i][k] * x[k][j] for k in range(n)) % P for j in range(n)] for i in range(n)]
    acase = next(c for c in author['cases'] if c['N'] == n)
    assert t == acase['matrix_mod_prime']
    eigen = sum(pow(1 - (q + 1) * pow(101, P - 2, P), P - 2, P) for q in range(10))
    eigen *= sum(pow(1 - (q + 1) * pow(101, P - 2, P), P - 2, P) for q in range(10, 20))
    eigen %= P
    assert all(sum(row) % P == eigen for row in t)
    stream = hashlib.sha256()
    minsurplus = n * n * 20
    for mask in range(1, 2 ** n - 1):
        inside = [i for i in range(n) if mask & (1 << i)]
        outside = [i for i in range(n) if not mask & (1 << i)]
        rr = rank([[t[i][j] for j in outside] for i in inside])
        assert rr == min(len(inside), len(outside)), (n, mask, rr)
        capacity = 5 * sum(bool(mask & (1 << p[j])) and not bool(mask & (1 << j))
                           for p in perms for j in range(n))
        minsurplus = min(minsurplus, capacity - rr)
        stream.update(f'{mask}:{rr}:{capacity}\n'.encode())
    assert stream.hexdigest() == acase['cut_stream_sha256']
    checks.append({'N': n, 'cuts': 2 ** n - 2, 'matrix_agrees': True,
                   'all_cross_blocks_full_rank': True, 'minimum_capacity_surplus': minsurplus,
                   'cut_stream_sha256': stream.hexdigest(), 'constant_eigenvalue_mod_p': eigen})
result = {'verdict': 'PASS', 'method': 'Closed-cycle resolvents plus separate fraction-free modular elimination',
          'prime_verified_by_trial_division': P, 'cases': checks,
          'total_directed_cuts': sum(c['cuts'] for c in checks), 'historical_or_author_programs_executed': False}
Path(__file__).with_name('CUT_INDEPENDENT_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
