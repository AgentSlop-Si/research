# Bounded outer-transfer production subgate

Status: author candidate, 17 October 2026. Independent numeric oracle and final
source review are required before independent acceptance.

## 1. Ownership and nonduplication

Fresh native reads of Research queue row 19 and Next cycle row 4 show that Q16
and STR-Q1 remain archived for low mathematical novelty/value. Their accepted
static coefficient contract and independent bounded reference regression remain
complete; production, provenance and complete outer integration are unfinished.
We do not reopen either archived research row. This separately requested
engineering subresult supports the still-open ALG-034/ALG-038 construction and
outer-transfer dependencies. The current ALG-034 row 19 retains general
full-recovery/owner obligations after its restricted producer and BUCKETS gates;
ALG-038 row 139 still requires a fully charged growing-parameter decoder.
No parent theorem, novelty score, priority or native-table state is changed.

The precise new deliverable is fresh executable coefficient/iterator code plus
an actual, paid Cartesian-median output producer and local semantic run binding.
There is no claim that the entire historical sparse pipeline executes at M=2^57.

## 2. Concrete numerical API and binding

The accepted source-pinned phase_medians.py defines MedianResult(pairs,bits),
where pairs is an immutable sorted sequence of (frequency,(real,imaginary))
integer numerators. Its cartesian_medians function validates exact immutable
candidate order and an odd nonempty sequence of estimate rows, sorts each real
and imaginary column independently, and returns the middle pair without extra
rounding. PipelineRun.output is that MedianResult numerical interface.

The fresh sparse_output.py implements these exact median semantics. Estimate
rows are supplied directly as immutable tuple rows instead of their historical
EstimateResult containers; output fields have the accepted numerical interface.
This is a newly reviewed implementation, not execution of a historical module.
A genuine call computes the output; no arbitrary four-support dataclass is
misrepresented as an executed pipeline. The fixture has three actual rows and
nontrivial signed values, while zero estimates may be retained.

ProducedMedians binds that exact computed output object to a frozen original
context containing M, P, the identical input candidate tuple and the identical
input row tuple. Outer.__init__ verifies the produced/context/output identities,
then actually recomputes the median from those immutable original inputs on the
same cumulative ledger and compares every output integer at its actual width.
Replacing the output alone fails identity. Replacing output and origin together
while retaining inconsistent inputs fails semantic replay. No hash, arbitrary
32-byte label, uncharged sorting or serialized assertion serves as provenance.

This is relative to trusted local execution and immutable ordinary Python
objects. Direct private-capability forgery, hostile memory mutation, monkeypatching
and arbitrary serialized objects are outside the accepted execution model, as in
the accepted deterministic pipeline. A new context containing new inputs is a new
run. No digital signature, cryptographic external-origin proof, or durable
serialized execution attestation is provided. Most importantly, supplied median
rows do not authenticate WINDOW/BUCKETS/phase execution, random tapes, sparse
recovery success, or the original source signal. Those full-pipeline provenance
obligations remain open. This closes only the local genuine-producer binding
subgate once independently accepted.

Outer retains a frozen Header(N,M,D,estimate_bits) with exact built-in integer
fields and the exact produced result. Support is independently checked for exact
integer type, strict order, uniqueness and range. All actual output integer
fields are copied/read and charged. Every incidence holds the same binding;
foreign or cloned bindings fail. Every emitted coefficient carries a private
origin tying its incidence and exact numerical certificate to the current
wrapper; foreign origin, substituted grid, index, numerical field or enclosure
fails validation. This is a defensive source invariant, not hostile-runtime
security.

## 3. Geometry and exact enumeration

The header requires N>=1, D>=5, and
M=2^ceil(log2(4N)). Put m=log2 M, s=Dm, h=16s+1, t=2h+2.
When t>=M the iterator returns OUTER_DENSE_REQUIRED without numerical setup.
This is a dispatch requirement, not random recovery failure, and the actual
dense transform is deliberately outside this component.

For each sorted support index k the code computes
r0=ceil(N(k-h-1)/M), r1=ceil(N(k+h+1)/M), using signed floor division.
It emits ell=r mod N for r0<=r<r1. The row-first stencil says
k=floor(ell M/N)+j mod M, -h<=j<=h+1. Lifting ell to r=ell+vN turns
this into k-h-1<=floor(rM/N)<=k+h, equivalently the half-open interval
N(k-h-1)/M<=r<N(k+h+1)/M. This proves exact set equality.
Its real length Nt/M<N, so no two emitted lifted values are congruent mod N;
no deduplication or N-row scan is necessary. Each support has at most ceil(Nt/M)
incidences and E<=St. Endpoint/prefix records are prepared once in O(S), and
record-ordinal checks use direct lookup, never an O(S) scan per coefficient.

The fresh regression separately constructs expected incidences by iterating the
stencil offsets j and solving floor(ell M/N)=(k-j) mod M. It checks all actual
row-first memberships and complete set equality. This is an independently
formulated algorithm by the same author, not a second-author acceptance.

## 4. Numerical recurrence and certificate

