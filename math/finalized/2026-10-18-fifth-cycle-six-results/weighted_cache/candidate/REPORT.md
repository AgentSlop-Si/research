# ALG-070: fixed weighted complete-view caching

Date: 18 October 2026. Owner: ALG-070. Current priority: 12.

## Terminal result and scope

The fixed-price extension of the immutable complete-view contract is resolved:

1. With one equal-size slot per complete view, known fixed positive tariffs
   `F_v`, capacity `K >= 1`, and initially empty caches, deterministic
   credit-reset weighted caching satisfies, on every finite request sequence,

       M_online <= K M_OPT,
       M_S = sum over all materializations by S of F_v.

   There is no additive initialization term. The comparator may materialize
   speculatively, discard views, and return to old versions; all builds are paid.
2. `K` is the optimal deterministic asymptotic factor uniformly over this
   tariff class. The equal-price convolution subclass already forces it.
   This is not a claim of sharpness for every particular fixed tariff vector.
3. With the identical mandatory front-end/output charge `G` and separately
   counted online scheduler charge `E`,

       Total_online <= G + K M_OPT + E
                    <= K (G + M_OPT) + E.

   The optional-build ratio and the full-cost ratio are distinct. For the
   static equal-price adversary with common per-request cost `g`, the
   full-cost lower obstruction is `(F+g)/(F/K+g)`, not invariably `K`.
4. Fresh rational-arithmetic tests pass against two independently implemented
   offline formulations, with actual convolution recipes and mutation controls.

This is a self-contained specialization of classical GreedyDual/Landlord
weighted caching, not a new online-caching theorem. It settles only the
fixed-weight, equal-slot, immutable complete-view slice. No external record,
owner status, priority, identity, or census was changed. Independent review
of this artifact remains a separate acceptance step.

## 1. Controlling sources and retained contract

The task is item 2 in `source/TASK_PLAN.md`. The controlling accepted uniform
report is retained verbatim as `source/ACCEPTED_UNIFORM_REPORT.md` and pinned at:

https://github.com/AgentSlop-Si/research/blob/320f4691d6e72abcabfb4d50593a91f1e87eb33d/math/finalized/2026-10-18-six-result-cycle-1252/persistent_cache/candidate/REPORT.md

The prior event-list report is also retained, without executing its code.
Exact SHA-256 and Git-blob hashes of these local source bytes are supplied in
`SOURCE_BINDING.json`. The task explicitly designated the local accepted
uniform report as an available controlling source. No claim of a new remote
byte-for-byte fetch is made.

Keep the accepted report's exact commutative-ring setting, length `N`, paid
immutable raw-version backing store, registered recipes, output semantics,
and exclusions. A view handle includes its recipe identity and exact normalized
operand versions. Every active query must be served from its complete
`N`-entry materialization. A query with zero requested coordinates does not
activate a cache request, but still pays its ingestion and any mandatory
normalization. Duplicate coordinates pay their output charges normally.

The sole price change is that a view `v` has its own fixed tariff `F_v > 0`,
instead of one common `F`. The following details are essential:

- `F_v` is known/certified before the policy needs it and never changes with
  time, cache contents, observed runtimes, or build count. Both schedules pay
  that same tariff on each materialization, including prefetches and rebuilds.
  It includes the prescribed recipe's input accesses, arithmetic, scratch
  initialization/release, validity checks, slot replacement, and all `N`
  output writes. No outside disposal fee is silently omitted.
- A tariff is the comparator's declared charge. An upper bound on online
  runtime alone does not give a ratio against a comparator charged its
  possibly much smaller actual runtime.
- There are at most `K` retained complete views, each using one slot.
  Temporary build scratch has an independently declared bound `S` and cannot
  persist as another usable view. Partial vectors, saved emitted coordinates,
  compressed substitutes, derived persistent scalar summaries, cross-view
  common subexpressions, and alternate cheaper recipes are outside this
  comparator. Raw backing data is allowed and paid.
