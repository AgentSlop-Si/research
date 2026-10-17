# Two neglected structural records: bounded primary comparisons

17 October 2026. Baseline: repository main `b8b53a98e7a85bbc9a470cd86df3664080c7704c`; live workbook 88 CLOSED + 239 TO RESEARCH = 327 views.

## Outcome and disposition

The named Tao, Pernet, GIRS and nullity comparisons are complete for **M-FCUT** and **M-SPARSE-PREFIX**. They establish exact classical ingredients and qualified interface nonmatches. They do not establish worldwide novelty, a new theorem, an unrestricted FFT lower bound, or practical speed. **Both parent records remain TO RESEARCH at priority 42.** No status, score, proof classification, assessment band or census change is proposed.

The selected source-specific stopping conditions have been met. The broader historical-attribution task is not silently declared solved. The already recorded final Delvaux–Van Barel comparison is retained as inherited evidence; its final 19-page primary PDF was not recovered or freshly reread here. A new owner-specific comparison to that final paper requires a verified readable copy. This does not invalidate the accepted mathematics or reopen the earlier comparison report. It is not a reason to repeat the four completed comparisons.

This pass read the complete pinned sparse-prefix theorem and original accepted review, and the complete FCUT accepted proof audit, including its original local bytes and public sanitized derivative. All historical programs stayed inert. Fresh, separately written exact controls are described below.

## Verified primary sources

