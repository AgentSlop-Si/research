# ALG-070: independent acceptance of fixed-tariff complete-view caching

Review date: 18 October 2026. Exact owner: ALG-070; existing priority 12 is unchanged.

## Decision

**ACCEPT the scoped theorem and its rational reference implementation.** No
blocking mathematical correction was found. This acceptance applies to the
frozen `candidate/` snapshot, not to arbitrary later edits of the author's work
directory. The accepted candidate REPORT SHA-256 is:

`f0114ef6dba06b840f9e91515537433b9487dc8789d81a4290ecddc67eb6c185`

The exact accepted statement is:

> In the declared immutable complete-N-entry-view grammar, one equal-size slot
> per view, fixed known positive build tariffs, capacity K >= 1, and empty
> initial caches, the specified deterministic reset-credit policy satisfies
> M_online <= K M_OPT on every finite active request sequence. All legal
> offline materializations, including speculative ones, are paid. No additive
> initialization constant is required. K is the optimal deterministic
> asymptotic factor uniformly over the admitted tariff class. With common
> mandatory cost G and separately charged online scheduling E, the accepted
> total bound is G + M_online + E <= G + K M_OPT + E.

The fixed-price/equal-slot interface can stop here. This does **not** close the
broader ALG-070 owner, alter its priority, change any census, or establish a
runtime advantage for unrestricted convolution computation.

## 1. Exact material reviewed and execution history

The reviewer read the entire candidate report and its Python sources before
replaying them. The initial author directory was still changing: a subsequent
copy contained the new registration method and interleaved update control.
That change was detected, its delta was inspected, and the full replay was
repeated after inspection. The frozen candidate now includes all 13 files
listed in its final manifest plus the manifest itself. The mixed initial
snapshot is not used as acceptance evidence.

Checks performed:

- Every candidate manifest byte length, SHA-256 and Git blob SHA-1 matches.
- All three retained controlling-text bindings match their local bytes.
- The accepted uniform report is byte-identical to the task-designated
  `/workspace/shared/alg070_persistent_cache_20261018_1244/REPORT.md`.
- The prior report's exact local text was inspected as context. Its code was
  not run. No new remote-byte-fetch claim is made for either inherited report.
- The candidate standard-library code was replayed in `replay/`, preserving
  the candidate's retained logs and validation artifact. It exited zero.
- The fresh replay's result, counts, examples, code hashes and scope equal the
  retained candidate validation semantically. Only runtime metadata can differ.
- The reviewer wrote `review_checks.py` independently and ran it with Python's
  standard library. Its output and result are retained separately.

Exact successful commands, from the review directory:

    (cd replay && python -B validate.py > REPLAY_OUTPUT.txt 2>&1)
    python -B review_checks.py > REVIEW_OUTPUT.txt 2>&1

Both final commands exited 0. No external state was written by this review.
No inherited research package, downloaded package, or historical executable
was run. Candidate modules imported by the review were the inspected fresh
sources in the frozen snapshot.

## 2. Independent proof audit

Let A and O be the online and offline resident sets. Extend the online credit
c(v) by zero outside A. For fixed tariffs F_v, the proposed potential is

    Phi = (K-1) sum_(v in A) c(v)
        + K sum_(v in O) (F_v-c(v)).

The invariant 0 <= c(v) <= F_v makes every term nonnegative. Empty caches give
Phi_initial = 0, without dummy free loads or an additive startup reserve.

Freeze O after its service of the current request x, then analyze the online
service. This guarantees x in O, including when O prefetched x earlier.
All actual O actions between successive service instants remain in the
analysis. Release constraints are respected by each original schedule; the
interleaving compares states rather than relocating actions in physical time.

The complete amortized audit is:

1. Removing v from O changes Phi by -K(F_v-c(v)) <= 0.
2. A paid load of v into O changes Phi by K(F_v-c(v)) <= K F_v.
   This is equally true for speculation. Redundant resident rebuilds add
   positive offline cost and do not hurt the bound.
3. On a full online miss, |A|=K and x is in O minus A. Hence
   |A intersect O| <= K-1. Decreasing every resident credit by delta changes
   Phi by -K(K-1)delta + K|A intersect O|delta <= 0.
