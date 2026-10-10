"""Consumer-aware dynamic Fourier views.

This module treats a signal as a *known relation* rather than a fresh dense
array.  The current signal is represented by

    x = sum_i c[i] * b_i + e,

where the full spectra F(b_i) are already cached and ``e`` is maintained as
an explicit sparse residual in the time domain.

Updates are metadata operations:

* ``add_coefficient(i, delta)`` changes one basis coefficient in O(1).
* ``add_point(index, delta)`` changes one time-domain sample in expected O(1).

A ``PreparedFourierView`` represents a consumer that needs only selected
frequency bins Q.  State updates append O(1)-size events; the view pays for
those updates only when queried.  If t events accumulated since the previous
query and u distinct relation coordinates survive coalescing, replay costs
O(t + |Q| u).  A rebuild from the current relation costs
O(|Q| (r + k)), where r is basis rank and k is current sparse support.
The automatic planner chooses a conservative replay/rebuild strategy before
reading a long event backlog.

This is a dynamic/structured-query data structure, not a new arbitrary-input
FFT complexity result.  Precomputing the basis spectra is external and must be
charged in an end-to-end application.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import weakref
from typing import Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class ViewStats:
    strategy: str
    q: int
    backlog_events: int
    coalesced_coefficients: int
    coalesced_points: int
    basis_rank: int
    sparse_support: int
    phase_cache_entries: int


class CachedFourierBasis:
    """Validate/register a basis spectrum matrix once and reuse it across states.

    Repeated O(rN) validation scans would defeat the purpose of a metadata-driven
    runtime.  A producer can construct this object once when a basis enters the
    cache, then create many cheap DynamicFourierState instances from it.
    """
    def __init__(self, basis_spectra: np.ndarray, *, validate: bool = True):
        basis = np.asarray(basis_spectra, dtype=np.complex128)
        if basis.ndim != 2 or basis.shape[1] < 1:
            raise ValueError("basis_spectra must have shape (r,n), n>=1")
        basis = np.ascontiguousarray(basis)
        if validate and (not np.isfinite(basis.real).all() or not np.isfinite(basis.imag).all()):
            raise ValueError("basis spectra must be finite")
        self.spectra = basis
        self.r, self.n = basis.shape


class DynamicFourierState:
    """Relation-aware signal state with O(1) metadata ingestion.

    ``basis_spectra`` has shape ``(r, n)`` and stores full complex DFTs of
    supplied basis vectors.  The state does *not* attempt to discover this
    representation from a dense signal.
    """

    def __init__(
        self,
        basis_spectra: np.ndarray,
        coefficients: Sequence[complex] | None = None,
        sparse_residual: Iterable[tuple[int, complex]] = (),
    ):
        if isinstance(basis_spectra, CachedFourierBasis):
            registered = basis_spectra
        else:
            registered = CachedFourierBasis(basis_spectra)
        self.basis = registered
        self.basis_spectra = registered.spectra
        self.r, self.n = registered.r, registered.n

        if coefficients is None:
            coeff = np.zeros(self.r, dtype=np.complex128)
        else:
            coeff = np.asarray(coefficients, dtype=np.complex128)
            if coeff.shape != (self.r,):
                raise ValueError("coefficients must have shape (r,)")
            if not np.isfinite(coeff.real).all() or not np.isfinite(coeff.imag).all():
                raise ValueError("coefficients must be finite")
            coeff = coeff.copy()
        self.coefficients = coeff

        self.sparse: dict[int, complex] = {}
        for index, delta in sparse_residual:
            self._validate_point(index, delta)
            j = int(index)
            value = self.sparse.get(j, 0j) + complex(delta)
            if value == 0j:
                self.sparse.pop(j, None)
            else:
                self.sparse[j] = value

        # Event versions are global and monotone.  _log_start_version is the
        # state version immediately before _events[0].
        self.version = 0
        self._log_start_version = 0
        self._events: list[tuple[int, str, int, complex]] = []
        self._views: weakref.WeakSet[PreparedFourierView] = weakref.WeakSet()

    def _validate_point(self, index, delta) -> None:
        if not isinstance(index, (int, np.integer)) or not 0 <= int(index) < self.n:
            raise ValueError(f"index {index!r} outside [0,{self.n})")
        z = complex(delta)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise ValueError("delta must be finite")

    def _append_event(self, kind: str, key: int, delta: complex) -> None:
        z = complex(delta)
        if z == 0j:
            return
        self.version += 1
        self._events.append((self.version, kind, int(key), z))

    def add_coefficient(self, index: int, delta: complex) -> None:
        """Add delta to one basis coefficient; O(1) state work."""
        if not isinstance(index, (int, np.integer)) or not 0 <= int(index) < self.r:
            raise ValueError(f"basis index {index!r} outside [0,{self.r})")
        z = complex(delta)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise ValueError("delta must be finite")
        if z == 0j:
            return
        i = int(index)
        self.coefficients[i] += z
        self._append_event("coeff", i, z)

    def add_coefficient_trusted(self, index: int, delta: complex) -> None:
        """Unchecked O(1) fast path for producer-certified metadata."""
        z = complex(delta)
        if z == 0j:
            return
        i = int(index)
        self.coefficients[i] += z
        self._append_event("coeff", i, z)

    def set_coefficient(self, index: int, value: complex) -> None:
        if not isinstance(index, (int, np.integer)) or not 0 <= int(index) < self.r:
            raise ValueError(f"basis index {index!r} outside [0,{self.r})")
        z = complex(value)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise ValueError("coefficient must be finite")
        i = int(index)
        self.add_coefficient(i, z - self.coefficients[i])

    def add_point(self, index: int, delta: complex) -> None:
        """Add a sparse time-domain edit; expected O(1) state work."""
        self._validate_point(index, delta)
        z = complex(delta)
        if z == 0j:
            return
        j = int(index)
        value = self.sparse.get(j, 0j) + z
        if value == 0j:
            self.sparse.pop(j, None)
        else:
            self.sparse[j] = value
        self._append_event("point", j, z)

    def add_point_trusted(self, index: int, delta: complex) -> None:
        """Unchecked O(1) fast path for producer-certified metadata."""
        z = complex(delta)
        if z == 0j:
            return
        j = int(index)
        value = self.sparse.get(j, 0j) + z
        if value == 0j:
            self.sparse.pop(j, None)
        else:
            self.sparse[j] = value
        self._append_event("point", j, z)

    def clear_point(self, index: int) -> None:
        if not isinstance(index, (int, np.integer)) or not 0 <= int(index) < self.n:
            raise ValueError(f"index {index!r} outside [0,{self.n})")
        j = int(index)
        old = self.sparse.get(j, 0j)
        if old != 0j:
            self.add_point(j, -old)

    @property
    def sparse_support(self) -> int:
        return len(self.sparse)

    def _events_since(self, version: int):
        if version < self._log_start_version:
            return None
        if version > self.version:
            raise ValueError("view version is ahead of state")
        start = version - self._log_start_version
        return self._events[start:]

    def _evaluate_bins(self, bins: np.ndarray, phase_provider=None) -> np.ndarray:
        q = len(bins)
        if self.r:
            # BLAS-friendly multiplication over only the requested bins.
            result = self.coefficients @ self.basis_spectra[:, bins]
            result = np.asarray(result, dtype=np.complex128)
        else:
            result = np.zeros(q, dtype=np.complex128)
        if self.sparse:
            if phase_provider is None:
                freq = bins.astype(np.float64)
                for j, delta in self.sparse.items():
                    result += delta * np.exp((-2j * np.pi * j / self.n) * freq)
            else:
                for j, delta in self.sparse.items():
                    result += delta * phase_provider(j)
        return result

    def view(
        self,
        bins: Sequence[int],
        *,
        prepared_positions: Sequence[int] | None = None,
        phase_cache_limit: int = 128,
        auto_rebuild_ratio: float = 1.0,
        pin_event_log: bool = False,
    ) -> "PreparedFourierView":
        v = PreparedFourierView(
            self,
            bins,
            prepared_positions=prepared_positions,
            phase_cache_limit=phase_cache_limit,
            auto_rebuild_ratio=auto_rebuild_ratio,
            pin_event_log=pin_event_log,
        )
        self._views.add(v)
        return v

    def dense(self) -> np.ndarray:
        """Materialize all N Fourier bins from the current relation state."""
        bins = np.arange(self.n, dtype=np.intp)
        return self._evaluate_bins(bins)

    def compact_event_log(self) -> int:
        """Drop events already consumed by every live view.

        Returns the number of dropped events.  If no views are alive, every
        event can be dropped because the current coefficients/residual already
        summarize the complete state.
        """
        # Only views that explicitly require replay pin old events.  Ordinary
        # auto/rebuild-capable views can recover from compaction by rebuilding
        # from the current factorized state.  This is crucial for many consumers:
        # a dormant dashboard must not retain the entire update history.
        pinned = [v for v in self._views if v.pin_event_log]
        if pinned:
            floor = min(v.version for v in pinned)
        else:
            floor = self.version
        if floor <= self._log_start_version:
            return 0
        drop = min(floor - self._log_start_version, len(self._events))
        if drop:
            del self._events[:drop]
            self._log_start_version += drop
        return drop


class PreparedFourierView:
    """A persistent selected-bin view over a DynamicFourierState.

    A view caches its last answer.  State updates remain O(1); on the next
    query the view either replays/coalesces only the intervening events or
    rebuilds directly from the current relation state.
    """

    def __init__(
        self,
        state: DynamicFourierState,
        bins: Sequence[int],
        *,
        prepared_positions: Sequence[int] | None = None,
        phase_cache_limit: int = 128,
        auto_rebuild_ratio: float = 1.0,
        pin_event_log: bool = False,
    ):
        self.state = state
        b = np.asarray(bins, dtype=np.int64)
        if b.ndim != 1 or b.size < 1:
            raise ValueError("bins must be a nonempty 1-D sequence")
        if np.any(b < 0) or np.any(b >= state.n):
            raise ValueError("frequency bin outside valid range")
        self.bins = b.astype(np.intp, copy=True)
        self.q = len(self.bins)
        self.phase_cache_limit = max(0, int(phase_cache_limit))
        self.auto_rebuild_ratio = float(auto_rebuild_ratio)
        self.pin_event_log = bool(pin_event_log)
        if not math.isfinite(self.auto_rebuild_ratio) or self.auto_rebuild_ratio <= 0:
            raise ValueError("auto_rebuild_ratio must be positive")

        # Consumer-specific projection of the cached basis.  This is the key
        # memory trade: O(r*q) instead of carrying/updating N bins per view.
        self._basis_q = np.ascontiguousarray(state.basis_spectra[:, self.bins])
        self._phase_cache: dict[int, np.ndarray] = {}
        self._prepared_row: dict[int, int] = {}
        self._prepared_phase: np.ndarray | None = None
        if prepared_positions is not None:
            positions = np.asarray(prepared_positions, dtype=np.int64)
            if positions.ndim != 1 or np.any(positions < 0) or np.any(positions >= state.n):
                raise ValueError("prepared position outside valid range")
            # Deduplicate while preserving order.
            unique = list(dict.fromkeys(int(x) for x in positions.tolist()))
            pf = np.asarray(unique, dtype=np.float64)
            self._prepared_phase = np.exp(
                (-2j*np.pi/state.n) * np.outer(pf, self.bins.astype(np.float64))
            )
            self._prepared_row = {p:i for i,p in enumerate(unique)}

        self._cached = self._evaluate_current()
        self.version = state.version
        self.last_stats = ViewStats(
            "initial", self.q, 0, 0, 0, state.r, state.sparse_support,
            len(self._phase_cache),
        )

    def _evaluate_current(self) -> np.ndarray:
        if self.state.r:
            result = np.asarray(self.state.coefficients @ self._basis_q, dtype=np.complex128)
        else:
            result = np.zeros(self.q, dtype=np.complex128)
        if self.state.sparse:
            # Use the compact prepared phase table wherever possible.
            prepared_keys=[]; prepared_vals=[]
            for j,delta in self.state.sparse.items():
                row=self._prepared_row.get(j)
                if row is None or self._prepared_phase is None:
                    result += delta*self._phase(j)
                else:
                    prepared_keys.append(row); prepared_vals.append(delta)
            if prepared_keys:
                rows=np.asarray(prepared_keys,dtype=np.intp)
                vals=np.asarray(prepared_vals,dtype=np.complex128)
                result += vals @ self._prepared_phase[rows]
        return result

    def _make_phase(self, position: int) -> np.ndarray:
        return np.exp((-2j * np.pi * position / self.state.n) * self.bins.astype(np.float64))

    def _phase(self, position: int) -> np.ndarray:
        row = self._prepared_row.get(position)
        if row is not None and self._prepared_phase is not None:
            return self._prepared_phase[row]
        p = self._phase_cache.get(position)
        if p is not None:
            return p
        p = self._make_phase(position)
        # Cache arbitrary positions only while under the opportunistic limit.
        if len(self._phase_cache) < self.phase_cache_limit:
            self._phase_cache[position] = p
        return p

    @staticmethod
    def _coalesce(events):
        coeff: dict[int, complex] = {}
        point: dict[int, complex] = {}
        for _, kind, key, delta in events:
            target = coeff if kind == "coeff" else point
            target[key] = target.get(key, 0j) + delta
        coeff = {k:v for k,v in coeff.items() if v != 0j}
        point = {k:v for k,v in point.items() if v != 0j}
        return coeff, point

    def _rebuild(self, backlog: int) -> np.ndarray:
        self._cached = self._evaluate_current()
        self.version = self.state.version
        self.last_stats = ViewStats(
            "rebuild", self.q, backlog, 0, 0, self.state.r,
            self.state.sparse_support, len(self._phase_cache),
        )
        return self._cached.copy()

    def query(self, *, strategy: str = "auto") -> np.ndarray:
        """Return the current selected Fourier bins.

        ``strategy='replay'`` coalesces intervening metadata events and applies
        their Fourier effects to the cached bins.

        ``strategy='rebuild'`` ignores the event log and evaluates the current
        relation state directly.

        ``strategy='auto'`` uses a conservative pre-scan upper bound.  Replaying
        t events costs at most O(t + q*t); rebuilding costs O(q*(r+k)).
        """
        if strategy not in ("auto", "replay", "rebuild"):
            raise ValueError("strategy must be auto, replay, or rebuild")
        backlog = self.state.version - self.version
        if backlog == 0:
            self.last_stats = ViewStats(
                "cached", self.q, 0, 0, 0, self.state.r,
                self.state.sparse_support, len(self._phase_cache),
            )
            return self._cached.copy()

        if strategy == "rebuild":
            return self._rebuild(backlog)

        events = self.state._events_since(self.version)
        if events is None:
            # The shared event log was compacted past this dormant view.
            return self._rebuild(backlog)

        if strategy == "auto":
            replay_upper = backlog * (self.q + 1)
            rebuild_proxy = self.q * max(1, self.state.r + self.state.sparse_support)
            if replay_upper > self.auto_rebuild_ratio * rebuild_proxy:
                return self._rebuild(backlog)

        coeff, point = self._coalesce(events)

        # After paying O(backlog) to inspect the events, a second exact proxy
        # can still prefer rebuilding if cancellations did not help enough.
        if strategy == "auto":
            replay_exact_proxy = backlog + self.q * (len(coeff) + len(point))
            rebuild_proxy = self.q * max(1, self.state.r + self.state.sparse_support)
            if replay_exact_proxy > self.auto_rebuild_ratio * rebuild_proxy:
                return self._rebuild(backlog)

        if coeff:
            # Tiny delta sets are faster as direct vector AXPYs; for larger
            # sets, batch them into one BLAS-friendly product.
            if len(coeff) < 24:
                for i,delta in coeff.items():
                    self._cached += delta*self._basis_q[i]
            else:
                ci = np.fromiter(coeff.keys(), dtype=np.intp, count=len(coeff))
                cv = np.fromiter(coeff.values(), dtype=np.complex128, count=len(coeff))
                self._cached += cv @ self._basis_q[ci]
        if point:
            if self._prepared_phase is not None and all(j in self._prepared_row for j in point):
                if len(point) < 24:
                    for j,delta in point.items():
                        self._cached += delta*self._prepared_phase[self._prepared_row[j]]
                else:
                    rows = np.fromiter((self._prepared_row[j] for j in point), dtype=np.intp, count=len(point))
                    pv = np.fromiter(point.values(), dtype=np.complex128, count=len(point))
                    self._cached += pv @ self._prepared_phase[rows]
            else:
                for j, delta in point.items():
                    self._cached += delta * self._phase(j)

        self.version = self.state.version
        self.last_stats = ViewStats(
            "replay", self.q, backlog, len(coeff), len(point), self.state.r,
            self.state.sparse_support, len(self._phase_cache),
        )
        return self._cached.copy()

    def rebuild(self) -> np.ndarray:
        return self._rebuild(self.state.version - self.version)
