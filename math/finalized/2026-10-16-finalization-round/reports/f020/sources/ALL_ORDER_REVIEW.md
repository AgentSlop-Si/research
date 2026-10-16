# Independent review of the F020 all order implication

Review completed 11 October 2026 UTC. The reviewed proof is ALL_ORDER_IMPLICATION.md, SHA256 8ca570c7e7c41c50827b1dea3feb931cbcfe0fdab3c3a2016c6e7d0989126abc, in the provisional archive whose SHA256 is 79273ecedccd68bf0d174c843eb5cecc9d32cbb596b115519d26da11352b9ffd. This verdict concerns those exact bytes.

## Verdict

**Accept the all-A implication proof in its stated characteristic-zero separated and one-simple-overlap scope.** The diagonal-operator identity, all-order block-divisibility argument, weighted formal passage, overlap correction τ=dW/g, signs, root-product normalization, and conversions among q−ω, q^d−1, and Φ_d all check. There is no required mathematical correction to the displayed formulas.

The review supplies a formal argument for every A, independently written exact recurrence controls, and a primary-source check. The finite controls support the audit; they do not substitute for its all-A argument. The reviewed author's program was read as inert text and was neither imported nor executed. This verdict is separate from the existing manuscript acceptance and does not relabel the research as historically anticipated or automatically change its family rank.

Two clarifications should accompany reuse: a nonzero characteristic-zero coefficient gives no unasserted positive-characteristic unit conclusion; and published lower-jet vanishing does not determine the first surviving coefficient. No source body reviewed here was found to state the full moving-root/discriminant formulas verbatim. That bounded observation is not an exhaustive publication-priority conclusion.

## Notation and guards

Let d be odd, ω primitive of order d, A≥1, 0≤b<d, n=Ad+b, F=1+z^d, G=H_b(z;ω), and H_n(z;q)=Σ_k [n choose k]_q z^k. Work over a characteristic-zero field containing the needed roots. All discriminants are ordinary monic z-discriminants, with Disc(1)=Disc(linear)=1. Write P_A=∏_(j=1)^A j^j.

For the separated discriminant require Disc(G)Res(F,G)≠0. The local coefficient identity itself is meaningful without that global guard, but can vanish at an overlapping root.

For the overlap assume d≥3, b odd, G=(z+1)U and g=U(−1)≠0. Set m=(d+b)/2<d, W=(ω;ω)_b/(ω²;ω²)_m and τ=dW/g. Every denominator factor of W is nonzero. The global overlap discriminant additionally requires Disc(U)Res(F,U)Disc(J_(A+1))≠0. These hypotheses ensure exactly one common residual root, with simple residual multiplicity, and simple first displacements. They cannot be removed by the present argument.

Use q=ωe^h, u=z−α, wt(u)=1, wt(h)=2, and q(ε)=ω(1+ε²)^(1/d). Thus h=log(1+ε²)/d, whose weight-two part is ε²/d. The separated reasoning also works at d=1,b=0; the author's principal statement explicitly restricts its new discussion to d≥3.

## The all order argument

### Exact operator and block factorization

Let P_n(z;q)=∏_(j=0)^(n−1)(1+q^jz), let T(z^k)=ω^(k(k−1)/2)z^k, and let L=z²∂_z². Coefficient comparison in the finite q-binomial identity gives, exactly in the h-adic polynomial module,

R_n=T^(−1)P_n(z;ωe^h),     H_n(z;ωe^h)=exp(−hL/2)R_n.

The exponential is well defined coefficientwise: the coefficient of h^r uses only finitely many operator powers. Since d is odd,

ω^[(k+d)(k+d−1)/2−k(k−1)/2]=ω^[dk+d(d−1)/2]=1.

Hence T and T^(−1) commute with z^d and all powers of F. For d even the same ratio is −1, so this specific proof cannot silently be extended to even d.

