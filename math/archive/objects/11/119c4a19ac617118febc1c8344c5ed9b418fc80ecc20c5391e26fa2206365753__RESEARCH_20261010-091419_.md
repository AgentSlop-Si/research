# Higher-dimensional local-ring Weil exponent gate and mixed-valuation hierarchy — v26

**Checkpoint:** 10 October 2026  
**Primary target:** exact full-output cyclic DFT of an arbitrary fresh input in fully charged sequential `o(N log N)` arithmetic.  
**Status:** the direct higher-dimensional Weil route over `R=Z/p^s Z` is classified enough to close the proposed cyclic embedding. Canonical p-adic cells give tensor products of shorter cyclic prime-power Fourier cores, while every dense higher-dimensional ring-Weil stage is monomially equivalent to the additive Fourier transform on `R^n`, not to the cyclic Fourier matrix of the same dimension. **No faster exact cyclic FFT is constructed.**

## 1. Starting point

v25 classified the one-dimensional Weil representation over

\[
R=\mathbb Z/p^s\mathbb Z
\]

for odd `p`. A one-dimensional cell with upper-right valuation `v` is computationally equivalent to `p^v` copies of the cyclic transform of length `p^(s-v)`. Proper cells form a congruence-parabolic subgroup and cannot assemble the full one-dimensional Fourier Weyl element without a valuation-zero, full-DFT-equivalent factor.

The proposed escape was to increase the symplectic dimension and let linear changes of variables exchange p-adic digit layers. In this checkpoint:

* `q=p^s` is the size of the coefficient ring;
* `V=R^n` is the position module;
* `Q=|V|=q^n=p^(sn)` is the operator dimension;
* `psi(t)=zeta_q^t` is a faithful additive character of `R`.

The finite-ring Weil representation is projective. Projective scalars do not affect zero patterns, support sizes or four-entry cross ratios, which are the invariants used below.

---

## 2. Exact dense/sparse dichotomy from the symplectic B-block

Write

\[
S=\begin{pmatrix}A&B\\C&D\end{pmatrix}\in Sp(2n,R)
\]

and let `rho(S)` be its Weil operator in the position basis.

### Theorem 2.1 — noninvertible B forces zeros

If `B` is not invertible as an endomorphism of the finite module `V`, then every row of `rho(S)` is supported on at most

\[
\boxed{|\operatorname{im}B|<|V|}
\]

columns. In particular, the operator matrix is not dense.

### Proof

Let `M_v` denote modulation by the character `psi(<v,x>)`. Heisenberg covariance gives, up to a scalar phase,

\[
\rho(S)M_v\rho(S)^{-1}=T_{Bv}M_{Dv}.
\]

For `v in ker B`, the translation disappears. If `K_S(x,y)` is the matrix kernel, then every nonzero entry satisfies an affine character constraint

\[
\langle v,y\rangle=\langle Dv,x\rangle+\text{constant}
\quad\text{for all }v\in\ker B.
\]

For fixed `x`, the permitted `y` lie in one affine coset of `(ker B)^perp`. The standard dot pairing on `R^n` is perfect, so

\[
|(\ker B)^\perp|=\frac{|V|}{|\ker B|}=|\operatorname{im}B|.
\]

A noninvertible square map on a finite module has a nonzero kernel, hence `|im B|<|V|`. QED.

### Theorem 2.2 — invertible B is additive-Fourier-equivalent

If `B` is invertible, then

\[
\boxed{
S=L(DB^{-1})\,G(-B)\,W\,L(B^{-1}A),
}
\tag{2.1}
\]

where

\[
L(T)=\begin{pmatrix}I&0\\T&I\end{pmatrix},\qquad
G(M)=\begin{pmatrix}M&0\\0&M^{-T}\end{pmatrix},\qquad
W=\begin{pmatrix}0&-I\\I&0\end{pmatrix}.
\]

The symplectic identities make `DB^{-1}` and `B^{-1}A` symmetric. In the Weil representation:

