# Independent final review: M-SPARSE-DEFECT

Date: 2026-10-18. Decision: **ACCEPT the three stated mathematical claims at their exact scopes.** No mathematical correction is required. Parent owner remains M-SPARSE-DEFECT, TO RESEARCH, priority 42. General support-budget sharpness remains open.

## Bound candidate

Reviewed `ACCEPTED_REPORT.md` and its complete source/verification packet after inspecting the final candidate manifest. Acceptance is bound to:

- Candidate REPORT.md SHA-256: `788bf8c9c342b7e6d6b6ece6ffe511c61f7d1d08bd4373046b0ef2ef2d7d031c`
- Candidate MANIFEST.json SHA-256: `6b107df3bf427b2d1fb5543f094667d1e74568b99b82bc1d207fe3599bc38c48`
- Pinned repository commit: `c3a882a7e6e61af05fe1045145bc1a43038d77c6`
- Phase20 source Git blob: `28212b19e78502ce5acf52a90570d42b0285d3d0`, independently recomputed from its exact bytes.

All 12 candidate manifest members matched both size and SHA-256. The manifest remained unchanged from first inspection through completion of the fresh controls. The review includes a copy of that manifest as `CANDIDATE_MANIFEST.json`. A modified candidate needs renewed review of the modifications; this decision is not an open-ended endorsement of later versions.

## 1. Original model and inherited floor

The selected record explicitly leaves global uniform inverse-row-sparsity sharpness open. Phase20 §5 treats the complex normalized Fourier matrix, invertible M, the spectral/operator 2-norm, and sparse rows of M^{-1}. Its floor uses only one sparse inverse row. The candidate correctly strengthens the admissibility requirement to every inverse row without changing the metric, field, target normalization, or invertibility assumption. All support permutations and complex nonzero coefficients remain available.

The inherited proof is valid: bM=e_i, unitarity gives ||bF||=||b||, and flat entries give |(bF)_i|≤sqrt(s/N)||b||. Completing the square yields ||M−F||²≥1−s/N. No conditioning restriction or hidden coefficient normalization is imposed. Sparse-column and common-frame commutator claims elsewhere in the owner record are not modified.

## 2. Half-density construction

**Accepted:** Delta(2m,m)=1/sqrt(2) for every m≥1, with attainment and condition number one.

Reordering columns even-first gives the displayed radix-two identity exactly. In the lower block, the odd column exponents acquire a minus sign, whereas the even columns repeat the upper block. Both F_m and D F_m are unitary. The retained diagonal blocks therefore have M M*=I/2, and the omitted off-diagonal blocks have (F−M)(F−M)*=I/2. These are operator-norm certificates, not merely Frobenius or row-norm calculations.

The inverse is the stated row-permuted block-adjoint matrix. Both inverse blocks are dense m-by-m matrices because Fourier entries and diagonal phases never vanish. Each inverse row and column has exactly m nonzero entries. Permuting inverse rows changes no support cardinality. Every singular value of M is 1/sqrt(2); its condition number is exactly one, while its absolute gain is separately stated. The inherited floor with s=m matches the witness. The argument is valid for odd m as well as even m and has no power-of-two assumption.

## 3. Singleton obstruction and strict infimum

**Accepted:** Delta(N,1)>sqrt(1−1/N) for every N≥3.

An invertible inverse with at most one nonzero per row must have one in each row and distinct occupied columns. It is monomial, as is its inverse. Thus the proof ranges over the full admissible class, not just diagonal matrices.

At equality with a=sqrt(1−1/N), every approximant coefficient must equal its selected Fourier entry by the exact row-norm identity. Then all residual row norms are a. Since a²I−EE* is positive semidefinite with zero diagonal, it vanishes. Equivalently, |A_ij|²≤A_ii A_jj for positive semidefinite A forces every off-diagonal entry to vanish. Computing a residual cross-row inner product removes the two distinct selected columns, yielding the candidate's necessary phase condition

omega^((k−l)(sigma(k)−sigma(l)))=−1.

