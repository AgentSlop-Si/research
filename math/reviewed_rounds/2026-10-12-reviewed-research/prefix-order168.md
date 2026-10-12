Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: f55c8477d3ef5fe35938790bf5a5f809b23fbfdea7d09937d1e14c63368dcb69

---

# Independent review of the order-168 D8 gate

11 October 2026 UTC. Decision: ACCEPT every stated mathematical conclusion within its exact scope. No mathematical repair is required.

## Result

For D8×C3×C7, the sharp unrestricted maximum is 508 and the sharp full-escape maximum is 466. The complete maximizing-order classification, unique top subgroup B, and labeled count are valid consequences of the finite escape theorem and already accepted proper-subgroup results. The uniform constructions are valid lower bounds for all distinct odd primes.

The method obstruction is a separate exact result: the specified escape conflict graph has integral optimum 299 but fractional clique-cover optimum 905/3. Consequently this graph's pure unbranched weighted-clique covers cannot establish 299, even after ordinary integer rounding. This does not refute the suggested escape formula for other prime pairs.

## 1. Independence and immutable inputs

The complete author candidate was frozen in source_snapshot before execution. Every one of its 25 declared payloads matched its byte count and SHA-256. The five dependency snapshots matched their named originals byte-for-byte. All 27 files in the candidate directory were preserved and rechecked after execution. The candidate SHA256SUMS was checked completely. The independently checked author ZIP has 27 members, valid CRCs, and exactly the same member bytes as the frozen candidate.

The candidate verifier and proof were read as text. No candidate, inherited, or uploaded mathematical program was executed or imported. independent_check.py was newly authored for this review. It uses standard-library integer and rational arithmetic, reconstructs graph conflicts by enumerating permitted intervening integers, and constructs D8 through its permutation action on a square. It reads certificates and witnesses only as JSON data. It uses no LP or MILP solver and trusts no discovery-time clique list or optimum.

Nine in-memory corruption controls were rejected: missing graph population, repeated split child, missing leaf coverage, forged selected score, a violated dual singleton inequality, a negative dual coefficient, a removed cover coefficient, a false stabilizer, and an incorrect B order. No source file was mutated by these controls.

## 2. Uniform constructions and score accounting

The order of C_pr is a concatenation of p distinct cosets of its order-r subgroup. A strict partial coset has trivial stabilizer inside the prime-order subgroup. The unique partially occupied coset forces trivial projection to the quotient C_p. At a proper complete-coset boundary, the subgroup C_r is the entire stabilizer because a nonempty proper subset of the prime quotient has trivial translation stabilizer. The final prefix has stabilizer C_pr. Thus its score is (p−1)(r−1)+(pr−1)=2pr−p−r.

The general fibre identity in the candidate is valid for arbitrary finite direct-product factors. A strict partial fibre has a unique partially occupied outer coordinate, so any stabilizer has trivial outer projection and is exactly the active local stabilizer. At a boundary the stabilizer is the full inner factor times the outer-prefix stabilizer. Replacing the local full-fibre contribution at each boundary gives

    Z_(H×K)=|K|Z_H+|H|Z_K.

This identity includes the final global prefix once; it does not double-count local full prefixes. The D8 orders d and e have scores 12 and 10. For e, the proper stabilizers are {0},{0,1},{0},{0,3},{0},{0,3},{0}; the two reflections generate D8. The two displayed fibre constructions therefore attain 28pr−8p−8r and 26pr−8p−8r, respectively. In the escaping construction, the first completed odd fibre contributes all C_pr to B and the two- and four-fibre boundaries contribute the generating reflections. The full-escape assertion is proved directly for every pair, rather than inferred from numerical stabilizer orders.

These arguments prove only lower bounds uniformly. The candidate consistently retains that restriction.

## 3. Structural constraints and scale transfer from order 120

Coprime powers split each subgroup into its D8 and cyclic odd components. All subgroup orders divide 168 and every prefix stabilizer order also divides the prefix size, by the free action. The complete list of maximal subgroups consists of three order-84 subgroups, one order-56 subgroup, and one order-24 subgroup. They are normal of prime index. Every subgroup of one of these orders is maximal.

