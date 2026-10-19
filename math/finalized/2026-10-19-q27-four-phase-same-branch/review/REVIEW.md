# Independent review: Q27 four moving phases in one original branch

## Verdict and scope

ACCEPT, narrowly: all 280 prescribed original-chart same-branch four-coordinate slices are excluded on their original guarded unit-phase domains. The accepted candidate is bound by MANIFEST.json SHA-256 45ccd9b65629ec16415750c341da7b4dbb086c770d0189b89c566cd224284ecc. All 17 required files, totaling 715,901 bytes, were independently byte-verified and copied into input/candidate/.

This review concerns exactly 280 labels: stage 0 or 1, fully free branch 1 or 2, and four of that branch's eight original free edges. The variables are assigned in ascending original edge order, which is cyclic order on that branch. The original N=8 chart, seeds 42420/42520, all six cycles, fourteen fixed unit tree gains, 34 witness gains, six inverse guards, unweighted three-Green stage sums, and product M=S2*S1 remain unchanged. Branch zero is outside this family because it has only one free coordinate. The result does not close Q27, the full 34-phase fiber, other four-coordinate families, five-or-more-coordinate motions, other witnesses, or other dimensions. No historical three-coordinate program was executed or adapted.

## Source and arithmetic reconstruction

The three accepted source files were independently SHA-256 checked against the exact bindings in the selection packet. In particular CHART.json is the original 3,138-byte source with hash 5528afbbd5b4008a5e0f79043870e72a613e0fd421288d2ce1e5dbffee1c9e98. The new independent source check verifies the two seeds, six length-eight permutations, all 34 Gaussian pairs, free-edge set 7 through 23, unit sum coefficients, and stage order.

The independent implementation computes each gain as

((a^2-b^2)+2ab i)/(a^2+b^2).

Exact rational arithmetic checks all 48 gains have norm one, all six holonomies have norm one and are neither zero nor one, and all denominator images are admissible in both modular embeddings. Four-coordinate labels are enumerated independently, giving 70 for each of the four stage/branch choices.

The verifier does not use the author's path-polynomial construction. At every point of {0,1}^4, in each Gaussian embedding, it constructs each of the six matrices I-W directly from the original edge convention, inverts them, sums the three inverses in each stage, forms S2*S1, and multiplies by all six guards. Each inverse is checked on both multiplication sides and its elimination determinant is compared to 1 minus the actual branch holonomy. Boolean difference interpolation recovers all sixteen coefficients of each multiaffine cleared numerator entry. The multiaffine bound is proved below, so interpolation is complete. Zero interpolation coordinates are legitimate polynomial evaluation points; every guard there is either 1 or its verified nonzero frozen value.

## Original division-free equations and divisibility

Let K=Q(i), R=xyzw, and let the one moving branch have holonomy hR. The A and D subscripts below use the certificate's zero-based stage indices 0,1; the physical Green-stage product remains M=S2*S1. Its active guard is F=1-hR. Every other guard is a fixed nonzero constant. For each branch,

B=I+W+...+W^7, d=1-h_b m_b,

and for each stage,

D_s=product_b d_sb, A_s=sum_b B_sb product_{c!=b}d_sc.

The weighted-cycle identity W^8=h_b m_b I gives (I-W)B=dI on both sides. Thus N=A_1 A_0=Delta M, where Delta=D_1 D_0 is a nonzero constant times F. Every path of length at most seven encounters each selected edge at most once. Products with the other branch guards introduce only disjoint selected variables. Therefore each entry of N is multiaffine.

Put Nt=R conjugate(N)(1/x,1/y,1/z,1/w), and H=N entrywise-multiplied by Nt. The 784 original polynomials P are all two-by-two minors of H, with row-pair/column-pair indexing fixed by the candidate schema. On unit phases,

P=R^2 |Delta|^4 times the corresponding two-by-two squared-modulus defect of M.

External invertible complex row and column monomials applied to F8 produce squared entry moduli of rank one. Hence all P are necessary equations. No sufficiency claim is used, and no matrix entry, anchor or determinant of M is inverted.

