# Independent bounded review: E25 and zero-resultant pseudo-remainder

## Decision

**PASS within the accepted regular H=0 fixed-F11 chart.** Fresh exact arithmetic independently reconstructs original E25, verifies its guarded cancellation, and obtains the claimed 54-term remainder S(e,c,q), with degrees (2,4,3). The division-free 5-by-5 Sylvester determinant of the accepted E41 remainder P and S is identically zero modulo H. The supplied nonzero cofactor syzygy and full polynomial pseudo-division identity are correct. The resulting necessary linear consequence has the form L1(e,c)q+L0(e,c), with 30 terms in each coefficient.

Only the conditional reconstruction q=-L0/L1 on L1!=0 is justified. The entire L1=0 case remains, with q retained and L0=0 required, together with every original chart predicate. The calculation provides no nontrivial q-free condition from this determinant and no global elimination of q.

All 50 original residuals, all 19 original guards, every additional guard, every branch predicate, every reconstruction definition, and both original reconstruction/projection maps are preserved verbatim. No optional-zero coordinate is newly excluded. All algebraic roots of H over every field extension of K remain in scope.

## Hash-bound trust boundary

The accepted base is research_cycle_2303/regular_hzero_analysis/CERTIFICATE.json, SHA-256 779b560d09cdf9dc6cae1afe5cd568f267bbf1db545c0639dcc937b4b00f4c2b, accepted by research_cycle_2308/hzero_continuation_review/RECEIPT.json, SHA-256 8d9767ba65f61fce39676dadd7b187d520ceb3f770b8f8b4401bfaf6c6b34127. Its atlas theorem and the earlier reductions explicitly accepted there remain assumptions of this bounded review. They are not reproved here.

The reviewed author packet is research_cycle_2325/f11_zero_resultant/. Its final CERTIFICATE.json hash is ed080d2ac61ef9b1fd68243c559eba953069c6ff53cc2f525c1f056ef966fc58; AUTHOR_RECEIPT.json hash is 4232cdd941d47089c3fb661e37f1cb15dd7a031f107026602616302e6b709aed; SHA256SUMS.txt hash is 47b60f15c14d37a112ff875702add0f46d43f9b4637176b6ca3949b976dc27d3. All 15 manifest entries and all 30 source-file pins were verified against the sealed bytes.

No author or inherited program was executed, imported, or used as an executable library. The independent checker was written afresh. It reads inert JSON and performs standard-library integer-vector/rational cyclotomic arithmetic. Source polynomial content hashes and canonical forms were checked for all 80 accepted original polynomial bindings, comprising 124,516 terms. The author programs are hashed as inert files only.

## Exact checks

1. Reconstruct original E25 from its content-addressed 55-term source polynomial, bound to retained E25. Initial coordinate substitutions and accepted reconstruction formulas are applied termwise. Each of x25, x39, x65, x88 occurs with maximum degree one, so clearing Den=N25d*D39*Dd*A35 is exact. The result has 882 terms and degrees (b,c,q,e)=(10,4,8,6).
2. Independently rebuild F=q^2*b*e*D25^2*a^2*D39 from the accepted data. Verify Clear25=F*Reduced25, with Reduced25 having 204 terms and degrees (6,4,3,3). Original N39, D39 and D25 are rebound to their source polynomials. The Dd and N25d factor identities are checked exactly.
3. Form T25=C1^6*Reduced25(-C0/C1,c,q,e) termwise without rational simplification, and independently divide in e by H. Both the supplied 339-term quotient and 54-term remainder are reproduced. The accepted C1 inverse and polynomial b-reconstruction identities are also rechecked exactly.
4. Bind P to the previously accepted 33-term E41 remainder. Recompute all q coefficients of P and S. Compute the fixed-degree Sylvester determinant using exterior-product row accumulation, with only coefficient-ring additions, multiplications and reductions modulo H. No leading q coefficient or parameter polynomial is inverted. The determinant is zero.
5. Verify the supplied U,V are a genuine signed Sylvester cofactor vector; verify they are nonzero with the stated q-degree bounds, and check U*P+V*S=H*QB as a full polynomial identity, before quotienting by H.
6. Independently perform two division-free pseudo-division steps. Reproduce the multiplier M=remainder_H(p2^2), quotient Qp and remainder L. Verify the full polynomial identity M*S-Qp*P-L=H*QH and both displayed formulas for L0 and L1. L has 60 terms and degrees (e,c,q)=(2,9,1), with 30 terms in each coefficient.

