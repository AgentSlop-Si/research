# F020: an all-order implication from the finite q-binomial theorem

11 October 2026 UTC. Provisional new implication proof, pending independent review. Existing manuscript correctness acceptance is unchanged. No historical anticipation or first-publication claim is made.

## Decision in brief

The arbitrary-A separated and one-simple-overlap leading forms can be derived from the classical finite q-binomial theorem, a first-order product calculation, and the classical value of the Rogers–Szegő polynomial at −1. An all-order weighted-remainder argument explains why no unexplored list of high q derivatives is necessary. The full ordinary-discriminant coefficients then follow by the usual root-product calculation.

This proves an explicit elementary-corollary route in the present audit, rather than locating these displayed formulas in an earlier publication. It does not prove that the particular corollary, packaging, or applications have previously appeared. The needed intermediate observation is a short block-divisibility and differential-operator lemma, fully proved below; it is not an appeal to an unstated all-order derivative theorem.

## 1. Conventions and exact hypotheses

Work in characteristic zero. Fix an odd integer d≥3, a primitive dth root ω, A≥1 and 0≤b<d. Set n=Ad+b, F(z)=1+z^d, G(z)=H_b(z;ω), and

H_n(z;q)=Σ_(k=0)^n [n choose k]_q z^k.

D_n(q) is its monic ordinary z-discriminant. Use Disc(1)=1. Let q=ωe^h and, at the end, h=log(1+ε²)/d, so q=ω(1+ε²)^(1/d) exactly. Write D=z∂_z and L=D(D−1)=z²∂_z².

For the separated discriminant assume Disc(G)Res(F,G)≠0. For the shared-root form assume b odd and G=(z+1)U with g=U(−1)≠0. Define

W=(ω;ω)_b/(ω²;ω²)_((b+d)/2),  τ=dW/g,

J_(A+1)(y;τ)=He_(A+1)(y)+A(1−τ)He_(A−1)(y).

Here He is monic probabilists' Hermite. The overlap discriminant additionally requires Disc(U)Res(F,U)Disc(J)≠0; in particular the resultant already implies g≠0. No finite-characteristic conclusion is part of this proof.

## 2. Exact diagonal-operator identity

The classical finite q-binomial theorem is

P_n(z;q):=∏_(j=0)^(n−1)(1+q^jz)=Σ_k q^(k(k−1)/2)[n choose k]_q z^k.

Define T_ω(z^k)=ω^(k(k−1)/2)z^k and R_n(z,h)=T_ω^(−1)P_n(z;ωe^h). Coefficientwise,

H_n(z;ωe^h)=exp(−hL/2)R_n(z,h).                         (2.1)

This is a formal power-series identity on the finite-dimensional space of polynomials of degree at most n. The exponential is not a truncation, and no analytic convergence is invoked.

For odd d, T_ω commutes with multiplication by z^d and hence by F. Indeed the multiplier ratio between z^(k+d) and z^k is ω^[dk+d(d−1)/2]=1. In particular

R_n(z,0)=F(z)^A G(z).                                  (2.2)

This also rederives the static q-Lucas specialization in the present normalization.

## 3. All-order block-divisibility lemma

Write R_n(z,h)=Σ_(r≥0)h^r R_(n,r)(z). For every r≥0,

F^max(A−r,0) divides R_(n,r) in Q(ω)[z].                (3.1)

Proof: group the first Ad factors of P_n into A consecutive d-factor blocks. At h=0 every intact block equals F. In any term of the rth product derivative, at most r blocks have been differentiated. Thus at least A−r full blocks remain intact if r≤A. Apply T_ω^(−1), which commutes with every power of F. Factorials do not affect divisibility. This proves the statement for all r at once.

At a root α of F let u=z−α, and assign weights wt(u)=1 and wt(h)=2. A term h^r R_(n,r) has weighted order at least

2r+max(A−r,0).

Thus every r≥1 term has weight at least A+1, and every r≥2 term has weight at least A+2. These inequalities also hold when r>A. The operator hL=h(α+u)²∂_u² never decreases weighted order. Therefore exp(−hL/2) preserves both remainder bounds. On a weighted leading term it reduces to exp(−hα²∂_u²/2). Each fixed weighted degree requires only finitely many terms, so this filtration argument is formal and well-defined.

This is the all-order justification absent from a fixed cubic jet: high derivatives of P_n cannot contribute at the required weight, even though high powers of the heat operator do contribute. Both effects are explicitly accounted for.

## 4. Separated leading form for every A

Since F'(α)=−d/α, the weight-A part of R_n at α is

(−d/α)^A G(α)u^A.

All positive-r terms have strictly larger weight by §3. With h=ε²/d+O(ε⁴) and u=εx, (2.1) gives

H_n(α+εx;q(ε))
=ε^A(−1)^A d^(A/2)G(α)He_A(√d x/α)+O(ε^(A+1)).    (4.1)

The standard identity exp(−s∂_u²/2)u^A=s^(A/2)He_A(u/√s) follows by the Hermite exponential generating series, or by expanding the finite sum. Apparent square roots cancel coefficientwise. The identity (4.1) holds even if G(α)=0, but then it is not the first nonzero term.

