# ALG-070: a paid persistent complete-view cache boundary

Date: 18 October 2026. Existing owner: ALG-070. Author-side mathematical continuation; external independent review pending. No owner status, priority, identity, or census change is proposed by this artifact.

## Result

The following precisely restricted extension of the accepted fixed-filter/event-list model is resolved:

* A persistent cache of K complete, equally priced convolution views admits deterministic LRU with optional-materialization cost at most K times the optimum with the same capacity and initially empty cache.
* No deterministic online policy has a uniform smaller asymptotic factor than K for that exact complete-view grammar. The lower bound is realized by actual filtered-bilinear convolution requests, not arbitrary unrealized metrical task-system cost vectors.
* With K slots against an optimum with h<=K slots, LRU has factor K/(K-h+1). In particular, 2h-1 slots suffice for factor below two (equal to one when h=1).
* Common ingestion, exact coalescing/version normalization, calibration, backing storage, and output work are retained. Extra scheduler work is an explicit additive term. If common cost is g per request, the equal-capacity adversary gives full-cost asymptotic lower bound (F+g)/(F/K+g), rather than incorrectly claiming K regardless of output cost.

These are applications of classical paging mathematics to a newly explicit owner-specific comparator. They are not new paging theorems, arithmetic lower bounds, claims about optimal unrestricted convolution algorithms, or closure of ALG-070's full comparator gate.

## 1. Source binding and what changes

The current 229-open-record index identifies ALG-070 at overview row 297, priority 12, as open. Its next mathematical task asks for a larger comparator with cancellation/coalescing, multiple cached kernels, downstream variable products, persistent memory, paid conversions, and cost learning. The preceding report is pinned at:

https://github.com/AgentSlop-Si/research/blob/22e4fbdff0dd655d4cac7408964142fd2476686d/math/finalized/2026-10-16-mathematical-development-1221/alg070/REPORT.md

Git blob: 0886460afffb4509934c6f1511c077b2e8982c7c. The exact fetched body is retained in source/ALG070_PRIOR_REPORT.md. Sections 2–4 prove a factor-two event-list reset theorem which explicitly excludes cancellation-aware coalescing, retained alternative kernels, and different representations. Section 6 only conditionally maps a complete metric-state model to MTS and warns that its arbitrary service vectors must not be treated as a realized Fourier lower bound. Section 9 leaves the wider comparator open.

This continuation chooses the complete-view caching slice. It does not repeat that event-list theorem or claim that the remaining broad comparator has now been solved. The new deliverable is a verified realization, a matching equal-capacity bound, a resource-augmentation remedy, and an exact accounting boundary.

## 2. Explicit complete-view contract

Fix a commutative ring R with exact operations, length N>=1, and positive integer cache capacities. A view is an immutable, registered recipe producing a vector in R[C_N]. Examples include (A*B)*H_i, a finite convolution product of changing operands followed by a kernel, or a finite exact convolution expression DAG. Every input version and its recipe remain accessible in a paid immutable backing store.

A request consists of an immutable recipe handle v_t and a list of q_t coordinates. A handle identifies the registered recipe plus exact normalized input versions, not merely its display name. Requests with q_t=0 need not activate a view; remove them from the cache-request sequence while charging their ingestion. Every other request must be served from the complete N-entry materialization of its handle. Emitted output is not rereadable as free internal storage.

The following are part of this selected comparator, not facts automatically true of every implementation:

