# One varying inner layer: complete row-membership gates

## Result and limits

After the certified outer-only rejection, allow one of the two inner N64 layers to vary and keep the other equal to its accepted-seed fiber pullback. All 512 outer coefficients remain free. Each choice therefore has 512 variable inner coefficients and 512 outer coefficients. Both still use all 24 Green terms and 1536 physical endpoint slots, of which 512 are fixed.

This note gives exact necessary-and-sufficient outer-elimination conditions, including singular and nonzero cases. It also identifies a Fourier-specific signed-symmetry branch that pairs the 64 row problems into 32 rank-six problems and lowers the cofactor compatibility degree from eight to seven. This restricted branch has 256 inner parameters. It is a declared ansatz, not a necessary condition on all one-inner lifts.

No coefficient fitting or solution claim is made. The complete 1536-variable N64 problem remains open.

## 1. Two choices and fixed guards

Let S be the row-masked eight-Green linear space

    S = { sum_j diag(a_j) G_j,64 }.

Write H_0*,H_1* for the two frozen inner N64 pullbacks. The bank B, Fourier target F, and routes are exactly those of the complete lift-system note.

- Input-layer variation: seek O K L=F with O,L in S and K=H_1* B fixed.
- Middle-layer variation: seek O L R=F with O,L in S and R=B H_0* fixed.

Both fixed pullbacks are rigorously invertible at the accepted algebraic seed. `FIXED_INNER_GUARDS.json` bounds ||I-Q_l H_l*|| by less than 2.374e-8 and 5.124e-8 for supplied exact dyadic preconditioners Q_l. The bounds include the full large-layer amplification of the accepted root coordinates. They use the derived seed radius 2*10^-12. The bank is invertible, so K and R are invertible.

A successful identity necessarily has det L != 0 and det O != 0. Thus singular L is an explicitly impossible stratum, not a case silently removed by a generic pivot choice.

There is no proved inclusion between S K S and S S R, and no justified claim that one choice has more intrinsic coefficient freedom. They have the same free-parameter budget. The reductions below put both in the same algebraic form; a preference would require target-specific evidence, not counting.

## 2. A common identity-target form

Right-multiply by the known F^(-1), obtaining O U(L)=I. Define

    U(L)=K L F^(-1)       in the input-variable branch,
    U(L)=L R F^(-1)       in the middle-variable branch.

For each output row i form the 8-by-64 template matrix

    T_i(L)[j,:]=row_i(G_j U(L)).

It is linear in the 512 inner coefficients. The outer row equation is

    c_i^T T_i(L)=e_i^T.

No inverse of the variable L, no inverse of a sum of Green operators, and no dense fixed inverse is required to define this system. F^(-1) is the known inverse Fourier map, and the other fixed factors are directly applicable.

Each original eight-Green row frame has rank eight: an exact nonzero modular minor proves this over characteristic zero. For det L != 0, U(L) is invertible, hence every T_i has rank eight. This invariant is why the successful rank stratum can be identified without a generic assumption.

## 3. General rank-stratified row membership and nonzero guards

For any proposed inner coefficients, even before using invertibility, put r_i=rank T_i. The row equation is solvable if and only if

    rank([T_i; e_i^T])=r_i.

For each r_i=0,...,8, this is expressible by vanishing of all (r_i+1)-minors of the augmented matrix and a nonzero r_i-minor of T_i, with the usual separate zero-rank convention. It covers singular template cases without dividing by a selected generic minor.

If a solution c0 and a basis N of ker(T_i^T) are supplied, all outer solutions are c0+N t. Over the infinite characteristic-zero field, one with all eight components nonzero exists exactly when no coordinate is identically zero on this affine solution space. In detail, for each coordinate j either some kernel vector has nonzero j-th component or c0_j must be nonzero. A finite union of proper coordinate hyperplanes cannot cover the entire affine solution space. This is the complete rank-stratified physical nonzero condition.

For the present invertible Fourier target, singular U cannot be successful because rank(O U)<=rank U<64. Once that stratum is explicitly rejected, rank T_i=8 and each consistent outer row has a unique solution. All eight of its entries must then be checked nonzero.