* `L(T)` is a diagonal quadratic chirp;
* `G(M)` is a coordinate permutation, up to a scalar character;
* `W` is the additive Fourier transform on `R^n`.

Therefore

\[
\boxed{
rho(S)=M_1\,F_{R^n}\,M_2
}
\tag{2.2}
\]

projectively, with monomial `M_1,M_2`. The matrix is dense.

Combining the two theorems gives an exact dichotomy:

\[
\boxed{
rho(S)\text{ is dense}\iff B\text{ is invertible}.
}
\tag{2.3}
\]

The executable certificate verifies (2.1) projectively on exact finite-field realizations of random symplectic words.

---

## 3. Mixed p-adic valuation cores

The natural higher-dimensional intermediate cells already appear in upper shears

\[
U(E)=\begin{pmatrix}I&E\\0&I\end{pmatrix},
\]

with symmetric `E`. Their operator is

\[
\rho(U(E))=F_{R^n}^{-1}C_EF_{R^n},
\qquad
C_E[z,z]=\psi\!\left(\frac12 z^TEz\right).
\]

### Diagonal valuation normal form

For the canonical diagonal form

\[
E=\operatorname{diag}(p^{v_1}u_1,\ldots,p^{v_n}u_n),
\qquad
0\le v_i\le s,
\]

where `u_i` is a unit when `v_i<s` and the entry is zero when `v_i=s`, the kernel factors coordinatewise into the one-dimensional v25 Gauss kernels.

### Theorem 3.1 — exact computational core

Up to diagonal phases and coordinate permutations,

\[
\boxed{
\rho(U(E))
\sim
\bigoplus_{\text{residue vectors}}
\bigotimes_{i:v_i<s}F_{p^{s-v_i}}.
}
\tag{3.1}
\]

Consequently:

\[
\boxed{
\#\text{blocks}=p^{\sum_i v_i},
}
\tag{3.2}
\]

\[
\boxed{
\text{nonzeros per row/column}=p^{\sum_i(s-v_i)},
}
\tag{3.3}
\]

and the largest root order visible in a nonzero four-entry ratio is

\[
\boxed{
p^{\max_i(s-v_i)}.
}
\tag{3.4}
\]

The blocks are Fourier transforms on the finite abelian group

\[
\bigoplus_{i:v_i<s}\mathbb Z/p^{s-v_i}\mathbb Z,
\]

not generally one cyclic transform of the product size.

For odd `p`, symmetric forms over the local principal ideal ring can be diagonalized by congruence. Unit square classes can refine the quadratic-form orbit, but they do not change the block lengths, support count or phase-depth values in (3.1)–(3.4).

### Example at `R=Z/9Z`, `n=2`

| Valuation profile | Blocks | Row support | Core |
|---|---:|---:|---|
| `(0,0)` | 1 | 81 | `F_9 tensor F_9` |
| `(0,1)` | 3 | 27 | `F_9 tensor F_3` |
| `(1,1)` | 9 | 9 | `F_3 tensor F_3` |
| `(0,2)` | 9 | 9 | `F_9` on each block |
| `(1,2)` | 27 | 3 | `F_3` on each block |
| `(2,2)` | 81 | 1 | monomial/identity class |

All six cases are built and checked exactly in the package.

---

## 4. Main cyclic obstruction: exponent of the additive group

The additive Fourier matrix on `R^n` has kernel

\[
F_{R^n}[x,y]=\psi(x^Ty).
\]

For rows `x,x'` and columns `y,y'`, its four-entry cross ratio is

\[
\Lambda
=
\psi\!\left((x-x')^T(y-y')\right).
\tag{4.1}
\]

Every such ratio has multiplicative order dividing

\[
q=p^s,
\]

the exponent of the additive group `R^n`.

The cyclic Fourier matrix of the same dimension

\[
C_Q[i,j]=\zeta_Q^{ij},
\qquad
Q=q^n,
\]

has the explicit witness

\[
\Lambda_{0,1;0,1}(C_Q)=\zeta_Q,
\]

of exact order `Q`.

