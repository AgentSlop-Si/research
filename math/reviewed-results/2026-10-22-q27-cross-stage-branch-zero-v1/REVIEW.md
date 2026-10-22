# Independent review: Q27 four-branch cross-stage exclusion

## Verdict

ACCEPT the bounded mathematical theorem, bound to the final bytes in `VERDICT.json`. This is not a Q27 owner closure, a full-fiber exclusion, a Fourier construction, a complexity result, or a novelty-priority conclusion.

For every e0,e1 in {8,...,23}, the original N=8 chart with only encoded gains [7,e0,31,24+e1] independently multiplied by complex unit phases has no externally invertible-complex row/column monomial equivalence to F8 on its original six inverse guards. Exactly 256 four-coordinate labels are covered. The 512 label/embedding replays are two arithmetic checks of those same 256 labels, not 512 different families.

## Source and actual-family binding

The chart is the 3,138-byte source with SHA-256 `5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98`, Git blob `d0a7a859b27574b0fd327587ba9e831984a98714`. It was independently fetched from the immutable 19 October predecessor. Its bytes equal the producer chart and the accepted 20 October whole-branch chart. `SOURCE_CHART_FETCH.json` records the fetch.

The Q27 record was independently fetched at commit `3834be7716370cfddf84ab1200da62b7887feb05`, path `math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json`, blob `fb3e4cff3c4d01e7b4d870215db875997d752847`. The Q27 projection exactly matches the producer's record. It explicitly leaves other four-coordinate placements open and asks for a distinct exact multi-coordinate result in the original chart with all six guards. This record predates the accepted 20 October whole-one-branch theorem, which was separately inspected and preserved, not forgotten or repeated. The later classification snapshot SHA-256 `944adf53e5d26584aa506e3c753df0dd4d4214d5785fc9bbbd337a42d10ff34d` was independently hash-checked; its Q27 row explicitly retains branch-zero and simultaneous-multibranch obligations, while stating that no automatic successor is assigned. The present separately selected review addresses one such remaining obligation and does not authorize automatically generating further slice batches.

The new labels have two variables in each stage, one on the sole free branch-zero edge and one on either fully free branch. All four variables can vary simultaneously across four different branches. No accepted triple or one-whole-branch theorem contains such a four-dimensional family. Some boundary subsets, obtained by fixing variables to 1, are naturally already covered by old results; the point sets are not asserted disjoint. No old result or numerical failure is relabeled as new evidence.

Both seeds 42420/42520, all six directed cycles, all 34 Gaussian-rational gains, fourteen fixed unit tree edges, unweighted three-inverse stage sums, and M=S2*S1 are retained. Edge 8b+j sends cycle[j-1] to cycle[j]. No diagonal, branch weight, anchor nonvanishing, determinant of M, nonunit gain, root-of-unity restriction, or witness change is introduced.

## Proof audit

1. In K=Q(i), define B=I+W+...+W^7, d=1-h*m, D_t=product of the three guards, A_t=sum B times the other two guards, and N=A_1 A_0. The weighted-cycle identity proves N=Delta M on exactly the original inverse domain. Disjoint branch variables and paths of length at most seven prove N is coordinatewise affine.
2. With R=x0*x1*x2*x3, Nt=R*bar(N)(x^-1) has coefficient conjugation but no transpose. H=N entrywise-multiplied by Nt is polynomial of coordinate degree at most two. On the unit torus, H=R|Delta|^2|M|^2. Arbitrary external invertible complex monomial transformations of F8 still force squared-modulus rank one. Thus the 784 H minors are valid necessities, not asserted sufficient conditions.
3. The cleared reciprocal identity preserves the order A_1 A_0: Nt=c1*c0*(3D1 I-A1^T)*(3D0 I-A0^T). Reversing these factors would be wrong. Polynomial clearing allows zero phase coordinates in the algebraic identities without claiming physical unitarity there.
4. Modulo any moving guard 1-h*xj, the relevant cycle has B=u*v^T with u_k*v_k=1 and B_00=1. These are identities over the quotient ring. The other guard factors are not inverted. Stage-0 poles give identical columns of H; stage-1 poles give identical rows, including intersecting poles.
5. Let L have rows e_r^T-e_0^T, r=1,...,7. Then K=LHL^T is divisible by each of the four prime, pairwise nonassociate guards. Their product F divides K. This uses coprime factors in the polynomial domain, not a false assertion that their ideals are comaximal. E=K/F is multiaffine by degree additivity. Sequential constant-term recurrences keep its coefficients in the Gaussian localization.
6. Rank(H)<=1 implies rank(K)<=1, and rank(E)<=1 uses only the original F!=0. The 441 E minors T have complete support contained in all 81 monomials {0,1,2}^4. This is a characteristic-zero degree theorem, not a support projection inferred from modular zeros.
7. Each F^2*T is exactly a nine-term signed combination of original H minors. For the two row pairs and two column pairs, the lists [(0,a),(0,r),(a,r)] and [(0,b),(0,c),(b,c)] both have signs [+1,-1,+1]. All nine signs and the generator normalization were checked.
8. For each fixed 81-row coefficient submatrix C using all 81 columns, its nonzero reduced determinant proves d=det(C)!=0 over Q(i). Cofactors of the constant-monomial column give d=sum_j cofactor(C)_(j,0)*T_j. Hence d*F^2 belongs to the original H-minor ideal I. Thus I:F^infinity=(1) over Q(i). In particular I:(R*F)^infinity=(1), but no extra use of R!=0 is needed for the ideal contradiction. Only the original guards are removed.