Partition the first Ad product factors into A d-factor blocks and the final b factors into one residual block. Each complete d-block becomes F at h=0. In any r-th derivative term, at most r complete blocks are touched. Consequently, writing R_n=Σ_r h^rR_r,

F^max(A−r,0) divides R_r, for every integer r≥0.

This argument is an all-order product-rule statement, not extrapolation from computations. For r=0, the residual finite q-binomial identity gives R_0=F^AG.

### Formal filtration details

At a simple root α of F, the contribution h^rR_r has weight at least 2r+max(A−r,0). If r≥1 this is at least A+1; if r≥2 it is at least A+2, including r>A. On a monomial h^r u^s, the three summands of hL are

hα²∂_u²,     2hαu∂_u²,     hu²∂_u²,

which respectively preserve weight or increase it by one or two. Therefore the full exponential preserves every weighted remainder ideal. Its associated-graded action is exp(−hα²∂_u²/2). On each fixed weighted degree the latter is a finite sum, because successive second derivatives terminate. For the full exponential, the coefficient of any fixed h^r u^s also receives finitely many contributions. There is no hidden analytic convergence assumption.

### Separated coefficient

Since F′(α)=−d/α, the weight-A part of R_n is (−d/α)^A G(α)u^A. Every r≥1 part lies at higher weight. The associated-graded operator thus gives

H_n(α+εx;q(ε))
=ε^A(−1)^A d^(A/2)G(α)He_A(√d x/α)+O(ε^(A+1)).

This follows immediately from the finite polynomial identity

exp(−s∂_u²/2)u^A=Σ_(j=0)^floor(A/2) [A! (−s)^j/(2^j j!(A−2j)!)]u^(A−2j).

In particular, the written square roots cancel coefficientwise. This proves the coefficient formula for every A.

### Overlap coefficient

Set E_b=∏_(r=0)^(b−1)(1+ω^rz) and S=Σ_(r=0)^(d−1)rω^rz∏_(s≠r)(1+ω^sz). Let S_b be the analogous residual-block derivative. The i-th full block derivative at h=0 equals S+i d²z^d. Summing i=0,...,A−1 gives the exact first-derivative identity

P′_n|_0=F^(A−1)[A E_bS+d²A(A−1)z^dE_b/2]+F^A[Ad(z∂_z)E_b+S_b].

After T^(−1), the z^dE_b term has an extra factor G, which vanishes at −1, and the final F^A term has too high a weight after multiplication by h. With c_b=(T^(−1)(E_bS))(−1), the only relevant first-derivative term is A d^(A−1)c_b h u^(A−1), where u=z+1. This remains valid at A=1: the A(A−1) term is zero, with no negative-power ambiguity.

Determine c_b at A=1 using R_1=∂_hH_(d+b)|_0+(L/2)(FG). The second term at −1 is dg, because FG=dg u²+O(u³). Independently, the recurrence at z=−1 gives H_(2m)(−1;q)=∏_(j=1)^m(1−q^(2j−1)), while odd degrees vanish. Equivalently this is (q;q)_(d+b)/(q²;q²)_m. Its numerator has one vanishing factor 1−q^d; the other factors at ω multiply to d(ω;ω)_b. Since ∂_h(1−ω^de^(dh))|_0=−d, its first derivative is −d²W. Thus

c_b=dg−d²W=dg(1−τ).

The weight-(A+1) part of R_n is consequently

d^Ag[u^(A+1)+A(1−τ)h u^(A−1)].

All r≥2 parts lie at weight at least A+2, by the proved general bound. Applying exp(−h∂_u²/2), then h=ε²/d+O(ε⁴), gives

H_n(−1+εx;q(ε))
=ε^(A+1)d^((A−1)/2)g[He_(A+1)(√d x)+A(1−τ)He_(A−1)(√d x)]+O(ε^(A+2)).