1. Each materialization uses a known exact recipe with the same declared tariff F>0. F includes its arithmetic, input accesses, scratch initialization, validation, full N-entry writes, and replacing the old slot. It may overwrite an evicted slot. There is no free rebuild, table, conversion, or admission. The theorem is a tariff theorem, not a measured runtime ratio.
2. At most K complete materialized vectors persist. Persistent derived scalar summaries, partial output caches, compressed substitutes, cross-view common-subexpression caches, and reuse of previously emitted outputs are outside this grammar. Temporary build workspace of S scalars is separately budgeted and is cleared or made unusable between builds. A full uncounted scratch view cannot survive as an extra cache slot.
3. A cache hit pays the declared coordinate-read/output cost, but no materialization. A miss must first pay F to materialize that handle. Speculative materialization is allowed and also pays F. Discarding a slot incurs no separate tariff because cleanup is included in the next replacement; any implementation with additional disposal cost must add it explicitly.
4. Inputs, version metadata, normalization, coordinate lists, root preparation when needed, and tariff acquisition have schedule-independent common cost G. They are not assigned zero work or zero space. Persistent raw-version storage is R_back; retained complete-view storage is at most KN; scratch S and scheduler metadata are additional. The comparison fixes R_back, S, and the same allowed raw recipes on both sides.
5. Before the competitive execution begins, F and every allowed recipe are certified as valid in this tariff model. A paid common calibration/preparation term may be included in G. Unknown nonpreemptive runtime prediction, policy-dependent learning, or free estimates are not supplied by this theorem.
6. Both schedulers begin without any real materialized view. The offline comparator knows the entire request sequence but obeys exactly the same format, tariffs, common costs, and capacity. It may not use clairvoyance to obtain cheaper algebraic recipes or omit mandatory front-end work.

This contract allows arbitrary registered downstream variable products as the contents of a view, but deliberately does not exploit their internal algebra to change the cache tariff. Nonuniform rebuild prices, value-dependent conversions, partial materializations and flexible shared intermediate states remain outside it.

### Paid cancellation, coalescing and persistent versions

The front end can apply updates to each current raw operand, coalescing equal-position deltas by exact addition. On registering a version it may scan the entire operand, compare it exactly with retained versions, and reuse an old handle if equality is verified. That scan, all dictionary/key work, and storing any genuinely new raw version are charged in G and R_back. A finite expression's recipe identity and operand-version tuple can likewise be normalized by an explicitly paid deterministic rule. A sequence +delta followed by -delta can therefore return to an earlier view handle, even while the earlier materialization remains cached.

No probabilistic hash collision is declared equality. No free canonical form for arbitrary algebraic circuits is assumed. Distinct normalized recipes that happen to evaluate to the same vector remain distinct handles unless an additional paid identification procedure certifies and merges them. The bounds hold for every resulting handle sequence and every nonnegative G, so they tolerate real cancellations without relying on the event-count monotonicity used in the older theorem.

The theorem therefore covers a precise cancellation/coalescing interface, multiple cached kernels, persistent old versions, and variable-product requests. It does not cover every possible cancellation-aware algebraic evaluator.

## 3. A realization inside the owner's original convolution target

For the lower-bound realization choose R=Q and N>=2. Fix a dense A whose cyclic convolution matrix is invertible, put B=e_0, and register K+1 pairwise distinct dense kernels H_0,...,H_K. Such A exists, for example by strict diagonal dominance. The resulting complete vectors are then pairwise distinct. The corresponding views are

    V_i=(A*B)*H_i=A*H_i.

Each is literally in the preceding report's filtered-bilinear family. One valid common recipe is the full double-loop cyclic convolution, with N^2 scalar products and N(N-1) scalar additions, together with fully charged indexed reads, addressing, N writes, and scratch handling. Thus equal F is available without assuming FFT roots or numerical arithmetic. The recipe is required by the selected grammar even if a particular input has a shortcut. All kernels and A are read and stored at paid cold cost; none is an uncharged oracle.

Any sequence of paging labels i_t in {0,...,K} is realized by requesting a fixed coordinate, or all coordinates, of V_(i_t). Cache presence is exactly presence of its complete materialization. Slot replacement is an actual rebuild cost F; cache hits use the stored vector. No new operator, changed target field, or generic MTS service vector is necessary.

Important restriction: this is a realization in the explicitly stipulated complete-view recipe model. An arbitrary solver could compute a requested coefficient directly, retain a compressed answer, share work among H_i, or use another convolution algorithm. The lower bound does not apply to that larger class. Making the raw kernels available does not itself prove that those options are slow.

