# Hero #1 — Phase 29: 120-point noncoprime-stage fusion and two rejection theorems

**Date:** 2026-10-10. **Status:** exact characteristic-zero identities, complete finite-field executable circuits and basis replays. **Not** a new sub-`N log N` Fourier bound, a claim of Winograd priority, or a numerical stability result.

## 1. Exact scalar model and main theorem

Let `h=2^t` for `t>=0` and `N=120h=15(8h)`. Let `F` be a field of characteristic not 2 containing a primitive `N`th root `w`; in characteristic zero the construction applies to complex roots. The unnormalized transform is

\[
(F_Nx)_k=\sum_{j=0}^{N-1} w^{jk}x_j.
\]

Field addition/subtraction costs one data operation; multiplication by a predetermined coefficient unequal to 1 costs one data operation. Twiddles such as `i` are *not* assumed free. Integer modular indices, CRT memory traffic, finite-field bit costs and coefficient preparation are separately scoped.

**Theorem (explicit all-input 120-fused circuit).** There is a fully expanded arithmetic network for `F_N` requiring at most

\[
A_{29}(N)=120h\log_2h+1038h\quad\text{additions},
\]
\[
M_{29}(N)=60h\log_2h+125h+15\quad\text{nonidentity scalar multiplications},
\]
\[
\boxed{T_{29}(N)=180h\log_2h+1163h+15.}
\]

In characteristic zero and in both independently tested prime fields, all these counts are exact, not merely upper bounds. On exceptional fields, accidental additional identity diagonal entries can only reduce the multiplicative count. Against the Phase 28 circuit with the same `N` and input conventions,

\[
T_{28}(N)=180h\log_2h+1176h+15,
\qquad\boxed{T_{28}-T_{29}=13h=N\frac{13}{120}.}
\]

This saves **43h scalar multiplications while spending 30h additional additions**; the net saving is `13h`. It remains `Theta(N log N)`.

## 2. Exact eight-point pre/diagonal/post codelet

Let `z` be a primitive 8th root, `i=z^2`,
\[
 c_+=z(1+i)/2,\qquad c_-=z(1-i)/2.
\]

For `j=0,...,3`, prepare `s_j=x_j+x_{j+4}` and `t_j=x_j-x_{j+4}` (eight additions). The eight before-diagonal channels in order are

\[
B_8x=(s_0+s_2,\ s_1+s_3,\ s_0-s_2,\ s_1-s_3,\ t_0,\ t_2,\ t_1+t_3,\ t_1-t_3).
\]

This costs 14 additions in total. Multiply them componentwise by

\[
\boxed{D_8=\operatorname{diag}(1,1,1,i,1,i,c_+,c_-).}
\]

Four central coefficients equal 1 and four are nontrivial. Denote the eight scaled channels by `z_0,...,z_7`. Apply the following 12-addition decoder:

\[
\begin{aligned}
 y_0&=z_0+z_1,&y_4&=z_0-z_1,\\
 y_2&=z_2+z_3,&y_6&=z_2-z_3,\\
 u_+&=z_4+z_5,&u_-&=z_4-z_5,\\
 v_+&=z_6+z_7,&v_-&=z_6-z_7,\\
 y_1&=u_++v_+,&y_5&=u_+-v_+,\\
 y_3&=u_-+v_-,&y_7&=u_--v_-.
\end{aligned}
\]

`symbolic_phase29.py` independently reconstructs integer matrices `A_8,B_8` and certifies, for every matrix entry, that

\[
A_8D_8B_8=F_8
\]

by exact polynomial division modulo `Phi_8(z)=z^4+1` over `Q`. The short algorithm uses **26 additions and four nonidentity scalar multiplications**. It is a classical Winograd-type factorization; see `PRIOR_ART.md`.

## 3. Tensor with the established 15-point Winograd factorization

The preserved Phase 28 `wfta15.py` provides `F_15=A_15 D_15 B_15`. Its rational/integer addition network has 39 pre-additions and 42 post-additions; the diagonal has width 18, with exactly one identity and 17 nonidentity scalings in characteristic zero.

Because `gcd(15,8)=1`, CRT permutations produce the exact 120-point tensor

\[
F_{120}=P_{\rm out}(A_{15}\otimes A_8)(D_{15}\otimes D_8)
 (B_{15}\otimes B_8)P_{\rm in}.
\]

The carefully selected execution order is `B8 -> B3 -> B5 -> D120 -> A5 -> A3 -> A8`. All intermediate data values are materialized and charged. Its additions are:

- Pre-diagonal: `15*14 + 8*39 = 522`.
- Post-diagonal: `8*42 + 15*12 = 516`.
- Total: **1038 additions**.

The central diagonal has `18*8=144` channels. `symbolic_phase29.py` checks all 144 polynomial differences from one modulo `Phi_120` and finds **exactly four identity channels**. Hence **140 scalar multiplications**, total **1178 field operations**.

The CRT permutations require moving/indexing data and are not counted as field additions; this exclusion is explicitly retained in the cost model.

## 4. Whole-length transform, including noncoprime coupling

Write `G=8h`, so `gcd(15,G)=1`. Outer CRT permutations split the length `N=15G` input into 15 independent `G` columns. Each of those uses a Cooley–Tukey `(8,h)` split, because `gcd(8,h)` is usually not 1:

1. Execute 120 independent length-`h` radix-2 FFTs. They cost `120h t` additions and `60h t-120h+120` multiplications.
2. Pay all `(8,h)` twiddle scalings, exactly `15*7*(h-1)=105(h-1)` multiplications: none is silently cancelled.
3. Execute `h` complete 120-point tensor kernels: `1038h` additions and `140h` multiplications in characteristic zero.
4. Scatter all `N` Fourier outputs to natural order.

