# Independent final review: sparse-original supplier

Date: 17 October 2026 UTC.

## Verdict

PASS: 525 independent named checks passed within the explicitly bounded
sparse-original, singleton-block contract.
No blocking production, mathematical, input-binding, or resource defect was
found. This is an independent review of the new supplier, not acceptance of a
general dense-input algorithm, general block sizes, a rounded-serial-equivalent
algorithm, or a free full DFT. The companion bucket theorem is reviewed
separately.

Reviewed production file:
`../candidate/sparse_supplier.py`

Pinned SHA-256:
`5c1454ef006d34c91be02643a57ebf4cd47adaf9aaaf85fb951e98095ca439ed`

The complete new production source was read before importing it. Only that
fresh source and standard-library modules were imported by the independent
test program. No historical uploaded research program was imported or run;
there were no network calls or external writes. The production file was not
changed. All ten delivered manifest entries matched their stated hashes and
byte lengths at review time.

## Independent evidence

`independent_review.py` is newly written review code. It does not import the
producer's checks or oracle. `INDEPENDENT_RESULTS.json` records all named
checks, exact source and sample query packets, and endpoint receipts. The
separate `RUN_LOG.txt` records the successful run and final count.

The checks include:

- Complete exact N=4 and N=8 transforms in the field Q(sqrt(2)), with exact
  algebraic ordering rather than floating comparison. Every output enclosure
  and complex error bound is tested. Applying the negative unitary transform
  twice gives reversal exactly; exact norm squared equals E/2^(2h).
- Independent rational-pi arithmetic using the identity
  pi=4(atan(1/2)+atan(1/3)), alternating-series remainder bounds, outward dyadic
  Taylor arithmetic, and a direct reciprocal sqrt(N) bracket. This differs
  from both the producer's half-angle implementation and its test oracle's
  Machin formula. Independent point-error certification passes for all seven
  theorem-scale fixture queries and 40 additional arbitrary-support queries
  across even and odd exponents, including m=63 and m=64.
- Exact algebraic point-error tests at the maximum requested precision
  R=4096, at N=4 and N=8, including negative phases.
- Successful fresh setup and three queries for every m from 2 through 64,
  with arbitrary signed complex coefficients and extremely large symbolic F.
- Simultaneous m=63/64, 64 arbitrary support locations, 1024-bit components,
  R=4096, and 128-bit q/p metadata. The largest observed arithmetic data integer
  is 11,824 bits; the largest observed query has 23,020 metered arithmetic
  records. The working grids are 5,411 and 5,415 bits, respectively. These are
  within the stated 6,000/12,288-bit and one-million-record caps.
- Independent replay of the entire delivered N=16 full-output artifact,
  including its source and all 16 index-specific point packets.
- Accepted-radius boundary tests on both sides of R=467 for the large fixture;
  a larger p with insufficient R; and negative symbolic shifts at very fine
  numerical grids. Required-radius queries reject exactly as their advertised
  conservative guard requires.
- Grammar and resource attacks, source/root/sign/normalizer/policy/context
  tampering, wholly regenerated alternatives for each original-context field,
  query-value/radius/index/grid/digest tampering, and oversized/cyclic packets.
- Isolation against mutation of the original raw list or returned packet
  copies; zero input; and explicit checks that successful replay does not
  claim external origin authentication.

The independent test count includes individual coordinates, domains and attack
cases. It is separate from the producer's 144 named checks. Finite tests
corroborate the proof; they do not replace it or imply an unbounded theorem.

## Mathematical review

### Original-input domain and exact representation

The input grammar enforces genuine built-in integer/list/dict types, sorted
unique nonzero rows, range and width bounds, at most 64 entries, and removal of
common numerator powers of two. The canonical zero has empty support and F=0.
Every dyadic exponent 2<=m<=64 is admitted. The only block regime is B_A=N;
the valid odd a and beta remain bound to the input even though singleton P is
the identity. No restriction to quarter-axis support remains.

For E=sum(re^2+im^2), the implemented h is exactly the least nonnegative integer
with 2^(2h)>=E. Therefore E<=2^(2h)<4E for nonzero input. With alpha=2^(h-F),
the exact normalized modal target is

    z_j = N^(-1/2) sum_n (re_n+i im_n) 2^(-h) exp(-2 pi i n j/N),

and 1/2<||z||_2<=1. The descriptor represents this exact expression with zero
representation error. It is not a finite-precision materialization of N values.
The second negative unitary transform has support -n mod N and coefficients
(re_n+i im_n)2^(-h). F can remain huge and symbolic; its power is not expanded.

The raw coefficient l1 mass divided by 2^h need not be one. The descriptor
retains that mass, and a downstream tail proof must use it. This is important
for the separate bucket consumer.

### Root rectangles and numerical query

