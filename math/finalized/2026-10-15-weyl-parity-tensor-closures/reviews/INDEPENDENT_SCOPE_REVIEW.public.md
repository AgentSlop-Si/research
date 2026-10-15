# Independent review of three scope-finalization candidates

Publication derivative: remove private workbook identification, transient live-count metadata and application workflow prose; retain the complete scientific review. Original and export hashes are recorded in PUBLIC_PROVENANCE.json.

Review date: 2026-10-15 UTC. Records: M-WEYL-RESIDUAL, M-PARITY-DEPTH, M-TENSOR-CUT.

## Verdict

**ACCEPT the three existing theorem scopes, subject to the precise guards below.** Their recorded correctness is already accepted; this review supports finalizing those named records after a bounded primary-source comparison, without treating finalization as three new discoveries. Worldwide priority remains unverified. The exact 66-value-cell plus three-status-background payload is independently ACCEPTED with application guards; its hash and fresh-preimage preservation audit are in INDEPENDENT_PAYLOAD_VERDICT.json. This review makes no external writes.


## Evidence identity

../SOURCE_BINDINGS.json records SHA256 verification of the three Catalogue-pinned source exports and exact canonical entries from the accepted review ledgers. Both review files retain their recorded hashes. The matching outcomes are proved_scoped. The relevant full proof/review bodies were read, not only their summaries.

M-TENSOR-CUT's existing sanitized-export/original-byte identity qualification survives. Hash equality to its pinned export is not proof that an unavailable original archive is byte-identical. Neither the original source programs nor historical large runs were executed. No new source-recovery assertion is made.

## M-WEYL-RESIDUAL

Use F[j,k]=omega^(jk)/sqrt(N), Z e_k=e_(k+1), D e_k=omega^k e_k, with the chosen sign convention consistent throughout. From MZ=DM, M[j,k]=b_j omega^(jk). From MD=Z^-1 M, b_(j+1)=b_j. Thus M=cF without assuming M invertible. Primitive-root availability implies the characteristic does not divide N; normalized field versions separately require the normalizer. Deterministic scalar calibration removes c.

Over C, set K=F* M. The two residuals become commutators of K with Z and D. The orthonormal Weyl basis diagonalizes the sum of squared Frobenius defects with weights |1-omega^a|^2+|1-omega^b|^2. The unique zero mode is scalar, and the least positive weight is 4 sin^2(pi/N). Consequently the sharp distance-to-scalar-family gap is 2 sin(pi/N); M=FD attains equality. This is not a uniform-in-N gap or a norm statement over a finite field.

For fixed linear M over F_q after calibration, one common random vector tests the stacked defect matrix C=[MZ-DM; MD-Z^-1M]. Rank-nullity gives exactly q^(N-rho) accepting vectors, hence q^(-h rho) for h independent uniform probes. This is an acceptance formula conditional on calibration. A wrong scalar has zero defects but fails calibration. The calls are one calibration call plus three calls per round. The candidate's preprocessing, root/field preparation and complete execution costs remain charged; additional vector work is linear per round, not a bit-complexity claim. The argument does not test linearity or protect against stateful/adaptive oracles. A modular rejection reaches characteristic zero only through a valid specialization preserving all denominators and required roots.

Primary comparison: Tyson's §2 Theorem5 explicitly gives scalar Fourier from the invertible complex Weyl conjugacy relations, with sign changed by conjugation. It overlaps the exact characterization, but does not itself state the singular-M/general-field variant, sharp residual constant or calibrated F_q rank-exact verifier. This is a precise component match plus qualified nonmatch, not evidence of novelty. The separate Q10/P05/S5 nonlinear obstruction is not counted as this theorem.

## M-PARITY-DEPTH

The exact rank formula is for complex Fourier, N=2^k with k>=2, nonzero masks, and all parity signs. With h=2^(u+1), the column halfset representatives contain one element of each residue class modulo h/2. The imported Osgood–Siripuram–Wu Theorem4 applies to this complex prime-power Fourier matrix: representative counts are balanced at every required modulus. The period-direction Fourier transform separates row residues. If v<log2(N/h), half the blocks are full and half absent, giving N/4; otherwise every surviving block is square of rank h/2, giving N/2. Hence the threshold u+v<=k-2 is correct.

For each quasiseparable stage of upper and lower contiguous-cut rank at most r_j, splitting membership runs gives cross rank at most r_j d(A_j). Product telescoping requires transported sets, rather than one fixed coordinate cut. GF(2)-affine pullback gives invertible linear transport of masks; translations only flip parity signs. If sum q_j<k, the low-bit constraints leave a nonzero mask. The weighted capacity is at most N sum r_j 2^(-q_j)-sum r_j<N/4 when some r_j>0. If all orders vanish, every stage is diagonal and the entire architecture with routed monomials is monomial or a degenerate monomial, so it cannot be Fourier. This separate zero-order branch avoids incorrectly using a strict inequality with sum r_j=0.

