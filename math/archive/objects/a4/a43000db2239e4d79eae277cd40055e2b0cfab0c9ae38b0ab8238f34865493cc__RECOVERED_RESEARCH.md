# Recovered branches beyond the earlier research map

The Library recovery exposed substantive earlier branches that the 14:04 synthesis did not fully represent. The statements below are grounded in source-text review. Historical source tests and benchmarks were not rerun as part of this inventory. The separate current phase14, nonlinear-network and Boolean audits identify their own independently checked claims.

No recovered branch establishes a new independent exact arbitrary-input FFT or general integer-multiplication improvement. The positive results concern explicit restricted operators, input classes, approximation contracts or related-input workloads.

## 1. Boolean-only computation is a separate target

A finite Boolean cube does not contain an open continuous-input set. Continuous-domain rank or differentiation arguments therefore cannot exclude all Boolean-only nonlinear circuits.

The recovered spectral-completion paper proves that no degree-at-most-two complex polynomial of a proper subset of Fourier bins produces an omitted bin on every Boolean input. It supplies finite degree-three non-completion certificates when a conjugate pair is omitted at N=8,16,32. A positive cubic N8 formula exists when seven bins are already known, but costs more than simpler recovery and provides no FFT saving. Even-frequency measurements alone leave 2^(N/2) Boolean inputs indistinguishable.

A separate midpoint identity converts any total-degree-at-most-two Boolean-correct polynomial circuit into a general linear evaluator with two evaluations. Higher-degree, rational, semilinear and direct-input nonlinear algorithms are not covered by those exclusions.

Sources: [spectral completion](canonical_sources/8b25ef43c7ee33d9__RESEARCH.md), [degree boundary](canonical_sources/282f1c330f664e66__RESEARCH.md), [conductor measurements and one-scalar recovery](canonical_sources/dddb9e4c155cc7f3__RESEARCH.md).

## 2. Noncommuting filters can recognize a larger structured family

Ordered affine-cycle filters can jointly produce a sparse final defect even when each constituent rejects the same dense input. Shared parameter preparation and exact closure give the stated field-operation ledger (1+r+6d+2s)N+r(log2N+2)+d for a supplied invertible chain with s final defects.

This is not universal coverage: the specified rational family has dimension at most r+s, so fixed r+s<N cannot cover generic complex inputs. Discovering parameters, handling singular factors and evaluating all corrections remain separate obligations. The witness compares its chosen constituent filters, not every possible single filter.

Sources: [ordered fusion](canonical_sources/837c563f27047531__README.md), [independent source review](canonical_sources/0d838ebbcc7268a3__INDEPENDENT_REVIEW.md), [coverage and correction gate](canonical_sources/9b6d9bfeedec91ed__FUSION_GATE.md).

## 3. Sparse nonminimal annihilators improve some exact decoders

Minimum polynomial degree is not the same as cheapest recurrence. A higher-degree annihilator multiple can have far fewer nonzero taps. The source's N4096 example has a dense degree16 minimal denominator but a two-tap degree32 multiple. After paid discovery and prefix computation, a sparse-tap recurrence can emit every output in linear work for fixed tap count.

This improves a certified support class, not all supports. The input interface supplies modal roots and amplitudes; extracting them from another representation is additional work. Reported operation comparisons are historical source results. The old independent review names a different README hash, so its hash binding should not be silently transferred to the final text.

Sources: [annihilator-multiple decoder](canonical_sources/f1b1856375df9240__README.md), [source review](canonical_sources/0df64bd669a94b81__INDEPENDENT_REVIEW.md).

## 4. Input side information supports further exact paths

A fresh binary-index tensor input can be certified by a pivot, bit-neighbor ratios and complete regeneration. Shared suffix products then produce all Fourier values in O(N) field work. This family has only O(logN) parameters, and failed certification must retain a paid general fallback.

Other recovered work extends recurrence recovery to zero and singular shifts, Galois-defect hybrids, rank-one orbit fusion, multiple-port feedback, coupling edits and exact multi-parent product reuse. Each has its own recognized-input or supplied-operator contract. They should not be compressed into a claim that all fresh dense vectors are structured.