The base roots 1, -1, and -i have the required negative sign. Half-angle cosine
uses the positive square root, with outward rounding. The sine quotient uses
s/(2c_new), with a strictly positive denominator. It therefore avoids the
cancellation-prone formula sqrt((1-c)/2). Integer square-root enclosures are
valid by monotonicity and exact square checks. The binary character product
selects root[m-bit] for each set bit of n*j mod N, which has the correct phase.

The even-m inverse square root is dyadic; odd m uses an explicit sqrt(2)
enclosure divided by 2^((m+1)/2). This is a genuine treatment of odd lengths.
The outward complex products, coefficient scaling, summation, normalizer and
2^h division preserve containment. The final exact squared-radius comparison
certifies the Euclidean complex error around the returned point; it is not
just a componentwise heuristic. Correctness of a returned certificate follows
from the enclosure and final inequality even without relying on the generous
a priori precision estimate. The guard estimate and full admitted-length
execution tests are consistent with availability throughout the declared
bounded domain.

### Accepted policy and original grid

The new source retains the stated inherited singleton policy formulas and
checks p>=p_min. It stores C=2^c and all large exponents symbolically. This
review validates the new implementation's specialization and guard; it does
not attest historical execution of the inherited serial program.

A normalized point base*2^(-G), G=R+3, becomes an original approximation with
error at most 2^(h-F-R). Its original-grid numerator can be represented as
base*2^shift, where shift=p+h-W-G. Adding kappa=W-F-p gives the correct original
scale h-F-G. Thus the grid condition is shift>=0. Comparing its certified error
budget with C*2^kappa gives R>=p-c-W+h. The implementation requires both for an
accepted-radius claim, checks the formal stored-width bound, and rejects the
required-radius call when either condition fails. This is a sufficient
certified-budget guard, not a claim that a fortuitously exact point could never
have a smaller true error when the guard fails.

For the actual N=2^28, x=delta_1+delta_3 fixture, h=1, alpha=2,
p=268436013, kappa=-268436012, R=468, and b=615. Its original point-error budget
is 2^-467, below the accepted radius 2^-466. The original-grid shift is
268435542, but it is never physically expanded into that many trailing zeros.

### Input binding and limitations

Both verifiers recreate the entire correct supplier/query from independently
supplied original arguments and compare complete canonical results. A digest
is only a label. Self-consistent packets for changed raw input, F, a, beta, t,
q, p or R do not pass against the original context. Full replay binds roots,
normalization, policy, source, query index, output and claimed error.

If both the caller's independently retained context and the packet are
replaced, the verifier checks a different statement. It cannot authenticate
external origin or attest historical execution. The code and contract correctly
deny these properties. Frozen objects are not an adversarial-interpreter
sandbox; the documented pinned-source/correct-integer/no-concurrent-mutation
execution model remains necessary.

## Resource and output accounting

There is no loop over N or p. Setup performs O(s+m) logical arithmetic and
retains O(m) root rectangles. Each point query performs O(s(m+1)) logical
arithmetic, with paid integer-width-dependent work. The m<=64 bound does not
justify dropping log N from a general asymptotic theorem. Products and square
root radicands have their intermediate widths recorded; validation,
serialization, hashes, counters and bounded control work receive a separate
large binary-model envelope. These are conservative logical-work/cumulative-
storage bounds, not CPU time, peak RSS or a machine instruction census.

In the admitted maximum domain b<=5415. A coefficient-weighted accumulated
endpoint and its product with the normalizer remain below the 12,288-bit cap;
physically constructed powers are controlled by b, h and b-R, not by p. The
128-bit p/q endpoint tests directly exercise this distinction.

Packet exports require their advertised additional charge. Replay pays its
own fresh setup/query and export. Source loading, pin checks, input acquisition,
consumer operations and destination writes remain additional. The complete
small artifact is genuinely 16 paid point results. A complete theorem-scale
DFT still requires N queries and N output writes unless a separately proved
consumer operates directly on the exact modal expression. There is no hidden
free full-vector or serial-recurrence equivalence claim in the delivered
contract. Pointwise numerical guarantees are not automatically a global
vector-error or arbitrary downstream-algorithm theorem.

## Release scope

The supplier can be accepted as the bounded arbitrary-support sparse-original
source described above. The companion bucket review must independently verify
its window construction, coefficient-mass/error analysis, state/phase wiring,
complete outputs, and downstream work. This report neither supplies that
proof nor licenses broader claims about arbitrary dense inputs, general B_A,
all p-dependent numerical radii, full sparse recovery, universal FFT speedups,
external authenticity, or novelty.

## Companion coordination

The separate final bucket review was received and its report inspected. It
accepts the restricted nonconstant theorem-scale integration and pins the same
5c1454ef supplier. It explicitly preserves exact-modal consumption versus
finite-query-radius separation. No cross-packet supplier integration issue was
reported. That reviewer owns the downstream mathematical and execution
acceptance; its report is retained at
`../../nonconstant_buckets/review`.