The normal-prime-index trapping lemma works for any nonempty proper invariant prefix, including any nonempty proper union of right cosets. Earlier prefixes have nonempty proper quotient support and cannot admit a nontrivial prime-quotient translation. Later proper prefixes contain one full coset; an outside stabilizer would move it through all quotient cosets and force the full group. Thus every proper-prefix stabilizer lies in the normal maximal subgroup. Full escape necessarily excludes the orders 24,56,84. No converse is needed or asserted.

The closure/core lemma is valid with odd factor C21 and indeed with any cyclic factor coprime to a finite q-group. For stabilizers L×C_d and R×C_e, the q-power component orders are comparable by divisibility even if the subgroups are not comparable. If |L|≥|R|, C_e T_i is an intermediate set invariant under L×C_lcm(d,e). If |L|<|R|, the intersection of C_d-translates of T_j is intermediate and invariant under R×C_lcm(d,e). The invariant subgroup has order lcm(|S_i|,|S_j|) in both cases. Equality at either endpoint forces exactly the candidate's endpoint permission. Centrality gives the required invariance and no product LR, subgroup permutability, persistence, or accumulated orbit is assumed.

The order-120 argument therefore transfers as a symbolic compatibility lemma. Its old finite cover does not transfer as an upper certificate; the new finite certificate is checked separately here.

## 4. Complete graph and exhaustive integer branch certificate

Fresh generation gives exactly 288 permitted nodes (j,s), with demand s−1, and 4,421 conflict edges. Same-size nodes conflict. For unequal sizes, the checker enumerates integers in the closed interval, tests divisibility by lcm(s,t), and enforces both endpoint restrictions. This is independent of the candidate's floor/ceiling implementation.

Any actual escaping order yields an independent set whose weight is its proper-prefix score. Trivial stabilizers contribute zero and the full prefix is excluded. The finite graph can contain unrealizable independent sets, which only weakens this upper envelope.

At each split, an arbitrary independent set either excludes the selected live vertex or includes it. The latter case deletes that vertex and every conflict neighbor and adds its integer weight. These two cases are disjoint and exhaustive. The checker reconstructs the remaining live population and the actual selected vertex set from the root. It verifies that selected vertices are independent and have no edge to any live vertex. It also verifies valid record references and that every record is reached exactly once, excluding omissions, shared subtrees, unreachable records, and cycles.

All 53 records pass: 26 binary splits, 27 leaves, maximum depth six. At the leaves, all 3,888 supplied cliques contain distinct live vertices and all 28,864 clique pairs are actual conflicts. Every coefficient and scale is a positive integer, every remaining node demand is covered, and all totals match. The maximum leaf scale is 18.

In fact, every leaf has selected score plus fractional cover weight exactly 899/3=299⅔. The score of an independent set is an integer, hence is at most 299. This strict bound below 300, applied at every leaf and propagated through the exhaustive split tree, proves root bound 299. Adding the full-prefix contribution 167 gives 466.

The escape witness supplies an actual independent set of weight 299. Therefore both the graph's integral optimum and the escaping proper-prefix optimum equal 299. No optimization solver's claimed optimality is used.

## 5. Fractional obstruction: every clique constraint

The packing has 288 nonnegative integral coefficients with scale three and 98 positive entries. The independent checker generates every clique in the induced positive-support graph by extending each increasing tuple with all larger vertices adjacent to all its members. This generates every clique exactly once: any nonempty clique has a unique largest vertex and a unique shorter prefix. The resulting 688 cliques, including the empty clique, all have scaled weight at most three.

For an arbitrary clique of the full 288-node graph, its positive-support intersection is one of those checked cliques and has the same packing weight. Nonnegative zero-weight entries therefore introduce no unchecked constraint. This establishes every clique inequality, not merely the inequalities for an author-supplied list of cliques or maximal cliques.

The weighted packing objective is exactly 905/3. Finite weak duality makes every fractional clique cover at least this large. The separately verified matching cover has 226 cliques, scale 30, total scaled weight 9,050, and 2,374 directly checked conflict pairs. Every node demand is covered and the minimum scaled slack is zero. Its value is exactly 905/3, proving equality of the fractional optimum.

