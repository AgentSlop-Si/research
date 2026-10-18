# Independent final review: nonconstant sparse-original BUCKETS

Date: 2026-10-17 UTC

## Verdict

ACCEPT_RESTRICTED_NONCONSTANT_THEOREM_SCALE_INTEGRATION.

No blocking finding was identified in the frozen 15-file packet. Acceptance covers the live, pinned sparse-original supplier followed by the new certified evaluator of the original ideal BUCKETS operator at N=M=2^28, B=131072, and rho=2^-464, for canonical nonzero inputs with at most 16 arbitrary support indices and at most 1024 bits per Gaussian-integer component. It covers legal odd sigma and arbitrary residue tau, exact modal normalization, all explicitly returned outputs, finite first-run precision sufficiency, and the stated conservative logical resource model.

It does not establish arbitrary dense inputs, non-singleton ALG-034 blocks, complete sparse recovery, outer transfer or t<M, probability/amplification, bit equivalence with the historical rounded serial or FFT implementation, historical execution attestation, or external-origin authentication.

## Inspection and reproducibility

Before executing candidate code, this reviewer read the complete numerical engine, live adapter, vendored supplier, both author control scripts, proof, contract, and manifest. No predecessor executable or author test/oracle was imported. All 15 file sizes and SHA-256 values matched the frozen manifest before execution and remained unchanged afterward.

The production pins reviewed are:

- nonconstant_buckets.py: 9b6accac4781c07a7e06acfa4239762b0cf21503bf619d7138971ce0c00d9993
- sparse_adapter.py: cdbe745859a7f729c26e43f1476bacb5d8ee0f0ee656ab5bf2674e102332efa7
- vendor/sparse_supplier.py: 5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed

The independent script and its complete result/receipt are retained beside this report. All writes were local review artifacts. No external writes occurred.

## Original operator correspondence

This review did not rely solely on the candidate's self-description. It read the accepted operator antecedents in alg034_scale_adapter_20261017_2045/PROOF.md, its retained vendor/buckets.py, and alg034_completion_20261017_1542/vendor/compact_window.py, together with the previous restricted acceptance verdict.

Those sources define the centered 2r-fold length-ell box convolution c_t, the nonnegative periodic transform Phi, C=sum_{a=-g}^g Phi(a), D_H(t)=sum_{a=-H}^H exp(2 pi i a t/M), and w_t=M c_t D_H(t)/C. Their ideal bucket folds w_t v_(sigma t+tau) modulo B, applies the negative-sign B-point DFT, and scales by 1/sqrt(M).

For the exact source v_j=M^(-1/2) sum_n (c_n/2^h) exp(-2 pi i n j/M), finite substitution cancels the two square-root factors against the window's M and yields exactly

bucket_j = sum_n (c_n/2^h) exp(-2 pi i n tau/M) [sum_{a=-H}^H Phi(jT+sigma n-a)]/C.

Thus the plus sign in jT+sigma n, the negative tau phase, the signed tap support, normalization, and original window all agree. This is a different evaluation of the same ideal operator; there is no assertion that a historical rounded tap-fold/FFT was executed. The second negative unitary transform is R(x)/alpha.

The candidate's exact parameter formulas give beta=5/56, beta*m=5/2, k=32, B=4096k, T=2048, ell=1048576, r=57, g=512, H=1536, W=119537551<M and P=464. The separate window-delta inequality 3073*M^4<=16^57 was checked exactly.

## Retained set, circular shifts, and omitted tail

For a mode n, the condition dist_M(jT+sigma n,0)<2T admits at most four bins. The five integer candidates centered at floor(-(sigma n mod M)/T) include all such bins, including wraparound and exact-boundary cases. The review exhaustively scanned every one of the 131072 bins separately for every mode in three independent test cases and compared the resulting sets with this selection rule and the complete active set.

