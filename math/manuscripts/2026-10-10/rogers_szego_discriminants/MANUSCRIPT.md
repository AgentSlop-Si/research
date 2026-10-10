# Moving root coefficients and ordinary discriminants of Rogers Szegő polynomials

Working manuscript, 10 October 2026 UTC. Existing guarded theorem finalized for mathematical review. This text assigns no authorship and makes no publication-priority claim.

## Abstract

For the Rogers–Szegő polynomial $H_n(z;q)$, the classical root-of-unity factorization identifies repeated roots at a fixed odd-order root $q=\omega$. The theorem below determines their first displacements when $q^d-1=\varepsilon^2$, and consequently the complete leading coefficient of the ordinary $z$-discriminant. Separated clusters have a monic probabilists’ Hermite initial form. When the residual polynomial has exactly one simple common root with $z^d+1$, at $-1$, the initial form is $y\operatorname{He}_A(y)-\tau\operatorname{He}'_A(y)$, with the explicit Rogers–Szegő parameter $\tau=dW/H_b'(-1;\omega)$. All residual and local simplicity guards are stated. The two cases have different exact cyclotomic orders and different nonzero coefficients.

The proofs use formal generating series and root differences, with integral cyclotomic division performed before any arithmetic reduction. A separate arithmetic section records the same-component guard and the exact finite-characteristic inverse-pair exception. A characteristic-zero half-residual-degree corollary is proved in an appendix. The narrowly defined comparison target is the fixed-nontrivial-root moving-variable coefficient, especially the shared-root parameter and its full normalization. Static q-Lucas factorization, Hermite discriminants, quasi-Laguerre reductions, and cyclotomic ramification are classical ingredients. Worldwide priority remains unresolved.

## 1 Definitions and theorem scope

The Gaussian binomial coefficients are the integral polynomials determined by

$$
{0\brack0}_q=1,\qquad
{n\brack k}_q={n-1\brack k}_q+q^{n-k}{n-1\brack k-1}_q,
$$

with coefficients outside $0\le k\le n$ equal to zero. Set

$$
H_n(z;q)=\sum_{k=0}^n{n\brack k}_qz^k,\qquad
D_n(q)=\operatorname{Disc}_zH_n(z;q)\in\mathbb Z[q].
\tag{1.1}
$$

Every $H_n$ is monic in $z$, with constant coefficient one. For a degree-$e\ge1$ polynomial $f=a\prod_i(z-\rho_i)$, the conventions are

