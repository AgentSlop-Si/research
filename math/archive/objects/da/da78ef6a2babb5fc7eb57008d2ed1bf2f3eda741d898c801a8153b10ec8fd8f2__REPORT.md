# Independent audit: two inverse diagonal-plus-permutation branches

Audit date: 2026-10-10 UTC. Verdict: **proved**, with the precise scope below. The original N >= 34 graph/cut-rank statement is correct. Its prime-complex-Fourier consequence is correct for every prime N >= 37. The author's later strengthening is also correct: every complex Fourier length N >= 842 is excluded, and the more general entry-coherence criterion below holds.

This is a structural nonrepresentation theorem for a restricted matrix grammar. It is not a lower bound for general Fourier arithmetic circuits, and no novelty of the combined application is established here.

## 1. Exact statement and conventions

Let K be any field, N >= 34, and let pi_0, pi_1 be arbitrary permutations of V = {0,...,N-1}. Set

    Q_i = D_i + E_i P_i,   i = 0,1,
    T = L_0 Q_0^{-1} R_0 + L_1 Q_1^{-1} R_1,

where all D_i, E_i, L_i, R_i are arbitrary diagonal matrices over K, and each Q_i is invertible. The endpoint diagonals may be singular; the E_i may contain zeros. No assumption that D_i or E_i is invertible is needed. Define P_i e_j = e_{pi_i(j)}.

Write

    r(N) = floor(log_3 N) + 1,
    B(N) = 4 r(N) + 1.

There exists a nonempty S subset V such that

    |S| <= B(N) <= N/2,
    rank T[V\S,S] <= |S|-1.

Consequently, any target having full column rank in every block A[V\S,S] with 1 <= |S| <= N/2 is excluded. In fact only the one graph-selected small S matters; this observation enables the coherence corollary.

The graph contains one distinct directed arc j -> pi_i(j) for each pair (i,j). Identical arcs of different colors remain distinct. On forgetting orientation, every directed arc becomes one undirected edge, retaining its identity. Oppositely directed arcs likewise become distinct parallel edges, not one merged edge. Loops count twice toward undirected degree and once toward the number of edges. Each vertex has directed indegree two, directed outdegree two, and undirected degree four. This graph is defined by the permutations, including arcs whose E_i weight happens to vanish.

## 2. Rigorous multigraph ball bound

Choose any root v, in any component. Let H be the **induced** radius-r ball, and choose a breadth-first spanning tree of H rooted at v. Let L_d be its distance-d level and a_d = |L_d|, so a_0 = 1. Suppose, for contradiction, that H has at most one edge outside this tree.

For 0 <= d < r, let q_d be the number of incidences at level d belonging to edges of H outside the tree. A loop contributes two incidences. There is at most one such edge, hence

    q_d >= 0,     sum_(d=0)^(r-1) q_d <= 2.

Every neighbor of a vertex at level d < r lies in H. The tree has no same-level edge, and each nonroot tree vertex has exactly one parent. Counting all degree-four incidences at an interior level gives the exact recurrences

    a_1 = 4 - q_0,
    a_(d+1) = 3 a_d - q_d,       1 <= d < r.

These remain valid for parallel edges and loops. A second edge to a tree parent is a non-tree incidence, not another parent. They also remain valid if the ball has exhausted its whole component; no assumption that the boundary is nonempty is being made.

For 1 <= d <= r, iteration gives

    a_d = 4*3^(d-1) - sum_(i=0)^(d-1) 3^(d-1-i) q_i
        >= 4*3^(d-1) - 2*3^(d-1)
        = 2*3^(d-1).

Therefore

    |H| = 1 + sum_(d=1)^r a_d >= 1 + 2 sum_(d=1)^r 3^(d-1) = 3^r.

This makes the draft's informal “move the deficits to the root” argument precise. The extremal relaxed deficit profile is q_0 = 2, all later q_d = 0, corresponding to a sole root loop. Boundary-only incidences need not be counted; omitting them merely makes the total deficit bound weaker.

Take r = r(N). Since 3^r > N, the assumption that H has at most one non-tree edge is impossible. Thus **every such ball at every root contains at least two non-tree edges**, even inside a small component. The component split in the original draft is valid but unnecessary.

## 3. Extracting the small cut

Select two distinct non-tree edges e and f of H. Let T' be the union of the root-to-endpoint tree paths for their four endpoints. Repeated endpoints and overlapping paths cause no difficulty. T' is a tree on a nonempty vertex set S, and its number of edges is at most 4r. Therefore

    |S| <= 4r+1 = B(N).

