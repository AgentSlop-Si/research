# ALG-032: omitted even-step/even-intercept dyadic slice

## Result and exact disposition

For the specified single-sketch natural adjoint decoder, the omitted even-d/even-b case is resolved by an exact DC error. Let M = 2^L with L >= 2, let K be any positive integer, N = KM, let a be odd, and let s_r = b + dr with b and d even. On the fixed input x_n = 1, the decoder returns Xhat_0 = 2 sqrt(N), whereas the unitary DFT has X_0 = sqrt(N). Thus

|Xhat_0 - X_0| / (||x||_1 / sqrt(N)) = 1.

This disproves the maximum-bin bound with any 0 <= epsilon < 1 for this decoder and every seed satisfying these guards. It is not merely a finite numerical observation. The statement needs neither even K nor K < M. In the source's original K-even, 2 <= K < M regime it supplies exactly the omitted parity branch.

Disposition: new elementary completion of an explicitly unclassified source slice; author proof and exact controls, pending independent review. The old accepted affine/dense-pair/collision results retain their original status and do not receive duplicate closure credit. ALG-032's broader primary-source comparison gate, score 34, history, status, changed-measurement/repetition obligations and historical-priority limits remain unchanged.

## 1. Decoder fixed before the claim

Write e_M(z) = exp(2 pi i z / M), r = 0,...,K-1 and t,u = 0,...,M-1. The source specifies

sigma_(r,t) = e_M(a t^2 + s_r t),
y_r = sum_t sigma_(r,t) x_(rM+t),
H_r(m) = sum_u conjugate(sigma_(r,u)) e_N(-m u),
Xhat_m = (1/sqrt(N)) sum_r e_K(-mr) y_r H_r(m).

This proof holds that decoder and its normalization fixed. It does not insert calibration, access to raw input, different measurements, or extra sketches. For x_n = 1, put S(s) = sum_t e_M(a t^2 + s t). Then y_r = S(s_r) and H_r(0) = conjugate(S(s_r)), so

Xhat_0 / sqrt(N) = (1/N) sum_r |S(s_r)|^2.  (1)

No alias-bin nonzeroness or inverse of d is needed at DC.

## 2. Self-contained Gauss-norm proof

For M = 2^L >= 4 and odd a, substitute t = u+h modulo M into the squared magnitude:

|S(s)|^2 = sum_(h mod M) e_M(a h^2 + s h) sum_(u mod M) e_M(2 a h u).

By finite geometric-sum orthogonality the inner sum is M if M divides 2ah and zero otherwise. Since gcd(a,M) = 1, precisely h = 0 and h = M/2 survive. Therefore

|S(s)|^2 = M [1 + e_M(a M^2/4 + s M/2)]
          = M [1 + exp(2 pi i a M/4) (-1)^s]
          = M [1 + (-1)^s],                                  (2)

because 4 divides M. This proves 2M for even s and zero for odd s directly; it does not rely on a numerical Gauss-sum evaluation or a division by the nonunit 2.

If b,d are even then every s_r is even, so (1) and (2) give Xhat_0/sqrt(N) = K(2M)/(KM) = 2. The true DFT of x_n = 1 equals sqrt(N) at DC and zero elsewhere; ||x||_1/sqrt(N) = sqrt(N). Hence the claimed normalized error equals one.

## 3. Complete even-step consequence

For any even d and arbitrary integer b, (1)-(2) give

Xhat_0/sqrt(N) = 1 + (-1)^b,
(Xhat_0-X_0)/sqrt(N) = (-1)^b,
|Xhat_0-X_0|/(||x||_1/sqrt(N)) = 1.

For b odd, the stronger previously recorded statement y_r = 0 for every r makes the entire decoded vector zero. For b even, the newly completed branch is DC overshoot; this proof does not claim that its entire decoded vector is constant or zero away from DC. Together these cover every even affine step for every positive K in the original odd-a, M >= 4 dyadic model. The same DC identity applies to any slope sequence of one common parity, but no new algorithmic or novelty claim is assigned to that elementary observation.

