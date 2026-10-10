# Zhedanov comparison: verified overlap and remaining access gap

10 October 2026 UTC. Bounded literature comparison against the accepted discriminant manuscript, SHA-256 `155434da08c53789edce92664c825e72c2ef7641ce405a96ec8fed4b1e0a641b`.

## Conclusion

The Zhedanov 1997 full-text obligation is **still open**. The exact bibliographic record and abstract were verified, but the six-page mathematical body was not obtained through the lawful routes checked. Consequently no theorem, equation, or individual page number is attributed to that unseen body, and this report does not assert that the candidate results are absent from it.

Inspectable primary papers do sharpen the boundary. Static root-of-unity factorization, the continuous-q-Hermite/Rogers–Szegő change of variables, the ordinary q-to-one Hermite limit, and taking q to a fixed root of unity are established ingredients. The manuscript's narrow comparison targets remain its fixed odd-order cluster polynomials and ordinary-discriminant constants, half-order resonance result, complete finite-characteristic inverse pairing, and same-component arithmetic theorem. Their mathematical acceptance is unchanged; their publication priority is not certified.

## Sources and what was actually inspected

1. **Z97:** A. S. Zhedanov, “Gauss sums and orthogonal polynomials,” *International Journal of Modern Physics A* 12 (1997), 289–294, [DOI 10.1142/S0217751X97000438](https://doi.org/10.1142/S0217751X97000438). Connected SciSpace returned the exact DOI, author, 1997-01-10 date, `is_oa=false`, `fulltext_url=null`, and only an ADS abstract locator. Its abstract describes finite q-Hermite orthogonality with complex Gauss-sum weights, also used for Stieltjes–Wigert and Rogers–Szegő orthogonality on regular polygons. This is abstract-level evidence only. The [author's Renmin publication list](https://math.ruc.edu.cn/szdw/rxjs/af49fa5636884e17a5ed5518a41f8025.htm), item 22, corroborates the 1997 volume and page range in indexed text. An inconsistent 2012 date on ResearchGate is not adopted.

2. **LS87:** Lubinsky–Saff, [DOI 10.1007/BF01890574](https://doi.org/10.1007/BF01890574). The supplied mathematical-body comparison is inherited, not falsely presented as a second fresh reading. It gives Lemma 4.1, p. 343, (4.1)–(4.5), for recurrence/reciprocity; Lemma 4.5, p. 346, (4.15), for the static factorization; and Theorem 3.2, p. 340, (3.11)–(3.12), for chirp determinant and Padé denominator. The source credits earlier work; its reference page 360 is still missing.

3. **AKK09:** Atakishiyeva, Atakishiyev and Koornwinder, [arXiv:0811.4100v2](https://arxiv.org/html/0811.4100v2), “On a q-extension of Mehta's eigenvectors of the finite Fourier transform for q a root of unity.” Relevant equations and their page locations were checked against searchable [institutional PDF text](https://pure.uva.nl/ws/files/848901/75463_0811.4100v2.pdf): (2.2), p. 3; (2.7)–(2.8), p. 4; Remark 3.4, (3.8), p. 6. Section 2 cites Z97 for complex-weight orthogonality on the zeros of the terminal Chebyshev polynomial. That attribution does not substitute for reading Z97.

4. **SZ96/97:** Spiridonov–Zhedanov, [arXiv:q-alg/9605034v1](https://arxiv.org/pdf/q-alg/9605034v1), 21 May 1996, “Zeros and orthogonality of the Askey–Wilson polynomials for q a root of unity.” The inspected p. 2 explicitly warns that complex recurrence coefficients do not imply simple roots, with the example P3(x)=x(x²−u1−u2), u2=−u1. Page 3, (2.1)–(2.4), takes q=exp(ε+2πiM/N) to its root-of-unity limit to evaluate the terminal-degree polynomial. The later [v2 HTML](https://arxiv.org/html/q-alg/9605034v2) was also inspected. These are separate papers from Z97.

## Exact comparison targets

### Established polynomial and chirp ingredients

Write K_n for AKK09's continuous q-Hermite polynomial and H_n for the manuscript's Rogers–Szegő polynomial. Its (2.2) gives

    K_n(cos θ;q) = exp(inθ) H_n(exp(−2iθ);q).

Combining this with its (2.8), K_(Ad+b)=(2T_d)^A K_b, gives the manuscript's H_(Ad+b)=(1+z^d)^A H_b by substitution. This is another explicit classical record, consistent with the earlier LS87 match. AKK09 (3.8) also records the standard q→1 Hermite scaling, citing earlier literature. Neither the change of variables nor the general appearance of Hermite polynomials should be advertised as a new ingredient.

The manuscript's Proposition 10.1 uses the shifted chirp annihilator T_m(z)=(−1)^mH_m(−z;q). Its determinant and denominator are already mapped to LS87 Theorem 3.2 by row reversal and generating-series rescaling in the inherited comparison. Z97's abstract establishes subject proximity to Gauss-sum orthogonality, but supplies no inspectable determinant normalization or exact annihilator equation. Do not replace LS87's precise citation with an invented Z97 equation reference.

### Local moving-q ordinary-discriminant theorem

The manuscript's Theorems 3.1–3.2, equations (3.1)–(3.9), fix an odd d≥3 and n=Ad+b, deform q by q^d−1=ε², and scale z=α+εx. They identify both the separated Hermite cluster and the shared-root polynomial y He_A−τ He_A′, with complete ordinary z-discriminant leading constants and exact cyclotomic orders dA(A−1)/2 and dA(A−1)/2+A under their respective guards.

These are more specific targets than either a static factorization or a q→1 limit. Likewise, SZ96's terminal-degree limiting evaluation shows that “moving q toward a root of unity” alone is too broad a contribution claim. This distinction is an assessment of the displayed formulas, not evidence that no earlier paper contains the local theorem. Z97 body-level comparison is unresolved.

### Half-order resonance and guard removal

The manuscript's Theorem 5.2, (5.4), asserts the exact gcd with z^N−1 for T_((N−1)/2): 1 for even half degree, z−1 for odd half degree, with a simple forced root in the latter case. Theorems 4.1 and Lemma 5.1 give the parameter-disk and inverse identity used in Corollary 5.3 to remove the quasi-Hermite guard.

Finite orthogonality on the support of a terminal-degree polynomial does not itself determine the zeros, gcd, or ordinary discriminant of this lower-degree polynomial. Complex weights give no positive-measure shortcut, as the explicit SZ96 counterexample confirms. Z97's abstract therefore cannot certify or refute this resonance theorem. Exact formulas and hypotheses from its body are still needed.

### The five composite squarefreeness families

The manuscript's Theorem 6.1 has the exact simultaneous-failure exception p≡1 mod 4 and τ=τ′=2, with triple zero. Lemma 7.1 and Theorem 7.2 use a single residue-field component, the augmented product Γ_s Γ_s^ι(2g_s−v_s), and integral cyclotomic division before reduction. Appendix A and (8.6) give contents

    s = 3, 7, 11, 15, 19
    c_s^+ = 1, 7², 11⁵, 3¹²5⁹, 19¹¹.

Theorem 9.1 consequently covers H_((sp−1)/2)(z;ζ_sp) for all primes p≡1 mod 4 with p∤s; the s=15 family excludes p=5. Corollary 9.2 supplies every local index A. This is the current five-family scope, superseding the older three-family description in the LS87 comparison. It is not a new proof supplied by this literature pass.

None of the inspectable abstract-level Z97 evidence contains the necessary residue-component, exceptional-parameter, or ordinary-discriminant assertions. This does **not** establish their absence from Z97. Preserve the theorem's accepted scope while marking exact prior-art comparison pending. All-composite squarefreeness, repeated-prime extensions, and uniform arbitrary-base content support remain separate open mathematical problems. All these target orders are 3 modulo 4, so the scalar-bank minimum remains m+1 by the existing resonance result.

## Access outcome and next evidence required

The publisher landing/abstract/PDF and ADS abstract/archive routes did not return inspectable Z97 text. Ordinary read attempts to the publisher and ADS archive returned HTTP 403; they were not bypassed. Public author, arXiv, institutional-repository and exact-title/DOI searches located bibliography/abstract records or different papers, not Z97's body. SciSpace supplies metadata, not the full text here. No purchase, login, author contact, access-control circumvention, or PDF redistribution was performed.

To close this particular obligation, obtain a lawful author manuscript or user/institution-supplied copy containing pp. 289–294, including bibliography, then compare its actual numbered formulas with the targets above. Until then, the precise status is “bibliography and abstract verified; exact mathematical-body comparison pending.” Search failure is not novelty evidence, and completing that one comparison would still not certify worldwide priority.

The frozen manuscript and prior accepted records were not modified. `STATUS_DELTA.json` is a local proposal for the existing master table, not a new sheet or an external write.
