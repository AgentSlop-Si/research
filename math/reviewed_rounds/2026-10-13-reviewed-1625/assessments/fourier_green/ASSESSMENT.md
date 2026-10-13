# Fourier–Green representation obstruction: source-bound assessment

13 October 2026. Read-only mathematical and literature assessment; no historical program was executed, and no Sheet or GitHub content was changed.

## Bottom line

This is a real, uniformly quantified representation obstruction with a plausible specialist-paper contribution. The available evidence does **not** support calling it a major FFT breakthrough, an unrestricted Fourier lower bound, or a newly discovered fundamental matrix principle. Its defensible contribution is a carefully scoped synthesis that prevents an exact Fourier/flat-unitary matrix from being a short **additive sum** of independently routed, low-separator inverse branches.

“Restricted family” must not be mistaken for “one fixed numerical resolvent.” The coefficients, cycles, graph, and allowed endpoint routings can vary arbitrarily within the theorem's grammar. The restriction is on the architecture. The strongest accepted formulation even applies to every complex flat unitary, not only Fourier matrices.

## Identity and evidence

- **C05**, “Fourier–Green one-layer obstruction,” is the historical weighted-permutation result.
- **F018**, “Bounded-separator inverse-sum obstruction,” is the stronger routed separator result. **Q04** and **TH-04** are its linked workflow/theorem views; they are not extra independent discoveries.
- **M-ROUTED-FIELD** is a separate exact-field counting application; **M-SEPARATION** is a separate independent-order theorem. Neither should silently inherit every field or architectural scope of F018.
- The all-331 snapshot explicitly records completed bounded comparison for C05/F018/Q04/TH-04. Its priority 15 is a completed-stage work score, not mathematical quality, correctness probability, or novelty probability.
- C05 and F018 are outside the original 225-group unknown-source cohort. Their absence from `complete_source_coverage_1453` is therefore not a missing-proof finding. Full proof-bearing reviews and the later F018 theorem body were found and read. Exact source bytes and six stable-ID records are preserved beside this report in `SOURCE_MANIFEST.json` and `EXACT_SOURCE_RECORDS.json`.

Source anchors: current all-331 records C05/F018; historical C05 proof-review SHA-256 `f155488c0657b63b2192a6a1ecd7e2264ce4c0e1051b9e084b4dee22bbbf2a07`; current independently accepted comparison, `INDEPENDENT_REVIEW.md`, and its source-bound `AUDIT.md` (paths/hashes in the manifest). The historical review's recorded repository source is [C05 proof audit](https://github.com/AgentSlop-Si/research/blob/main/math/archive/objects/f1/f155488c0657b63b2192a6a1ecd7e2264ce4c0e1051b9e084b4dee22bbbf2a07__REVIEW.md). This link is source-recorded; no fresh remote repository readback is claimed.

## Exact historical theorem, C05

Work over the complex numbers. Each Green branch is a guarded weighted-permutation resolvent `(I−W_i)^−1`: arbitrary cycle decompositions, fixed points, and zero weights are permitted, but the weight product on every cycle must differ from 1. Scalar coefficients and independent diagonal endpoint masks, including singular masks, are allowed. Independent unmatched left/right endpoint permutations are **not** part of this historical extension.

Suppose the Fourier matrix is an additive sum of r such branches, a row-degree-s correction S, a rank-at-most-t correction K, and an arbitrary diagonal correction. For integers r≥1 and s,t≥0, put

`m=r+t+1`, `L=m(s+2)`, `B=(L−1)^(2^(r−1))+1`.

The representation is impossible when

`N > 2(m−1)(B−m)(B−1)`.

For r=2 and s=t=0 the threshold is N>2300. The proof separately excludes that two-branch representation when N has a prime divisor p≥29; its N=4096 cyclotomic argument is also retained. Fixed s,t imply r=Ω(log log N) in this historical one-layer grammar.

The proof is explicit: order each branch by concatenating its directed cycles; separated rectangles have rank at most one. Repeated monotone-subsequence selection finds a common separated set. Remove columns touched by S; K adds at most t rank. A surviving m-square rectangle has rank at most m−1. Its Fourier determinant is a Vandermonde factor times a positive-coefficient homogeneous Schur polynomial. The displayed small-arc condition confines all its monomials to an open half-plane, so the determinant is nonzero. No division by individual edge weights occurs. Diagonal corrections vanish because the row and column labels are disjoint.

This is a complex nonvanishing argument. Neither finite-field tests nor the title justify transplanting its positivity step to arbitrary characteristic.

## Stronger accepted theorem, F018

Let U be an N-square complex normalized unitary with every entry of modulus N^(-1/2), and

`U = S + K + δD + Σ_(i=1)^r L_i Q_i^−1 R_i`.

Assume r,q≥1, s,t≥0, δ∈{0,1}; S has at most s nonzeros **per row**; rank K≤t; D is diagonal. Every Q_i is invertible. Every L_i,R_i has support contained in a permutation matrix, with independent permutations and possibly zero weights. The symmetric bipartite support lift `[[0,Q_i],[Q_i^T,0]]` must admit separators of size at most q leaving every remaining component with at most half the weight for the two-color markings used in the proof. Requiring this for all nonnegative weights is sufficient; treewidth≤q−1 is a sufficient condition, not the definition.

