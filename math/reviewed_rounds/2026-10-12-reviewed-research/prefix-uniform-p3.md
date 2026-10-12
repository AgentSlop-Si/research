Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 226e12117926e3610b55b6eb934087efe308d61c9ebe13d3f0b5b2cf569832b9

---

# Independent review: uniform prefix theorem for D8 × C3 × Cr

11 October 2026 UTC. Decision: **ACCEPT**, subject to the exact source bindings in this packet. No mathematical repair is required.

This is independent project mathematical review of a computer-assisted theorem. It is not external peer review, a proof-assistant formalization, or a historical-priority finding.

## Accepted result

For every prime r ≥ 5, let G = D8 × C3 × Cr, N = 24r. For a labeled order x of G, let Tj be its first j elements, Sj its left stabilizer, Z(x)=Σj=1..N (|Sj|−1), and B(x)=⟨Sj:1≤j<N⟩. The full prefix is scored exactly once and excluded from B; the empty prefix is excluded.

- The maximum proper-prefix independent-set score in the stated forbidden-maximal-order compatibility graph is exactly 46r−23.
- The maximum of Z among B(x)=G is exactly 70r−24.
- The unrestricted maximum is exactly 76r−24, so the sharp full-escape deficit is 6r.
- The unrestricted maximizers are precisely recursive maximal-subgroup right-coset block orders, with independent optimal internal orders. Their unique top subgroup is B(x).
- With A(1)=1, the labeled unrestricted-optimizer count is

  A(G)=2 A(C4×C3×Cr)^2 + 4 A(C2²×C3×Cr)^2
       + 6 A(D8×Cr)^3 + r! A(D8×C3)^r.

Actual subgroups are counted. No quotient by translations or automorphisms and no extra coset-representative factor is used. No classification or count of all full-escape maximizers is asserted.

## Independent checks and trust boundary

The reviewer wrote three fresh mathematical programs. No candidate, inherited, or uploaded mathematical program was executed or imported. The affine checker reads the author's JSON certificate as data only. All mathematical arithmetic is exact Python integers. No solver status, floating-point tolerance, or finite-sample extrapolation is used in the acceptance.

1. `independent_check.py` reconstructs conflicts by directly searching for an allowed common-order multiple, rather than importing the author's ceiling/floor predicate. Its independent frontier recurrence passes all 160,060 exact inequalities on 32,012 affine records, all eight residues, and all 24 bands. The final slope is at most 1,104 in each residue and the final value at t=3 is at most 3,312+46rho−23. It also checks all 23 admissible abstract-graph bases 5≤r<73, gcd(r,24)=1.
2. `check_explicit_graph.py` separately constructs every node and edge from the complete divisor list and runs an uncompressed graph DP. At r=5,7,11,13 it obtains respectively 207,299,483,575. The node/edge counts are respectively (218,3193), (288,4421), (428,6877), (498,8105). These are finite consistency controls, not the justification for the uniform quantifier.
3. `check_group_bridge.py` independently regenerates all ten D8 subgroups by closure; verifies the one cyclic and two Klein-four maximal subgroups and their normality; directly checks the D8 attaining seeds; and evaluates the count recurrence. It recovers both previously accepted labeled counts at r=5 and r=7. Additional r=11,13 count evaluations in its output are consistency controls conditional on the accepted classification, not exhaustive enumeration of all labeled orders.
4. Fresh negative controls reject a deleted residue, a deleted reachable state, a lowered affine base anchor, and a checker modified to omit distance-24 low conflicts. The pristine certificate is left unchanged.

## Graph and state equivalence

The subgroup form L×Cd follows by coprime power isolation; d divides 3r and |L| is a power of two. All maximal subgroups are normal with prime index. If a proper prefix is invariant under such a subgroup J, an outside stabilizer has transitive action on the prime quotient. Before that prefix its nonempty support would have to be full; after it a full J-coset would force every J-coset full. Thus B=G excludes stabilizer orders 12r,8r,24.

For two nested prefixes, odd saturation or odd core supplies an intermediate invariant set of size a multiple of the lcm of their stabilizer orders, with the specified endpoint restrictions. This depends on comparable D8 subgroup cardinalities, not on comparable or permuting actual D8 subgroups. Hence every actual full-escape order gives an independent set of exactly its proper-prefix score. Realizability of arbitrary graph independent sets is unnecessary.

Since r is prime and coprime to 24, all remaining stabilizer orders are exactly the six low orders {2,3,4,6,8,12} and the five high orders {r,2r,3r,4r,6r}. The 49 high vertices are (kr,ar), a|k, 1≤k≤23. There is neither overlap nor omission.

For low–low edges, every lcm divides 24. A displacement exceeding 24 contains an interior lcm-multiple, so the exact future edge radius is at most 24. At displacement 24 there are six oriented type pairs at phase zero: (3,8),(6,8),(8,3),(8,6),(8,12),(12,8). Both endpoint restrictions matter. These edges are retained and independently checked.

