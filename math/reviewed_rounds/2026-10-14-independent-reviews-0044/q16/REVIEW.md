# Independent acceptance of the new Q16 bounded reference regression

Verdict: **ACCEPT_INDEPENDENT_BOUNDED_REFERENCE_REGRESSION_ONLY**.

No blocking numerical or mathematical repair was found. This independent review
accepts the newly authored three-record reference/oracle experiment and confirms
the earlier static contract within its stated fixed-D arithmetic model. It does
not accept a production outer wrapper, sparse-output provenance adapter, full
coefficient stream, all-length transform, or general FFT improvement.

## Objects and execution boundary

Reviewed inputs are `bounded_reference_regression/` and
`outer_contract_static_acceptance/`, with the latter's pinned contract/proof and scalar
source read as inert text. The new regression source SHA-256 is
`e2226910c0abdc5a3fd0da5bdc6c0262db6c83248d26fa12340582a191c681be`.
Both packet manifests/seals, all 19 payload hashes/sizes, and all 26 static-review
input pins verify. These hashes establish byte integrity, not signatures.

Only a byte-identical local copy of the new `regression.py` and its new launcher,
plus this review's newly authored `audit_checks.py`, were executed. No historical
uploaded code was imported, compiled for execution, or run. Original input files
were not changed. No table, repository, document, or other external write occurred.

The preserved-copy regression exited 0, with empty stderr, no timeout, and
unchanged pre/post source hash under its 180-second cap. Its complete RESULTS.json
matches the submitted result **byte for byte**. Its measured process duration was
0.5677133589997538 seconds. The separate reviewer controls exited 0 in
1.8864867230004165 measured process seconds, also with empty stderr and no timeout.
These durations are observations, not complexity evidence.

## Independent enclosure audit

The reference's Machin pi, point-Taylor sine, fixed bisection square root,
all-corner quotient/products, signed endpoint power, phase, and nearest-even
certificate assembly match the accepted mathematical recurrence. The historical
scalar implementation was inspected only as text to check that correspondence.

The oracle has no call to the Reference class or its numerical methods. It shares
the `Paid` elementary integer helpers and the target formula, which were explicitly
audited; it does not consume reference pi, sine, root, power, or output bounds.
Its fixed metadata means it is an oracle for this fixture, not a general API.

The oracle's independent numerical choices are valid:

1. pi = 4 atan(1/2) + 4 atan(1/3). The tangent addition is exactly 1, with
   both positive angles summing below pi/2. Alternating-series next-term tails
   are applied to the correct side after outward rounding each term.
2. Sine uses signed integer-part/parity reduction and interval Horner evaluation.
   Starting Y=1 and repeatedly replacing Y by 1-X^2 Y/((2j)(2j+1)) gives the
   degree-(2n-1) sine polynomial after multiplying by X. Interval dependency
   can widen the enclosure, but cannot invalidate it. The degree-2n Taylor
   theorem is applicable because the even coefficient vanishes. The computed
   factorial and 2^(2n+1)/(2n+1)! tail rigorously bound the remainder for X<=2.
3. The restoring base-4 root algorithm maintains the usual exact root/remainder
   invariant. Both its result and the reference bisection root independently
   equal Python's integer isqrt of floor(M*2^(2B)/N), with exact rational-square
   inequalities checked afterward.
4. Repeated integer multiplication of each signed endpoint and one final outward
   division encloses the odd power. It does not reuse square-and-multiply.
5. The zero-residue limit, odd integer Dirichlet orders, normalization constants,
   and real/imaginary phase arguments agree with the exact target. Every selected
   nonzero division has a strictly positive denominator lower endpoint.

Thus nesting of the valid oracle rectangle inside the reference rectangle is
meaningful. This review supplies the separate reviewer missing from the original
same-author report; it does not retrospectively relabel that report's authorship.

## Three selected coefficients and exact bounds

The verified metadata are D=5, m=57, N=2^55-1, M=2^57, s=285,
J=587, K=623, p=459, and eta=2^-456. For each record, independent Fraction
arithmetic reconstructed the rounded midpoint, both squared-radius certificates,
oracle nesting, and the advertised power-of-two error upper bound.

- (ell,k)=(0,0): exact Dirichlet limit branch; absolute complex error <=2^-496.
- (ell,k)=(0,1710): strictly negative normalized ratio raised to odd s=285;
  oracle real lower bound is positive, rounded complex output is zero, and
  absolute complex error <=2^-693.
- (ell,k)=(2^53,2^55+1): ell*M-k*N=1 exactly; absolute complex error <=2^-460,
  which is at most eta/16.

