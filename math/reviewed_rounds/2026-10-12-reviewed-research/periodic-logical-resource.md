Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: a1cc2ae0100f3ee1ff2c4a9cc37761aac41e3657cb1c71235bb0c03ca6ad32d4

---

# Independent review: periodic resource-admission contract

Review ID: PERR-2026-10-11-2115. Date: 11 October 2026 UTC.

## Decision

**ACCEPT AT THE EXPLICIT BOUNDED LOGICAL-RESOURCE SCOPE**, without a source repair,
for the fresh derivative at SHA256:

`cd302fc96b7455d7b63c76d478c3921b95c83e487953fc32784b8765b3b81a5f`.

The accepted additions are:

1. An explicit, conservative logical-resource admission API, checked before input
   elements are accessed or input-sized working buffers are allocated.
2. Default-domain compatibility and preservation of the prior numerical result,
   certificate, branch, and interval-product-bit measurement.
3. Complete accounting of the **named** bulk buffer operations described below,
   including the length-one root-table write, retry work and final materialization.

This is a return-or-refuse reference, not a production or universally successful
algorithm. It does not establish a bound on RSS, bytes, elapsed time, every
arithmetic operand or bit operation, or failed-call accounting. It does not
establish fixed-word execution, competitive certified-library performance,
external priority, a new FFT improvement, or discovery/optimization of Q.
Q09's theorem/proof status and classical Pythagorean classification are unchanged.
No Sheet or GitHub writes were made by this review.

## Artifact identity and method

The author supplied:

- Candidate archive: `Q09_STRQ4_Periodic_Resource_API_CANDIDATE_2026-10-11.zip`.
- Archive SHA256: `3b81c556d94eb3cde4cc0cde922889e6f9e70d93e09c0fd7b5f922586d99e037`.
- Candidate source SHA256: `cd302fc96b7455d7b63c76d478c3921b95c83e487953fc32784b8765b3b81a5f`.
- Candidate manifest SHA256: `c8bc1de260ba3d74263639f24ef7adc11aed85076428b5f5b4af12380b2fca5c`.
- Accepted numerical baseline SHA256: `22f6820e9719d3fb89cb0db62f333a3fe092301dd110593515d13e0d8ae0f884`.

Every one of the ten candidate-manifest entries was checked for byte length and
SHA256. Every non-directory archive member was byte-compared against the frozen
candidate copy. `evidence/source_binding.json` records the checks. No original
uploaded provenance executor was imported, executed, compiled or AST-parsed.
Executable inputs were the fresh candidate, the independently accepted fresh
baseline, their fresh tests, and newly written reviewer tests. The candidate source
and baseline were not edited. An explicitly separate, reviewer-created AST
instrumentation derivative was used to observe buffer operations; it is not the
accepted implementation.

The frozen candidate preserves the author's report and original evidence without
retrofitting the independent verdict into them. Author tests ran in a separate
replay copy. This review's own report, tests and evidence are separately named.
The sealed review manifest hashes all included files; the externally recorded ZIP
hash binds that manifest. This is a byte-integrity seal, not a digital signature
or proof-assistant certificate. No Library upload or remote publication was
performed as part of this review.

## Exact public contract

The inherited numerical domain remains in force:

- The outer input and every length-two pair have type exactly built-in list or
  tuple. Components, f, epsilon numerator and exponent, and supplied Q have type
  exactly built-in int. Booleans and subclasses are rejected. No input or pair may
  change concurrently during a call.
- N is a power of two, 1 <= N <= 2^20. Let ell = max(1, log2 N) and cap = 4 ell.
- Each component has absolute value strictly below 2^cap; |f| <= cap.
- Epsilon is u / 2^t, where 0 <= t <= cap and 0 < u <= 2^t. Noncanonical dyadic
  forms are admitted. Q is None or a power of two from 1 through N.
- The represented input is (a_j + i b_j) 2^(-f). Successful dense output certifies
  relative l2 error at most epsilon against its negative-sign unitary DFT. This
  does not certify the error of an earlier conversion from a different signal.
- Exact Python integer arithmetic and correct isqrt are the arithmetic model.
  At most two prescribed precisions are attempted. CertificationFailure and
  interpreter failures do not return an approximate result.

New entry points are ResourceLimits, plan_resources and the optional limits
argument of transform. ResourceLimits must be an exact instance of the supplied
frozen dataclass; each of its four declared fields must be an exact nonnegative
integer. Limits are logical admission controls. They can be larger than machine
words and are not allocation sizes. With limits=None the declared defaults apply.

plan_resources validates a header and returns the reservation; it does not inspect
or validate input components or certify that a numerical result will be obtained.
The returned plan has a constant number of metadata fields in N. The source's
'O(1)-size' description is a size claim about the preflight plan, not a wall-time,
security-sandbox, arbitrary-object-mutation, or physical-memory guarantee.

## Admission and validation audit

