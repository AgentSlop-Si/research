#!/usr/bin/env python3
"""Minimal-state certificate for sequential Fourier moment generation.

For arbitrary x, y_k=sum_j x_j omega^(k j).  Any input-independent scalar
linear recurrence valid for every x must have order at least N: applying it to
x=e_j would give a degree-r polynomial vanishing at all N distinct roots.
Equivalently, a linear time-invariant state-space generator needs at least N
states.  A generic N x N Hankel moment matrix factors as
V diag(x) V^T and has full rank N.
"""
from __future__ import annotations
from typing import Sequence
from permutation_displacement import find_prime_root, rank_mod


def moments_mod(x: Sequence[int], p: int, omega: int, count: int) -> list[int]:
    n = len(x)
    return [sum((x[j] % p) * pow(omega, (k * j) % n, p) for j in range(n)) % p
            for k in range(count)]


def hankel_moment_rank(n: int) -> dict:
    p, omega = find_prime_root(n)
    # Deterministically nonzero modal weights.
    x = [(j + 1) % p or 1 for j in range(n)]
    y = moments_mod(x, p, omega, 2 * n - 1)
    h = [[y[i + j] for j in range(n)] for i in range(n)]
    r = rank_mod(h, p)
    if r != n:
        raise AssertionError((n, r))
    return {"n": n, "prime": p, "hankel_rank": r, "minimal_state_lower_bound": n}


def recurrence_polynomial_impossibility(n: int, order: int) -> bool:
    """Degree counting certificate: no monic order-r polynomial has N roots."""
    if not 0 <= order < n:
        raise ValueError("need 0<=order<n")
    # This function records the exact symbolic reason rather than searching
    # coefficients: a nonzero degree-r polynomial over a field has <=r roots.
    return n > order


if __name__ == "__main__":
    import json
    print(json.dumps({
        "hankel": [hankel_moment_rank(n) for n in (5, 7, 8, 9, 16, 25, 32, 49)],
        "degree_certificates": [
            {"n": n, "order": r, "impossible": recurrence_polynomial_impossibility(n, r)}
            for n in (8, 16, 32) for r in (1, 2, n // 2, n - 1)
        ],
    }, indent=2))