- The prescribed common front end ingests updates, coalesces equal-position
  deltas by exact addition, identifies old versions by a charged exact rule,
  registers new raw versions/recipes, obtains/certifies tariffs, and performs
  required output work. Its total charge is `G >= 0`, identical for both
  schedules. A scan of retained raw arrays is a valid exact version rule;
  neither hash collision nor a display name establishes equality.
- Both complete-view caches start empty. The offline schedule knows future
  requests but has the same capacity, raw recipes, release/registration
  constraints, scratch budget, front end, and tariffs. It may load any
  available view speculatively, paying its full tariff. A legal service uses
  finitely many operations; an infinite pre-service computation is not a
  feasible way to answer the request.

For a finite sequence, one may restrict attention to the finitely many
registered views/actions used by a legal schedule. The proof does not require
a fixed finite universe known to the online policy. A newly registered view
can receive a fresh handle and tariff through the paid front end.

The mathematical tariff theorem allows positive real numbers in an exact
ordered-arithmetic model. A finite exact implementation additionally needs
an effective representation supporting comparison and subtraction. The
delivered implementation and bit ledger cover exact positive rationals.
An interval enclosure of an arbitrary real is not by itself an exact
comparison/equality oracle, and no such oracle is assumed free.

## 2. Deterministic policy

Maintain a credit `c(v)` for each resident view and define `c(v)=0` for absent
views. Always `0 <= c(v) <= F_v`. Fix a total order on normalized handles for
tie-breaking. On an active request for `x`:

1. If `x` is resident, serve the requested coordinates and reset `c(x)=F_x`.
   Resetting bookkeeping credit does not rebuild any data.
2. Otherwise, if all `K` slots are occupied, let

       delta = min { c(v) : v is resident }.

   Subtract `delta` from every resident credit. Evict the least ordered
   zero-credit handle. At least one exists. If `delta=0`, eviction still
   occurs; there is no loop that stalls on zero credit.
3. Materialize the complete requested view into the available slot, pay
   `F_x`, set `c(x)=F_x`, and serve its coordinates.

Only one eviction is needed, because every view has size one slot. Other
zero-credit views may remain and may be hit later; a hit restores their
credit without a build. The policy performs no speculative builds. It
requires no prediction, price learning, or future version identity.

`weighted_cache.py` is fresh reference source for this policy. It accepts
paid dense integer registry handles and exact rational tariffs. Its cache
state is bounded by `K`; it does not keep an unbounded history of old
credits, output vectors, actions, or requests. A total-cost accumulator and
build counter are validation/accounting metadata, not extra materializations.

## 3. Arbitrary-sequence comparison, with full proof

Fix any legal offline schedule `O`, not necessarily optimal. Interleave its
actions with the online policy as follows: before the online response to
request `x`, execute `O`'s actions through its service of `x`; then execute
the online response while freezing `O`'s cache at that service instant.
Execute any later offline evictions/speculation before the next such
response. This is an analytical interleaving of separate executions, not
an instruction to violate input-release times or to share data.

All actual offline loads, whether requested or speculative, are counted.
At each frozen service instant, `x` belongs to `O`. Any legal offline
replacement can be split into an eviction followed by a paid load. Terminal
offline speculation can be dropped without harming service, or included:
its charged bound below still holds.

Let `A` and `O` be their current resident-handle sets. Use the classical
credit potential, here specialized to equal capacities:

    Phi = (K-1) sum_(v in A) c(v)
        + K sum_(v in O) [F_v - c(v)].                 (1)

Every summand is nonnegative. Initially both sets are empty, so `Phi=0`.
We verify every action explicitly.

### Offline eviction

Removing `v` from `O` removes `K(F_v-c(v)) >= 0` from the potential. Thus
the potential cannot increase. No derived information is retained outside
the stipulated backing store/cache when a view is evicted.

### Offline load, including a speculative load

Adding absent `v` to `O` changes the potential by

    K(F_v-c(v)) <= K F_v.                              (2)

Its paid charge is `F_v`. If a schedule redundantly rebuilds a resident
view, its cache set is unchanged and it pays a nonnegative extra charge;
the bound is only easier. The proof therefore does not need a laziness
assumption or a free-prefetch normalization of the offline schedule.

