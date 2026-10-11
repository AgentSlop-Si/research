# Independent review of the periodic early exit reference

Review ID: PEXR-2026-10-11. Date: 11 October 2026 UTC.

## Verdict

ACCEPT the bounded, return-or-refuse certified reference at repaired source SHA256
`22f6820e9719d3fb89cb0db62f333a3fe092301dd110593515d13e0d8ae0f884`,
under the exact API contract below. The mathematical gate, interval FFT,
normalization, short error budget, dense output and gate-rejection fallback pass
independent review and executable checks. No ordinary admitted-input numerical
counterexample was found.

The initial source at SHA256
`5ecb9417a5aa80e2b5f6998dabad63cd7204f2bb0f2beb39cc47c60c982ef814`
has a reproducible container-validation hole. Its arithmetic is accepted only for
an honest stable sequence. The released implementation should be the explicitly
revised source in `repaired/periodic_reference.py`, whose narrow admission repair
has been independently audited and tested. This review does not silently relabel
the original source as repaired.

ACCEPT the saved timing evidence as an accurately reported, plan-cold Python
reference comparison for the ORIGINAL source. All 36 cases were replayed on both
versions: certificates, counters and complete returned results were identical.
That replay is not a new timing experiment. The original timing figures must not
be attributed to the repaired source as newly measured figures.

No acceptance of universal resource-policy success, production fixed-word
execution, optimized-library superiority, a general FFT improvement, or external
novelty/priority is given. S4/R22 and Q09's classical Pythagorean classification
remain unchanged.

## Source binding and review method

The author archive is `STR_Q4_Q09_Periodic_Exit_Reference_CANDIDATE_2026-10-11.zip`,
Library `libfile_2110ff4ea7148191857d6f5e28aeb4bd`, version 0, 81,550 bytes,
SHA256 `e4c07321a483b6efe14c960ee6c12a5f678880f449d712ff679632d194bccb80`.
Its bytes were independently materialized from Library and hashed. Every archive
member matched the supplied local packet; all 21 entries in its MANIFEST matched
their recorded byte lengths and SHA256 values.

The accepted S4 source is `author_packet/sources/00_05-structured-fusions.md`,
SHA256 `02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787`.
R22 in the saved decisions binds this source and requires exact dyadic energies
and a representable epsilon/2 short tolerance. The inherited proof, decisions,
source programs, hardening tests and row snapshots were read as inert evidence.
The original uploaded/source programs under `sources/` were not imported,
executed, compiled or AST-parsed. Executable work used only the newly authored
reference/tests and the review's own tests and replay.

The full author packet is preserved unchanged under `author_packet/`.
The original fresh numerical source and tests are additionally under `frozen/`;
the admitted revised source and exact patch are under `repaired/`. The review
scripts and logs are included. The sealed manifest binds every included member;
the archive's externally reported SHA256 binds the manifest itself. This is an
integrity seal, not a digital signature or a formal proof-assistant certificate.

## Exact accepted API

The public entry point is `transform(values, *, f=0, epsilon_a=1,
epsilon_t=4, q=None)` in the repaired source.

1. `values` must have type exactly the built-in `list` or `tuple`. Every pair
   must also have type exactly `list` or `tuple` and length exactly two.
   Subclasses, generators, mappings, arrays and custom sequence objects are
   rejected. No input or nested pair may change concurrently during the call.
2. N is the actual outer-container length and is a power of two from 1 through
   2^20 inclusive. Let ell=max(1,log2 N) and cap=4 ell.
3. Both pair components have type exactly built-in `int`, with absolute value
   strictly less than 2^cap. Booleans, integer subclasses and floating-point
   values are outside the contract. The represented input is
   x_j=(a_j+i b_j) 2^(-f), with integer f and |f|<=cap.
4. Epsilon is exactly u/2^t, where u=`epsilon_a` and t=`epsilon_t` are built-in
   integers, 0<=t<=cap and 0<u<=2^t. Noncanonical dyadic representations, including
   u=2^t for epsilon=1, are legal. The internal epsilon/2 is exactly represented
   by u/2^(t+1); it need not satisfy the public input parameter bound t<=cap.
5. Q is supplied as `q`, either None or an exact built-in integer power of two
   with 1<=Q<=N. Since N is dyadic, Q divides N. No Q selection or input conversion
   is included. With Q=None the call runs the general baseline directly.
