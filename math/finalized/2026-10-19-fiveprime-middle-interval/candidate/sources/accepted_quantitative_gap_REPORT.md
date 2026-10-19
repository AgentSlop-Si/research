# M-SPARSE-DEFECT: entrywise stability and polynomial small-codimension gaps

Date: 2026-10-18. Owner: **M-SPARSE-DEFECT**. Candidate for independent review; retain **TO RESEARCH**, priority **42**.

## Results first

Continue the accepted model

\[
F_N[r,c]=N^{-1/2}\omega^{rc},\quad \omega=e^{-2\pi i/N},\qquad
\Delta_{N,s}=\inf\{\|M-F_N\|_2:M\in GL_N(\mathbb C),\ \text{every row of }M^{-1}\text{ has at most }s\text{ nonzeros}\}.
\]

Write \(d=N-s\), \(q=s/N\), and \(a=\sqrt{d/N}\). The support condition is simultaneous on **every** inverse row, with arbitrary complex coefficients and support patterns. No condition-number hypothesis is imposed.

### A. Stronger general quantitative no-mask theorem

If no weight-\(d\) complementary Fourier mask is a scaled unitary, then

\[
\boxed{\Delta_{N,s}^2\ge \frac dN+\frac1{10N\,d^{\varphi(N)-1}}.}\tag{A}
\]

The premise automatically excludes \(d=1\) and \(N=2\). A stronger, explicitly stated radical bound is proved in (S) below. In contrast to the earlier accepted quantitative result, this proof has no powers of \(s/N\), loses no global trace factor \(N\), and uses paired complex embeddings to halve the cyclotomic exponent.

### B. Polynomial gaps in the two accepted small-codimension nonsharp families

\[
\boxed{\begin{aligned}
N\ge4,\quad3\nmid N&\quad\Longrightarrow\quad
\Delta_{N,N-3}^2\ge\frac3N+\frac1{30N^3},\\
N\ge3\text{ odd}&\quad\Longrightarrow\quad
\Delta_{N,N-2}^2\ge\frac2N+\frac1{5N^3}.
\end{aligned}}\tag{B}
\]

These are lower bounds on the **squared** gap. They neither determine the exact nonsharp optimum nor assert optimal rates. The no-mask classifications in these two families are accepted input, not re-proved or re-tested here. This packet supplies new stability and root-separation arguments. It does not classify weight four or the remaining composite budgets.

## 1. Accepted inputs and scope

The exact source files used are copied and hashed in `SOURCE_BINDINGS.json`.

The accepted equivalence is

\[
\Delta_{N,s}=a\quad\Longleftrightarrow\quad
C=F_N\circ R,\quad R\in\{0,1\}^{N\times N},\quad
\text{each column of }R\text{ has }d\text{ ones},\quad C^*C=a^2I.
\]

The accepted sources classify weight three as sharp exactly when \(3\mid N\) and record the earlier weight-two classification, sharp exactly when \(2\mid N\). They also prove the older general no-mask gap

\[
g_{\rm old}=\frac{s^6}{2^{22}N^{10}d^{2\varphi(N)-2}}.
\]

This packet gives a direct inequality for every admissible \(M\), followed by taking an infimum. No new attainment or compactness claim is needed. When \(d=1\), a mask supported on any permutation is a scaled unitary; thus every no-mask case has \(d\ge2\), \(N\ge3\), and even \(\varphi(N)\).

## 2. Entrywise near-equality stability

The following formulation isolates the analytic argument from root-sum estimates.

**Stability theorem.** Suppose no equality mask exists, and let \(0<\eta\le1/N\) be such that every bad column-weight-\(d\) Fourier mask has some off-diagonal Gram entry of modulus at least \(\eta\). Then

\[
\boxed{\Delta_{N,s}^2\ge a^2+
\frac{\eta^2}{\left(a+\sqrt{a^2+2\eta}+\eta/\sqrt q\right)^2}.}\tag{S}
\]

In particular,