For low–high edges, the lcm equals r·lcm(s,a). It cannot equal the low order s and equals the high order ar exactly when lcm(s,a)=a. After dividing positions by r, all candidate multiples are at integer ranks. No integer rank occurs inside any open unit-rank category. Consequently every low position in the same category has exactly the same high neighbors for a fixed low type. The doubled-integer representative formula is therefore exact for all r, not a sampled approximation. High–high edges are exact after cancelling r.

The processing order visits each actual node once, with highs before lows at a shared position. H retains every future high conflict; B retains every still-relevant category/type conflict induced by selected highs; L retains every future low conflict induced by selected lows. Each selected edge is recorded until its other endpoint is processed. Cleared H bits and past-category B bits cannot affect any future decision. Low stream shifts preserve the exact ordinal position of every low neighbor, including across high boundaries. Two histories with the same masks have identical legal continuations. Thus skip/take maxima over these masks give the exact graph optimum. Extra low bits beyond the final finite position are harmless when taking the final maximum.

## Why the certificate is a uniform proof

Every prime r≥5 has exactly one residue rho in {1,5,7,11,13,17,19,23} modulo 24. Write r=24t+rho. The t<3 bases cover every remaining prime. Composite values checked in the base suite are statements about the same abstract low/high graph only, not group claims with omitted extra divisors.

Within band k, the phase k·rho mod24 is independent of t. The first 24t positions comprise t identical 24-position transition cycles; the residue tail has rho−1 positions. High weights are 24a·t+a·rho−1. Thus all parameter dependence is affine and there are no hidden variable-length transitions after the repeated cycles.

At the n=2 base, coefficients and values at t=3 are propagated separately. For each source history, a coefficient bound and an anchor bound imply the whole affine upper bound for t≥3. Taking these two maxima along different histories can only weaken the bound; it cannot invalidate it.

For cycle induction, the complete domain t≥3, 2≤n<t is

  (t,n)=(3,2)+u(1,0)+v(1,1), u=t−n−1≥0, v=n−2≥0.

Every possible cycle route is checked at the vertex and both rays. These are exactly the three coefficient/anchor inequalities required to prove F_source(t,n)+reward≤F_target(t,n+1) throughout this unbounded cone. Reachability closure is checked explicitly: every output state must occur in the next bound vector. Induction gives the certified bound for every 2≤n≤t. The n=t exits and fixed tails/boundaries propagate to the next band using the same valid affine-envelope argument. The final two bounds imply 1,104t+46rho−23=46r−23 for every t≥3.

The coefficients may have been discovered empirically. Discovery does not justify the theorem; the independently checked finite induction does. This is a genuine uniform integer argument, not extrapolation and not the known-failing pure weighted-clique-cover route.

## Attainment, global upper bound, equality, and count

The D8 seed orders have directly checked scores 12 and 10. The escape seed has proper stabilizers containing reflections labeled 1 and 3, which generate D8. The cyclic odd-factor order of three order-r cosets has score 5r−3: strict partial cosets have trivial stabilizer, and the two internal completed-coset boundaries have stabilizer Cr. Whole-fibre score accounting gives the actual global constructions 76r−24 and 70r−24. In the escape construction, proper checkpoints supply the odd factor and both generating reflections. Subtracting the final contribution 24r−1 also proves the graph bound is attained at 46r−23.

An unrestricted optimizer cannot have B=G because the sharp escape score is smaller by 6r. For B proper, choose a maximal J containing it. Every proper stabilizer lies in J and is contained in the active local-prefix stabilizer in its right J-coset. The exact local accounting has only nonnegative deficits. Every proper subgroup belongs to the accepted abelian or arbitrary-two-Sylow scope. Its local value therefore gives the required unrestricted upper 76r−24.

Equality forces every local order optimal and every deficit zero. At the first completed coset, the global prefix is J-invariant, so every other not-yet-completed coset is empty. Repeating proves consecutive complete coset blocks. The accepted local classifications supply the full recursion. Conversely such recursive orders attain the bound; the first completed block has stabilizer J, and the trapping lemma puts all proper stabilizers in J. Hence B=J and the top is unique, preventing double-counting between top-subgroup choices. The one C4, two C2², and unique index-3 and index-r choices give exactly the stated count coefficients.

## Scope and unresolved work

This establishes the entire p=3 slice for D8×Cp×Cr, with r any other odd prime. By symmetry it also covers pairs with r=3. The remaining distinct-odd-prime family therefore has 5≤p<r after reordering. No upper theorem for that two-variable family is established here. Nor does this settle arbitrary nonabelian three-prime groups, larger exponents in this three-prime setting, or all finite nilpotent groups.

The accepted r=5 and r=7 results remain unchanged and become special cases. The exact r=7 fractional-cover obstruction 905/3>299 remains valid; this proof uses integral finite-state induction. All prior abelian, pairwise-permutable, and arbitrary-two-Sylow results are dependencies, without new novelty credit. Historical priority and the retained full external-source/EFK comparison gaps remain open.

No external write was performed by this reviewer.
