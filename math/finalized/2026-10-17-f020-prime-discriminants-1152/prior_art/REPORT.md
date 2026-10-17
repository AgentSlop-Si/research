# F020: explicit prior-art normalization and implication map

Date: 2026-10-17 UTC. Scope: the shifted parity-Wronskian valuation and unramified collision exclusion in the frozen October 17 packet. This is a focused historical/mathematical comparison, not a second acceptance of the full Rogers–Szegő composition theorem and not a priority determination.

## Result

The comparison yields more than a terminology-level nonmatch:

1. The two parity Wronskians are exactly scalar multiples of diagonal Laguerre Christoffel–Darboux kernels at parameters −1/2 and +1/2.
2. The cited Christoffel–Darboux paper's affine nonsingularity lemma implies, by the calculation below, that these Wronskians are squarefree in characteristic zero. This is a genuine consequence of prior work.
3. The collision-location equation in the frozen packet is exactly the evaluation argument in Sawa–Uchida's published quasi-Laguerre discriminant formula, after the complete parameter conversion below. The general discriminant and elimination machinery must be credited as established.
4. The specific arithmetic input still required is the shifted integral reduction that forces every Wronskian root to satisfy v₂(y−1)=1/2. The inspected results do not supply that coefficient calculation. The current comparison therefore does not derive the full arithmetic assertion from a cited theorem alone.
5. A proof assembled from classical recurrences plus a further calculation is not evidence of historical novelty. Novelty remains UNVERIFIED; no project gate or canonical status is changed.

## 1. Primary-source statements used