## 4. Exact rank-seven gate and degree-eight cofactor charts

For invertible L, delete target column i from T_i and call the resulting 8-by-63 matrix W_i. Because T_i has rank eight and one column was deleted, rank W_i is either seven or eight. Then

    e_i^T belongs to row(T_i)  if and only if  rank W_i=7.

If W_i has rank seven, its left kernel is one-dimensional. The missing column is not annihilated by that kernel, since otherwise rank T_i would also be seven. This proves sufficiency and supplies a unique normalized outer row. Rank below seven is incompatible with the already established rank-eight template frame.

A complete chart consists of seven columns J_i of W_i with rank seven. Define a kernel vector k_i by the signed seven-by-seven row-deletion cofactors of the 8-by-7 matrix W_i[:,J_i]. Then impose

    k_i^T W_i[:,remaining columns]=0,
    delta_i=k_i^T T_i[:,i] != 0,
    k_i[j] != 0 for every j.

The chosen seven pivot columns are annihilated automatically. The other 56 conditions are polynomial equations of degree at most eight in the inner coefficients: k_i has degree seven and T_i is linear. The outer coefficients are exactly c_i=k_i/delta_i.

Taking the union over all verified rank-seven charts is equivalent to the full membership condition. Failure of one chosen pivot chart is not a rejection of another chart or the entire family. Across 64 rows there are 3584 compatibility equations in 512 inner variables, plus det L != 0, all 512 inner nonzero guards, the cofactor/pivot guards, and all 512 reconstructed outer nonzero guards. The degree is eight rather than the degree-sixteen elimination that arose with two varying inner layers.

## 5. Fourier character structure shared by both choices

Let X be the high-x swap, the shift by 32, and D=diag((-1)^k). All fixed Greens, H_0*, H_1*, and B commute with X. Fourier obeys

    F X=D F,  X F^(-1)=F^(-1) D.

Both template families have the form

    T_i[j,:]=row_i(A_j L S),

where A_j commutes with X and X S=S D:

- input-variable: A_j=G_j K and S=F^(-1);
- middle-variable: A_j=G_j and S=R F^(-1).

Thus the 32 columns of S of each parity are known X-character vectors. For every successful row, the outer coefficient vector must annihilate the 8-by-32 template submatrix on columns of parity opposite to i. That wrong-character matrix must have rank at most seven. In the rank-seven stratum, its unique kernel vector reduces the remaining problem to matching the 32 same-parity entries, one of which is the identity target and the other 31 are zero.

This is a target-specific homogeneous-annihilation structure. It organizes the equations and candidate charts, but does not by itself reduce the total number of independent equations or establish a solution. Both inner choices have this structure; neither gains a proven freedom advantage merely from bank placement.

## 6. Signed-symmetry branch: 32 rank-six gates and degree seven

Impose the additional declared constraint

    X L=epsilon L X,  epsilon in {+1,-1}.

Since all Greens commute with X and their row frames have rank eight, this is equivalent to the physical coefficient conditions

    a_j[i+32]=epsilon a_j[i]

for every j and i<32. Each signed branch therefore has 256 free inner coefficients, with their physical nonzero guards. The plus branch includes two-value high-y masks. The minus branch has pure high-x odd dependence. Outer coefficients remain unrestricted, so the earlier full-product commutation obstruction does not automatically exclude either branch.

The template rows then satisfy

    T_(i+32)=epsilon T_i D.

For i<32 the two outer row problems are equivalent to requiring that row(T_i) contain both e_i^T and e_(i+32)^T. The second normalized target acquires only the known scalar epsilon*(-1)^i when reconstructing its outer coefficients.

Delete these two target columns from T_i and call the resulting 8-by-62 matrix W_pair,i. Since rank T_i=8, deleting two columns leaves rank at least six. Exact simultaneous membership of both unit rows is equivalent to

    rank W_pair,i=6.

Proof: simultaneous membership supplies two independent left-kernel vectors, so rank is at most six. Conversely, rank six gives a two-dimensional kernel; the two omitted target columns map it isomorphically onto C^2 because T_i has full rank eight. Both normalized outer rows are therefore uniquely recoverable.

