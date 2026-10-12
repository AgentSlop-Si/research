Public derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical statements, source attribution, review method and remaining limitations are retained. Original source-report SHA-256: 740e2f556f51900c70ab92c7e63d2809eeae2ffec394999e6b6bd343e4c455e1.

Review date: 12 October 2026 UTC.

Independent review of Rogers–Szego overlap for b=17

The sixteen ramified middle orders and the full b=17 family

**ACCEPT** October 2026 UTC

**Decision.** Accept the candidate’s original characteristic-zero overlap theorem for $$\mathcal D=\{39,45,51,57,63,69,75,81,87,93,99,105,111,117,123,129\},$$ every primitive order-$d$ root, and every integer $A\ge1$. The independently accepted unramified input and lower/tail strips then complete the $b=17$ family for *every odd $d>17$*. No mathematical repair is required. All sixteen witnesses were rebuilt by a fresh arithmetic implementation, with 6,801 positive checks and 34 rejected controls. No candidate or predecessor program was executed.

This is a degree-family closure. The broader guard problem remains open; higher-degree overlap, the separate ordinary-residual problem, and historical priority remain unresolved.

# 1 Original normalization and every denominator

For $q$ of exact odd order $d>17$, put $$H_{17}(z;q)=\sum_{j=0}^{17}{17\brack j}_qz^j=(z+1)U(z),\qquad g=H'_{17}(-1;q)=U(-1),$$ $${17\brack j}_q=\frac{\prod_{r=1}^{17}(1-q^r)}{\prod_{r=1}^j(1-q^r)\prod_{r=1}^{17-j}(1-q^r)},\quad
W=\frac{\prod_{r=1}^{17}(1-q^r)}{\prod_{r=1}^{(d+17)/2}(1-q^{2r})},\quad \tau=\frac{dW}{g}.$$ The original overlap polynomial is $$J_{A+1}(x;\tau)=x\operatorname{He}_A(x)-A\tau\operatorname{He}_{A-1}(x),\qquad
\operatorname{He}_0=1,\ \operatorname{He}_1=x,\ \operatorname{He}_{n+1}=x\operatorname{He}_n-n\operatorname{He}_{n-1}.$$ Both $q$ and $q^2$ have order $d$. Every original product length is below $d$, so its factors are nonzero. Set $h=(d-1)/2$ and $$B_8=\prod_{r=1}^8(1-q^{2r}),\quad E=\prod_{r=1}^h(1-q^{2r}),\quad
s_j=\prod_{r=1}^j\frac{1-q^{2r-1}}{1-q^{2r}},\quad S_t=\sum_{j=0}^t s_j.$$ Gaussian coefficient comparison gives $H_{n+1}=(1+z)H_n-(1-q^n)zH_{n-1}$. At $z=-1$, differentiation gives $$g_m:=H'_{2m+1}(-1)=(q;q^2)_m+(1-q^{2m})g_{m-1},\qquad g_0=1.$$ Dividing by $B_m=(q^2;q^2)_m$ and summing yields $g=B_8S_8$. At degree $d$, all interior Gaussian coefficients vanish, so $H_d=1+z^d$ and $ES_h=d$. The factors after $E$ in the original denominator of $W$ have exponents $d+1,d+3,\ldots,d+17$. Cancelling exactly the odd numerator factors gives $$\boxed{\quad W=B_8/E,\qquad \tau=d/(ES_8)=S_h/S_8.\quad}$$ No sign, factor $d$, or Hermite scaling has changed. The fresh verifier independently divides the exact Gaussian product polynomials, differentiates, and verifies these identities in every $\mathbb Q[q]/(\Phi_d)$ for $d\in\mathcal D$.

# 2 Nonreality and the all-index annulus

In the principal embedding put $v=\pi/d$, $q=e^{2iv}$. Then $$s_j=a_je^{-ijv},\qquad a_j=\prod_{r=1}^j\frac{\sin((2r-1)v)}{\sin(2rv)}>0.$$ Since $hv<\pi/2$, $\Re S_8>0$, so $g\ne0$. Also, writing $T=S_h-S_8$, $$\Im(T\overline{S_8})=-\sum_{j=9}^h\sum_{r=0}^8a_ja_r\sin((j-r)v)<0.$$ Thus $\tau$ is nonreal. Cyclotomic automorphisms commute with conjugation, so $\tau-\overline\tau\ne0$ remains nonzero at every primitive embedding. This transfers nonreality, not a sign or norm inequality.

