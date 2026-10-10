#!/usr/bin/env python3
"""Exact joint decoder for the complete beta-shifted Green frame.

For Q=K*M, fixed unit a and beta_r=beta0+r*K, r=0..M-1, the
complete-frame average equals the exact unitary Q-DFT.  A literal evaluator
runs M Green scans.  This module exposes the joint polyphase algebra:

  1) batch the M block summaries with an M-IFFT in every block;
  2) K-FFT every summary channel;
  3) M-FFT across channels demixes the local coordinate t;
  4) dechirp/reindex to recover the K-FFT of each polyphase column;
  5) finish with K independent M-FFTs.

The two M transforms around the K transforms commute and cancel algebraically;
a collapsed implementation is exactly the ordinary mixed-radix Cooley--Tukey
factorization.  Thus the exact Green-frame batching gate closes at O(Q log Q),
not below it.
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any
import numpy as np

try:
    from phase4_source.composite_cycle_core import (
        ChirpState, local_phase_matrix, compress_blocks, decode_balanced_scan,
    )
except ImportError:
    from composite_cycle_core import (
        ChirpState, local_phase_matrix, compress_blocks, decode_balanced_scan,
    )


def validate(q: int, m: int, a: int) -> int:
    if q < 2 or m < 1 or q % m:
        raise ValueError("require Q=K*M")
    k = q // m
    if k < m:
        raise ValueError("require K>=M for inherited Green executor")
    if not (0 < a < q) or math.gcd(a, q) != 1:
        raise ValueError("a must be a unit modulo Q")
    return k


def batched_summaries(x: np.ndarray, m: int, a: int = 1, beta0: int = 0) -> np.ndarray:
    """Return D[r,b] for all beta_r=beta0+r*K in O(Q log M)."""
    arr = np.asarray(x, dtype=np.complex128).reshape(-1)
    q = arr.size
    k = validate(q, m, a)
    base = local_phase_matrix(q, m, ChirpState(a, beta0 % q))
    local = base * arr.reshape(k, m)
    return (m * np.fft.ifft(local, axis=1)).T


def joint_from_batched_summaries(
    summaries: np.ndarray, q: int, m: int, a: int = 1, beta0: int = 0
) -> np.ndarray:
    """Jointly decode all M complete-frame channels into the exact unitary DFT."""
    k = validate(q, m, a)
    d = np.asarray(summaries, dtype=np.complex128)
    if d.shape != (m, k):
        raise ValueError(f"summaries must have shape {(m, k)}")

    # M length-K FFTs.  F[r,p] = sum_t c_t e^(2pi i rt/M) H_t[p-a t].
    f = np.fft.fft(d, axis=1)
    # Demix the beta character.  G[t,p] = c_t H_t[p-a t].
    g = np.fft.fft(f, axis=0) / m

    c = local_phase_matrix(q, m, ChirpState(a, beta0 % q))[0]
    h = np.empty((m, k), dtype=np.complex128)
    for t in range(m):
        shift = (a * t) % k
        h[t] = np.roll(g[t], -shift) / c[t]

    # Cooley--Tukey recombination: k=q0+K*s.
    out = np.empty(q, dtype=np.complex128)
    tt = np.arange(m, dtype=np.float64)
    for q0 in range(k):
        lanes = h[:, q0] * np.exp(-2j * np.pi * q0 * tt / q)
        z = np.fft.fft(lanes) / math.sqrt(q)
        out[q0 + k * np.arange(m)] = z
    return out


def joint_green_frame_exact(x: np.ndarray, m: int, a: int = 1, beta0: int = 0) -> np.ndarray:
    arr = np.asarray(x, dtype=np.complex128).reshape(-1)
    return joint_from_batched_summaries(batched_summaries(arr, m, a, beta0), arr.size, m, a, beta0)


def mixed_radix_collapsed(x: np.ndarray, m: int) -> np.ndarray:
    """The algebraically collapsed joint frame: ordinary mixed-radix FFT."""
    arr = np.asarray(x, dtype=np.complex128).reshape(-1)
    q = arr.size
    if q % m:
        raise ValueError("M must divide Q")
    k = q // m
    h = np.fft.fft(arr.reshape(k, m), axis=0)  # H[t,q0], stored q0,t
    out = np.empty(q, dtype=np.complex128)
    tt = np.arange(m, dtype=np.float64)
    for q0 in range(k):
        lanes = h[q0, :] * np.exp(-2j * np.pi * q0 * tt / q)
        z = np.fft.fft(lanes) / math.sqrt(q)
        out[q0 + k * np.arange(m)] = z
    return out


def naive_complete_frame(x: np.ndarray, m: int, a: int = 1, beta0: int = 0) -> np.ndarray:
    """Reference only: average M separately decoded Green rows."""
    arr = np.asarray(x, dtype=np.complex128).reshape(-1)
    q = arr.size
    k = validate(q, m, a)
    out = np.zeros(q, dtype=np.complex128)
    for r in range(m):
        state = ChirpState(a, (beta0 + r * k) % q)
        d = compress_blocks(arr, m, state)
        out += decode_balanced_scan(d, q, m, state)
    return out / m


@dataclass(frozen=True)
class WorkLedger:
    q: int
    m: int
    k: int
    naive_green_scans: int
    naive_scan_length: int
    naive_k_ffts: int
    joint_k_ffts: int
    joint_m_ffts: int
    collapsed_k_ffts: int
    collapsed_m_ffts: int
    asymptotic_naive: str
    asymptotic_joint: str
    conclusion: str


def work_ledger(q: int, m: int) -> dict[str, Any]:
    k = validate(q, m, 1)
    rec = WorkLedger(
        q=q, m=m, k=k,
        naive_green_scans=m, naive_scan_length=q, naive_k_ffts=m,
        joint_k_ffts=m, joint_m_ffts=2 * k + k,
        collapsed_k_ffts=m, collapsed_m_ffts=k,
        asymptotic_naive="Theta(Q*M + Q*log K)",
        asymptotic_joint="Theta(Q*log K + Q*log M) = Theta(Q*log Q)",
        conclusion="Complete Green-frame fusion is exactly mixed-radix Cooley--Tukey, not an exact sub-QlogQ advance.",
    )
    return asdict(rec)
