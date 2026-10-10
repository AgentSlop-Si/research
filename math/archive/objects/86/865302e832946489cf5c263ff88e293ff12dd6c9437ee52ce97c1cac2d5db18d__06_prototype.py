#!/usr/bin/env python3
"""All-length near-grid lift for the unit-step chirp Fourier sketch (v10).

For an arbitrary length N, lift to Q=2^ceil(log2 N), map every target
frequency k/N to its nearest Q-grid point j_k/Q, and approximate the residual
phase exp(-2*pi*i*theta_k*n/Q) by a truncated Taylor expansion.  Each Taylor
term is a dyadic Q-point DFT and is evaluated by the v9 unit-step chirp row.

The code is a research prototype.  It prioritizes explicit formulas,
independent checks, and fully charged operation counts over production speed.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import numpy.typing as npt
from scipy.special import jv

import unit_step_core as core

ComplexArray = npt.NDArray[np.complex128]


def next_power_of_two(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return 1 << (n - 1).bit_length()


def choose_dyadic_block(q: int) -> int:
    """Choose a power-of-two M=Theta(log Q) with M^2<=Q."""
    if q < 2 or q & (q - 1):
        raise ValueError("q must be a power of two")
    if q <= 4:
        return 1
    target = max(1.0, math.log2(q))
    m = 1 << int(math.floor(math.log2(target)))
    while m * m > q:
        m //= 2
    return max(1, m)


def nearest_grid_map(n: int, q: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Return injective nearest-grid indices j_k and offsets theta_k.

    theta_k = k*Q/N - j_k lies in [-1/2,1/2].  Since Q>=N, nearest rounded
    indices are strictly increasing before the harmless modulo operation.
    """
    if q is None:
        q = next_power_of_two(n)
    if q < n:
        raise ValueError("q must be at least n")
    k = np.arange(n, dtype=np.float64)
    scaled = k * (q / n)
    nearest = np.floor(scaled + 0.5).astype(np.int64)
    theta = scaled - nearest.astype(np.float64)
    indices = nearest % q
    if np.max(np.abs(theta), initial=0.0) > 0.500000000001:
        raise AssertionError("nearest-grid offset exceeded one half")
    if np.unique(indices).size != n:
        raise AssertionError("nearest-grid map is not injective")
    return indices, theta


def taylor_tail_bound(rank: int) -> float:
    """Uniform tail for exp(i*y), |y|<=pi: pi^rank/rank!."""
    if rank < 0:
        raise ValueError("rank must be nonnegative")
    return math.pi**rank / math.factorial(rank)


def rank_for_tail(tol: float) -> int:
    if not (0.0 < tol < 1.0):
        raise ValueError("tol must lie in (0,1)")
    rank = 0
    while taylor_tail_bound(rank) > tol:
        rank += 1
    return rank


def normalized_dft(x: npt.ArrayLike) -> ComplexArray:
    arr = np.asarray(x, dtype=np.complex128)
    return np.fft.fft(arr) / math.sqrt(arr.size)


def _term_coefficients(theta: np.ndarray, rank: int) -> list[np.ndarray]:
    coeffs: list[np.ndarray] = []
    cur = np.ones_like(theta, dtype=np.complex128)
    coeffs.append(cur.copy())
    if rank == 0:
        return []
    z = -2j * math.pi * theta
    for r in range(1, rank):
        cur = cur * z / r
        coeffs.append(cur.copy())
    return coeffs



def bessel_tail_bound(rank: int) -> float:
    """Uniform Jacobi--Anger tail on s in [0,1], theta in [-1/2,1/2].

    e^{-2*pi*i*s*theta} = J_0(pi*s)
      + 2 sum_{r>=1} (-i)^r J_r(pi*s) T_r(2*theta).

    The bound follows from
      |J_r(z)| <= (z/2)^r/r! * exp(z^2/(4(r+1)))
    and a geometric majorant for the remaining exponential-series tail.
    """
    if rank < 1:
        return float("inf")
    a = math.pi / 2.0
    if rank + 1 <= a:
        return float("inf")
    return (
        2.0
        * math.exp(math.pi * math.pi / (4.0 * (rank + 1)))
        * (a**rank / math.factorial(rank))
        / (1.0 - a / (rank + 1))
    )


def bessel_rank_for_tail(tol: float) -> int:
    if not (0.0 < tol < 1.0):
        raise ValueError("tol must lie in (0,1)")
    rank = 1
    while bessel_tail_bound(rank) > tol:
        rank += 1
    return rank


