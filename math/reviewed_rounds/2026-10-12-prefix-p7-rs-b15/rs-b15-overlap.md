Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical proof, source attribution, limitations and review method are retained. Original source-report SHA-256: 13f35e2c0ed8348b19070552bd712c659a83612e4678793b0af10de3af85cc7c.

Review date: 12 October 2026 UTC.

Rogers–Szego overlap for b=15 independent review

Accepted mathematical scope 12 October 2026 UTC

**Decision.** ACCEPT the frozen candidate for every odd $d=33,35,\ldots,119$ and every integer $A\ge1$, in characteristic zero. The $29$ residue cases and $16$ annulus witnesses covering the other $15$ orders are complete. The $d=33$ witnesses genuinely cover different size regimes. No finite-size extrapolation, numerical approximation, or squarefree-reduction assumption is needed. The independently reconstructed normalization and exact certificates agree with the candidate.

**Frozen input.** `RS_B15_Middle_Overlap_CANDIDATE_FINAL_2026-10-12.zip`, SHA-256

<div class="center">

`98aea53653d198b5f03ded3039b80bf30836f8e0fd0a9852c94be0731bf088bc`

</div>

Its $34$ manifest entries and $9$ archived source pins were rechecked. The source author’s replay is supplementary evidence; the new reviewer program imports neither candidate nor predecessor programs.

# 1 Original definitions and normalization

For a primitive odd order-$d$ root $q$ and $b=15$, the original definitions are $$H_{15}(z;q)=\sum_{j=0}^{15}{15\brack j}_qz^j=(1+z)U(z),\qquad
 g=H'_{15}(-1),\qquad W=\frac{(q;q)_{15}}{(q^2;q^2)_{(d+15)/2}},$$ $$\tau=\frac{dW}{g},\qquad J_{A+1}(x;\tau)=x\operatorname{He}_A(x)-A\tau\operatorname{He}_{A-1}(x).$$ The normalization is the monic probabilists’ recurrence $\operatorname{He}_{n+1}=x\operatorname{He}_n-n\operatorname{He}_{n-1}$. The integer $15$ is the Rogers–Szego degree; $J$ has degree $A+1$.

Put $m=7$, $h=(d-1)/2$, $E=(q^2;q^2)_h$, $s_j=(q;q^2)_j/(q^2;q^2)_j$ and $S_r=\sum_{j=0}^rs_j$. Differentiating the Gaussian degree recurrence at $-1$ gives $$g_m=(q;q^2)_m+(1-q^{2m})g_{m-1},\qquad g_0=1.$$ Consequently $g=(q^2;q^2)_7S_7$. At degree $d$, the interior Gaussian coefficients vanish and the two endpoint coefficients are $1$, so $H_d=1+z^d$ and $ES_h=d$. Cancellation of precisely the odd factors with exponents $1,3,\ldots,15$ gives $$W=(q^2;q^2)_7/E,\qquad \tau=d/(ES_7)=S_h/S_7.$$ Every original denominator is nonzero since its relevant exponent is nonzero modulo $d$.

The reviewer constructed $H_{15}$ over $\mathbb Z[q]$ and checked the derivative-prefix identity as an unrestricted polynomial identity. For each of the $44$ orders, fresh arithmetic modulo $\Phi_d$ in characteristic zero verifies the uncancelled $W$ identity, the degree-$d$ derivative $d$, and nonzero original denominators and $g$. This checks the sign, factor $d$, and polynomial degree before any reduction modulo $3$.

# 2 Uniform local arithmetic proof

Let $\tau$ be integral at a prime of a number field above $3$, with residue $t\notin\mathbb F_3$. The quantities $\tau$, $\tau-1$ and $A\tau+1$ are units for every integer $A$. Indeed, if $A$ has residue $0$, the last residue is $1$; otherwise its vanishing would put $t$ in the prime field.

At zero, the Hermite constant terms and derivatives give the exact possible multiple-root parameters: $\tau=0$ for odd $A$ and $\tau=-1/A$ for even $A$. The latter is not integral when $3\mid A$; otherwise its residue is in $\mathbb F_3$. Thus neither is permitted.

For a nonzero multiple root, the recurrence shows consecutive Hermite polynomials cannot vanish together. The equations $J=J'=0$ therefore give $$J'=(1+A\tau)\operatorname{He}_A+Ax(1-\tau)\operatorname{He}_{A-1},\qquad
 x^2=\frac{\tau(A\tau+1)}{\tau-1}=y.$$ Since $y$ is a unit, both $x$ and $x^{-1}$ are integral over the local ring. After extending the prime to the field containing $x$, its residue $\bar x$ is defined and nonzero. Ramification in this extension does not harm the argument: a unit remains a unit.

