Public derivative of a source-bound reviewed research report. Private tracking and delivery details are omitted; mathematical claims, evidence, source attribution and remaining limits are retained. Original source-report SHA-256: 2f8aa2dbde1c4e80cfdba1e936183d2cee4771023d29c144733cb4d9e0538ff5.

Review date: 12 October 2026 UTC.

Independent review of the general RS prime criterion

Rogers–Szego parameter b=17 at every unramified odd order

ACCEPT for the precise scope below 12 October 2026 UTC

**Decision.** The sealed candidate’s sufficient one-prime criterion, finite-exception corollary, degree-seventeen unramified family, and bad-prime example are mathematically valid. A fresh standard-library verifier passes 348 checks and rejects 17 corrupted inputs or invalid uses. The author and predecessor mathematical programs were neither read nor executed. No mathematical repair is required.

For odd $b=2m+1$, let $$S_m(X)=\sum_{j=0}^m\prod_{r=1}^j\frac{1-X^{2r-1}}{1-X^{2r}}=\frac{N_m(X)}{D_m(X)}\in\mathbb F_3(X),
 \quad (N_m,D_m)=1,\quad D_m\text{ monic},$$ $$P_m=N_m^8-XD_m^8.$$ For every primitive odd order $d>b$ with $3\nmid d$, the condition $$(\Phi_d\bmod3)\nmid N_mP_m
 \tag{1}$$ is sufficient for the characteristic-zero original overlap polynomial to have nonzero discriminant for *every* integer $A\ge1$. Condition (1) holds for $b=17$ at *every* such $d>17$, with no upper bound on $d$.

This does not prove the whole $b=17$ family. Combining inherited lower and upper strips, the remaining middle orders are exactly $$39,45,51,57,63,69,75,81,87,93,99,105,111,117,123,129.$$ All sixteen are divisible by three. The broader guard problem remains open. Ordinary residual squarefreeness is unchanged and separate.

# 1 Original parameter and the local theorem

Let $q$ have exact odd order $d>b$ in a characteristic-zero field. Set $$H_b(z;q)=\sum_{j=0}^b{b\brack j}_qz^j,
 \quad g=H'_b(-1;q),\quad
 W=\frac{(q;q)_b}{(q^2;q^2)_{(d+b)/2}},\quad \tau=\frac{dW}{g}.$$ The original monic overlap polynomial is $$J_{A+1}(x;\tau)=x\operatorname{He}_A(x)-A\tau\operatorname{He}_{A-1}(x),
 \quad \operatorname{He}_{n+1}=x\operatorname{He}_n-n\operatorname{He}_{n-1}.$$ All product lengths in $W$ are below $d$. With $h=(d-1)/2$ and $E=\prod_{j=1}^h(1-q^{2j})$, direct product cancellation and the Gaussian recurrence give $$B_m=\prod_{j=1}^m(1-q^{2j}),\quad g=B_mS_m(q),\quad W=B_m/E,
 \quad \tau=\frac{d}{E S_m(q)}. \tag{2}$$ The original Gaussian derivative was independently reconstructed from the finite Euler product; cancellation has not altered its normalization.

**Local lemma.** If $\tau$ is integral at a prime above three with residue $t\notin\mathbb F_3$, then $\operatorname{Disc}J_{A+1}\ne0$ for every $A\ge1$.

Indeed, $\tau$, $\tau-1$ and $1+A\tau$ are all units, by considering the three residues of $A$. A repeated zero root would require $\tau=0$ for odd $A$ or $\tau=-1/A$ for even $A$. The latter is nonintegral when $3\mid A$ and otherwise has prime-field residue; both cases are excluded.

