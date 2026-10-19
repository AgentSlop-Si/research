# M-SPARSE-DEFECT: codimension-three classification and an explicit strict gap

Date: 2026-10-18. Stable owner: **M-SPARSE-DEFECT**. Candidate for independent review. Retain parent status **TO RESEARCH**, priority **42**.

## Results first

Use the accepted complex spectral-norm model

\[
 F_N[r,c]=N^{-1/2}\omega^{rc},\qquad \omega=e^{-2\pi i/N},\qquad
 \Delta_{N,s}=\inf\{\|M-F_N\|_2:M\in GL_N(\mathbb C),\ \text{every row of }M^{-1}\text{ has at most }s\text{ nonzeros}\}.
\]

The support constraint is simultaneous on **all inverse rows**. There is no restriction on their complex coefficients or support patterns, and no condition-number assumption.

### Theorem A: complete codimension-three floor-sharpness classification

For every integer \(N\ge4\),

\[
\boxed{\begin{aligned}
3\mid N&\quad\Longrightarrow\quad \Delta_{N,N-3}=\sqrt{3/N},\quad\text{attained},\\
3\nmid N&\quad\Longrightarrow\quad \Delta_{N,N-3}>\sqrt{3/N}.
\end{aligned}}
\]

More strongly, every complementary Fourier mask of weight three that is a scaled unitary is, after separate row and column permutations, a direct sum of full \(3\times3\) Fourier submatrices. The exact arithmetic condition on each such block is given in §4. This classifies the support structure and phase test of **every** floor-attaining mask at this budget.

The positive direction was already supplied by the accepted complementary-divisor construction. The new result is necessity, including even composite dimensions not divisible by three, together with the full block-support description.

### Theorem B: quantitative replacement for qualitative no-mask separation

Let \(N\ge2\), \(1\le s\le N-1\), \(d=N-s\), and let \(\varphi\) be Euler's totient function. If no complementary Fourier mask of weight \(d\) satisfies the accepted equality criterion, then

\[
\boxed{\Delta_{N,s}^{\,2}\ \ge\ \frac dN+
       \frac{s^6}{2^{22}N^{10}d^{\,2\varphi(N)-2}}.}\tag{Q}
\]

This deliberately conservative bound is explicit, positive, and valid for the unrestricted simultaneous inverse-row model. It is a lower bound on the **squared** gap, not an exact nonsharp optimum.

In particular, for \(N\ge4\) with \(3\nmid N\),

\[
\Delta_{N,N-3}\ge
\sqrt{\frac3N+\frac{(N-3)^6}{2^{22}N^{10}3^{\,2\varphi(N)-2}}}.
\]

The same quantitative theorem also applies to the already accepted odd codimension-two and nontrivial prime-dimensional nonsharp cases. This is a consequence of their accepted no-mask obstructions; those classifications are not re-audited here.

These results do not classify all composite budgets or compute the exact nonsharp optima.

## 1. Accepted input, normalization, and boundary

The accepted input is the candidate `/workspace/shared/sparse_defect_budget_20261018_1240` together with its independent acceptance in `/workspace/shared/sparse_mask_final_review_20261018_1248`. Exact source bytes and hashes are recorded in `SOURCE_BINDINGS.json` and copied under `sources/`.

The accepted theorem says, with \(q=s/N\), \(a=\sqrt{1-q}\), that

\[
\Delta_{N,s}=a
\quad\Longleftrightarrow\quad
C=F_N\circ R,\ R\in\{0,1\}^{N\times N},\ \text{each column has }d=N-s\text{ ones},\ C^*C=\frac dN I.
\tag{1.1}
\]

Such a mask automatically has \(d\) entries in each row. If \(A=F_N-C\), every floor-attaining minimizer is recovered by

\[
M=q(A^*)^{-1},\qquad M^{-1}=q^{-1}A^*.
\tag{1.2}
\]

In particular, its inverse has exactly \(s\) nonzeros in every row and column. The accepted proof also shows that equality of the **infimum** with the floor forces attainment, using boundedness, uniform nonsingularity below error one, continuity of inversion, and closedness of the simultaneous inverse-row sparsity class.

The new classification uses this accepted equivalence. The quantitative argument in §5 proves a bound for every admissible \(M\) directly and then takes the infimum, so it has no new attainment assumption.

## 2. Elementary support lemma at weight three

**Lemma.** Let \(U\) be any square complex matrix with exactly three nonzero entries per row and per column, and with mutually orthogonal columns. Each connected component of its bipartite support graph is one of:

