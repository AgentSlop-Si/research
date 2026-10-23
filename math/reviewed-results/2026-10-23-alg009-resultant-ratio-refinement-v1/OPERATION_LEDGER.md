# Paid schedule for the new executor only

This ledger is for `paid_executor.py`, not repaired counts for the historical
program. Additions, subtractions, multiplications, negations and inversions
are separately metered; exact zero tests are metered separately. A field
operation includes modular reduction. This is a unit-cost F_p model, not a
bit-operation or Python-instruction bound. The supplied certified prime and
canonical residues specify the field; no primality test, field search,
primitive-root search, representation conversion or extension construction
is claimed free inside a stronger input model.

## A. Capped all-path field work

- Root setup and validation: N products build the N entries and closing
  power, and N subtractions/zero tests check no earlier power equals 1 and
  omega^N=1. This checks exact order without factoring N. At most 2N field
  operations plus N zero tests and linear reads/writes.
- Eight Fourier samples: each sample streams powers of its known table
  entry, using 2N multiplications and N additions. Total 24N field
  operations. The code intentionally charges a final stream update even
  when its result is unused. There is no Fourier oracle or hidden FFT.
- Fixed algebra: 46 padded Sylvester determinants and direct Lagrange
  interpolation. All loops are bounded by 46,6,4 and are independent of N.
  A conservative 500,000 field-operation cap includes every normalization,
  sign, interpolation inverse and unsuccessful pivot search's arithmetic.
  One resultant evaluation has fewer than 600 field operations: two cubics
  use at most 410, five powers use five, and the six-by-six elimination
  uses fewer than 180. One Lagrange basis uses at most 4,369 field operations
  (4,140 convolution, 135 denominator/node, two scale, 92 accumulation);
  46 such bases plus 46 resultants are below 230,000, hence below the cap.
  Variable-length trims and pivot equality tests are also bounded constants;
  they are recorded separately, not omitted from runtime discussion.
- Root admission: Horner with at most 46 coefficients costs at most
  92(N-1) field operations and N-1 zero tests. The scan returns the exponent
  d directly. It does not assume an algebraic root is in the supplied
  subgroup or perform an uncharged discrete logarithm. At most 45 shifts
  survive, by the proved polynomial degree bound.
- Anchors: at most N raw zero tests and reads, followed by exactly three
  inversions after T!=0. Those inverses are shared over all candidate shifts.
- Proposals: at most 135 multiplications, including repetitions and zero
  candidates. No deduplication or expected retry bound is needed.
- Raw certificates: at most 135N products and 135N subtractions, plus
  135N zero tests and O(N) index work per proposal. Scans stopping on the
  third defect are charged for every processed coordinate; the bound charges
  the entire N anyway. A support count of zero is rejected.
- Pole policies: for each proposal passing the support scan, all N
  denominators are formed with 2N products and N subtractions, N zero tests,
  and N stream updates already included in the products. At most 135 such
  scans give 405N field operations. Multipole candidates are rejected after
  this charged scan. No gcd, exponentiation or pole-finding oracle is needed.
- Complete output: two geometric streams need at most 4N products and 2N
  additions. Nonpole division uses at most N inversions and N products.
  One direct pole repair uses at most 2N products and N additions. Thus at
  most 11N field operations produce all N coordinates, including the paid
  single-pole repair. Pole tests and all output writes are explicit.

Consequently an upper bound for all fast-path arithmetic, success or decline,
is

    500,000 + 804N + 138 field operations.

The coefficients are deliberately loose: 2+24+92+270+405+11=804, plus three
anchor inversions and 135 proposal products. The implementation's exact
meter may be substantially smaller. This is not an optimized performance
claim. All paths are deterministically capped; there are no random restarts
or unaccounted failed trials. Root/setup reuse is explicit, not assumed for
objects that actually rebuild tables.

Exact indexing and loop counters use O(log N)-bit words. Data storage is O(N)
field elements plus a fixed amount of polynomial storage and at most 135
small attempt records. Canonical field-element read/write/comparison costs
depend on log p; field inverses and reductions are not constant bit-time.
No floating-point operations or tolerance tests are used.

## B. Fallback and Green composition

When `with_fallback=True`, every decline adds a full direct DFT using the
already built root table: exactly 2N^2 multiplications and N^2 additions in
the streaming schedule, plus N output writes. It uses no extra roots. This
gives universal correct output in the specified field domain, not a generic
sub-N-log-N or O(N log N) theorem. Invalid field/root-domain inputs raise a
domain error rather than pretending to have an exact fallback.

Alternatively a separately valid exact FFT backend can be composed, but its
entire cost and required roots must be added; no such backend was executed
here. The historical Bluestein needs compatible 2N-th and convolution roots.

For original x, construct the fixed Green diagonals and cyclic factors,
verify all nonzero constructor guards, apply P, then solve L. Each uses a
fixed number of linear passes and field inversions. These are additional
paid O(N) stages on the same constructor domain; they are not included in
the raw-r scalar total above. The candidate's full-x witness uses independent
dense linear algebra as a control only. No costed execution or repaired meter
for the historical Green wrapper, hybrid, or fallback is asserted. Its
literal implementation audit remains open.

## C. Execution evidence boundary

`run_executor_controls.py` executes only newly authored `paid_executor.py`
and `exact_controls.py`; no historical module is imported, compiled or run.
Reference DFTs, dense input construction/Green lifts and witness search are
test work outside the claimed fast-path runtime. `EXECUTOR_RESULTS.json`
contains all new-executor stage meters, failures and complete reference
outputs. `CONTROL_SUMMARY.json` is the compact control result. These finite
controls support implementation inspection; the uniform coverage and budget
claims depend on the proof, not on extending finite measurements to all N.
