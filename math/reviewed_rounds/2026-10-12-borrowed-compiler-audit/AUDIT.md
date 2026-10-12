# Borrowed Fourier compiler audit

Review snapshot 12 October 2026 at 20:10 UTC | Manuscript dated 13 October 2026

**Conclusion.** The supplied construction supports an exact-width, all-input O(1 + log² r) Fourier layer theorem. The same asymptotic bound and a two-bank route already appear in OpenAI’s formalization introduced on 8 October 2026. The earlier comparison against only the written O(log⁴ r) compiler was incomplete. The supported output is an explicit one-bank construction and local prototype; historical originality remains unestablished. Fresh independent bounded compiler and synchronization checks now pass. The candidate’s own recorded suite and the fast global engine were not run.

## Exact theorem and model

For every integer r ≥ 1 and the specified primitive rth root u, the compiler computes the full positive, unnormalized Fourier matrix Fᵣ(u) = (uⁱʲ) on arbitrary complex inputs. Its emitted circuit addresses exactly r data coordinates and has O(1 + log² r) layers of disjoint shears and invertible monomial maps. Every borrowed coordinate may begin arbitrarily and is restored after the operation that borrows it.

This is exact complex arithmetic with unrestricted scalar magnitudes and unit-cost operations on logarithmic-size indices; preparation and data movement are charged. Polynomial scalar and schedule preparation uses rational operations on u, suitable supplied power-of-two roots and their inverses. Prepared coefficient conjugates are obtained by evaluating shared arithmetic programs at inverse roots; input-vector entries are never conjugated. Arbitrary externally supplied Toeplitz coefficients would require their conjugates too, or a separately allowed nonuniform shift.

Exactly r refers to data registers in the abstract word. Prepared scalars, schedules and indices are separate resources. The Python evaluator copies its input list, so it is not a literal constant-extra-data-space implementation. There is no floating-point stability, bit-complexity or practical speed theorem.

## Why the local proof works

The one-bank primitive regularizes a circulant K with A = K + αI, where α = 1 + Σⱼ|λⱼ|² and λ are its Fourier eigenvalues. Since α > |λⱼ|, A is invertible even when K is singular. A reversible nine-step update cancels the arbitrary scratch value and the added αI contribution, leaving y ← y + Tx.

For an a-by-e chunk and q the least power of two at least max(2e−1, a+e−1), the product update uses a + 2e + q coordinates. With b = floor(v/8) and a,e ≤ b, this is less than 7b ≤ v. At most 36 chunk pairs, each with three displacement products, cost O(log v) layers. Parallel children give d(v) ≤ max d(child) + O(1 + log v), hence quadratic logarithmic depth. Mixed disjoint layers must be split into shear and monomial layers once globally, adding at most a factor two.

## Prior result and contribution boundary

**The formal prior changes the comparison.** OpenAI’s FourierWords.lean contains exact-width soundness, correctness for every input and a bound of 20,000,000(e+1)² + 7 beats, with r ≤ 2ᵉ. Taking e = ceil(log₂ r) gives O(log² r). LocalCompiler and ToeplitzCompiler supply the polynomial preparation interface. The relevant formalization was introduced in the verified 8 October 2026 commit and is present in the pinned comparison revision. [1, 2, 4]

A beat consists of a scaled gather and disjoint fixed two-coordinate kernel pairs. Exact-width soundness prevents access to outside data. On the finite r-dimensional space, the final Fourier map is invertible, forcing every factor to be invertible; the scaled gathers are therefore nonzero monomials. Each kernel pair has a constant-size shear/monomial decomposition. Thus the quadratic bound applies to the same asymptotic layer model. This interface was inspected as source; Lean was not rebuilt.

OpenAI’s written local section separately states O(log⁴ r). That statement is a valid but weaker displayed upper bound, and cannot represent the strongest inspected prior compiler. The candidate therefore does not establish a new asymptotic local bound, a first sub-N log N transform, or a better tensor saving exponent.

