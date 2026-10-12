Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 334425fb0b075b9fc1890f352ef7bb2662e5efceaf5308b84dc3c003efdb9339

---

# Independent ACCEPT: Q09 / STR-Q4 bounded arithmetic-work reservation

Review date: 11 October 2026 (UTC). Verdict: **ACCEPT at the explicitly declared source-semantic elementary exact-integer model**, with no source repair. This is a conservative reservation theorem, not an exact dynamic operation ledger or a physical-performance guarantee.

## Sealed subject

- Candidate ZIP: `Q09_STRQ4_Bounded_Arithmetic_Work_CANDIDATE_2026-10-11.zip`
- Candidate ZIP SHA256: `2507b788dafa08daf8d93060ec1ddbcb768d2862af17632e36db33bd3905e165`
- Reviewed wrapper `bounded_work.py` SHA256: `9349e5a4afd480a03b818189e42d883b6992f1ee47fd3c872f6fdd1707619c40`
- Unchanged accepted numerical source `accepted_reference.py` SHA256: `cd302fc96b7455d7b63c76d478c3921b95c83e487953fc32784b8765b3b81a5f`
- All 16 entries of the candidate manifest were independently verified for byte count and SHA256. The candidate archive separately binds its manifest.

Only the included already accepted fresh reference, this round's new wrapper/tests, and fresh independent test-only derivatives were executed. No uploaded original research executor was executed. No external service, repository, or spreadsheet was changed during this review.

## Accepted statement and exact boundaries

For a legal header, h=log2(N), ell=max(1,h), t=epsilon_t, and delta=1 when Q is supplied, the new API reserves

    pbar=(9+delta)ell+t+48
    D=5ell+pbar+3h(h+1)
    W=8(D+t+h+1)+256
    P=2^28 N(h+1)^2
    T=64P(W+1)^3.

W bounds source-visible validated/imported arithmetic operands and results. P bounds the complete source-semantic primitive execution. T bounds an elementary signed-integer implementation of those semantics, including integer division and square root. The model already charges arithmetic algorithm scratch work; W is not an assertion that every internal arithmetic scratch register has W bits.

All three budget comparisons are inclusive. At required==limit the work planner accepts; at required==limit+1 it refuses, with the correct named resource and exact required/limit values. The check order is operand width, primitive steps, then bit work. Independent logical-resource admission remains a separate check. Both checks precede signal element access and input-sized working buffers.

Every supplied field in both exact dataclass budget records is checked as an exact nonnegative integer of at most 256 bits. Those seven fields do not determine allocation dimensions. Oversized metadata is refused before it enters the accepted reference's asdict/error-formatting paths. Header controls similarly have bounded legal ranges and exact-type checks before dimension/exponent arithmetic. This closes the previously important possibility of an arbitrarily wide accepted caller budget being silently included in a fixed arithmetic-width theorem.

The maximum header reservations are W=14,568, P=124,130,464,729,399,296, and T=24,566,743,150,123,429,473,025,309,802,496. Default budgets admit all 13,420 legal headers. The domain restriction is a new wrapper contract; it is not a claim that every unbounded metadata input accepted by the old API remains accepted by the new one.

## Independent proof audit

### Widths and finite arithmetic

The proof's precision ceiling is valid for both attempts: the accepted kernel chooses b+5ell+t+16 and then adds 32; b<=4ell, and the periodic branch adds at most another ell. Residue sums have magnitude below 2^(4ell+ell). Group energy and residual bounds follow by exact sums and Cauchy-Schwarz; no floating subtraction is used.

The half-angle root construction uses only exact interval arithmetic and integer square roots. The cosine interval bound of 2S and sine bound S are preserved by its outward rounding and nonnegative-radicand intersection. A conservative complex-root multiplication grows a component by at most a factor eight. With at most h doublings, root components are bounded by S*2^(3h). For each nontrivial half-angle stage there are two interval-root calls, containing four elementary isqrt calls, plus one normalization isqrt per attempt; all are included by the node/helper count. No trigonometric call, transcendental oracle, coefficient cache, or uncharged precomputation occurs.

Each butterfly can increase an endpoint bound by at most 8*2^(3h). At most h stages give the stated D. Normalization endpoints do not exceed S; normalization, midpoint, radii, squared-error accumulation, certificate comparisons, the final orthogonal-budget assertion, and their left-associated products all fit the proof's smaller intermediate bounds and hence W. Valid input import, fixed-grid conversion, normalization, and dense dyadic export are included. Numeric success is not used to bound either precision attempt.

Source integer powers have fixed exponents only: the header's constant 2**20 and four squares. Addition, multiplication, signed floor quotient/remainder, shifts, and isqrt admit the elementary scan/schoolbook/restoring implementations described in the candidate. Their bit work fits the deliberately loose per-primitive allowance 64(W+1)^3. Bounded logical-refusal decimal formatting also fits that allowance. This does not assert a CPython-library complexity bound.

### Control flow and expanded builtins

The independently counted combined AST has 4,138 nodes, below 8,192. The proof includes helper and meter entries rather than merely FFT butterflies: cmul has 16 method/meter entries, cadd has five, csub has eleven, and each butterfly adds four explicit meter entries. Root construction, bit reversal, conversion, normalization, and outer scanning are separately covered.