The recurrence in characteristic $3$ proves, by complete three-step blocks for every $u\ge0$, $$\operatorname{He}_{3u}=x^{3u},\qquad \operatorname{He}_{3u+1}=x^{3u+1},\qquad
 \operatorname{He}_{3u+2}=x^{3u}(x^2-1).$$ The block closes because $x(x^2-1)-2x=x^3$ in characteristic $3$. Thus, for $A=3u+r$, the reductions of $J,J'$ are $x^{3u}P_r,x^{3u}P'_r$, where $$P_0=x,\qquad P_1=x^2-t,\qquad P_2=x^3-(1+2t)x.$$ At $\bar x\ne0$, respectively $P_0\ne0$, $P'_1=2\bar x\ne0$, or $P'_2=t-1\ne0$. Simultaneous vanishing is impossible. This is an all-$A$ proof, including $3\mid A$ and both parity classes.

**Important limit.** The reduction of the entire $J$ usually has a large repeated zero factor. The argument never asserts squarefree reduction. Its essential point is that a hypothetical nonzero characteristic-zero multiple root must reduce to a unit. Nor are factorial or Laguerre scaling constants assumed to be local units.

# 3 Nonreality and all size annulus

In the principal embedding, put $v=\pi/d$. Each $s_j=a_je^{-ijv}$ has $a_j>0$. Since $hv<\pi/2$, $S_7$ has positive real part and $$\operatorname{Im}((S_h-S_7)\overline{S_7})
 =-\sum_{j=8}^h\sum_{r=0}^7a_ja_r\sin((j-r)v)<0.$$ Hence $\tau$ is nonreal. Cyclotomic conjugacy preserves the nonzero algebraic difference $\tau-\bar\tau$, because the cyclotomic Galois group commutes with conjugation. It need not preserve the sign or a numerical norm bound.

For a hypothetical nonzero multiple root and $A\ge3$, rewrite the critical equation as $$y=A\tau+(A+1)+\frac{A+1}{\tau-1}.$$ Write $A+1=2r+s$, $s\in\{0,1\}$, and $\alpha=s-1/2$. The Hermite coefficient formula or the monic Laguerre recurrence gives $$J=x^s\det(x^2I-M),$$ where $M$ is complex symmetric tridiagonal, with diagonal $4j+2\alpha+2$ for $0\le j<r$, off-diagonal entries $2\sqrt{j(j+\alpha)}$ for $1\le j<r$, and the additional last diagonal term $A(\tau-1)$.

All off-diagonals are nonzero. Backward elimination therefore proves that every eigenvector has a nonzero last coordinate and that the eigenspace is one-dimensional. Since the nonzero root $x$ is multiple, $y=x^2$ is a repeated eigenvalue; the quadratic substitution is unramified there. A Jordan chain supplies $(M-yI)w=v$. Symmetry yields $v^Tv=0$. In particular $$0<t_0=\frac{|v_r|^2}{\|v\|^2}\le\frac12.$$ The Hermitian inner product of $Mv=yv$ gives $\operatorname{Im}y=A\operatorname{Im}\tau\,t_0$. Combining this with the critical equation and cancelling $\operatorname{Im}\tau\ne0$ proves $$1+\frac1A<|\tau-1|^2\le2+\frac2A.$$ The strict lower bound uses $t_0>0$; the weak upper bound allows equality. The argument does not assume diagonalizability. The identities $J_2=x^2-\tau$ and $J_3=x(x^2-1-2\tau)$ give only the real exceptions $0,-1/2$. The zero-root exceptions for arbitrary $A$ are also real, so nonreality handles all of them.

At $d=33$, the $k=16$ embedding has $1004/1000\le\rho\le1005/1000<4/3$, excluding $A=3$. The different $k=14$ embedding has $2601/1000\le\rho\le2602/1000$, exceeding $5/2$ and excluding every $A\ge4$. For all the other fourteen orders divisible by $3$, the certified lower bound exceeds $8/3$, excluding every $A\ge3$ at once. The two low sizes are already covered.

For fixed $A$, the discriminant is a polynomial in $\tau$ with rational coefficients. A vanishing value would vanish at every primitive conjugate. Therefore the use of different embeddings for the two $d=33$ regimes is valid. No norm inequality is transported between embeddings.

# 4 Fresh arithmetic and structural audit

The new reviewer program independently constructs $\tau$ from the uncancelled $W$ and the original $H'_{15}(-1)$ in the full ring $\mathbb F_3[q]/(\Phi_d)$. For each of the $29$ orders coprime to $3$, it proves the full denominator and $\tau^3-\tau$ are units. This is stronger than testing one selected factor: it verifies the prime-field exclusion at every prime above $3$ for these bounded orders. The saved irreducible field moduli and saved residues are also checked against this full-ring route.

The reviewer derives the reduced $S_7=N/D$ from the original derivative, recovering $\deg N=\deg D=33$ and $\deg(N^8-qD^8)=265$. All $88$ full polynomial Bezout identities in the structural supplement are re-evaluated, with fresh gcd computations as well. The proof $$E(q)E(q^{-1})=d,\quad E(q^{-1})=(-1)^hq^{-h(h+1)}E(q)
 \quad\Longrightarrow\quad E^8=q^{-1}$$ is valid modulo $3$ when $3\nmid d$, because $4h(h+1)=d^2-1$ and $d^4=1$. It implies $t^8S_7^8=q$. A nonzero prime-field residue would force $S_7^8=q$, which the obstruction Bezout identities exclude. These are bounded results, not an unbounded-order classification.