\[
\boxed{\Delta_{N,s}^2\ge a^2+\frac{\eta^2}{10a^2}.}\tag{S'}
\]

### 2.1 Exact row identities and support saturation

Fix an admissible \(M\), and set \(B=M^{-1}\), \(E=M-F\), \(\rho=\|E\|_2\), \(D=\rho^2-a^2\ge0\). If the actual support size of row \(b_i\) is \(t_i\), Cauchy--Schwarz gives

\[
\rho^2\ge\frac{\|e_i^T-b_iF\|_2^2}{\|b_i\|_2^2}
\ge 1+\|b_i\|_2^{-2}-2\sqrt{t_i/N}\,\|b_i\|_2^{-1}
\ge 1-t_i/N.
\]

Consequently, if \(D<1/N\), **every** \(t_i=s\). Otherwise the final lower bound follows from the easy-branch comparison in §2.4.

For the actual supports \(S_i\), define

\[
A[r,i]=F[r,i]\mathbf1_{r\in S_i},\qquad C=F-A,\qquad
B_0=q^{-1}A^*,\qquad K=q(B-B_0).
\]

Every column of \(C\) has norm \(a\). Each row \(b_{0i}\) has norm \(q^{-1/2}\). Completing the square on the common support gives the exact identity

\[
q\|b_i-b_{0i}\|_2^2
=\|b_iE\|_2^2-a^2\|b_i\|_2^2
\le D\|b_i\|_2^2.\tag{2.1}
\]

Because \(D<1/N\le q\), the triangle inequality implies

\[
\|b_i\|_2\le\frac1{\sqrt q-\sqrt D}.
\]

Put \(k_i=\|K[i,:]\|_2\) and \(u_i=\sqrt{qD}\,\|b_i\|_2\). Then

\[
k_i\le u_i\le u:=\frac{\sqrt D}{1-\sqrt{D/q}}.\tag{2.2}
\]

These are rowwise bounds, with no inverse condition-number estimate and no sum over the rows.

### 2.2 A PSD decomposition with matching diagonals

Let \(H=\rho^2I-EE^*\succeq0\) and define

\[
P=qBHB^*+KK^*\succeq0,\qquad Z=C^*C-a^2I.
\]

Equation (2.1), before replacing \(\|b_iE\|^2\) by its upper bound, gives

\[
P_{ii}=qD\|b_i\|_2^2=u_i^2.\tag{2.3}
\]

The exact matrix identity is

\[
\boxed{Z=qD BB^*-P+KC+C^*K^*.}\tag{2.4}
\]

For completeness, put \(G(X)=I-XF-F^*X^*+qXX^*\). Using \(BE=I-BF\),

\[
G(B)=B(EE^*-a^2I)B^*=D BB^*-BHB^*,\qquad qG(B_0)=Z.
\]

Expanding \(G\) at \(B_0\), with \(qB_0^*=A\) and \(F-A=C\), yields
\(Z=qG(B)+KC+C^*K^*-KK^*\), which is (2.4).

### 2.3 Control one nonzero entry, rather than the full spectral defect

Both \(qD BB^*\) and \(P\) are positive semidefinite and have diagonal entries \(u_i^2\). Hence their \((i,j)\) entries each have modulus at most \(u_i u_j\). Since each column of \(C\) has norm \(a\), (2.4) gives

\[
|Z_{ij}|\le2u_i u_j+a(k_i+k_j)\le2u^2+2au.\tag{2.5}
\]

The diagonal of \(Z\) is zero. The extracted \(C\) cannot be an equality mask, so some off-diagonal entry has modulus at least \(\eta\). Therefore

\[
\eta\le2u^2+2au,\qquad
u\ge\frac{\sqrt{a^2+2\eta}-a}{2}
=\frac{\eta}{\sqrt{a^2+2\eta}+a}=:r.
\]

Substitute (2.2) and solve for \(\sqrt D\):

\[
\sqrt D\ge\frac{r}{1+r/\sqrt q}
=\frac{\eta}{a+\sqrt{a^2+2\eta}+\eta/\sqrt q}.
\]

This proves the bound in the branch \(D<1/N\).

### 2.4 Easy branch and a clean constant

Let \(g\) be the additive term in (S). Its denominator is at least \(2a\), so

\[
g\le\frac{\eta^2}{4a^2}\le\frac1{4Nd}<\frac1N.
\]

Thus the easy branch \(D\ge1/N\) obeys the same bound. Taking the infimum proves (S).

For (S'), use \(d\ge2\), \(s\ge1\), and \(\eta\le1/N\):

\[
\frac\eta{a^2}\le\frac1d\le\frac12,
\qquad\frac\eta{a\sqrt q}\le\frac1{\sqrt{ds}}\le\frac1{\sqrt2}.
\]

Consequently,

\[
\frac{a+\sqrt{a^2+2\eta}+\eta/\sqrt q}{a}
\le1+\sqrt2+1/\sqrt2=1+3/\sqrt2,
\]

whose square is \(11/2+3\sqrt2<10\). This proves (S'). The exact radical bound (S) remains available instead of the rounded constant 10. ∎

## 3. Paired cyclotomic embeddings: the general theorem

An off-diagonal entry of a column-weight-\(d\) mask Gram is

\[
\frac1N\xi,\qquad \xi=\sum_{r\in T}\omega^{r(j-i)},\quad |T|\le d.
\]

If nonzero, \(\xi=P(\omega)\) is a nonzero cyclotomic algebraic integer. The norm over \(\mathbb Q(\omega)\) is a nonzero integer. Its factors include both \(\xi\) and \(\overline\xi\), because \(N\ge3\). Every other conjugate has modulus at most \(d\). Therefore

\[
1\le|\operatorname{Norm}(\xi)|\le|\xi|^2 d^{\varphi(N)-2},
\qquad |\xi|\ge d^{1-\varphi(N)/2}.
\]

Irreducibility ensures that a nonzero value has no zero conjugate. Repeated exponents cause no difficulty. This argument still uses both embeddings when \(\xi\) is real; they are factors of the field norm with their appropriate multiplicities.

Thus the admissible entrywise separation is

\[
\eta_{\rm cyc}=\frac1{N d^{\varphi(N)/2-1}}\le\frac1N.
\]

Apply (S') to obtain

\[
\Delta_{N,s}^2\ge a^2+\frac{\eta_{\rm cyc}^2}{10a^2}
=\frac dN+\frac1{10N d^{\varphi(N)-1}},
\]

which proves (A). Its ratio to the previously accepted additive gap is exactly

\[
\frac{g_{\rm new}}{g_{\rm old}}=
\frac{2^{22}N^9d^{\varphi(N)-1}}{10s^6}>1.
\]

This is a uniform strengthening wherever the old no-mask theorem applies, not merely an improvement in selected numerical examples.

## 4. Elementary geometry eliminates the exponential factor at weights two and three

### 4.1 Two roots

For two \(N\)-th roots, write their circular exponent difference as \(k\), with \(0\le k\le N/2\). The modulus of their sum is \(2\cos(\pi k/N)\).

If \(N\) is odd, the minimum is \(2\sin(\pi/(2N))\ge2/N\), using \(\sin x\ge2x/\pi\) for \(0\le x\le\pi/2\). For even \(N\), a nonzero two-root sum has modulus at least \(2\sin(\pi/N)\ge4/N\). Exact zero sums in the even case are excluded from this statement.

Thus in odd dimension every nonzero sum of at most two roots has modulus at least \(2/N\). Every bad weight-two mask has a Gram entry of modulus at least \(\eta=2/N^2\le1/N\). The accepted odd-dimensional no-mask theorem and (S') give

\[
\Delta_{N,N-2}^2\ge\frac2N+\frac{(2/N^2)^2}{10(2/N)}
=\frac2N+\frac1{5N^3}.
\]

### 4.2 Three roots when \(3\nmid N\)

**Lemma.** If \(3\nmid N\), every sum of three \(N\)-th roots, with repetitions allowed, has modulus at least \(1/N\).

**Proof.** For any two of the roots, put \(u=\pi k/N\in[0,\pi/2]\), so their sum has modulus \(2\cos u\). Reverse triangle inequality with the third root gives

\[
|z_1+z_2+z_3|\ge|2\cos u-1|.
\]

For \(0\le u\le\pi/3\), concavity of \(2\cos u\) places its graph above the chord from \((0,2)\) to \((\pi/3,1)\), giving
\(2\cos u-1\ge(3/\pi)(\pi/3-u)\).
For \(\pi/3\le u\le\pi/2\), integration of \(2\sin t\ge\sqrt3>3/\pi\) gives
\(1-2\cos u\ge(3/\pi)(u-\pi/3)\).
Since \(3\nmid N\), the integer \(3k-N\) is nonzero. Hence

\[
|2\cos u-1|\ge\frac3\pi\left|u-\frac\pi3\right|
=\frac{|3k-N|}{N}\ge\frac1N.
\]
∎

At weight three with \(3\nmid N\), a nonzero overlap sum has one, two, or three terms. A singleton has modulus 1, the nonzero two-term sums satisfy §4.1, and the three-term sums satisfy the lemma. Therefore every bad mask has a Gram entry of modulus at least \(\eta=1/N^2\). The accepted codimension-three obstruction and (S') give

\[
\Delta_{N,N-3}^2\ge\frac3N+\frac{(1/N^2)^2}{10(3/N)}
=\frac3N+\frac1{30N^3}.
\]

The general cyclotomic bound and these polynomial bounds can be combined by taking their maximum; neither is claimed to dominate the other at every small dimension. The sharper formula (S) can also be used with the larger available \(\eta\).

## 5. Fresh exact controls and negative controls

`verify_exact.py` is new and imports or executes none of the accepted checkers. Its controls concern the new proof, not a re-search of the accepted support classifications.

1. Exact algebraic matrix tests of (2.1)--(2.4), support saturation, matching PSD diagonals, and the Gram-entry reconstruction for a nonsharp \(N=3,s=1\) witness and a nonuniform row-scaled perturbation. The base witness has \(\|M-F_3\|_2^2=3/4\) exactly, hence \(D=1/12\), while every inverse row has exactly one nonzero.
2. Two fresh perturbed witnesses at \(N=4\), with \(s=2,3\). The extracted masks need not be bad for the identities to hold. PSD is certified by **all principal minors**, with exact rational or algebraic arithmetic.
3. Negative controls: increasing the nonuniform perturbation while retaining the same claimed error bound produces a negative principal minor; reversing the sign of the \(KC\) terms fails reconstruction. These catch an uncertified norm bound and a sign error in the new argument.
4. Exact cyclotomic resultants, conjugation reductions, and paired norm identities for deterministic root polynomials, including repeated exponents and vanishing examples. The conjugation operation and field multiplicities are checked independently of numeric complex evaluation.
5. Exhaustive circular-difference lattice checks and exhaustive root sums at the dimensions listed in `RESULTS.json`. Trigonometric enclosures are rigorous integer fixed-point intervals derived from an exact alternating-series Machin bound for \(\pi\) and a Taylor remainder. No floating-point tolerance decides zero, a norm inequality, or a theorem.
6. Rational checks of the uniform constant, easy-branch bounds, formula normalization, and strict improvement over the old general gap. The polynomial bounds are checked algebraically, without assuming they dominate the general bound at small dimensions.

Finite controls are checks of formulas and proof mechanisms, not substitutes for the infinite arguments. The checker prints `PASS` and writes `RESULTS.json` only after all assertions pass.

## 6. Scope and proposed record delta

No new equality-mask classification is asserted. In particular, the remaining composite budgets, weight four, exact nonsharp optima, and optimal asymptotic gaps remain open. Nothing here gives a low-cost algorithm for applying the associated approximating matrices, changes the global inverse-row budget, or weakens earlier shared-frame, implementation, stability, or arithmetic-cost caveats. No priority or worldwide-novelty claim is made.

Conditional record delta after independent acceptance:

> Strengthened the general no-mask squared-gap bound to 1/[10 N d^(phi(N)−1)], d=N−s, using an entrywise matching-diagonal PSD identity and paired cyclotomic embeddings; a sharper explicit radical bound is available. Added polynomial squared gaps 1/(30N^3) in the accepted codimension-three nonsharp family 3∤N and 1/(5N^3) in the accepted odd codimension-two family. These bounds hold for every admissible matrix before taking the infimum and preserve simultaneous sparsity of all inverse rows. Remaining composite classifications and exact optima stay open. Retain M-SPARSE-DEFECT, TO RESEARCH, priority 42.

No GitHub, repository index, spreadsheet, or other external state was modified.
