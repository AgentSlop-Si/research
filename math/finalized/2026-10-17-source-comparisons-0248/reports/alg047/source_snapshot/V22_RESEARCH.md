# Two-line Weyl product classification and Fourier-hard factor theorem — v22

**Checkpoint:** 10 October 2026  
**Primary target:** exact full-output DFT of arbitrary fresh input in fully charged sequential `o(N log N)` arithmetic.  
**Status:** exact classification of products of two non-collinear Weyl-line operators. Successful pairs exist, but every successful factorization contains at least one factor already monomially/diagonally equivalent to the full Fourier transform. **No faster FFT is constructed.**

## 1. Starting point

v21 proved that the complete multi-shift Weyl–Green span contains the Fourier matrix, but the Fourier-compatible coefficients collapse onto one isotropic Weyl line and become Bluestein chirp convolution. The exact next gate was therefore a **product of two non-collinear Weyl lines**, rather than another sum on one line.

This checkpoint resolves that gate completely for odd prime length.

---

## 2. Symmetric Weyl coordinates

Let `N` be an odd prime and let `omega` be a primitive `N`th root of unity over `C`, or over any field of characteristic not dividing `2N` in which the required Gauss sum is nonzero. Define

\[
X e_j=e_{j+1},\qquad Z e_j=\omega^j e_j,
\]

and the symmetric Weyl operators

\[
D_{a,b}=\omega^{ab/2}X^aZ^b.
\]

They obey

\[
D_uD_v=\omega^{\sigma(u,v)/2}D_{u+v},
\]

where for `u=(a,b)`, `v=(c,d)`

\[
\sigma(u,v)=bc-ad.
\]

The `N^2` operators `D_(a,b)` form an orthogonal basis of the full matrix algebra.

For the unnormalized Fourier matrix

\[
F[i,j]=\omega^{ij},
\]

a direct trace calculation gives its exact Weyl coefficients:

\[
\boxed{
F=\gamma\sum_{a,b\in\mathbb Z_N}
\omega^{-(a^2+b^2)/4}D_{a,b},
}
\tag{2.1}
\]

with

\[
\gamma=\frac1N\sum_{j=0}^{N-1}\omega^{j^2}\ne0.
\]

Thus the Fourier Weyl symbol is one nondegenerate quadratic phase.

---

## 3. Two-line product tensor

Fix two independent directions

\[
u=(a,b),\qquad v=(c,d),\qquad ad-bc\ne0.
\]

Consider arbitrary line operators

\[
A=\sum_m\alpha_mD_{mu},\qquad
B=\sum_n\beta_nD_{nv}.
\]

Because `(m,n) -> m u+n v` is a bijection of `Z_N^2`, the Weyl coefficient of `AB` at `mu+nv` is

\[
\alpha_m\beta_n\omega^{\sigma(u,v)mn/2}.
\]

Remove this known product cocycle from the Fourier coefficients and define the `N x N` tensor

\[
T_{m,n}
=
\gamma\,
\omega^{-\|mu+nv\|^2/4}
\omega^{-\sigma(u,v)mn/2},
\]

where

\[
\|(x,y)\|^2=x^2+y^2.
\]

Writing `u dot v=ac+bd`, this separates as

\[
T_{m,n}
=
\gamma\,
\omega^{-\|u\|^2m^2/4}
\omega^{-\|v\|^2n^2/4}
\omega^{-\kappa mn/2},
\]

with

\[
\boxed{
\kappa=u\cdot v+\sigma(u,v).
}
\tag{3.1}
\]

The first two factors are invertible diagonal row/column scalings. The remaining middle matrix is either the all-ones matrix or a permuted Fourier matrix.

### Theorem 3.1 — exact rank dichotomy

\[
\boxed{
\operatorname{rank}T=
\begin{cases}
1,&\kappa=0,\\
N,&\kappa\ne0.
\end{cases}}
\tag{3.2}
\]

Therefore:

* one product `AB` can equal `F` only when `kappa=0`;
* when `kappa!=0`, a sum of `r` products using the same two line directions needs `r>=N`, because every product contributes rank at most one to the dephased coefficient tensor.

This is a complete exact dichotomy: there is no intermediate tensor rank.

---

## 4. Classification of all successful line pairs

The compatibility condition is

\[
(a+b)c+(b-a)d=0.
\]

For nonzero `u`, every solution is

\[
\boxed{
v=t(a-b,a+b),\qquad t\ne0.
}
\tag{4.1}
\]

Moreover

\[
\det(u,v)=t(a^2+b^2).
\]

Hence the directions are independent exactly when

\[
\boxed{a^2+b^2\ne0.}
\tag{4.2}
\]

For every such pair, the line coefficients are unique up to one nonzero scalar. A canonical choice is

\[
L_u=\sum_m\omega^{-\|u\|^2m^2/4}D_{mu},
\]

\[
L_v=\sum_n\omega^{-\|v\|^2n^2/4}D_{nv}.
\]

### Theorem 4.1 — exact two-line Fourier factorization

For `v=t(a-b,a+b)` and `a^2+b^2!=0`,

\[
\boxed{
F=L_u\,(\gamma L_v).
}
\tag{4.3}
\]

Conversely, every exact product of one operator from the `u` line algebra and one from the `v` line algebra is this factorization up to a reciprocal scalar rescaling of the two factors.

So the proposed two-line product architecture is algebraically feasible; the crucial question becomes the complexity of its factors.

---

## 5. Each successful line factor is already Fourier-hard

Let

\[
L_u=\sum_m\omega^{-\|u\|^2m^2/4}D_{mu},
\qquad u=(a,b).
\]

### Vertical direction

If `a=0`, then `L_u` is diagonal. Completing the square gives

\[
L_u[j,j]=G_-\,\omega^{j^2},
\]