The byte-identical fresh production_scalar.py is the paired scalar candidate.
Its separate proof and final independent review own the recurrence details.
The wrapper forwards only verified retained incidences and never rounds the
returned p-grid output again. For fixed D:
J=(D+5)m+bit_length(s)+8,
K=J+2 bit_length(J+1)+16, p=(D+3)m+3, eta=2^-((D+3)m).
One Machin pi and one fixed-step integer square root are prepared lazily on the
first actual coefficient call. Repeated preparation is charged but does not
repeat those computations. Empty support, enumeration-only operation and dense
guard rejection perform no pi/sqrt setup.

The target remains the exact accepted phase times normalized Dirichlet factors
and sqrt(M/N). Residue zero uses the exact dyadic limit before division.
Nonzero residue is at least 1/(NM), and the fixed precision proves positive
lower denominator endpoints. Odd signed powers remain signed. The fixed K-grid
rectangle contains the true complex target. Midpoint nearest-even rounding to
p-grid uses floor/nonnegative remainder, including negative ties. For each record
the exact integer inequality R_real^2+R_imag^2<=2^(2(K-(D+3)m)) proves absolute
complex error at most eta. A certificate failure is an implementation defect,
never the sparse theorem's allowed random failure event.

At D=5,m=57,N=2^55-1,M=2^57, all 9,123 incidences on support
{0,1710,2^55+1,2^57-1} are enumerated. Counts are 2,281; 2,280; 2,281; 2,281.
Exactly three coefficients are evaluated: (ell,k)=(0,0),
(2^53,2^55+1), and (0,1710). They respectively exercise exact zero limit,
minimum nonzero residue 1, and the negative odd-power ratio. J=587,K=623,p=459.
The actual signed_power([-1/2,-1/4],285) returns exact K-grid numerator
endpoints -2^338 and -2^53. A fresh even-only stand-in rejects exponent 285;
an absolute-power replacement gives positive endpoints and fails the primitive
control. The tiny sign witness is not claimed to violate eta at final rounding.

The theorem's beta=1/8 branch metadata are checked by exact integers: B|M,
B>=4, T>=4, B>=4096k_sparse, W<M, t<M and beta*m>=2. The fixture's estimate
grid is the theorem grid P=16m+16=928. These facts are parameter compatibility,
not execution of the theorem-sized sparse front end or validation of its
success event.

## 5. Complete resource accounting and finite caps

ReceiptLedger records exact reached integer fields, copies, comparisons,
endpoint arithmetic, loop/address bookkeeping, sort steps, returned incidences,
record certificates and binding/replay work. Its deliberately conservative
per-event factor pays 256*w^2 bit operations and 64*w cumulative produced/control
bits at relevant integer and counter widths. Failed validation preserves spent
prefixes. A 16,385-bit malformed field is actually visited and paid before a
later boolean field is rejected. The numerical Paid ledger independently pays
all arithmetic, powers, shifts, reductions, divisions, Taylor/factorial/sqrt
loops and certificates plus its documented control envelope. The two ledgers
are cumulative and add; none is reset on repeated validation or preparation.

For the outer stage after local-producer association, bounded-width estimate
metadata and fixed D give O((S+E+1)m^2) nonnumeric work, plus conditional
O_D(m^5) numerical setup and O_D(m^5) per evaluated coefficient. With F evaluated
coefficients, the total coefficient-stage bound is
O_D((S+E+1)m^2 + 1_{F>0}m^5 + F*m^5).
The full stream, if evaluated, would have F=E; this regression has F=3.
The endpoint/prefix table costs O(Sm) bits. Streaming working state contains no
N-vector, phase cache or E-record retention. Caller-retained outputs cost extra
storage; the test harness deliberately stores E incidence receipts and pays
that through its separate host cap and source test bound.

Producer and semantic replay are additional, explicitly charged work. For S
candidates, R odd estimate rows and maximum input/output width H_e, merge sorting
costs O(S R log(R+1) H_e^2) bit work in the conservative model, plus header and
input-reading costs. Replay incurs this again. This must not be hidden inside
the outer O(Sm^2) bound, especially for unbounded caller-supplied R or H_e.
In this fixture R=3, S=4, H_e=O(m), so it is fixed bounded extra preparation.
The general numerical API permits arbitrary exact integer amplitudes; their
actual input widths are charged. No general theorem-sized sparse producer cost
or random-output bound is inferred from this fixture.

These are source-level arithmetic ledgers, not CPU instruction or Python heap
measurements. The launcher independently applies 180 s wall, 120/125 s CPU,
512 MiB address-space, 32 MiB per-file and 64-open-descriptor caps. A cap failure
would be a resource blocker. PROCESS_EXIT.json retains the actual exit, empty
stderr on success, observed time and unchanged pre/post source hashes. The source
scan, rather than fast elapsed time, establishes absence of hidden N/M loops.

## 6. Required final checks and exclusions

Independent review must check these new source bytes and the fresh median API
refinement, reject plausible binding/enumeration/certificate mutations, and
independently enclose the three true coefficients using different pi/error
control. Shared production Scalar bounds are not an independent oracle.

Full coefficient-stream evaluation, accepted full sparse-pipeline provenance,
estimate multiplication, scatter, every-tape finite accumulators, N outputs,
final rounding/scale-back, dense fallback/all-length dispatch, and independent
J-call amplification are all outside this subgate. All original norms,
probabilities, fixed-parameter scopes, and trust assumptions remain unchanged.
