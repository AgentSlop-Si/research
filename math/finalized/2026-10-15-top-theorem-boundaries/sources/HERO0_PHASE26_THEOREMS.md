# HERO #0 — Phase 26: permutation-aligned Fourier–Green rigidity

**Date:** 11 October 2026  
**Status:** Self-contained exact matrix proofs and independently reproducible finite-field/numerical tests; **no new all-input FFT algorithm or verified external publication novelty**.

## Problem and exact scope

Let `s >= 2`, `N=s²`, with indices `k=s x+y`, `j=s a+b`. Define

\[
F_N[(x,y),(a,b)]=\eta^{yb}\omega^{xb+ya},\qquad
\eta=e^{2\pi i/s^2},\ \omega=\eta^s.
\tag{1}
\]

We investigate the two-stage *mixed-axis rook* architecture

\[
T=(Y_H+Y_V)(X_H+X_V),\tag{2}
\]

where `H` is block diagonal with respect to the second digit, while `V` is block diagonal with respect to the first digit. **Both `X_V` and `Y_V` can be arbitrary complex rook matrices** (not necessarily Green, invertible, or fast).

On each horizontal fiber, `X_H` is a sum of at most `r_X` weighted one-cycle Green resolvents and `Y_H` is a sum of at most `r_Y`. A term is `(I-P)^{-1}` where `P e_i=w_i e_{next(i)}` for an arbitrary Hamiltonian cycle permutation and arbitrary complex edge weights, including zero, provided the inverse exists. A scalar factor and an arbitrary horizontal diagonal may also be included.

**Template hypothesis:** The traversal permutations of *all* these horizontal Green terms belong to a fixed collection of `q` permutation orders, independent of the fiber. The edge weights may be entirely unrelated between fibers and layers; cycles may be traversed forward or backward. The template hypothesis is indispensable; fiber-dependent permutations are not excluded by the resulting theorem.

## Lemma 26.1: exact crossing rank of a weighted Hamiltonian Green inverse

Let `pi` be the traversal order, and let `X,A` be disjoint nonempty subsets of `{0,...,s-1}`. Delete all symbols outside `X ∪ A` from the cyclic word `pi`. Write `c_pi(X,A)` for the number of cyclic transitions `A -> X` in the remaining word. If all edge weights are nonzero and their product `W ≠ 1`, then

\[
\boxed{\operatorname{rank} (I-P)^{-1}[X,A]=c_\pi(X,A).}\tag{3}
\]

With some weights zero, the equality can fail, but the **upper bound** `rank <= c_pi(X,A)` still holds.

**Proof.** Index positions in `pi` by `0,...,s-1` and define `d_i=prod_{t<i}w_{pi(t)}`. With `W=prod_i w_i`, the explicit inverse formula is

\[
G_{\pi(i),\pi(j)}=
\frac{d_i}{d_j(1-W)}
\begin{cases}1&i\ge j\\W&i<j.\end{cases}\tag{4}
\]

The row and column scalings are invertible when all weights are nonzero. After sorting `A` in permutation order, a row for an `X` vertex having `k` `A` vertices before it is

\[
(1,\ldots,1,W,\ldots,W)
\quad\text{with }k\text{ initial ones}.\tag{5}
\]

Distinct occupied gaps yield independent row patterns, except that gaps `k=0` and `k=|A|` represent the same *cyclic* gap and their rows are proportional. Successive differences have disjoint nonempty supports and coefficients `1-W`, while an endpoint row has nonzero constant tail (`W≠0`); this proves (3). The rank bound for zero weights follows by polynomial specialization of the vanishing `(c+1)`-minors after multiplication by the nonzero common denominator `1-W`.

In particular, if `X` lies entirely before or entirely after `A` in `pi`, then

\[
\boxed{\operatorname{rank}G[X,A]\le1.}\tag{6}
\]

This holds for arbitrary inhomogeneous weights, including zero, and both cycle orientations. A sum of `r` such resolvents has rank at most `r` across the same separated rectangle.

