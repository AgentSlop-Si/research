# Exact global C8 rank-zero phase minimum

20 October 2026 UTC. Candidate proof, pending independent review.

## Theorem and scope

Let

\[
F_{jk}=8^{-1/2}e^{-2\pi i jk/8},\qquad 0\leq j,k<8.
\]

In the original model with arbitrary invertible complex-monomial outer matrices, arbitrary real core, rank-zero correction, and the external operator norm,

\[
\boxed{\min_{L,R\text{ invertible complex monomial},\ C\in\mathbb R^{8\times8}}
\|F-LCR\|_2
=\min_{P,Q\text{ diagonal unitary}}\|\operatorname{Im}_{\rm entry}(PFQ)\|_2
=\frac12\sqrt{1+\sqrt{\sqrt2-1}}.}
\]

The minimum is attained by the previously accepted exact witness, reproduced below. The new part is the all-phase lower bound. In particular, four-periodicity is proved to be sufficient in the relevant positive-accretivity regime; it is not assumed for arbitrary phases. No claim that every minimizer is periodic, or a classification of all minimizing phases, is made.

Write

\[
h=\sqrt{\sqrt2-1},\quad m=\frac{1-h}{2},\quad
\theta_* =\arccos m,\quad d_*=\frac12\sqrt{1+h}.
\]

Thus \(0<m<1/2\), \(0<\theta_*<\pi/2\), and \(d_*^2=(1-m)/2\).

## 1. Exact reduction from the original model

Every complex invertible monomial L and R can be written
\(L=D_LM_L\), \(R=M_RD_R\), where D_L,D_R are diagonal unitary and M_L,M_R are real invertible monomial. Therefore \(M_LCM_R\) ranges over all real cores. This is equality of the represented approximants, not a nonunitary rescaling of the residual.

For fixed diagonal-unitary P,Q, put V=PFQ. Entrywise imaginary part is contractive in complex operator norm, because
\(\operatorname{Im}_{\rm entry} M=(M-\overline M)/(2i)\) and \(\|\overline M\|_2=\|M\|_2\). Consequently

\[
\min_{C\in\mathbb R^{8\times8}}\|V-C\|_2
=\|\operatorname{Im}_{\rm entry}V\|_2,
\]

attained at C=Re_entry V. Unitary exterior factors preserve the external norm, proving the first equality of the theorem.

Let A=P², B=Q² and U=FAFB. For V=X+iY, the symmetric unitary matrix W=VᵀV satisfies

\[
Y^TY=(I-\operatorname{Re}_{\rm entry}W)/2.
\]

Since W is symmetric, its entrywise real part equals its Hermitian part. Also \(Q^{-1}WQ=U\), a unitary similarity. Therefore

\[
\|Y\|_2^2=\frac{1-\lambda_{\min}(\operatorname{Herm}U)}2,
\qquad \operatorname{Herm}U=(U+U^*)/2.
\]

All diagonal unitary A,B occur, because every such phase has a unitary square root. It remains to prove

\[
\lambda_{\min}(\operatorname{Herm}(FAFB))\leq m
\quad\text{for every diagonal unitary A,B.}
\tag{1}
\]

## 2. Positive-accretivity normalization lemma

**Lemma 1.** Let U be unitary, T Hermitian with \(0\leq T\leq I\), and c>0. If
\(\operatorname{Herm}(UT)\geq cI\), then \(\operatorname{Herm}U\geq cI\).

For a unit eigenvector Ux=λx, normality gives x*U=λx*. Hence

\[
c\leq x^*\operatorname{Herm}(UT)x
=(\operatorname{Re}\lambda)\,x^*Tx.
\]

Because \(0\leq x^*Tx\leq1\) and c>0, this forces \(\operatorname{Re}\lambda\geq c\). The eigenvectors of U form an orthonormal basis, proving the claim. **No commutation of U and T is needed.**

## 3. A valid all-phase four-periodicity reduction

Let H be the half-shift \(He_j=e_{j+4}\), with indices modulo 8. For arbitrary A, the unitary cyclic-Hankel matrix C=FAF has entries C[j,k]=c[j+k]. Therefore