## 5. One shared root: the first derivative reduces to A=1

Let E_b(z)=∏_(r=0)^(b−1)(1+ω^r z), and set

S(z)=Σ_(r=0)^(d−1) rω^r z ∏_(0≤s<d,s≠r)(1+ω^s z),

S_b(z)=Σ_(r=0)^(b−1) rω^r z ∏_(0≤s<b,s≠r)(1+ω^s z).

Differentiating the d-blocks and final b-block once gives the exact identity

∂_h P_n(z;ωe^h)|_(h=0)
=F^(A−1){A E_b S + [d²A(A−1)/2]z^d E_b}
 +F^A{Ad D E_b+S_b}.                                  (5.1)

T_ω^(−1) commutes with F and z^d. Since G(−1)=0, the second summand inside braces has an additional zero at −1 after applying T_ω^(−1). The final F^A term is also irrelevant to weight A+1 after multiplication by h. Hence, if

c_b=(T_ω^(−1)(E_b S))(−1),

then at u=z+1 the only weight-(A−1) term of R_(n,1) is A d^(A−1)c_b u^(A−1).

To evaluate c_b use A=1. From (2.1),

R_(d+b,1)=∂_h H_(d+b)(z;ωe^h)|_0 +(L/2)[FG].

At z=−1, (L/2)[FG]=dg, since FG=dg u²+O(u³). As d+b=2m is even and m<d, the classical special value gives

H_(2m)(−1;q)=(q;q²)_m=(q;q)_(d+b)/(q²;q²)_m.

The numerator has exactly one vanishing factor at ω. Consequently

H_(d+b)(−1;ωe^h)=−d²W h+O(h²),

and therefore

c_b=dg−d²W=dg(1−τ).                                   (5.2)

All r≥2 terms have weight at least A+2 by §3. The static part F^A G has weight-(A+1) term d^A g u^(A+1). Thus the complete weight-(A+1) part of R_n is

d^A g {u^(A+1)+A(1−τ)h u^(A−1)}.                      (5.3)

Applying the leading heat operator at α=−1 and substituting h=ε²/d yields

H_n(−1+εx;q(ε))
=ε^(A+1)d^((A−1)/2)g J_(A+1)(√d x;τ)+O(ε^(A+2)).    (5.4)

By the parity of J this equals the manuscript's form

ε^(A+1)(−1)^(A+1)d^((A−1)/2)g J_(A+1)(−√d x;τ).

Thus every A is controlled by the same A=1 special-value correction together with the all-order block lemma. This proof neither assumes the target overlap formula nor substitutes it as derivative input.

## 6. Full ordinary-discriminant normalization

Put P_A=∏_(j=1)^A j^j. The elementary Hermite identity is Disc(He_A)=P_A. Under the separated guards, formal simple-root lifting of (4.1) gives A branches at each root α of F, with displacements αh_j/√d, and b residual branches. The within-cluster product contributes ε^[dA(A−1)]d^[−dA(A−1)/2]P_A^d. The cross-cluster product contributes Disc(F)^(A²), with Disc(F)=(−1)^((d−1)/2)d^d. Residual factors contribute Disc(G)Res(F,G)^(2A). Consequently, for K=dA(A−1)/2,

D_n(q(ε))=ε^(2K){C_sep+O(ε²)},

C_sep=(−1)^(A(d−1)/2)d^[dA(A+1)/2]P_A^d Disc(G)Res(F,G)^(2A).   (6.1)

Under the overlap guards the shared cluster has A+1 displacements, −j_k/√d, while the other d−1 clusters have A. Put L_ov=dA(A−1)/2+A. The within-cluster contribution is ε^(2L_ov)d^(−L_ov)P_A^(d−1)Disc(J). With F_0=F/(z+1), Disc(F_0)=(−1)^((d−1)/2)d^(d−2) and F_0(−1)=d. Cross-cluster factors give (−1)^(A(d−1)/2)d^(dA²+2A). Residual factors give Disc(U)Res(F,U)^(2A)g². Hence

D_n(q(ε))=ε^(2L_ov){C_ov+O(ε²)},

C_ov=(−1)^(A(d−1)/2)d^[dA(A+1)/2+A]P_A^(d−1)Disc(J)Disc(U)Res(F,U)^(2A)g².   (6.2)

The products are nonzero precisely under the stated guards, establishing exact orders. The normalized remainder is even because q(ε) and D_n(q(ε)) are even series. Monicity is retained throughout.

For M=K or L_ov and t=q^d−1, the coefficient is C in D_n=t^M(C+O(t)). In q−ω it is (dω^(d−1))^M C. Let Q_d(q)=(q^d−1)/Φ_d(q). Galois conjugacy and monic division give D_n=Φ_d^M E with E∈Z[q], and

E(ω)=Q_d(ω)^M C.                                      (6.3)

No q-difference discriminant is substituted, and no unit condition is inferred in positive characteristic.

## 7. What this changes, and what it does not