**Independently checked:** all three-color selected-set patterns for sizes `3,...,10` under randomly ordered nonzero weighted cycles; exact field ranks coincide with cyclic transition counts. The zero-edge rank upper bound and the O(s) cycle solve were checked separately.

## Lemma 26.2: an off-axis Fourier compatibility dichotomy

For `y != b`, `x != a`, only the two crossed paths in (2) survive. On arbitrary nonempty disjoint coordinate sets `X,A`, let

\[
H_y=Y_H^{(y)}[X,A],\qquad G_b=X_H^{(b)}[X,A].
\]

For unrestricted vertical matrices there are arbitrary diagonal vectors `u^{yb},v^{yb}` such that

\[
T^{yb}_{X,A}=H_y\,\mathrm{diag}(v^{yb})+
\mathrm{diag}(u^{yb})G_b.\tag{7}
\]

The target is

\[
F^{yb}_{X,A}=\eta^{yb} f_b g_y^T,
\qquad f_b[x]=\omega^{bx},\quad g_y[a]=\omega^{ya}.\tag{8}
\]

If (7) equals (8), necessarily **one** of

\[
\boxed{f_b\in\operatorname{col}(H_y)
\quad\text{or}\quad g_y\in\operatorname{row}(G_b)^T}\tag{9}
\]

holds. Otherwise take a left null vector `u` of `H_y` and a right null vector `v` of `G_b` with `u^Tf_b != 0` and `g_y^Tv != 0`. Pairing (7) with `(u,v)` gives zero, while pairing (8) gives the nonzero value `eta^(yb)(u^Tf_b)(g_y^Tv)`. The argument has **no division by unknown Green weights or vertical variables**.

## Lemma 26.3: Fourier-mode capacity on an arbitrary coordinate subset

Fix `X` of size `u`. The complex Fourier vectors `f_b|_X` form a tight frame:

\[
\sum_{b=0}^{s-1}f_bf_b^*=s I_u.\tag{10}
\]

If `H` is a subspace of dimension at most `r`, let `P_H` be its Hermitian orthogonal projector. Each vector `f_b` has squared norm `u`; if it belongs to `H`, its projected squared norm is `u`. Therefore

\[
\#\{b:f_b\in H\}\,u
\le\sum_b\|P_Hf_b\|_2^2
=s\operatorname{tr}(P_H)\le sr.
\]

Hence