\[
HCH=C,
\tag{2}
\]

because simultaneously shifting both indices by 4 changes their sum by 8. This holds without any periodicity of A.

Suppose \(\operatorname{Herm}(CB)\geq cI\) for c>0. Average with the H-conjugate and use (2):

\[
\operatorname{Herm}(CE)\geq cI,
\qquad E=(B+HBH)/2.
\]

E is diagonal, its entries j and j+4 are equal, and every entry has modulus at most one. Write E=DT, where D is diagonal unitary with period 4 and T=|E| is diagonal with \(0\leq T\leq I\). Any phase can be chosen at a zero entry; the argument works regardless. Since CD is unitary, Lemma 1 gives

\[
\operatorname{Herm}(CD)\geq cI.
\]

Thus B may be replaced by a four-periodic diagonal unitary without degrading a positive lower bound on the Hermitian part.

Next note that FAFB and FBFA are unitarily similar: with X=FA and Y=FB, they are XY and YX, and \(X^{-1}(XY)X=YX\). Apply the same argument to FBFA to replace A by a four-periodic diagonal unitary while keeping the already periodic B. Swap back by the same unitary cyclic similarity.

**Conclusion.** Whenever an arbitrary pair has \(\operatorname{Herm}(FAFB)\geq cI\) with c>0, a pair with both A and B four-periodic has the same or stronger inequality. This is an existence reduction, not a claim about every minimizer.

## 4. A sharp elementary inequality for positive 2-by-2 contractions

Here asin and acos have their usual real principal branches.

**Lemma 2 (opposite-pair balancing).** If

\[
R=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
0<a,b,c,d<1,\qquad \|R\|_2\leq1,
\]

then

\[
\arcsin b+\arcsin c
\leq 2\arcsin\sqrt{(1-a)(1-d)}.
\tag{3}
\]

First, if necessary, increase b and c by a common positive factor until the norm is one, holding a,d fixed. Continuity and monotonicity of the norm for entrywise nonnegative matrices guarantee such a first boundary point; it remains a contraction and its entries remain below one. This only increases the left side. We may therefore assume the largest singular value is one.

Set q=bc and K=a²+d²−a²d². The exact singular-value boundary identity is

\[
0=\det(I-R^TR)
=1-a^2-b^2-c^2-d^2+(ad-bc)^2.
\]

Rearranging gives

\[
(b+c)^2=(1-ad+q)^2-(a-d)^2.
\tag{4}
\]

Since \((b+c)^2\geq4q\), equation (4) implies

\[
[q-(1-a)(1-d)]\,[q-(1+a)(1+d)]\geq0.
\]

As q<1 and (1+a)(1+d)>1,

\[
q\leq q_{\max}:=(1-a)(1-d).
\tag{5}
\]

The cosine addition formula and (4) yield

\[
\cos(\arcsin b+\arcsin c)
=\sqrt{K+2adq}-q.
\tag{6}
\]

The function on the right is strictly decreasing for q≥0, because

\[
K-a^2d^2=a^2+d^2-2a^2d^2>0.
\]

At q=q_max,

\[
K+2adq_{\max}=(a+d-ad)^2,
\]

so the right side of (6) equals \(1-2q_{\max}\), the cosine of \(2\arcsin\sqrt{q_{\max}}\). Both angles lie in [0,π], on which cosine is decreasing. Equations (5) and (6) prove (3).

**Lemma 3 (sharp four-angle inequality).** If every entry r_ij of a real nonnegative 2-by-2 contraction is at least m, with \(0<m\leq1/2\), then

\[
\sum_{i,j}\arccos r_{ij}
\geq2\arccos m+2\arccos(1-m).
\tag{7}
\]

All entries are strictly below one because each row and column has another positive entry. Write R as in Lemma 2 and set \(t=\sqrt{(1-a)(1-d)}\). Lemma 2 shows that replacing the off-diagonal pair b,c by t,t cannot decrease the sum of the four arcsines. The replacement

\[
R'=\begin{pmatrix}a&t\\t&d\end{pmatrix}
\]