6. A successful result contains all N output integer pairs and one shared binary
   exponent. It approximates the negative-sign unitary DFT of the represented
   input with relative l2 error at most epsilon. This is not componentwise
   relative error, and does not cover error to a signal before its conversion
   to the represented dyadics. Zero input returns N exact zero pairs.
7. The arithmetic model is ordinary correct Python arbitrary-precision integer
   operations and `math.isqrt`, with sufficient memory/runtime to finish a call.
   At most two specified working precisions are tried. If neither certifies,
   `CertificationFailure` propagates without returning an approximate result.
   Resource/interpreter failures may also abort; successful completion for every
   legal input is not claimed. Gate rejection runs the general fallback. A short
   transform certification refusal does not silently invoke a general fallback.

Returned dictionaries/lists are ordinary mutable Python objects; the guarantee
describes their contents at return. Private helpers are not independent public
APIs for arbitrary dimensions, precisions or intervals.

## Numerical argument

### Exact gate and finite integer bounds

For the unscaled integer input z, the complete scan forms
A=sum_j |z_j|^2 and residue-class sums S_c. Put M=N/Q,
B=sum_c |S_c|^2 and D=M A-B. The common factor 2^(-2f) cancels from every
relative comparison. Exact orthogonal projection gives projected energy B/M and
residual energy D/M. In particular D>=0 and B<=M A.

The code tests exactly `2*D*2^(2t) <= M*A*u^2`. All products and the subtraction
M A-B are Python integers. This is not a floating cancellation check, fixed-width
overflow assumption, sample-based detector or probabilistic certificate.
The advertised gate bit bounds are conservative under the admitted input size:
A needs at most 9 ell+2 bits; M A, B and D at most 10 ell+2; the comparison
products at most 18 ell+3. These bounds do not assert that 64-bit arithmetic
suffices, and do not substitute unit-cost machine operations for Python bignums.

The cancellation witness was rerun in both author-suite passes. With N=4096,
Q=1, z_j=2^40+(-1)^j and epsilon=2^-44, ordinary binary64 subtraction yields
zero residual while the true residual energy is 4096. D=N^2 in the certificate,
and the exact gate rejects.

### Interval operations and coefficient preparation

An endpoint integer denotes that endpoint times 2^-p. Addition, negation and
subtraction are exact endpoint operations. Multiplication takes the minimum and
maximum of all four endpoint products and divides outward using integer floor
and ceiling. Halving similarly rounds outward, including negative odd integers.
Square roots use exact integer square roots and an exact upper-endpoint equality
check. Each therefore encloses its exact real operation.

The roots begin with exact 1, -1 and -i. For each doubled length, even roots are
reused and odd roots multiply the preceding enclosing root by the new half-angle
root. The cosine and sine half-angle formulas enclose the correct first-quadrant
values. Intersecting the sine radicand with its known nonnegative domain is safe:
the exact radicand lies in that domain and the incoming interval already contains
it. There is no trigonometric/libm accuracy premise. Reusing even roots and one
enclosing product for each odd root does not create a serial chain of N rotations.
Every call constructs its own coefficient table.

Bit reversal is the usual radix-two permutation. Every butterfly composes the
enclosing operations, so induction over stages encloses the exact unnormalized
DFT. Dependence between intervals can enlarge the error bound but cannot cause
under-enclosure. The normalization lower endpoint is
isqrt(floor(2^(2p)/N)), exactly floor(2^p/sqrt(N)); a square-equality test selects
whether the upper endpoint is identical or one tick larger. Final midpoint
rounding remains inside the rectangle. Summing squared farthest-endpoint distances
over both real components gives H, a rigorous squared l2 error upper bound in
tick units. This includes coefficient, butterfly, normalization and output-grid
rounding errors.

### Short transform and full error budget

The short transform computes DFT_Q(S)/sqrt(N), exactly sqrt(M) U_Q(mu), where
mu=S/M. It avoids a separate rounded division by M and multiplication by sqrt(M).
For grid factor G=2^(2p), certification requires

    4 M 2^(2t) H <= u^2 B G.

Thus the embedded short error is at most (epsilon/2)^2 times the projected
energy. Only bins M*l contain short outputs; every other bin is explicitly zero.
The residual transform is zero on these bins because every residue-class sum of
the residual vanishes. Its support is therefore disjoint from the short-output
error. The full squared error is bounded by D/M+H/G, and the code additionally
checks

    (D G + M H) 2^(2t) <= u^2 M A G.

