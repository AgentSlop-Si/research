# ALG-071: heterogeneous pair materialization at one common epoch

17 October 2026. A bounded extension of the accepted homogeneous pair result; no historical novelty, general optimizer, production result, or owner closure is claimed.

## 1. Outcome and relation to the accepted work

The matching reduction does not require equal consumer bin sets, equal pair costs, or equal refresh savings. It requires a precise pair-service contract and the inequality that every pair charge is at least each endpoint's solo charge. Under that contract, all beneficial overlap between active pairs can be removed without increasing cost. The optimum is a maximum-weight matching when no additional constraint binds. With a nonredundant memory constraint, it is a constrained maximum-weight matching; the memory constraint must not be erased.

This extends only §5 of the previously accepted `MODEL_AND_THEOREMS.md` at [repository commit 22e4fbd](https://github.com/AgentSlop-Si/research/blob/22e4fbdff0dd655d4cac7408964142fd2476686d/math/finalized/2026-10-16-mathematical-development-1221/alg071/MODEL_AND_THEOREMS.md). The finite model, non-submodularity witness, restricted triple hardness, and prior-theorem gate in that work are retained, not repeated or reopened. The exact earlier proof is copied into `evidence/ACCEPTED_MODEL_AND_THEOREMS.md` for source binding. Recorded owner status remains TO RESEARCH, priority 12; the closed formalization gate stays closed. This packet does not propose any source-cell replacement or change any repository, spreadsheet, or external record.

The anticipated interrupted heterogeneous artifact was not found under the available shared-workspace names or text search; this is a freshly written recovery of the stated mathematical claim, anchored to the existing accepted result. No historical program was executed, imported, or compiled. The verification code in this packet was freshly authored for these statements.

## 2. Exact static pair-service contract

Let `G=(V,E)` be a finite simple undirected graph. Every vertex is a consumer requiring service at the same producer version. A candidate edge `e={u,v}` serves exactly the two declared endpoint consumers, or either one separately, after one activation. There is no extra compatible consumer unless it is an endpoint. In particular, arbitrary bin-set containment must not silently add non-endpoint service.

For each vertex, a solo plan is always available at fixed cost `s_v >= 0`. For each edge, activating its whole-pair plan costs `c_e >= 0`. These costs are independent of which other plans are activated, of the chosen request order, and of routing within the epoch. An activated pair can serve both endpoints without additional variable cost beyond the common explicit output bill. Shared physical mutations, partial-bin assembly, pair-to-pair copying, and multi-epoch freshness interactions are excluded. Unused resident edges need not be activated.

Let `O` be the common output and other route-independent bill. For an active edge set `T`, let `V(T)` be its incident vertices. Its optimal service cost in this restricted ledger is

`C(T) = O + sum_{e in T} c_e + sum_{v not in V(T)} s_v`.

Indeed, already-covered vertices can use an active incident pair without paying another solo charge; every uncovered vertex must use its solo plan. Output is still paid even when a cached result is fresh. A specified nonnegative construction/initialization charge can be included in `c_e`; it cannot be omitted from a cold objective merely because a warm service comparison omitted it.

The admissible edge-set family `F` must be nonempty and downward closed: `T in F` and `T' subset T` imply `T' in F`. In addition, the solo fallback assumed above must remain executable within the resource cap. Sections 5 and 6 make this requirement operational.

## 3. Pruning theorem

**Theorem.** Assume, for every edge `{u,v}`,

`c_{uv} >= max(s_u,s_v)`.

Every feasible active edge set `T` has a feasible matching `M subset T` with `C(M) <= C(T)`. Consequently,

`min_{T in F} C(T) = O + sum_v s_v - max_{M matching, M in F} sum_{{u,v} in M} (s_u+s_v-c_{uv})`.

Empty matching is allowed, so the maximum saving is nonnegative. Negative-weight edges can be discarded; zero-weight edges may be discarded without worsening the optimum.

**Proof.** If `T` is not a matching, some vertex `u` has degree at least two. Choose an incident edge `e={u,v}` and remove it. Vertex `u` is still covered. If `v` also has degree at least two, no vertex becomes uncovered and the cost difference is `-c_e <= 0`. If `v` has degree one, only `v` becomes uncovered and the cost difference is `s_v-c_e <= 0`. The smaller set remains feasible by downward closure. Repeating strictly decreases the number of edges and terminates after at most `|T|` deletions at a matching `M subset T` with no larger cost. For a matching, covered endpoints are disjoint, so subtracting its cost from the all-solo baseline gives exactly the sum of its edge weights `s_u+s_v-c_{uv}`. Maximizing proves the equality. ∎

The theorem asserts existence of a matching optimum, not that every optimum is a matching. Equality cases can retain overlapping edges at the same cost. The stated endpoint-dominance condition is sufficient, not asserted to be a necessary characterization for every instance.

If `F=2^E`, or the resource limit is already satisfied by every considered matching, the right-hand side is ordinary maximum-weight matching. This is the classical problem addressed by [Edmonds, 1965, *Maximum Matching and a Polyhedron With 0,1-Vertices*](https://nvlpubs.nist.gov/nistpubs/jres/69B/jresv69Bn1-2p125_A1b.pdf), pp.125–130, especially the weighted-pairing problem on p.125. The reduction is the contribution here; no new matching algorithm is proposed. Rational weights with an explicit finite encoding permit the standard polynomial-time weighted-matching algorithms. Construction of the candidate graph, intersections, and weights must also be paid.

## 4. Arbitrary bin sets at a common epoch

Let every consumer have an arbitrary finite bin set `Q_v`; empty sets and repeated sets are allowed. Let `lambda >= 0` be the common per-bin refresh charge at the epoch. For example, in the accepted warm common-version ledger, `lambda = min(H,r+k)` when all relevant history is available, or `lambda = r+k` after history loss. All participating caches must have the common freshness/history assumptions that justify that same factor. This is a stipulated arithmetic ledger, not a measured hardware cost.

A solo refresh costs `s_v = lambda |Q_v|`. A declared pair refresh, including a nonnegative fixed pair activation/construction charge `h_{uv}`, costs

`c_{uv} = lambda |Q_u union Q_v| + h_{uv}`.

Since union cardinality dominates either endpoint cardinality, the pruning hypothesis holds. Inclusion-exclusion gives the exact matching edge weight

`w_{uv} = lambda |Q_u intersection Q_v| - h_{uv}`.

Thus the optimum service-plus-declared-activation saving is the maximum feasible sum of intersection savings minus activation charges over disjoint consumer pairs. No equal-size, common-core, private-bin, or uniform-edge-price assumption is needed when endpoint membership defines service. If physical overlap allows undeclared consumers to be served, this formula alone is insufficient; see §6.

The same derivation holds with cardinality replaced by any nonnegative additive bin measure `mu`: `s_v=lambda mu(Q_v)`, `c_uv=lambda mu(Q_u union Q_v)+h_uv`, and `w_uv=lambda mu(Q_u intersection Q_v)-h_uv`. It does not hold automatically for arbitrary cache- or group-dependent timing functions. If solo activation costs are added, check `c_uv >= max(s_u,s_v)` anew and use `s_u+s_v-c_uv`; do not retain the simplified intersection formula without a derivation.

**Recovery of the accepted homogeneous case.** For `m` common bins and one distinct private bin per consumer, `lambda=1`, and `h=0`, every solo cost is `m+1`, every pair cost is `m+2`, and every matching edge saves `m`. Therefore the accepted identity `F(S)=m nu(S)` follows. With equal additional pair-memory charge `m+2` and capacity for at most `K` pairs, the saving is `m min(K,nu(E))`. This homogeneous cardinality formula does not extend by replacing heterogeneous weights with a single average.

## 5. Memory, construction, and algorithmic limits

### Already-resident pair caches

For a fixed feasible resident graph `S`, unused pairs may stay resident and inactive. Their allocation cost is sunk for a warm service-only comparison. Optimize activation only over `T subset S`. The theorem yields an ordinary weighted matching in `S` when all such activations are feasible under the reserved solo/scratch budget. It says nothing about whether the initial resident set was optimally or feasibly built.

### Selecting and building pair caches

Reserve a base charge `M0` that includes permanent solo caches, their legal refresh scratch, basis/history/state objects, mappings, output buffers, and every other claimed baseline object. With duplicated pair payloads, let each pair have a nonnegative fully specified incremental charge `m_e`. Require

`M0 + sum_{e in T} m_e <= M`.

This is downward closed, so the pruning theorem survives. The reduced problem remains

`max sum_{e in matching} w_e subject to sum m_e <= M-M0`.

A binding heterogeneous budget is an additional knapsack constraint. Ordinary unconstrained weighted matching cannot simply be used and declared budget-feasible. For example, two disjoint pairs of weights 5 and 6 and memory charges 6 and 6 have unconstrained optimum 11, but budget 6 permits only saving 6.

More generally the abstract ledger contains 0–1 knapsack exactly: give item `i` a separate disjoint pair, choose both endpoint solo costs `p_i`, pair cost `p_i`, and pair memory charge `a_i`. The matching constraint is then automatic, each edge saves `p_i`, and the memory constraint is `sum a_i <= B`. This is an exact embedding in the abstract rational/integer cost ledger; no claim is made that every such binary-encoded instance is realized by explicitly listed unit-cost bin sets with the same input size. No general polynomial-time solution of the budgeted problem follows from this packet.

Monotone atom-union accounting `M0 + sum_{a in union A_e} size(a) + sum headers_e` is also downward closed if immutable/shared objects obey the stated version contract and solo fallback stays available. Matching structure still follows, but feasibility remains the atom-union constraint; it is not an additive knapsack unless separately proved so. Aliased mutable caches with different freshness versions are outside this static ledger.

Cold construction and migration must pay their own cost and peak memory. One sufficient simple construction contract is sequential build, permanent solo fallback, all retained pair payloads charged, and a fixed base scratch reserve sufficient for any single legal construction/refresh. If an endpoint or a source cache has been evicted, if a rebuild needs additional peak storage, or if deletion removes the only feasible copy source, endpoint resident feasibility alone is not enough. The theorem applies only after the full operation-level resource contract has justified downward-closed feasible plans with valid solo fallback. No runtime is claimed from an arithmetic-only ledger that omits output, planning, gathers, allocation, traffic, or root/buffer charges.

## 6. Sharp scope controls

1. **Dropping endpoint dominance can fail.** Three consumers have solo costs 1 and edges `{1,2}` and `{1,3}` each cost 0. Both edges together cost 0. Every matching leaves an uncovered consumer and costs at least 1. Thus the nonoverlap conclusion is false for arbitrary pair prices. Nonnegative pair cost by itself does not suffice.
2. **Implicit containment can fail.** Give three consumers the same single bin, all solo costs 1, and only the declared edge `{1,2}` with union refresh cost 1. If this candidate may also serve consumer 3 by containment, its actual cost for all consumers is 1; the endpoint-only matching model computes 2. The pair graph and service domain must agree.
3. **Downward closure matters.** If the only feasible active set is the two-edge path, it has no feasible matching subset even when every pair cost dominates both solo costs. This is a logical negative control, not a proposed memory model.
4. **Cold charges matter.** Identical two-bin consumers, `lambda=1`, and pair activation charge 3 yield edge saving `2-3=-1`; the all-solo optimum is better. Dropping the activation charge incorrectly predicts positive saving 2.
5. **Budget cannot be erased.** The disjoint-edge example in §5 gives unconstrained saving 11 and budgeted saving 6.
6. **Time dependence is not covered.** Different cache versions, multiple producer epochs, migration hysteresis, state-dependent costs, and partial-group service can defeat the fixed-cost decomposition. This theorem is not a general stateful approximation or competitive guarantee.

## 7. Fresh validation and disposition

`fresh_verify.py` checks the theorem against an independent recursive matching oracle, exhaustive small abstract ledgers, freshly generated heterogeneous bin sets, additive and shared-atom memory predicates, all deletion steps, and the negative controls above. `FRESH_RESULTS.json` records exact counts and outcomes. These finite tests supplement the proof, not replace it.

The bounded result is ready for independent mathematical review. It generalizes the accepted homogeneous matching subcase under fully stated assumptions and explicitly retains the budgeted optimization boundary. Production numerical stability, heap/traffic accounting, guards, fair tuned-baseline qualification, general stateful optimization, and any historical-priority determination remain unfinished or unclaimed. No existing acceptance, score, owner status, or source cell is changed by this packet.
