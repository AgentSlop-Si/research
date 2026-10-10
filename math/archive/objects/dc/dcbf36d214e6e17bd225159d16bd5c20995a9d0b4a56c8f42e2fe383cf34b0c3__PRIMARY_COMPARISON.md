# Lubinsky and Saff comparison for the Rogers Szegő research package

10 October 2026 UTC

## Result and scope

The supplied 1987 paper directly contains the root-of-unity factorization, the chirp Toeplitz determinant, and the Rogers–Szegő Padé denominator used by the project. The odd-cycle shifted annihilator and the product for its forced diagonal are direct consequences after an explicit normalization change. These ingredients must be attributed to classical work rather than retained as independent originality claims.

The paper does not supply the project's moving-root Hermite splitting coefficients, ordinary-discriminant leading coefficients, simultaneous residue-component arithmetic, or the three composite half-order families with lower bases 3, 7, and 11 and prime multiplier congruent to 1 modulo 4. Its results also do not settle the all-composite simplicity question. This conclusion describes the scope of this particular comparison; it is not a finding of publication novelty. The Zhedanov 1997 comparison and broader citation chaining remain open.

The supplied scan has all mathematical body pages 331–359, followed by page 361. Journal page 360, containing the middle references, is absent; PDF pages 31 and 32 are blank. It should therefore be described as a mathematical-body comparison with an incomplete bibliography, not an unqualified complete-scan read.

This report compares the frozen `research_cycle_0958/composite_guard/final_v1` and `research_cycle_0958/algebra/final_v1` packages and the inherited `research_finalization_0923/algebra/final_v1` manuscript. It also reads the inherited odd-cycle classification and reciprocal-content reports cited by that manuscript. Existing proof acceptance is not replaced by this literature review. No supplied research program was executed, imported, compiled, or used as an arithmetic module. A small, freshly written comparison control checks only the normalization and signs derived below.

## Primary source and reading record

D. S. Lubinsky and E. B. Saff, *Convergence of Padé Approximants of Partial Theta Functions and the Rogers–Szegő Polynomials*, Constructive Approximation **3** (1987), 331–361. Bibliographic DOI locator from the existing primary-source ledger: https://doi.org/10.1007/BF01890574. This review uses the user-supplied PDF, not a new retrieval from that link.

Source: `../76.pdf`, 962409 bytes, SHA-256 `034c2af8f6b6696d90d2f744e2932740f9fe1696b3a937b984fd7faca4f39b56`.

All supplied page images were visually inspected, and the OCR of the mathematical body was read. Formulas used below were checked against the page images. OCR is not reliable for inequality signs, subscripts, and exponents: for example, it repeatedly replaces “m ≥ n−1” by an equality and loses parts of the Toeplitz product. The visual equations govern this report.

The source uses G_n for the polynomial called H_n in the project. Its H_n in equations (4.6)–(4.7), page 343, is a different, q-weighted binomial polynomial. Its D(m/n) is a Toeplitz determinant, not the project's ordinary z-discriminant D_n(q). These two notation collisions must not be used as evidence of an identical discriminant formula.

The paper's coverage is:

- Sections 1–2, pages 331–338: definitions; norm growth; asymptotic zero distributions; subsequence limits; zero-exclusion regions and annulus bounds.
- Section 3, pages 338–342: Padé formulas and convergence statements. Theorem 3.2 is the directly relevant algebraic identity.
- Section 4, pages 342–351: recurrence, reciprocity, q-binomial inputs, root-of-unity factorization, and proofs of asymptotic distribution statements.
- Section 5, pages 351–353: continued-fraction zero-exclusion arguments.
- Section 6, pages 353–359: natural boundary, determinant and denominator proofs, convergence, and numerator coefficients.
- References 1–8 on page 359 and 37–45 on page 361. References 9–36 are missing with page 360.

## Exact classical overlaps

### Recurrence and reciprocity

Lemma 4.1, page 343, equations (4.1)–(4.5), gives

    G_(n+1)(z) = (1+z)G_n(z) − (1−q^n)zG_(n−1)(z),
    G_n(z) = G_(n−1)(z) + q^(n−1)zG_(n−1)(z/q),
    G_n(qz) = G_n(z) − (1−q^n)zG_(n−1)(z),
    G_0 = 1,  G_1 = 1+z,
    z^n G_n(1/z) = G_n(z).

