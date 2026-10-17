# ALG-071: budgeted spectral materialization, exact model and reduction boundary

16 October 2026. Baseline repository commit: `de5dc664448d8e3e219df9651b2805d5a2cecbb1`.

## Result

The owner-linked successor can be made precise. Its **independently priced, single-plan surrogate** is ordinary monotone submodular knapsack and inherits the classical `1−1/e` approximation under the assumptions below. Its **actual lazy group-refresh objective is not generally submodular**, even for one synchronous epoch, additive memory, rank one, and three two-member candidate groups. A four-consumer counterexample proves this. A restricted homogeneous pair case reduces exactly to ordinary graph matching; candidate-restricted triples already give an NP-hard selection problem by an explicit three-dimensional-matching reduction.

These are scoped modeling/reduction results, not claims of historical novelty, practical speed, or a new DFT bound. General online migration is a finite state-control problem; a metrical-task-system theorem applies only to an expressly stronger reset/metric contract. The current source does not supply that contract. No general approximation or competitive guarantee for the full engine follows from its measured per-group scores.

## 1. Source and scope

The exact source is [ADAPTIVE_VIEW_ORGANIZER_RESEARCH.md, §10](https://github.com/AgentSlop-Si/research/blob/de5dc664448d8e3e219df9651b2805d5a2cecbb1/math/archive/objects/96/965a2b512b3a8abf3f3d200cd4ac3325637c7e386d72c15ca93df6c8593ec9f5__ADAPTIVE_VIEW_ORGANIZER_RESEARCH.md). The connector returned Git blob `ad705ed76f68c1a4e4983a2c5e7db2f3887ad0e4`; the source text is 8,981 UTF-8 bytes, SHA-256 `965a2b512b3a8abf3f3d200cd4ac3325637c7e386d72c15ca93df6c8593ec9f5`. Its full pinned response is preserved in `evidence/PINNED_ORGANIZER_SOURCE.json`.

The source proposes selecting possibly overlapping groups under a memory budget, accounting for union storage, optional contiguous basis projections, maintenance/query benefit, and migration/hysteresis. It does not specify a theorem objective, adversary, finite candidate encoding, storage-sharing convention, or approximation target. The existing greedy partition and empirical synchronization score are therefore not an optimization specification.

The preceding full-source report [previously accepted full-source finalization report](https://github.com/AgentSlop-Si/research/blob/de5dc664448d8e3e219df9651b2805d5a2cecbb1/math/finalized/2026-10-16-full-open-index-coverage-audit/reports/alg071/REPORT.md) was read. The accepted ordered-word occupancy/cache supplement concerns a different object and is not reopened. Existing numerical-stability, heap accounting, and production qualifications remain outside the results below. No owner-supplied program was executed, imported, or compiled. No spreadsheet or repository state was changed in this work.

## 2. Finite source-granular model

### 2.1 Input and admissible computation

Fix a signal length `N`, a rank `r`, a finite consumer set `V`, and Fourier-bin sets `Q_v ⊆ {0,…,N−1}`. Write `q_v=|Q_v|` and `W=⋃_v Q_v`. The producer supplies an event trace of length `L`, consisting of metadata updates and consumer queries. After producer version `t`,

`x_t = B c_t + e_t`, with `|supp(e_t)|=k_t`.

The matrix of basis Fourier values on `W` is already available, or its construction is an explicitly charged preprocessing step. The trace supplies all changed coefficients/points needed to replay an update. A fixed bounded-history policy determines whether events after an old version are still available. Exact complex arithmetic is the mathematical semantics; no floating-point error theorem is asserted.

The candidate family `C={1,…,J}` is an explicitly listed part of the input. Candidate `g` has members `G_g ⊆ V`, union `U_g=⋃_{v∈G_g}Q_v`, and `u_g=|U_g|`. A finite list of representation modes, including whether contiguous basis data is duplicated, can be included. Selecting all `2^|V|` groups is not polynomial-size input unless separately compressed and provided with appropriate oracles.

A query can use its permanent solo view or one compatible resident group whose union contains the entire requested bin set. Compatibility may be declared by membership or by `Q_v⊆U_g`; this choice must be fixed. The examples below work under either convention, because each consumer has a private bin. Combining several partial group caches into one answer is excluded from the base model; it is an additional plan family, not a free operation.

The permitted primitives are the source's whole-view/whole-group replay, rebuild, same-version union assembly, and output extraction, plus explicitly priced allocation, projection-layout creation, and eviction. This is an organizer model over those primitives. It is not a lower bound against arbitrary Fourier algorithms, arbitrary sub-bin caching, or a larger unlisted candidate family.

### 2.2 State and refresh ledger

A resident group has a representation mode and a last-valid producer version `τ_g`; an allocated but uninitialized group has a special empty state. Solo views have their own versions. Queries routed through a group do not silently refresh solo views; any copied-back cache update is a separate permitted action with its own cost and memory effect.

For a simple arithmetic ledger, define `H(τ,t)` to be the number of available metadata events between versions `τ` and `t`. For a nonempty group,

`R_g(τ,t) = u_g · min(H(τ,t), r+k_t)` if full history is retained,

`R_g(τ,t) = u_g · (r+k_t)` otherwise.

This equation defines the unit-priced abstraction; it is not an exact hardware timing claim. A richer fixed primitive-cost table can distinguish coefficient/point event costs, arithmetic, layout gathers, vector initialization, allocation, and traffic. At `τ=t`, no refresh is needed. For an empty group, cold initialization is a rebuild or an admissible same-version copy, never replay from nonexistent values.

Every query additionally pays for its explicit `q_v` outputs. Thus the familiar asymptotic single-query expression is `O(q_v[1+min(H,r+k_t)])`, or `O(q_v[1+r+k_t])` after history loss. A refresh-only expression without the output term is not a complete query bound. Producer metadata changes, query logging, candidate generation, score estimation, planning, and losing-plan preparation must be charged separately if an end-to-end objective is claimed.

Same-version union assembly avoids Fourier arithmetic but still reads/copies/places `u_g` values and constructs its mappings. It cannot be assigned zero total work merely because it needs no rebuild. Its source caches must remain available until copying completes.

### 2.3 Memory and migration ledger

Choose one precise memory unit, such as numeric payload cells, or explicit byte sizes including index/allocator objects. A big-O expression is not a hard budget. Fix a base ledger `M_0(t)` for permanent basis projections, coefficients/residual state, solo caches, history, mappings, roots if used, and permanently reserved work/output buffers. Missing base objects cannot be silently excluded from an advertised total-memory cap.

With duplicated mutable union caches, a candidate mode has a specified integer charge

`m_g = numeric(u_g) + optional_projection(r u_g) + index/header(g)`.

Resident feasibility is `M_0(t)+Σ_{g∈S_t}m_g ≤ M`. Two groups sharing a bin still retain two numeric cells in this convention. Optional contiguous copies likewise duplicate basis data; the global basis projection is counted in `M_0` if retained. This is one additive knapsack only when base reservation is fixed and all remaining charges are modular.

If physical objects are shared instead, list atoms `a` with sizes `w_a` and group dependencies `A_g`. Then

`M(S)=M_0+Σ_{a∈⋃_{g∈S}A_g}w_a+Σ_{g∈S}header_g`.

This generally is not an additive item budget. Immutable basis rows can be shared without changing freshness. Mutable spectrum cells require version/alias semantics: one cell cannot simultaneously hold two independently stale versions. A per-group timestamp is insufficient if aliases are refreshed independently. Shared mutable storage therefore changes both feasibility and the state-transition system.

For a move `z→z'`, record allocation/deallocation, cold rebuild or same-version copying, optional projection construction, and all planner work. Check peak memory during the move, including old and new objects and scratch. Feasible endpoints alone do not imply a feasible migration. Evict-before-build may fit where simultaneous construction does not, but loses the evicted warm state and may remove copy sources.

The scalar objective may be arithmetic work, a specified weighted operation ledger, or an explicitly measured platform cost. Different units may not be added without stated conversion weights. Keep traffic, peak cells, and arithmetic as separate diagnostics when no conversion is justified.

### 2.4 Objective and exact finite solution

For the given finite trace, minimize total primitive cost over legal initial construction, routing, refresh, eviction, and migration actions, subject to the memory cap at every intermediate step. The comparison baseline is the same trace served by solo views under the same output, history, initialization, and primitive-cost conventions. Static selection fixes the resident candidates for the trace; dynamic selection permits migrations at the stated decision boundaries.

A state contains all resident modes, cache versions/empty markers, permanent-solo versions, and any history/alias information needed to price future actions. With the trace fixed, numeric values at an exact version are determined, so they need not be separate combinatorial state coordinates. With finite primitive modes and bounded history, the state space is finite. A coarse version-coordinate count alone is of order `(T+2)^(J+|V|)` before representation and sharing factors; no efficient state count is claimed.

Let `C_s(z,z')` be the shortest nonnegative-cost legal primitive path that consumes event `s` exactly once, consumes no later event, and maps state `z` to `z'`, with infeasible paths assigned infinity. The exact recurrence is

`D_0(z_initial)=0`, `D_0(z)=∞` for every other state, and `D_s(z')=min_z[D_{s−1}(z)+C_s(z,z')]`.

The optimum is `min_z D_L(z)`. To justify this, split any legal execution at event boundaries; each segment costs at least its corresponding `C_s`. Conversely, concatenate minimizing feasible segments. Induction gives equality. Finite-state shortest paths handle within-event choices; nonnegative cycles can be removed. This establishes a precise exact optimization problem and a finite exhaustive method, not a polynomial-time optimizer or an online guarantee.

## 3. The classical surrogate and its exact theorem implication

Suppose the workload is a list of request types `i` with weights `w_i≥0`, baseline costs `c_i0`, and fixed per-request candidate-plan costs `c_ig`. Each request uses exactly one complete plan. Costs are independent of other requests, resident alternatives, freshness histories, and selection-dependent refresh schedules. Define `b_ig=max(0,c_i0−c_ig)`, with zero benefit for incompatible plans. Then

`F(S)=Σ_i w_i max_{g∈S} b_ig`, with empty maximum zero.

**Proposition 1.** `F` is normalized, nonnegative, monotone, and submodular.

**Proof.** Let `B_i(S)=max_{h∈S}b_ih`. The marginal of candidate `g` is `Σ_i w_i max(0,b_ig−B_i(S))`. Since `B_i(A)≤B_i(B)` whenever `A⊆B`, this marginal cannot increase when the selected set grows. All other properties follow immediately. ∎

With one additive integer memory budget, polynomially evaluable costs, and zero-cost items handled first, Sviridenko's 2004 Theorem 1 gives a `1−1/e` approximation to maximum benefit. Freeze one representation per candidate for this implication: an additional at-most-one-mode constraint is not automatically covered by the one-knapsack theorem. Its algorithm includes enumeration through three-item seeds and marginal-density completion; ordinary density greedy alone is not this theorem. The approximation is for saved cost `F`, not a multiplicative approximation to the remaining query cost. Overlapping candidates and redundant benefits are fully allowed. [Primary theorem](https://thibaut.horel.org/submodularity/papers/sviridenko2004.pdf), pp.41–43.

If every item's benefit is genuinely independent and additive, this simplifies further to ordinary 0–1 knapsack. That additional property must not be inferred from separately measured scores.

Subtracting a fixed additive maintenance/construction bill, `F(S)−Σ_g h_g`, preserves submodularity but can destroy monotonicity and nonnegativity. The cited monotone theorem then does not apply without further hypotheses. If one instead may activate only a subset of selected groups and pays activation only for those used, the optimized set function is a different object; Proposition 2 shows it need not even be submodular.

## 4. A source-granular counterexample to general submodularity

**Proposition 2.** Best service savings from optional use of a fixed resident set of lazy groups need not be submodular, even under the synchronous rank-one, additive-memory restrictions below.

Take four consumers with `Q_i={a,p_i}`, where `a` is common and all `p_i` are distinct. Let `r=1`, residual size zero, and one coefficient event since all caches were valid. Each consumer asks once at the new version. Every solo refresh costs two units; every two-member group refresh costs three. Explicit output costs are identical under all routes and are included on both sides, so they cancel in savings.

There are only three candidates:

`A={1,2}`, `B={1,3}`, `C={2,4}`.

Fix the resident candidate set `S`. Allocation/construction is sunk for this warm service comparison; every selected cache has the same old version. The controller may leave a candidate unused. If the refreshed candidates form `T⊆S`, every covered consumer can be served by one of them and every uncovered consumer uses its solo cache. Relative to baseline refresh cost eight, the saving is exactly

`2|⋃_{g∈T}G_g|−3|T|`.

It follows by listing subsets that

`F({A})=F({A,B})=F({A,C})=1`, while `F({A,B,C})=2`.

The marginal of `C` is zero at `{A}` and one at `{A,B}`. This violates diminishing returns. Equivalently, `F({A,B})+F({A,C})=2<3=F({A})+F({A,B,C})`.

Private bins guarantee that accidental `Q_v⊆U_g` compatibility adds no unlisted members. No partial-cache assembly, shared physical cells, long history, temporal uncertainty, or adaptive adversary is needed. Candidate caches are duplicated, so memory is additive. A fixed modular charge for every selected candidate cancels from the submodularity inequality and does not repair it.

This is not a counterexample to Sviridenko: paying one union refresh that can serve several requests violates the independently priced request-plan hypothesis. It also does not prove novel complementarity in materialized views. Mistry et al. already define set-dependent maintenance benefit and explicitly warn that marginal benefit can increase when more views are materialized. Their preprint is from 2000; the SIGMOD publication is 2001. [Primary preprint](https://arxiv.org/pdf/cs/0003006), §6, especially §6.2.

## 5. A complete restricted case: graph matching

The same example belongs to a solvable family. Let every consumer's bins be a common set of `m≥1` bins plus one private bin, let every candidate have two members, and use the same synchronous, one-unit-refresh, warm-resident convention. Candidate pairs form a graph. For resident edges `S`,

`F(S)=max_{T⊆S}[(m+1)|V(T)|−(m+2)|T|]`.

**Proposition 3.** `F(S)=m·ν(S)`, where `ν(S)` is the maximum matching size.

**Proof.** A matching of size `k` covers `2k` vertices and gives saving `mk`. For the reverse direction, split any nonempty selected edge set `T` into connected components. A component with `e≥1` edges has at most `e+1` vertices, so its contribution is at most `(m+1)(e+1)−(m+2)e=m+1−e≤m`. Pick one edge from every such component. Those edges form a matching and give at least the original contribution, even if some component contributions were negative. Maximizing proves the equality. ∎

With equal candidate memory `m+2` and capacity for at most `K` candidate groups, the best service saving is therefore `m·min(K,ν(C))`. This is an exact ordinary matching reduction under the stated homogeneous assumptions. Construction, unequal sizes/prices, asynchronous requests, or larger groups change the problem. The non-submodularity witness is also the familiar failure of matching edge families to form a matroid; it is not a new general combinatorial phenomenon.

## 6. Candidate-restricted triples are already NP-hard

Here is an explicit hardness boundary that includes a nonzero cold-construction charge. Start from a three-dimensional-matching instance with disjoint parts `X,Y,Z`, each of size `K`, and a listed triple family `E⊆X×Y×Z`. Each element is a consumer with four common bins plus one private bin, so `q_v=5`. Each candidate is one listed triple, with `u_g=7`. The mandatory solo caches already exist, are stale by one rank-one metadata event, and each requested consumer is queried once at one version.

Use a fixed primitive ledger: solo refresh costs five; a new group pays seven units for allocated payload initialization and seven for a full current rebuild/copy, total fourteen. Every new group pays the same fourteen, including one assembled from same-version member views; there are no free sub-bin copies, mutable aliases, or partial-initialization discounts in this restricted model. Output costs and base state costs are common. The additional resident-memory budget is `7K`, so a static selection contains at most `K` groups. No other groups or partial-cache plans are available. The construction is polynomial in the listed 3DM instance.

For used groups `T` of size `h≤K`, the best saving is

`5|⋃_{g∈T}G_g|−14h ≤15h−14h=h≤K`.

Equality with `K` holds exactly when `h=K` and all `3K` covered consumers are distinct, which is exactly a perfect three-dimensional matching. Conversely such a matching saves `K`. A group with no served request can be dropped; paying initialization on unused selected groups cannot improve the optimum. Thus deciding whether service-plus-construction savings reach `K` is NP-hard in this finite-candidate, static, exact-primitive model. Karp's 1972 three-dimensional-matching hardness supplies the classical premise; see the [authorized primary reprint](https://sites.math.washington.edu/~thomas/teaching/m514_web/50YearsIP.pdf), original pp.95–100.

The charge of fourteen is a stipulated weighted primitive ledger, not a measured machine time. It avoids pretending cold construction is free. The simpler warm-ledger version uses cost seven per group and threshold `8K` with the same proof. These are hardness results for choosing among given whole-group plans. Allowing all possible groups, arbitrary partial-bin reuse, or new Fourier algorithms can create additional cheaper plans and requires a new argument. No unrestricted DFT hardness or approximation-hardness threshold is claimed.

## 7. Online migration: what does and does not follow

An online policy sees the revealed trace prefix and its current state. It must specify whether it sees the current query before choosing a group, whether future batch membership is known, and whether a workload distribution is given. A measured window predicts future demand; it is not an adversary restriction or a proof.

Adding real nonnegative migration costs to the objective is necessary but does not prove absence of thrashing. Positive costs may still be repeatedly worth paying. A hysteresis rule that requires forecast or accumulated savings to exceed a threshold is a policy choice. Without a proved prediction assumption or competitive analysis it has no automatic global guarantee. An extra hysteresis penalty is distinct from actual copying/allocation cost and must not substitute for that ledger.

There is a clean **conditional** classical implication. Suppose there is a finite family of feasible epoch configurations; each epoch begins under a prescribed canonical freshness/reset convention so service cost `c_t(S)` depends only on the chosen configuration and the revealed epoch task, not earlier routing. All reset work is included in the service or movement ledger; canonicalization is not free. Suppose changing configurations costs a fixed symmetric metric `d(S,S')`, independent of producer data/time/history, and every current cost vector is revealed before the state choice. Then this is a metrical task system on `n` configurations. Borodin–Linial–Saks give deterministic competitive ratio `2n−1`, allowing an additive sequence-independent constant. [Primary paper](https://www.cs.toronto.edu/~bor/Papers/optimal-online-algorithm-for-metrical-task-systems.pdf), definitions pp.746–747 and Theorems 1.1–1.2.

Here `n` counts feasible configurations, potentially exponentially many, not candidate groups. The general lower bound uses arbitrary task vectors and need not hold for a restricted Fourier task family. This is a standard theorem implication, not a useful small-factor optimizer promised for the engine.

Actual free eviction/paid construction is asymmetric; same-version copying depends on warm contents; producer updates change cache usefulness; and refresh ages affect service cost. Endpoint configurations alone are not ordinary MTS states. Enlarging the state to include freshness does not automatically produce a fixed metric or MTS service semantics. Directed variants need their own hypotheses and parameters.

Ordinary file caching is also insufficient by name alone. Young's Landlord theorem assumes a request names a particular file, positive integer sizes, and fixed per-file retrieval costs. Its `k/(k−h+1)` resource-augmentation bound compares capacities `k` and `h`. The paper explicitly excludes varying retrieval costs and cache consistency/invalidation. Overlapping substitute groups and shared refresh are not that model without a separate reduction. [Primary paper](https://www.cs.ucr.edu/~neal/Young98Online.pdf), Theorem 1.1 and p.83 footnote 1.

## 8. Validation and disposition

`verify_model.py` is newly written for this report. It exhaustively verifies the four-value witness; the matching identity on every simple graph on five vertices for three common-core sizes (3,072 cases); and the triple hardness threshold on all 256 subfamilies of the `2×2×2` tripartite triple family. `CONTROL_RESULTS.json` records all assertions passing. These finite checks support implementation-free model arithmetic; the proofs, not the tests, establish the universal statements. They neither execute the original engine nor validate numerical stability or timing.

This finishes a bounded formalization and primary-theorem comparison gate. It gives a precise implementable specification for a trace oracle and separates standard corollaries from unresolved claims. It does not establish historical novelty or a general efficient approximation/competitive algorithm for the exact stateful successor. A new research identity, discovery count, performance claim, whole-owner closure, or automatic archive is not justified by this report alone.

If continuing, the next decision must choose one fixed target: (i) implement/evaluate the explicitly proved submodular surrogate, (ii) solve a declared structural subclass such as homogeneous pairs, or (iii) state one general sequential approximation/competitive question with all model choices above frozen. Those alternatives cannot be silently mixed. The existing owner status and priority should remain unchanged unless the parent independently accepts a scoped disposition.