## 4. LRU upper bound, including unequal cache capacities

Let OPT_h be any legal offline schedule with h slots and let LRU_K have K>=h>=1 slots. Let a and o denote their numbers of complete materializations. Then

    (K-h+1) a <= K o,
    F a <= [K/(K-h+1)] F o.                 (1)

LRU_K materializes only on a miss, evicts the least recently requested resident view when necessary, and moves the requested handle to the front of its recency order. Returned old versions are treated exactly like any other handle.

### Proof

Pad initial empty caches with dummy handles that are never requested. Put OPT_h's h dummies in the most recent h positions of LRU_K; the remaining K-h dummies fill the latter cache. Keeping an otherwise discarded page until its slot is needed does not hurt any schedule, so OPT can be assumed to have exactly h entries counting dummies at all times. Intermediate speculative loads are charged individually.

For a handle v let r(v) be its LRU rank, 1 through K if resident, and K+1 if absent. Define

    Phi = sum_(v in OPT_h cache) r(v).

Although many absent handles have rank K+1, any h distinct handles have sum of ranks at least h(h+1)/2. This equals the initial Phi.

Process each offline load before the next LRU request. Replacing one offline entry by another increases Phi by at most K, since both ranks lie between 1 and K+1. Thus all offline loads contribute at most K o to the increase in potential.

At a request to v, the offline cache contains v. If LRU hits at rank j, moving v to the front decreases its contribution by j-1. At most j-1 other offline entries have their rank increased by one; all others are unchanged. Hence Delta Phi<=0.

If LRU misses, v's contribution decreases from K+1 to 1, a decrease of K. Each of at most h-1 other offline entries increases rank by at most one, including a possibly evicted least-recent entry. Thus Delta Phi<=-(K-h+1).

Summing yields

    Phi_final - Phi_initial <= K o - (K-h+1) a.

The left side is nonnegative. This proves (1), including prefetching offline schedules. No additive initial-cache term is necessary under the stipulated empty start. QED.

For h=K, LRU is K-competitive. For K=2h-1 its factor is (2h-1)/h=2-1/h. The memory increment is h-1 full N-scalar slots and their metadata; it is not free space.

## 5. Matching equal-capacity obstruction

Fix any deterministic online policy A with K slots. Supply the K+1 views from Section 3. After each completed service and any paid speculative work, request a view absent from A's retained cache. Such a view always exists. If A performs infinitely many speculative loads before servicing another request, it already has unbounded cost; otherwise the construction proceeds. Each of T requests forces at least one further materialization, so

    a_A >= T.                                (2)

This adaptive construction proves a worst-case input sequence for each fixed deterministic policy. It is not an oblivious-adversary randomized lower bound.

Partition the realized sequence greedily into maximal contiguous phases with at most K distinct labels. Every completed phase has K distinct labels; the final one may have fewer. Consecutive full phase-label sets are K-subsets of a K+1-element universe, so they differ in at most one label. Extend the final smaller set to a K-subset. An offline schedule may prefetch the first phase's set for at most K loads and, at each subsequent phase, replace at most one view to hold the next set. It then has no within-phase misses.

If P phases occur, every phase except the last has length at least K. Therefore P-1<=floor((T-1)/K), and

    OPT_K materializations <= K + floor((T-1)/K).   (3)

For K=1 this also holds. Prefetches, the initial K loads, and every conversion are charged. Equations (2)–(3) show that no c<K with any request-length-independent additive constant can bound A's materialization cost by c times OPT_K's materialization cost. Combined with Section 4, the optimal deterministic asymptotic factor is exactly K in this grammar.

The adversary does not need updates or exotic downstream products. Those richer features may be allowed by the model; its static multi-kernel subfamily already forces the boundary.

## 6. Full cost and scheduler accounting

Let G be the identical mandatory front-end, backing-store, calibration, and output cost for the realized finite sequence. Let E_A be additional policy work. Then

    Total_LRU <= [K/(K-h+1)] Total_OPT_h + E_LRU.   (4)

