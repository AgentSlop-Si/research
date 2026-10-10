# Adaptive Fourier view reorganization

**Date:** 2026-10-09  
**Status:** Exact numerical prototype (up to floating-point roundoff), 34 regression tests passing. This is a workload/data-structure result for relation-aware Fourier queries, **not** a new worst-case arbitrary-input DFT upper bound.

## 1. Problem

A producer maintains a structured signal

\[
x = Bc + e,
\]

where the `r` basis spectra have already been projected to a fixed union of consumer Fourier bins, `c` changes through coefficient metadata, and `e` is a sparse residual changed through known point metadata.

Consumer `v` requests only a set `Q_v` of `q_v` Fourier bins. Existing `SharedProjectedFourierStore` already gives one global relation state and exact consumer views, with per-view query work approximately

\[
C_v = q_v \min(H_v, d), \qquad d=r+k,
\]

where `H_v` is the number of producer metadata events since the view was last current and `k` is the present sparse-residual size. The minimum is replay-vs-rebuild.

The remaining problem was automatic **view organization**. If several overlapping consumers query at nearly the same producer versions, independently refreshing them repeats work. If they are asynchronous, forcing a shared union wastes work.

## 2. Lazy spectral groups

For a group `G` of consumers, define

\[
U_G = \bigcup_{v\in G} Q_v, \qquad u_G = |U_G|.
\]

A `SpectralGroup` stores a lazy cache on `U_G`. It is not maintained eagerly. The first group member query after producer changes updates the union; other nearby members read slices from that same cache.

If the group has lag `H_G`, an update of the union costs approximately

\[
C_G = u_G\min(H_G,d).
\]

For a synchronous burst, independent work is approximately

\[
C_{\rm separate}=\sum_{v\in G}q_v\min(H_v,d).
\]

Thus grouping is attractive when temporal synchronization is high and

\[
u_G \ll \sum_{v\in G} q_v.
\]

This is *consumer-level* common-subexpression reuse. It does not change the Fourier identities used by the projected store.

## 3. Online grouping heuristic

`view_optimizer.py` records a bounded sequence of producer versions at which each consumer queried.

For two histories it greedily pairs query timestamps within a small version window and divides the number of matches by the **larger** query count. This deliberately penalizes grouping a very hot view with a much slower one.

For a candidate group:

- `sync(G)` = conservative blend of average and minimum pairwise synchronization;
- `overlap(G) = sum_v q_v / |union_v Q_v|`;
- `benefit(G) = sync(G) * overlap(G)`.

A greedy agglomerative planner merges groups only when synchronization and benefit exceed configured thresholds. This is a cost heuristic, not a claim of globally optimal partitioning.

At execution time there is a second safety guard. Even if the historical partition says to group, the engine compares the currently estimated group cost against the requested member's solo cost, amortized by expected near-future group reuse.

## 4. Zero-rebuild group creation

A subtle but important optimization: if all member views are already current at the same producer version when a group is created, the group union cache can be assembled directly from those member caches. No Fourier arithmetic or low-rank rebuild is required. Overlapping bins are identical by construction.

This prevented a newly merged group from paying a large cold-start rebuild and then being rejected forever by the safety guard.

## 5. Replanning without destroying hot asynchronous workloads

A first prototype replanned after every fixed number of **queries**. This was pathological: one hot asynchronous consumer triggered hundreds of repeated "do not merge" decisions and made the adaptive engine about 2.6x slower in that negative workload.

The final design uses two mechanisms:

1. **Update-epoch pacing for active groups.** Query topology can only become meaningfully different as producer versions advance, so stable partitions exponentially back off the number of update versions between replans.
2. **Dormant singleton probing.** Once the optimizer has established that all views are independent, it stops instrumenting every query. Periodically it opens a bounded observation window, learns recent timing again, and then either forms groups or returns to dormancy.

Replanning at a probe boundary happens on the **next producer update**, after all queries for the previous producer version are complete. That avoids observing only the first member of a synchronized batch.

A regression test confirms that a dormant singleton partition can later wake up, observe newly synchronized overlapping views, and merge them again.

## 6. Benchmark

