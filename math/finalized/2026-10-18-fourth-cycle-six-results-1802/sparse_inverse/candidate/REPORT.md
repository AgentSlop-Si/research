# Arbitrary sparse-core inverse obstruction and one-debit rank repair

18 October 2026. Existing owner: **M-NONLINEAR-COMPATIBILITY**. New mathematical candidate for independent review. No external writes, new record IDs, owner-status changes, or priority changes.

## Result

In the accepted separated-generator stage chart, let

\[
F_N=BPA,\qquad (F_N)_{ij}=\zeta^{ij},
\]

where \(\zeta\) is a primitive \(N\)-th root of unity, \(P\) is any permutation matrix, and the field is \(\mathbb C\). There is **no such factorization** if

\[
A^{-1}=S+R,
\quad \text{each column of }S\text{ has at most }s\text{ nonzeros},
\quad \operatorname{rank}R\le r,
\quad N\ge(s+1)(r+2),
\]

for integers \(s\ge1\), \(r\ge0\). The sparse core \(S\) need not be invertible, and its nonzero positions are arbitrary. The transposed condition excludes a decomposition of \(B^{-1}\) into a **row-sparse** core plus rank at most \(r\).

Two useful consequences are:

1. Arbitrary column-sparse inverses with at most \(s\) nonzeros per column are excluded for \(N\ge2s+2\). This removes the previous cyclic-support restriction.
2. Diagonal-plus-rank-\(r\) inverses are excluded for **\(N\ge2r+4\)**, including singular diagonal cores. The accepted earlier bound was \(N\ge4r+4\). Thus the pinned \(F_8\) target now excludes diagonal-plus-rank-two inverses on either stage, as well as arbitrary three-sparse columns of \(A^{-1}\) or three-sparse rows of \(B^{-1}\).

The improved bound uses one rank debit, rather than two. The earlier theorem remains valid; its cutoff was sufficient but non-sharp for this argument. A local exact example below attains the new rank estimate, and separate examples show why consecutive samples, independence, and enough samples matter.

**The unrestricted 64-equation \(F_8\) target ideal remains undecided.** This is a reusable restricted-family theorem, not a global closure, historical-priority determination, or arithmetic-runtime lower bound.

## 1. Source and exact model

The current open-owner record is retained in `sources/OWNER_RECORD.json`, copied from the current third-cycle index (229 open, 98 closed). The assignment's repository main commit is `e6273471e459bd9fdf2e3ec38a468cd9ea592ae6`. No global catalogue audit was repeated.

Three exact primary task bodies were retrieved with the GitHub connector at immutable commits and retained locally:

- [Accepted chart and target](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-17-research-finalization-0222/reports/network/REPORT.md), Git blob `b1ec71aadc96c08161d69bc2c42d057416b3636a`.
- [Accepted cyclic-tridiagonal inverse obstruction](https://github.com/AgentSlop-Si/research/blob/511689fb34ffa88921b3d2a0dc801e048b49dce2/math/finalized/2026-10-17-resumed-mathematics-0916/reports/fourier_target/REPORT.md), Git blob `8fbc4b60b9591405464b1153698a35f90ce36674`.
- [Accepted diagonal-plus-low-rank supplement](https://github.com/AgentSlop-Si/research/blob/511689fb34ffa88921b3d2a0dc801e048b49dce2/math/finalized/2026-10-17-resumed-mathematics-0916/reports/fourier_target/SUPPLEMENT_V1.md), Git blob `ef7a44a6f5b88f783026182df501f33b48caa75d`.

The stage chart, in indices \(0,\ldots,N-1\), is

\[
T_{ii}=d_i,\qquad T_{ij}=l_i m_j\ (i>j),\qquad T_{ij}=u_i v_j\ (i<j).
\]

Individual generators may vanish. Every submatrix entirely below the diagonal has rank at most one; the same is true above the diagonal. Transposing a stage preserves this chart. The pinned \(N=8\) permutation is \(p=[7,0,6,3,4,1,2,5]\), with \(Pe_j=e_{p(j)}\). The new proof permits every \(P\), so it includes that source branch without changing its convention.

The field, fixed-coordinate stage chart, target, and original inverse-guard requirement are unchanged. Since \(F_N\) and \(P\) are invertible, any putative factorization already forces \(A,B\) invertible.

## 2. Consecutive Fourier sampling

Let \(I=\{a,a+1,\ldots,a+m-1\}\) modulo \(N\), with \(m\le N\), and let \(U\) be any set of at most \(m\) frequency indices. Then

\[
(F_N)_{I,U}
\]

has full column rank. Indeed, after multiplying column \(j\) by the nonzero inverse scalar \(\zeta^{-aj}\), its first \(|U|\) rows form the Vandermonde matrix at the distinct nodes \(\{\zeta^j:j\in U\}\). Its determinant is

\[
\prod_{j<k,\ j,k\in U}(\zeta^k-\zeta^j)\ne0.
\]

No assumption about contiguity or spacing of the **frequency** set \(U\) is used. Only the output rows are consecutive. Consequently, the sampling map \(T=(F_N)_{I,:}\) is injective on the entire coordinate subspace supported in \(U\).

## 3. One-debit kernel lemma

Let \(C_J=S_J+R_J\) be a matrix with \(k\) independent columns, and let \(T\) be any linear map that is injective on \(\operatorname{im}S_J\). Then

\[
\boxed{\operatorname{rank}(TC_J)\ge k-\operatorname{rank}R_J.}
\]

### Proof

On \(K=\ker(TC_J)\), consider the map \(x\mapsto R_Jx\). It is injective: if \(x\in K\) and \(R_Jx=0\), then

\[
0=TC_Jx=TS_Jx.
\]

Injectivity of \(T\) on \(\operatorname{im}S_J\) gives \(S_Jx=0\). Thus \(C_Jx=S_Jx+R_Jx=0\), and independence of the columns of \(C_J\) gives \(x=0\). Therefore

\[
\dim K\le\operatorname{rank}R_J,
\]

and rank-nullity proves the inequality. \(\square\)

In particular, no injectivity of \(S_J\), and no invertibility of a full sparse core \(S\), is needed. Merely writing \(\operatorname{rank}(TS_J+TR_J)\ge\operatorname{rank}S_J-r\) and then \(\operatorname{rank}S_J\ge k-r\) loses a second \(r\). The kernel proof avoids that loss by using independence of the actual corrected columns.

### Local support formulation

Suppose \(C\) is invertible, \(C=S+R\), and a set \(J\) of \(k\) columns of \(S\) is supported on a union \(U\) of at most \(m\) coordinates. For any \(m\) consecutive Fourier rows \(I\), Sections 2 and 3 give

\[
\operatorname{rank}(F_NC)_{I,J}\ge k-\operatorname{rank}(R_{:,J})\ge k-r.
\]

This local statement can use the actual support union and the actual restricted correction rank. A uniform column bound is only one convenient sufficient hypothesis.

## 4. Proof of the target-fiber obstruction

Assume \(F_N=BPA\), and put \(C=A^{-1}=S+R\). Then

\[
B=F_NCP^{-1}.
\]

Set \(k=r+2\) and \(m=sk\). Take the first \(k\) columns of \(B\). The permutation \(P^{-1}\) selects \(k\) distinct columns \(J\) of \(C\). These columns are independent because \(C\) is invertible. The corresponding sparse-core columns have support union size at most \(sk=m\), regardless of their pattern.

Take the last \(m\) Fourier rows \(I=\{N-m,\ldots,N-1\}\). The local lemma yields

\[
\operatorname{rank} B_{I,\{0,\ldots,k-1\}}\ge k-r=2.
\]

But the size condition

\[
N\ge m+k=(s+1)(r+2)
\]

ensures every row index in \(I\) is greater than every selected column index. The displayed block is therefore wholly in the strict lower triangle of \(B\), where the accepted chart makes it \(l_I m_{\{0,\ldots,k-1\}}^T\), of rank at most one. This is a contradiction.

For the left inverse, suppose \(B^{-1}=S+R\), with at most \(s\) nonzeros **per row** of \(S\) and \(\operatorname{rank}R\le r\). Transpose the factorization:

\[
F_N=A^T P^T B^T.
\]

The right-stage inverse is now \((B^{-1})^T=S^T+R^T\), whose sparse core has the required **column** bound. Transpose invariance of the stage chart and \(F_N^T=F_N\) reduce to the preceding contradiction.

This proves both stated orientations. It does not silently replace a left-inverse row bound by a left-inverse column bound.

### Diagonal target rescalings

The same conclusions hold for \(D_LF_ND_R\) with arbitrary invertible diagonal \(D_L,D_R\). Absorb these matrices into the stage factors to reduce to \(F_N\). The stage chart, sparse row/column support bounds, and rank bound are preserved by the required invertible diagonal multiplications. Arbitrary endpoint **permutations** are not claimed here, because they need not preserve the consecutive-output-row argument.

### Rank-t cut extension

The same proof applies if the relevant strict lower block is known to have rank at most \(t\): choose \(k=r+t+1\), \(m=sk\), and require \(N\ge(s+1)(r+t+1)\). The stage owner here is specifically \(t=1\); no separate architecture or task is introduced.

## 5. Concrete gains and strict boundaries at F8

### 5.1 A genuine newly excluded source-chart stage

Let

\[
A=I+E_{2,0}+E_{5,7},\qquad C=A^{-1}=I-E_{2,0}-E_{5,7}.
\]

This \(A\) lies in the accepted chart: set all diagonal entries to one, take \(l_2=m_0=1\), \(u_5=v_7=1\), and all other lower/upper generators zero. The two off-diagonal matrix units multiply to zero in either order, so \(AC=CA=I\).

Every column of \(C\) has at most two nonzeros, and the new theorem excludes this inverse class for \(N\ge6\), including \(N=8\). Yet \(C\) is outside both formerly certified F8 inverse restrictions:

- \(C_{2,0}=-1\) is outside cyclic tridiagonal support.
- The disjoint-row/column minor
  \[
  \det C_{\{2,5\},\{0,7\}}=1
  \]
  rules out \(C=D+R\) with \(D\) diagonal and \(\operatorname{rank}R\le1\).

Thus arbitrary sparse support is a genuine extension within the source chart. This example is a valid stage, not a Fourier factorization.

### 5.2 The improved diagonal rank cutoff

For \(s=1\), every diagonal matrix is a permitted sparse core, even with zero diagonal entries. The bound becomes \(N\ge2r+4\). Taking \(N=8,r=2\) excludes diagonal-plus-rank-two inverses on either stage. More generally, a column-one-sparse core need not be diagonal or even injective, so the same bound covers arbitrary such cores; transpose the condition for the left inverse.

### 5.3 A boundary that still remains

The accepted supplement gives the stage

\[
A_{ij}=\begin{cases}3&i=j,\\1&i>j,\\2&i<j.\end{cases}
\]

Its inverse \(C\) has all 64 entries nonzero, so it does not meet the new three-sparse inverse bound. The freshly checked disjoint minor is

\[
\det C_{\{0,2,4\},\{1,3,5\}}=-8/511\ne0.
\]

Therefore \(C\) also cannot be diagonal plus rank at most two. This demonstrates that the two explicit new F8 corollaries still leave genuine source-chart stages. It does not assert this example lies outside every possible sparse-core decomposition, nor decide whether any remaining stage participates in a Fourier factorization.

## 6. Sharpness and guard controls

### 6.1 The local k-r estimate is attained

The checker constructs an exact invertible \(C=I+R\) in \(\mathbb Q(\zeta_8)\) with \(\operatorname{rank}R=2\). On rows \(4,5,6,7\) and columns \(0,1,2,3\), the Fourier-transformed columns occur in equal pairs, giving rank exactly two:

\[
\operatorname{rank}(F_8C)_{\{4,5,6,7\},\{0,1,2,3\}}=2=4-2.
\]

Construction: choose \(w_2,w_3\) in the kernel of the last-four-row Fourier map with respective coordinates \((w_2)_2=1,(w_2)_3=0\) and \((w_3)_2=0,(w_3)_3=1\), and zero coordinates at 0 and 1. Solve their remaining four coordinates on indices 4 through 7 by the invertible consecutive-row Vandermonde block. Replace columns 2 and 3 of \(I\) with \(e_0+w_2\) and \(e_1+w_3\). Then \(\det C=1\), the correction has rank exactly two, and the selected samples are equal to those of columns 0 and 1. Full exact entries are in `RESULTS.json`.

This proves sharpness of the local rank lemma, not sharpness of the final target-fiber size cutoff or existence of a factorization below it.

### 6.2 Two sparse columns may collide with one fewer sample

With \(2s\le N\), an \((2s-1)\)-consecutive-row Fourier block on \(2s\) columns has a one-dimensional kernel whose coordinates are all nonzero: every \((2s-1)\)-column minor is Vandermonde and nonzero. Split a kernel vector into two disjoint \(s\)-supported parts with opposite signs. Their Fourier samples coincide on those \(2s-1\) rows. Both sampled columns are nonzero because each support has size at most the number of samples. The two coefficient columns are independent because their supports are disjoint, and they can be completed to an invertible column-\(s\)-sparse matrix by adjoining coordinate columns, omitting one anchor from each support.

The exact \(N=8,s=3\) control uses supports \(\{0,2,4\}\) and \(\{1,3,5\}\), colliding on rows 3 through 7. The completed matrix is invertible and column-three-sparse. Its two selected transformed columns have rank one on those five rows, and rank two when row 2 is added. This shows why the six-sample arbitrary-support argument cannot simply be replaced by five samples. It is not a source-chart factorization.

### 6.3 Other dropped hypotheses fail

- Nonconsecutive sample rows \(\{0,2,4,6\}\) of \(F_8\) make columns 0 and 4 identical, despite their independent one-sparse coefficient vectors.
- Repeating a coefficient column makes the inverse candidate singular and leaves the Fourier samples rank one, even with six consecutive samples.
- A separate exact control takes a singular diagonal sparse core and a rank-one repair giving \(C=I\); thus the proof and implementation do not accidentally impose an invertible-core guard.

## 7. Executable evidence and limits

Run `python3 verify_exact.py` using Python's standard library. It defines exact arithmetic in \(\mathbb Q[z]/(z^4+1)\), with rational coefficients and no floating-point operations. No historical script is imported or executed. The successful run verifies:

- Primitivity of the eighth root and all entries of the Fourier inverse identity.
- All 224 six-by-six Fourier minors from eight consecutive cyclic starts and 28 six-column sets, by Gaussian elimination and the separate Vandermonde product formula.
- All 4,278 unordered pairs, with repetition, of nonempty support patterns of size at most three; their 246 distinct unions extend to tested full-rank six-column minors.
- All entries of both inverse identities for the newly excluded stage and the inherited dense boundary, plus the source-chart generators and exact disjoint minors.
- The sharp rank-two-correction example, the five-versus-six-sample collision, the singular-core positive control, and the two additional dropped-hypothesis controls.

The finite checks support the proof. The all-N statement comes from Sections 2 through 4, not finite enumeration. The code is an executable exact certificate, not a machine-formalized proof.

No decomposition-recognition or coefficient-preparation costs are waived. The theorem is a structural exclusion conditional on an actual decomposition satisfying the stated support/rank bound. It supplies no algorithm to find such a decomposition, no numerical tolerance version, no production implementation, no full-owner closure, and no lower bound on arbitrary Fourier computation.

After independent acceptance, retain the owner as **TO RESEARCH, priority 34**. The legitimate new mathematical boundary is the arbitrary-sparse-core plus low-rank inverse family, with the precise one-sided orientation above. An unrestricted solution or characteristic-zero infeasibility certificate for the full \(F_8\) ideal is still required for unrestricted target closure.