This last assertion follows already from the accepted gate and short inequality:
the two contributions are at most epsilon^2 A/2 and epsilon^2 A/4. Consequently
Python's optimized mode removing this redundant assertion does not remove the
actual certification inequalities in `_certified` and the gate. An explicit
exception instead of `assert` would be sensible future defensive style, but is
not a correctness repair required for the current admitted source.

On gate rejection, `_certified` operates on the complete owned snapshot and
checks `H*2^(2t) <= u^2*A*G`. It is the same general numerical backend, requested
tolerance and output representation as the baseline. Common exponent f is only
incorporated in the final grid exponent; the cancellation of 2^(-2f) in all
relative comparisons is exact. If A=0, all components are zero and the early
dense zero output is exact. If Q=N, D=0 and the branch still performs a full-size
short FFT; there is no structural saving.

## Validation defect and reviewed repair

Original `_scan` validated `len(values)` but then trusted a separate iteration.
There was no outer-container type check, and pair types used `isinstance`.
An object reporting length four can therefore:

- Yield no elements and return a successful zero result with N=0
- Yield three (1,0) pairs with Q=1 and return a certified periodic result with N=3
- Yield two (255,0) pairs and return N=2, although the N=2 mantissa cap is <16

These are admitted-dimension/mantissa validation failures. They are not examples
of a false numerical error bound for the actual yielded snapshot. Other length
mismatches can throw arithmetic or indexing exceptions. An unbounded iterator
also defeats any resource interpretation based on the initial length.

The reviewed patch requires exact built-in list/tuple types for both the outer
container and each pair. It rejects custom outer containers before calling their
length or iteration hooks, and rejects pair subclasses before calling their
hooks. Under the retained no-concurrent-mutation precondition, actual length and
iteration now agree. No numerical, tolerance, coefficient, precision or output
code changed. All ordinary list/tuple combinations remain supported. Rejecting
subclasses and arrays is an explicit narrowing of the API, not an incidental
compatibility promise.

## Independent execution evidence

Both the original and repaired sources passed all nine author-authored test
groups in independent reruns. Those include 60 author-oracle full-output checks
and the floating-cancellation witness. An important count correction is needed:
the author suite makes 810 projection test calls, of which 800 evaluate a nonzero
gate and 10 take the zero shortcut. “810 exact gate evaluations” overstates the
literal count by ten.

The independent suite is newly written for this review. It uses explicit eighth
roots, rational interval arithmetic and a separate integer-bisection square-root
routine to bound every coordinate of the direct DFT for N=1,2,4,8. It does not
reuse the reference FFT, half-angle table, `math.isqrt` normalization, or the
author's Machin/Taylor oracle. It checks all supplied-Q choices, all four built-in
container combinations on the repair, extreme mantissas and f, epsilon=1 in
canonical/noncanonical form, numerator 3, and the smallest admitted epsilon.

For the repaired source the saved results contain:

- 672 rigorous independent full-output oracle comparisons
- 798 nonzero certificate verifications, including 622 exact nonzero gate checks
- 371 periodic paths, 251 fallback paths and 176 direct-general paths
- 56 zero paths and 54 separate bit-identical fallback/baseline checks
- 9 exact gate boundary/neighbor controls
- 6,075 exhaustive small-endpoint interval multiplication checks and 630 square-root controls
- 20 ordinary invalid-input rejections
- 3 repaired length/iteration mismatch rejections and 6 custom/subclass rejections before hooks
- 4 admitted built-in outer/pair container combinations
- 2 maximum-N=2^20 tests: dense zero and extreme-mantissa constant Q=1 input
- 2 forced two-attempt safe refusals and 1 forced successful second-precision retry

The original independent run has the same 672 oracle comparisons, 794 nonzero
certificate verifications and 618 nonzero gate checks, and records the three
validation counterexamples. The four additional repaired-container checks account
for the difference. Maximum-N tests are separate and do not imply coverage of a
maximum-size general FFT.

Refusal/retry controls deliberately substitute a huge synthetic enclosure-error
bound in the private backend. They establish that the policy refuses or retries
as coded, without returning the substituted bad output. They are not evidence of
a naturally occurring legal-input refusal. No natural refusal occurred in these
tests or saved profiles; neither that observation nor finite testing proves
universal success of the resource policy.

Every saved profile was independently reconstructed from its documented seeded
input generator. Both original and repaired candidate and baseline calls were
run: 36 rows times four calls, 144 transforms. All complete return values were
equal before and after the admission repair. Each saved certificate, counter
dictionary and maximum-product diagnostic reproduced exactly. This is stronger
than comparing only a floating numerical norm, but remains finite replay evidence.

