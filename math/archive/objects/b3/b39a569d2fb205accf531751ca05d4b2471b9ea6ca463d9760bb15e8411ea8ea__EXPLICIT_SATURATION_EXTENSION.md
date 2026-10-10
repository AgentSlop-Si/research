# Explicit inverse-corner products and patch-equivalent reductions

This audit contribution specializes elementary cofactor algebra to the submitted model. It is not a novelty claim or a Fourier existence/exclusion result. All indices are zero-based, and K=Q(z) with z^4=-1.

## 1. General all-size cofactor identity

Let S be any n-by-n separated stage, n≥2:

S_ij=L_i V_j for i>j; S_ii=d_i; S_ij=U_i W_j for i<j.

Then the following polynomial identities hold even when S is singular or generators vanish:

adj(S)_(n-1,0) = -L_(n-1)V_0 ∏_(k=1)^(n-2)(d_k-L_k V_k),

adj(S)_(0,n-1) = -U_0 W_(n-1) ∏_(k=1)^(n-2)(d_k-U_k W_k).

For invertible S, division by det(S) gives the corresponding inverse entries.

### Proof, including the sign

For the lower cofactor, let H=S[1:n,0:n-1]. First work over the rational function field of the generators so division is allowed. Divide each H row i by L_i and its first column by V_0. Every entry in the first column is then one. For i=1,...,n-2 in increasing order, replace row i by row i minus row i+1. Such a row has zeros in columns 0,...,i-1 and entry d_i/L_i-V_i in column i. The last row is unchanged.

Expand along the first column. Its only remaining nonzero entry is in the last row, producing sign (-1)^(n-2). The remaining matrix is upper triangular. Undoing the scalings gives

det(H)=(-1)^(n-2)L_(n-1)V_0 ∏(d_k-L_k V_k).

The cofactor contributing to adj(S)_(n-1,0) has the additional sign (-1)^(n-1), so the total sign is minus for every n. Both sides are polynomials in the original generators and agree over their rational function field; hence the identity extends to all substitutions, including zero generators. Transpose S to obtain the upper formula.

## 2. Explicit quartic-patch localization

For the normalized C chart, put t=V0=C70 and s=W7=C07, and define for k=1,...,6

r_k=1-L_k V_k,   q_k=1-U_k W_k.

The formulas become

A70=-t ∏r_k / det(C),
A07=-s ∏q_k / det(C),   where A=C^-1.

Therefore the precise stated regular patch is the nonvanishing of

g4 = t s det(C) B70 B07 ∏r_k ∏q_k.

No separate inverse computation is needed. These factors do not assert that every excluded zero-gap point fails the separated model. They encode the chosen regular chart; some excluded points can still be valid elsewhere in the complete quadratic model.

The determinant has exact variable degree 14; each cofactor has degree 13. The product g4 has exact degree 44. A single Rabinowitsch variable v with v*g4-1=0 encodes the open condition as an affine polynomial system, giving 31 equations in 27 variables and an added equation of degree 45. Alternatively, compute the ideal saturation by g4 without explicitly adding that equation.

## 3. Explicit reduced-patch localization

Use the submitted 21 variables, D=t(z-1), T_k as defined in the source, Ctilde=D C, and Btilde=F Ctilde P^-1. Define

R_k=D-T_k V_k,
Q_k=1-h_k eta_k,   k=1,...,6.

Because L_k=T_k/D and U_k W_k=h_k eta_k,

A70 = -t D^2 ∏R_k / det(Ctilde),
A07 = -h0 D^8 ∏Q_k / det(Ctilde).

Thus a concrete saturation polynomial is

g6 = t h0 det(Ctilde) Btilde70 Btilde07 ∏R_k ∏Q_k.

The constant z-1 is a nonzero element of K, so t≠0 already enforces D≠0. Nonzero Btilde anchors are equivalent to nonzero B anchors on this patch. This g6 is exactly sufficient and necessary for all of the stated regular-patch requirements, rather than merely a list of informal inverse-corner caveats.

`explicit_sextic_saturation_certificate.json` exports the twelve local gap polynomials, the two output-anchor polynomials, and all entries of the determinant matrix. It deliberately leaves the determinant and product factored. `corner_cofactor_certificate.json` exports both n=8 expanded cofactor polynomials.

### Degree accounting

- R_k has degree 3 and Q_k degree 2.
- Btilde70 has degree 2 and Btilde07 degree 3.
- det(Ctilde) has exact degree 22.
- This explicit g6 has exact degree 59; v*g6-1 has degree 60.

The determinant degree bound is elementary: all entries of Ctilde have degree at most 3; its last row and last column have degree at most 2, and their intersection has degree 1. Each determinant term therefore has degree at most 22. An exact integer scaling specialization in the checker produces a nonzero degree-22 coefficient, proving equality. For C, the first and last rows have degree at most 1 and the six other rows degree at most 2; the analogous degree-14 coefficient is nonzero.

These are the degrees of the displayed, unoptimized saturation products. Factors can have repetitions or removable common powers; they should not be interpreted as minimal possible localization degree. Because the coefficient field and polynomial ring are integral domains, total degrees add across these nonzero factors.

## 4. Remove irrelevant t powers before solving

The submitted reduced equations contain powers of t that are units on the stipulated patch. Exact division gives:

- Divide lower_3_2, lower_4_2, lower_5_2, lower_6_2 by t²: four degree-3 equations.
- Divide lower_4_3, lower_5_3, lower_5_4, lower_6_3, lower_6_4, lower_6_5 by t: six degree-4 equations.
- Divide upper_1_2 by t: one degree-5 equation.
- Leave the fourteen other upper equations unchanged: fourteen degree-6 equations.

The resulting system has the same 25 equations and 21 variables, and still 1,749 terms. It is exported in `reduced_patch_primitive_equations.json`, with each removed t power recorded. Multiplication back is checked coefficient-for-coefficient. Localizing either system at t gives the same ideal; consequently subsequent saturation by the full regular-patch product has the same solutions.

This is a modest algebraic simplification, not a certified runtime gain. It does not remove singular or zero-anchor components that remain unless all required saturation factors are imposed.

## 5. Proof-compatible stopping condition

For the regular patch, form the ideal of the supplied or patch-primitive equations over K and localize at g6. An exact representation of 1 in the corresponding Rabinowitsch ideal certifies no complex regular-patch solution. A verified zero with g6≠0 gives a genuine separated-stage F8 factorization by the reconstruction proof. Either result concerns this regular chart only. The complete quadratic model or a proven exhaustive stratification is still needed for a statement about every zero-corner/zero-diagonal branch.
