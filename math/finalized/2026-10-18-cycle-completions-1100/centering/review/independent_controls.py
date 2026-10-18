"""Independent exact controls, written after source inspection.

No candidate or preserved program is imported or executed. This file uses only
the standard library. The finite checks supplement the general complex proof.
"""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
from itertools import combinations
from math import isqrt
import ast
import json
import time

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / 'candidate_snapshot'
LIVE = HERE.parent / 'candidate'


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': sha256(data).hexdigest()}


def shift(p, exponent):
    """Multiply a coefficient vector by X^exponent modulo X^d+1."""
    d = len(p)
    out = [0] * d
    for j, a in enumerate(p):
        q, r = divmod(j + exponent, d)
        out[r] += -a if q % 2 else a
    return tuple(out)


def plus(p, q):
    return tuple(a + b for a, b in zip(p, q))


def minus(p):
    return tuple(-a for a in p)


def monomial(M, exponent=0, coefficient=1):
    return shift((coefficient,) + (0,) * (M // 2 - 1), exponent)


def multiply(p, q):
    out = (0,) * len(p)
    for k, a in enumerate(q):
        if a:
            out = plus(out, tuple(a * v for v in shift(p, k)))
    return out


def subset_determinant(support, start, M):
    """Signed subset dynamic programming, not a product formula or permutations."""
    states = {0: monomial(M)}
    for row in range(len(support)):
        following = {}
        for mask, value in states.items():
            for col, n in enumerate(support):
                if (mask >> col) & 1:
                    continue
                v = shift(value, -(start + row) * n)
                if (mask >> (col + 1)).bit_count() % 2:
                    v = minus(v)
                nextmask = mask | (1 << col)
                following[nextmask] = plus(following.get(nextmask, (0,) * (M // 2)), v)
        states = following
    return states[(1 << len(support)) - 1]


def dft(vector, sign):
    M = len(vector)
    zero = (0,) * (M // 2)
    out = []
    for k in range(M):
        total = zero
        for j, value in enumerate(vector):
            total = plus(total, shift(value, sign * j * k))
        out.append(total)
    return out


def rounding_by_nearest_distance(q):
    floor = q.numerator // q.denominator
    a, b = floor, floor + 1
    da, db = abs(q - a), abs(q - b)
    return a if da < db or (da == db and a % 2 == 0) else b


def integrity():
    manifest = json.loads((CANDIDATE / 'MANIFEST.json').read_text())
    seal = json.loads((CANDIDATE / 'SEAL.json').read_text())
    assert digest(CANDIDATE / 'MANIFEST.json')['sha256'] == seal['manifest_sha256']
    assert len(manifest['files']) == seal['file_count']
    for rel, spec in manifest['files'].items():
        assert digest(CANDIDATE / rel) == spec
        assert digest(LIVE / rel) == spec
    assert digest(CANDIDATE / 'MANIFEST.json') == digest(LIVE / 'MANIFEST.json')
    assert digest(CANDIDATE / 'SEAL.json') == digest(LIVE / 'SEAL.json')
    remote = (HERE / 'REMOTE_RELEASE_MANIFEST.json').read_text()
    local = (CANDIDATE / 'sources/MANIFEST.json').read_bytes()
    assert remote.encode() == local
    fetched = json.loads(remote)
    bindings = json.loads((CANDIDATE / 'SOURCE_BINDINGS.json').read_text())
    for row in bindings['files']:
        actual = digest(CANDIDATE / row['local_path'])
        expected = {k: row[k] for k in ('bytes', 'sha256')}
        assert actual == expected == fetched['files'][row['path']]
    return {'author_manifest_sha256': seal['manifest_sha256'],
            'author_manifest_members': len(manifest['files']),
            'source_bindings_checked_against_remote_release': len(bindings['files']),
            'release_manifest_sha256': sha256(local).hexdigest(),
            'candidate_and_snapshot_unchanged': True}


def main():
    started = time.monotonic()
    before = integrity()
    determinant_count = 0
    support_count = 0
    for M in (4, 8, 16):
        for s in range(1, min(4, M) + 1):
            for support in combinations(range(M), s):
                support_count += 1
                for start in range(M):
                    assert any(subset_determinant(support, start, M))
                    determinant_count += 1

    # A sharpness witness: an N-1-root polynomial has exactly N-1 sampled
    # zeros, so an interval-supported transform can require M-N+1 entries.
    # This is an auxiliary complex-algebra control, not a dyadic admissible input.
    sharpness = []
    transform_coordinates = 0
    for M in (4, 8, 16, 32):
        for N in range(M // 8 + 1, M // 4 + 1):
            unit = monomial(M)
            zero = monomial(M, coefficient=0)
            coefficients = [unit]
            for r in range(N - 1):
                new = [zero] * (len(coefficients) + 1)
                for j, c in enumerate(coefficients):
                    new[j] = plus(new[j], minus(shift(c, r)))
                    new[j + 1] = plus(new[j + 1], c)
                coefficients = new
            a0 = (N - 1) // 2
            v = [zero] * M
            for j, c in enumerate(coefficients):
                v[(j - a0) % M] = c
            x = dft(v, +1)
            zeros = [j for j, value in enumerate(x) if not any(value)]
            assert zeros == list(range(N - 1))
            assert sum(any(value) for value in x) == M - N + 1
            back = dft(x, -1)
            assert back == [tuple(M * c for c in value) for value in v]
            transform_coordinates += M
            sharpness.append({'M': M, 'N': N, 'support': M - N + 1})

    # Negative-sign target-chain controls include complex and wrapped entries.
    chain_cases = 0
    for M in (4, 8, 16, 32):
        for start in (0, 1, M - 1):
            x = [monomial(M, coefficient=0)] * M
            x[start] = plus(monomial(M, coefficient=3), monomial(M, M // 4, -2))
            x[(start + 2) % M] = monomial(M, coefficient=-5)
            y = dft(dft(x, -1), -1)
            assert y == [tuple(M * a for a in x[-j % M]) for j in range(M)]
            chain_cases += 1

    # A negative control: arbitrary zero positions do not have the interval property.
    M = 8
    x = [monomial(M, coefficient=int(j == 0) - int(j == 4)) for j in range(M)]
    y = dft(x, -1)
    assert [j for j, a in enumerate(y) if not any(a)] == [0, 2, 4, 6]

    M = 1 << 28
    Nlo, Nhi = (1 << 25) + 1, 1 << 26
    compatibility = []
    for N, expected in ((Nlo-1, False), (Nlo, True), (Nhi, True), (Nhi+1, False)):
        accepted = 1 << (4*N - 1).bit_length() == M
        assert accepted == expected
        compatibility.append({'N': N, 'compatible': accepted})
    lower = M - Nhi + 1
    assert lower == 201326593 and lower > 64
    root = isqrt(M)
    assert root * root == M and root == 1 << 14
    gap = 1 - Fraction(1, root) - Fraction(9, 1 << 400)
    assert gap > Fraction(1, 32)
    assert Fraction(4, 1 << 7) == Fraction(1, 32)
    P, t = 16*28 + 16, 32*5*28 + 4
    assert P == 464 and t == 4484 and t < M
    assert 3*M*M*(1 << P) == 3*(1 << 520)
    assert (1 << 480) - 1 < 3*M*M*(1 << P)

    contraction_cases = 0
    for a in range(-256, 257):
        for numerator in range(1, 25):
            for denominator in range(numerator, 25):
                q = Fraction(a*numerator, denominator)
                rounded = rounding_by_nearest_distance(q)
                assert abs(rounded) <= abs(a)
                contraction_cases += 1
    for a in (-(1 << 480) + 1, -1, 0, 1, (1 << 480) - 1):
        for mid in ((1 << 560), (1 << 560) + 1, (1 << 561)-1, (1 << 579)-1):
            rounded = rounding_by_nearest_distance(Fraction(a*(1 << 560), mid))
            assert abs(rounded) <= abs(a) < (1 << 480)
            contraction_cases += 1

    # A fresh one-row Cartesian median model checks shape conversion, including empty.
    median_cases = 0
    for support in ((), (0,), (0, 1, M - 1), tuple(range(16))):
        row = tuple(((-1)**j * ((1 << 479) - j), j - 3) for j in range(len(support)))
        rows = (row,)
        converted = tuple((k, (sorted(r[j][0] for r in rows)[0],
                               sorted(r[j][1] for r in rows)[0])) for j, k in enumerate(support))
        assert converted == tuple(zip(support, row))
        median_cases += 1

    # Static code audit is evidence of what was inspected, not execution of it.
    inspected = {}
    for file in ('checks.py', 'sources/sparse_recovery__candidate__recovery.py',
                 'sources/sparse_recovery__candidate__vendor__vendor__sparse_supplier.py',
                 'sources/sparse_recovery__candidate__vendor__sparse_adapter.py',
                 'sources/outer_stream__candidate__sparse_output.py',
                 'sources/outer_stream__candidate__outer_wrapper.py',
                 'sources/outer_stream__candidate__full_transfer.py'):
        tree = ast.parse((CANDIDATE / file).read_text())
        inspected[file] = {'sha256': digest(CANDIDATE / file)['sha256'],
                           'syntax_parsed': isinstance(tree, ast.Module)}
    after = integrity()
    assert after == before
    result = {
        'status': 'PASS', 'integrity': after,
        'cyclotomic_control': {'method': 'subset dynamic-programming determinant over exact Z[X]/(X^(M/2)+1)',
                               'lengths': [4, 8, 16], 'support_size_max': 4,
                               'all_cyclic_start_rows': True, 'support_sets': support_count,
                               'nonzero_determinants': determinant_count},
        'sharp_support_bound_witnesses': sharpness,
        'sharpness_inverse_transform_coordinates': transform_coordinates,
        'negative_transform_target_chain_cases': chain_cases,
        'nonconsecutive_zero_negative_control': {'M': 8, 'raw_support': 2, 'fourier_zeros': [0,2,4,6]},
        'dimension_boundary_cases': compatibility,
        'support_lower_bound': lower, 'impulse_gap_exceeds': '1/32',
        'impulse_gap_fraction': [gap.numerator, gap.denominator],
        'rounding_contraction_cases': contraction_cases,
        'one_row_median_identity_cases': median_cases,
        'inspected_code': inspected,
        'candidate_checks_executed': False, 'preserved_programs_executed': False,
        'historical_test_counts_used_as_new_evidence': False,
        'integrated_adapter_executed': False, 'numeric_tolerances_used': False,
        'external_writes': False, 'elapsed_seconds': time.monotonic() - started}
    (HERE / 'INDEPENDENT_RESULTS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
