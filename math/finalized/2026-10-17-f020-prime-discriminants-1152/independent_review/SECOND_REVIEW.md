# Public derivative notice

Private native-table links and row/cell locators are omitted. The original scientific review is bound by ORIGINAL_ACCEPTANCE.json. SCIENTIFIC_PROVENANCE_EXCERPT.json is a redacted original scientific-entry list excluding private canonical-evidence fingerprints. SHA256SUMS.json binds this distributed derivative. Mathematical statements and proof conclusions are unchanged.

# F020: second independent review

2026-10-17 UTC

## Decision and exact scope

**ACCEPT the frozen mathematical packet at its stated characteristic-zero scope.** No mathematical correction to its principal statements, the composition with the accepted version-3 local theorem, or the signed leading coefficients was found. Historical priority remains **UNVERIFIED**. The manuscript's historical baseline and attribution require the additive reconciliation below before public project integration.

For the ordinary z-discriminant D_n(q) of the monic Rogers–Szegő polynomial H_n(z;q), with Disc(1)=Disc(monic linear)=1, the accepted conclusions are:

1. For every odd prime p and n=Ap+b, A>=0 and 0<=b<p,

       ord_(Phi_p) D_n = p A(A−1)/2 + A(b mod 2).

2. For d=p^s, p odd prime, the analogous formula with d replacing p holds for n=Ad+b **only in the stated residual range 0<=b<p**. This review does not enlarge that range to b<d.
3. For every odd d>=3, every primitive dth root omega, every odd 1<=b<d and every A>=1, the original derivative g_b is nonzero and the original overlap polynomial J_(A+1)(x;tau_b)=x He_A(x)−A tau_b He_(A−1)(x) is squarefree. Here He is monic probabilists' Hermite and tau_b=dW_b/g_b retains the original product normalization.
4. The complete separated and overlap leading coefficients in the parameter q^d−1, and their conversions to q−omega and Phi_d, are accepted at the same guarded scope as the inherited local theorem. The all-odd overlap conclusion removes its J guard; it does not supply arbitrary odd-composite ordinary residual squarefreeness.

This is a scoped proof acceptance. F020 stays the canonical owner, F023 an alias; parent status, priority, paired-support and endpoint obligations are unchanged. No even-order, positive-characteristic, numerical-conditioning, faster-FFT or operation-count consequence is accepted.

## Independent proof challenge

### Arithmetic input and field hypothesis

I reconstructed both parity families from the ordinary Hermite recurrence, rather than the first reviewer's factorial construction. For R=U,V and pi^2=2, the scaled polynomials pi^(−m)R_m(1+pi X) are integral and reduce to

    rho_m=X^(m mod 2)(X^2+1)^floor(m/2).

The derivative chain rule gives precisely the factor pi^(−2m+2) in the scaled Wronskian. Its reduction is (X^2+1)^(m−1). Monicity and a unit constant term imply every root X has valuation zero, so every Wronskian root y satisfies v_2(y−1)=1/2. The constant m=1 Wronskian is handled separately.

At a nonzero repeated J-root, consecutive Hermite coprimality justifies elimination and gives

    (tau−1)y=tau(A tau+1),  y=x^2.

Tau=1 is separately impossible; otherwise y belongs to the same field as tau. Parity elimination forces the appropriate Wronskian to vanish at y. If tau lies in an algebraic unramified extension of Q_2, this contradicts its integer valuation group. The zero-root exceptions are exactly tau=0 for odd A and tau=−1/A for even A. No integrality assumption on tau itself is needed.

The field restriction cannot be replaced by nonreality: for A=3 and tau=(−1+2 sqrt(−2))/3, direct exact expansion gives J_4=[x^2−(1+sqrt(−2))]^2. This was independently checked. The root y has the predicted half-integer shifted valuation, and its field is ramified.

For the actual RS parameter, the partial-sum identity tau_b=S_h/S_r and the strict principal-embedding sine sum establish nonreality. Every denominator is nonzero because the order is odd and b<d. Cyclotomic automorphisms commute with conjugation, so the algebraic nonreality assertion passes to all primitive embeddings. An odd cyclotomic field embeds into a finite unramified extension at 2. These facts justify the application; no inference from a numerical plot or finite A sweep is used.

### Static prime-power step

The substitution q=1+t^2, z=−1+tx has the integral Hermite initial form. It gives D_b(q)=(q−1)^[b(b−1)/2]V_b(q) with V_b(1)=product_(j=1)^b j^j. Since Phi_(p^s)(1)=p, a zero at a primitive p^s root would contradict b<p. The fixed-node quotient values are the stated signed odd double factorials; monic division ensures integral quotients. This checks squarefreeness and the deflated separation guards, including b=0,1 and A=0 boundaries. The argument's b<p restriction is essential to this proof; it does not assert that every excluded residual is false.

### Leading coefficients and local parameters

I independently re-derived the coefficients from root-cluster products. For F(z)=1+z^d, Disc(F)=(-1)^((d−1)/2)d^d. A separated cluster at alpha contributes the Hermite discriminant P_A=product_(j=1)^A j^j and scale (alpha/sqrt(d))^[A(A−1)]. Cross-cluster contributions give Disc(F)^(A^2).

