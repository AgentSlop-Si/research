# FFT research — recovered chain / publication audit checkpoint

**Date:** 2026-10-10. **Mission:** assess originality and publication readiness of the user's FFT research, while preserving the ultimate objective of an exact arbitrary-input full DFT in less than \(N\log N\) sequential charged arithmetic, ideally \(O(N)\). Do not conflate input-restricted acceleration, approximate transforms, rank/circuit obstructions, or packet aggregation with that objective.

## Recovery inventory (locally accessible archives)

- Located the user's principal archive `fft_research_master_20261009.zip` (205,321,858 bytes), containing **5,839 archive members**.
- Indexed **258** locally materialized ZIP file paths, containing **194 unique ZIP contents by SHA-256**; across them **14,787 file-member instances**, **13,776 text/code instances**, and **4,558 unique text/code payload hashes**. **No archive parse failures.** This is an index and deduplication scan, not a human mathematical proof-review of all 4,558 payloads.
- Additional library ZIPs exist, and some current Library-backed ZIPs could not be materialized; do not claim a mathematically exhaustive review of every available file.
- Inventory: `fft_review/RESEARCH_INVENTORY.json` and `RESEARCH_DOCS.tsv` (locally generated).

## Reproduced verification

| Archive | Tests independently rerun in this session | Result |
|---|---:|---|
| Hero #1 Phase 21 | 46 | pass |
| Hero #0 Phase 12 | 23 | pass |
| Hero #17 Phase 9 | 15 | pass |
| Green Phase 34 | 11 | pass |
| Weyl–Krylov v20 | 8 | pass |
| **Total** | **103** | **pass** |

Full output: `fft_review/test_results.json`. In addition, a *separately written* SymPy calculation of the reciprocal Hankel resultant at `s=1` and `s=2`, using integer sample sequences, confirmed the universal factors and palindromic quotient. This is a small-degree sanity check, not a general proof. The written general proofs are inside the research packages.

## Strongest publication directions, sorted by plausibility

### 1. Reciprocal Hankel-resultant universal factor theorem (Hero #1 Phase 21; later Phase 22/23 improvements)

For \(m=s+1\), sample sequence \(T_k\), and

\[
P_e(a,w)=\det\left[T_{e+i+j}(1-aw^{e+i+j})\right]_{i,j=0}^{s},\quad e=0,1,
\]
let \(\mathcal R_s(w)=\operatorname{Res}_a(P_0,P_1)\).

The submitted manuscript claims, **for arbitrary formal samples**, the polynomial identity

\[
\mathcal R_s(w)=w^{v_s}(w-1)^{(s+1)^2}U_s(w),\qquad
v_s=\frac{s(s+1)(4s+5)}6,
\]

where \(U_s\) is reciprocal/palindromic of grade \(2b_s\), \(b_s=s(s+1)(2s+1)/6=\sum_{j=1}^s j^2\), so \(U_s(w)=w^{b_s}V_s(w+w^{-1})\) for \(\deg V_s\le b_s\). This is the **best candidate for a self-contained mathematical algebra paper**, if the universal proof is rigorously written and the exact factorization is not covered by existing resultant/Hankel literature. A clean theorem-proofs-examples manuscript would be easier to evaluate than the entire FFT project.

The *algorithmic corollary* uses a fully verified cyclic certificate to recognize a fixed-support sparse-rational Fourier family in \(O_s(N)\) field operations, with fallback \(O(N\log N)\) on generic inputs. Later Phase 23 reduces the sufficient input probe prefix from `4s` to `2s+2` for constructing two adjacent Hankel minors and improves instrumented operation counts, without changing worst-case all-input asymptotics. Do **not** present this as an arbitrary-input linear-time FFT.

### 2. Fourier–Green restricted representation impossibility (Hero #0 Phase 12)

A one-layer sum of two arbitrary invertible weighted-permutation Green resolvents cannot equal the complex Fourier matrix for \(N\ge2301\), even with an additional diagonal term. Proof: order separation via Erdős–Szekeres, Green rank-one crosscuts, and nonzero small-arc Fourier minors via Schur positivity. The work generalizes to \(r\) summands plus bounded-rank and row-sparse corrections and includes cases with a prime divisor \(p\ge29\).

This is a **meaningful, precise, model-specific negative theorem**. Potential paper: *Fourier Minor Obstructions for Finite Sums of Permutation Green Resolvents*. Its combinatorial and quasiseparable ingredients are classical; literature checking is necessary to establish whether the compound theorem is new. It does not cover products, arbitrary graph solves, or unrestricted FFT circuits.