The exact squared-error upper numerators over 2^1800 are retained in
INDEPENDENT_RESULTS.json and the byte-identical rerun/RESULTS.json. These are
rigorous upper bounds, not exact transcendental errors or floating estimates.

The actual new signed_power on [-1/2,-1/4]^285 returns K-grid endpoints
(-2^338,-2^53). The absolute-power control returns positive endpoints and fails
this sentinel; the newly authored even-only control reports exactly
`even exponent required`. The historical even-only helper was not executed.
The tiny (0,1710) coefficient is correctly **not** claimed as an eta-violating
final-output counterexample for an absolute-power substitution.

## Preparation, enumeration, and paid work

The numerical preparation is charged once per nonempty engine. A repeated
reference prepare call leaves both state and ledger unchanged. Empty support
has zero pi/root setup and zero sine calls, while header charges remain positive.
The fresh dense-guard control similarly performs no scalar preparation.

Both original engines make 12 sine calls for the three records: two for the zero
case and five each for the nonzero cases. The reference's 1,262 atan iterations,
625 root iterations, 5,040 Taylor iterations, and 10,096 factorial iterations agree
with its fixed loop structure. The oracle's 1,832 atan terms, 902 restoring root
pairs, 7,320 Horner iterations, 14,656 factorial iterations, and 1,710 endpoint
power steps likewise agree. The two extra reference signed-power controls are
included in its ledger rather than omitted from the reported arithmetic totals.

Maximum reported numeric widths are 177,556 and 256,501 bits, respectively.
They correctly include large power intermediates and binary denominators. The
instrumented arithmetic is charged; uninstrumented bounded control/index/copy
work uses the explicitly declared conservative envelope. That envelope and all
reported ledger totals/storage formulas were independently recomputed.

This accepts the stated finite binary-arithmetic bookkeeping, not a measurement
of Python allocations, CPU instructions, JSON serialization, hash time, or RSS.
The ledger is deliberately loose. It is not experimental proof of an asymptotic
bound. The separate static derivation is valid: for fixed D, K,s=O_D(m), maximum
numeric width H=O_D(m^2), and O_D(m) arithmetic steps per coefficient imply
O_D(m^5) schoolbook bit work. Header/incidence work is separately bounded by
O_D((S+E+1)m^2), retaining the empty-header +1 and conditional scalar setup.

The original enumerator emitted exactly 9,123 unique incidences for the four
support indices. This review independently constructed the expected pairs by
iterating stencil offsets j and solving floor(ell*M/N)=(k-j) mod M, rather than
reusing the same lifted-interval formula. Its expected set equals the emitted
set exactly. Source inspection finds no N/M-sized scan, array, or phase table;
the only numerical coefficient evaluations remain the three selected records.

## New independent finite controls

All **11,015 assertions** pass. The complete categories are in
INDEPENDENT_RESULTS.json. In addition to integrity, selected-record and ledger
checks, these include:

- 9,123 exact row-first center checks and complete incidence-set equality
- 1,560 exact signed-power endpoint controls with odd/even exponents and
  negative, positive, zero, and crossing-zero intervals
- 94 exact algebraic sine controls per engine across positive and negative
  periods, using rational squared values for sin(pi*x)
- independent integer-root and rational-square checks for both engines
- minimum-residue denominator positivity and the large odd-power sentinel
- ten malformed-header controls, with exact ValueError text retained

The smaller primitive controls supplement the source/proof audit; they are not
additional theorem-sized coefficient runs or a general production validation suite.

## Remaining boundaries

The original production obligations remain in force. In particular this reference
class is not the promised production API: the 32-byte label is fixture metadata,
its Python attributes do not establish immutable binding to a real accepted sparse
output, and the coefficient method is not a validated public emission interface.
The dense guard is an internal flag/empty iterator rather than a complete caller
dispatch. Malformed-input controls here do not establish paid production prefix
receipts. The oracle is hard-coded to this fixture.

The next justified gate is a concrete source-pinned production wrapper and
accepted sparse-output association, followed by the same bounded regression
through that real API. Full stream/scatter, estimate multiplication, paid finite
accumulation and N outputs, scale-back, dense/all-length dispatch, and independent
amplification remain separate. No norm, probability, novelty, or FFT-wide claim
has been strengthened by this review.

UTC timing and actual counter availability are recorded in STATUS.json. No model
token-use counter was exposed; none is estimated or inferred. No unexpected
scientific/tool error occurred during this review. Expected negative-control
errors are preserved exactly and distinguished from failures.