is a contraction: its eigenvalues are 1 and a+d−1, both in [−1,1]. Moreover t≥m. To see this, (5) applied after the boundary increase gives \(t^2\geq bc\geq m^2\); or the same inequality follows directly from positivity of I−Herm R and \((b+c)/2\geq m\). Also a,d≥m imply t≤1−m.

Apply Lemma 2 again to the column-swapped matrix \(\begin{psmallmatrix}t&a\\d&t\end{psmallmatrix}\). It gives

\[
\arcsin a+\arcsin d\leq2\arcsin(1-t).
\]

Thus

\[
\sum_{i,j}\arcsin r_{ij}
\leq2\arcsin t+2\arcsin(1-t).
\]

The function \(t\mapsto\arcsin t+\arcsin(1-t)\) is convex and symmetric on [0,1]. Its maximum on [m,1−m] is therefore its common endpoint value. Subtract from 2π to obtain (7). Equality is attained at \(\begin{psmallmatrix}m&1-m\\1-m&m\end{psmallmatrix}\).

## 5. Four full invariant sectors for periodic phases

By Section 3 it suffices to rule out a periodic pair satisfying Herm U≥cI for c>m. Parameterize the four entries of A and B, repeated twice, as

\[
\begin{aligned}
a_0&=e^{i(s+x)},&a_2&=e^{i(s-x)},&
a_1&=e^{i(t+y)},&a_3&=e^{i(t-y)},\\
b_0&=e^{i(u+v)},&b_2&=e^{i(u-v)},&
b_1&=e^{i(w+r)},&b_3&=e^{i(w-r)}.
\end{aligned}
\]

All real choices of the original phases are covered; no restriction on the signs of cosines or sines is imposed. Put

\[
\alpha=e^{is}\cos x,\quad \beta=i e^{is}\sin x,
\quad\gamma=e^{it}\cos y,\quad\delta=e^{it}\sin y.
\]

The four orthogonal parity/half-shift sectors have ordered bases
\((e_j+\eta e_{j+4})/\sqrt2,(e_{j+2}+\eta e_{j+6})/\sqrt2\),
with j=0,1 and η=±1. Direct normalized Fourier summation gives, in the order even,+; even,−; odd,+; odd,−,

\[
\begin{aligned}
M_0&=\begin{pmatrix}\alpha&\beta\\\beta&\alpha\end{pmatrix}\operatorname{diag}(b_0,b_2),\\
M_1&=\begin{pmatrix}\gamma&\delta\\\delta&-\gamma\end{pmatrix}\operatorname{diag}(b_0,b_2),\\
M_2&=\begin{pmatrix}\beta&\alpha\\\alpha&\beta\end{pmatrix}\operatorname{diag}(b_1,b_3),\\
M_3&=\begin{pmatrix}\delta&-\gamma\\-\gamma&-\delta\end{pmatrix}\operatorname{diag}(b_1,b_3).
\end{aligned}
\tag{8}
\]

Each block is unitary. Their determinant half-arguments, taken modulo π, are

\[
S_0=s+u,\quad S_1=t+u+\pi/2,\quad
S_2=s+w+\pi/2,\quad S_3=t+w+\pi/2.
\]

In particular

\[
S_0+S_3-S_1-S_2\equiv-\pi/2\pmod\pi.
\tag{9}
\]

Their absolute normalized traces are

\[
p_0=|\cos x\cos v|,\quad p_1=|\cos y\sin v|,
\quad p_2=|\sin x\cos r|,\quad p_3=|\sin y\sin r|.
\tag{10}
\]

The matrix

\[
K_0=\begin{pmatrix}p_0&p_1\\p_2&p_3\end{pmatrix}
\tag{11}
\]

is a real nonnegative contraction. Indeed, it is the entrywise product of

\[
\begin{pmatrix}|\cos x|&|\cos y|\\|\sin x|&|\sin y|\end{pmatrix},\qquad
\begin{pmatrix}|\cos v|&|\sin v|\\|\cos r|&|\sin r|\end{pmatrix}.
\]

The first factor has unit Euclidean norm in each column, and the second in each row. Cauchy–Schwarz applied to the double sum for \(\ell^TK_0 k\) bounds its absolute value by \(\|\ell\|_2\|k\|_2\). Thus (11) is an operator-norm contraction, not a heuristic compression surrogate.