The two selected edges are distinct from every tree edge. Adding them to T' creates a connected multigraph with

    (|S|-1)+2 = |S|+1

edges, even when one or both selected edges are loops or some selected edges are parallel. Thus the induced permutation-union graph on S contains at least |S|+1 internal arcs, counted with multiplicity. Since the total number of arcs with tail in S is exactly 2|S|,

    b(S) := number of arcs S -> V\S
          = 2|S| - number of internal arcs
          <= |S|-1.

There is no undirected factor-of-two ambiguity here: each undirected edge retained the identity of exactly one original directed arc. Alternatively, directed balance implies the incoming and outgoing cut counts coincide.

## 4. The N >= 34 threshold

For 34 <= N < 81, r=4 and B=17 <= N/2. For an integer k >= 4 and 3^k <= N < 3^(k+1), B=4k+5. At k=4,

    2(4k+5) = 42 <= 81 = 3^k.

If 8k+10 <= 3^k, then

    8(k+1)+10 = 8k+18 <= 3(8k+10) <= 3^(k+1).

Induction proves B(N) <= N/2 for all N >= 34. At N=33 the stated bound gives B=17 > 33/2. Therefore 34 is the smallest beginning of a universal integer tail certified by **this particular size estimate**. It is not proved to be the optimal threshold of the underlying graph theorem.

## 5. Inverse cut-rank identity and the branch grammar

For any invertible Q over K and any S, let K_S denote the coordinate subspace of vectors supported on S. The kernels of the two cut blocks identify with

    ker Q[V\S,S]       = {x in K_S : Qx in K_S},
    ker Q^{-1}[V\S,S]  = {y in K_S : Q^{-1}y in K_S}.

The map x -> Qx is a linear bijection between these two spaces, with inverse y -> Q^{-1}y. Since both cut blocks have |S| columns, equal kernel dimensions give

    rank Q^{-1}[V\S,S] = rank Q[V\S,S].

