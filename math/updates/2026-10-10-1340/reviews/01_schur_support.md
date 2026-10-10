# Schur v31: superconcentrator support audit

Date: 10 October 2026. Verdict: accept the rank/flow implication, its properly scoped Schur-rectangle application, and the generic-weight existence argument. Accept the two quoted bounded-depth asymptotic orders as classical edge-count theorems. Correct the interpretation of depth, work, fields, and what a successful half-rectangle construction would establish.

## 1. Source and review boundary

The reviewed source is `fft_superconcentrator_interface_v31.zip`, 529,688 bytes, SHA-256 `fdc0772ed669d6c486298bead2a80039ba85d6f96b0532af1537af687d58601f`. Its CRC check and all 15 manifest entries pass. The embedded v30 ZIP has SHA-256 `ce2fba707468da831596f7bd74653ac59221a43707559ccf80724d89f4bde916`, matching the earlier audited source. The standalone v31 checkpoint was also read. The mathematical source is preserved under [source statements](../sources/schur/README.md); private conversation access is not part of this public export.

The research text, prior-art note, ledger, test definitions, implementation, runner, saved results, and independent-verifier text were inspected. No uploaded program or runner was executed or imported. The accompanying controls were written afresh. Source-reported “10/10” remains a source report; the independent controls below have their own record.

This audit also reads the accepted v30 proof and its separate completion review. Their claims are preserved, not recounted as new v31 discoveries. No remote files were changed. No Fourier algorithm, numerical-stability result, bit-complexity bound, or literature-wide novelty certification is established here.

## 2. Correct model and terminology

Use a finite scalar linear DAG over a field K, with n distinct source terminals and n distinct sink terminals; these two sets are disjoint. Every other node stores one scalar linear combination of its predecessors. Each nonzero scalar coefficient is an edge weight. Sources have no incoming edges, sinks have no outgoing edges, and all preprocessing constants are independent of the fresh input.

For inputs i and outputs o, let T[o,i] be the sum of products of weights over directed i-to-o paths. The graph may have unbounded fan-in and fan-out. No coefficient-magnitude restriction or positivity assumption is needed.

“Totally nonsingular” means every square submatrix has nonzero determinant, including every one-by-one minor. This is the property used throughout. “Full spark” is often used elsewhere only for maximal-column-minor independence; for a square matrix that weaker convention would require merely invertibility. Invertibility alone does not imply superconcentrator support: the identity circuit is an immediate counterexample. The source defines its intended stronger meaning, but future statements should use “totally nonsingular.”

Zero-weight edges may be deleted. Keeping them produces a harmless support supergraph, but deleting them is preferable for a minimal edge ledger. Negative weights and exact cancellation are allowed. Parallel edges may be consolidated; if their weights sum to zero, remove the resulting edge.

## 3. Rank versus vertex-disjoint paths

For terminal subsets I and O, let nu(I,O) be the maximum number of directed paths from I to O that are disjoint at every vertex, including terminals. Then

    rank T[O,I] <= nu(I,O).

Here and below paths may match the selected inputs to outputs in any permutation. A superconcentrator does not require a separately prescribed matching.

Proof: let S be a smallest vertex separator between I and O, permitting terminal vertices in the cut. The vertex-capacitated version of Menger's theorem gives |S|=nu(I,O). Set unselected input values to zero. Cut the incoming edges of every vertex of S and supply its original scalar value externally. In a topological evaluation of the remaining graph, the selected outputs are linear functions of these |S| values: all other selected-input-to-output paths have been interrupted. Thus the transfer factors through K^S, proving the rank bound. This argument also handles a separator meeting one path more than once; it does not require S to be an antichain.

If T is totally nonsingular, every k-by-k selected block has rank k, and hence every pair of equally sized terminal subsets admits k disjoint paths. This is exactly superconcentrator support. The converse is false for fixed weights: a complete two-input/two-output bipartite graph has the connectivity property, but assigning every edge weight one gives the rank-one all-ones matrix.