4. Evicting a zero-credit online view changes Phi by zero. A zero minimum
   still permits eviction, so there is no zero-credit infinite loop.
5. Loading x and setting its credit to F_x changes Phi by
   (K-1)F_x-KF_x=-F_x, paying its entire online build.
6. Raising a hit's credit by eta >= 0 changes Phi by -eta <= 0.

Therefore Phi_final + M_online <= K M_O for **every** legal finite offline
schedule O. Nonnegativity yields the claimed inequality, also against an
infimum if necessary. Filling a nonfull cache is already covered by item 5.
K=1, empty sequences, restored old handles, unused zero-credit residents and
online registration cause no exceptional additive term.

This proof does not require a lazy offline comparator. It also does not use
the finite validation oracle to establish an arbitrary-sequence theorem.

## 3. Comparator and convolution realization audit

The inherited and extended contracts agree on exact commutative-ring
arithmetic, immutable paid raw backing, normalized recipe/operand-version
handles, complete N-entry materializations and external output streaming.
Zero-output requests have no active cache service but retain their mandatory
front-end charge. Duplicate coordinates still pay their output work.

The proof is conditional on that exact grammar. Partial vectors, cached
emitted coordinates, compressed representations, persistent derived scalar
summaries, cross-view common subexpressions and cheaper alternate recipes
cannot silently enter the comparator. Scratch must not survive as an extra
usable view. Ordinary raw backing and the registry remain explicitly paid.

The source's static lower-bound family is valid. With
A=(N+1,1,...,1) and B=e_0, convolution by A sends h to

    N h + (sum_i h_i) 1.

Over Q this has eigenvalues N and 2N and is invertible. Consequently K+1
distinct dense rational kernels produce K+1 distinct complete filtered-
bilinear views. The prescribed identical double-convolution recipe supplies
an equal-price subclass inside the declared tariff class. This is an actual
family in the owner grammar, not an arbitrary metric service-cost instance.

For any deterministic K-slot policy, requesting a currently absent member of
this family forces a paid build per request. Finite speculation only adds
cost; infinite pre-service work is not legal service. Greedy maximal phases
with at most K labels each have at least K requests except possibly the last.
Their label sets extend to K-subsets of a K+1-element universe. Holding the
first set costs at most K builds, and each phase change costs at most one.
Thus a legal paid offline schedule uses at most

    K + floor((T-1)/K)

builds. This proves the asymptotic factor obstruction, including a possible
sequence-independent additive constant in a proposed smaller-factor bound.

**Scope is correct:** sharpness is uniform over the admitted tariff class,
whose equal-price subclass suffices. The artifact does not claim that every
specified strictly unequal vector of prices forces K, or that an arbitrary
algebraic evaluator is subject to this cache lower bound. The adversary is
deterministic/adaptive; no randomized oblivious-adversary conclusion follows.

## 4. Charged ledger audit and qualifications

### Common and optional costs

G is prescribed to be identical across schedules. It includes raw/update
ingestion, exact coalescing and version comparison, registry work, backing
writes, tariff/root/coefficient preparation and all required output work.
If calibration is policy-dependent, its extra online work must instead be
charged in E or a separate preparation term. This is stated correctly.

The accepted full-cost consequence is

    G + M_online + E <= G + K M_OPT + E.

It does not turn E into free work or assert a pure K wall-clock ratio. If
offline bookkeeping is also counted, its total cost only becomes larger for
the upper comparison. For the static equal-price lower-bound sequence with
G=G0+gT, the front-end-plus-build obstruction approaches

    (F+g)/(F/K+g).

That expression is below K when g>0. The source correctly separates this
end-to-end statement from optional-build sharpness.

### Scheduling and rational arithmetic

A deterministic resident scan gives O(KT) handle/credit operations and O(K)
resident records. The Python reference uses a small dictionary; the report
does not incorrectly use its hash-table behavior to prove a bit bound.
For rational tariffs, integer scaling by a paid common denominator gives
bounded credit magnitude. Every Fraction credit remains in the integer span
of tariff fractions, so its reduced denominator divides that common
denominator and its size does not grow with request count alone. The stated
coarse cubic school-arithmetic bounds are safe. The growing cost accumulator
is separately acknowledged and is not needed by the decisions.