\[
\boxed{\#\{b:f_b\in H\}\le\lfloor sr/u\rfloor.}\tag{11}
\]

No consecutive-index assumption or Vandermonde full-spark assumption is needed. The analogous bound holds for the `g_y` vectors restricted to `A`.

This **counting argument is over C** (or the usual complex Hilbert space), not a claim about positivity over arbitrary finite fields.

## Theorem 26.4: all-weights fixed-template permutation obstruction

Let `pi_1,...,pi_q` be arbitrary permutation orders of `s` vertices, all globally shared templates in the horizontal terms of (2). Repeated applications of Erdős–Szekeres produce a subset `B` of length at least

\[
L_q(s)=\underbrace{\left\lceil\sqrt{\cdots\left\lceil\sqrt{s}\right\rceil}\right\rceil}_{q-1\ \text{square-root operations}}
\tag{12}
\]

that is monotone (in either direction) in **every** template. For a split `B=X ⨿ A` into an initial and terminal segment of sizes `u,v`, `u+v<=L_q(s)`, the Green crossing ranks are at most `r_Y` and `r_X`, respectively, for **all weights**.

Apply (9) to each off-axis pair `(y,b)` with `y != b`, then (11):

\[
s(s-1)\le s\left\lfloor \frac{sr_Y}{u}\right\rfloor
+s\left\lfloor\frac{sr_X}{v}\right\rfloor.
\]

In particular the *exact complex* factorization requires

\[
\boxed{\frac{r_Y}{u}+\frac{r_X}{v}\ge1-\frac1s.}\tag{13}
\]

This is weight-independent, holds with **arbitrary vertical rook matrices**, and allows completely unrelated complex edge weights within and between all cycles. It does not demand aligned natural intervals, and remains valid for the fully interleaved or bit-reversed traversals that escaped the *natural-cut* test from Phase 25.

**Asymptotic corollary:** for fixed `q, r_X,r_Y`, the length `L_q(s)` diverges; choose `u,v` both diverging. Then (13) fails for all sufficiently large sides `s`. Consequently any **fixed-depth two-layer** network with a constant number of globally templated Green cycles per horizontal fiber is impossible for unbounded square transform lengths.

### Explicit two-template corollary

For `q=2`, one Green term per horizontal stage (`r_X=r_Y=1`), every `s>=17` has `L_2(s)>=5`; choose `u=2,v=3`. Then

\[
\frac12+\frac13=\frac56<1-\frac1s.
\]

Thus **every** pair of globally fixed traversal permutations fails, regardless of whether they are equal, inverse, random, bit-reversed, maximally interleaved, or independently chosen, and regardless of arbitrary complex weights:

\[
\boxed{s\ge17\ \Longrightarrow\ F_{s^2}\ne (Y_H+Y_V)(X_H+X_V).}\tag{14}
\]

Here each horizontal stage has *one* weighted cyclic Green per fiber, with its globally fixed traversal order; both vertical rook matrices are arbitrary. This is **not** a no-go for fiber-dependent permutations.

### Stronger prime-side subcase (no Chebotarëv theorem needed)

For prime `s`, two distinct characters restricted to **any two distinct coordinates** cannot be proportional, because `gcd(s, x_1-x_0)=1`. Thus an arbitrary rank-one subspace on two coordinates can contain at most one Fourier mode. Any two template orders possess a common monotone subset of length >=4 for prime `s>=11`. Splitting it into `u=v=2` shows the two crossed-path locks can cover at most `2s` pairs, fewer than `s(s-1)`. Therefore (14) also holds for **all prime sides `s>=11`**.

## Lemma 26.5: independent all-weights finite-field certificate for rank-one cuts

Let `K` be a field containing a primitive `s`-th root of unity, of characteristic not dividing `s`. For a nonempty `X`, choose `x_0∈X` and set

\[
g_X=\gcd(s,\{x-x_0:x\in X\}).\tag{15}
\]

If one Fourier mode `f_{b_0}|_X` lies on a given one-dimensional line, exactly `g_X` modes lie on that same line, since `f_b|_X` is proportional to `f_{b_0}|_X` precisely when `(b-b_0)(x-x_0)≡0 mod s` for all `x∈X`. And `g_X <= floor(s/|X|)`. Thus for **one Green term per horizontal stage**, the bound `s(g_X+g_A)<s(s-1)` is an all-weights impossibility certificate over the field, independent of Hilbert-space positivity.

All tests here use a field containing the required *primitive `s²`-th root*, so the whole Fourier target is well-defined. The finite-field certificates are an independent algebraic control, **not** a generalization of (10) to finite fields.

Saved exact certificates use `GF(65537)` at sides 32, 64, 128 and 256 and prime-side fields `GF(727)` at `s=11`, `GF(677)` at `s=13`, and `GF(3469)` at `s=17`, with primitive field generators as reported. Each has a nonzero scalar `(left annihilator) * (Fourier block) * (right annihilator)` yet zero for **all** arbitrary vertical completions with the pinned horizontal cycles. The combinatorial rank-one line bound separately certifies *all possible* horizontal weights.

## Theorem 26.6: all-order multiscale approximation obstruction

An even stronger result is available when **every horizontal Green term uses one shared permutation order `pi`** (or its reverse). This includes the bit-reversed cycles with maximal natural dyadic cut rank.

For a balanced binary interval tree in the `pi` order, every oriented sibling rectangle `(X,A)` has horizontal Green ranks at most `r_Y` and `r_X`. The sets `X,A` need **not** be consecutive in natural index order: the tight frame identity (10) works for every subset.

Orthogonal projection of each Fourier off-axis block onto the orthogonal complements of the column/row spaces in (7) yields a weight-independent error-energy inequality. If the sibling rectangles over all tree nodes are `R_pi`, then

\[
\boxed{
\frac{\|F_{s²}-T\|_F^2}{\|F_{s²}\|_F^2}
\ge \frac1{s^4}\sum_{(X,A)\in R_\pi}
\left[s(s-1)|X||A|-s^2(|A|r_Y+|X|r_X)\right]_+.
}\tag{16}
\]

Every offdiagonal ordered pair `(x,a)` belongs to exactly one oriented sibling rectangle, so there is **no double counting**. The right-hand side depends only on the *sizes* of the binary tree nodes, not on permutation `pi` or the weights. By the same balanced-tree estimate established in Phase 25, when `r_X+r_Y=o(s)`, the right-hand side tends to **1**.

Thus **any shared-order** two-stage network with sublinear horizontal Green term count satisfies

\[
\boxed{\frac{\|F_{s²}-T\|_F}{\|F_{s²}\|_F}\ge1-o(1).}\tag{17}
\]

The same lower bound holds for the spectral norm of the normalized Fourier difference `U_N-T/s`. This theorem does **not** apply unchanged to two distinct stage-specific orders: there is no single shared sibling partition on which both stages have low Green cut rank.

## Constructive control: bit reversal defeats natural dyadic rank cuts, not Fourier compatibility

For `s=2^k`, define `pi` to list each vertex by the bit reversal of its `k`-bit binary index. Consider any pair of **aligned natural dyadic siblings** `(X,A)`, each of size `2^h`. The restricted traversal alternates between `X` and `A` exactly `2^h` times. Lemma 26.1 therefore gives

\[
\boxed{\operatorname{rank}G[X,A]=2^h}\tag{18}
\]

for nonzero edge weights and nonsingular monodromy. This is *maximal* rank on **every** such natural dyadic cut. Yet Theorems 26.4 and 26.6 exclude the corresponding globally shared-order architecture from exact Fourier execution at sufficiently large lengths, and give an asymptotic approximation floor approaching 1.

Tested exact-field sizes `s=4,8,16,32,64`: all `s-1` natural dyadic sibling blocks passed the full-rank check. A second independently interleaved permutation was also tested to have a full natural balanced-cut rank while the two-order factorization was rejected via different, *permutation-aligned* cuts.

## What this does and does not prove

**Established here:** exact rank/cyclic-alternation characterization for weighted Hamiltonian Green inverses; Fourier-frame capacity bound on arbitrary coordinate subsets; common-monotone-subsequence all-weights no-go for any constant number of shared permutation templates; an all-order, asymptotically unit-error two-stage approximation barrier; explicit full-natural-dyadic-rank positive controls; and exact modular/nonlinear-vertical completion witnesses.

**Not established:** any factorization of the arbitrary-input Fourier matrix with fewer than `N log N` operations, a universal lower bound on FFTs, any exclusion of networks whose cycle orders vary independently between fibers, a third or deeper stage, a proof of independent mathematical novelty, or realistic speedups against FFTW/NTT. These restrictions concern a carefully stated 2-stage network grammar.

## Prior work and provenance

The phase relies on classical Erdős–Szekeres monotone subsequences, finite Fourier orthogonality, Green/quasiseparable inverse structure, and classical operator low-rank projections. See the inherited Phase 25 proof for its original natural-coordinate multiscale estimate. Related literature includes Boito–Eidelman, *Computation of quasiseparable representations of Green matrices* (Linear Algebra Appl., 2025); Li–Yang–Martin–Ho–Ying, *Butterfly Factorization* (SIAM, 2015); and Solomonik, *Sparse LDL, LU, and inverse butterfly factorization via tree decomposition* (arXiv v5, July 2026). No publication novelty is claimed without a substantial independent review.