$$
\operatorname{Disc}f=a^{2e-2}\prod_{i<j}(\rho_i-\rho_j)^2
=(-1)^{e(e-1)/2}a^{-1}\operatorname{Res}(f,f'),
\tag{1.2}
$$

where $f'$ is the ordinary derivative. For degrees $e,h$,

$$
\operatorname{Res}(f,g)=a^h\prod_{i=1}^e g(\rho_i).
\tag{1.3}
$$

In particular the root-product formulas below have no suppressed leading-coefficient factors because the relevant global polynomials are monic. Adopt $\operatorname{Disc}1=1$, $\operatorname{Disc}(\text{monic linear})=1$, and $\operatorname{Res}(f,1)=1$. Thus $D_0=D_1=1$. No q-difference, q-shift, operator discriminant, or absolute value of a discriminant is used.

Write

$$
(a;q)_j=\prod_{t=0}^{j-1}(1-aq^t),\quad
\operatorname{He}_0=1,\quad\operatorname{He}_1=y,\quad
\operatorname{He}_{a+1}=y\operatorname{He}_a-a\operatorname{He}_{a-1},\quad
P_A=\prod_{j=1}^A j^j.
\tag{1.4}
$$

These are monic probabilists’ Hermite polynomials. The notation $P_A$ is reserved for this scalar product throughout the manuscript.

Fix an odd integer $d\ge1$, a primitive complex $d$-th root $\omega$, $A\ge1$, and $0\le b<d$. Let

$$
n=Ad+b,\qquad F(z)=z^d+1,\qquad G(z)=H_b(z;\omega),
$$
$$
q(\varepsilon)=\omega(1+\varepsilon^2)^{1/d},\qquad
q(\varepsilon)^d-1=\varepsilon^2.
\tag{1.5}
$$

The fractional power is the binomial series with constant term one. Big-O terms are coefficientwise formal orders in $\varepsilon$, over a characteristic-zero field containing the displayed algebraic constants. At any fixed coefficient of the generating variable only finitely many series terms are used. No analytic interchange of infinite sums is required. The separated theorem includes $d=1,b=0$, a classical endpoint. The fixed-nontrivial-root comparison concerns $d\ge3$.

The case statements are conditional. They do not classify higher residual multiplicities, several shared roots, or a repeated local initial form. Those cases are outside this theorem, rather than obtained by putting a zero into a claimed nonzero leading coefficient.

## 2 The two case theorem

### Theorem 2.1 Separated clusters

Assume

$$
\Delta=\operatorname{Disc}G\ne0,\qquad
R=\operatorname{Res}(F,G)\ne0.
\tag{2.1}
$$

For every $\alpha^d=-1$,

$$
H_n(\alpha+\varepsilon x;q(\varepsilon))
=\varepsilon^A(-1)^Ad^{A/2}G(\alpha)
\operatorname{He}_A(\sqrt d\,x/\alpha)+O(\varepsilon^{A+1}).
\tag{2.2}
$$

Let $K=dA(A-1)/2$. Then

$$
D_n(q(\varepsilon))=\varepsilon^{2K}(C_{\rm sep}+O(\varepsilon^2)),
\tag{2.3}
$$
$$
C_{\rm sep}=(-1)^{A(d-1)/2}d^{dA(A+1)/2}P_A^d\Delta R^{2A}\ne0,
\qquad\operatorname{ord}_{\Phi_d}D_n=K.
\tag{2.4}
$$

The residual hypotheses mean precisely that $G$ has simple roots and is disjoint from $F$. They cannot be replaced by either condition alone. For odd $b$, $G(-1)=0$, so the separated resultant vanishes; that parity does not satisfy (2.1).

### Theorem 2.2 One simple shared root

Assume $d\ge3$, $b$ odd, and $1\le b<d$. Write

$$
G=(z+1)U,\qquad g=U(-1)=G'(-1),\qquad
W=\frac{(\omega;\omega)_b}{(\omega^2;\omega^2)_{(b+d)/2}}.
\tag{2.5}
$$

First require $\operatorname{Res}(F,U)\ne0$. This implies $g\ne0$, so the following parameter is defined:

$$
\tau=dW/g,\qquad
J_{A+1}(y;\tau)=y\operatorname{He}_A(y)-\tau\operatorname{He}'_A(y)
=\operatorname{He}_{A+1}(y)+A(1-\tau)\operatorname{He}_{A-1}(y).
\tag{2.6}
$$

Every denominator in $W$ is nonzero: $(b+d)/2<d$ and $\omega^2$ has order $d$. In addition require

$$
\Delta_U=\operatorname{Disc}U\ne0,\qquad
R_U=\operatorname{Res}(F,U)\ne0,\qquad
S_A(\tau)=\operatorname{Disc}_y J_{A+1}(y;\tau)\ne0.
\tag{2.7}
$$

Then

$$
H_n(-1+\varepsilon x;q(\varepsilon))
=\varepsilon^{A+1}(-1)^{A+1}d^{(A-1)/2}g
J_{A+1}(-\sqrt d\,x;\tau)+O(\varepsilon^{A+2}).
\tag{2.8}
$$

At each other root of $F$, (2.2) is the nonzero leading form. With $L=K+A$,

$$
D_n(q(\varepsilon))=\varepsilon^{2L}(C_{\rm ov}+O(\varepsilon^2)),
\tag{2.9}
$$
$$
C_{\rm ov}=(-1)^{A(d-1)/2}d^{dA(A+1)/2+A}P_A^{d-1}
S_A(\tau)\Delta_U R_U^{2A}g^2\ne0,
\qquad\operatorname{ord}_{\Phi_d}D_n=L.
\tag{2.10}
$$

In this case exactly one residual simple root joins a cluster. The cluster at $-1$ has $A+1$ branches, the other (d-1) clusters each have $A$, and (b-1) residual branches remain. The hypothesis $R_U\ne0$ excludes both an additional root of $U$ at $-1$ and any other cluster intersection. The local form $J$ must not be replaced by $\operatorname{He}_{A+1}$.

### Corollary 2.3 Normalization and exact integral quotient

Let $M=K,C=C_{\rm sep}$ or $M=L,C=C_{\rm ov}$ under the respective hypotheses, and set

$$
Q_d(q)=\frac{q^d-1}{\Phi_d(q)}.
$$

Then there is an integral polynomial $E_{n,d}\in\mathbb Z[q]$ such that

$$
D_n(q)=\Phi_d(q)^M E_{n,d}(q),\qquad
E_{n,d}(\omega)=Q_d(\omega)^M C\ne0.
\tag{2.11}
$$

The coefficient $C$ is the leading coefficient in the local parameter $q^d-1$. In $q-\omega$ the coefficient is

$$
(d\omega^{d-1})^M C.
\tag{2.12}
$$

Thus the $\varepsilon$-order is (2M), the $q-\omega$-order and cyclotomic multiplicity are $M$, and the integral quotient value is $Q_d(\omega)^MC$. These are three different normalizations of the same nonzero term.

**Source lineage.** Theorems 2.1–2.2 and Corollary 2.3 reproduce the accepted symbolic results of S01 §§2–4 and S03 §§2–3,6, audited in S02 §§3–5 and S04 §§3–4,7. The current rereading is R06 §1. Identifiers refer to the exact local sources and hashes in EVIDENCE_CONCORDANCE.md and SOURCE_PINS.json. They are provenance citations, not external-publication priority claims.

## 3 Elementary identities and formal local splitting

### Lemma 3.1 Polynomial and generating identities

The coefficient definition implies

$$
H_0=1,\quad H_1=1+z,\quad
H_n=(1+z)H_{n-1}+(q^{n-1}-1)zH_{n-2},\quad
z^nH_n(z^{-1};q)=H_n(z;q).
\tag{3.1}
$$

Moreover,

$$
\sum_{n\ge0}\frac{H_n(z;q)t^n}{(q;q)_n}
=\exp\left(\sum_{k\ge1}\frac{(1+z^k)t^k}{k(1-q^k)}\right),
\tag{3.2}
$$

initially as a coefficientwise identity over $\mathbb Q(q,z)$. At an odd-order root,

$$
H_{Ad+b}(z;\omega)=(1+z^d)^AH_b(z;\omega).
\tag{3.3}
$$

**Proof.** Substitute the coefficient definition into (3.1); Gaussian symmetry gives reciprocity. For (3.2), put $E(t)=\sum_{j\ge0}t^j/(q;q)_j$. Its coefficient recurrence gives $E(qt)=(1-t)E(t)$, and formal logarithms give $\log E(t)=\sum_{k\ge1}t^k/[k(1-q^k)]$. Multiplication of $E(t)E(zt)$ proves (3.2).

The finite q-binomial identity follows from q-Pascal:

$$
\prod_{j=0}^{n-1}(1+tq^j)
=\sum_k q^{k(k-1)/2}{n\brack k}_q t^k.
$$

At $q=\omega$, each full block is $1+t^d$, since $d$ is odd. For $k=cd+e$, the exponent difference from (e(e-1)/2) is $dc(cd+2e-1)/2$, an integer multiple of $d$. Coefficient comparison therefore gives $ {Ad+b\brack cd+e}_\omega=\binom Ac{b\brack e}_\omega$; summing yields (3.3). This is the classical q-Lucas specialization [Sagan92, Theorem 2.2] and [LS87, Lemma 4.5], not a new static factorization. ∎

### Lemma 3.2 Singular weight calculation

In (3.2), split the exponent into $d\mid k$ and $d\nmid k$, and denote the exponential of the regular part by $B(t;z,q)$. At $z=\alpha+\varepsilon x$, $\alpha^d=-1$, put $u=t^d$. The singular logarithm has first two coefficients

$$
[u]=\frac{x}{\alpha\varepsilon}+O(1),\qquad
[u^2]=-\frac1{2d\varepsilon^2}+O(\varepsilon^{-1}).
\tag{3.4}
$$

For $u^l$, $l\ge3$, its pole order is strictly less than $l$. Thus

$$
[u^a]\exp(\text{singular logarithm})
=\varepsilon^{-a}\frac{d^{-a/2}}{a!}
\operatorname{He}_a(\sqrt d\,x/\alpha)+O(\varepsilon^{-a+1}).
\tag{3.5}
$$

Also

$$
(q(\varepsilon);q(\varepsilon))_{Ad+b}
=(-1)^AA!d^A(\omega;\omega)_b\varepsilon^{2A}(1+O(\varepsilon^2)).
\tag{3.6}
$$

**Proof.** In the term indexed by $k=ld$, $1-q^{ld}=1-(1+\varepsilon^2)^l$ has order two. The numerator has zero constant for odd $l$, and nonzero constant for even $l$. The pole order is at most one or two, respectively. Expanding $l=1,2$ gives (3.4). For $l\ge3$ these weights are strictly smaller than the $u$-degree. Hence only the displayed terms reach pole order $a$ in degree $u^a$. Their exponential is the Hermite generating function $\exp(Ys-s^2/2)=\sum_a\operatorname{He}_a(Y)s^a/a!$ with $s=u/(\sqrt d\,\varepsilon)$, proving (3.5).

The multiples (jd) in the factorial contribute $-j\varepsilon^2(1+O(\varepsilon^2))$. Each complete block of nonmultiples contributes $\prod_{j=1}^{d-1}(1-\omega^j)=d$, and the last incomplete block contributes $(\omega;\omega)_b$. All perturbations are even in $\varepsilon$. This proves (3.6), including $d=1,b=0$ with empty nonmultiple products. ∎

### Proof of the separated initial form

Because $b<d$, the constant term in $\varepsilon$ of $[t^b]B(t;\alpha+\varepsilon x,q(\varepsilon))$ is $G(\alpha)/(\omega;\omega)_b$. To extract $t^{Ad+b}$, the regular degree $b+jd$ pairs with singular degree (A-j). Every $j\ge1$ has pole order at most $A-j<A$. Combining the $j=0$ term in (3.5) with (3.6) proves (2.2).

Its coefficient at $x^{A-2j}$ is explicitly

$$
\frac{(-1)^{A+j}A!d^{A-j}G(\alpha)\alpha^{-A+2j}}
{2^j j!(A-2j)!},\qquad0\le j\le\lfloor A/2\rfloor.
\tag{3.7}
$$

This verifies that the square roots cancel and the leading coefficient in $x$ is $(-d/\alpha)^AG(\alpha)=F'(\alpha)^AG(\alpha)$. The identity remains true with zero right-hand leading coefficient if $G(\alpha)=0$, but then it does not determine the first nonzero local term. ∎

### Proof of the shared initial form

Odd reciprocity gives $H_b(-1;q)=0$ identically. At $z=-1+\varepsilon x$, the first relevant regular coefficient is

$$
[t^b]B=\frac{\varepsilon xg}{(\omega;\omega)_b}+O(\varepsilon^2).
\tag{3.8}
$$

There is also a contribution at regular degree $b+d$. At $z=-1$, the full logarithm has only even powers of $t$; the first positive even multiple of $d$ is $2d>b+d$. Removing the divisible-by-$d$ terms therefore does not affect this coefficient. The formal identity $E(t)E(-t)=\sum_{j\ge0}t^{2j}/(q^2;q^2)_j$ gives

$$
[t^{b+d}]B(t;-1,\omega)
=\frac1{(\omega^2;\omega^2)_{(b+d)/2}}.
\tag{3.9}
$$

The contributions from (3.8) and (3.9) have total order $\varepsilon^{A+1}$ after multiplication by (3.6); all regular degrees $b+jd$, $j\ge2$, have order at least $A+2$. For a square-root-free expression define

$$
T_0(x)=1,\quad T_1(x)=-x,\quad
T_a(x)=-xT_{a-1}(x)-\frac{a-1}{d}T_{a-2}(x).
$$

Thus $T_a=d^{-a/2}\operatorname{He}_a(-\sqrt d\,x)$, and the leading polynomial is

$$
[\varepsilon^{A+1}]H_n(-1+\varepsilon x;q(\varepsilon))
=(-1)^Ad^A\{gxT_A(x)+AWT_{A-1}(x)\}.
\tag{3.10}
$$

Use $\operatorname{He}'_A=A\operatorname{He}_{A-1}$ and $\tau=dW/g$ to obtain (2.8). The $x^{A+1}$ coefficient is $gd^A$, exactly the coefficient supplied by $F(z)^A(z+1)U(z)$ at $-1$. This check also rules out a missing local leading-coefficient factor. ∎

## 4 Root branches and the full discriminant coefficients

### Lemma 4.1 Hermite discriminant and simple lifting

The recurrence gives $\operatorname{He}'_A=A\operatorname{He}_{A-1}$ and

$$
\operatorname{Disc}\operatorname{He}_A=P_A\ne0.
\tag{4.1}
$$

Indeed, if $r_A=\operatorname{Res}(\operatorname{He}_A,\operatorname{He}_{A-1})$, evaluation at roots of $\operatorname{He}_{A-1}$ gives $r_A=(-1)^{A-1}(A-1)^{A-1}r_{A-1}$. The derivative contributes $A^A$, and the sign in (1.2) cancels the accumulated sign. Every leading polynomial used in (2.2) or (2.8) is squarefree under the corresponding guards. Its simple roots lift coefficientwise by the formal implicit-function theorem. As the branch counts sum to $n$, these are all the roots of the monic polynomial $H_n$.

### Proof of Theorem 2.1 for the discriminant

If $h_1,\ldots,h_A$ are the roots of $\operatorname{He}_A$, the branches at $\alpha$ are

$$
z_{\alpha,j}=\alpha+\varepsilon\frac{\alpha}{\sqrt d}h_j+O(\varepsilon^2).
\tag{4.2}
$$

One cluster contributes $\varepsilon^{A(A-1)}(\alpha^2/d)^{A(A-1)/2}P_A$ to the product of squared differences. Since $\prod_{F(\alpha)=0}\alpha=-1$ and $A(A-1)$ is even, all $d$ clusters together contribute $\varepsilon^{2K}d^{-K}P_A^d$.

Differences between distinct clusters contribute $(\operatorname{Disc}F)^{A^2}$, where

$$
\operatorname{Disc}(z^d+1)=(-1)^{(d-1)/2}d^d.
\tag{4.3}
$$

Differences among residual roots contribute $\Delta$, and cluster-to-residual differences contribute $R^{2A}$. Multiplication gives (2.4), because $dA^2-K=dA(A+1)/2$ and $A^2\equiv A\pmod2$. Every factor is nonzero. The exact order is therefore (2K) in $\varepsilon$. Since $D_n(q(\varepsilon))$ is even, the remainder after the nonzero leading term is of relative order at least two. ∎

### Proof of Theorem 2.2 for the discriminant

At $-1$, the branches have first displacements $-j_k/\sqrt d$, where $j_k$ range over the $A+1$ simple roots of $J_{A+1}$. At the other clusters use (4.2). Their combined within-cluster factors are

$$
\varepsilon^{2L}d^{-L}P_A^{d-1}S_A(\tau),\quad
L=(d-1)\frac{A(A-1)}2+\frac{A(A+1)}2.
\tag{4.4}
$$

The product of roots of $F$ other than $-1$ is one, so no root-scaling factor is omitted. Write $F_0=F/(z+1)$. As $F_0(-1)=F'(-1)=d$,

$$
\operatorname{Disc}F_0=(-1)^{(d-1)/2}d^{d-2}.
$$

Between the ordinary clusters the factor is $(\operatorname{Disc}F_0)^{A^2}$; between those clusters and the shared one it is $d^{2A(A+1)}$. Together these are $(-1)^{A(d-1)/2}d^{dA^2+2A}$. Residual differences contribute $\Delta_U R_U^{2A}g^2$; the last $g^2$ accounts for the one extra branch at $-1$. Combining with (4.4) yields (2.10). Nonvanishing and evenness give the exact order and remainder in (2.9). ∎

### Proof of Corollary 2.3

The parameter $q^d-1$ has a simple zero at $q=\omega$, with derivative $d\omega^{d-1}$. Thus the exact local multiplicity is $M$, and (2.12) follows. Galois conjugacy transports the nonzero coefficient to every primitive $d$-th root. Hence $\Phi_d^M\mid D_n$ and $\Phi_d^{M+1}\nmid D_n$ over $\mathbb Q[q]$. Successive division by the monic integral polynomial $\Phi_d$ gives $E_{n,d}\in\mathbb Z[q]$. Finally $q^d-1=\Phi_dQ_d$ gives (2.11) by leading-term comparison. No reduction modulo a prime has yet occurred. ∎

## 5 Arithmetic use with a single common good component

This section is an application of the local theorem, not a general statement of composite squarefreeness. All derivatives and discriminants remain ordinary. It contains no claim that a characteristic-zero guard stays nonzero in every finite-characteristic component.

### Proposition 5.1 One good leading coefficient suffices

Let $p$ be an odd prime, $p\nmid d$, $A=(p-1)/2$, $b=(d-1)/2$, and $n=(dp-1)/2$. Suppose that at one prime of $\mathbb Z[\omega]$ above $p$, either all the separated guards, or all the overlap guards in (2.7), reduce to nonzero elements. Rational expressions in $\tau$ are evaluated only after their denominators have been checked to be units. Then

$$
D_{(dp-1)/2}(\zeta_{dp})\ne0
\tag{5.1}
$$

for every primitive complex (dp)-th root.

**Proof.** At this component, $d$ is a unit and $A<p$, so $P_A$ is a unit. In the overlap case $R_U\ne0$ also makes $g$ a unit. Each factor of $W$ is a unit: exact order $d$ is preserved in this residue field because $p\nmid d$, and all relevant exponents are nonzero modulo $d$. Thus the relevant $C$ is a unit. In particular the characteristic-zero guards hold, and Corollary 2.3 applies.

The polynomial $q^d-1\bmod p$ is squarefree, so its cyclotomic factors are pairwise coprime and $Q_d(\omega)$ is a unit. Consequently $E_{n,d}(\omega)=Q_d(\omega)^MC$ is nonzero at the chosen component. If $D_n(\zeta_{dp})=0$, irreducibility and integrality give $\Phi_{dp}\mid D_n$, hence $\Phi_{dp}\mid E_{n,d}$, since $\Phi_{dp}\ne\Phi_d$. But

$$
\Phi_{dp}(q)\Phi_d(q)=\Phi_d(q^p),\qquad
\Phi_{dp}(q)\equiv\Phi_d(q)^{p-1}\pmod p
\tag{5.2}
$$

would force $E_{n,d}$ to vanish in every lower residue component. This contradicts the chosen one. All of $\Phi_d^M$ was removed in $\mathbb Z[q]$ before reduction; no bound $M<p-1$ is needed. ∎

### Proposition 5.2 Content is a same-component existence test

For $a\in\mathbb Z[\omega]$, let $\operatorname{cont}_d(a)$ be the nonnegative gcd of the coefficients of its unique representative of degree below $\varphi(d)$; the zero element has content zero. If $p\nmid d$, the ring $\mathbb Z[\omega]/p\mathbb Z[\omega]$ is a product of finite fields. For $a\ne0$, $p\nmid\operatorname{cont}_d(a)$ means that its reduction is nonzero in at least one component. For a product $a=a_1\cdots a_t$, this means that all factors are nonzero in the same component.

**Proof.** Squarefreeness of $\Phi_d\bmod p$ and the Chinese remainder theorem give the product of fields. A canonical remainder represents zero modulo $p$ exactly when all its integral coefficients are divisible by $p$. A product is nonzero in a field exactly when every factor is nonzero there. ∎

A nonzero element of this product ring need not be a unit in the whole ring. Separate good components for separate factors do not suffice. An algebraic norm, which multiplies over components and sums local valuations, does not replace the canonical coefficient content.

### Proposition 5.3 The finite characteristic pairing and its exact exception

Let $p$ be any odd prime and $A=(p-1)/2$. Over a field of characteristic $p$, let $\tau,\tau'\ne0$ be finite and satisfy

$$
1/\tau+1/\tau'=1.
\tag{5.3}
$$

At least one of $J_{A+1}(y;\tau)$ and $J_{A+1}(y;\tau')$ is squarefree over the algebraic closure, except exactly when

$$
p\equiv1\pmod4,\qquad\tau=\tau'=2.
\tag{5.4}
$$

In (5.4) both have a zero of multiplicity exactly three at $y=0$.

**Proof.** Put $H=\operatorname{He}_A$. Because $A<p$, consecutive Hermite polynomials are coprime by downward recurrence and $H'=A\operatorname{He}_{A-1}$; hence $\gcd(H,H')=1$. At any root of $J=yH-\tau H'$, $H\ne0$. Relation (5.3) implies $\tau\ne1$ and $\tau'=\tau/(\tau-1)$. The Hermite equation $H''-yH'+AH=0$ shows that a multiple root satisfies

$$
y^2=t(\tau)=\frac{\tau(\tau-2)}{2(1-\tau)},\qquad t(\tau')=-t(\tau),
\tag{5.5}
$$

using $A=-1/2$ in the field. If both polynomials had a multiple root with $y\ne0$, choose $i^2=-1$ in the algebraic closure; parity permits matching the second root at (iy). Put $V(y)=i^{-A}H(iy)$. The two Hermite differential equations imply

$$
[H'V-HV'-yHV]'=-(2A+1)HV=0.
$$

The bracket is odd, of degree $p$, and has leading coefficient $-1$, so

$$
H'V-HV'-yHV=-y^p.
\tag{5.6}
$$

At the alleged pair $H'/H=y/\tau$ and $V'/V=-y/\tau'$. Dividing the left side by $HV\ne0$ gives zero by (5.3), contradicting $y\ne0$.

Thus simultaneous failure requires zero as a multiple root; (5.5) forces $\tau=\tau'=2$. If $A$ is odd, $H'(0)\ne0$ and $J(0;2)\ne0$. If $A$ is even, $H(0)=c_0\ne0$ and $J'(0;2)=(1+2A)c_0=0$. The Hermite equation gives $c_2=-Ac_0/2$ and $c_4=A(A-2)c_0/24$; the cubic coefficient of (yH-2H') is $A(1-2A)c_0/6=-c_0/6\ne0$. Here $p\equiv1\pmod4$ implies $p\ge5$, so these denominators are units. This proves the exact exception and multiplicity, including $p=5,A=2$. ∎

The identity (5.6) has a classical Hermite-Wronskian interpretation [GGM18; GG20, Theorem 8]. Its elementary proof here does not claim a new Wronskian mechanism. A complex-parameter disk argument cannot replace this finite-characteristic proof.

### Corollary 5.4 Three distinct lower content criteria

For the separated case at odd $s$, set $b=(s-1)/2$ and

$$
c_s^{\rm sep}=\operatorname{cont}_s\!\left(
\operatorname{Disc}H_b\operatorname{Res}(z^s+1,H_b)\right).
\tag{5.7}
$$

If $p$ is an odd prime, $p\nmid s$, $c_s^{\rm sep}\ne0$, and $p\nmid c_s^{\rm sep}$, then $H_{(sp-1)/2}(z;\zeta_{sp})$ is squarefree. This content is zero when $s\equiv3\pmod4$, since the residual odd-degree polynomial shares $-1$.

For overlap, let $s=4r+3$, $b=2r+1$, $\iota(\omega)=\omega^{-1}$, and define

$$
U_s=H_b/(z+1),\quad g_s=U_s(-1),\quad
v_s=(\omega^2;\omega^2)_r(\omega;\omega^2)_b=sW,
$$
$$
\Gamma_s=\operatorname{Disc}U_s\operatorname{Res}(z^s+1,U_s),\qquad
\delta_s=2g_s-v_s,
$$
$$
c_s^{\rm pair}=\operatorname{cont}_s(\Gamma_s\Gamma_s^\iota),\qquad
c_s^+=\operatorname{cont}_s(\Gamma_s\Gamma_s^\iota\delta_s).
\tag{5.8}
$$

If $p\nmid s$, the same squarefreeness conclusion holds under either of these separate hypotheses:

1. $p\equiv3\pmod4$, $c_s^{\rm pair}\ne0$, and $p\nmid c_s^{\rm pair}$.
2. $p\equiv1\pmod4$, $c_s^+\ne0$, and $p\nmid c_s^+$.

**Proof.** The separated conclusion is Propositions 5.1–5.2. For overlap, the denominator-free identity

$$
g_sv_s^\iota+g_s^\iota v_s=v_sv_s^\iota
\tag{5.9}
$$

is proved in Appendix A. Its polynomial product expressions are integral and survive reduction. Proposition 5.2 selects one component where both inverse residual guards are nonzero, and in the second parity $\delta_s$ is also nonzero. Both $g$'s and both $v$'s are units there. Thus $\tau=v_s/g_s$ and $\tau'=v_s^\iota/g_s^\iota$ are defined and satisfy (5.3). In the first parity there is no exception; in the second $\delta_s\ne0$ excludes $\tau=2$ and hence the simultaneous exceptional pair. Proposition 5.3 supplies one inverse root where $S_A\ne0$. That selected root has all overlap guards in one component, so Proposition 5.1 applies. Inversion may move between irreducible factors; inverse stability of a factor is not assumed. ∎

The local coefficient proof remains separate from finite fixed-base certifications. This manuscript does not certify new bases, append isolated repeated-prime exceptions, or use the equality of some historical paired and augmented contents as an identity of the two contents.

## 6 Comparison target and classical dependencies

The exact first-displacement polynomial at fixed $\omega\ne1$, especially the overlap parameter (dW/g), is the narrow candidate contribution. The full coefficient records its consequence for the ordinary discriminant, including sign, scale, and cyclotomic cofactor. This contribution description is a bounded comparison target, not a proof of worldwide originality.

The static factorization (3.3) is classical q-Lucas. The $d=1$ Hermite endpoint, Hermite discriminant $P_A$, root-product discriminant calculation, and elementary cyclotomic identities are also classical. Lubinsky–Saff [LS87] provides recurrence/reciprocity in Lemma 4.1, p.343, and the static factorization in Lemma 4.5, (4.15), p.346. Its Theorem 3.2, (3.11)–(3.12), p.340, addresses the related Padé determinant and denominator. Its determinant notation must not be confused with the present ordinary discriminant $D_n$.

The standalone discriminant of $J$ is reducible to established quasi-Laguerre formulas. If $A=2m-1$, put

$$
\mathcal P_m(t)=(-1)^m m!\{L_m^{(-1/2)}(t)+cL_{m-1}^{(-1/2)}(t)\},\qquad
c=\frac{(2m-1)(\tau-1)}{2m}.
$$

Then $J_{2m}(y;\tau)=2^m\mathcal P_m(y^2/2)$. If $A=2m$, the analogous formulas are

$$
\mathcal P_m(t)=(-1)^m m!\{L_m^{(1/2)}(t)+cL_{m-1}^{(1/2)}(t)\},\quad c=\tau-1,
\quad J_{2m+1}(y;\tau)=y2^m\mathcal P_m(y^2/2).
\tag{6.1}
$$

Here $\mathcal P_m$ is monic. Elementary paired roots give

$$
\operatorname{Disc}[2^m\mathcal P_m(y^2/2)]
=(-1)^m2^{2m^2+m}\mathcal P_m(0)(\operatorname{Disc}\mathcal P_m)^2,
$$
$$
\operatorname{Disc}[y2^m\mathcal P_m(y^2/2)]
=(-1)^m2^{2m^2+3m}\mathcal P_m(0)^3(\operatorname{Disc}\mathcal P_m)^2.
\tag{6.2}
$$

These identities show why a standalone general $J$-discriminant formula is not the contribution claimed here. Cite Sawa–Uchida’s final journal Theorem 3.6, equation (3.6), pp.844–845 [SU19], or explicitly the preprint’s Theorem 4.8, equation (4.13), arXiv v1 [SU18v1]. Do not combine the final title with the preprint numbering without identifying the version. Final Theorem 3.8 concerns adjacent quasi-Hermite polynomials and does not, by itself, replace the parity reduction (6.1). Any rational representation must be simplified before a singular parameter is specialized.

Ismail–Witte’s explicit Rogers–Szegő q-discriminant is a different invariant [IW01, (5.13), (5.17)]. For the monic $H_2=z^2+(1+q)z+1$, the ordinary discriminant is $(q-1)(q+3)$; the corresponding monic q-difference discriminant is $(q-1)(q+1)^2$. At a primitive cubic root, $H_3=z^3+1$ has ordinary discriminant (-27), while the q-discriminant vanishes. These distinctions prevent transferring a q-difference formula into (2.4) or (2.10).

The source comparison in this finalization is inherited from the pinned P2109 inspection, not a new retrieval of external papers. The project manuscript records reading LS87 journal pp.331–359 and reference p.361; reference p.360 remains missing, and its original scan was not newly inspected here. Zhedanov’s distinct “Gauss sums and orthogonal polynomials” [Z97] remains a full-text gap. The Spiridonov–Zhedanov Duke paper [SZ97] is not a substitute. No denied access route has been retried or bypassed. Missing access is not negative evidence about a theorem’s presence in those sources. The complex disk and inverse-pair application also retain their own priority-comparison boundary.

## 7 Scope boundaries and status

No missing proof lemma was identified in Theorems 2.1–2.2, their normalization, the conditional arithmetic statements of Section 5, or the characteristic-zero refinement in Appendix A. Their proofs are reproduced above and below, with existing independent local review cited. This is not external specialist or journal validation, formal proof-assistant verification, or worldwide-priority clearance.

The following extensions remain outside the proved scope:

- Ordinary squarefreeness of every composite half-order Rogers–Szegő polynomial.
- Unconditional separated or augmented content support at arbitrary lower orders.
- Dropping $p\nmid s$, or replacing a target (sp) by $sp^a$, $a\ge2$, using the same first coefficient. For $A=(p^a-1)/2\ge p$, $P_A$ is divisible by $p$, and the present unit bridge fails.
- Using complex-parameter inequalities as finite-characteristic nonvanishing statements.
- Replacing same-component guard selection by separate good factors, a norm, or unreduced coefficient content.
- An unrestricted inverse-bank optimum, an FFT complexity improvement, or numerical stability.

Failure of a sufficient residue criterion does not prove a characteristic-zero multiple root. The only claims made about historical fixed-base arithmetic and the separated-content valuation are the separately labeled context in NORMALIZATION_AND_GUARDS.md and EVIDENCE_CONCORDANCE.md; their full certificate packages are not annexed as newly verified evidence here.

## Appendix A Characteristic zero half residual degree refinement

### Lemma A.1 The inverse parameter identity

Let $d=4r+3$, $b=2r+1=(d-1)/2$, $Q=\omega^2$, $a_j=(\omega;Q)_j/(Q;Q)_j$, and $M_0=(\omega;Q)_b$. Then

$$
v=dW=(Q;Q)_rM_0,\qquad
g=(Q;Q)_r\sum_{j=0}^r a_j,
\quad gv^\iota+g^\iota v=vv^\iota.
\tag{A.1}
$$

At every primitive complex embedding $g\ne0$, $2g-v\ne0$, and

$$
\tau=v/g\ne0,\qquad|1-\tau|=1.
\tag{A.2}
$$

**Proof.** Complete the denominator in $W$ against the full product $d=\prod_{k=1}^{d-1}(1-\omega^k)$ to obtain the expression for $v$. At $z=-1$, (3.1) gives $H_{2j}(-1;q)=(q;q^2)_j$ and $H_{2j+1}(-1;q)=0$. Differentiate the recurrence: if $g_j=H'_{2j+1}(-1;q)$, then $g_j=(q;q^2)_j+(1-q^{2j})g_{j-1}$, $g_0=1$. Induction gives the expression for $g$.

Since $\omega=Q^{-b}$, the finite q-binomial theorem gives $\sum_{j=0}^b a_j=M_0$. Direct inversion and Gaussian symmetry give

$$
a_j^\iota=\omega^j a_j,\qquad
a_{b-j}=(M_0/M_0^\iota)a_j^\iota.
$$

Splitting the full sum into $0\le j\le r$ and its complementary half yields $g/v+g^\iota/v^\iota=1$, equivalently the denominator-free identity in (A.1). All canceled factors have exponents strictly between zero and $d$.

For nonvanishing, first take $\omega=e^{2\pi i/d}$. Each ratio $(1-\omega^{2k+1})/(1-\omega^{2k+2})$, for $k<r$, has argument $-\pi/d$ and positive modulus. Thus $a_j$ has argument $-j\pi/d$. The product $M_0$ has argument $-b\pi/(2d)$. Every summand $a_j/M_0$, $j\le r$, therefore has argument $(b/2-j)\pi/d\in(0,\pi/4)$. Hence (g/v) has strictly positive real and imaginary parts; it is neither zero nor (1/2). Galois conjugacy gives $g\ne0$ and $2g-v\ne0$ at all primitive embeddings. At any such embedding $\iota$ is complex conjugation. Therefore $1/\tau+1/\overline\tau=1$, equivalently (A.2). The sector assertion itself is used only at the principal embedding; it is not transported as an absolute-value statement by Galois conjugacy. ∎

### Lemma A.2 A disk of simple Hermite combinations

For every $A\ge1$, $J(y;\tau)=y\operatorname{He}_A-\tau\operatorname{He}'_A$ is squarefree over $\mathbb C$ if

$$
\tau\ne0,\qquad |1-\tau|\le\sqrt{(A+1)/A}.
\tag{A.3}
$$

**Proof.** The roots of $H=\operatorname{He}_A$ are real, simple, and symmetric: $H$ is the characteristic polynomial of the real symmetric tridiagonal matrix with edges $\sqrt1,\ldots,\sqrt{A-1}$; each eigenspace has dimension at most one by the row recurrence. Pair opposite roots and put $z=y^2$. Away from poles,

$$
f(z)=\frac{H'(y)}{yH(y)}=\sum_j\frac{w_j}{z-a_j},
$$

where $a_j\ge0$, and the weights are two for positive squared roots and one for a possible zero root. At a nonzero multiple root with $\tau\ne0$, $f(z)=1/\tau$, $f'(z)=0$, and the Hermite equation gives $1+A\tau+(1-\tau)z/\tau=0$. The value $\tau=1$ is impossible. Writing $\sigma=1-\tau$,

$$
z=(2A+1)-A\sigma-(A+1)/\sigma.
\tag{A.4}
$$

Imaginary parts of the partial fractions yield $\operatorname{Im}z\sum_jw_j/|z-a_j|^2=\operatorname{Im}\tau/|\tau|^2$. For nonreal $\tau$, $\operatorname{Im}z$ has the opposite sign from $\operatorname{Im}\sigma$, whereas (A.4) gives $\operatorname{Im}z=\operatorname{Im}\sigma((A+1)/|\sigma|^2-A)$. Hence every such multiple root requires $|1-\tau|^2>(A+1)/A$.

For real nonzero $\tau$, the same identity forces $z$ real, but then $f'(z)=-\sum_jw_j/(z-a_j)^2<0$, contradicting a nonzero multiple root. At zero, odd $A$ allows a multiple root only when $\tau=0$; even $A$ gives $J'(0)=(1+A\tau)H(0)$, so the only possible value is $\tau=-1/A$, outside (A.3). Thus (A.3) suffices. ∎

### Lemma A.3 Half order resonance

Let $N=2m+1\ge3$, $q$ primitive of order $N$, and $T_m(z)=(-1)^mH_m(-z;q)$. In characteristic zero,

$$
\gcd(T_m,z^N-1)=
\begin{cases}1,&m\text{ even},\\z-1,&m\text{ odd}.
\end{cases}
\tag{A.5}
$$

In the odd case $1$ is a simple root of $T_m$.

**Proof.** First use $q=e^{2\pi i/N}$. Put $S_0=1,S_1=x$, and $S_n=xS_{n-1}-(1-q^{n-1})S_{n-2}$. The recurrence gives

$$
T_n(z)=(i\sqrt z)^n S_n((z-1)/(i\sqrt z)).
\tag{A.6}
$$

For $|z|=1$ its argument is real. The polynomial $S_m$ is the characteristic polynomial of a symmetric tridiagonal matrix $\mathcal J$ with edge

$$
c_j=\sqrt{2\sin(\pi j/N)}\exp(i[-\pi/4+\pi j/(2N)]),\quad1\le j<m.
$$

Write $\mathcal J=DR_0D$, where $R_0$ is real symmetric with the positive edge moduli, and $D_{jj}=e^{i\theta_j}$, $\theta_j=-\pi/8+\pi(2j+1)/(8N)$, $0\le j<m$. The edge phases add correctly. Since $-\pi/8<\theta_j<0$, $B=D^{-2}$ has strictly positive real and imaginary diagonal parts.

If $t\ne0$ were a real eigenvalue, a nonzero vector $v$ would satisfy $R_0v=tBv$. Then $v^*R_0v$ is real but $t v^*\operatorname{Im}(B)v\ne0$, impossible. For even $m$, the determinant at zero is a nonzero product of alternate squared edges. For odd $m$, the row recurrence makes the kernel of $R_0$ one-dimensional with a real generator $v_0$. In an orthonormal basis starting with that vector, the complementary block is invertible; the linear coefficient of $\det(R_0-tB)$ is a nonzero real factor times $v_0^TBv_0\ne0$. Thus zero is simple. The change of variable in (A.6) has nonzero derivative at $z=1$. It follows that the only possible unit-circle root is $1$, exactly as in (A.5). Galois automorphisms carry the algebraic gcd and its multiplicity to every primitive $q$. They are not used to preserve moduli of arbitrary roots. ∎

### Corollary A.4 Guard reduction at half residual degree

For $d\equiv3\pmod4$, $b=(d-1)/2$, and every $A\ge1$, squarefreeness of $H_b(z;\omega)$ alone implies all the hypotheses of Theorem 2.2.

**Proof.** Lemma A.3 gives a simple residual root $-1$ and $\operatorname{Res}(z^d+1,H_b/(z+1))\ne0$. Squarefreeness of $H_b$ gives $\operatorname{Disc}U\ne0$. Lemma A.1 puts $\tau\ne0$ on $|1-\tau|=1$, inside the disk in Lemma A.2 for every $A$. Hence $S_A\ne0$. ∎

This corollary is characteristic zero, at the stated half residual degree only. It proves neither its squarefreeness assumption for arbitrary composite $d$ nor any same-component condition after reduction. Source lineage: S24 §§4–5, independently reread and accepted in R06 §1 and R03 §2.

## References

External references below identify classical dependencies and comparison targets. Their reading status is inherited from P2109 and stated in EVIDENCE_CONCORDANCE.md. None is represented as newly retrieved in this finalization.

- **[Sagan92]** B. E. Sagan, “Congruence properties of q-analogs,” *Advances in Mathematics* 95 (1992), 127–143, Theorem 2.2, pp.131–132. [Author-hosted paper](https://users.math.msu.edu/users/bsagan/Papers/Old/cpq-pub.pdf).
- **[LS87]** D. S. Lubinsky and E. B. Saff, “Convergence of Padé approximants of partial theta functions and the Rogers–Szegő polynomials,” *Constructive Approximation* 3 (1987), 331–361. [DOI](https://doi.org/10.1007/BF01890574). The mathematical-body comparison is inherited; reference p.360 remains unavailable.
- **[SU19]** M. Sawa and Y. Uchida, “Discriminants of classical quasi-orthogonal polynomials with application to Diophantine equations,” *Journal of the Mathematical Society of Japan* 71(3) (2019), 831–860. Theorem 3.6, equation (3.6), pp.844–845. [Final paper](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf), [DOI](https://doi.org/10.2969/jmsj/79877987).
- **[SU18v1]** M. Sawa and Y. Uchida, “Discriminants of classical quasi-orthogonal polynomials, with combinatorial and number-theoretic applications,” arXiv:1802.00605v1, Theorem 4.8, equation (4.13). [Specified preprint version](https://arxiv.org/pdf/1802.00605v1). This is the version crosswalk for [SU19], not a second independent antecedent.
- **[IW01]** M. E. H. Ismail and N. S. Witte, “Discriminants and functional equations for polynomials orthogonal on the unit circle.” Ordinary and operator definitions (1.7), (5.12)–(5.13); Rogers–Szegő q-difference formula (5.17). [Primary preprint](https://arxiv.org/pdf/math/0012259).
- **[GGM16]** D. Gómez-Ullate, Y. Grandati and R. Milson, “Durfee rectangles and pseudo-Wronskian equivalences for Hermite polynomials,” Theorem 3.1. [Primary preprint](https://arxiv.org/pdf/1612.05514).
- **[GG20]** C. Grosu and C. Grosu, “The irreducibility of some Wronskian Hermite polynomials,” arXiv:2007.00065v1, Theorem 8. [Specified preprint version](https://arxiv.org/pdf/2007.00065v1).
- **[SZ97]** V. P. Spiridonov and A. S. Zhedanov, “Zeros and orthogonality of the Askey–Wilson polynomials for q a root of unity,” *Duke Mathematical Journal* 89 (1997), 283–305. [Primary preprint](https://arxiv.org/pdf/q-alg/9605034). This is distinct from [Z97].
- **[Z97]** A. S. Zhedanov, “Gauss sums and orthogonal polynomials,” *International Journal of Modern Physics A* 12 (1997), 289–294. [DOI](https://doi.org/10.1142/S0217751X97000438). Full-text comparison remains unresolved; no unverified theorem from it is used as a proof dependency.
- **[Sharifi]** R. Sharifi, *Algebraic Number Theory*, Chapter 3, Lemma 3.1.13 and Propositions 3.1.20–3.1.21. [Author notes](https://math.ucla.edu/~sharifi/notes/algnum-ch03.html). Standard cyclotomic ring and ramification background; the bridge above also gives its elementary polynomial proof.
