# Four-source Fourier research update

10 October 2026, 12:40 dated supplement

This supplement preserves four newly reviewed source families and two bounded dependent refinements. It distinguishes mathematical correctness, implementation costs, inherited results and unresolved historical priority. It contains scientific notes, exact/numerical data, fresh verifiers and public references. It does not contain the original submitted archives or publisher PDFs.

## Four source families

1. [Transverse bridge obstruction](notes/01_transverse_bridge.md). A division-free rank-one condition controls four adjustable axis terms. It gives exact pinned exclusions, generic obstructions, an all-real-fixed-background exclusion for square lengths N=s² with s≥7, and explicit approximation floors. The submitted all-rectangle scan has Θ(N√N) index work; constant-work coordinate selection repairs the intended linear scan.
2. [Stable inverse defect bound](notes/02_stable_inverse_defect.md). A spectral-quantile certificate bounds the error of an invertible approximation with a sparse-plus-low-rank inverse. Scalar corollaries need s≥1; positive integer rank optimization is equivalent to the 4sr/N bound. Classical inverse-submatrix nullity gives the same graph certificate. [Independent refinements](notes/05_inverse_refinement_review.md) settle local defect rank, sharpness for one allowed neighborhood and the zero-singular-value unattained infimum.
3. [Sparse q-defect evaluator](notes/03_sparse_q_defect.md). A reciprocal q-factorial kernel spectrum takes O(N), and a raw input with k recurrence defects has a complete padded transform in O((k+1)N). Dense forcing remains an arbitrary transform. Preserve the N=243 comparator loss, the omitted inverse negations and the radix-2/3 fallback restriction.
4. [Low-conductor projected Fourier transform](notes/04_projected_fourier.md). The modal decomposition and projected output are valid, but retain fewer independent coordinates. The norm certificate does not guarantee small error. The full N=960 method is 27.81% more expensive than the stronger specified reference. A same-output additive-shell comparator is handled as a separate dependent review.

## How to use the record

- Read PROOF_STATUS.json for the final accepted scope and dependent-review state.
- [CORRECTIONS_AND_LINEAGE.md](CORRECTIONS_AND_LINEAGE.md) preserves superseded statements, why they changed and what remains open.
- [REPRODUCE.md](REPRODUCE.md) gives the portable disposable-copy tests. Exact modular, rational-cyclotomic and finite-field assertions are distinguished from floating-point diagnostics.
- [REFERENCES.md](REFERENCES.md) gives primary literature and the limits of each comparison.
- SOURCE_MANIFEST.json separates source hashes from edited-export hashes; SHA256SUMS covers every public file except itself.

Earlier snapshots are unchanged. The older selected-pair N=4 obstruction remains essential because the new transverse blocks there are only 1×1. No earlier treewidth result is duplicated. Source-family and discovery counts are not increased merely by adding a refinement, correction or independent test.

These results do not establish a new unrestricted linear-time DFT, a general circuit lower bound, globally sharp sparse-inverse constants, or worldwide priority.
