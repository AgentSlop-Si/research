"""Independent, newly authored exact supplementary controls; standard library only.

This program does not read, import, execute, compile, or parse an inherited
research program. Finite controls do not establish the all-size theorems.
"""
import itertools
import json
from pathlib import Path


def inverse(a, p):
    n = len(a)
    b = [[x % p for x in a[i]] + [int(i == j) for j in range(n)] for i in range(n)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        if pivot is None:
            return None
        b[j], b[pivot] = b[pivot], b[j]
        scale = pow(b[j][j], p - 2, p)
        b[j] = [(scale * x) % p for x in b[j]]
        for i in range(n):
            if i != j:
                scale = b[i][j]
                b[i] = [(x - scale * y) % p for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def rank(a, p, width=None):
    if not a:
        return 0
    b = [list(row) for row in a]
    n = len(b[0]) if width is None else width
    k = 0
    for j in range(n):
        pivot = next((i for i in range(k, len(b)) if b[i][j] % p), None)
        if pivot is None:
            continue
        b[k], b[pivot] = b[pivot], b[k]
        scale = pow(b[k][j] % p, p - 2, p)
        b[k] = [(x * scale) % p for x in b[k]]
        for i in range(k + 1, len(b)):
            scale = b[i][j] % p
            b[i] = [(x - scale * y) % p for x, y in zip(b[i], b[k])]
        k += 1
        if k == len(b):
            break
    return k


def direction(v, p):
    first = next((x for x in v if x), None)
    if first is None:
        return None
    inv = pow(first, p - 2, p)
    return tuple((x * inv) % p for x in v)


def restrictions(n):
    return [tuple(i for i in range(n) if mask >> i & 1) for mask in range(1, 1 << n)]


def columns(n, p):
    for size in (1, 2):
        for support in itertools.combinations(range(n), size):
            for values in itertools.product(range(1, p), repeat=size):
                col = [0] * n
                for j, v in zip(support, values):
                    col[j] = v
                yield tuple(col)


counts = dict(column_two_matrices=0, invertible_matrices=0,
              inverse_row_restrictions=0, nullity_identities=0,
              high_row_degree_invertible=0, color_count_cases=0,
              strict_threshold_cases=0, vandermonde_minors=0)
for p, maximum in ((2, 4), (3, 3)):
    for n in range(1, maximum + 1):
        rowsets = restrictions(n)
        for cols in itertools.product(tuple(columns(n, p)), repeat=n):
            counts['column_two_matrices'] += 1
            a = [list(row) for row in zip(*cols)]
            inv = inverse(a, p)
            if inv is None:
                continue
            counts['invertible_matrices'] += 1
            if any(sum(x != 0 for x in row) > 2 for row in a):
                counts['high_row_degree_invertible'] += 1
            for rows in rowsets:
                directions = {direction(tuple(inv[i][j] for i in rows), p) for j in range(n)}
                directions.discard(None)
                assert len(directions) == len(rows)
                assert rank(list(directions), p) == len(rows)
                counts['inverse_row_restrictions'] += 1
            # Complete swapped-complement identities on every order <= 2 instance.
            if n <= 2:
                sets = [()] + rowsets
                for i in sets:
                    for j in sets:
                        ic = [x for x in range(n) if x not in i]
                        jc = [x for x in range(n) if x not in j]
                        lhs = rank([[inv[x][y] for y in j] for x in i], p)
                        rhs = rank([[a[x][y] for y in ic] for x in jc], p) + len(i) + len(j) - n
                        assert lhs == rhs
                        counts['nullity_identities'] += 1

for u in range(1, 101):
    for red in range(u + 1):
        for blue in range(u + 1):
            if 2 * u <= 3 * (red + blue) <= 4 * u:
                keep = (u + 2) // 3
                assert max(min(red, u - blue), min(u - red, blue)) >= keep
                counts['color_count_cases'] += 1

for q, r, s, t, delta in itertools.product(range(1, 7), range(1, 7), range(5), range(5), (0, 1)):
    d = s + 1 + delta
    R = q * r + t
    a = 3 ** r
    c = d - 1 + d * q * (a - 1) // 2
    cutoff = d * d * R * a * a + 2 * c
    for addition in (1, d, a):
        N = cutoff + addition
        m = N // d
        for j in range(r):
            assert m >= 4 * q
            m = (m - q + 2) // 3
        assert d * a * m >= N - c
        assert m * m > N * R
        counts['strict_threshold_cases'] += 1

# Exact Vandermonde controls include cyclic wrapping and composite orders.
for p, n, omega in ((5, 4, 2), (7, 6, 3), (17, 8, 2), (13, 12, 2)):
    assert pow(omega, n, p) == 1
    assert all(pow(omega, j, p) != 1 for j in range(1, n))
    for k in range(1, min(n, 4) + 1):
        for start in (0, n - 1):
            rows = [(start + j) % n for j in range(k)]
            for cols in itertools.combinations(range(n), k):
                a = [[pow(omega, i * j, p) for j in cols] for i in rows]
                assert rank(a, p) == k
                counts['vandermonde_minors'] += 1

# A useful guard against accidentally importing arbitrary-row full spark.
assert rank([[pow(2, i * j, 5) for j in (0, 2)] for i in (0, 2)], 5) == 1
result = {
    'status': 'PASS',
    'arithmetic': 'Exact prime-field and integer arithmetic only',
    'counts': counts,
    'negative_control': 'N=4 Fourier rows {0,2}, columns {0,2} over GF(5) have rank one',
    'inherited_programs_executed': False,
    'all_size_proof_substitution': False,
}
out = Path(__file__).with_name('FRESH_CONTROLS.json')
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