The implementation validates exact outer type before any length/iteration hook.
The built-in container length and scalar headers are checked before the resource
planner; no arbitrary sequence, generator or subclass is admitted. The planner
checks each resource limit before the scanner constructs groups or a snapshot.
The first overrun, in N / fraction-bits / butterflies / slots order, raises a
ResourceLimitExceeded carrying resource, required and limit. Invalid API data
raises ValueError instead. This ordering was checked on malformed element payloads
which would have raised ValueError if reached.

The mantissa change from abs-and-compare to exact-int bit_length is equivalent on
both signs: bit_length(v) <= cap iff |v| < 2^cap. It rejects giant invalid integers
before squaring or taking an allocated absolute value. The f comparison similarly
avoids an unnecessary absolute-value copy before rejection. Type checks precede
operations which could invoke subclass hooks. Normal construction of the exact
ResourceLimits type supplies only the four scalar fields; no input iterable is
consumed in planning. The implementation is ordinary trusted Python code, not a
sandbox against callers rewriting class definitions or bypassing frozen-object
internals.

Fresh tests checked every declared resource field with invalid exact types,
negative values and malicious hook objects; generator, list subclass, int subclass
and malformed input shapes; positive/negative million-bit mantissas; and
million-bit valid nonnegative limit values. No unexpected hook invocation occurred.
The intentionally huge valid limit values remained metadata and did not cause
allocation proportional to their values.

All 15 early-refusal probes, across N=1, 2, 256 and 262144, refused before touching
invalid elements for each positive reservation. This run's traced incremental
peaks were 2,961–3,289 bytes. These observations support the ordering audit; they
are not a portable RSS/allocator bound. N=1 has zero required butterflies, so
required-minus-one is not a legal nonnegative cut for that field.

## Reservation bounds

For each header the reservation is:

- max_working_fraction_bits = (9 + indicator(Q supplied)) ell + t + 48.
- max_transform_butterflies = N log2 N.
- max_logical_complex_slots = 7N + Q, taking Q=0 for q=None.

The input bit length b is at most 4 ell. The general first precision is
b + 5 ell + t + 16; the periodic call uses b + ell instead of b. The retry adds
32. Thus both first and second precisions fit the reserved fraction-bit field.
This field does not bound all product/energy/grid integer widths: it bounds the
working fractional scale p identified in the API.

A length-L radix-two transform performs L log2 L / 2 butterflies. L is N on the
general/fallback branch and Q on the periodic branch, so two attempts consume at
most N log2 N. Zero output skips transforms, but the reservation is deliberately
made before learning that the input is zero or periodic. A tighter budget may
therefore refuse a call whose actual selected branch could have fit. No optimal
admission policy is claimed.

Slots count sequence entries holding complex records, not scalar limbs, endpoint
pairs, object headers, list spare capacity, caller input, dictionaries or Python
execution state. Snapshot plus groups contribute N+Q. While roots double, old
and new root lists overlap by at most 3L/2 entries; the previous-attempt output
may contribute a further L. During a retry's normalization phase, roots, FFT data,
new intermediate output and previous intermediate output contribute at most 4L.
Final output formation overlaps at most L intermediate entries with N dense
entries. All these phases fit the additional 6N allowance in 7N+Q; aliases to an
existing list do not create another buffer. This is a logical live-buffer proof,
not a statement that an allocator promptly returns unreachable physical storage.

The fresh exhaustive header pass covered all 13,420 combinations of legal N,
supplied Q or None, and legal t. Maximum reservations were exactly 328 fraction
bits, 20*2^20 butterflies and 8*2^20 slots. Thus every prior legal header fits the
default limits. At the maximum legal t for each N/Q header, exact-boundary
acceptance and each possible required-minus-one cut supplied 1,006 independent
budget refusals with the correct structured exception fields.

## Named bulk ledger

The ledger counts semantic buffer operations, not all Python primitive actions:

- Every successful call reads N external input records, writes N snapshot records,
  forms N exact energy terms and writes N dense output records.
- With Q, it initializes Q group records and performs N projection updates. Each
  update reads and writes two scalar group components; these are the declared
  2N group_buffer_reads/writes. A nonzero Q call then reads Q group records for
  group energy. Outer-list indexing mechanics are not an additional claimed
  primitive-instruction ledger.
- Per actual length-L transform attempt, FFT input reads are L; FFT data writes
  are L + 2s + 2B and reads are 2s + 2B + L, where s is the number of bit-reversal
  swaps and B = L log2 L / 2.
- Each cold roots call writes 1 + 2 + 4 + ... + L = 2L-1 records, including one
  write for L=1. Root-table reads are max(0,L-2)+B.
- Each attempt writes L intermediate outputs and inspects L normalized/error
  records. Only the final successful intermediate output is read for dense
  materialization, L=Q on the periodic branch and L=N otherwise.

The fresh instrumentation wraps newly constructed semantic buffers in a separate
AST derivative. It observes initialization, append, indexing, iteration and
assignment without changing the candidate Meter logic. Across 72 cases at
N=1,2,4,8,32,128, including zero, periodic, fallback and forced second attempts,
the observed named operation counts exactly matched the returned counters.
Instrumented and plain full results were also compared on non-forced cases.
Weak-reference tracking of owned semantic buffers never exceeded the reservation;
the largest observed ratio was 0.75. The N=1 Q=1 case appears twice when the
parameter list contains both Q=1 and Q=N; 72 is a case count, not 72 distinct
parameter triples.