1. [Tao, arXiv math/0308286v6](https://arxiv.org/html/math/0308286v6), Lemma 1.3 and Corollary 1.4, with their proof context. This is the exact complex prime-Fourier nonzero-minor ingredient. The source expressly attributes the underlying result to Chebotarev. Normalization, Fourier sign, invertible diagonal scaling and row/column permutations preserve nonvanishing. This direct ingredient match does not by itself attribute the downstream sparse-sandwich or mixed-order theorem.

2. [Pernet, arXiv 1602.01246v2](https://arxiv.org/pdf/1602.01246v2), Definition 1, Theorems 2–4 and §5.2. In one specified ordering, the off-diagonal block ranks define quasiseparability. Compact generators support matrix-vector application in O(N(r_L+r_U)) field operations once available; construction has a separate O(N² s^(omega−2)) bound. The paper explicitly distinguishes exact rank-revealing arithmetic from floating-point issues. These are representation/upper-cost statements, not lower bounds obtained from dense entry counts or from the number of factors in another grammar.

3. [Chandrasekaran–Epperly–Govindarajan, arXiv 1911.05858v3](https://arxiv.org/pdf/1911.05858v3), §2.1, Definition 1 and Propositions 2.1–2.3. Opposite blocks on a complementary graph cut have the same ranks under inversion; GIRS parameters add for sums/products on the same graph. The scalar/block real notation in the source is retained. The relevant rank identities also follow over the complex field by the same purely algebraic block argument, without a positivity or conjugation premise. Neither a shared graph with controlled cuts nor a compact constructor follows merely from independently routed endpoints.

4. [Vandebril–Van Barel, author-hosted 15 July 2004 text](https://people.cs.kuleuven.be/~raf.vandebril/homepage/publications/papers_html/nullity/node3.html), Theorem 1, Corollaries 1–2, with both proof arguments read. The exact identity is rank(A^-1[alpha,beta]) = rank(A[beta^c,alpha^c]) + |alpha| + |beta| − N, assuming A invertible. Its complementary-cut specialization transports the cyclic Green branch ranks. The printed theorem uses real notation; the kernel/block proof is algebraic and applies over the complex field. Inversion is essential and cannot be inserted into the singular-denominator FCUT scope.

No more than a source-specific implication/nonmatch is claimed. Failure of a direct substitution is not a proof that no more elaborate reduction could exist.

## M-FCUT: exact implication and remaining step

Accepted statement: for prime p≥3, arbitrary Hamiltonian cycles alpha,beta, arbitrary complex edge weights and invertible monomial endpoints, C=(I−D_a P_alpha)L^-1 F_p R^-1(I−D_b P_beta) has each adjacent-alpha row-pair support union at least ceil(p/2). Therefore nnz(C)≥ceil(p ceil(p/2)/2). Neither difference factor needs to be invertible. Zero edges and singular all-one factors are allowed.

Here is the exact inference chain, reread against the accepted audit:

- Two adjacent left rows have a rank-two coefficient matrix on three distinct frequency labels, with rows (1,−a_i,0) and (0,1,−a_alpha(i)). Monomial changes preserve this rank and the distinct labels.
- Tao's full-minor input makes every three-column restriction of the resulting two-row H rank two.
- Mark the support of the two output rows of H(I−D_b P_beta). At every unmarked destination, the two-vectors propagate by multiplication along the beta edge. With m>0 marks, cutting those incoming edges leaves exactly m paths. Each path's columns have rank at most one, so it has at most two vertices. With m=0, the full cycle has rank at most one, also impossible. Thus p≤2m.
- Summing the adjacent-pair bounds counts each row support at most twice, producing the stated ceiling.

The marking-and-path argument is additional to the four named primary statements. The scalar uncertainty theorem alone cannot be applied through the arbitrary weighted difference: an all-ones row has full support and is annihilated by I−S. This is a legal singular-denominator case. Nullity/GIRS inversion cannot be applied to that factor, and ordinary quasiseparable upper ranks do not count the nonzero output entries here.

The accepted composite-length extension instead checks primitive-stride three-frequency Vandermonde profiles. Arbitrary composite non-affine triples, finite-field full spark, shared dense evaluators and products of sums are not certified. The prime p≥11 two-resolvent consequence is already subsumed by the project's earlier separator results; this comparison does not count it as another discovery.

## M-SPARSE-PREFIX: source-specific mapping

Accepted original theorem: for totally nonsingular T, invertible P with at most s nonzeros in each row, and H=sum H_j with integer separation-rank total R and d distinct independent row/column order pairs, T=P^-1 H requires floor(N/(s 2^d))≤R. Complex prime Fourier supplies a target, and t individual Green-prefix factors yield s≤2^t.

The branchwise mechanism is classical: in cycle order, the two off-diagonal blocks of an invertible cyclic first-order difference have rank at most one. Complementary-cut nullity gives the same bound for its Green inverse. Pernet's definition gives the standard ordered formulation. Independently routed/gauged branches retain that property after transporting each branch's own two position maps.

Two further steps are required for the accepted mixed-order theorem:

1. Strict asymmetric halving once per distinct order pair produces m=floor(N/(s 2^d)) selected rows and c=floor(N/2^d) columns, with c≥sm. Cross-map ties are allowed; m=0 is handled as vacuous. A single ordinary-coordinate cut cannot silently replace those d transported cuts.
2. If S is the union of the selected supports of P, then m≤|S|≤sm≤c. Total nonsingularity gives a right inverse to T[S,Y]. Multiplying (PT)[X,Y] by that inverse recovers P[X,S], so its rank is m. The tail ranks total at most R, proving m≤R.

The four primary comparisons supply the full-spark and branch-rank ingredients, but none of the inspected statements supplies this combined independent-order selection and arbitrary per-row sparse mixing contract. Same-graph GIRS closure cannot be invoked without constructing and bounding an appropriate common graph; a union graph can lose the required small cuts. This is a qualified nonmatch, not a novelty finding.

The original fixed-P approximation certificate remains conditioning dependent. Products of two additive Green sums need not have sparse inverses. The separately named SPARSE-PREFIX-20261010 endpoint-nonzero problem is not this theorem; its matching construction and other parents remain untouched. The supplied source helper's m=0 cardinality caveat remains historical and was not repaired or executed.

## Source integrity and execution boundary

- Exact sparse-prefix theorem SHA256: `a5784d6922eb3e959570929c4a1a036774a45900a0430b2ac082dec585b87bd2`. [Pinned public theorem](https://github.com/AgentSlop-Si/research/blob/b8b53a98e7a85bbc9a470cd86df3664080c7704c/math/archive/objects/a5/a5784d6922eb3e959570929c4a1a036774a45900a0430b2ac082dec585b87bd2__THEOREM_3_.md).
- Exact original sparse-prefix review SHA256: `5d43263d5a535a9e430ef17b4d1a55514677026b1719b3847bb97e6963899a70`. Its existing source-to-review seal is `54b796b03f0454b7e47f3138cca477e0dfa0d904ea2e80759c25eef2acaf7a04`; this pass rehashed the theorem and review, not every historic manifest member.
- Original FCUT audit SHA256: `688ee118a6fc3855176ccedf78ff6663307af84d70b10ecaae51ed9c4aa154b2`. The [public sanitized derivative](https://github.com/AgentSlop-Si/research/blob/b8b53a98e7a85bbc9a470cd86df3664080c7704c/math/archive/objects/68/688ee118a6fc3855176ccedf78ff6663307af84d70b10ecaae51ed9c4aa154b2__688ee118a6fc3855176ccedf78ff6663307af84d70b10ecaae51ed9c4aa154b2__FCUT_AUDIT.md) has a different expected SHA256, `24708f0c38135ac7630eb9bff1e0b68059e4b553074fc5eff019b9643b161977`; the original hash in its filename is not its content hash.

Fresh exact controls pass: 251 rational Cauchy minors, 570 admissible sparse-mixing rectangles, 162 Green complementary-cut blocks including six zero-weight systems, 18 constant-row annihilation examples, a 4×4 independent-permutation rank countercontrol and a too-few-columns cancellation example. They test the comparison boundaries. They are neither a historical replay nor a uniform-proof substitute. The small fresh checker is self-contained and imports no historical program.

## Native editing proposal

Only existing current-action, evidence and stopping-condition cells are proposed. Each new dated paragraph is prepended to the exact live preimage. Earlier text remains verbatim. Status and score cells are excluded. Private native snapshots, exact preimages and postimages are held separately from the publication-safe report; only the explicit accepted allowlist may be published or applied.
