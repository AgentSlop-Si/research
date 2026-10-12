Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematics, source attribution, limitations and review method are retained. Original source-report SHA-256: a19dd555bfa7538596997dbea7a93b8c79018f83e623fde62c4840f158ae2f88.

Review date: 12 October 2026 UTC.

Rogers–Szegő overlap for b=13 independent review

Accepted bounded theorem 12 October 2026 UTC

**Decision. ACCEPT** the final frozen candidate for every odd $29\le d\le103$, every integer $A\ge1$, in characteristic zero. All 38 orders are covered: 26 exact residue-field certificates and 12 rigorous conjugate-annulus certificates. A fresh checker reconstructs all finite evidence, and the reviewed infinite-index arguments cover every $A$. No mathematical repair is required.

Only the final archive was reviewed:

<div class="center">

`RS_B13_Middle_Overlap_CANDIDATE_FINAL_2026-10-12.zip`  
SHA-256 `1544c2e7c27a183aa5398ae4911287705b26e1bfbb0574bf7cd527232a1348c9`.

</div>

The obsolete packaging draft is not the review target. All 31 manifest entries and nine source pins match the final extracted bytes. Each of those nine source pins also matches its separately existing local source. Candidate and historical programs were neither executed nor imported.

# 1 Exact theorem and original normalization

Let $q$ have exact odd order $d>13$ in a characteristic-zero field. The source normalization is $$H_{13}(z;q)=\sum_{j=0}^{13}{13\brack j}_qz^j=(z+1)U(z),\quad
 g=U(-1)=H'_{13}(-1),$$ $${13\brack j}_q=\frac{(q;q)_{13}}{(q;q)_j(q;q)_{13-j}},\qquad
 W=\frac{(q;q)_{13}}{(q^2;q^2)_{(d+13)/2}},\quad \tau=\frac{dW}{g},$$ $$J_{A+1}(x;\tau)=x\operatorname{He}_A(x)-A\tau\operatorname{He}_{A-1}(x),\qquad
 \operatorname{He}_{n+1}=x\operatorname{He}_n-n\operatorname{He}_{n-1},\quad \operatorname{He}_0=1,\quad\operatorname{He}_1=x.$$ The accepted assertion is $\operatorname{Disc}_xJ_{A+1}(x;\tau)\ne0$. This overlap discriminant is distinct from the ordinary residual discriminant $\operatorname{Disc}_zU$.

Put $h=(d-1)/2$, $E=(q^2;q^2)_h$, $s_j=(q;q^2)_j/(q^2;q^2)_j$, and $S_r=\sum_{j=0}^r s_j$. Differentiating the Gaussian degree recurrence at $-1$ yields $$g_m=(q;q^2)_m+(1-q^{2m})g_{m-1},\quad g_0=1,
 \qquad g=(q^2;q^2)_6S_6.$$ At degree $d$, Gaussian polynomial specialization gives $H_d=1+z^d$, hence $ES_h=d$. The last factors in the denominator of $W$ are the odd factors through exponent 13. Therefore $$W=(q^2;q^2)_6/E,\qquad \tau=S_h/S_6=d/(ES_6).$$ Every product length is below $d$, and $q^2$ has order $d$. No product denominator vanishes. In the principal embedding, $s_j=a_je^{-ij\pi/d}$ with $a_j>0$ and $h\pi/d<\pi/2$; thus $S_6\ne0$. The imaginary part of $(S_h-S_6)\overline{S_6}$ is a strictly negative sum. Consequently $\tau$ is nonreal. Cyclotomic conjugacy transports this algebraic nonreality, not a sign or metric inequality.

# 2 Residue proof for all sizes

The accepted degree-eleven local criterion applies to the newly reconstructed degree-thirteen parameter. Let $\mathfrak p$ be above 3 and suppose $\tau$ is integral there with residue $t\notin\mathbb F_3$. A multiple root at zero requires $\tau=0$ when $A$ is odd, or $\tau=-1/A$ when $A$ is even. The former has prime-field residue; the latter is nonintegral if $3\mid A$ and otherwise has prime-field residue. Neither occurs.