The two Hermite terms have the same parity. This is exactly the manuscript's (−1)^(A+1)J_(A+1)(−√d x;τ) convention. Both the factor d in τ and the factor 1/d in h=ε²/d are essential.

## Ordinary discriminant and coefficient conversions

Under the stated simplicity and separation guards, the formal implicit-function theorem lifts each simple initial root to a branch over the algebraic closure's ε-series. Counting the A branches at each F-root plus the residual roots accounts for all n roots. For overlap the shared cluster has A+1 roots, leaving A at the other d−1 roots and b−1 residual roots.

For the separated case, within-cluster squared differences contribute

ε^[dA(A−1)]d^[−dA(A−1)/2]P_A^d.

The omitted α powers really cancel: ∏_(F(α)=0)α=−1 and A(A−1) is even. Cross-cluster pairs contribute Disc(F)^(A²), where Disc(F)=(−1)^((d−1)/2)d^d. The residual pairs and mixed pairs contribute Disc(G)Res(F,G)^(2A). Since A²≡A mod 2, multiplying gives, with K=dA(A−1)/2,

D_n(q(ε))=ε^(2K)[C_sep+O(ε²)],

C_sep=(−1)^[A(d−1)/2]d^[dA(A+1)/2]P_A^d Disc(G)Res(F,G)^(2A).

For overlap let L_ov=dA(A−1)/2+A and F_0=F/(z+1). The product of the nonshared α roots is 1. Within clusters the factor is

ε^(2L_ov)d^(−L_ov)P_A^(d−1)Disc(J_(A+1)).

Here F_0(−1)=d and Disc(F_0)=(−1)^((d−1)/2)d^(d−2). Thus cross-cluster factors are Disc(F_0)^(A²)d^[2A(A+1)], giving sign (−1)^[A(d−1)/2] and d-power dA²+2A. Residual pairs contribute Disc(U)Res(F,U)^(2A)g². Multiplication proves

D_n(q(ε))=ε^(2L_ov)[C_ov+O(ε²)],

C_ov=(−1)^[A(d−1)/2]d^[dA(A+1)/2+A]P_A^(d−1)Disc(J_(A+1))Disc(U)Res(F,U)^(2A)g².

The coefficient is nonzero exactly when the applicable displayed factors are nonzero, with τ only defined under g≠0. Exact order follows in the guarded cases. Without the guards this root lifting proof does not certify the same order. The normalized remainder is even because q(ε) is even; it is not necessary to assume individual branches are even.

For either exponent M and coefficient C, t=q^d−1=ε² gives D_n=t^M(C+O(t)). Since t=dω^(d−1)(q−ω)+O((q−ω)²), the q−ω coefficient is (dω^(d−1))^M C, rather than C. With Q_d=(q^d−1)/Φ_d, Galois conjugacy gives the same exact multiplicity at every primitive d-th root; monic division yields D_n=Φ_d^M E with E∈Z[q], and E(ω)=Q_d(ω)^M C. These scale factors go in the stated direction.

## Primary source and logical implication check

Schultz–Walker, arXiv:1202.0199v1, Theorem 1.1, printed p.3, was checked in the primary PDF text. For a cluster root of order 2c, take their k=d/c, z=0, derivative index r, congruence index 0, and polynomial P(m)=m(m−1)…(m−ℓ+1). Their condition becomes n≥(ℓ+2r+1)d. Therefore ∂_q^r∂_z^ℓH_n(α;ω)=0 for 2r+ℓ<A. All α^d=−1 are covered: c divides odd d, and d/c is odd. The primitive-choice passage on printed p.13 was also checked. The Gaussian formula on p.2 supplies the special value used above. Printed pp.17–18 contain quotient multiplicity/recurrence statements; no leading moving-root coefficient is asserted by those selected statements. Page-image retrieval failed; this review claims indexed primary-text inspection, not rendered-page verification or a full-paper negative finding. Source: https://arxiv.org/pdf/1202.0199v1 .

