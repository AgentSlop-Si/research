# Independent final review: theorem-scale restricted ALG-034 → BUCKETS

Date: 2026-10-17 UTC
Verdict: ACCEPT_RESTRICTED_THEOREM_SCALE_INTEGRATION
Blocking findings: none within the stated restricted contract.

## Exact accepted statement

The frozen implementation actually executes the accepted, pinned exact structured producer on separately supplied original canonical sparse input x = 2^-F delta_0 at N = 2^28, with B_A = N and legal phase state. It exactly normalizes the resulting source to the positive constant 2^-14 and produces all 131,072 dyadic complex bucket values. Each differs by at most 2^-464 from the original ideal Q16 BUCKETS operator for this source, at beta = 5/56, k = 32, B = 131072, T = 2048, r = 57, g = 512, H = 1536, and P = 464.

This closes only the actual restricted producer-to-theorem-parameter BUCKETS integration gate. It is not acceptance of arbitrary ALG-034 inputs, general sparse recovery, outer transfer including its separate t<M guard, an exact general recovery threshold, random schedules/amplification, all-length dispatch, legacy rounded-serial/FFT equivalence, original-input Fourier recovery, novelty, or a universal FFT speedup. The local threshold 1/2 is a valid diagnostic only for this delta_0 instance.

## Frozen artifact and execution evidence

Candidate: ../candidate

- constant_buckets.py SHA-256: 951da991cf6cc795e2faf4cf14a7aae75639e0be79e4ce09af7363c0dd5b6359
- scale_adapter.py SHA-256: 24506f440d70f6008ff59c333a89b237457251ebd58313cfa49e79ba679667c7
- checks.py SHA-256: 2b5e4b864d5c18587c8fd0e491da7542bed2ce8a2b9d9d0c95ffb8f1035f6b54
- compact_window.py SHA-256: e29741e71c276c156d708f1d9dce6d60ff9d3d2c34a6045b03630c46506dac59
- structured_producer.py SHA-256: 9bbd77a44f8a265f170b1993b63cae71d8f5a8da9f108a85d68b2a7719fca717
- Candidate SAFE_MANIFEST.json SHA-256: 7eddc5b80a776cf9276a31bb61a0dc62cc4e25e07060c92636416d1c694168c1

The reviewer inspected executable source and original ideal-window/BUCKETS definitions before execution. All 21 manifest entries independently match size and hash. Source hashes were checked before and after the fresh independent run. The author supplied a frozen 348-assertion successful run; this review did not merely replay that test program.

The new reviewer-owned independent_review.py completed 393,270 assertions in 60.614 seconds. It constructed a fresh ScaleAdapter and genuinely ran its pinned producer and full numerical engine. The independently written higher-resolution oracle finished in 13.656 seconds; fresh actual numerical preparation finished at 46.328 seconds. These observed times are diagnostics, not complexity claims. A supplemental complete-period root control passed all 512 residues.

## Original ideal operator identity

For the centered 2r-fold convolution coefficients c_t of the normalized length-ell box, ell = 8B, the negative-sign Fourier transform is

Phi(a) = [sin(pi ell a/M)/(ell sin(pi a/M))]^(2r).

The integer-centered convolution removes the box phase. Phi is real, even, nonnegative, M-periodic and equals 1 at the limiting zero residue. The original ideal window is w_t = M c_t D_H(t)/C, where D_H(t) = sum_{a=-H}^H exp(2 pi i a t/M) and C = sum_{a=-g}^g Phi(a) >= 1.

The original BUCKETS path folds signed t modulo B, takes the negative-sign B-point DFT, and multiplies by 1/sqrt(M). The source itself is the positive constant 1/sqrt(M). Thus its two factors give exactly 1/M, and finite sum interchange gives

bucket_j = (1/M) sum_t w_t exp(-2 pi i j t/B)
         = sum_{a=-H}^H Phi(jT-a)/C.

This is the original ideal operator evaluated algebraically, not a different approximate window. W = 119537551 < 268435456 verifies the original signed-support nonalias guard. Legal odd sigma and legal tau cannot change a constant source, but both remain validated and bound in the packet. Side-bin equality follows from evenness, not an untested rounded-root identity.

The independent test also built a separate small exact box convolution and evaluated the original signed time-window sum using complex exponentials. It matched the frequency expression at every bucket to below 10^-90. This diagnostic is explicitly a reduced identity check; acceptance at the real theorem parameters rests on the exact finite-sum derivation and the actual full-scale interval execution.

## Certified numerics and global error

The candidate's 560-bit Machin pi enclosure, exact argument reduction, 128-term sine series, outward term arithmetic, midpoint angle radius and Lipschitz correction are sound. A degree-256 Taylor polynomial has the same sine polynomial as the degree-255 odd truncation, so the 2^257/257! remainder bound is valid. The exact shared scaled-tail inequality is checked. Positive denominator intervals, normalized Dirichlet bound, outward all-corner quotient and exact even power provide sound Phi intervals. All relevant denominator angles lie in (0,pi/2).

The independent oracle uses a different 704-bit grid, independently implemented 220-term arctangent intervals, 160 sine terms, and a full positive interval-angle recurrence rather than the candidate's midpoint-plus-radius construction. It imports none of the candidate's numerical helpers. It computes all Phi terms 1 through 3584 afresh and independently encloses C, the center numerator and the side numerator. Supplemental controls verify all 512 numerator sine residues, exact axes and a strict sign margin for every nonzero residue, validating the absolute-value branch.

