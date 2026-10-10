# Prior-work and source audit (10 October 2026)

## Accessible local corpus

Inspected local research materials available in this conversation container, including the 9 Oct `fft_research_master_20261009.zip` (3,532 member occurrences), Phase 22 Green/Gram, Phase 21 Weyl, Phase 20 projective-curvature, Phase 26 non-affine Green cuts, the previous phase-cone theory, two-sided Fourier-rank gates, inverse-footprint theory, and latest projective algebraic/Segre certificates. The reproducibility script also scanned and integrity-checked **30 accessible ZIPs with 4,033 ZIP-member occurrences**, including duplicated and nested research materials. These are inventory figures, **not** independent re-verification of 4,033 proofs; source inspection focused on mathematical predecessors and potential overlaps.

## Provenance boundaries

- **Pre-existing project result:** Master archive, `additions/1807/.../fft_green_phase22_gram_gate/THEOREM.md`, already proves a connected-Gram obstruction for `F=A Q P B` with real invertible `A,B`, even `N>=4`, but **without arbitrary complex outer diagonal gauges**. Its real Fourier reflection basis and covariance tests are earlier work.
- **Pre-existing project result:** Phase 20 established nonreal Fourier `2x2` cross-ratios and their invariance under outer complex monomial changes; Phase 21 established two-state single-Green row ratios. Neither should be relabeled.
- **Pre-existing project result:** The latest `fft_phase_cone_20261010/THEOREM.md` allows outer complex gauges and many positive stages but excludes a single complex mask only when its angular width is <pi with a quantitative error bound. **The present exact theorem closes its unrestricted-width positive-stage escape** for exact Fourier equality.
- **Added in this package:** Unitarity-driven Gram phase synchronization **with arbitrary complex outer gauges**; all-N exact positive Green no-go (N>=3); and a sharp all-N Frobenius realification formula attained by quadratic CAZAC chirps. An exactly-unitary restricted network inherits a conditioning-free operator error lower bound approaching 1/sqrt(2).
- **Scope not covered:** genuinely complex stage aggregates not projectively gaugeable to positive real matrices, two or more internal independent complex masks, approximate nonunitary candidates, or all possible FFT circuits.

## External foundations (not new)

1. Östergård and Valtonen, *Equivalence of complex Hadamard matrices*, Journal of Algebraic Combinatorics (published July 28, 2026): https://link.springer.com/article/10.1007/s10801-026-01568-x . Standard complex-Hadamard equivalence and Haagerup cross-ratio invariant.
2. Classical Chu/Zadoff–Chu CAZAC sequences, constant-amplitude Fourier spectra: original D.C. Chu, IEEE Transactions on Information Theory (1972), and https://arxiv.org/abs/2211.05702 . Quadratic chirps and zero cyclic autocorrelation are existing techniques.
3. Phase-22 and Phase-20 project archives explicitly credited above.
4. OpenAI exact DFT problem #130, https://github.com/openai/math/blob/main/lean/docs/130.md : reported exact sub-NlogN in a particular arithmetic model. No claim in this package competes with this bound.

**Novelty assessment:** A mathematically verified **project-specific strengthening**, but no comprehensive global prior-art survey or peer review. Publication priority should not be asserted without expert validation.

## Further all-group extension

Theorem 6 extends the cyclic chirp realification identity to all finite abelian Fourier character tables, with the exact constant determined by the size of the 2-torsion subgroup. Tensor products of classical Chu chirps prove sharpness. The mathematical ingredients (finite abelian Fourier tensor products and Chu sequences) are classical; this particular combined formula was not located in the sampled project checkpoints. No worldwide priority claim is made.
