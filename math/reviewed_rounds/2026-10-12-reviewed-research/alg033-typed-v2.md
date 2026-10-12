Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 0e54112f277c9638d23873207520db3fea6927e89a4a76c0ec630cf0eb0168e6

---

# Independent review: ALG033 bounded typed certificate API, version 2

Review date: 11 October 2026 UTC.

## Verdict and immutable identities

**ACCEPT_BOUNDED_TYPED_EXACT_REFERENCE_API_ONLY.** Version 2 fixes the previously blocking typed-revalidation defect and passes independent replay, structural/adversarial checks, and finite mathematical verification. This accepts only the specified bounded reference API. The generic ALG-033::immutable-certificate gate remains OPEN. The original uploaded v13 executed certificate remains REFUTED. No randomized approximation-accuracy advantage or practical speed improvement is established.

- Accepted candidate archive: ALG033_Bounded_Immutable_Certificate_v2_Candidate_2026-10-11.zip; SHA256 `60939f57c3657639390b1f62ee5400e451e7467b6cbfc01f03380439ae56aa26`; 132,912 bytes.
- Candidate source: immutable_certificate.py; SHA256 `7b536a6c967adb6e5d6594c1c8c4d8b517e12afd98201f4af4c2839bc729a0c5`.
- Candidate manifest: SHA256 `e7cf0155ae2a843f9fef53d4df2b19c0bd50cee2c44c1f8f3e24f80fb363b88b`; all 24 bound files independently verified.
- Superseded v1 candidate remains on HOLD and unchanged: SHA256 `bb93825f324f16fc0b0286f6e79200ec586f65bbd2ea23f45347915dd4a6340c`.
- Original independent v1 HOLD review remains unchanged: SHA256 `f1770af0d7f51941e92c9dfda4135555adce5802e9af039a97b45dbba26fd790`.
- Original uploaded v13 archive remains inert and refuted: SHA256 `465d0cf5573539887fdb93376e7dc6fba740512a92ac8121952dafc3492b51fd`.

The reviewer made no Sheet, Library or GitHub writes. No original uploaded program was imported, compiled or executed. Only the newly authored bounded candidate and inspected/newly authored controls ran.

## Precisely accepted implementation scope

Inputs are length 2, 3 or 4 rational-complex vectors with 128-bit numerator/denominator ceilings. Positive odd row counts are at most 101; rejection caps are 1 through 32. Epsilon and delta are exact bounded rationals with epsilon>0 and 0<delta<1. Output is an exact symbolic numerator divided by sqrt(N), with numerator in Q(sqrt(3),i), under the negative-exponent unitary Fourier convention.

1. `identity_offset`, N in {2,3,4}, M=1: a dense exact DFT reference followed by actual coordinate medians. It needs no entropy. The admitted output is exact, and all five saved N=2/N=3 grid witnesses now have zero error through this new API.
2. `direct_n4`, N=4,M=2: exact projected rows, actual coordinate medians, exact rational probability arithmetic, finite capped unit/shift sampling, explicit abort-without-output, and kernel-budget checks under the stated ideal independent-fair-bit interface. Its whole admitted accuracy range already follows from a deterministic bound, detailed below.

The new code is a separate reference implementation, not a repair or execution of the original optimized NumPy/scan/Bessel program. Bessel and floating backends are refused. Zero Bessel/addition/numerical-error fields mean those terms are absent from these exact routes; they do not certify a Bessel approximation or finite-precision FFT. H and rank are fixed zero. There is no grid-g parameter because the admitted aggregator is an actual coordinate median; no grid quantizer is invoked or reselected at execution.

The plan binds the original-source provenance and fresh implementation hash, exact input/hash, N/Q/M/K/prime/rank/H, row count, energy-scaled epsilon and delta, normalization, aggregator, variance/error terms, sampler/cap/abort law, exact binomial tail and failure bound, resource ceilings and seal. There are no execution-time overrides of those choices.

## Typed revalidation repair

The v1 validator used dataclass value equality. In ordinary Python, 4.0, Fraction(4) and 4 compare equal. A v1 plan with n=4.0 therefore consumed 12 bits before TypeError, and a numerically equal floating failure_bound could be returned as a purported exact certificate.

Version 2 first calls `validate_plan_types`:

- Only the exact Plan class is accepted, with every field present.
- Strings and integer fields must have their exact declared types, excluding subclasses and booleans in integer fields.
- Every probability/error/tolerance field is an exact Fraction with actual integer numerator/denominator, positive denominator and gcd 1.
- Input x is a tuple of canonical pair tuples whose leaves are canonical Fractions; mutable containers, subclasses and numeric-equal scalar substitutes are rejected.

Only then does `verify_plan` reconstruct the certificate from the admitted request and compare every exact typed field and seal. `execute` and `plan_json` invoke this gate. The canonical schema makes the later value comparison sufficient; loose equality is no longer used as a substitute for field identity.

All 19 saved v1 typed substitutions now raise Refusal before bits. The independent reviewer additionally tested 212 malformed plans spanning all 35 fields, missing slots, a Plan subclass, scalar/container subclasses, wrong scalar types, and corrupt Fraction internals. All 636 verify/execute/serialize calls raised Refusal with zero certificate reconstruction and zero bit calls. All 35 genuinely changed-value field controls also refuse before bits. Legal canonical plans still execute and serialize correctly.

