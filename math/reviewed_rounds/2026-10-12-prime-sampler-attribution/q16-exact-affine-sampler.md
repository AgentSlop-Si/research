Public derivative of a source-bound reviewed research report. Private tracking and delivery details are omitted; mathematical claims, evidence, source attribution and remaining limits are retained. Original source-report SHA-256: 629b3eba306db4936146d1179fd21e0cf2c2bed6c51aaf2fc1dfc418b6437c71.

Review date: 12 October 2026 UTC.

Cumulative-scope clarification, 12 October 2026: bounded deterministic ranking/location and companion estimation are already independently accepted (ranking review archive SHA-256 10797360653f5cd171ee8c61fa236f3b961018d361132dd9e23bdd0b6a6eabfc; estimation review archive SHA-256 60f9168baa667446dc00be46e809b4b8c6c270613a124029b59293f387348718). The remaining selection/estimation slack obligation below means composing those accepted bounds with probabilistic recovery events; it does not reopen their bounded deterministic correctness. The original report remains unchanged.

# Independent review: exact dyadic affine sampler

Verdict: ACCEPT_BOUNDED. No change to the candidate implementation is needed.
Review date: 2026-10-12 UTC. The accepted object is the exact candidate ZIP
SHA-256 dbb72125d85c7e7d150da8a6b17eb82d807a14e3bfa8b9bb935e5f24936fe315,
739,830 bytes. The sampler itself has SHA-256
e18e5705910dda08441f8b49297058eed7df174712b29739ed6ba7e02ccdfd6b.

This accepts a classical random-bit-to-parameter component conditional on a
mathematical source contract. It does not accept a concrete source of entropy,
a general-modulus sampler, randomized recovery, an outer loop, S6, or closure
of Q16. It is not a novelty or priority result.

## 1. Independent mathematical audit

For m >= 1, let K = 2m-1 and n = 2^m. The first m-1 fair independent bits
encode U in [0,n/2), and the next m encode T in [0,n). The output is
(2U+1,T). Every odd canonical multiplier and every canonical translation have
exactly one binary preimage: encode floor(sigma/2) and tau at the prescribed
widths. Hence the probability of each pair is 2^-K; sigma and tau have product
uniform law. This proof includes m=1, whose multiplier block is empty.

Successive calls consume fixed disjoint blocks. Under a mutually independent
fair-bit stream, their inverse-image events factor, giving probability
2^(-sum K_j) for any prescribed sequence of outputs at fixed exponents m_j.
The mathematical source must be fresh across calls and independent of fixed
signal/tap data for downstream claims. Reusing a seed, replaying a buffer,
pairwise-only independence, or matching individual marginals is insufficient.
No implementation test can establish this physical-source assumption.

The cardinality 2^K gives the claimed lower bound. A deterministic algorithm
with at most b independent fair bits has at most 2^b depth-b transcripts after
padding earlier leaves. Full support on 2^K outputs requires b >= K. This is
the fixed/worst-case bit optimum claimed, not a new theorem about arbitrary
real generators or algorithms given free random initial state.

Actual accepted Windows satisfy B >= 4, q >= 10, and 16Bq+1 < 2^m, so m >= 10.
The helper's smaller domain is a transparent extension used for finite tests;
it is not a claim that these small exponents are accepted window instances.
Odd residues are exactly the units of the dyadic ring. No gcd, rejection,
factorization, or random-word modular reduction is required.

## 2. Source convention and frequency-phase audit

The primary paper was independently read on 2026-10-12 through its public
PDF text: [Hassanieh, Indyk, Katabi and Price, Simple and Practical Algorithm
for Sparse Fourier Transform](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf).
Section 2 gives the dyadic domain; Section 3(b), Claim 3.5 gives the time
permutation; Section 4.1, step 1 gives the odd multiplier/translation draw.
No whole-PDF byte hash or visual-PDF verification is claimed here. The source
paper uses the opposite Fourier sign from the accepted local convention;
the accepted code/proof, not an unadjusted phase copied from the paper, governs.

Independently deriving the accepted negative-sign convention gives

    y_t = x_(sigma*t+tau)
    F_y(sigma*i) = exp(+2*pi*i*tau*i/n) F_x(i).

After windowing, the retained identity is

    Z_j = sum_i F_i exp(+2*pi*i*tau*i/n) H_(j*n/B-sigma*i).

Thus tau contributes phases and changes time-sample addresses. It does not
translate frequency locations or the hash h_sigma(i). In particular frequency
zero remains at zero for every sigma and tau; one cannot infer a uniform
frequency location from the uniform time-affine pair. Multiplication also
preserves the 2-adic valuation of nonzero frequency differences. The candidate
makes none of those erroneous stronger claims. Beta is not an API parameter
or sampled exponent. The sampler's sigma and tau pass unchanged to locate.

Fresh exact exponent checks verify the phase identity without floating point.
Fresh nonzero integrations use x_j = i^j, sigma=n-1, and tau=0,1,2,3 across
every pinned fixture. Outputs rotate by i^tau, candidate fibers remain the
same, sample addresses match (sigma*t+tau) modulo n in their exact order, and
the central bucket agrees with its exact rational target within the accepted
reported arithmetic error. This materially extends the author's zero-signal
API checks. It does not reprove accepted tap response or arbitrary recovery.

