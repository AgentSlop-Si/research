# Supplement v1: inverse diagonal-plus-low-rank obstruction

17 October 2026. This is a separately frozen supplement. The original REPORT.md, SHA256 b50edd28ad4ceb2feb52dc861e0586337581d13106bd94b8a1e98bc933806326, is unchanged.

## Result and boundary

Let $r$ be a nonnegative integer and $N\geq4r+4$. For every primitive $N$-th root $\zeta$ and every middle permutation $P$, no factorization $F_N=BPA$ exists in the same separated-generator stage chart if either inverse stage can be written

\[
C=D+R,\qquad D\text{ diagonal},\qquad \operatorname{rank}R\leq r.
\]

For the pinned $F_8$ target, take $r=1$. This excludes inverse diagonal-plus-rank-one stages, including the dense inverse $I-J/9$ appearing in the original report's boundary example. This is a second restricted-family obstruction, not an extension of the theorem to all inverse stages.

**The unrestricted owner M-NONLINEAR-COMPATIBILITY remains TO RESEARCH, with priority unchanged.** The original 64-equation target-fiber ideal is still undecided. There is no numerical nonexistence inference, worldwide-novelty claim or algorithmic runtime claim.

## Proof

First consider any invertible $C=D+R$ with $\operatorname{rank}R\leq r$. If $x\in\ker D$ and $Rx=0$, then $Cx=0$, so $x=0$. Thus the restriction of $R$ to $\ker D$ is injective, giving

\[
\dim\ker D\leq\operatorname{rank}R\leq r.
\]

Since $D$ is diagonal, at most $r$ of its diagonal entries vanish.

Fix $m$ consecutive Fourier row indices and any $m$ distinct column indices, where $1\leq m\leq N$. The corresponding submatrix of $F_N D$ has at least $m-r$ nonzero columns. The nonzero columns are independent: after removing their nonzero scalars, they form a consecutive-row Vandermonde matrix at distinct roots. Therefore its rank is at least $m-r$. The corresponding submatrix of $F_N R$ has rank at most $r$. The elementary rank inequality gives

\[
\operatorname{rank}\big((F_N C)_{\text{selected rows, selected columns}}\big)
\ \geq\ m-2r.
\]

Column permutation does not change this conclusion. Choose $m=2r+2$, the last $m$ Fourier rows and the first $m$ columns of $F_N C P^{-1}$. Since $N\geq2m$, these row and column sets define a strict lower cut block of a stage. Its rank is at least two.

If $F_N=BPA$ and $C=A^{-1}=D+R$, then $B=F_N C P^{-1}$. The stage formula $B_{ij}=l_i m_j$ for $i>j$ makes that strict lower block rank at most one, a contradiction.

If $B^{-1}$ instead has the stated form, transpose the factorization. Fourier symmetry $F_N^T=F_N$, invariance of the stage chart under transpose, and invariance of diagonal-plus-rank-$r$ matrices under transpose reduce to the case just proved. This proves the theorem.

Invertible diagonal rescalings of the Fourier target are also excluded: left or right invertible diagonal multiplication preserves the diagonal-plus-rank-$r$ class and the stage chart, exactly as in the original report.

## A concrete boundary outside both F8 restrictions

The two obstructions together still do not cover the stage chart. Define the accepted-chart stage

\[
A_{ij}=\begin{cases}
3&i=j,\\
1&i>j,\\
2&i<j.
\end{cases}
\]

Its inverse is $C=H/511$, where

\[
H_{ij}=\begin{cases}
255&i=j,\\
-2^{\,8-(j-i)}&i<j,\\
-2^{\,i-j-1}&i>j.
\end{cases}
\]

The supplement checker verifies all 64 equations $AC=I$ exactly. The entry $C_{0,2}=-64/511$ is nonzero, so $C$ is not cyclic tridiagonal. Moreover

\[
\det C_{\{0,2\},\{1,3\}}=\frac{32}{511}\ne0.
\]

The row and column index sets in this minor are disjoint. If $C=D+R$ with $D$ diagonal and $\operatorname{rank}R\leq1$, this submatrix would equal the corresponding submatrix of $R$ and have rank at most one. Its nonzero determinant contradicts that possibility. Thus this one genuine accepted-chart stage lies outside both inverse restrictions, without assuming any unknown Fourier factorization.

This example demonstrates the strictness of the combined restrictions; it is not a Fourier factorization and does not prove that a Fourier factorization exists in the remaining class.

## Sources and checks

The model and target are bound to the unchanged SOURCE_BINDING.json and accepted baseline report identified in the original report. The proof above is self-contained and uses only Vandermonde independence and elementary rank inequalities.

check_supplement_v1.py is newly authored standard-library code. It verifies the exact inverse and both nonzero boundary quantities. It imports or executes no historical program and does not import the original checker. SUPPLEMENT_V1_RESULTS.json records its exact results, and SUPPLEMENT_V1_MANIFEST.json binds this supplement separately while retaining the original report hash.
