# C13 fixed-direction entry-oracle integration boundary

19 October 2026 UTC. Scope: a costing/implementation increment under the recorded
C13-FIXED-DIRECTIONS owner. This is **not whole-owner closure** and is **not a
new proof of the already accepted fixed-direction iff theorem**.

## Result and disposition

1. A classical, exact, unstructured target-entry oracle cannot support a
   worst-case subquadratic fixed-direction completion decision procedure. For
   every feasible target and supplied invertible directions, the elementary
   adversary below gives at least
   `N^2 - |supp(U) union supp(V)|` necessary distinct entry queries. In the C13
   two-support setting this is at least `N^2 - 4N`. The bound survives an
   invertible-target promise over fields of size greater than two.
2. An explicit Hamiltonian family with **all edge weights nonzero** gives
   `N^2 - 2N` queries over Q for every N >= 3. A permitted zero-edge family gives
   `N(N-1)`. Thus the obstruction is not dependent on allowing zero edges.
3. A fresh exact streaming adapter implements the inherited completion test
   for two prescribed Hamiltonian relative routes over Q or a supplied prime
   field. It uses at most `4N^2` target calls and `12N^2` sandwich field
   operations, O(N) field operations in the supported graph stage, O(N^2)
   explicit forbidden-root comparisons, and O(N) auxiliary storage when oracle
   tracing is disabled. Field setup, arithmetic bit costs, target-entry cost,
   target setup, and any target-invertibility certificate remain separately
   charged.

This closes the stated **scoped unstructured-entry costing/adapter task** in
this packet. It does not close the owner's direction-discovery, singular-mask,
primary-comparison, or application-specific integration tasks. No worldwide
priority, new algorithmic novelty, production readiness, or Fourier lower bound
is claimed. The proof and implementation have exact self-checks; this packet
does not claim an independent acceptance review.

## Why this is an actual remaining owner subtask

The source-bound Overview row 218 states that implementation, costing,
integration, or a stronger extension remains open while the earlier accepted
scoped result is retained. Catalogue row 101 says the complete off-support check
costs O(N^2), distinguishes the sparse affine solve, and separately preserves
general direction selection and constructive singular-mask work. The accepted
review explicitly calls its O(N^2) cost a complete **unstructured** verification
cost after target setup. These are the precise words addressed here.

The same records retain a primary-source theorem comparison/qualification gate.
That gate is not discharged by this elementary argument. Nor does the supplied
history identify a specific implicit Fourier target formula or a Fourier
implementation contract that this adapter could be said to complete. The
19 October triage already rejected whole-owner closure; that disposition stays
valid. The provided review, overview, catalogue and triage are copied unchanged
under `sources/`, with hashes and exact provenance in `SOURCE_BINDINGS.json`.

## Dependency: accepted fixed-direction theorem, retained verbatim in substance

Given fixed projective row/column directions U,V, nonzero base coordinates,
fixed legal structural routes, invertible branch denominators and free endpoint
scales, completion is equivalent to the existence of nonzero x_i,y_j satisfying

    U B V = U D_y + D_x V.

The complete off-support vanishing condition is indispensable. A row-pair gate,
independent pairwise nullspaces, or linear consistency without nonzero scales
does not substitute for it. Relative route order, base-coordinate nonvanishing,
cycle products unequal to one, and the original endpoint-routing obligations
must all be retained. Fixed zero-weight routes cannot be silently replaced.

We use this accepted theorem; we do not repackage it as new. Its historical
review is dated 10 October 2026, SHA256
`052b4155a0737109131d4d668495be161d867e209c1dea5c27717e366a4d339c`.

## Elementary query theorem

Let F be a field. Let U,V be fixed invertible N-by-N matrices, and write

    S = supp(U) union supp(V).

Assume the supplied directions/routes satisfy the inherited branch guards. Let
C be their fixed-direction completion set, with all scale variables nonzero.
The only varying input is a coherent exact oracle returning one target entry
B[a,b] per query. Preprocessing U,V is permitted, but the varying target has no
additional promise except, optionally, invertibility. The algorithm must be
correct on every target in this input class, including infeasible targets.

For any B0 in C, every deterministic correct algorithm must query at least
`N^2 - |S|` distinct entries on B0. With an invertibility promise, assume B0 is
invertible and |F| > 2; the same bound holds. Without that promise, no field-size
restriction is needed beyond F being a field.

### Proof