It also establishes polynomial dependence on q. These are exactly the recurrence, q-shift relation, and self-reciprocity used by the project. The q-shift relation concerns values at z and qz; it is not an ordinary derivative identity and cannot by itself prove squarefreeness.

Disposition: classical input. “Identifying an RS recurrence,” “discovering reciprocal pairing,” or “using the q-shift relation” is not a defensible originality headline for F020/F021.

### Root of unity factorization and static multiplicities

Lemma 4.5, page 346, equation (4.15), states that for q of primitive order ν and n=kν+l, 0≤l<ν,

    G_n(z;q) = (1+z^ν)^k G_l(z;q).

The proof on that page is a double induction from equation (4.2). In project notation this is precisely

    H_(Ad+b)(z;ω) = (z^d+1)^A H_b(z;ω),   0≤b<d.

The paper's statement works for all positive orders ν; the project's restriction to odd d does not make this static factorization new. It already determines the specialized root multiplicity A at each root of z^d+1 not shared with H_b, and A plus the residual multiplicity at a shared root. Thus even a reformulation as a “root-of-unity multiplicity theorem” must be demoted when it refers only to the polynomial at q=ω.

Disposition: exact anticipation of the static factorization and its immediate multiplicity consequences. This directly replaces the old “Lubinsky–Saff full-text comparison unavailable” status for this ingredient.

### Chirp Toeplitz determinant and Padé denominator

Set a_j=q^(j(j−1)/2), so h_q(t)=Σ_(j≥0) a_j t^j, as in equation (1.1), page 331. Equation (3.1), page 338, defines

    D(M/n) = det[a_(M−i+j)]_(0≤i,j<n).

Theorem 3.2, page 340, equations (3.11)–(3.12), gives

    D(M/n) = a_M^n ∏_(j=1)^(n−1)(1−q^j)^(n−j),
    Q_(M,n)(−zq^(−M)) = G_n(z;q).

The denominator is normalized by Q_(M,n)(0)=1; the statement assumes q^j≠1 for 1≤j≤n. The printed statement has M≥n−1>0; its proofs on pages 354–355 explicitly include the low-degree boundary cases M≥n−1≥0. The product's empty cases also follow immediately.

The paragraph immediately preceding Theorem 3.2 says the result is essentially contained in Balk [5], Gragg [16], and Wynn [45]. Hence Lubinsky–Saff is a direct accessible primary record, but not a justified first-priority attribution. Gragg's reference entry is among the missing references; its title is not reconstructed here. Wynn [45] is visibly *A general system of orthogonal polynomials*, Quarterly Journal of Mathematics Oxford 18 (1967), 81–96, on page 361.

The determinant proof uses the Padé “star” identity, equation (6.3), page 354. The denominator proof uses a Frobenius triangle identity, equation (6.4), pages 354–355, and the RS recurrence. Lemma 6.4, page 357, equation (6.15), additionally gives the numerator leading coefficient

    A_(M,n) = q^(M(M−1)/2) ∏_(j=1)^n(1−q^j)
             = D(M/(n+1))/D(M/n).

Disposition: the exact chirp moment determinant and its Padé/RS correspondence are classical formulas, not merely conceptually similar antecedents.

## Exact translation to the scalar bank package

The following is a derived comparison, not a quotation or theorem claimed to be printed in the paper. It shows why the overlap includes two particular project formulas.

### Hankel determinant translation

Let

    Δ_n^(r) = det[a_(i+j+r)]_(0≤i,j<n),  r≥0.

Reverse the rows in D((r+n−1)/n). Then

    Δ_n^(r) = (−1)^(n(n−1)/2) D((r+n−1)/n)
            = (−1)^(n(n−1)/2) a_(r+n−1)^n
              ∏_(j=1)^(n−1)(1−q^j)^(n−j).

For r=0, this is exactly the Hankel formula in the even-cycle proof:

    Δ_n^(0) = q^(n(n−1)(n−2)/2)
              ∏_(j=1)^(n−1)(q^j−1)^(n−j).