All three candidate nonzero-bin enclosures strictly contain the narrower independent oracle enclosures. Each returned dyadic value independently passes the endpoint error bound at radius 2^-464. The actual imaginary coordinates are zero.

For every other bin, the circular distance d from jT-a to zero is at least 2T-H = 2560 and at most M/2 after reflection. The chord inequality gives sin(pi d/M) >= 2d/M. Therefore the normalized sine ratio is at most T/(16d) <= 1/20, and

0 <= bucket_j <= 3073/20^114 < 2^-464.

The independent program exhaustively checked all 131072 circular-distance classes and all actual returned coordinates, and checked the last strict comparison by integers. Consequently returning zero at every remaining bin is certified. No unexamined length-M tail sum is being assumed negligible.

The separate window error is 3073/16^57 <= M^-4, independently checked by exact integers. It is not substituted for the much smaller numerical rho. Actual producer and normalization errors are zero. The formal accepted-policy radius divided by alpha is also honestly checked: 2^-466 for the fixture, with q >= 464. The direct error bound is stronger than the accepted combined BUCKETS allowance.

For this instance alone, the ideal center is at least 1, while every other ideal bucket is at most 3073/4^114. Adding rho preserves separation at 1/2. This is not asserted to implement the missing general recovery rule.

## Producer premise, normalization and binding

The separately accepted producer review is ../../alg034_producer/review. Its exact ideal-target premise, pinned source and singleton-block specialization are relied upon, and the actual pinned execute is called here. The producer was not replaced by supplied payload, digest or attestation.

An exact period of four unit values uniquely identifies raw delta_0 within the producer's quarter-axis family by invertibility of the four-point transform. The adapter rejects all other produced periods and all other N. For input 2^-F delta_0, producer output is 2^(-F-14), alpha is 2^-F, and normalized squared norm is exactly M*2^-28 = 1. Signed F, including near-128-bit magnitudes, is handled by exact exponent arithmetic without expanding enormous powers. The second negative-sign transform targets R(Px)/alpha = delta_0.

Independent controls changed returned source sign, target, recovery flag, final imaginary bucket, middle-vector length, producer phase, formal radius and raw-input digest. Every mutated packet rejected. Separate-original replay controls changed F, legal phase, t, q, p, legal sigma and legal tau; each rejected despite numerical invariances in several cases. Wrong-support, nonconstant, negative, imaginary and zero originals reject. Large positive/negative F and legal extreme schedules execute successfully and retain exactly the same immutable numeric output.

The original grammar, complete producer context, source metadata, downstream metadata and every output coordinate are compared by typed canonical serialization after actual producer re-execution. Independent controls exercised duplicate keys, exponent-form/nonfinite numbers, excessive nesting and arbitrary-object hooks. Frozen outputs do not retain caller-owned mutable input lists. This establishes semantic binding to separately retained originals; it does not authenticate an unknown origin or attest historical execution. No hostile reflection, monkeypatching or concurrent input mutation is promised.

## Work, storage and deployment accounting

This is a bounded, fixed-parameter deployment, not an uncapped asymptotic theorem. The observed reviewer run's candidate ledger records:

- 6,442,092 numerical operations after review calls
- 63,840 maximum recorded integer bits
- 684,386 cumulative logical allocation slots
- 3,584 Phi evaluations
- 129 numerator sine roots and 3,699 sine evaluations in total
- 1,136 arctangent terms and 256 shared factorial steps
- all 131,072 bucket outputs
- zero actual FFT roots and butterflies

The declared caps are 30,000,000 numerical operations, 70,000 recorded integer bits and 4,000,000 cumulative allocation slots. These checks are meaningful for the successful path. A binary-operation rejection can first materialize an at-most-double-width intermediate; this is accurately disclosed and is not a strict Python peak-memory limit. Arbitrarily oversized caller objects and host exhaustion do not receive successful certificates.

No N-vector, W-tap vector, full Phi vector or literal p-grid array is allocated. A period-four source, 129 numerator root intervals, three streaming sum intervals and the full B-output vector suffice by the proved identity. Reuse of the prepared trusted engine is paid once; every original-input execution and schedule validation remains paid. There is no claim that the displaced legacy coefficient construction, tap scan or FFT actually ran.

Arithmetic, control/index operations and cumulative logical storage are charged by the pinned schoolbook model. Candidate source reads, hashing and serialization have explicit oversized charges. Bounded canonicalization, parser allocation, copies, complete output comparison and rejected bounded attempts are covered by the documented fixed envelopes. Source/private-state trust and standard-library correctness are stated assumptions. The finite tree/byte/type/depth caps make these loose envelopes credible; they are not estimates of CPU cycles or RSS. Exports after a receipt are separate and require their stated extra charge. Reviewer-generated oracles, deep-copy mutations and diagnostics are test work, not hidden production work claimed inside that receipt.

The sample integrated receipt in INDEPENDENT_RESULTS.json is reproducible evidence of accounting, not a practical performance promise or evidence of totality under arbitrary resource exhaustion.

## Final boundary

Accepted: an actually executed, original-context-bound, restricted exact producer → exact normalized source → original ideal BUCKETS backend at genuine theorem parameters, with complete output, certified rho error and explicit bounded resource accounting.

Still open: full recovery, separate outer transfer, arbitrary inputs, general thresholds/probabilities, legacy rounded equivalence and broader end-to-end claims. No external write or publication occurred during this review.