**Critical-parameter lemma.** For $A\ge3$ and nonreal $\tau$, a multiple root of $J_{A+1}$ forces $$\boxed{\quad 1+\frac1A<|\tau-1|^2\le2+\frac2A\le\frac83.\quad}$$ At zero, the exceptional parameters are $\tau=0$ for odd $A$, and $\tau=-1/A$ for even $A$; Hermite’s constant coefficients prove this directly. Both are excluded. At a nonzero multiple root $x$, consecutive Hermite factors cannot vanish together, by descending the recurrence to $\operatorname{He}_0=1$. Since $A\tau x\ne0$, both factors used below are nonzero. Differentiation and elimination give $$J'=(1+A\tau)\operatorname{He}_A+Ax(1-\tau)\operatorname{He}_{A-1},\qquad
 y=x^2=\frac{\tau(A\tau+1)}{\tau-1}
 =A\tau+(A+1)+\frac{A+1}{\tau-1}.$$ Write $A+1=2r+s$, $s\in\{0,1\}$, $\alpha=s-1/2$. The factorial formula $$\operatorname{He}_n(x)=n!\sum_{j=0}^{\lfloor n/2\rfloor}\frac{(-1)^jx^{n-2j}}{2^jj!(n-2j)!}$$ proves the parity recurrence $P_0=1$, $P_1=y-(2\alpha+2)$ and $$P_{j+1}=(y-(4j+2\alpha+2))P_j-4j(j+\alpha)P_{j-1},\qquad
\operatorname{He}_{2j+s}=x^sP_j(x^2).$$ Since $J=\operatorname{He}_{A+1}+A(1-\tau)\operatorname{He}_{A-1}$, this proves $J=x^s\det(x^2I-M)$ for every index. Here $M=M_0+A(\tau-1)e_re_r^T$; $M_0$ is real symmetric with diagonal $4j+2\alpha+2$, $0\le j<r$, and off-diagonal $2\sqrt{j(j+\alpha)}$, $1\le j<r$.

The nonzero multiple root gives a repeated eigenvalue $y$. All off-diagonals are nonzero; backward recurrence shows that the eigenspace has dimension one and $v_r\ne0$. A repeated eigenvalue with this geometric multiplicity has a Jordan chain $(M-yI)w=v$. As $M$ is complex symmetric, $$v^Tv=v^T(M-yI)w=((M-yI)v)^Tw=0,\qquad
0<t=\frac{|v_r|^2}{\|v\|^2}\le\frac12.$$ The separate Hermitian inner product gives $\Im y=A\Im\tau\,t$. For $\rho=|\tau-1|^2$, the rational expression for $y$ gives $At=A-(A+1)/\rho$. Division by $\Im\tau$ is valid; $0<t\le1/2$ proves the claimed bounds. No diagonalizability is assumed.

For $A=1,2$, the exact discriminants are $4\tau$ and $4(1+2\tau)^3$; their exceptional parameters are real. Therefore one nonreal witness with $\rho>8/3$ excludes multiple roots for *all* $A\ge1$.

# 3 Sixteen independently certified conjugates

At $q=e^{2\pi ik/d}$, the following are exact closed rational enclosures $L/1000\le\rho\le U/1000$. Every $\gcd(d,k)=1$ and every $3L>8000$.

<div class="center">