The ideal (F) is prime: its quotient identifies every variable as a unit and is a Laurent polynomial ring in three variables over K. Modulo F the active weighted cycle has holonomy one, and B has rank one because eigenvalue 1 of an eight-cycle is simple in characteristic zero. The other terms of the cleared affected stage carry F, so N has rank at most one modulo F. Coefficient conjugation combined with reciprocal variables preserves F up to a Laurent unit, since conjugate(h)=h^(-1). It therefore gives rank at most one for Nt on the same divisor. H, the entrywise product of two rank-one matrices, has rank at most one there. Every P is divisible by F in K[x,y,z,w]. Write P=FQ. Each P has coordinate degree at most four; degree additivity over the integral domain proves each Q has coordinate degree at most three.

## Independent proof of the new 27/126 support bounds

The originally proposed dimension146 is a valid upper bound but cannot be attained: already the first label has modular rank126. This is explained by a stronger exact bound, not by a failed Fourier search.

For formal conjugate-reciprocal transpose, W^dagger=W^(-1). Hence each branch Green function satisfies G+G^dagger=I and each stage satisfies S_s+S_s^dagger=3I. Clearing denominators gives

R_s conjugate(A_s)(reciprocals)=c_s(3D_s I-A_s^T),

where c_s=-1/(h_s0 h_s1 h_s2) is a nonzero constant. Consequently

Nt=c_1 c_0 (3D_1 I-A_1^T)(3D_0 I-A_0^T).

These are initially identities in the rational function field; both cleared sides are polynomials. They remain valid when selected variables are zero. No unitarity at zero is assumed.

First, set any one selected variable u to zero and take another variable v on a different edge of the same cycle. The active cycle is a directed path. The coefficient of v in its path numerator factors U V^T, with U supported downstream of v and V upstream. The two other selected variables may remain as polynomial coefficients in these factors; their presence does not change the disjoint vertex supports. The active guard becomes 1, so D_s is independent of v. The v coefficients of the affected stage numerator and its cleared reciprocal conjugate are scalar multiples of U V^T and -V U^T. If the affected stage is 0, multiplication by the fixed other stage leaves right factors V^T and U^T. If it is stage 1, left factors U and V remain. Their entrywise product is zero in either case. H therefore has no term with u exponent zero and v exponent two.

Since H has coordinate degree at most two, its exponents have spread at most one. This leaves 31 exponent vectors: the two cubes {0,1}^4 and {1,2}^4 with their common all-one vector counted once.

Next take opposite variables in the cyclic order of the four selected edges, for example x=z=0. Their spacings along the eight-cycle need not be equal. The cycle splits into two disjoint directed path components, one containing the y edge and the other the w edge. The affected stage numerator has the form

A=A_0+y U_y V_y^T+w U_w V_w^T.

There is no yw term because no remaining path traverses both components; the active guard is 1. All supports associated with y lie in one component, all supports associated with w in the other. Therefore the mixed yw coefficient of H is zero: for stage 0 each cross term has column factor V_y entrywise-multiplied by U_w or V_w entrywise-multiplied by U_y; for stage 1 the corresponding row factors are disjoint. Setting y=w=0 proves the other lower alternating exponent vanishes as well.

The identity H=R^2 conjugate(H)(reciprocals) transfers these two zeros to their exponent complements about (1,1,1,1). Thus all four alternating vectors are absent: (0,1,0,1), (1,0,1,0), (1,2,1,2), (2,1,2,1).

For a four-vector e in cyclic order define TV(e)=|e1-e2|+|e2-e3|+|e3-e4|+|e4-e1|. Among spread-at-most-one vectors in {0,1,2}^4, exactly those four excluded alternating vectors have TV greater than two. Every H therefore has support in the 27-dimensional monomial space with spread at most one and TV at most two.

Each P is a difference of products of H entries. Spread and TV are subadditive under addition of exponent vectors, so each P has support of spread at most two and TV at most four. Division by F preserves both constraints: the ascending coefficient recurrence is

Q_e=P_e+h Q_(e-(1,1,1,1)),

with negative-coordinate terms interpreted as zero. Simultaneously shifting all four exponents preserves spread and TV. Induction on minimum exponent proves every forbidden Q coefficient is zero. Together with the already proved coordinate-cubic bound, Q belongs to

V=span{x^e1 y^e2 z^e3 w^e4: 0<=ej<=3, spread(e)<=2, TV(e)<=4}.

Independent finite enumeration gives dimension 126. Analytically, the two cubes {0,1,2}^4 and {1,2,3}^4 each lose ten vectors: two alternating extreme-value patterns and their eight single-coordinate changes toward the middle value. Each leaves 71. Their entire 16-vector intersection survives, so the dimension is 71+71-16=126. Equivalently the initial146 cube-and-spread monomials lose exactly twenty vectors with TV greater than four. The constant monomial belongs to V. All support statements above are characteristic-zero polynomial arguments; modular support checks are supplementary controls only.