1. a full \(3\times3\) block, or
2. a \(4\times4\) block with one zero in each row and column, whose zeros form a perfect matching.

Only the supports and the fact that a singleton overlap cannot be orthogonal are used in this lemma.

**Proof.** Any two column supports have intersection size \(0,2,\) or \(3\), because size one gives a nonzero inner product.

First suppose two columns have the same support \(S=\{a,b,c\}\). They use two of the three incidences available at each of these rows. The remaining columns therefore have exactly three incidences with \(S\) in total. A column meeting \(S\) must contribute at least two incidences. Thus exactly one further column meets \(S\), and it meets all three rows. These three columns and three rows are now saturated, giving an isolated full \(3\times3\) block.

Otherwise choose a column with support \(S=\{a,b,c\}\), assuming no equal-support pair in its component. The six remaining incidences at these rows lie in columns that each meet \(S\) in exactly two rows. There are exactly three such columns. If the multiplicities of the pairs \(ab,ac,bc\) are \(x,y,z\), the row degrees give \(x+y=x+z=y+z=2\), so \(x=y=z=1\). Write their supports as

\[
\{a,b,x_0\},\qquad \{a,c,y_0\},\qquad \{b,c,z_0\},
\]

where the added rows lie outside \(S\). The first two supports already intersect at \(a\); avoiding a singleton intersection forces \(x_0=y_0\). The same argument forces \(x_0=y_0=z_0=:e\). All four rows and four columns are saturated. Their support is the full \(4\times4\) pattern with a matched zero in each row and column. Remove the isolated component and repeat. ∎

The second alternative cannot be discarded for arbitrary complex matrices: a real conference matrix of order four and weight three exists. What rules it out below is specifically the rank-one Fourier exponent pattern.

## 3. No Fourier-phase conference block

**Lemma.** No submatrix of any Fourier matrix, restricted to a \(4\times4\) support with matched zeros and otherwise retaining its original Fourier entries, can have mutually orthogonal columns.

**Proof.** Label its distinct row indices \(r_0,r_1,r_2,r_3\) and distinct column indices \(c_0,c_1,c_2,c_3\) so that the missing entries are \((r_i,c_i)\). If \(\{i,j,k,l\}=\{0,1,2,3\}\), columns \(i,j\) overlap in exactly rows \(k,l\). Their orthogonality requires

\[
\omega^{r_k(c_j-c_i)}+\omega^{r_l(c_j-c_i)}=0.
\]

For odd \(N\), this is impossible because \(-1\) is not an \(N\)-th root of unity. For even \(N\), it is equivalent to all six congruences

\[
(r_k-r_l)(c_i-c_j)\equiv N/2\pmod N,
\qquad \{i,j,k,l\}=\{0,1,2,3\}.
\tag{3.1}
\]

Write \(N=2^n m\), with \(m\) odd and \(n\ge1\). Modulo \(2^n\), the right side of (3.1) is \(2^{n-1}\). Consequently every row and column difference appearing in (3.1) is nonzero modulo \(2^n\), and

\[
v_2(r_k-r_l)+v_2(c_i-c_j)=n-1.
\tag{3.2}
\]

All these valuations are finite and less than \(n\). Put

\[
\alpha=\min_{k<l}v_2(r_k-r_l),\qquad \beta=n-1-\alpha.
\]

Translate the rows by \(-r_0\), divide them by \(2^\alpha\), and partition the four indices by the parity of the resulting integers. Both parity classes are nonempty. A cross-class row difference has valuation exactly \(\alpha\), so its complementary column difference has valuation exactly \(\beta\). A same-class row difference has valuation greater than \(\alpha\), so its complementary column difference must have valuation strictly less than \(\beta\).

There are only two possible split types:

- **One plus three.** The three cross-class row edges form a star. Their complementary column edges form a triangle. All three differences on that triangle would have valuation exactly \(\beta\), which is impossible: if two differences from a common vertex have valuation \(\beta\), their difference has valuation at least \(\beta+1\).
- **Two plus two.** Complementing an edge of the four-cycle of cross-class row edges gives another cross-class edge. All cross-class column differences therefore have valuation \(\beta\). Two column indices in one class, compared with a fixed index in the other class, must consequently have difference of valuation at least \(\beta+1\). But that within-class column edge is complementary to a within-class row edge, so (3.2) requires its valuation to be strictly less than \(\beta\). Again a contradiction.

Thus (3.1) has no solution. The argument allows row or column residues initially to coincide modulo \(2^n\); the congruences themselves exclude such coincidences. It therefore covers all even \(N\), not merely powers of two. ∎