Since 905/3>299 and its floor is 301, no different pure unbranched clique-weight assignment on this same graph can prove the desired integer target. Branching plus integrality succeeds at this finite pair. The conclusion does not rule out stronger graphs, additional realizability constraints, inequalities beyond clique covers, or a group-theoretic uniform argument.

## 6. Actual group witnesses and supplementary controls

D8 was freshly represented by the eight permutations of a square, composed directly. The direct product with C21 supplies the group table. Identity, regular rows, and all 4,741,632 associativity triples pass. Both witness files are permutations of all 168 labels and agree exactly with the stated fibre constructions.

All 168 prefix stabilizers of each witness were recomputed as actual sets of group elements. Both complete lists, scores, generated proper-stabilizer subgroups, and B orders match. The maximum witness has score 508 and |B|=56. The escape witness has score 466 and B equal to the entire 168-element group. The latter's proper-prefix independent set has weight 299.

For the two witnesses, all 3,656 pairs of nontrivial proper stabilizers also pass explicit geometric closure/core checks: 2,555 lower closures and 1,101 upper cores. These check actual intermediate sets, containment, subgroup invariance, divisibility, and endpoint restrictions.

Fresh exhaustive enumeration of all 40,320 D8 orders gives maximum 12 with 2,432 optimizers and escape maximum 10 with 3,072 escaping maximizers among 9,216 escaping orders. An additional 12 recursive order-168 orders all attain 508 and recover a maximal B and its consecutive blocks. Twelve further random orders, together with those recursive orders, give 26,768 compatibility checks and 25 maximal-stabilizer trapping checks. These supplementary controls corroborate the structural proofs and do not replace the complete finite certificate or establish any additional uniform upper bound.

## 7. Unrestricted maximum, classification, and count

The escaping upper bound 466 is strictly below the explicit score 508. Thus every possible order above 466 has B proper, and in particular every unrestricted optimizer has B proper. Choose a maximal J containing B. Every proper subgroup is already in accepted scope: its proper D8 component is abelian, or its full D8 component is accompanied by at most one odd prime factor.

At each insertion the global proper stabilizer lies in J and in the stabilizer of the active local J-coset prefix. Summing all local prefix contributions exactly once, and replacing the final local stabilizer J by G, gives

    Z_G=Σ_C Z_J(local order)+168−|J|−Σ_(j<168)(|L_j|−|S_j|).

Every displayed deficit is nonnegative. Accepted local maxima are 212 for each order-84 top, 132 for order 56, and 52 for order 24. In each case [G:J]V(J)+168−|J|=508. This proves the unrestricted bound without requiring an additional unrestricted graph cover.

Equality forces local optimality and zero deficits. The first completed coset then makes the prefix J-invariant, and all other cosets must be empty because none has completed. Induction on successive completions forces consecutive whole blocks. Accepted local classifications finish the recursion. Conversely, normal-prime-index blocks with optimal interiors have zero deficits and attain 508. The first completed block has stabilizer J while every proper stabilizer lies in J, proving B=J and uniqueness of the top.

The reviewer independently enumerated all identity-containing D8 subsets and tested multiplication closure, obtaining ten subgroups. Their products with the four subgroups of C21 give all forty subgroups. Maximal subgroups were recovered by inclusion, and every one of the forty candidate counts was recomputed with exact integers. The count for a fixed top of index k is k! A(J)^k. Unique B prevents overlap between tops; representative choices introduce no additional multiplicity. The candidate's four-term formula and its stated 101-digit total both match the fresh recurrence. This is a consequence of classification and accepted local counts, not an enumeration of 168! orders.

## 8. Closed and open scope

Closed: the concrete order-168 maximum, sharp escaping maximum, every-optimizer classification, unique top, labeled count, the explicit uniform lower constructions, and the exact fractional-cover obstruction at (3,7).

Open here: the uniform upper bounds for D8×C_p×C_r with distinct odd primes, a uniform integrality or stronger-constraint argument, arbitrary nonabelian three-prime groups, and all finite nilpotent groups. The 53-record tree is not extrapolated. Earlier order-120 and proper-subgroup results remain unchanged and receive no new discovery credit. No external historical novelty or literature-comparison gap is closed.

No original proof, certificate, or review was altered. No Sheet or GitHub write was performed. This is independent project mathematical review, not external peer review or proof-assistant certification.
