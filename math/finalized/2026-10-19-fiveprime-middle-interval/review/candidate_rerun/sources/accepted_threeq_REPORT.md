# Complete interior exclusion and classification at order 3q

Date: 2026-10-19 UTC. Owner M-SPARSE-DEFECT, priority 42. Proof candidate; independent review required. No novelty or priority claim.

## 1. The theorem and its exact scope

Let q>3 be prime, N=3q, and zeta any primitive N-th root of unity. There is no binary matrix R of order N for which

    D[r,c] = R[r,c] zeta^(rc),       D*D = d I_N,

with q<d<2q. Consequently, combining this theorem with the previously accepted small-degree exclusion, endpoint d=2q exclusion, strict-upper exclusion, and divisor construction, the possible positive degrees at order 3q are exactly

    d in {1,3,q,3q}, equivalently d divides 3q.

The new argument is the entire formerly unresolved open interval, uniformly for every prime q>3. It does not rely on a census. It uses the actual binary supports and exact Fourier phases. In particular, the clique structure below is derived for a graph inside each of three row-residue groups; it is not a full-square-block assumption for the full support graph. The accepted connected (8,4) countercontrol to such an assumption remains valid.

Both Gram conditions are retained. Since D is square and d>0, D*D=dI makes D invertible and gives DD*=dI. Thus all row degrees and all column degrees are d. The proof uses row orthogonality, row degrees, and column degrees explicitly.

## 2. Exact CRT coordinates and cancellation lemmas

Put e_3=q(q^(-1) mod 3) and e_q=3(3^(-1) mod q), taken modulo N. These satisfy e_3+e_q=1, e_3e_q=0, and e_3^2=e_3, e_q^2=e_q modulo N. Relabel the actual rows and columns by

    r=a e_3+b e_q,       c=u e_3+v e_q,
    a,u in Z/3,         b,v in Z/q.

With alpha=zeta^(e_3) and beta=zeta^(e_q), the unchanged original pairing is exactly

    zeta^(rc)=alpha^(au) beta^(bv).

Here alpha has order 3 and beta has order q. Write G_a for the q rows with first coordinate a, F_v for the three columns with second coordinate v, and L_u for the q columns with first coordinate u. No CRT weighting or phase substitution is made.

We record three elementary facts.

**Prime-order balance.** If integers k_v satisfy sum_v k_v beta^(hv)=0 with h nonzero modulo q, then every k_v is equal. This is the minimal-polynomial statement for 1+X+...+X^(q-1). The same statement applies at order 3.

**Primitive binary cancellation.** If a binary set T of columns has zero sum against a character nontrivial in both CRT coordinates, then T is a union of full F_v fibers or a union of full L_u lines. For a self-contained proof, relabel both coordinates by the two nonzero character multipliers. The products alpha^i beta^j, 0<=i<2 and 0<=j<q-1, span the cyclotomic field and have its dimension 2(q-1), so are a basis. Reducing the vanishing sum gives

    epsilon_(i,j)-epsilon_(i,q-1)-epsilon_(2,j)+epsilon_(2,q-1)=0.

It follows, also on the boundary coordinates, that epsilon_(u,v)=A_u+B_v for integer-valued A and B. If both varied, their ranges would each have length at least one, and the range of their sum on the Cartesian product would have length at least two, impossible for a binary array. One is constant, which is precisely one of the two stated parallel-line forms.

**Minimum nonempty overlap.** A nonempty binary support whose sum vanishes against any nontrivial row-difference character at order 3q has at least three entries. For character order 3 or q this follows from prime balance; for order 3q it follows from the preceding lemma. In particular, no intersection of size one or two can occur between distinct orthogonal rows. This fact applies to all row differences, including the order-three differences with equal b coordinates.

The primitive cancellation fact is classical in content. The accepted source packet credits Lam and Leung and de Bruijn. Its elementary proof is included only to make the argument self-contained, without a new vanishing-sum claim.