For odd N the right side is not an Nth root. For even N≥4 the neighboring pairs (0,1) and (1,2) each force an image increment N/2 modulo N; adding them forces sigma(0)=sigma(2), contradicting permutation injectivity. At N=2 the two supports do satisfy the phase condition, as the half-density witness requires.

The compactness argument proves a strict gap at the infimum. If a sequence approached a<1, the triangle inequality would bound its matrices. Pass to a convergent subsequence of one of finitely many support patterns. Its limit has error a, and its smallest singular value is at least 1−a>0 by ||Mx||≥||Fx||−||(M−F)x||. It therefore cannot lose invertibility or any required monomial nonzero. The limit would attain forbidden equality. This rules out equality of the infimum, not merely attainment. No uniform numerical gap or general exact optimum is implied.

## 4. Exact N=3 optimum

**Accepted:** Delta(3,1)=sqrt(3)/2, attained with condition number one and singular values 1/2.

The diagonal unitary transform C=D F_3 D equals ((1−omega)I+omega J)/sqrt(3), with eigenvalues −i and sqrt(3)/2+i/2. It is normal and invariant under all coordinate permutations. The six-permutation average of any diagonal approximation is the scalar trace/3. Operator-norm convexity and unitary invariance show scalar approximation is no worse. This lower-bound reduction is valid even when the averaged scalar is zero: it minimizes over a larger class, and the eventual midpoint witness is nonzero.

The two eigenvalues are distance sqrt(3) apart. Their midpoint gives optimal radius sqrt(3)/2 and has modulus 1/2. Pullback through D yields M=cD, since D^3=I. This is invertible and has the claimed gain and condition number.

Every permutation of three residues is affine j↦aj+b with a=1 or 2. Column reordering diagonalizes any monomial support; unitary row phases then reduce its Fourier target to F_3 or its complex conjugate. The coefficient space remains the full complex diagonal space, and conjugation preserves the norm. Thus the lower bound and optimum apply to all six support patterns. Fresh exact controls additionally constructed and verified a pulled-back minimizing witness on each of those six supports.

## 5. Fresh independent controls after inspection

`fresh_exact_controls.py` was written for this review after the report, sources, candidate checker, and manifest were inspected. It does not import or run the candidate checker or historical code.

- Half-density: exact integer polynomial remainder arithmetic in the Nth cyclotomic quotient at N=2,4,…,40,42,50,64. At each of these 23 dimensions, both Gram orders were checked for the retained and omitted matrices, together with complement identity and every inverse row/column support count. The two retained Gram identities also verify both inverse products via the exact scaled adjoint formula.
- Singleton equality: all 409,112 support permutations for N=2 through 9; exactly the two N=2 permutations pass, and none for N≥3. A separate neighboring-pair congruence control covers every even N=4 through 200.
- N=3: exact radical algebra checks the symmetrized Fourier identity, the fully symbolic diagonal twirl, the two-eigenvalue radius, and six explicit monomial minimizers. Both inverse products, every inverse-row singleton support, exact error Gram 3I/4, and witness Gram I/4 were checked.
- Negative controls: invalid/odd construction dimensions, a corrupted retained entry, a singular repeated-column mask, an altered absolute gain, and an N=4 residual with the right row norms but the wrong operator-norm Gram certificate. All were rejected as intended.
- All candidate manifest entries and the source Git blob were checked before and after controls. The candidate manifest did not change.

The controls passed with empty stderr. `FRESH_RESULTS.json` and `FRESH_RUN.log` record the results. These finite checks support, but do not replace, the general proofs above. They provide no floating-point production, measured-cost, finite-field norm-transfer, or novelty certificate.

## 6. Accepted record delta and stop

The proposed record delta is accurate as written: mark the even half-density family and singleton nonsharpness/exact N=3 slices complete, retain the existing owner/status/priority, and leave general budgets open. Preserve all original model, implementation/preparation/output cost, sparse-column, commutator-frame, and historical-priority limitations. No new research identity, generic Fourier speedup, unrestricted arithmetic lower bound, or worldwide novelty clearance follows.

This review's requested stop condition is met: proof inspection, fresh exact and negative controls, final candidate manifest verification, and sealed review evidence are complete. No repository, table, or other external state was changed. No further general support-budget search was started.