Adding the complete ledger proves the theorem. The implementation is `fused120.py`; it makes no uncharged calls to an `F_N` oracle.

## 5. Cold arithmetic, finite-field and memory scope

Both Phase 28 and Phase 29 start from **exactly the same** `make_wfta_plan(N)` coefficient and root table. Phase 28 prepares 17 additional 60-point diagonal products. Phase 29 prepares the 8-point phases using four multiplications plus two additions (`i` is reused from the existing roots table) and 68 nontrivial 15x8 tensor products, 74 extra operations total. Thus its additional setup relative to Phase 28 is 57 field operations.

\[
\boxed{T_{28}^{\rm cold}-T_{29}^{\rm cold}=13h-57.}
\]

It is negative for `h=1,2,4`, and first positive for `h=8` (`N=960`); setup is not free. Integer primitive-root testing, modular CRT inverses, software allocation, cache/memory traffic, and bit complexity are not part of the field-add/multiply count. The full transform uses `O(N)` field-element storage plus constant-size 120/144-channel work buffers; it is **not** in-place and no wall-clock speedup is claimed.

## 6. New restricted obstruction: C4-free gauge graph

Let `b,h>=1`, let `xi` have exact order `b h`, and let

\[
T_{u,q}=\xi^{u q},\qquad 0\le u<b,\quad0\le q<h.
\]

Allow arbitrary nonzero scalings `r_u,c_q` of rows and columns, even granting these rephasings for free. Construct a bipartite graph whose edges are positions with `r_u T_{u,q} c_q=1`. No two row vertices can be adjacent to the same two column vertices: otherwise the four equalities imply

\[
\xi^{(u-v)(q-q')}=1,
\]

impossible because `0<|(u-v)(q-q')|<bh`. So the bipartite graph is `C4`-free. Let `d_q` be its degree at column `q`. Every row-pair has at most one common column, so

\[
\sum_q {d_q\choose 2}\le {b\choose 2}.
\]

Using `d-1<=d(d-1)/2` for positive `d` and zero for `d=0`, we obtain

\[
\boxed{\#\{(u,q):r_uT_{u,q}c_q=1\}\le h+{b\choose2}.}
\]

The ordinary ungauged twiddle diagonal already has `h+b-1` unit entries (`u=0` or `q=0`). Therefore **any** row/column gauge can save at most

\[
{b\choose2}-(b-1)={b-1\choose2}
\]

more multiplications than the original diagonal. In particular, for `b=8` the maximum additional saving is at most **21 scalars**, independent of `h`, even under *free* rephasing. This does not bound general multiwire additions, non-diagonal transforms, or nonlocal computation sharing.

`gauge_obstruction.py` independently enumerates root-of-unity gauges for `b=4` and `h=1,2,4,8`, checking the graph bound in every case. A small exhaustive check cannot establish general optimality, which is provided by the mathematical proof above.

## 7. New restricted obstruction: weighted F4 needs at least six fixed-rational diagonal channels

Consider the formal weighted 4-point DFT

\[
M(a)=F_4\operatorname{diag}(1,a,a^2,a^3).
\]

Suppose `M(a)=A diag(d_1(a),...,d_r(a)) B`, with **fixed rational** pre/post matrices `A,B` and complex polynomial/rational diagonal coefficients `d_l(a)`; only these diagonal coefficients depend on the formal parameter `a`.

Taking the rational real and imaginary parts of the coefficient matrices of `a^0,...,a^3` yields **six linearly independent matrices**: one for column 0, two for column 1, one for column 2 and two for column 3. Every such matrix must lie in the `Q`-linear span of the `r` fixed rational rank-one matrices `A[:,l] B[l,:]`. Thus `r>=6`. `weighted4_rank_gate.py` verifies this six-dimensional span and an explicit width-six factorization symbolically.

`weighted4_gate.py` realizes the width-six factorization and tensors it with the 15-point WFTA. At a generic nontrivial phase it requires 468 additions and 107 multiplications (575 operations), compared with 558 for Phase 28's 60-point kernel plus the 45-stage twiddles. Hence **this** diagonal-absorption attempt loses 17 operations per nonzero frequency block, instead of saving work. This is not an unrestricted lower bound for q-dependent pre/post programs or other higher-arity circuits.

## 8. Evidence, provenance, and limits

- `symbolic_phase29.py`: 64 exact `F8` entries modulo `Phi8`, plus 144 exact tensor-diagonal identity checks modulo `Phi120`.
- `test_phase29.py`: 11 new tests, including all 120 basis vectors of the short tensor, direct DFTs, both fields and coefficient mutation checks.
- `test_phase28.py`, `test_phase27.py`: 17 retained tests; **28/28 total** pass.
- `audit_phase29.py`: **2,448,000 distinct Fourier entries** from complete bases for sizes 120, 240, 480, 960 across two prime fields; **7,344,000 exact comparisons**, counting both Phase 28 and the prior 15-point alternative separately.
- `benchmark_phase29.py`: both fields and lengths 120 through 61,440; checks complete output vectors, exact operation formulas, and shared-root cold preparation.
- `gauge_obstruction.py`, `weighted4_rank_gate.py`, `weighted4_gate.py`: constructive negative-result audits.

The bounded-width gauge and weighted-4 results are project-specific lemmas using elementary existing algebra/graph arguments. No exhaustive literature search or independent formal proof assistant verification has established worldwide novelty. The short Winograd transform is classical and the all-input saving is a constant/lower-order refinement, not an independent `o(N log N)` breakthrough.