## Timing and operation-accounting audit

All 36 saved rows contain seven samples for candidate, matched baseline and
ordinary NumPy, for 756 timed calls. Every saved median and baseline/candidate
ratio recomputes exactly from the raw samples. Every recorded scalar certificate
inequality holds, every candidate/baseline dense-output count is N, and all saved
calls report one precision attempt. NumPy's median is smaller in every row.

For the original N=4096,Q=8 periodic input the recorded medians are:

- Periodic reference: 2.796538 ms
- Identical certified general backend at epsilon=1/16: 145.254559 ms
- Ratio: 51.940849364464206
- Ordinary uncertified NumPy context: 0.690086 ms

The main comparison has matching represented input, complete dense dyadic output,
and relative-l2 error obligations. The baseline is not forced to epsilon/2;
it receives the requested epsilon. It performs its own complete scan, energy,
coefficient setup, FFT, normalization, certification and output. The candidate
pays projection/gating and output costs and, on rejection, the same full backend.
The source alternates candidate/baseline order, excludes common input generation,
and includes instrumentation inside the timed call.

“Cold” here means no coefficient plan, transform, energy certificate or output
reused across calls, within an already running Python interpreter. It does not
mean cold process/CPU caches, isolated hardware, no competing work, or controlled
thermal state. No independent new performance estimate is made in this review.
The saved short-period speed ratios are credible for this particular reference
backend; they are not a generalized speed claim or evidence against optimized
certified libraries. Q=N retains full transform work; rejected inputs pay
recognition plus the general call. Small inverted ratios are not justified as
negative-input speedups.

NumPy is explicitly a different contract: raw-pair conversion and a dense Python
complex output are included, but exact dyadic output and a rigorous error
certificate are absent. Its being faster on all cases correctly prevents claiming
a practical win over ordinary optimized FFT execution.

Counters are not a complete machine-operation ledger. One small descriptive
qualification: `_roots(1)` returns before incrementing `root_table_writes`, so
the length-one coefficient-table write is not represented in that named counter.
It is still executed and timed. This does not undermine the all-in wall-clock
comparison or O(N+T(Q,epsilon/2)) structural claim. Avoid describing the dictionary
as an exact count of every primitive operation. The `max_product_bits` field
likewise measures interval-multiplication endpoint products, not every integer
temporary or gate product.

The returned “certificate” is an arithmetic audit record from the trusted reviewed
implementation. It does not serialize all coefficient enclosures or bind the
output to the input cryptographically. Saved benchmark JSON retains those scalar
records and counters, not every dense output; independent replay generated and
compared the full outputs. Do not present the scalar JSON alone as a standalone
untrusted proof object.

## Table implications and remaining obligations

The scoped STR-Q4 reference stopping condition is met by the repaired accepted
implementation, correctness review and honestly limited original profile. A status
such as “Scoped bounded reference validated; production open” is justified.
Q09 may append the implementation evidence and distinguish “bounded reference
validated” from “production pending.” Preserve its existing proof closure and
classical classification, and preserve prior history and source citations.

Any appended evidence must bind BOTH hashes: the repaired code for API acceptance,
and the original code/archive for the measured figures. Replace author-pending
wording with this actual review identity only after the review artifact is saved.
Correct the 810-call versus 800-gate wording and document the exact container
restriction. `ROW_PROPOSALS.json` remains a proposal; this reviewer made no Sheet
or GitHub changes.

Still open: a proof or explicit redesign giving total success for the resource
policy; production fixed-word arithmetic with complete overflow/rounding bounds;
general input conversion and supplied-Q discovery costs; optimization preserving
directed enclosures; competitive certified-backend comparisons and controlled
hardware measurements; and external priority. The Python reference does not
inherit a production word-RAM bound merely by using bounded legal inputs.

## Reproduction

From this review directory, use Python 3.10+:

    python3 independent_tests.py frozen
    python3 independent_tests.py repaired
    PYTHONPATH=frozen python3 -m unittest discover -s frozen -p test_reference.py -v
    PYTHONPATH=repaired python3 -m unittest discover -s repaired -p test_reference.py -v
    python3 replay_profile.py

Only fresh reference/review programs are needed. Do not execute provenance
programs under `author_packet/sources/`. The initial author benchmark is preserved
for provenance and optional explicit reproduction; this review's replay makes no
new timing claim. Evidence JSON and logs distinguish each source variant.
