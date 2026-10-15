# Metaplectic Bruhat rigidity and the three-shear FFT gate — v23

**Checkpoint:** 10 October 2026  
**Primary target:** exact full-output DFT of arbitrary fresh input in fully charged sequential `o(N log N)` arithmetic.  
**Status:** the entire finite one-dimensional metaplectic/shear factorization route is classified. Every stage is either an `O(N)` monomial operator or already Fourier-equivalent. **No faster FFT is constructed.**

## 1. Starting point

v22 classified products of two Weyl-line operators. Compatible pairs factor Fourier exactly, but at least one successful line factor is already diagonally/permutationally equivalent to the full Fourier transform. The proposed next gate was a three-factor metaplectic/shear architecture whose factors might individually be easier and whose joint execution might avoid the hard line factor.

This checkpoint proves that the obstruction is not limited to two lines or three factors. It holds for **every finite word in the one-dimensional finite Weil representation**.

---

## 2. Symplectic generators and the computationally easy subgroup

Let `N` be an odd prime. Work over `F_N` for symplectic parameters and over a coefficient field containing a primitive `N`th root `omega`.

Set

\[
L(t)=\begin{pmatrix}1&0\\ t&1\end{pmatrix},\qquad
D(a)=\begin{pmatrix}a&0\\0&a^{-1}\end{pmatrix},\qquad
W=\begin{pmatrix}0&-1\\1&0\end{pmatrix}.
\]

In the position realization of the finite Weil representation:

* `rho(L(t))` is the diagonal chirp
  \[
  C_t[x,x]=\omega^{t x^2/2};
  \]
* `rho(D(a))` is the coordinate permutation `e_j -> e_(a j)`;
* `rho(W)` is the unnormalized DFT
  \[
  F[x,y]=\omega^{xy}.
  \]

The lower Borel subgroup is

\[
B_-=
\left\{
\begin{pmatrix}a&0\\c&a^{-1}\end{pmatrix}:a\ne0
\right\}.
\]

Every element factors as

\[
\begin{pmatrix}a&0\\c&a^{-1}\end{pmatrix}
=L(c/a)D(a),
\]

so its Weil operator is one chirp and one permutation. It applies in `O(N)` scalar work and has exactly one nonzero entry in every row and column.

### Theorem 2.1 — closure of all individually easy metaplectic stages

`B_-` is a subgroup. Therefore any product of chirp/permutation metaplectic stages remains a chirp/permutation monomial operator.

Since the Fourier Weyl element `W` is not in `B_-`, no finite product of only these individually `O(N)` metaplectic stages can equal the DFT.

---

## 3. Big Bruhat cell: every other stage is Fourier-equivalent

Let

\[
S=\begin{pmatrix}a&b\\c&d\end{pmatrix}\in SL_2(F_N).
\]

When `b != 0`, there is the exact decomposition

\[
\boxed{
S=L(d/b)D(-b)W L(a/b).
}
\tag{3.1}
\]

Consequently its Weil operator is, up to one nonzero projective scalar,

\[
\boxed{
\rho(S)=C_{d/b}\,P_{-b}\,F\,C_{a/b}.
}
\tag{3.2}
\]

Its matrix kernel is

\[
\rho(S)[x,y]
=
\omega^{(d x^2-2xy+a y^2)/(2b)}
\]

in the normalization used by the executable certificate. Every entry is nonzero.

### Theorem 3.1 — exact complexity dichotomy

Every finite Weil operator belongs to exactly one of two computational classes:

1. `b=0`: a monomial chirp/permutation operator, applicable in `O(N)` work;
2. `b!=0`: diagonally/permutationally equivalent to one full DFT.

The equivalence works both ways. Applying such a big-cell operator costs

\[
T_F(N)+O(N),
\]

and an application of `F` can be recovered from it using only `O(N)` extra chirp, permutation and scaling work.

There is **no intermediate metaplectic stage** between monomial-linear and Fourier-hard.

---

## 4. Any-depth metaplectic word collapses to at most one Fourier core

The Bruhat decomposition is

\[
SL_2(F_N)=B_-\sqcup B_-WB_-.
\]

Given any finite word

\[
S_1S_2\cdots S_t,
\]

multiply its `2 x 2` symplectic matrices. The final matrix lies either in `B_-` or in `B_-WB_-`. Therefore the complete projective operator word fuses exactly to either

\[
\text{one monomial operator},
\]

or

\[
\text{monomial}\times F\times\text{monomial}.
\]

