# M-SPARSE-DEFECT: simultaneous inverse-row sparsity, two exact slices

Date: 2026-10-18. Stable owner: **M-SPARSE-DEFECT**. Parent status and priority remain **TO RESEARCH, 42**. This is a source-bound mathematical candidate requiring independent review; it is not a new research identity or a parent closure.

## Result first

Let \(F_N[j,k]=N^{-1/2}\omega^{jk}\), with \(\omega=e^{-2\pi i/N}\), and define
\[
\Delta_{N,s}=\inf\{\|M-F_N\|_2:M\in GL_N(\mathbb C),\ \text{every row of }M^{-1}\text{ has at most }s\text{ nonzeros}\}.
\]
All support choices and all nonzero complex coefficients are allowed.

1. **Exact simultaneous half-density sharpness.** For every even \(N=2m\ge2\),
   \[\Delta_{2m,m}=1/\sqrt2.\]
   An explicit minimizing matrix has exactly \(m\) nonzeros in every inverse row and inverse column; all its singular values are \(1/\sqrt2\), so its spectral condition number is exactly 1.
2. **The one-row bound is not globally sharp in general.** For every \(N\ge3\),
   \[\Delta_{N,1}>\sqrt{1-1/N}.\]
   This is a strict separation of the infimum, not merely nonattainment. No explicit uniform numerical size of this strict gap is claimed.
3. **Exact smallest nonsharp case.**
   \[\Delta_{3,1}=\sqrt3/2>\sqrt{2/3}.\]
   The minimum is attained by a diagonal matrix of condition number 1. For comparison, \(\Delta_{2,1}=1/\sqrt2\) follows from result 1.

These results settle the stated half-density family and the singleton sharpness question, including the exact three-dimensional optimum. Other support budgets remain unresolved here.

## 1. Source and selected gate

The repository was read at commit `c3a882a7e6e61af05fe1045145bc1a43038d77c6`. The current open-record index, lines 1254–1270 at that commit, explicitly says: “Global uniform-row-sparsity sharpness remains OPEN.” Its preceding one-neighborhood comparison is complete and is not repeated here.

