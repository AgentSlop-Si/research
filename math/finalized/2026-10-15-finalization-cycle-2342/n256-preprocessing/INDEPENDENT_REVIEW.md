# Independent N256 feasibility-reformulation review

Reviewer: separate adversarial reviewer, 15 October 2026 UTC.

## Verdict

**PASS, scoped mathematical reformulations only. REJECT any Fourier-feasibility closure, infeasibility, novel-theory, or speedup claim.** The candidate consists of standard elimination, rank factorization, and polynomial lifting specialized to the frozen N256 architecture. It does not provide an admissible Fourier root or exclude all such roots. The recorded completion gate remains open.

The final reviewed candidate is `n256_chart_free_reduction_20261015/REPORT.md`, SHA256 `29ac3bbee71006056cba722c72d72bb714bc9af99ae8bcbc9af59ec5371e69c0`. Its complete text was read after the author froze it. The author correctly preserves all qualifications below; no required correction remains for these scoped claims.

## 1. Independently verified source and scope

The reviewer fetched the archived NEXT_ACTIONS.json at private repository commit `e5c9c53f7d34e8d858e781d2d5321393aec7e85c` and independently read the live workbook's `Research overview!A139:Q139` and `Incoming queue!A33:L34` after checking metadata. Overview139 remains TO RESEARCH. Its completion evidence is an exact admissible Fourier root or complete infeasibility certificate, with middle-stage compatibility and full coefficient verification. Recorded local Phase52 path isolation is not global exclusion.

The complete source formulation and fixed layout were read and freshly SHA256-matched:

- Formulation: `9e3936a8c45f0d912beac775e73f57a66e3ac638fe1ceca04be3c9b4492ab490`.
- Layout: `77c5c0fcdcfa850dac44dd34dbe3188539aa9cb143f22978b86127add76b8e45`.

The archived scripts were inspected as text, not imported or run. Their bytes were independently hash-checked:

- `four_stage_operator.py`: `8af7b12ae29cc863061571f46f5469103257664bbf5b14c2712848b756fc54db`.
- `quadratic_feasibility.py`: `ca2acaafe7cfd8e584cfd246e73f763d8614d1bf54a8c0f39ea64a0c3d27a1f8`.
- `kernel_lift_gate.py`: `2de52fb9e97dbbeab268f17013b0f98164b099e6b2240b63703ff374a7a60dd7`.
- Prior saturation archive: `2b712be2a70f7293a0c7d59ef2ed08c66b0c845f329e0afa2a38fd114cda90cc`.
- Prior saturation proof: `5442a65785ccca406582c567d84bdb96550ab24fc1f3af0e0d4ec16baf795a09`.
- Prior saturation specification: `b2bcac2846254fce7f162b8e71cd88f4d467e09223d1eaefab64f1c3a4bb790c`.

The live row preserves corrections to the older saturation prose. In particular, high Taylor order at a singular point does not establish an irreducible singular component, and determinant nonvanishing over fields must become determinant-unit conditions over rings.

## 2. Exact target, orientation, and middle stages

Let ζ be the positive primitive 256th root and U[i,j] = ζ^(ij)/16. The frozen target is

`S4 P3 S3 P2 S2 P1 S1 = U`.

Each separated stage has entries `a_i b_j` for i>j, `d_i` for i=j, and `c_i e_j` for i<j. The permutation convention is `(P_s x)_i = x[p_s(i)]`. Only the three arrays in `affine_shuffle_columns` are used. The archived Toffoli list is not part of this model.

Fresh reviewer-written 256-element enumeration, without importing supplied code, gives 256 distinct images for each permutation, cycle counts 4, 4, 2, and even parity for all three. This is source/convention checking, not new feasibility evidence. The positive normalized transform has determinant +i; the negative-exponent convention would change that sign. The already accepted product-determinant necessity is not an obstruction for arbitrary middle determinants.

With invertible outer stages, define

`G = P1 S1 U^-1 S4 P3` and `H = G^-1 = P3^-1 S4^-1 U S1^-1 P1^-1`.

A sufficient middle completion must exhibit actual separated-generator S2,S3 with `S3 P2 S2 = H`. A rank-factorization witness for one or even all known subblocks of G does not furnish that completion. Rank-one cut conditions also must not silently replace the stronger globally separated generator class on exceptional zero/reset branches.

The full Fourier equality forces every stage determinant to be nonzero over the field, so the full model needs no separate saturation. An isolated gate involving only outer generators still needs outer determinant guards. Finite-field synthetic controls do not supply a complex Fourier witness, and a failed saved parameter point is not global infeasibility.

## 3. Fixed-basis first-stage elimination

For input basis column j, the first stage's scan coordinates are uniquely

`L_i = b_j` if j<i and zero otherwise; `R_i = e_j` if j>i and zero otherwise.

Substitution eliminates exactly `2 N (N-1) = 130560` auxiliary coordinates and the same number of recurrence equations. The inverse map reinstates these explicit values, so there is neither division nor chart loss. Retaining the stage-2 input variables keeps all remaining equations degree at most two and support at most four. Eliminating those inputs as well would require a new degree audit.