The finite q-binomial identity was independently checked in Gorodetsky, arXiv:1805.01254v2, p.2, equation (1.5): https://arxiv.org/pdf/1805.01254v2 . This attributes a classical identity; it does not assign its historical origin to that paper.

The implications have the following precise directions:

1. The finite q-binomial identity plus the proved block lemma, first-derivative calculation, and standard root-product algebra imply the complete displayed F020 formulas for all A under the guards.
2. The Schultz–Walker specialization implies below-weight-A vanishing. It alone does not fix the surviving coefficients. For example, for b=0 and A≥2, adding λ(q^d−1)F^(A−2) to a monic family preserves its static value and all below-weight-A vanishings but changes its weight-A initial form. For overlap, λ(q^d−1)F^(A−1) similarly preserves the static value and lower weight vanishings while changing weight A+1. These are logical countermodels to inferring a coefficient from vanishing data alone; they are not claimed to be Rogers–Szegő polynomials.
3. Conversely, a complete local ε-initial-form identity implies all corresponding lower mixed-derivative vanishings. Indeed the change q−ω=ωh+O(h²) is an invertible filtered coordinate change, and substituting u=εx,h=ε²/d+O(ε⁴) separates each weight into independent powers of x. No coefficient of weight below the stated order can survive. This converse concerns the local specialization only; it does not recover the full general Schultz–Walker theorem or the finite q-binomial identity.
4. The guarded initial forms imply the discriminant coefficient. A single discriminant coefficient does not determine all cluster polynomials or imply the operator identity. No two-way equivalence of those stronger statements is asserted.

## Independent checks and reproducibility

The saved independent_controls.py computes directly from H_0=1, H_1=1+z and H_n=(1+z)H_(n−1)+(q^(n−1)−1)zH_(n−2). It performs exact rational truncated ε arithmetic in Q[w]/(w^d−1), followed by reduction modulo Φ_d. It uses neither the author's q-Pascal construction nor the operator proof to generate the checked jets.

All 16 moving-root controls pass, including A=10 and A=12, d=9 and d=15, b close to d, roots with order properly smaller than 2d, and the d=1 endpoint. Five directly computed ordinary discriminants pass exact cyclotomic valuation and both coefficient conversions: (A,d,b)=(1,3,2),(1,5,1),(2,3,2),(2,3,1),(1,5,3). Degree-zero residual discriminants are explicitly normalized to 1, rather than using a computer algebra system's constant-polynomial default.

Mutation controls reject dropping the heat term, setting τ=1, omitting d from τ, extending T-periodicity to even d, and equating the t coefficient with the q−ω coefficient. The numerical examples are bounded; the all-A conclusion rests on the formal proof above. Full exact outputs, executable fresh source, and the complete final run log are included and hash-bound.

## Positioning and remaining limits

The core identities, ordinary Hermite discriminant, root-product assembly, and cited mixed-derivative vanishing are established ingredients. The weighted block lemma and first surviving coefficients are explicitly derived and checked here. This closes the previously unworked all-A implication route from a finite classical identity; it is more than a fixed-cubic or small-A comparison.

Being derivable from classical inputs does not itself prove the exact result was previously published, nor that its explicit coefficient calculation or applications have no value. The appropriate description is an independently accepted explicit all-order derivation/refinement with historical publication priority unresolved. This review makes no automatic downgrade of family priority, no worldwide originality clearance, and no finding about separate arithmetic, inverse-pair, disk-exclusion, all-composite, repeated-overlap, or growing-degree-uniform claims. The previously recorded inaccessible Zhedanov and Lubinsky–Saff material is not treated as read.

The source-pinning distinction is preserved: the recovered separated independent-audit bytes have SHA256 f093175f18d1941a99a605a5d816b1db31e5b2c4161ee7df4bf29291ff8eff3c; the catalogue's different export hash 4b86b307... is not silently identified with them. No Sheet or GitHub writes were performed by this review.