This is an ordinary-runtime integrity boundary, not cryptographic authenticity or protection against a hostile Python runtime. Intentionally making a different valid new plan remains permitted. The implementation file hash is the source bytes observed at import; neither a sealed dataclass nor a SHA is a signature.

## Exact probability statement and conditioning

For each fixed admitted input x and its plan chosen before fresh ideal independent fair bits, the accepted statement is

P[sampler abort OR a successful vector has some k with |z[k]−(U_N x)[k]| > epsilon * ||x||_2] <= plan.failure_bound <= delta.

The error is additive and input-energy-scaled. It is not absolute epsilon error or per-bin relative error. Version 2 REPORT.md now states this explicitly and inserts ||x||_2 in the row disk/median/bias error steps. Identity execution is exact without a random-source premise, and zero input returns exact zero without drawing bits.

The finite N=4 operator has exact mean U_4. Independently derived Gram covariances Q_k are positive semidefinite and satisfy Q_k^2=Q_k/2, yielding E|Y_k−(U_4 x)_k|^2 <= (1/2)||x||_2^2 for every complex x. With p=min(1,1/epsilon^2), the exact odd-row majority tail T bounds the per-output median failure via complex-disk Markov and a strict majority. A union over four output coordinates requires no independence between those coordinates.

Each capped unit draw aborts with probability 2^(-A); conditional on success its a and beta are uniform. Under the independent bit source, conditioning on all rows succeeding preserves the product uniform row-state law. The final unconditional bound `min(1,R*2^(-A)+4*T)` correctly includes abort. No physical entropy source, public fixed seed, arbitrary PRNG or external callable is thereby certified. A replay tape only demonstrates execution.

Missing source, exhausted iterator/EOF, and malformed returned bits have the stated Refusal behavior. Acceptance does not assert conversion of every out-of-contract callback error into Refusal: for example a non-callable `read_bit=3` raises ordinary TypeError, and an arbitrary callback can raise its own exception. Those cases return no Fourier vector or certificate and are outside the declared callable ideal-bit interface. The finite sampler model and successful executions are unaffected.

## No randomized accuracy advantage anywhere in the admitted range

This limitation is part of acceptance and must remain in table summaries.

For each output and state, the normalized error functional U_4(P−I) has four coefficients of modulus 1/2, hence squared norm 1. Thus each row's complex error is at most ||x||_2 for every input and every state. Real and imaginary medians each remain within ||x||_2 of their scalar targets, so every successful state sequence has complex error at most sqrt(2)||x||_2, even for chosen or correlated states.

If epsilon<=sqrt(2), then p>=1/2. For every odd R, the majority binomial tail at p=1/2 is 1/2, and monotonicity gives T>=1/2. The N=4 bound is therefore clipped to 1 and cannot meet delta<1. Every admitted direct_n4 epsilon is strictly above sqrt(2), so its accuracy target is already attained deterministically on every successful path.

The probability machinery is correct, but randomness is needed here only to support the declared sampler-abort law. This is a bounded certificate-mechanics/reference-execution result, not evidence of a nontrivial randomized approximation-accuracy or speed advantage.

## Independent verification inventory

- All 24 candidate manifest entries verified after safe extraction. Original v1 candidate and HOLD hashes rechecked unchanged.
- Inspected v2 controls replayed in a fresh location. All three result JSON files were byte-identical to the frozen outputs: FRESH_CONTROLS, LEGAL_PLAN, LEGAL_RESULT.
- Author controls include the original-source internal 20-entry manifest, all five old grid witnesses, N=129 planned-M=4 versus executed-M=8 source mismatch, 15 exact DFT/root cases, 2,560 complete three-row executions, 141 malformed Plan tests, 35 changed-value refusals and sampler/underflow checks.
- Independent reviewer controls derive all four exact covariance matrices without using candidate phase/DFT functions; verify zero mean errors, Q^2=Q/2, and all 32 error-functional norm-one identities.
- 64 state/basis execution checks cover all real and imaginary basis directions.
- 306 independent dynamic-programming binomial distributions cover every odd R from 1 to 101 and include p=1/2 symmetry.
- 4,096 two-row A=2 reserved-bit tapes yield 1,792 abort tapes and exactly 36 successes for each of 64 ordered state pairs, verifying the conditioned product law.
- All 19 old numeric-equality bypasses now refuse; 212 additional malformed structures produce 636 zero-reconstruction/zero-bit refusals. All 35 changed-value refusals remain.
- Six boundary executions consume the maximum admitted fair-bit counts and stay within the conservative kernel work allowance, including R=101 and A=32 edges.

The bound is for explicitly charged reference-kernel operations and bit reads. Parsing, hashing, reconstruction, rational bit complexity, memory, output serialization and whole-program setup costs remain outside it. This is not an end-to-end resource theorem.

## Integration and retained obligations


Still open: the all-length adaptive dispatcher; source-bound optimized offset/Bessel execution; Bessel tail plus local-addition and finite-precision transfer; outward-rounded numerical certificates; physical random-source verification; full end-to-end work/bit accounting; general sharp composite covariance and historical-priority assessment. Q01 is separate. No discovery/canonical-ID count or novelty upgrade follows.

ROW_GUIDANCE.json supplies exact target URLs and proposed scoped language. SOURCE_PINS.json binds the decisive code, documents, predecessor and controls. Evidence includes both the v2 candidate and original independent v1 HOLD archive, unchanged.