where `G_-` is a nonzero quadratic Gauss sum. This factor applies in `O(N)` scalar work.

### Nonvertical direction

If `a!=0`, a direct entry calculation gives

\[
\boxed{
L_u[i,j]
=
\omega^{-((a-b)^2/(4a^2))i^2}
\omega^{((a^2+b^2)/(2a^2))ij}
\omega^{-((a+b)^2/(4a^2))j^2}.
}
\tag{5.1}
\]

If `a^2+b^2!=0`, the middle coefficient

\[
\frac{a^2+b^2}{2a^2}
\]

is nonzero, so the middle matrix is a row-permuted Fourier matrix. Therefore

\[
\boxed{
L_u=D_L\,P\,F\,D_R
}
\tag{5.2}
\]

for invertible diagonal matrices `D_L,D_R` and a permutation `P`.

If `a^2+b^2=0`, the mixed term vanishes and `L_u` has rank one. Such an isotropic direction cannot participate in an independent successful pair by (4.2).

### Corollary 5.2 — no complexity reduction from two lines

Every exact two-line factorization of `F` contains at least one nonvertical anisotropic factor and therefore contains a factor already monomially/diagonally equivalent to `F` itself.

* If one direction is vertical, that factor is diagonal but the other factor is Fourier-equivalent.
* If both directions are nonvertical, **both** factors are Fourier-equivalent.

Thus the product identity does not reduce exact Fourier application to two simpler transforms. It merely factors Fourier into another Fourier-equivalent transform and optional diagonal/chirp gauges.

---

## 6. Low-order Green/rational realizations are also excluded

Suppose a successful nonvertical line factor is represented on its cyclic Weyl generator `C` as

\[
L_u=q(C)^{-1}p(C),
\qquad
\deg q=d,\quad \deg p=e.
\]

For one cyclic order, the standard recurrence rectangle argument gives a separated square block of size

\[
m=\left\lfloor\frac{N-e}{2}\right\rfloor
\]

and rank at most `d`. But `L_u` is monomially equivalent to a prime Fourier matrix, whose every square minor is nonzero. Therefore

\[
\boxed{
d\ge\left\lfloor\frac{N-e}{2}\right\rfloor.
}
\tag{6.1}
\]

In particular, a constant- or polylogarithmic-order Green recurrence with a local numerator cannot realize the hard factor. A direct low-state recurrence route is impossible within this line architecture.

---

## 7. Arithmetic ledger

| Architecture | Exact structural requirement | Charged consequence |
|---|---|---|
| One product on incompatible line pair | impossible (`rank T=N`) | no factorization |
| Sum of products on incompatible fixed pair | at least `N` products | separately executed cost at least quadratic |
| Compatible pair, one vertical line | one diagonal chirp + one Fourier-equivalent factor | same asymptotic difficulty as Fourier |
| Compatible pair, both nonvertical | two Fourier-equivalent factors | no simplification; naive cost two Fourier transforms |
| Compatible low-order rational factors | denominator degree `Omega(N)` for local numerator | no constant/polylog-state Green solve |
| A hypothetical direct joint evaluator of the product | would evaluate `F` itself | exactly the original open problem |

The result does not prove an unrestricted Fourier lower bound. It closes the specific strategy “factor Fourier into two non-collinear Weyl-line operators and apply each through a short line recurrence.”

---

## 8. Verification

The package uses exact arithmetic in finite fields containing the needed prime-order roots of unity.

* The Weyl coefficient formula (2.1) is checked entry-by-entry for `N=5,7,11,13`.
* Every independent ordered line pair is exhausted for `N=5,7`:
  * `N=5`: 480 independent pairs; 64 compatible tensors of rank 1 and 416 incompatible tensors of rank 5.
  * `N=7`: 2016 independent pairs; 288 compatible tensors of rank 1 and 1728 incompatible tensors of rank 7.
* Exact factorizations are checked at `N=7,11,13,17` for vertical and nonvertical examples and multiple partner scales.
* The closed form (5.1) is checked for every anisotropic direction at `N=5,7,11,13,17`.
* Every isotropic line factor in the tested fields has rank one; every anisotropic line factor has full rank.
* An independently written verifier reconstructs four exact factorizations without importing the main module.
* `8/8` automated test groups pass before the final cold-run wrapper.

---

## 9. Prior-art and claim boundary

Finite Weyl systems, quadratic Gauss sums and the Weil/metaplectic representation are classical. In that language, the Fourier transform is the operator attached to the Weyl element and quadratic phases are the natural metaplectic symbols. The present tensor-rank dichotomy and “one factor is already Fourier-equivalent” classification are project-specific deductions from those standard ingredients; no literature-wide novelty claim is made.

Relevant adjacent sources include:

* S. Gurevich, R. Hadani and R. Howe, *Quadratic reciprocity and the sign of the Gauss sum via the finite Weil representation*, arXiv:0808.2447.
* N. A. Lopez and I. Y. Dodin, *Exactly unitary discrete representations of the metaplectic transform for linear-time algorithms*, arXiv:2012.06028.
* The classical Bluestein chirp-convolution reduction already identified in v21.

---

## 10. Honest conclusion and next gate

We still do **not** have an exact `o(N log N)` FFT.

What v22 establishes is the complete answer for a product of two Weyl lines:

\[
\boxed{
\text{either the pair is incompatible and needs tensor rank }N,
}
\]

or

\[
\boxed{
\text{it factors Fourier exactly, but one factor is already Fourier-equivalent.}
}
\]

The next exact candidate must therefore use more than two line factors in a way that does **not** leave a Fourier-equivalent factor exposed. The most concrete surviving direction is a three-factor metaplectic/shear architecture with a genuinely shared executor—or a high-treewidth non-Krylov stage outside line algebras.
