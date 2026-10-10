"""Adaptive reuse engine for real-valued FFTs (experimental research software).

Uses optimized rFFT as the safe default and selectively exploits exact cache
hits, cyclic shifts, sparse edits, and rank-one/two linear spans. All returned
spectra are fresh arrays. Ordinary FFT complexity is not improved in general.

Requires numpy; scipy is optional. Python >= 3.10.
"""
from __future__ import annotations

from collections import OrderedDict, Counter
from dataclasses import dataclass
import math
from typing import Optional

import numpy as np

try:
    from scipy import fft as _scipy_fft
except ImportError:
    _scipy_fft = None


def _as_real_1d(x):
    original = np.asarray(x)
    if original.ndim != 1 or original.size < 1:
        raise ValueError("expected a nonempty, one-dimensional real array")
    if not np.issubdtype(original.dtype, np.number) or np.iscomplexobj(original):
        raise ValueError("expected real numeric input")
    a = np.ascontiguousarray(original, dtype=np.float64)
    if not np.isfinite(a).all():
        raise ValueError("NaN and infinity are unsupported")
    return a


def _as_real_2d(x):
    original = np.asarray(x)
    if original.ndim != 2 or min(original.shape) < 1:
        raise ValueError("expected a nonempty real matrix (signals x samples)")
    if not np.issubdtype(original.dtype, np.number) or np.iscomplexobj(original):
        raise ValueError("expected real numeric input")
    a = np.ascontiguousarray(original, dtype=np.float64)
    if not np.isfinite(a).all():
        raise ValueError("NaN and infinity are unsupported")
    return a


def _fingerprint(raw: bytes, n: int):
    # Python's process-local SipHash is noticeably faster than cryptographic
    # hashes for this in-memory table. We ALWAYS compare the complete raw
    # bytes before accepting a hit; a hash collision cannot corrupt results.
    return (n, hash(raw))