If $x\ne0$ is a multiple root, consecutive Hermite polynomials cannot vanish together, by descending their recurrence to $\operatorname{He}_0=1$. The equations $J=J'=0$ give $$J'=(1+A\tau)\operatorname{He}_A+Ax(1-\tau)\operatorname{He}_{A-1},\qquad
 x^2=\frac{\tau(A\tau+1)}{\tau-1}.$$ Because $t\notin\mathbb F_3$, each of $\tau$, $\tau-1$, and $A\tau+1$ is a local unit for every integer $A$. Thus both $x$ and $x^{-1}$ are integral at an extended prime: the nonzero multiple root must reduce to a nonzero element.

The exact all-index characteristic-three recurrence yields $$\operatorname{He}_{3u}=x^{3u},\quad \operatorname{He}_{3u+1}=x^{3u+1},\quad
 \operatorname{He}_{3u+2}=x^{3u}(x^2-1)\pmod3.$$ For $A=3u+r$, write $\bar J=x^{3u}P_r$, where $$P_0=x,\qquad P_1=x^2-t,\qquad P_2=x^3-(1+2t)x.$$ At a nonzero reduced root, respectively $P_0\ne0$, $P'_1=2x\ne0$, or $P'_2=t-1\ne0$. This contradicts simultaneous reduction of $J=J'=0$ and proves the criterion for *every* $A\ge1$.

**Essential limitation.** The whole reduction of $J$ generally has a factor $x^{3\lfloor A/3\rfloor}$ and is not squarefree. The unit argument excludes a characteristic-zero multiple root from that bad-reduction factor. Neither full good reduction nor a positive-characteristic theorem is asserted.

# 3 Exact finite fields and original products

For every $d$ below, a fresh standard-library polynomial engine verifies a monic modulus over $\mathbb F_3$, all Rabin prime-divisor conditions and full polynomial Bezout identities, terminal Frobenius, cyclotomic divisibility, and exact order of $Q=X\bmod f_d$. It independently verifies every even-denominator inverse, $E$, $S_6$, $S_h$, $D=ES_6$, $D^{-1}$, $t=dD^{-1}$, $(t^3-t)^{-1}$, and all three critical-unit cases.

<div class="center">

| $d$ | $\deg f$ | $\deg t$ | $d$ | $\deg f$ | $\deg t$ | $d$ | $\deg f$ | $\deg t$ | $d$ | $\deg f$ | $\deg t$ |
|----:|---------:|---------:|----:|---------:|---------:|----:|---------:|---------:|----:|---------:|---------:|
|  29 |       28 |       27 |  47 |       23 |       22 |  65 |       12 |       10 |  85 |       16 |       15 |
|  31 |       30 |       28 |  49 |       42 |       41 |  67 |       22 |       21 |  89 |       88 |       85 |
|  35 |       12 |       10 |  53 |       52 |       51 |  71 |       35 |       34 |  91 |        6 |        4 |
|  37 |       18 |       17 |  55 |       20 |       18 |  73 |       12 |       10 |  95 |       36 |       31 |
|  41 |        8 |        6 |  59 |       29 |       28 |  77 |       30 |       29 |  97 |       48 |       46 |
|  43 |       42 |       41 |  61 |       10 |        9 |  79 |       78 |       77 | 101 |      100 |       99 |
|     |          |          |     |          |          |  83 |       41 |       40 | 103 |       34 |       33 |

</div>

The checker forms the original Gaussian coefficients by *product quotients*, separately reconstructs the finite Euler product and checks its $Q^{j(j-1)/2}$ factor, differentiates at $-1$, and evaluates the uncancelled $W$. The resulting $dW/g$ matches the full saved residue vector in every case. Every original denominator is proved nonzero. Since $t$ is nonconstant of degree below $\deg f_d$, the local criterion applies. One prime above 3 suffices for the characteristic-zero algebraic conclusion.

