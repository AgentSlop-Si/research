"""Online reorganization of many projected Fourier consumers.

This module sits on top of :mod:`multi_view`.  It observes *when* consumers
query and *which* Fourier bins they request.  Consumers that repeatedly query
within a small producer-update window and have overlapping frequency sets are
placed into a lazy spectral group.  A group stores one cached spectrum on the
union of its members' bins; the first member query updates/rebuilds that union,
and nearby member queries become cache hits.

The partition is recomputed from a bounded recent history, so groups disappear
again when query rates or phases diverge.  Producer metadata changes remain one append except at scheduled probe
boundaries, when an update can also execute the nonconstant greedy planner.
Planning time is reported separately and charged in end-to-end benchmarks.

This is a workload optimizer, not a different Fourier identity.  Its planner
uses a simple cost proxy and all numerical answers remain exact up to normal
floating-point roundoff of the underlying projected representation.
"""
from __future__ import annotations

from collections import deque, OrderedDict
from dataclasses import dataclass, field
from itertools import combinations, islice
from time import perf_counter_ns
from typing import Iterable, Mapping, Sequence

import numpy as np

from multi_view import SharedProjectedFourierStore


@dataclass
class SpectralGroup:
    gid: int
    members: tuple[str, ...]
    indices: np.ndarray
    take: dict[str, np.ndarray]
    sync_score: float
    overlap_ratio: float
    benefit_score: float
    cached: np.ndarray | None = None
    version: int = -1
    strategy: str = "cold"
    uses: int = 0
    cache_hits: int = 0
    replays: int = 0
    rebuilds: int = 0

    @property
    def width(self) -> int:
        return int(self.indices.size)


@dataclass
class OptimizerStats:
    replans: int = 0
    planning_ns: int = 0
    replay_records: int = 0
    published_bins: int = 0
    group_cache_evictions: int = 0
    group_queries: int = 0
    solo_queries: int = 0
    group_cache_hits: int = 0
    group_replays: int = 0
    group_rebuilds: int = 0
    guarded_solo: int = 0
    partitions: list[tuple[tuple[str, ...], ...]] = field(default_factory=list)


def _greedy_match_fraction(a: Sequence[int], b: Sequence[int], window: int) -> float:
    """Symmetric recent-query synchronization score in [0,1].

    Query timestamps are producer versions.  We greedily pair timestamps whose
    distance is <= ``window`` and divide by the larger history length.  The
    denominator is deliberately the larger count: a slow consumer that happens
    to align with a tiny subset of a hot consumer should *not* look synchronized.
    """
    if not a or not b:
        return 0.0
    aa = list(a); bb = list(b)
    i = j = matches = 0
    while i < len(aa) and j < len(bb):
        d = aa[i] - bb[j]
        if abs(d) <= window:
            matches += 1; i += 1; j += 1
        elif d < 0:
            i += 1
        else:
            j += 1
    return matches / max(len(aa), len(bb))


