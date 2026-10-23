# Independent scoped acceptance: Q27 complete 3+2 five-phase family

23 October 2026. ACCEPT the frozen complete 10,240-label theorem, not the full 34-phase problem.

## Scope and source delta

The accepted label set is exactly:

- [7,a,b,c,d], a=8..15, b=16..23, and (c,d) either (31,e), e=32..47, or (e,f), e=32..39, f=40..47;
- [c,d,31,a,b], a=32..39, b=40..47, and (c,d) either (7,e), e=8..23, or (e,f), e=8..15, f=16..23.

There are 2*8*8*(16+64)=10,240 original coordinate labels, with one edge per active branch, three active branches in one stage and two in the other. For every label, all five multipliers remain arbitrary complex unit phases and all six original inverse guards are retained. No original guarded point is externally invertible-complex row/column monomial-equivalent to F8.

The chart is unchanged, SHA-256 5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98. The source edge directions, gains, fixed tree edges, stage sums and M=S_1 S_0 order were independently reconstructed. These are five-coordinate labels beyond the accepted triples, one-branch families and four-coordinate families, including the immediately preceding 2,176 distribution-3+1 labels. Intersections at fixed-phase specializations are not re-counted as new coordinate labels. This count is not a number of disjoint matrix-image components, symmetry classes or separate discoveries.

Q27 remains open. Arbitrary five-edge motion, the 3+3 six-phase family and the full 34-phase fiber are not settled here. There is no construction, FFT improvement, priority change or historical novelty claim.

## Proof review

The previously accepted original numerator and pole-division argument applies unchanged to five variables: N=Delta M, the polynomial reciprocal Ntilde is defined without transpose, H=N entrywise Ntilde, K is the doubly centered H, and K=F E globally as polynomials. Here F is the product of the five active guards. E is multiaffine. The fully active stage's three-guard ideal J gives E in J and every centered minor T in J^2. Thus the initial containing support has 207 monomials. These facts were independently rechecked, not assumed from a finite rank pattern.

The new double-pole reduction is valid. In the partial stage with active guards f,g and fixed nonzero third guard d, write the pole residues U=u v^T and V=r s^T. Then A=d(gU+fV) modulo (f,g)^2, and its reciprocal numerator is -d(gU^T+fV^T) to first order. In the f*g coefficient of H, the same-branch square terms have constant row or column direction because u_i v_i=r_i s_i=1; double-centering removes them. The cross terms have the two frozen directions formed from u entrywise s and r entrywise v. After centering these are alpha and beta.

For a partial stage 1, E restricted to f=g=0 therefore has fixed left span {alpha,beta}; for a partial stage 0 it has the corresponding fixed right span. The other stage's guard product can be inverted temporarily to derive this identity in a fraction field. Multiplying the resulting minor cross-difference by that product squared gives a polynomial identity. Cancellation in the integral polynomial ring then proves the cross-difference itself is zero. This does not exclude any zero of a guard or alter the admissible domain.

Let rho be the 21 frozen wedges of alpha,beta. The reference rho_ref is a coefficient, not a new variable guard. The equations Q=rho_ref T-rho_pair T_ref multiply by rho and never divide by it. They are constant combinations of the original centered minors, lie in J^2, and vanish modulo (f,g). Hence their complete characteristic-zero support is precisely contained in the multiquadratic exponents having full-stage total degree at least two and partial-stage total degree at least one. Its dimension is (27-4)*(9-1)=184.

The specified 184x184 coefficient determinant is nonzero in characteristic zero by a legitimate map from the original Gaussian coefficient localization to F65537. All inverted Gaussian factors survive; the affine guard substitution and frozen pole substitutions use only original holonomy inverses. The 21 rho values also lie in that coefficient ring. Every selected reference is nonzero in the recorded specialization, so none is an omitted case.

The target monomial y_j^2*y_k, with j the full-stage branch-zero variable and k the first partial-stage variable, belongs to the proved support. The adjugate identity expresses d_C times this monomial as an exact constant combination of recorded Q rows. Applying the original signed Cauchy-Binet bridge to each centered minor proves

    d_C F^2 y_j^2 y_k belongs to the ideal of the original 784 H minors.

All factors on the left are nonzero on the original guarded unit torus. Fourier monomial equivalence would force every generator on the right to vanish, a contradiction. This is a guard-ideal certificate, not a unit-ideal statement, finite-field rootlessness claim, or inference from an unproved modular support projection.

## Independent computation and controls

reconstruct_five.py is reviewer-authored, extended only from the reviewer's own prior independent four-variable reconstruction. It imports no author or historical scientific program. The frozen certificate JSONL and coefficient-scheme JSON are inert inputs.

The program independently constructs all original weighted paths in both Gaussian embeddings, all 243 H coefficient positions, the opposite-embedding reciprocal, and full guard division with multiply-back in every position. It converts to guard coordinates, verifies the full-stage ideal support, reconstructs both original branch pole residues and all 21 rho values, forms the required row or column cross-differences, and checks every excluded coefficient before selecting the 184-column support. The two recorded complete column schemes are checked against the independently generated lexicographic support.

All 20,480 recorded determinants passed, covering every one of the 10,240 labels in each embedding. Every frozen selected row was used as recorded; no replacement minor was selected. Complete uniqueness and coverage, all references and rho values, and every determinant residue were checked. The complete frozen JSONL SHA-256 is fd004db865803a03add7a67ca6a6571387feb9e0d6c1a0b814f72b7a0a9c7152. The full replay took approximately 118 seconds. Four cross-orientation/embedding records also pass Python -O. All checks use explicit exceptions, so none is disabled by optimization.

Fresh exact Gaussian-rational controls isolate the mixed f*g coefficient by an exact four-point coefficient identity, at one fixture in each stage orientation. They verify all 441 proportionality cross-differences per fixture, 882 exact identities in total. Altering one frozen direction weight is detected in each fixture. The directional fixture is nontrivial, with a nonzero restricted minor. Ordinary and optimized exact-control results agree. The exact controls are self-contained with this reviewer's own reconstruction module; no author executable is used.

All NumPy coefficient and determinant arithmetic is exact integer arithmetic: the longest coefficient accumulation has at most 1,024 products below 65537^2, safely below signed 64-bit capacity. Python scalar products are unbounded integers. The hand proof, not the finite controls, establishes the support and pole statements for characteristic zero.

## Frozen acceptance and limits

Accepted author manifest: c9905e4131f47dd692db6c1ea7b0dc77e651770139059afc8faba3f4ffea50ac.
Accepted proof: 6849d7e3f9d4170291e4555870901511a7550826138b5f1d1120f272b7989933.
Accepted complete certificates: fd004db865803a03add7a67ca6a6571387feb9e0d6c1a0b814f72b7a0a9c7152.

The author manifest and its listed source bytes have been checked; exact inventories are retained in BINDINGS.json. The original-ideal proof and adequate negative controls pass. Acceptance is mathematical and scoped as above; repository publication state and native table writes are not audited or performed here. The next six-phase research packet is outside this acceptance.

Reproduction: set Q27_CANDIDATE_DIR to the frozen candidate directory, run reconstruct_five.py with the complete JSONL, result output path and optional process count, then run exact_direction_controls.py. All scientific code needed by this review is contained in this review directory.