The per-attempt unit ceiling sums conservatively to 40B+3Lh+40L+70h+80 for L<=N. Two attempts plus outer work give at most 46Nh+144N+140h+672, which is below 1024N(h+1) throughout the legal domain, including N=1. The source skeleton multiplier 8192 and fixed scalar/record multiplier 32 yield 2^28N(h+1), below the reserved P. There are only 26 possible meter keys; no unbounded dictionary-key population is hidden in fixed-key bookkeeping. The named dictionaries, dataclass fields and record arities are bounded. sum, comprehensions, and list copies have per-element expansion rather than arbitrary-length unit cost. The extra factor h+1 in P supplies further slack.

The resulting count is a conservative structural proof. Test traces corroborate selected executions; they are not the proof and are not advertised as an exact primitive ledger.

### Admission, invalid records, and exceptions

The new wrapper validates materialized exact list/tuple headers and all control/budget fields before invoking the numerical scanner. Work refusal and logical refusal therefore happen without a transform attempt. Those pre-admission exceptions are not promised a work_reservation attachment.

Once both admissions pass, invalid-record ValueError carries the complete reservation even when a valid prefix has already been scanned. Exact type and cached magnitude-length checks precede input arithmetic. Rejected caller-owned giant objects are outside W; their rejection uses the explicitly declared descriptor-access convention. This is not a bound on arbitrary external parsing or on the caller's cost of constructing such objects. Concurrent mutation, user hooks, rewritten classes, altered frozen objects, and monkeypatching are excluded from production execution as stated in the proof.

The source runs at most two precisions. Each attempt rebuilds roots, imports/converts its transform input, computes every butterfly and error scan, and performs its certificate comparison. On a first failure and second success, the full reservation still applies. On two failures, CertificationFailure returns no output and carries the same reservation plus completed_precision_attempts=2. Forced tests changed only the error returned after the real numerical attempt; they demonstrate retry and reporting paths, not natural failure existence or universal success. Numerical ArithmeticError/assertion failures excluded by the already accepted invariant proof are not newly promised as failure ledgers. MemoryError and interruption propagate, with no reliable attachment guarantee.

## Fresh independent evidence

The independent test suite passes in ordinary Python and Python -O, separately. Each run verifies:

- 16 candidate manifest entries and both exact source hashes.
- 13,420 headers, independently recomputed formulas, and exact-boundary admissions.
- 40,260 one-unit-below refusals: every legal header against each of the three work fields.
- 69 adversarial control/protocol cases, including all seven budget fields at the 256/257-bit boundary, million-bit positive/negative controls, and exact-type/hook rejection.
- 27 work/logical refusals with the scanner replaced by an immediate sentinel failure, proving the scanner is not entered on those paths.
- 63 admitted invalid-prefix cases, including middle/final records and million-bit rejected mantissas, with the promised attached reservation.
- 740 complete comparisons against the byte-identical accepted reference over all four output branches, general/fallback/periodic/zero; tolerance numerator extremes, common-exponent extremes, Q extrema, and exact work budgets are included. Normal and optimized result digests match: `286cd30caae0f8a772d1ddea509bf2fa7eef5eafa5777ed4a38548ffa6e2b950`.
- Ten real two-attempt controls: five terminal refusals and five retry successes. Counts confirm cold-root writes and normalization scans occur twice. Two interpreter-boundary probes cover MemoryError and KeyboardInterrupt.
- Two N=2^20 paths: zero with Q=N and a nonzero extreme periodic Q=2 signal with a directly checked exact output. No maximum-N general FFT is claimed to have run.

A separately authored AST instrumentation script passes 97 cases in normal and optimized mode. It instruments entries, loop/comprehension visits, expression integer widths, expanded sum, and dense list-copy work. It includes real forced two-attempt controls and 256-bit caller budget metadata. Observed maxima are 375 source-visible integer bits, 104,322 activation units, and 2,281,962 expression observations in normal mode (2,281,935 in -O). The largest observed activation count is 0.076171875 of the conservative activation ceiling. These observations cover only the tested executions.

The candidate author's eight test groups were also rerun from a separate copy in both modes and passed. Those results remain author-suite replays, separately labeled from fresh independent evidence.

## Scope and remaining work

> Independently accepted conservative source-semantic arithmetic-work reservation in the explicit elementary exact-integer model. Header-only admission, source-visible operand-width bounds, complete conservative primitive/bit-work ceilings, bounded dyadic import/export, and both cold precision attempts (including terminal refusal) are covered. Failure charges are full reservations, not actual measured tallies.

The previously accepted numerical certificate, mathematical proof closure, and classical Pythagorean attribution are unchanged. This result does not establish universal numerical success, exact dynamic operation counts, actual CPython instruction/bit costs, physical memory/RSS/bytes, wall time, fixed-word production execution, arbitrary external-file/real-to-dyadic conversion, automatic Q discovery, competitive backend performance, external priority, or general FFT improvement. Prior timings must remain attributed to their original measured source.