### 3. Low-rank perturbation barriers for products of Green stages (Green Phase 34)

For a product of stages which are sums of resolvents close in rank to sparse-reference inverses, the research proves

\[
\sum_{j=1}^{t}r_j\ge\left\lfloor\frac{N}{1+\prod_{j=1}^{t}d_j}\right\rfloor
\]

when the product equals a DFT; \(d_j\) is the reference inverse's row sparsity and \(r_j\) is the explicitly charged difference budget for denominators and diagonal gauges. For uniformly bounded stage correction rank and constant \(d>1\), the restricted architecture requires \(t\ge\log_d N-O(\log\log N)\). The proof follows an exact Fourier-versus-row-sparse Vandermonde lemma and a telescoping inverse-product rank budget. Useful as a second algorithmic lower-bound section; not a universal FFT lower bound. The basic rank lemma is elementary and likely not strong enough as a standalone novelty claim.

### 4. Weyl–Green packet character fusion and obstruction (v20)

A Fourier character over \(N\) Weyl-related Green resolvents yields one matrix with exactly \(N-1\) or \(2N-1\) nonzeros, hence an \(O(N)\) application. A reflected quadratic fiber forces a zero \(2\times2\) minor not shared by affine-gauged DFTs; this excludes that **particular** packet model. Potential short algebraic note, but it mostly combines classical Heisenberg/Weyl operators, roots-of-unity filtering, and a new-looking explicit minor certificate. Priority unverified.

### 5. Spectral projector/local rational Green rank-distance theorem (Hero #17 Phase 11)

For nontrivial Fourier spectral mask \(K\) and a low-degree rational circulant \(p(S)/q(S)\) of degree at most \(d\), the rank distance is either the trivial mask rank (zero/identity filter) or at least \(N-2d\), attained in the documented range. This is a sharp **restricted commuting filter** result, not a runtime lower bound. An actual rank-\(N\) difference can still apply in linear time in a special Green representation, illustrating a common rank-to-cost fallacy.

## Literature boundary / no priority claim

- Uteshev, Baravy & Kalinina (2021), *Rational Interpolation: Jacobi’s Approach Reminiscence* establishes mature Hankel/rational interpolation and resultant background. https://www.mdpi.com/2073-8994/13/8/1401
- Boito & Eidelman (2025), *Computation of quasiseparable representations of Green matrices*, documents the long-developed quasiseparable/Green theory. https://arxiv.org/abs/2308.02701
- Dvir & Liu (2020), *Fourier and Circulant Matrices are Not Rigid*, warns against claiming an unrestricted Fourier rigidity theorem. https://zesty2.cs.uchicago.edu/articles/v016a020/
- OpenAI's October 2026 exact-complex formalization documents an **external** uniform \(O(N(\log N)^{1-10^{-13}})=o(N\log N)\) exact DFT in a specific unrestricted exact complex arithmetic model. This is *not* a stable floating-point or integer bit-time FFT bound. https://github.com/openai/math/blob/main/lean/docs/130.md

The narrow combined identities above did not appear in a preliminary targeted search, but **absence of a quick search hit is not evidence of worldwide originality**. A specialist literature review and independent referee review are required before publication novelty can be asserted.

## Bottom line

**There are serious, paper-shaped results worth developing**, especially the universal reciprocal Hankel resultant symmetry and the Fourier–Green one-layer obstruction. Their proof coverage and reproducible certificates are much stronger than an informal FFT hypothesis. **No user-project exact general \(O(N)\) full FFT has been proved**; the supported accepted-class algorithms remain conditional on sparse structure and the generic fallback incurs \(O(N\log N)\). Do not call performance comparisons in a unit-cost finite field model bit-complexity or floating-point speedups.

## Next step after a future break

1. Resume from this checkpoint and `RESEARCH_INVENTORY.json`, **not** from an earlier speculative FFT construction.
2. Select the reciprocal Hankel-resultant theorem as the primary intended first paper; separately verify the generic Newton-polygon valuation proof and check specializations in rings of arbitrary characteristic.
3. Ask a mathematical algebra specialist to check the explicit universal factors against Hankel pencils/resultant literature. Pin the new mathematical statement, not generic FFT acceleration, as the originality claim.
4. For a second paper, develop the complex Fourier–Green one-layer theorem together with the Phase 34 non-additive restricted architecture, keeping hypotheses unambiguous.
5. Preserve source archives unchanged and maintain exact tests, proof scripts, negative controls and clear model/cost ledger.
