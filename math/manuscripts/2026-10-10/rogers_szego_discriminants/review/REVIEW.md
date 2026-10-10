# Independent review of the guarded discriminant manuscript

10 October 2026 UTC. Final review of the sealed working manuscript in `research_cycle_2224/discriminant_manuscript/`.

## Verdict

**Accept within the stated guarded scope.** The separated and single-simple-overlap moving-root forms, complete ordinary-discriminant coefficients, integral quotient normalization, conditional arithmetic bridge, parity-complete finite-characteristic pairing, and separate characteristic-zero half-residual-degree refinement are correct as stated. No substantive mathematical correction or missing proof lemma was identified.

Acceptance is bound to:

- `MANUSCRIPT.md`: SHA-256 `3787db24f66bd8dcd2c6d6fceb40b596fe376c84924dae1792717602efbf35be`
- Submitted `MANIFEST.json`: SHA-256 `b50eaa36c3f27aef7fb844e3ab23df8b0d71395a8ad9eec017075865a224b700`
- Submitted `SHA256SUMS`: SHA-256 `39fe39151106fcdf66b4280909be8b8a2d0f85c3d17e00a03b333c68735b53d2`

One pre-seal correction was requested: equation (5.7) had a missing backslash before the left delimiter. It is corrected in the accepted bytes. It did not change a mathematical statement. All 10 submitted manifest entries, 11 checksum entries, and 17 source pins verify independently. The actual exported S02 hash is correctly distinguished from its historical filename hash.

This is a local independent proof review with exact controls. It is not external specialist or journal validation, formal proof-assistant verification, or worldwide-priority clearance. The acceptance does not certify all composite half-degree polynomials, new fixed bases, repeated-prime lifting, or historical certificate arrays not replayed here.

## Review method and independence

The complete final manuscript and its normalization sheet, evidence concordance, and README were read. The comparison used the relevant symbolic proof sections in pinned S01–S04; S06's exact quasi-Laguerre and Wronskian reductions; S24's local, disk, inverse-parameter, resonance, and finite-characteristic proofs; and the Rogers–Szegő sections of R06, R03, P2109, and READY. Source identity and prior acceptance were checked separately from mathematical reasoning. Unrelated Fourier theorems in those broader reports were not part of this review.

No submitted or historical implementation was executed, imported, or used as an arithmetic library. `independent_checks.py` and `boundary_checks.py` were written for this review and use installed SymPy and the Python standard library. Gaussian coefficients are rebuilt by q-Pascal. The local checks expand individual monomials using the binomial theorem rather than executing the submitted generating-series code. Complete target discriminants use ordinary derivatives and exact integer polynomial division. An initial reviewer-script API error was corrected before the successful complete run; it produced no mathematical finding.

Selected primary statements were also freshly checked online. Their exact scope is recorded in `PRIMARY_CITATION_CHECKS.json`; this additional review activity does not contradict the manuscript author's statement that its own finalization inherited the literature inspection.

## Two-case local proof

The recurrence, reciprocal symmetry, and formal q-exponential identity agree with the Gaussian coefficient definition. The q-Lucas phase cancellation is valid for odd d: the relevant exponent difference is a multiple of d. The argument includes the stated d=1, b=0 endpoint.

In the singular logarithm, the degree-one and degree-two terms have pole weights one and two, respectively. Terms of higher singular degree have strictly smaller pole weight. Multiplying by the factorial contributes exactly the factor (−1)^A A! d^A times the residual Pochhammer product and epsilon to power 2A. Thus only the Hermite generating terms attain the separated leading order. The square-root-free coefficient in (3.7) has the correct signs and powers and leading x coefficient F′(alpha)^A G(alpha).

At the shared root, odd reciprocity makes H_b(−1;q) identically zero. The regular term of degree b contributes its first derivative, while degree b+d contributes the even q-exponential coefficient. Both occur at order A+1; all subsequent regular degrees have higher order. The resulting expression is exactly (3.10), hence the stated J with tau=dW/g. The leading x coefficient is g d^A. Replacing this J by an unmodified Hermite polynomial of degree A+1 would change the theorem.