The statement is classical linear-circuit information flow. A second proof follows from the determinant/path identity; [Talaska's Theorem 2.5](https://arxiv.org/pdf/1202.3128), specialized to acyclic graphs, gives the signed sum over vertex-disjoint path families. In that specialization the cycle denominator is one. This audit uses no cyclic denominator graph as a substitute for an execution DAG.

## 4. Exact Schur consequence

In the direct-coordinate same-branch setting already audited in v30, suppose M=T+R and T is lower triangular in a specified common coordinate order. Let m=floor(N/2), I be its first m coordinates, and J its last m coordinates. These sets are disjoint and T[I,J]=0. Therefore

    R[I,J] = M[I,J].

If M is totally nonsingular, so is this m-by-m rectangle. Every scalar linear DAG actually evaluating that rectangle has m-superconcentrator support, relative to those m inputs and m outputs. The graph may contain additional internal vertices. Unselected inputs are set to zero, unselected outputs are ignored, and irrelevant vertices can be pruned.

For complex prime N, Fourier total nonsingularity follows from Chebotarev's theorem; see [Tao, Lemma 1.3](https://arxiv.org/pdf/math/0308286). Independent row/column permutations and nonzero diagonal gauges preserve this property. They do not automatically preserve the triangular baseline in the same coordinates. The proof must identify the actual zero rectangle after all endpoint changes.

This theorem applies to the entire expanded evaluation, including injection, branch solves, the Schur-complement inverse application, all routing, and extraction. It does not force each component separately to be a superconcentrator, or give the same lower bound for the number of nonzeros in U,V,S, or S^{-1} individually. A dense inverse cannot be treated as one scalar gate; conversely an implicit fast inverse application must be charged by its actual arithmetic circuit rather than by dense-matrix nonzero count.

A singular branch pivot is another boundary. The separately accepted v30 complementary-minor proof remains valid for the inverse-rank obstruction, but the formula involving A^{-1} and its named correction R is then unavailable. One may apply the v31 circuit theorem directly to an actual totally nonsingular transfer block; one may not resurrect an undefined Schur correction formula.

The same reasoning applies to any shared zero rectangle of multiple triangular baselines. It preserves the stronger shared-rectangle obstruction already accepted in the completion review; it does not turn the LIS-only inequality into an exact characterization.

## 5. Depth and cost: exact conventions

Both classical theorems count edges, and depth is the maximum number of edges on a directed input-to-output path. A depth-two network has one middle layer; depth three has two. Each has n inputs and n outputs, not n total vertices. The number of middle vertices is unrestricted. [Radhakrishnan–Ta-Shma, introduction and Theorems 1.1, 3.1, 3.5](https://www.cs.tau.ac.il/~amnon/Papers/RT.siam00.pdf) prove the depth-two minimum is Theta(n log^2 n / log log n). [Alon–Pudlak, introduction and Theorems 3.1, 4.4](https://www.cs.tau.ac.il/~nogaa/PDFS/super2.pdf) prove the depth-three minimum is Theta(n log log n). Their definitions do not impose bounded degree. Fixed-depth graphs with skipped layers can be subdivided into consecutive layers with only a constant-factor size change.

Consequently, for m=floor(N/2):

- An entire correction evaluator of edge-depth at most two must have Omega(N log^2 N/log log N) edges. Its ratio to N log N diverges.
- An entire correction evaluator of edge-depth at most three must have Omega(N log log N) edges. The best generic support order is sub-N-log-N, but this gives no matching Fourier-specific upper bound.
- These conclusions concern total edges of the complete evaluator. “The interface has only O(N) routing entries” is not alone ruled out if the solve or other components carry the required work.

A literal sparse product R=XY fits the depth-two interpretation when both factor applications are evaluated directly as weighted scalar sums. Fixed diagonal intermediate scaling can be absorbed into adjacent edge weights. Zero diagonal entries remove routes, while nonzero diagonal scaling does not remove the lower bound. If X or Y is itself applied by a deeper structured circuit, the literal-factor depth-two classification no longer applies to that implementation.

These depths are not bounded-fanin parallel arithmetic depth. If every scalar gate has fan-in at most b>=2, an output at depth d depends on at most b^d inputs. Total nonsingularity forces every output to depend on all n inputs, hence d>=ceil(log_b n). In particular binary-gate depth two or three is impossible for arbitrarily large n, irrespective of size. Replacing an unbounded-fanin sum by a binary addition tree increases depth. A coefficient multiplication represented on an edge need not count as a separate graph level in the quoted combinatorial convention.

An edge-by-edge evaluation costs O(E+n) field operations. In an explicitly edge-charged ledger it costs Theta(E+n) by the ledger's definition; this must not be advertised as the minimum arithmetic complexity of the represented matrix without the architecture restriction. Identity wires, fixed signs and constant preparation need an explicit cost convention. Any claimed end-to-end speedup must separately include coefficient generation, graph construction, branch work, inverse application, reconstruction, memory conventions and all required outputs.

## 6. Generic totally nonsingular transforms: correct quantifiers

Assign a separate commuting variable x_e to every edge of an n-superconcentrator. For any terminal minor, the acyclic determinant/path identity leaves a signed sum of vertex-disjoint path families. Such a family exists. Its union of edges uniquely determines its component paths and endpoint matching, so two different families cannot yield the same monomial. Every surviving monomial has coefficient +1 or -1. Thus the minor is a nonzero polynomial over every characteristic. The classical cancellation proof can be read in [Gessel–Viennot, Section 2](https://sites.math.washington.edu/~billey/classes/561.fall.2019/past.articles/Gessel.Viennot.1985.pdf); the general weighted formulation is covered by the Talaska source above.

The product of the finitely many minor polynomials is nonzero. Over an infinite field it has a nonzero evaluation, simultaneously preserving all minors. Multiplying the product by all edge variables also allows every selected edge weight to be nonzero. This proves existence for every infinite field, including the rationals and complex numbers. It does not say that every assignment, tied assignment, Fourier phase assignment, or small-alphabet assignment works.

[Pippenger's original published abstract](https://doi.org/10.1137/0206022) explicitly gives n-superconcentrators with at most 40n edges, depth O(log n), and maximum total degree 16. Combining that result with the polynomial argument yields some totally nonsingular n-by-n transformations computed by O(n)-edge exact nonuniform linear circuits. Bounded degree makes O(n) scalar arithmetic evaluation immediate; binary normalization changes size and depth only by constants. This existence statement concerns preselected constants and no fixed-precision or uniform coefficient-generation guarantee. The full Pippenger proof was not independently rederived here; the exact quantitative theorem is verified against its primary publication statement.

Over a finite field F_Q the generic-polynomial argument requires a field-size qualification. For example, if the longest path has d edges, each k-minor has degree at most kd, so the product of all nonempty minors and edge variables has degree at most

    D = E + d * (n/2) * binomial(2n,n).

Since this polynomial is nonzero in every characteristic, Q>D is one sufficient, very nonoptimal condition for a nonzero specialization. Passing to a sufficiently large finite extension also suffices. No fixed finite field works for all n: for n>=2, comparing the first two rows of a totally nonsingular matrix forces n distinct nonzero ratios, so n<=Q-1. The two-by-two case over F_2 already fails.

Cancellation cannot invalidate the necessary rank bound. It can and does make a selected minor vanish despite abundant routes. Independence of formal edge variables is exactly what prevents cancellation in the existence proof; imposing cyclotomic or other algebraic relations removes that generic guarantee.

Therefore all-minor rank and connectivity alone do not force an N log N lower bound for unrestricted-depth linear circuits. The broader wording “every rank, separator, treewidth or expansion argument is exhausted” should be narrowed: the theorem refutes a universal N-log-N lower bound from total nonsingularity or superconcentrator support alone. Quantitative rank profiles, simultaneous architectural constraints, or Fourier-specific algebraic information might still support further arguments.

## 7. Prior accepted results remain separate

The earlier v30 audit establishes dimension/rank obstructions and sharp triangular completion. Its independently reviewed refinements establish an invertible triangular residual for every totally nonsingular target, stronger shared-zero rectangles, the reordered composite N=4 counterexample, and the singular-pivot complementary-minor extension.

v31 adds the circuit-support consequence of all minors on the chosen rectangle, then imports classical bounded-depth edge bounds. It does not strengthen the unrestricted interface-dimension minimum beyond m, replace the accepted completion, or show that the completed routing factors are sparse. The source's q=n depth-two enumeration is only a restricted small-case test; the asymptotic theorem optimizes over arbitrary middle-layer size.

The composite and finite-field qualifications from v30 remain controlling. Prime transform length alone does not ensure finite-field total nonsingularity. The v31 saved results correctly report failure of total nonsingularity for the N=11, F_23 half-rectangle, even though its full determinant is nonzero. Its support realization can still be a superconcentrator; the implication has no converse for those assigned weights.

## 8. Fresh controls and source implementation observations

The fresh standard-library-only verifier passes:

- Exhaustive depth-two q=n support minima: n=2 has 6 edges and 12 minimizing labeled supports; n=3 has 11 edges and 216 minimizers. It enumerates disjoint path families directly.
- Beneš n=4 and n=8 controls: respectively 24/80 edges, depth 3/5, and all 69/12,869 terminal-subset path tests and minors. Independent Edmonds–Karp flow and fresh transfer evaluation reproduce the recorded first rows over F_1,000,003.
- 1,520 rank/flow block checks on 80 fresh random scalar DAGs, including zero and negative weights and shuffled edge storage. Checks use the effective nonzero support.
- Complete half-rectangle minor checks at (N,Q)=(5,11),(7,29),(11,23). Counts are 5,19,251. The last case has rank 5 and determinant 5 but exactly two zero minors. The first is rows {0,1,2,4}, actual Fourier columns {6,7,8,10}, root 2 modulo 23.
- A two-input complete-support/all-ones specialization over F_2 has path capacity 2 and rank 1, certifying the fixed-weight non-converse and small-field limitation.

Two source software qualifications do not invalidate the mathematical theorem or the supplied constructor examples:

1. `LinearDAG.depth` processes the stored edge list once, rather than traversing vertices topologically. Topologically numbered vertices do not imply a topologically ordered edge list. A chain 0->1->2->3 stored as [(2,3),(1,2),(0,1)] is assigned depth 1 although its depth is 3. The source constructors store edges in the needed order, so their listed Beneš depths remain correct. Repair the routine before using it to classify arbitrary supplied DAGs.
2. The constructor checks distinct/disjoint terminals and increasing edge endpoints, but does not enforce all source/sink and terminal-range conventions. The existing constructors satisfy the needed conditions. Future general inputs should be validated and normalized explicitly.

The source's “independent verifier” avoids importing the main module but repeats its Beneš construction, seeds and Dinic-style flow method. That is useful redundancy, not a proof of algorithmic independence. The fresh verifier deliberately uses different flow and small-support certification methods.

## 9. Corrected research conclusion

There is a valid, sharply scoped support gate: any scalar linear DAG computing the prime-complex-Fourier half-rectangle forced by the triangular zero pattern has superconcentrator connectivity. Its complete edge-depth-two implementation is too large for the target sub-N-log-N ledger. Depth-three generic supports admit the quoted smaller edge order, without known Fourier-compatible weights in this package.

Producing weights for one half-rectangle would solve a necessary subproblem. It would not by itself produce the full correction, a compatible Schur realization, the remaining Fourier outputs, cheap branch solves, or charged coefficient generation. Those are additional obligations. Likewise a lower bound restricted to one selected depth-three graph would not exclude all such graphs.

Keep the proof status as “accepted with model/scope clarifications”; keep the algorithm and Fourier weight assignment unconstructed in v31; keep novelty/priority unresolved. The source package does not settle the literature-wide status of unrestricted exact FFT models.
