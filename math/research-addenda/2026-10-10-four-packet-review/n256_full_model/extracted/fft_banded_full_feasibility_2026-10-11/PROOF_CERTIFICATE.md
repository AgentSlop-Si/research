# Proof certificate — pivot-safe scan inversion and exact lifted FFT feasibility

**Date:** 2026-10-11. **Status:** exact identities and independent modular controls; does **not** solve the Fourier factorization, nor establish a faster FFT or literature novelty.

## 1. All-pivot quasiseparable inverse through a banded augmented matrix

For a field `K`, define the order-one separated-generator scan matrix

\[
S_{ij}=\begin{cases}a_i b_j& i>j,\\ d_i&i=j,\\ c_i e_j&i<j.\end{cases}
\]

To solve `Sx=y`, introduce the two independent running sums

\[
L_i=\sum_{j<i}b_jx_j,\qquad R_i=\sum_{j>i}e_jx_j.
\]

For each coordinate `i`, impose three equations in the interleaved unknowns `(x_i,L_i,R_i)`:

\[
\begin{split}
y_i&=d_ix_i+a_iL_i+c_iR_i,\\
L_0&=0,\quad L_i-L_{i-1}-b_{i-1}x_{i-1}=0\quad(i>0),\\
R_{N-1}&=0,\quad R_i-R_{i+1}-e_{i+1}x_{i+1}=0\quad(i<N-1).
\end{split}
\]

Let `B_N` be this `3N × 3N` coefficient matrix. By construction it has lower bandwidth at most four and upper bandwidth at most three in the interleaved order. Its entries are polynomial in the generators; there are no coefficient divisions. The equations for `L` and `R` have a **unique solution for every x**, since they are triangular recurrences with boundary data. Eliminating `L,R` therefore yields exactly `Sx=y`.

The block of `B_N` corresponding to the `L,R` equations and unknowns is triangular (in each family), with diagonal entries equal to one; it has determinant one. After simultaneously reordering rows and columns to put `x` first, the Schur-complement identity gives

\[
\boxed{\det B_N=\det S.}
\]

This is a polynomial identity, valid over arbitrary fields and at zero pivots or singular coefficients. In particular, **B_N is invertible iff S is invertible.** An exact banded Gaussian elimination with partial pivoting only within its constant lower bandwidth therefore solves `Sx=y` in `O(N)` field operations. The executable verifier uses a conservative pivot window of eight and also tests a window of four.

The algorithm is an application of known quasiseparable/banded linear algebra, not a new generic complexity result. This project implements it with the exact generator convention used by its Fourier feasibility solver.

## 2. Complete quadratic encoding of an exact t-stage Fourier factorization

Fix `N`, `t`, and permutations `P_1,...,P_(t-1)`. For every standard basis column `e_j` introduce each stage's input vector `x^(s,j)` and running sums `L^(s,j), R^(s,j)`, with `x^(1,j)=e_j`. At each stage impose

\[
\begin{aligned}
L_{i+1}^{(s,j)}-L_i^{(s,j)}-b_i^{(s)}x_i^{(s,j)}&=0,\\
R_i^{(s,j)}-R_{i+1}^{(s,j)}-e_{i+1}^{(s)}x_{i+1}^{(s,j)}&=0,
\end{aligned}
\]

with boundary values `L_0=R_(N-1)=0`. Let

\[
y_i^{(s,j)}=d_i^{(s)}x_i^{(s,j)}+a_i^{(s)}L_i^{(s,j)}+c_i^{(s)}R_i^{(s,j)}.
\]

For `s<t`, impose `x_i^(s+1,j)=y_(P_s[i])^(s,j)`. For the last stage impose

\[
y_i^{(t,j)}=U_{ij}=\zeta_N^{ij}/\sqrt N.
\]

Every polynomial in the resulting system has total degree at most two and at most four additive terms. The scanning-state recurrences uniquely determine each output from the input at each stage. Hence the system is solvable **if and only if**

\[
\boxed{S_tP_{t-1}\cdots P_1S_1=U_N.}
\]

