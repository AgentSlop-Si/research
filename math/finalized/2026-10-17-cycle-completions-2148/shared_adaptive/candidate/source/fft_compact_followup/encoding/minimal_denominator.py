#!/usr/bin/env python3
"""Minimal collected-product denominator for the compact binomial quotient.

The minimum is d=lcm(1,...,r)/r, rather than the larger denominator needed to
reduce every high basis vector separately. The proof is in this directory.
Existing modules are imported read-only; individual high folds need not be
integral, while the complete collected multiplication is integral.
"""
from dataclasses import dataclass
from pathlib import Path
import sys
from time import perf_counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "fft_next" / "compact_newton"))
sys.path.insert(0, str(ROOT / "fft_next" / "transfer"))
from compact_binomial import lcm_range, primes_through, prime_power_in
from compact_binomial import encode_integer, evaluate
from modular_compiler import exact_product as previous_exact_product
from modular_compiler import fields_for_bound, modular_product, next_power_of_two
from local_carry import CarryPlan, Counts, normalize_to_Q
from local_carry import normalize_rows as previous_normalize_rows
from monic_baseline import MonicPlan


@dataclass(frozen=True)
class Plan:
    r: int
    denominator: int
    radix_lcm: int
    k: int
    point: int
    block_base: int
    weights: tuple[int, ...]
    point_choice: str
    scale_denominator: int = 1


