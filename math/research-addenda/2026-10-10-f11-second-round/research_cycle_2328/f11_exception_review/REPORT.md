# Independent review of the fixed-F11 affine exception

Date: 2026-10-10 UTC.

## Bounded verdict

PASS for the sealed candidate's mathematical content. Within the accepted regular H!=0 chart, the retained A(b,e)=B(b,e)=0 exception necessarily satisfies the explicitly stored monic degree-10 equation F10(e)=0. The full A=B=0 residual circuit remains compulsory on that locus. The F10!=0 piece is excluded; the F10=0 piece is retained unresolved.

This does not show that the exception is empty, that F10=0 is sufficient, that F10 is irreducible, or that a feasible Fourier factorization exists. It does not modify the generic A!=0 chart, the separate H=0 chart, any ranking, or external research records. No novelty, dimension, full-support factorization, generic FFT, or speed claim is accepted or made.

Candidate: research_cycle_2325/f11_affine_exception/CANDIDATE.json

Candidate SHA-256: 67cb144d8adc3c25909e2e6c13b5bcf32abe49ccef69ab51fb77a1f508aacd0f

Accepted base review: research_cycle_2310/hnonzero_continuation_review/RECEIPT.json

Base review SHA-256: 22e0babbd1d637a38a355bed333317fb1f38c98057403715374fcdd066880d9e

## Independent exact work

The fresh checker reads inert JSON certificates, never imports, inspects, or executes an author or inherited research program. Arithmetic uses Python's standard library only. Coefficients are reduced rational vectors in K=Q[zeta]/Phi11. Every distinct coefficient product is checked by two arrangements: ordinary convolution followed by long Phi11 reduction, and cyclic convolution modulo zeta^11-1 followed by subtraction of the tenth coefficient. All reasoning concerns K and every field extension of K; there is no modular, numerical, or sample-point feasibility inference.

The independent checker verifies:

1. Every accepted prerequisite pin supplied by the accepted review, candidate source pin, and unchanged exception record.
2. A=b^3 e alpha and B=b^3 e beta, with alpha of b-degree 3 and beta of b-degree 2. A fresh Euclidean calculation shows that their joint coefficient content in K[e] is 1. The nonzero resultant rules out a common factor of positive b-degree. Thus the exact bivariate gcd of A and B is b^3 e up to a nonzero K scalar.
3. The resultant in b by evaluating the 5 by 5 Sylvester determinant directly with subset dynamic programming. This computation has no polynomial or leading-coefficient division. Its full coefficient vector matches the candidate's degree-53 resultant.
4. The exact multiplication identity expressing the resultant as a nonzero scalar times H^9 D25^4, five monic linear factors with multiplicities 1,1,4,4,2, and the candidate's monic F10 with multiplicity 1. No factorization algorithm or claim of irreducibility is trusted.
5. Every coefficient of all five root specializations, all Bezout identities, all G-divisibility identities, and independent specialized Euclidean gcds. The specialized (alpha degree, beta degree, gcd degree) triples are (2,1,0), (3,2,1), (1,0,0), (1,0,0), and (2,1,0), in the candidate's linear-factor order.
6. The two coefficients of the cleared F_A polynomial, derived independently from the accepted atlas by substituting c=cn/cd and multiplying by cd=bH. The c-clearing exponent is exactly one. In the sole linear-G case, both q coefficients are divisible by G. Consequently every possible q, including the original required q!=0 values, forces F_A=0 at the common b root, contrary to the inherited F_A!=0 guard.

The successful run completed 168 exact checks and rejected 16 semantic corruptions without using a candidate-hash gate. Corruptions include altered resultant/factor/Bezout data, an omitted fifth linear branch, a missing q coefficient in the guard obstruction, a removed residual, removal of the q guard, a new optional x0!=0 restriction, a dropped cancellation ledger entry, an altered clearing power, removal of the unresolved decic branch, and unjustified infeasibility or sufficiency claims. The run dual-checked 17,102 distinct coefficient products and completed in approximately 11 seconds.

## Zero, leading-coefficient, and cancellation cases

The only initial common monomial canceled is b^3 e. Its nonvanishing follows from the accepted additional b!=0 guard and the original x83=e!=0 guard. The proof does not infer either guard from polynomial gcd data.

Common finite b roots imply vanishing of the fixed-size Sylvester determinant even when leading coefficients vanish. Therefore the necessary resultant condition introduces no generic-leading-coefficient assumption and drops no lower-degree specializations. A nonzero resultant polynomial is never treated as having no roots.

The factors H and D25 can be removed from the vanishing product only because H!=0 is the explicit accepted chart condition and D25!=0 is an original retained guard. The product's scalar is a verified nonzero element of K. Each of the five remaining linear zero cases is separately excluded: four by U alpha+V beta=1, the fifth by U alpha+V beta=G together with G dividing both cleared F_A coefficients. These identities remain valid at intersections of linear factors or at degree drops. No additional nonzero condition on a specialized leading coefficient is assumed.

For the F_A obstruction, cd=bH is nonzero throughout the accepted chart; multiplying F_A by cd cannot create the contradiction. The checker also directly verifies the obstructed root has nonzero b and H. No new division in q, x0, another optional-zero coordinate, a resultant factor, or F10 is introduced.

## Predicate retention and maps

The complete retained_exception object is byte-for-byte equal as parsed JSON to the accepted A=B=0 branch record. Its 50 original residual equations and 19 original guards match the accepted atlas. Every additional equation, guard, regular-chart condition, ordered coordinate definition, and denominator justification is unchanged. In particular, q!=0 and e!=0 remain original guard tests, while no new full-support requirement is imposed on original optional-zero coordinates.

The candidate's coordinate cancellation ledger, E41 denominator, E41 cancellation quotient, c denominator, and c-clearing exponent are equal to the accepted base fields. Their historical correctness remains within the accepted base's trust boundary; they are not silently replaced or re-proved by a new formula.

The new partition F10!=0 versus F10=0 is exhaustive and disjoint. The first has no retained solution by the verified necessary-condition proof. The second runs the same reconstruction and every original/accepted predicate and retains the same three inputs (b,q,e). Both projection/reconstruction wrapper maps are the identity on these retained inputs. Therefore adding F10=0 preserves exactly the accepted exception's solution set; it does not establish existence or a new parameter count.

## Trust boundary and reproduction

The accepted base review and the historical theorems it accepts remain prerequisites. This review independently checks the new source bindings, exact determinant, factor product, all five branch certificates, cleared-guard obstruction, and retention/equivalence wrapper. It does not re-prove the historical atlas, reconstruct every original Fourier edge equation from scratch, or decide feasibility of the surviving decic locus.

From the workspace root:

    python research_cycle_2328/f11_exception_review/check_independent.py

The review's RECEIPT.json binds the candidate, author seal, author artifacts, source hashes, arithmetic receipt, report, and fresh checker. Program files in the author packet are hash-bound only, not inspected or executed.