Thus the nonzero chirp Hankel rank used in both even and odd bank arguments is a row-reversal form of the existing determinant. The lower bound obtained by applying that rank to a specified resolvent grammar is an application, not a new determinant.

### Odd shifted annihilator

Let N=2m+1, h=m+1, q primitive of order N, and f_j=q^(h j²). Since 2h=N+1,

    f_j = q^(hj) a_j,
    f_(k+1) = q^h (q^(h+1))^k a_k.

The generating series of the shifted moments is consequently

    Σ_(k≥0) f_(k+1)t^k = q^h h_q(q^(h+1)t).

Take the [m−1/m] Padé denominator. Theorem 3.2 yields

    Q(t) = G_m(−q^(m−1)q^(h+1)t;q) = G_m(−t;q),

because m+h=N. Reversing to the monic annihilator and using Lemma 4.1 gives

    T_m(z) = z^m Q(1/z) = (−1)^m G_m(−z;q).

This is exactly the annihilator in the project's odd-cycle classification. The standard Padé orthogonality equations are its shifted moment equations. The m=1 boundary can be checked directly and is included in the source's denominator induction.

Disposition for F021: demote the explicit shifted annihilator to a direct classical specialization. Retain only the additional legal-node analysis and exact grammar-dependent minimum, where proved, as the application-specific question.

### Forced diagonal product

The project shows that an m-node representation forces

    δ = det[f_(i+j)]_(0≤i,j≤m)
        / det[f_(i+j+2)]_(0≤i,j<m).

Writing f_j=γ^j a_j with γ=q^h, the γ-powers of these two determinants are both γ^(m(m+1)); they cancel. Substitute the preceding row-reversed Toeplitz product. The remaining sign is (−1)^m, the a-factor ratio is

    a_m^(m+1)/a_(m+1)^m = q^(−m(m+1)/2),

and the remaining product is ∏_(j=1)^m(1−q^j). Therefore

    δ = (−1)^m q^(−m(m+1)/2) ∏_(j=1)^m(1−q^j).

Disposition: the product evaluation is a direct consequence of the classical determinant. The rank-one-change interpretation as the forced free diagonal belongs to the project's application, but the evaluated product should not be counted as an independent special-function theorem. It also does not override a failed squarefreeness or resonance guard.

Fresh controls in `CLASSICAL_MAPPING_CONTROLS.json` verify 15 exact integer Hankel/Toeplitz normalizations and six finite-field shifted-annihilator/diagonal normalizations, N=3,5,7,9,11,13. These bounded controls check signs and substitutions only. They are not evidence for an all-composite theorem or priority.

## What remains a distinct scoped mathematical assertion

### Moving root splitting and ordinary discriminant coefficients

The inherited manuscript's Theorems 1 and 2 begin with the classical static factorization, then vary q and z jointly:

    q(ε)=ω(1+ε²)^(1/d),  q(ε)^d−1=ε²,
    z=α+εx.

The separated leading coefficient is

    H_(Ad+b)(α+εx;q(ε))
      = ε^A (−1)^A d^(A/2) H_b(α;ω)
        He_A(√d x/α) + O(ε^(A+1)).

With F=z^d+1, G=H_b(z;ω), K=dA(A−1)/2 and P_A=∏_(j=1)^A j^j, the claimed ordinary-discriminant coefficient is

    C_sep = (−1)^(A(d−1)/2) d^(dA(A+1)/2) P_A^d
            Disc(G) Res(F,G)^(2A),
    Disc_z H_(Ad+b)(z;q(ε)) = ε^(2K)(C_sep+O(ε²)),

under Disc(G)Res(F,G)≠0.

For one simple overlap G=(z+1)U, the analogous exponent is

    L=dA(A−1)/2+A,

and the coefficient C_ov also involves Disc(J_(A+1)), Disc(U), Res(F,U)^(2A), and U(−1)², with the explicit powers and sign in the frozen Theorem 2. These formulas describe how multiple roots split, not merely where the roots are at q=ω.