| $d$ | $k$ |   $L$ |   $U$ | $d$ | $k$ |   $L$ |   $U$ |
|----:|----:|------:|------:|----:|----:|------:|------:|
|  39 |  17 |  3063 |  3064 |  87 |  13 | 14207 | 14208 |
|  45 |  17 |  5325 |  5326 |  93 |  14 | 14691 | 14692 |
|  51 |  11 |  5839 |  5840 |  99 |  47 | 21340 | 21341 |
|  57 |  25 | 20353 | 20354 | 105 |  23 | 19618 | 19619 |
|  63 |   4 |  8557 |  8558 | 111 |  49 | 19793 | 19794 |
|  69 |  31 | 10227 | 10228 | 117 |  46 | 17474 | 17475 |
|  75 |  17 |  9891 |  9892 | 123 |  55 | 17928 | 17929 |
|  81 |   4 | 11540 | 11541 | 129 |  28 | 20005 | 20006 |

</div>

The tightest lower margin is $3063/1000-8/3=1189/3000>0$ at $d=39$, $k=17$.

**Why one conjugate suffices.** For each fixed $A$, $D_A(T)=\operatorname{Disc}_xJ_{A+1}(x;T)\in\mathbb Q[T]$. If it vanished at any primitive conjugate of $\tau$, a cyclotomic automorphism would make it vanish at the tabulated one. The lemma contradicts this for every $A$. Norm bounds are never transported through an automorphism. Any characteristic-zero field containing the given root receives an injective image of its cyclotomic field, preserving the nonzero discriminant; the whole field need not embed in $\mathbb C$.

**Independent rational arithmetic.** The new verifier represents complex numbers by a dyadic center $c$ and one radius $r$, guaranteeing $|z-c|_1\le r$, at 768-bit precision. It uses a third identity $$\pi=4\{2\arctan(1/3)+\arctan(1/7)\}.$$ The tangent of $2\arctan(1/3)$ is $3/4$, and adding $\arctan(1/7)$ gives tangent one in the first quadrant. Each 320-term alternating arctangent sum is bounded by its first omitted term. A degree-340 exponential polynomial at the resulting angle ball is enlarged by the exact integral-remainder bound $2\theta_{\max}^{341}/341!$ in $\ell^1$ norm.

For centers $c,d$ and radii $r,s$, multiplication uses the radius $$|c|_1s+|d|_1r+rs$$ plus exact outward-rounding errors. For inversion, $m=\max(|\Re c|,|\Im c|)>r$ is checked first. Since $|c|_2\ge m$ and $|z|_2\ge m-r$, $$|z^{-1}-c^{-1}|_1\le\frac{2r}{m(m-r)}.$$ Every center operation is rational with outward dyadic rounding. Squared-norm error is bounded by $2|c|_1r+r^2$. These estimates need no floating-point assumptions.

The verifier forms original Gaussian product quotients, $H'_{17}(-1)$, uncancelled $W$, and $dW/g$, as well as both reduced parameter routes. All original denominators exclude zero: 1,016 fresh division guards pass. The new enclosures fit *inside* the saved author intervals for every complex quantity and all three norm routes. Thus the frozen endpoints themselves are validated, rather than merely obtaining overlapping numerical approximations.

# 4 Cumulative closure and inherited inputs

The pinned accepted general-prime review proves $b=17$ overlap for every odd $d>17$ with $3\nmid d$, and every $A\ge1$. Its characteristic-three argument is explicitly unramified. Its complete obstruction factorization and distinct residual degrees $13,93,128,141$ rule out full cyclotomic divisibility: the odd degrees cannot equal $\varphi(d)$, and an odd $d$ coprime to three cannot have $\varphi(d)=128$. This is an unbounded structural theorem, not a scan over $d$.

The present review imports that accepted theorem on exactly its proved domain. No field of characteristic three has an element with multiplicative order divisible by three. At ramified orders both $d$ and factors of $E$ reduce to zero; $d/(ES_8)$ cannot be treated as an automatically defined inverse. The new sixteen-order proof takes place wholly in characteristic zero.

**Lower strip.** The accepted general odd-guards review proves overlap for $b<d\le2b+1$. Its principal-embedding reflection identity is $$|\tau-1|^2=\frac{|S_{h-m-1}|^2}{|S_m|^2},\qquad b=2m+1.$$ The positive-sector summands make $|S_j|^2$ strictly increasing, so $h-m-1\le m$ gives $\rho\le1$, below the annulus. At $b=17$ this includes precisely odd $19\le d\le35$.

