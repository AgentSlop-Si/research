# Projected Relation-Aware Fourier Views

**Date:** 9 October 2026  
**Status:** implemented, correctness-tested, benchmarked in Python/C++; restricted dynamic/structured result. **Not a new arbitrary fresh-input full-DFT or integer-multiplication upper bound.**

## 1. Problem we now solve

The previous adaptive engine still tended to materialize an entire `N`-bin spectrum even when:

1. an upstream producer already knew an exact relation such as a basis-coefficient change or point edit; and
2. a downstream consumer needed only a small set of Fourier bins.

Represent the signal as

\[
 x=\sum_{i=1}^r c_i b_i+e,
\]

where the basis vectors `b_i` are fixed for the lifetime of the view, `c_i` are dynamic coefficients, and `e` is a dynamic `k`-sparse residual. Let `Q` be the consumer's requested frequency set and `q=|Q|`.

The engine stores only the projected basis

\[
 P_{i,u}=F_N(b_i)[u],\qquad i<r,\;u\in Q,
\]

rather than all `r*N` spectral entries. A coefficient update `c_i += delta` and a point update `e_j += delta` are ingested as relation metadata without scanning a dense input.

## 2. Dynamic view theorem

Suppose the view cached its exact selected-bin value after its previous query, and `H` producer updates have occurred since then.

### Replay

Each coefficient event contributes

\[
 \Delta c_i\,P_{i,Q}
\]

and each point event contributes

\[
 \Delta e_j\,(\omega_N^{ju})_{u\in Q}.
\]

Replaying `H` events costs `O(qH)` arithmetic.

### Rebuild

Ignoring the event history and evaluating the current factorized state costs

\[
 O(q(r+k)).
\]

### Planner

At query time `H` is already known from the version counters. Therefore the engine selects replay if `H <= r+k` and rebuild otherwise, before scanning a long event log. With enough recent history retained, the query bound is

\[
 \boxed{T_{query}=O\!\left(q\min\{H,r+k\}\right)}.
\]

A metadata update is expected `O(1)` in the prototype (`array` coefficient change + hash-table sparse residual + append-only event record).

A bounded event log is safe: if a view falls behind the retained history it simply rebuilds from the current factorized state. Dormant/rebuild-capable views do not have to pin old events.

This is a **structured dynamic query result**. It assumes the relation is supplied; it does not discover a low-rank model from an arbitrary dense vector.

## 3. Storage theorem

For one view, persistent numeric Fourier storage is

\[
 O(rq)+O(q)+O(r+k)
\]

plus an optional `O(Pq)` phase table if the producer declares a set of `P` editable point positions. Without prepared positions, phases can be generated on demand/cached.

The basis-projection storage saving over `r` full spectra is exactly

\[
 \boxed{N/q}.
\]

No `O(rN)` basis-spectrum matrix is required by `ProjectedFourierState`.

## 4. Registering a basis without a full spectrum

For `N=K*M`, the first `K` DFT outputs can be computed by `M` strided length-`K` FFTs followed by `O(N)` twiddle/sum work. This is the classical output-pruned FFT construction and costs

\[
 O(N\log K).
\]

`FirstKDFTPlan` prepares the shared twiddle table once for `(N,K)` and then streams basis vectors one at a time. Only their `K` requested outputs are retained. `BandDFTPlan` adds an `O(N)` modulation to support any contiguous block of `K` bins.

The plan is temporary. After all basis rows are registered, it can be discarded, leaving only the `r*K` projection.

### Conditional exact-#130 composition

OpenAI result #130 claims an exact length-`K` DFT cost

\[
 A(K)=O(K(\log K)^{1-\delta}),\qquad \delta=10^{-13},
\]

in its exact complex-arithmetic/specified-root model. Replacing the `M=N/K` small FFTs in the same pruning identity by that primitive gives, for the first `K` outputs,

\[
 \boxed{O\!\left(N\left[1+(\log K)^{1-\delta}\right]\right)}.
\]

For a power-of-two `N` and any requested prefix length `q`, choose the next power of two `K>=q` and discard unused outputs; `K<2q`, giving the same bound with `q+2` inside the logarithm.

A master root can be chosen with order divisible by both `N` and the polynomial-order root required by the size-`K` #130 call. A crude product bound is polynomial (`<1024*N*K^3 <= 1024*N^4`). This is the same *kind* of supplied-root exact-arithmetic model, but the displayed root-order bound is our composition, not #130's original `<1024 N^3` statement.

For `r` streamed basis vectors this makes exact projected registration

\[
 O\!\left(rN\left[1+(\log(q+2))^{1-\delta}\right]\right)
\]

under that conditional backend, after which dynamic selected-bin queries use the relation bound above.

## 5. Sparse-input + sparse-output regime

If only `k` time-domain residual coordinates are nonzero and only `q` Fourier bins are wanted, no FFT is necessary for the residual:

\[
 F_N(e)[u]=\sum_{j\in\operatorname{supp}(e)}e_j\omega_N^{ju},\quad u\in Q,
\]

so the residual contribution costs `O(kq)`. This is why a full-spectrum sparse-update routine is the wrong primitive for a projected consumer.

## 6. C++ hot-path benchmark: predicted crossover appears

Single-threaded C++20, `-O3 -march=native`, complex128. Cached relation:

- `N=8192`
- `r=256`
- `q=64`
- 32 prepared editable point positions
- 4096 mixed coefficient/point updates

