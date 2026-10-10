# Arbitrary-output + multi-consumer relation-aware Fourier continuation

**Date:** 2026-10-09  
**Status:** 30 regression tests pass. The underlying pruning identities are classical; the contribution here is the integrated runtime/data-structure design, planner experiments, and a straightforward conditional corollary of OpenAI #130. No novelty/priority claim is made without a dedicated literature review.

## 1. Arbitrary requested bins with one shared pruned pass

Let `Q={j_1,...,j_q}` be any requested Fourier bins and let `N=K*M`. Write a time index as

`n = m + M*r`, with `0<=m<M`, `0<=r<K`.

For the length-N DFT,

`X[j] = sum_m G[m, j mod K] exp(-2*pi*i*m*j/N)`,

where

`G[m,s] = sum_r x[m+M*r] exp(-2*pi*i*r*s/K)`

is a length-K DFT along each strided fiber. Hence one batch of `M=N/K` length-K FFTs is shared by every requested output. The final combination costs `O(q*N/K)`.

Classically,

`T(N,q,K)=O(N log K + q*N/K)`.

For divisor-friendly lengths (in particular power-of-two `N`), choose `K=Theta(q)` to obtain

`T(N,q)=O(N log q)`

for **arbitrary** output locations, not only a prefix or a contiguous band. This is standard generic FFT pruning; FFTW's pruning notes explicitly describe the same general case.

### Implementation

`arbitrary_output.py` implements:

- `ArbitraryBinsDFTPlan`: reusable arbitrary-output Cooley--Tukey plan;
- `FullFFTBinPlan`: full optimized FFT fallback;
- `AutoOutputPlan`: measured but explicitly charged active tuner;
- `ProductiveProjectionPlanner`: experimental tuner whose transform trials are useful basis registrations, not throwaway work.

The reusable phase table has `q*(N/K)` complex values. If `K>=q`, this is `O(N)` temporary plan storage even for completely scattered bins.

## 2. Conditional #130 arbitrary-output corollary

OpenAI result #130 states an all-length exact DFT algorithm in its exact-complex/specified-root model with

`A(s)=O(s (log s)^theta (log log s)^(4-theta))`, `theta<1`,

and the displayed corollary `O(s (log s)^(1-10^-13))`.

Substitute that exact transform only into the `M=N/K` inner length-K transforms above. For power-of-two `N`, choose the next power of two `K` with `q<=K<2q`. Then

`T_130_partial(N,q)`
`= (N/K) A(K) + O(q*N/K) + O(N)`
`= O(N [1 + (log q)^theta (log log q)^(4-theta)])`.

Using the paper's decimal corollary as a coarser statement gives

`O(N [1 + (log q)^(1-10^-13)])`.

This is a black-box partial-output corollary, not a stronger full-DFT theorem. For constant `q`, the bound is `Theta(N)` because even reading an arbitrary dense input is linear.

A repository search did not locate this arbitrary-output corollary stated explicitly in result #130, but that is **not** a priority claim; the derivation is a direct classical pruning composition.

## 3. Practical arbitrary-bin benchmark

`benchmark_arbitrary_output.py` uses uniformly random requested bins and compares the shared pruned plan with SciPy's complete FFT followed by gather.

Representative captured medians:

| N | q random bins | best K | full FFT+gather | pruned | speedup |
|---:|---:|---:|---:|---:|---:|
| 262,144 | 1 | 1 | 5.875 ms | 0.604 ms | **9.73x** |
| 262,144 | 16 | 64 | 4.503 ms | 2.255 ms | **2.00x** |
| 262,144 | 64 | 256 | 4.203 ms | 3.251 ms | **1.29x** |
| 1,048,576 | 4 | 16 | 29.920 ms | 10.245 ms | **2.92x** |
| 1,048,576 | 16 | 64 | 34.956 ms | 14.294 ms | **2.45x** |
| 1,048,576 | 64 | 256 | 29.032 ms | 14.874 ms | **1.95x** |
| 1,048,576 | 256 | 1024 | 30.410 ms | 16.572 ms | **1.84x** |

Not every `q` wins. For `N=262144,q=256`, the measured pruned plan was approximately break-even/slightly slower. This is why the runtime retains the native full-FFT fallback.

A notable engineering result is that the fastest measured radix is often around `4q`, rather than the simple arithmetic-count optimum. Backend locality and the smaller final phase table matter.

## 4. Active tuning failed to amortize quickly

`benchmark_autotune_registration.py` explicitly charges testing several plans. On `N=262144,q=64`, active tuning cost around 160--180 ms in the captured runs and did not amortize even across 32 basis vectors.

This is a **negative result**: a planner should not benchmark many complete candidate transforms merely to choose a radix for one small registration job.

`ProductiveProjectionPlanner` therefore explores a different idea: candidate strategies process different basis rows that are required anyway. This removes throwaway transform executions, though construction of losing phase tables is still real overhead. The current results are mixed; it remains experimental rather than the default policy.

## 5. Multi-consumer shared relation state

If many consumers observe the same factorized signal but request different frequency sets, duplicating the relation state is unnecessary.

`multi_view.py` implements one global state

`x = sum_i c_i b_i + e`

