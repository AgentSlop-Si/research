Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 87f85cc3d2bf1e642b2c8e448c2f2d8ad4b8b6462febf691c3945f6a7b48f5d5

---

# Independent review of the D8 × C3 × C5 prefix certificate

11 October 2026 UTC. Decision: ACCEPT all five bounded mathematical conclusions. No mathematical repair is required.

## Outcome and exact scope

For G=D8×C3×C5, with all nonempty prefixes scored by |S_j|−1, including the full prefix exactly once, the maximum is 356. When the stabilizers of proper prefixes generate all G, the exact maximum is 326. Every score-356 ordering is a recursive maximal-subgroup right-coset block order; its unique top is B, and its labeled count is

    133607109033492884009664101615026762044984137577546008808652800.

The finite certificate closes a genuine bounded case outside the previously accepted pairwise-permutable scope. It does not close the general three-prime or all-nilpotent problem. No historical novelty conclusion is drawn.

## Independence and source binding

The complete candidate directory was copied to a frozen source_snapshot. Every one of its 22 declared payload members was checked against its byte length and SHA-256; the complete SHA256SUMS file also verified. Each of the six mathematical dependency snapshots was compared byte-for-byte with its named original and with its declared hash. The previously accepted arbitrary two-Sylow statement and review, the abelian review, and the project-scope audit were read. Their conclusions are used only within their accepted scope.

The candidate verifier and group-control source were inspected as inert text. Neither was executed or imported. The reviewer independently authored independent_verify.py, which reads the frozen certificates and witnesses only as JSON data. It uses standard-library exact arithmetic, enumerates permitted intervening multiples directly rather than copying the floor/ceiling conflict test, and constructs D8 from the eight permutations of a square. No linear-programming output or discovery-time maximal-clique enumeration is trusted.

The accepted proof is THEOREM.md, 15,704 bytes, SHA-256 683ade7bb67695bc6a968e3bd1eed442a18249f5b949a39413baf4b87a022603. SOURCE_VERIFICATION.json supplies all remaining hashes and exact dependency identities.

## 1. Normal prime-index trapping

Section 2.2 is correct for any finite group and any normal prime-index subgroup K. A nonempty proper K-invariant prefix is a union of a nonzero proper number of right K-cosets. For earlier nonempty prefixes, their quotient supports are nonempty subsets of that proper support. An element outside K acts on G/K by a nonidentity translation of the prime-order quotient, hence as one cycle on all quotient cosets. Such an element cannot preserve a nonempty proper support.

For a later proper prefix, one whole K-coset from the earlier prefix is present. If an outside element stabilized the later prefix, its successive powers would carry this whole coset through every quotient coset. The prefix would then be G, a contradiction. Thus every proper-prefix stabilizer is contained in K on both sides of the checkpoint.

No persistence, nesting or normality of the smaller stabilizers is assumed. The argument applies when the checkpoint is any proper union of K-cosets, rather than just a single coset.

Every subgroup of D8×C15 splits as L×C_d. All maximal subgroups have orders 60, 40 or 24 and are normal of prime index: three come from the three index-two subgroups of D8, one removes C3, and one removes C5. Conversely every subgroup of any of those three orders is maximal. Full escape therefore excludes stabilizer orders 24, 40 and 60 at every proper prefix. This necessary exclusion is all the escape upper certificate requires; it is not asserted to characterize full escape.

## 2. Closure/core compatibility and endpoint strictness

Section 3 is correct for H×C_m, with H any finite q-group and gcd(q,m)=1. Subgroup splitting gives S_i=L×C_d and S_j=R×C_e. The orders α=|L| and β=|R| are comparable powers of q; the actual subgroups need not be comparable or permutable.

When α≥β, the union U=C_e T_i lies between T_i and T_j. Centrality of C_e makes it L-invariant, and invariance under both cyclic factors makes it invariant under L×C_lcm(d,e). This subgroup has order M=lcm(|S_i|,|S_j|), so |U| is a multiple of M. If U=T_i, then C_e stabilizes T_i, forcing e|d and M=|S_i|. If U=T_j, its order-M invariance forces M to divide |S_j|; since |S_j| also divides M, equality follows.

When α<β, the intersection U=∩_(c∈C_d)cT_j contains T_i and lies in T_j. Centrality makes U invariant under R and under C_e; translation permutes the intersected sets, giving C_d-invariance as well. Its invariant subgroup R×C_lcm(d,e) again has order M. Equality with the left endpoint forces M=|S_i|, and equality with the right endpoint forces d|e and M=|S_j|.