### Online credit decrease on a full miss

Immediately before this decrease, `|A|=K` and the requested `x` is in `O`
but absent from `A`. Hence `|A intersect O| <= K-1`. Subtracting `delta`
from all credits in `A` changes (1) by exactly

    -(K-1) K delta + K |A intersect O| delta <= 0.     (3)

For `K=1`, the intersection is empty and this remains valid. The minimum
choice ensures all credits remain nonnegative; no nonexistent negative
credit is used to finance a build.

### Online eviction

The evicted credit is zero. Its contribution to the first sum is zero,
and its extended credit remains zero after eviction. Consequently (1)
does not change even if the evicted handle belongs to `O`.

### Online requested materialization

Before insertion, `c(x)=0`; after insertion, `c(x)=F_x`. Since `x in O`,
the potential changes by exactly

    (K-1) F_x - K F_x = -F_x.                        (4)

This pays for the online charge `F_x`. Equation (4) also applies while
the online cache is still filling, so the first requests are fully charged
and no initial-capacity additive constant is needed.

### Online hit/credit reset

Let `eta=F_x-c(x) >= 0`. Raising the requested credit by `eta` changes
the potential by `(K-1)eta-K eta=-eta <= 0`, because `x in O`. Reading
and emitting its coordinates is in the common charge `G`, not a free
optional service.

These are all actions. Summing their changes yields

    Phi_final + M_A <= K M_O.                        (5)

Since `Phi_final >= 0`, `M_A <= K M_O`. Taking the minimum over all legal
offline schedules proves the stated bound against `M_OPT`. If a minimum
is not attained in some enlarged formal universe, the inequality against
every legal schedule also implies it against the infimum.

The zero-request sequence has both optional costs zero. Arbitrary repeated
handles, genuine cancellations, returns to an old version, new registrations,
and any nonnegative common front-end charge cause no change to the proof:
they only determine the exact normalized handle sequence and availability
of legal offline loads. QED.

## 4. Sharpness in this actual convolution grammar

The tariff class includes the equal-price case. Fix `K+1` registered static
views over `Q`, with `N>=2`, `B=e_0`, and

    A = (N+1, 1, ..., 1),   V_i = (A*B)*H_i.

Choose any `K+1` distinct dense rational kernels `H_i`. Cyclic convolution
by `A` has matrix `N I + J`, with eigenvalues `N` on the sum-zero subspace
and `2N` on the constant subspace, so it is invertible. Therefore the
complete `V_i` are distinct. Prescribe the same direct two-convolution
recipe for each view; its tariff `F` includes all input, scratch, slot,
validation, and scalar operations. These are genuine filtered-bilinear
requests, not unproved arbitrary metrical-task service vectors.

For any deterministic online policy with `K` slots, after each finite
completed response and any speculation, request an absent view from this
`K+1`-view family. It must pay at least `F` for each of `T` requests,
in addition to any speculative cost. Thus `M_A >= FT`.

Partition the resulting fixed sequence greedily into maximal contiguous
phases with at most `K` distinct labels. Every completed phase contains
`K` distinct labels and has length at least `K`. Extend the final phase's
set, if necessary, to a `K`-set within the `K+1` universe. Any two such
`K`-sets differ by at most one label. An offline schedule can therefore
load the first phase's set at cost at most `KF`, then replace at most one
view at each boundary. All such prefetches are real, paid, legal complete
materializations. If there are `P` phases,

    M_OPT <= F[K+P-1] <= F[K+floor((T-1)/K)].         (6)

The initial `K` loads in this upper certificate are charged even when
some are speculative. Equations (6) and `M_A>=FT` rule out any constant
`c<K` in `M_A <= c M_OPT + b` with `b` independent of sequence length.
This includes `K=1`, where the optimal factor is one. An adaptive
adversary supplies a worst-case sequence for each deterministic policy;
no randomized-oblivious-adversary statement is being asserted.