Choose six columns and six rows giving a nonzero six-by-six pivot minor. Cramer's-rule cofactors produce an 8-by-2 left-kernel basis C_i whose entries have degree at most six. Its two free coordinates can be chosen as the pivot determinant times the coordinate basis; its pivot coordinates are minus the corresponding adjugate products. Impose

    C_i^T W_pair,i[:,remaining 56 columns]=0.

These are 112 equations of degree at most seven per pair. The 2-by-2 target-coordinate matrix C_i^T T_i[:,{i,i+32}] must be invertible; its determinant has degree at most fourteen. Solving this two-by-two normalization gives the two unique outer rows, all 16 physical entries of which must be nonzero. As in section 4, take the union of valid pivot charts; singular chosen minors are not silently discarded.

There are 32 paired problems rather than 64 separate problems, still totaling 3584 scalar compatibility equations, now degree seven in 256 inner variables. The benefit is a lower-degree, explicitly paired determinantal system, not a dimension-based existence claim. No reduction to a linear-size independent equation set has been proved.

These are not automatically the mean-anchored branches of the earlier complete system. The minus branch has zero four-sheet mean and is incompatible with preserving a nonzero scalar multiple of the accepted seed mean. In the plus branch, fixing that mean leaves only 128 high-y-character inner parameters. If outer means are also anchored, their 128 mean conditions must be checked after unique outer reconstruction; they do not disappear in the row-membership reduction.

## 7. Preparation and application costs

If exact coefficients are supplied and verified, applying the resulting size-N product uses 24 length-N Green scans, endpoint multiplications and additions, and the stated active bank. For N64 this is 24 scans plus four F8 transforms and routing, all charged. At a symbolic general size the scan work is O(24N) field operations and the bank has active mass N/2; no coefficient-generation saving is implied.

For example, the two-pass scalar cyclic recurrence uses 2N multiplications, 2N additions, and one multiplication by a precomputed wrap inverse per Green. Including all 24 endpoint diagonals and the seven vector additions per eight-term layer gives 72N+24 multiplications and 69N additions outside the bank, plus routing. The eight fixed wrap inverses can be shared across the three layers. Other scan implementations may change constants but may not omit terms.

For a bounded dense elimination preparation, generating all row templates for one proposed inner layer can be done by dense matrix products in O(8N^3) field operations as a safe bound. A better explicitly paid evaluator applies U and the eight following Greens to each standard basis vector. In either branch, U uses two eight-term layers, one bank, and one inverse Fourier transform. Across all N columns, template preparation therefore costs N times 24 Green scans, 16N endpoint multiplications, 14N layer-sum additions, one bank application, and one inverse Fourier application. If an ordinary FFT supplies the latter, this is O(N^2 log N) field operations with all constants charged, before solving any equations. Materializing all eight N-by-N transported templates takes O(8N^2) storage. Per-row rank and kernel work with eight template rows is O(8^2 N), hence O(8^2 N^2) across all rows; polynomial solving and exact algebraic root handling are additional, presently unbounded preparation costs.

Fixed guards need not be recomputed for every candidate: the exact seed-pullback nonsingularity certificates are reusable. The input-variable and middle-variable normal forms require no hidden application of an inverse Green sum. All inverse Fourier normalizations are explicit.

The cost model counts field operations. Algebraic coefficient degree, bit complexity, and a uniform O(N) coefficient generator remain open obligations. Solving a finite system would not establish a faster Fourier algorithm.

## 8. Bounded next use

A principled small next experiment can target one signed-symmetry branch and one declared inner choice, testing its 32 exact rank-six gates with full chart/nonzero guards. A candidate must still satisfy every full-product Fourier entry. Failure of a chart or bounded search would exclude only that scope.

The unrestricted one-inner systems are completely specified by sections 1-5 and retain 512 inner variables. The signed branch is offered because it has a genuine Fourier-pair structure and lower-degree equations, not because it is known to contain a solution. No such coefficient search is performed in this package.