def _chebyshev_values(x: np.ndarray, rank: int) -> list[np.ndarray]:
    if rank <= 0:
        return []
    vals = [np.ones_like(x, dtype=np.float64)]
    if rank == 1:
        return vals
    vals.append(x.astype(np.float64).copy())
    for _ in range(2, rank):
        vals.append(2.0 * x * vals[-1] - vals[-2])
    return vals


def lifted_exact_bessel(x: npt.ArrayLike, rank: int) -> ComplexArray:
    """Stable Jacobi--Anger/Chebyshev lift using exact NumPy Q-FFTs."""
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_power_of_two(n)
    indices, theta = nearest_grid_map(n, q)
    cheb = _chebyshev_values(2.0 * theta, rank)
    s = np.arange(q, dtype=np.float64) / q
    out = np.zeros(n, dtype=np.complex128)
    for r in range(rank):
        padded = np.zeros(q, dtype=np.complex128)
        padded[:n] = arr * jv(r, math.pi * s[:n])
        f = normalized_dft(padded)
        coeff = 1.0 if r == 0 else 2.0 * ((-1j) ** r)
        out += coeff * cheb[r] * f[indices]
    return math.sqrt(q / n) * out


def lifted_direct_bessel_kernel(x: npt.ArrayLike, rank: int) -> ComplexArray:
    """Independent O(N^2) evaluation of the truncated Bessel kernel."""
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_power_of_two(n)
    indices, theta = nearest_grid_map(n, q)
    ss = np.arange(n, dtype=np.float64) / q
    cheb = _chebyshev_values(2.0 * theta, rank)
    out = np.empty(n, dtype=np.complex128)
    nn = np.arange(n, dtype=np.float64)
    for k in range(n):
        p = jv(0, math.pi * ss).astype(np.complex128)
        for r in range(1, rank):
            p += 2.0 * ((-1j) ** r) * jv(r, math.pi * ss) * cheb[r][k]
        phase = np.exp(-2j * math.pi * indices[k] * nn / q)
        out[k] = np.dot(arr * p, phase) / math.sqrt(n)
    return out


def lifted_bessel_chirp_row(
    x: npt.ArrayLike,
    rank: int,
    block: int,
    state: core.ChirpState,
    dtype: Any = np.complex128,
) -> ComplexArray:
    """One v9 row combined through the stable Jacobi--Anger lift."""
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_power_of_two(n)
    core.validate_dimensions(q, block)
    state.validate(q)
    indices, theta = nearest_grid_map(n, q)
    cheb = _chebyshev_values(2.0 * theta, rank)
    s = np.arange(q, dtype=np.float64) / q
    out = np.zeros(n, dtype=np.complex128)
    for r in range(rank):
        padded = np.zeros(q, dtype=np.complex128)
        padded[:n] = arr * jv(r, math.pi * s[:n])
        row = core.one_row_estimate(padded, block, state, dtype).astype(np.complex128)
        coeff = 1.0 if r == 0 else 2.0 * ((-1j) ** r)
        out += coeff * cheb[r] * row[indices]
    return math.sqrt(q / n) * out

def lifted_exact_taylor(x: npt.ArrayLike, rank: int) -> ComplexArray:
    """Taylor-lift approximation using exact NumPy Q-point FFTs."""
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_power_of_two(n)
    indices, theta = nearest_grid_map(n, q)
    coeffs = _term_coefficients(theta, rank)
    s = np.arange(q, dtype=np.float64) / q
    power = np.ones(n, dtype=np.float64)
    out = np.zeros(n, dtype=np.complex128)
    for r in range(rank):
        padded = np.zeros(q, dtype=np.complex128)
        padded[:n] = arr * power
        f = normalized_dft(padded)
        out += coeffs[r] * f[indices]
        power *= s[:n]
    return math.sqrt(q / n) * out


def lifted_direct_kernel(x: npt.ArrayLike, rank: int) -> ComplexArray:
    """Independent O(N^2) evaluation of the truncated separable kernel."""
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_power_of_two(n)
    indices, theta = nearest_grid_map(n, q)
    nn = np.arange(n, dtype=np.float64)
    ss = nn / q
    out = np.empty(n, dtype=np.complex128)
    for k in range(n):
        z = -2j * math.pi * theta[k] * ss
        p = np.ones(n, dtype=np.complex128)
        term = np.ones(n, dtype=np.complex128)
        for r in range(1, rank):
            term *= z / r
            p += term
        phase = np.exp(-2j * math.pi * indices[k] * nn / q)
        out[k] = np.dot(arr * p, phase) / math.sqrt(n)
    return out


