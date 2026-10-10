#!/usr/bin/env python3
"""Information-rank certificates for projected Green measurement transcripts.

A projected row that records one scalar per block exposes at most K independent
linear measurements. No subsequent Green scan, FFT, resampler, or nonlinear
postprocessor can recover every arbitrary input exactly from a transcript with
fewer than N independent scalars.

The adaptive statement follows by taking the branch selected by the all-zero
transcript and choosing a nonzero vector in the common kernel of all linear
measurements on that branch.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import math
import random
import sympy as sp

from permutation_displacement import rank_mod, find_prime_root, fourier_matrix


def null_vector_mod(matrix: Sequence[Sequence[int]], p: int) -> list[int] | None:
    a = [list(map(lambda x: int(x) % p, row)) for row in matrix]
    if not a:
        return [1]
    m, n = len(a), len(a[0])
    pivots = []
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], p - 2, p)
        a[r] = [(v * inv) % p for v in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [(a[i][j] - q * a[r][j]) % p for j in range(n)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    free = next((c for c in range(n) if c not in set(pivots)), None)
    if free is None:
        return None
    x = [0] * n
    x[free] = 1
    for row in range(len(pivots) - 1, -1, -1):
        c = pivots[row]
        x[c] = (-sum(a[row][j] * x[j] for j in range(c + 1, n))) % p
    if not any(x):
        raise AssertionError("zero null vector")
    for row in matrix:
        if sum((int(v) % p) * x[j] for j, v in enumerate(row)) % p:
            raise AssertionError("nullspace failure")
    return x


def matvec(a: Sequence[Sequence[int]], x: Sequence[int], p: int) -> list[int]:
    return [sum((int(v) % p) * x[j] for j, v in enumerate(row)) % p for row in a]


def balanced_partition(n: int, k: int, shift: int = 0) -> list[list[int]]:
    if not 1 <= k <= n:
        raise ValueError
    q, r = divmod(n, k)
    blocks = []
    pos = 0
    for b in range(k):
        size = q + (b < r)
        blocks.append([((pos + t + shift) % n) for t in range(size)])
        pos += size
    return blocks


def measurement_matrix(n: int, partitions: Sequence[Sequence[Sequence[int]]], p: int,
                       seed: int = 20261010) -> list[list[int]]:
    rng = random.Random(seed)
    rows: list[list[int]] = []
    for part in partitions:
        seen = sorted(i for block in part for i in block)
        if seen != list(range(n)):
            raise ValueError("each row must partition all coordinates")
        for block in part:
            row = [0] * n
            for j in block:
                row[j] = rng.randrange(1, p)
            rows.append(row)
    return rows


def complete_local_fourier_measurements(n: int, m: int, p: int) -> list[list[int]]:
    """M rows on a fixed partition, giving a full local Fourier frame."""
    if n % m:
        raise ValueError
    k = n // m
    _, root = find_prime_root(m)
    # find_prime_root may return a different prime; derive m-th root in p.
    if (p - 1) % m:
        raise ValueError("p-1 must be divisible by m")
    primitive = int(sp.primitive_root(p))
    w = pow(primitive, (p - 1) // m, p)
    rows = []
    for r in range(m):
        for b in range(k):
            row = [0] * n
            for t in range(m):
                row[b * m + t] = pow(w, r * t, p)
            rows.append(row)
    return rows


def transcript_certificate(n: int, block_counts: Sequence[int], shifts: Sequence[int] | None = None,
                           seed: int = 20261010) -> dict:
    p, omega = find_prime_root(n)
    shifts = list(shifts or range(len(block_counts)))
    parts = [balanced_partition(n, k, shifts[i] % n) for i, k in enumerate(block_counts)]
    a = measurement_matrix(n, parts, p, seed)
    rank = rank_mod(a, p)
    total = sum(block_counts)
    witness = null_vector_mod(a, p)
    dft_nonzero = None
    if witness is not None:
        f = fourier_matrix(n, p, omega)
        y = matvec(f, witness, p)
        dft_nonzero = any(y)
        if not dft_nonzero:
            raise AssertionError("invertible DFT killed nonzero witness")
    return {
        "n": n,
        "block_counts": list(block_counts),
        "total_scalar_measurements": total,
        "rank": rank,
        "rank_upper_bound": min(n, total),
        "has_common_kernel_witness": witness is not None,
        "witness_dft_nonzero": dft_nonzero,
    }


def adaptive_zero_path_certificate(n: int, k_per_round: Sequence[int], seed: int = 20261010) -> dict:
    """Certify failure on the all-zero adaptive branch when total measurements<N."""
    # A deterministic adaptive algorithm sees only zeros on x=0. Its chosen
    # measurements on that branch are therefore fixed. A common-kernel vector
    # follows the identical branch and is indistinguishable from zero.
    rec = transcript_certificate(n, k_per_round, seed=seed)
    rec["adaptive_interpretation"] = (
        "zero input and the nonzero common-kernel witness generate the same all-zero transcript, "
        "so any deterministic decoder following this branch returns the same answer for both"
    )
    return rec


def separate_execution_lower_bound(n: int, r: int) -> dict:
    """Idealized best proxy with R independently executed rows.

    Each row pays N for a full scan and K_i log2 K_i for its K_i transform.
    Exact rank coverage requires sum K_i >= N. Convexity is minimized by equal
    K_i=N/R (continuous relaxation).
    """
    if not 1 <= r <= n:
        raise ValueError
    k = n / r
    proxy = r * n + n * math.log2(k)
    baseline = n * math.log2(n)
    return {
        "n": n,
        "rows": r,
        "equalized_K": k,
        "lower_bound_proxy": proxy,
        "baseline_N_log2_N": baseline,
        "ratio_to_baseline": proxy / baseline,
    }


def shift_polynomial_gate(n: int, coeffs: Sequence[int]) -> dict:
    """Verify F p(Z)=p(D) F in an exact finite field."""
    p, omega = find_prime_root(n)
    f = fourier_matrix(n, p, omega)
    # Z e_j=e_(j+1), so F Z = diag(omega^k) F with our convention.
    z = [[0] * n for _ in range(n)]
    for j in range(n):
        z[(j + 1) % n][j] = 1
    # Polynomial p(Z).
    eye = [[int(i == j) for j in range(n)] for i in range(n)]
    pz = [[0] * n for _ in range(n)]
    power = eye
    from permutation_displacement import matmul
    for c in coeffs:
        for i in range(n):
            for j in range(n):
                pz[i][j] = (pz[i][j] + c * power[i][j]) % p
        power = matmul(power, z, p)
    left = matmul(f, pz, p)
    right = [[0] * n for _ in range(n)]
    for k in range(n):
        val = 0
        wk = pow(omega, k, p)
        pw = 1
        for c in coeffs:
            val = (val + c * pw) % p
            pw = pw * wk % p
        for j in range(n):
            right[k][j] = val * f[k][j] % p
    ok = left == right
    if not ok:
        raise AssertionError("shift polynomial identity failed")
    return {"n": n, "degree": len(coeffs) - 1, "verified": ok, "prime": p}


if __name__ == "__main__":
    import json
    records = {
        "transcripts": [
            transcript_certificate(32, [4]),
            transcript_certificate(32, [4, 4, 4, 4, 4, 4, 4]),
            transcript_certificate(32, [4] * 8),
            transcript_certificate(60, [30, 20, 10], shifts=[0, 1, 2]),
        ],
        "adaptive": adaptive_zero_path_certificate(64, [8] * 7),
        "costs": [separate_execution_lower_bound(2**20, r) for r in range(1, 17)],
        "shift_polynomial": [shift_polynomial_gate(n, [3, 5, 7, 11]) for n in (8, 9, 16, 25)],
    }
    print(json.dumps(records, indent=2))
