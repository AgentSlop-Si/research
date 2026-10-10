# Phase 16 proof certificate: Fourier–Green interface rigidity

**10 October 2026.** Exact mathematics with explicitly stated operator restrictions. This is not a proof that arbitrary DFTs need superlinear time. The underlying polynomial-zero argument is classical Fourier uncertainty; historical priority of the packaging here is **not claimed**.

## 0. Conventions

Let `K` be a field containing a primitive `N`-th root `omega`, with `N>=2`. Since the root has order `N`, the characteristic does not divide `N`. Let

\[
(F_N)_{k,j}=\omega^{-kj},\qquad 0\le k,j<N.
\]

Call a column *cyclicly `b`-banded* when all its potentially nonzero entries lie in `{j-b,...,j+b} mod N`, where `j` is its column index. A matrix has cyclic column-band radius `b` when every column does. If `2b+1>=N` the restriction is vacuous; in this case the lower bound below is immediate.

## Theorem 1 — a consecutive-support Fourier zero certificate

**Claim.** If `v != 0` is supported within `q<=N` consecutive cyclic coordinates, then `F_N v` has at most `q-1` zero coordinates. Equivalently,

\[
|\operatorname{supp}(F_Nv)|\ge N-q+1.
\]

**Proof.** Write the allowed interval as `{c,c+1,...,c+q-1}` modulo `N`. At frequency `k`,

\[
(F_Nv)_k=\omega^{-kc}h(\omega^{-k}),\qquad
h(z)=\sum_{t=0}^{q-1}v_{c+t}z^t.
\]

The coefficient polynomial `h` is nonzero, degree at most `q-1`, and the `N` values `omega^-k` are distinct in the field. A nonzero degree-`q-1` polynomial has at most `q-1` distinct roots. QED.

Unlike the additive prime-order uncertainty theorem, this statement holds for **composite N** and suitable exact finite fields because the time support is consecutive.

## Theorem 2 — Fourier interface rigidity with arbitrary diagonal gauges

**Claim.** Suppose

\[
F_N=D_L P Q^{-1}D_R,
\]

where `D_L,D_R` are invertible diagonal matrices, `Q` invertible, `P` has at most `t` nonzero entries in each column (in arbitrary positions), and `Q` has each column supported in some consecutive cyclic interval of length `s`. Then

\[
\boxed{s+t\ge N+1.}
\]

In particular, for column-band radii `a,b` of `P,Q`,

\[
\boxed{2(a+b)+1\ge N,\qquad a+b\ge\left\lceil(N-1)/2\right\rceil.}
\]

**Proof.** Rearrange the proposed exact identity:

\[
D_L^{-1}F_N D_R^{-1}Q=P.
\]

For any column `j`, the vector `v=D_R^-1 Q e_j` is nonzero because `Q` is invertible; it retains the same consecutive support of length `s` because diagonal scaling does not create or remove zeros. Its Fourier transform is a nonzero diagonal multiple of `P e_j`, so it has at most `t` nonzero entries. Theorem 1 gives `N-s+1<=t`, proving the claim. QED.

**Scope.** This includes arbitrary position-dependent coefficients in `P` and `Q`, even when those operators do not commute, and **arbitrary invertible endpoint diagonal gauges**, not just quadratic chirps. It does not include general sums of inverses, free dense transformations, or nonconsecutive long-range supports at composite lengths.

## Corollary 3 — rational Harper/Green degree tradeoff

Let `H` be any cyclic tridiagonal `N x N` matrix (position-dependent diagonal and nearest-neighbor entries are permitted), so that every column of `H^d` is supported in a cyclic neighborhood of radius `d`. Suppose

\[
F_N=D_L p(H)q(H)^{-1}D_R,
\]

where `q(H)` is invertible and `p,q` are scalar polynomials of degrees `u,v`. Then `p(H)` has cyclic radius at most `u` and `q(H)` radius at most `v`, so

\[
\boxed{u+v\ge\lceil(N-1)/2\rceil.}
\]

In particular, if both degrees are at most `d`, then `d>=ceil((N-1)/4)`. The result is **degree rigidity**, not an arithmetic-time lower bound: unusually structured high-degree polynomial products can sometimes be jointly evaluated in linear time (the Phase 15 dyadic-Green fusion is a counterexample to naive degree-to-cost implications).

## Theorem 4 — uniqueness at the bandwidth boundary

Let `N=2(a+b)+1` be odd. Fix for column `j` an allowed time window `I_j={j-b,...,j+b}` and an allowed frequency window `J_j={j-a,...,j+a}`. Suppose a nonzero vector `v_j` is supported in `I_j` and its Fourier transform is supported in `J_j`.

Then its polynomial, after removing the monomial corresponding to the start of `I_j`, is *forced up to one scalar*:

\[
\boxed{h_j(z)=c_j\prod_{k\notin J_j}(z-\omega^{-k}),\quad c_j\ne0.}
\]

**Proof.** The complement of `J_j` consists of precisely `2b` distinct frequencies. The coefficient polynomial has degree at most `2b`; because it vanishes at all those roots, it must be a scalar multiple of their monic product. QED.