def lifted_chirp_row(
    x: npt.ArrayLike,
    rank: int,
    block: int,
    state: core.ChirpState,
    dtype: Any = np.complex128,
) -> ComplexArray:
    """One unbiased row for the truncated all-length approximation.

    The same random dyadic projection is used for every Taylor term.  For a
    fixed output k, linearity combines the terms into one v9 row applied to
    z_k[n]=x[n] p_rank(-2*pi*i*theta_k*n/Q).  This is the key variance proof.
    """
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_power_of_two(n)
    core.validate_dimensions(q, block)
    state.validate(q)
    indices, theta = nearest_grid_map(n, q)
    coeffs = _term_coefficients(theta, rank)
    s = np.arange(q, dtype=np.float64) / q
    power = np.ones(n, dtype=np.float64)
    out = np.zeros(n, dtype=np.complex128)
    for r in range(rank):
        padded = np.zeros(q, dtype=np.complex128)
        padded[:n] = arr * power
        row = core.one_row_estimate(padded, block, state, dtype).astype(np.complex128)
        out += coeffs[r] * row[indices]
        power *= s[:n]
    return math.sqrt(q / n) * out


def one_row_variance_bound(x: npt.ArrayLike, rank: int, block: int) -> float:
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    tail = bessel_tail_bound(rank)
    return (block / n) * (1.0 + tail) ** 2 * float(np.linalg.norm(arr)) ** 2


def deterministic_lift_error_bound(x: npt.ArrayLike, rank: int) -> float:
    arr = np.asarray(x, dtype=np.complex128)
    return bessel_tail_bound(rank) * float(np.linalg.norm(arr))


def streaming_all_length_fft(
    x: npt.ArrayLike,
    rank: int,
    rows: int,
    g: float,
    rng: np.random.Generator,
    dtype: Any = np.complex128,
) -> ComplexArray:
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_power_of_two(n)
    block = choose_dyadic_block(q)
    if rows <= 0 or rows % 2 != 1:
        raise ValueError("rows must be positive and odd")
    norm = float(np.linalg.norm(arr))
    if norm == 0.0:
        return np.zeros(n, dtype=np.complex128)
    tail = bessel_tail_bound(rank)
    tau = g * (1.0 + tail) * math.sqrt(block / n) * norm
    real_state = core.MajorityGridState.zeros(n)
    imag_state = core.MajorityGridState.zeros(n)
    for _ in range(rows):
        state = core.draw_state(q, rng)
        row = lifted_bessel_chirp_row(arr, rank, block, state, dtype)
        core.majority_grid_update(real_state, row.real, tau)
        core.majority_grid_update(imag_state, row.imag, tau)
    return (
        core.majority_grid_finalize(real_state, tau)
        + 1j * core.majority_grid_finalize(imag_state, tau)
    )


def robust_statistical_radius(x: npt.ArrayLike, rank: int, g: float) -> float:
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_power_of_two(n)
    block = choose_dyadic_block(q)
    tail = bessel_tail_bound(rank)
    return (
        (5.0 / math.sqrt(2.0))
        * g
        * (1.0 + tail)
        * math.sqrt(block / n)
        * float(np.linalg.norm(arr))
    )


def total_uniform_error_bound(x: npt.ArrayLike, rank: int, g: float) -> float:
    return deterministic_lift_error_bound(x, rank) + robust_statistical_radius(x, rank, g)


def fixed_row_g(n: int, rows: int, delta: float) -> float:
    if rows <= 0 or rows % 2 != 1:
        raise ValueError("rows must be positive and odd")
    if not (0.0 < delta < 1.0):
        raise ValueError("delta must lie in (0,1)")
    s = (rows + 1) // 2
    c = math.comb(rows, s)
    return (2.0 * n * c / delta) ** (1.0 / (2.0 * s))


def fixed_row_failure_bound(n: int, rows: int, g: float) -> float:
    s = (rows + 1) // 2
    return min(1.0, 2.0 * n * math.comb(rows, s) * g ** (-2 * s))


def row_work_proxy(n: int, rank: int) -> float:
    q = next_power_of_two(n)
    block = choose_dyadic_block(q)
    return rank * core.row_work_proxy(q, block) + rank * n


def asymptotic_rank(n: int, alpha: float, slack: float = 0.1) -> int:
    """A practical rank near (alpha+slack) log N/log log N, then certified."""
    if n < 3 or alpha <= 0 or slack <= 0:
        raise ValueError("need n>=3 and positive alpha/slack")
    target = n ** (-(alpha + slack))
    return bessel_rank_for_tail(target)


def make_cases(n: int, rng: np.random.Generator) -> dict[str, ComplexArray]:
    idx = np.arange(n)
    spike = np.zeros(n, dtype=np.complex128)
    spike[int(rng.integers(n))] = 1.0
    return {
        "flat": np.ones(n, dtype=np.complex128),
        "gaussian": rng.normal(size=n) + 1j * rng.normal(size=n),
        "random_phase": np.exp(2j * np.pi * rng.random(n)),
        "spike": spike,
        "prime_chirp": np.exp(2j * np.pi * (3 * idx * idx + 5 * idx) / n),
    }


