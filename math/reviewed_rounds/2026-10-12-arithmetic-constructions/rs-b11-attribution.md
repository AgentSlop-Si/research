Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical scope, attribution, limitations and review method are retained. Original source-report SHA-256: f998a66e23e35ebac91d86c8c6f7445da2610a0b11f1db79d02f2fc01ab60172.

Review date: 12 October 2026 UTC.

Degree eleven attribution addendum

Independent normalization verification October 2026 UTC

**Decision.** Accept the bounded prior-work comparison and its exact parity map. The local residue criterion follows from the identified classical discriminant and congruence identities with the additional unit argument below. This establishes an implication, not a first-publication claim. The accepted mathematical review remains unchanged; historical priority of the exact criterion and its Rogers–Szego application remains unresolved.

# 1 Source interface and uniform parity identities

Sawa and Uchida, *J. Math. Soc. Japan* 71 (2019), 831–860, Theorem 3.6, equation (3.6), printed pp. 844–845, give the quasi-Laguerre discriminant formula. Appendix A.2–A.3, p. 858, fixes the Laguerre and physicists’ Hermite conventions. The source is the [publisher paper](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf), DOI [10.2969/jmsj/79877987](https://doi.org/10.2969/jmsj/79877987).

For $F(u)=L_m^{(\alpha)}(u)+cL_{m-1}^{(\alpha)}(u)$, the needed formula is $$\operatorname{Disc}F=K_{m,\alpha}\frac{(-c)^mF(\xi)}{m+\alpha+mc},\qquad
 \xi=\frac{mc^2+(2m+\alpha)c+m+\alpha}{c},$$ $$K_{m,\alpha}=\prod_{j=1}^m j^{j-2m+3}
                  \prod_{j=1}^{m-1}(j+\alpha)^{j-1}.$$ At $\alpha=\pm1/2$, $K_{m,\alpha}$ is nonzero rational. The rational identity extends to the characteristic-zero parameters here. Theorem 3.8’s adjacent-Hermite family alone is not the required direct interface.

Our all-index calculation uses $u=x^2/2$, $C_m=(-1)^m2^m m!$ and the coefficient formulas for the polynomials. They yield $$\operatorname{He}_{2m}=C_mL_m^{(-1/2)}(u),\qquad
 \operatorname{He}_{2m-1}=C_{m-1}xL_{m-1}^{(1/2)}(u),$$ $$L_m^{(-1/2)}=L_m^{(1/2)}-L_{m-1}^{(1/2)},\qquad
 uL_{m-1}^{(1/2)}=(m-1/2)L_{m-1}^{(-1/2)}-mL_m^{(-1/2)}.$$ Substitution in $J_{A+1}=x\operatorname{He}_A-A\tau\operatorname{He}_{A-1}$ proves, for every $m\ge1$, $$\begin{aligned}
 A=2m:\quad J_{2m+1}
 &=C_mx\left[L_m^{(1/2)}(u)+(\tau-1)L_{m-1}^{(1/2)}(u)\right],\\
 A=2m-1:\quad J_{2m}
 &=C_m\left[L_m^{(-1/2)}(u)+\frac{2m-1}{2m}(\tau-1)L_{m-1}^{(-1/2)}(u)\right].
\end{aligned}$$ These are coefficient identities for arbitrary degree, not conclusions from bounded symbolic tests. Thus even $A$ uses $(\alpha,c)=(1/2,\tau-1)$; odd $A$ uses $(-1/2,A(\tau-1)/(A+1))$. Both give $$\xi=\frac{\tau(A\tau+1)}{2(\tau-1)}=\frac y2,
 \quad m+\alpha+mc=
 \begin{cases}(A\tau+1)/2,&A\text{ even},\\ A\tau/2,&A\text{ odd}.\end{cases}$$ There is no $m=0$ case when $A\ge1$.

# 2 Nonzero guards and the additional local argument

Suppose $\tau$ is integral at a prime above $3$, with residue $t\notin\mathbb F_3$. Then $\tau$, $\tau-1$, and $A\tau+1$ are local units for every integer $A$. Hence all divisions in $\xi$ are valid. The factors $C_m,c,K_{m,\alpha},m+\alpha+mc$ are nonzero in characteristic zero. They *need not be units at $3$*: $A$, $m$, factorials, or rational parameter denominators can involve $3$. We therefore do not reduce the Laguerre discriminant formula or its scaling factors modulo $3$.

The zero-root guard must also be retained. Directly from the Laguerre coefficients, $$F(0)=\frac{m+\alpha+mc}{m}\binom{m-1+\alpha}{m-1}.$$ The binomial factor is nonzero at $\alpha=\pm1/2$. Consequently $F(0)=0$ requires $\tau=0$ for odd $A$, or $\tau=-1/A$ for even $A$. The first has prime-field residue; the second is nonintegral if $3\mid A$ and has prime-field residue otherwise. At $m=1$, the two cases are exactly $J_2=x^2-\tau$ and $J_3=x(x^2-1-2\tau)$; the remaining Laguerre polynomial is linear, with discriminant one.

With $F(0)\ne0$, the quadratic substitution is unramified away from zero, and the extra $x$ for even $A$ is a simple root. Therefore $J$ is squarefree exactly when $F$ is squarefree. By the nonzero factors in Sawa–Uchida’s formula, it suffices to prove $F(\xi)\ne0$.

Let $x^2=y=\tau(A\tau+1)/(\tau-1)$ in an algebraic extension. Since $y$ is a unit, both $x$ and $x^{-1}$ are integral at an extended prime. Reduce the *original monic Hermite polynomial* $J$ at this nonzero $\bar x$.

Grosu and Grosu, [arXiv:2007.00065v1](https://arxiv.org/pdf/2007.00065v1), Theorem 31, printed p. 18, state and prove $\operatorname{He}_{n+M}\equiv x^M\operatorname{He}_n\pmod M$ for odd $M\ge3$, attributing the result to Carlitz. Page 2 fixes the monic probabilists’ normalization. This audit inspected that proof; the attribution to Carlitz is mediated through this source, not a claim to have inspected his original paper.

The case $M=3$ gives, with $A=3t_0+r$, $$\bar J=x^{3t_0}P_r(x),\quad
 P_0=x,\quad P_1=x^2-t,\quad P_2=x\bigl(x^2-(1+2t)\bigr).$$ At $x^2=\bar y$, these residual factors become $$r=0:\ \bar x;\qquad
 r=1:\ \frac{2t}{t-1};\qquad
 r=2:\ -\bar x.$$ All are nonzero. Thus $J(x)\ne0$ and, by the characteristic-zero parity identity, $F(\xi)\ne0$. This proves the criterion for every $A\ge1$. It does not claim good reduction of the full polynomial: for $A\ge3$ its reduction contains $x^{3\lfloor A/3\rfloor}$ and is not squarefree.

# 3 Verification scope and attribution guidance

The independent checker uses factorial coefficients for Hermite polynomials and the explicit generalized-binomial sum for Laguerre polynomials. It runs 91 exact checks: full parity identities and zero-value formulas through $m=12$, the two contiguous identities, symbolic formulas for $\xi$ and the scalar denominators with arbitrary $m$, equation (3.6) through $m=5$ for each $\alpha$, all three reduced critical evaluations, and the two smallest sizes. These checks confirm normalization; the all-index coefficient argument and residue calculation provide the uniform proof. No candidate or prior-comparison program is executed or imported.

**Permitted description.** The characteristic-three residue criterion is an explicit local-arithmetic consequence of classical quasi-Laguerre discriminant and Hermite congruence identities, with an elementary unit argument, applied to the specified Rogers–Szego parameter. The modular block identities are classical. The exact parity reduction supplies the relevant classical discriminant interface.

**Unresolved priority.** The inspected sources do not expressly state the exact number-field criterion in this form. This bounded comparison does not establish absence elsewhere. Neither the exact criterion nor the order-25 application receives a novelty or first-publication designation. Mathematical correctness of the accepted degree-eleven theorem is unaffected.

**Scope.** Accepted degree-eleven mathematics and its higher-degree overlap and ordinary-residual boundaries remain unchanged. This attribution addendum does not close unrelated source-access gaps or establish historical priority.

**Immutable review binding.** The accepted review archive remains

<div class="center">

`RS_B11_Middle_Overlap_Independent_Review_ACCEPT_2026-10-12.zip`

</div>

with SHA-256

<div class="center">

`3a398beac4f6ca47f2ddc76e4061c9d22e62bf0efb29144321d7631230caea00`.

</div>

This addendum is a separate sealed artifact. The candidate archive remains bound to

<div class="center">

`e0ecd3e0fb869f10f64a2f2598e46c86b4c905da303cd61c2fa76141cc510688`.

</div>

**Source-record limits.** The source locators and reading depth are recorded in `SOURCE_MAP.json`. Web-extracted theorem text and the polynomial conventions were checked directly. The browser’s screenshot retrieval failed, so no claim of visual inspection of the original article pages is made. No full-paper byte identity is asserted or full third-party paper republished. The local comparison report and accepted archive are independently hash-bound in `INPUT_PINS.json`.