Cross ratios are invariant under arbitrary row/column permutations and arbitrary nonzero row/column diagonal scalings. Hence, for `n>1`,

\[
Q=q^n>q
\]

and

\[
\boxed{
C_{q^n}
\text{ is not monomially equivalent to }
F_{R^n}.
}
\tag{4.2}
\]

### Theorem 4.1 — no higher-dimensional local-ring Weil embedding

For every `n>1` and every

\[
S\in Sp(2n,\mathbb Z/p^s\mathbb Z),
\]

the Weil operator `rho(S)` is not monomially equivalent to the cyclic Fourier matrix of dimension `p^(sn)`.

**Proof.** If `B(S)` is noninvertible, Theorem 2.1 gives zeros, while the cyclic Fourier matrix is dense. If `B(S)` is invertible, Theorem 2.2 reduces `rho(S)` to `F_(R^n)`, and (4.2) gives the cross-ratio contradiction. QED.

Because the Weil representation is projective,

\[
\rho(S_t)\cdots\rho(S_1)
\]

collapses to a scalar multiple of `rho(S_t\cdots S_1)`. Therefore:

\[
\boxed{
\text{no finite higher-dimensional local-ring Weil word computes }C_{p^{sn}}\text{ when }n>1.
}
\tag{4.3}
\]

This closes the direct digit-mixing symplectic embedding proposed after v25.

---

## 5. General finite-abelian-group exponent gate

The obstruction is not special to free local-ring modules.

Let `G` be a finite abelian p-group of order `p^K` and exponent `p^e`. Every entry and every cross ratio of its character table has order dividing `p^e`. The cyclic Fourier matrix `F_(p^K)` has a primitive `p^K` cross ratio.

Therefore monomial equivalence requires

\[
p^e=p^K.
\]

For a finite abelian group, exponent equals order only when the group is cyclic. Thus:

\[
\boxed{
F_G\sim_{\rm monomial}F_{|G|}^{\rm cyclic}
\quad\Longrightarrow\quad
G\text{ is cyclic}.
}
\tag{5.1}
\]

This also closes mixed-exponent embeddings such as

\[
\mathbb Z/p^{k_1}\mathbb Z\oplus\cdots\oplus\mathbb Z/p^{k_m}\mathbb Z
\]

with more than one nontrivial factor. If one factor already has exponent equal to the full group order, the group is cyclic and the full cyclic core has simply been reintroduced.

---

## 6. Rank budget and the ordinary tensor FFT ledger

Define the unit rank of a symplectic stage by

\[
r(S)=\operatorname{rank}_{\mathbb F_p}(B(S)\bmod p).
\]

For two stages,

\[
B(ST)=A(S)B(T)+B(S)D(T),
\]

so

\[
\boxed{
r(ST)\le r(S)+r(T).}
\tag{6.1}
\]

The full additive Fourier Weyl element on `R^n` has `B=-I_n` and rank `n`. Therefore any factorization of that **additive tensor transform** satisfies

\[
\boxed{
\sum_j r(S_j)\ge n.
}
\tag{6.2}
\]

The `n` coordinate swaps attain equality. Each applies one cyclic `q`-point transform independently on `Q/q` fibers. If a dense radix-`p` implementation of `F_q` uses `p q s` multiply-add terms, one coordinate stage costs

\[
pQs,
\]

and all `n` stages cost

\[
\boxed{
pQns=\Theta_p(Q\log_pQ).}
\tag{6.3}
\]

This is exactly the ordinary tensor/mixed-radix FFT on the additive group `R^n`. Equations (6.1)–(6.3) are a structural and literal-schedule ledger, not a lower bound for every arithmetic DAG.

The crucial point is that this additive transform is still not the cyclic transform of length `Q`, by Theorem 4.1.

---

## 7. Exact verification

The package uses exact arithmetic in finite coefficient fields containing the needed roots of unity.

### Mixed-valuation kernels

At `R=Z/9Z`, `n=2`, all six valuation profiles listed in Section 3 were checked. The measured row/column supports agree exactly with (3.3).

A direct `81 x 81` multidimensional Gauss-sum kernel for