## 4. Codimension-three classification and all equality masks

Let \(C\) satisfy (1.1) with \(d=3\). Its rows and columns each have exactly three nonzeros. Section 2 decomposes its support into full blocks of size three or conference blocks of size four. Section 3 excludes all conference blocks. Therefore \(N\) is a sum of threes, proving \(3\mid N\).

Conversely, if \(N=3m\), the accepted divisor construction retains the omitted Fourier entries on

\[
I_t\times J_t,\qquad
I_t=\{3t,3t+1,3t+2\},\qquad
J_t=\{t,t+m,t+2m\},\qquad 0\le t<m.
\]

Every block is a row-phased \(\sqrt{3/N}\,F_3\), so \(C^*C=(3/N)I\). Equation (1.2) supplies an attained simultaneous-budget witness. This proves Theorem A, with the accepted compactness argument justifying strictness of the infimum when \(3\nmid N\). Section 5 strengthens that strictness quantitatively.

### Exact block-phase test

The support statement alone is not sufficient: arbitrary partitions into triples need not give orthogonal Fourier blocks. A full block with row triple \(\{r_0,r_1,r_2\}\) and column triple \(\{c_0,c_1,c_2\}\) works if and only if, after ordering the triples,

\[
\begin{array}{ll}
(r_1-r_0)(c_1-c_0)\equiv N/3,&
(r_1-r_0)(c_2-c_0)\equiv 2N/3,\\
(r_2-r_0)(c_1-c_0)\equiv 2N/3,&
(r_2-r_0)(c_2-c_0)\equiv N/3
\end{array}\pmod N.
\tag{4.1}
\]

To prove necessity, multiply rows and columns by unit phases so that the first row and column become all ones. The remaining entries are \(\omega^{(r-r_0)(c-c_0)}\). For unit-modulus \(x,y\), the equation \(1+x+y=0\) forces \(\{x,y\}\) to be the two primitive cube roots: \(|1+x|=1\) gives \(\operatorname{Re}x=-1/2\), and then \(y=-1-x\). The two noninitial columns must have opposite orientations of these roots to remain orthogonal. This gives (4.1), after swapping labels if necessary. Sufficiency is immediate because the dephased block is \(F_3\) without its normalization.

Thus every floor-attaining mask is exactly a pairing of row triples and column triples partitioning the coordinates, with each paired block satisfying (4.1). Every associated minimizer is given by (1.2). No uniqueness of the partition or of the minimizer is claimed.

## 5. Quantitative no-mask separation

This section proves Theorem B for arbitrary omission weight \(d\). It does not assume the codimension-three support lemma.

### 5.1 Discrete spectral separation of a bad mask

Let \(C=F_N\circ R\) have exactly \(d\) retained entries in every column. Its Gram diagonal is \(d/N\). If it is not a scaled unitary, some off-diagonal Gram entry is nonzero and has the form

\[
\frac1N\sum_{r\in T}\omega^{r(k-j)},\qquad 1\le |T|\le d.
\]

Write the nonzero root sum as \(\xi=P(\omega)\), with \(P\) an integer polynomial consisting of at most \(d\) unit terms; coinciding exponents are allowed. Its cyclotomic norm

\[
\prod_{\substack{1\le u\le N\\(u,N)=1}} P(\omega^u)
\]

is a nonzero integer, equivalently the nonzero resultant of the monic cyclotomic polynomial \(\Phi_N\) with \(P\). Every factor other than the displayed embedding has modulus at most \(d\). Hence

\[
|\xi|\ge d^{-(\varphi(N)-1)},\qquad
\boxed{\|C^*C-(d/N)I\|_2\ge\gamma:=\frac1{N d^{\varphi(N)-1}}.}
\tag{5.1}
\]

Irreducibility of \(\Phi_N\) ensures that a nonzero value at one primitive root cannot have a zero conjugate. This is an algebraic-integer bound, with no numerical root-separation threshold.

### 5.2 Near equality rigidifies every inverse row

Fix any admissible \(M\), and write

\[
F=F_N,\quad B=M^{-1},\quad E=M-F,\quad
\rho=\|E\|_2,\quad q=s/N,\quad a=\sqrt{1-q},\quad D=\rho^2-a^2\ge0.
\]

Set

\[
\rho_0=(1+a)/2,\qquad L=1-\rho_0=(1-a)/2,\qquad U=1+\rho_0=(3+a)/2.
\]

The elementary estimates used below are