At a nonzero multiple root, descending the Hermite recurrence excludes a common root of consecutive Hermite polynomials. Differentiating the original monic $J$ gives $$J'=(1+A\tau)\operatorname{He}_A+Ax(1-\tau)\operatorname{He}_{A-1},
 \quad x^2=\frac{\tau(1+A\tau)}{\tau-1}. \tag{3}$$ The right side is a local unit. At any extended prime, both $x$ and $x^{-1}$ are integral, so $\bar x\ne0$. The Hermite recurrence modulo three, proved in three-step blocks, gives $$\operatorname{He}_{3u}=x^{3u},\quad \operatorname{He}_{3u+1}=x^{3u+1},\quad
 \operatorname{He}_{3u+2}=x^{3u}(x^2-1).$$ For $A=3u+r$, $\bar J=x^{3u}R_r$ with $$R_0=x,\quad R_1=x^2-t,\quad R_2=x^3-(1+2t)x.$$ At $\bar x\ne0$, either $R_0\ne0$, $R'_1=2\bar x\ne0$, or $R'_2=t-1\ne0$. This excludes a common root of $\bar J$ and $\bar J'$, proving the lemma. This argument is uniform in $A$; finite-size checks do not provide that quantifier.

The unit step (3) is indispensable: for $A=3$, $\bar J_4=x^4$ has a repeated zero. No squarefree reduction of the whole polynomial is asserted. No factorial or Laguerre normalization scalar is silently inverted modulo three.

# 2 Separability and the existential quantifier

For $3\nmid d$, $X^d-1$ is separable over $\mathbb F_3$. Its cyclotomic decomposition shows that the roots of $C_d=\Phi_d\bmod3$ have exact order $d$ and that $C_d$ is squarefree. Thus (1) is equivalent to an irreducible factor $f\mid C_d$ avoiding $N_mP_m$. It is *not* equivalent to coprimality of $C_d$ and $N_mP_m$.

Take a root $Q$ of that factor. Since $D_m$ divides $B_m$, and all original product exponents are nonzero modulo $d$, every required original product denominator is a unit at the corresponding cyclotomic prime above three. Since $N_m(Q)\ne0$, the original $g$ is a unit. Formula (2) therefore gives a well-defined nonzero residue $$t=d\{E(Q)S_m(Q)\}^{-1}.$$ The sets $\{2j:1\le j\le h\}$ and $\{-2j:1\le j\le h\}$ partition the nonzero residues modulo odd $d$. Hence $$E(Q)E(Q^{-1})=d,\quad E(Q^{-1})=(-1)^hQ^{-h(h+1)}E(Q).$$ Since $4h(h+1)=d^2-1$ and $d^4=1$ in $\mathbb F_3$, $$E(Q)^8=Q^{-1},\qquad t^8 S_m(Q)^8=Q. \tag{4}$$ A nonzero prime-field $t$ would have $t^8=1$, forcing $P_m(Q)=0$. The chosen factor forbids this. The local lemma now applies in $\mathbb Q(q)$, and an injective field extension to the specified characteristic-zero field preserves nonvanishing.

**Limits of the test.** A factor with $P_m(Q)=0$ need not have $t\in\mathbb F_3$: equation $t^8=1$ allows elements outside the prime field. The test is sufficient and may miss a good prime. Conversely, $N_m(Q)=0$ obstructs integrality of the original parameter when the numerator is a unit. These are distinct reasons a particular prime fails the test.

**Finite exceptions.** At infinity the $j$th summand in $S_m$ has leading order $X^{-j}$; the $j=0$ term is one. Thus $r_m=\deg N_m=\deg D_m\le m(m+1)$ and $\deg(N_mP_m)=9r_m+1$. If $\varphi(d)>9r_m+1$, divisibility is impossible. For odd $d$, prime-factor multiplication of $$\frac{\varphi(p^a)^2}{p^a}=p^{a-2}(p-1)^2\ge1$$ gives $d\le\varphi(d)^2$. Thus uncertified unramified orders for any fixed $b$ lie in $d\le(9r_m+1)^2$. This bounds failures of the sufficient criterion, not actual multiple-root exceptions.

