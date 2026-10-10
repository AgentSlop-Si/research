Public source-text preservation. The mathematical source body below is unchanged. Read [the scoped audit](../../reviews/04_jordan_jets.md) and [independent second review](../../reviews/05_jordan_second_review.md) for the accepted qualifications. In particular, the exponential-generating restatement needs invertible factorials (d < characteristic in positive characteristic); a finite union of proper finite-field subspaces need not be proper, so use the review’s corrected piecewise counting bound; and greedy piecewise recognition is an accepted-input guarantee, not a complete recognizer. Source benchmark numbers are unrerun author reports, and the padded 2N-output crossover is not an ordinary N-output speedup. No source programs are included.

# Hero #17 — Phase 22: Jordan–Green Union, dense forcing with bounded recurrence rank

**Date:** 10 October 2026. **Research status:** mathematical identities derived, exact finite-field executable implementation and independent regression/audit. This is a fresh-input **structured transform** result, not the universal exact `O(N)` FFT and not a new integer-multiplication upper bound.

## Executive findings

1. **Coupled q-Gaussian spectral jets:** the `2N` evaluations of `sum_t t^j h_t z^t` for every `0<=j<=d` are computed in `O(N(d+1)^2)` exact field operations; the ordinary `N`-point DFT needs only the relevant parity cycles.
2. **Blind shifted Jordan–Prony recognizer:** from a fresh raw vector, divide by the known nonzero kernel `h`, infer up to `R` total exponential-polynomial modes via Berlekamp–Massey, enumerate root-grid factors, solve a confluent Vandermonde system, and check **every raw sample**. No mode coordinates are supplied. Once accepted, compute all outputs in `O(N R²+R³)` field arithmetic. For fixed `R`, this is `O(N)`.
3. **Dense q-defects can be easy:** `x_t=t h_t` has `N-1` nonzero Phase 21 defects but Jordan order 2. The old sparse-defect algorithm must use fallback; the new algorithm does not.
4. **Piecewise union:** bounded numbers of pieces with different local spectral modes are handled by exact two-endpoint spectral recurrences and blind segmentation. It includes piecewise-constant normalized coefficients (the Phase 21 sparse q-defects) and dense polynomial/exponential innovations.
5. **Ordinary `N`-point DFT output support:** the new parity-selective evaluator computes *only* the N required bins, avoiding the extraneous half-grid of the Phase 21 zero-padded spectral task.
6. **Boundary of applicability:** bounded Jordan/Hankel order does not cover generic vectors. A finite-union-of-subspaces count quantifies this. Any universal fast algorithm must handle growing rank without proportional work.

## What exactly is new to the project?

Phase 21 treated a fixed reciprocal Gaussian kernel and sparse coefficient defects. Phase 22 removes **defect sparsity** and replaces it by **bounded exponential-polynomial rank in the normalized coefficients**. This can be highly oscillatory and have a defect at every time index. Derivative jets, blind Prony roots, and interval endpoint corrections are fused into one operation-charged executor. It produces a genuine larger family of supported signals. Historic priority is not established: each ingredient belongs to established q-holonomic, Prony and Fourier methods.

## Key mathematical equations

Let `eta` be primitive of order `2N`, `q=eta^8`, and `h_t=eta^(2t²)/prod_{j<=t}(1-q^j)`.

Define `Y_j(k)=sum_{t<N} t^j h_t eta^(kt)`. Then

`Y_j(k+8) = Y_j(k) - eta^(k+2)*sum_{l<=j}binom(j,l)*Y_l(k+4) + eta^(Nk-2)*h_(N-1)*N^j`.

For an interval `[a,b)`, the two-boundary variant is

`Y_[a,b),j(k+8) = Y_[a,b),j(k) - eta^(k+2)*sum_{l<=j}binom(j,l)*Y_[a,b),l(k+4) - (1-q^a)h_a*a^j*eta^(ka) + eta^(4b-2)h_(b-1)*b^j*eta^(kb)`.

If `x_t=h_t sum_i P_i(t) eta^(m_i*t)` and `R=sum_i(deg(P_i)+1)` is fixed, then

`F_(2N)(x,0)(k)=sum_i sum_j P_i[j] Y_j(k+m_i)`.

For the actual ordinary length-N DFT, `F_N(x)(k)=F_(2N)(x,0)(2k)`, and each mode requires only one of the two parity orbits. For fixed R, both the recognition and the transform cost `O(N)` scalar field operations. The fully charged proof and field model are in `PROOF_CERTIFICATE.md`.

## Correctness verification

- 42/42 new regression test groups (22 general Jordan, 10 piecewise, 10 parity-selective).
- 18/18 Phase 21 inherited regression tests.
- 295,164 checked `2N` spectral outputs in the medium-length independent audit; 1,134 also matched direct full quadratic evaluation, plus 793 independently summed rows.
- 450 random dense raw inputs and 60 adversarial prefix-spoof inputs rejected from the fast path; wrong-grid geometric frequencies also rejected.
- `N=177147`: full 354,294-bin padded Fourier vector compared against two distinct conventional implementation codepaths, plus direct sampled summations.
- All 24 ordinary N-point comparison cases (3 structures times 8 lengths through N=177147) matched an ordinary N-point NTT, with independently summed bins.