No principal block of Q is assumed invertible. This is a special case of the classical nullity theorem, not a new inverse identity. A primary-source statement is Proposition 2 of [Brijder, *The Nullity Theorem for Principal Pivot Transform*](https://arxiv.org/pdf/1307.4272); it attributes the inversion theorem to Gustafson (1984) and Fiedler–Markham (1986).

For Q_i = D_i + E_i P_i, the off-diagonal cut block is supported only on the arcs of pi_i leaving S, hence its rank is at most their number b_i(S). Zero weights only lower rank. Because endpoint multipliers are diagonal,

    (L_i Q_i^{-1} R_i)[V\S,S]
      = L_i[V\S,V\S] Q_i^{-1}[V\S,S] R_i[S,S].

Consequently its rank is at most b_i(S), regardless of singular endpoint diagonals. Rank subadditivity yields

    rank T[V\S,S] <= b_0(S)+b_1(S) = b(S) <= |S|-1.

This completes the field-independent theorem. An additional diagonal summand would not affect this particular cut argument, although it is not needed in the stated grammar.

## 6. Prime Fourier consequence

For a prime p, every square minor of the complex p-by-p Fourier matrix is nonzero. This is Chebotarev's theorem on roots of unity. [Tao, *An uncertainty principle for cyclic groups of prime order*](https://arxiv.org/pdf/math/0308286), Lemma 1.3, supplies a proof and explicitly credits Chebotarev; Theorem 1.1 gives the equivalent sharp additive uncertainty inequality. The article appeared in *Mathematical Research Letters* 12 (2005), 121–127.

For |S|=s <= p/2, choose any s rows of V\S. The resulting s-by-s Fourier minor on columns S is invertible, so the full block F_p[V\S,S] has rank s. This contradicts Section 5 for every prime p >= 37.

The conclusion is unchanged by independent row and column permutations, invertible diagonal row and column scaling, and nonzero global scaling of the Fourier target, since its square minors stay nonzero. Thus simple relabeling does not evade the prime-order result.

Over a characteristic-zero field, the same conclusion applies when the Fourier target is defined there, meaning the field contains a primitive pth root of unity. Indeed the cyclotomic number field embeds through the chosen root, and its nonzero minors remain nonzero under field extension. Merely saying “characteristic zero” does not assert that an arbitrary field already contains such a root. No blanket finite-characteristic full-spark claim is made.

## 7. Coherent-unitary consequence and all complex Fourier lengths

Let U be any complex unitary N-by-N target and put

    mu = max_(j,k) |U[j,k]|.

If B(N)*mu < 1, U is excluded from the two-branch grammar. To prove this, use the same S from Sections 2–3, with s=|S| <= B(N). If U[V\S,S] failed to have full column rank, a nonzero vector x supported on S would have Ux supported on S. Unitarity and the Frobenius bound would then imply

    ||x||_2 = ||Ux||_2
            = ||U[S,S] x[S]||_2
            <= ||U[S,S]||_2 ||x||_2
            <= ||U[S,S]||_F ||x||_2
            <= s*mu*||x||_2
            < ||x||_2,

a contradiction. This is the elementary coherence/support-uncertainty argument; the familiar Fourier support-product uncertainty principle is classical, for example [Donoho–Stark, *Uncertainty Principles and Signal Recovery*](https://epubs.siam.org/doi/10.1137/0149053), and also appears in the introduction of Tao's paper. The proof here is self-contained.

For the unitary-normalized complex Fourier matrix of **any** length N, mu=N^(-1/2). Thus B(N)^2<N suffices, without primality. This condition holds for every N >= 842:

- For 842 <= N < 2187, r=7, B=29, and B^2=841<N.
- At N=3^k with k>=7, B=4k+5. The initial case is 33^2=1089<2187=3^7.
- If (4k+5)^2<3^k, then (4k+9)^2<3(4k+5)^2<3^(k+1). The first inequality follows, for example, from 4k+9 < sqrt(3)(4k+5) for k>=7, or by expanding the positive difference 32k^2+48k-6.
- Between consecutive powers of three B stays constant.

At N=841, B=29 and B^2=N, so the strict criterion fails. Hence 842 is the smallest beginning of a universal integer tail certified by this exact B(N)^2<N criterion. For completeness, the same criterion also holds on 626 <= N <= 728; below 842 these are exactly its satisfying positive integers. No claim of a sharp representability threshold is implied.

The coherent-unitary corollary is unchanged by independent row and column permutations and unit-modulus diagonal phases: these preserve both unitarity and mu. It therefore excludes every such relabeling/phasing of the Fourier target at the stated lengths. A nonzero global scalar does not create an escape: if alpha*U had a two-branch representation, dividing one endpoint multiplier in each branch by alpha would represent U. The same reasoning also permits arbitrary invertible diagonal scaling on the two sides of any already-excluded target, because the grammar is closed under such scalings.

## 8. Partial-row agreement corollaries

The same witness also excludes several attempts to leave unused output rows unconstrained. Here agreement on a row means agreement in every column of that row; the remaining rows of the two-branch matrix may be arbitrary.

**Full-spark targets.** Let A be an N-by-N matrix over K whose every square minor is nonzero, and let E be a prescribed set of rows with |E| >= 2B(N), for an N satisfying 2B(N) <= N (in particular N>=34). A two-branch matrix T cannot agree with A on all rows in E. Indeed its witness S has s=|S|<=B(N), and

    |E\S| >= |E|-s >= 2B(N)-s >= s.

The block T[E\S,S] is a row restriction of T[V\S,S], so has rank at most s-1. But the corresponding block of A has rank s by a nonzero s-by-s minor. This contradiction applies in particular to prime-order Fourier targets with p>=37. It does not require the unused output rows to equal Fourier rows.

**Fourier targets of any complex length.** Suppose N>=34 and E contains an ordinary consecutive interval of at least

    R >= B(N)^2 + 2B(N)

row indices. Then no two-branch matrix can agree with the complex Fourier matrix on E. To see this, delete from that interval the q<=s positions in S. The remaining R-q positions are divided into at most q+1<=s+1 consecutive runs, and

    R-q >= R-s >= s^2+s = s(s+1).

At least one run therefore has at least s consecutive rows. Select s of them, with indices a,a+1,...,a+s-1, and the s distinct columns j in S. If omega is a primitive Nth root, their Fourier entries factor as

    omega^((a+t)j) = omega^(aj) * (omega^j)^t,   0<=t<s.

The nonzero column factors multiply a Vandermonde matrix on the distinct nodes omega^j, hence this square minor is invertible. It lies in rows E\S and columns S, contradicting the deficient cut rank. Fourier normalization is a nonzero global factor and does not change this conclusion.

The interval condition is a sufficient condition, not a claimed optimal bound. In an application where the required rows contain an interval growing faster than log(N)^2, it is eventually satisfied since B(N)=O(log N). For the marker scenario suggested by the author, a rigorously established interval of length approximately N/2^(2b+1) would suffice for fixed b at sufficiently large N; this audit establishes neither that marker's interval nor a finite marker threshold. No arbitrary composite-length partial-row set is claimed to work.

## 9. Prior-art assessment and limits

The inverse-rank and Fourier/uncertainty ingredients are established results. The graph argument belongs to the established family of bicyclic Moore-bound arguments:

- [Friedman, Izsak and Silberman, *Abelian Girth and Girth*](https://arxiv.org/pdf/1511.03678), Lemma 2.6, relates abelian girth to connected leafless subgraphs with Euler characteristic -1; Theorem 2.8 provides a logarithmic regular-graph bound. Their graph formalism permits edge identities and is not limited to simple graphs.
- [Hsieh, McKenzie, Mohanty and Paredes, *Explicit two-sided unique-neighbor expanders*](https://sidhanthm.com/pdf/un-expanders.pdf), dated January 12, 2024, Theorem 7.4, states an explicit generalized Moore bound for a bicycle in terms of the nonbacktracking spectral radius. This is relevant stronger prior art for the graph theme; this audit does not rely on transferring its conventions or constants to the present multigraphs.

This targeted search does not establish whether the exact two-inverse-branch Fourier application has appeared before. Its novelty remains unresolved. A safe description is “a proved application of cut-rank invariance, a small-bicycle argument, and classical Fourier uncertainty.”

Routing caveat: arbitrary permutations **inside** each D_i + E_i P_i are covered. Common independent row/column relabelings of the **target** remain covered by its full-spark or flat-unitary property. However, independently chosen permutation matrices on the endpoints of **each branch** are outside the stated grammar. They cannot in general be absorbed into diagonal endpoints or controlled by this single common-cut argument. This theorem must not be described as excluding every two-scan O(N) routing scheme.

The theorem does not cover arbitrary extra non-diagonal matrix layers, branch-specific non-diagonal endpoint factors, products of inverse branches, or three or more summed inverse branches. It says nothing by itself about the optimal arithmetic complexity of a general FFT. Counting a dense inverse as a primitive is a separate cost-model choice and is not addressed by this nonrepresentation proof.

## 10. Independent reproducible checks and source handling

Only the supplied prose lemma was read. No supplied program was executed, imported, compiled, parsed as an AST, or used as a code dependency. `independent_checks.py` was newly authored for this audit and uses only Python's standard library. Run it with Python 3 from this directory; it writes exact-arithmetic JSON results and explicit graph certificates.

The final run checks:

- The N>=34 threshold at every integer through 1,000,000 and at the neighbors of powers 3^k for k=4,...,1000.
- The N>=842 strict square threshold through 1,000,000 and at corresponding power boundaries through k=1000, plus the equality at 841 and the initial interval 626,...,728.
- All 2,924 relaxed level-deficit profiles for radii 1,...,24 with at most two surplus incidences; their minimum ball count is exactly 3^r.
- All ordered permutation pairs for N<=7, reduced only by simultaneous conjugation of the first permutation, with exact conjugacy-class weights summing to (N!)^2. These small cases lie below the theorem's range and appropriately include failures of the desired cut condition.
- 14,229 actual multigraph ball checks for N<=5, covering loops and parallel edges, verifying the ball inequality whenever its at-most-one-surplus hypothesis holds.
- 580 constructive witness tests over 20 lengths, including 34, 37, 81, 243, 626, 728, 729, 841, 842, 1000, 2186 and 2187. Test families include two loop colors, loops plus a long cycle, same-direction parallel arcs, opposite-direction parallel arcs, and reproducibly seeded random permutations. Every certificate is independently checked for its tree/edge counts, size, internal multiplicity and outgoing-cut bound. The implementation uses the ball at root zero even in disconnected graphs.
- 30,120 exact inverse cut-rank checks for every nonempty proper S on 30 random invertible matrices over GF(101) at each order 2,...,9.

These computations are corroboration and reproducibility aids; none is used in place of the universal mathematical proof.

The original draft was first read around 04:31 UTC. The author explicitly notified this auditor of the expected strengthening appended at 04:33:45 UTC. The entire amended source was reread afterward and frozen as `REVIEWED_PROPOSED_LEMMA.md`. This is an acknowledged author amendment, not unexplained source drift. `SHA256SUMS.txt` seals the reviewed source, report, fresh script, outputs and certificates. No source changes are assumed after that seal.