These implications give precisely the candidate's permitted endpoint rule. The proof does not form LR, assume LR=RL, or use an accumulated orbit. The nonpermuting reflection subgroups of D8 therefore create no missing step.

## 3. Complete finite upper certificates

The node population contains every pair (j,u) with 1≤j<120, 1<u<120, u|j and u|120, subject only to the declared forbidden orders. A nontrivial stabilizer of any actual proper prefix must supply one such node, by the free left action. Trivial stabilizers contribute zero and need no node; the full prefix is handled separately. Different nodes at the same prefix size conflict. All other conflicts use the proved necessary compatibility condition.

Thus every actual ordering gives a graph independent set with weight exactly its proper-prefix score. A clique intersects this set in at most one node. Summing nonnegative clique weights that cover every node demand u−1 gives an upper bound by elementary finite weak duality. Unrealizable independent sets can only weaken this upper envelope, so graph realizability and exact graph optimization are unnecessary.

Fresh exact verification gives:

- Unrestricted population: all 225 nodes, 121 supplied cliques, 1,719 pairwise conflict checks, total integer clique weight 237, and nonnegative coverage slack at every node.
- Escape population: all 218 nodes after excluding 24, 40 and 60, 139 supplied cliques, 1,586 pairwise conflict checks, weight scale 20, scaled total 4,140, hence proper-score bound 207, and nonnegative scaled coverage slack at every node.

The minimum coverage slack is zero in both certificates. All node IDs are valid and distinct inside each clique; every clique weight and the scale is a positive integer. The listed complete populations are exactly the independently regenerated populations. Every potential conflict in each supplied clique was tested by directly enumerating multiples of M in [i,j] with the specified endpoint restrictions.

Adding 119 gives total upper bounds 356 and 326. These finite inequalities are proof components, not random controls. They do not depend on a solver's status, floating-point output, optimality claim or clique-discovery completeness.

## 4. Actual attaining orders and full-prefix accounting

All 120 labels in each witness are distinct and exhaustive. Every one of the 120 prefix stabilizers in each file was freshly reconstructed as a set of actual group elements. Both complete stabilizer lists, their sizes, their accumulated proper-prefix generated subgroup B, and their scores match the saved JSON exactly.

The C15 order a=(0,3,6,9,12,1,4,7,10,13,2,5,8,11,14) has score 22. The D8 order d=(0,4,2,6,1,5,3,7) has score 12, and e=(0,1,2,3,5,6,4,7) has score 10. The proper stabilizers of e are exactly {0}, {0,1}, {0}, {0,3}, {0}, {0,3}, {0}; the two reflection subgroups generate D8.

Putting D8 fibres in the residue order a, each internally ordered by d, gives 15·12+8·22=356 and B of order 40. Putting C15 fibres in the D8 order e, each internally ordered by a, gives 8·22+15·10=326 and B of order 120. Both serialized orders also agree exactly with independent reconstruction of those mathematical descriptions.

At a strict partial-fibre prefix, there is a unique partially occupied outer coordinate, so a stabilizer must have trivial outer projection and equals the active local stabilizer. At a boundary the stabilizer is the product of the whole fibre group and the outer-prefix stabilizer. Replacing the full local-fibre contribution at each boundary by this actual product contribution proves the displayed score identities. The final global prefix is included once, with no overcount of local full-prefix terms.

The first C15 fibre is itself a proper prefix, contributing the C15 subgroup to B. The two- and four-fibre boundaries supply the generating D8 reflections. This confirms full escape directly, rather than inferring it from absence of forbidden stabilizer orders or from the compatibility graph.

## 5. Complete optimizer classification

The strict escape bound 326<356 makes B proper for every optimizer. Choose a maximal subgroup J containing B. It is normal of prime index. Every proper subgroup of G belongs to accepted local scope: a proper D8 component is abelian, while a full D8 component with proper odd part has zero or one additional prime divisor. Thus the accepted abelian or arbitrary two-Sylow classification applies to J, not merely a conjectural cardinality-only value formula.

At each insertion, the proper global stabilizer S_j lies in J and is contained in the stabilizer L_j of the active local J-coset prefix. Each local prefix is counted once at its active insertion. At the final global insertion, J is replaced by G. Therefore the exact deficit identity is

    Z_G=Σ_cosets Z_J(local order)+120−|J|−Σ_(j<120)(|L_j|−|S_j|).