# 3 Why the degree seventeen conclusion is unbounded

Fresh polynomial arithmetic gives $\deg N_8=\deg D_8=50$, $\deg P_8=401$, and the complete identities $$\begin{aligned}
 N_8&=X(X-1)^6\Phi_5 F_{10}F_{13}F_{16},\\
 P_8&=-X\Phi_{11}\Phi_{13}\Phi_{17}F_{93}F_{128}F_{141}.
\end{aligned}$$ Each $F_j$ is monic irreducible of degree $j$; all residual multiplicities are one. The verifier checks every irreducible factor, including the split cyclotomic pieces, by Rabin’s criterion. It verifies $$X^{1342}=-1\pmod{F_{10}},\qquad X^{21523360}=-1\pmod{F_{16}},$$ so these factors have even-order roots.

If $C_d\mid N_8P_8$ for an odd $d>17$ coprime to three, its factors cannot come from $X$, order-one roots, the displayed low-order cyclotomic factors, or $F_{10},F_{16}$. The only choices left have distinct degrees $13,93,128,141$. All irreducible factors of $C_d$ have the same degree $\operatorname{ord}_d(3)$, because Frobenius sends a primitive root $Q$ to $Q^3$. Consequently $C_d$ would be just one of these four factors.

For $d>2$, $\varphi(d)$ is even, excluding singleton degrees $13,93,141$. If $\varphi(d)=128$, every odd prime $\ell\mid d$ satisfies $\ell-1\mid128$, so $\ell\in\{3,5,17\}$. No odd prime power beyond the first is possible, since that prime would then divide 128. With $3\nmid d$, only products of 5 and 17 remain, and their totients are at most 64. This excludes the degree-128 case and proves (1) for every permitted $d$.

The factorization supplies a finite exact certificate for a structural argument. No cutoff on $d$, no finite-$A$ extrapolation, and no factorization of $3^{141}-1$ is involved.

# 4 Counterexamples to stronger interpretations

The factor $$F_{13}=X^{13}-X^{12}-X^{11}-X^{10}-X^8+X^7-X^6-X^2-1$$ is independently irreducible. Exact trial division proves $797161$ prime, and modular powering verifies $$X^{797161}=1\pmod{F_{13}},\quad X\ne1\pmod{F_{13}}.$$ Its roots therefore have exact order $797161$. At the corresponding degree-thirteen prime in the cyclotomic field, $N_8(Q)=0$, $D_8(Q)\ne0$, and the original $B_8,W,d$ are units. Thus $g=B_8S_8$ has positive valuation and $v(\tau)<0$. This is a genuine counterexample to the assertion that *every* prime above three is good. It is not a squarefreeness counterexample: $\varphi(797161)=797160>451$, so another prime satisfies the sufficient test.

For $d=3^ae$, $a\ge1$ and $3\nmid e$, reduction has exact order $e$, and $$\Phi_d\bmod3=(\Phi_e\bmod3)^{2\cdot3^{a-1}}.$$ Here $e\le(d-1)/2$, so $E$ contains a factor that vanishes after reduction, and $d$ also reduces to zero. The displayed inverse in (2) is not automatically legitimate. At $d=39$, the fresh verifier confirms $\Phi_{39}=\Phi_{13}^2$ modulo three and a nonunit $E$. The odd exact-order, separable argument cannot be reused without justified ramified arithmetic.

Two further logical negative controls are explicit. With $C=(X-1)^2$ and $T=X-1$, $C\nmid T$ although every distinct factor of $C$ divides $T$; separability cannot be dropped. In $\mathbb F_3[i]$, $i^2=-1$ gives $i^8=1$ but $i^3\ne i$; the eighth-power condition has no prime-field converse.

# 5 Independent computation and evidence binding