All comparisons are exact modulo primes. Floating-point stability and bit complexity are not audited.

## Fully charged counts — two different workloads

### A. `2N`-output, zero-padded transform

This is a *valid same-task comparison only when all `2N` padded Fourier values are requested.* Fresh prepared q-kernel, recognition, final output, and scalar field arithmetic are counted on both sides.

| Original input length N | Jordan degree-one padded transform | Conventional length-2N NTT | Ratio generic/Jordan |
|---:|---:|---:|---:|
| 19,683 | 1,358,211 | 1,279,461 | 0.942 |
| 59,049 | **4,074,473** | 4,231,919 | **1.039** |
| 177,147 | **12,223,249** | 13,876,603 | **1.135** |

The first tested arithmetic crossover was at N=59,049. This is **for a structured input with N-1 nonzero q-defects**, not an algorithmic upper bound for unrelated dense inputs. Both complete vectors matched the independent conventional NTT. These are operation ledgers, not hardware timings.

### B. Actual `N`-output DFT (fairer for the original FFT goal)

Using parity-selective recurrences and an ordinary length-N NTT baseline, no tested finite-size crossover was found:

| N | Parity-selective Jordan degree-one | Ordinary N-point NTT |
|---:|---:|---:|
| 6,561 | 295,345 | **181,578** |
| 59,049 | 2,657,323 | **2,027,424** |
| 177,147 | 7,971,747 | **6,672,626** |

For fixed structural order the new method stays asymptotically `O(N)` whereas the chosen classical NTT is `O(NlogN)`. That does **not** make it a new worst-case FFT algorithm, nor does it guarantee a performance win at any particular finite input length or over optimized FFT libraries.

## Technical implementation and exact fallback

- `phase22.py` includes the q-Gaussian preparation, root validation, jet and interval-jet recurrences, parity-selective N-output mode, raw-input blind Jordan/Prony recognition, a piecewise segmented recognizer, independently counted arithmetic, and conventional radix 2/3 NTT fallback.
- `test_phase22.py`, `test_piecewise.py`, `test_parity.py` independently cover algebraic identities, raw recognition, exact output, root multiplicity, anti-spoof fallback, and recurrence stitching.
- `independent_audit.py` compares the new implementation to the *previous phase's independently authored mixed NTT* and sampled quadratic direct sums.
- `large_crossover.py` verifies complete large padded DFTs and all field-op counts; `n_point_comparison.py` compares the correct **N-output** task.
- At arbitrary odd `N` with a large unfactored radix, this specific demonstration's generic fallback can be quadratic. The smooth cases `N=3^m` used for the asymptotic cost comparisons have radix-3 `O(NlogN)` fallback. A production all-length fallback would use a general mature NTT/FFT method with its own model accounting.

## Research limitations and research priorities

The speedup is caused by a short **recurrence** in the normalized coefficients, not by a universal property of random input FFT subtrees. Generic vectors have high quotient Hankel rank; the representation is not universal at fixed R. Reusing cached root tables across multiple calls is allowed only when explicitly charged as shared preparation; the finite-size crossover tables use fresh plans for every case. The field-operation ledger does not represent integer indexing costs, machine-word bit complexity, exact complex coefficient representation, or numerical conditioning.

There is strong prior art for q-holonomic evaluation, polynomial-exponential Prony recognition and Hankel structure. Related literature includes Garoufalidis & Koutschan (2012) https://arxiv.org/abs/1201.3353; Bostan & Yurkevich (2020/2022) https://arxiv.org/abs/2012.08656; and classical generalized Prony algorithms. Historical novelty of this specialization requires dedicated review.

A truly **universal** breakthrough would need an input-independent shared executor for growing normalized Hankel rank `R(N)` that avoids `Omega(RN)`-style explicit jet emission, with proof that the *complete input-to-output arithmetic circuit* on arbitrary vectors is cheaper than the comparator. The current externally published exact-complex benchmark is the 2026 OpenAI Math #130 algorithm with `O(N(log N)^(1-10^-13))`, under its precise arithmetic assumptions: https://github.com/openai/math/blob/main/lean/docs/130.md.

## Next checkpoint — Phase 23

Investigate the exponential-generating-function jet bundle `J_(k+8)(z)=J_k(z)-eta^(k+2)exp(z)J_(k+4)(z)+boundary`, with exact truncated polynomial multiplication, and ask whether a **single joint decoder** of an unbounded jet order can avoid explicitly materializing `R*N` intermediate jets. Also test nonseparable rank compression of the dense q-defect forcing across both parity cycles. Stop immediately if the proposed gain hides a conventional FFT or a generic convolution.

### Additional independent N-point verification

`n_reference_check.py` reruns 12 complete ordinary N-point transforms, totaling **729,000** entries when summing the four tested lengths with three cases each, against the separately implemented Phase21 zero-padded NTT's even frequency bins; each run also checks 29–32 directly summed rows. This stronger independent check supplements the conventional same-length NTT in `n_point_comparison.py`.
