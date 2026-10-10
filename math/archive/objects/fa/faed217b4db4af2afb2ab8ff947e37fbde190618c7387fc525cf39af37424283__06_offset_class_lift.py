#!/usr/bin/env python3
"""Hero #0: exact offset classes + dyadic unit-step-chirp randomized estimator.

A fresh arbitrary complex length-n vector is embedded in Q=2^ceil(log2(n)).
The fractional offsets of k*Q/n have h=n/gcd(n,Q) exact classes.
Each class is a modulation followed by a *single* length-Q chirp sketch;
no Bessel order expansion is used. This is a randomized approximate FFT
with EXACT expectation (ideal arithmetic), not an exact FFT algorithm.

The dyadic core unit_step_core.py is preserved from the user's v11 project.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
import numpy as np

import unit_step_core as core


def next_power_of_radix(n: int, radix: int) -> int:
    if n < 1 or radix < 2:
        raise ValueError("invalid n or radix")
    # The dyadic core supports prime-power moduli, not arbitrary composite radices.
    for d in range(2,math.isqrt(radix)+1):
        if radix%d == 0:
            raise ValueError("radix must be prime")
    q=radix
    while q<n:
        q*=radix
    return q


def next_power_of_two(n: int) -> int:
    return next_power_of_radix(n, 2)


@dataclass(frozen=True)
class OffsetPlan:
    n: int
    q: int
    m: int
    cofactor: int
    radix: int
    # For each output, its exact nearest-grid frequency and signed numerator.
    indices: np.ndarray
    theta_numerators: np.ndarray

    @classmethod
    def build(cls, n: int, m: int | None = None, radix: int = 2) -> 'OffsetPlan':
        q = next_power_of_radix(n,radix)
        if m is None:
            # M=Theta(log Q) for any fixed radix; M^2<=Q.
            ceiling=min(math.isqrt(q),max(radix,math.ceil(math.log2(q))))
            m=1
            while m*radix<=ceiling:
                m*=radix
        core.validate_dimensions(q, m)
        idx = np.empty(n, dtype=np.int64)
        signed = np.empty(n, dtype=np.int64)
        for k in range(n):
            j = (2*k*q+n)//(2*n)
            idx[k] = j
            signed[k] = k*q-j*n
        h = n // math.gcd(n,q)
        assert len(set(map(int,signed))) == h
        assert np.max(np.abs(signed),initial=0)*2 <= n
        assert np.unique(idx).size==n
        return cls(n=n, q=q, m=m, cofactor=h, radix=radix, indices=idx,
                   theta_numerators=signed)

    def classes(self) -> list[tuple[int,np.ndarray]]:
        return [(int(t), np.flatnonzero(self.theta_numerators==t))
                for t in np.unique(self.theta_numerators)]


def row_estimate(x, plan: OffsetPlan, state: core.ChirpState,
                 *, max_classes: int | None = None) -> np.ndarray:
    """O(h*Q) ideal-arithmetic steps at M=Theta(log Q).

    Uses the same state for all offset classes. Different states across
    repeated rows must be independently sampled to use median concentration.
    """
    arr = np.asarray(x, dtype=np.complex128).reshape(-1)
    if arr.size != plan.n:
        raise ValueError('length mismatch')
    if max_classes is not None and plan.cofactor > max_classes:
        raise ValueError('number of offset classes exceeds budget')
    state.validate(plan.q)
    if not np.any(arr):
        return np.zeros(plan.n, dtype=np.complex128)
    out = np.empty(plan.n, dtype=np.complex128)
    padded = np.zeros(plan.q, dtype=np.complex128)
    nn = np.arange(plan.n, dtype=np.float64)
    scale = math.sqrt(plan.q/plan.n)
    for numerator, ks in plan.classes():
        theta = numerator/plan.n
        # All k in this class have kQ/n = j_k + theta *exactly*.
        # The Q-DFT of y_theta at j_k therefore equals the N-DFT of x
        # at k, multiplied by sqrt(n/Q), with no approximation error.
        padded[:plan.n] = arr * np.exp((-2j*math.pi*theta/plan.q)*nn)
        # This randomized dyadic sketch introduces variance; the lift does not.
        spectrum = core.one_row_estimate(padded,plan.m,state)
        out[ks] = scale*spectrum[plan.indices[ks]]
    return out


def robust_estimate(x, plan: OffsetPlan, rows: int, seed: int=20261009,
                    *, max_classes: int | None = None) -> np.ndarray:
    if rows < 1 or rows%2 != 1:
        raise ValueError('rows must be positive and odd')
    rng = np.random.default_rng(seed)
    if rows==1:
        return row_estimate(x,plan,core.draw_state(plan.q,rng),max_classes=max_classes)
    buf = np.empty((rows,plan.n),dtype=np.complex128)
    for j in range(rows):
        buf[j] = row_estimate(x,plan,core.draw_state(plan.q,rng),max_classes=max_classes)
    return np.median(buf.real,axis=0)+1j*np.median(buf.imag,axis=0)


def expected_variance_ceiling(x, plan: OffsetPlan) -> float:
    """Bound on E|one_row(k) - unitary_DFT(x)[k]|^2, all k."""
    return (plan.m/plan.n)*float(np.vdot(x,x).real)


def polynomial_error_failure_bound(n: int, m: int, rows: int, alpha: float) -> float:
    """Chebyshev + coordinate-median + union bound, threshold sqrt(2)n^-alpha ||x||2.

    Returns a conservative bound, not the actual failure probability.
    """
    if rows<1 or rows%2!=1 or not (0.0<alpha<0.5):
        raise ValueError('invalid parameters')
    p=min(1.0,m*n**(2*alpha-1))
    majority=(rows+1)//2
    return min(1.0,2*n*(2**rows)*p**majority)


def reference(x):
    x=np.asarray(x,dtype=np.complex128)
    return np.fft.fft(x)/math.sqrt(x.size)
