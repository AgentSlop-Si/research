#!/usr/bin/env python3
"""Fresh exact controls for the balanced-divisor higher-rank theorem.

This imports no project/source scientific implementation. It uses no float
arithmetic, numerical ranks, MILP solver, or claimed exhaustive tiling search.
"""
import hashlib
import json
import math
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent


def nearest_pair(n):
    d = math.isqrt(n)
    while n % d:
        d -= 1
    return d, n // d


def prime(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, math.isqrt(n) + 1))


def prime_factors(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def splitting_field(n):
    k = 1
    while not prime(k * n + 1):
        k += 1
    p = k * n + 1
    factors = prime_factors(p - 1)
    generator = next(g for g in range(2, p)
                     if all(pow(g, (p - 1) // q, p) != 1 for q in factors))
    omega = pow(generator, (p - 1) // n, p)
    assert pow(omega, n, p) == 1
    assert all(pow(omega, n // q, p) != 1 for q in prime_factors(n))
    return p, omega


def rank_mod(matrix, p):
    a = [row[:] for row in matrix]
    m, n = len(a), len(a[0])
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, m) if a[i][col] % p), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], p - 2, p)
        a[rank] = [(x * inv) % p for x in a[rank]]
        for i in range(rank + 1, m):
            factor = a[i][col]
            if factor:
                a[i] = [(x - factor * y) % p
                        for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == min(m, n):
            break
    return rank


def scalar_shapes():
    eligible = []
    tested = 0
    smallest_integer_gap = None
    for n in range(2, 161):
        d, e = nearest_pair(n)
        D = d + e
        if D * D >= 8 * n:
            continue
        eligible.append(n)
        for a in range(1, n + 1):
            for b in range(1, n + 1):
                r = max(2, (a * b + n - 1) // n)
                if r > min(a, b):
                    continue
                assert a * b <= n * r
                gap = n * r * (a + b) - D * a * b
                assert gap > 0, (n, a, b, r, D)
                tested += 1
                if smallest_integer_gap is None or gap < smallest_integer_gap:
                    smallest_integer_gap = gap
    return {"length_range": [2, 160], "eligible_lengths": eligible,
            "feasible_minimal_rank_shapes": tested,
            "smallest_strict_integer_gap": smallest_integer_gap}


def coset_constructions():
    checked_tiles = checked_entries = checked_differences = 0
    examples = {}
    eligible_count = 0
    for n in range(2, 129):
        d, e = nearest_pair(n)
        D = d + e
        assert D == min(k + n // k for k in range(1, n + 1) if n % k == 0)
        # Equivalent forms of the balanced-divisor criterion, without roots.
        assert (D * D < 8 * n) == (e * e - 6 * d * e + d * d < 0)
        assert D * D != 8 * n
        eligible_count += D * D < 8 * n
        coverage = bytearray(n * n)
        cost = 0
        for u in range(e):
            rows = [u + k * e for k in range(d)]
            for v in range(d):
                cols = [v + ell * d for ell in range(e)]
                assert len(rows) * len(cols) == n
                # The chosen row/column base is enough for every 2x2 minor.
                for row in rows:
                    for col in cols:
                        assert (row - rows[0]) * (col - cols[0]) % n == 0
                        checked_differences += 1
                        idx = n * row + col
                        assert not coverage[idx]
                        coverage[idx] = 1
                        checked_entries += 1
                cost += len(rows) + len(cols)
                checked_tiles += 1
        assert all(coverage)
        assert cost == n * D
        if n in [6, 10, 22, 27, 35, 125]:
            examples[str(n)] = {"d": d, "e": e, "D": D, "cost": cost,
                                "balanced_domain": D * D < 8 * n}
    return {"length_range": [2, 128], "eligible_lengths_count": eligible_count,
            "tiles": checked_tiles, "covered_entries": checked_entries,
            "divisibility_checks": checked_differences, "examples": examples}


def sampled_fourier_ranks():
    rng = random.Random(20261018)
    lengths = [10, 12, 14, 15, 18, 20, 21, 22, 24, 27, 32, 35,
               39, 45, 50, 51, 75, 125]
    cases = []
    count = rank_one_count = higher_rank_count = 0
    for n in lengths:
        d, e = nearest_pair(n)
        D = d + e
        assert D * D < 8 * n
        p, omega = splitting_field(n)
        powers = [pow(omega, k, p) for k in range(n)]
        row_col_pairs = []
        # Algebraic rank-one coset controls; avoid rerunning the earlier
        # exhaustive N=2..8 rectangle census.
        row_col_pairs.append(([k * e for k in range(d)],
                              [ell * d for ell in range(e)]))
        # Contiguous equal-side blocks have a Vandermonde determinant.
        for size in [2, min(n, 5), min(n, 9)]:
            row_col_pairs.append((list(range(size)), list(range(size))))
        for _ in range(40):
            a = rng.randint(2, min(n, 14))
            b = rng.randint(2, min(n, 14))
            row_col_pairs.append((sorted(rng.sample(range(n), a)),
                                  sorted(rng.sample(range(n), b))))
        for rows, cols in row_col_pairs:
            matrix = [[powers[(-r * c) % n] for c in cols] for r in rows]
            rank = rank_mod(matrix, p)
            a, b = len(rows), len(cols)
            assert rank >= 1
            # This is a concrete modular control, not an assumption that
            # the complex singular-value argument transfers to finite fields.
            if rank == 1:
                assert all((r - rows[0]) * (c - cols[0]) % n == 0
                           for r in rows for c in cols)
                assert n * (a + b) >= D * a * b
                rank_one_count += 1
            else:
                assert n * rank * (a + b) > D * a * b
                higher_rank_count += 1
            if rows == cols == list(range(a)):
                assert rank == a
            count += 1
        cases.append({"N": n, "prime": p, "primitive_root": omega,
                      "submatrix_count": len(row_col_pairs)})
    return {"total_submatrices": count, "rank_one_controls": rank_one_count,
            "higher_rank_controls": higher_rank_count, "cases": cases,
            "qualification": "Supplementary exact modular minors only; the universal proof is complex."}


def boundary_and_families():
    n, a, b, r = 26, 7, 7, 2
    d, e = nearest_pair(n)
    D = d + e
    assert (d, e, D) == (2, 13, 15)
    assert D * D > 8 * n
    assert a * b <= n * r and 2 <= r <= min(a, b)
    assert n * r * (a + b) == 728 < 735 == D * a * b
    n, a, b, r, D = 57, 10, 11, 2, 22
    assert nearest_pair(n) == (3, 19)
    assert D * D > 8 * n and a * b <= n * r
    assert n * r * (a + b) == 2394 < 2420 == D * a * b
    twice_prime_shapes = 0
    excluded_full_column_candidates = 0
    for p in range(3, 150):
        if not prime(p):
            continue
        n, D = 2 * p, p + 2
        assert nearest_pair(n) == (2, p)
        for a in range(2, n + 1):
            for b in range(a, n + 1):
                r = max(2, (a + 1) // 2)
                # A full-column Fourier rectangle has independent rows.
                if b == n:
                    if a == 4 and r == 2:
                        excluded_full_column_candidates += 1
                    r = a
                assert n * r * (a + b) > D * a * b
                twice_prime_shapes += 1
    # Infinite-family formulas are algebraically proved in REPORT.md.
    # These integer checks corroborate representative exponents only.
    family_cases = []
    for p in (2, 3, 5):
        assert (p + 1) ** 2 < 8 * p
        for k in range(8):
            n = p ** (2 * k + 1)
            d, e = p ** k, p ** (k + 1)
            assert d * e == n
            assert (d + e) ** 2 < 8 * n
            assert n * (d + e) == p ** (3 * k + 1) * (p + 1)
            family_cases.append({"p": p, "k": k, "N": n,
                                 "objective": n * (d + e)})
    return {"initial_relaxation_counterexample": {"N": 26, "a": 7, "b": 7, "r": 2,
            "stable_rank_guard": "49 <= 52", "failed_density_guard": "728 < 735",
            "not_an_actual_fourier_counterexample": True},
            "residual_relaxation_counterexample": {"N": 57, "a": 10, "b": 11, "r": 2,
            "stable_rank_guard": "110 <= 114", "failed_density_guard": "2394 < 2420",
            "not_an_actual_fourier_counterexample": True},
            "twice_prime_minimal_rank_shapes": twice_prime_shapes,
            "excluded_full_column_equality_candidates": excluded_full_column_candidates,
            "prime_power_cases": family_cases}


def main():
    source = (HERE / "SOURCE_PHASE7_AUDIT.md").read_bytes()
    expected = "ed3a259cc88ecb2cf12092f612aabaeb917885fe84147cf2feb99802d1fd32c4"
    digest = hashlib.sha256(source).hexdigest()
    assert digest == expected, (digest, expected)
    git_blob = hashlib.sha1(b"blob " + str(len(source)).encode() + b"\0" + source).hexdigest()
    assert git_blob == "58be131bc82c3ccc7dfb15b435d01bd9edd17942"
    result = {"status": "PASS", "source_sha256": digest, "source_git_blob": git_blob,
              "no_original_scientific_program_imported_or_executed": True,
              "scalar_shapes": scalar_shapes(),
              "coset_constructions": coset_constructions(),
              "sampled_fourier_ranks": sampled_fourier_ranks(),
              "boundary_and_families": boundary_and_families()}
    (HERE / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    summary = {"status": result["status"],
               "scalar_shapes": result["scalar_shapes"]["feasible_minimal_rank_shapes"],
               "coset_tiles": result["coset_constructions"]["tiles"],
               "sampled_submatrices": result["sampled_fourier_ranks"]["total_submatrices"],
               "source_hash_verified": True}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