## Characteristic-zero determinant lift and all-label conclusion

Use the ring R0=Z[i,(a+ib)^(-1),(a-ib)^(-1) for all 34 original pairs]. Original gains, conjugate gains, holonomies and inverse holonomies lie in R0. N, Nt and P use only ring operations. The coefficient recurrence for division by F has constant coefficient 1 and shows directly that Q has coefficients in R0; no additional inverse guard or coefficient denominator is introduced.

Independent complete trial division proves p=1,000,000,009 is prime. The two images 569,522,298 and 430,477,711 square to -1 modulo p. Every Gaussian integer inverted in R0 has nonzero image under both maps. Hence these are genuine ring homomorphisms R0 to F_p. Coefficient conjugation is implemented by exchanging the embeddings, not by an alleged finite-field absolute value.

The independent verifier forms H from the sixteen interpolated N coefficients and the reversed sixteen opposite-embedding coefficients. It forms each requested original P in the full 625-dimensional coordinate-degree-four array, divides by F by the independent ascending recurrence, checks every coefficient outside the full 126 support is zero, and multiplies back coefficientwise. No unsupported coefficient is projected away before testing. H is likewise checked on its full 81 possible exponents against the 27-support theorem.

For each label and embedding, 126 selected original windows give a square matrix in all 126 permitted coefficient columns. A nonzero modular determinant is the image of that particular exact determinant in R0, so the exact determinant is nonzero. It is therefore a characteristic-zero full-rank result in V. The exact identity can be made explicit without expanding enormous rationals. If C is the recorded coefficient matrix, d=det(C), and C_j0 is the cofactor of row j and the constant-monomial column, then cofactor expansion gives d F=sum_j C_j0 P_j. These are determinants of precisely specified original coefficients in R0. Since d is nonzero in K, F belongs to the original necessary-equation ideal I for every label.

This identity holds in K[x,y,z,w] before any localization, so no variable-zero, entry-zero, or endpoint component is silently discarded. On the original guarded domain F is nonzero, as are the five fixed guards, whereas simultaneous vanishing of the P would imply F=0. The guarded unit-phase slice therefore contains no point externally invertible-complex monomial-equivalent to F8. This proves only the stated 280 slices.

## Reproduction

The independently authored programs are independent_structure.py and independent_minors.cpp, with a freshly extracted chart header. They import no author code and no historical accepted program. A rank-search run independently selected minors in both embeddings; fixed-input replay is used separately to establish the frozen author's recorded determinants without replacement. The source-level proof remains necessary for the exact support, interpolation and ring-homomorphism assertions.

The candidate's complete required manifest is checked in FROZEN_CANDIDATE_BINDING.json. The source identifiers in the final proof are exact contiguous hashes, and its stated scope agrees with this review. Its exploratory rank-146 pilot and local compiled binary are explicitly outside the required certificate boundary.

Independent fixed-input replay results, repeated identically after a separate-directory clean rebuild:

- 280 unique original labels, with 70 in each stage/branch combination.
- 560 fixed 126-by-126 determinants, all nonzero and exactly equal to the author's recorded residues.
- 70,560 full original-polynomial quotient and multiplication-back checks per fixed replay.
- 53,760 direct Green inversions per replay, each checked against its actual determinant/guard.
- 6,881,280 two-sided inverse-entry comparisons per replay.
- Full H27 and Q126 support checks without projection.
- Two duplicate-row determinant negative controls per replay, both zero.

The independent rank-search run also chose exactly the same windows and columns and obtained exactly the same 560 determinant residues. It checked 260,712 full quotient rows while searching and replaying its selected rows. The subsequent fixed-input runs allowed no substitute minor. The clean rebuild reproduced both the fixed-minor output and its complete deterministic log byte-for-byte.

For a clean independent replay, run from the review directory:

python -I -S independent_structure.py
g++ -O3 -std=c++17 independent_minors.cpp -o independent_minors
./independent_minors AUTHOR_FIXED_MINORS.txt > replay.txt 2> replay.log
cmp replay.txt FIXED_REPLAY.txt
cmp replay.log FIXED_REPLAY.log

The separately inspected fresh author source is replayed only as a supplementary control; it is not the independent reconstruction. The programs retained in sources/ are historical prose/data only and were not executed. No external write or repository change is part of this review.
