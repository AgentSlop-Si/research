"""Fresh exact controls for the centering composition obstruction.

No historical module is imported or executed. Cyclotomic checks are over Q;
the separate large finite-field checks are labelled analogues, not complex
numerical certificates. All pseudo-random fixtures use a fixed disclosed seed.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
from math import isqrt
from pathlib import Path
from random import Random
import json
import time

BASE = Path(__file__).resolve().parent


def mono(e, M, a=1):
    d = M // 2
    e %= M
    out = [0] * d
    out[e % d] = a if e < d else -a
    return tuple(out)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(a, b):
    d = len(a)
    out = [0] * d
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    k = i + j
                    out[k % d] += x * y if k < d else -x * y
    return tuple(out)


def permutation_sign(p):
    return -1 if sum(p[i] > p[j] for i in range(len(p))
                     for j in range(i + 1, len(p))) % 2 else 1


def consecutive_determinant(support, first, M):
    """Leibniz determinant, independent of the product-of-differences formula."""
    total = mono(0, M, 0)
    for p in permutations(range(len(support))):
        exponent = sum((first + q) * support[p[q]]
                       for q in range(len(support)))
        total = add(total, mono(exponent, M, permutation_sign(p)))
    return total


def vandermonde_product(support, first, M):
    out = mono(first * sum(support), M)
    for i in range(len(support)):
        for j in range(i + 1, len(support)):
            factor = add(mono(support[j], M), mono(support[i], M, -1))
            out = mul(out, factor)
    return out


def prime_by_trial(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, isqrt(n) + 1, 2))


def field_det(matrix, p):
    a = [list(row) for row in matrix]
    out = 1
    for col in range(len(a)):
        pivot = next((r for r in range(col, len(a)) if a[r][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            a[pivot], a[col] = a[col], a[pivot]
            out = -out
        val = a[col][col]
        out = out * val % p
        inv = pow(val, -1, p)
        for row in range(col + 1, len(a)):
            factor = a[row][col] * inv % p
            for k in range(col, len(a)):
                a[row][k] = (a[row][k] - factor * a[col][k]) % p
    return out % p


def main():
    started = time.monotonic()
    result = {'status': 'PASS', 'historical_code_executed': False,
              'external_writes': False, 'independent_review': False,
              'numeric_tolerances_used': False}

    bindings = json.loads((BASE / 'SOURCE_BINDINGS.json').read_text())
    for row in bindings['files']:
        data = (BASE / row['local_path']).read_bytes()
        assert len(data) == row['bytes']
        assert sha256(data).hexdigest() == row['sha256']
    result['source_files_hash_checked'] = len(bindings['files'])

    determinants = 0
    support_sets = 0
    for M in (4, 8, 16):
        for s in range(1, min(4, M) + 1):
            for support in combinations(range(M), s):
                support_sets += 1
                for first in (0, 1, M - 1):
                    actual = consecutive_determinant(support, first, M)
                    expected = vandermonde_product(support, first, M)
                    assert actual == expected
                    assert any(actual)
                    determinants += 1
    result['cyclotomic_consecutive_minors'] = {
        'dyadic_lengths': [4, 8, 16],
        'support_sets': support_sets, 'determinants': determinants,
        'first_rows': ['0', '1', 'M-1 (wrap)'],
        'ring': 'Z[z]/(z^(M/2)+1), the dyadic cyclotomic ring'}

    identities = 0
    for M in (4, 8, 16, 32):
        for j in range(M):
            for ell in range(M):
                total = mono(0, M, 0)
                for k in range(M):
                    total = add(total, mono(k * (j + ell), M))
                expected = mono(0, M, M if (j + ell) % M == 0 else 0)
                assert total == expected
                identities += 1
    result['unnormalized_dft_squared_exact_entries'] = identities

    M = 1 << 28
    N = 1 << 26
    p = 3221225473
    assert prime_by_trial(p)
    assert (p - 1) % M == 0
    root = next(pow(a, (p - 1) // M, p) for a in range(2, 100)
                if pow(pow(a, (p - 1) // M, p), M // 2, p) != 1)
    assert pow(root, M, p) == 1 and pow(root, M // 2, p) != 1
    rng = Random(202610181042)
    fixtures = [[0], [M - 1], list(range(16)),
                [M - 16 + i for i in range(16)],
                [i * (M // 16) for i in range(16)]]
    fixtures += [sorted(rng.sample(range(M), s))
                 for s in range(2, 17) for _ in range(2)]
    modular_count = 0
    for support in fixtures:
        for first in (0, 1, M - 3):
            nodes = [pow(root, n, p) for n in support]
            matrix = [[pow(z, first + q, p) for z in nodes]
                      for q in range(len(nodes))]
            actual = field_det(matrix, p)
            expected = pow(root, first * sum(support), p)
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    expected = expected * (nodes[j] - nodes[i]) % p
            assert actual == expected != 0
            modular_count += 1
    result['large_finite_field_analogues'] = {
        'scope': 'Exact finite-field analogues only; complex theorem is proved separately.',
        'prime': p, 'primality_method': 'complete odd trial division through isqrt(p)',
        'root_of_exact_order_2pow28': root,
        'fixtures': len(fixtures), 'determinants': modular_count,
        'fixed_fixture_seed': 202610181042}

    lower = M - N + 1
    assert lower == 201326593 and lower > 64
    assert (1 << 25) < N <= (1 << 26)
    assert 1 << (4 * N - 1).bit_length() == M
    theta = Fraction(1, 1 << 400)
    error_lower = 1 - Fraction(1, 1 << 14) - 9 * theta
    outer_error = Fraction(1, 32)
    assert error_lower > outer_error
    P = 464
    t = 32 * 5 * 28 + 4
    assert P == 16 * 28 + 16 and t == 4484 < M
    assert (1 << 480) < 3 * M * M * (1 << P)
    result['exact_composition_obstruction'] = {
        'M': M, 'largest_compatible_outer_N': N,
        'least_compatible_outer_N': (1 << 25) + 1,
        'necessary_original_support_minimum': lower,
        'accepted_recovery_support_maximum': 16,
        'standalone_supplier_support_maximum': 64,
        'nonzero_exact_intersection': False,
        'impulse_gap_lower_numerator': error_lower.numerator,
        'impulse_gap_lower_denominator': error_lower.denominator,
        'required_outer_error_beta_one_quarter': '1/32',
        'same_grid_bits': P, 'outer_t_D5': t,
        'returned_decoder_numerator_width_bound_bits': 480,
        'outer_cap': '3*2^520'}

    # The reflection in the target chain matters. Small Gaussian coefficient
    # vectors test H^2 x=M R x by a second, vector-level exact calculation.
    vector_count = 0
    for M in (4, 8, 16):
        d = M // 2
        for _ in range(10):
            raw = [(rng.randrange(-3, 4), rng.randrange(-3, 4)) for _ in range(M)]
            enc = [add(mono(0, M, re), mono(M // 4, M, im)) for re, im in raw]
            first = [tuple(sum(mul(enc[j], mono(j * k, M))[a]
                               for j in range(M)) for a in range(d))
                     for k in range(M)]
            second = [tuple(sum(mul(first[k], mono(k * ell, M))[a]
                                for k in range(M)) for a in range(d))
                      for ell in range(M)]
            for ell in range(M):
                assert second[ell] == tuple(M * v for v in enc[(-ell) % M])
            vector_count += 1
    result['gaussian_vector_second_transform_checks'] = vector_count
    result['elapsed_seconds'] = time.monotonic() - started
    (BASE / 'RESULTS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