def _shift_from_bytes(base: np.ndarray, target_raw: bytes) -> Optional[int]:
    """Return shift to the right; C-level bytes search with exact verification.

    Deliberately bit-exact. Since raw bytes may contain accidental matches that
    begin mid-double, only aligned matches count. A matching aligned full
    pattern is by definition the desired circular shift.
    """
    raw = base.tobytes()
    if len(raw) != len(target_raw):
        return None
    haystack = raw + raw[:-8]  # all N distinct rotations at 8-byte boundaries
    start = 0
    while True:
        offset = haystack.find(target_raw, start)
        if offset == -1:
            return None
        if offset % 8 == 0:
            return (len(raw)//8 - offset//8) % (len(raw)//8)
        start = offset + 1


@dataclass
class _Entry:
    input: np.ndarray
    spectrum: np.ndarray  # non-redundant rfft output, complex128
    raw: bytes
    bytes_used: int
    signature: tuple[float, float]


@dataclass
class _Span:
    basis: np.ndarray   # (r, n)
    spectra: np.ndarray # (r, n//2+1)
    pivots: tuple[int, ...]
    tolerance: float
    bytes_used: int

    def coefficients(self, row: np.ndarray) -> Optional[np.ndarray]:
        if len(row) != self.basis.shape[1]:
            return None
        r = self.basis.shape[0]
        if r == 1:
            p = self.pivots[0]
            alpha = row[p] / self.basis[0, p]
            coefficients = np.array([alpha], dtype=float)
        else:
            i, j = self.pivots
            a, b = self.basis
            determinant = a[i]*b[j] - a[j]*b[i]
            if abs(determinant) <= 1e-15 * (abs(a[i]*b[j])+abs(a[j]*b[i])+1e-300):
                return None
            coefficients = np.array([
                (row[i]*b[j] - row[j]*b[i])/determinant,
                (a[i]*row[j] - a[j]*row[i])/determinant,
            ], dtype=float)
        # Validating ALL N coordinates is vital: matching only at pivots would
        # silently produce incorrect spectra for random arrays.
        estimate = coefficients @ self.basis
        if not np.allclose(estimate, row, rtol=self.tolerance, atol=self.tolerance):
            return None
        return coefficients


def _make_span(signals: np.ndarray, tol=2e-12) -> Optional[tuple[_Span, np.ndarray]]:
    """Determine rank<=2 family, verify all coordinates, return exact basis rows.

    O(M*N) work for a constant rank. It is not a general numerical rank estimator.
    Reject poorly conditioned second bases instead of promising stable answers.
    """
    rows, n = signals.shape
    chosen = []
    coefficients = []
    pivot0 = None
    pivot1 = None
    for row in signals:
        if not chosen:
            if not np.any(row):
                coefficients.append([])
                continue
            chosen.append(row.copy())
            pivot0 = int(np.argmax(np.abs(row)))
            coefficients = [[0.0] for _ in coefficients]
            coefficients.append([1.0])
            continue
        if len(chosen) == 1:
            alpha = row[pivot0]/chosen[0][pivot0]
            if np.allclose(alpha*chosen[0], row, rtol=tol, atol=tol):
                coefficients.append([float(alpha)])
                continue
            # Determine the second pivot with a well-scaled determinant.
            dets = chosen[0][pivot0]*row - chosen[0]*row[pivot0]
            pivot1 = int(np.argmax(np.abs(dets)))
            scale = float(np.max(np.abs(chosen[0])) * np.max(np.abs(row)))
            if abs(dets[pivot1]) <= 1e-10 * max(scale, 1e-300):
                return None
            chosen.append(row.copy())
            coefficients = [c+[0.0] for c in coefficients]
            coefficients.append([0.0, 1.0])
            continue
        a, b = chosen
        det = a[pivot0]*b[pivot1] - a[pivot1]*b[pivot0]
        alpha = (row[pivot0]*b[pivot1] - row[pivot1]*b[pivot0]) / det
        beta = (a[pivot0]*row[pivot1] - a[pivot1]*row[pivot0]) / det
        if not np.allclose(alpha*a+beta*b, row, rtol=tol, atol=tol):
            return None
        coefficients.append([float(alpha), float(beta)])
    if not chosen:
        # Degenerate all-zero family: handled cheaply by caller.
        return None
    basis = np.stack(chosen)
    c = np.asarray(coefficients, dtype=float)
    if not np.isfinite(c).all():
        return None
    pivots = (pivot0,) if len(chosen) == 1 else (pivot0, pivot1)
    empty = np.zeros((len(chosen), n//2+1), dtype=np.complex128)
    span = _Span(basis, empty, pivots, tol, 0)
    return span, c


class AdaptiveFFT:
    """Cacheable real FFTs with bounded memory and exact/validated reuse.

    auto: conservative heuristic; exact lookup, structural only at large sizes.
    aggressive: always attempt available reuse, even if it can be slower.
    plain: no structural reuse or caching lookup; optimized backend only.

    n can be any positive integer. This is an online runtime optimization, not a
    mathematical improvement to worst-case FFT complexity.
    """
    def __init__(self, *, max_cache_bytes=64*1024*1024,
                 max_references=3, max_sparse_edits=1, max_spans=3,
                 mode='auto', backend='auto', auto_threshold=262144,
                 rank_batch_threshold=8192, rank_min_batch=12):
        if mode not in ('auto', 'aggressive', 'plain'):
            raise ValueError("mode must be auto, aggressive or plain")
        if backend not in ('auto', 'numpy', 'scipy'):
            raise ValueError("backend must be auto, numpy or scipy")
        if backend == 'scipy' and _scipy_fft is None:
            raise ImportError('scipy backend requested but scipy unavailable')
        self.backend = 'scipy' if (backend in ('scipy', 'auto') and _scipy_fft is not None) else 'numpy'
        self.mode = mode
        self.max_cache_bytes = int(max_cache_bytes)
        self.max_references = int(max_references)
        self.max_sparse_edits = int(max_sparse_edits)
        self.max_spans = int(max_spans)
        self.auto_threshold = int(auto_threshold)
        self.rank_batch_threshold = int(rank_batch_threshold)
        self.rank_min_batch = int(rank_min_batch)
        if min(self.max_cache_bytes, self.max_references, self.max_spans) < 0 or self.max_sparse_edits < 0:
            raise ValueError('memory/limits must be nonnegative')
        self.cache: OrderedDict[tuple, _Entry] = OrderedDict()
        self.spans: OrderedDict[int, _Span] = OrderedDict()
        self.cache_bytes = 0
        self.stats = Counter()
        self.last_strategy = 'none'
        self._freqs: dict[int, np.ndarray] = {}  # small bounded indices cache
        self._samples: dict[int, np.ndarray] = {}
        self._miss_streak = 0

    def _sample_indices(self, n):
        if n not in self._samples:
            if len(self._samples) >= 8:
                self._samples.pop(next(iter(self._samples)))
            self._samples[n] = np.linspace(0, n-1, min(16,n), dtype=np.intp)
        return self._samples[n]

    @staticmethod
    def _signature(a):
        # Rotation-invariant screening; floating-point summation can change
        # slightly on rotation, hence the tolerances in _similar_signature.
        return (float(np.sum(a)), float(np.dot(a, a)))

    @staticmethod
    def _similar_signature(a, b):
        return (math.isclose(a[0], b[0], rel_tol=1e-10, abs_tol=1e-7) and
                math.isclose(a[1], b[1], rel_tol=1e-10, abs_tol=1e-7))

    def _forward(self, x, axis=-1):
        if self.backend == 'scipy':
            return _scipy_fft.rfft(x, axis=axis)
        return np.fft.rfft(x, axis=axis)

    def _inverse(self, x, n, axis=-1):
        if self.backend == 'scipy':
            return _scipy_fft.irfft(x, n=n, axis=axis)
        return np.fft.irfft(x, n=n, axis=axis)

    def _frequencies(self, n):
        if n not in self._freqs:
            if len(self._freqs) >= 8:
                self._freqs.pop(next(iter(self._freqs)))
            self._freqs[n] = np.arange(n//2+1, dtype=float)
        return self._freqs[n]

    @staticmethod
    def _rotation_factors(n, step, count):
        """Compute powers of one root of unity using O(count) C-level multiplies.

        Avoid exp() per frequency. Long products can accumulate rounding error;
        for unusually large n callers seeking high precision should use the
        backend FFT and/or compare accuracy against it.
        """
        omega = np.exp((-2j*math.pi/n)*int(step))
        phase = np.full(count, omega, dtype=np.complex128)
        phase[0] = 1+0j
        np.cumprod(phase, out=phase)
        return phase

    def _expire(self):
        while self.cache_bytes > self.max_cache_bytes:
            if self.cache:
                _, entry = self.cache.popitem(last=False)
                self.cache_bytes -= entry.bytes_used
                self.stats['evictions'] += 1
            elif self.spans:
                _, span = self.spans.popitem(last=False)
                self.cache_bytes -= span.bytes_used
                self.stats['evictions'] += 1
            else:
                break

    def _save(self, a, spectrum, raw=None):
        if self.mode == 'plain' or self.max_cache_bytes <= 0:
            return
        if raw is None:
            raw = a.tobytes()
        key = _fingerprint(raw, len(a))
        old = self.cache.pop(key, None)
        if old is not None:
            self.cache_bytes -= old.bytes_used
        a = a.copy()
        spec = np.asarray(spectrum, dtype=np.complex128).copy()
        a.setflags(write=False)
        spec.setflags(write=False)
        entry = _Entry(a, spec, raw, a.nbytes + spec.nbytes + len(raw),
                       self._signature(a))
        if entry.bytes_used > self.max_cache_bytes:
            self._expire()
            return
        self.cache[key] = entry
        self.cache_bytes += entry.bytes_used
        self._expire()

    def _save_span(self, span):
        if self.mode == 'plain' or self.max_spans == 0 or self.max_cache_bytes <= 0:
            return
        span.bytes_used = span.basis.nbytes + span.spectra.nbytes
        if span.bytes_used > self.max_cache_bytes:
            return
        old = self.spans.pop(span.basis.shape[1], None)
        if old is not None:
            self.cache_bytes -= old.bytes_used
        self.spans[span.basis.shape[1]] = span
        self.cache_bytes += span.bytes_used
        while len(self.spans) > self.max_spans:
            _, old = self.spans.popitem(last=False)
            self.cache_bytes -= old.bytes_used
        self._expire()

    def _matching_entries(self, n):
        if self.max_references == 0:
            return []
        found = []
        for key, entry in reversed(self.cache.items()):
            if len(entry.input) == n:
                found.append((key, entry))
                if len(found) >= self.max_references:
                    break
        return found

    def _try_cached(self, a, raw, *, structural=True):
        n = len(a)
        key = _fingerprint(raw, n)
        entry = self.cache.get(key)
        if entry is not None and entry.raw == raw:
            self.cache.move_to_end(key)
            self.stats['exact_hits'] += 1
            return entry.spectrum.copy(), 'exact'
        if not structural or not self.max_cache_bytes:
            return None
        for k, span in list(reversed(self.spans.items())):
            if k != n:
                continue
            coeff = span.coefficients(a)
            if coeff is not None:
                self.spans.move_to_end(k)
                self.stats['span_hits'] += 1
                return coeff @ span.spectra, 'span'
        query_signature = None
        sample = self._sample_indices(n)
        for key, e in self._matching_entries(n):
            if self.max_sparse_edits:
                # Necessary cheap condition: if already > max_edits differ in
                # 16 sampled cells, there's no need to scan all N cells.
                promising = (np.count_nonzero(a[sample] != e.input[sample])
                             <= self.max_sparse_edits)
                mismatches = np.flatnonzero(a != e.input) if promising else np.empty(0,int)
                if 0 < len(mismatches) <= self.max_sparse_edits:
                    spec = e.spectrum.copy()
                    for pos in mismatches:
                        difference = a[pos] - e.input[pos]
                        # For pos=0, only addition is needed: no complex exp.
                        if pos == 0:
                            spec += difference
                        else:
                            phase = self._rotation_factors(n, int(pos), len(spec))
                            spec += difference * phase
                    self.cache.move_to_end(key)
                    self.stats['sparse_hits'] += 1
                    return spec, 'sparse'
            if query_signature is None:
                query_signature = self._signature(a)
            if not self._similar_signature(query_signature, e.signature):
                continue
            shift = _shift_from_bytes(e.input, raw)
            if shift is not None:
                # Distinguish unchanged from shifts (exact should catch unchanged).
                phase = self._rotation_factors(n, shift, len(e.spectrum))
                spec = e.spectrum * phase
                self.cache.move_to_end(key)
                self.stats['shift_hits'] += 1
                return spec, 'shift'
        return None

    def rfft(self, x, *, reuse=None):
        """Return the nonredundant complex spectrum, always as a new array.

        reuse=None -> engine policy, True -> try reuse, False -> no structural
        reuse (exact cache lookup remains enabled unless mode='plain').
        """
        a = _as_real_1d(x)
        n = len(a)
        if self.mode == 'plain':
            self.last_strategy = 'fft'
            self.stats['fallback'] += 1
            return self._forward(a)
        # In the auto policy, avoid the cost of even hashing the input during
        # a run of unrelated (high-entropy) inputs. Probe periodically so a
        # later repeated input can eventually re-enable the cache.
        if (self.mode == 'auto' and reuse is None and
                self._miss_streak >= 3 and self._miss_streak % 12 != 0):
            self._miss_streak += 1
            self.stats['auto_bypass'] += 1
            self.stats['fallback'] += 1
            self.last_strategy = 'fft_bypass'
            return self._forward(a)
        raw = a.tobytes()
        structural = self.mode == 'aggressive' or n >= self.auto_threshold
        if reuse is not None:
            structural = bool(reuse)
        found = self._try_cached(a, raw, structural=structural)
        if found is None:
            result = self._forward(a)
            strategy = 'fft'
            self.stats['fallback'] += 1
            self._miss_streak += 1
        else:
            result, strategy = found
            self._miss_streak = 0
        self.last_strategy = strategy
        if strategy != 'exact' and (strategy != 'shift' or self.mode != 'auto'):
            self._save(a, result, raw)
        return result

    def fft(self, x, *, reuse=None):
        """Full complex FFT, reconstructing Hermitian-redundant negative bins."""
        a = _as_real_1d(x)
        half = self.rfft(a, reuse=reuse)
        if len(a) % 2:
            tail = np.conj(half[-1:0:-1])
        else:
            tail = np.conj(half[-2:0:-1])
        return np.concatenate((half, tail))

    def fft_batch(self, x, *, reuse=None, return_info=False):
        """Return (M, N//2+1) rFFT spectra for real (M,N) data.

        Detect exact copies and a rank<=2 family; otherwise use batch rfft.
        When a cached span exists, reuse it row-by-row where applicable.
        """
        x = _as_real_2d(x)
        m, n = x.shape
        if self.mode == 'plain':
            answer = self._forward(x, axis=1)
            self.stats['fallback'] += m
            info = {'strategies': {'fft_batch': m}, 'rank': None}
            self.last_strategy = 'fft_batch'
            return (answer, info) if return_info else answer
        # Avoid a full scan for zero detection on ordinary nonzero batches.
        if not np.any(x.ravel()[:min(32,x.size)]) and not np.any(x):
            answer = np.zeros((m, n//2+1), dtype=np.complex128)
            self.stats['zero_batch'] += m
            self.last_strategy = 'zero_batch'
            info = {'strategies': {'zero': m}, 'rank': 0}
            return (answer, info) if return_info else answer
        if self.mode == 'auto' and reuse is None and m >= 8 and not self.spans:
            # SciPy batched rFFT is already exceptionally fast. Avoid Python
            # row-wise hashes and costly rank verification unless inexpensive
            # pilot columns strongly suggest a low-rank family AND the batch
            # is large enough to plausibly amortize the search cost.
            rank_hint = False
            if m >= 128 and n >= self.rank_batch_threshold:
                sample = x[:, np.linspace(0, n-1, 12, dtype=int)]
                rank_hint = np.linalg.matrix_rank(sample, tol=1e-9) <= 2
            if not rank_hint:
                answer = self._forward(x, axis=1)
                self.last_strategy = 'fft_batch'
                self.stats['fallback'] += m
                if self.max_references and m <= 16:
                    for j in range(max(0,m-min(self.max_references,2)),m):
                        self._save(x[j], answer[j])
                info = {'strategies': {'fft_batch': m}, 'rank': None}
                return (answer,info) if return_info else answer
        results = np.empty((m, n//2+1), dtype=np.complex128)
        strategies = Counter()
        missing = []
        # Exact cache is O(N) in compiled hashing code, and handles overlap
        # across calls. Do NOT scan every stored reference for every batch row.
        for index, row in enumerate(x):
            raw = row.tobytes()
            found = self._try_cached(row, raw, structural=False)
            if found is None:
                missing.append(index)
            else:
                results[index] = found[0]
                strategies[found[1]] += 1
        if missing:
            unknown = x[missing]
            aggressive = self.mode == 'aggressive'
            want_rank = (reuse is not False and (aggressive or
                         (n >= self.rank_batch_threshold and len(missing) >= self.rank_min_batch)))
            rank_fitted = None
            if want_rank:
                rank_fitted = _make_span(unknown)
            if rank_fitted is not None:
                span, coeffs = rank_fitted
                span.spectra = self._forward(span.basis, axis=1)
                generated = coeffs @ span.spectra
                results[missing] = generated
                self._save_span(span)
                strategies[f'rank{len(span.basis)}'] += len(missing)
                self.stats['rank_batch'] += len(missing)
                self.last_strategy = 'rank_batch'
            else:
                # When nearly all rows are new, single optimized batch call
                # avoids expensive per-row Python object and twiddle overhead.
                if aggressive or (reuse is True) or (len(missing) <= 4 and n >= self.auto_threshold):
                    need_fft = []
                    for index in missing:
                        raw = x[index].tobytes()
                        found = self._try_cached(x[index], raw, structural=True)
                        if found is None:
                            need_fft.append(index)
                        else:
                            results[index] = found[0]
                            strategies[found[1]] += 1
                    missing = need_fft
                if missing:
                    computed = self._forward(x[missing], axis=1)
                    results[missing] = computed
                    strategies['fft_batch'] += len(missing)
                    self.stats['fallback'] += len(missing)
                    self.last_strategy = 'fft_batch'
        # Cache at most recent candidate spectra within bounded byte budget.
        # In particular don't automatically cache a giant whole batch.
        for index in range(max(0, m - max(1, self.max_references)), m):
            self._save(x[index], results[index])
        info = {'strategies': dict(strategies), 'rank': len(span.basis) if (missing and rank_fitted is not None) else None}
        return (results, info) if return_info else results

    def convolution(self, a, b, *, reuse=None):
        """Linear convolution, using cached real spectra when possible."""
        a = _as_real_1d(a)
        b = _as_real_1d(b)
        target = len(a)+len(b)-1
        if self.backend == 'scipy':
            n = _scipy_fft.next_fast_len(target)
        else:
            n = 1 << (target-1).bit_length()
        pa = np.zeros(n, dtype=np.float64)
        pb = np.zeros(n, dtype=np.float64)
        pa[:len(a)] = a
        pb[:len(b)] = b
        fa = self.rfft(pa, reuse=reuse)
        fb = self.rfft(pb, reuse=reuse)
        return self._inverse(fa*fb, n)[:target]

    def fft_family(self, basis, coefficients, *, register=False):
        """Transform a KNOWN linear family: inputs = coefficients @ basis.

        This is the fastest and most reliable reusable relationship. The
        caller provides r basis rows and an M-by-r coefficient matrix. FFT
        only the r bases, then form M transforms in O(M*r*N) arithmetic.
        Unlike automatic rank detection there is no expensive full-input
        validation because the inputs are constructed from these ingredients.
        """
        basis = _as_real_2d(basis)
        co = np.asarray(coefficients, dtype=np.float64)
        if co.ndim != 2 or co.shape[1] != len(basis) or not len(co) or not np.isfinite(co).all():
            raise ValueError('coefficients must be a finite M-by-r matrix')
        spectra = self._forward(basis,axis=1)
        results = np.einsum('mr,rk->mk', co, spectra, optimize=True)
        self.stats['known_family'] += len(co)
        self.last_strategy = 'known_family'
        if register and len(basis) <= 2:
            identified = _make_span(basis)
            if identified is not None:
                span,_ = identified
                span.spectra = spectra.copy()
                self._save_span(span)
        return results

    def register_basis(self, basis):
        """Register one or two independent basis arrays for future queries."""
        basis = _as_real_2d(basis)
        if not 1 <= len(basis) <= 2:
            raise ValueError('register_basis needs one or two basis signals')
        identified = _make_span(basis)
        if identified is None:
            raise ValueError('zero/ill-conditioned basis is not supported')
        span, _ = identified
        if len(span.basis) != len(basis):
            raise ValueError('basis signals are linearly dependent')
        span.spectra = self._forward(span.basis,axis=1)
        self._save_span(span)
        return len(span.basis)

    def clear(self):
        self.cache.clear()
        self.spans.clear()
        self.cache_bytes = 0
        self._freqs.clear()
        self._samples.clear()
        self._miss_streak = 0
        self.last_strategy = 'cleared'

    def summary(self):
        return {'backend': self.backend, 'mode': self.mode,
                'entries': len(self.cache), 'models': len(self.spans),
                'cache_bytes': self.cache_bytes,
                'stats': dict(self.stats), 'last_strategy': self.last_strategy}


def two_real_ffts_packed(a, b):
    """Two length-N real FFTs from one length-N complex FFT (educational)."""
    a, b = _as_real_1d(a), _as_real_1d(b)
    if len(a) != len(b):
        raise ValueError('same length required')
    z = np.fft.fft(a+1j*b)
    partner = np.conj(z[(-np.arange(len(a))) % len(a)])
    return (z+partner)/2, (z-partner)/(2j)


class CanonicalFFTGraph:
    """Optional radix-2 DAG for operation counts, NOT the fast NumPy path."""
    def __init__(self):
        self.keys = {}
        self.nodes = []
        self.results = {}
        self.butterflies = 0
        self.build_calls = 0
        self.twiddles = {}

    def add(self, a):
        a = _as_real_1d(a)
        if len(a) & (len(a)-1):
            raise ValueError('DAG length must be a power of two')
        return self._add(a, 0, 1, len(a))

    def _add(self, a, off, stride, n):
        self.build_calls += 1
        if n == 1:
            key = ('leaf', float(a[off]))
            children = None
        else:
            l = self._add(a, off, stride*2, n//2)
            r = self._add(a, off+stride, stride*2, n//2)
            key = ('node', n, l, r)
            children = (l, r)
        node_id = self.keys.get(key)
        if node_id is None:
            node_id = len(self.nodes)
            self.keys[key] = node_id
            self.nodes.append((n, children, float(a[off]) if n==1 else None))
        return node_id

    def evaluate(self, node_id):
        if node_id in self.results:
            return self.results[node_id].copy()
        n, children, scalar = self.nodes[node_id]
        if n == 1:
            answer = np.array([complex(scalar)])
        else:
            l, r = children
            e = self.evaluate(l)
            o = self.evaluate(r)
            if n not in self.twiddles:
                self.twiddles[n] = np.exp(-2j*np.pi*np.arange(n//2)/n)
            t = self.twiddles[n]*o
            answer = np.concatenate((e+t, e-t))
            self.butterflies += n//2
        self.results[node_id] = answer
        return answer.copy()

    def summary(self):
        return {'unique_nodes': len(self.nodes),
                'butterflies': self.butterflies,
                'cached_spectral_values': sum(len(v) for v in self.results.values()),
                'build_calls': self.build_calls}
