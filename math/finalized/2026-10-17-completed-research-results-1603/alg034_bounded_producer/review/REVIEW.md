# Independent review of the bounded ALG-034 producer binding

17 October 2026. ACCEPT the scoped bounded executable producer binding. Frozen source manifest SHA-256: `671e3aeed371400ee62606fef30fad412bc988cc96bc494cbe0dcb83983c0046`.

## Scope and disposition

The new executable composition closes the previously missing bounded original exact input → accepted zero/precision policy → specified serial fixed-point producer → actual immutable payload → pinned conditional source adapter gate. The accepted precision and all-length policy theorems are antecedents, not new results of this review. The disposition is acceptance of this bounded composition, with the wider ALG-034 owner remaining open.

This review inspected all of `producer.py`, `policy.py`, the three vendored dependencies, the new proof, and the candidate control program before permitted local numerical execution. It also read the accepted serial theorem report (SHA-256 `8dcc83d64316a136cb482fd04cff81ebaf7bf2351ab61fec1f02d8eadaf81cf8`) as text and matched the implementation stage by stage. No archived producer or archived control program was executed. The pinned legacy adapter and BUCKETS component were deliberately executed, so a claim that no historical numerical code ran would be false. No network or external writes were performed.

## Binding and numerical correspondence

The public entrypoint validates exact built-in input, copies the original arrays, derives the balanced longer-first state and parity, recomputes actual W and the exact cyclotomic policy, and selects or validates actual p. The implementation's compression, endpoint multiplication, factor-by-factor coefficients, direct B seeds, serial recurrence, inverse-square-root multiplication, gauge-cycle ordering, exact prefixes, one half-sum rounding and final product match the accepted serial specification. Symbolic kappa=W-F-p avoids a physical shift by a huge common exponent.

The new root routine is an allowed implementation of the theorem's intended-embedding premise: outward Machin arctangent intervals, an outward intended-angle interval, finite Taylor inclusion, and an exact squared complex endpoint-radius admission test establish error at most 2^-p. Axis values are exact. The independent finite integer-square-root construction establishes the normalization scalar's absolute-error premise. A failed root admission is a failed run; there is no assertion that every permitted parameter combination must succeed.

The actual tuple returned by the serial arithmetic is passed directly to the pinned adapter. Actual input/state/p/F/W/C fields and the digest of those same rows are constructed inside that call. The adapter's legacy conditional label does not become an independent proof object: this wrapper supplies its previously missing trusted antecedent. Existing actual-width, dyadic-length and metadata checks remain in force. Generic q can legitimately yield TARGET_BUDGET_NOT_ESTABLISHED; the code does not label that a Q16 budget pass.

Run contains immutable bytes/tuples and a deeply immutable adapted source. Mutating the caller's input or a decoded export cannot change the completed result. The trusted model requires the reviewed interpreter, standard library and program, and excludes concurrent mutation during input validation or hostile in-process code replacement. Neither self-contained records nor source hashes authenticate an unknown external original data source or historical execution.

## Semantic replay and adversarial controls

`verify` derives a fresh deterministic producer result from separately supplied retained original context, bounds the untrusted packet, and compares full typed canonical content. It does not trust packet flags or hashes. Any changed row, grid exponent, original context or policy is rejected, even if attacker-editable commitments are recomputed. This is present semantic numerical verification, not execution-history attestation or external-origin authentication.

The fresh reviewer controls constructed a one-unit forged output, genuinely regenerated every legacy consistency-record digest, and regenerated the adapter output digest. Both the legacy consistency checker and the legacy conditional adapter accepted that forged statement, illustrating their intended weaker interfaces. The new semantic replay rejected it against the retained original input. Separate controls cover row sign/order changes, bool substitution, null payload, altered context fields, altered policy hash, original-argument substitution, unsupported self-certification flags, oversized packet serialization, immutable outputs, and both zero branches.

## Precision and resource accounting

No new precision theorem is credited. On successful nonzero runs the actual p, intended-root error, scalar error, exact-grid rounding, accepted integer-magnitude budget and exact product-accumulator bounds instantiate the existing theorem. Original zero and projected zero terminate distinctly before normalization; approximate zero on an accepted nonzero run is an invariant failure.