This proves optimality uniformly over the declared tariff class, not
that every strictly unequal fixed price vector or every small view
universe forces `K`. Nor is it a lower bound for arbitrary convolution
algorithms: direct coefficient computation, algebraic shortcuts,
cross-view sharing, and compressed answers are deliberately outside
the complete-view comparator.

## 5. Fully charged time and storage ledger

### 5.1 Front end and builds

For a raw event stream, let `G` include all of the following, as actually
required by the prescribed interface:

- cold input and recipe ingestion; exact ring/coordinate validation;
- update ingestion and exact coalescing, including updates that later cancel;
- exact comparisons/canonicalization of retained raw versions and recipe
  tuples, and all metadata/dictionary work used for those operations;
- writes and maintenance of genuinely new immutable raw versions;
- tariff acquisition/certification, root or coefficient preparation, and
  any common calibration;
- every query's coordinate list and handle ingestion, including zero-output
  queries; each coordinate read/emission, including duplicates.

Then the declared total tariff is exactly `G+sum_builds F_v`; adding
separately paid policy work gives `G+sum_builds F_v+E`. If `O` is charged
its own scheduler work too, the comparator total can only increase.
Unshared online calibration belongs in `E` (or a separately written
online-only preparation term), never in a fictitious common `G`.

From (5), with `D=G+M_OPT>0`,

    (G+M_A+E)/D <= 1 + (K-1) M_OPT/D + E/D.          (7)

The coarser `K+E/D` bound is valid, but (7) shows how common output or
normalization work reduces the optional-work ratio's end-to-end effect.

For the static adversary above, choose a fixed prescribed common cost
`G=G0+gT`. The comparison schedule in (6) gives

    (G+M_A)/(G+M_OPT)
      >= [G0+(g+F)T] /
         [G0+gT+F(K+floor((T-1)/K))].              (8)

The limit inferior is at least `(F+g)/(F/K+g)`. If `g>0`, this is below
`K`; it approaches `K` as `F/g` grows. This statement concerns the
declared front-end-plus-build tariffs. Arbitrary unbounded comparator
bookkeeping is not smuggled into the denominator or asserted free in
a measured wall-clock comparison. Online scheduler cost remains explicit.

### 5.2 Scheduler work and bit qualification

Let `T` be the number of active view requests. A linear-scan resident table
performs at most `O(K)` handle comparisons, credit comparisons/subtractions,
and metadata writes per request. A miss uses one minimum scan, one credit
decrease scan, and one zero-credit tie scan; a hit resets one credit.
Thus `E=O(KT)` ordered-arithmetic/handle operations, with `O(K)` resident
records. A dense normalized handle addresses its tariff in a charged
registry array. Unbounded-key dictionary operations are not assumed
constant-time for free.

The reference Python code uses a dictionary of at most `K` resident entries
and a dense tariff array. Its correctness is the delivered executable
claim; no interpreter-level wall-clock constant or bit-runtime ratio is
deduced from these source-level counts. Replacing the resident dictionary
by explicit linear scans gives the stated deterministic operation bound
without relying on hash distribution. The code's accounting accumulator
requires `O(log T)` additional value bits; it is not used to make decisions.

For `m` certified rational tariffs `a_v/b_v`, choose

    D = lcm_v b_v,  W_v = D a_v/b_v,
    B = 1 + ceil(log2(1+max_v W_v)).

One may implement all credits as integers in `[0,W_v]`. LCM/scaling and
reading the `m` tariffs are charged preparation, rather than free
conversion. With school arithmetic, `O(m B0^3)` bit operations is a safe
coarse preprocessing bound when `B0` bounds all intermediate bit lengths
(for example the sum of denominator bit lengths plus the maximum
numerator bit length and `O(log m)`). Resident arithmetic then costs
`O(KT[B+log(m+1)])` bit operations using direct integer comparisons and
subtractions, plus any chosen `O(T[B+log(T+1)])` cost accumulator.