\[
E=\operatorname{diag}(1,3)
\]

matches the Kronecker-factorized `F_9 tensor F_3` core entry-for-entry.

A non-diagonal congruent form

\[
E'=A^TEA
\]

has the same image size and support count.

### General symplectic words

Sixty deterministic random words in lower shears, linear coordinate changes and partial/full Weyl swaps were evaluated exactly at dimension nine.

For every word:

* the measured support per row equals `|im B|`;
* noninvertible `B` obeys the Heisenberg support equations;
* invertible `B` agrees projectively with the dense Bruhat factorization (2.1).

Failures: **0**.

A separate dimension-81 dense word over `Z/9Z` also agrees projectively with its additive-Fourier normal form and has only cross-ratio orders `1,3,9`.

### Cyclic exponent witnesses

Exact cyclic witnesses were checked for dimensions

\[
9,\ 25,\ 81,\ 625,\ 729.
\]

Their cross-ratio orders equal the full dimensions, while the corresponding additive-module exponents are respectively

\[
3,\ 5,\ 9,\ 25,\ 9.
\]

### Independent implementation

A second implementation, which does not import the main module, independently checks:

* six exact multidimensional Gauss kernels at dimension 81;
* tensor/additive cross-ratio orders;
* the primitive cyclic order-81 witness;
* the general finite-abelian exponent gate for several order-`3^6` groups.

### Test status

\[
\boxed{10/10\text{ automated test groups pass}.}
\]

The complete v25 predecessor ZIP is embedded, hash-checked and CRC-checked.

---

## 8. Correctness and claim boundaries

This checkpoint does **not** establish:

* an exact `o(N log N)` cyclic FFT;
* a lower bound for unrestricted arithmetic circuits;
* a bit-complexity or fixed-precision theorem;
* a practical speed improvement over FFTW, MKL, pocketfft or cuFFT;
* a literature-wide novelty claim.

The dense/sparse dichotomy and exponent obstruction classify the direct higher-dimensional ring-Weil route. They do not exclude:

* restriction to a specially chosen invariant subspace of a larger representation;
* non-Weil high-treewidth stages;
* nonlinear or non-projective constructions;
* a completely different global arithmetic DAG.

Any subspace embedding would need to preserve all `Q` independent input and output coordinates and supply a fully charged extraction/reconstruction map; no such embedding is constructed here.

---

## 9. Prior-art boundary

Classical ingredients include:

* Weil representations of symplectic groups over finite rings;
* Heisenberg covariance;
* Bruhat factorizations when the upper-right block is invertible;
* quadratic Gauss sums and local-ring normal forms;
* Fourier analysis on finite abelian groups;
* Smith/congruence reduction over principal ideal local rings.

The project-specific combination is:

1. the exact support bound `|supp row| <= |im B|` from the Heisenberg kernel equation;
2. the dense-cell additive-Fourier normal form;
3. the mixed-valuation computational hierarchy;
4. the cyclic-vs-additive cross-ratio exponent obstruction;
5. the all-word closure and charged rank ledger.

These derivations and executable certificates have not been independently peer reviewed.

---

## 10. Honest conclusion and next gate

We still do **not** have an exact sub-`N log N` cyclic FFT.

What v26 proves is:

\[
\boxed{
\text{higher-dimensional local-ring Weil geometry produces additive-group Fourier cores, not the cyclic DFT of the same size.}
}
\]

The p-adic intermediate cells are real and exactly classifiable, but their natural fusion is the ordinary tensor/mixed-radix transform on a noncyclic additive group. The primitive phase depth required by the cyclic group cannot be created by monomial ring-Weil decoration.

The remaining exact routes are now outside direct finite-ring Weil words:

1. a **non-Weil high-treewidth operator** with a genuine exact non-Krylov `O(N)` or `O(N log log N)` solver;
2. a larger representation with a rigorously charged invariant-subspace embedding and extraction map that preserves the cyclic `p^(sn)` phase depth;
3. a non-metaplectic global arithmetic DAG with a complete operation and precision ledger.