The implementation's N<=64, raw width<=1024, selected p<=4096, four-million metered-operation and 100000-bit working-integer caps are deployment limits. They are not strengthened universal complexity claims or a guarantee that every admitted input avoids a resource stop. No speed, practical wall-time or machine-RSS guarantee is asserted.

The policy envelope is deliberately oversized but finite and conservative on the declared bounded domain. It pays exact polynomial setup, actual scans, planning, bounded canonical traversal and hashing even when the policy cache is warm. Meter charges elementary big-integer operations by operand/output widths; its control/storage envelope covers fixed loop/index/phase and copying work. Intended roots and inverse square root are recomputed and paid on every producer run. Actual adapter cost, dependency loading/hash cost and emitted trace/context/policy plus ledger serialization are added to the receipt. The original receipt and replay receipt must be added if both operations are performed; repeated exports require the documented additional policy envelope.

The reviewer requested one repair: replay originally returned only a work bound. The author added `recomputation_cumulative_storage_upper_bits`, including the zero-branch fallback and both extra policy-storage envelopes. The repaired source is the one exercised by the independent controls. Replay now exposes both the work and cumulative-storage bound for fresh computation plus bounded packet validation/expected serialization/comparison. These are accounting envelopes, not measured CPU or peak memory estimates.

## Independent execution evidence

`review_controls.py` is fresh reviewer-authored standard-library code. Its interval oracle uses the separate identity pi=4(atan(1/2)+atan(1/3)), outward rational interval operations, direct phase-weighted block projection and dense negative-sign unitary DFT. It shares neither the candidate recurrence/gauge schedule nor its root construction. Nine new states span N=3,4,5,6,7,8,10,11,16, odd parity, wrapped phases, nondividing blocks and B=N. All direct target enclosures satisfy the claimed numerical radius; independent intended-root enclosures fit within the producer's root certificates. Receipt sum identities and emitted-byte charging are also checked.

The main fresh suite passes 92 named controls, and four further boundary controls pass, for 96 independent named controls in total. Actual N=4,p=4096 and N=B=64,p=203 runs pass. The combined N=64,B=3,p=4096 case passes with 3,689,193 metered integer operations, maximum working width 65,251 bits and a 1,272,939-byte diagnostic trace. A p=4097 request is explicitly rejected. No inference that every permitted combination succeeds is needed. The author's separately retained final suite reports 69 named checks and 14 direct interval-DFT cases; those retained results were inspected rather than independently relabeled as a reviewer rerun. Finite tests corroborate the reviewed implementation; they are not a universal theorem proof.

## Exact downstream stopping boundary

A separate actual call constructs the pinned BUCKETS engine with WindowSpec(N=64,B_Q=4,r=1,Pq=112,beta_Q=None), then runs the real adapted DyadicSource with sigma=3,tau=7. It queries 63 supported entries and returns four output buckets. The source class identity and actual component execution are established. Its theorem window-delta guard is false, as expected for this reduced fixture. Neither the source budget pass nor the component call qualifies it as a theorem sparse instance.

The retained adapter admits N<=4096. Any theorem sparse Q16 instance has beta_Q>0 and k=2^ceil(2 beta_Q m)>=2, together with B_Q>=4096k and B_Q<=N. Consequently B_Q>=8192>4096>=N. The interfaces have no common theorem instance. This is an exact domain incompatibility, independent of benchmarks, feasibility opinions or test coverage; stronger window and outer guards are unnecessary to establish it.

Full theorem-scale integration requires a separately reviewed widened producer/deployment interface as well as a cap-compatible source adapter and genuinely eligible downstream instance. The present producer itself has N<=64. The second ideal target remains R P x/alpha, with R[j]=(-j mod N); original-input Fourier recovery, sampling accuracy, a fast backend and all-size guarantees are not consequences of this bounded completion.

## Authorized endpoint

Accept and stop the bounded producer-binding task. All 14 files in the final manifest were independently checked for byte count and SHA-256; the executed producer/policy/dependency source matches the frozen source exactly. Preserve ALG-034's wider open status and priority. Do not promote the reduced fixture to universal sparse integration, treat replay as remote attestation, claim a new precision theorem, or infer original-input recovery. No Sheet or GitHub mutation is part of this review.