## 3. Deriving the same-group clique structure

Assume q<d<2q. For distinct rows r,s in one G_a, prime-order balance says that

    |S_r intersect S_s intersect F_v|=k(r,s)

is independent of v. Since the whole intersection has size at most d<2q, k(r,s) is either zero or one. Define a graph on the q rows of G_a, with an edge precisely when k(r,s)=1. Thus adjacent rows meet in exactly one column in every fiber and have total overlap q; nonadjacent rows have disjoint full supports.

Every row has at least one fiber in which it has at most one entry, because its total degree is less than 2q. If it has zero entries there, it is isolated in this graph. If it has exactly one entry there, every neighbor contains that same column. Any two neighbors therefore meet in that fiber, so are themselves adjacent. Every vertex has a clique as its neighborhood.

It follows that each connected component is a clique: if a connected component were not complete, a shortest path between nonadjacent vertices would include a vertex with two nonadjacent neighbors. There are at most two components. Indeed, three components would supply three pairwise disjoint row supports of size d>q inside only 3q columns.

This proves, rather than assumes, that each G_a is either one clique or the disjoint union of two nonempty cliques.

## 4. Local incidence counts, including singleton components

A family of n>=4 binary subsets of a three-element set with every pair intersecting in exactly one point has a common point. If none were a singleton, a tripleton could not coexist with another set of size at least two, and the only possible sets would be the three distinct doubletons. There cannot be n>=4 such sets. A singleton therefore exists and its point is in every set. Every other used coordinate occurs in exactly one member, since two members sharing it would intersect twice. If the union has k coordinates, the total incidence count is exactly n+k-1, and at most n+2.

For n=2 the same incidence identity holds by inclusion-exclusion. For n=3 it holds unless the three sets are the three doubletons, in which case their union is all three coordinates. For n=1 the identity n+k-1=k holds even for an empty set.

### One clique

If G_a is one clique, q>=5 permits the preceding common-point argument in every fiber. Let its unique common coordinate in F_v be its baseline. Each row contains all q baseline columns. All off-baseline entries are extras, and each off-baseline coordinate is used by at most one row. Thus there are at most two extra incidences per fiber and

    qd <= q(q+2), hence d<=q+2.

### Two cliques

Suppose G_a has components of sizes n,m with n+m=q. Their used-coordinate sets in every fiber are disjoint. The exceptional three-doubleton configuration for a component of size three cannot occur: it would use all three coordinates, forcing the other component empty in that fiber. A component of size at least two cannot be empty because its members have pairwise intersection one; if the other component had size one, q would be four, which is excluded.

Thus, writing k_1,k_2 for the two local union sizes, the total incidence in every fiber is exactly

    (n+k_1-1)+(m+k_2-1)=q+k_1+k_2-2 <= q+1.

It follows that d<=q+1. Since d>q, necessarily d=q+1. Equality holds in every fiber, so the two local unions exhaust the three coordinates.

Every nonsingleton component has a common baseline in each fiber. Its rows therefore have q baseline entries and exactly one extra entry over all fibers. No such row contains a whole three-column fiber. A singleton component also cannot contain a whole fiber, because the other component is nonsingleton and has a nonempty local union. Consequently no row of a split group contains any full F_v.

The three column degrees contributed by this group in each fiber are a permutation of

    (n,m,1).

When n,m>=2, the components use respectively one and two coordinates: the two baselines have multiplicities n,m and the remaining coordinate is a single extra. When n=1, m=q-1, the large component has one baseline of multiplicity q-1; every other coordinate belongs either to one extra of that component or to the singleton row, so both have multiplicity one. This explicitly permits the singleton to have zero, one, or two entries in a fiber. No singleton baseline is being presumed.

We have now reduced the entire interior to d=q+1 or q+2. A two-component group is possible only in the former case.

## 5. Excluding d=q+2