with:

- one coefficient vector;
- one sparse residual map;
- one bounded event log;
- one basis projection onto the union of all declared bins;
- independent consumer view versions/caches.

A producer metadata update is stored **once**, expected `O(1)`, regardless of consumer count.

Consumer `v`, with `q_v` bins and lag `H_v`, still satisfies the view planner bound

`O(q_v * min(H_v, r+k))`.

Dormant consumers do not force unbounded history. If bounded history drops events they missed, they rebuild exactly from the current factorized state.

### Cross-consumer query fusion

For a set `S` of consumers querying at the same logical update, the runtime compares individual work

`sum_{v in S} q_v min(H_v,r+k)`

with one exact rebuild on their current union

`|union_{v in S} Q_v| (r+k)`.

If the union rebuild is cheaper, it is computed once and scattered back to the consumers. This converts frequency overlap into computation reuse.

### Hot-view locality cache

Very frequently queried consumers may cache a contiguous `r x q_v` basis slice. Cold consumers continue to reference the shared union projection. This is a deliberate memory/locality tradeoff; prepared sparse-phase tables remain shared globally so promotion cannot silently duplicate the dominant phase cache.

## 6. Multi-consumer benchmark: positive and negative regimes

`benchmark_multi_view.py` uses 8 consumers, 16 bins each, 8 bins shared by all consumers, 72 distinct union bins, `N=262144`, `r=16`, and 4096 mixed metadata updates.

### Heterogeneous query cadence

Intervals: `1,2,4,8,16,32,64,128` updates.

The shared Python store was slower than 8 independent projected views in the captured run (about `0.57x` relative speed) despite lower numeric storage. This is a real negative result: Python control/indexing overhead can dominate when views query at very different rates and fusion rarely applies.

### Synchronized query cadence

All 8 consumers query every 64 updates.

The shared fused store was **3.28x faster** than 8 independent relation views in the captured run. Earlier repeated runs varied around roughly 3.3--3.8x. Numeric storage remained lower, and basis projection storage was about **3641x smaller** than hypothetical cached full basis spectra.

The lesson is not "shared is always faster". The useful planner dimension is **consumer synchrony/overlap**.

## 7. Arbitrary-bin end-to-end workload

`benchmark_arbitrary_end_to_end.py` uses:

- `N=262144`, `r=16`, `q=64` uniformly random bins;
- 512 mixed coefficient/point updates;
- a query every 4 updates.

Captured result:

- arbitrary pruned registration: `112.5 ms`;
- full FFT registration: `104.7 ms` (pruned registration lost by ~7% in this run);
- projected steady-state: `1.94 ms`;
- dense signal maintenance + fresh FFT queries: `1254.8 ms`;
- steady-state ratio: **648x**;
- persistent basis-spectrum storage reduction: **4096x**.

The 648x figure is an application/data-structure result, **not an FFT-vs-FFT claim**. The projected engine never materializes the full dense signal or unused spectrum. If the consumer needs those values, that work returns.

## 8. Current theorem-form abstraction

For a fixed arbitrary consumer frequency set `Q`, `|Q|=q`, producer-supplied factorization

`x = B c + e`, `rank(B)=r`, `||e||_0=k`,

and `H` trusted metadata events since the consumer last queried:

### After projected basis registration

- coefficient metadata update: expected `O(1)`;
- sparse point metadata update: expected `O(1)`;
- consumer query: `O(q min(H,r+k))`;
- persistent basis projection: `Theta(rq)` complex values.

### Fresh basis registration, classical power-of-two case

- arbitrary `q` outputs per basis: `O(N log q)` arithmetic;
- temporary plan storage: `O(N)` with `K=Theta(q)`;
- persistent storage after registration: `Theta(rq)`.

### Fresh basis registration, conditional exact #130 model

- arbitrary `q` outputs per basis:
  `O(N [1 + (log q)^theta (log log q)^(4-theta)])`;
- coarser displayed corollary:
  `O(N [1 + (log q)^(1-10^-13)])`.

For many consumers, replace `q` in registration/storage by the size `u` of their union if one shared projection is used.

## 9. Originality boundary

Known ingredients include:

- generic pruned FFTs for arbitrary output subsets (`O(N log q)`);
- dynamic/incremental DFT techniques;
- Fourier linearity and low-rank reconstruction;
- output-sensitive/truncated Fourier methods.

What is specific to this project is the integrated **relation-state + arbitrary-output projection + per-consumer lag planner + multi-consumer union/fusion** runtime and the measured positive/negative break-even maps. A serious novelty claim would require a broader systems/data-structure literature review.

## 10. Reproduce

```bash
OPENBLAS_NUM_THREADS=1 python -m unittest discover -v tests
OPENBLAS_NUM_THREADS=1 python benchmark_arbitrary_output.py
OPENBLAS_NUM_THREADS=1 python benchmark_arbitrary_end_to_end.py
OPENBLAS_NUM_THREADS=1 python benchmark_multi_view.py
```

Primary external references:

- FFTW pruning notes: https://fftw.org/pruned.html
- OpenAI result #130 scope: https://github.com/openai/math/blob/main/lean/docs/130.md
