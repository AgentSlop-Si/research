# Independent mathematical acceptance: Q27 original 3+1 guard strata

23 October 2026. Verdict: ACCEPT THE EXACT SCOPED THEOREM BELOW.

## Accepted result and the exact delta

For the pinned original N=8 chart, every original four-phase coordinate label

- [7,a,b,c], 8<=a<=15, 16<=b<=23, 31<=c<=47;
- [c,31,a,b], 7<=c<=23, 32<=a<=39, 40<=b<=47

is excluded from external invertible-complex row/column monomial equivalence to F8, on the original complex unit-phase domain and all six original inverse guards. The count is 2*8*8*17=2,176 coordinate labels. This is the complete one-moving-edge-per-active-branch distribution 3+1. It is not a claim of 2,176 disjoint matrix-image components, symmetry classes, or separate discoveries. The corresponding coordinate subspaces can overlap at fixed-phase specializations, including with earlier accepted families.

The accepted predecessor covers 256 distribution-2+2 labels [7,e0,31,24+e1], plus inherited 5,984 triples and four whole-one-free-branch families. The new 3+1 labels are distinct from that 2+2 list, have four freely moving coordinates rather than three, and are not contained in a single-branch family. Thus this is a genuine additional family exclusion, not a re-count of the predecessor. No claim is made about four-coordinate distributions not specified above.

Q27 remains open at its unchanged priority. The full 34-phase fiber, five-or-more-phase motion, other witnesses, FFT construction, complexity improvement and historical novelty are not resolved. Nothing here establishes a surviving legal Fourier witness in a family whose rank test is inconclusive.

## Independent proof verification

### 1. Original model and polynomial necessity

The chart has been matched byte-for-byte to the accepted predecessor: SHA-256 5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98. The directed cycle convention, all Gaussian gains, fixed tree edges, unit stage-sum coefficients and product M=S_1 S_0 are preserved.

For each branch, W^8=h*m I gives the numerator B=sum_{k=0}^7 W^k and denominator d=1-h*m. The stage numerator A=sum_b B_b product_{c!=b}d_c and denominator D=product_b d_b therefore give N=A_1 A_0=Delta M. Each N entry is multiaffine in the four separate moving-edge variables: a path of length at most seven uses an edge at most once, and all other-branch guards involve disjoint variables.

The polynomial reciprocal numerator Ntilde=(product x_j) conjugate(N)(x^-1) does not transpose N. On the unit torus, H=N entrywise Ntilde equals a common nonzero scalar times |M|^2. Complex invertible diagonal row/column scalings of a Fourier matrix have rank-one entrywise squared modulus, even with permutations. Thus vanishing of the 784 original H minors is a valid necessary condition, with no additional entry or determinant guard.

### 2. Pole division is globally valid

Coefficient conjugation, reciprocal variables and transpose give W^dagger=W^-1, hence G+G^dagger=I. Clearing this identity gives exactly the stated stage reciprocal formulas, and in particular Ntilde=c_1 c_0(3D_1 I-A_1^T)(3D_0 I-A_0^T). The product order was independently checked and is essential.

Modulo any active guard, B has the polynomial rank-one factorization u v^T with u_j v_j=1. It makes H have equal columns at a stage-0 pole and equal rows at a stage-1 pole. This remains true when another guard also vanishes: the scalar multiplying u v^T is allowed to be zero. Therefore every centered entry K_ij=H_ij-H_i0-H_0j+H_00 is divisible by every active guard. These are pairwise coprime primes in separate variables. Their product F divides K in the polynomial ring, and E=K/F is multiaffine by degree additivity. This is polynomial divisibility, not numerical interpolation, saturation, or localization away from a discarded pole.

### 3. The new rank-69 support theorem is correct

Use affine coordinates y_j=1-h_j x_j. If stage t has all three branches active, let J be the ideal of those three y variables. Then A_t is in J^2 and D_t is in J^3. Both N and Ntilde have entries in J^2, so H and K are in J^4. In K=F E, the factor F has exactly degree three in these variables, times a nonzero polynomial in the opposite-stage variable. Polynomial coefficient uniqueness implies E is in J. No guard is inverted in this argument.

Thus every 2x2 minor T of E lies in J^2 and is coordinatewise of degree at most two. Its full characteristic-zero support is contained in all exponent vectors in {0,1,2}^4 whose total degree in the three fully moving stage variables is at least two. This space has (27-4)*3=69 monomials. The proof establishes support before reduction modulo a prime; numerical zero coefficients are only supplementary checks.

The rank deficiency from 81 to 69 is consequently not a failure or a unit-ideal certificate. All T vanish on the common triple-pole stratum, so 1 cannot lie in their ideal. The target y_j^2, where j is the fully moving stage's branch-zero variable, belongs to the complete 69-monomial support and is nonzero throughout the legal guarded domain.