\[
L\ge q/4,\qquad U\le2,\qquad
\rho_0^2-a^2=(1-a)(1+3a)/4\ge q/8.
\tag{5.2}
\]

If \(\rho\ge\rho_0\), then \(D\ge q/8\). If \(D\ge1/N\), there is already another explicit positive separation. It remains to analyze

\[
\rho<\rho_0,\qquad D<1/N.
\tag{5.3}
\]

The inherited one-row inequality gives \(\rho^2\ge1-t_i/N\) for actual inverse-row support size \(t_i\). Condition (5.3) therefore forces \(t_i=s\) for **every** row.

Let \(S_i\) be those supports and let \(A[r,i]=F[r,i]\mathbf1_{r\in S_i}\), so each column of \(A\) has exactly \(s\) entries. Define

\[
B_0=q^{-1}A^*,\qquad C=F-A.
\]

The mask \(C\) has exactly \(d\) entries per column, but it has not been assumed row-regular or orthogonal. For the rows \(b_i,b_{0i}\), the exact support-restricted identity is

\[
q\|b_i-b_{0i}\|_2^2
=1+q\|b_i\|_2^2-2\operatorname{Re}(b_iF)_i
=\|b_iE\|_2^2-a^2\|b_i\|_2^2
\le D\|b_i\|_2^2.
\tag{5.4}
\]

Here \(b_iE=e_i^T-b_iF\). The normalization \(\|b_{0i}\|_2^2=1/q\) and the common support are essential. Since \(\rho<\rho_0<1\),

\[
\|M\|_2\le U,\qquad \|B\|_2\le1/L,\qquad
\|B_0\|_2\le\|B_0\|_F=\sqrt{N/q}.
\]

Summing (5.4) over **all** rows gives

\[
T:=\|B-B_0\|_2\le\|B-B_0\|_F
\le\frac{\sqrt{ND/q}}{L}.
\tag{5.5}
\]

### 5.3 Controlling the full error Gram

Put \(H=\rho^2I-EE^*\succeq0\). Equation (5.4) gives

\[
0\le b_iHb_i^*=D\|b_i\|_2^2-q\|b_i-b_{0i}\|_2^2
\le D\|b_i\|_2^2.
\]

Therefore

\[
\operatorname{tr}(BHB^*)\le D\|B\|_F^2\le ND/L^2,
\qquad
\|H\|_2\le\operatorname{tr}H
\le\|M\|_2^2\operatorname{tr}(BHB^*)
\le NU^2D/L^2.
\]

Since \(EE^*-a^2I=DI-H\),

\[
\|EE^*-a^2I\|_2\le NU^2D/L^2.
\tag{5.6}
\]

This step genuinely needs all inverse rows; a single near-sharp row cannot control the complete error Gram.

### 5.4 Transfer to the discrete mask

For any square matrix \(X\), define

\[
G(X)=I-XF-F^*X^*+qXX^*.
\]

Using \(BE=I-BF\), one obtains

\[
G(B)=B(EE^*-a^2I)B^*,\qquad
\|G(B)\|_2\le NU^2D/L^4.
\tag{5.7}
\]

The exact complementary-mask identity is

\[
qG(B_0)=C^*C-a^2I.
\tag{5.8}
\]

Also,

\[
\|G(B_0)-G(B)\|_2
\le T\bigl(2+q\|B\|_2+q\|B_0\|_2\bigr)
\le T(2+q/L+\sqrt{Nq}).
\]

Combining (5.5), (5.7), and (5.8),

\[
\|C^*C-a^2I\|_2
\le \frac{qNU^2}{L^4}D
+\frac{\sqrt{Nq}}L(2+q/L+\sqrt{Nq})\sqrt D.
\tag{5.9}
\]

In the present branch, \(D<1/N<1\), so \(D\le\sqrt D\). Using (5.2), \(q\le1\), and \(N\ge2\), the coefficient of \(\sqrt D\) in (5.9) is at most

\[
\frac{1024N}{q^3}+24\sqrt{N/q}+4N
\le\frac{1052N}{q^3}
\le\frac{2048N}{q^3}.
\tag{5.10}
\]

The inequality \(\sqrt{N/q}\le N/q^3\) follows by squaring and using \(q^5\le N\).

If no equality mask exists, the \(C\) extracted from these inverse supports is necessarily a bad mask. Equations (5.1) and (5.10) imply

\[
D\ge\left(\frac{\gamma q^3}{2048N}\right)^2
=\frac{s^6}{2^{22}N^{10}d^{2\varphi(N)-2}}
=:g_{N,s}.
\tag{5.11}
\]

