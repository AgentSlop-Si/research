#!/usr/bin/env python3
"""Fresh exact controls; no historical checker imports or execution."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from itertools import permutations, combinations, product
from pathlib import Path
import hashlib
import json
import random
import time
import sympy as sp

ROOT = Path(__file__).resolve().parent
SHARED = ROOT.parent
rng = random.Random(2873_20261019)
START = time.monotonic()
COUNTS = Counter()
CERTIFICATES = []
CROSSCHECKS = []

SOURCES = [
    'rectangle_rank_two_20261018_1240/REPORT.md',
    'rank_two_review_20261018_1248/REVIEW.md',
    'mixed_prime_rank_three_20261018_1501/REPORT.md',
    'mixed_prime_rank_three_review_20261018_1514/REVIEW.md',
    'prime_cube_sharp_rank_three_20261018_1748/REPORT.md',
    'prime_cube_sharp_review_20261018_1753/REVIEW.md',
    'rectangle_triprime_20261018_1140/REPORT.md',
    'dominant_prime_review_20261018_1143/REVIEW.md',
]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

source_hashes = {s: digest(SHARED / s) for s in SOURCES}

@lru_cache(None)
def signed_permutations(k):
    result = []
    for perm in permutations(range(k)):
        sign = (-1) ** sum(perm[i] > perm[j]
                           for i in range(k) for j in range(i + 1, k))
        result.append((perm, sign))
    return result

def determinant_polynomial(n, rows, columns):
    coeffs = Counter()
    for perm, sign in signed_permutations(len(rows)):
        e = sum(rows[i] * columns[perm[i]] for i in range(len(rows))) % n
        coeffs[e] += sign
    return {e: c for e, c in coeffs.items() if c}

@lru_cache(None)
def prime_power_remainder(prime, power, exponent):
    modulus = prime ** power
    stride = prime ** (power - 1)
    exponent %= modulus
    digit, low = divmod(exponent, stride)
    if digit < prime - 1:
        return ((exponent, 1),)
    return tuple((low + j * stride, -1) for j in range(prime - 1))

@lru_cache(None)
def field_components(n):
    result = []
    for prime, power in sp.factorint(n).items():
        prime, power = int(prime), int(power)
        modulus = prime ** power
        unit = pow(n // modulus, -1, modulus)
        result.append((prime, power, unit))
    return tuple(result)

@lru_cache(None)
def monomial_remainder(n, exponent):
    parts = [prime_power_remainder(p, power, unit * exponent)
             for p, power, unit in field_components(n)]
    result = []
    for choice in product(*parts):
        basis = tuple(entry[0] for entry in choice)
        sign = 1
        for _, c in choice:
            sign *= c
        result.append((basis, sign))
    return tuple(result)

def exact_determinant(n, rows, columns, crosscheck=False):
    assert len(rows) == len(columns)
    assert len(set(rows)) == len(rows) and len(set(columns)) == len(columns)
    poly = determinant_polynomial(n, rows, columns)
    remainder = defaultdict(int)
    for exponent, coeff in poly.items():
        for basis, multiplier in monomial_remainder(n, exponent):
            remainder[basis] += coeff * multiplier
    nonzero = any(remainder.values())
    COUNTS[str(n)] += 1
    if crosscheck:
        CROSSCHECKS.append((n, list(rows), list(columns), nonzero))
    return nonzero

def find_nonzero_minor(n, rows, columns, trials=100):
    k = len(columns)
    for _ in range(trials):
        chosen = rng.sample(rows, k)
        if exact_determinant(n, chosen, columns):
            return chosen
    for chosen in combinations(rows, k):
        if exact_determinant(n, chosen, columns):
            return list(chosen)
    raise AssertionError(('No nonsingular minor', n, rows, columns))

results = {
    'status': 'running',
    'method': 'Exact characteristic-zero CRT cyclotomic tensor basis; independent literal cyclotomic polynomial division cross-checks. No floating point or finite-field rank substitutes.',
    'proof': 'REPORT.md gives a universal proof; the finite controls are supplemental.',
}

# Prime-power minor controls include arbitrary higher digits on both sides.
universal = 0
for p in [5, 7, 11, 13, 17, 19]:
    for trial in range(160):
        residues = rng.sample(range(p), 4)
        rows = [r + p * rng.randrange(p) for r in residues]
        columns = rng.sample(range(p * p), 4)
        assert exact_determinant(p * p, rows, columns, trial < 3)
        universal += 1
results['prime_square_universal_minors'] = universal

# Universal new minor pattern, both orientations of the two distinct primes.
pairs = [(5, 7), (7, 5), (7, 11), (11, 7), (11, 13),
         (13, 11), (13, 17), (17, 13), (17, 19), (19, 17)]
new_minors = 0
for p, q in pairs:
    n = p * p * q
    for trial in range(240):
        r0 = rng.randrange(p * p)
        lifts = rng.sample(range(q), 3)
        rows = [r0 + p * p * w for w in lifts]
        rstar = rng.randrange(n)
        while (rstar - r0) % p == 0:
            rstar = rng.randrange(n)
        rows.append(rstar)
        classes = rng.sample(range(q), 3)
        c1 = classes[0] + q * rng.randrange(p * p)
        c4 = classes[0] + q * rng.randrange(p * p)
        while c4 == c1:
            c4 = classes[0] + q * rng.randrange(p * p)
        columns = [c1,
                   classes[1] + q * rng.randrange(p * p),
                   classes[2] + q * rng.randrange(p * p), c4]
        assert exact_determinant(n, rows, columns, trial < 3)
        new_minors += 1
results['new_two_prime_four_minor_controls'] = new_minors

# Every nonzero k (the repeated-q column separation) at the target.
p, q, n = 13, 17, 2873
exhaustive_separations = 0
for k in range(1, p * p):
    for d in range(1, p * p):
        if d % p:
            rows, columns = [0, p * p, 2 * p * p, d], [0, 1, 2, q * k]
            assert exact_determinant(n, rows, columns)
            exhaustive_separations += 1
results['target_all_nonzero_separations_and_units'] = exhaustive_separations

# The unit-mod-p hypothesis is necessary for the displayed minor pattern.
negative_rows, negative_columns = [0, 169, 338, 13], [0, 1, 2, 221]
assert not exact_determinant(2873, negative_rows, negative_columns, True)
results['negative_control_without_unit_hypothesis'] = {
    'rows': negative_rows, 'columns': negative_columns, 'determinant': 0,
    'reason': '(13-0)*(221-0)=2873, so the final entry after subtraction vanishes.'
}

# Short-support full-column-rank controls at exactly the strict threshold.
short_support = 0
for p, q in [(5, 7), (7, 11), (11, 13), (13, 17), (17, 19)]:
    modulus = p * q
    for k in [2, 3, 4]:
        for trial in range(80):
            size = (k - 1) * max(p, q) + 1
            if trial % 2:
                rows = rng.sample(range(modulus), size)
            else:
                # Several complete small-prime-residue fibers plus one point.
                order = [y + p * z for y in rng.sample(range(p), p)
                         for z in rng.sample(range(q), q)]
                rows = order[:size]
            columns = rng.sample(range(modulus), k)
            certificate = find_nonzero_minor(modulus, rows, columns)
            if trial == 0:
                assert exact_determinant(modulus, certificate, columns, True)
            short_support += 1
results['semiprime_short_support_threshold_examples'] = short_support

# Arbitrary target rectangles above the bound, every relevant residue-count
# pairing. Each exact minor is selected by the proof; these are not exhaustive
# rectangles of the indicated scalar shape.
def selected_set(n, p, occupied_count, size):
    residues = rng.sample(range(p), occupied_count)
    mandatory = [r + p * rng.randrange(n // p) for r in residues]
    universe = [x for x in range(n) if x % p in residues and x not in mandatory]
    return mandatory + rng.sample(universe, size - len(mandatory))

def select_proof_minor(rows, columns):
    by_row_p = defaultdict(list)
    by_col_p = defaultdict(list)
    for r in rows:
        by_row_p[r % 13].append(r)
    for c in columns:
        by_col_p[c % 13].append(c)
    if len(by_col_p) >= 4:
        row_fibers = defaultdict(list)
        for r in rows:
            row_fibers[r % 17].append(r)
        rs = next(v[:4] for v in row_fibers.values() if len(v) >= 4)
        cs = [v[0] for v in list(by_col_p.values())[:4]]
        return rs, cs, 'prime_square_projection'
    if len(by_row_p) >= 4:
        cs, rs, _ = select_proof_minor(columns, rows)
        return rs, cs, 'transposed_prime_square_projection'
    if len(by_row_p) == 1:
        fibers = {}
        for c in columns:
            fibers.setdefault(c % 221, c)
        cs = list(fibers.values())[:4]
        assert len(cs) == 4
        rs = find_nonzero_minor(2873, rows, cs)
        return rs, cs, 'one_row_residue_short_support'
    row_fibers = defaultdict(list)
    for r in rows:
        row_fibers[r % 169].append(r)
    rs = next(v[:3] for v in row_fibers.values() if len(v) >= 3)
    rs.append(next(r for r in rows if (r - rs[0]) % 13))
    col_fibers = defaultdict(list)
    for c in columns:
        col_fibers[c % 17].append(c)
    assert len(col_fibers) >= 3
    repeated_residue = next(y for y, v in col_fibers.items() if len(v) >= 2)
    c1, c4 = col_fibers[repeated_residue][:2]
    others = [v[0] for y, v in col_fibers.items() if y != repeated_residue][:2]
    return rs, [c1, *others, c4], 'new_two_prime_minor'

branches = Counter()
for s in [1, 2, 3, 4, 5, 13]:
    for t in [1, 2, 3, 4, 5, 13]:
        for trial in range(20):
            rows = selected_set(2873, 13, s, 79)
            columns = selected_set(2873, 13, t, 79)
            rs, cs, branch = select_proof_minor(rows, columns)
            assert exact_determinant(2873, rs, cs, trial == 0)
            branches[branch] += 1
            CERTIFICATES.append({'row_residue_count': s, 'column_residue_count': t,
                                 'rectangle_side_sizes': [79, 79], 'branch': branch,
                                 'selected_rows': rs, 'selected_columns': cs})
results['target_rectangles_certified'] = dict(branches)

# Genuine rank-three controls: three distinct K-cosets and full annihilator.
# Their projective row classification proves rank<=3; nonzero 3-minors prove
# the reverse inequality, and all sampled 4-minors vanish exactly.
genuine = []
for d in [13, 17, 169, 221]:
    step = 2873 // d
    rows = [offset + step * j for offset in [0, 1, 2] for j in range(d)]
    columns = [d * j for j in range(2873 // d)]
    assert exact_determinant(2873, [0, 1, 2], columns[:3], True)
    for trial in range(150):
        assert not exact_determinant(2873, rng.sample(rows, 4),
                                     rng.sample(columns, 4), trial == 0)
    genuine.append({'d': d, 'side_sizes': [len(rows), len(columns)],
                    'nonzero_three_minor': [[0, 1, 2], columns[:3]],
                    'vanishing_four_minors': 150})
results['genuine_rank_three_controls'] = genuine

# Exact density and obstruction census. This is a scalar consequence only.
N, B = 2873, 78
divisors = [d for d in range(1, N + 1) if N % d == 0]
D = min(d + N // d for d in divisors)
E2 = min(2 * d + N // d for d in divisors[:-1])
floor = Fraction(3, B) + Fraction(B, N)
penalty = floor - Fraction(D, N)
assert (D, E2, N * D, floor, penalty) == (
    186, 203, 534378, Fraction(29, 442), Fraction(5, 5746))
assert 64 * N > 377 ** 2 and Fraction(E2, N) > floor
shape_count = 0
minimum, minimizing_shapes = Fraction(10 ** 9), []
global_minimum, global_minimizing_shapes = Fraction(10 ** 9), []
obstructions = []
for a in range(3, sp.integer_nthroot(3 * N, 2)[0] + 1):
    for b in range(a, min(N, 3 * N // a) + 1):
        density = Fraction(3 * (a + b), a * b)
        if density < global_minimum:
            global_minimum, global_minimizing_shapes = density, [[a, b]]
        elif density == global_minimum:
            global_minimizing_shapes.append([a, b])
        if density <= Fraction(D, N):
            obstructions.append([a, b])
            assert a > B
        if a <= B:
            shape_count += 1
            assert density >= floor
            if density < minimum:
                minimum, minimizing_shapes = density, [[a, b]]
            elif density == minimum:
                minimizing_shapes.append([a, b])
assert global_minimum == Fraction(62, 957)
assert global_minimizing_shapes == [[87, 99]]
assert Fraction(16015, 247078) - global_minimum == Fraction(7519, 236453646)
assert Fraction(185, 2852) - global_minimum == Fraction(221, 2729364)
assert [3 * N // a for a in range(88, 93)] == [97, 96, 95, 94, 93]
assert Fraction(12, 185) > global_minimum and Fraction(187, N) > global_minimum
assert 186 * 186 - 4 * 3 * N == 120
assert min(d for d in range(0, 187, 2) if d * d >= 120) == 12
assert (186 * 186 - 12 * 12) // 4 == 8613
results['N2873_exact_density_controls'] = {
    'D': D, 'E2': E2, 'cost': N * D, 'continuous_rank_three_floor': str(floor),
    'higher_rank_area_penalty': str(penalty), 'scalar_shapes_under_cutoff': shape_count,
    'integer_scalar_minimum': str(minimum), 'integer_scalar_minimizers': minimizing_shapes,
    'unrestricted_integer_scalar_minimum': str(global_minimum),
    'unrestricted_integer_scalar_minimizers': global_minimizing_shapes,
    'unrestricted_scalar_density_gap': str(global_minimum - Fraction(D, N)),
    'former_scalar_obstructions': obstructions,
}

# Explicit full partition and per-entry rank-one difference identities.
covered = bytearray(N * N)
tile_count, total_cost = 0, 0
for row_residue in range(169):
    rows = [row_residue + 169 * j for j in range(17)]
    for col_residue in range(17):
        columns = [col_residue + 17 * j for j in range(169)]
        for r in rows:
            for c in columns:
                index = r * N + c
                assert not covered[index]
                covered[index] = 1
                assert ((r - rows[0]) * (c - columns[0])) % N == 0
        tile_count += 1
        total_cost += len(rows) + len(columns)
assert all(covered) and tile_count == N and total_cost == N * D
results['full_target_partition'] = {'tiles': tile_count, 'entries_covered_once': len(covered),
                                    'cost': total_cost, 'unordered_sizes': [17, 169]}

# Fresh retained-domain census. Add only the new isolated target.
def retained_domain(n):
    ds = sp.divisors(n)
    d = min(x + n // x for x in ds)
    if d * d < 12 * n:
        return True
    factors = sp.factorint(n)
    if any(p > n // p for p in factors):
        return True
    if n in [1331, 2197]:
        return True
    if n % 11 == 0:
        q, perfect = sp.integer_nthroot(n // 11, 2)
        if perfect and q > 11 and sp.isprime(q):
            return True
    return False

previous = [n for n in range(2, 10001) if not retained_domain(n)]
remaining = [n for n in previous if n != 2873]
assert previous[0] == 2873 and remaining[0] == 3757
assert sp.factorint(3757) == {13: 1, 17: 2}
next_D = min(d + 3757 // d for d in sp.divisors(3757))
assert next_D == 238 and 12 * 3757 < next_D * next_D < 16 * 3757
results['retained_domain_census_through_10000'] = {
    'previous_residuals': previous, 'newly_settled': [2873],
    'remaining_residuals': remaining, 'all_lengths_through': 3756,
    'next_N': 3757, 'next_factorization': '13 * 17^2', 'next_D': next_D,
    'next_problematic_rank': 3,
}

# Independent cyclotomic polynomial long-division checks, including zeros.
x = sp.Symbol('x')
for n, rows, columns, expected in CROSSCHECKS:
    poly = determinant_polynomial(n, rows, columns)
    expression = sum(c * x ** e for e, c in poly.items())
    remainder = sp.rem(sp.Poly(expression, x), sp.Poly(sp.cyclotomic_poly(n, x), x))
    assert (not remainder.is_zero) == expected
results['independent_sympy_polynomial_crosschecks'] = len(CROSSCHECKS)

assert source_hashes == {s: digest(SHARED / s) for s in SOURCES}
results['source_hashes_unchanged'] = True
results['exact_determinant_counts_by_order'] = dict(sorted(COUNTS.items(), key=lambda z: int(z[0])))
results['exact_determinant_evaluations'] = sum(COUNTS.values())
results['elapsed_seconds'] = round(time.monotonic() - START, 3)
results['status'] = 'all_passed'
(ROOT / 'SOURCES.json').write_text(json.dumps(source_hashes, indent=2) + '\n')
(ROOT / 'RESULTS.json').write_text(json.dumps(results, indent=2) + '\n')
(ROOT / 'TARGET_MINOR_CERTIFICATES.json').write_text(json.dumps(CERTIFICATES, indent=2) + '\n')
print(json.dumps(results, indent=2))