Every retained numerator argument has folded distance at most 2T+H-1=5631. The two prefix-sum formulas in the implementation correctly include Phi(0) exactly once, including d=H. Prefix subtraction is outward and assumes no false independence or error cancellation.

For any omitted mode/bin pair, the circular triangle inequality gives distance at least 2T-H=2560 for every numerator term. The elementary sine lower bound then gives Phi<=20^-114 and K<=eta=3073/20^114. The strict inequality eta<2^-480 was checked with integers.

For arbitrary complex coefficients, lambda=sum_n (|Re c_n|+|Im c_n|)/2^h is a valid upper bound on the sum of modal magnitudes. Cauchy-Schwarz gives lambda<=sqrt(2s)<=sqrt(32)<6. The implementation uses the actual integer component mass and ceil(eta*lambda*2^560), rather than an empirical tail or a positivity assumption about coefficients. This bounds all omitted modes simultaneously at each bin. Zero outputs outside the retained union therefore have a valid complex absolute-error certificate.

## Interval correctness and uniform precision

The production Machin enclosure, exact argument reductions, midpoint/Lipschitz sine enclosure, 128-term sine polynomial and degree-256 Taylor remainder were checked at source level. In particular 2^257/257! is a valid remainder on |x|<=2, and outward integer arithmetic plus the shared factorial test makes the bound finite and checkable. The even power is evaluated by rounded nonnegative interval products, whose operands remain in [0,1]. The phase implements cos(2 pi n tau/M)-i sin(2 pi n tau/M). General complex multiplication and division by 2^h have the correct signs and outward directions.

The proof's family-wide precision bounds are sufficient, not merely observations on the small fixture:

1. Machin width <2^14 grid units; reduced-angle and Taylor propagation keep every sine width <2^14.
2. Every nonzero denominator has true size at least 2^-7, lower endpoint at least 2^-8, and width at most 2^34 grid units. The ratio-width bound <2^52 follows conservatively.
3. Nonnegative power 114 has width <2^59. The prefix, C, numerator and quotient bounds imply every retained K interval has width <2^82.
4. With s<=16 and lambda<6, the total normalized coefficient widths and magnitudes give each final retained component width <2^87.
5. For U=2^96, component rounding errors are at most U/2+2^86. The exact inequality 2(U/2+2^86)^2<(3U/4)^2 holds, while the entire tail allowance is <U/4.

Consequently the exact Euclidean check er^2+ei^2<=(U-tail)^2 must pass on a fresh sufficient-budget engine throughout the stated bounded family. It certifies complex modulus error <=2^-464, not merely separate Cartesian errors at that radius. The runtime check still independently enforces the actual radius for every retained bin.

## Independent oracle and actual full outputs

The reviewer wrote a new 832-bit interval oracle using positive integer-square-root half angles, complex dyadic-root products, exact endpoint power 114, and direct 3073-term window sums. It uses no Machin formula, Taylor evaluator, prefix logic, rounded binary power, production numerical primitive, or author oracle. Its enclosure contains the exact dyadic-angle root by the elementary half-angle identities and outward integer-square-root brackets.

Fresh live execution reproduced the entire frozen delta_1+delta_3 fixture packet byte-for-byte under canonical serialization, including every one of its 131072 output pairs. Three full-output runs received independent numerical checks:

- Fixture: support 2, h=1, sigma=1, tau=17, 4 active bins, norm squared 1/2.
- Arbitrary maximum-width case: support 16 spread across [0,M), 1024-bit complex components, h=1027, sigma=M-3, tau=M-17, 64 active bins.
- Circular boundary case: support at 0, T, 2T and M-1, complex coefficients, h=3, sigma=1, tau=M-1, 6 active bins.

For all 74 retained certificates, the independent oracle intervals lie inside the production enclosures and independently satisfy the Euclidean radius budget including the global omitted tail. All 393216 output pairs across these three runs were checked for explicit integer representation; every far-only pair was checked to be zero. The largest observed retained component interval width was 496082309332 units of 2^-560, far below the universal 2^87 bound.

