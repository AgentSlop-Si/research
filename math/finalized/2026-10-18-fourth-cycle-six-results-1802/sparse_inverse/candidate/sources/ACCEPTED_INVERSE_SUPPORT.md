# M-NONLINEAR-COMPATIBILITY: exact Fourier obstruction for the inverse-cyclic-tridiagonal slice

17 October 2026. Fresh bounded target-fiber result. Candidate for independent acceptance.

## Result and disposition

**New restricted-family obstruction:** For every integer $N\geq 8$, every primitive $N$-th root of unity $\zeta$, and every middle permutation matrix $P$, the Fourier matrix $F_{ij}=\zeta^{ij}$ cannot factor as $F=BPA$ in the accepted separated-generator chart if **either $A^{-1}$ or $B^{-1}$ is cyclic tridiagonal**. Ordinary tridiagonal inverses are included. All coefficients may be arbitrary complex numbers.

For the pinned $N=8$ permutation, the small exact certificate has determinant

\[
\Delta=28\zeta^3+28\zeta^2+12\zeta-12\ne 0,
\qquad N_{\mathbb Q(\zeta)/\mathbb Q}(\Delta)=2048.
\]

This settles an actual restricted target-fiber branch; it does not repeat the previous totally nonsingular matrix or dimension-60 witness. **Keep M-NONLINEAR-COMPATIBILITY open / TO RESEARCH.** The unrestricted 64-equation ideal is still undecided. The cyclic-tridiagonal-inverse hypothesis is a genuine additional restriction, not a consequence of the accepted stage chart.

No worldwide novelty, general Fourier lower bound, or runtime improvement is claimed. No historical script was run, no numerical fit was used, and no external write was made by this worker.

## 1. Exact source binding and model

The accepted baseline is [network/REPORT.md at commit bcbc3854c9af6bac7ccaf8378c1629ae63889fbb](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-17-research-finalization-0222/reports/network/REPORT.md), Git blob `b1ec71aadc96c08161d69bc2c42d057416b3636a`. Its text is retained as `SOURCE_REPORT.md`; `SOURCE_BINDING.json` records the pin.

The baseline fixes, for row and column indices starting at zero,

\[
S_{ii}=d_i,\qquad S_{ij}=l_i m_j\;(i>j),\qquad S_{ij}=u_i v_j\;(i<j).
\]

In particular every strict lower cut block, such as rows $N-4,\ldots,N-1$ and columns $0,\ldots,3$ when $N\geq8$, has rank at most one. This follows directly from the displayed outer product; it is not a graph-capacity inference. Transposes of permitted stages are permitted, with lower and upper generators exchanged.

The baseline's fixed permutation is

\[
p=[7,0,6,3,4,1,2,5],\qquad Pe_j=e_{p(j)},
\]

and its exact equation is $F=BPA$. The new general-$N$ statement uses the same stage definition in size $N$ and allows any $P$. Restricting it back to $N=8$ and the displayed $p$ gives the requested target branch.

A matrix $C$ is **cyclic tridiagonal** here when

\[
C_{s,k}=0\quad\text{unless }s\equiv k-1,k,k+1\pmod N.
\]

Zeros on the permitted diagonals are allowed. No nonvanishing individual-entry hypothesis is imposed. Ordinary tridiagonal matrices satisfy this support condition.

## 2. The four-column lemma

Let $N\geq8$, and let $C$ be an invertible cyclic tridiagonal matrix. Fix four distinct column centers $k_1,k_2,k_3,k_4$, and restrict $FC$ to its last four rows. **The resulting $4\times4$ matrix has rank at least two.**

### Proof

Write $t_k=\zeta^k$ and $a=1+\zeta+\zeta^{-1}$. The three possible frequencies in column $k$ are $k-1,k,k+1\pmod N$. Hence the four-entry column vector $y_k$, whose entries are indexed by $r=0,1,2,3$, is

\[
(y_k)_r=\sum_{s\in\{k-1,k,k+1\}\bmod N}C_{s,k}\,\zeta^{(N-4+r)s}.
\]

The map from these three coefficients to $y_k$ is injective: its first three rows form a Vandermonde matrix at three distinct roots, multiplied by nonzero column scalars. Therefore $y_k\ne0$, since invertibility of $C$ ensures that column $k$ is nonzero. This step covers all coefficient-zero subcases without a genericity assumption.

The polynomial

\[
q_k(x)=\prod_{s\in\{k-1,k,k+1\}\bmod N}(x-\zeta^s)
=x^3-a t_k x^2+a t_k^2x-t_k^3
\]

annihilates this four-entry exponential vector. With coefficients in ascending degree, put

\[
Q_k=(-t_k^3,\ a t_k^2,\ -a t_k,\ 1),\qquad Q_k y_k=0.
\]

The four rows $Q_{k_j}$ are linearly independent, because

\[
\det\begin{pmatrix}Q_{k_1}\\Q_{k_2}\\Q_{k_3}\\Q_{k_4}\end{pmatrix}
=a^2\prod_{1\leq i<j\leq4}(t_{k_j}-t_{k_i})\ne0.
\]

The roots are distinct. Also $a=0$ would imply $\zeta^2+\zeta+1=0$, making $\zeta$ a primitive third root, impossible for $N\geq8$.

If the four columns $y_{k_j}$ had rank at most one, their nonzeroness would give $y_{k_j}=\lambda_j y$ for a common nonzero $y$ and nonzero scalars $\lambda_j$. Each $Q_{k_j}y=0$. The invertible four-row coefficient matrix would then force $y=0$, a contradiction. This proves the lemma. \(\square\)