The fresh verifier uses only Python’s standard library. It expands $$\prod_{r=0}^{b-1}(1+q^rz)=\sum_j q^{j(j-1)/2}{b\brack j}_qz^j$$ with integer coefficients, removes the exact monomial shifts, and differentiates at $z=-1$. It separately clears the complete even denominator in the rational prefix. The two constructions agree for $m=0,\ldots,12$, including $b=17$. These finite controls supplement the written general proof.

All three complete factor products, canonical coefficients, scalar factors, multiplicities, and Rabin irreducibility checks are rebuilt. Quotient-ring inverses are computed by Euclid and checked by multiplication, without assuming a cyclotomic quotient is a field. At $d=19,25,35,37,65$, the program independently reconstructs the original Gaussian quotients, original $W$, and $dW/g$, then checks (2), (4), and the critical local units. Additional finite-order checks through 201 are labeled corroboration only.

The 17 rejected controls cover original-domain boundaries, ramification, nonunit inverses, reducible moduli, wrong characteristic or degree, invalid coefficients, corrupted numerator and obstruction, missing high-degree factor, wrong factor scalar, and altered multiplicity. Formal Hermite recurrence controls include the repeated reduction $J_4=x^4$.

The candidate ZIP has SHA-256

<div class="center">

`41de36b91e94c5882f1ce8d0d3a53b12a2df2baadb8039b792b3264971e21491`.

</div>

Its 16 manifest entries and ZIP CRC were verified. The independent input certificate and theorem source are byte-identical to the sealed candidate. The review archive includes the immutable candidate, fresh verifier, exact results, integrity verifier and proof sources. Cold replay uses only archive-contained files and executes no author mathematical program.

# 6 Classical sources and the accepted additions

Grosu and Grosu, [arXiv:2007.00065v1](https://arxiv.org/pdf/2007.00065v1), p. 2, fix the monic probabilists’ Hermite convention. Theorem 31 on printed p. 18 gives the odd-modulus congruence, attributes it to Carlitz, and includes a proof. Those passages were freshly inspected through the primary paper. Carlitz’s original body was not inspected.

Sawa and Uchida, [J. Math. Soc. Japan 71 (2019), 831–860](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf), Theorem 3.6 and equation (3.6), printed pp. 844–845, give the classical quasi-Laguerre discriminant formula. This passage was freshly inspected. The present direct local proof does not need that formula; its normalization and attribution remain relevant inherited context. Nonzero characteristic-zero Laguerre scalars need not be local units.

The accepted additions relative to the degree-fifteen baseline are the correctly existential obstruction criterion, its fixed-degree finite-exception corollary, the unbounded degree-seventeen unramified theorem, and the explicit counterexample to universal-prime wording. They are exact derivations reviewed here. Historical priority of this exact criterion and RS application remains unresolved. There is no first-publication or worldwide-novelty determination.

# 7 Cumulative scope and retained open work

The accepted b15 source archive is pinned by SHA-256

<div class="center">

`478d927042eebaa16d5c03f54bbe535269221db296634a61cc89645346d9b7d1`.

</div>

Of the 49 odd middle orders $37\le d\le133$, 33 are now discharged and 16 remain. The broader guard problem remains open. Retain full accepted odd-degree families $b\le15$, the $b=17$ lower strip $17<d\le35$, and the tail $d\ge135$.

The next unresolved overlap task is the sixteen ramified orders listed on the first page, with every $A\ge1$. The broader overlap remainder is odd $b\ge19$ with $2b+1<d<15(b+1)/2$, except separately proved instances. Ordinary residual squarefreeness remains accepted for odd $b\le25$ at all odd $d>b$, and for odd $b\ge3$ at $d\ge4b^2$; its remaining general strip is odd $b\ge27$, $b<d<4b^2$, except separately proved instances.

Even orders, nonprimitive roots, $A=0$, a positive-characteristic theorem, quantitative conditioning, and priority remain separate. No historical-priority determination follows. The seal certifies reviewed bytes and evidence, not novelty.