Instrumentation is corroborating executable evidence for the source-level bound,
not a physical-memory profiler or formal proof. The wrapper's own bookkeeping is
not presented as part of the original implementation's resource use.

Successful-call counters accumulate both attempts. A failed numerical call still
does not expose its ledger. max_product_bits measures only interval-multiplication
endpoint products, not all arithmetic. These exclusions are material and retained.

## Numerical compatibility and failure behavior

The full diff changes validation, metadata and counters; it does not change the
energy gate, root/interval arithmetic, butterfly operations, normalization,
precision schedule, acceptance inequalities, dense output values or exponent.
The earlier certified return-or-refuse numerical argument is therefore retained.
The new preflight may introduce a refusal under explicit tight limits, but the
defaults do not narrow the previous legal header domain.

Fresh full baseline comparison covered 1,504 complete outputs, exponents, branches,
certificates and max_product_bits values at N=1,2,4,8,16,32,128,512. Inputs included
zero, extreme constants, impulses, alternating and fresh deterministic random
vectors, all supplied Q, minimum tolerance, noncanonical epsilon, and extreme
input exponents. All matched the accepted baseline exactly.

640 of these outputs were independently checked against an exact rational
sixteenth-root DFT enclosure, using explicit radical root identities and an
integer-comparison bisection sqrt enclosure. The oracle calls neither the FFT,
its half-angle root builder, nor isqrt. It bounds the full output's squared l2
error, including every bin, rather than inspecting a selected coefficient.
There were 1,317 independent nonzero certificate checks, including the fresh
N=8192 cancellation witness. Exact rational residue means independently validated
projection/residual energy and the gate.

Fresh boundary checks accepted the exact epsilon=1 gate equality and rejected a
strictly larger residual. The N=8192 input 2^44+(-1)^j with Q=1 and epsilon=2^-48
correctly took fallback with residual numerator N^2; no floating cancellation was
used. Three forced two-attempt failures raised CertificationFailure after exactly
two attempts. Three injected MemoryErrors propagated. Neither path returned an
approximate result. The Q=1 short refusal did not silently invoke a general retry.

Two further full-N checks at N=2^20 passed: zero with Q=N, and an extreme signed
alternating input with Q=2, epsilon=2^-80 and f=-80. The latter returned the exact
Nyquist output and zero at every other bin, with the required complete scan,
copy and root counters. No maximum-N general FFT was executed.

The inherited final orthogonal-budget assert remains in the source. It is
redundant given the unchanged explicit gate and short certification inequality;
removing Python asserts does not remove the actual error acceptance checks.
Sixty complete result snapshots matched byte-for-byte after canonical
serialization in normal Python and Python -O; all three forced numerical refusals
also remained refusals in both modes. An explicit exception could be preferable
as defensive coding style, but is not needed to repair this admitted algorithm.

## Cold-cost claims and remaining limits

No new timing or speed claim is made. Roots are prepared cold for every actual
transform attempt and their named cost is counted, including retries. The old
source's timing evidence must not be relabeled as timing for this derivative;
additional metering/preflight can change elapsed cost. This review gives no
optimized-library, process-cold, controlled-hardware or bit-complexity conclusion.

Still open:

- Numerical certificate success for every admitted input within the two attempts.
- Physical byte/RSS/runtime guarantees and fixed-word production execution.
- Complete primitive/bit-operation accounting and observable failure ledgers.
- Arbitrary input conversion and Q selection/discovery.
- Competitive certified-backend measurement, external novelty/priority, or general
  FFT speed improvements.

These are not hidden prerequisites to the narrow accepted logical-admission gate;
they are separate obligations which remain open.

## Reproduction and audit trail

Python 3.12.14 was used; the code is standard-library-only. From the review root:

```
python3 independent_resource_tests.py
python3 edge_checks.py
python3 edge_checks.py --snapshot
python3 -O edge_checks.py --snapshot
```

The last two JSON results should match. Replay the author suites in a fresh copy
of frozen_candidate, so their generated evidence does not overwrite frozen bytes:

```
python3 test_resource_gate.py
python3 -m unittest discover -s . -p test_accepted_regression.py -v
```

All seven author resource groups and nine inherited regression groups were rerun
successfully. Their 912 baseline replays, 216 small-oracle checks and 57 budget
cuts are inherited/author-suite replay evidence, separate from the reviewer counts
above. The independently authored suite has six passing groups plus the edge
checks. Its first draft mistakenly classified f=-1 as invalid; that reviewer
harness error was corrected, and the entire suite reran successfully. The first
log is retained as evidence/harness_first_run.log. No candidate repair followed
from that harness error.

Suggested concise status: “Conservative preflight logical resource admission and
the full named bulk-buffer ledger independently accepted at source cd302fc9…;
certified bounded reference retained. Universal numerical success, physical
resources and production remain open.”