The prior statement that fixed cubic q-binomial data do not by themselves yield arbitrary A remains correct. The inference that arbitrary A requires computing arbitrarily many new q-binomial coefficient derivatives is too strong: (2.1) and (3.1) reduce the relevant product data to order zero and one. This audit provides the missing worked implication from a classical exact identity, including the shared-root constant and all normalizations.

Recommended mathematical positioning, subject to independent review: “We derive the fixed-root first-displacement formulas and their normalized ordinary-discriminant consequences from the finite q-binomial theorem, using a weighted block-divisibility argument. The shared-root correction reduces to the classical value at −1. The formulas and their applications may constitute a useful explicit corollary; historical publication priority remains unresolved.”

This is a narrower originality posture than treating the transverse coefficient as an unexplained new mechanism. It does not justify saying the whole theorem has been found verbatim in prior literature, that no one has stated it, or that the separate arithmetic applications are settled. The short filtration argument itself needs proof in a publication; it is supplied here rather than assumed to be a named classical theorem.

## 8. Primary-source implication comparison

### Classical finite product and special value

Gorodetsky, *q-congruences, with applications to supercongruences and the cyclic sieving phenomenon*, arXiv:1805.01254v2 (1 December 2019), preprint p.2, equation (1.5), explicitly records the finite q-binomial theorem used in §2. This is an attribution of a classical identity, not a priority claim for that paper. Its higher-derivative framework, Theorem 2.4 and Remark 2.8, is unnecessary for the completed implication above. [Primary PDF](https://arxiv.org/pdf/1805.01254)

Atakishiyeva–Atakishiyev–Koornwinder, arXiv:0811.4100v2 (21 May 2009), equations (2.1)–(2.4), gives the continuous q-Hermite recurrence and its Gaussian-binomial expansion. Putting the continuous variable at zero recovers H_(2m)(−1;q)=(q;q²)_m and odd-degree vanishing. Equation (2.8) gives the static root-of-unity factorization after C_n((s+s^−1)/2|q)=s^−n H_n(s²;q). The present transverse calculation is a derived consequence, not an equation asserted to occur there. [Primary HTML](https://arxiv.org/html/0811.4100v2)

### A closer all-order antecedent: Schultz–Walker

Schultz–Walker, arXiv:1202.0199v1, Theorem 1.1 (printed p.3), proves cyclotomic divisibility of polynomially weighted Gaussian-binomial derivatives. For α of order 2c, c|d, substitute their k=d/c, their z=0, derivative order r, congruence parameter 0, and P(m)=m(m−1)…(m−ℓ+1). Their size condition becomes n≥(ℓ+2r+1)d. Since n=Ad+b, it gives

∂_q^r ∂_z^ℓ H_n(α;ω)=0 whenever 2r+ℓ<A.

Thus the full below-weight-A vanishing is already an explicit published-theorem consequence, for every cluster root α^d=−1. The root can have smaller order; k stays odd. Their p.13 proof expressly allows any primitive choice. Their statement supplies divisibility, not the surviving coefficients; Proposition 6.1 and Lemma 6.2 (p.17) concern cyclotomic quotients and their recurrence. The heat/block proof above supplies the leading coefficients and overlap correction. Their Gaussian formula (p.2) also supplies the special value. [Primary PDF](https://arxiv.org/pdf/1202.0199v1)

Journal identity independently verified: Andrew Schultz and Robert Walker, *Journal of Number Theory* 133(11) (November 2013), 3717–3738, DOI 10.1016/j.jnt.2013.05.003. The equation/page locators just used are explicitly for arXiv v1, not silently relabeled as journal locators. [Publisher record](https://www.sciencedirect.com/science/article/pii/S0022314X13001558)

### Source gaps and bounded stopping condition

The exact six-page Zhedanov 1997 body and Lubinsky–Saff 1987 printed p.360 image remain unrecovered. Targeted fresh index searches produced bibliography/citation leads, not a new lawful body. Previously blocked publisher, author-host and ResearchGate retrievals were not repeated or bypassed. No author contact, purchase, login, or access expansion was made. No absence-of-theorem inference is drawn from those gaps.

The present all-order implication no longer depends on filling those gaps; historical comparison still does. No whole-paper negative-content verdict is claimed for any source read only at the listed statements.

## 9. Publication work after independent review

1. Review §§2–6 as a new proof; retain provisional status until an independent verdict is sealed. The existing manuscript's prior acceptance is a separate record.
2. Attribute the all-order below-weight-A vanishing explicitly to Schultz–Walker and the input identities to classical q-binomial/RS theory. Present the short block lemma and computed leading constants in full.
3. State the complete residual and local simplicity guards, ordinary-discriminant convention, and all q−ω / q^d−1 / Φ_d scale factors.
4. Position the result as an explicit coefficient calculation/corollary, with application significance assessed separately. Whether this exact corollary was previously published still requires targeted body and citation-chain work; a new proof of a consequence does not itself settle that question.
5. Do not restart finite Q29 base enumeration in place of this theory work. No all-composite, multiple-overlap, growing-A uniformity, or finite-characteristic guard removal is supplied here.