class AdaptiveSpectralOrganizer:
    """Adaptive grouping layer for :class:`SharedProjectedFourierStore`.

    Parameters are intentionally conservative.  A merge must have both recent
    temporal synchronization and enough frequency overlap to reduce the proxy
    cost.  Replanning uses only bounded query history and never touches the
    producer's dense signal.
    """

    def __init__(
        self,
        store: SharedProjectedFourierStore,
        *,
        sync_window: int = 1,
        history_queries: int = 24,
        min_history: int = 4,
        replan_every: int = 24,
        replan_min_updates: int = 64,
        replan_max_updates: int = 512,
        probe_period_updates: int = 1024,
        probe_window_updates: int = 256,
        merge_threshold: float = 1.08,
        min_sync: float = 0.45,
        immediate_guard: float = 1.08,
        max_group_size: int | None = None,
        max_group_cache_bytes: int = 8*1024**2,
        partition_history_limit: int = 128,
    ):
        self.store = store
        self.max_group_cache_bytes = int(max_group_cache_bytes)
        if self.max_group_cache_bytes < 0: raise ValueError("negative cache budget")
        self._group_cache_bytes = 0
        self._cache_order = OrderedDict()
        self.sync_window = max(0, int(sync_window))
        self.history_queries = max(2, int(history_queries))
        self.min_history = max(2, int(min_history))
        # replan_every is retained as a minimum number of observed queries, but
        # update epochs are the primary cadence. Query-count-only replanning is
        # pathological when one consumer is very hot.
        self.replan_every = max(1, int(replan_every))
        self.replan_min_updates = max(1, int(replan_min_updates))
        self.replan_max_updates = max(self.replan_min_updates, int(replan_max_updates))
        self.probe_period_updates = max(1, int(probe_period_updates))
        self.probe_window_updates = max(1, int(probe_window_updates))
        self.merge_threshold = float(merge_threshold)
        self.min_sync = float(min_sync)
        self.immediate_guard = float(immediate_guard)
        self.max_group_size = None if max_group_size is None else max(2, int(max_group_size))

        self.history: dict[str, deque[int]] = {
            name: deque(maxlen=self.history_queries) for name in self.store.views
        }
        self.groups: dict[int, SpectralGroup] = {}
        self.member_group: dict[str, int] = {}
        self._queries_since_replan = 0
        self._last_replan_version = self.store.version
        self._next_replan_updates = self.replan_min_updates
        self._last_partition = None
        self._all_singletons = True
        self._probe_active = True
        self._probe_end_version = self.store.version + self.probe_window_updates
        self._next_probe_version = 0
        self._next_gid = 1
        self.stats = OptimizerStats()
        self.stats.partitions = deque(maxlen=max(0,int(partition_history_limit)))
        self._install_singletons()

    # ---------- planner ----------
    def _install_singletons(self) -> None:
        self.groups.clear(); self.member_group.clear()
        for name in sorted(self.store.views):
            self._install_group((name,), sync=0.0, overlap=1.0, benefit=1.0)

    def _install_group(self, members: Iterable[str], *, sync: float, overlap: float, benefit: float) -> SpectralGroup:
        mem = tuple(sorted(members))
        idx = np.asarray(sorted(set(int(i) for n in mem for i in self.store.views[n].indices)), dtype=np.intp)
        pos = {int(x): j for j, x in enumerate(idx)}
        take = {
            n: np.asarray([pos[int(i)] for i in self.store.views[n].indices], dtype=np.intp)
            for n in mem
        }
        g = SpectralGroup(self._next_gid, mem, idx, take, float(sync), float(overlap), float(benefit))
        self._next_gid += 1
        self.groups[g.gid] = g
        for n in mem: self.member_group[n] = g.gid
        return g

    def _seed_from_member_caches(self, g: SpectralGroup) -> bool:
        """Seed a union cache by copying members at a common version.

        Replanning should not force a numerical rebuild merely because two
        already-current views were merged.  Their cached coordinates cover the
        union; overlapping bins are identical by construction.
        """
        if len(g.members) <= 1 or g.width*16 > self.max_group_cache_bytes:
            return False
        versions={self.store.views[n].version for n in g.members}
        if len(versions)!=1:
            return False
        version=next(iter(versions))
        y=np.empty(g.width,dtype=np.complex128)
        filled=np.zeros(g.width,dtype=bool)
        for n in g.members:
            v=self.store.views[n]
            pos=g.take[n]
            missing=~filled[pos]
            if np.any(missing):
                y[pos[missing]]=v.cached[missing]
                filled[pos[missing]]=True
        if not np.all(filled):
            return False
        g.cached=np.ascontiguousarray(y); g.version=version; g.strategy='seeded'
        return True

    def _sync(self, a: str, b: str) -> float:
        return _greedy_match_fraction(self.history[a], self.history[b], self.sync_window)

    def _cluster_metrics(self, members: Sequence[str]) -> tuple[float, float, float]:
        members = tuple(members)
        widths = [len(self.store.views[n].indices) for n in members]
        total = sum(widths)
        union = len(set(int(i) for n in members for i in self.store.views[n].indices))
        overlap = total / max(1, union)
        if len(members) == 1:
            return 1.0, overlap, 1.0
        syncs = [self._sync(a,b) for a,b in combinations(members,2)]
        # Harmonic-ish conservative blend: the minimum prevents a single badly
        # phased member from hitchhiking on an otherwise synchronized cluster.
        avg = float(np.mean(syncs)) if syncs else 0.0
        mn = min(syncs) if syncs else 0.0
        sync = 0.65 * avg + 0.35 * mn
        benefit = sync * overlap
        return sync, overlap, benefit

    def _eligible(self, members: Sequence[str], metrics: tuple[float,float,float]) -> bool:
        if len(members) <= 1: return True
        if self.max_group_size is not None and len(members) > self.max_group_size: return False
        if any(len(self.history[n]) < self.min_history for n in members): return False
        sync, _overlap, benefit = metrics
        return sync >= self.min_sync and benefit >= self.merge_threshold

    def replan(self) -> tuple[tuple[str, ...], ...]:
        """Greedy agglomerative partition under the measured cost proxy."""
        planning_start = perf_counter_ns()
        clusters = [tuple([n]) for n in sorted(self.store.views)]
        while True:
            best = None
            for i in range(len(clusters)):
                for j in range(i+1, len(clusters)):
                    merged = tuple(sorted(clusters[i] + clusters[j]))
                    metrics = self._cluster_metrics(merged)
                    if not self._eligible(merged, metrics):
                        continue
                    # Prefer the largest expected multiplicative saving.  A tiny
                    # size bonus makes deterministic larger cohesive groups win ties.
                    score = metrics[2] + 1e-6 * len(merged)
                    if best is None or score > best[0]:
                        best = (score, i, j, merged, metrics)
            if best is None:
                break
            _, i, j, merged, _metrics = best
            clusters = [c for k,c in enumerate(clusters) if k not in (i,j)] + [merged]

        # Preserve numerical caches for unchanged groups. Greedy planning,
        # new index maps, and bookkeeping still have a measured cost.
        old_by_members = {g.members:g for g in self.groups.values()}
        self.groups = {}; self.member_group = {}
        for members in sorted(clusters):
            metrics = self._cluster_metrics(members)
            old = old_by_members.get(tuple(sorted(members)))
            g = self._install_group(members, sync=metrics[0], overlap=metrics[1], benefit=metrics[2])
            if old is not None:
                g.cached = old.cached
                g.version = old.version
                g.strategy = old.strategy
                g.uses = old.uses; g.cache_hits = old.cache_hits
                g.replays = old.replays; g.rebuilds = old.rebuilds
            else:
                self._seed_from_member_caches(g)

        self._cache_order.clear()
        self._group_cache_bytes = 0
        for group in self.groups.values():
            if group.cached is not None: self._touch_group_cache(group)
        self.stats.replans += 1
        part = tuple(sorted((g.members for g in self.groups.values()), key=lambda x:(len(x),x)))
        self.stats.partitions.append(part)
        changed = self._last_partition is not None and part != self._last_partition
        self._all_singletons = all(len(x)==1 for x in part)
        if changed:
            self._next_replan_updates = self.replan_min_updates
        else:
            self._next_replan_updates = min(self.replan_max_updates, max(
                self.replan_min_updates, self._next_replan_updates * 2))
        if self._all_singletons:
            # Stable singleton workloads go dormant.  We reopen a bounded
            # observation window periodically so new synchronization can still
            # be discovered without taxing every hot query.
            self._probe_active = False
            self._next_probe_version = self.store.version + self.probe_period_updates
        else:
            self._probe_active = True
        self._last_partition = part
        self._last_replan_version = self.store.version
        self._queries_since_replan = 0
        self.stats.planning_ns += perf_counter_ns()-planning_start
        return part

    def _maybe_replan(self) -> None:
        if self._queries_since_replan < self.replan_every:
            return
        if self.store.version - self._last_replan_version < self._next_replan_updates:
            return
        self.replan()

    @property
    def partition(self) -> tuple[tuple[str, ...], ...]:
        return tuple(sorted((g.members for g in self.groups.values()), key=lambda x:(len(x),x)))

    # ---------- group execution ----------
    def _group_history_available(self, g: SpectralGroup) -> bool:
        if g.cached is None: return False
        if g.version == self.store.version: return True
        return bool(self.store.events) and self.store.events[0][0] <= g.version + 1

    def _replay_group(self, g: SpectralGroup) -> None:
        assert g.cached is not None
        backlog = self.store.version-g.version
        recent = list(islice(reversed(self.store.events), backlog))
        self.stats.replay_records += len(recent)
        for ver,kind,key,delta in reversed(recent):
            if kind == 'c':
                g.cached += delta * self.store.projection[key, g.indices]
            else:
                g.cached += delta * self.store._phase_view(key, g.indices)

    def _publish_group(self, g: SpectralGroup, backlog: int, strategy: str, requested: str) -> None:
        assert g.cached is not None
        for name in (requested,):
            v = self.store.views[name]
            self.stats.published_bins += len(v.indices)
            v.cached = np.ascontiguousarray(g.cached[g.take[name]])
            v.version = self.store.version
            v.backlog = backlog
            v.strategy = strategy

    def _group_query(self, g: SpectralGroup, requested: str) -> np.ndarray:
        current = self.store.version
        if g.cached is not None and g.version == current:
            g.cache_hits += 1; self.stats.group_cache_hits += 1
            g.strategy = 'group_cached'; g.uses += 1; self.stats.group_queries += 1
            self._publish_group(g, 0, 'group_cached', requested)
            self._touch_group_cache(g)
            return self.store.views[requested].cached.copy()

        H = current - g.version if g.cached is not None else current + 1
        d = self.store.r + len(self.store.sparse)
        if g.cached is not None and H <= max(1,d) and self._group_history_available(g):
            self._replay_group(g)
            g.replays += 1; self.stats.group_replays += 1
            strategy = 'group_replay'
        else:
            g.cached = self.store._rebuild(g.indices)
            g.rebuilds += 1; self.stats.group_rebuilds += 1
            strategy = 'group_rebuild'
        g.version = current; g.strategy = strategy; g.uses += 1; self.stats.group_queries += 1
        self._publish_group(g, max(0,H), strategy, requested)
        self._touch_group_cache(g)
        return self.store.views[requested].cached.copy()

    def _should_use_group(self, g: SpectralGroup, name: str) -> bool:
        if len(g.members) <= 1 or g.width*16 > self.max_group_cache_bytes: return False
        v = self.store.views[name]
        if v.version == self.store.version: return False
        if g.cached is not None and g.version == self.store.version: return True
        d = max(1, self.store.r + len(self.store.sparse))
        Hv = self.store.version - v.version
        Hg = (self.store.version - g.version) if g.cached is not None else d
        solo_work = min(max(1,Hv), d) if self.store._history_available(v) else d
        solo = max(1, len(v.indices)) * solo_work
        group_work = min(max(1,Hg), d) if self._group_history_available(g) else d
        grouped = max(1, g.width) * group_work
        expected_queries = 1.0 + g.sync_score * (len(g.members)-1)
        amortized = grouped / expected_queries
        return amortized <= self.immediate_guard * solo

    def _touch_group_cache(self, g):
        if g.cached is None: return
        if g.gid not in self._cache_order:
            self._cache_order[g.gid] = g.cached.nbytes
            self._group_cache_bytes += g.cached.nbytes
        self._cache_order.move_to_end(g.gid)
        while self._group_cache_bytes > self.max_group_cache_bytes:
            gid, size = self._cache_order.popitem(last=False)
            self._group_cache_bytes -= size
            old = self.groups[gid]
            old.cached = None; old.version = -1
            self.stats.group_cache_evictions += 1

    def memory_report(self):
        return {"group_cache_bytes": self._group_cache_bytes,
                "group_cache_budget": self.max_group_cache_bytes,
                "query_history_numeric_bytes": sum(len(v)*8 for v in self.history.values()),
                "retained_partition_snapshots": len(self.stats.partitions),
                "total_numeric_payload_bytes": self.storage_bytes,
                "excludes_python_objects_and_planner_temporary_memory": True}

    # ---------- public query/update API ----------
    def _observe(self, name: str) -> None:
        self.history.setdefault(name, deque(maxlen=self.history_queries)).append(self.store.version)
        self._queries_since_replan += 1

    def _start_probe(self) -> None:
        for h in self.history.values(): h.clear()
        self._queries_since_replan = 0
        self._probe_active = True
        self._probe_end_version = self.store.version + self.probe_window_updates

    def _singleton_query_preamble(self) -> bool:
        """Return True when this query should be observed."""
        if self._probe_active:
            return True
        if self.store.version >= self._next_probe_version:
            self._start_probe(); return True
        return False

    def _finish_probe_before_update(self) -> None:
        # Producer updates delimit a complete query epoch: every query for the
        # previous version has already happened. Replanning here avoids seeing
        # only the first member of a synchronized query batch.
        if self._all_singletons and self._probe_active and self.store.version >= self._probe_end_version:
            self.replan()

    def query(self, name: str) -> np.ndarray:
        # Very hot asynchronous workloads spend most of their lifetime here:
        # a stable singleton partition outside a probe window. Keep this path
        # intentionally tiny.
        if self._all_singletons and not self._probe_active and self.store.version < self._next_probe_version:
            return self.store.query(name)
        name = str(name)
        if name not in self.store.views: raise KeyError(name)
        if self._all_singletons:
            observe=self._singleton_query_preamble()
            if observe:self._observe(name)
            self.stats.solo_queries += 1
            out=self.store.query(name)
            return out

        self._observe(name)
        gid = self.member_group.get(name)
        g = self.groups.get(gid) if gid is not None else None
        if g is not None and self._should_use_group(g,name):
            out = self._group_query(g,name)
        else:
            if g is not None and len(g.members)>1: self.stats.guarded_solo += 1
            self.stats.solo_queries += 1
            out = self.store.query(name)
        self._maybe_replan()
        return out

    def query_many(self, names: Sequence[str]) -> dict[str,np.ndarray]:
        names = list(dict.fromkeys(str(n) for n in names))
        for n in names:
            if n not in self.store.views: raise KeyError(n)
        if self._all_singletons:
            observe=self._singleton_query_preamble()
            if observe:
                for n in names:self._observe(n)
            out=self.store.query_many(names)
            return out
        for n in names:self._observe(n)
        out=self.store.query_many(names)
        self._maybe_replan()
        return out

    def add_coefficient(self, i: int, delta: complex) -> None:
        if self._all_singletons and self._probe_active and self.store.version >= self._probe_end_version:
            self.replan()
        self.store.add_coefficient(i,delta)

    def add_point(self, j: int, delta: complex) -> None:
        if self._all_singletons and self._probe_active and self.store.version >= self._probe_end_version:
            self.replan()
        self.store.add_point(j,delta)

    def compact(self) -> None:
        self.store.compact()

    @property
    def storage_bytes(self) -> int:
        extra = 0
        for g in self.groups.values():
            extra += g.indices.nbytes
            if g.cached is not None: extra += g.cached.nbytes
            extra += sum(x.nbytes for x in g.take.values())
        extra += sum(len(h)*8 for h in self.history.values())
        return int(self.store.storage_bytes + extra)
