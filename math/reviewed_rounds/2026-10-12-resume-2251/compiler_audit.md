# Fourier compiler priority audit

12 October 2026. Repository snapshot: AgentSlop-Si/research at 95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d. Read-only audit; no live table or repository changes.

## Recommendation

Treat ALG-022/F096 plus the borrowed-register compiler as an accepted exact-arithmetic construction with an implementation-comparison opportunity, not an open route to a newly established FFT exponent. The imported tensor engine is a proved theorem dependency in the accepted source review, not a missing conjecture. The genuinely open, bounded question is whether the one-bank implementation improves a clearly specified resource ledger over the already available two-bank implementation.

The strongest inspected OpenAI formal source already has an exact-width O(log² r) compiler. Consequently the claimed O(N(log N)^(1-a)(log log N)^(1+a)) transfer is mathematically supported but is also obtainable from that prior compiler and the written transfer. Repeating its proof or finite Fourier tests has low information value. A publication could present a carefully credited one-bank construction, normalized constant/space comparison, and reproducible implementation if those remaining claims are established. It should not claim a new local asymptotic exponent, a new tensor saving, or first sub-N log N DFT.

## What is established

### Classical factorization and its separate kernel gate

The original F096 source explicitly gives the positive, unnormalized factorization F=S T diag(d) Tᵀ S, with f_j=∏_(s=1)^j(1-q^s), T_ij=[i≥j]/f_(i-j), and d_j=(-1)^j q^(j(j-1)/2)/f_j. The source credits the known q-binomial/Vandermonde identity and does not claim it as new. Its bytes were re-fetched and verified against SHA-256 bc62a95e8677464a5ecc682f5afc9a62f329a5e08c218e86f1782986b1998ab0. [1]

Its own online cost is 2C(N)+O(N), where C(N) is a fresh-input triangular convolution application, plus charged preparation. The one-term coefficient recurrence does not give a constant-state input filter or a linear-time application oracle. The full-rank Hankel obstruction rules out the stated short-state streaming model, not arbitrary random-access speedups. These accepted statements do not close the different q-exponential tail or sparse-forcing branches. [1,2]

### One-bank local construction

For every r≥1 and specified primitive rth root, the accepted construction computes the full positive unnormalized Fourier matrix on arbitrary complex data using exactly r data coordinates and O(1+log²r) disjoint shear/monomial layers. Polynomial coefficient/schedule preparation uses rational operations on supplied roots and their inverses. Prepared conjugates are computed by a shared scalar DAG; data entries are not conjugated. [2,3]

The key primitive regularizes a circular convolution K by A=K+αI, α=1+∑|λ_j|². The nine-step borrowed-bank word cancels arbitrary initial scratch and the αI term. Since α>|λ_j|, every λ_j+α is nonzero. A rectangular product chunk uses a+2e+q coordinates, with q the least power of two at least max(2e−1,a+e−1). Constant-fraction chunking, restored intermediate registers and parallel recursive children yield quadratic logarithmic depth. Exactly r counts data coordinates, not scalar-table storage, schedule storage or the copying Python interpreter. [2,3]

The archived F096 contract is dyadic over suitable fields; this compiler contract is all positive local lengths over the complex numbers with additional supplied roots. Finite-field tests use a different nonzero-shift selection, so they do not prove a finite-field analogue of the complex norm regularizer. [2]

### Charged global transfer

For one fixed fully charged C-tensor engine of cost O(2^k(k+1)^θ), θ=1−a<1, the synchronized small-axis transform has cost O(R(ℓ+1)^θ(1+log r_max)²), plus polynomial local preparation. Sector adapters and tensor monomials cost O(R), all sectors together contain R entries, and the engine permits arbitrary data in its auxiliary roles. [3]

The written prime-product/CRT/Bluestein construction has ℓ=Θ(log N/log log N), log r_max=O(log log N), and a working transform length 2N≤L<4N. Hence Nℓ^θ(log ℓ)² becomes O(N(log N)^θ(log log N)^(2−θ)), or O(N(log N)^(1−a)(log log N)^(1+a)). There are three charged working transforms including the fixed convolution kernel. This is a valid theorem-level implication, not evidence of a working end-to-end fast implementation. [3]

The root contract supplies one specified root of order D*=(2N)L·2^ceil(log₂(16L))<1024N³. It is stronger than receiving only an Nth root. The model is unrestricted exact complex arithmetic with logarithmic-size integer indices; no bit-complexity, numerical stability, bounded-coefficient or measured-speed conclusion follows. [2,3]

## Decisive prior source check

I re-fetched the primary OpenAI source at fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb:

- FourierWords.lean has Git blob 50e57b23f72e6c830ead098e80776d70e02db646. Its sound_ballad, creates_ballad and score_le give exact width, all-input correctness and score(e)≤20,000,000(e+1)²+7 for r≤2^e. [4]
- LocalCompiler.publish supplies the prepared word; the accepted composition audit traces Engrave→Makes→PolyCan→Can to one polynomially bounded preparation program. [3,5]
- CirculantUpdates.eddy already transforms two arbitrary banks, makes the spectral accumulation and inversely transforms them; spill_eddy proves restoration. ToeplitzUpdates.duct and well nest commutators; MeasuredFit supplies the chunked product mechanism. I re-fetched these source bodies. [6]

The local manuscript’s O(log⁴r) construction is a weaker comparator than this same corpus’s formal O(log²r) compiler. The sharper log-log expression is an inference from the prior quadratic local theorem and written transfer, not a claim that the earlier formal all-length theorem literally displays it. The audit’s prior chronology identifies the introducing commit as 301488868beec11bfd897168433b0a64f5258559 on 8 October 2026. [3,4]