**Upper strip.** The accepted degree-nine review proves the general improved tail $d\ge15(b+1)/2=15(m+1)$. Telescoping sine products and $\sin u>131u/135$ for $0<u<2\pi/15$ yield $$|S_m|^2<\frac{270}{131}(m+1),\qquad
|\tau|^2>\frac{131d}{270(m+1)}\ge\frac{131}{18}.$$ The exact positive comparison $(101/18)^2-4(131/18)=769/324$ proves $(\sqrt{131/18}-1)^2>8/3$. Hence $b=17$ is covered at every odd $d\ge135$.

The remaining 49 odd orders $37\le d\le133$ partition into the 33 accepted coprime-to-three orders and the sixteen orders of this review. There is no missing endpoint. Therefore $$\boxed{\operatorname{Disc}_xJ_{A+1}(x;\tau)\ne0\quad\text{for every odd }d>17\text{ and every }A\ge1.}$$ Accepted ordinary squarefreeness for odd $b\le25$, general $g\ne0$, and general $\operatorname{Res}_z(1+z^d,U)\ne0$ supply the other degree-seventeen guards. Their accepted status is retained; none follows solely from the new overlap calculation.

**Retained open work.** Full accepted odd overlap families now include $b=1,3,5,7,9,11,13,15,17$. The remaining general overlap region is odd $b\ge19$, odd $2b+1<d<15(b+1)/2$, except separately proved instances. The next untouched family starts with $b=19$ and odd $d=41,43,\ldots,149$.

Ordinary residual squarefreeness remains separately accepted for odd $b\le25$ at all odd $d>b$, and odd $b\ge3$ at $d\ge4b^2$. Its remaining region is odd $b\ge27$, $b<d<4b^2$, except separately proved instances. Even orders, nonprimitive roots, $A=0$, positive-characteristic theorems, quantitative conditioning, and historical priority are not certified.

**Attribution.** The annulus method and classical Hermite–Laguerre/Jacobi background are inherited from the pinned degree-fifteen and earlier accepted reviews. Their Sawa–Uchida attribution and the separate unramified Carlitz/Grosu–Grosu attribution are preserved. No fresh primary-paper inspection or historical-priority determination is made here. The seal establishes evidence identity and reviewed scope, not novelty.

# 5 Evidence binding and controls

The reviewed candidate ZIP is pinned by SHA-256

<div class="center">

`fe3eba252fff2ca3e586a9599d8d9059a66852287bef3c185f729c85d38b5c22`.

</div>

The inherited accepted unramified archive is pinned by

<div class="center">

`e1a457a85dfbd30e1910d70850255dc155f3450078c3ae721f4306e3db7cfa69`.

</div>

All 31 candidate manifest entries, 12 source pins, nested source copies, and ZIP CRCs pass. The accepted reviews are bound to their archived bytes. This review also retains the candidate author’s cold report and delivery receipt as provenance, without treating either as independent acceptance.

The 6,801 positive checks include byte/provenance validation, exact rational enclosures, direct Gaussian polynomial division, characteristic-zero cyclotomic normalization, denominator coprimality, and factorial/Jacobi diagnostics for $1\le A\le40$. These finite diagnostics do not supply the infinite quantifier: Section 2 does.

The 34 negative controls reject wrong Rogers–Szego or Hermite degrees, finite-$A$ scope, ramified separable reduction, missing or duplicated orders, a wrong scale or $\pi$ interval, nonprimitive roots, omission of $A=3$, a missing factor $d$, conjugation/sign corruption, wrong original $g$ or $W$ denominator, a substituted prefix, forged norm/coarse bounds, a zero denominator record, invalid ball inverses, duplicate/nonfinite JSON, unsafe archive paths, nonregular archive entries, changed proof bytes, and unmanifested payloads.

The source programs were inspected as text before any local calculation. Only newly written reviewer programs are executed. The final review archive contains the immutable candidate, fresh verifier and results, this proof, hashes, and replay program. Cold replay checks the sealed ZIP, validates its payload, runs the archive-contained fresh verifier against the archive-contained candidate, and requires exact result-byte identity. Its independently hashed report lives outside the ZIP to avoid self-reference.