Sources: [tensor certificate and full evaluator](canonical_sources/a5bbf86f5f9382be__README.md), [direct recurrence including singular shifts](canonical_sources/5a1a90472e166176__README.md), [multi-port feedback](canonical_sources/322f0d1a5a76019f__README.md), [multi-parent products](canonical_sources/e8282dc5a3f8faa9__README.md).

## 5. Exact integer products have useful structured cases

Repdigit baselines plus exceptions, constant runs and sparse digits admit verified exact products with signed corrections and complete carrying. Fixed structural complexity gives linear digit work, without an approximate FFT. Unstructured inputs explicitly decline to a general backend.

A separate arbitrary-length backend uses the composite-capable ring modulo 2^t+1 and principal roots, avoiding prime search and CRT. Its straightforward bit cost and storage are large; it is an exact correctness backend rather than an asymptotic multiplication improvement. A graph's scalar-operation optimum is not automatically its bit-cost optimum.

Sources: [structured integer recovery](canonical_sources/5618cf3cc85e3f2b__README.md), [prime-free backend](canonical_sources/33cb0a98b2111c2d__README.md).

## 6. Approximation cannot be promoted to integer recovery for free

The recovered convolution-rounding ledger separately charges forward-transform errors, product error, inverse error and final rounding. Under that particular L1-scaled certificate, every nonempty integer residual tail forces the current sampler into its exact-input bypass. A k-sparse surrogate also reduces a two-sparse-column filter's defect count by at most 2k.

These are exclusions of specific bridges. They do not prohibit correlated-error designs, modular arithmetic, new refinement decoders or every exact integer algorithm.

Sources: [exact-recovery review](canonical_sources/20a1b09d49db1f52__INDEPENDENT_REVIEW.md), [fusion gate](canonical_sources/9b6d9bfeedec91ed__FUSION_GATE.md).

## 7. Strong error requires nearly full rank for input-independent linear sketches

Let U be unitary. If the law of the random linear estimator A is independent of x, and each fixed input succeeds with probability at least 1−delta at maximum-coordinate error epsilon||x||1/sqrt(N), then E rank(A)≥N(1−delta)(1−epsilon²). A deterministic rank cap obeys the same bound. The argument also reaches all-coordinate-nonzero inputs by limits.

This is a representation restriction, not a time lower bound. Input dependence and nonlinearity matter: v4 importance sampling depends on the input, and v6 median decoding is nonlinear, so neither is excluded by this theorem.

See the strong-scale and rank-barrier sources under the [source index](SOURCE_INDEX.md).

## 8. Chirp sketches have exact decoders and exact collision obstructions

For N=KM and K≤M, the natural affine-slope chirp sketch has an O(N log(2K)) exact full-output decoder with O(M+K) additional storage. Nonunit slopes require folded gcd-orbit filters; arbitrary quadratic coefficients require period reduction. Only the common-slope case retains the better O(N+K logK) factorization. This decodes the sketch, not the original DFT.

For M divisible by 4 and even K, a particular Mth-root quadratic sketch with arbitrary integer-polynomial block slopes has two fixed fully dense equal-magnitude inputs with identical sketches on a half-probability event. Any decoder using only those sketches, even nonlinear/randomized, must fail one fixed input with probability at least 1/4 at the stated strong scale. Changing to 2Mth-root CAZAC phases repairs that collision but not the separate failure of the natural adjoint decoder. These are precise architecture-specific exclusions.

Sources: [affine-chirp decoder](canonical_sources/958a37ab8f0db835__DECODER.md), [repetition](canonical_sources/0554f98e8eb0cdca__REPETITION.md), [resonance](canonical_sources/504e7f01540b55df__AFFINE_RESONANCE.md); additional structured-phase proofs are indexed in SOURCE_INDEX.md.

## 9. Deterministic energy pruning is an approximation branch