The eager comparator maintains all `N` Fourier bins after every metadata update. The rebuild comparator evaluates the selected bins from all current basis coefficients and prepared sparse positions. Replay applies only events since the last query.

| Updates between queries H | Replay ms | Rebuild ms | Eager full-spectrum ms | Rebuild / replay |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1.017 | 299.382 | 61.561 | **294.3x** |
| 4 | 0.875 | 80.915 | 61.561 | **92.5x** |
| 16 | 0.834 | 19.469 | 61.561 | **23.3x** |
| 64 | 0.992 | 4.587 | 61.561 | **4.62x** |
| 128 | 0.929 | 2.580 | 61.561 | **2.78x** |
| 256 | 1.042 | 0.979 | 61.561 | 0.94x |
| 512 | 0.901 | 0.510 | 61.561 | 0.57x |

The empirical crossover is near `H=256`, matching the predicted scale `r+k` (at most about 288 here). Maximum replay/rebuild numerical disagreement was about `3.2e-13`.

## 7. Reused output-pruning plan: practical registration win

After moving twiddle construction out of the per-vector path, the classical pruned transform beats SciPy's full FFT for sufficiently small selected output sets on this runtime.

Examples (median per-vector execution after plan preparation):

| N | K outputs | full FFT ms | planned pruned ms | speedup |
| ---: | ---: | ---: | ---: | ---: |
| 65,536 | 16 | 1.379 | 0.501 | **2.75x** |
| 65,536 | 64 | 0.953 | 0.585 | **1.63x** |
| 262,144 | 16 | 6.121 | 2.075 | **2.95x** |
| 262,144 | 64 | 4.828 | 3.510 | **1.38x** |
| 1,048,576 | 16 | 29.954 | 15.624 | **1.92x** |
| 1,048,576 | 64 | 31.164 | 20.150 | **1.55x** |

At larger `K`, full FFT can still win; e.g. `N=262144,K=256` was slower with pruning. This is exactly why the runtime needs a measured planner rather than assuming the arithmetic-count winner is the wall-clock winner.

### Whole basis registration including plan construction

| N | K | r | full registration | pruned plan + stream | speedup | persistent projection | hypothetical r full spectra |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 262,144 | 64 | 16 | 105.5 ms | 75.4 ms | **1.40x** | 16 KiB | 64 MiB |
| 1,048,576 | 16 | 8 | 276.2 ms | 153.7 ms | **1.80x** | 2 KiB | 128 MiB |

The persistent storage reductions are 4096x and 65,536x respectively. The temporary pruning plans were 4 MiB and 16 MiB and can be freed after registration.

## 8. View-only end-to-end workload

For `N=262144,r=16,q=64`, 512 mixed coefficient/point updates and first-64-bin queries, the projected engine was compared with a baseline that explicitly maintains the dense time-domain signal under coefficient changes and runs a fresh SciPy FFT at each query.

Observed steady-state ratios ranged from roughly **423x to 1316x**, depending on query frequency. This very large ratio is an application result, **not an FFT-vs-FFT speedup**: the projected engine is allowed to preserve the signal in factorized form and never materialize the other `N-q` time/frequency values. If the application also needs the full dense signal, that omitted materialization cost returns.

## 9. Relation to prior work / originality boundary

- Reif and Tate (1997) already studied general incremental DFT and gave an `O(sqrt(N))`-per-request algorithm. Our operation model is stronger/restricted: coefficient updates can encode dense changes in a fixed basis, and producer-supplied structure is trusted.
- Classical pruned FFTs already give `O(N log K)` for `K` selected outputs; FFTW documents both the arithmetic bound and the practical difficulty. Our `FirstKDFTPlan` is an engineering composition around this known identity.
- Dynamic sparse Fourier transform work in 2026 studies a different problem: dynamically maintaining structured measurements for sparse-frequency recovery.
- The novelty claim we can safely make today is **the integrated relation-aware architecture and its measured planner behavior in this prototype**, not priority for the underlying Fourier identities.

A defensible research question is whether this exact producer/consumer-aware abstraction, its `q*min(H,r+k)` planner, and projected-basis registration have appeared together as a Fourier runtime/data-structure design. That needs a dedicated literature review before any novelty claim.

## 10. Files

- `relation_view.py` — shared full-basis relation state + persistent consumer views.
- `projected_fourier.py` — no-`rN` projected state; bounded-history replay/rebuild planner.
- `pruned_output.py` — first-K and contiguous-band reusable output-pruning plans.
- `relation_view_bench.cpp` — compiled hot-path crossover benchmark.
- `benchmark_relation_view.py` — Python relation-view ablations.
- `benchmark_pruned_plan.py` — plan-reuse pruning benchmark.
- `benchmark_registration.py` — end-to-end projected basis registration.
- `benchmark_end_to_end_view.py` — view-only workload benchmark.
- `tests/test_relation_view.py`, `tests/test_projected_fourier.py`, `tests/test_pruned_output.py`.

## 11. Current conclusion

The project's strongest distinct direction is now:

> **Maintain Fourier queries as incremental materialized views over an explicitly factorized signal, rather than treating each state as a fresh dense FFT input.**

This does not beat the arbitrary full-transform theorem or the integer-multiplication `kappa` race on their own terms. It changes the problem in a useful, explicit way and gives a parameterized runtime whose cost can be independent of `N` after basis projection when both relation dimension and requested spectrum are small.