**CD source.** Sawa–Uchida, *Algebro-geometric aspects of the Christoffel–Darboux kernels for classical orthogonal polynomials*, accepted manuscript, [Kobe primary repository](https://da.lib.kobe-u.ac.jp/da/kernel/90009429/90009429.pdf). Equation (5) defines the normalized kernel; Lemma 3.2 excludes affine singularities. Theorem 1.4(i), Section 4 and Remark 4.6 concern rational splitting/root counts for adjacent quasi-Hermite combinations. Proposition 4.1 and Lemma 4.2 give the Newton-polygon obstruction. Relevant manuscript pages: 5–8, 10–11, 13 and 19–20. The repository PDF has a cover, so manuscript page 11 is PDF page 12.

**Discriminant source.** Sawa–Uchida, *Discriminants of classical quasi-orthogonal polynomials with applications to Diophantine equations*, JMSJ 71 (2019), 831–860, [published primary text](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf). Theorem 3.6, equation (3.6), printed pages 844–845, gives the adjacent quasi-Laguerre discriminant used below. This is reference [24] of the CD paper.

**Classical normalization.** [DLMF 18.7.11](https://dlmf.nist.gov/18.7.E11), [18.7.19](https://dlmf.nist.gov/18.7.E19) and [18.7.20](https://dlmf.nist.gov/18.7.E20) record the Hermite normalization and quadratic Laguerre transformations. The following sections calculate their implications for the packet's objects.

## 2. Full polynomial normalization

Let Heₙ be monic probabilists' Hermite polynomials, with He₀=1, He₁=x and Heₙ₊₁=xHeₙ−nHeₙ₋₁. Let Hₙ be the physicists' normalization used in the CD paper:

    Heₙ(x) = 2^(−n/2) Hₙ(x/√2).

Use one parity index s∈{0,1} and set

    A = 2m+s−1,   α = s−1/2,   Cₘ = (−1)^m 2^m m!,
    Rₘ(y) = Uₘ(y) if s=0, and Vₘ(y) if s=1.

Then, with derivatives of Laguerre polynomials taken in their displayed argument,

    He₂ₘ(x) = Uₘ(x²),        He₂ₘ₊₁(x) = xVₘ(x²),
    Rₘ(y) = Cₘ Lₘ^(α)(y/2).                                      (N1)

Consequently, putting k=A(τ−1) and c=k/(2m),

    pₘ(y;τ) = Rₘ(y) − k Rₘ₋₁(y),
    J_A₊₁(x;τ) = x^s pₘ(x²;τ),
    pₘ(y;τ) = Cₘ [Lₘ^(α)(y/2) + c Lₘ₋₁^(α)(y/2)].               (N2)

The plus sign in the last bracket follows from Cₘ₋₁/Cₘ=−1/(2m). In particular this is a first-order quasi-Laguerre family in y, whereas in x

    J_A₊₁ = He_A₊₁ − A(τ−1)He_A₋₁

has a two-degree Hermite gap. It is not obtained by merely renaming the parameter in an adjacent first-order quasi-Hermite family.

For an exact bridge to ordinary Hermite Wronskians, using the packet orientation W(f,g)=f'g−fg',

    W_x(He₂ₘ, He₂ₘ₋₂) = 2x Wₘ^U(x²),
    W_x(He₂ₘ₊₁, He₂ₘ₋₁) = 2x³ Wₘ^V(x²).                         (N3)

These identities specify the parity deflation and variable change needed before applying any theorem about general Hermite Wronskians.

## 3. Exact diagonal-kernel identification and an actual prior implication

Define, directly in Laguerre normalization,

    fₘ₋₁^(α)(u,v)
      = [Lₘ^(α)(u)Lₘ₋₁^(α)(v) − Lₘ₋₁^(α)(u)Lₘ^(α)(v)]/(u−v).

Its diagonal value is

    fₘ₋₁^(α)(z,z) = (Lₘ^(α))'(z)Lₘ₋₁^(α)(z)
                       − Lₘ^(α)(z)(Lₘ₋₁^(α))'(z).

Applying the chain rule to (N1) gives the exact scalar:

    Wₘ^R(y)
      = (Cₘ Cₘ₋₁/2) fₘ₋₁^(α)(y/2,y/2)
      = −2^(2m−2) m!(m−1)! fₘ₋₁^(α)(y/2,y/2).                   (N4)

This is an identity of polynomials, including the sign and the derivative factor 1/2. A scalar or argument factor must not be dropped when comparing coefficient valuations.

**Derived consequence.** For m≥3, apply CD Lemma 3.2 with r=m−1 and α=±1/2. If d(z)=f(z,z) had d(z₀)=d'(z₀)=0, the symmetry f(u,v)=f(v,u) would give

    ∂₁f(z₀,z₀) = ∂₂f(z₀,z₀) = d'(z₀)/2 = 0.

The point (z₀,z₀) would be an affine singularity, which is excluded. Hence Wₘ^R is squarefree. The small cases require no extension of the lemma's index range:

    W₁^U = W₁^V = 1,
    W₂^U = y²−2y+3,     Disc = −8,
    W₂^V = y²−6y+15,    Disc = −24.

Thus characteristic-zero squarefreeness of the Wronskians is an actual corollary of the cited geometric result. It gives no valuation of their roots at 2. In particular, squarefreeness of W and absence of a W-root in an unramified field are different properties.

## 4. Collision elimination: exact agreement with the quasi-Laguerre formula

Write P=Lₘ^(α), Q=Lₘ₋₁^(α), F_c=P+cQ, and z=y/2. The Laguerre recurrence/derivative identities give

    zP' = mP−(m+α)Q,
    zQ' = mP+(z−m−α)Q.

At a root F_c(z)=0, consecutive-polynomial coprimality implies Q(z)≠0, and direct elimination gives

    zF_c'(z) = [cz−m c²−(2m+α)c−m−α] Q(z).                     (C1)

For a nonzero repeated root, c≠0 and therefore

    z = z_c := [m c²+(2m+α)c+m+α]/c.

Substitution of c=A(τ−1)/(2m), with A=2m+s−1 and α=s−1/2, gives the identity

    2z_c = τ(Aτ+1)/(τ−1).                                     (C2)

This is the same collision location as the packet's Hermite elimination, not merely an analogous expression. Both symbolic parity cases were checked for general m.

For completeness, define

    Bₘ,α = product_{j=1}^m j^(j−2m+3)
              × product_{j=1}^{m−1}(j+α)^(j−1).

Sawa–Uchida Theorem 3.6 reads, in this notation,

    Disc_z(F_c) = Bₘ,α (−c)^m F_c(z_c)/(m+α+mc).                (C3)

The formula is a polynomial identity after cancellation. At c=0 and c=−(m+α)/m the rational display must be interpreted by cancellation/limit, not by evaluating an undefined expression.

The parameter c₀=−(m+α)/m produces a simple zero of F_c at z=0:

    F_c₀(z) = −(z/m)Lₘ₋₁^(α+1)(z).

This explains why multiplying the derivative by z in (C1) can introduce a spurious zero-root condition for F. In the composed polynomial J, however, this simple y-root creates the genuine repeated x=0 root. The exact parameters are τ=0 for s=0 and τ=−1/A for s=1. The case c=0 is τ=1, when J=He_A₊₁.

### Ordinary-discriminant scaling, with no hidden monic convention

For the monic degree-m polynomial p=pₘ(y;τ), product-of-root differences gives

    Disc_y(p) = 2^[m(m−1)] (m!)^(2m−2) Disc_z(F_c),
    Disc_x(p(x²)) = (−1)^m 4^m p(0) Disc_y(p)²,
    Disc_x(xp(x²)) = (−1)^m 4^m p(0)³ Disc_y(p)².              (C4)

Here

    p(0) = (−1)^m(2m−1)!! τ                  when s=0,
    p(0) = (−1)^m(2m−1)!! (1+2mτ)           when s=1.

These calculations make the distinction precise: (C3) plus (N2)/(C4) already determines the general ordinary discriminant of J. An exclusion theorem for its nonzero collision parameters is an additional arithmetic assertion.

## 5. Where the shifted arithmetic enters

The frozen packet supplies the following calculation, restated here to identify the precise additional input rather than attributing it to the prior paper. Put π²=2 and

    R̃ₘ(X) = π^(−m) Rₘ(1+πX).

Its two scaled recurrences have integral coefficients in Z[π]. Modulo π both have

    ρₘ₊₁ = Xρₘ + (m mod 2)ρₘ₋₁,
    ρₘ = X^(m mod 2)(X²+1)^floor(m/2).

The chain rule and differentiation modulo π then give

    π^(−2m+2) Wₘ^R(1+πX) ≡ (X²+1)^(m−1) mod π.              (A1)

The left side is integral and monic, and its constant term is a unit. Any root X has valuation zero: a negative valuation would isolate the leading monomial as the unique term of minimum valuation; a positive one would isolate the constant term. Hence

    Wₘ^R(y)=0  ⇒  v₂(y−1)=1/2.                              (A2)

Equivalently, for Wₘ^R(1+w)=Σaⱼwʲ,

    v₂(aⱼ) ≥ m−1−j/2,
    v₂(a₀)=m−1,     a₂ₘ₋₂=1.

The whole lower polygon is the indicated single segment. Merely finding one half-integral segment, or establishing that W has no rational roots, is weaker.

Under (N4), the same assertion for diagonal Laguerre roots is

    fₘ₋₁^(α)(z,z)=0 ⇒ v₂(z−1/2)=−1/2,

and also v₂(z)=−1. The translation by 1/2 is essential.

### Why Section 4 is not a direct substitution proof

There are three independent changes to account for:

- **Polynomial:** the diagonal kernel in (N4) has degree 2m−2; the adjacent quasi-Hermite combination is another family. There is no equality of those two polynomial families in the normalization map.
- **Field:** Hₙ(x/√2)=2^(n/2)Heₙ(x). The √2 scaling is ramified at 2; it cannot silently preserve an unramified coefficient-field hypothesis.
- **Polygon convention:** for coefficients indexed by x^(N−k), an edge slope equals the corresponding root valuation. For ascending powers wʲ, the edge slope is its negative. Thus the shared displayed slope −1/2 is insufficient to identify the two conclusions.

The inspected source result does not supply (A1). Repeating the classical recurrence argument and proving (A1) is a valid derivation, but it is an extra derivation, not a direct application of the cited rational-splitting conclusion. Conversely, that absence is not proof that (A1) or an equivalent consequence was never published elsewhere.

## 6. Implication chain to collision exclusion and the RS application

Let K be a subfield of the maximal unramified algebraic extension of Q₂. Every individual element of K belongs to a finite unramified extension and has integer valuation.

A nonzero repeated J-root gives, by (C2), y=x²∈K (τ=1 is separately impossible). Eliminating k from pₘ(y)=pₘ'(y)=0 gives Wₘ^R(y)=0. Equation (A2) contradicts y∈K. The exceptional zero roots were accounted for above. This establishes exactly

    A odd:   J is squarefree ⇔ τ≠0,
    A even:  J is squarefree ⇔ τ≠−1/A.

The final valuation-field contradiction is standard local-field/Newton-polygon reasoning. The family-specific information is (A1)/(A2).

The reverse algebraic reduction is also useful: if Wₘ^R had a root y∈K, coprimality gives Rₘ₋₁(y)≠0, so k=Rₘ(y)/Rₘ₋₁(y) lies in K and makes Rₘ−kRₘ₋₁ have a repeated root. Since Wₘ^R(0)≠0, it is a nonzero collision. Thus absence of K-rational W-roots is equivalent to exclusion of these nonzero collisions. The exact valuation statement is stronger than this absence statement.

For the RS parameter τ_b, the remaining arrows are project-specific: the partial-sum argument establishes nonreality and nonvanishing, and odd-order roots of unity embed in an unramified extension at 2. Those inputs avoid both rational exceptional parameters. Neither the CD geometry nor the quasi-Laguerre discriminant formula alone proves these RS parameter properties.

The ramified negative control remains decisive:

    A=3, τ=(−1+2√(−2))/3,
    J₄(x;τ)=[x²−(1+√(−2))]².

The double-root y has v₂(y−1)=1/2. Nonreality by itself cannot replace the unramified-field hypothesis.

## 7. Cited-literature boundary

The general polygon product theorem has an independently inspected older primary source: Dumas, *Sur quelques cas d'irréductibilité des polynômes à coefficients rationnels* (1906), §5, printed pages 214–217, [Numdam scan](https://www.numdam.org/item/JMPA_1906_6_2__191_0.pdf). It composes the edge vectors of the factor polygons in slope order. This supplies general Newton-polygon infrastructure; determining the packet's shifted coefficient bounds remains a separate calculation.

The CD bibliography also routes its arithmetic discussion to Bannai–Damerell, *Tight spherical designs II* [4], Neukirch [20] and Prasolov [21]. Their full bodies were not independently audited in this narrow pass. DLMF routes the quadratic transformations to Szegő. The exact-polygon claim is therefore not priority-cleared across the cited literature. Neither a failed full-text retrieval nor an empty title/keyword search is counted as evidence of nonexistence.

The independent review's existing Grosu–Grosu, Bonneux–Dunning–Stevens and Lubinsky–Saff records are preserved. This comparison does not reopen or erase the completed Lubinsky–Saff mathematical-body audit, and does not claim to have rechecked it.

## 8. Checks, scope and recommended wording

A newly written symbolic checker, `check_normalizations.py`, uses exact arithmetic and imports no submitted program. `normalization_controls.json` records 126 passing checks across both parity families m=1,…,8: parity conversion, J conversion, Wronskian scalar, collision location, W squarefreeness, and (for m≤5) both discriminant scalings and Theorem 3.6. It also verifies (C2) symbolically for general m in each parity. These are normalization controls; the unlimited statements rest on the displayed algebra/proofs, not the finite checks.

Primary sources were inspected with the web PDF reader. A separate local-download attempt for the CD PDF returned HTTP 403, so no local PDF hash is claimed. This did not prevent inspection of the primary text. PDF screenshot rendering returned an internal error; the displayed formula was additionally checked against exact polynomial discriminants to guard against extraction ambiguity.

Suggested manuscript language:

> The parity reduction identifies the overlap polynomial with a quasi-Laguerre combination at parameter α=±1/2. Its general discriminant and collision-location formula are specializations of established formulas. The associated parity Wronskian is a diagonal Christoffel–Darboux kernel, and its characteristic-zero squarefreeness follows from known affine nonsingularity. The additional arithmetic input used here is the exact shifted 2-adic valuation of all its roots, which excludes nonzero collisions over unramified 2-adic fields. Historical priority for that arithmetic input remains unverified.

The frozen mathematical acceptance is retained. F020 remains the canonical owner and F023 an alias. Existing later fixed-residual and derivative/separation acceptances are not reset. OPEN58, the separate endpoint gate and all other project-wide assertions retain their prior scope. No numerical FFT improvement, arbitrary odd-composite static theorem, positive-characteristic extension, canonical promotion, repository change, or novelty claim follows from this comparison.
