# ALG-070: bounded downstream views and a competitive rebasing dispatcher

Date: 16 October 2026. Baseline: `de5dc664448d8e3e219df9651b2805d5a2cecbb1`.

## Decision

**Retain ALG-070 open, but replace its benchmark-only next-action wording.** Phase 6 §11 explicitly asks mathematical questions about bounded downstream representations and competitive dispatch. This supplement supplies a fully proved restricted answer: a compact exact view for one varying bilinear product followed by fixed convolution filters, together with a deterministic 2-competitive replay/rebase rule against a precisely delimited offline comparator. It also gives elementary counterexamples to stronger unrestricted readings and a conditional reduction of finite-mode dispatch to classical metrical task systems.

These are scoped derivations and classical online-algorithm applications, not claims of historical novelty, universal FFT improvement, or a new integer-multiplication exponent. Existing accepted Phase 6 ring identities remain unchanged. No external write, inherited program execution, numerical production validation, or timing benchmark occurred. A separate independent review has accepted the named scoped proofs; that review and its limitations must accompany any publication of acceptance.

The new work is distinct from ALG-071's shared-cut materialization, cache-rewrite selection, production executor, and real-FFT packing questions.

## 1. Source and owner binding

The complete current records were read at:

- [Catalogue A171:AF171]([private research-register link omitted])
- [novelity breakthough A209:Z209]([private research-register link omitted])
- [Research overview A297:Q297]([private research-register link omitted])