def run_experiments(seed: int = 20261009) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    payload: dict[str, Any] = {"seed": seed}

    # 1. Independent algebraic equality of the truncated lift.
    equality: list[dict[str, Any]] = []
    for n in [7, 10, 15, 17, 31, 45]:
        x = rng.normal(size=n) + 1j * rng.normal(size=n)
        rank = 10
        a = lifted_exact_bessel(x, rank)
        b = lifted_direct_bessel_kernel(x, rank)
        equality.append({"N": n, "rank": rank, "max_error": float(np.max(np.abs(a - b)))})
    payload["lift_equality"] = equality

    # 2. Deterministic Taylor error against the true arbitrary-length DFT.
    truncation: list[dict[str, Any]] = []
    for n in [7, 15, 17, 31, 61, 97, 127]:
        for name, x in make_cases(n, rng).items():
            rank = 10
            ref = normalized_dft(x)
            got = lifted_exact_bessel(x, rank)
            scale = float(np.linalg.norm(x))
            truncation.append({
                "N": n,
                "case": name,
                "rank": rank,
                "normalized_max_error": float(np.max(np.abs(got - ref)) / max(scale, 1e-300)),
                "tail_bound": bessel_tail_bound(rank),
            })
    payload["truncation"] = truncation

    # 3. Empirical one-row variance for arbitrary lengths.
    variance: list[dict[str, Any]] = []
    for n in [15, 17, 31, 45, 61]:
        q = next_power_of_two(n)
        block = choose_dyadic_block(q)
        rank = 12
        for name in ["gaussian", "random_phase", "spike"]:
            x = make_cases(n, rng)[name]
            center = lifted_exact_bessel(x, rank)
            samples = []
            for _ in range(1200):
                samples.append(lifted_bessel_chirp_row(x, rank, block, core.draw_state(q, rng)))
            stack = np.asarray(samples)
            empirical = np.mean(np.abs(stack - center[None, :]) ** 2, axis=0)
            bound = one_row_variance_bound(x, rank, block)
            variance.append({
                "N": n,
                "Q": q,
                "M": block,
                "case": name,
                "max_empirical_variance": float(np.max(empirical)),
                "theorem_bound": float(bound),
                "ratio": float(np.max(empirical) / max(bound, 1e-300)),
            })
    payload["variance"] = variance

    # 4. End-to-end robust arbitrary-length examples.
    robust: list[dict[str, Any]] = []
    for n in [31, 61, 97, 127]:
        rank = 12
        rows = 9
        g = fixed_row_g(n, rows, 0.1)
        for name, x in make_cases(n, rng).items():
            ref = normalized_dft(x)
            got = streaming_all_length_fft(x, rank, rows, g, rng)
            err = float(np.max(np.abs(got - ref)))
            bound = total_uniform_error_bound(x, rank, g)
            robust.append({
                "N": n,
                "case": name,
                "rank": rank,
                "rows": rows,
                "g": g,
                "error": err,
                "bound": bound,
                "ratio": err / max(bound, 1e-300),
            })
    payload["robust"] = robust

    # 5. Complexity/rank table for large formal sizes, without allocating.
    complexity: list[dict[str, Any]] = []
    for exp in [10, 20, 30, 40, 60, 80, 120]:
        n = (1 << exp) - 1  # deliberately non-dyadic
        alpha = 1.0 / 3.0
        rank = asymptotic_rank(n, alpha, 0.08)
        q = next_power_of_two(n)
        block = choose_dyadic_block(q)
        work = row_work_proxy(n, rank)
        baseline = n * math.log2(n)
        complexity.append({
            "log2_N_approx": exp,
            "rank": rank,
            "Q_over_N": q / n,
            "M": block,
            "work_proxy_over_NlogN": work / baseline,
            "tail": bessel_tail_bound(rank),
        })
    payload["complexity"] = complexity
    return payload


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results.json"))
    parser.add_argument("--seed", type=int, default=20261009)
    args = parser.parse_args(list(argv) if argv is not None else None)
    payload = run_experiments(args.seed)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "max_lift_equality_error": max(r["max_error"] for r in payload["lift_equality"]),
        "max_truncation_ratio": max(r["normalized_max_error"] / r["tail_bound"] for r in payload["truncation"]),
        "max_variance_ratio": max(r["ratio"] for r in payload["variance"]),
        "max_robust_ratio": max(r["ratio"] for r in payload["robust"]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
