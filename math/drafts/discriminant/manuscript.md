# Research draft on local Rogers Szegő discriminants and composite squarefreeness

10 October 2026. Mathematical draft for review. No authorship, publication, or priority claim is assigned by this document.

## Abstract

Let \(H_n(z;q)=\sum_{k=0}^n {n\brack k}_qz^k\) be the Rogers–Szegő polynomial, and let its discriminant use the ordinary derivative in \(z\). We give the complete leading polynomial and ordinary-discriminant coefficient when \(q\) moves away from an odd-order root of unity along \(q^d-1=\varepsilon^2\). Separate root clusters have a Hermite limit. A cluster sharing the simple residual root \(-1\) has the limit \(y\operatorname{He}_A(y)-\tau\operatorname{He}'_A(y)\). A parameter-disk argument removes its discriminant guard at half residual degree in characteristic zero. An inverse-pair argument in characteristic \(p\), with its exact exceptional case, then gives a simultaneous residue-component criterion for squarefreeness at order \(sp\).

Exact integral certificates establish that, for
\[
s\in\{3,7,11,15,19\},\qquad p\equiv1\pmod4\text{ prime},\qquad p\nmid s,
\]
\(H_{(sp-1)/2}(z;\zeta_{sp})\) is squarefree for every primitive \(sp\)-th root. In the \(s=15\) family this requires \(p\ne5\). These are five infinite families, not a proof for arbitrary composite or repeated-prime orders. All proof dependencies needed for these statements, including the half-order resonance result and the arithmetic bridge, are reproduced below. The finite certificates are included in an appendix with exact reconstruction instructions and integer gcd witnesses.

Lubinsky and Saff [LS87] already supply the root-of-unity factorization, recurrence, and relevant Padé determinant and denominator. These are explicitly treated as classical ingredients. Completion of the proofs in this note does not establish publication priority: comparison with the full text of Zhedanov [Z97] and the earlier citation chain remains pending.

## 1 Notation and theorem scope

For \(n\ge0\), the Gaussian binomial coefficients are the polynomials determined by
\[
{0\brack0}_q=1,\qquad {n\brack k}_q={n-1\brack k}_q+q^{n-k}{n-1\brack k-1}_q,
\]
with out-of-range coefficients zero. Equivalently, when the denominators are nonzero,
\[
{n\brack k}_q=\frac{(q;q)_n}{(q;q)_k(q;q)_{n-k}},\qquad
(a;q)_j=\prod_{t=0}^{j-1}(1-aq^t).
\]
Set
\[
H_n(z;q)=\sum_{k=0}^n{n\brack k}_qz^k,\qquad D_n(q)=\operatorname{Disc}_zH_n(z;q)\in\mathbb Z[q].
\]
For a monic polynomial \(f=\prod_{i=1}^e(z-\rho_i)\), use
\[
\operatorname{Disc}f=\prod_{i<j}(\rho_i-\rho_j)^2
=(-1)^{e(e-1)/2}\operatorname{Res}(f,f').
\]
Discriminants of constant \(1\) and monic linear polynomials are \(1\). Our resultant convention is \(\operatorname{Res}(f,g)=\prod_{f(\rho)=0}g(\rho)\) for monic \(f\), with multiplicity. No q-derivative discriminant is used.

The monic probabilists' Hermite polynomials satisfy
\[
\operatorname{He}_0=1,\quad \operatorname{He}_1=y,\quad
\operatorname{He}_{a+1}=y\operatorname{He}_a-a\operatorname{He}_{a-1}.
\]
Write \(P_A=\prod_{j=1}^A j^j\), with an empty product equal to one. The letter \(P\) without a subscript will also denote a reciprocal-polynomial transform in Section 8, and a cycle matrix only in Section 10; these uses are explicitly local.

For a primitive \(s\)-th root \(\omega\), let
\(\mathcal O_s=\mathbb Z[\omega]\), and let \(\iota\) send \(\omega\) to \(\omega^{-1}\). Define
\[
\operatorname{cont}_s(a)=\gcd(|a_0|,\ldots,|a_{\varphi(s)-1}|),\qquad
a=\sum_{j=0}^{\varphi(s)-1}a_j\omega^j.
\]
The content of zero is zero. For nonzero \(a\), this is equivalently the greatest positive integer \(k\) for which \(a\in k\mathcal O_s\); it is computed only after reduction modulo the cyclotomic polynomial \(\Phi_s\). It is neither an algebraic norm nor the content of an unreduced product. The power basis is a free integral basis for this ring because \(\Phi_s\) is monic and irreducible.

The main family result is proved in Section 9. Sections 2–7 contain general guarded statements as well as their proofs. General lower-base content support and repeated-prime arithmetic are not silently included in the theorem.

## 2 Elementary polynomial identities

### Lemma 2.1 Rogers Szegő identities

The defining coefficients give
\[
H_0=1,\quad H_1=1+z,\quad
H_n=(1+z)H_{n-1}+(q^{n-1}-1)zH_{n-2},\tag{2.1}
\]
\[
z^nH_n(z^{-1};q)=H_n(z;q),\tag{2.2}
\]
and, as a coefficientwise formal identity over \(\mathbb Q(q,z)\),
\[
\sum_{n\ge0}\frac{H_n(z;q)t^n}{(q;q)_n}
=\exp\left(\sum_{k\ge1}\frac{(1+z^k)t^k}{k(1-q^k)}\right).\tag{2.3}
\]
For \(\omega\) of odd order \(d\), \(n=Ad+b\), and \(0\le b<d\),
\[
H_n(z;\omega)=(1+z^d)^AH_b(z;\omega).\tag{2.4}
\]

**Proof.** Equations (2.1) and (2.2) follow by substituting the coefficient formulas; (2.1) is also Lemma 4.1 of [LS87]. Put \(E(t)=\sum_{j\ge0}t^j/(q;q)_j\). Comparing coefficients gives \(E(qt)=(1-t)E(t)\), hence \(\log E(t)=\sum_{k\ge1}t^k/[k(1-q^k)]\). Multiplication of \(E(t)E(zt)\) gives (2.3).

For completeness, the finite binomial identity
\[
\prod_{j=0}^{n-1}(1+xq^j)=\sum_{k=0}^nq^{k(k-1)/2}{n\brack k}_qx^k
\]
follows by multiplying the last factor and using q-Pascal. At \(q=\omega\) its left side is
\((1+x^d)^A\prod_{j=0}^{b-1}(1+x\omega^j)\).
For \(k=ad+c\), \(0\le c<d\), coefficient comparison gives
\({Ad+b\brack ad+c}_\omega=\binom Aa{b\brack c}_\omega\): the difference of the exponents \(k(k-1)/2\) and \(c(c-1)/2\) is divisible by odd \(d\). Summing over \(a,c\) proves (2.4). This is the classical root-of-unity factorization, also [LS87, Lemma 4.5, equation (4.15)]. ∎

### Lemma 2.2 Hermite facts

One has
\[
\operatorname{He}'_A=A\operatorname{He}_{A-1},\qquad
\operatorname{He}''_A-y\operatorname{He}'_A+A\operatorname{He}_A=0,\qquad
\operatorname{Disc}(\operatorname{He}_A)=P_A.\tag{2.5}
\]
Over \(\mathbb R\), the roots are simple, real, and symmetric. Over a field of characteristic \(p>A\), consecutive Hermite polynomials and \(\operatorname{He}_A,\operatorname{He}'_A\) are coprime.

**Proof.** Differentiate the recurrence inductively for the first two identities. In characteristic zero, \(\operatorname{He}_A\) is the characteristic polynomial of the real symmetric tridiagonal matrix with zero diagonal and consecutive off-diagonal entries \(\sqrt1,\ldots,\sqrt{A-1}\). Each eigenspace has dimension at most one, since the first coordinate and the eigenvalue determine all coordinates recursively, and a zero first coordinate forces the vector to vanish. The spectral theorem gives real simple roots. Parity of the recurrence gives symmetry.

In characteristic \(p>A\), a common root of two consecutive polynomials descends along the recurrence, whose coefficients \(1,\ldots,A-1\) are nonzero, to \(\operatorname{He}_0=1\). The derivative identity then gives the stated coprimality. Finally the recurrence computes the consecutive resultants inductively; multiplying by \(A^A\) for the derivative identity and by the discriminant sign gives \(\operatorname{Disc}\operatorname{He}_A=\prod_{j=1}^A j^j\). More explicitly, if \(R_A=\operatorname{Res}(\operatorname{He}_A,\operatorname{He}_{A-1})\), evaluation at the roots of \(\operatorname{He}_{A-1}\) gives \(R_A=(-1)^{A-1}(A-1)^{A-1}R_{A-1}\); its sign cancels \((-1)^{A(A-1)/2}\). ∎

## 3 Local splitting at a fixed root of unity

Fix an odd integer \(d\ge3\), a primitive \(d\)-th root \(\omega\), and \(n=Ad+b\), where \(A\ge1\), \(0\le b<d\). Work formally in \(\varepsilon\) with
\[
q(\varepsilon)=\omega(1+\varepsilon^2)^{1/d},\qquad q(\varepsilon)^d-1=\varepsilon^2.
\]
The fractional power denotes its unique binomial series with constant term one. Put \(F(z)=z^d+1\), \(G(z)=H_b(z;\omega)\). All big-O statements in this section are formal coefficientwise orders; no convergence assertion is needed.

### Theorem 3.1 Separated clusters

If \(\operatorname{Disc}G\operatorname{Res}(F,G)\ne0\), then, for each \(\alpha^d=-1\),
\[
H_n(\alpha+\varepsilon x;q(\varepsilon))
=\varepsilon^A(-1)^Ad^{A/2}G(\alpha)
\operatorname{He}_A(\sqrt d\,x/\alpha)+O(\varepsilon^{A+1}).\tag{3.1}
\]
With \(K=dA(A-1)/2\),
\[
D_n(q(\varepsilon))=\varepsilon^{2K}(C_{\rm sep}+O(\varepsilon^2)),\tag{3.2}
\]
\[
C_{\rm sep}=(-1)^{A(d-1)/2}d^{dA(A+1)/2}P_A^d
\operatorname{Disc}G\operatorname{Res}(F,G)^{2A}.\tag{3.3}
\]
In particular \(\operatorname{ord}_{\Phi_d}D_n=K\).

**Proof.** In the logarithm of (2.3), separate terms with \(d\mid k\) from the others and put \(u=t^d\). At \(z=\alpha+\varepsilon x\), the singular part begins
\[
\frac{xu}{\alpha\varepsilon}-\frac{u^2}{2d\varepsilon^2}.
\]
For a term of \(u\)-degree \(l\), the pole order in \(\varepsilon\) is at most one for odd \(l\), at most two for even \(l\), and is strictly less than \(l\) for \(l\ge3\). Corrections at degrees one and two also have smaller pole order. Consequently the coefficient of \(u^a\) in the singular exponential has leading term
\[
\varepsilon^{-a}\frac{d^{-a/2}}{a!}
\operatorname{He}_a(\sqrt d\,x/\alpha).\tag{3.4}
\]
The remaining exponential is regular in \(\varepsilon\). Its \(t^b\) coefficient at zero is \(G(\alpha)/(\omega;\omega)_b\), because \(b<d\). To extract \(t^{Ad+b}\), its coefficients of degrees \(b+jd\), \(0\le j\le A\), are paired with \(u^{A-j}\); every \(j\ge1\) is lower order than \(j=0\) under the present nonvanishing hypothesis. Finally,
\[
(q(\varepsilon);q(\varepsilon))_n
=(-1)^AA!d^A(\omega;\omega)_b\varepsilon^{2A}(1+O(\varepsilon^2)).\tag{3.5}
\]
Here the multiples \(jd\) contribute \(-j\varepsilon^2\), each full block of nonmultiples contributes \(\prod_{j=1}^{d-1}(1-\omega^j)=d\), and the last block contributes \((\omega;\omega)_b\). Multiplication proves (3.1). Expressions involving \(\sqrt d\) are unchanged by its sign choice, and cancel coefficientwise after the indicated scaling.

The simple Hermite roots and formal implicit-function theorem now give \(A\) roots near each \(\alpha\), with first displacement \(\varepsilon\alpha h_j/\sqrt d\); the \(b\) residual roots remain simple and separated. These account for all \(n\) roots. Their squared differences within the \(d\) clusters contribute \(\varepsilon^{2K}d^{-K}P_A^d\), since the product of the powers of \(\alpha\) is one. Between clusters the factor is \((\operatorname{Disc}F)^{A^2}\); between cluster and residual roots it is \(\operatorname{Res}(F,G)^{2A}\), and between residual roots it is \(\operatorname{Disc}G\). Since \(\operatorname{Disc}F=(-1)^{(d-1)/2}d^d\), this is (3.3). The left side of (3.2) is even in \(\varepsilon\), so the normalized remainder starts at \(\varepsilon^2\). The change of variable \(q^d-1\) has a simple zero at \(\omega\); Galois conjugacy and irreducibility of \(\Phi_d\) turn the exact local order into the stated cyclotomic multiplicity. ∎

### Theorem 3.2 One simple shared root

Suppose \(b\) is odd, write \(G=(z+1)U\), and set
\[
g=U(-1),\qquad W=\frac{(\omega;\omega)_b}{(\omega^2;\omega^2)_{(b+d)/2}},
\qquad \tau=\frac{dW}{g},
\]
\[
J_{A+1}(y;\tau)=y\operatorname{He}_A(y)-\tau\operatorname{He}'_A(y)
=\operatorname{He}_{A+1}(y)+A(1-\tau)\operatorname{He}_{A-1}(y).
\]
Assume
\[
\operatorname{Disc}U\operatorname{Res}(F,U)\operatorname{Disc}J_{A+1}\ne0.\tag{3.6}
\]
The resultant assumption implies \(g\ne0\), and the denominator defining \(W\) is nonzero because \((b+d)/2<d\). Then
\[
H_n(-1+\varepsilon x;q(\varepsilon))
=\varepsilon^{A+1}(-1)^{A+1}d^{(A-1)/2}g
J_{A+1}(-\sqrt d\,x;\tau)+O(\varepsilon^{A+2}).\tag{3.7}
\]
With \(L=dA(A-1)/2+A\),
\[
D_n(q(\varepsilon))=\varepsilon^{2L}(C_{\rm ov}+O(\varepsilon^2)),\tag{3.8}
\]
\[
C_{\rm ov}=(-1)^{A(d-1)/2}d^{dA(A+1)/2+A}P_A^{d-1}
\operatorname{Disc}J_{A+1}\operatorname{Disc}U
\operatorname{Res}(F,U)^{2A}g^2.\tag{3.9}
\]
Thus \(\operatorname{ord}_{\Phi_d}D_n=L\).

**Proof.** Odd reciprocity in (2.2) gives \(G(-1)=0\). In the regular exponential used above, the \(t^b\) coefficient now has first term \(\varepsilon xg/(\omega;\omega)_b\). Its coefficient of degree \(b+d\), evaluated at \(z=-1\), is
\((\omega^2;\omega^2)_{(b+d)/2}^{-1}\): all odd powers vanish, and the first positive even multiple of odd \(d\) is \(2d>b+d\), so deleting the d-divisible logarithmic terms does not change this coefficient. The same q-exponential identity (2.3), with the variable \(t^2\), computes it. These two terms have the same leading order by (3.4); terms of degree \(b+jd\), \(j\ge2\), contribute later. Multiplying by (3.5), and using \(\operatorname{He}'_A=A\operatorname{He}_{A-1}\), gives (3.7).

There are \(A\) roots at each nonshared cluster and \(A+1\) at \(-1\). Their within-cluster factors are
\(\varepsilon^{2L}d^{-L}P_A^{d-1}\operatorname{Disc}J_{A+1}\).
Put \(F_0=F/(z+1)\). Then \(F_0(-1)=d\) and
\(\operatorname{Disc}F_0=(-1)^{(d-1)/2}d^{d-2}\).
The between-cluster factors are
\[
(\operatorname{Disc}F_0)^{A^2}d^{2A(A+1)}
=(-1)^{A(d-1)/2}d^{dA^2+2A}.
\]
The residual roots contribute
\(\operatorname{Disc}U\operatorname{Res}(F,U)^{2A}g^2\), the final \(g^2\) accounting for the extra root at the shared cluster. Combining these factors proves (3.9), and the evenness and exact-order arguments are as in Theorem 3.1. ∎

## 4 The Hermite parameter disk

### Theorem 4.1

For \(A\ge1\), let \(H=\operatorname{He}_A\) and \(J(y;\tau)=yH-\tau H'\) over \(\mathbb C\). If a nonreal \(\tau\) gives a multiple root of \(J\), then
\[
|1-\tau|^2>\frac{A+1}{A}.\tag{4.1}
\]
For real parameters, the only multiple-root cases are \(\tau=0\) when \(A\) is odd and \(\tau=-1/A\) when \(A\) is even. In particular \(J\) is squarefree if
\[
\tau\ne0,\qquad |1-\tau|\le\sqrt{(A+1)/A}.\tag{4.2}
\]

**Proof.** Pair opposite real roots of \(H\), put \(z=y^2\), and write
\[
f(z)=\frac{H'(y)}{yH(y)}=\sum_j\frac{w_j}{z-a_j}.
\]
The \(a_j\) are the squares of positive Hermite roots with weights two, and there is additionally \(a_j=0\) with weight one for odd \(A\). All weights are positive. At a nonzero multiple root for \(\tau\ne0\), coprimality gives \(H(y)\ne0\), and
\(f(z)=1/\tau\), \(f'(z)=0\). Using the Hermite differential equation in \(J'=0\) gives
\[
1+A\tau+(1-\tau)z/\tau=0.
\]
The value \(\tau=1\) is impossible; with \(\sigma=1-\tau\), this becomes
\[
z=(2A+1)-A\sigma-(A+1)/\sigma.\tag{4.3}
\]
Taking imaginary parts in the partial fractions gives
\[
\operatorname{Im}z\sum_j\frac{w_j}{|z-a_j|^2}
=\frac{\operatorname{Im}\tau}{|\tau|^2}.
\]
For nonreal \(\tau\), \(\operatorname{Im}z\) has the sign opposite to \(\operatorname{Im}\sigma\). But (4.3) gives
\(\operatorname{Im}z=\operatorname{Im}\sigma((A+1)/|\sigma|^2-A)\), proving (4.1).

For real nonzero \(\tau\), the same identity forces \(z\) real, whereas \(f'(z)=-\sum_jw_j/(z-a_j)^2<0\), a contradiction. It remains to check zero. For odd \(A\), \(H'(0)\ne0\), so zero is a root of \(J\) only for \(\tau=0\), when \(yH\) has a double zero. For even \(A\), \(H(0)\ne0\) and \(J'(0)=(1+A\tau)H(0)\), giving exactly \(\tau=-1/A\); parity makes that zero multiple. At \(\tau=0\) and even \(A\), \(yH\) is squarefree. Finally \(|1+1/A|>\sqrt{(A+1)/A}\), which proves (4.2). ∎

## 5 Half residual degree and resonance

### Lemma 5.1 Integral inverse identity

Let \(d=4r+3\), \(b=2r+1=(d-1)/2\), and \(\omega\) primitive of order \(d\). Define
\[
U=H_b(z;\omega)/(z+1),\quad g=U(-1),\quad
v=(\omega^2;\omega^2)_r(\omega;\omega^2)_b.
\]
Then \(v=dW\) for the \(W\) in Theorem 3.2, and
\[
gv^\iota+g^\iota v=vv^\iota.\tag{5.1}
\]
Moreover \(g\ne0\), \(2g-v\ne0\) at every primitive root in characteristic zero, and
\[
\tau=v/g\ne0,\qquad |1-\tau|=1.\tag{5.2}
\]

**Proof.** Put \(Q=\omega^2\), \(a_j=(\omega;Q)_j/(Q;Q)_j\), and \(M=(\omega;Q)_b\). Cancellation against \(\prod_{k=1}^{d-1}(1-\omega^k)=d\) gives \(dW=(Q;Q)_rM\).

For additional detail on \(g\), (2.1) at \(-1\) gives
\(H_{2j}(-1;q)=(q;q^2)_j\) and \(H_{2j+1}(-1;q)=0\).
Differentiating (2.1), with \(g_j=H'_{2j+1}(-1;q)\), gives
\(g_j=(q;q^2)_j+(1-q^{2j})g_{j-1}\), \(g_0=1\).
Hence
\[
g=(Q;Q)_r\sum_{j=0}^r a_j.\tag{5.3}
\]
Because \(\omega=Q^{-b}\), the finite q-binomial theorem proves
\(\sum_{j=0}^b a_j=M\): explicitly
\(a_j=(-1)^jQ^{-bj+j(j-1)/2}{b\brack j}_Q\).
Direct cancellation also gives
\(a_j^\iota=\omega^j a_j\) and
\(a_{b-j}=(M/M^\iota)a_j^\iota\).
Splitting the sum at \(r\) thus gives
\[
\frac{\sum_{j=0}^r a_j}{M}+
\frac{\sum_{j=0}^r a_j^\iota}{M^\iota}=1.
\]
Equations (5.3) and \(v=(Q;Q)_rM\) prove (5.1). All displayed products have exponents strictly between zero and \(d\), so the cancellations are legal.

To prove the asserted nonvanishing without presupposing squarefreeness, take \(\omega=e^{2\pi i/d}\). Every quotient
\[
\frac{1-\omega^{2k+1}}{1-\omega^{2k+2}}
=e^{-\pi i/d}\frac{\sin((2k+1)\pi/d)}{\sin((2k+2)\pi/d)}
\]
in \(a_j\), \(j\le r\), has positive sine ratio. Thus \(a_j\) has argument \(-j\pi/d\). The product \(M\) has argument \(-b\pi/(2d)\), since summing its factor arguments gives \(-b\pi/2+\pi b^2/d\). Every summand of \(g/v=\sum_{j=0}^r a_j/M\) therefore has argument
\[
(b/2-j)\pi/d\in[\pi/(2d),b\pi/(2d)]\subset(0,\pi/4).
\]
Its real and imaginary parts are strictly positive. In particular \(g/v\) is neither zero nor \(1/2\). Galois conjugacy proves \(g\ne0\) and \(2g-v\ne0\) at every embedding. At any such embedding, \(\iota\) is complex conjugation, and (5.1) says \(1/\tau+1/\overline\tau=1\), equivalent to (5.2). ∎

### Theorem 5.2 Uniform half-order resonance

Let \(N=2m+1\ge3\), \(q\) any primitive \(N\)-th root in characteristic zero, and \(T_m(z)=(-1)^mH_m(-z;q)\). Then the monic gcd is
\[
\gcd(T_m,z^N-1)=
\begin{cases}1,&m\text{ even},\\z-1,&m\text{ odd}.
\end{cases}\tag{5.4}
\]
When \(m\) is odd, \(1\) is a simple root of \(T_m\). Equivalently, for \(N\equiv3\pmod4\), \(-1\) is a simple root of \(H_m\) and
\(\operatorname{Res}(z^N+1,H_m/(z+1))\ne0\).

**Proof.** First take \(q=e^{2\pi i/N}\). Define \(S_0=1\), \(S_1=x\),
\(S_n=xS_{n-1}-(1-q^{n-1})S_{n-2}\). The recurrence proves, for nonzero \(z\),
\[
T_n(z)=(i\sqrt z)^nS_n((z-1)/(i\sqrt z)).\tag{5.5}
\]
For \(|z|=1\), the argument of \(S_n\) is real, with either square-root choice. The polynomial \(S_m\) is the characteristic polynomial of a symmetric tridiagonal matrix \(J\) whose edge \(j\) is
\[
c_j=\sqrt{2\sin(\pi j/N)}\exp(i[-\pi/4+\pi j/(2N)]),\quad1\le j<m.
\]
Write \(J=DRD\), where \(R\) is the real symmetric zero-diagonal tridiagonal matrix with the positive moduli of these edges, and
\[
D_{jj}=e^{i\theta_j},\qquad \theta_j=-\pi/8+\pi(2j+1)/(8N),\quad0\le j<m.
\]
Indeed \(\theta_{j-1}+\theta_j\) is the phase of \(c_j\). All \(\theta_j\) lie strictly between \(-\pi/8\) and zero. Therefore \(B=D^{-2}\) has strictly positive real and imaginary parts as Hermitian diagonal matrices.

If a nonzero real \(t\) were an eigenvalue of \(J\), a nonzero vector \(v\) would satisfy \(Rv=tBv\). Multiplication by \(v^*\) gives a real left side and a nonzero imaginary part \(t v^*\operatorname{Im}(B)v\) on the right, a contradiction. Thus zero is the only possible real root of \(S_m\).

For even \(m\), the tridiagonal determinant at zero is a nonzero signed product of alternate squared edges, so zero is not a root. For odd \(m\), the elementary row recurrence shows \(R\) has a one-dimensional kernel with a real vector \(v_0\). In an orthonormal basis beginning with \(v_0/\|v_0\|\), the complementary block of \(R\) is invertible. The coefficient of \(t\) in \(\det(R-tB)\) is a nonzero real factor times \(v_0^TBv_0\), which is nonzero since its real part is positive. Thus zero is a simple root. Equation (5.5), whose argument has nonzero derivative at \(z=1\), proves the asserted unit-circle conclusion in this principal embedding. In particular it proves (5.4). Field automorphisms \(q\mapsto q^a\) carry the polynomial gcd to the gcd at any primitive root. This last step asserts the algebraic resonance conclusion, not preservation of absolute values of arbitrary roots under Galois automorphisms. ∎

### Corollary 5.3 Guard removal at half residual degree

For \(d\equiv3\pmod4\), \(b=(d-1)/2\), the conclusions of Theorem 3.2 hold for every \(A\ge1\) whenever \(H_b(z;\omega)\) is squarefree. There is no remaining quasi-Hermite or resonance guard.

**Proof.** Theorem 5.2 gives the simple root \(-1\) and the residual resultant. Squarefreeness gives \(\operatorname{Disc}U\ne0\). Lemma 5.1 puts \(\tau\ne0\) on \(|1-\tau|=1\), so Theorem 4.1 gives \(\operatorname{Disc}J_{A+1}\ne0\) for every \(A\). ∎

### Proposition 5.4 Prime-order squarefreeness

If \(\ell\) is prime and \(0\le n<\ell\), then \(H_n(z;\zeta_\ell)\) is squarefree. Consequently Corollary 5.3 is unconditional for every prime lower order \(d\equiv3\pmod4\).

**Proof.** Put \(T_n=(-1)^nH_n(-z;q)\), \(q=1+\varepsilon^2\), \(z=1+\varepsilon x\). Its recurrence shows that
\(\varepsilon^{-n}T_n(1+\varepsilon x;1+\varepsilon^2)\) is a monic polynomial over \(\mathbb Z[\varepsilon]\), specializing to \(\operatorname{He}_n(x)\). Discriminant scaling gives
\[
D_n(q)=(q-1)^{n(n-1)/2}E_n(q),\qquad E_n\in\mathbb Z[q],\quad E_n(1)=P_n.
\]
If \(D_n(\zeta_\ell)=0\), then \(\Phi_\ell\mid E_n\) in \(\mathbb Z[q]\); evaluating at one gives \(\ell\mid P_n\), impossible for \(n<\ell\). Reflection and multiplication making \(T_n\) monic do not change the discriminant. ∎

## 6 The complete finite-characteristic inverse pairing

### Theorem 6.1

Let \(p\) be an odd prime, \(A=(p-1)/2\), and \(k\) a field of characteristic \(p\). For \(\tau,\tau'\in k^\times\) satisfying
\[
1/\tau+1/\tau'=1,
\]
at least one of \(J(y;\tau)=y\operatorname{He}_A-\tau\operatorname{He}'_A\) and \(J(y;\tau')\) is squarefree over the algebraic closure, except exactly when
\[
p\equiv1\pmod4,\qquad \tau=\tau'=2.\tag{6.1}
\]
In (6.1), both have a root of multiplicity exactly three at zero.

**Proof.** Write \(H=\operatorname{He}_A\). Lemma 2.2 gives \(\gcd(H,H')=1\); at a root of \(J\), \(H\ne0\). The parameter relation implies \(\tau\ne1\) and \(\tau'=\tau/(\tau-1)\). The Hermite equation gives, at any root of \(J\),
\[
J'=[1+A\tau+(1-\tau)y^2/\tau]H.
\]
Since \(A=-1/2\) in \(k\), a multiple root must satisfy
\[
y^2=t(\tau)=\frac{\tau(\tau-2)}{2(1-\tau)},\qquad t(\tau')=-t(\tau).\tag{6.2}
\]
Suppose both polynomials have a multiple root and the first has a nonzero one \(y\). Choose \(i^2=-1\) in the algebraic closure and put \(V(y)=i^{-A}H(iy)\). The multiple-root locations for the second have square \(-y^2\); by parity they include \(iy\). Both \(H(y)\) and \(V(y)\) are nonzero.

Differentiating, using the equations for \(H\) and \(V\), gives
\[
[H'V-HV'-yHV]'=-(2A+1)HV=0.
\]
The bracket is an odd polynomial of degree \(p\) with leading coefficient \(-1\). In characteristic \(p\), a derivative-zero polynomial of degree at most \(p\) has only a constant and a \(y^p\) term. Hence
\[
H'V-HV'-yHV=-y^p.\tag{6.3}
\]
At the two alleged roots, \(H'/H=y/\tau\) and \(V'/V=-y/\tau'\). Dividing the left side of (6.3) by \(HV\) gives zero, but the right side is nonzero. This is impossible.

Simultaneous failure therefore requires a multiple root at zero. Equation (6.2) forces \(\tau=\tau'=2\). If \(A\) is odd, \(H'(0)\ne0\) and \(J(0;2)\ne0\), so no failure occurs. If \(A\) is even, \(H(0)=c_0\ne0\), and \(J\) is odd with \(J'(0;2)=(1+2A)c_0=0\). From the differential equation, \(c_2=-Ac_0/2\), \(c_4=A(A-2)c_0/24\). The cubic coefficient of \(yH-2H'\) is \(A(1-2A)c_0/6=-c_0/6\ne0\). Here \(p\equiv1\pmod4\) implies \(p\ge5\), so the denominators are units; the formula also covers \(A=2\) with \(c_4=0\). Thus the multiplicity is exactly three. ∎

The Wronskian identity (6.3) is proved here for this application. It belongs to established Hermite-Wronskian congruence theory; no claim that the general mechanism originates here is intended. Most importantly, a characteristic-zero disk bound cannot replace Theorem 6.1 after reduction modulo \(p\).

## 7 Exact cyclotomic division and the arithmetic bridges

For \(s=4r+3\), \(b=(s-1)/2\), define in \(\mathcal O_s\)
\[
U_s=H_b(z;\omega)/(z+1),\quad g_s=U_s(-1),\quad
v_s=(\omega^2;\omega^2)_r(\omega;\omega^2)_b,
\]
\[
\Gamma_s=\operatorname{Disc}U_s\operatorname{Res}(z^s+1,U_s),\quad
\delta_s=2g_s-v_s,\quad B_s=\Gamma_s\Gamma_s^\iota\delta_s,
\quad c_s^+=\operatorname{cont}_s(B_s).\tag{7.1}
\]
The factor \(z+1\) divides \(H_b\) over \(\mathbb Z[q,z]\), so these definitions are integral. The integral identity (5.1) survives every reduction.

### Lemma 7.1 Same-component selection and cyclotomic reduction

If \(p\nmid s\), then \(\mathcal O_s/p\mathcal O_s\) is a product of finite fields, one for each irreducible factor of \(\Phi_s\bmod p\). An element has content not divisible by \(p\) if and only if its image is nonzero in at least one factor. For a product, this means that all its factors are nonzero in that same field. Moreover,
\[
\Phi_{sp}(q)\equiv\Phi_s(q)^{p-1}\pmod p\qquad(p\nmid s).\tag{7.2}
\]
At a primitive lower root, \(Q_s(\omega)\), where \(Q_s=(q^s-1)/\Phi_s\), is a unit in every residue field over such \(p\).

**Proof.** The derivative \(sq^{s-1}\) is relatively prime to \(q^s-1\bmod p\). Its cyclotomic factors are consequently squarefree and pairwise coprime there. The Chinese remainder theorem gives the first assertion, and the coefficient definition of content gives the equivalence. The elementary identity \(\Phi_{sp}(q)=\Phi_s(q^p)/\Phi_s(q)\) for \(p\nmid s\), reduced in characteristic \(p\), gives (7.2). The coprimality of the cyclotomic factors makes \(Q_s\) nonzero at every root of \(\Phi_s\bmod p\). ∎

### Theorem 7.2 Augmented overlap bridge

If \(s\equiv3\pmod4\), \(p\equiv1\pmod4\) is prime, \(p\nmid s\), and
\[
c_s^+\ne0,\qquad p\nmid c_s^+,
\]
then \(H_{(sp-1)/2}(z;\zeta_{sp})\) is squarefree in characteristic zero for every primitive \(\zeta_{sp}\).

**Proof.** Lemma 7.1 selects a field factor and primitive lower root \(\bar\omega\) in which
\(\Gamma_s(\bar\omega)\Gamma_s(\bar\omega^{-1})\delta_s(\bar\omega)\ne0\).
Both inverse residual discriminants and resultants are therefore nonzero in this one component. The resultants include \(U_s(-1)=g_s\), so \(g_s\) and its inverse counterpart are units. Every factor of \(v_s\) and its counterpart is also a unit, since all its exponents are strictly between zero and \(s\). The reduction of (5.1) gives the inverse parameter relation. Nonzero \(\delta_s\) rules out \(\tau=2\), hence also \(\tau'=2\). Theorem 6.1 chooses one of \(\bar\omega,\bar\omega^{-1}\) for which \(\operatorname{Disc}J\ne0\).

Set \(A=(p-1)/2\), \(b=(s-1)/2\), and \(n=As+b=(sp-1)/2\). At the chosen reduction every factor of the overlap coefficient (3.9) is a unit: \(p\nmid s\), \(A<p\) makes \(P_A\) a unit, and the other factors were just selected. Rational expressions in \(\tau=v_s/g_s\) are interpreted in the localization at this component, where their denominators are units. This nonvanishing also establishes the characteristic-zero guards of Theorem 3.2 at the corresponding embedding.

With \(L=sA(A-1)/2+A\), exact order and monic division give
\[
D_n(q)=\Phi_s(q)^L E(q),\qquad E\in\mathbb Z[q],
\]
\[
E(\omega)=Q_s(\omega)^L C_{\rm ov}.\tag{7.3}
\]
Indeed \(q^s-1=\Phi_sQ_s\), and comparison of the exact leading terms gives (7.3). The quotient is integral by repeated division by the monic polynomial \(\Phi_s\); all primitive lower embeddings have the same exact order by Galois conjugacy. The right side of (7.3) is nonzero in the chosen residue field by Lemma 7.1.

If \(D_n(\zeta_{sp})=0\), irreducibility would give \(\Phi_{sp}\mid D_n\), hence \(\Phi_{sp}\mid E\) since \(\Phi_{sp}\ne\Phi_s\). Reducing (7.2) would force \(E\) to vanish in every lower residue field, contradicting (7.3). Galois conjugacy covers every primitive \(\zeta_{sp}\). No inequality such as \(L<p-1\) was used; cyclotomic division occurred before reduction. ∎

### Corollary 7.3 The other parity

For \(p\equiv3\pmod4\), \(p\nmid s\), replace the augmented content by
\(\operatorname{cont}_s(\Gamma_s\Gamma_s^\iota)\). If this content is nonzero and not divisible by \(p\), the same squarefreeness conclusion holds.

**Proof.** In this parity Theorem 6.1 has no exceptional pair, so \(\delta_s\) is unnecessary. Every other step of Theorem 7.2 is unchanged. ∎

### Proposition 7.4 Separated bridge

Let \(s\) be odd, \(b=(s-1)/2\), \(G=H_b(z;\omega)\), and
\(c_s=\operatorname{cont}_s(\operatorname{Disc}G\operatorname{Res}(z^s+1,G))\).
If \(p\) is odd, \(p\nmid s\), and \(c_s\ne0\), \(p\nmid c_s\), then \(H_{(sp-1)/2}(z;\zeta_{sp})\) is squarefree.

**Proof.** Choose the same-component nonvanishing of the two lower factors by Lemma 7.1. Use Theorem 3.1 with \(A=(p-1)/2\), whose coefficient is a unit at this component. The exact factorization has exponent \(K=sA(A-1)/2\), and the quotient value is \(Q_s(\omega)^K C_{\rm sep}\). The contradiction using (7.2) is identical to (7.3). In practice the hypothesis excludes \(s\equiv3\pmod4\), since then \(-1\) is shared. ∎

## 8 Reciprocal reduction and finite certification

If \(s=4r+3\), reciprocity makes \(U_s\) monic reciprocal of degree \(2r\). Hence there is a unique monic polynomial \(P_s(t)\) of degree \(r\) with
\[
U_s(z)=z^rP_s(z+z^{-1}).\tag{8.1}
\]
This follows, for example, from the basis \(S_0=2\), \(S_1=t\), \(S_{j+1}=tS_j-S_{j-1}\), for which \(S_j(z+z^{-1})=z^j+z^{-j}\). If \(U=\sum_{k=0}^{2r}u_kz^k\), then
\(P=u_r+\sum_{j=1}^ru_{r+j}S_j\).

For odd \(s\), define \(C_1=1\), \(C_3=t-1\), and \(C_{s+2}=tC_s-C_{s-2}\). These recurrences give
\[
z^s+1=(z+1)z^{(s-1)/2}C_s(z+z^{-1}),\qquad
S_s(t)+2=(t+2)C_s(t)^2.\tag{8.2}
\]

### Lemma 8.1 Exact reduced-degree formulas

For \(U=z^rP(z+z^{-1})\),
\[
\operatorname{Disc}U=P(2)P(-2)(\operatorname{Disc}P)^2,\tag{8.3}
\]
\[
\operatorname{Res}(z^s+1,U)=(-1)^rP(-2)\operatorname{Res}(P,C_s)^2.\tag{8.4}
\]
Consequently
\[
\Gamma_s=(-1)^rP_s(2)P_s(-2)^2
[\operatorname{Disc}P_s\operatorname{Res}(P_s,C_s)]^2.\tag{8.5}
\]

**Proof.** First take generic distinct roots \(t_i\) of \(P\), and the reciprocal pair \(\lambda_i,\lambda_i^{-1}\) above each \(t_i\). Within a pair the squared difference is \(t_i^2-4\). The resultant of two quadratics \(z^2-t_i z+1\), \(z^2-t_jz+1\) is \((t_i-t_j)^2\), so the cross-pair discriminant contribution is \((t_i-t_j)^4\). This proves (8.3). For the resultant the paired contribution is
\((1+\lambda_i^s)(1+\lambda_i^{-s})=S_s(t_i)+2=(t_i+2)C_s(t_i)^2\).
Taking the product proves (8.4), including \(\operatorname{Res}(P,t+2)=(-1)^rP(-2)\). Resultant interchange has positive sign since \(\deg U=2r\). All expressions are integral polynomial identities in the coefficients, so they hold under every specialization, including coincident roots. ∎

Appendix A supplies \(P_s\), \(\delta_s\), the complete normalized augmented remainders, and gcd witnesses for all five bases. They prove
\[
\begin{array}{c|ccccc}
s&3&7&11&15&19\\\hline
c_s^+&1&7^2&11^5&3^{12}5^9&19^{11}.
\end{array}\tag{8.6}
\]
These are finite exact computations in degrees \(r=0,1,2,3,4\), inserted into an all-prime theorem. They are not a finite target-order census. The complete unreduced-in-z coefficient records are also distributed as JSON for checking, but the mathematical reconstruction and all final coordinate data needed for (8.6) appear in the appendix.

## 9 The five infinite families and their local consequences

### Theorem 9.1 Main family theorem

Let \(s\in\{3,7,11,15,19\}\), and let \(p\equiv1\pmod4\) be prime with \(p\nmid s\). Put \(d=sp\). Then, for every primitive \(d\)-th root \(\zeta_d\),
\[
H_{(d-1)/2}(z;\zeta_d)\text{ is squarefree}.\tag{9.1}
\]
In particular \(-1\) is a simple root. For \(s=15\) the exclusion is \(p=5\); for the other four bases the condition \(p\nmid s\) is automatic in this prime congruence class.

**Proof.** The contents (8.6) are nonzero and have prime divisors only among the divisors of \(s\). Thus \(p\nmid c_s^+\), and Theorem 7.2 proves (9.1). Since \(d\equiv3\pmod4\), Theorem 5.2 gives the assertion at \(-1\). ∎

### Corollary 9.2 Complete overlap expansion for every local index

For every \(d\) in Theorem 9.1, every primitive \(\omega\) of order \(d\), and every integer \(A\ge1\), set \(b=(d-1)/2\), \(n=Ad+b\). Then (3.7)–(3.9) hold with nonzero coefficient and
\[
\operatorname{ord}_{\Phi_d}D_n=\frac{dA(A-1)}2+A.
\]

**Proof.** Theorem 9.1 supplies squarefreeness; Corollary 5.3 removes all the other guards. ∎

The excluded order \(d=75\) is not declared a counterexample. It is outside this bridge because \(p=5\) divides the lower base \(s=15\). The proof says nothing adverse about its characteristic-zero polynomial.

## 10 A fully scoped scalar resolvent application

This section is included to make the practical consequence and its limitation explicit. Work over \(\mathbb C\). Fix \(N=2m+1\), a natural \(N\)-cycle matrix \(P\), a primitive root \(q\), and \(h=m+1\). Put \(f_k=q^{hk^2}\) and \(C=\sum_{k=0}^{N-1}f_kP^k\). The grammar allows only
\[
C=\delta I+\sum_{j=1}^{Q}a_j(I-\lambda_jP)^{-1},\quad
 a_j\lambda_j\ne0,\quad\lambda_j^N\ne1,\tag{10.1}
\]
with scalar algebraic coefficients. Branch-dependent endpoints, different cycles, higher-order resolvents, and arbitrary matrix inverses are outside this statement.

### Proposition 10.1 Exact criterion and the odd-parity minimum

In (10.1), \(Q\ge m\). Equality holds exactly when
\(T_m(z)=(-1)^mH_m(-z;q)\) is squarefree and has no root among the \(N\)-th roots of unity. It never has zero as a root. A legal representation with \(m+1\) branches exists for every odd \(N\), even with \(\delta=0\). Thus for every \(N\equiv3\pmod4\), in particular every order in Theorem 9.1,
\[
Q_{\min}=m+1.
\]
Without a free scalar diagonal, \(Q_{\min}=m+1\) for every odd \(N\).

**Proof.** The resolvent identity gives moments \(f_k=\sum_j b_j\lambda_j^k\), with \(b_j=a_j/(1-\lambda_j^N)\), for \(1\le k\le2m\); at zero the diagonal may intervene. The shifted Hankel matrix \([f_{i+j+1}]_{0\le i,j<m}\) has rank \(m\): each entry factors as
\(f_1[f_iq^i][f_jq^j]q^{ij}\), and \([q^{ij}]\) is a Vandermonde matrix at distinct nodes. Thus \(Q\ge m\).

The unique monic shifted annihilator has coefficients \((-1)^{m-j}{m\brack j}_q\). To check this directly, use
\(f_{k+j+1}/f_{k+1}=q^{j(j-1)/2+(h+k+1)j}\).
The q-binomial theorem makes the annihilation sum, for \(0\le k<m\), equal to
\((-1)^m\prod_{l=0}^{m-1}(1-q^{h+k+1+l})=0\), since the interval contains \(N\). This proves the formula for \(T_m\) and also follows from [LS87, Theorem 3.2]. Its constant term is \((-1)^m\). Any m-node representation must have these distinct nodes as its annihilator roots, so the guards are necessary. Conversely, if the guards pass, solve the Vandermonde system for \(b_j\lambda_j\) on the first m shifted moments. The annihilator recurrence supplies the next m. All weights are nonzero by rank; the zero moment determines \(\delta\). Thus the guards suffice.

Here is a proof of the universal upper bound that does not assume a missing genericity theorem. Extend \(f_k\) by the same formula for all \(k\ge0\), and define the linear functional \(\mathcal L(z^k)=f_k\). Every leading Hankel determinant \(\Delta_j=\det[f_{a+b}]_{0\le a,b<j}\), \(j\le m+1\), is nonzero, by the same Vandermonde factorization at \(1,q,\ldots,q^{j-1}\). There are therefore monic orthogonal polynomials \(P_j\) through degree \(m+1\), characterized by \(\mathcal L(z^kP_j)=0\), \(k<j\). Linear algebra gives their squared norms \(\Delta_{j+1}/\Delta_j\) for \(j\le m\). Expanding \(zP_j\) in this orthogonal basis gives
\(P_{j+1}=(z-\alpha_j)P_j-\beta_jP_{j-1}\), with
\(\beta_j=\Delta_{j+1}\Delta_{j-1}/\Delta_j^2\ne0\).
Indeed terms below \(P_{j-1}\) vanish by orthogonality and symmetry of \(\mathcal L(ab)\). Thus consecutive \(P_{m+1},P_m\) are coprime, by descending the recurrence.

The monic pencil \(Q_t=P_{m+1}+tP_m\) is orthogonal to \(1,z,\ldots,z^{m-1}\). There are only finitely many values of \(t\) giving a root in the finite forbidden set \(\{0\}\cup\{\lambda:\lambda^N=1\}\), since its two constituent polynomials are coprime. There are also only finitely many \(t\) giving a repeated root: away from zeros of \(P_m\), such a root is a critical point of the nonconstant rational function \(-P_{m+1}/P_m\), whose derivative is nonzero in characteristic zero and has finitely many zeros. A zero of \(P_m\) cannot be a root of \(Q_t\). Choose an integer \(t\) avoiding these finite sets. Its \(m+1\) distinct legal roots give weights from moments \(0,\ldots,m\); orthogonality to \(1,\ldots,z^{m-1}\) and the monic recurrence then give all moments through \(2m\). None of the weights is zero, since the full Hankel matrix of size \(m+1\) has rank \(m+1\). This is (10.1) with \(\delta=0\).

The same full Hankel rank is the lower bound without a diagonal. With a diagonal and odd \(m\), Theorem 5.2 forces the forbidden node one in the unique m-node annihilator, so \(m\) branches are impossible and \(m+1\) is exact. ∎

This application explains why squarefreeness in the five new \(3\bmod4\) families is mathematically useful for the local theorem yet does not improve their scalar-bank minimum. Branch count alone makes no claim about an FFT speedup, numerical stability, or unrestricted Green-function complexity.

## 11 Boundary controls and unresolved statements

First, the exceptional parameter in Theorem 6.1 occurs in an actual lower-base reduction. At \(s=7,p=13\),
\[
\Phi_7=(q^2+3q+1)(q^2+5q+1)(q^2+6q+1)\quad\text{over }\mathbb F_{13}.
\]
The coefficient data in Appendix A give
\(\gcd(\Phi_7,\Gamma_7\Gamma_7^\iota)=1\) and
\(\gcd(\Phi_7,\delta_7)=q^2+6q+1\).
In the last, inverse-stable component, \(\tau=\tau'=2\) and
\(J(y;2)=y^7+12y^5+9y^3\), which has a triple root at zero. The other components suffice for the theorem. In particular a good residual discriminant alone cannot remove the augmented factor. Although \(\operatorname{Norm}(\delta_7)=1183=7\cdot13^2\), \(c_7^+=49\) is not divisible by 13. Requiring all components to be units would be unnecessarily strong.

Second, unreduced coefficient contents are wrong for this purpose. For the canonical factors of Appendix A, taking the gcd of the unreduced product of the three canonical factors gives \(11^4\), \(3^{12}5^8\), and \(19^{10}\) at \(s=11,15,19\); after reduction the correct values are \(11^5\), \(3^{12}5^9\), and \(19^{11}\).

The following problems remain open in this note:

1. For arbitrary \(s\equiv3\pmod4\), prove characteristic-zero squarefreeness of \(H_{(s-1)/2}(z;\zeta_s)\). The resonance theorem resolves only the shared-root question, not all repeated reciprocal pairs.
2. Assuming \(\Gamma_s\ne0\), prove that every prime \(p\equiv1\pmod4\), \(p\nmid s\), fails to divide \(\operatorname{cont}_s(\Gamma_s\Gamma_s^\iota\delta_s)\). The sector proof shows \(\delta_s\ne0\) in characteristic zero but does not prove this simultaneous finite-characteristic support assertion. The five constants do not imply a general theorem.
3. Replace the unramified bridge when \(p\mid s\), or handle a target \(sp^a\) uniformly for \(a\ge2\). The lower algebra can then be nonreduced; \(Q_s\) need not be a unit, and the index \((p^a-1)/2\) reaches \(p\), making \(P_A\) divisible by \(p\). Neither the current unit argument nor the pairing proof covers this case.
4. Complete the exact literature comparison. An absent formula in one inspected paper is not a proof of worldwide novelty.

No q-shift argument bypasses these issues. For example \(H_2(z;-3)=(z-1)^2\) has a repeated ordinary root even though its q-shift has no root in common with it. Complex formal orthogonality also supplies no positivity argument for simple roots; see the explicit warning in [SZ97].

## 12 Attribution and bibliography

The recurrence and reciprocity are [LS87, Lemma 4.1, equations (4.1)–(4.5), p. 343]; the static root-of-unity factorization is [LS87, Lemma 4.5, equation (4.15), p. 346]. The chirp determinant and Padé denominator are [LS87, Theorem 3.2, equations (3.11)–(3.12), p. 340; proofs pp. 354–355]. Its notation \(G_n\) is our \(H_n\), and its determinant \(D(M/n)\) is not our ordinary discriminant \(D_n\). These distinctions prevent false priority comparisons. The paper itself credits earlier Padé work; it is cited as a directly inspected classical record, not asserted to be the first source of every ingredient.

The supplied LS87 scan includes the complete mathematical body, journal pp. 331–359, and reference page 361; reference page 360 is missing. The comparison therefore closes mathematical-body access for this paper, not its entire bibliography chain. The draft's fixed-root moving-zero coefficients, ordinary-discriminant coefficients, and simultaneous residue-component bridge are separate scoped statements whose proofs have been supplied here. Their publication priority remains unclaimed, pending Z97 and broader chaining.

- **[LS87]** D. S. Lubinsky and E. B. Saff, “Convergence of Padé approximants of partial theta functions and the Rogers–Szegő polynomials,” *Constructive Approximation* **3** (1987), 331–361. https://doi.org/10.1007/BF01890574. Primary mathematical body inspected in the supplied scan; precise formula locations listed above.
- **[Z97]** A. S. Zhedanov, “Gauss sums and orthogonal polynomials,” *International Journal of Modern Physics A* **12** (1997), 289–294. https://doi.org/10.1142/S0217751X97000438. Bibliographic comparison target; full-text comparison remains pending and this paper is not used as an unverified proof dependency.
- **[SZ97]** V. P. Spiridonov and A. S. Zhedanov, “Zeros and orthogonality of the Askey–Wilson polynomials for q a root of unity,” *Duke Mathematical Journal* **89** (1997), 283–305; arXiv:q-alg/9605034, version 2. https://arxiv.org/abs/q-alg/9605034. Primary background on root-of-unity limits and the distinction between positive and complex recurrence data; no half-order simplicity theorem is inferred from terminal-degree formulas.
- **[C16]** J. Cigler, “Elementary observations on Rogers–Szegő polynomials,” arXiv:1602.07850. https://arxiv.org/abs/1602.07850. Background on special values and q-products; all particular identities needed here are proved in Sections 2 and 5.
- **[SU18]** M. Sawa and Y. Uchida, “Discriminants of classical quasi-orthogonal polynomials, with combinatorial and number-theoretic applications,” arXiv:1802.00605, version 1, Theorem 4.8. https://arxiv.org/abs/1802.00605. Adjacent quasi-Laguerre discriminants are established background; the parity substitution for the quasi-Hermite polynomial is not claimed as a new general discriminant theory.
- **[GG20]** C. Grosu and C. Grosu, “The irreducibility of some Wronskian Hermite polynomials,” arXiv:2007.00065, version 1, Theorem 8. https://arxiv.org/abs/2007.00065. Background for established Hermite-Wronskian congruence methods; the specialized identity used here is independently proved in (6.3).

## Appendix A Finite exact certificates

All vectors below list coefficients in ascending powers of \(q\), reduced modulo \(\Phi_s(q)\); omitted trailing entries are zero. For the four prime bases, \(\Phi_s=1+q+\cdots+q^{s-1}\). For \(s=15\),
\[
\Phi_{15}=q^8-q^7+q^5-q^4+q^3-q+1.
\]
Write \(P_s(t)=\sum_{j=0}^r p_{s,j}(q)t^j\), with monic top coefficient one. The listed \(P_s\) are obtained directly from q-Pascal, division of \(H_b\) by \(z+1\), and (8.1). Let \(a_s\) be the listed vector satisfying
\[
\operatorname{rem}_{\Phi_s}(\Gamma_s\Gamma_s^\iota\delta_s)=c_s^+\sum_ja_{s,j}q^j.\tag{A.1}
\]
For each base a listed integer vector \(w_s\) satisfies \(\sum_jw_{s,j}a_{s,j}=1\). Thus the coordinates on the right of (A.1) have gcd exactly \(c_s^+\), not merely a common divisor.

There is a finite determinant recipe for checking (A.1) without any project software. In the free rank-r algebra \(R[t]/P_s(t)\), \(R=\mathbb Z[q]/\Phi_s(q)\), the determinant of multiplication by a polynomial \(B(t)\) is \(\operatorname{Res}(P_s,B)\). Its column j is the remainder of \(t^jB\) modulo \(P_s\). Apply this to \(B=P_s'\) and \(B=C_s\); multiply the first determinant by \((-1)^{r(r-1)/2}\) for \(\operatorname{Disc}P_s\). Use (8.5), substitute \(q^{-1}=q^{s-1}\) and reduce, multiply by the listed \(\delta_s\), and reduce again. Every determinant has size at most four, so the permutation formula alone suffices. For \(r=0\), the resultant and discriminant are one. This gives exactly the normalized vectors below. The equations defining \(g_s\), \(v_s\), and \(\delta_s\) provide an independent direct check of the listed \(\delta_s\).

### Base 3

Here \(r=0\) and \(c_3^+=1\). The coefficients of \(P_3\) are:

- \(p_{3,0}\): [1, 0]

The vector of \(\delta_3\) is

[1, 1].

The normalized augmented vector \(a_3\) is

[1, 1].

A Bezout vector \(w_3\) is

[0, 1].

### Base 7

Here \(r=1\) and \(c_7^+=49\). The coefficients of \(P_7\) are:

- \(p_{7,0}\): [0, 1, 1, 0, 0, 0]
- \(p_{7,1}\): [1, 0, 0, 0, 0, 0]

The vector of \(\delta_7\) is

[2, -1, 0, 1, -2, 0].

The normalized augmented vector \(a_7\) is

[27348, 17547, -21955, -61457, -71258, -43910].

A Bezout vector \(w_7\) is

[812298, -1266014, -1, 0, 0, 0].

### Base 11

Here \(r=2\) and \(c_{11}^+=161051\). The coefficients of \(P_{11}\) are:

- \(p_{11,0}\): [-1, 0, 1, 1, 1, 1, 1, 0, 0, 0]
- \(p_{11,1}\): [0, 1, 1, 1, 1, 0, 0, 0, 0, 0]
- \(p_{11,2}\): [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

The vector of \(\delta_{11}\) is

[3, -2, -1, 0, 0, 0, 0, -1, -2, 3].

The normalized augmented vector \(a_{11}\) is

[-2360899828777433, -8694030300823112, -16988667238997447, -24611322022556028, -29141855616808621, -29141855616808621, -24611322022556028, -16988667238997447, -8694030300823112, -2360899828777433].

A Bezout vector \(w_{11}\) is

[1043150420605847, -283271804236096, 0, 0, 0, 0, 0, 0, 0, 0].

### Base 15

Here \(r=3\) and \(c_{15}^+=1037970703125\). The coefficients of \(P_{15}\) are:

- \(p_{15,0}\): [-5, 0, 0, -4, 2, -3, -2, 5]
- \(p_{15,1}\): [-6, 2, 2, -2, 4, -1, 1, 5]
- \(p_{15,2}\): [0, 1, 1, 1, 1, 1, 1, 0]
- \(p_{15,3}\): [1, 0, 0, 0, 0, 0, 0, 0]

The vector of \(\delta_{15}\) is

[10, -8, -3, 1, -2, 1, 2, -2].

The normalized augmented vector \(a_{15}\) is

[36519624804568070593272981830504, -144482416373710208914682915965726, -125814668900235309059922662163369, -48872797378957263942601015809634, -174687466279192573002523677973003, -59089994190184874378808918325588, -107962791569142138321409934135222, -174687466279192573002523677973003].

A Bezout vector \(w_{15}\) is

[86729718455026776043942407993513259136617140973833484926883056, 21921953251328128968606881698396162793454374795863046630926892, -1, 0, 0, 0, 0, 0].

### Base 19

Here \(r=4\) and \(c_{19}^+=116490258898219\). The coefficients of \(P_{19}\) are:

- \(p_{19,0}\): [1, 0, -2, -2, -2, -2, -3, -2, -1, -1, 0, 1, 1, 2, 2, 2, 2, 1]
- \(p_{19,1}\): [-1, -3, -3, -2, -2, -1, 0, 0, 1, 4, 4, 4, 4, 3, 2, 2, 1, 0]
- \(p_{19,2}\): [-3, 0, 1, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 1, 1, 0, 0, 0]
- \(p_{19,3}\): [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
- \(p_{19,4}\): [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

The vector of \(\delta_{19}\) is

[6, -4, 0, -6, 0, -4, 6, 0, 0, 1, 0, 1, -1, -1, 1, 0, 1, 0].

The normalized augmented vector \(a_{19}\) is

[-91965351741027126694478835893795912347504539364529635481479, -165849473782970318073927649925785641333129986016231393789510, -213645875072310738740952689734199536280456896365615039762869, -230175073891768778682938205615969473147771991967598347176308, -213645875072310738740952689734199536280456896365615039762869, -165849473782970318073927649925785641333129986016231393789510, -91965351741027126694478835893795912347504539364529635481479, 0, 100080708589510684969220423710597307944042156916657040895516, 197431476339635583747303090268489026095471573922926115825572, 281502837011849364943317070563874136510861004708114793937772, 343184354175749375549863750419144472865315770563616389570536, 375791878359276119976509375505846305752867211777799084707534, 375791878359276119976509375505846305752867211777799084707534, 343184354175749375549863750419144472865315770563616389570536, 281502837011849364943317070563874136510861004708114793937772, 197431476339635583747303090268489026095471573922926115825572, 100080708589510684969220423710597307944042156916657040895516].

A Bezout vector \(w_{19}\) is

[68424302042046467015714588488272963729972772418021441444141, -37942025750203041439253413659407262584134131571977325398154, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0].

## Appendix B Reproducibility and review scope

The finite arithmetic in Appendix A was reconstructed afresh for this note with q-Pascal coefficients, the reciprocal transform, and permutation determinants of size at most four. Every coefficient field U, P, g, v, delta, Disc(U), the resultant, Gamma, Gamma Gamma^iota, and the augmented product matched the supplied exact data. Integer Bezout identities and the inverse identity were also checked. The fresh checker and its results accompany the note as verify_finite_certificates.py and FRESH_FINITE_CHECKS.json.

The prior independent review used a different construction: Gaussian coefficients from subset enumeration and direct full-degree multiplication matrices, with exact determinant calculations. Its coefficient records are supplied as additional finite evidence. None of the predecessor programs was executed, imported, compiled, or parsed during preparation of this note. Prior JSON was treated as data, not as authority for mathematical steps left unstated.

The reference and certificate index records source provenance and exact hashes. Review receipts are evidence of a scoped review, not published references and not substitutes for the proofs above. This note remains a research draft after mathematical proof completion. No external publication or priority certification is represented by that status.
