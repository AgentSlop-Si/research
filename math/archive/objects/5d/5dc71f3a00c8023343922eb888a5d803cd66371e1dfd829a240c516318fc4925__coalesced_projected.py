"""Single fixed-bin relation view with coalesced, snapshot-based changes.

This is an independent experimental derivative, not a dense FFT algorithm.
Exact-arithmetic algebra and floating-point implementation are distinct.
See REPORT.md for bounds, ownership, numerical limits and benchmark scope.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence
import numpy as np


def modular_phase(n: int, bins: np.ndarray, j: int) -> np.ndarray:
    """Reduce integer products before floating conversion; never overflow int64.

    The fallback handles products outside signed int64 with Python integers.
    Big-integer bit complexity is not included in the fixed-word cost model.
    """
    maximum = int(bins.max(initial=0))
    if j == 0 or maximum <= np.iinfo(np.int64).max // j:
        residue = (bins * j) % n
    else:
        residue = np.fromiter(((int(b) * j) % n for b in bins), dtype=np.int64, count=len(bins))
    return np.exp((-2j*np.pi) * (residue.astype(float) / n))


@dataclass(frozen=True)
class QueryStats:
    strategy: str
    pending_keys: int
    q: int
    r: int
    k: int
    reclaimed_keys: int


class RelationState:
    """Owned projection plus mutable producer-supplied relation metadata.

    The basis projection must use NumPy's forward, unnormalized DFT convention.
    This API trusts finite input values and assumes no direct external mutation
    of its arrays or dictionaries. Index bounds are checked. Bins may repeat.
    """
    def __init__(self, n: int, bins: Sequence[int], basis_projection: np.ndarray,
                 coefficients: Sequence[complex] | None = None,
                 sparse_residual: Iterable[tuple[int, complex]] = (), *,
                 prepared_positions: Sequence[int] | None = None):
        self.n = int(n)
        if self.n < 1 or self.n > np.iinfo(np.int64).max:
            raise ValueError("n must be a positive signed-int64 value")
        b = np.asarray(bins, dtype=np.int64)
        if b.ndim != 1 or b.size < 1 or np.any(b < 0) or np.any(b >= self.n):
            raise ValueError("bad frequency bins")
        self.bins = b.astype(np.intp, copy=True)
        self.q = len(b)
        p = np.asarray(basis_projection, dtype=np.complex128)
        if p.ndim != 2 or p.shape[1] != self.q:
            raise ValueError("basis_projection must have shape (r,q)")
        # ascontiguousarray alone can retain an r-by-N parent allocation.
        self.projection = np.array(p, dtype=np.complex128, order="C", copy=True)
        self.r = p.shape[0]
        c = np.zeros(self.r, dtype=np.complex128) if coefficients is None else np.asarray(coefficients, dtype=np.complex128)
        if c.shape != (self.r,):
            raise ValueError("bad coefficients")
        self.coefficients = c.copy()
        self.sparse: dict[int, complex] = {}
        for j, value in sparse_residual:
            j = self._point_index(j)
            updated = self.sparse.get(j, 0j) + complex(value)
            if updated == 0j:
                self.sparse.pop(j, None)
            else:
                self.sparse[j] = updated
        self._prepared_row = {}
        self._prepared_phase = None
        if prepared_positions is not None:
            unique = list(dict.fromkeys(self._point_index(j) for j in prepared_positions))
            self._prepared_row = {j: i for i, j in enumerate(unique)}
            self._prepared_phase = np.asarray([modular_phase(self.n, self.bins, j) for j in unique], dtype=np.complex128).reshape(len(unique), self.q)
        self.cached = self._rebuild_value()

    def _point_index(self, j):
        j = int(j)
        if not 0 <= j < self.n:
            raise ValueError("point outside signal")
        return j

    def _coefficient_index(self, i):
        i = int(i)
        if not 0 <= i < self.r:
            raise ValueError("coefficient outside basis")
        return i

    def _phase(self, j):
        row = self._prepared_row.get(j)
        if row is not None and self._prepared_phase is not None:
            return self._prepared_phase[row]
        return modular_phase(self.n, self.bins, j)

    def _rebuild_value(self):
        y = np.asarray(self.coefficients @ self.projection, dtype=np.complex128)
        for j, value in self.sparse.items():
            y += value * self._phase(j)
        return y

    def _set_point(self, j, value):
        if value == 0j:
            self.sparse.pop(j, None)
        else:
            self.sparse[j] = value

    @property
    def numeric_payload_bytes(self):
        """Numeric buffers only; excludes dict/tuple/scalar allocator overhead."""
        phase = 0 if self._prepared_phase is None else self._prepared_phase.nbytes
        return self.projection.nbytes + self.coefficients.nbytes + self.bins.nbytes + self.cached.nbytes + phase


class CoalescedProjectedFourier(RelationState):
    """At most one pending snapshot for each changed coefficient/point.

    A snapshot stores the value before the first post-query edit. The replay
    delta is CURRENT - SNAPSHOT, not the sum of the requested update deltas.
    Returning exactly to the snapshot removes the entry immediately.

    Expected update cost: O(1), with Python dictionary amortization.
    Query cost: O(q*(1 + min(u,r+k)) + u), including snapshot reclamation.
    Live payload: O(r*q + P*q + r + k + u + q), P prepared positions.
    Python dictionary capacity can follow prior high-water sizes; see report.
    In particular, rebuild is not claimed to have a worst-case O(q*(r+k))
    total latency when u is large. No delayed garbage is hidden off-timer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pending: dict[tuple[str, int], complex] = {}
        self._pending_high_water = 0
        self.last_stats = QueryStats("initial", 0, self.q, self.r, len(self.sparse), 0)

    def _remember(self, key, before, after):
        baseline = self.pending.get(key, before)
        if after == baseline:
            removed = self.pending.pop(key, None)
            if removed is not None:
                size = len(self.pending)
                # Deletions leave dictionary tombstones. Shrink geometrically
                # on UPDATE so query clear cannot inherit a much larger table.
                # The occasional O(size) copy/old-table destruction is charged
                # to the intervening deletions: amortized O(1) per update.
                if size == 0:
                    self.pending.clear()
                    self._pending_high_water = 0
                elif 4*size < self._pending_high_water:
                    self.pending = dict(self.pending)
                    self._pending_high_water = size
        else:
            self.pending[key] = baseline
            self._pending_high_water = max(self._pending_high_water, len(self.pending))

    def add_coefficient(self, i, delta):
        i = self._coefficient_index(i)
        z = complex(delta)
        if z == 0j:
            return
        before = complex(self.coefficients[i])
        self.coefficients[i] += z
        self._remember(("c", i), before, complex(self.coefficients[i]))

    def add_point(self, j, delta):
        j = self._point_index(j)
        z = complex(delta)
        if z == 0j:
            return
        before = self.sparse.get(j, 0j)
        after = before + z
        self._set_point(j, after)
        self._remember(("p", j), before, after)

    def query(self):
        u, k = len(self.pending), len(self.sparse)
        if not u:
            strategy = "cached"
        elif u <= self.r + k:
            strategy = "coalesced"
            for (kind, key), before in self.pending.items():
                if kind == "c":
                    self.cached += (self.coefficients[key] - before) * self.projection[key]
                else:
                    self.cached += (self.sparse.get(key, 0j) - before) * self._phase(key)
        else:
            strategy = "rebuild"
            self.cached = self._rebuild_value()
        # CPython clear releases u entries here: O(u), including on rebuild.
        self.pending.clear()
        self._pending_high_water = 0
        self.last_stats = QueryStats(strategy, u, self.q, self.r, k, u)
        return self.cached.copy()

    def rebase(self):
        """Explicit O(q*(1+r+k)+u) rebuild to limit accumulated replay drift."""
        u = len(self.pending)
        self.cached = self._rebuild_value()
        self.pending.clear()
        self._pending_high_water = 0
        self.last_stats = QueryStats("explicit_rebase", u, self.q, self.r, len(self.sparse), u)
        return self.cached.copy()


class AlwaysRebuild(RelationState):
    """Matched-q comparator with O(1) metadata edits and no event logging."""
    def add_coefficient(self, i, delta):
        self.coefficients[self._coefficient_index(i)] += complex(delta)

    def add_point(self, j, delta):
        j = self._point_index(j)
        self._set_point(j, self.sparse.get(j, 0j) + complex(delta))

    def query(self):
        self.cached = self._rebuild_value()
        return self.cached.copy()


class EagerProjected(RelationState):
    """Matched-q O(q)-per-edit comparator, based on represented state changes."""
    def add_coefficient(self, i, delta):
        i = self._coefficient_index(i)
        before = complex(self.coefficients[i])
        self.coefficients[i] += complex(delta)
        self.cached += (self.coefficients[i] - before) * self.projection[i]

    def add_point(self, j, delta):
        j = self._point_index(j)
        before = self.sparse.get(j, 0j)
        after = before + complex(delta)
        self._set_point(j, after)
        self.cached += (after - before) * self._phase(j)

    def query(self):
        return self.cached.copy()