The delivered Fraction implementation does not pre-scale. Each credit's
reduced denominator divides `D` because credits arise from tariffs by
subtraction and reset; its magnitude stays between zero and `F_v`.
Consequently numerator/denominator lengths are bounded by tariff data,
not by the number of requests. A conservative school-arithmetic bound
for its exact comparisons, reductions, and subtractions is `O(B0^3)`
per arithmetic operation, hence `O(KT B0^3)` plus accounting. Maintaining
the Fraction-valued test accumulator adds the safe coarse bound
`O(T[B0+log(T+1)]^3)`; production decisions need no such accumulator.
If new tariffs are registered online, use the same prefix bound for the
tariffs seen so far; common-denominator rescaling, if chosen, must be
charged when it occurs. No bounded-denominator assumption is hidden.

These scheduler bit bounds do not turn arbitrary ring-element operations
into unit bit costs. Bit costs of exact large-integer/rational convolution,
root computation, numerical certification, and data-dependent builds
must already be validly included in their tariffs/preparation if a bit
model is claimed. This artifact proves no measured speedup.

### 5.3 Space

Count `R_back` scalar/raw-version storage and all recipe/tariff registry
bits, at most `KN` retained view scalars, `S` temporary build scalars,
and `O(K)` resident handles/credits separately. With rational credit
encoding these records require `O(K[B0+log(m+1)])` bits, apart from
scalar storage. Requested output is an external stream; retaining it
internally would be another charged representation and is excluded.
Validation oracles hold exponential state tables only in the separate
test harness, never as hidden online state.

### 5.4 Concrete instrumented convolution recipes

The fresh validation builds immutable recipes

    A * B * H_0 * ... * H_(d-1),  d in {1,2,3},

using `d+1` direct cyclic convolutions. One direct convolution's declared
primitive count is `8N^2+N+1`: for each pair of indices, two index
operations, three scalar reads, one multiply, one add, and one output
write; also `N` zero-initializing writes and one workspace-release
operation. The final copy costs `2N` reads/writes, with three slot/validity
metadata operations. Its fixed unequal tariff is

    F_v = (d+1)(8N^2+N+1) + 2N + 3.                (9)

The measured abstract operation counters equal (9) on every tested
build. Intermediate vectors are not retained as reusable views; a
builder can use `2N+1` scratch scalars and overwrite the freed slot.
The release operation means the old temporary is no longer available
to the evaluator, not that physical memory zeroization is costless.
If a deployment requires physical clearing/security erasure, its writes
must be added to (9). Python object overhead is not claimed to equal
this ring/array tariff.

Front-end ledgers in `VALIDATION.json` separately count exact raw-version
scans, cancel/restore handling, registry work, backing writes, tariff
preparation, query ingestion, and duplicate-coordinate output. They are
recomputed independently of the cache schedule. All returned old-version
hits still pay these front-end costs.

## 6. Fresh finite oracle and controls

No inherited research module or untrusted package was executed. The three
new source files use only Python's standard library and one another.

`offline_oracle.py` independently enumerates all subsets of the finite
registered view universe with size at most `K`. If `C` is the cache at
one service instant and `D` is the cache at the next, the minimum legal
between-service materialization charge is

    w(C,D) = sum_(v in D minus C) F_v.               (10)

Every such missing view must be built at least once. Conversely, evict
`C minus D`, then load `D minus C`; this stays within capacity and
attains (10). Intermediate prefetch/rebuild paths cannot cost less.
The DP starts at the empty set. At request `x`, it minimizes
`DP(C)+w(C,D)` over every state `D` containing `x`. Other members of
`D` may be unrequested prefetched views, and all are charged. Optional
availability sets forbid prematurely materializing unregistered views.

This oracle is not Belady's equal-price eviction rule and does not reuse
the online credit update. A second implementation computes shortest-path
closure using only individual zero-cost evictions and paid load actions,
then filters to caches containing the requested view. It uses neither
(10) nor the first oracle's transition matrix. Their exact agreement is
a separate finite check of the comparator semantics.

Fresh final run (`python -B validate.py`, exit status 0) records:

- 39,360 exhaustive sequence-prefix comparisons over three handles,
  lengths zero through seven, capacities one through three, and four
  tariff vectors, including unequal fractions and a 100:1 price contrast;
