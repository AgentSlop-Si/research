# Independent audit: HERO0 Phase 23 coupled transverse-path claims

Audit date: 2026-10-10. Source: `fft_hero0_phase23_coupled_dual_bridge_2026-10-10.zip`. Original source archive identity is recorded in SOURCE_ARCHIVE_LEDGER.json at the export root. Archive SHA-256: `cee9c1cfdea48bdbc4597568237d39f2f838a943eb45c7f58274619a6138cc82`.

## Verdict

The rank-product theorem, uniform full-matrix Frobenius lower bound, homogeneous-crossed-pair corollary, and effective nonreal-entry budgets are mathematically valid within the explicitly specified model. The proofs do not require either path to be fixed, real, or inactive. They do not settle the high-transverse-rank two-stage family, alternative endpoint orderings, or general Fourier-transform complexity. The statements already qualify these limits appropriately.

No source-supplied program was executed or imported. The new checker reads source JSON only as data. All 12 entries of the archived SHA-256/size manifest were verified. The source ZIP is the authoritative mathematical source for this audit.

## 1. Exact model and path identity

Let N=s², flat coordinates sx+y, and use the unnormalized positive-sign Fourier matrix F[i,j]=exp(2π i i j/N). Consider exactly two factors T=(Y_H+Y_V)(X_H+X_V), where H preserves the second coordinate and V preserves the first. All four supported matrices may be arbitrary complex, singular, dense within fibers, and jointly adjustable. There are no assumptions about positivity, inverse existence, parameter independence, or Green formulas in the proof.

For x≠a and y≠b, only intermediate vertices (x,b) and (a,y) can contribute. The H-H and V-V products vanish there. With x,b fixed, the (s−1)×(s−1) output block is uvᵀ+A⊙B, with A[y,a]=Y_H[(x,y),(a,y)] and B[y,a]=X_V[(a,y),(a,b)]. The transpose is not conjugate-transpose. Fixing y,a yields the mirrored identity for the other crossed pair.

These two partitions contain the same off-rook entries in different arrangements. Their error lower bounds may be maximized, not added. On-rook and diagonal equations remain unexamined; meeting every derived off-rook gate is not sufficient for a full factorization.

## 2. Fourier rank and the rank-product gate

Expanding (sx+y)(sa+b) modulo s² gives the block as a unit-modulus scalar and row diagonal times F_s with one row and one column removed. Its Gram matrix is sI−vv*, with ||v||²=s−1. The eigenvalues are s repeated s−2 times and 1 once; hence the singular values are √s (s−2 copies) and 1, and the rank is s−1. In the mirrored orientation the analogous phases occur on columns instead.

If rank(A)=r and rank(B)=u, tensoring their rank-one expansions gives rank(A⊙B)≤ru over any field. Therefore rank(T_block)≤1+ru and exact equality with Fourier forces ru≥s−2 for every block. Both orientations must satisfy their respective inequalities for the same factorization.

The complex proof is all-length. The finite-field analogue needs an appropriate primitive Nth root for F_N; the punctured F_s rank fact only needs a primitive sth root and characteristic not dividing s. Invertibility of the Fourier matrix and nonzero inverse entries prove every relevant cofactor nonzero. Finite-field data are consistency checks, not the sole bridge to the complex theorem.

If each of the two transverse ranks is ≤r, then r²≥s−2. This Ω(N^(1/4)) necessary rank scale is a rank statement, not an arithmetic-operation lower bound.

## 3. Approximation and normalization

Assume, in one fixed orientation, r_xb u_xb≤ρ for every block, with integer rank budget 0≤ρ≤s−3. Each approximating block has rank≤1+ρ. Removing its at most 1+ρ largest singular directions leaves squared Fourier tail energy s(s−3−ρ)+1. The s² blocks partition all off-rook entries without overlap, so their errors sum to at least s²[s(s−3−ρ)+1]. Since F has N²=s⁴ unit-modulus entries, ||F||_F²=s⁴. Dividing yields

relative error squared ≥ 1−(3+ρ)/s+1/s².

The square root is the reported relative Frobenius lower bound. In particular, ρ=o(s) gives a lower bound tending to 1. It does not claim the actual error tends to exactly 1. The same relative bound holds with a consistent normalized Fourier target and corresponding scaled candidates, because rank is unchanged and numerator/denominator scale together. It is an aggregate full-matrix error statement, not a per-input error guarantee or a spectral/operator-norm bound.

For heterogeneous rank products, the proof also supplies the direct sum of the applicable per-block tail bounds; the single-ρ formula needs the uniform hypothesis. When ρ≥s−2, this argument gives no positive bound. The radical should not be extrapolated outside the stated range.

