# M-SPARSE-DEFECT: a complete equality criterion and new budget families

Date: 2026-10-18. Stable owner: **M-SPARSE-DEFECT**. Candidate for independent review. Keep parent status **TO RESEARCH**, priority **42**.

## Results first

Let \(F=F_N\), \(F[j,k]=N^{-1/2}\omega^{jk}\), \(\omega=e^{-2\pi i/N}\), and
\[
\Delta_{N,s}=\inf\{\|M-F_N\|_2:M\in GL_N(\mathbb C),\ \text{every row of }M^{-1}\text{ has at most }s\text{ nonzeros}\}.
\]
Throughout, \(N\ge2\) and \(1\le s\le N-1\). All support patterns and complex coefficients are allowed. The following statements concern the simultaneous constraint on **all** inverse rows.

1. **Necessary and sufficient condition for the inherited floor.** Set \(q=s/N\), \(a=\sqrt{1-q}\). Then \(\Delta_{N,s}=a\) if and only if a 0–1 mask \(R\) exists with exactly \(N-s\) ones in every column such that
   \[
   C=F_N\circ R,\qquad C^*C=\frac{N-s}{N}I.
   \]
   Any such mask automatically has exactly \(N-s\) ones in every row. Writing \(A=F-C\), an explicit minimizing matrix is
   \[
   M=q(A^*)^{-1},\qquad M^{-1}=q^{-1}A^*.
   \]
   Its inverse has exactly \(s\) nonzeros in every row and column. Every minimizer at the inherited floor has this form. If no mask exists, the infimum is **strictly** above the floor.

2. **Exact complementary-divisor family.** For every proper positive divisor \(d\mid N\),
   \[
   \boxed{\Delta_{N,N-d}=\sqrt{d/N}.}
   \]
   The construction is explicit and attained. In particular, the previously unresolved family \(s=N-1\) satisfies \(\Delta_{N,N-1}=1/\sqrt N\) for every \(N\ge2\). This includes but is not limited to the previously accepted even half-density family.

3. **Complete answer to floor sharpness at codimension two.** For \(N\ge3\),
   \[
   \Delta_{N,N-2}=\sqrt{2/N}\quad(N\text{ even}),\qquad
   \Delta_{N,N-2}>\sqrt{2/N}\quad(N\text{ odd}).
   \]
   The exact odd-dimensional values are not claimed, apart from the inherited value \(\Delta_{3,1}=\sqrt3/2\).

4. **Prime dimensions: complete classification of floor sharpness.** If \(p\) is prime, the floor is sharp exactly at \(s=p-1\). For every \(1\le s\le p-2\),
   \[
   \boxed{\Delta_{p,s}>\sqrt{1-s/p}.}
   \]
   No quantitative gap or exact value in these nonsharp slices is asserted.

These are proofs in the original complex spectral-norm model, with no conditioning restriction. They do not classify all composite-dimensional masks or solve all remaining exact values.

## 1. Source binding and selected scope

The input is the accepted packet `catalogue_next_gate_20261018_1140` and its independent review `sparse_defect_review_20261018_1147`. Their accepted claims are: even half-density sharpness; strict singleton nonsharpness for every \(N\ge3\); and \(\Delta_{3,1}=\sqrt3/2\). They explicitly leave other simultaneous support budgets open. This task does not repeat their audit or change their evidence.

The underlying owner and one-row inequality are pinned to repository commit `c3a882a7e6e61af05fe1045145bc1a43038d77c6`:

- [Open-record index](https://github.com/AgentSlop-Si/research/blob/c3a882a7e6e61af05fe1045145bc1a43038d77c6/math/finalized/2026-10-15-rebuilt-open-record-index/open-record-index.json), M-SPARSE-DEFECT.
- [Phase20 audit, §5](https://github.com/AgentSlop-Si/research/blob/c3a882a7e6e61af05fe1045145bc1a43038d77c6/math/archive/objects/e7/e7413d1d591cfae89647304a88b1ca664dea9602dd86fec79a58688f346a7946__e7413d1d591cfae89647__PHASE20_AUDIT.md).

Exact input bytes and their SHA-256 values are bound in `SOURCE_BINDINGS.json`; selected source copies are included. The inherited floor is credited to Phase20, not presented as new. New work starts with its simultaneous equality conditions. The next budget \(s=N-1\), its divisor extension, and the immediately adjoining \(s=N-2\) obstruction form the selected scope; the prime-dimensional consequence follows from the same criterion.

## 2. Equality conditions for every inverse row

Put \(B=M^{-1}\), \(E=M-F\), and let \(b_i\) be row \(i\) of \(B\). If its support has size \(t_i\le s\) and \(x_i=\|b_i\|_2>0\), the accepted argument gives
\[
\|E\|_2^2x_i^2\ge\|b_iE\|_2^2
=\|e_i^T-b_iF\|_2^2
\ge1+x_i^2-2\sqrt{t_i/N}\,x_i.
\]
Equivalently,
\[
\|E\|_2^2\ge(1/x_i-\sqrt{t_i/N})^2+1-t_i/N\ge1-s/N.
\]

Suppose \(\|E\|_2=a\). Equality throughout forces \(t_i=s\), \(x_i=q^{-1/2}\), and equality with positive real phase in the Cauchy–Schwarz estimate for \((b_iF)_i\). If \(S_i\) is the support of row \(i\), then
\[
(b_i)_j=q^{-1}\overline{F[j,i]}\,\mathbf 1_{j\in S_i},\qquad (b_iF)_i=1.
\]
Define the retained Fourier mask \(A\) by \(A[j,i]=F[j,i]\mathbf 1_{j\in S_i}\). Then each column of \(A\) contains exactly \(s\) nonzeros and
\[
B=q^{-1}A^*.
\]
In particular, the equality case leaves no additional continuous coefficient choice once its mask has been chosen.

It is essential here to use **all rows simultaneously**. The matrix \(H=a^2I-EE^*\) is positive semidefinite, and equality in the first estimate says \(b_iHb_i^*=0\) for every \(i\). Thus \(BHB^*\) is positive semidefinite with zero diagonal, hence zero. Since \(B\) is invertible,
\[
EE^*=a^2I.\tag{2.1}
\]
Using \(BE=I-BF\) and \(FF^*=I\), equation (2.1) is equivalent to
\[
I-BF-F^*B^*+qBB^*=0.
\]
Substitute \(B=q^{-1}A^*\) and multiply by \(q\):
\[
qI-A^*F-F^*A+A^*A=0.
\]
For the complementary mask \(C=F-A\), this is exactly
\[
C^*C=(1-q)I=a^2I.\tag{2.2}
\]
The square matrix \(C/a\) is unitary, so also \(CC^*=a^2I\). Its row norms show that every row has exactly \(N-s\) nonzeros. Thus both rows and columns of \(A\), and of the resulting inverse, have the asserted support counts.

## 3. Sufficiency, invertibility, and strict infimum separation

Conversely, suppose a complementary mask \(C\) satisfies (2.2) and has \(N-s\) nonzeros per column. Since \(a<1\),
\[
\|Ax\|_2=\|(F-C)x\|_2\ge(1-a)\|x\|_2,
\]
so \(A\) is invertible. Set \(B=q^{-1}A^*\), \(M=B^{-1}\). Every row of \(B\) has exactly \(s\) nonzeros. Expanding (2.2) and reversing the identities in §2 gives
\[
BEE^*B^*=a^2BB^*,\quad\text{hence}\quad EE^*=a^2I.
\]
Thus \(\|M-F\|_2=a\), proving sufficiency with exact attainment. The same argument shows that all floor-attaining minimizers are represented by these masks.

To pass from equality of an infimum to attainment, suppose \(M_j\) is admissible and \(\|M_j-F\|_2\to a<1\). The matrices are bounded, so a subsequence converges to \(M_\infty\). For all sufficiently large \(j\), the smallest singular value is bounded below by a fixed positive number using \(\sigma_{\min}(M_j)\ge1-\|M_j-F\|_2\). Therefore \(M_\infty\) is invertible and \(M_j^{-1}\to M_\infty^{-1}\). The set of matrices whose every row has at most \(s\) nonzeros is closed (a finite union of coordinate subspaces), so the inverse-row condition survives the limit. Continuity gives \(\|M_\infty-F\|_2=a\). By §§2–3 it yields a mask.

Consequently, the absence of a mask implies \(\Delta_{N,s}>a\), rather than only failure to attain \(a\). No numerical lower bound for the strict gap follows from this compactness argument.

### Conditioning is bounded, not generally one

For any mask witness, \(1-a\le\sigma_{\min}(A)\le\sigma_{\max}(A)\le1+a\). Since \(q=1-a^2\), the singular values of \(M=q(A^*)^{-1}\) lie in \([1-a,1+a]\), and
\[
\kappa_2(M)\le\frac{1+a}{1-a}.
\]
The previous half-density witness had condition number one. That stronger assertion is **not** extended to the new general construction. In particular, the witness is \(q(A^*)^{-1}\), not simply the retained Fourier mask \(A\).

## 4. Explicit masks for every complementary divisor

Let \(d\mid N\), \(1\le d<N\), and write \(N=md\). Partition the rows and columns into \(m\) sets of size \(d\):
\[
I_t=\{td,td+1,\ldots,td+d-1\},\qquad
J_t=\{t+\ell m:0\le\ell<d\},\quad0\le t<m.
\]
Retain Fourier entries in the **omitted** mask \(C\) precisely on the disjoint rectangles \(I_t\times J_t\). Each row and column belongs to exactly one such rectangle, so each has exactly \(d\) nonzeros.

For \(r=td+u\), \(c=t+\ell m\), the entries of block \(t\) are
\[
C[td+u,t+\ell m]
=N^{-1/2}\omega^{(td+u)t}(\omega^m)^{u\ell},
\]
because \(\omega^{td\ell m}=1\). After regrouping columns, each block is \(\sqrt{d/N}\) times a diagonal unitary times \(F_d\). The row and column sets are disjoint, and hence
\[
C^*C=CC^*=\frac dN I.
\]
Applying §3 with \(s=N-d\) gives the explicit witness and the exact value \(\Delta_{N,N-d}=\sqrt{d/N}\).

For \(d=1\), \(C\) is simply the diagonal of \(F_N\). Thus \(A\) is \(F_N\) with its diagonal removed, and
\[
M=\frac{N-1}{N}\big((F_N-\operatorname{diag}(F_N))^*\big)^{-1}
\]
is invertible with exactly \(N-1\) nonzeros per inverse row and column. For \(d=2\), row pairs are consecutive and matched column pairs differ by \(N/2\), proving the even codimension-two assertion.

The divisor condition is sufficient. This report does **not** claim it is necessary for composite dimensions.

## 5. Odd-dimensional obstruction at codimension two

Suppose \(N\ge3\) is odd, \(s=N-2\), and a mask \(C\) from §1 exists. Every column of \(C\) has exactly two nonzero entries. For distinct columns \(j,k\), let \(T\) be their intersection of row supports. Column orthogonality requires
\[
\sum_{r\in T}\omega^{r(k-j)}=0.
\]
If \(|T|=1\), the sum is nonzero. If \(|T|=2\), cancellation would require the ratio of two \(N\)-th roots of unity to equal \(-1\), impossible for odd \(N\). Thus all column supports must be pairwise disjoint. There cannot be \(N\) disjoint two-element subsets of an \(N\)-element row set. No mask exists. Section 3 proves the strict inequality for the infimum.

Together with the \(d=2\) construction, this completely decides sharpness of the inherited floor for the entire budget family \(s=N-2\).

## 6. Prime-dimensional obstruction for every remaining budget

Let \(N=p\) be prime and \(w=p-s\ge2\). If a mask exists, every column has \(w\le p-1\) nonzeros. For distinct columns \(j,k\), their support intersection \(T\) must satisfy
\[
\sum_{r\in T}\omega^{r(k-j)}=0.
\]
Multiplication by \(k-j\not\equiv0\pmod p\) permutes the residues. The sum is therefore the value at \(\omega\) of a polynomial \(P(x)\) of degree at most \(p-1\), with coefficients in \(\{0,1\}\), having \(|T|\le w<p\) ones. The minimal polynomial of \(\omega\) is
\[
\Phi_p(x)=1+x+\cdots+x^{p-1}.
\]
For completeness, irreducibility follows by Eisenstein at \(p\) after the substitution \(x\mapsto x+1\): \(((x+1)^p-1)/x\) has leading coefficient 1, every other coefficient divisible by \(p\), and constant term \(p\) not divisible by \(p^2\).

If \(P(\omega)=0\), the degree bound forces \(P\) to be zero or a constant multiple of \(\Phi_p\). The 0–1 coefficients and \(|T|<p\) exclude the latter unless the constant is zero. Hence \(T\) is empty. Again, \(p\) disjoint supports of size \(w\ge2\) cannot fit in \(p\) rows. No mask exists, and §3 gives strict infimum separation.

At \(w=1\), the divisor construction attains the floor. This proves the stated complete sharpness classification in prime dimensions, including the vacuous remaining-budget range when \(p=2\).

## 7. Exact reproducible checks

`verify_exact.py` is newly written for this packet and does not import or execute historical checkers. It uses exact integer/cyclotomic-field arithmetic, with no floating-point norm thresholds.

- Both Gram orders and all row/column support counts passed for 149 divisor-mask cases: every proper divisor of each \(2\le N\le36\), and of \(N\in\{40,42,48,50,60,64\}\).
- The retained-mask equality identity is checked directly in the unnormalized Fourier model.
- Fifteen explicit inverse witnesses are computed in exact cyclotomic fields, through \(N=12\). Both inverse products, the error Gram \(dI\) in the unnormalized model, and every inverse-row/column support passed.
- All 208,116 fixed-column-weight 0–1 masks in dimensions 2 through 5 are exhaustively filtered for the exact equality criterion. The weight-one masks pass in exactly \(N!\) ways; at \(N=4\), exactly eight weight-two masks pass; all other tested weights fail. These are finite controls only, not the proof of the infinite claims.
- Every nonempty proper root subset is checked at primes \(2,3,5,7,11,13\); every pair of distinct roots is checked at odd \(3\le N\le61\). No prohibited zero sum occurs. Negative controls deliberately corrupt coefficients, support regularity, admissible constructor parameters, or the witness formula, and are rejected. In particular, using the retained mask itself as the witness at \((N,d)=(3,1)\) has the correct error but a dense inverse and is rejected by the simultaneous budget.

All checks passed with empty stderr. The machine-readable result records the exact tested ranges and counts. These controls corroborate the general proofs; they do not substitute for them. Running the checker is reproducible using the included instructions.

## 8. Costs, limitations, and justified stop

The witness has a sparse inverse with \(Ns\) nonzeros, but \(M\) itself can be dense. Constructing it entails the inverse of a known matrix, or an equivalent solve. The displayed omitted mask has \(Nd\) nonzeros and Fourier blocks of size \(d\); this description does not provide a new cheap application algorithm for \(M\), a faster Fourier transform, a finite-word stability theorem, a measured runtime, or an arithmetic lower bound. The spectral condition bound in §3 is the only general conditioning claim here.

No historical-priority or worldwide novelty claim is made. All original field/model, sparse-column, shared-frame commutator, preparation/output cost, and implementation limitations remain intact.

The selected gate is complete when the equality characterization, complementary-divisor construction, codimension-two parity classification, and prime-dimensional sharpness classification have passed independent review with the sealed exact controls. The finite mask check stops at \(N=5\); it is not a search for a complete composite-dimensional classification. No general-budget optimization is requested or implied.

Conditional record delta after acceptance:

> Added a necessary-and-sufficient complementary Fourier-mask criterion for simultaneous sharpness of the one-row floor. Proved exact \(\Delta(N,N-d)=\sqrt{d/N}\) for every proper divisor \(d\mid N\), including all \(s=N-1\). At \(s=N-2\), the floor is sharp for even \(N\) and strictly nonsharp for odd \(N\). For prime \(p\), floor sharpness occurs exactly at \(s=p-1\), with strict infimum gaps for all other nontrivial budgets. Exact nonsharp values, quantitative gaps, and the remaining composite-budget classification stay open. Retain owner M-SPARSE-DEFECT, TO RESEARCH, priority 42.

No GitHub, Google Sheets, repository index, or other external state was modified by this task.