Lubinsky–Saff Lemma 4.5 does not determine these coefficients or exact q-discriminant orders. Static data alone is insufficient: z²−t and z²−t² have the same specialization z² at t=0, but their ordinary discriminants have different t-orders. This elementary example explains the logical gap; it is not a counterexample to the project theorem.

The paper's Theorems 2.4–2.5 concern n→∞ with q fixed and irrational in angle. Theorem 2.6, page 337, and its proof on pages 351–353 give a zero-exclusion region and the annulus with outer radius 2√2+1+|1+q|. Such localization permits root collisions and does not provide the moving-root coefficient. Theorem 2.7, page 338, also explicitly assumes an irrational angle. These hypotheses cannot be transferred to a primitive root parameter and a fixed-degree local deformation without a new argument.

Disposition for F020/FUS-02: retain the explicit fixed-root splitting, ordinary-discriminant coefficient, and their arithmetic consequences as the precise remaining comparison targets. Remove static factorization and specialized root multiplicities from their asserted contribution. Retention here means not settled by this source, not novel.

### Derivative statements are reformulations of the leading coefficient

Write D_n(q)=Disc_z H_n(z;q). From the separated expansion one obtains

    D_n^(j)(ω)=0 for j<K,
    D_n^(K)(ω)=K! (dω^(d−1))^K C_sep.

For the overlap replace K,C_sep by L,C_ov. These follow because q^d−1 has derivative dω^(d−1) at ω. They are useful exact derivative normalizations, but once the local discriminant coefficient is known they are immediate reformulations, not additional independent theorem candidates. Lubinsky–Saff's notation D(M/n) must not be confused with D_n here.

### Half order guards and the three composite families

The target is H_((d−1)/2)(z;ζ_d). At its own root of unity the degree is less than d, so Lemma 4.5 has k=0 and reads G_n=G_n. It provides no half-order squarefreeness conclusion.

The inherited characteristic-zero disk result for J(y;τ)=yHe_A(y)−τHe_A′(y), its half-order reciprocal parameter identity |1−τ|=1, and the finite-characteristic inverse-pairing argument are not supplied by the paper's zero-distribution theorems. In particular, a complex parameter disk is not a finite-field nonvanishing argument.

The current Q29 result remains exactly:

    For s in {3,7,11} and every prime p≡1 (mod 4),
    H_((sp−1)/2)(z;ζ_(sp)) is squarefree in characteristic zero
    at every primitive ζ_(sp).

Its project proof uses the parity-complete Hermite pairing exception τ=τ′=2, the same-component augmented product Γ_s Γ_s^ι(2g_s−v_s), and its fixed reduced-coordinate contents 1,49,161051. The s=7,p=13 adverse component is part of why the augmented condition is needed. None of these finite-characteristic, content, or exceptional-component statements is asserted by Lubinsky–Saff.

The conclusion extends the already accepted all-A local overlap formula to lower orders d=3p,7p,11p in this regime. Every such d is 3 modulo 4; the forbidden resonant root remains present. Thus the scalar-bank minimum at these target orders remains m+1. The comparison does not enlarge Q29 to all composite orders, remove repeated-prime restrictions, or establish uniform unramified content support.

Disposition: retain Q29's accepted scoped proof status; close only the Lubinsky–Saff mathematical-body comparison obligation. External priority remains unresolved.

### Reciprocal discriminant and resultant reduction

There are two different reciprocal constructions in the package.

First, for the half-order polynomial at d=4r+1, the inherited content report writes H_(2r)(z;q)=z^r P(z+z^(−1);q). Lemma 4.1 supplies the self-reciprocity enabling that change of variable. The standard reciprocal-quadratic calculation then gives

    Disc_z H = P(2)P(−2)(Disc_u P)²,
    Res_z(z^d+1,H) = H(−1) Res_u(C_d,P)²,

where (z^d+1)/(z+1)=z^(2r)C_d(z+z^(−1)). These two displayed identities are not printed in the reviewed paper, but their elementary reciprocal-quadratic mechanism is classical and was already so classified by the project. Nonappearance here does not promote them. The more specific surviving question is the reduced-coordinate, simultaneous-component obstruction after known special-value units are removed; the paper does not establish that obstruction's uniform nonvanishing.