## 4. Dimensions, endpoints and guard checks

- K is a positive integer; K = 1, odd K, K = M and K > M all obey the proof. K = 0 does not define this normalized transform and is excluded.
- M = 4 is included: M/4 = 1 makes the proof valid. There is no missing smallest admitted block size.
- M = 2 is outside the source's stated M >= 4 branch. Directly, for odd a, S(s) = 1 + (-1)^(a+s) and |S(s)|^2 = 2[1-(-1)^s]. Thus the two DC outcomes swap: even d/even b gives zero and even d/odd b gives 2 sqrt(N), still with normalized error one. The displayed 2 sqrt(N) conclusion for even b must not be extended to M = 2.
- M = 1 is a genuine nonfailure exception: every sketch equals its single raw coordinate and the decoder is the exact K-point unitary DFT. Flat-input DC is exact. The theorem must not be stated for all powers of two without a lower-size guard.
- Odd a is essential to (2). With M = 4, a = 0, b = d = 0, the normalized decoded DC is 4, not 2. No classification for even a is claimed.
- Even d is essential to the uniform parity/DC-error conclusion. For odd d, Xhat_0/sqrt(N) = 1 + ((-1)^b/K) sum_(r=0)^(K-1) (-1)^r: it equals 1 for even K and 1+(-1)^b/K for odd K. The source's separate odd-d nonzero-alias resonance is unchanged.
- Parities refer to integer representatives modulo the even modulus M, so they are representation-invariant. Negative or unreduced a,b,d introduce no extra cases.
- For any nonzero constant input x_n = c, both error and target scale by |c|, giving the same normalized error one. The zero input is exact and has no nonzero normalizing scale.
- The exact error one contradicts a non-strict error guarantee only for epsilon < 1. It does not by itself refute epsilon = 1.

## 5. Boundaries retained

This is a one-sketch, fixed natural-adjoint-decoder obstruction on one explicit fixed flat input. It is not a sketch-only information-theoretic lower bound for every decoder. Dividing the output by two would remove this even-b DC overshoot, illustrating why a changed decoder needs its own analysis; that change is neither endorsed nor analyzed here, and it cannot recover the all-zero sketches in the odd-b branch by simple linear rescaling. Repeated sketches, aggregation, nonlinear reconstruction, altered phases/measurements, side information, arbitrary-input concentration, runtime claims and historical priority are not settled by this lemma.

The existing dense-pair theorem permits nonlinear sketch-only postprocessing under its different stated hypotheses. This result neither reproves nor broadens it. Likewise the maximum-bin epsilon ||x||_1/sqrt(N) contract is preserved; no relative-l2 rank-barrier argument is substituted.

## 6. Evidence and reproducibility

Source: AFFINE_RESONANCE.md, section 2, exact SHA256 504e7f01540b55df9a65692fe6d79e87fee014e7b08ab7f50f0bf499239aad55. The source explicitly leaves even-d/even-b cases unclassified. SOURCE_REGISTER.json records the pinned repository path and source provenance. Only source text was inspected; no supplied research program was executed.

The accompanying fresh self-authored exact_controls.py uses integer exponent counts in the cyclotomic quotient Z[z]/(z^(M/2)+1), rather than floating-point evaluations, to check the finite controls. The mathematical proof above establishes the unbounded theorem; finite checks independently test transcription, signs, normalization and edge guards. CONTROL_RESULTS.json records actual coverage and exceptions: 2,730 exact Gauss identities, 599,144 even-step DC cases, 21,816 odd-step guard controls, and 16 negative-representative checks passed. The finite modulus grid is M in {2,4,8,16,32,64}; every odd a, every b, every even d and the recorded boundary/odd/large K values were checked. M = 1 and the excluded-a counterexample have separate direct certificates.

No external write is performed by this candidate. Any owner-cell proposal is additive, remains pending independent review and fresh preflight, and is separate from the already sealed 79-cell round.
