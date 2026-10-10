"""Sparse Fourier decomposition to combine adaptive FFT reuse with a fast DFT oracle.

Algebraically exact (for exact arithmetic), power-of-two length N:
  N = b * m,  k = number of nonzero edits, b = power-of-two >= k.
  T_r[q] = sum_t delta[r+b*t] * omega_m**(t*q).
  C[q,r] = T_r[q] * omega_N**(r*q).
  output[q + m*l] = DFT_b(C[q,:])[l].

Total charged work: O(N + (N/b)*k + (N/b)*DFT_COST(b)).
With b>=k: O(N + (N/b)*DFT_COST(b)).

With a hypothetical/uniform exact DFT backend that implements OpenAI #130's
claimed O(b * (log b)^(1-delta)) bound in its specific arithmetic model,
this is O(N [1 + (log(k+2))^(1-delta)]). This module does NOT implement
OpenAI #130. It uses floating-point FFT backends to check the decomposition.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence
import math
import numpy as np

try:
    from scipy import fft as sp_fft
except ImportError:
    sp_fft = None


@dataclass(frozen=True)
class SparsePlan:
    n: int
    k: int
    b: int
    m: int
    rows_transformed: int
    classical_full_butterflies: int
    classical_inner_butterflies: int
    sparse_phase_terms: int


def _validate_n(n: int) -> int:
    n = int(n)
    if n < 1 or n & (n-1):
        raise ValueError('n must be a positive power of two')
    return n


def normalize_changes(n: int, changes: Iterable[tuple[int, complex]]) -> dict[int, complex]:
    """Aggregate duplicate edits; discard exact-zero coefficients."""
    n = _validate_n(n)
    merged: dict[int, complex] = {}
    for j, value in changes:
        if not isinstance(j, (int, np.integer)) or not 0 <= j < n:
            raise ValueError(f'index {j!r} outside [0,{n})')
        v = complex(value)
        if not (math.isfinite(v.real) and math.isfinite(v.imag)):
            raise ValueError('edits must be finite')
        merged[int(j)] = merged.get(int(j), 0j) + v
    return {j:v for j,v in merged.items() if v != 0j}


def sparse_plan(n: int, changes: Iterable[tuple[int, complex]]) -> SparsePlan:
    n = _validate_n(n)
    d = normalize_changes(n, changes)
    k = len(d)
    b = 1 << (max(1, k)-1).bit_length()
    m = n // b
    logn = n.bit_length()-1
    logb = b.bit_length()-1
    return SparsePlan(n, k, b, m, m, n*logn//2, n*logb//2, m*k)


def sparse_dft(
    n: int,
    changes: Iterable[tuple[int, complex]],
    *,
    backend: str = 'scipy',
    small_transform_1d: Callable[[np.ndarray], Sequence[complex]] | None = None,
    return_plan: bool = False,
):
    """Calculate all N bins from k explicit nonzero input coefficients.

    A future exact scalar DFT routine for length b can be supplied through
    small_transform_1d. The existing SciPy and NumPy backends are numerical,
    NOT the proposed #130 exact DFT algorithm.

    The nonzero-edit data, including locations, are part of the input. The
    2-D intermediate array and all N output coefficients are materialized.
    """
    n = _validate_n(n)
    edit = normalize_changes(n, changes)
    plan = sparse_plan(n, edit.items())
    k, b, m = plan.k, plan.b, plan.m
    if not k:
        ans = np.zeros(n, dtype=np.complex128)
        return (ans, plan) if return_plan else ans

    # One column per residue modulo b; only k nonzero coefficients feed it.
    # O(m*k) arithmetic for all nonzero terms, at most O(N) because b >= k.
    q = np.arange(m, dtype=np.float64)
    intermediate = np.zeros((m,b), dtype=np.complex128)
    active_residues = set()
    for j, value in edit.items():
        r, t = j % b, j // b
        intermediate[:,r] += value * np.exp((-2j*np.pi * t / m) * q)
        active_residues.add(r)

    # The global Nth-root twiddle. O(m*number_of_active_residues) <= O(N).
    for r in active_residues:
        intermediate[:,r] *= np.exp((-2j*np.pi * r / n) * q)

    # m independent DFT_b operations. Replaceable by OpenAI #130 oracle if
    # one becomes available; the shipped backend runs ordinary native FFTs.
    if small_transform_1d is not None:
        freq = np.empty((m,b),dtype=np.complex128)
        for j in range(m):
            row = np.asarray(small_transform_1d(intermediate[j,:]))
            if row.shape != (b,):
                raise ValueError('small transform returned incorrect shape')
            freq[j] = row
    elif backend == 'scipy' and sp_fft is not None:
        freq = sp_fft.fft(intermediate, axis=1)
    elif backend in ('scipy','numpy'):
        freq = np.fft.fft(intermediate, axis=1)
    else:
        raise ValueError('backend must be scipy or numpy')

    # Our row/column formula generates y[q+m*l].
    ans = np.asarray(freq.T.reshape(n), dtype=np.complex128)
    return (ans, plan) if return_plan else ans


def update_spectrum(
    cached_spectrum: Sequence[complex],
    changes: Iterable[tuple[int, complex]],
    **kwargs,
):
    """Reuse F(x), computing F(x+delta) with sparse delta coordinates."""
    cached = np.asarray(cached_spectrum, dtype=np.complex128)
    if cached.ndim != 1:
        raise ValueError('cached spectrum must be 1-D')
    edit = list(changes)
    delta, plan = sparse_dft(cached.size, edit, return_plan=True, **kwargs)
    ans = cached + delta
    return ans, plan


def low_rank_plus_sparse(
    basis_spectra: np.ndarray,
    coefficients: Sequence[complex],
    changes: Iterable[tuple[int, complex]],
    **kwargs,
):
    """Known B*c + k-sparse residual, with stored basis spectra F(B).

    Output is dense. Relation discovery and basis preprocessing are external.
    """
    basis = np.asarray(basis_spectra, dtype=np.complex128)
    c = np.asarray(coefficients, dtype=np.complex128)
    if basis.ndim != 2 or c.ndim != 1 or basis.shape[0] != c.shape[0]:
        raise ValueError('basis spectra must have shape (r,n) and coefficients (r,)')
    if not _validate_n(basis.shape[1]):
        raise ValueError('bad length')
    result = np.einsum('r,rn->n', c, basis)
    residual, plan = sparse_dft(basis.shape[1], changes, return_plan=True, **kwargs)
    return result + residual, plan
