# Exact certificates — Fourier tail rank and complete four-column gate collapse

**Research checkpoint: 9 October 2026.** Exact arithmetic. These results restrict two-stage quasiseparable factorizations but give no new FFT runtime bound.

## Theorem A: two-sided Fourier tail-rank obstruction (all lengths)

Work over the complex numbers (or any field of characteristic not dividing `N` containing a primitive `N`th root). Let `F_N[i,k] = zeta^(i k)`, let `C` be an invertible `N x N` matrix, let `pi` be a permutation, and set `B[:,j] = (F_N C)[:,pi[j]]`.

Suppose every strict lower-left off-diagonal rectangular submatrix of `C` has rank at most `r_C_down`, while every strict upper-right off-diagonal rectangular submatrix of `B` has rank at most `r_B_up`. For `1 <= t < N`, define `J = {pi[N-t], ..., pi[N-1]}`, `a = max(J)`, and `ell = N-1-a`.

**Claim:**

`min(t, ell) <= r_C_down + r_B_up`.

**Proof.** Let `X=C[:,J]` be the selected `N x t` matrix. It has rank `t` because `C` is invertible. Let `R` select the first `N-t` output coordinates and `T` select input coordinates `a+1,...,N-1` (there are `ell` of them). The upper off-diagonal condition of `B` gives `rank(R F_N X) <= r_B_up`; the lower off-diagonal condition of `C` gives `rank(T X) <= r_C_down`.

Put `W=col(X)` (`dim W=t`) and `K=ker(R F_N)`. Then `dim(W intersect K) >= t-r_B_up`. Since the first `N-t` Fourier coordinates vanish on `K`, inverse Fourier transformation shows that `K` is spanned by the `t` Fourier characters `zeta^(r k)`, `r=1,...,t`. Restricting them to the `ell` consecutive input indices `k=a+1,...,N-1` produces a Vandermonde matrix (nonzero row scalings are immaterial), of rank `min(t,ell)`. Thus `dim ker(T|K)=t-min(t,ell)`. Consequently

`dim T(W intersect K) >= (t-r_B_up) - (t-min(t,ell)) = min(t,ell)-r_B_up`.

But `dim T(W intersect K) <= rank(TX) <= r_C_down`. The claimed inequality follows. This also covers `ell=0`. QED.

**Mirror theorem.** If `C` has strict upper-right rank at most `r_C_up` and `B` has strict lower-left rank at most `r_B_down`, put `J0={pi[0],...,pi[t-1]}`, `a0=min(J0)`. Applying the same argument to the last `N-t` Fourier rows and the first `a0` input coordinates gives

`min(t, a0) <= r_C_up + r_B_down`.

No normalization, nonzero generator, conditioning, unitary stage, or root-size bound is assumed. Both results hold for general quasiseparable matrices, not only globally separated generator stages.

**Special case that excludes the proposed length growth.** For `pi[-3:] = (1,2,5)`, `t=3`, and `a=5`, the first inequality reads `min(3,N-6) <= r_C_down+r_B_up`. For `N=8` it demands `2 <= r_C_down+r_B_up`, allowing `(1,1)`. For **every N>=9**, it demands `3 <= r_C_down+r_B_up`, excluding two rank-one stages in the indicated orientations. At `N=16`, prime `12289`, root `4134`, the high-frequency restriction to input positions `6,7,8` has determinant **1099 modulo 12289**; at prime `65537`, root `64`, it has determinant **121 modulo 65537**. This modular calculation is an independent witness of the Vandermonde fact, not the proof over complex numbers.

The bounds are sharp for arbitrary full-rank selected-column spaces: take the `t` high-frequency Fourier characters themselves; their first `N-t` Fourier outputs vanish, while their trailing input restriction has rank `min(t,ell)`. This does not construct separated-stage factorizations attaining equality.

## Theorem B: spectral complement identity (all lengths)

For any `b` with `N>=2b`, consider a tail sequence supported on input coordinates `k=b,...,N-1` whose nonzero part is

`L_k = sum_{r=1}^b alpha_r zeta^(r k)`.

For `i=0,...,N-b-1`, the complete root-of-unity sum vanishes because `1 <= i+r <= N-1`, hence