The complete three source bodies named by the owner were read at the pinned baseline. The decisive source is [Phase 6 RESEARCH §11](https://github.com/AgentSlop-Si/research/blob/de5dc664448d8e3e219df9651b2805d5a2cecbb1/math/archive/objects/0b/0bf1ba9d8091d2f5e7479783623a14b2a1e27055e93ffd6071a1e1f2cbb05a37__019_0bf1ba9d8091d2f5.md), SHA-256 `0bf1ba9d8091d2f5e7479783623a14b2a1e27055e93ffd6071a1e1f2cbb05a37`. The other two are the sparse/low-rank merger README (`ad60dca00f5e729d…`) and Phase 6 README (`ce8b2e31e08f1fb8…`). The full Phase 6 source has 11 sections; the different local package named `fft_phase6_graph_reuse` has another report and was not substituted for it.

The owner currently records accepted classical sparse/low-rank/bilinear identities, numerical validation and benchmark obligations, and prohibits free basis recognition, cache population, history, memory, subscriptions, input reading and initial transforms. Those limits are preserved. The source's two mathematical extension questions are additional to the performance obligation.

## 2. Cost model and exact downstream representation

Work in the cyclic convolution algebra R[C_N], over a commutative ring R, with random-access scalar arrays. Scalar arithmetic, indexed reads/writes and index arithmetic have stated unit costs. Bit complexity, growing integer coefficients and floating-point error require separate analyses. An exact convolution backend of cost M_R(N), scratch S_R(N), and paid root/setup cost P_R(N) may be used; do not assume an FFT exists over every R. If suitable exact roots and inverses exist, a conventional FFT gives M_R(N)=O(N log N) arithmetic operations after paid setup.

There are two current input arrays A,B. The downstream operator is convolution with a fixed dense kernel H, possibly the paid composition of a fixed chain of convolution filters. The required result is D=(A*B)*H. Queries request q specified coordinates; duplicates and q=0 are allowed. Point updates provide exact additive deltas to A or B. There is one active version; retaining old persistent versions is an extra memory obligation.

At a rebase, save three dense core arrays:

    X=A0*H,   Y=B0*H,   Z=(A0*B0)*H.

Keep current A,B,H,X,Y,Z, and two chronological event lists L_A and L_B since this rebase. Events are not coalesced, dropped because they cancel, or treated as free semantic simplifications. If L_A contains (p_i,a_i) and L_B contains (s_j,b_j), write k_A=|L_A| and k_B=|L_B|. Then every requested coefficient is exactly

    D[t] = Z[t]
         + sum_i a_i Y[t-p_i]
         + sum_j b_j X[t-s_j]
         + sum_(i,j) a_i b_j H[t-p_i-s_j],

with all indices modulo N. This follows by substituting A=A0+sum_i a_i e_(p_i), B=B0+sum_j b_j e_(s_j) and using bilinearity and shift equivariance. Repeated positions and cancellations do not affect the identity. The last sum is essential.

**Representation proposition.** With k_A+k_B<B, this view uses O(N+B+S_R(N)) working storage, including its dense cores and backend scratch, and answers q coordinates in O(q[1+k_A+k_B+k_A k_B]) arithmetic/read/write work. The pair sum is streamed, so it needs no k_A k_B-sized stored expansion. Updates to current A or B and list appends cost O(1), apart from rebases. A rebase costs a stated fixed tariff F>0 covering core recomputation, array writes, list clearing and scratch management. For 1≤B≤N, a conventional exact backend permits F=O(M_R(N)+N), including the O(B) clearing cost. Cold initialization I includes current input reads, H preparation, root preparation, and all initial cores.

The representation is also closed under another fixed convolution filter G: replace H,X,Y,Z by H*G,X*G,Y*G,Z*G and keep both event lists. This costs four dense convolutions plus G ingestion/preparation. Thus representation size remains bounded through fixed-filter composition, but the new filter application is not free or automatically sub-full-transform. A fully known chain can instead be composed during charged initialization.

**Not covered:** multiplying two already complicated varying views, arbitrary non-shift-invariant linear operators, unbounded branching, unlimited retained versions, automatic discovery of relations, or cheap reconfiguration under changing dense filters.

## 3. A 2-competitive, memory-capped reset theorem

This theorem is about the explicit event-list evaluator above, not the best arbitrary algebraic implementation.

### Model

Events are totally ordered and atomic. An event is a supplied update to A, an update to B, or a query specifying q≥0 coefficients. Both schedules start with the same paid, current cores and empty event lists. After processing each event, at most B−1 update events may remain pending, where B is a positive integer.

A rebase costs exactly F in the declared tariff and empties both lists. It can be performed after applying an update, or before answering a query. Any rebase between events can be postponed to the next event without increasing its cost or query rent, so these event-local positions suffice. Attribute every such rebase to its event, once.

At a query, an unre-based view incurs incremental rent

    r_t(k_A,k_B)=q_t(c_A k_A+c_B k_B+c_AB k_A k_B),

where c_A,c_B,c_AB are fixed nonnegative costs accounting for the corresponding streamed arithmetic and reads. The key property is coordinatewise monotonicity in pending event counts. Positive weights model the filtered bilinear formula; c_AB=0 includes an affine/single-varying-operand case. Uniform loop tariffs are compared even when an instance admits cancellation or a cheaper specialized kernel. All queries pay the same additional core/output charge g_t, and all events pay the same ingestion/accounting charge g_t. The theorem first bounds reset-plus-rent cost; Section 4 treats these common costs.

The comparator OPT_B knows the entire event sequence, uses the same F, B, initial cores, event-list semantics, query tariff and allowed reset action. It may choose any feasible reset schedule. It may not discard/coalesce events, retain additional uncharged caches, use a cheaper unlisted kernel, or choose a different representation.

### Algorithm

Maintain an accumulator R of rent actually paid since the last rebase, initially zero.

1. After each update, append it. If the total pending count reaches B, rebase immediately and set R=0.
2. At a query, calculate its current rent r. If R+r≥F, rebase before answering and set R=0; the query then has zero rent. Otherwise answer by replay and set R←R+r.

The arithmetic to calculate r and maintain counters is O(1) per event in the stated unit-cost model, separately charged below. The algorithm never pays rent R≥F between rebases.

### Theorem

For every finite event sequence and every F>0, integer B≥1 and fixed nonnegative weights,

    reset_and_rent(ALG) ≤ 2 reset_and_rent(OPT_B).

There is no additive final-epoch F term.

### Proof

Partition the event sequence into disjoint intervals ending at each ALG rebase, plus a final interval with no ALG rebase. A complete interval contains the event at its right endpoint and excludes the event at its left endpoint. Thus an offline rebase attached to an event is charged to exactly one interval.

ALG pays less than F in query rent in a complete interval and F for its concluding rebase, so its interval cost is less than 2F.

Consider any feasible offline schedule in that same interval. If it rebases at an event in the interval, its interval cost is at least F. Otherwise its latest rebase is no later than the interval's start. At every query its pending A and B event counts are therefore at least the counts ALG would have had since the start without its concluding rebase.

- If the interval ends because the rent threshold is crossed, monotonicity implies that the offline schedule's query rents in this interval are at least the previous rents ALG paid plus the triggering query's hypothetical rent, hence at least F.
- If the interval ends at the capacity threshold, it contains B updates. An offline schedule with no rebase in it would retain at least B events after the last update, violating the same B−1 cap. Thus this case necessarily has an offline rebase and cost at least F.

Consequently ALG's cost on each complete interval is at most twice the offline cost on that interval.

Let R_tail<F be ALG's rent in the final interval. If the offline schedule rebases there, its cost is at least F>R_tail. If it does not, its older pending-event prefix and monotonicity give query rent at least R_tail. Hence the final interval costs ALG no more than the offline schedule. Sum the disjoint interval inequalities and minimize over offline schedules. QED.

### Edge conditions and sharpness boundary

- B=1 means zero events may remain pending; both feasible schedules must rebase on every update. There is no hidden exception for a zero-sized history.
- q=0 costs no rent. Updates with no queries still force the same capacity condition on both schedules. The cap is a representation contract, not evidence that such rebasing is useful to an unconstrained consumer.
- Zero-weight or zero-delta events are allowed under the declared tariff; semantic pruning would be a different comparator.
- The final partial interval is paid as proved above, so no end-of-stream rebase is performed.
- With one pending A edit, unit query rent, no further edits and F=100, this policy pays 199 on 100 queries while OPT pays 100. This demonstrates a near-two instance for this policy. We do not claim a new optimality theorem for the complete capped model. Its uncapped single-edit special case is classical rent-or-buy.

### Concrete end-to-end consequence

Let U be the number of supplied updates, V the number of query events, and Q the total number of requested coefficients. Fix positive tariff coefficients, F≥1, and a feasible cap parameter 1≤B≤N. A feasible comparison schedule rebases every B updates, so it pays at most floor(U/B)F in resets and O(QB²) in the filtered bilinear query tariff. The competitive theorem therefore yields

    T_ALG = O(I + U + V + Q + UF/B + QB²),

including the O(1)-per-event scheduler work, even for zero-output queries. For a declared balanced workload U=Q=T, V=O(T), and B=ceil(F^(1/3))≤N, this is O(I+T F^(2/3)); thus the amortized cost after paid initialization is sub-F. With only one operand changing, the pair term disappears and the corresponding bound is O(I+U+V+Q+UF/B+QB), giving O(I+T sqrt(F)) at B=ceil(sqrt(F))≤N in that balanced regime.

These are arithmetic, workload-restricted amortized consequences of the stated evaluator and classical rebuilding. An individual rebase still costs F, the optimal B requires a chosen workload regime or separate adaptation argument, and a newly supplied dense filter has its own charged preparation. This is not a worst-case sub-F service bound or an improvement for a fresh arbitrary dense transform.

## 4. What the ratio includes, and what it does not

Let G=I+sum_t g_t be identical, unavoidable charged preparation, input/update work and requested-output work for both schedules. The exact tariff theorem gives

    G+ALG_optional ≤ 2(G+OPT_optional).

If an implementation incurs extra scheduler bookkeeping E(T) not included in that common tariff, write the honest bound instead as

    T_ALG ≤ 2 T_OPT_tariff + E(T) + P_extra.

Here E(T)=O(number of events) in the unit-cost model, and P_extra is any calibration or preparation paid only by ALG. Neither term is silently erased. For finite-word execution, counters and threshold arithmetic also need a word/bit model; they may be capped at thresholds where appropriate, but arbitrary precision is not free. The standard asymptotic statement is a constant-factor bound only after controlling these costs relative to mandatory reads/outputs. No measured runtime ratio follows from symbolic tariffs.

The theorem assumes a known valid F and known tariff weights. Training those weights from hardware is not proved exact. Mandatory calibration P(N) versus a clairvoyant comparator that pays no calibration already gives a cold one-query ratio at least P(N) when that query otherwise costs one. This rules out dropping the calibration term for such a policy; it does not rule out all calibration-avoiding dispatchers.

For a broader nonpreemptive black-box selector, two kernels with hidden runtimes 1 and L suffice to rule out any L-independent competitive ratio on one request: assign L to the kernel selected by a deterministic policy. A randomized policy chooses some kernel with probability at least 1/2; assigning L to that kernel gives expected cost at least (L+1)/2 while OPT costs one. This statement assumes no distinguishing information, no certified estimates and no preemption/racing. It is not a lower bound on inspectable Fourier code or on all dispatcher designs.

## 5. Why the unrestricted representation question remains open

**Explicit sparse-normal-form obstruction.** For integer d≥1 and N≥2^d, the d factors (e_0+a_i e_(2^i)), indexed by i=0,…,d−1 and with every a_i nonzero in a field, have a product with 2^d nonzero, distinct impulse positions. Every subset of {0,…,d−1} has a different binary subset sum below N; its coefficient is the nonzero product of its a_i. Thus an explicit list of impulse terms cannot have a depth-independent bound under arbitrary products, even though each factor has two terms.

This is a lower bound for that representation format only. The factored expression itself has O(d) nodes, and some instances have even simpler special formulas. The argument does not show that every compressed representation is large or that every selected coefficient is hard to compute.

**Total-state counting obstruction.** Over a finite field of size q, any self-contained exact representation supporting all coefficient queries for every possible length-N vector must distinguish q^N states: convolution with e_0 already returns an arbitrary input vector. With s field words and b additional metadata bits, injectivity forces s log_2 q+b≥N log_2 q, after counting all stored information, including handles and referenced data. This does not lower-bound additional memory when an N-word input or anchor is retained separately. Section 2 has O(N) paid anchors and does not evade this bound.

Neither obstruction establishes an unrestricted FFT lower bound. Neither settles all possible downstream circuits, shared identities, dynamic kernels, persistence policies or cancellation-aware canonical forms.

## 6. General finite-mode dispatcher: an existing-theorem reduction

Suppose a proposed implementation supplies a finite state set S of size m, a common initial state, nonnegative full service-cost vectors revealed before each event, and a fixed symmetric metric d giving the actual cost of conversion between complete valid states. Assume representation invariants, staleness, memory limits, retained caches and all conversion work are represented in those states and costs. Then its offline scheduling objective is exactly the metrical task-system objective sum_t[d(s_(t−1),s_t)+c_t(s_t)].

Borodin, Linial and Saks, Theorem 1.1, supplies a deterministic (2m−1)-competitive scheduler up to the theorem's additive initialization constant. This is a reduction to prior art, not a new dispatcher theorem. See the [author-hosted paper](https://www.cs.toronto.edu/~bor/Papers/optimal-online-algorithm-for-metrical-task-systems.pdf), JACM 39(4), 1992, pp. 745–763, especially printed p.747.

The general MTS lower bound uses arbitrary task-cost vectors. It cannot be transferred as a matching lower bound for a restricted Fourier workload without showing those vectors are realizable. Actual Phase 6 caches do not automatically satisfy the reduction: conversions can be asymmetric, costs can depend on history and data, future service costs can depend on caches not encoded by a mere kernel label, and full cost vectors require paid estimation. Enumerating complete configurations may make m enormous. The classical scheduling ratio also omits scheduler computation unless that is separately charged. Simply naming three kernels does not establish a three-state MTS or a factor-five runtime guarantee.

## 7. Prior-art classification

The threshold-and-reset proof is an application of a long-established rent-or-buy/batching idea. It is not asserted historically new. Dooly, Goldman and Scott's [institutional 1998 technical report](https://repository.library.washu.edu/cse_research/477/) describes threshold acknowledgment algorithms and factor-two guarantees in the TCP acknowledgment model; the journal version is *On-line analysis of the TCP acknowledgment delay problem*, JACM 48(2), 243–273 (2001), DOI 10.1145/375827.375843. The institutional abstract was read; the journal full body was not retrieved in this pass. This is antecedent identification, not a claim that its theorem statement is identical to our finite-event tariff/cap model. The proof in Section 3 is self-contained.

[Karlin, Manasse, McGeoch and Owicki](https://courses.csail.mit.edu/6.895/fall03/handouts/papers/karlin.pdf) provides primary rent-or-buy/nonuniform online-algorithm context. No randomized guarantee from it is claimed for this implementation.

[Reif and Tate's author-hosted dynamic-algebra paper](https://home.uncg.edu/cmp/faculty/srtate/papers/dynalg2.pdf), particularly Section 4, already uses paid rebuilding and buffered changes to obtain sublinear per-request dynamic algebraic algorithms. This rules out presenting rebasing, sparse pending edits or dynamic convolution itself as new. [Frandsen, Hansen and Miltersen's BRICS report](https://www.brics.dk/RS/98/11/BRICS-RS-98-11.pdf), Theorem 1 and its convolution reduction, gives a square-root worst-case lower bound in its listed dynamic algebraic models. We do not transfer that lower bound to the present amortized reset tariff or claim a new match.

Recent literature still differentiates delay models: [Bhore, Pawłowski and Umboh, APPROX/RANDOM 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX/RANDOM.2026.26) studies general TCP acknowledgment delays. Therefore a blanket statement that every monotone batch-cost objective inherits factor two would be unsafe. Section 3 uses additive per-query rents monotone in pending counts, not an arbitrary monotone cost of a completed batch.

This is a targeted primary-source comparison, not an exhaustive priority clearance.

## 8. Exact validation and scope of evidence

The original `EXACT_CHECKS.py` imports only Python standard-library modules; no supplied research code was executed. `VALIDATION.json` records:

- 25,600 exact filtered-convolution identity cases over F_3 and F_5, including repeated/cancelling two-sided updates;
- 1,562,500 length-seven scheduling cases against an independently enumerated offline dynamic program, with F in {1,2,3,5,8}, B in {1,2,3,5}, and events {A-update,B-update,q=0,q=1,q=3};
- 32,768 additional weighted-rent scheduling cases;
- explicit sparse-normal-form support doubling through depth eight;
- zero failures, and the separate 199/100 near-two example.

These checks test identities, interval bookkeeping, capacity, zero-query and tail edge cases. The arbitrary-sequence guarantee follows from the proof, not finite enumeration. No empirical speed, numerical stability, bit-complexity or independent-review acceptance is inferred.

## 9. Exact owner recommendations

Keep stable ID ALG-070, status TO RESEARCH, current priority, historical accepted identities and no-discovery qualification. Do not create another discovery count or close/reopen ALG-071.

After independent acceptance, a supplement may close only:

1. Exact bounded-view correctness for one changing A*B followed by fixed convolution filters, with all dense cores and preprocessing paid.
2. The factor-two reset/rent theorem under the identical capped event-list comparator and known tariffs.
3. Explicit sparse-normal-form and total finite-field-state obstructions at precisely their proved scopes.
4. Conditional finite-metric dispatch as a reduction to existing MTS theory, not a new theorem.

The remaining mathematical gate is to define and resolve a larger comparator covering cancellation/coalescing, multiple cached kernels, arbitrary downstream variable products and memory-constrained persistent views, with state-dependent/asymmetric conversions and paid cost learning. A new closure must provide a proof, a reduction with verified hypotheses, or a model-specific impossibility result; benchmark-only evidence cannot settle that gate. Numeric error certification and matched tuned-baseline experiments remain separate engineering obligations.

Recommended synchronized fields: Catalogue AE171/AF171; novelity breakthough Y209/Z209; Research overview P297/Q297. Section-specific summaries may also be appended to Catalogue Z171, novelity breakthough N209 and Research overview F297, preserving historical text. `PUBLISHABLE_OWNER_CHANGE_SUMMARY.json` identifies the six synchronized next-action/stop targets and the opening wording. No spreadsheet write is claimed by this report.