Additional independent root controls cover signs, full-period reduction, axes and near-axis phases. A fresh 180-decimal-digit reduced signed-time convolution diagnostic checks all 8 bins at two nontrivial schedules with four complex non-quarter modes; it is labeled as a reduced numerical diagnostic, not theorem-scale proof by numerical coincidence.

The run passed 786952 assertions. Counts include individual output/type/zero checks and should not be mistaken for that many mathematically independent experiments.

## Live binding and the query distinction

The adapter obtains entries and h only by executing the pinned supplier on separately supplied canonical original raw/state. It does not accept a caller-provided modal descriptor, root table, success flag, or digest in place of that execution. The immutable header retains original context. Semantic verification recomputes from the separately supplied original and compares the complete canonical packet.

Fresh controls rejected a changed far output coordinate, changed original support, changed tau, and changed valid ALG state. The original-state binding remains meaningful even though B_A=N makes its mathematical transform effect the identity. Strict JSON controls rejected duplicate keys, floating numbers and nonfinite values.

The exact modal representation and finite point-query interface must remain separate. A query_bits=8 supplier still gives the exact descriptor, so its BUCKETS output is unchanged; a request to label its finite query accepted-radius compliant correctly fails. The adapter's formal policy-radius exponent check is not presented as a certificate for a separately coarse finite query. Accepted finite queries retain their separate producer proof and paid receipts.

The separately coordinated supplier reviewer reported no descriptor, normalization, phase, formal-radius or admitted-domain blocker after 503 independent controls, including N=4/8 exact algebra, arbitrary supports and large endpoints. This report does not replace that separate supplier review.

## Resource audit

The fixed-size preparation and source-dependent formulas support the stated first-run envelopes. A nontrivial scalar sine uses 127 recurrences; counting its integer operations plus quotient, binary power and prefix updates stays below the loose 2048-per-expensive-preparation bound. Machin/factorial/guards fit below 20000 extra operations. Each mode's two phase roots, at most four windows, products and certificates fit below the loose 8192-per-mode bound. Therefore (5631+129)*2048+20000+16*8192<2^24<30000000.

The largest numerical integers are the fixed 239-power Machin terms, below 9000 bits. The 1024-bit coefficient cap, energy calculation, h<=1027 at this support cap, interval products and exponent cancellations do not approach the declared 20000-bit limit. Preparation uses fewer than 2^19 logical slots and a full call fewer than 2^20 additional slots, including every B output. These source-level bounds establish fresh-run sufficiency; cumulative repeated calls can legitimately exhaust a finite cap.

The independent nine-call workload actually recorded:

- 1179648 output writes, exactly 9*131072
- 8226659 numeric operations
- 8994 maximum recorded integer bits
- 6195643 logical slots
- 5631 prepared Phi terms and 129 numerator roots, prepared once
- zero actual FFT roots and zero FFT butterflies

This workload also includes supplemental phase checks. It stayed below all cumulative numerical caps. Supplier receipts, loading, bounded parsing/canonical copying/export/compare and control work are added under intentionally loose fixed envelopes. External packet exports require the documented extra charge; the receipt API does not claim to detect arbitrary unreported exports automatically. The accounting is a bounded schoolbook-work/cumulative-logical-storage claim, not Python peak RAM or elapsed-time complexity. The trusted correct runtime, pinned unmodified source/private state, and independently retained original context assumptions remain essential.

## Completion boundary

The formerly constant delta_0 integration has genuinely been extended to arbitrary non-quarter sparse original modes within the declared bounded family, with the same ideal BUCKETS target, genuine theorem parameters, complex phases, live original binding, finite proof and actual paid complete output. The broader recovery/outer-transfer and dense/general-block gaps remain open and are explicitly excluded in the packet and this acceptance.