With d=s+1+δ, exact equality requires

`N ≤ d²(qr+t)9^r + dq(3^r−1) + 2(d−1)`.

Column-two invertible denominators permit q=2; forest support lifts permit q=1. Thus fixed q,s,t force r=Ω(log N). Equality at the numerical boundary is not excluded.

Proof: first retain a correction-free rectangle of side floor(N/d). Each branch's separator and a two-color packing argument retain side `m_(j+1)=ceil((m_j−q)/3)`, whenever m_j≥4q. Complementary inverse ranks bound that branch's selected rank by q; previous bounds survive restriction. K contributes t. The final rank is at most qr+t, whereas every m-square flat-unitary block has rank≥m²/N. Iterating the side bound gives the displayed cutoff, and the accepted proof explicitly verifies every selection precondition under its contradiction hypothesis.

The rank/selection steps are field-general; the last flat-unitary norm estimate is complex. M-ROUTED-FIELD instead uses an exact-order-N root and consecutive-row Vandermonde nonsingularity to prove `N≤r(r+1)^r`, or `N≤s(r+1)+r(r+1)^r` with row-degree-s correction. This is a separately guarded application, not a finite-field version of the complex norm proof.

## Prior work and novelty classification

1. **Classical structural ingredients.** Complementary inverse-rank/nullity is established. The column-two inverse-direction lemma is an explicit quotient/frame-contraction corollary, including binary singleton columns via half edges, not a new matrix principle. Sources: [Vandebril–Van Barel, TW397](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf), Theorem 1/Corollary 1; [Zaslavsky, Biased Graphs IV](https://people.math.binghamton.edu/zaslav/Tpapers/bg4.pdf), §2.1 and Theorem 2.1(b). These exact attributions were independently established in the preserved source comparison; fresh TW397 retrieval during this pass timed out.

2. **Closest freshly inspected rank-structure sources.** [Chandrasekaran–Epperly–Govindarajan, GIRS v3](https://arxiv.org/pdf/1911.05858v3), Propositions 2.1–2.3, gives inverse cut-rank preservation and sum/product algebra on a common graph. [Govindarajan–Chandrasekaran–Dewilde, final TQS](https://repository.tudelft.nl/file/File_6b7549c8-222e-4316-8ac4-a113d7d4da1e), Theorem 4.4 and Propositions 4.6–4.8, characterizes profiles on a specified tree and composes compatible partitions. The relevant full-text statements were reopened in this pass. They do not state uniform low profiles on one common partition after independent branch-specific routing.

3. **Exact unmatched synthesis, bounded claim.** The accepted increment is retaining one actual target rectangle through successive unrelated branch separators while eliminating row-sparse entries and charging low-rank/diagonal corrections, producing the explicit cutoff. The inspected sources do not state this entire clause. That is a bounded nonmatch, not proof that no prior theorem implies it. Standard inverse ranks, separators, stable rank, and additive rank accounting remain classical.

4. **Historical C05 ingredients versus exact application.** Monotone-subsequence selection, Vandermonde/Schur factorization, and positivity are classical mechanisms. The exact all-composite small-arc threshold is an application whose own historical priority was not closed by the later GIRS/TQS comparison. Delvaux–Van Barel's [final Fourier-submatrix paper](https://doi.org/10.1016/j.laa.2008.04.043) supplies important Fourier-minor/hierarchy antecedents; it is not an inverse-sum theorem. No separate discovery should be claimed merely because the exact combined inequality was not found there.

This result's actual invariant is a selected submatrix rank controlled by inverse sparsity/separators. It should not be relabeled a new displacement-rank theorem. Separate fixed-pair displacement or Weyl–Green claims require their own exact statements and audits.

## What follows for FFTs and publication

It excludes a bounded number of these additive inverse branches as an exact DFT architecture at growing size, even when each allowed solve is cheap. It supplies no arbitrary-input FFT algorithm and no lower bound for all Fourier circuits, products of Green-sum layers, arbitrary interstage permutations, or shared evaluation. A concrete counterexample explains the product boundary: for three m-blocks, A=I+E12⊗I_m and B=I+E23⊗I_m have zero (block 1, block 3) rectangles, while AB has I_m there. Both inverse denominators have forest lifts. Selected-rectangle rank does not compose as assumed by an overbroad product claim.

The theorem is useful architectural pruning and a credible specialized mathematical contribution. The exact unrelated-routing synthesis is the publication candidate; the elementary ingredients and immediate correction variants are not separate breakthroughs. Evidence records an internally accepted 15-page scoped manuscript, but no external human specialist or journal review. Sharpness, broader usefulness, and whole-synthesis historical priority remain unresolved. Those are substantive limits on significance, not missing implementation details. My assessment is therefore **specialist-paper potential, with modest-to-moderate novelty still to be externally established; no supported serious/general FFT breakthrough from this result alone**.