For $d=3^ae$, $3\nmid e$, fresh computations check $\Phi_d\bmod3=(\Phi_e\bmod3)^{2\cdot3^{a-1}}$ for all $15$ remaining orders. Reduction loses the $3$-power part of the root order. The factor indexed by $j=e$ in $E$ vanishes. Thus the exact-order field certificate and its denominator inversions cannot be used. The candidate’s “$0/0$” language describes this failed naive reduction; any prefix quotient with vanishing denominator must first be cleared or interpreted locally. It supplies no proof against a more refined ramified argument. The accepted proof uses characteristic-zero annuli for these orders.

For the $16$ complex witnesses, the independent interval evaluator uses $448$-bit outward-rounded integer endpoints and the different identity $$\pi=4\left(\arctan\frac12+\arctan\frac13\right).$$ Each arctangent has $300$ alternating terms with a signed next-term enclosure. Separate cosine and sine Taylor polynomials of degrees $240$ and $241$ use integral-remainder bounds. The evaluator forms the original Gaussian product quotients and original $W$ directly, then independently evaluates the prefix expression. All complex denominator norms have positive lower bounds. The new exact intervals fit inside the saved candidate boxes, and all stated rational annulus inequalities pass.

The new program also checks the exact Hermite congruence through index $40$ and the Jacobi matrix, derivative, and classical parity identities through $A=24$. These are normalization controls only; the preceding induction and Jordan-chain proof establish all $A$.

**Replay evidence.** The inspected producer reruns byte-identically. The candidate’s separate checker repeats $7{,}682$ checks and rejects its $10$ mutations; its structural checker repeats $914$ checks and $88$ Bezout identities. All $3{,}544$ new reviewer checks and four negative controls pass. The results are recorded in `reviewer_output/INDEPENDENT_EXACT_REPORT.json`. The reviewer archive is re-extracted into a new directory and its programs rerun before the external seal is issued. Historical programs remain inert throughout. No network or external write occurs in any mathematical replay.

# 5 Classical attribution and limits

Fresh source-body checks confirm that Grosu and Grosu, [arXiv:2007.00065v1](https://arxiv.org/pdf/2007.00065v1), Theorem 31, printed p. 18, state and prove the odd-modulus Hermite congruence with attribution to Carlitz. Their p. 2 fixes the monic probabilists’ convention. Carlitz’s original paper was not inspected.

Fresh source-body checks also confirm Sawa and Uchida, [J. Math. Soc. Japan 71 (2019), 831–860](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf), Theorem 3.6, equation (3.6), printed pp. 844–845, as the quasi-Laguerre discriminant interface. With $u=x^2/2$ and $C_m=(-1)^m2^mm!$, the verified parity maps are $$J_{2m+1}=C_mx\{L_m^{(1/2)}(u)+(\tau-1)L_{m-1}^{(1/2)}(u)\},$$ $$J_{2m}=C_m\left\{L_m^{(-1/2)}(u)+\frac{2m-1}{2m}(\tau-1)L_{m-1}^{(-1/2)}(u)\right\}.$$ The local criterion is an explicit local-arithmetic consequence of these classical ingredients together with the unit argument. Its direct proof also stands without invoking the published discriminant formula. The accessed passages do not establish first publication of the exact criterion or its Rogers–Szego application. Historical priority remains unresolved. Source text was inspected; the web screenshot service failed, so this review makes no claim to have visually inspected the publisher pages or to bind their full bytes.

# 6 Cumulative scope and remaining domains

The accepted lower range $15<d\le31$ and accepted general tail $d\ge15(15+1)/2=120$ cover every odd order outside the newly proved strip. Thus the cumulative overlap result is every odd $d>15$ and every $A\ge1$. The separately accepted ordinary squarefreeness, nonvanishing, and separation results imply all four guards for $b=15$. These older conclusions are imported through the pinned accepted reports, not presented as new computations.

The new theorem holds in any characteristic-zero field containing such $q$: the map from the corresponding cyclotomic number field is injective, so the nonzero discriminant remains nonzero. No embedding of the entire base field into $\mathbb C$ is needed.

The cumulative accepted full families are $b=1,3,5,7,9,11,13,15$. The broader guard problem remains open; no historical-priority conclusion follows. The separate remaining domains are:

- Overlap: odd $b\ge17$ and odd $2b+1<d<15(b+1)/2$, except separately proved instances. The next fixed strip is $b=17$, odd $d=37,39,\ldots,133$.

- Ordinary residual squarefreeness: odd $b\ge27$ and odd $b<d<4b^2$, except separately proved instances. Accepted ordinary ranges remain odd $b\le25$ for all odd $d>b$, and odd $b\ge3$ with odd $d\ge4b^2$.

- Even order, nonprimitive roots, $A=0$, positive-characteristic theorems, quantitative conditioning, and historical priority remain outside this acceptance.

In particular $\operatorname{Disc}_xJ\ne0$ is not itself a proof of $\operatorname{Disc}_zU\ne0$. Reduction modulo $3$ is a proof device for the characteristic-zero theorem. No broader mathematical or implementation conclusion follows from this review.