### 4. Exact characteristic-zero certificate

For the recorded 69 equation rows and every one of the 69 support columns, let C be the exact Gaussian-rational coefficient matrix. A nonzero specialized determinant proves d=det(C) is nonzero in characteristic zero. The adjugate identity has the correct orientation:

    d*y_j^2 = sum_r cofactor(C)_(r,k) T_r,

where column k is y_j^2. The polynomial Cauchy-Binet identity with row and column signs (+1,-1,+1) gives F^2 T as the stated nine-term signed sum of original H minors. Hence d F^2 y_j^2 lies in their original ideal. Its value is nonzero on the original guarded unit torus, which proves the exclusion.

All coefficients belong to the stated Gaussian localization. Division by 1-h*x uses constant coefficient one; the guard-coordinate change uses only the already available h^-1. All 68 Gaussian factors are nonzero at both finite-field coefficient-ring maps. This is not an impossible field embedding Q(i) into F_p, nor a lift of finite-field rootlessness or modular row-space membership with unproved support.

## Independent reconstruction and controls

The reviewer wrote reconstruct.py from the chart and mathematical definitions. No author or historical scientific program was read, imported or executed. The author's certificate JSON was used only as inert frozen data for labels, rows, columns and expected determinant values. Selected rows were replayed as recorded, without replacement.

The independent implementation:

1. Reconstructs every directed weighted path and stage numerator from the original chart in each embedding.
2. Forms the opposite-embedding reciprocal numerator independently, convolves all coefficients, and double-centers all 81 positions.
3. Recovers E by formal constant-one guard division and checks complete F*E=K multiply-back in all 81 positions, not just a truncated subset.
4. Performs the affine guard substitution; checks E in J and checks every excluded coefficient of all 441 minors before selecting the proved 69-column support.
5. Reconstructs and replays all 2,176 recorded 69x69 determinants in each embedding: 4,352 nonzero residues agree exactly. It checks every label once, complete coverage, all support columns, and recorded original holonomies.
6. Uses row-pivot Gaussian elimination independently of the author's recorded pivot-column sequence. NumPy integer arithmetic is exact here: the largest un-reduced 256-term coefficient accumulation is below 2^42, far below the signed 64-bit limit. All matrix products have eight terms and are likewise safe.

The complete replay passes in ordinary Python and Python -O; explicit exceptions, not removable assert statements, enforce checks. A separate fresh exact Gaussian-rational control verifies two original model fixtures, one in each orientation, N=Delta M, reciprocal matrix order, the unit-torus modulus relation, and all four active pole directions. Another independent exact-integer control checks all 441 Cauchy-Binet identities on three unrelated matrices, 1,323 identities total.

Negative controls reject a changed determinant residue, detect singularity after deleting a required support column, distinguish the conjugate embedding's determinant, and retain the triple-pole base locus that forbids a unit-ideal conclusion. These controls supplement the proof rather than substitute for it. The author's additional controls are not labeled independent reviewer evidence.

## Source and candidate pins

The exact accepted author manifest is SHA-256 88a31df561f57197a939ae6c59d6901316f3786110b19caed43d641d0137cba7. Its 17 listed files have been byte/hash checked. The accepted final proof is c39559235d8cab8a6f0f186dba9a19f67c33f4da70d7f91c82342072d4354f72. The final two proof changes from the first reviewed draft clarify “holonomies different from 1” and document author controls; they do not change the mathematics.

The primary complete certificate file is 5fe6530d9114ec59cfbc7120b8072ecf792f9a16f6637fa9df11869fe33439e8, and the conjugate complete certificate file is 4cdcb50a65176535d77bf27adbb2d49f6d36697259634fb00d5c98d10c820c31. All have been independently reconstructed as described above.

The source chart is pinned to repository AgentSlop-Si/research, commit 3834be7716370cfddf84ab1200da62b7887feb05, path math/finalized/2026-10-19-q27-four-phase-same-branch/candidate/sources/CHART.json. The accepted predecessor proof, review, verdict and source ledger are retained as inert source copies and hash-matched to the locally accepted packet. Repository publication state itself is not audited here; this is a mathematical review, not a Git or table audit.

No external state has been changed. Publication and table synchronization are separate from this scoped mathematical acceptance.

## Reproduction

Set Q27_CANDIDATE_DIR to the frozen candidate directory. From the review directory run reconstruct.py with the two complete certificate JSON paths and a result JSON output path. Run exact_controls.py separately. Repeat with Python -O if desired. No author executable is needed. BINDINGS.json pins the exact candidate and source bytes; MANIFEST.json pins this independent review and its own fresh code/results.