Homogeneous Y_H independent of horizontal fiber y makes A rank≤1; homogeneous X_V independent of vertical fiber a makes B rank≤1. Thus ρ≤1 regardless of the other two matrices. For s≥4, 1<s−2, so exact Fourier equality is impossible and the lower bound is √(1−4/s+1/s²). This also covers sums of replicated fiber kernels. It does not cover arbitrary fiber-varying Green kernels just because each individual resolvent has a short application algorithm.

## 4. Effective nonreal-entry budget

Let m=⌊(s−1)/2⌋. For s≥3, choose one available row from each nonself-conjugate Fourier frequency pair, avoiding the deleted row. The imaginary rows, including the row phases in this block, are orthogonal before column deletion with squared norm s/2. Removing one column changes their Gram matrix to (s/2)I−vvᵀ with ||v||²≤m. Hence at least m−1 singular values are ≥√(s/2), and the mth is ≥√(s/2−m)>0. Transposition gives the mirrored result. At s=2, m=0 and the rank/count claims are trivial; references to an mth singular value should simply be omitted.

The imaginary part of a complex outer product has real rank≤2. If q_xb positions in A or B contain a nonzero imaginary part, then Im(A⊙B) is supported on at most q_xb entries, hence has rank≤q_xb. Thus q_xb≥max(m−2,0). Every relevant nonreal off-diagonal effective factor entry is charged in at most s−1 blocks. This proves, separately for each crossed pair,

q ≥ ceil(s² max(m−2,0)/(s−1)).

Counts are 86 per pair at s=16 and 1886 at s=64. They approach N/2 per crossed pair, or N across both pairs. The budget counts effective matrix entries with multiplicity across the two matrices. It does not count independent complex parameters, edges, gates, or operations. A single complex edge may make many entries of its Green inverse nonreal.

For approximation, the proven sine singular tail gives per-block squared error ≥(s/2)max(m−3−q_xb,0). Summing and charging as above yields the source's squared relative bound max(0,(m−3)/(2s)−(s−1)q/(2s³)). Thus q=o(N) for either pair implies liminf of relative Frobenius error ≥1/2. This is valid but weaker than retaining the last positive sine singular value or using each block's full exact spectrum.

## 5. Gauge and architecture qualifications

- The target, coordinate ordering, and chosen factor realization are fixed. The imaginary support count is phase/gauge dependent, and individual transverse ranks need not be invariant under arbitrary intermediate diagonal gauge changes.
- An intermediate gauge X↦DX, Y↦YD⁻¹ preserves the product and rook support but can change ranks of transverse views and imaginary support. Any realization of the fixed Fourier target must still obey the theorem in that realization; no gauge-invariant parameter lower bound follows.
- Arbitrary input/output permutations can change the punctured-Fourier block structure. They require a separate analysis; the source explicitly does not include them.
- The rank is that of a transverse view of effective fiber entries. A Green resolvent is normally full rank as an operator; the theorem does not assume its global matrix rank is small.
- High transverse ranks can pass both gates while the nonlinear Fourier equations remain unsatisfied. Passing these necessary conditions is neither existence nor an implementation.
- The theorem applies only to exactly two rook-supported stages in this arrangement. Additional stages, different supports, other coordinate layouts, high-rank varying fibers, and general arithmetic circuits are not excluded.
- No external priority or novelty conclusion was audited. No faster FFT or complexity lower bound follows from these certificates.

## 6. Fresh bounded verification

Checker: `verify_phase23_fresh.py`. Machine-readable result: `phase23_fresh_receipt.json`.

- Verified primality of 65537 and order 65536 of 3, then root orders for the tested power-of-two transform lengths.
- Recomputed the declared 3×3 determinants as 1024, 8736, 36857, 17660 for s=4,8,16,32.
- Recomputed six punctured Fourier ranks per tested side (three fixed blocks, both orientations), each equal to s−1 by exact modular elimination.
- Directly built 2,982 full-Fourier subblocks over s=3…16, both orientations. Their complex singular values matched √s (s−2 times) and 1 to numerical tolerance; all sine rank and lower singular-value claims held. Independently tested the selected-sine-row Gram formula.
- Fresh arbitrary complex rook factors satisfied the exact two-path decomposition to floating precision. Homogeneous crossed-pair controls had transverse rank product 1 and off-rook block rank≤2; unrestricted controls had high transverse ranks, illustrating where this obstruction is vacuous.
- Built four genuine cyclic Green resolvents per example by independent linear solves at s=4,8,16. Their full complex-matrix relative errors exceeded the proven bound in every case.

The floating checks corroborate algebraic identities; they are not substitutes for the all-length proofs above. Archived statements that 105 old/new tests passed were not independently rerun. The prior nested archive was hash-verified only; predecessor proofs were outside this audit.