This is a positive exact fusion: an arbitrarily deep metaplectic circuit never needs multiple DFT cores. But it does **not** improve the DFT itself. When the word represents `W`, the fused core is precisely `F`.

### Corollary 4.1 — factor-by-factor FFT obstruction

If

\[
\rho(S_1)\cdots\rho(S_t)=\lambda F
\]

for nonzero scalar `lambda`, at least one factor `S_i` lies in the big Bruhat cell. That factor is already Fourier-equivalent.

Thus no factor-by-factor metaplectic FFT can have every factor cheaper than Fourier.

A completely new joint evaluator of the entire word is not logically ruled out—but after fusion the word is simply the DFT operator again, so the factorization itself supplies no new computational state reduction.

---

## 5. The unique three-shear decomposition

Let

\[
U(t)=\begin{pmatrix}1&t\\0&1\end{pmatrix}.
\]

Solving

\[
L(x)U(y)L(z)=W
\]

over any odd prime field gives the unique solution

\[
\boxed{(x,y,z)=(1,-1,1).}
\]

Hence

\[
\boxed{W=L(1)U(-1)L(1).}
\tag{5.1}
\]

The two outer lower shears are diagonal chirps and cost `O(N)`. The middle upper shear has nonzero upper-right entry and therefore belongs to the big Bruhat cell: it is diagonally/permutationally equivalent to a full DFT.

The alternative pattern has the unique solution

\[
\boxed{W=U(-1)L(1)U(-1),}
\]

which exposes two Fourier-hard outer shears.

So the best three-shear decomposition contains exactly one Fourier-hard factor. This is not a new FFT algorithm; it is the metaplectic normal form of the existing DFT.

---

## 6. Exact projective certificates

The executable representation uses:

\[
\rho(L(t))=C_t,
\qquad
\rho(D(a))=P_a,
\qquad
\rho(W)=F.
\]

It verifies projective multiplication

\[
\rho(S)\rho(T)=\lambda(S,T)\rho(ST)
\]

with nonzero scalar `lambda(S,T)`.

The package exhausts all

\[
|SL_2(F_5)|^2=120^2=14,400
\]

ordered multiplication pairs. It also checks random longer words at lengths `7,11,13`, direct Bruhat kernel formulae, all cell cardinalities, every three-shear parameter triple at four prime lengths, and independent implementations of the kernel and shear identities.

The expected Bruhat counts are reproduced:

\[
|B_-|=N(N-1),
\qquad
|B_-WB_-|=N^2(N-1),
\qquad
|SL_2(F_N)|=N(N^2-1).
\]

---

## 7. Arithmetic ledger

| Route | Charged structure | Work |
|---|---|---:|
| Lower-Borel stage | one chirp + one permutation | `O(N)` |
| Big-cell stage | chirp + permutation + one DFT + chirp | `T_F(N)+O(N)` |
| Unique `LUL` Fourier word | two easy chirps + one big-cell shear | `T_F(N)+O(N)` |
| Arbitrary metaplectic word | collapse group product, then Bruhat form | either `O(N)` or `T_F(N)+O(N)` |
| Fused word whose product is `W` | exactly the DFT | `T_F(N)` |

Projective scalar normalization contributes only one final `O(N)` output scaling and does not change the dichotomy.

---

## 8. Correctness and claim boundary

This checkpoint does **not** prove an unrestricted FFT lower bound. It covers operators in the one-dimensional finite Weil/metaplectic representation over odd prime lengths.

It does not exclude:

* higher-dimensional symplectic/tensor embeddings;
* non-metaplectic global operators;
* nonlinear or input-adaptive arithmetic circuits;
* a genuinely new direct evaluator of `F` itself;
* composite-length ring phenomena outside the two-cell field Bruhat decomposition.

It does prove that deeper products of finite one-dimensional chirps, scalings, shears and metaplectic operators do not create a third computational class. Every such search reduces to either an easy monomial stage or one DFT core.

---

## 9. Honest conclusion and next gate

We still do **not** have an exact `o(N log N)` FFT.

The three-factor metaplectic route is now closed much more broadly than requested:

\[
\boxed{
\text{every finite one-dimensional metaplectic word collapses to at most one Fourier core.}
}
\]

The next exact route must therefore leave rank-one metaplectic geometry. The most credible options are:

1. a higher-dimensional symplectic/tensor embedding with a joint executor that does not reduce to Cooley--Tukey;
2. a high-treewidth non-Krylov exact stage outside the Weil representation;
3. a non-metaplectic globally coupled arithmetic DAG whose state dimension genuinely grows across scales while total charged work remains `o(N log N)`.