## 3. Implementation, failures, and termination

The source is 3,106 bytes, has no imports or global mutable sampling state,
and contains no RNG, seed, hidden reseed, cache, prefetch, retry, or fallback.
Each successful call makes exactly K supplied-callback calls, with separate
contiguous multiplier and translation blocks. Strict built-in integer checks
reject booleans and integer subclasses. Arguments and insufficient caps are
rejected before any callback. Output is assembled only after all bits pass.

A source exception at attempted call j propagates with the original exception
identity, including BaseException subclasses. An invalid return raises
Rejected. Neither produces a pair. Prefix consumption is retained, and a
later caller-initiated attempt starts at the current callback position.
MeteredBits records j attempted calls and j-1 valid returns with the correct
exception/invalid classification. Its in-process state is trusted; it is not
a hostile-code audit or cryptographic erasure facility.

Arbitrary source failure does not preserve conditional uniformity. A fresh
negative control fails at the last bit when the first and last bits differ.
For m=3, the 16 successes have uniform individual sigma and tau marginals but
only half of the 32 possible pairs. Thus even success-conditioned marginal
checks cannot justify the joint law. The candidate explicitly excludes such
an inference and does not automatically retry these failures.

For sufficient cap, a terminating ideal source and adequate physical
resources, all tapes succeed after exactly K calls. The expectation and
worst-case call count are K and the tail above K is zero. A low cap is a
zero-read deterministic refusal, not random failure. The implementation has
no timeout: a hanging source can hang it. No claimed bound on source latency,
physical availability, process failure, or resource exhaustion follows from
the ideal bit law.

## 4. Complete cost audit

The repeated immutable integer shifts accumulate at most O(m^2) elementary
bit work. The decoded-control preflight costs O(lambda_m+lambda_cap), and
the output/working integers occupy O(m+lambda_m+lambda_cap) bits apart from
the provider. Loop overhead O(m log m) in a conservative bit model fits the
stated O(m^2) upper bound. The supplied packed-word upper bound

    O(ceil(lambda_m/W)+ceil(lambda_cap/W)+m*ceil(m/W))

is valid for W >= 1 with the K scalar source accesses and their own word costs
also charged. It is not a constant-time sampler merely because m fits a word.
Serialized input/output parsing, object/format handling, source acquisition,
decoding, buffering, actual source latency, and hidden entropy consumption
remain paid separately. The return field random_bits counts valid callback
bits, not all possible entropy used inside an external provider.

The meter's four cumulative counters require their own width. With largest
pre-call count C and h=bit_length(C+K+1), O(Kh) extra bit work,
O(K ceil(h/W)) extra word work, and O(h) retained bits are conservative. The
packet charges snapshots/serialization. A synthetic 4,097-bit counter test
confirms that the Python reference does not silently wrap a fixed word.
Failed calls pay control work, the whole attempted prefix, provider work
through the failing attempt, and optional meter work. The O(jm) prefix bound
is conservative and sufficient. No n-entry table or free source preparation
has been concealed in the sampler's own charges.

## 5. Independent verification and replay

The reviewer-owned independent_checks.py does not import author checker
functions. Its exact results are stored in INDEPENDENT_RESULTS.json:

- 699,050 inverse-image cases, all outcomes for m=1 through 10
- 4,112 joint tapes, including mixed exponent sequences
- 536 raw/metered original-exception cases across every tested read position
- 2,010 raw/metered invalid-return cases, including malicious equality objects
- 37 zero-read preflight cases and 120 width/cap/no-prefetch boundary cases
- 18,724 exact negative-DFT phase identities
- 28 nonzero phase integrations across all seven fixtures
- consumed-prefix/no-rewind, large-counter, correlation, and failure controls

All 27 original working-directory files matched the input archive exactly.
The candidate's 26-file manifest and the accepted review/candidate nesting
were checked independently. All 10 copied accepted files, including seven
fixtures, match their accepted dependency bytes. The author checker and
integrity checker were also rerun, and the former is byte-identical to the
author's stored FRESH_RESULTS.json. Those are additional replay evidence,
separate from the fresh reviewer checks and independent proof audit.

The sealed review includes CANDIDATE.zip, the reviewer tests, results and
replay_review.py. The final cold procedure verifies the review manifest,
extracts the candidate safely in a new temporary directory, runs both fresh
reviewer and author checks, and compares exact output bytes. Its separately
sealed cold record binds the final review ZIP hash and result hashes.

## 6. Remaining obligations

The accepted component is an independently reviewed dyadic parameter primitive with
exact 2m-1 fresh IID-bit input, product-uniform parameters, independent fresh
trials, explicit failure/cap behavior and complete source/bit/word charges.
The source assumption is essential. Preserve Qmin=56, trusted
tap/in-process-cache limitations, original ideal-arithmetic theorem and
weak-coordinate versus all-input relative-l2 distinction.

Still open: accepted-window isolation/interference and crowding probabilities;
finite-word selection/estimation slack; repetitions, aggregation, pruning,
medians, and every abort; concrete source assumptions/certification; unitary
and full-output integration; the full engine and S6. The complete sparse engine remains open; no historical-priority or novelty determination follows.
