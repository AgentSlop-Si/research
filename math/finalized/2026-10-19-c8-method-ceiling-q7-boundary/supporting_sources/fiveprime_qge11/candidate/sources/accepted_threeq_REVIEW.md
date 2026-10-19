# Independent review: the complete order-3q interior exclusion

Date: 2026-10-19 UTC.

## Verdict and binding

**PASS, without a required repair.** For every prime q>3, no binary N-by-N matrix R at N=3q and q<d<2q makes the original fixed-phase matrix D[r,c]=R[r,c] zeta^(rc) satisfy D*D=dI. The proof closes the whole interior, not merely the initial clique reduction. Combining it with the separately accepted small-degree and upper-range exclusions, the accepted d=2q endpoint, and divisor sufficiency gives exactly the allowable positive degrees {1,3,q,3q}.

This is an existence classification by degree. It is not a classification of all supports at those degrees, a theorem for every odd semiprime, or a resolution of the wider mixed-prime problem. The wider M-SPARSE-DEFECT owner remains TO RESEARCH, priority 42. No external record is changed by this review.

The verdict binds the frozen candidate `/workspace/shared/sparse_threeq_interior_20261019_1220`:

- Manifest SHA-256: `597d0de53a54cdc28f8d3d4130ce0df5acfd790b51c11cbcbf10956214ebb8ed`
- Report SHA-256: `adb4b382dad3de602d802214b5b548a107683158777c1421156b21be4965c3d8`

The mathematical review below is independent of the candidate program. No candidate or historical research code was imported or executed. The fresh review programs separately recompute both original Gram orders and original inverse-model witnesses, then audit the frozen candidate's retained data.

## 1. Fixed phases, both Grams, and cancellation

The CRT idempotents e_3=q(q^(-1) mod 3) and e_q=3(3^(-1) mod q) satisfy the required identities modulo 3q. For the actual row and column indices r=a e_3+b e_q and c=u e_3+v e_q,

    rc=au e_3+bv e_q modulo 3q.

Thus alpha=zeta^(e_3) and beta=zeta^(e_q) give precisely zeta^(rc)=alpha^(au) beta^(bv). This is a relabeling, not a replacement Fourier pairing or a weighted CRT model. The identity works for every primitive choice of zeta, including both residue classes of q modulo 3.

Squareness and d>0 make D invertible when D*D=dI; hence DD*=dI too. The argument therefore has both row norms and column norms, as well as row orthogonality. Its later uses of column regularity are justified by the original condition, not by a relaxed one-Gram model.

The order-q balance lemma is the exact minimal-polynomial statement, including coefficients equal to zero. The primitive binary cancellation proof is correct: the 2(q-1) displayed products span a cyclotomic field of that same degree and so form a basis. Reduction forces the coefficient grid to be A_u+B_v with integer A and B. Both cannot vary because their ranges would add to at least two, incompatible with binary entries. Thus a primitive zero support is a union of full three-column fibers or full q-lines.

The minimum nonempty overlap statement is also correct for every nonzero row difference, not only primitive ones. At odd order a still simpler check is available: one root cannot sum to zero, and two roots could cancel only if their ratio were -1, impossible in a group of odd order. This verifies the crucial order-three pairs used in the last stages. No arbitrary-phase inference is made.

## 2. Simpliciality really gives one or two cliques

Within a fixed group G_a of q rows, a pair has uniform local intersections over the q three-column fibers. Since d<2q, the constant is zero or one. An edge therefore means overlap q, and a nonedge means completely disjoint supports.

Every row has a fiber of weight at most one because its total weight is below 2q. A zero there makes the row isolated. A singleton there forces all neighbors to share its single coordinate, so any two neighbors are adjacent. Every vertex is simplicial. A connected graph with every vertex simplicial is complete: a shortest path between nonadjacent vertices would otherwise have a middle vertex with two nonadjacent neighbors. The components are consequently cliques.

Three components would give three disjoint supports of size d>q in 3q columns, which is impossible. This derives at most two cliques in each residue group. It says nothing about full square blocks of the entire bipartite support graph, and does not conflict with the accepted connected order-eight example.

## 3. The local-to-global incidence step, including all q=5 cases