# 4 Annulus proof for the other twelve orders

For a nonreal multiple-root parameter and $A\ge3$, the reviewed necessary bound is $$1+\frac1A<\rho:=|\tau-1|^2\le2+\frac2A\le\frac83.$$ Here is the uniform argument. Write $A+1=2r+s$, $s\in\{0,1\}$, $\alpha=s-1/2$. The monic Hermite–Laguerre coefficient identity realizes $J$ as $x^s\det(x^2I-M)$, with real unperturbed Jacobi diagonal $4j+2\alpha+2$, off-diagonals $2\sqrt{j(j+\alpha)}$, and last diagonal perturbation $A(\tau-1)$.

Every off-diagonal is nonzero. Thus each eigenspace is one-dimensional and its last coordinate is nonzero. A repeated eigenvalue $y=x^2\ne0$ has a Jordan chain. Complex symmetry then gives $v^Tv=0$. Hence $$0<t_0=\frac{|v_r|^2}{\|v\|^2}\le\frac12.$$ Taking imaginary parts of the Hermitian inner product in $Mv=yv$, and using $$y=A\tau+(A+1)+\frac{A+1}{\tau-1},$$ gives $At_0=A-(A+1)/\rho$, exactly the claimed strict lower and weak upper bounds. No diagonalizability assumption is made. For $A=1,2$, the only exceptional parameters are the real numbers $0,-1/2$; a multiple zero root in any size likewise requires a real parameter.

The independent checker uses 640-bit outward dyadic intervals, exact rational alternating arctangent enclosures for $\pi$, and sine/cosine Taylor polynomials at $\theta/16$, followed by four complex squarings. It does not reuse the candidate’s exponential evaluator. Taylor remainder bounds are rational. Every real reciprocal excludes zero and every complex division has a strictly positive squared-norm lower bound.

All independently computed $q,E,S_6,S_h,g,\tau$ and norm enclosures are contained in the saved 320-bit enclosures, including *three* routes: $d/(ES_6)$, $S_h/S_6$, and the original Gaussian-product $dW/g$. Independent norm widths are below $2^{-320}$. The controls enclose $q^d=1$, $|E|^2=d$, and $ES_h=d$.

<div class="center">

| $d$ | $k$ |   $L$ |   $U$ | $d$ | $k$ |   $L$ |   $U$ |
|----:|----:|------:|------:|----:|----:|------:|------:|
|  33 |   7 |  3668 |  3669 |  69 |  29 | 20661 | 20662 |
|  39 |  17 |  4485 |  4486 |  75 |  16 | 15034 | 15035 |
|  45 |  16 |  7351 |  7352 |  81 |  34 | 24637 | 24638 |
|  51 |  11 |  8975 |  8976 |  87 |  38 | 17643 | 17644 |
|  57 |  25 | 10112 | 10113 |  93 |  10 | 17142 | 17143 |
|  63 |  22 | 10805 | 10806 |  99 |   5 | 17792 | 17793 |

</div>

Here $q=e^{2\pi ik/d}$, $\gcd(k,d)=1$, and $L/1000\le\rho\le U/1000$. Every $L/1000>8/3$. Thus all $A\ge3$ are excluded simultaneously, and nonreality handles $A=1,2$. For each fixed $A$, $\operatorname{Disc}_xJ_{A+1}(x;T)\in\mathbb Q[T]$; vanishing would persist under every cyclotomic embedding. One certified conjugate outside the annulus suffices. The metric inequality itself is not transported.

# 5 Verification record and classical attribution

The main independent checker passes **15,174 exact checks**. Ten deliberate corruptions are rejected: missing residue order, changed residue coefficient, wrong denominator inverse, wrong irreducibility Bezout coefficient, missing Rabin prime, reversed original-parameter sign, false norm interval, nonprimitive embedding, false root enclosure, and missing annulus order. These controls check that coverage and normalization fail closed.

