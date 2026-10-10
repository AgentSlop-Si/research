#!/usr/bin/env python3
"""Frequency-shift median Fourier sketch (v5 research prototype).

This module implements a randomized approximation to the *full* unitary DFT for
length N = K*M.  One sketch uses one length-K FFT and K length-M FFTs.  The
random frequency shifts make the estimator unbiased and give an exact per-bin
variance formula.

The implementation is intentionally readable and independently checkable.  It
is a research prototype, not a replacement for an optimized FFT library.
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

ComplexArray = npt.NDArray[np.complex128]
IntArray = npt.NDArray[np.int64]

FOURTH_ROOTS: ComplexArray = np.asarray([1.0, -1.0, 1.0j, -1.0j], dtype=np.complex128)


def unitary_fft(x: ComplexArray, axis: int = -1) -> ComplexArray:
    """Return the unitary DFT along ``axis``."""
    n = x.shape[axis]
    if n <= 0:
        raise ValueError("FFT axis must be non-empty")
    return np.fft.fft(x, axis=axis) / math.sqrt(n)


def exact_unitary_dft(x: ComplexArray) -> ComplexArray:
    """Reference full unitary DFT."""
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("x must be a non-empty one-dimensional array")
    return unitary_fft(x)


@dataclass(frozen=True)
class SketchRandomness:
    """Random state for one frequency-shift sketch."""

    shifts: IntArray
    phases: ComplexArray

    def validate(self, *, k: int, m: int) -> None:
        if self.shifts.shape != (m,):
            raise ValueError(f"shifts must have shape ({m},)")
        if self.phases.shape != (m,):
            raise ValueError(f"phases must have shape ({m},)")
        if np.any(self.shifts < 0) or np.any(self.shifts >= k):
            raise ValueError("all shifts must lie in [0, K)")
        if not np.allclose(np.abs(self.phases), 1.0):
            raise ValueError("all phases must have unit magnitude")


def draw_randomness(k: int, m: int, rng: np.random.Generator) -> SketchRandomness:
    """Draw independent q_t in Z_K and fourth-root phases xi_t."""
    if k <= 0 or m <= 0:
        raise ValueError("k and m must be positive")
    shifts = rng.integers(0, k, size=m, dtype=np.int64)
    phases = FOURTH_ROOTS[rng.integers(0, 4, size=m)]
    return SketchRandomness(shifts=shifts, phases=phases)


def frequency_shift_sketch_with_state(
    x: ComplexArray,
    m: int,
    state: SketchRandomness,
) -> ComplexArray:
    """Evaluate one randomized full-spectrum estimate.

    The input is reshaped as x[r, t] = x[r*M + t], with N = K*M.  For q_t and
    xi_t from ``state`` we form

        z_r = sum_t conj(xi_t) exp(-2*pi*i*r*q_t/K) x[r,t],

    compute its length-K unitary FFT Z, then for each p compute a length-M
    unitary FFT of

        xi_t Z[(p-q_t) mod K] exp(-2*pi*i*p*t/N).

    The output is ordered in the ordinary DFT order m_out = p + K*v.
    """
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("x must be a non-empty one-dimensional array")
    if m <= 0 or x.size % m != 0:
        raise ValueError("m must be a positive divisor of len(x)")

    n = int(x.size)
    k = n // m
    state.validate(k=k, m=m)
    q = state.shifts
    xi = state.phases
    x2 = x.reshape(k, m)

    # O(N) sketch construction.  The matrix is materialized only to keep the
    # prototype transparent; a streaming implementation can accumulate z using
    # O(K+M) auxiliary storage.
    r = np.arange(k, dtype=np.float64)[:, None]
    modulation = np.conj(xi)[None, :] * np.exp(-2j * np.pi * r * q[None, :] / k)
    z = np.sum(x2 * modulation, axis=1)
    z_hat = unitary_fft(z)

    # K independent length-M FFTs.  Vectorization changes no arithmetic count.
    p = np.arange(k, dtype=np.int64)[:, None]
    t = np.arange(m, dtype=np.float64)[None, :]
    gather = z_hat[(p - q[None, :]) % k]
    local = xi[None, :] * gather * np.exp(-2j * np.pi * p * t / n)
    values = unitary_fft(local, axis=1)  # values[p, v]

    # Standard frequency order: output index is p + K*v.
    return np.ascontiguousarray(values.T.reshape(n))


def balanced_bucket_sketch_with_state(
    x: ComplexArray,
    m: int,
    bucket_count: int,
    state: SketchRandomness,
) -> ComplexArray:
    """Generalization with equally sized deterministic column buckets.

    Columns are assigned to ``bucket = t mod bucket_count``.  Only columns in
    the same bucket collide.  If ``c = M / bucket_count``, the exact per-bin
    variance becomes ``(c-1)||x||_2^2/N``.  The price is ``bucket_count``
    length-K FFTs.
    """
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("x must be a non-empty one-dimensional array")
    if m <= 0 or x.size % m != 0:
        raise ValueError("m must be a positive divisor of len(x)")
    if bucket_count <= 0 or m % bucket_count != 0:
        raise ValueError("bucket_count must be a positive divisor of m")

    n = int(x.size)
    k = n // m
    state.validate(k=k, m=m)
    q = state.shifts
    xi = state.phases
    x2 = x.reshape(k, m)
    buckets = np.arange(m, dtype=np.int64) % bucket_count

    r = np.arange(k, dtype=np.float64)[:, None]
    modulation = np.conj(xi)[None, :] * np.exp(-2j * np.pi * r * q[None, :] / k)
    mixed = x2 * modulation
    z = np.zeros((k, bucket_count), dtype=np.complex128)
    for b in range(bucket_count):
        z[:, b] = np.sum(mixed[:, buckets == b], axis=1)
    z_hat = unitary_fft(z, axis=0)

    p = np.arange(k, dtype=np.int64)[:, None]
    t = np.arange(m, dtype=np.float64)[None, :]
    gather = z_hat[(p - q[None, :]) % k, buckets[None, :]]
    local = xi[None, :] * gather * np.exp(-2j * np.pi * p * t / n)
    values = unitary_fft(local, axis=1)
    return np.ascontiguousarray(values.T.reshape(n))


def balanced_bucket_sketch(
    x: ComplexArray,
    m: int,
    bucket_count: int,
    rng: np.random.Generator,
) -> ComplexArray:
    """Draw fresh randomness and evaluate a balanced-bucket sketch."""
    n = int(np.asarray(x).size)
    if m <= 0 or n % m != 0:
        raise ValueError("m must be a positive divisor of len(x)")
    return balanced_bucket_sketch_with_state(
        x, m, bucket_count, draw_randomness(n // m, m, rng)
    )


def balanced_bucket_per_bin_variance(
    x: ComplexArray, m: int, bucket_count: int
) -> float:
    """Exact per-bin variance for equal buckets of size c=M/bucket_count."""
    x = np.asarray(x, dtype=np.complex128)
    if (
        x.ndim != 1
        or x.size == 0
        or m <= 0
        or x.size % m != 0
        or bucket_count <= 0
        or m % bucket_count != 0
    ):
        raise ValueError("invalid x, m, or bucket_count")
    collision_size = m // bucket_count
    return float((collision_size - 1) * np.vdot(x, x).real / x.size)


def frequency_shift_sketch(
    x: ComplexArray,
    m: int,
    rng: np.random.Generator,
) -> ComplexArray:
    """Draw fresh randomness and evaluate one sketch."""
    n = int(np.asarray(x).size)
    if m <= 0 or n % m != 0:
        raise ValueError("m must be a positive divisor of len(x)")
    return frequency_shift_sketch_with_state(x, m, draw_randomness(n // m, m, rng))


def direct_expansion_estimate(
    x: ComplexArray,
    m: int,
    state: SketchRandomness,
) -> ComplexArray:
    """Slow independent evaluation of the algebraic expansion.

    This routine first computes every column transform

        A_t[p] = K^{-1/2} sum_r x[r,t] exp(-2*pi*i*r*p/K)

    and then evaluates the double sum directly.  It is used only as a verifier
    for the fast separable implementation.
    """
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0 or m <= 0 or x.size % m != 0:
        raise ValueError("x must be one-dimensional and m must divide len(x)")
    n = int(x.size)
    k = n // m
    state.validate(k=k, m=m)
    q = state.shifts
    xi = state.phases

    x2 = x.reshape(k, m)
    a = unitary_fft(x2, axis=0)  # a[p, t]
    t_idx = np.arange(m, dtype=np.float64)
    u_idx = np.arange(m, dtype=np.int64)
    values = np.empty((k, m), dtype=np.complex128)

    for p in range(k):
        pre_fft = np.empty(m, dtype=np.complex128)
        for t in range(m):
            freq = (p + q[u_idx] - q[t]) % k
            mixed = np.sum(np.conj(xi) * a[freq, u_idx])
            pre_fft[t] = xi[t] * mixed * np.exp(-2j * np.pi * p * t / n)
        values[p, :] = unitary_fft(pre_fft)

    return np.ascontiguousarray(values.T.reshape(n))


def coordinatewise_complex_median(estimates: ComplexArray) -> ComplexArray:
    """Median real and imaginary components separately."""
    estimates = np.asarray(estimates, dtype=np.complex128)
    if estimates.ndim != 2 or estimates.shape[0] % 2 != 1:
        raise ValueError("estimates must have shape (odd_rows, N)")
    return np.median(estimates.real, axis=0) + 1j * np.median(estimates.imag, axis=0)


def median_frequency_shift_fft(
    x: ComplexArray,
    m: int,
    rows: int,
    rng: np.random.Generator,
) -> ComplexArray:
    """Return the coordinatewise median of an odd number of independent sketches."""
    if rows <= 0 or rows % 2 != 1:
        raise ValueError("rows must be a positive odd integer")
    estimates = np.stack([frequency_shift_sketch(x, m, rng) for _ in range(rows)])
    return coordinatewise_complex_median(estimates)


def per_bin_variance(x: ComplexArray, m: int) -> float:
    """Exact E|estimate[j]-DFT(x)[j]|^2 for every output bin j."""
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0 or m <= 0 or x.size % m != 0:
        raise ValueError("x must be one-dimensional and m must divide len(x)")
    return float((m - 1) * np.vdot(x, x).real / x.size)


def median_uniform_bound(
    x: ComplexArray,
    m: int,
    rows: int,
    delta: float,
) -> float:
    """The proved all-output absolute error bound for coordinatewise medians.

    If rows = 2*t-1 and C_t = binom(2*t-1, t), then with probability at least
    1-delta,

      max_j |estimate[j]-DFT(x)[j]|
        <= sqrt(2) * (2*N*C_t/delta)^(1/(2*t))
           * sqrt((M-1)/N) * ||x||_2.
    """
    x = np.asarray(x, dtype=np.complex128)
    if rows <= 0 or rows % 2 != 1:
        raise ValueError("rows must be a positive odd integer")
    if not (0.0 < delta < 1.0):
        raise ValueError("delta must lie in (0,1)")
    if m <= 0 or x.size % m != 0:
        raise ValueError("m must divide len(x)")
    t = (rows + 1) // 2
    c_t = math.comb(2 * t - 1, t)
    sigma = math.sqrt(per_bin_variance(x, m))
    return math.sqrt(2.0) * (2.0 * x.size * c_t / delta) ** (1.0 / (2.0 * t)) * sigma


def arithmetic_cost_proxy(n: int, m: int, rows: int = 1) -> float:
    """Asymptotic operation proxy R*N*(log2 M + log2(N/M)/M + 1)."""
    if n <= 1 or m <= 0 or n % m != 0 or rows <= 0:
        raise ValueError("require n>1, positive divisor m, and positive rows")
    k = n // m
    return rows * n * (1.0 + math.log2(m) + math.log2(k) / m)


def balanced_bucket_cost_proxy(
    n: int, m: int, bucket_count: int, rows: int = 1
) -> float:
    """Cost proxy for the equal-bucket extension.

    With collision size c=M/bucket_count, the proxy is
    R*N*(log2 M + log2(N/M)/c + 1).
    """
    if (
        n <= 1
        or m <= 0
        or n % m != 0
        or bucket_count <= 0
        or m % bucket_count != 0
        or rows <= 0
    ):
        raise ValueError("invalid dimensions")
    k = n // m
    c = m // bucket_count
    return rows * n * (1.0 + math.log2(m) + math.log2(k) / c)


def _case_signals(k: int, m: int, rng: np.random.Generator) -> dict[str, ComplexArray]:
    n = k * m
    r = np.arange(k)
    tone = max(1, k // 5)
    cases: dict[str, ComplexArray] = {}
    cases["flat"] = np.ones(n, dtype=np.complex128)
    cases["random_phase"] = np.exp(2j * np.pi * rng.random(n))
    cases["gaussian"] = rng.normal(size=n) + 1j * rng.normal(size=n)

    local = np.zeros((k, m), dtype=np.complex128)
    local[:, m // 3] = np.exp(2j * np.pi * tone * r / k)
    cases["local_spike_tone"] = local.reshape(n)

    pattern = np.exp(2j * np.pi * rng.random(m))
    repeated = np.exp(2j * np.pi * tone * r[:, None] / k) * pattern[None, :]
    cases["repeated_pattern_tone"] = repeated.reshape(n)

    spike = np.zeros(n, dtype=np.complex128)
    spike[n // 3] = 1.0
    cases["single_spike"] = spike
    return cases


def run_reproducible_experiments(seed: int = 20261009) -> dict[str, Any]:
    """Run compact algebra, variance, median, and cost checks."""
    rng = np.random.default_rng(seed)

    # 1. Fast evaluator versus a structurally independent double-sum evaluator.
    expansion_rows: list[dict[str, Any]] = []
    for k, m in [(5, 3), (8, 4), (9, 5), (16, 8)]:
        n = k * m
        x = rng.normal(size=n) + 1j * rng.normal(size=n)
        state = draw_randomness(k, m, rng)
        fast = frequency_shift_sketch_with_state(x, m, state)
        slow = direct_expansion_estimate(x, m, state)
        expansion_rows.append(
            {
                "K": k,
                "M": m,
                "N": n,
                "max_abs_difference": float(np.max(np.abs(fast - slow))),
            }
        )

    # 2. Exact variance prediction checked empirically.  We average over every
    # output bin as well as trials, so modest trial counts are informative.
    variance_rows: list[dict[str, Any]] = []
    for k, m in [(64, 8), (64, 16), (128, 16), (128, 32)]:
        for name, x in _case_signals(k, m, rng).items():
            exact = exact_unitary_dft(x)
            predicted = per_bin_variance(x, m)
            sq_error_sum = 0.0
            trials = 40
            for _ in range(trials):
                estimate = frequency_shift_sketch(x, m, rng)
                sq_error_sum += float(np.sum(np.abs(estimate - exact) ** 2))
            empirical = sq_error_sum / (trials * x.size)
            variance_rows.append(
                {
                    "K": k,
                    "M": m,
                    "N": k * m,
                    "case": name,
                    "trials": trials,
                    "predicted_per_bin_mse": predicted,
                    "empirical_per_bin_mse": empirical,
                    "empirical_over_predicted": empirical / predicted if predicted else 1.0,
                }
            )

    # 3. Median behavior, normalized by the coefficient energy scale ||x||/sqrt(N).
    median_rows: list[dict[str, Any]] = []
    for k, m in [(128, 16), (128, 32), (256, 32)]:
        for name, x in _case_signals(k, m, rng).items():
            exact = exact_unitary_dft(x)
            scale = float(np.linalg.norm(x) / math.sqrt(x.size))
            for rows in [1, 3, 5, 9]:
                max_errors: list[float] = []
                rms_errors: list[float] = []
                for _ in range(8):
                    estimate = median_frequency_shift_fft(x, m, rows, rng)
                    error = np.abs(estimate - exact)
                    max_errors.append(float(np.max(error) / scale))
                    rms_errors.append(float(np.sqrt(np.mean(error**2)) / scale))
                median_rows.append(
                    {
                        "K": k,
                        "M": m,
                        "N": k * m,
                        "case": name,
                        "rows": rows,
                        "normalized_max_median": float(np.median(max_errors)),
                        "normalized_max_p90": float(np.quantile(max_errors, 0.9)),
                        "normalized_rms_median": float(np.median(rms_errors)),
                        "single_sketch_predicted_normalized_rms": math.sqrt(m - 1),
                    }
                )

    # 4. Balanced-bucket extension: exact variance c-1, with c=M/d.
    bucket_rows: list[dict[str, Any]] = []
    k, m = 64, 16
    for name, x in _case_signals(k, m, rng).items():
        exact = exact_unitary_dft(x)
        for bucket_count in [1, 2, 4, 8, 16]:
            predicted = balanced_bucket_per_bin_variance(x, m, bucket_count)
            trials = 40
            observed = 0.0
            for _ in range(trials):
                estimate = balanced_bucket_sketch(x, m, bucket_count, rng)
                observed += float(np.mean(np.abs(estimate - exact) ** 2))
            observed /= trials
            bucket_rows.append(
                {
                    "K": k,
                    "M": m,
                    "N": k * m,
                    "case": name,
                    "bucket_count": bucket_count,
                    "collision_size": m // bucket_count,
                    "predicted_per_bin_mse": predicted,
                    "empirical_per_bin_mse": observed,
                    "empirical_over_predicted": (
                        observed / predicted if predicted else 1.0
                    ),
                }
            )

    # 5. Symbolic scaling proxies for two useful parameter regimes.
    scaling_rows: list[dict[str, Any]] = []
    for log2_n in [20, 30, 40, 60, 80, 120, 160, 240]:
        # Use real-valued proxies rather than requiring astronomically large integer N.
        l = float(log2_n)
        m_fast = max(2.0, l)
        m_trade = max(2.0, math.log2(l))
        for label, m_value in [("M~logN", m_fast), ("M~loglogN", m_trade)]:
            per_n = 1.0 + math.log2(m_value) + (l - math.log2(m_value)) / m_value
            scaling_rows.append(
                {
                    "log2_N": log2_n,
                    "regime": label,
                    "M_proxy": m_value,
                    "cost_over_N": per_n,
                    "cost_over_Nlog2N": per_n / l,
                    "single_sketch_std_over_energy_scale": math.sqrt(max(0.0, m_value - 1.0)),
                }
            )

    max_expansion_error = max(row["max_abs_difference"] for row in expansion_rows)
    variance_ratios = [row["empirical_over_predicted"] for row in variance_rows]

    return {
        "metadata": {
            "seed": seed,
            "normalization": "unitary DFT",
            "algorithm": "frequency-shift median Fourier sketch",
        },
        "summary": {
            "max_fast_vs_expansion_error": max_expansion_error,
            "variance_ratio_min": min(variance_ratios),
            "variance_ratio_max": max(variance_ratios),
            "variance_ratio_median": float(np.median(variance_ratios)),
            "number_of_expansion_checks": len(expansion_rows),
            "number_of_variance_checks": len(variance_rows),
            "number_of_median_checks": len(median_rows),
            "number_of_balanced_bucket_checks": len(bucket_rows),
        },
        "fast_vs_direct_expansion": expansion_rows,
        "variance_checks": variance_rows,
        "median_checks": median_rows,
        "balanced_bucket_checks": bucket_rows,
        "scaling_proxies": scaling_rows,
    }


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20261009)
    parser.add_argument("--output", type=Path, default=Path("results.json"))
    args = parser.parse_args(list(argv) if argv is not None else None)

    results = run_reproducible_experiments(args.seed)
    args.output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results["summary"], indent=2))
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