Here the comparator's total tariff is G+F o. If its own scheduling work is also charged, it only enlarges the right side. The factor on G is harmless because it is at least one. Policy-dependent calibration is not a common G and must instead be added to E or analyzed separately.

One deterministic implementation scans at most K resident handles on each active request, then updates a recency list. This proves E_LRU=O(K T) handle comparisons, index operations, and writes, with O(K) metadata words. It does not pretend constant-time dictionary access for unbounded keys. With certified machine-word handles and a suitable separately charged dictionary, stronger bookkeeping bounds can be substituted. Handle widths, pointer/index bits, and exact field operations are not unit bit costs.

For the lower bound take a registered static family with common cost G_0+gT, where G_0 contains all cold inputs, view recipes, and common preparation, and g is the actual declared per-request lookup/output tariff. Equations (2)–(3) imply

    Total_A / Total_OPT_K
      >= [G_0+(F+g)T] / [G_0+gT+F(K+floor((T-1)/K))].

Thus the limit inferior is at least

    (F+g)/(F/K+g).                             (5)

This is smaller than K when g>0. In particular F>=K g gives lower bound at least (K+1)/2, and F/g tending to infinity recovers K. For a fixed K and the full direct-convolution recipe, growing N makes F grow quadratically while full-vector output grows linearly, so the admissible family can meet F>=K g. For coordinate-only queries this is easier, but the complete-view restriction remains essential.

Equation (5), not an unqualified K, is the honest full-cost obstruction. With large mandatory output or version-normalization work, the end-to-end ratio can be much smaller. This result also does not make O(KT) LRU bookkeeping disappear; it gives a charged cost expression rather than an unsupported machine-speed guarantee.

## 7. Classical attribution

Sleator and Tarjan, “Amortized Efficiency of List Update and Paging Rules,” Communications of the ACM 28(2), 202–208 (1985), Section 4, Theorems 5 and 6, give the classical online paging lower bound and LRU upper bound, including different cache capacities. The author-hosted primary PDF was inspected at printed pages 207–208:

https://www.cs.cmu.edu/~sleator/papers/amortized-efficiency.pdf

The ratio K/(K-h+1), the equal-capacity K boundary, and the memory-augmentation principle are classical. The independent rank-potential and phase proofs above establish the exact empty-start and explicit-tariff variant used here. The owner-specific contribution is the fully declared convolution-view realization and its accounting limits. No historical novelty is claimed, and no generic MTS lower bound is substituted for an unrealized convolution workload.

## 8. Validation and final scope

The accompanying check_cache.py is a fresh standard-library-only verifier, not inherited research-code execution. It compares LRU to an independently enumerated finite offline dynamic program, checks the unequal-capacity inequality, verifies the greedy-phase offline upper certificate, tests paid coalescing/version returns and exact convolution answers, and checks accounting guard mutations. VALIDATION.json records 143,650 request-potential transitions; 366,028 offline-load transitions; 6,795 exhaustive request sequences with 55,618 competitive inequalities and 6,795 phase certificates; 32 length-200 adversarial traces; 1,296 exact full-vector convolution queries and 324 cancel/restore version checks; and five rejected accounting mutations. All passed. The offline Bellman oracle permits paid arbitrary-subset prefetching, rather than assuming the online policy is optimal. Empty-sequence, zero-output and one-slot controls are separate.

The proofs, rather than finite enumeration, establish the arbitrary-sequence claims. The script is not a performance benchmark, production implementation, floating-point certification, or evidence that any larger representation class obeys this lower bound.

Bounded gate disposition: the uniform-cost immutable complete-view comparator is resolved mathematically, subject to independent review. ALG-070 itself remains open. The next distinct unresolved extensions include nonuniform build prices; partial or compressed persistent answers; certified cross-view sharing; state-dependent conversion costs; changing available capacity; policy-dependent cost learning; and numerical/bit/runtime qualification. No status, score, ID, count, or external file was changed.