The auxiliary audit passes **264 normalization and evidence-consistency checks**, including: Hermite derivatives, the critical derivative identity, zero-root formulas, Jacobi normalizations for both parities, the exact Hermite–Laguerre maps, characteristic-three blocks, degree-thirteen prefix identity, source and evidence consistency. Finite symbolic tests support the normalization only. Sections 2 and 4 supply the infinite-$A$ proofs.

The classical ingredients retain the accepted degree-eleven attribution:

- Grosu and Grosu, *The irreducibility of some Wronskian Hermite polynomials*, [arXiv:2007.00065v1](https://arxiv.org/pdf/2007.00065v1), Theorem 31, printed p. 18, prove the Hermite congruence with attribution to Carlitz. No fresh inspection of Carlitz’s original body is claimed.

- Sawa and Uchida, *J. Math. Soc. Japan* 71 (2019), 831–860, [Theorem 3.6, equation (3.6)](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf), provide the quasi-Laguerre discriminant interface. The relevant parity map, with $C_m=(-1)^m2^m m!$ and $u=x^2/2$, is $$J_{2m+1}=C_mx\bigl[L_m^{(1/2)}(u)+(\tau-1)L_{m-1}^{(1/2)}(u)\bigr],$$ $$J_{2m}=C_m\bigl[L_m^{(-1/2)}(u)+\tfrac{2m-1}{2m}(\tau-1)L_{m-1}^{(-1/2)}(u)\bigr].$$

This review checks the source-bound accepted attribution addendum and independently reconfirms its normalization. It does not claim a fresh full-paper review or full-paper byte identity. The criterion is an explicit local-arithmetic consequence of classical ingredients together with the additional unit argument. Factorials and rational Laguerre scalings need not be units above 3; the proof reduces the original monic Hermite polynomial, not a rationally rescaled discriminant formula.

**Priority remains unresolved.** Neither this criterion nor its Rogers–Szego applications is assigned first-publication status. No novelty, rank, canonical identity count or priority promotion follows from this acceptance.

# 6 Cumulative scope and remaining domains

The 26 residue orders and 12 annulus orders are disjoint and exhaust every odd $d=29,31,\ldots,103$. Accepted general guards supply $13<d\le27$; the accepted sharper general tail supplies $d\ge15(13+1)/2=105$. These three ranges exhaust all odd $d>13$. Hence degree thirteen has all-order, all-$A\ge1$ overlap nonvanishing.

The separately accepted ordinary residual theorem covers every odd $b\le25$ and all odd $d>b$. Together with accepted general $g\ne0$ and $\operatorname{Res}_z(1+z^d,U)\ne0$, all four guards now hold for $b=1,3,5,7,9,11,13$. The imported ordinary and tail theorems are source-verified and used as accepted inputs; their historical computations are not rerun.

An arbitrary characteristic-zero field containing a primitive order-$d$ root receives an injective map from $\mathbb Q(\zeta_d)$, so the nonzero discriminants remain nonzero. No embedding of the whole base field into $\mathbb C$ is needed.

# 7 Remaining domains

Overlap remains open for odd $b\ge15$ and odd $2b+1<d<15(b+1)/2$, except separately proved instances. Ordinary residual squarefreeness remains separately accepted for odd $b\le25$, all odd $d>b$, and odd $b\ge3$, odd $d\ge4b^2$; its remaining general strip is odd $b\ge27$, $b<d<4b^2$, except separately proved instances. Even orders, nonprimitive roots, $A=0$, positive-characteristic theorems, quantitative conditioning and historical priority are not certified.

The next overlap strip is $b=15$, odd $d=33,35,\ldots,119$; this is a remaining problem, not a theorem about that strip. Preserve the classical attribution and local-unit qualifications above. The review’s sealed cold replay repeats the complete finite-field and rational-interval audit with all ten mutations. No requested order or size remains unresolved inside the accepted $b=13$ middle strip.
