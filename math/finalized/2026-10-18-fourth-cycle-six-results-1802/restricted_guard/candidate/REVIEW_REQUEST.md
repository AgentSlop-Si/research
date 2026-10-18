# Independent review request

Review the restricted-product precision claims and implementation in this package. Do not modify the source candidate.

Check especially:

1. The height-envelope precision formula is sufficient and its closed form has the exact delta condition. It is not asserted to be globally optimal for restricted products.
2. The low-part plus short-tail reconstruction really recovers all exact coefficients, including zero tail precision, and avoids a hidden wide-by-large-coefficient solve.
3. The lower witnesses are genuinely original m-bit chunk arrays, not merely canonical H-bit factors. Check their degrees, common left factor, fixed divisor at all positive and negative integers, nonzero target coefficients, and invariance under translation.
4. Check the simple 4/5 lower-bound constant and improved constant `(16-log2(200 sqrt(5)/27))/14`, including the m>=t premise.
5. Check every sample product and both forward shifts, the fused inverse-shift explanation, final carry/output work, O(L²W log L) non-product time, O(LW+L³) storage, and the address-cost qualification.
6. Verify that the claimed progress does not contradict the accepted fixed-precision ring-bilinear obstruction, or claim a new fast multiplier or exact restricted optimum.
7. Reproduce RESULTS.json and independently test boundary cases. Consecutive d+1 sample residues determine the entire integer evaluation function modulo the same power, via the Newton-binomial identity; this justifies the finite information minima.

The accepted source reports are dependencies/mersenne_bilinear_guard_20261018_1502_REPORT.md and dependencies/review_correlated_precision_20261018_1515_REVIEW.md. Mandatory qualifications from that review have been retained.