The proof actually only uses that the four selected columns have the displayed three-frequency supports; the other columns of $C$ may be arbitrary. Cyclic tridiagonality is a uniform, permutation-independent way to guarantee those supports.

## 3. Consequence for the exact target fiber

Suppose $F=BPA$. The Fourier and permutation matrices are invertible, so $A$ and $B$ are invertible. If $C=A^{-1}$ is cyclic tridiagonal, then

\[
B=FCP^{-1}.
\]

Columns $0,1,2,3$ of $B$ correspond to four distinct columns of $FC$, irrespective of $P$. The four-column lemma says their restriction to rows $N-4,\ldots,N-1$ has rank at least two. The stage formula says that same strict lower block is an outer product and has rank at most one. Contradiction.

If instead $B^{-1}$ is cyclic tridiagonal, transpose the assumed factorization. Since $F^T=F$,

\[
F=A^T P^T B^T.
\]

This is another permitted-stage factorization with an arbitrary middle permutation and right-stage inverse ($B^{-1}$^T), which is cyclic tridiagonal. The previous argument again contradicts existence. \(\square\)

The result also excludes invertible diagonal rescalings $D_L F D_R$ as targets under the same restriction. Such a factorization would yield (F=$D_L^{-1}B$P$AD_R^{-1}$); diagonal scaling preserves the stage chart and the relevant inverse support. This is a consequence, not an additional endpoint-permutation claim.

## 4. Pinned F8 certificate

For $p=[7,0,6,3,4,1,2,5]$, columns $0,1,2,3$ of $FCP^{-1}$ select columns $1,5,6,3$ of $FC$. Their supports, in that order, are

\[
\{0,1,2\},\quad\{4,5,6\},\quad\{5,6,7\},\quad\{2,3,4\}.
\]

Work in (K=\mathbb Q[\zeta]/$\zeta^4+1$). The four annihilator rows are

\[
Q=\begin{pmatrix}
-\zeta^3 & \zeta^3+\zeta^2+\zeta & -\zeta^2-\zeta-1 &1\\
\zeta^3 & \zeta^3+\zeta^2+\zeta & \zeta^2+\zeta+1 &1\\
-\zeta^2 & \zeta^3-\zeta-1 & \zeta^3+\zeta^2+\zeta &1\\
-\zeta & -\zeta^3-\zeta^2-\zeta & -\zeta^3-\zeta^2+1 &1
\end{pmatrix}.
\]

Its determinant is $\Delta=28\zeta^3+28\zeta^2+12\zeta-12$, with the particularly small inverse certificate

\[
\Delta\left(-\tfrac58\zeta^3+\tfrac14\zeta^2+\tfrac14\zeta-\tfrac58\right)=1
\quad\text{modulo }\zeta^4+1.
\]

Thus the certificate is characteristic-zero and exact. It excludes the restricted branch over the algebraic closure and over \(\mathbb C\); it does not infer complex infeasibility from a finite-field experiment.

## 5. The restriction is meaningful and strictly narrower

The restricted slice has genuine accepted-chart members. Let (C=\operatorname{tridiag}$-1,2,-1$) in size eight. Its inverse is

\[
A_{ij}=\frac{(\min(i,j)+1)(8-\max(i,j))}{9}.
\]

For $i>j$, this is ($8-i$$j+1$/9); for $i<j$, it is ($i+1$$8-j$/9). Hence $A$ is exactly a separated-generator stage. The checker verifies $CA=I$ entrywise.

Conversely the full stage chart does not force a cyclic-tridiagonal inverse. With $J$ the all-ones $8\times8$ matrix, $A=I+J$ is a permitted stage: off-diagonal generators can all equal one, and the diagonal is two. But $A^{-1}=I-J/9$, whose ($0,2$) entry is $-1/9\ne0$. The checker verifies this inverse as well. Consequently the restricted obstruction cannot be promoted to nonexistence in the whole source chart.

## 6. Reproducibility and exact remaining gate

Run `python3 check_restricted_fiber.py`. The program uses only Python's standard library and independently constructs arithmetic in (\mathbb Q[\zeta]/$\zeta^4+1$). It checks:

- The four pinned annihilator rows, determinant, reciprocal certificate and field norm 2048.
- All 24 annihilator dot products for the eight three-frequency supports.
- Injectivity of all eight restricted $4\times3$ Fourier maps through exact $3\times3$ minors.
- The scaled Vandermonde determinant identity for all 70 four-frequency subsets.
- The accepted-chart tridiagonal-inverse example and the dense-inverse counterexample to an unwarranted chart restriction.

`RESULTS.json` contains exact rational coefficient vectors. `RUN.log` records the successful run. The general-$N$ proof is analytic algebra above; finite checks are supporting certificates, not a substitute for that proof.

The accepted unrestricted problem remains

\[
I_F=\langle(BPA)_{ij}-\zeta_8^{ij}:0\leq i,j<8\rangle
\subset\mathbb Q(\zeta_8)[\theta],
\]

with the original 80 displayed parameters and no inverse-support restriction. This work proves emptiness only after requiring a cyclic-tridiagonal inverse for at least one stage. It neither constructs a solution of $I_F$ nor proves $1\in I_F$, and gives no polynomial excluding $F_8$ from the unrestricted image closure.

**Precise missing step:** control the dense inverse columns allowed by a general separated-generator stage, without imposing three-frequency support. Those columns need not lie in the fixed three-dimensional Fourier subspaces used here, so the annihilator Vandermonde contradiction does not apply. A valid next step must settle that general target fiber, or explicitly state and certify another genuinely restricted branch. No owner-priority change is justified by the present result.
