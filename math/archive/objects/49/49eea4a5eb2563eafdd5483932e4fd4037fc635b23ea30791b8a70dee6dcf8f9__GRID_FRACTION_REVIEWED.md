# A sparse grid matrix fraction and a common-anchor exclusion

This is a distinct construction pass after the universal-orbit bank returned to the ordinary FFT endpoint. The proposed primitives are genuinely nonseparable raw-grid solves. The first fixed pencil fails by an exact boundary theorem over C, with all projective coupling and singular branches covered. A shifted route removes that particular obstruction and remains a separate next test.

## 1. Primitive, parameters, and honest apply cost

On t,u=0,...,M-1, N=M^2, use row-major index tM+u and zero-boundary shifts

    (L_t y)[t,u]=y[t-1,u],   (L_u y)[t,u]=y[t,u-1].

For arbitrary edge masks a[t,u],b[t,u], set

    U=I-D_a L_t-D_b L_u,    G=U^-1.

U is unit lower triangular, hence invertible for every edge value, including zeros. Apply G by one forward pass:

    y[t,u]=x[t,u]+a[t,u]y[t-1,u]+b[t,u]y[t,u-1].

There are exactly 2M(M-1) active directed edges. Coefficient storage/preparation, two products/additions per interior grid cell, boundary cases, output writes, and routing are O(N). Arbitrary externally specified coefficients are not synthesized for free.

A fixed product of these Green solves with monomial factors is not a viable escape by itself: each inverse row has at most three entries, so k stages give inverse row support at most 3^k. Exact Fourier inversion needs support N in each row. Taking sums before products avoids applying that inverse-support conclusion mechanically.

The broader proposed two-stage family has two independently routed Green terms per stage, with independent left/right diagonal factors. An upper parameter count is

    4[2M(M-1)+2N]=16N-8M.

Permutations are discrete and scalar sum weights can be absorbed into endpoint diagonals. This upper count first falls below N^2 at M=4,N=16 among nontrivial square sizes: at M=2,3 the counts are 48,120 versus N^2=16,81, while M=4 gives 224<256. This is only a dimension comparison; it proves neither existence nor nonexistence at any size. The test below fixes most of these parameters and does not exclude the full edge-mask family.

## 2. Exact sparse matrix-fraction identity

Let U_i,V_i be invertible routed component denominators; their rows and columns have at most three entries when the endpoint factors are monomial. Let

    H_i=alpha_i U_i^-1+beta_i V_i^-1,
    W_i=alpha_i V_i+beta_i U_i.

Then

    H_i=U_i^-1 W_i V_i^-1.

For an invertible middle monomial C=QP, the two-stage target

    F=H_2 C H_1

is equivalent to

    U_2 F V_1=W_2 K^-1 W_1,
    K=U_1 C^-1 V_2.

K is invertible with at most nine entries per row/column; W_i have at most six. No inverse of W_i was taken, so zero couplings and singular sums were not discarded algebraically. Equivalently the 2N-by-2N block matrix

    [ K      W_1   ]
    [ W_2  U_2 F V_1 ]

has rank exactly N, since its Schur complement at the always-invertible K must vanish. If F is invertible then both H_i and W_i must be invertible; a singular sum cannot be rescued by the other factors. This supplies a checkable sparse-sandwich target rather than a free dense inverse oracle.

## 3. A complete fixed-pencil probe at N=16

For constant directional weights define G(a,b)=(I-a L_t-b L_u)^-1. Let R_N be bit reversal of the log_2 N index bits for dyadic M. Choose

    U=I-2L_t-3L_u,
    V=R_N (I-5L_t-7L_u) R_N^-1,
    H(alpha,beta)=alpha U^-1+beta V^-1.

The test target is

    F_N=H(alpha_2,beta_2) Q P H(alpha_1,beta_1),

where Q is any invertible complex diagonal, P is any permutation, and each (alpha_i,beta_i) is any nonzero projective pair. Both finite ratios, beta=0, and alpha=0 are included. No outer nonuniform-amplitude diagonal is inserted after the rightmost H in this fixed-pencil target; that additional freedom belongs to the broader family and would change the obstruction.

## 4. Common-anchor lemma

Suppose A has first row a e_0^T with a!=0, and B has its final column supported only in its final row. If A Q P B equals the unnormalized Fourier matrix, then the row of B selected by the first row of QP must be a nonzero constant row, because the first Fourier row is all ones. Its final-column entry must be nonzero, so it must be the last row of B.