## One bank and the existing two bank route

The inspected formal construction already has a two-bank FFT circulant accumulator: transform both arbitrary banks, apply the spectral shear, then invert both transforms. Zero eigenvalues are harmless. Its nested Toeplitz and product commutators restore arbitrary contents, and its constant-size chunking yields quadratic logarithmic depth. The two-bank construction independently derived during this review must be credited as a rediscovery of that existing mechanism. [3]

The candidate’s stated distinction is its regularized one-bank primitive. In the review’s corresponding chunk implementation, one bank uses a + 2e + q registers, while two banks use a + 2e + 2q. Choosing smaller constant-fraction chunks makes either fit in the original width. The one-bank economy changes a constant in borrowed width; no superiority in total constants or runtime has been proved. This focused comparison does not establish historical originality of the primitive.

## Factorization and dependency credits

The Newton/Vandermonde identity Fᵣ = D_H T diag(pⱼ/Hⱼ) Tᵀ D_H, with Hⱼ = ∏ₛ₌₁ʲ(1−uˢ), pⱼ = (−1)ʲuʲ⁽ʲ⁻¹⁾ᐟ² and Tᵢⱼ = [i≥j]/Hᵢ₋ⱼ, is reused. It is identical to the archived ALG-022/F096 identity under symbol substitution, with the same positive sign, no normalization and ordinary transpose. The archived package states dyadic lengths over suitable fields; the new theorem states all positive lengths over ℂ with extra supplied roots. The contracts are not identical. [5, 7]

Credit the prior framework for the factorization, parallel-child scaffold, cross matrix, displacement identities, fixed-kernel conversion, synchronization and all-length reduction. Dumas–Grenet provide earlier in-place accumulation and Toeplitz/displacement primitives. Those work bounds alone should not be relabeled as this exact layer theorem. [5, 6]

## Global implication and its limits

Fix a valid, fully charged engine for the kth tensor power of C = ½[[1+i,1−i],[1−i,1+i]], costing O(2ᵏ(k+1)ᶿ), where 0 < θ = 1−ε < 1. The quadratic local compiler and the published synchronization, CRT and Bluestein reduction give

T(N) = O(N(log N)^(1−ε)(log log N)^(1+ε)) = o(N log N).

The transfer audit found compatible interfaces: arbitrary values in borrowed roles, charged preparation, initialization, indexing, data movement and the fixed convolution-kernel transform. Synchronizing complete words remains valid even when different axes alter each other’s temporary coordinates. The imported tensor engine is an existing written theorem dependency, not an unfilled task. The global algorithm may use extra arrays; exact width is a local circuit guarantee. [5]

The root model supplies one specified root of order D* = (2N)L·2^ceil(log₂(16L)) < 1024N³, with 2N ≤ L < 4N. An ordinary supplied Nth root alone is insufficient for the stated construction. The same quadratic local bound already available in the formal prior supports the same transfer substitution; the candidate does not establish a fresh two-power log-log improvement over that complete prior framework. This is an inference from the prior local theorem and written reduction, not a claim that the formal all-length source literally states this sharper expression.

## What was checked and what was not run

**Fresh independent checks passed.** Separately written exact calculations covered 50 characteristic-zero accumulations, 16 nested products, 148 FFT-vector/inverse cases, 45 full Fourier-factorization matrices, 2,652 rectangular displacement chunks and 39,940 width inequalities. Additional checks covered 48 two-bank identities, 100 synchronization-sector instances and an independently derived recurrence matching all 18 stored metric rows. These finite tests support the algebra and bookkeeping; they do not prove the all-length theorem.

**Fresh complete local reproduction passed.** A separately written compiler passed 181 full Fourier basis columns over verified prime fields across 17 lengths, with inverse and strict-layer checks for every basis. Exact Q(i) tests covered recursive width-16 Toeplitz using the actual norm regularizer. Fixed-C conversion and sector adapters passed 85 synchronized Fourier basis columns across (2,3), (3,5), (2,3,5) and (2,17), plus 20 borrowed-role interference columns. Seven negative controls were detected. Finite basis equality certifies every input at the tested sizes and fields, not all lengths or arbitrary complex coefficients.