Every G_a must be one clique. Equality in its incidence bound forces it to use both off-baseline coordinates once in every fiber. Each row has exactly two extras in total. The group contributes degree q on its baseline coordinate and degree one on both others.

For a fixed column let h be the number of groups for which it is a baseline column. Its full column degree is

    hq+(3-h)=3+h(q-1)=q+2,

so h=1. The three group baselines are therefore distinct in every fiber.

Choose a row r and one of its extra columns c. That column is the baseline of a different group G_a'. Every row s in G_a' contains c. Since the two group baselines are disjoint, their common support is contained in the union of the two sets of extras and has at most four entries. For the q-1 rows s whose b coordinate differs from r's, the row-difference character is primitive. Because 4<q, their nonempty overlap cannot contain a full q-line. Primitive binary cancellation forces it to be one full three-column fiber.

Such an overlap requires r and s both to contain all three columns of that fiber. Row r has only two extras, so can contain only one full fiber. All q-1 primitive partners must therefore be tripletons at that same fiber. But in G_a' each off-baseline coordinate occurs in only one row, so at most one row of G_a' can be a tripleton there. This contradicts q-1>1. Thus d=q+2 is impossible.

## 6. Excluding single-clique groups at d=q+1

At this degree, a one-clique group has q baseline entries and exactly one extra per row. Its contributions to column degrees are q on each baseline and either zero or one off the baseline. A two-clique group has positive contributions in every column, as proved above.

There are four possibilities for the number of one-clique groups.

**Exactly one.** Its baseline columns already receive q entries, and each of the other two groups contributes at least one. The resulting degree is at least q+2, contradicting d=q+1.

**Exactly two.** Their baselines must be distinct in each fiber, as 2q>q+1. At either baseline column the split group contributes at least one, so it must contribute exactly one and the other one-clique group contributes zero. The split group can have only one column of multiplicity greater than one in that fiber; hence its component sizes are 1 and q-1. That multiplicity q-1 occurs on the third column. The two one-clique groups must each contribute one at this third column to reach q+1. Therefore each of those groups has exactly one extra in every fiber, all on the common third column. Every row has exactly one extra, so extra fiber is a bijection from its q rows to the q fibers. Match two rows from the two groups having the same extra fiber. Their baselines are disjoint, neither has an extra on the other's baseline, and their only intersection is their common extra column. A singleton intersection cannot have zero Gram for any nonzero row difference. Contradiction.

**Exactly three.** A column with no baseline contributes at most three entries, less than q+1; a column with at least two baselines contributes at least 2q, more than q+1. Thus exactly one group has its baseline there. Choose any row r and its extra column, whose baseline group is different. Any row s in that group intersects r nontrivially. The baselines are disjoint and there is only one extra per row, so the intersection has at most two entries. Again this cannot vanish for any nonzero row difference.

Thus the only remaining possibility has all three groups split into two cliques.

## 7. Closing the all-split case at d=q+1

By Section 4, no row contains a full F_v. Suppose a row r also contains no full L_u. Its intersection with any row in either other group whose b coordinate differs from r's has a primitive zero sum. The primitive binary lemma says that this intersection is a union of full F_v or full L_u. Neither can be contained in r, so all these intersections are empty.

Consequently, for each column c in r's support, either other group can contribute at most one entry: its single row whose b coordinate equals r's. Since c has total degree q+1, its contribution from r's own group is at least q-1.

In a split group the fiber column contributions are (n,q-n,1). They are at most q-1, and a contribution q-1 is possible only for component sizes 1,q-1. There is then exactly one such high-degree column per fiber, so only q such columns in the entire group. But r uses q+1 columns, each of which has just been forced to be one of these q high-degree columns. This contradiction shows that every row contains a full q-line.

Every row therefore has the form

    S_r = L_(u(r)) union {e_r},       e_r outside L_(u(r)).

