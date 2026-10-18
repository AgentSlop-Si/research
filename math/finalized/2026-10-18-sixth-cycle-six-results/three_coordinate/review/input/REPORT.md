# Q27 terminal-gate candidate: all three-coordinate labels excluded

Status: complete candidate theorem and exhaustive certificates; independent review pending.

The remaining 5,744 guarded unit-phase three-coordinate slices through the original
N=8 witness are excluded from invertible-complex external monomial equivalence to
F8. Together with the inherited 240 accepted exclusions this would cover all 5,984
labels. The full 34-phase fiber and four-or-more-coordinate slices remain open.

The new mechanism uses all division-free 2-by-2 entry-modulus minors. A cut-edge
support lemma and two exact pole-intersection Taylor spaces give coefficient-space
dimensions 46, 56, 41 and 52. Every remaining label has a nonzero characteristic-zero
minor, certified by an admissible modular determinant. No finite-field rootlessness
is used. The resulting exact ideal contains F or F^2, so saturation at xyzF is the
unit ideal. Original poles and zero-entry components are treated explicitly.

Coverage:
- 112 same-stage, same-branch triples, rank 46
- 1,008 same-stage two-plus-one branch placements, rank 41
- 1,904 mixed-stage triples with a same-branch pair, rank 56
- 2,720 mixed-stage triples with a different-branch pair, rank 52

All 5,744 labels pass in both Gaussian embeddings of F_1000000009. The primary run
took 6.40 seconds and the conjugate run 6.29 seconds in this environment. These are
certificate reconstruction timings, not an algorithmic complexity or FFT claim.

Additional controls, separate from the frozen review core:
- exact Gaussian rational direct inversion of all six original branches at 16
  representative label/phase points: 96 inversions;
- 1,024 exact comparisons of N=Delta M entries;
- 12,544 exact original-modulus bridge comparisons;
- independent Python reconstruction of eight stored C++ minors, including their
  same fixed minors in the opposite embedding;
- eight duplicated-row controls all give determinant zero.

PROOF.md gives the theorem, exact model, support lemma, coefficient spaces,
denominator lift, saturation and scope. CORE_MANIFEST.json freezes the review
core. OPTIONAL_CONTROLS_MANIFEST.json binds later control artifacts. No historical
program was executed and no external state was changed.