- [Pinned open-record index](https://github.com/AgentSlop-Si/research/blob/c3a882a7e6e61af05fe1045145bc1a43038d77c6/math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json)
- [Pinned Phase20 audit, §5](https://github.com/AgentSlop-Si/research/blob/c3a882a7e6e61af05fe1045145bc1a43038d77c6/math/archive/objects/e7/e7413d1d591cfae89647304a88b1ca664dea9602dd86fec79a58688f346a7946__e7413d1d591cfae89647__PHASE20_AUDIT.md)

The Phase20 audit proves the lower bound \(\sqrt{1-s/N}\) if even one inverse row has support at most \(s\), and expressly does not claim sharpness when every inverse row is sparse. The selected missing step is simultaneous realization or obstruction. The construction and counterargument below concern that stronger admissible class.

The fetched index slice, exact source text, Git blob IDs, and SHA-256 bindings are retained in `sources/`. A mistyped duplicate-hash source URL returned 404 during retrieval; it was corrected to the exact index URL before source use. No external files, tables, or repository state were modified.

## 2. Inherited one-row lower bound

For clarity, here is the short accepted argument, credited to Phase20 §5 rather than counted as new work. If row \(b\) of \(M^{-1}\) has at most \(s\) nonzeros and corresponds to output coordinate \(i\), then \(bM=e_i^T\). Put \(x=\|b\|_2>0\) and \(\varepsilon=\|M-F_N\|_2\). Unitarity and flatness of \(F_N\) imply
\[
\varepsilon^2x^2\ge\|e_i^T-bF_N\|_2^2
\ge1+x^2-2\sqrt{s/N}\,x.
\]
Consequently
\[
\varepsilon^2\ge(1/x-\sqrt{s/N})^2+1-s/N\ge1-s/N.
\]
Thus \(\Delta_{N,s}\ge\sqrt{1-s/N}\). This does not, on its own, settle simultaneous sharpness.

## 3. Exact half-density construction for every even length

Write \(N=2m\). Let \(P\) be the column permutation putting the even indices first, followed by the odd indices. Let \(A=F_m\) and \(D=\operatorname{diag}(1,\omega,\ldots,\omega^{m-1})\). Direct substitution into every Fourier entry gives the exact radix-two block identity
\[
F_{2m}P=\frac1{\sqrt2}\begin{pmatrix}A&DA\\A&-DA\end{pmatrix}.
\]
Define
\[
MP=\frac1{\sqrt2}\begin{pmatrix}A&0\\0&-DA\end{pmatrix}.
\]
Both \(A\) and \(DA\) are unitary. Hence
\[
MM^*=\tfrac12I,\qquad
M^{-1}=\sqrt2\,P\begin{pmatrix}A^*&0\\0&-A^*D^*\end{pmatrix}.
\]
Every entry in each displayed \(m\times m\) inverse block is nonzero. Row permutation by \(P\) preserves each row's support cardinality, and therefore every inverse row has exactly \(m\) nonzeros. Every inverse column also has exactly \(m\) nonzeros. Moreover,
\[
(F_{2m}-M)P=\frac1{\sqrt2}\begin{pmatrix}0&DA\\A&0\end{pmatrix},
\qquad(F_{2m}-M)(F_{2m}-M)^*=\tfrac12I.
\]
Thus \(\|F_{2m}-M\|_2=1/\sqrt2\), matching §2 for \(s=m\). This proves the exact optimum and attainment for the entire even-length family, including odd \(m\). There is no power-of-two restriction.

## 4. Singleton inverse sparsity: equality is impossible for N≥3

An invertible matrix whose inverse has at most one nonzero per row is monomial: each inverse row must contain one nonzero, the occupied columns must be distinct, and inversion preserves monomiality. Thus \(s=1\) permits exactly the invertible monomial matrices \(M\).

Write the nonzero of row \(k\) at column \(\sigma(k)\), with value \(d_k\ne0\), where \(\sigma\) is a permutation. Put \(E=F_N-M\) and \(a=\sqrt{1-1/N}\). Each row satisfies
\[
\|E[k,:]\|_2^2=a^2+|d_k-F_N[k,\sigma(k)]|^2.
\]
Suppose \(\|E\|_2=a\). Then every \(d_k=F_N[k,\sigma(k)]\). All row norms of \(E\) are exactly \(a\). The positive-semidefinite matrix \(a^2I-EE^*\) has zero diagonal, so it is zero. Hence different rows of \(E\) are orthogonal.

For \(k\ne l\), orthogonality of the full Fourier rows and distinctness of \(\sigma(k),\sigma(l)\) give
\[
0=(EE^*)_{kl}
=-\frac1N\left(\omega^{(k-l)\sigma(k)}+\omega^{(k-l)\sigma(l)}\right).
\]
Therefore
\[
\omega^{(k-l)(\sigma(k)-\sigma(l))}=-1.\tag{*}
\]
For odd \(N\), \(-1\) is not an \(N\)-th root, so this is impossible. For even \(N\ge4\), apply (*) to \((k,l)=(0,1)\) and \((1,2)\). It forces both consecutive permutation differences to equal \(N/2\pmod N\), giving \(\sigma(0)=\sigma(2)\), a contradiction. Thus equality is impossible whenever \(N\ge3\).

### Why the infimum is also strictly larger

Suppose instead that an admissible sequence \(M_j\) had \(\|F_N-M_j\|_2\to a<1\). Its norms are bounded. There are finitely many monomial support permutations, so a subsequence has one support pattern and converges to a possibly singular matrix \(M_\infty\) of that pattern. Continuity gives \(\|F_N-M_\infty\|_2=a<1\). Since \(F_N\) is unitary, this implies \(M_\infty\) is invertible: otherwise a unit vector in its kernel would give error at least 1. Thus \(M_\infty\) is an admissible invertible monomial matrix attaining \(a\), contradicting the preceding proof. Therefore \(\Delta_{N,1}>a\).

This argument addresses the open invertibility constraint explicitly; nonattainment alone would not have sufficed.

## 5. Exact singleton optimum at N=3

Set \(\omega=e^{-2\pi i/3}\), \(D=\operatorname{diag}(1,\omega,\omega)\), and \(C=DF_3D\). Since \(i^2+j^2+ij=(i-j)^2\pmod3\),
\[
C=\frac1{\sqrt3}\big((1-\omega)I+\omega J\big),
\]
where \(J\) is the all-ones matrix. Its two eigenvalues are
\[
\lambda_0=(1+2\omega)/\sqrt3=-i\quad\text{(multiplicity 1)},\qquad
\lambda_1=(1-\omega)/\sqrt3=\sqrt3/2+i/2\quad\text{(multiplicity 2)}.
\]
The matrix \(C\) is invariant under conjugation by every coordinate permutation. Averaging any diagonal approximant \(T\) over all six coordinate permutations replaces it by \(cI\), \(c=\operatorname{tr}(T)/3\); convexity and unitary invariance of the operator norm imply
\[
\|C-cI\|_2\le\|C-T\|_2.
\]
This inequality remains valid even if the averaged scalar is zero. The minimum over all complex scalars is half the distance between the two eigenvalues:
\[
\min_c\max(|\lambda_0-c|,|\lambda_1-c|)
=\frac{|\lambda_0-\lambda_1|}{2}=\sqrt3/2,
\]
attained at \(c=(\lambda_0+\lambda_1)/2=\sqrt3/4-i/4\ne0\). It follows that the minimum over invertible diagonal approximants to \(F_3\) is \(\sqrt3/2\), attained by
\[
M_3=D^{-1}(cI)D^{-1}=cD.
\]
This matrix has all singular values \(|c|=1/2\).

It remains to justify allowing all monomial supports. Every permutation of the three residues has the form \(\sigma(j)=aj+b\pmod3\), with \(a\in\{1,2\}\), \(b\in\{0,1,2\}\). Reorder columns so that row \(i\)'s selected column \(\sigma(i)\) becomes column \(i\). The monomial approximant becomes diagonal, and the Fourier target has entries
\[
F_3[i,\sigma(j)]=\omega^{bi}\,3^{-1/2}\omega^{aij}.
\]
Removing the unitary row phase gives \(F_3\) when \(a=1\), or \(\overline{F_3}\) when \(a=2\). Complex conjugation preserves the same diagonal minimization problem. Thus every one of the six support patterns has optimum \(\sqrt3/2\), proving the full claim.

## 6. Verification and costs

`verify_exact.py` is newly authored for this candidate. It does not import or execute historical code.

- Exact cyclotomic-ring Gram checks verify the unnormalized retained and omitted Fourier masks at every even \(N\) from 2 through 32. They check both Gram orders, exact row/column support counts, and the inverse identity without floating-point roots or square roots.
- Exact finite controls test the necessary singleton phase congruences over all support permutations for \(2\le N\le8\); only \(N=2\) passes.
- Exact symbolic checks verify the \(N=3\) eigenvalue separation, midpoint and explicit diagonal witness. The proof covers all coefficients and all six supports, rather than relying on numerical optimization.
- Negative controls use a singular repeated-column-block mask and a corrupted retained entry; these must fail the appropriate Gram/invertibility certificates. Odd lengths are rejected by the half-density constructor.

The complete symbolic proofs, not these finite controls, establish the infinite families. This packet makes no finite-word, numerical-production or measured-runtime claim.

The half-density construction is a classical radix-two Fourier block decomposition used to settle the stated optimization slice. Preparing or applying its dense blocks is not free. A naive explicit matrix representation has \(N^2/2\) stored nonzeros; a factored application uses two length-\(m\) Fourier transforms, the permutation and diagonal phases. No cheaper Fourier evaluator, arithmetic lower bound, independent novelty claim or historical-priority clearance follows. The singleton \(N=3\) argument is elementary symmetry/convexity, again with no novelty assertion.

## 7. Exact stopping condition and proposed record delta

The selected work stops once these proofs and the bounded exact controls are independently accepted. Do not dispatch a general support-budget optimization merely because it remains open.

Proposed owner update, conditional on independent acceptance:

> Completed two simultaneous inverse-row-sparsity slices: for every even N, the global optimum at s=N/2 is 1/√2, attained with condition number 1 and exactly N/2 nonzeros in every inverse row/column. For singleton inverse rows, the one-row floor √(1−1/N) is strictly below the global infimum for every N≥3; the exact N=3 optimum is √3/2. General budgets remain open. Retain parent TO RESEARCH, priority 42, and all original field/model/cost/novelty limitations.

This is a prospective update only. No index, native table, status, priority or source was edited by this task.