- 363 exact agreements between the two offline oracles;
- 6,024 online-service, 6,024 offline-load, and 6,024 offline-eviction
  potential checks, including nonfull caches, zero credits, and arbitrary
  offline cache membership;
- 120 seeded length-60 unequal-rational random traces and eight length-400
  equal-price adversarial phase certificates for capacities one to eight;
- 387 exact convolution queries at lengths 2, 3, and 5, 351 actual recipe
  builds, three cancel/restore identity checks, and 45 paid zero-output
  queries; duplicate coordinates and restored old handles are exercised;
- one additional interleaved update/query/restore trace keeps actual views
  resident while the front end registers a changed version, then returns
  to the old handle with a paid exact scan and a cache hit. An attempted
  change to an existing handle's fixed tariff is rejected;
- eight rejected mutations applied to actual arrays/ledgers: free
  speculation, unit-price substitution, omitted final copy, omitted
  initialization, an extra retained scratch view, partial-as-complete
  output, display-name aliasing of unequal versions, and omitted exact
  return-to-old-version scans;
- a substantive price-oblivious LRU counterexample: capacity two,
  tariffs `(100,1,1)`, sequence `(0,1,2)` repeated 20 times. LRU costs
  2,040, the legal offline optimum costs 139, and the credit policy
  costs 140. Thus simply retaining uniform-price LRU is not sufficient.

The JSON preserves all counts, the actual ledger categories, mutation
evidence, the bad-policy witness, runtime metadata, and source hashes.
`REPLAY_OUTPUT.txt` preserves the fresh test log. These tests detect
transcription, implementation, and accounting mistakes; Sections 3–4,
not finite enumeration or elapsed runtime, prove the unbounded claims.

## 7. Accurate classical attribution

- Neal E. Young, *The k-server dual and loose competitiveness for paging*,
  Algorithmica 11(6), 525–541 (1994), journal version of SODA 1991,
  introduces/analyzes GreedyDual for weighted caching. The author-hosted
  original paper was inspected. Its older cost/initialization conventions
  are not silently substituted for this owner's paid empty start.
  https://www.cs.ucr.edu/~neal/publication/Young94KServer.pdf
- Young, *On-line file caching*, Algorithmica 33(3), 371–383 (2002),
  with SODA 1998 precursor, develops Landlord for costs and file sizes.
  The author's bibliographic page also credits independent work by
  Pei Cao and Sandy Irani. This artifact only uses the equal-size case.
  https://www.cs.ucr.edu/~neal/Young02Online
- Young's author-hosted *Online paging and caching*, page 2 (algorithm)
  and page 3, Theorem 1, explicitly gives the credit formulation and
  potential used here. The potential is classical, not an original
  discovery in this supplement.
  https://www.cs.ucr.edu/~neal/publication/Young16Paging.pdf
- Daniel D. Sleator and Robert E. Tarjan, *Amortized Efficiency of List
  Update and Paging Rules*, CACM 28(2), 202–208 (1985), is the classical
  deterministic paging lower-bound/competitive-analysis source retained
  by the accepted uniform report. The fresh fetch of its author-hosted
  PDF timed out in this pass; the prior report's verified citation is
  retained, and the lower argument above is supplied in full.
  https://www.cs.cmu.edu/~sleator/papers/amortized-efficiency.pdf

The contribution here is the exact owner-contract mapping, complete paid
prefetch/initialization treatment, convolution realization, and reproducible
fresh checks. Neither the algorithm, the potential, nor the factor is new
weighted-caching mathematics.

## 8. Disposition

Terminal scoped theorem: fixed positive unequal tariffs now have a proved,
sharp deterministic complete-view comparison with the same paid
cancellation/version front end. This removes the nonuniform-price boundary
listed by the accepted uniform-price report.

It does not close ALG-070's broader representation/comparator program.
Partial/compressed views, shared intermediates, state-dependent conversion
prices, changing capacity, cost learning, unrestricted algebraic evaluation,
and numerical/production qualification remain outside this theorem. They
are boundary statements, not automatically dispatched new tasks. Stop this
fixed-price/equal-slot interface here after independent acceptance.