The guards have their full intended force. The separated discriminant and resultant jointly enforce simple disjoint residual roots. For overlap, Res(F,U) excludes an extra root at −1 and any other cluster intersection; it also makes g nonzero before tau is defined. Disc(U) and Disc(J) remain independent requirements in the general-b theorem. No omitted multiple cluster, residual multiplicity, or repeated local model is silently covered.

## Complete discriminant and normalization

Formal simple lifting produces the entire degree count, so the squared-root-difference computation has no missing branches. In the separated case the within-cluster factor is d^(−K) P_A^d; the between-cluster factor is Disc(F)^(A²), with Disc(F)=(−1)^((d−1)/2)d^d. Since A² and A have the same parity, the final sign and exponent are exactly those in (2.4). Residual differences supply Delta and R^(2A).

For overlap the within-cluster exponent is L=K+A. The ordinary clusters and shared cluster contribute P_A^(d−1) Disc(J) with scale d^(−L). The cross-cluster power is d^(dA²+2A), and the extra shared branch contributes the additional g² against the residual roots. Combining these gives the full exponent dA(A+1)/2+A and sign in (2.10). The convention Disc(1)=1 is needed and correctly used when U is constant. The even dependence of q on epsilon justifies the relative remainder of order at least two.

The exact integral quotient is handled correctly. The local coefficient is in q^d−1. Conversion to q−omega introduces (d omega^(d−1))^M; conversion to the value of D_n/Phi_d^M introduces Q_d(omega)^M. Monic integral cyclotomic division occurs before reduction. Galois conjugacy transports algebraic nonvanishing and multiplicity, not an arbitrary numerical modulus statement.

## Arithmetic and finite characteristic

Proposition 5.1 uses p odd, p not dividing d, and A=(p−1)/2<p. These ensure the Hermite product and cyclotomic cofactor are units at the selected component. Nonzero reduction of every required guard in that same component also gives the characteristic-zero nonvanishing needed to apply the local theorem. If Phi_dp divided D_n, exact removal of Phi_d^M would force Phi_dp to divide the integral quotient. Its reduction is Phi_d^(p−1), contradicting the selected unit value. The argument does not require M<p−1.

Canonical coefficient content tests whether the whole guard product survives in at least one field factor. Separate nonzero factors in different components would not suffice. The paired and augmented products in Corollary 5.4 correctly select the simultaneous inverse residual guards; the augmented delta excludes precisely the exceptional parameter. Inversion need not preserve a single irreducible factor.

Proposition 5.3 is parity-complete. Coprimality of consecutive Hermite polynomials holds because all necessary indices are below p. At a nonzero multiple root the Hermite differential equation gives the displayed squared-root location. The inverse parameter has the opposite location. For H and its imaginary transform V, the derivative of H′V−HV′−yHV vanishes; degree p, odd parity, and leading coefficient −1 determine it as −y^p. This excludes simultaneous nonzero multiple roots over the algebraic closure without requiring i in the original field.

Zero is handled separately. Odd A excludes it. Even A gives the exceptional pair tau=tau′=2, exactly when p is 1 modulo 4; its cubic coefficient is −H(0)/6. The denominators are units because this parity has p at least 5. Thus the multiplicity is exactly three, including p=5. No complex-parameter argument is imported into this proof.

## Characteristic-zero refinement

Lemma A.1's complementary q-binomial pairing proves the denominator-free inverse identity. Completing the Pochhammer products gives v=dW with the stated integral product. The principal-embedding sector calculation proves g and 2g−v are nonzero. Galois conjugacy is used only to transport those algebraic nonvanishing statements. At each complex embedding, inversion is complex conjugation and the inverse identity places tau on the circle |1−tau|=1.

Lemma A.2 treats nonzero and zero multiple roots separately. The positive weights in the logarithmic derivative have the required signs. For nonreal tau the imaginary-part comparison forces every nonzero multiple-root parameter outside the stated closed disk. For real nonzero tau the partial-fraction derivative cannot vanish at a real nonpole. At zero, the even-A exceptional value −1/A lies outside the disk. The excluded tau=0 is explicitly retained.

Lemma A.3's diagonal congruence has the correct edge phases. The diagonal metric has positive imaginary part, excluding nonzero real eigenvalues in the principal embedding. The odd-size zero eigenvalue is algebraically simple: the pencil determinant's linear coefficient is nonzero on the one-dimensional kernel. This also covers m=1 with an empty complementary block. The transformation has nonzero derivative at z=1, and the final Galois step transports the polynomial gcd rather than absolute values. Therefore Corollary A.4 is valid only with its stated half residual degree and remaining squarefreeness assumption. It gives no finite-characteristic guard removal.

