#!/usr/bin/env python3
"""Exact rational covariance certificates for v14 unequal blocks."""
from __future__ import annotations

from fractions import Fraction
import math
import numpy as np

from arbitrary_block_core import balanced_partition


def factor_trial(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("n must be positive")
    out: dict[int, int] = {}
    z = n
    while z % 2 == 0:
        out[2] = out.get(2, 0) + 1
        z //= 2
    p = 3
    while p * p <= z:
        while z % p == 0:
            out[p] = out.get(p, 0) + 1
            z //= p
        p += 2
    if z > 1:
        out[z] = out.get(z, 0) + 1
    return out


def euler_phi(n: int) -> int:
    result = n
    for p in factor_trial(n):
        result -= result // p
    return result


def displacement_weight(n: int, d: int) -> Fraction:
    if d <= 0:
        raise ValueError("d must be positive")
    return Fraction(1, euler_phi(n // math.gcd(n, d)))


def overlap_variance_factor_lengths(n: int, lengths: list[int] | np.ndarray) -> Fraction:
    """Diagonal-domination certificate for arbitrary contiguous block lengths.

    For a position t in a block of length L, the active positive/negative
    displacements are 1..t and 1..L-1-t.  Each displacement d contributes at
    most 1/phi(N/gcd(N,d)) to the covariance operator at that position.
    """
    lens = [int(v) for v in lengths]
    if not lens or sum(lens) != n:
        raise ValueError("lengths must be a positive partition of n")
    if 2 * (max(lens) - 1) >= n:
        raise ValueError("displacement differences may wrap modulo n")
    max_len = max(lens)
    prefix = [Fraction(0, 1)] * max_len
    running = Fraction(0, 1)
    for d in range(1, max_len):
        running += displacement_weight(n, d)
        prefix[d] = running
    best = Fraction(0, 1)
    for ell in lens:
        for t in range(ell):
            value = prefix[t] + prefix[ell - 1 - t]
            if value > best:
                best = value
    return best


def balanced_overlap_variance_factor(n: int, blocks: int) -> Fraction:
    _, lengths, _ = balanced_partition(n, blocks)
    return overlap_variance_factor_lengths(n, lengths)


def old_triangle_variance_factor(n: int, max_length: int) -> Fraction:
    total = Fraction(0, 1)
    for d in range(1, max_length):
        total += 2 * displacement_weight(n, d)
    return total


def equal_block_overlap_variance_factor(n: int, m: int) -> Fraction:
    if n % m:
        raise ValueError("m must divide n")
    return overlap_variance_factor_lengths(n, [m] * (n // m))


def prime_balanced_closed_form(n: int, blocks: int) -> Fraction:
    """Closed form for prime n: (ceil(n/B)-1)/(n-1)."""
    if len(factor_trial(n)) != 1 or next(iter(factor_trial(n).values())) != 1:
        raise ValueError("n must be prime")
    max_len = (n + blocks - 1) // blocks
    return Fraction(max_len - 1, n - 1)


def least_prime_equal_block_closed_form(n: int) -> tuple[int, Fraction]:
    factors = factor_trial(n)
    if len(factors) == 1 and next(iter(factors.values())) == 1:
        raise ValueError("n must be composite")
    p = min(factors)
    if n % p:
        raise AssertionError
    return p, Fraction(p - 1, euler_phi(n))


def bulk_bad_fraction_expectation_bound(variance_factor: float, tolerance: float) -> float:
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    return min(1.0, variance_factor / (tolerance * tolerance))


def variance_only_rows_for_union(
    n: int,
    variance_factor: float,
    tolerance: float,
    target_failure: float,
) -> int:
    """Smallest odd row count certified by Chebyshev+median+union."""
    if not (0 < target_failure < 1):
        raise ValueError("target_failure must lie in (0,1)")
    component_margin = tolerance / math.sqrt(2.0)
    p = min(1.0, variance_factor / (component_margin * component_margin))
    if p >= 0.5:
        return -1
    rows = 1
    while rows < 100000:
        majority = (rows + 1) // 2
        bound = 2.0 * n * (2.0**rows) * (p**majority)
        if bound <= target_failure:
            return rows
        rows += 2
    return -1
