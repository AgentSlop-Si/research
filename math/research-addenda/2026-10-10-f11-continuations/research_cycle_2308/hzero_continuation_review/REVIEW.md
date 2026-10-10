# Independent bounded H=0 continuation review

## Verdict

**PASS within the pinned accepted fixed-F11 atlas boundary.** No correction is required.

The reviewed candidate is `research_cycle_2303/regular_hzero_analysis/CERTIFICATE.json`, SHA-256 `779b560d09cdf9dc6cae1afe5cd568f267bbf1db545c0639dcc937b4b00f4c2b`.

Its final seven-file author seal is `research_cycle_2303/regular_hzero_analysis/SHA256SUMS.txt`, SHA-256 `ed870c0450090dc8244311c450b12a30588acf197a652f46f31e0ffb2341512e`.

The accepted result is precisely:

1. On the regular H=0 chart, the old b=-C0/C1 reconstruction equals a degree-two polynomial B(e) with denominator one.
2. The original guards x83, D25 and g98 are forced nonzero after that reconstruction, by exact polynomial Bezout identities modulo H.
3. The retained original E41 has an explicitly certified 33-term residual P(e,c,q), of degrees (2,3,2). On the same guarded H=0 chart, P=0 and original E41=0 are equivalent.
4. All 50 original residuals, all 19 original guards, the accepted additional guards, chart predicates, ordered reconstructions and three retained input coordinates are preserved, except for the proven equivalent b-definition.

This proves no safe linear pivot, further input elimination, dimension, unrestricted parameters, solution existence, full infeasibility, unrestricted Fourier sufficiency, FFT improvement or novelty. It is not a new fusion. The remaining residual system is open.

## Independent method and evidence

The reviewer wrote `independent_check.py` afresh. It imports only Python standard-library modules and reads historical inputs as inert JSON or bytes. It does not execute or import any author or inherited program. The author program was inspected to locate and understand its data layout; that program's execution and claimed successful assertions are not evidence for this verdict.

Coefficients are normalized ten-component integer vectors over a positive rational denominator. Polynomial arithmetic is sparse and exact. Each distinct coefficient product is computed both by ordinary convolution with descending reduction modulo Phi11 and by cyclic convolution modulo zeta^11-1 followed by elimination of zeta^10. The results agree for all 11,478 products. The checker also verifies the Eisenstein coefficient conditions at 11 for Phi11(t+1), zeta^11=1, and Phi11(zeta)=0.

The independent run checks 35 exact identities, rejects 35 unit perturbations of their right-hand sides, and independently recomputes all 79 bounded author mutation controls. Those 79 include every single residual or guard omission and an unauthorized c!=0 addition. The total is 114 rejected controls. There are 22,077 sparse term products and at most 323 polynomial terms in an intermediate result; the arithmetic result file records the authoritative counts.

The source binding audit verifies the complete content-addressed encodings of all 80 referenced original polynomials, comprising 124,516 terms. This includes every retained residual and guard, all inherited reconstruction data needed for this chart, and x91 restoration. Every definition is checked for acyclic dependency ordering; all sixteen circuit coordinates are eventually bound. Every author-sealed file and every independently pinned input is rehashed at finalization.

## Accepted boundary

The atlas certificate is `research_cycle_2014/fused_chart_atlas/CERTIFICATE.json`, SHA-256 `3fd7382a6207024853f7cf466b05a1f7aba9d9ef7e1b737353711a0394d49024`, accepted by `research_cycle_2016/three_input_atlas_review/RECEIPT.json`. The certificate hash, receipt, all eleven receipt artifacts, and the atlas source and prerequisite hashes are checked.

The historical atlas theorem and the older reductions it explicitly accepts are the trust boundary. In particular, its slice/reconstruction equivalence and nonvanishing facts for b, a, A35, B35 and inherited denominators are accepted, not silently reproved. The continuation registry and its two later exceptional-chart receipts are additionally hash-checked as context. This review does not reprove their exclusions or infer a new global feasibility statement from them.