`sum_{k=b}^{N-1} L_k zeta^(i k) = - sum_{j=0}^{b-1} zeta^(i j) * sum_{r=1}^b alpha_r zeta^(r j)`.

Thus the first `N-b` Fourier outputs lie in the **fixed** `b`-dimensional span of characters `1,zeta^i,...,zeta^((b-1)i)`, regardless of `alpha`. The converse also holds: the Fourier map from the tail `k=b,...,N-1` to the first `N-b` output coordinates is an invertible Vandermonde-type square map; the `b`-dimensional exponential tail space maps onto the fixed `b`-dimensional low-character space. Therefore membership is equivalent.

For `N=8,b=3`, the previous adjacent-tail identities force `L_3,...,L_7` into the three-frequency tail family. Hence *all six columns* of the top block `[Y_1,-Y_2]` of the 11x9 gate lie in one fixed three-dimensional Fourier-output subspace. The top block therefore has row rank at most 3.

## Theorem C: all 55 maximal minors of the 11x9 gate collapse

Use exactly the previous checkpoint's polynomially rescaled `Uhat,Lhat` and 11x9 gate `K`. Its first five rows are `[Y_1,-Y_2,0]`, its next five are `[Y_1,0,-Y_5]`, and the last is the four-column cofactor row `[ell,0,0]`.

Theorem B gives rank at most 3 for the first five rows; the middle five have rank at most 5. To choose nine linearly independent rows, one must choose **exactly three of the first five, all five of the middle five, and the last row**. Thus 45 of the 55 9x9 minors vanish identically. The 10 potentially nonzero minors factor (by Laplace expansion along the three columns of `Y_2`) as `-det(Y_2[R,:])*D_H`, for `R` any three of the first five row positions. Since `col(Y_2)` lies in the fixed Fourier Vandermonde space `V` of dimension three, its row minors satisfy the exact Plücker proportionality

`det(Y_2[R,:]) * det(V[{0,1,2},:]) = det(Y_2[{0,1,2},:]) * det(V[R,:])`.

All `det(V[R,:])` are nonzero because the `zeta^i` are distinct. Therefore **every** 9x9 gate minor vanishes if and only if the one selected minor `Dhat=-D_B D_H` vanishes, i.e.

`rank(K) <= 8 <=> D_B * D_H = 0`.

This is an exact identity *inside the earlier reconstructed polynomial family*, including points where the rescaled polynomial generators are zero; those exceptional polynomial points need not correspond to valid original normalized stages. It does **not** give a new feasibility exclusion beyond the prior selected minor.

The script `collapse_certificate.py` regenerated the polynomials and proved the following as **identities over the integral cyclotomic ring** `Z[z]/(z^4+1)`: 30 four-by-four Fourier-subspace determinants vanish; all 10 three-by-three Plücker cross products vanish; 45 nine-by-nine gate minors vanish identically; each of the remaining ten is exactly `-D_H * det(Y_2[R,:])`.

## Theorem D: the rank-drop quadric is absolutely irreducible

The degree-two polynomial `D_B(h0,h1,h2,h6)` has nine nonzero terms over `Z[zeta_8]`. Homogenize it to degree two in five variables `(h0,h1,h2,h6,q)` and write the quadratic form as `x^T M x` with a symmetric matrix `M`. Under the exact ring homomorphism `Z[z]/(z^4+1) -> GF(12289)` sending `z` to `8246`, the upper-left 4x4 minor of `M` is **11251**, nonzero. Hence `rank(M)>=4` over the complex numbers. Were `D_B` reducible over `C`, its degree-two homogenization would be a product of two linear forms, whose symmetric coefficient matrix would have rank at most 2 (in characteristic zero). Contradiction.

Therefore `D_B` is **absolutely irreducible over C**. This does not rule out points on the quadric, or the complete Fourier factorization.

## Scope / research significance

- Theorem A excludes an **entire family of growing-length internal permutations** in a two-stage, rank-one-quasiseparable architecture, without using the chart-specific polynomials.
- Theorem C shows that rechecking other minors of the old 11x9 gate cannot yield new information; focus must shift to independent stage-compatibility constraints, different permutations, or more stages.
- These results do not prove any general FFT arithmetic lower bound; nor do they produce an `o(N log N)` construction.
- The earlier single-slice characteristic-zero exclusion and codimension bound remain as previously stated and are included intact in the nested archive.