OpenAI’s current scope page separately reports an all-length exact O(n(log n)^(1−10^-13)) result, with supplied roots and unrestricted coefficients. I opened this page during this audit. It does not confer numerical or bit-cost guarantees. [7]

The Sussman pinned Seam.lean was also re-fetched: hillsE8_program explicitly uses the kernel saving 8762479/10^10. The slightly weaker all-length pure-log headline saving 8762478/10^10 is a different constant. Neither is a new saving discovered by the borrowed-register compiler. Compatibility with the particular fixed C is established in the accepted composition audit; I did not rebuild Lean or re-audit the finite-certificate dependency graph. [3,8]

## Evidence and remaining verification limits

The accepted prior check report records 181 local Fourier basis columns over 17 prime-field lengths, recursive exact Q(i) Toeplitz checks, 85 synchronized Fourier columns, 20 dirty-role interference columns and seven detected negative controls. The complete source review accepts the local construction and global implication. These historical executions were not rerun in this audit. [9]

The authored 455 modular and ten characteristic-zero positive cases were not independently rerun at the previous checkpoint either. The independent synchronization tests used ordinary C-tensor butterflies, not the fast imported engine. No full CRT/Bluestein backend was executed and Lean was not rebuilt. These execution limits do not turn the accepted mathematical engine dependency into an open conjecture. [3,9]

The repository checkpoint deliberately publishes documentation and results, but omits the executable source and original run logs. Hashes preserve evidence identity; they do not make the packet publicly rerunnable. The publication/implementation gate therefore includes delivering an actual replayable compiler and verifier, not simply another result table. [9,10]

## One executable next check

**Produce a model-matched one-bank versus two-bank resource comparison.** Freeze the exact candidate and pinned prior algorithms, then emit both into one strict shear/monomial instruction representation, using the same radix-two primitive and one final global mixed-layer normalization.

The check should:

1. Count data width, generalized/strict layers, scalar additions/multiplications/inversions, index/routing/copy work, and prepared scalar/schedule storage separately. Include scalar-DAG conjugate caching and all preparation.
2. Compare identical rectangular accumulation shapes and full local Fourier lengths, including 15/16/17 and 31/32/33 to exercise base-case and chunk boundaries. Use full basis and arbitrary-dirty-bank restoration checks over exact characteristic-zero cyclotomic arithmetic for the complex algorithm, plus negative controls.
3. Preserve each algorithm’s actual chunk rule and also separate primitive-level comparisons at the same q from whole-compiler comparisons. Both banks’ transforms can be parallelized when disjoint; layer savings are not automatically sequential-work savings. Do not compare the candidate’s layer count directly with the prior’s differently defined beat count.
4. Extract explicit recurrences from these emitters and prove the resulting bounds under the same ledger. A lower local borrowed-width constant is already visible; a total-work or total-preparation improvement is not yet established.

Stop with either a certified, precisely scoped resource advantage and runnable artifacts, or a documented tradeoff/no advantage. This bounded check is more informative than another identity test and does not require implementing the enormous fast tensor engine. A positive result could support an implementation/theory note, but historical originality of the one-bank primitive still needs a separate comparison with the prior in-place accumulation literature. [2,3,6,9]

For ranking: information gain 4/5, tractability 3/5, defensible novelty opportunity 1/5, impact 2/5, evidence readiness 4/5. Weighted 25/25/20/15/15: 2.85/5. These are task-priority judgments, not correctness or breakthrough probabilities.

## Related growing tensor proposal

The live GTSL row correctly remains open: no all-input growing tensor-union compiler is established. Its recurrence conclusions are conditional on a realized, uniformly charged saving. Mere convergence ρ(w)→1/2 is insufficient for O(N log log N); the accepted correction requires a sufficient rate or an appropriate envelope condition. The next gate there is an explicit fused all-input DAG with a scale-uniform resource saving, not further manipulation of the already audited recurrence. This is distinct from the accepted fixed-engine borrowed-compiler transfer above. [11]

## Sources

[1] [Original F096 source](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/archive/objects/bc/bc62a95e8677464a5ecc682f5afc9a62f329a5e08c218e86f1782986b1998ab0__059_bc62a95e8677464a.inert.txt).

[2] [Source binding](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-borrowed-compiler-audit/SOURCE_BINDING.md) and [corrected audit](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-borrowed-compiler-audit/AUDIT.md).

[3] [Composition and prior-source review](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-borrowed-compiler-audit/COMPOSITION_AND_PRIOR_REVIEW.md). The proof reading copy in the same directory was inspected; its sections 1–5 preserve the mathematical construction and its opening correction supersedes the old comparison.

[4] [OpenAI FourierWords.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/FourierWords.lean#L101-L119).

[5] [OpenAI LocalCompiler.publish](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/LocalCompiler.lean#L113-L138).

[6] [OpenAI CirculantUpdates.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/CirculantUpdates.lean), [ToeplitzUpdates.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/ToeplitzUpdates.lean), [MeasuredFit.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/MeasuredFit.lean).

[7] [OpenAI exact Fourier formalization scope](https://github.com/openai/math/blob/main/lean/docs/130.md), accessed 12 October 2026.

[8] [Sussman Seam.lean](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/Work/FourierE8/Seam.lean#L186-L204), fetched blob 8907b4c04af9b5d7df6db728759d968b50db4804.

[9] [Fresh bounded-check report](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-borrowed-compiler-audit/checks/REPORT.md).

[10] [Publication and reproducibility limits](https://github.com/AgentSlop-Si/research/blob/95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d/math/reviewed_rounds/2026-10-12-borrowed-compiler-audit/README.md).

[11] Live table snapshot: Incoming queue row 38 (GTSL), row 42 (borrowed compiler), Catalogue row 122 (ALG-022); read-only capture in live_full_values.json. [Master research table](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit).