The proof defines the original polynomial generators explicitly, avoiding any silent identification with differently cleared historical Laurent equations. No literal multiplier transport between equal-holonomy slices is used.

## Coefficient field, roots, and specialization

The coefficient ring is A=Z[i,(a+ib)^-1,(a-ib)^-1 for all 34 source pairs]. All gains, conjugate gains, holonomies, and inverse holonomies lie in A. No guard is inverted to construct N,H,E,T or their coefficient matrices.

Complete trial division verifies p=65537 is prime. The images i=256 and i=65281 both satisfy i^2=-1, and every inverted Gaussian factor has nonzero image. Thus A maps to F_p in either way. This is a coefficient-ring homomorphism, NOT a field embedding Q(i)->F_p, which cannot exist. Conjugation is evaluated via opposite embeddings, not a finite-field absolute-value operation or a residue-field automorphism fixing every residue.

A nonzero determinant image certifies a nonzero original determinant. It does not lift a finite-field solution, and no finite-field rootlessness assertion is used. The theorem concerns the characteristic-zero complex unit-phase problem. It is not claimed uniformly in arbitrary characteristics: denominators, determinant images, and the interpretation of conjugation require their own checks there.

No primitive eighth root occurs in the coefficient matrices; only the complex Fourier target's flat moduli are used. No extra compatible-root assumption is imposed on the four phases. They are arbitrary unit complex numbers, not just roots of unity or elements of Q(i).

## Independently authored execution

No producer program or historical program was run, imported, or compiled. All producer programs were treated as read-only text. The new independent control reconstructs the weighted matrices and B by polynomial matrix powering, rather than tracing the producer's paths. It divides by guards by descending leading-term long division rather than the producer's constant-term recurrence, then multiplies the entire product back. It reconstructs every coefficient of every full 441-by-81 matrix and replays only the originally selected fixed minors, with ordinary row-pivot determinant elimination. No replacement minor is selected.

Results:
- 256 labels in each of two embeddings, 512 complete instances.
- Every full coefficient-matrix hash agrees.
- Every specified 81-by-81 determinant agrees and is nonzero; pilot [7,8,31,32] gives 47914 modulo 65537.
- Every guard division and complete coefficient multiplication-back succeeds.
- 4,608 evaluations against independently computed actual six Green inverses agree with N=Delta M, including 2,560 zero-coordinate algebraic controls.
- 2,048 moving-pole collapse checks pass.
- 3,969 nine-term identities pass on arbitrary test matrices, not only candidate matrices.
- Supplementary exact Q(i) controls on [7,8,31,32] and [7,23,31,47] pass 288 cycle/inverse polynomial identities, 12 cleared reciprocity checks, and 8 pole-collapse checks. These supplement, not replace, the uniform symbolic proof and all-label replay.
- Deleting the constant column and duplicating a selected row make the determinant zero; swapping two rows negates the pilot determinant. These negative controls are detected.

The modular arithmetic uses exact integers. Matrix products contain at most eight residue products per entry, bounded by 8*(65536)^2<2^36. All other unreduced convolution and elimination values also remain far below signed 64-bit range; no floating-point arithmetic is used in the modular reconstruction. The exact rational control uses Gaussian rational arithmetic.

## Mathematical usefulness and remaining boundary

This is a legitimate but bounded advance against the source-named distinct-multi-coordinate gate. The useful structural addition is simultaneous row-and-column pole removal, which makes the original cross-stage family admit a small exact certificate. It is not merely another rerun of known triples or same-branch cases. The 256 placements are the complete natural family specified by both branch-zero phases plus one other original edge in each stage, not arbitrary successful pilot labels cherry-picked after failed certificates.

Its impact should remain modest: it resolves one four-dimensional family around one original witness. It does not supply a strategy completing the full 34-phase fiber or all branch-zero motions. Q27 remains open at its unchanged priority. Do not count this as finishing the table row, a positive Fourier factorization, an FFT speedup, or a historical novelty result. A separate three-branch rank-69 exploratory pilot is outside this theorem; neither its rank deficiency nor the successful family entails anything about its feasibility.

No external write, publication, table edit, or status change was made by this review. No mathematical counterexample or unresolved theoretical gap was found in the accepted scope.