For G(a,b), the first row is e_0^T and the last column is e_(N-1). Bit reversal fixes 0 and N-1, so the same holds for the routed Green. Consequently H(alpha,beta) has first row (alpha+beta)e_0^T and last column (alpha+beta)e_(N-1). If alpha+beta=0 it is singular and cannot occur in a Fourier factorization. This covers that branch directly rather than dividing it away.

For the remaining branches, the lemma forces the last row of the rightmost H to be constant. Set k=M/2. Three entries of that row are

    column N-1:     alpha+beta,
    column N-2:     3alpha+5^k beta,
    column N-1-M:   2alpha+7^k beta.

Indeed bit reversal sends the last-minus-one column to a column k vertical grid steps from the last point, and last-minus-M to k horizontal steps from it. Straight coordinate paths have weights 5^k and 7^k, respectively.

Thus constant-row necessity gives the homogeneous equations

    2alpha+(5^k-1)beta=0,
    alpha+(7^k-1)beta=0.

Their determinant is

    Delta_M=2*7^k-5^k-1>0   for every k>=1.

Only alpha=beta=0 solves them, contrary to the projective hypothesis. Therefore this entire fixed pencil has no two-stage middle-monomial Fourier factorization over C at any dyadic square N=M^2, M>=2. At the requested N=16 size, the determinant is 72. The proof uses exact integer entries and covers every complex coupling, every middle Q,P, both projective endpoints, and every singular-sum branch.

### Stronger constant-modulus form

The same three entries show that the last row cannot have constant nonzero modulus, even if their phases differ. Divide by alpha+beta and put r=beta/(alpha+beta). Let

    u=3+(5^k-3)r,    v=2+(7^k-2)r.

If |u|=|v|=1, then

    (7^k-2)u-(5^k-3)v=3*7^k-2*5^k.

The left side has magnitude at most 7^k+5^k-5, whereas the positive right side exceeds that bound by

    2*7^k-3*5^k+5>0.

For k=1 the gap is 4; for k>=2, 2*7^k>3*5^k. Thus no such u,v exist. This also blocks any flat-modulus target under output row/column permutations and phase-only right masks in this anchored setting. Arbitrary nonuniform right amplitude masks can remove the condition and are explicitly outside this exclusion.

## 5. Independent finite-field controls and covariance gate

The checker independently generates the grid Green columns by forward recurrence and verifies their three-sparse inverse denominators. It then enumerates every projective coupling over F_p and retains every invertible sum.

For F Z=D F and F D=Z^-1 F, a factorization F=A QP B requires both pairs

    A^-1 D A       and B Z B^-1,
    A^-1 Z^-1 A    and B D B^-1

to be conjugate by the same monomial QP. Diagonal conjugation preserves diagonal entries, so their paired diagonal fingerprints must have the same multiset. This is necessary, not sufficient. The checker uses the pair rather than claiming a small fingerprint set is complete. A=F,B=I is an exact positive control.

At N=16 the exact tests find:

- p=17: 18 projective parameters; 15 invertible; all 225 invertible pairs rejected.
- p=97: 98 projective parameters; 93 invertible; all 8,649 pairs rejected.
- p=193: 194 projective parameters; 191 invertible; all 36,481 pairs rejected.
- p=257: 258 projective parameters; 253 invertible; all 64,009 pairs rejected.

All singular projective values, primitive roots, determinants, and fingerprints are retained in GRID_PENCIL_RESULTS.json. The finite tests alone would not prove a characteristic-zero exclusion; the separate common-anchor argument does. Full matrix inversions and certification are charged research computations, not advertised O(N) primitive application work.

## 6. Next candidate after removing this obstruction

The rejected route preserved both boundary anchors. Replace R_N by R'_N=T_1 R_N, where T_1 translates the output index cyclically by one, and use R'_N G(5,7) R'_N^-1. The two Green components now have different minimal and maximal vertices; the above common-anchor proof no longer applies. Each component remains a routed acyclic O(N) solve. This gives a precise next pencil to test with the same sparse-sandwich and Weyl conditions, retaining all zero and projective branches. It is not a claim that the shifted pencil succeeds.

## Context

Structured recurrence and low-displacement algorithms are established topics; for a primary reference see [De Sa, Gu, Puttagunta, Ré and Rudra, A Two Pronged Progress in Structured Dense Matrix Multiplication](https://arxiv.org/abs/1611.01569). The project contributions here are the explicit specialized formulas, branch accounting, and charged tests. No novelty or unrestricted lower-bound claim is made.
