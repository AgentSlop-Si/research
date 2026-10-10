"""Relation-aware, lazy Fourier-state prototype (research, not a novel DFT theorem).

A dynamic input is represented by (base_signal, base_rfft, sparse_pending).
The input producer supplies exact edited indices and real-valued deltas.
The implementation uses floating-point SciPy rfft for practicality; mathematical
identities are exact only in ideal arithmetic.
"""
from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Iterable

import numpy as np
from scipy import fft
from phase import phases_tiled


class LazyRealFFT:
    def __init__(self, signal: Iterable[float]):
        self.base_signal = np.asarray(signal, dtype=np.float64).copy()
        if self.base_signal.ndim != 1 or not self.base_signal.size:
            raise ValueError("need a nonempty real one-dimensional signal")
        self.n = self.base_signal.size
        self.base_spectrum = fft.rfft(self.base_signal)
        self.base_signal.flags.writeable = False
        self.base_spectrum.flags.writeable = False
        self.pending: dict[int, float] = {}
        self.events = 0

    def fork(self):
        """Share immutable base FFT and signal, copy only the pending edits.

        O(k) metadata to fork a version with k pending positions, O(1) if
        forking an unedited base. No FFT is recomputed.
        """
        clone = object.__new__(LazyRealFFT)
        clone.n = self.n
        clone.base_signal = self.base_signal
        clone.base_spectrum = self.base_spectrum
        clone.pending = self.pending.copy()
        clone.events = self.events
        return clone

    @property
    def distinct_edits(self):
        return len(self.pending)

    def edit(self, position: int, delta: float):
        """Expected O(1) dictionary update; no Fourier arithmetic or dense write."""
        position = int(position)
        if not (0 <= position < self.n):
            raise IndexError("position outside signal")
        delta = float(delta)
        if not math.isfinite(delta):
            raise ValueError("edit must be finite")
        self.events += 1
        new = self.pending.get(position, 0.0) + delta
        if new == 0:
            self.pending.pop(position, None)
        else:
            self.pending[position] = new

    def frequency(self, q: int) -> complex:
        """O(k) exact-formula frequency query, k = distinct pending positions."""
        q = int(q)
        if not (0 <= q <= self.n // 2):
            raise IndexError("rfft frequency index out of range")
        z = complex(self.base_spectrum[q])
        for position, delta in self.pending.items():
            angle = -2 * math.pi * ((position * q) % self.n) / self.n
            z += delta * cmath.exp(1j * angle)
        return z

    def frequencies(self, indices: Iterable[int]) -> np.ndarray:
        """Evaluate selected frequencies, O(Q*k) vector operations."""
        qs = np.asarray(list(indices), dtype=np.int64)
        if np.any(qs < 0) or np.any(qs > self.n//2):
            raise IndexError("rfft frequency index out of range")
        out = self.base_spectrum[qs].copy()
        for position, delta in self.pending.items():
            angle = -2*np.pi*((qs*position) % self.n)/self.n
            out += delta * np.exp(1j*angle)
        return out

    def materialize_direct(self, tiled: bool = True) -> np.ndarray:
        """O(N*k) arithmetic: explicitly produce every frequency."""
        out = self.base_spectrum.copy()
        for position, delta in self.pending.items():
            if tiled:
                phase = phases_tiled(self.n, position)
            else:
                qs = np.arange(out.size, dtype=np.int64)
                phase = np.exp((-2j*np.pi/self.n)*((qs*position) % self.n))
            out += delta*phase
        # The real-input transform has real DC and, for even lengths, Nyquist.
        out[0] = out[0].real
        if self.n % 2 == 0:
            out[-1] = out[-1].real
        return out

    def signal(self):
        out = self.base_signal.copy()
        for position, delta in self.pending.items():
            out[position] += delta
        return out

    def materialize_fresh(self):
        """O(N log N) production fallback, including pending-application copies."""
        return fft.rfft(self.signal())

    def materialize(self, direct_threshold: int = 0):
        if self.distinct_edits <= direct_threshold:
            return self.materialize_direct()
        return self.materialize_fresh()

    def commit(self, direct_threshold: int = 0):
        """Replace base with latest signal and spectrum; clear pending deltas."""
        new_base = self.signal()
        new_spec = self.materialize(direct_threshold=direct_threshold)
        new_base.flags.writeable = False
        new_spec.flags.writeable = False
        self.base_signal = new_base
        self.base_spectrum = new_spec
        self.pending.clear()


@dataclass
class PreparedDenseFFT:
    """Dense spectrum after EVERY event, when position known and recurring."""
    n: int
    position: int
    spectrum: np.ndarray
    phase: np.ndarray

    @classmethod
    def from_signal(cls, signal, position):
        a = np.asarray(signal, dtype=np.float64)
        n = a.size
        if not (0 <= position < n):
            raise ValueError('bad position')
        phase = phases_tiled(n, position)
        return cls(n, position, fft.rfft(a), phase)

    def edit(self, delta):
        # Allocate one temporary, return a dense spectrum after the update.
        self.spectrum += delta*self.phase
        return self.spectrum


def exact_modular_check(n: int = 16, prime: int = 998244353, generator: int = 3):
    """Exact integer check of lazy Fourier identities over a prime field."""
    assert (prime - 1) % n == 0
    w = pow(generator, (prime - 1)//n, prime)
    assert pow(w, n, prime) == 1
    assert all(pow(w, n//f, prime) != 1 for f in [2] if n>1)
    a = [(7*i*i+11*i+3)%prime for i in range(n)]
    updates = [(1 % n, 17), (5 % n, 24), (1 % n, -9), (n-1, 6)]
    def dft(seq):
        return [sum(seq[j]*pow(w,j*q,prime) for j in range(n))%prime for q in range(n)]
    spec0 = dft(a)
    adjusted = a[:]
    for p,d in updates:
        adjusted[p] = (adjusted[p] + d)%prime
    actual = dft(adjusted)
    updated = []
    for q in range(n):
        y = spec0[q]
        for p,d in updates:
            y += d*pow(w,p*q,prime)
        updated.append(y%prime)
    assert actual == updated, (actual, updated)
    return True

class TrackedFrequencies:
    """Maintain a fixed subscribed set of Q rFFT outputs, O(Q) per known edit.

    Input producer gives edit positions; only subscribed frequencies are
    materialized. Initial rFFT provides the starting Q values.
    """
    def __init__(self, signal: Iterable[float], frequency_indices: Iterable[int],
                 positions: Iterable[int] = ()):
        a=np.asarray(signal, dtype=np.float64)
        if a.ndim!=1 or not a.size:
            raise ValueError('bad signal')
        self.n=a.size
        self.qs=np.asarray(list(frequency_indices),dtype=np.int64)
        if (self.qs<0).any() or (self.qs>self.n//2).any():
            raise IndexError('bad frequency')
        self.spec=fft.rfft(a)[self.qs].copy()
        self.phases = {}
        for p in positions:
            self.prepare(p)

    def prepare(self,p):
        p=int(p)
        if p<0 or p>=self.n: raise IndexError('bad position')
        self.phases[p]=np.exp(-2j*np.pi*((self.qs*p)%self.n)/self.n)

    def edit(self,p,delta):
        if p not in self.phases:
            self.prepare(p)
        self.spec += float(delta)*self.phases[p]
        return self.spec