The full model therefore changes from 723968 unknowns / 784384 equations to **593408 unknowns / 653824 equations**, before removing the 16 matrix-unused coordinates. Fixing `a_0,b_255,c_255,e_0` in each of four stages subtracts 16 unknowns, giving 593392, without altering matrix feasibility. These are counts of a complete equivalent system, not a solution to it.

**Disposition: PASS exact preprocessing; no new obstruction or feasibility conclusion.**

## 4. Chart-free factorization of the one mask64 gate

For the selected 128×128 block B=G[I,J], replace its rank≤16 condition by

`B = C D`, with C of shape 128×16 and D of shape 16×128.

Over any field, a factorization implies rank≤16. Conversely, a rank-r matrix, r≤16, has an ordinary rank factorization of width r; append zero columns and rows to obtain width16. Thus lower-rank, zero-matrix, and all kernel-chart branches are covered. No invertible 16×16 factor minor or other generic normalization is required. Nonuniqueness/gauge is allowed. This is a standard algebraic characterization, not a new theorem about Fourier feasibility.

The rank-factor variables number4096 and equality equations number16384. The raw separated-generator degree is at most4 because each outer matrix entry has degree≤2 and G is bilinear in those two outer matrices. It is degree≤2 in independent outer matrix-entry coordinates, but those coordinates themselves require structure equations if introduced as unknowns. The original sparse support≤4 claim does not carry over to these dense equations.

There are2560 raw outer generator coordinates, including8 matrix-unused coordinates. Under the archived cubic saturation convention, each outer stage adds515 coordinates/equations:514 states u_0..u_256,v_0..v_256, plus eta, with512 transitions,2 boundary equations, and `eta v_256 = 1`. Both stages add1030.

Consequently the direct guarded **one-gate** formulation has **7686 unknowns /17414 equations**, maximum degree4. These are not complete four-stage feasibility-system counts. Omitting the1030 guard coordinates/equations requires explicitly stating a different nonvanishing mechanism or working on a previously justified open domain.

**Disposition: PASS field-equivalent one-gate encoding; REJECT any claim that rank factorization proves middle compatibility or full Fourier feasibility.**

## 5. Quadratic one-gate core and its cubic guards

Let J be ordered, let q_j = p3^-1(j), and set M=U^-1. Define256×128 variables T by

`T_ij = M_iq d4_q + b4_q sum_(k>q) M_ik a4_k + e4_q sum_(k<q) M_ik c4_k`.

This is exactly `T = U^-1 S4 P3[:,J]`, using the verified pullback permutation convention. It has32768 coordinates/equations; each expanded equation has degree≤2 and at most257 terms, counting T itself.

Introduce the prefix and suffix states for applying S1 to all128 T columns, with the two boundaries fixed as literal zeros. These contribute `2(N-1)·128 = 65280` states and equations. For each i in I put h=p1(i). Enforce

`d1_h T_hj + a1_h L_hj + c1_h R_hj = sum_(ell<16) C_i,ell D_ell,j`.

There are16384 final equations, degree≤2 and support≤19. The scan equations have support≤3. The exact equalities, not a probabilistic or sampled test, establish equivalence to B=CD.

The core count is2560 raw generators +32768 T +65280 scan coordinates +4096 factors = **104704 unknowns**. Its equations number32768+65280+16384 = **114432**. Adding the archived1030 cubic saturation coordinates/equations gives **105734 unknowns /115462 equations**, maximum degree3. The complete guarded encoding is therefore not quadratic under that convention. Further quadratization of the determinant recurrence would need a separately specified count.

This representation trades many more auxiliary variables and equations for a lower degree. No generic solver improvement, practical tractability, or runtime benefit has been demonstrated. It remains a single necessary gate.

**Disposition: PASS exact one-gate reformulation and counts; REJECT unchanged support≤4 or fully quadratic guarded-system claims.**

## 6. What is and is not completed

The current recorded stopping evidence is not met. There is no exact root, no complete all-chart exclusion, no compatible middle-stage construction, and no all-coefficient Fourier verification. The new descriptions may be recorded as scoped preprocessing with the stable record still open. Do not increment theorem/discovery counts, promote novelty, or claim a faster FFT.

The remaining concrete mathematical gate is either an exact separated four-stage assignment with every Fourier coefficient proved, or a complete impossibility proof for the fixed affine model. No single chart, finite family of synthetic controls, local path isolation, generic dimension count, or necessary rank condition substitutes for that gate.

## 7. Review limitations and operations

Read-only external connector access; no repository or workbook writes. Local report and source-receipt files only. No supplied program execution/import, package installation, solver invocation, or denied-network retry. The only fresh mathematical computation beyond arithmetic counts was a tiny reviewer-written permutation enumeration. Historical numerical/modular checks were read as evidence, not rerun or claimed as new execution.

This is a mathematical/static audit, not a compiled formal proof or an implementation verification. Statements extending field rank factorization to arbitrary commutative rings are expressly outside acceptance.