Second, C03 is the arbitrary-matrix diagonal-pencil Sylvester resultant in the new algebra package. Its universal factors w^v(w−1)^(m²), reciprocal grade, and quotient V(w+w^(−1)) are not the RS polynomial identity of Lemma 4.1. The paper supplies no such arbitrary-pencil theorem. C03 therefore receives no new exact demotion from this source, but it remains a supporting explicit formula based on classical determinant, resultant, and reciprocal-invariant algebra. This is not a cleared originality claim or an RS-derived invention.

## Claim level dispositions and queue changes

- **F020 / ALG-RS-LOCAL / FUS-02:** Keep the accepted scoped moving-root and ordinary-discriminant statements. Explicitly cite Lemma 4.5 for the factorization. Demote static root-of-unity multiplicities and the recurrence to classical consequences. Derivative formulations count with the local coefficient theorem, not as extra results. Replace the unavailable-source blocker with “mathematical body compared; bibliography page missing.” Keep Zhedanov and broader exact-priority comparison open.
- **F021 / ALG-SCALAR-CHIRP-BANK:** Stronger demotion of ingredients. The chirp Hankel determinant, shifted RS annihilator, and forced-diagonal product are direct consequences of Theorem 3.2. Preserve the specific legal-node restrictions, resonance classification, scoped squarefreeness input, and exact common-cycle minimum as the application under review. Do not present the package as a new general Prony/Padé construction.
- **Q29 / composite_guard:** Retain the exact three p≡1 mod4 families and their independently accepted proof scope. The comparison neither proves all-composite simplicity nor clears novelty. Its source-access obligation is reduced, not all priority work completed.
- **ALG-RS-RECIPROCAL-CONTENT / F023-related arithmetic:** Keep reciprocity and reciprocal-quadratic identities classified as classical. Retain the explicit reduced-coordinate obstruction and guarded valuation/carry assertions as the narrower arithmetic statements. No uniform support theorem follows from the paper.
- **C03 / ALG-RECIPROCAL-PENCILS:** No exact matching formula found in this source; keep its current supporting-formula status and external-priority caveat. Do not conflate it with the paper's scalar reciprocal polynomial.
- **FUS-06:** The fixed-degree conditioning result is not settled by this paper's asymptotic zero-distribution results. Its constants, fixed-degree assumption, and legality restrictions remain unchanged.
- **Even bank extra-pole theorem:** Its chirp Hankel determinant is classical by row reversal of Theorem 3.2. The finite exclusion construction giving h≤Q≤h+1 is not supplied by this paper. Preserve its proof scope; do not infer an all-even h-pole optimum.

## Suggested manuscript attribution

“Write H_n for the Rogers–Szegő polynomial denoted G_n by Lubinsky and Saff. We use their Lemma 4.1 for the recurrence and reciprocity, Lemma 4.5 for H_(Ad+b)(z;ω)=(1+z^d)^A H_b(z;ω), and Theorem 3.2 for the chirp Padé denominator and determinant. The shifted moment annihilator and its determinant-ratio diagonal follow from these classical identities by rescaling and row reversal. Our local analysis concerns the joint deformation q^d−1=ε², z=α+εx, its ordinary-discriminant leading coefficients, and the stated guarded arithmetic and legal-node consequences.”

This accurately identifies the mathematical extension relative to the reviewed source without asserting first publication.

## Remaining priority work and stopping boundary

1. Compare the legitimate full text of Zhedanov 1997 and other close sources at the exact moving-root, ordinary-derivative/discriminant, and finite residue-component level.
2. Trace the earlier Padé identities credited by Lubinsky–Saff, particularly Balk, Gragg, and Wynn, before making historical first-attribution claims. The absent reference page should be obtained if that bibliography chain is pursued.
3. Keep mathematical open problems separate: all-composite half-order squarefreeness, repeated-prime arithmetic, and uniform unramified content support are not settled here.
4. Do not interpret the absence of a displayed result in this one paper as proof that it has not appeared elsewhere. The defensible outcome is a completed direct comparison of the available mathematical body, exact attribution of overlapping ingredients, and a narrower list of remaining candidate contributions.

The output provenance manifest records the actual input hashes, page map, visual reading record, and comparison files. Frozen project sources remain unchanged.