Two rows with different baseline lines have an intersection of size at most two. By the minimum-overlap lemma, they must be disjoint. Adjacent rows in a same-group clique have overlap q, so all rows in each component have the same baseline line. The two components have distinct baseline lines because their supports are disjoint.

In a fixed group, all q extras lie on its third, missing baseline line. An extra cannot lie on the other component's baseline, since that would violate disjointness. The q extras are distinct: within one component a repeated extra would give overlap q+1 instead of q, and between components it would violate disjointness. Thus each of the q columns on the missing line receives exactly one extra from the group.

Take any extra column c of any row r. If none of the three groups used c's line as a baseline, each group would contribute exactly one extra there, giving column degree three. This is less than q+1. Some other group therefore has a row s with that line as its baseline. Then r and s have different baseline lines and meet at c, while their intersection has size at most two. This contradicts orthogonality once more.

The all-split case is impossible. This completes the exclusion of every q<d<2q.

## 8. Combining accepted boundaries; original inverse-row consequence

The accepted results already show that d<q permits only 1 or 3, that d=2q is impossible, and that 2q<d<3q is impossible. The complementary-divisor construction supplies 1,3,q,3q in the original phases: for any divisor d of N, put m=N/d and take

    R[r,c]=1 iff floor(r/d)=c modulo m.

Rows within one block have the same supported d-column coset and cancel by a complete d-point character sum; rows in different blocks have disjoint supports. Both Grams equal dI.

Combining those accepted results with Sections 2-7 gives the stated exact degree classification for every N=3q, q>3 prime. This classification concerns existence by degree; it does not classify all support geometries at the allowed degrees.

Using only the separately accepted equality criterion and attainment theorem, for every newly excluded integer q<d<2q the original simultaneous inverse-row-sparsity model has

    Delta_(3q,3q-d) > sqrt(d/(3q)).

Substituting into the already accepted quantitative gap bound yields

    Delta_(3q,3q-d)^2 >= d/(3q) + 1/[30q d^(2q-3)].

This is an inherited bound composed with the new nonexistence theorem, not a new sharp error formula or a new gap method. The wider mixed-prime problem, other odd-semiprime interiors, exact nonsharp optima, and sharper rates remain open. The owner remains TO RESEARCH, priority 42.

## 9. Fresh controls, sources, and limitations

The fresh verifier in this packet imports or executes no historical research code. It computes the original cyclotomic polynomial and exact root-power reductions, evaluates both complete Gram orders, checks the original CRT identity, and retains explicit positive and negative masks. The accepted connected (8,4) mask is copied as data and its odd CRT lift at (24,12) is also checked. Proper-divisor masks are reconstructed in the original inverse-row model with exact field arithmetic, and both inverse products, inverse-row/column budgets, and both error Grams are checked. See RESULTS.json for the completed run and controls for the full witnesses.

The all-split near-mask control at degree q+1 is explicit. In G_a, the q-1 rows with b nonzero use baseline L_a, and the row b=0 uses baseline L_(a+1). Each row adds column (a+2,b). Every row and column has degree q+1, and every same-group row Gram vanishes. Nevertheless cross-group Grams fail in the original phases. This checks that same-group clique structure and degree regularity alone are insufficient; the primitive and small-overlap arguments are essential.

The endpoint degree-2q near-mask, with R[r,c]=1 iff r mod 3 differs from c mod 3, is retained as a separate control: it passes all order-q and primitive differences but fails the order-three pairs. A degree-preserving switch in a divisor mask checks that regularity alone does not prove either Gram.

Source files and their SHA-256 hashes are recorded in SOURCE_BINDINGS.json. Accepted endpoint and mixed-prime packets are treated as data, and the combined classification is explicitly separated from the new interior argument. This report does not claim historical originality. No external service, repository, registry, status table, owner status, or priority is changed. All writes are confined to this new local packet. A manifest and seal bind the completed candidate submitted for independent review.