`benchmark_view_optimizer.py` uses 8 consumers, 32 bins per consumer, `r=256`, 4096 mixed coefficient/point metadata updates, and precomputed projected basis data. Results below are local wall-clock medians (11 runs) and are hardware/runtime dependent.

| Workload | Sequential views | Adaptive organizer | Relative |
|---|---:|---:|---:|
| 8 synchronized overlapping consumers | 119.52 ms | 69.37 ms | **1.72x faster** |
| two phase-separated 4-consumer clusters | 116.80 ms | 81.38 ms | **1.44x faster** |
| fully asynchronous rates | 179.52 ms | 170.57 ms | **near parity (1.05x in this run)** |
| synchronized first half, asynchronous second half | 132.35 ms | 137.50 ms | **near parity (0.96x in this run)** |

The regime-shift run learned one 8-view group during the synchronized half and ended with eight singleton views after schedules diverged. Timings fluctuate enough that near-parity cases should not be described as wins.

The synchronized workload produced 420 group-cache hits and only 60 group replays after learning. The two-cluster workload correctly converged to `{'v0'..'v3'}` and `{'v4'..'v7'}`.

The explicit `query_many` batch API is *not* an oracle lower bound in Python: on these small vectors, building/slicing the ad-hoc batch can itself be slower than sequential NumPy operations. The adaptive persistent group can therefore beat that API by retaining a reusable union cache across bursts.

## 7. Complexity summary

Producer updates remain the same shared-state operations:

\[
\text{coefficient update}=O(1),\qquad \text{point update}=O(1)
\]

in the metadata model.

Without grouping, a query is

\[
O\!\left(q_v\min(H_v,r+k)\right).
\]

For a synchronized group `G`, one group refresh is

\[
O\!\left(u_G\min(H_G,r+k)\right)
\]

plus slicing/copying requested outputs. The benefit therefore depends on **both** temporal synchronization and spectral overlap.

This gives a four-parameter workload picture:

\[
\boxed{\text{cost} = f(\text{relation size},\ \text{requested bins},\ \text{query lag},\ \text{cross-consumer overlap/synchrony})}.
\]

## 8. Originality boundary

Automatic workload clustering and materialized-view selection are longstanding database problems. Prior work explicitly clusters similar queries, merges candidate views, and uses cost-driven selection; materialized-view selection is generally a hard optimization problem. Examples include:

- Aouiche, Jouve, Darmont, *Clustering-Based Materialized View Selection in Data Warehouses* (2007), arXiv:cs/0703114.
- Mistry, Roy, Ramamritham, Sudarshan, *Materialized View Selection and Maintenance Using Multi-Query Optimization* (2000), arXiv:cs/0003006.
- Pang et al., *Materialized View Selection & View-Based Query Planning for Regular Path Queries* (PACMMOD 2024), DOI 10.1145/3654955.

Therefore the generic idea "cluster overlapping queries and materialize shared work" is **not new**. The research value here is narrower: a concrete Fourier-specific state representation and cost model that combines producer-supplied low-rank/sparse relations, arbitrary projected Fourier bins, lazy replay/rebuild, exact union caches, and online merge/split behavior.

## 9. Files

- `view_optimizer.py` — adaptive organizer and lazy spectral groups.
- `tests/test_view_optimizer.py` — merge, split, cache reuse, no-overlap, and dormant-wakeup correctness tests.
- `benchmark_view_optimizer.py` — four workload regimes.
- `benchmark_view_optimizer_results.json` — captured medians and learned partitions.
- `multi_view.py` — shared producer relation state and consumer projections.

## 10. Next research step

The current grouping objective is greedy and memory-unconstrained. The next meaningful extension is a **budgeted spectral materialization problem**:

- each candidate group has storage `O(u_G)` plus optional contiguous basis projection cache;
- each candidate has measured maintenance/query benefit under the observed workload;
- choose a set of possibly overlapping spectral groups under a memory budget;
- include hysteresis/migration cost so the optimizer does not thrash when workloads oscillate.

That would connect the Fourier-specific engine to the classical materialized-view-selection literature while retaining the relation-aware update/query algebra developed here.
