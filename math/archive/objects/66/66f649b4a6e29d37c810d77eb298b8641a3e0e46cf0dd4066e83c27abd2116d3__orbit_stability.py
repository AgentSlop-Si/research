"""Joint primitive-orbit stability limits for fresh binary FFTs.

Pure Python theorem checks. The analytical theorem is in RESEARCH.md.
Optional NumPy/SciPy/mpmath are used only in experiment.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil, isqrt


def is_power_of_two(n: int) -> bool:
    return n >= 2 and (n & (n - 1)) == 0


def canonical_representatives(n: int) -> tuple[int, ...]:
    """One per rational cyclotomic conductor orbit, for n a power of two."""
    if not is_power_of_two(n):
        raise ValueError("n must be a power of two >=2")
    return (0,) + tuple(1 << i for i in range(n.bit_length() - 1))


def complementary_signal(u: int, n: int) -> tuple[int, ...]:
    """x=(u, 1-u) with independent binary bits u, little-endian."""
    if not is_power_of_two(n) or not (0 <= u < (1 << (n // 2))):
        raise ValueError("invalid length or bitmask")
    m = n // 2
    bits = tuple((u >> j) & 1 for j in range(m))
    return bits + tuple(1 - t for t in bits)


def folded_odd_coefficients(u: int, n: int) -> tuple[int, ...]:
    """Coefficients of odd spectral values in power basis (2u_j-1)."""
    x = complementary_signal(u, n)
    m = n // 2
    return tuple(x[j] - x[j + m] for j in range(m))


def theoretical_lipschitz_bound(n: int, r: int = 1) -> dict:
    """Combinatorial packing bound for decoding all unnormalized bins from r odd bins.

    Restrict to x=(u,1-u), 2^(n/2) different binary inputs.  All even
    frequencies are constant; each odd frequency lies in the disk |z|<=n/2.

    Split each real coordinate into M equal intervals where M=2^floor(m/(2r))-1.
    There are strictly fewer than 2^m cells if M>=1.  Some pair satisfies
    ||measured difference||_inf <= 2 sqrt(2) m/M (complex norm), whereas
    ||full DFT difference||_inf >= sqrt(2) by Parseval.
    Therefore any Lipschitz all-spectrum decoder has L>=M/(2m)=M/n.
    """
    if not is_power_of_two(n) or r < 1 or r > n // 2:
        raise ValueError("invalid n or number of odd representatives")
    m = n // 2
    expo = m // (2 * r)
    cells_per_real_dimension = (1 << expo) - 1 if expo >= 1 else 0
    # Underflow to 0 indicates a vacuous bound at large r.
    return {
        "N": n,
        "m": m,
        "odd_measured": r,
        "input_family_size_bits": m,
        "exponent_floor": expo,
        "M": cells_per_real_dimension,
        "lipschitz_lower_bound_numerator": cells_per_real_dimension,
        "lipschitz_lower_bound_denominator": n,
        "vacuous": cells_per_real_dimension == 0,
    }


def identical_even_spectrum(n: int) -> tuple[int, ...]:
    """Even-frequency bins for all (u,1-u), exact integer values."""
    if not is_power_of_two(n):
        raise ValueError("n power of 2 required")
    return (n // 2,) + (0,) * (n // 2 - 1)


def necessary_odd_representatives(n: int, lipschitz_upper: int) -> int:
    """Necessary integer r from the packing bound (not sufficient!)."""
    if not is_power_of_two(n) or lipschitz_upper < 0:
        raise ValueError("invalid n or Lipschitz bound")
    m = n // 2
    for r in range(1, m + 1):
        b = theoretical_lipschitz_bound(n, r)
        if b["M"] <= n * lipschitz_upper:
            return r
    return m