Invertibility supplies a nonzero determinant term in each matrix. Accordingly
choose bijections f,g on {0,...,N-1} such that

    U[f(a), a] != 0 for every column a,
    V[b, g(b)] != 0 for every row b.

The map (a,b) -> (f(a),g(b)) is a bijection on matrix positions. Define

    H = {(a,b) : (f(a),g(b)) is not in S}.

It follows that |H| = N^2 - |S|. For h=(a,b) in H and any nonzero delta, put
B_h = B0 + delta E_ab. The inherited necessary identity says every feasible
target has zero sandwich entry outside S. Since B0 is feasible,

    (U B_h V)[f(a),g(b)]
      = delta U[f(a),a] V[b,g(b)] != 0.

Thus B_h is infeasible for these supplied directions, regardless of how the
nonzero scales are chosen. It differs from B0 at exactly the entry h.

If the varying target is also promised invertible, the rank-one determinant
identity gives

    det(B0 + delta E_ab)
      = det(B0) (1 + delta (B0^(-1))[b,a]).

At most one nonzero delta makes this vanish. A field with more than two
elements offers at least two nonzero choices, so one makes B_h both invertible
and infeasible. The elementary determinant identity follows by determinant
multilinearity in the changed column (or row); no genericity assumption is used.

Now run a deterministic adaptive correct algorithm on B0. If it never queries
some h in H, the complete observed transcript and every adaptive decision are
identical on B_h. It returns the same decision for the feasible and infeasible
targets, a contradiction. Therefore every h in H must be queried. QED.

The lower bound is a bound on an algorithm whose input varies over the stated
oracle class. It does not assert that a particular already-known constant
matrix is expensive to recognize when its identity is promised in advance.

### Randomized extension in the same classical query model

Suppose a randomized algorithm has error at most epsilon < 1/2 on every input.
Couple its random bits on B0 and a fixed permitted B_h. Unless h is queried,
the two executions are identical. The difference between their acceptance
probabilities is at most the probability that h is queried on B0. Correctness
makes that difference at least 1-2 epsilon. Summing over h in H gives

    E[distinct queries on B0] >= (1-2 epsilon)(N^2-|S|).

This includes the zero-error expected-query statement. It is not a quantum
query lower bound or a lower bound for vector/batched oracle primitives.

## Explicit all-size witness families

Let P be the row-action cyclic successor permutation matrix for one N-cycle.

### Nonzero edges, invertible branches and target

Over Q, take N >= 3,

    U = I - 2P,  V = I - 3P,  x = y = (1,...,1),
    B0 = U^(-1) + V^(-1).

The base coordinates are all one, all two branch edge weights are respectively
2 and 3, the routes are the prescribed N-cycle, and the denominator products
are 2^N and 3^N, both different from one. The union support has exactly 2N
entries. The directions commute, so

    B0 = (UV)^(-1)(2I-5P).

The determinants 1-2^N, 1-3^N and 2^N-5^N are nonzero, hence B0 is invertible.
The theorem therefore gives N^2-2N necessary queries, even with the invertible
target promise. Alternatively, identity determinant matchings expose every
position outside the diagonal and successor edge directly.

### Permitted zero-edge sharpening

Over any field F with more than two elements, choose nonzero lambda != 1 and
take U=V=I while keeping legal prescribed structural N-cycles with zero edge
weights. Set x_i=1 and y_i=lambda-1. Then B0=lambda I is feasible and invertible,
and the actual union support has N entries. Every single off-diagonal
perturbation is still invertible and is rejected. The lower bound is N(N-1).
This is lawful because the inherited theorem allows zero edge weights but keeps
their structural routes fixed. It does not replace a prescribed route.

Over F2 the base sum can instead be B0=0 when target invertibility is not
required. We do not assert the invertible-target form of this zero-edge example
over F2; its nonzero scales force a zero diagonal sum there.

These are mathematical all-size statements about **validation in the specified
query model**. They provide neither an all-size Fourier constructor nor an
all-size fast transform impossibility theorem.

## Adapter contract and operation accounting

`adapter.py` accepts the four fixed row-action permutations r0,r1,s0,s1;
U-row coefficients a,b; V-column coefficients d,e; an exact target-entry
callback; and Q or a prime field. It deliberately supports the Hamiltonian
relative-cycle subcase. Other cycle grammars are outside this interface, even
when allowed by the broader inherited theorem.

