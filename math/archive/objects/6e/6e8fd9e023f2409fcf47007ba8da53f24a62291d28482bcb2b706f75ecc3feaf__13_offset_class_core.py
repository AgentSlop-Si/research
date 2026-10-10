#!/usr/bin/env python3
"""Offset-class prime-power lift and scan-fusion rank gate (v12).

This module extends the v9/v11 research line in two ways:

1. For an arbitrary original length N and a prime-power lift Q=p^E >= N,
   the nearest-grid offsets take exactly L=N/gcd(N,Q) distinct values.
   One exact phase-modulated v9 row per offset class gives an unbiased
   estimator of the exact N-point DFT, with no Bessel/Jacobi--Anger
   truncation.  Its per-output variance remains at most M||x||_2^2/N.

2. A black-box linear scan-fusion gate proves that, once R independent
   dyadic channels have already been materialized, any one-pass linear
   state carrying their first forcing term to R distinct offset queries
   needs at least R scalar state coordinates.  This is a restricted
   architecture barrier, not a lower bound for all Fourier algorithms.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import numpy.typing as npt

import unit_step_core as core

ComplexArray = npt.NDArray[np.complex128]


def is_prime(p: int) -> bool:
    if p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    q = 3
    while q * q <= p:
        if p % q == 0:
            return False
        q += 2
    return True


def next_prime_power(n: int, p: int) -> int:
    """Smallest p^E >= n, for prime p."""
    if n < 1:
        raise ValueError("n must be positive")
    if not is_prime(p):
        raise ValueError("p must be prime")
    q = 1
    while q < n:
        q *= p
    return q


def choose_prime_power_block(q: int, p: int) -> int:
    """Choose a p-power block M ~ log Q with M^2 <= Q.

    This keeps one v9 row at O(Q + (Q/M) log(Q/M)).  M=1 is permitted for
    very small or low-exponent prime powers, but then the row may cost
    Theta(Q log Q), which the planner charges explicitly.
    """
    if not is_prime(p):
        raise ValueError("p must be prime")
    # Verify q is a p-power.
    tmp = q
    while tmp % p == 0:
        tmp //= p
    if tmp != 1:
        raise ValueError("q must be a power of p")
    target = max(1.0, math.log(q))
    m = 1
    while m * p <= target and (m * p) ** 2 <= q:
        m *= p
    while m * m > q:
        m //= p
    return max(1, m)


def exact_nearest_grid_map(n: int, q: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Nearest Q-grid map for N target frequencies using exact integers.

    j_k = floor(kQ/N + 1/2), theta_k = kQ/N - j_k = theta_num/N.
    The map is injective whenever Q>=N.
    """
    if n < 1 or q < n:
        raise ValueError("require q >= n >= 1")
    j = np.empty(n, dtype=np.int64)
    theta_num = np.empty(n, dtype=np.int64)
    for k in range(n):
        jk = (2 * k * q + n) // (2 * n)
        if jk >= q:
            # This can only occur at the right endpoint under a tie; wrap the
            # frequency modulo Q and preserve the centered residual.
            jk %= q
        j[k] = jk
        theta_num[k] = k * q - jk * n
        # Center the exact residue if the wrapped convention moved it.
        while theta_num[k] > n // 2:
            theta_num[k] -= n
        while theta_num[k] < -(n // 2):
            theta_num[k] += n
    if np.unique(j).size != n:
        raise AssertionError("nearest-grid map must be injective for q>=n")
    if np.max(np.abs(theta_num), initial=0) * 2 > n:
        raise AssertionError("offset exceeded one half")
    return j, theta_num, theta_num.astype(np.float64) / float(n)


def offset_class_count(n: int, q: int) -> int:
    """Exact number of fractional-offset classes."""
    if q < n:
        raise ValueError("q must be at least n")
    return n // math.gcd(n, q)


def offset_classes(n: int, q: int) -> dict[int, np.ndarray]:
    """Map centered theta numerators to target output indices."""
    _, nums, _ = exact_nearest_grid_map(n, q)
    out: dict[int, list[int]] = {}
    for k, num in enumerate(nums.tolist()):
        out.setdefault(int(num), []).append(k)
    result = {num: np.asarray(indices, dtype=np.int64) for num, indices in out.items()}
    expected = offset_class_count(n, q)
    if len(result) != expected:
        raise AssertionError(f"class count mismatch: {len(result)} != {expected}")
    return result


def normalized_dft(x: npt.ArrayLike) -> ComplexArray:
    arr = np.asarray(x, dtype=np.complex128)
    return np.fft.fft(arr) / math.sqrt(arr.size)


@dataclass
class PrimePowerRowPlan:
    """Reusable structural plan for multiple inputs under one chirp state."""

    q: int
    block: int
    state: core.ChirpState
    phase: np.ndarray
    idx: np.ndarray
    gauge: np.ndarray
    boundary: np.ndarray
    src1: np.ndarray
    src2: np.ndarray

    @classmethod
    def build(cls, q: int, block: int, state: core.ChirpState) -> "PrimePowerRowPlan":
        _, k, _ = core.validate_dimensions(q, block)
        state.validate(q)
        phase = core.local_phase_matrix(q, block, state)
        j = np.arange(q, dtype=np.int64)
        idx = (state.a * j) % q
        tri_j = core._tri_array_mod(j, q)
        phase_n = ((state.a % q) * tri_j + (state.beta * j) % q) % q
        phase_2q = (2 * phase_n + (q & 1) * j) % (2 * q)
        gauge = np.exp(1j * np.pi * phase_2q.astype(np.float64) / q)
        boundary_n = (
            block * ((idx + state.beta) % q)
            + state.a * (core.tri_int(block) % q)
        ) % q
        boundary_2q = (2 * boundary_n + (q & 1) * block) % (2 * q)
        boundary = np.exp(-1j * np.pi * boundary_2q.astype(np.float64) / q)
        return cls(
            q=q, block=block, state=state, phase=phase, idx=idx, gauge=gauge,
            boundary=boundary, src1=idx % k,
            src2=(idx + state.a * block) % k,
        )

    def apply(self, padded: npt.ArrayLike, dtype: Any = np.complex128) -> ComplexArray:
        _, k, _ = core.validate_dimensions(self.q, self.block)
        arr = np.asarray(padded, dtype=np.complex128)
        if arr.shape != (self.q,):
            raise ValueError("padded input has wrong shape")
        summaries = core.pairwise_sum_axis1(
            self.phase * arr.reshape(k, self.block), np.complex128
        )
        d_fft = np.asarray(np.fft.fft(summaries), dtype=dtype)
        gauge = self.gauge.astype(dtype, copy=False)
        forcing = (
            d_fft[self.src1]
            - self.boundary.astype(dtype, copy=False) * d_fft[self.src2]
        ) / math.sqrt(self.q)
        terms = (forcing / gauge).astype(dtype)
        seed = np.asarray(core.pairwise_sum(terms, dtype) / 2.0, dtype=dtype).item()
        prefix = core.balanced_exclusive_scan(terms, dtype)
        out = np.empty(self.q, dtype=dtype)
        out[self.idx] = gauge * (seed - prefix)
        return out.astype(np.complex128)

    def apply_batch(self, padded: npt.ArrayLike, dtype: Any = np.complex128) -> np.ndarray:
        """Vectorized application to a small batch of class inputs.

        This uses O(batch*Q) workspace and is therefore intended only when
        the exact offset-class count is small.  The streaming theorem uses
        ``apply`` sequentially and retains O(Q+N) storage.
        """
        _, k, _ = core.validate_dimensions(self.q, self.block)
        arr = np.asarray(padded, dtype=np.complex128)
        if arr.ndim != 2 or arr.shape[1] != self.q:
            raise ValueError("padded batch must have shape (batch,Q)")
        batch = arr.shape[0]
        summaries = np.sum(
            arr.reshape(batch, k, self.block) * self.phase[None, :, :], axis=2
        )
        d_fft = np.asarray(np.fft.fft(summaries, axis=1), dtype=dtype)
        gauge = self.gauge.astype(dtype, copy=False)
        boundary = self.boundary.astype(dtype, copy=False)
        forcing = (
            d_fft[:, self.src1] - boundary[None, :] * d_fft[:, self.src2]
        ) / math.sqrt(self.q)
        terms = (forcing / gauge[None, :]).astype(dtype)
        seed = np.sum(terms, axis=1, dtype=dtype) / 2.0

        size = 1 << (self.q - 1).bit_length()
        work = np.zeros((batch, size), dtype=dtype)
        work[:, : self.q] = terms
        stride = 2
        while stride <= size:
            right = np.arange(stride - 1, size, stride)
            left = right - stride // 2
            work[:, right] = work[:, left] + work[:, right]
            stride *= 2
        work[:, -1] = 0.0 + 0.0j
        stride = size
        while stride >= 2:
            right = np.arange(stride - 1, size, stride)
            left = right - stride // 2
            tmp = work[:, left].copy()
            work[:, left] = work[:, right]
            work[:, right] = work[:, right] + tmp
            stride //= 2
        prefix = work[:, : self.q]
        out = np.empty((batch, self.q), dtype=dtype)
        out[:, self.idx] = gauge[None, :] * (seed[:, None] - prefix)
        return out.astype(np.complex128)


def phase_modulated_padded_input(
    x: npt.ArrayLike, q: int, theta_num: int
) -> ComplexArray:
    """Build y_theta[n]=x[n] exp(-2pi i n theta/Q), zero-padded to Q.

    theta = theta_num / N.  Consequently a Q-DFT sample at j_k equals the
    desired N-grid Fourier sample at k, up to the normalization sqrt(Q/N).
    """
    arr = np.asarray(x, dtype=np.complex128)
    n = arr.size
    idx = np.arange(n, dtype=np.float64)
    phase = np.exp(-2j * np.pi * idx * float(theta_num) / float(n * q))
    padded = np.zeros(q, dtype=np.complex128)
    padded[:n] = arr * phase
    return padded


def offset_class_row(
    x: npt.ArrayLike,
    p: int,
    state: core.ChirpState,
    block: int | None = None,
    dtype: Any = np.complex128,
) -> ComplexArray:
    """One unbiased exact-center N-output row via distinct offset classes.

    A single chirp state is shared across all classes.  For each centered
    offset theta, one phase-modulated Q-input is evaluated by the v9
    prime-power row and only the outputs belonging to that class are kept.
    """
    arr = np.asarray(x, dtype=np.complex128)
    if arr.ndim != 1 or arr.size < 1:
        raise ValueError("x must be a non-empty one-dimensional array")
    n = int(arr.size)
    q = next_prime_power(n, p)
    if block is None:
        block = choose_prime_power_block(q, p)
    core.validate_dimensions(q, block)
    state.validate(q)
    selected, nums, _ = exact_nearest_grid_map(n, q)
    classes = offset_classes(n, q)
    out = np.empty(n, dtype=np.complex128)
    scale = math.sqrt(q / n)
    plan = PrimePowerRowPlan.build(q, block, state)
    for num, targets in classes.items():
        padded = phase_modulated_padded_input(arr, q, num)
        row_q = plan.apply(padded, dtype)
        out[targets] = scale * row_q[selected[targets]]
    return out


def offset_class_row_batched(
    x: npt.ArrayLike,
    p: int,
    state: core.ChirpState,
    block: int | None = None,
    dtype: Any = np.complex128,
) -> ComplexArray:
    """Small-class vectorized variant using O(LQ) temporary storage."""
    arr = np.asarray(x, dtype=np.complex128)
    n = int(arr.size)
    q = next_prime_power(n, p)
    if block is None:
        block = choose_prime_power_block(q, p)
    selected, _, _ = exact_nearest_grid_map(n, q)
    classes = offset_classes(n, q)
    nums = list(classes)
    idx = np.arange(n, dtype=np.float64)[None, :]
    num_arr = np.asarray(nums, dtype=np.float64)[:, None]
    mod = np.exp(-2j * np.pi * idx * num_arr / float(n * q))
    padded = np.zeros((len(nums), q), dtype=np.complex128)
    padded[:, :n] = arr[None, :] * mod
    plan = PrimePowerRowPlan.build(q, block, state)
    rows = plan.apply_batch(padded, dtype)
    out = np.empty(n, dtype=np.complex128)
    scale = math.sqrt(q / n)
    for row_idx, num in enumerate(nums):
        targets = classes[num]
        out[targets] = scale * rows[row_idx, selected[targets]]
    return out


def offset_class_exact_center(x: npt.ArrayLike, p: int) -> ComplexArray:
    """The exact expectation of offset_class_row, equal to U_N x."""
    # Returned explicitly to make tests and theorem boundaries obvious.
    return normalized_dft(x)


def offset_class_variance_bound(x: npt.ArrayLike, p: int, block: int | None = None) -> float:
    """Per-output variance bound M||x||_2^2/N."""
    arr = np.asarray(x, dtype=np.complex128)
    n = arr.size
    q = next_prime_power(n, p)
    if block is None:
        block = choose_prime_power_block(q, p)
    core.validate_dimensions(q, block)
    return float(block * np.vdot(arr, arr).real / n)


def offset_class_work_proxy(n: int, p: int, block: int | None = None) -> float:
    """Charged scalar-arithmetic proxy for one complete N-output row."""
    q = next_prime_power(n, p)
    if block is None:
        block = choose_prime_power_block(q, p)
    _, k, _ = core.validate_dimensions(q, block)
    classes = offset_class_count(n, q)
    # Each class forms Q phases/summaries, one K-FFT, and one Q scan.
    return classes * (2.0 * q + k * math.log2(max(2, k)))


def bessel_tail_bound(rank: int) -> float:
    """Uniform Jacobi--Anger tail after orders 0,...,rank-1."""
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


def bessel_lift_work_proxy(n: int, rank: int | None = None) -> float:
    """v11 H=0 work proxy for comparison, using the dyadic lift."""
    q = next_prime_power(n, 2)
    block = choose_prime_power_block(q, 2)
    _, k, _ = core.validate_dimensions(q, block)
    if rank is None:
        # Main N^{-1/3}-scale deterministic tail used in prior checkpoints.
        rank = bessel_rank_for_tail(n ** (-1.0 / 3.0))
    return q + rank * (q + k * math.log2(max(2, k)))


@dataclass(frozen=True)
class LiftPlan:
    method: str
    prime: int
    q: int
    block: int
    classes: int
    rank: int
    work_proxy: float


def choose_adaptive_plan(
    n: int,
    primes: tuple[int, ...] = (2, 3, 5, 7),
    rank: int | None = None,
) -> LiftPlan:
    """Choose the cheapest exact-class or v11 Bessel plan by a charged proxy."""
    if rank is None:
        rank = bessel_rank_for_tail(n ** (-1.0 / 3.0))
    candidates: list[LiftPlan] = []
    for p in primes:
        q = next_prime_power(n, p)
        block = choose_prime_power_block(q, p)
        classes = offset_class_count(n, q)
        work = offset_class_work_proxy(n, p, block)
        candidates.append(LiftPlan("offset_classes", p, q, block, classes, 0, work))
    q2 = next_prime_power(n, 2)
    b2 = choose_prime_power_block(q2, 2)
    bwork = bessel_lift_work_proxy(n, rank)
    candidates.append(LiftPlan("bessel_rank", 2, q2, b2, 0, rank, bwork))
    return min(candidates, key=lambda item: item.work_proxy)


def streaming_offset_class_fft(
    x: npt.ArrayLike,
    p: int,
    rows: int,
    g: float,
    rng: np.random.Generator,
    block: int | None = None,
    dtype: Any = np.complex128,
) -> ComplexArray:
    """O(N)-memory robust aggregation of offset-class rows."""
    arr = np.asarray(x, dtype=np.complex128)
    n = arr.size
    q = next_prime_power(n, p)
    if block is None:
        block = choose_prime_power_block(q, p)
    if rows <= 0 or rows % 2 != 1:
        raise ValueError("rows must be positive and odd")
    norm = float(np.linalg.norm(arr))
    if norm == 0.0:
        return np.zeros(n, dtype=np.complex128)
    tau = g * math.sqrt(block / n) * norm
    real_state = core.MajorityGridState.zeros(n)
    imag_state = core.MajorityGridState.zeros(n)
    for _ in range(rows):
        state = core.draw_state(q, rng)
        row = offset_class_row(arr, p, state, block, dtype)
        core.majority_grid_update(real_state, row.real, tau)
        core.majority_grid_update(imag_state, row.imag, tau)
    return core.majority_grid_finalize(real_state, tau) + 1j * core.majority_grid_finalize(imag_state, tau)


def robust_uniform_radius(x: npt.ArrayLike, block: int, g: float) -> float:
    arr = np.asarray(x, dtype=np.complex128)
    return (5.0 / math.sqrt(2.0)) * g * math.sqrt(block / arr.size) * float(np.linalg.norm(arr))


# ---------------------------------------------------------------------------
# Exact black-box scan-fusion rank gate
# ---------------------------------------------------------------------------


def chebyshev_values_fraction(x: Fraction, rank: int) -> list[Fraction]:
    """Return T_0(x),...,T_{rank-1}(x) exactly."""
    if rank < 1:
        return []
    vals = [Fraction(1)]
    if rank == 1:
        return vals
    vals.append(x)
    for _ in range(2, rank):
        vals.append(2 * x * vals[-1] - vals[-2])
    return vals


def fraction_matrix_rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pv = a[rank][col]
        a[rank] = [v / pv for v in a[rank]]
        for r in range(rows):
            if r != rank and a[r][col] != 0:
                f = a[r][col]
                a[r] = [a[r][c] - f * a[rank][c] for c in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def scan_fusion_rank_certificate(n: int, rank: int, q: int | None = None) -> dict[str, Any]:
    """Exact rank certificate for the black-box channel scan gate.

    We use outputs with R distinct nearest-grid offsets.  If only the first
    forcing vector q_r[0] is nonzero, every later row output contains
    -q_r[0]/2 times a nonzero gauge.  The final Chebyshev combination is
    therefore a diagonally scaled Chebyshev-Vandermonde matrix.  Its exact
    rank is R, so a one-pass *linear* state passing this information across
    the cut after position zero must have at least R scalar coordinates.
    """
    if rank < 1:
        raise ValueError("rank must be positive")
    if q is None:
        q = next_prime_power(n, 2)
    _, nums, _ = exact_nearest_grid_map(n, q)
    unique: list[int] = []
    seen: set[int] = set()
    for num in nums.tolist():
        if num not in seen:
            seen.add(int(num))
            unique.append(int(num))
        if len(unique) == rank:
            break
    if len(unique) < rank:
        raise ValueError("not enough distinct offsets for requested rank")
    # x=2 theta = 2*num/n is rational.  Scalar factors 2(-i)^r and gauges
    # are nonzero and do not alter rank, so we certify the real T_r matrix.
    matrix = [chebyshev_values_fraction(Fraction(2 * num, n), rank) for num in unique]
    exact_rank = fraction_matrix_rank(matrix)
    return {
        "n": n,
        "q": q,
        "requested_rank": rank,
        "distinct_offsets_used": unique,
        "exact_chebyshev_rank": exact_rank,
        "state_dimension_lower_bound": exact_rank,
    }


def make_cases(n: int, rng: np.random.Generator) -> dict[str, ComplexArray]:
    idx = np.arange(n, dtype=np.float64)
    spike = np.zeros(n, dtype=np.complex128)
    spike[n // 3] = 1.0
    return {
        "flat": np.ones(n, dtype=np.complex128),
        "gaussian": rng.normal(size=n) + 1j * rng.normal(size=n),
        "random_phase": np.exp(2j * np.pi * rng.random(n)),
        "chirp": np.exp(2j * np.pi * (3 * idx * idx + 5 * idx) / n),
        "spike": spike,
    }


def run_experiments(seed: int = 20261009) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    results: dict[str, Any] = {}

    # Class-count and work table.
    class_table = []
    for n in [3 * (1 << 8), 5 * (1 << 8), 15 * (1 << 8), (1 << 12) - 1, 4093]:
        for p in [2, 3, 5]:
            q = next_prime_power(n, p)
            b = choose_prime_power_block(q, p)
            class_table.append({
                "N": n,
                "p": p,
                "Q": q,
                "M": b,
                "classes": offset_class_count(n, q),
                "work_proxy": offset_class_work_proxy(n, p, b),
            })
    results["class_table"] = class_table

    # Exhaustive state enumeration on small lifted moduli.  These checks are
    # exact up to floating-point evaluation of roots and do not confuse finite
    # Monte-Carlo fluctuation with bias.
    exhaustive = []
    max_exhaustive_mean_error = 0.0
    max_exhaustive_variance_ratio = 0.0
    for n, p0 in [(12, 2), (18, 3), (20, 2)]:
        q = next_prime_power(n, p0)
        block = choose_prime_power_block(q, p0)
        x = rng.normal(size=n) + 1j * rng.normal(size=n)
        all_rows = []
        for a in range(1, q):
            if math.gcd(a, q) != 1:
                continue
            for beta in range(q):
                all_rows.append(offset_class_row(x, p0, core.ChirpState(a, beta), block))
        sample = np.asarray(all_rows)
        target = normalized_dft(x)
        mean_error = float(np.max(np.abs(np.mean(sample, axis=0) - target)))
        empirical = np.mean(np.abs(sample - target[None, :]) ** 2, axis=0)
        bound = offset_class_variance_bound(x, p0, block)
        ratio = float(np.max(empirical) / bound)
        max_exhaustive_mean_error = max(max_exhaustive_mean_error, mean_error)
        max_exhaustive_variance_ratio = max(max_exhaustive_variance_ratio, ratio)
        exhaustive.append({
            "N": n, "p": p0, "Q": q, "M": block,
            "states": int(sample.shape[0]),
            "mean_max_error": mean_error,
            "max_variance_ratio": ratio,
        })
    results["exhaustive_state_checks"] = exhaustive
    results["max_exhaustive_mean_error"] = max_exhaustive_mean_error
    results["max_exhaustive_variance_ratio"] = max_exhaustive_variance_ratio

    # Empirical exact-center and variance checks on larger composite original lengths.
    variance_rows = []
    max_mean_error = 0.0
    max_variance_ratio = 0.0
    for n, p in [(48, 2), (80, 2), (45, 3), (75, 5)]:
        q = next_prime_power(n, p)
        block = choose_prime_power_block(q, p)
        for name, x in make_cases(n, rng).items():
            target = normalized_dft(x)
            samples = np.stack([
                offset_class_row(x, p, core.draw_state(q, rng), block)
                for _ in range(300)
            ])
            mean_error = float(np.max(np.abs(np.mean(samples, axis=0) - target)))
            empirical = np.mean(np.abs(samples - target[None, :]) ** 2, axis=0)
            bound = offset_class_variance_bound(x, p, block)
            ratio = float(np.max(empirical) / bound) if bound else 0.0
            max_mean_error = max(max_mean_error, mean_error)
            max_variance_ratio = max(max_variance_ratio, ratio)
            variance_rows.append({
                "N": n,
                "p": p,
                "Q": q,
                "M": block,
                "classes": offset_class_count(n, q),
                "case": name,
                "mean_max_error": mean_error,
                "max_variance_ratio": ratio,
            })
    results["variance_checks"] = variance_rows
    results["max_mean_error_300_rows"] = max_mean_error
    results["max_variance_ratio"] = max_variance_ratio

    # Robust end-to-end checks.
    robust_rows = []
    max_robust_ratio = 0.0
    for n, p in [(48, 2), (80, 2), (45, 3)]:
        q = next_prime_power(n, p)
        block = choose_prime_power_block(q, p)
        rows = 9
        g = 3.0
        for name, x in make_cases(n, rng).items():
            got = streaming_offset_class_fft(x, p, rows, g, rng, block)
            err = float(np.max(np.abs(got - normalized_dft(x))))
            radius = robust_uniform_radius(x, block, g)
            ratio = err / radius if radius else 0.0
            max_robust_ratio = max(max_robust_ratio, ratio)
            robust_rows.append({
                "N": n,
                "p": p,
                "case": name,
                "error": err,
                "radius": radius,
                "ratio": ratio,
            })
    results["robust_checks"] = robust_rows
    results["max_robust_ratio"] = max_robust_ratio

    # Exact scan rank certificates.
    certs = []
    for n, r in [(127, 8), (255, 10), (511, 12)]:
        certs.append(scan_fusion_rank_certificate(n, r))
    results["scan_rank_certificates"] = certs

    # Planner examples.
    planners = []
    for n in [3 * (1 << 20), 5 * (1 << 20), 15 * (1 << 20), (1 << 24) - 1, 16_777_213]:
        plan = choose_adaptive_plan(n)
        planners.append(plan.__dict__)
    results["adaptive_plans"] = planners
    return results


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results.json"))
    parser.add_argument("--seed", type=int, default=20261009)
    args = parser.parse_args(list(argv) if argv is not None else None)
    result = run_experiments(args.seed)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "max_exhaustive_mean_error": result["max_exhaustive_mean_error"],
        "max_exhaustive_variance_ratio": result["max_exhaustive_variance_ratio"],
        "max_monte_carlo_variance_ratio_300_rows": result["max_variance_ratio"],
        "max_robust_ratio": result["max_robust_ratio"],
        "rank_certificates": [c["exact_chebyshev_rank"] for c in result["scan_rank_certificates"]],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