Any balanced complex Fourier restriction has rank at least N/4 by its Frobenius norm and operator-norm bound. Arbitrary nonzero external diagonal factors and permutations preserve the applicable restriction rank. Thus the coarse depth bound allows arbitrary invertible external monomials while the internal routing remains GF(2)-affine. Uniform r>=1 yields k<=t ceil(log2(4rt)). It is a structural depth obstruction, not an N log N arithmetic lower bound. No nonlinear internal routing exclusion follows.

The historical uniform helper omits r in the displayed capacity for r>1. The explicit regression k=9,t=2,r=2,mask=16 gives boundaries 31,31 and capacity 124, not 62. Saved r=1 witnesses are unaffected; no original helper repair is claimed here. Finite-field ranks corroborate selected cases, but universality is the complex primary theorem. A concrete universal set still drops from rank8 to rank7 modulo12289 and has rank8 modulo65537.

Primary comparison: Osgood–Siripuram–Wu supplies the exact imported sampling ingredient. Its theorem does not state the moving-affine depth argument. The accepted application and elementary norm route remain correctly identified; historical novelty is not resolved.

## M-TENSOR-CUT

Let Q,M be positive integers, N=QM, with a primitive Nth root omega in a compatible splitting field and xi=omega^M, eta=omega^Q. For j=t+Qu and k=h+Ms, expansion gives T[s,h,t,u]=omega^(-ht)xi^(-st)eta^(-hu). No coprimality of Q,M is needed. The labels are essential:

- (s,h)|(t,u): rank N, the Fourier input/output cut.
- (s,t)|(h,u): rank min(Q,M), after removing nonzero scales and repetitions, leaving the rectangular Vandermonde [omega^(-ht)].
- (s,u)|(h,t): rank N, reducible to the tensor product of the two invertible endpoint Fourier matrices with nonzero column scaling.

Input/output rank lower-bounds CP rank by N. Fixing each (t,u) gives N explicit four-leg rank-one summands, so the bound is attained. Separate invertible changes on each single leg preserve the paired ranks. Joint two-leg changes are outside that statement.

When A acts on s and B on u, transformed entries factor as (AF_Q)[a,t] omega^(-ht) (F_M B^T)[h,b]. The middle factor never vanishes, so total support equals nnz(AF_Q)nnz(F_M B^T), at least QM. Equality holds exactly when both invertible factors are monomial. Thus the N-entry center requires inverse-Fourier endpoints up to monomials, whose evaluation costs remain paid. A growing crossed-cut obstruction requires min(Q,M) to grow; a fixed radix does not suffice. There is no general arithmetic-circuit lower bound or faster all-input evaluator.

Primary comparison: Tyson Definition12/Corollary15 maps exactly to the (s,u)|(h,t) cut under (M1,M2,N1,N2)=(M,Q,Q,M), input (ell,m)=(u,t), output (j,k)=(s,h), and conjugation for the sign. It supplies rank N there. It is not an exact source for the distinct min(Q,M) cut, CP rank or local support-equality package. The bounded nonmatch leaves exact priority open and does not count unrelated recurrence/innovation results from the same source document.

## Fresh independent controls

Run python -I checks/independent_controls.py from the package root. The checker was written for this review; it imports no inherited program.

- Five exact Weyl linear-constraint ranks over F97: N=2,3,4,6,8, with one-dimensional joint solution space.
- Ten calibrated perturbations exhaustively enumerate probes over F5 at N2 and F7 at N3; exact rank-nullity counts agree, wrong-scalar controls reject, and two rounds make seven candidate calls.
- Nine numerical complex lengths N=2,3,4,5,6,8,9,12,16 verify the FD equality ratio and random-map inequality.
- 2,264 exact modular parity submatrix ranks, every nonzero mask pair and all four signs at N4,8,16 over F97 and F193.
- The bad-prime universal-set control and the weighted-capacity regression above.
- 42 exact tensor flattening ranks over fourteen rectangular/square sizes, including unit radices and asymmetric pairs; every digit entry checks against the full Fourier exponent.
- All 230,400 pairs of invertible 2x2 matrices over F5 verify the endpoint-support minimum/equality condition; 1,024 minimizing pairs.

FRESH_CONTROLS.json records outputs. Exact finite checks and floating controls corroborate the displayed proofs; they do not establish all-size statements by extrapolation or certify original implementation branches.

## Publication and application conditions

The separate public payload-verdict derivative records the final exact-payload acceptance and guards. The scientific acceptance does not itself prove that any external write occurred. Any application must preserve the existing unrelated records and metadata, use the exact reviewed request bytes, recheck current preimages, and verify the resulting statuses and dashboard counts.

The author's FINALIZATION_REVIEW.md was independently checked. Its additional Freivalds comparison is valid as a technique-level partial match: the 1979 Theorem3 uses independent random sign vectors for a real matrix-product defect, not the rank-exact finite-field probability. Cooley–Tukey Equation(3) confirms the mixed-radix index substitution r1=M,r2=Q,j0=h,j1=s,k0=t,k1=u; direct expansion supplies the phase identity.

Primary sources verified online: https://arxiv.org/html/1204.0992v1#S4.SS2 and https://arxiv.org/html/quant-ph/0306144#S2 and https://arxiv.org/html/quant-ph/0306144#S5. Exact comparison metadata is in PRIMARY_SOURCE_CHECKS.json.