In the overlap case, the larger cluster at −1 contributes Disc(J), while the other clusters contribute P_A^(d−1). Relative to the equal-size cluster product, the cross-cluster term adds d^(2A), the internal scaling changes by d^(−A), and the extra interaction with the roots of U=H_b/(z+1) contributes g^2. This recovers exactly the source's sign, total power d^[dA(A+1)/2+A], resultant exponent 2A, Disc(U), and g^2. In particular g is not silently cancelled or raised to an incorrect power.

For exponent M and coefficient C in q^d−1, the exact conversions are

    coefficient in q−omega: C(d omega^(−1))^M;
    (D_n/Phi_d^M)(omega): C[d omega^(−1)/Phi_d'(omega)]^M.

For d=p^s the latter is C(omega^(d/p)−1)^M. The direct full-polynomial controls below check this last quotient independently.

## Fresh controls and input integrity

Only newly written reviewer programs were executed. No uploaded, archived or earlier reviewer program was imported or executed.

- 128 parity-Wronskian cases: U and V, m=1,...,64. The checks use the ordinary Hermite recurrence, parity extraction, integer derivatives and products, and binomial translation y=1+z. Monicity, both Newton endpoints, every Newton inequality and every coefficient of the scaled mod-pi reduction pass.
- Nine complete ordinary z-discriminants over Z[q], n=2,...,10, obtained directly from the Gaussian coefficient recurrence without reciprocal reduction. Together with n=0,1 conventions, these give 38 exact cyclotomic-order and full leading-quotient checks for d=3,5,7,9 in the accepted residual ranges. Every formula matches, including odd overlap, A=3 and d=9 prime-power examples.
- 20 exact parity/Laguerre/kernel-scalar checks for both parities, m=1,...,10, plus two symbolic collision-location identities for unrestricted m. Exact Wronskian squarefreeness controls and the ramified negative control pass. A shift-sensitive control distinguishes y from y−1.
- All 37 entries of the frozen first-review manifest were independently rehashed and match. Its original PDF/ZIP identities remain distinct; this review does not replace them with text-equivalence claims.

These are bounded controls, not substitutes for the unlimited proofs. No failed check or interrupted computation occurred in this second review. The first review's separately documented interrupted d=49 optional control remains an unclaimed upstream attempt.

## Prior-art reconciliation

I independently inspected the primary texts and checked the comparator's exact identities. With s=0 or 1, alpha=s−1/2, A=2m+s−1 and C_m=(−1)^m 2^m m!,

    R_m(y)=C_m L_m^alpha(y/2),
    W_m^R(y)=−2^(2m−2)m!(m−1)! f_(m−1)^alpha(y/2,y/2).

Thus the parity Wronskians are diagonal Laguerre Christoffel–Darboux kernels. Their characteristic-zero squarefreeness is a **known consequence** of affine nonsingularity: symmetry turns a repeated diagonal zero into an affine singularity. The small m cases are explicit. This is not a new standalone theorem. Source: Sawa–Uchida, equation (5) and Lemma 3.2, [primary manuscript](https://da.lib.kobe-u.ac.jp/da/kernel/90009429/90009429.pdf).

With c=A(tau−1)/(2m), the evaluation argument in the known quasi-Laguerre formula satisfies

    2[m c^2+(2m+alpha)c+m+alpha]/c = tau(A tau+1)/(tau−1).

The general collision/discriminant mechanism therefore receives classical attribution. The rational display must be cancelled before special-parameter substitution; the apparent denominator does not justify omitting the genuine zero-root exceptions of J. Source: Sawa–Uchida, Theorem 3.6, equation (3.6), printed pp.844–845, [published primary text](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf).

The exact shifted valuation is a separate arithmetic input. A descending-power Newton-polygon slope in the cited paper and an ascending-power slope here have opposite root-valuation conventions. The physicists/probabilists Hermite conversion also uses sqrt(2), a ramified scaling. Neither shared terminology nor a shared displayed slope identifies the statements. This comparison establishes no worldwide novelty for the shifted calculation or its RS application.

## Canonical reconciliation and permitted integration

Fresh read-only native inspection at approximately 11:57 UTC confirms:

- F020 remains TO RESEARCH, priority 58; F023 is an alias.
- The all-m paired-support gate remains OPEN 58 and the general endpoint gate OPEN 53.
- Later accepted fixed-residual all-A overlap families through odd b=31 are already recorded. The new theorem is uniform beyond this coverage and supplies another proof within it. The October-11 b=1,3 baseline must not be presented as the latest project state.
- Existing derivative/nonvanishing/separation inputs retain their recorded exact scopes and provenance. They are not new discoveries in this cycle.
- The Lubinsky–Saff full mathematical-body comparison is already recorded. This review did not repeat that audit; current access limitations cannot erase it. Remaining recorded gaps include reference page 360/citations 9–36, Zhedanov 1997 full text, and broader local/arithmetic priority. The focused Sawa–Uchida comparison narrows attribution without clearing those gaps.
- The October-16 bounded low-order cyclotomic deflation remains a distinct accepted result. All-m characteristic-two paired support and endpoint claims do not follow from the present characteristic-zero overlap theorem.


The scientific acceptance permits an additive, history-preserving report and bounded evidence/gate clarification under the existing owner after coordinator review. It does not support parent closure, priority changes, resetting accepted subfamilies, promoting novelty, or erasing source failures. Exact external application must be reviewed separately; this verifier made no external writes. Raw native snapshots are private and excluded from this public packet.