All new identities are valid over K=Q[zeta]/Phi11 and every field extension of K. No numerical root, sampling, finite-field point search, resultant heuristic, radical assumption or restriction to K-rational roots is used.

## Polynomial reconstruction and guards

Direct exact multiplication verifies

    I*C1 + J*H = 1,
    C1*B + C0 = H*T.

H has degree three in e and B has degree two. The old numerator and denominator are independently rebound to -C0 and C1. The accepted compatibility polynomial is rebound to b*C1+C0-b*H*c.

At every root of H in every extension, the first identity makes C1 nonzero and the second gives B=-C0/C1. Both projection/reconstruction compositions are therefore unchanged: replacing the b-definition changes no downstream value, and the polynomial definition also implies the old rational definition. This argument does not require H to split in K or have distinct roots.

Each guard identity is independently multiplied to one. The guard polynomial is first rebound to its actual original source after x22=1, x49=zeta-c, and b=B(e). For g98, its intermediate b-only expression is also checked. Thus no new interpretation of an original guard is substituted. All three redundant guards remain explicitly present.

## E41 provenance and exact clearing

The review verifies the original x92 numerator and denominator, the exact factorization Dd=zeta^4*b*q*e*D25, and the cancellation yielding

    y=x92+x0*d=Yn/Yd,
    Yn=-(q*b*t*Nd+C*Dd),
    Yd=q*a*Dd.

It directly checks the accepted affine D88 expression, J35=A35*N88+B35*K0, the regular x0 numerator and denominator, and the cross-multiplied identity proving r=-B35/A35 on the chart. N88,D88,N39,D39 are also independently rebound to original source polynomials after the slice bindings.

The full original N25 polynomial is multiplied out and checked against

    alpha(e)+beta(e)*r*(1-x92-x0*d).

The supplied N25n and N25d then agree exactly with substitution of r=-B35/A35 and y=Yn/Yd. The original 22-term E41 is reconstructed from its content-addressed polynomial and cleared with exactly the first powers of N25d and D39. The resulting polynomial equals the supplied 320-term E41_clear.

Exact multiplication verifies

    E41_clear=(q^2*b*D25*a*D39)*E,
    C1^4*E(-C0/C1,c,q,e)=H*Q+P.

The second left-hand side is constructed termwise as a polynomial, without rational evaluation. E has 105 terms and degrees (b,c,q,e)=(4,3,2,3). P has exactly 33 terms and degrees (e,c,q)=(2,3,2). Q and P are multiplied back against H; no claimed division result is trusted.

## Denominators and retained boundaries

- C1 is nonzero on H=0 by the freshly checked inverse identity. The new b-denominator is one.
- q is the retained x41 guard; e and D25 are retained original guards and also have new Bezout proofs.
- b, a, A35 and B35 have accepted nonvanishing proofs and remain explicit additional guards.
- Dd has the exact nonzero factorization checked above.
- N25d=A35*Yd*D25, with Yd=q*a*Dd, uses only those same nonzero factors.
- D39 is the unchanged original x39 reconstruction denominator and must remain nonzero under accepted circuit semantics.
- d and M are unchanged explicit regular-chart predicates for the x0 reconstruction. This continuation makes no separate claim about their zero branches.
- All other inherited denominators and guards are unchanged.

The E41 cancellation factor and all cleared denominators are therefore nonzero on the original chart. At H=0, C1^4 is also nonzero, giving the stated equivalence to P=0. The original E41 is nevertheless retained.

There is no division by c, x0, x49, the leading q coefficient, a factor of P, or any newly assumed nonzero coordinate. Leading-coefficient-zero cases and every originally allowed optional-zero case remain. No algebraic root of H or denominator exception belonging to the accepted chart is discarded. The other H row and all historical exceptional-chart conclusions are outside the new bounded result and are unchanged.