For n>=4 three-coordinate restrictions with pairwise intersection one, some restriction is a singleton. Otherwise only the three distinct doubletons could occur. All restrictions contain the singleton's point, and any additional coordinate belongs to exactly one row. If the union has k coordinates, incidence is exactly n+k-1.

The same identity holds for n=2 by inclusion-exclusion and for n=1 even when its single restriction is empty. For n=3, the only exception is the three-doubleton triangle occupying all three coordinates. In a split group it would leave the other component empty. The other component has at least two rows whenever q>=5 and one component has size three, except the nonexistent q=4 case. It is therefore nonempty in every fiber, excluding that triangle. In particular, the smallest split 3+2 at q=5 is covered.

For one clique, local incidence is at most q+2, yielding d<=q+2. For two cliques of sizes n,m, disjoint local unions give incidence q+k_1+k_2-2<=q+1 in every fiber. Since d>q, saturation forces d=q+1 and equality in each fiber. This is a valid passage from a global total to local equality because every local count has the same upper bound and their sum attains its total.

The singleton case is essential. The singleton can have local weight zero, one, or two. Nevertheless saturation leaves degree q-1 on the large component's common coordinate and degree one on both other coordinates, so the degree triple is (q-1,1,1). There is no premature singleton baseline assumption. For n,m>=2 the two unions use one and two coordinates, yielding (n,m,1) up to permutation.

Another essential global step is made correctly in the candidate. A saturated local singleton-plus-K_(q-1) configuration can contain a tripleton in the large component. Local incidence alone does not exclude it. Each nonsingleton row, however, contains its component's baseline in all q fibers and has total degree q+1, so it has only one extra overall. That rules out its tripletons. The singleton cannot be a tripleton because the other component is locally nonempty. Thus every row of a split group has no full three-column fiber, exactly as used later.

The independent q=5 dynamic program retains all 15 saturated local weight patterns for singleton plus K4 and imposes degree six on each of the five rows over five fibers. The layer state counts are 15,104,284,141,1. Its sole terminal state has no tripleton. This is a control of the global inference, not a replacement for its proof.

## 4. The q+2 branch is fully excluded

At d=q+2 every group is a single clique and each fiber has contributions (q,1,1). If h groups use a particular column as baseline, its full degree is 3+h(q-1)=q+2, giving h=1. The three group baselines are pairwise disjoint in every fiber.

Choose a row extra that lies on another group's baseline. All q rows of that group meet it. Their intersections with the chosen row lie inside the union of two two-element extra sets and therefore have size at most four. Among those rows there are q-1 primitive partners. Since q>=5, four is strictly less than q; their nonempty primitive overlaps must be exactly one full three-column fiber.

The chosen row can have at most one such full fiber because it has only two extras. At that fiber, the other group's two off-baseline coordinates are each used by at most one row, so at most one partner can contain the full fiber. The q-1>=4 primitive partners cannot all do so. All inequalities remain strict at q=5.

## 5. All mixtures at q+1 are correctly handled

At q+1 a single-clique group has one extra per row, contributes q on its baseline, and contributes zero or one elsewhere. Every split group contributes positively in every column.

- Exactly one single-clique group: either split group contributes at least one to each of its baseline columns, forcing degree at least q+2.
- Exactly two: their baselines differ. The split group must contribute one at both of them, so its sizes are 1,q-1 and its high column is the third coordinate. Each single-clique group must place exactly one extra on that third coordinate in every fiber. Their row-to-extra-fiber maps are bijections. Matching a fiber gives two rows intersecting in exactly one column. This contradiction includes equal-b, order-three row pairs.
- Exactly three: a column without a baseline has degree at most three, and one with two baselines has degree at least 2q. Since 3<q+1<2q, every column has exactly one baseline group. Every extra then meets another group's baseline. The two row supports meet in one or two positions, forbidden for every nontrivial difference.

The only residual is therefore three split groups. No mixture was omitted.

## 6. The all-split residual is closed, rather than assumed away

Suppose a row contains no q-line. It already contains no full three-column fiber. Hence its intersection with every primitive partner in another group must be empty by the binary cancellation lemma. At any supported column, each other group can consequently contribute only its one row with the same b coordinate. Column degree q+1 then forces at least q-1 contributions from the row's own group.

The local degree pattern (n,q-n,1) has maximum q-1. Achieving q-1 requires sizes 1,q-1 and occurs at exactly one column per fiber. Only q columns can therefore have this multiplicity, but the row needs q+1 such columns. Contradiction. Every row contains a full q-line and, because its degree is q+1, consists of that line plus one extra.