The proof is bidirectional: a valid factorization provides a witness for every internal variable; conversely, a solution of these equations computes every basis output and therefore the complete linear operator. Since `U_N` is invertible, all `S_s` must be invertible; no determinant saturation constraints are required for this **complete** system. This last conclusion is **not true** for the previous 550 selected minor equations, which were only necessary conditions.

When the two boundary coordinates of each scan are fixed as literal zeros, rather than treated as unknowns, the counts for `N=256,t=4` are:

| Type | Number |
|---|---:|
| Generator coefficients | `5tN=5120` |
| Intermediate stage input values | `(t-1)N²=196608` |
| Free prefix/suffix sums | `2tN(N-1)=522240` |
| **Total unknowns** | **723968** |
| Stage-output/coupling equations | `tN²=262144` |
| Running-sum equations | `2tN(N-1)=522240` |
| **Total equations** | **784384** |

The coefficients lie in `Q(zeta_256)` for the exact complex FFT. The modular tests instantiate them in two primes containing primitive 256th roots. A finite-field feasible witness alone would **not** prove a complex solution.

## 3. An exact incidence-system alternative to 17x17 minors

For one selected `128×128` block `B=G[I,J]` from the original 64 Jacobi-dual gates, `rank(B)<=b` if and only if there exists a `128×(128-b)` full-column-rank kernel matrix `Z` satisfying `BZ=0`. Full column rank is equivalent to at least one invertible `(128-b)`-row minor of `Z`; by a change of basis in its columns, it can be normalized to identity. Thus the rank condition is equivalent to the **union of polynomial charts**

\[
\boxed{BZ=0,\quad Z[K,:]=I_{128-b}},
\]

as `K` varies over `(128-b)`-element row subsets. This equivalence includes the zero-generator, singular-minor and rank-`<b` branches. No chart may be discarded without further proof.

For the strongest saved mask `64`, `b=16`: a fixed chart has `16×112=1792` free kernel variables and `128×112=14336` equations. Because `B` is bilinear in the two outer-stage generator matrices (whose entries themselves are linear or bilinear in generators), its exact degree in raw generator coordinates may be **up to five**, not automatically three. More precisely, it is **cubic in the outer-stage matrix entries plus Z** (bilinear in S1/S4 entries times Z), and degree at most five in the five raw separated-generator arrays. This distinction must be retained in any symbolic solver.

The archived valid synthetic middle product has rank exactly 16 in the selected gate. Exact elimination produced a normalized 112-dimensional kernel witness modulo both 12289 and 65537. The saved Fourier-target outer-generator witness has rank 128, so it fails that same necessary gate; this is only a rejection of the saved parameter point.

## 4. Scientific limitations

- There is **no** feasible factorization of `F256` in this checkpoint. The original architecture's feasibility is unresolved.
- The quadratic full-coefficient lift is large; bounded degree alone does not make computational elimination practical.
- The 550-minor system remains a useful smaller necessary-condition screen. Its spurious singular and near-singular roots remain real concerns unless stage invertibility is imposed.
- The kernel incidence lift is exact only as a **union of pivot charts**; fixing one chart covers one open patch.
- The middle-operator `H=G^-1` computes with a classical FFT internally, so its `O(N log N)` per-vector evaluation is **not** an improved FFT.
- Efficient structured solves and incidence systems for determinantal varieties are established ideas. These are model-specific applied tools whose external novelty has not been demonstrated.

## 5. Exact verification

Run `OPENBLAS_NUM_THREADS=1 bash RUN_ALL.sh`.

Independent controls compare the banded determinant to 252 dense finite-field determinants, perform 246 invertible stage roundtrips and eight zero-diagonal roundtrips (including N=1024), reconstruct the actual saved Fourier-layout middle operator on 30 vectors, evaluate the quadratic witness on all 512 basis-column/field combinations, and check the strongest rank-16 kernel chart and rank-128 Fourier-witness failure over two fields. The entire previous checkpoint is included intact.