For every column `j`, choose `c_j=1` and use the resulting polynomial coefficients to build the matrix `Q`: polynomial coefficient `r` goes into row `j-b+r`. Set `P=F_N Q`. Then `P` has radius `a`, `Q` radius `b`, and the identity `F_N Q=P` holds *for every N and every admissible field*. But `Q` **may be singular**, in which case one cannot conclude `F_N=P Q^-1`.

Our exact prime-field tests give invertible `Q` for odd `N=3,5,7,9,11,13,15,17` with the supplied primes and `N=45` over `GF(271)`. Because the construction has entries in the integral cyclotomic ring `Z[omega]`, a nonzero determinant after reduction to an admissible finite field also certifies a nonzero determinant in characteristic zero at that `N`. Hence these are genuine algebraic **sharpness examples** for the radius inequality—not evidence of an `O(N)` execution algorithm.

**Important counterexample to universal field invertibility:** with `N=45,a=b=11`, the explicit `Q` has rank 43 over `GF(181)` but rank 45 over `GF(271)`. At `N=49,a=b=12`, ranks 47 over `GF(197)` and 49 over `GF(491)`; at `N=53,a=b=13`, ranks 49 over `GF(107)` and 53 over `GF(743)`. All fields contain primitive roots of the required orders. An exact interpolation identity does **not** guarantee an invertible denominator in every field.

## Theorem 5 — the sharpness denominator hides chirp convolution

Retain the odd-length boundary construction, `N=2(a+b)+1`. Let

\[
g_0(z)=\prod_{k\notin J_0}(z-\omega^{-k})=
\sum_{r=0}^{2b}c_r z^r.
\]

The forbidden roots for column `j` are the base roots multiplied by `omega^-j`; therefore the coefficient at row `t=j+s` is

\[
Q_{j+s,j}=c_{s+b}\,\omega^{j(s-b)},\qquad -b\le s\le b,
\]

and zero otherwise. Define invertible diagonal chirps

\[
L_{t,t}=\omega^{t(t-1)/2},\quad
R_{j,j}=\omega^{-j(j-1)/2-bj},
\]

and a cyclic convolution `C_h` with kernel

\[
h_s=c_{s+b}\omega^{-s(s-1)/2},\quad -b\le s\le b,
\]

setting the other `h_s=0`. Because `N` is odd, the exponents are well-defined modulo `N` and the quadratic phases are periodic. Then

\[
\boxed{Q=L C_h R.}
\]

**Proof.** At `t=j+s`, the exponent contributed by `L_t R_j h_s` is

\[
\frac{(j+s)(j+s-1)-j(j-1)-s(s-1)}2-bj=j(s-b),
\]

which is exactly the coefficient above. Outside `|s|<=b`, both sides vanish. QED.

This is the **hidden cost** of the apparently banded Fourier factorization. Computing `Q^-1` requires applying an inverse cyclic convolution, plus cheap diagonal chirps. Nothing here proves that convolution can be applied to arbitrary inputs in `O(N)`.

## Theorem 6 — chirp conjugations normalize Weyl shift monomials

For any `N` with `omega` of order `N`, define `D_c e_j = omega^(c j^2)e_j`, shift `S e_j=e_(j+1)`, and modulation `T e_j=omega^j e_j`. Then

\[
\boxed{D_c S^s D_c^{-1}=\omega^{c s^2}S^s T^{2cs}.}
\]

**Proof.** Apply both sides to `e_j`, and compare exponents `c((j+s)^2-j^2)=cs^2+2csj`. QED.

Conjugating a Weyl-sparse inverse stage by a **paired** chirp does not increase its Weyl-support count; it only changes its Weyl direction. This is the familiar Clifford/metaplectic shear action. It does not license treating arbitrary *unpaired* chirp insertions as Weyl-monomial gauges in Phase 15's support theorem.

## Theorem 7 — stronger arbitrary-support facts over complex numbers

For any nonzero complex vector `v`, the general discrete uncertainty principle gives

\[
|\operatorname{supp}(v)|\,|\operatorname{supp}(F_N v)|\ge N.
\]

Thus, even with arbitrary nonconsecutive support patterns, the interface `F_N=D_L P Q^-1 D_R` requires `s*t>=N` when the two factors have at most `s` and `t` nonzero entries per column. For **prime N**, the stronger theorem of Tao gives

\[
|\operatorname{supp}(v)|+|\operatorname{supp}(F_N v)|\ge N+1,
\]

so the additive interface barrier holds for arbitrary support locations at prime lengths as well. These are **known** uncertainty theorems, not original claims. The additive prime-order theorem should not be silently transferred to every modular field: Fourier minors can degenerate in finite characteristic.

References: Terence Tao, *An uncertainty principle for cyclic groups of prime order*, Math. Res. Lett. 12 (2005), arXiv:math/0308286; Murty–Whang, *The uncertainty principle and a generalization of a theorem of Tao* (2012).

## Verification scope

`test_phase16.py` contains 19 independently named test groups. `independent_audit.py` separately checks basis vectors and fresh random vectors against direct modular DFT sums, including sharpness construction, unique-polynomial constraints, exceptional denominator fields, rational Harper finite-field experiments, and exact Fourier covariance. The predecessor `test_phase15.py` was rerun (21 groups passed).

The *uniform* result of this phase is the bandwidth theorem and its stated consequences, proved above—not the finite list of numerical certificates. No new all-input FFT time upper bound, nontrivial unrestricted time lower bound, or historical first-discovery claim is made.