Arbitrary exact ordered reals belong to the abstract theorem only. Rational
code and the reported bit ledger do not establish an effective implementation
for arbitrary interval-described reals. Fixed tariffs themselves must be
valid charges on both sides; an online runtime upper estimate alone cannot
be substituted for the comparator's actual runtime. Both limits are explicit.

### Concrete recipe accounting

For each direct convolution the counter convention sums two index operations,
three scalar reads, multiplication, addition and output write per index pair,
then N initialization writes and one logical workspace release. This gives
8N^2+N+1. A chain with d kernels uses d+1 convolutions, a 2N final copy and
three slot/validity operations, agreeing with the declared formula.

The fixture counters are an abstract tariff/accounting witness, not a trace
of every Python allocation, pointer operation, deallocation or wall-clock
cycle. The claimed 2N+1 scratch scalar budget is achievable by the stipulated
streamed array recipe and slot reuse; the test harness intentionally also
holds expected answers and offline state tables. Those are not production
cache memory. Physical secure erasure would require an additional charge.

The proof and executable policy assume validated registered handles from the
paid front end. The reference is not offered as a hardened API for malformed
or hostile handles. This is a nonblocking implementation qualification, not
a change to the accepted mathematical contract.

## 5. Independent fresh controls

The review oracle uses global states (request index, cache bitmask). Primitive
edges either load one available view at its full tariff, discard one view at
zero cost, or advance the request index when the requested complete view is
present. Dijkstra's exact rational shortest path starts from (0, empty).
It therefore permits paid arbitrary speculation without importing the
candidate's subset-transition formula or credit logic. Zero-output services
and monotone time-indexed registration availability are supported directly.

The independent online implementation uses arrays of handles and scaled
integer credits, then cross-checks every step against the inspected candidate
Fraction implementation. Additional exact per-action potential checks use
different prices and a finer credit grid than the candidate's controls.

All final controls passed:

- 4,368 exhaustive sequence comparisons against the independent global oracle.
- 22,752 exact integer-credit/reference-policy step matches.
- 180 seeded release/registration and zero-output traces.
- Two explicit paid-prefetch checks.
- 12,208 online-service, 12,208 offline-load and 12,208 offline-eviction
  potential transitions.
- 20 fresh invertible-convolution realizations.
- 12 fresh exact chain-recipe/counter checks at N=1,2,4,7 and d=1,2,3.
- Nine fresh deterministic-adversary phase schedules, capacities 1 through 9.
- The full candidate test suite replayed and matched its retained semantic
  results, including immutable repricing rejection and interleaved old-version
  restore-as-hit evidence.

These finite results check implementation, transcription and accounting. The
proof audit establishes the unbounded theorem and its correct lower-bound
scope; neither elapsed runtime nor finite ratios are used as that proof.

## 6. Attribution independently checked

The author's primary sources were independently opened during this review.
[Young's survey](https://www.cs.ucr.edu/~neal/publication/Young16Paging.pdf),
printed pages 2-3, explicitly presents the weighted-credit algorithm and
the same general-capacity potential. The algorithm, potential and factor
are classical GreedyDual/Landlord ingredients.

[Young's 1994 paper](https://www.cs.ucr.edu/~neal/publication/Young94KServer.pdf)
confirms its SODA 1991 precursor and weighted-caching analysis. Its older
eviction-cost/free-initial-placement conventions explain why a bare citation
would not replace the candidate's paid-empty-start proof.

[The author's Landlord bibliography](https://www.cs.ucr.edu/~neal/Young02Online)
confirms the 2002 publication, SODA 1998 precursor and independent Cao-Irani
work. The candidate's original-contribution language is appropriately limited
to the owner-specific mapping, charged conventions and fresh checks.

The Sleator-Tarjan citation was already bound by the accepted uniform report;
this review does not claim a fresh inspection of that PDF. The lower bound is
fully proved in the candidate and independently audited above.

## 7. Final disposition

Accept this exact fixed-positive-tariff, immutable complete-view, equal-slot
comparison and stop the selected interface. Preserve the broader owner's
open status and priority 12. Partial/compressed representations, shared
intermediates, changing/state-dependent tariffs or capacity, cost learning,
unrestricted algebraic evaluation, numerical certification and production
performance remain outside the accepted result. No automatic new task,
external write, owner closure or census change is authorized by this review.
