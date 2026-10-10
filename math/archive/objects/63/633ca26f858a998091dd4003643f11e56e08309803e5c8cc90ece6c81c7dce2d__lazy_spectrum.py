"""Lazy relation-aware Fourier state.

This module deliberately separates *metadata ingestion* from spectrum
materialization.  A state represents

    S = sum_i alpha_i * B_i + DFT(delta),

where B_i are already-computed dense spectra and ``delta`` is a sparse
set of known time-domain point edits supplied by the producer.

Point edits are O(1) expected-time dictionary updates.  A query for q
frequency bins costs O(q*(r+k)) arithmetic for r dense basis terms and k
pending edit locations, without touching all N spectrum entries.  Dense
materialization is explicit and can choose direct rank-one updates or the
factorized sparse transform in ``hybrid_sparse``.

This is an engineering/data-structure result, not a new worst-case FFT
upper bound.  The algebra is exact in exact arithmetic; NumPy/SciPy paths
are floating-point implementations.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence
import math
import numpy as np

from hybrid_sparse import normalize_changes, sparse_dft, SparsePlan

try:
    from scipy.fft import fft as _native_fft
except ImportError:
    from numpy.fft import fft as _native_fft


@dataclass(frozen=True)
class MaterializationPlan:
    n: int
    dense_terms: int
    pending_edits: int
    method: str
    sparse_plan: SparsePlan | None
    estimated_direct_phase_values: int
    estimated_factorized_values: int


def _as_spectrum(x: Sequence[complex], n: int | None = None) -> np.ndarray:
    a = np.asarray(x, dtype=np.complex128)
    if a.ndim != 1 or a.size < 1:
        raise ValueError("spectrum must be a nonempty 1-D array")
    if n is not None and a.size != n:
        raise ValueError("spectrum length mismatch")
    if not np.isfinite(a.real).all() or not np.isfinite(a.imag).all():
        raise ValueError("spectrum must be finite")
    return a


def _normalize_bins(n: int, bins: Sequence[int]) -> np.ndarray:
    idx = np.asarray(bins)
    if idx.ndim != 1:
        raise ValueError("bins must be one-dimensional")
    if not np.issubdtype(idx.dtype, np.integer):
        # Permit Python integer lists that NumPy may infer unusually, but no floats.
        if any(not isinstance(v, (int, np.integer)) for v in bins):
            raise ValueError("bins must contain integers")
        idx = idx.astype(np.int64)
    idx = idx.astype(np.int64, copy=False)
    if np.any(idx < 0) or np.any(idx >= n):
        raise ValueError("frequency bin outside spectrum")
    return idx


def direct_sparse_correction(n: int, edits: dict[int, complex], *, chunk_bins: int = 65536) -> np.ndarray:
    """Materialize DFT(delta) by direct phase accumulation.

    Work is O(N*k), but memory is bounded by O(chunk_bins*k) rather than
    allocating a full N-by-k matrix.  This is often faster than the
    factorized Python prototype for very small k.
    """
    if n < 1:
        raise ValueError("n must be positive")
    if not edits:
        return np.zeros(n, dtype=np.complex128)
    pos = np.fromiter(edits.keys(), dtype=np.float64, count=len(edits))
    val = np.fromiter(edits.values(), dtype=np.complex128, count=len(edits))
    out = np.empty(n, dtype=np.complex128)
    scale = -2j * np.pi / n
    chunk_bins = max(1, int(chunk_bins))
    for start in range(0, n, chunk_bins):
        stop = min(n, start + chunk_bins)
        freq = np.arange(start, stop, dtype=np.float64)
        phases = np.exp(scale * np.multiply.outer(freq, pos))
        out[start:stop] = phases @ val
    return out


class LazySpectrum:
    """Deferred Fourier state with producer-supplied relation metadata.

    The object owns no time-domain base vector.  Dense terms are spectra
    that were already computed elsewhere.  Pending edits are exact metadata
    describing additions in the time domain.

    ``add_edit`` / ``add_edits`` do not scan N values and do not materialize
    any spectrum.  ``bins`` is the preferred operation when a downstream
    consumer needs only a subset of frequencies.
    """

    def __init__(self, n: int, *, dense_terms: Iterable[tuple[complex, Sequence[complex]]] = (), edits: Iterable[tuple[int, complex]] = ()):
        n = int(n)
        if n < 1:
            raise ValueError("n must be positive")
        self.n = n
        self._terms: list[tuple[complex, np.ndarray]] = []
        for coefficient, spectrum in dense_terms:
            self.add_dense_term(coefficient, spectrum)
        self._edits: dict[int, complex] = {}
        self.add_edits(edits)

    @classmethod
    def from_spectrum(cls, spectrum: Sequence[complex]) -> "LazySpectrum":
        s = _as_spectrum(spectrum)
        return cls(s.size, dense_terms=[(1.0 + 0j, s)])

    @classmethod
    def from_basis(cls, basis_spectra: np.ndarray, coefficients: Sequence[complex], *, edits: Iterable[tuple[int, complex]] = ()) -> "LazySpectrum":
        basis = np.asarray(basis_spectra, dtype=np.complex128)
        coeff = np.asarray(coefficients, dtype=np.complex128)
        if basis.ndim != 2 or coeff.ndim != 1 or basis.shape[0] != coeff.size or basis.shape[1] < 1:
            raise ValueError("basis_spectra must have shape (r,n), coefficients shape (r,)")
        terms = [(complex(coeff[i]), basis[i]) for i in range(coeff.size) if coeff[i] != 0]
        return cls(basis.shape[1], dense_terms=terms, edits=edits)

    @property
    def pending_count(self) -> int:
        return len(self._edits)

    @property
    def dense_term_count(self) -> int:
        return len(self._terms)

    @property
    def pending_edits(self) -> dict[int, complex]:
        return dict(self._edits)

    def add_dense_term(self, coefficient: complex, spectrum: Sequence[complex]) -> None:
        c = complex(coefficient)
        if not (math.isfinite(c.real) and math.isfinite(c.imag)):
            raise ValueError("coefficient must be finite")
        if c == 0:
            return
        s = _as_spectrum(spectrum, self.n)
        # Keep a reference intentionally: cached spectra can be shared across
        # many lazy expressions.  Callers should treat them as immutable.
        self._terms.append((c, s))

    def add_edit(self, index: int, delta: complex) -> None:
        if not isinstance(index, (int, np.integer)) or not 0 <= int(index) < self.n:
            raise ValueError("edit index outside signal")
        z = complex(delta)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise ValueError("edit must be finite")
        j = int(index)
        if z == 0:
            return
        new = self._edits.get(j, 0j) + z
        if new == 0:
            self._edits.pop(j, None)
        else:
            self._edits[j] = new

    def add_edits(self, edits: Iterable[tuple[int, complex]]) -> None:
        for j, v in edits:
            self.add_edit(j, v)

    def bins(self, bins: Sequence[int]) -> np.ndarray:
        """Evaluate only selected Fourier bins, preserving order/duplicates.

        If q bins are requested, this performs O(q*r) dense-term reads and
        O(q*k) phase arithmetic.  It does not touch the other N-q bins.
        """
        idx = _normalize_bins(self.n, bins)
        out = np.zeros(idx.size, dtype=np.complex128)
        for c, s in self._terms:
            out += c * s[idx]
        if self._edits and idx.size:
            pos = np.fromiter(self._edits.keys(), dtype=np.float64, count=len(self._edits))
            val = np.fromiter(self._edits.values(), dtype=np.complex128, count=len(self._edits))
            phase = np.exp((-2j * np.pi / self.n) * np.multiply.outer(idx.astype(np.float64), pos))
            out += phase @ val
        return out

    def _dense_terms_materialized(self) -> np.ndarray:
        out = np.zeros(self.n, dtype=np.complex128)
        for c, s in self._terms:
            out += c * s
        return out

    def choose_dense_method(self, *, direct_k_threshold: int = 8) -> str:
        """Simple deterministic planner for the current Python backends.

        Factorized sparse_dft is asymptotically better than O(N*k), but its
        Python/SciPy setup cost is substantial.  Keep direct phase updates for
        tiny k; use the grouped factorization otherwise when N is a power of 2.
        """
        k = self.pending_count
        if k == 0:
            return "none"
        if k <= int(direct_k_threshold):
            return "direct"
        if self.n & (self.n - 1):
            return "direct"
        return "factorized"

    def materialize(self, *, method: str = "auto", direct_k_threshold: int = 8, commit: bool = False, backend: str = "scipy") -> tuple[np.ndarray, MaterializationPlan]:
        """Return a dense spectrum and an explicit accounting plan.

        ``commit=True`` compacts the expression into one dense cached term and
        clears pending edits.  This is useful at natural synchronization points.
        """
        if method == "auto":
            method = self.choose_dense_method(direct_k_threshold=direct_k_threshold)
        if method not in ("none", "direct", "factorized", "native"):
            raise ValueError("method must be auto, none, direct, factorized or native")
        k = self.pending_count
        if method == "none" and k:
            raise ValueError("pending edits require a correction method")

        out = self._dense_terms_materialized()
        sparse_plan = None
        if k:
            if method == "direct":
                correction = direct_sparse_correction(self.n, self._edits)
            elif method == "factorized":
                correction, sparse_plan = sparse_dft(self.n, self._edits.items(), backend=backend, return_plan=True)
            elif method == "native":
                delta = np.zeros(self.n, dtype=np.complex128)
                for j, v in self._edits.items():
                    delta[j] = v
                correction = _native_fft(delta)
            else:
                raise AssertionError("unreachable")
            out += correction

        # A rough operation-volume proxy, not a runtime prediction.
        b = 1 << (max(1, k)-1).bit_length() if k else 1
        est_factorized = self.n + (self.n // b) * b * max(1, int(math.log2(b))) if k else 0
        plan = MaterializationPlan(
            n=self.n,
            dense_terms=len(self._terms),
            pending_edits=k,
            method=method,
            sparse_plan=sparse_plan,
            estimated_direct_phase_values=self.n * k,
            estimated_factorized_values=est_factorized,
        )

        if commit:
            self._terms = [(1.0 + 0j, out)]
            self._edits.clear()
        return out, plan

    def compact(self, **kwargs) -> MaterializationPlan:
        """Materialize once, store the result as the sole base spectrum."""
        _, plan = self.materialize(commit=True, **kwargs)
        return plan

    def shared_dense_bytes(self) -> int:
        """Bytes referenced by dense terms (may be shared with other states)."""
        return sum(s.nbytes for _, s in self._terms)

    def private_metadata_bytes_lower_bound(self) -> int:
        """Conservative payload-only lower bound, excluding Python dict overhead."""
        # int64 index + complex128 delta + complex128 coefficient per dense term
        return self.pending_count * (8 + 16) + self.dense_term_count * 16

class PreparedBinView:
    """Prepared partial-spectrum view for a known editable support.

    This is the partial-output analogue of precomputing full N-length phase
    vectors.  For q requested bins and k allowed edit positions it stores only
    q*k phases, so memory is O(qk), independent of N.
    """
    def __init__(self, base_spectrum: Sequence[complex], positions: Sequence[int], bins: Sequence[int]):
        base = _as_spectrum(base_spectrum)
        self.n = int(base.size)
        self.bins_index = _normalize_bins(self.n, bins)
        pos_list = [int(p) for p in positions]
        if len(set(pos_list)) != len(pos_list):
            raise ValueError("positions must be unique")
        if any(p < 0 or p >= self.n for p in pos_list):
            raise ValueError("edit position outside signal")
        self.positions = np.asarray(pos_list, dtype=np.int64)
        self._slot = {p:i for i,p in enumerate(pos_list)}
        self._delta = np.zeros(len(pos_list), dtype=np.complex128)
        self._base = np.asarray(base[self.bins_index], dtype=np.complex128).copy()
        if self.bins_index.size and self.positions.size:
            self._phase = np.exp(
                (-2j*np.pi/self.n) *
                np.multiply.outer(self.bins_index.astype(np.float64), self.positions.astype(np.float64))
            )
        else:
            self._phase = np.zeros((self.bins_index.size,self.positions.size), dtype=np.complex128)

    def add_edit(self, index: int, delta: complex) -> None:
        try:
            slot = self._slot[int(index)]
        except (KeyError, ValueError):
            raise ValueError("edit index is not in prepared support") from None
        z=complex(delta)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise ValueError("edit must be finite")
        self._delta[slot] += z

    def values(self) -> np.ndarray:
        if self.positions.size:
            return self._base + self._phase @ self._delta
        return self._base.copy()

    @property
    def phase_bytes(self) -> int:
        return int(self._phase.nbytes)

    @property
    def full_phase_cache_equivalent_bytes(self) -> int:
        """Bytes for k separate full complex N-bin phase vectors."""
        return int(self.positions.size * self.n * np.dtype(np.complex128).itemsize)

class BufferedSpectrum(LazySpectrum):
    """LazySpectrum with threshold compaction for mixed update/query streams.

    Distinct pending edit locations are kept sparse until ``flush_threshold``.
    At that point they are folded into the dense cached spectrum.  This is a
    square-root-decomposition style engineering tradeoff: larger thresholds
    make updates cheaper but selected-bin queries more expensive.
    """
    def __init__(self, n: int, *, flush_threshold: int, flush_method: str = "native", dense_terms=(), edits=()):
        if int(flush_threshold) < 1:
            raise ValueError("flush_threshold must be positive")
        self.flush_threshold = int(flush_threshold)
        self.flush_method = flush_method
        self.flush_count = 0
        super().__init__(n, dense_terms=dense_terms, edits=edits)
        if self.pending_count >= self.flush_threshold:
            self._threshold_flush()

    @classmethod
    def from_spectrum(cls, spectrum: Sequence[complex], *, flush_threshold: int, flush_method: str = "native") -> "BufferedSpectrum":
        s=_as_spectrum(spectrum)
        return cls(s.size,flush_threshold=flush_threshold,flush_method=flush_method,dense_terms=[(1+0j,s)])

    def _threshold_flush(self) -> None:
        self.compact(method=self.flush_method)
        self.flush_count += 1

    def add_edit(self,index:int,delta:complex) -> None:
        super().add_edit(index,delta)
        if self.pending_count >= self.flush_threshold:
            self._threshold_flush()

    def add_edits(self,edits:Iterable[tuple[int,complex]]) -> None:
        for j,v in edits:
            self.add_edit(j,v)


def threshold_cost_proxy(n: int, q: int, updates_per_query: float, threshold: int, *, backend: str = "native", exact_dft_alpha: float = 1.0) -> float:
    """Dimensionless steady-state work proxy per update.

    Assumes mostly distinct pending positions.  A flush every B updates costs C,
    and a q-bin query every H updates sees about B/2 pending edits on average:

        cost/update ~ C/B + q*B/(2H).

    ``native`` uses C=N log2 N. ``hybrid`` uses
    C=N*(1+log2(B+1)^alpha), matching the parameterized sparse-correction
    shape up to constants.  This is a planner heuristic, not a wall-clock model.
    """
    n=int(n);q=int(q);B=int(threshold);H=float(updates_per_query)
    if n<1 or q<1 or B<1 or H<=0: raise ValueError("positive parameters required")
    if backend=='native':
        C=n*max(1.0,math.log2(n))
    elif backend=='hybrid':
        C=n*(1.0+max(1.0,math.log2(B+1))**float(exact_dft_alpha))
    else: raise ValueError("backend must be native or hybrid")
    return C/B + q*B/(2.0*H)


def suggest_flush_threshold(n: int, q: int, updates_per_query: float, *, backend: str = "native", exact_dft_alpha: float = 1.0, max_threshold: int | None = None) -> int:
    """Choose a power-of-two threshold minimizing ``threshold_cost_proxy``."""
    n=int(n)
    if max_threshold is None: max_threshold=n
    top=max(1,min(n,int(max_threshold)))
    candidates=[]
    b=1
    while b<top:
        candidates.append(b);b*=2
    candidates.append(top)
    return min(candidates,key=lambda B:threshold_cost_proxy(n,q,updates_per_query,B,backend=backend,exact_dft_alpha=exact_dft_alpha))

@dataclass(frozen=True)
class RuntimeThresholdCalibration:
    n: int
    q: int
    updates_per_query: float
    probe_k: int
    flush_ms: float
    empty_query_ms: float
    probe_query_ms: float
    phase_pair_ms: float
    raw_threshold: float
    threshold: int


def calibrate_runtime_threshold(base_spectrum: Sequence[complex], q: int, updates_per_query: float, *, probe_k: int = 64, reps: int = 5, max_threshold: int | None = None) -> RuntimeThresholdCalibration:
    """Empirically calibrate the buffer threshold for the current machine.

    The steady-state model is

        time/update ~= F/B + P*q*B/(2H),

    where F is one dense native compaction, P is time per pending-edit/bin
    phase contribution, and H is updates per selected-bin query.  Its optimum is

        B* = sqrt(2 F H / (P q)).

    This calibration is intentionally local/hardware-specific; it turns the
    asymptotic tradeoff into a practical planner rather than pretending Python
    operation counts predict FFT library wall time.
    """
    import time
    base=_as_spectrum(base_spectrum)
    n=base.size;q=int(q);H=float(updates_per_query);probe_k=int(probe_k);reps=int(reps)
    if q<1 or q>n or H<=0 or probe_k<1 or reps<1: raise ValueError("invalid calibration parameters")
    probe_k=min(probe_k,n)
    if max_threshold is None:max_threshold=n
    # Deterministic, spread-out bins/support to reduce accidental cache/path quirks.
    bins=np.unique(np.linspace(0,n-1,q,dtype=np.int64))
    # unique may shrink only when q>n, rejected above; still use actual size below.
    qeff=bins.size
    positions=np.unique(np.linspace(0,n-1,probe_k,dtype=np.int64))
    probe_k=positions.size
    edits=[(int(j),complex(0.5 + (i % 7)*0.03125, -0.125 + (i % 5)*0.015625)) for i,j in enumerate(positions)]

    empty=LazySpectrum.from_spectrum(base)
    probe=LazySpectrum.from_spectrum(base);probe.add_edits(edits)

    def median_ms(fn):
        vals=[]
        for _ in range(reps):
            t0=time.perf_counter_ns();fn();vals.append((time.perf_counter_ns()-t0)/1e6)
        return float(np.median(vals))

    empty_q=median_ms(lambda:empty.bins(bins))
    probe_q=median_ms(lambda:probe.bins(bins))
    # Fresh probe each time because commit mutates state.
    def do_flush():
        s=LazySpectrum.from_spectrum(base);s.add_edits(edits);s.materialize(method='native')
    flush=median_ms(do_flush)
    phase_total=max(probe_q-empty_q,1e-9)
    P=phase_total/(qeff*probe_k)
    raw=math.sqrt((2.0*flush*H)/(P*qeff))
    raw=max(1.0,min(float(max_threshold),raw))
    # Round to nearest power of two, while respecting the cap.
    lo=2**int(math.floor(math.log2(raw))) if raw>=1 else 1
    hi=min(int(max_threshold),lo*2)
    threshold=lo if abs(raw-lo)<=abs(hi-raw) else hi
    threshold=max(1,min(int(max_threshold),int(threshold)))
    return RuntimeThresholdCalibration(n,qeff,H,probe_k,flush,empty_q,probe_q,P,raw,threshold)
