# Division-free Fourier coefficient compatibility

This is an exact feasibility system, not a solved construction and not evidence of feasibility when layout tests pass.

## Complete inverse-variable formulation

Use the permutation convention P e_j=e_{p(j)}. Given a target T and internal permutations P1,P2, let U,V be unknown N-by-N matrices and define

K=U T V,    H=P2^{-1} K P1^{-1}.

Then

T=S3 P2 S2 P1 S1

with all three factors of quasiseparable order at most one is equivalent to:

1. All upper-right and lower-left cut 2-by-2 minors of U and V vanish.
2. All upper-right and lower-left cut 2-by-2 minors of H vanish.
3. det(U) det(V) is nonzero.

Here T is invertible, as is the Fourier matrix. In that case H is automatically invertible too. From a solution recover S3=U^{-1}, S2=H, S1=V^{-1}.

Proof: inversion preserves each strict off-diagonal cut rank of an invertible square matrix. The complementary-submatrix rank identity gives rank((A^{-1})[I,J])=rank(A[J^c,I^c])+|I|+|J|-N. Taking complementary prefix/suffix I,J makes the last term zero and the remaining block the same oriented cut of A. This is valid without assuming invertible principal blocks. Vanishing of every 2-by-2 minor is exactly the rank-at-most-one condition, including all zero and degenerate branches.

For repeated bit reversal P=P^{-1}, the middle expression simplifies to H=P U F_N V P.

If a purely polynomial feasibility system is desired, add a scalar z and the equation z det(U) det(V)-1=0 instead of the inequation. This excludes spurious singular roots explicitly.

## Fourier-specific coupling equation

For F_N[a,c]=omega^(ac), write a<b and c<d. Its 2-by-2 minor is

Delta_F(a,b;c,d)=omega^(ac+bd)-omega^(ad+bc).

For any distinct output indices i,j and input indices k,l, the double Cauchy-Binet identity gives

Delta_K(i,j;k,l)
 = sum_{a<b} sum_{c<d}
       Delta_U(i,j;a,b)
       [omega^(ac+bd)-omega^(ad+bc)]
       Delta_V(c,d;k,l).                       (1)

Every cut minor required of H must set the appropriate expression (1) to zero, with i=p2(r), j=p2(s), k=p1^{-1}(u), l=p1^{-1}(v). Order these selected indices consistently or retain signed determinants.

The exact Fourier coefficients in (1) are now explicit. At composite N some vanish when N divides (a-b)(d-c); they must be retained as genuine zeros rather than replaced by a full-spark assumption. The system is bilinear in the two exterior-power matrices wedge^2 U and wedge^2 V, but these exterior powers share entries and satisfy Pluecker compatibility. Treating their entries as independent variables would be a relaxation, not an exact parametrization.

This formulation removes the middle stage as an unknown and exposes the shared-coefficient obstruction that independent min-cut tests miss. It is still a large algebraic synthesis problem. Dense determinant evaluation, elimination, root isolation, inverses and coefficient preparation are all charged; no linear-time solver is supplied.

## Completeness warning for separated generators

The chart A[i,j]=a_i b_j below the diagonal and c_i d_j above the diagonal does not include every order-one quasiseparable matrix when zeros occur. For example

[[1,0,0], [1,1,0], [0,1,1]]

is invertible and has all strict off-diagonal cut ranks at most one. A separated lower parametrization would require a_1 b_0=1 and a_2 b_1=1, forcing a_2 b_0 nonzero although entry(2,0)=0. Complete searches must use full cut minors or transition generators with zero transitions allowed. Normalizing by a possibly zero entry loses branches.

The new cyclic-discrepancy theorem eliminates every fixed-order three-stage family with at least one affine Fourier endpoint at sufficiently large N, regardless of this nonlinear system. The system remains relevant for finite sizes, both-nonaffine composite-length endpoint layouts, or modified architectures. A numerical N=8 fit found during this pass is only a diagnostic; it is not labeled an exact factorization or proof. The N=16 failures of a local optimizer likewise are not nonexistence evidence.