Different baseline lines give intersection at most two and must therefore be disjoint. A same-group component, whose adjacent rows have overlap q, has a single baseline line. Its two components have distinct baselines. Every group extra is on the third line: placement on the other component's baseline would violate disjointness. The q extras are distinct, since repetition within a component gives overlap q+1 and repetition across components violates disjointness. Each column on the missing line gets exactly one extra from that group.

Choose any extra column. If its line is a baseline for no group, its degree is three, below q+1. Some other group must therefore have a row with that baseline line, producing a nonempty overlap of at most two with the chosen row. This final contradiction is valid in the original Fourier phases and closes the entire interior.

## 7. Fresh independent controls

The completed `independent_checks.py` run uses integer cyclotomic remainders for the Grams and SymPy rational algebraic fields for matrix inverses. It imports no candidate or historical research program. Standard error in the completed run is empty.

- Exact CRT checks cover all row-column pairs and all primitive-root multipliers at q=5,7,11,13,17.
- The 32,768 binary order-15 supports have exactly 38 primitive zero supports, all parallel-line unions. A further 120,192 checks verify nonvanishing of all one- and two-column overlaps for the tested odd orders and every nontrivial character.
- Local component multisets are exhausted at q=5,7,11,13, including every split size and singleton weights zero, one, and two. All 32,768 labeled five-row local restrictions are inspected for the simpliciality implication. The singleton-plus-K4 global budget is checked separately as described above.
- Fourteen positive masks include divisor degrees at N=15,21,33, the connected (8,4) mask, and its connected (24,12) odd CRT lift. Connectivity is recomputed, not trusted as a label.
- Sixteen negative masks at q=5,7,11,13 cover the q+2 all-clique branch, the q+1 balanced all-split branch, the exactly-two-single-clique branch, and the singleton-empty-fiber branch. Every one is regular of the claimed degree and passes all same-group row Grams. Both complete original Grams nevertheless fail. Every failure residue is retained.
- Five proper original inverse-model reconstructions at (N,d)=(15,1),(15,3),(15,5),(21,7),(8,4) verify both mask Grams, B_tilde=(H-D)*/(N-d), both inverse products for M_tilde=B_tilde^(-1), every inverse-row and inverse-column budget N-d, E_tilde=M_tilde-H, and both error Grams dI. Full rational coefficient matrices are saved.

The independent controls evaluate 20,764 entries in each full Gram order, 1,180 entries in each inverse-product order, and 1,180 entries in each error-Gram order. They corroborate the symbolic proof; no full equality-mask census is claimed.

`DEVELOPMENT_NOTES.md` records two corrected checker-development mistakes. Neither changed the candidate proof or affected the completed run. The failed preliminary logs are preserved to make their status explicit.

## 8. Frozen-candidate audit and original-model consequences

The separate `audit_candidate_data.py` treats the candidate solely as data. It checks all 25 manifest entries and all 13 source bindings against the original local bytes, both before and after the audit. Both checks match the binding above.

It independently recalculates every entry of both Grams for all 18 candidate positive masks and 9 candidate countercontrols. All retained nonzero residues and every zero-by-character-order count match. For the three candidate original-model witnesses it decodes the ascending rational coefficient arrays, verifies the B and E definitions, both mask Grams, both inverse products, both error Grams, and all inverse row and column support sizes. It does not trust success flags or execute `verify_interior.py`. This audit covers 20,521 entries in each full Gram order and 514 entries in each inverse-product and error-Gram order.

The accepted equality criterion and attainment theorem then give, for newly excluded q<d<2q,

    Delta_(3q,3q-d) > sqrt(d/(3q)).

The accepted general bound specializes correctly to

    Delta_(3q,3q-d)^2 >= d/(3q) + 1/[30q d^(2q-3)],

because phi(3q)=2(q-1). This is an inherited nonsharp bound, not a new sharp optimum or rate. The d=N divisor control remains only a mask control; s=0 is not represented as an admissible inverse-model witness.

The primitive cancellation attribution is inherited from the accepted source packet, with a self-contained proof independently checked here. This review makes no historical-priority or novelty claim and performs no external publication, repository, registry, status, or owner update. All writes are confined to this new local review packet.