## Fresh exact controls

All new controls pass; the complete values are saved, not inferred from earlier test counts.

- 33 complete local-cluster initial forms across nine triples: (1,4,0), (3,2,0), (3,2,2), (5,1,2), (3,1,1), (3,2,1), (3,3,1), (5,1,3), and (7,1,3). Every lower epsilon coefficient and every leading x coefficient is checked. The (5,1,3) case deliberately tests overlap away from half residual degree.
- Eight complete symbolic discriminants, with exact integral quotient and full coefficient: (d,A,b)=(1,4,0), (3,2,0), (3,2,2), (5,1,2), (3,1,1), (3,2,1), (5,1,3), (7,1,0). Their exact Phi_d orders are 6,3,3,0,1,5,1,0.
- For each p in {3,5,7,11,13,17,19,23,29,31}, the reciprocal-parameter discriminant-polynomial gcd, after excluding the inadmissible parameters 0 and 1, has exactly the predicted bad set over the algebraic closure. The Wronskian identity and zero multiplicity at tau=2 also pass. These are finite-prime controls of the uniform proof, not an extrapolation.
- Five exact inverse identities at d=3,7,11,15,19, including nonzero g and 2g−v.
- Both Hermite–Laguerre parity substitutions and complete pullback discriminants for A=1 through 8.
- The existing actual boundary (s,p)=(7,13): all inverse residual guards survive, delta vanishes at q²+6q+1, tau=2, and J=y⁷−y⁵−4y³ has a triple zero. The canonical augmented content is 49, so other components remain good.
- The existing separated boundary (d,p)=(5,61): omega=58 gives a repeated residual root although the residual resultant is nonzero; three other primitive roots pass both guards.
- The monic H_2 ordinary discriminant is (q−1)(q+3), whereas its q-difference counterpart is (q−1)(q+1)².

## Citation and scope reconciliation

The Sawa–Uchida version crosswalk is correct: final journal Theorem 3.6/(3.6), pages 844–845, is the quasi-Laguerre result; arXiv v1 uses Theorem 4.8/(4.13). Final Theorem 3.8 concerns adjacent Hermite degrees. These selected statements were freshly verified in the [final paper](https://www.jstage.jst.go.jp/article/jmath/71/3/71_831/_pdf) and [specified preprint](https://arxiv.org/pdf/1802.00605v1).

The ordinary versus operator distinction is supported by [Ismail–Witte (5.12)–(5.13), (5.17)](https://arxiv.org/pdf/math/0012259). Static factorization is appropriately attributed to [Sagan Theorem 2.2](https://users.math.msu.edu/users/bsagan/Papers/Old/cpq-pub.pdf). The established Wronskian mechanism and prime-modulus congruence agree with [Gómez-Ullate–Grandati–Milson Theorem 3.1](https://arxiv.org/pdf/1612.05514) and [Grosu–Grosu Theorem 8](https://arxiv.org/pdf/2007.00065v1). These checks do not assert that those papers state the complete Rogers–Szegő moving-root application.

The guard sheet keeps six historical separated bases, five historical paired-overlap bases, and six current augmented bases distinct. Their prime congruences, p not dividing the lower order, later base-23 provenance, and isolated exceptions are not silently combined. The separated-content valuation is labeled as a different, conditional theorem and is not transferred to paired or augmented content. The concordance explicitly distinguishes R03's local source namespace from the manuscript's source namespace.

LS87's original scan and missing bibliography page 360 were not newly inspected. Zhedanov's distinct 1997 Gauss-sums paper remains a full-text gap. No denied route was requested or bypassed. The narrower fixed-nontrivial-root coefficient, complex disk, and inverse-pair application retain unresolved priority comparisons. The present draft's claims are honest about these limits.

## Final disposition

No further change is required for this sealed working draft. Keep the exact guards, normalization sheet, classical attributions, historical-certificate qualifications, and priority limitations with any downstream copy. A contribution-claiming submission requires the remaining source comparison or its explicit disclosure; this review is not that clearance.