Every deficit is nonnegative. Local maxima are 148 for the three order-60 tops, 92 for the order-40 top, and 52 for the order-24 top. Consequently [G:J]V(J)+120−|J|=356 for every possible J.

Equality forces every local order to maximize and every proper deficit to vanish. At the first completed J-coset, the local stabilizer is J, so the global prefix is J-invariant. Because no other coset has completed, all other cosets must be empty. The first entire block is therefore consecutive. Repeating at later proper completions forces all subsequent blocks; the final coset occupies the remaining positions. Accepted local classifications supply the complete recursion.

Conversely, a consecutive normal-prime-index coset construction with optimal local orders has each proper global stabilizer equal to the active local stabilizer. At boundaries an outside element would cycle the prime-order quotient; inside a block it would move the unique partially occupied coset. Hence no such outside element stabilizes a proper prefix, all deficits vanish, and score 356 is attained.

The first full block has stabilizer J, and every proper stabilizer lies in J, so B=J. This proves unique top, rather than only the existence of some maximal containing subgroup.

## 6. Count and count scope

For a fixed maximal J of prime index p, the labeled count is p! A(J)^p. The cosets are distinct, local choices are independent, and right translation supplies an equivariant identification of each coset with J. Changing the representative only changes the identification, not the available labeled sequences. The final ordering recovers its blocks, and the recovered unique B separates distinct tops.

D8 has one C4 maximal subgroup and two C2² maximal subgroups. Together with the index-three and index-five tops this gives

    A(G)=2 A(C4×C15)²+4 A(C2²×C15)²
         +6 A(D8×C5)³+120 A(D8×C3)⁵.

The reviewer independently enumerated the ten actual D8 subgroups by testing all identity-containing subsets for multiplication closure, formed all forty product subgroups, found maximal subgroups by inclusion rather than by the candidate's type formula, and evaluated the subgroup recurrence with arbitrary-precision integers. Every one of the candidate's forty subgroup counts matches. The local counts are:

- A(C4×C15)=494655307311578131971535011840
- A(C2²×C15)=3705762430664346663882986618880
- A(D8×C5)=235279707678588272640
- A(D8×C3)=203047403520

The resulting A(G) is 133607109033492884009664101615026762044984137577546008808652800. This is an exact consequence of the proved classification plus accepted local counts. It is not an exhaustive enumeration of 120! orders.

## 7. Additional fresh controls

The independent D8 and order-120 multiplication tables passed all 1,728,512 associativity checks, identity checks and row-permutation checks. Exhaustive enumeration of all 40,320 D8 orders gives maximum 12 with 2,432 optimizers, and full-escape maximum 10 with 3,072 escaping maximizers among 9,216 escaping orders.

For the two order-120 witnesses, all 1,964 nontrivial-stabilizer prefix pairs were checked not only for numerical compatibility but also by explicitly constructing the lower closure or upper core, testing containment, its claimed subgroup invariance, cardinality divisibility, and both endpoint restrictions. These comprise 1,394 lower-closure and 570 upper-core checks.

Thirty further full order-120 controls were generated independently: fifteen recursive optimal orders and fifteen random labeled orders. They supplied 16,544 further compatibility checks and fifteen maximal-stabilizer trapping checks. All fifteen recursive orders attain 356 and recover a maximal B with the expected consecutive blocks. These supplementary tests corroborate the lemmas; they are not a substitute for their symbolic proofs or for the complete finite covers.

## 8. Closed gate and remaining work

Closed: this concrete D8×C3×C5 instance, maximum 356, sharp full-escape maximum 326, every-optimizer classification, unique top, and the labeled count.

Still open here: a uniform sharp bound for D8×C_p×C_r with distinct odd primes; a universal three-prime envelope; arbitrary products with two or three nonabelian Sylow factors; and all finite nilpotent groups. The candidate's generalized compatibility lemma is valid, but one finite cover does not supply a uniform cover family. The suggested full-escape value V−2pr for the variable-prime family remains a conjectural upper bound here, with a valid construction giving the corresponding lower bound.

The all-abelian and stronger pairwise-permutable theorems were already accepted project scope and are reused without new discovery credit. Existing historical-priority and external full-source gaps remain unchanged. No original proof, candidate file, Sheet or GitHub entry was altered by this review. This is an independent project mathematical acceptance, not external peer review or proof-assistant certification.