**The package’s recorded 465 positive and 6 negative cases were not rerun.** The 465 comprise 455 modular and 10 characteristic-zero cases. Static review verified source-hash binding and agreement of attached and bundled manuscript content, although their PDF bytes differ. Its modular regularizer uses a shift avoiding eigenvalues; the ten characteristic-zero checks use the norm shift but include no odd-length Fourier case. Its six negative controls are four validator rejections and two result-changing corruptions, not a complete rejection theorem.

**Execution boundary.** Fresh synchronization tests used ordinary O(k·2^k) C-tensor butterflies. No supplied candidate verifier, imported fast tensor engine or all-length CRT/Bluestein algorithm was run. No Lean build, numerical speed benchmark, stability analysis or bit-cost proof was performed. These bounded executions and source inspections are not a fresh formal certification or execution of the asymptotically fast global method.

## Recommended next checks

1. Correct the manuscript’s comparison to distinguish the written quartic-log bound from the existing formal quadratic-log compiler. Credit the two-bank primitive and scope any originality claim to a precisely identified difference.

2. State the displacement product dimensions explicitly: L is a-by-e and U is e-by-e. Document one final global mixed-layer split and distinguish data-register width from evaluator memory and schedule storage.

3. Keep a future rerun of the authored suite separate from the completed fresh implementation. Expand characteristic-zero odd-length, boundary-size and malformed-input coverage. Keep assertions enabled and preserve exact source and output hashes.

4. Compare one-bank and prior two-bank circuits under the same accounting for homogeneous layers, preparation, width and total scalar work. Rebuild the relevant formal dependencies before asserting a newly verified machine-checked result.

5. Treat the global composition as a proved mathematical implication until an end-to-end implementation is supplied. Do not promote it to practical speed, stability, bit complexity, a direct O(N) q-kernel oracle or a result for unresolved structured-input branches.

## Primary sources

**[1] OpenAI exact-width quadratic Fourier word.** [FourierWords.lean, sound_ballad, creates_ballad and score_le](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/FourierWords.lean#L101-L119). All OpenAI file links below are pinned to revision fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb.

**[2] Uniform preparation.** [LocalCompiler.lean, publish](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/LocalCompiler.lean#L113-L138) and [ToeplitzCompiler.lean, buildHarp](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/ToeplitzCompiler.lean#L166-L170).

**[3] Existing two-bank mechanism.** [CirculantUpdates.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/CirculantUpdates.lean), [ToeplitzUpdates.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/ToeplitzUpdates.lean) and [MeasuredFit.lean](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierTransform/MeasuredFit.lean).

**[4] Provenance.** [OpenAI commit introducing the formalization, 8 October 2026](https://github.com/openai/math/commit/301488868beec11bfd897168433b0a64f5258559).

**[5] Written framework and theorem dependencies.** [Local compiler](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/local.tex), [fixed tensor engine](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/network.tex), [synchronization](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/synchronization.tex) and [all-length reduction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/all-lengths.tex).

**[6] Dumas–Grenet.** [In-place accumulation of fast multiplication formulae, v3](https://arxiv.org/pdf/2307.12712v3); [Fast in-place accumulation, v7, §§6.1–6.4](https://arxiv.org/pdf/2302.13600v7).

**[7] Earlier factorization in the research archive.** [Content-addressed original README for ALG-022/F096](https://github.com/AgentSlop-Si/research/blob/main/math/archive/objects/bc/bc62a95e8677464a5ecc682f5afc9a62f329a5e08c218e86f1782986b1998ab0__059_bc62a95e8677464a.inert.txt), lines 11–40. This archive link uses the main branch; the reviewed content is identified by SHA-256 bc62a95e8677464a5ecc682f5afc9a62f329a5e08c218e86f1782986b1998ab0.