def plan_at_point(r, point, point_choice="supplied point", *, rational=False):
    if not isinstance(r, int) or r < 2:
        raise ValueError("r must be an integer at least two")
    L = lcm_range(r)
    d = L // r
    scale_denominator = L // lcm_range(r - 1) if rational else 1
    if point <= 1 or (point - 1) % L:
        raise ValueError("need P=1+k L with positive integer k")
    k = (point - 1) // L
    weights = [1]
    for j in range(1, r + 1):
        weights.append(weights[-1] * (1 + (point - 1) // j))
    Q = weights.pop()
    if Q % d:
        raise ValueError("minimal denominator does not divide B_r(P)")
    beta = (Q // d) * scale_denominator
    if beta <= weights[-1]:
        raise ValueError("top retained weight does not fit in a block")
    return Plan(r, d, L, k, point, beta, tuple(weights), point_choice,
                scale_denominator)


def make_plan(r, *, rational=False):
    """An exact uniform producer; no added D or exponential CRT offset."""
    if not isinstance(r, int) or r < 2:
        raise ValueError("r must be an integer at least two")
    L = lcm_range(r)
    d = L // r
    k0, modulus = 0, 1
    for ell in primes_through(r):
        mod = prime_power_in(d, ell)
        if mod == 1:
            continue
        m = prime_power_in(L, ell)
        residue = -pow(L // m, -1, mod) % mod
        step = (residue - k0) * pow(modulus, -1, mod) % mod
        k0 += modulus * step
        modulus *= mod
    if modulus != d:
        raise ArithmeticError("incomplete CRT factorization")
    k = k0 if d > 1 else 1
    if not 1 <= k <= max(1, d - 1):
        raise ArithmeticError("CRT unit residue was not positive")
    return plan_at_point(r, 1 + k * L,
                         "least positive residue in the stated CRT class",
                         rational=rational)


def capacity_tuned_plan(r, target_base, *, upper_point, rational=False):
    """Least P in the stated CRT progression whose beta reaches target_base.

    Returns (plan, setup_report). The supplied previous point is normally an
    admissible upper bound. If not in this CRT class it is rounded upwards
    to a class member; if too small, explicit counted doubling supplies a
    valid bound. Every tested beta is computed exactly.
    """
    started = perf_counter()
    if not isinstance(target_base, int) or target_base <= 0:
        raise ValueError("target_base must be a positive integer")
    native = make_plan(r, rational=rational)
    L, d, k0, e = (native.radix_lcm, native.denominator,
                    native.k, native.scale_denominator)
    evaluations = 0

    def beta_at_index(t):
        nonlocal evaluations
        evaluations += 1
        k = k0 + t * d
        Q = 1
        for j in range(1, r + 1):
            Q *= 1 + k * L // j
        if Q % d:
            raise ArithmeticError("CRT progression lost its divisibility")
        return (Q // d) * e

    native_beta = beta_at_index(0)
    if native_beta >= target_base:
        index, beta = 0, native_beta
    else:
        # Round the supplied upper point upwards in P=1+(k0+t*d)*L.
        step = d * L
        high = max(1, (upper_point - 1 - k0 * L + step - 1) // step)
        high_beta = beta_at_index(high)
        while high_beta < target_base:
            high *= 2
            high_beta = beta_at_index(high)
        low = 0
        while high - low > 1:
            middle = (low + high) // 2
            middle_beta = beta_at_index(middle)
            if middle_beta >= target_base:
                high, high_beta = middle, middle_beta
            else:
                low = middle
        index, beta = high, high_beta
    point = 1 + (k0 + index * d) * L
    result = plan_at_point(r, point, "least point in stated CRT family meeting capacity",
                           rational=rational)
    if result.block_base != beta or result.block_base < target_base:
        raise ArithmeticError("capacity search result does not meet target")
    return result, {
        "family": "minimal denominator CRT progression",
        "target_base_bits": target_base.bit_length(),
        "progression_index": index,
        "beta_predicate_evaluations": evaluations,
        "setup_seconds": perf_counter() - started,
        "scope": "exact minimum in the declared progression, not all possible compact evaluation points",
    }


def monic_capacity_tuned_plan(r, target_base, *, upper_point):
    """Least positive integer P with prod_(j<r)(P+j)>=target_base."""
    started = perf_counter()
    if not isinstance(r, int) or r < 2:
        raise ValueError("r must be an integer at least two")
    if not isinstance(target_base, int) or target_base <= 0:
        raise ValueError("target_base must be a positive integer")
    evaluations = 0

    def beta_at_point(point):
        nonlocal evaluations
        evaluations += 1
        Q = 1
        for j in range(r):
            Q *= point + j
        return Q

    low, high = 0, max(1, upper_point)
    high_beta = beta_at_point(high)
    while high_beta < target_base:
        high *= 2
        high_beta = beta_at_point(high)
    while high - low > 1:
        middle = (low + high) // 2
        middle_beta = beta_at_point(middle)
        if middle_beta >= target_base:
            high, high_beta = middle, middle_beta
        else:
            low = middle
    weights = [1]
    for j in range(r):
        weights.append(weights[-1] * (high + j))
    result = MonicPlan(r, high, weights[-1], tuple(weights[:-1]))
    if result.block_base != high_beta or result.block_base < target_base:
        raise ArithmeticError("monic capacity search failed")
    return result, {
        "family": "all positive integer monic evaluation points",
        "target_base_bits": target_base.bit_length(),
        "beta_predicate_evaluations": evaluations,
        "setup_seconds": perf_counter() - started,
        "scope": "exact least positive integer point meeting the target",
    }


@dataclass(frozen=True)
class UnitCarryPlan:
    radices: tuple[int, ...]
    denominator: int = 1


def carry_plan(plan):
    scale_denominator = getattr(plan, "scale_denominator", 1)
    if plan.denominator > 1 and scale_denominator == 1:
        return CarryPlan.from_binomial_plan(plan)
    radices = [1 + (plan.point - 1) // j for j in range(1, plan.r + 1)]
    radices[-1] *= scale_denominator
    if plan.denominator == 1:
        return UnitCarryPlan(tuple(radices))
    # Multiplying the final radix changes Q to eQ, without changing any
    # retained weight. beta=eQ/d is thus covered by the same integer carry
    # theorem, with denominator d and the enlarged final radix.
    value = plan.block_base
    digits = []
    for R in radices:
        value, digit = divmod(value, R)
        digits.append(digit)
    if value or not any(digits) or radices[-1] <= plan.denominator:
        raise ArithmeticError("invalid rational-scale carry plan")
    return CarryPlan(tuple(radices), plan.denominator, tuple(digits))


def exact_product(a, b, plan):
    if getattr(plan, "scale_denominator", 1) == 1:
        return previous_exact_product(a, b, plan)
    r, la, lb = plan.r, len(a[0]), len(b[0])
    height_a = max(abs(value) for row in a for value in row)
    height_b = max(abs(value) for row in b for value in row)
    unrestricted = r * r * 3 ** (2 * r - 2) * min(la, lb) * height_a * height_b
    num = unrestricted * (plan.scale_denominator + (r - 1) * plan.denominator)
    bound = (num + plan.scale_denominator - 1) // plan.scale_denominator
    if bound == 0:
        return [[0] * (la + lb) for _ in range(r)], {"primes": [], "bound_bits": 0}
    maxlen = max(next_power_of_two(4 * r - 3), next_power_of_two(la + lb))
    result, modulus, reports = [[0] * (la + lb) for _ in range(r)], 1, []
    for arithmetic in fields_for_bound(maxlen, bound, 2 * r):
        p = arithmetic.prime
        field_scale = plan.denominator * pow(plan.scale_denominator, -1, p) % p
        proxy = type("LocalPlan", (), {"r": r, "denominator": field_scale})()
        residues = modular_product(a, b, proxy, arithmetic)
        inverse_modulus = pow(modulus, -1, p)
        for j in range(r):
            for t in range(la + lb):
                delta = (residues[j][t] - result[j][t]) * inverse_modulus % p
                result[j][t] += modulus * delta
        modulus *= p
        reports.append({"prime": p, **arithmetic.counts})
    if modulus <= 2 * bound:
        raise ArithmeticError("insufficient CRT modulus")
    result = [[value - modulus if value > modulus // 2 else value for value in row]
              for row in result]
    if any(abs(value) > bound for row in result for value in row):
        raise ArithmeticError("reconstructed coefficient exceeds uniform bound")
    return result, {"primes": reports, "bound_bits": bound.bit_length(),
                    "modulus_bits": modulus.bit_length(),
                    "maximum_ntt_length": maxlen}


def normalize_rows(rows, prepared, counts=None):
    if prepared.denominator > 1:
        return previous_normalize_rows(rows, prepared, counts)
    # For d=1, beta=Q is exactly the ordinary product of the short radices.
    # There is no truncated top digit or second normalization pass.
    if counts is None:
        counts = Counts()
    r = len(prepared.radices)
    if len(rows) != r or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("wrong or ragged channel array")
    out = [[] for _ in range(r)]
    carry, index = 0, 0
    while index < len(rows[0]) or carry:
        if index >= len(rows[0]) and carry < 0:
            raise ValueError("normalize the magnitude and handle the sign separately")
        block = [row[index] if index < len(row) else 0 for row in rows]
        counts.local_blocks += 1
        carry, digits = normalize_to_Q(block, prepared.radices, carry, counts)
        for j, digit in enumerate(digits):
            out[j].append(digit)
        index += 1
    if not out[0]:
        return [[0] for _ in range(r)]
    while len(out[0]) > 1 and all(row[-1] == 0 for row in out):
        for row in out:
            row.pop()
    return out


def multiply_integer(a, b, plan):
    left = encode_integer(abs(a), plan)
    right = encode_integer(abs(b), plan)
    raw, report = exact_product(left, right, plan)
    counts = Counts()
    canonical = normalize_rows(raw, carry_plan(plan), counts)
    sign = -1 if (a < 0) != (b < 0) else 1
    return sign * evaluate(canonical, plan), report, counts