## 6. All-phase lower bound and exact endpoint

Suppose, for contradiction, that some arbitrary phases satisfy
\(\lambda_{\min}(\operatorname{Herm}U)=c>m\). Let θ=acos c, so \(0\leq\theta<\theta_*<\pi/2\). Section 3 yields periodic phases with Herm U≥cI.

For each of the four unitary blocks, choose its two eigenvalue arguments φ_i,+ and φ_i,− in [−θ,θ]. Define their midpoint σ_i and half-separation β_i≥0. Then

\[
|\sigma_i|+\beta_i\leq\theta,\qquad
p_i=|\operatorname{tr}M_i|/2=\cos\beta_i,
\quad \beta_i=\arccos p_i.
\tag{12}
\]

In particular p_i≥c>m. The determinant identity (9) implies

\[
\sigma_0+\sigma_3-\sigma_1-\sigma_2\equiv-\pi/2\pmod\pi,
\]

so \(\sum_i|\sigma_i|\geq\pi/2\). Summing (12) gives

\[
\sum_i\arccos p_i\leq4\theta-\pi/2.
\tag{13}
\]

On the other hand Lemma 3 applied to (11), with the fixed lower threshold m, gives

\[
\sum_i\arccos p_i\geq2\arccos m+2\arccos(1-m).
\tag{14}
\]

The radical identity h²=√2−1 implies

\[
\sqrt{1-m^2}=\sqrt2(1-m)-m>0.
\]

Consequently

\[
\cos(\theta_*-\pi/4)=1-m.
\]

Since θ_*∈(π/4,π/2), the principal branches give
\(\arccos(1-m)=\theta_*-\pi/4\). The right side of (14) is therefore \(4\theta_*-\pi/2\), strictly larger than (13). This contradiction proves (1), including all nonperiodic phases.

## 7. Exact attaining witness and legal external residual

Let

\[
z=h+i\sqrt{2-\sqrt2},\quad \zeta=e^{i\pi/4},\quad\rho=e^{i\pi/8},
\quad w=\sqrt{(1+h)/2}+i\sqrt{(1-h)/2}.
\]

Then |z|=|w|=1 and w²=z. Repeat the following four entries twice:

\[
P=(-iw,\rho^{-1}w,1,\rho^{-1}),\qquad
Q=(1,\rho^3w^{-1},iw^{-1},\rho^3).
\]

Their squares are
\(A=(-z,\zeta^{-1}z,1,\zeta^{-1})\) and
\(B=(1,\zeta^3/z,-1/z,\zeta^3)\), repeated twice.

Substitution in (8) gives traces/determinants (1−h,1) for M₀,M₃ and \((\zeta^{-1}(1+h),-i)\) for M₁,M₂. The full spectrum is

\[
e^{i\theta_*}\ (2),\qquad e^{-i\theta_*}\ (4),\qquad
 e^{i(\theta_*-\pi/2)}\ (2).
\]

Thus the minimum Hermitian eigenvalue is exactly m, and the phase defect is exactly \(\sqrt{(1-m)/2}=d_*\). The actual original-model witness is

\[
C=\operatorname{Re}_{\rm entry}(PFQ),\quad L=P^*,\quad R=Q^*,\quad E=0.
\]

Its external residual is \(P^*i\operatorname{Im}_{\rm entry}(PFQ)Q^*\), of norm d_*.

## 8. Dependencies, computational role, and exclusions

The original phase equivalence and exact upper witness were previously independently accepted. This document reproduces their needed mathematical details and supplies a new global lower proof. Its new argument does not use, alter, or retune the completed quantitative lower-bound chain.

The accompanying fresh exact checker verifies generic sector entries, trace/determinant identities, pair-balancing polynomial identities, the radical threshold, and the supplied witness trace/determinant data. The normalization lemma, monotonicity and branch arguments are elementary proofs stated above; finite grids and numerical optimization are not premises.

Exploratory searches used all 15 free phase variables. They found no smaller witness but do not prove optimality. Separate exploratory files record their numerical provenance. No external service was mutated during this candidate work.