Finally, \(g_{N,s}\le q/(2^{22}N^4)<q/8\) and \(g_{N,s}<1/N\). Thus the easy branches excluded before (5.3) obey the same lower bound. Every admissible \(M\) satisfies \(\|M-F\|_2^2\ge d/N+g_{N,s}\). Taking the infimum proves (Q), with no compactness or attainment assumption needed for this quantitative step. ∎

## 6. Fresh exact controls

`verify_exact.py` is newly written for this packet and does not import or execute either accepted checker. It uses integer and rational arithmetic, exact cyclotomic reductions, exact resultants, and algebraic-field matrix inverses. No floating-point norm tolerance is used.

The checks cover:

1. Exhaustive unlabelled-column support multisets for every \(3\le N\le12\), starting only from degree-three regularity and the prohibition of singleton overlaps. Every result decomposes into the two support types of §2. Column labels are counted exactly; no proposed component classification is used to prune this search.
2. Exhaustive exact Fourier assignment of column labels for \(3\le N\le9\). The passing mask counts are \(1,0,0,14,0,0,432\), respectively. Every passer consists only of full triple blocks and passes (4.1). The \(N=3\) case is a control for the support theorem, not an admissible \(s=0\) optimization claim.
3. Direct exhaustive congruence tests of all normalized conference-block configurations at every even \(2\le N\le32\), and at \(N=40,48,64\). All six congruences are tested using integer modular arithmetic, without using the valuation obstruction as a filter. None passes.
4. Both exact omitted-mask Grams, both inverse support counts, and the block congruences for the divisor construction at every multiple of three from 6 through 60, plus 72, 81, and 90.
5. Equivalence of the four congruences with exact Fourier block orthogonality for every pair of row and column triples at each \(4\le N\le18\).
6. Direct algebraic-field inverse witnesses at \(N=6,9,12\). With \(W=\sqrt N F\), \(Z=\sqrt N M\), and \(K=M^{-1}/\sqrt N\), both inverse products are exactly \(I\), both error Grams are exactly \(3I\), and every inverse row and column has exactly \(N-3\) entries. Deliberately doubling the inverse verifies the nonequality row-rigidity and \(G\)-identities, while failing the floor error Gram.
7. Exact cyclotomic resultants for three-term root polynomials, including exponent collisions, at \(4\le N\le24\), confirming the zero/nonzero norm dichotomy used in (5.1).
8. Rational checks of the final gap formula, exponent normalization, and easy-branch bounds for every \(2\le N\le200\), \(1\le s<N\).
9. Negative controls: a real order-four conference matrix passes ordinary orthogonality but its support filled with Fourier phases fails; an arbitrary triple-block partition in dimension six fails; deleting a required entry fails; and the wrong inverse gain fails.

These finite controls validate formulas and catch normalization or structural mistakes. They do not replace the infinite proofs or claim a complete search of higher composite budgets.

## 7. Scope, cost, and proposed record delta

The new exact classification is for omission weight three. The quantitative theorem applies to any already certified no-mask case; it does not itself decide which other composite weights admit masks. In particular, the condition \(d\mid N\) remains a general sufficient condition and is now known necessary at \(d=2,3\), but necessity is not asserted for general \(d\).

The explicit quantitative gap is intentionally small. No optimal rate, conditioning improvement, exact nonsharp optimizer, numerical tightness, faster Fourier transform, low-cost application algorithm, finite-word stability guarantee, or arithmetic lower bound is asserted. Formula (1.2) can produce a dense approximating matrix and requires an inverse or equivalent solve. All original sparse-column, shared-frame, preparation/output cost, and implementation limitations remain intact. No historical-priority or worldwide-novelty claim is made.

Conditional record delta after independent acceptance:

> Added a complete codimension-three sharpness classification: Delta(N,N−3)=sqrt(3/N) exactly when 3 divides N; otherwise the infimum is strictly above the floor. Every weight-three equality mask decomposes into full 3×3 blocks, with an explicit four-congruence phase test. Proved the general quantitative no-mask bound Delta(N,s)^2 ≥ (N−s)/N + s^6/[2^22 N^10 (N−s)^(2φ(N)−2)], giving explicit strict gaps in this family and in previously accepted no-mask cases. Exact nonsharp optima and the remaining composite-budget classification stay open. Retain M-SPARSE-DEFECT, TO RESEARCH, priority 42.

No GitHub, repository index, spreadsheet, or other external state was modified by this task.