Coefficient multiplication uses cyclic convolution modulo zeta^11-1 followed by the Phi11 relation. The first 250 nontrivial coefficient products and regularly spaced later products are cross-checked by a separate descending Phi11 reduction. Only the fixed nonzero element of K that is the leading coefficient of H is inverted for H division. No irreducibility of H is assumed, and the quotient coefficient ring is not treated as a field.

The determinant implementation also passes identity-matrix, sign-change and nonzero-resultant controls. The padded-polynomial warning is verified exactly: q+1 and q+2, treated as quadratics, have zero fixed-size Sylvester determinant although their difference is the unit 1. Thus the zero determinant alone cannot certify a common affine root after degree drops, much less feasibility of the full original system.

## Guard and conditional-cover audit

The clearing denominator is nonzero on the unchanged accepted chart. N25d=A35*q*a*Dd*D25, Dd=zeta^4*b*q*e*D25, and D39 is the unchanged inherited x39 denominator. A35 and a are retained accepted extra guards; b is a retained accepted extra guard; q, e and D25 are original guards; D39 is required nonzero before evaluating its original reconstruction definition.

The cancellation factor F therefore contains only already nonzero factors. C1 is invertible on H=0, with its accepted exact inverse rechecked. Consequently, on the original guarded chart,

E25 = F*S/(Den*C1^6),

and E25=0 if and only if S=0. Original E25 nevertheless remains in the retained residual list.

Every full chart solution has P=S=0, hence L1*q+L0=0. Over any field extension this yields an exhaustive conditional cover:

- L1!=0: q=-L0/L1, and every original residual, guard, reconstruction denominator and branch predicate must still be tested.
- L1=0: retain q and require L0=0 together with the entire original chart. No part of this zero-pivot case is discarded and its feasibility is undecided.

A nonzero formal polynomial L1 need not be nonzero at a particular solution. There is no division by p2, s3, c, x0 or x49, and no exclusion of their zero cases. The unchanged preserved_chart is authoritative; the cover is a proved possible refinement, not an implicit replacement by L1!=0.

## Negative controls and limits

The independent verifier rejects 80 deliberate mutations: changed E25 reconstruction, cancellation factor, remainder, syzygy or pseudo-remainder; each of the 50 possible individual original-residual deletions; each of the 19 possible individual guard deletions; and six unproved nonzero restrictions. No mathematical defect was found within the reviewed scope.

This review establishes an exact additional residual, the bounded zero-resultant obstruction, and a necessary linear consequence with a conditional reconstruction cover. It does not decide feasibility, infeasibility, dimension, unrestricted parameters, global q elimination, novelty, general Fourier sufficiency, a new fusion, or an FFT improvement. The H!=0 chart and all previous exceptional conclusions are untouched. No external writes were performed.

## Reproduction and receipt

From the workspace root, run the newly written independent_check.py in this review directory, then finalize_review.py. The independent checker emits EXACT_CHECKS.json, NEGATIVE_CONTROLS.json, INPUT_PINS.json, INDEPENDENT_LINEAR_COEFFICIENTS.json and ARITHMETIC_RESULT.json. The finalizer validates the author seal and all input hashes again, then emits the hash-bound RECEIPT.json and review manifests. Historical and author programs must not be invoked to reproduce this independent review.