An adaptive ideal-arithmetic DIF traversal returns the exact hard-thresholded normalized spectrum at threshold epsilon||x||2. It costs O(N[1+min(logN,log(epsilon^−2))]) with norm scans, comparisons and dense output charged. The returned coefficients above threshold are exact in that model; discarded coefficients make the overall transform approximate.

This coarse maximum-coordinate scale can legitimately return all zeros on diffuse spectra. Converting to the stronger epsilon||x||1/sqrt(N) scale can restore FFT-sized work. The floating prototype has no certified rounding guarantee, and its historical timings do not establish a native-library speedup.

Sources: [all-size pruning proof](canonical_sources/aba79ba13dfbd987__PROOF.md), [implementation scope](canonical_sources/89c6226655a82738__IMPLEMENTATION.md).

## 10. Sparse-surrogate refinements need their corrections retained

Importance sampling plus a sparse-input full-output transform gives an input-adaptive approximate theorem; exact retained heads can reduce residual mass. The recovered corrections matter: use relative rather than arbitrarily rescalable absolute decay assumptions, charge a single-selection planner rather than repeated whole-input selection, bind plans to the actual input/tolerance, and distinguish sample count from coalesced support. A vanishing error multiplier need not mean vanishing absolute error.

Signed or complex sparse surrogate weights do not remove the source's representation-specific support barriers. These barriers do not establish a general approximate-FFT lower bound.

Sources: [v1 research](canonical_sources/917aeb770759da19__SPARSE_SURROGATE_RESEARCH.md), [v2 research](canonical_sources/172809eb3dfc0558__SPARSE_SURROGATE_V2_RESEARCH.md), [focused corrections](canonical_sources/f023fcf6bd1d270a__DELTA_REVIEW.md).

## 11. q-kernel identities are reusable algebra, not automatic speedups

Finite-root q-kernel preparation, orbit compression, cycle-flow corrections, sparse grading, tail aggregation and rational-degree restrictions form a substantial exact branch. A complete phase orbit really compresses to shorter residue-chain actions. A median minimizes the signed first-order correction passes within the specified cycle-flow rewrite family.

The Fourier factorization does not automatically contain that favorable word. Changed child actions, finite boundary terms, dense corrections and final evaluation still need charging. A three-child decimation can already be asymptotically worse than FFT. High cut rank alone is not a runtime lower bound, but a compact representation alone is not a fast evaluator either.

Sources: [cycle-flow compiler](canonical_sources/790aea73dfd7d6f1__README.md), [orbit identity](canonical_sources/e0b4fdd1981b6366__README.md), [finite branch-fusion obstruction](canonical_sources/81253748166701a9__README.md), [noncommuting q-Weyl tails](canonical_sources/d866c38fb26c76d9__README.md).

## 12. Conditional stability and practical reuse remain separate

The constructive conditioning branch assumes an existing exact sub-NlogN local primitive and a certified coefficient/printer model. Transparent replay and serial full-state unitary resets then permit an explicit slowly growing radix and condition budget. This is a conditional composition theorem in an expanded state/conditioning model, not an independently discovered faster FFT.

The cache-rewrite branch proves valid commutative-ring identities and can expose useful internal cached products. Its floating implementation can change cancellation error, still pays ordinary input/output FFTs, and reports both wins and losses. Repeated or correlated workloads cannot establish arbitrary fresh-input complexity.

Sources: [conditioning certificate](canonical_sources/c07cf114f2827288__PROVED_CONDITIONING_TRADEOFF.md), [cache-directed rewrite](canonical_sources/3f93cd7a20516fca__RESEARCH.md), [complete historical benchmark table](canonical_sources/9783c98c4118c587__BENCHMARKS.md).

## Integration rule

The right combined objective is a complete evaluator in a fixed model. A proposed fusion must preserve the input domain, exactness/error contract, scalar representation, parameter discovery, coefficient preparation, state restoration, corrections and full output cost of every component. A theorem may remove one bottleneck while leaving another unchanged. The recovered positive controls and scoped vetoes are useful precisely when these interfaces remain explicit.