The adapter checks shape, permutation validity, nonzero a,d, the precise
relative routes r0^(-1) composed with r1 and s1 composed with s0^(-1), and each
cycle denominator. It preserves zero-weight route constraints. It then streams
every entry of UBV, rejecting an off-support residual immediately and storing
only the at-most-4N supported equations

    V[i,j] x_i + U[i,j] y_j = (UBV)[i,j].

Every sandwich entry uses at most four target entries and, per term, two
multiplications and one addition. This gives at most 4N^2 target calls and
12N^2 field operations in this stage. Calls are not memoized; repeated calls
count again. Early rejection can cost less. The oracle's coherence, exactness,
and entry-call cost are caller obligations.

The affine graph stage constructs spanning-forest parameterizations, checks
every pin/cycle equation, and enforces all scales nonzero. Its field work is
O(N); root deduplication and candidate membership use explicit comparisons with
a conservative O(N^2) total bound. A component with m variables forbids at most
m parameter values. For Q, test the distinct integers 0 through m. For F_p,
test 0 through min(p-1,m). If no value works, the component exhausts the actual
base field and is rejected; an extension field is never substituted.

The adapter returns scale and graph certificates and the recovered canonical
Green-plan data with the source's different left/right permutation orders.
The tests independently reconstruct the dense branch matrices from those plans
and compare their sum to B. No uploaded historical program is executed.

Auxiliary storage is O(N), excluding the caller's target representation and
optional query-trace instrumentation. The rational/integer bit lengths are not
bounded by this field-operation count. Prime validation uses explicit trial
division and is separately charged as field setup; modular division and exact
rational arithmetic are not constant-time bit operations. No asymptotic
bit-complexity claim is made.

The adapter does not certify that B is invertible: the sum theorem does not
require it, and this is recorded in every completed answer. A forced-feedback
application needing invertible B must provide/check that additional guard.
Separately prescribed original endpoint permutations or endpoint values must
likewise be checked by a caller-side original-endpoint adapter before claiming
that stronger application contract. They have not been silently freed here.

## Implicit Fourier and other structured targets: remaining boundary

The callback can evaluate any exact supplied formula, including a Fourier
entry formula. If target setup costs T_setup(N) and one entry costs T_entry(N),
the direct adapter costs at most

    T_setup(N) + 4N^2 T_entry(N) + O(N^2)

field operations/comparisons in the stated accounting, plus separate field
setup and representation costs. This is a usable upper-bound interface.

It is **not** a lower bound for that structured formula. The single-entry
perturbations used in the proof usually leave the Fourier or other promised
structured class, so the adversary does not apply there. A primitive root,
its exact representation, the intended field, and any required target-inverse
or feedback formula would need to be supplied and costed. Algebraic residual
compression for such a target could beat a literal entry scan; none is proved
or ruled out here. The source-bound owner history supplied to this task does
not give a more specific target formula/implementation contract to discharge.

No direction selection is performed; failure excludes only the supplied
directions. Singular endpoint masks require their own forward construction.
No O(N) application or all-length FFT result follows merely from an O(N)
supported graph solve.

## Exact checks, reproducibility and limits

Run `python3 -I check.py`. The checker imports only the fresh local adapter and
the Python standard library. It does not import, parse, or execute historical
source code. It performs:

- 480 affine systems compared with exhaustive nonzero assignments over F2,
  F3 and F5, including self-loops, zero coefficients, contradictions and pins;
- 210 fixed-route positive instances at N=3,...,9 over F2,F3,F5,F7,F241,
  plus 210 independently rescaled projective-gauge variants, with full dense
  plan reconstruction and matrix equality checks;
- 604 invertible single-entry rejecting alternatives across the zero-edge
  and nonzero-edge query witness families at N=3,...,10;
- 36 nontrivial endpoint-permutation controls of the general matching count;
- explicit wrong-route, zero-base, singular-denominator, off-support,
  field-exhaustion and singular-target-sum controls.

The fresh N=5 shift-one/shift-two off-support-pass/scale-failure analogue has
determinants -31, -242 and **-923** over Q. It is intentionally distinguished
from the historical review's route witness with determinant **-1625**, whose
complete permutation vectors are not listed in the supplied review. The
historical witness and its acceptance remain unchanged; no purported replay
of it is claimed.

The all-size lower bound is established by the displayed proof, not by these
finite controls. Operation counts test the implementation contract at bounded
sizes; they are not timing benchmarks or production certification. Historical
priority remains unassessed; the adversary argument is elementary, and no
novelty credit is claimed for it.
