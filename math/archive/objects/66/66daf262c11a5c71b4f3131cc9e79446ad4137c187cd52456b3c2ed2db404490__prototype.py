#!/usr/bin/env python3
"""Predecode-median Fourier sketch (v6 research prototype).

The algorithm continues the v5 frequency-shift sketch, but moves the robust
aggregation before the K families of short M-point decoders.  Each randomized
row stores only one length-K mixed spectrum plus its shifts/phases.  For every
local Fourier coordinate A_t[p], we gather the row estimates, take separate
real/imaginary medians, and run the deterministic M-point decoder once.

This is a research prototype in the algebraic complex-arithmetic model.  It is
not a machine-precision FFT replacement.
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
    x = np.asarray(x, dtype=np.complex128)
    n = x.shape[axis]
    if n <= 0:
        raise ValueError("FFT axis must be non-empty")
    return np.fft.fft(x, axis=axis) / math.sqrt(n)


def unitary_ifft(x: ComplexArray, axis: int = -1) -> ComplexArray:
    x = np.asarray(x, dtype=np.complex128)
    n = x.shape[axis]
    if n <= 0:
        raise ValueError("FFT axis must be non-empty")
    return np.fft.ifft(x, axis=axis) * math.sqrt(n)


def exact_unitary_dft(x: ComplexArray) -> ComplexArray:
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0:
        raise ValueError("x must be a non-empty vector")
    return unitary_fft(x)


@dataclass(frozen=True)
class SketchRandomness:
    shifts: IntArray
    phases: ComplexArray

    def validate(self, k: int, m: int) -> None:
        if self.shifts.shape != (m,) or self.phases.shape != (m,):
            raise ValueError("invalid randomness shape")
        if np.any(self.shifts < 0) or np.any(self.shifts >= k):
            raise ValueError("shift outside Z_K")
        if not np.allclose(np.abs(self.phases), 1.0):
            raise ValueError("phases must have unit magnitude")


@dataclass(frozen=True)
class CompressedRows:
    """Compressed randomized rows needed for deferred recovery."""

    spectra: ComplexArray  # shape (R,K)
    shifts: IntArray       # shape (R,M)
    phases: ComplexArray   # shape (R,M)

    @property
    def rows(self) -> int:
        return int(self.spectra.shape[0])

    @property
    def k(self) -> int:
        return int(self.spectra.shape[1])

    @property
    def m(self) -> int:
        return int(self.shifts.shape[1])

    def validate(self) -> None:
        r, k = self.spectra.shape
        if self.shifts.shape != (r, self.m) or self.phases.shape != (r, self.m):
            raise ValueError("compressed row dimensions disagree")
        if np.any(self.shifts < 0) or np.any(self.shifts >= k):
            raise ValueError("invalid compressed-row shift")


def draw_randomness(k: int, m: int, rng: np.random.Generator) -> SketchRandomness:
    if k <= 0 or m <= 0:
        raise ValueError("k,m must be positive")
    return SketchRandomness(
        shifts=rng.integers(0, k, size=m, dtype=np.int64),
        phases=FOURTH_ROOTS[rng.integers(0, 4, size=m)],
    )


def compress_one_row(x: ComplexArray, m: int, state: SketchRandomness) -> ComplexArray:
    """Return Z[s] = sum_u conj(xi_u) A_u[s+q_u]."""
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0 or m <= 0 or x.size % m:
        raise ValueError("m must divide a non-empty one-dimensional x")
    n = int(x.size)
    k = n // m
    state.validate(k, m)
    x2 = x.reshape(k, m)
    r = np.arange(k, dtype=np.float64)[:, None]
    modulation = np.conj(state.phases)[None, :] * np.exp(
        -2j * np.pi * r * state.shifts[None, :] / k
    )
    z = np.sum(x2 * modulation, axis=1)
    return unitary_fft(z)


def build_compressed_rows(
    x: ComplexArray,
    m: int,
    rows: int,
    rng: np.random.Generator,
) -> CompressedRows:
    """Build R independent compressed rows without materializing R full outputs."""
    x = np.asarray(x, dtype=np.complex128)
    if rows <= 0 or rows % 2 != 1:
        raise ValueError("rows must be a positive odd integer")
    if x.ndim != 1 or x.size == 0 or m <= 0 or x.size % m:
        raise ValueError("m must divide a non-empty one-dimensional x")
    k = x.size // m
    spectra = np.empty((rows, k), dtype=np.complex128)
    shifts = np.empty((rows, m), dtype=np.int64)
    phases = np.empty((rows, m), dtype=np.complex128)
    for j in range(rows):
        state = draw_randomness(k, m, rng)
        shifts[j] = state.shifts
        phases[j] = state.phases
        spectra[j] = compress_one_row(x, m, state)
    result = CompressedRows(spectra=spectra, shifts=shifts, phases=phases)
    result.validate()
    return result


def local_estimate_from_row(
    spectrum: ComplexArray,
    state: SketchRandomness,
) -> ComplexArray:
    """Recover all local estimates Ahat[p,t] from one compressed row."""
    spectrum = np.asarray(spectrum, dtype=np.complex128)
    if spectrum.ndim != 1 or spectrum.size == 0:
        raise ValueError("spectrum must be a non-empty vector")
    k = spectrum.size
    m = state.shifts.size
    state.validate(k, m)
    p = np.arange(k, dtype=np.int64)[:, None]
    return state.phases[None, :] * spectrum[(p - state.shifts[None, :]) % k]


def decode_local_spectra(local_spectra: ComplexArray) -> ComplexArray:
    """Decode exact/estimated A_t[p] into standard-order length-N DFT values."""
    local_spectra = np.asarray(local_spectra, dtype=np.complex128)
    if local_spectra.ndim != 2 or 0 in local_spectra.shape:
        raise ValueError("local_spectra must have shape (K,M)")
    k, m = local_spectra.shape
    n = k * m
    p = np.arange(k, dtype=np.float64)[:, None]
    t = np.arange(m, dtype=np.float64)[None, :]
    pre = local_spectra * np.exp(-2j * np.pi * p * t / n)
    values = unitary_fft(pre, axis=1)  # [p,v]
    return np.ascontiguousarray(values.T.reshape(n))


def one_row_full_estimate(
    x: ComplexArray,
    m: int,
    state: SketchRandomness,
) -> ComplexArray:
    """One v5-equivalent full output, written through the local interface."""
    zhat = compress_one_row(x, m, state)
    return decode_local_spectra(local_estimate_from_row(zhat, state))


def coordinatewise_complex_median(values: ComplexArray, axis: int = 0) -> ComplexArray:
    values = np.asarray(values, dtype=np.complex128)
    if values.shape[axis] % 2 != 1:
        raise ValueError("median axis must have odd length")
    return np.median(values.real, axis=axis) + 1j * np.median(values.imag, axis=axis)


def predecode_median_from_compressed(rows: CompressedRows) -> ComplexArray:
    """Take local medians and execute the short decoder only once.

    The function processes one p-slice at a time.  It stores R*K compressed
    spectral values, not R*N materialized local estimates or outputs.
    """
    rows.validate()
    rcount, k = rows.spectra.shape
    m = rows.m
    if rcount % 2 != 1:
        raise ValueError("an odd number of rows is required")
    n = k * m
    out = np.empty(n, dtype=np.complex128)
    row_ids = np.arange(rcount, dtype=np.int64)[:, None]
    t = np.arange(m, dtype=np.float64)
    v_indices = np.arange(m, dtype=np.int64)

    for p in range(k):
        gather_idx = (p - rows.shifts) % k
        estimates = rows.phases * rows.spectra[row_ids, gather_idx]
        local_median = coordinatewise_complex_median(estimates, axis=0)
        pre = local_median * np.exp(-2j * np.pi * p * t / n)
        decoded = unitary_fft(pre)
        out[p + k * v_indices] = decoded
    return out


def predecode_median_fft(
    x: ComplexArray,
    m: int,
    rows: int,
    rng: np.random.Generator,
) -> ComplexArray:
    return predecode_median_from_compressed(build_compressed_rows(x, m, rows, rng))


def postdecode_median_fft(
    x: ComplexArray,
    m: int,
    rows: int,
    rng: np.random.Generator,
) -> ComplexArray:
    """v5 comparator: decode every row, then take output medians."""
    if rows <= 0 or rows % 2 != 1:
        raise ValueError("rows must be positive and odd")
    n = int(np.asarray(x).size)
    k = n // m
    estimates = []
    for _ in range(rows):
        state = draw_randomness(k, m, rng)
        estimates.append(one_row_full_estimate(x, m, state))
    return coordinatewise_complex_median(np.stack(estimates), axis=0)


def exact_local_spectra(x: ComplexArray, m: int) -> ComplexArray:
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0 or m <= 0 or x.size % m:
        raise ValueError("m must divide x.size")
    return unitary_fft(x.reshape(x.size // m, m), axis=0)


def local_variance_vector(x: ComplexArray, m: int) -> npt.NDArray[np.float64]:
    """Exact variance of each Ahat[p,t]-A[p,t], independent of p."""
    x = np.asarray(x, dtype=np.complex128)
    if x.ndim != 1 or x.size == 0 or m <= 0 or x.size % m:
        raise ValueError("m must divide x.size")
    x2 = x.reshape(x.size // m, m)
    energies = np.sum(np.abs(x2) ** 2, axis=0)
    total = float(np.sum(energies))
    k = x.size // m
    return np.maximum(0.0, total - energies) / k


def predecode_median_uniform_bound(
    x: ComplexArray,
    m: int,
    rows: int,
    delta: float,
    *,
    refined: bool = True,
) -> float:
    """Proved simultaneous absolute output-error bound.

    With rows=2*t-1 and C_t=binom(2*t-1,t), the local coordinate medians
    obey a 2*t-moment bound.  The final M-point decoder is then charged once.
    """
    x = np.asarray(x, dtype=np.complex128)
    if rows <= 0 or rows % 2 != 1:
        raise ValueError("rows must be positive and odd")
    if not (0.0 < delta < 1.0):
        raise ValueError("delta must lie in (0,1)")
    if x.ndim != 1 or x.size == 0 or m <= 0 or x.size % m:
        raise ValueError("m must divide x.size")
    tmed = (rows + 1) // 2
    c_t = math.comb(2 * tmed - 1, tmed)
    amp = math.sqrt(2.0) * (2.0 * x.size * c_t / delta) ** (1.0 / (2.0 * tmed))
    if refined:
        variances = local_variance_vector(x, m)
        return amp * float(np.sum(np.sqrt(variances))) / math.sqrt(m)
    return amp * math.sqrt(m * (m - 1) / x.size) * float(np.linalg.norm(x))


def predecode_cost_proxy(n: int, m: int, rows: int) -> float:
    """Arithmetic proxy for R local rows plus one final decoder.

    R*N*(1 + log2(K)/M) + N*log2(M), K=N/M.
    """
    if n <= 1 or m <= 0 or n % m or rows <= 0:
        raise ValueError("invalid dimensions")
    k = n // m
    return rows * n * (2.0 + math.log2(k) / m) + n * math.log2(m)


def postdecode_cost_proxy(n: int, m: int, rows: int) -> float:
    """v5 proxy: each row also pays the short M-point decoder."""
    if n <= 1 or m <= 0 or n % m or rows <= 0:
        raise ValueError("invalid dimensions")
    k = n // m
    return rows * n * (2.0 + math.log2(k) / m + math.log2(m))


def compressed_memory_proxy(n: int, m: int, rows: int) -> int:
    """Number of complex/integer cells up to constants: output + R(K+M)."""
    if n <= 0 or m <= 0 or n % m or rows <= 0:
        raise ValueError("invalid dimensions")
    k = n // m
    return int(n + rows * (k + 2 * m))


def local_sparse_failure_bound(n: int, m: int, rows: int, h: int) -> float:
    """Union-bound failure probability for h-sparse local spectra.

    Each source column has at most h nonzero length-K Fourier coefficients.
    A row is collision-free for a target local coordinate with probability at
    least 1-rho, rho <= (M-1)h/K.  A median fails only if at least t rows are
    bad, where rows=2*t-1.
    """
    if n <= 0 or m <= 0 or n % m or rows <= 0 or rows % 2 != 1 or h < 0:
        raise ValueError("invalid arguments")
    k = n // m
    tmed = (rows + 1) // 2
    rho = min(1.0, (m - 1) * h / k)
    return min(1.0, n * math.comb(rows, tmed) * rho**tmed)


def make_local_sparse_signal(
    k: int,
    m: int,
    h: int,
    rng: np.random.Generator,
) -> tuple[ComplexArray, ComplexArray]:
    """Create x whose K-point transform in each of M columns is h-sparse."""
    if k <= 0 or m <= 0 or not (0 <= h <= k):
        raise ValueError("invalid k,m,h")
    a = np.zeros((k, m), dtype=np.complex128)
    for t in range(m):
        if h:
            idx = rng.choice(k, size=h, replace=False)
            a[idx, t] = rng.normal(size=h) + 1j * rng.normal(size=h)
    x = unitary_ifft(a, axis=0).reshape(k * m)
    return x, a


def tone_moment_theory(k: int, m: int, amplitude: float = 1.0) -> dict[str, float]:
    """Exact one-output moments for a single local Fourier tone.

    At p equal to the tone frequency, C~Bin(M-1,1/K) colliders contribute
    independent fourth-root phases.  Conditional on C, E|sum_{j<=C} zeta_j|^4
    = 2*C^2-C.
    """
    if k <= 0 or m <= 1:
        raise ValueError("require k>0,m>1")
    c = m - 1
    variance = amplitude**2 * c / (m * k)
    fourth = amplitude**4 * (c / k + 2.0 * c * (c - 1) / (k * k)) / (m * m)
    kurtosis = fourth / (variance * variance)
    return {
        "variance": variance,
        "fourth_moment": fourth,
        "kurtosis": kurtosis,
        "closed_form_kurtosis": k / c + 2.0 - 2.0 / c,
    }


def simulate_tone_moments(
    k: int,
    m: int,
    trials: int,
    rng: np.random.Generator,
) -> dict[str, float]:
    """Fast direct simulation of the single-local-tone output error."""
    q = rng.integers(0, k, size=(trials, m), dtype=np.int64)
    xi = FOURTH_ROOTS[rng.integers(0, 4, size=(trials, m))]
    t0 = 0
    alpha = np.exp(-2j * np.pi * np.arange(m) / (k * m))
    hit = q[:, 1:] == q[:, [t0]]
    error = (
        np.conj(xi[:, t0])
        * np.sum(alpha[None, 1:] * xi[:, 1:] * hit, axis=1)
        / math.sqrt(m)
    )
    abs2 = np.abs(error) ** 2
    return {
        "empirical_variance": float(np.mean(abs2)),
        "empirical_fourth_moment": float(np.mean(abs2**2)),
        "empirical_kurtosis": float(np.mean(abs2**2) / np.mean(abs2) ** 2),
        "zero_fraction": float(np.mean(abs2 == 0.0)),
    }


def _case_signals(k: int, m: int, rng: np.random.Generator) -> dict[str, ComplexArray]:
    n = k * m
    r = np.arange(k, dtype=np.float64)
    tone = max(1, k // 5)
    out: dict[str, ComplexArray] = {
        "flat": np.ones(n, dtype=np.complex128),
        "random_phase": np.exp(2j * np.pi * rng.random(n)),
        "gaussian": rng.normal(size=n) + 1j * rng.normal(size=n),
    }
    local = np.zeros((k, m), dtype=np.complex128)
    local[:, m // 3] = np.exp(2j * np.pi * tone * r / k)
    out["local_spike_tone"] = local.reshape(n)
    pattern = np.exp(2j * np.pi * rng.random(m))
    out["repeated_pattern_tone"] = (
        np.exp(2j * np.pi * tone * r[:, None] / k) * pattern[None, :]
    ).reshape(n)
    spike = np.zeros(n, dtype=np.complex128)
    spike[n // 3] = 1.0
    out["single_spike"] = spike
    return out


def run_reproducible_experiments(seed: int = 20261009) -> dict[str, Any]:
    rng = np.random.default_rng(seed)

    # 1. One deferred row equals one fully decoded row exactly.
    equivalence: list[dict[str, Any]] = []
    for k, m in [(5, 3), (8, 4), (16, 8), (31, 5)]:
        x = rng.normal(size=k * m) + 1j * rng.normal(size=k * m)
        state = draw_randomness(k, m, rng)
        z = compress_one_row(x, m, state)
        local = local_estimate_from_row(z, state)
        via_local = decode_local_spectra(local)
        direct = one_row_full_estimate(x, m, state)
        equivalence.append(
            {"K": k, "M": m, "max_abs_difference": float(np.max(np.abs(via_local - direct)))}
        )

    # 2. Exact local-coordinate variance identity.
    local_variance_checks: list[dict[str, Any]] = []
    for k, m in [(32, 8), (64, 8), (64, 16)]:
        for name, x in _case_signals(k, m, rng).items():
            exact_a = exact_local_spectra(x, m)
            predicted = local_variance_vector(x, m)
            accum = np.zeros(m, dtype=np.float64)
            trials = 120
            for _ in range(trials):
                state = draw_randomness(k, m, rng)
                est = local_estimate_from_row(compress_one_row(x, m, state), state)
                accum += np.mean(np.abs(est - exact_a) ** 2, axis=0)
            empirical = accum / trials
            valid = predicted > 1e-15
            ratios = empirical[valid] / predicted[valid] if np.any(valid) else np.ones(1)
            local_variance_checks.append(
                {
                    "K": k,
                    "M": m,
                    "case": name,
                    "ratio_min": float(np.min(ratios)),
                    "ratio_max": float(np.max(ratios)),
                    "ratio_median": float(np.median(ratios)),
                }
            )

    # 3. Compare medians before and after the short decoder.
    median_comparison: list[dict[str, Any]] = []
    k, m = 128, 16
    for name, x in _case_signals(k, m, rng).items():
        exact = exact_unitary_dft(x)
        scale = float(np.linalg.norm(x) / math.sqrt(x.size))
        for rows in [1, 3, 5, 9, 17, 33]:
            pre_max: list[float] = []
            post_max: list[float] = []
            for _ in range(5):
                pre = predecode_median_fft(x, m, rows, rng)
                post = postdecode_median_fft(x, m, rows, rng)
                pre_max.append(float(np.max(np.abs(pre - exact)) / scale))
                post_max.append(float(np.max(np.abs(post - exact)) / scale))
            median_comparison.append(
                {
                    "case": name,
                    "K": k,
                    "M": m,
                    "rows": rows,
                    "predecode_normalized_max_median": float(np.median(pre_max)),
                    "postdecode_normalized_max_median": float(np.median(post_max)),
                    "predecode_cost_proxy": predecode_cost_proxy(k * m, m, rows),
                    "postdecode_cost_proxy": postdecode_cost_proxy(k * m, m, rows),
                }
            )

    # 4. Exact recovery on locally Fourier-sparse inputs.
    sparse_recovery: list[dict[str, Any]] = []
    k, m = 4096, 8
    for h in [1, 2, 4, 8]:
        for rows in [3, 5, 7]:
            successes = 0
            trials = 12
            max_errors: list[float] = []
            for _ in range(trials):
                x, _ = make_local_sparse_signal(k, m, h, rng)
                exact = exact_unitary_dft(x)
                got = predecode_median_fft(x, m, rows, rng)
                err = float(np.max(np.abs(got - exact)))
                max_errors.append(err)
                successes += int(err < 1e-10)
            sparse_recovery.append(
                {
                    "K": k,
                    "M": m,
                    "h": h,
                    "rows": rows,
                    "successes": successes,
                    "trials": trials,
                    "empirical_failure_rate": 1.0 - successes / trials,
                    "union_failure_upper_bound": local_sparse_failure_bound(k * m, m, rows, h),
                    "median_max_error": float(np.median(max_errors)),
                }
            )

    # 5. Exact heavy-tail/kurtosis obstruction.
    tone_moments: list[dict[str, Any]] = []
    for k, m in [(64, 8), (128, 8), (128, 16), (256, 16), (512, 16)]:
        theory = tone_moment_theory(k, m)
        empirical = simulate_tone_moments(k, m, 60000, rng)
        tone_moments.append({"K": k, "M": m, **theory, **empirical})

    # 6. Asymptotic cost/error proxy for the explicit theorem regime.
    asymptotic: list[dict[str, Any]] = []
    a = 1.0
    eps = 0.25
    for log2_n in [32, 64, 128, 256, 512, 1024, 2048]:
        loglog = math.log2(log2_n)
        rows = max(3, int(math.ceil((1 + a) * log2_n / (eps * loglog))))
        if rows % 2 == 0:
            rows += 1
        # Basic M~log N regime, rounded to a power of two proxy.
        m = 2.0 ** math.floor(math.log2(log2_n))
        cost_per_n = rows * (2.0 + (log2_n - math.log2(m)) / m) + math.log2(m)
        # Omit fixed binomial/2 constants: this is the asymptotic exponent proxy.
        error_factor = m * 2.0 ** ((1 + a) * log2_n / (rows + 1))
        memory_over_n = 1.0 + rows / m + 2.0 * rows * m * math.exp2(-log2_n)
        asymptotic.append(
            {
                "log2_N": log2_n,
                "rows": rows,
                "M_proxy": m,
                "cost_over_Nlog2N": cost_per_n / log2_n,
                "error_factor_over_energy_coefficient_scale": error_factor,
                "target_polylog_proxy": log2_n ** (1 + eps),
                "memory_cells_over_N": memory_over_n,
            }
        )

    all_ratios = [
        value
        for row in local_variance_checks
        for value in (row["ratio_min"], row["ratio_max"], row["ratio_median"])
    ]
    return {
        "metadata": {
            "seed": seed,
            "algorithm": "predecode-median frequency-shift Fourier sketch",
            "normalization": "unitary DFT",
        },
        "summary": {
            "max_one_row_equivalence_error": max(r["max_abs_difference"] for r in equivalence),
            "local_variance_ratio_min": min(all_ratios),
            "local_variance_ratio_max": max(all_ratios),
            "number_of_equivalence_checks": len(equivalence),
            "number_of_local_variance_checks": len(local_variance_checks),
            "number_of_median_comparisons": len(median_comparison),
            "number_of_sparse_recovery_checks": len(sparse_recovery),
            "number_of_tone_moment_checks": len(tone_moments),
        },
        "one_row_equivalence": equivalence,
        "local_variance_checks": local_variance_checks,
        "median_comparison": median_comparison,
        "local_sparse_exact_recovery": sparse_recovery,
        "tone_moment_barrier": tone_moments,
        "asymptotic_proxies": asymptotic,
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
