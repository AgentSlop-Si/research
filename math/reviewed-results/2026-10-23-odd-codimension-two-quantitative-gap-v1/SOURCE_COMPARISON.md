# Bounded predecessor comparison: odd inverse codimension two

Date: 2026-10-23 UTC. Owner: M-SPARSE-DEFECT. This is a domain/attribution comparison, not a second proof review. No external state was changed and no author or historical scientific code was executed.

## Decision for the research record

The new packet is a **mathematically accepted quantitative strengthening of the inherited result**, according to the separately sealed independent review. It must **not** be described as historically novel or as an exact optimum on the evidence of this search.

The two-column obstruction contains identifiable classical mathematics: the equal-support Gram estimate is the Welch bound for three vectors in dimension two, and its support obstruction is a small instance of quadrangularity/strong quadrangularity. The candidate's contribution relative to its inherited internal baseline is the explicit coefficient-stability transfer from that mask obstruction to the unrestricted simultaneous inverse-row problem, producing an order-1/N squared gap. Whether that transfer or a stronger theorem already occurs elsewhere remains unresolved. No directly matched published bound or optimum was established by the primary sources inspected in this bounded pass. This is a limitation of the comparison, not a novelty certificate.

Recommended record text: “Accepted: for every odd N≥3, Δ(N,N−2)²≥(9−4√3)/N in the original unrestricted spectral-norm inverse-row model. The proof combines classical Welch/orthogonality obstructions with an original-model stability argument. Exact optimum, optimal constant, and historical priority remain unresolved.” Here “original-model” means the initial admissible class, not a claim of originality.

## Exact comparison target and normalization

F[j,k]=N^(−1/2) exp(−2πijk/N), and Δ(N,s)=inf ||M−F||₂ over invertible complex M whose **every inverse row** has at most s nonzeros. Supports, amplitudes, phases, and conditioning are unrestricted; s=N−2; N is odd and at least 3. The target norm is the operator norm induced by Euclidean vector norm, not Frobenius norm.

A theorem for an unnormalized complex Hadamard H with HH*=NI must be rescaled: X=√N M and H=√N F preserve inverse zero patterns, while ||X−H||₂²=N||M−F||₂². Thus the simple claimed bound becomes ||X−H||₂²≥9−4√3. The candidate actually depends only on flat magnitudes and unitarity, so an odd-order flat-unitary theorem could be a genuine predecessor even without Fourier arithmetic. A theorem for real Hadamards alone does not cover these odd orders.

## Inherited, not newly established here

The frozen E_REVIEW supplies the one-row floor Δ²≥1−s/N, the complementary-mask equality characterization with coefficient rigidity, attained divisor cases, and strict nonattainment of the floor for odd codimension two. It also identifies the already accepted exact Δ(3,1)=√3/2. The new packet does not improve that exact N=3 result. The new internal advance is a uniform relative gap over the floor for all odd dimensions, not the qualitative odd/even obstruction itself.

## Classical ingredients: exact maps

1. **Welch bound.** Datta–Howard–Cochran, *Geometry of the Welch Bounds*, Lemma 2.1 and Theorem 2.2, derive the trace/rank Gram inequality and credit Welch's 1974 result. For three candidate mask columns on the same two coordinates, set xᵢ=√(N/2)cᵢ. These are three unit vectors in a space of dimension at most two. The first Welch bound gives maxᵢ≠ⱼ|〈xᵢ,xⱼ〉|≥1/2, hence max|〈cᵢ,cⱼ〉|≥1/N. This is exactly the candidate's Case II estimate. It is a classical ingredient, not an independently new coherence bound. [Primary manuscript](https://arxiv.org/pdf/0909.0206); [Welch DOI](https://doi.org/10.1109/TIT.1974.1055219). The Welch DOI full text was inaccessible here; the formula and proof were read in the primary geometric paper.

2. **Unitary support obstruction.** Severini, *On the digraph of a unitary matrix* (2003), Definitions 1–2 and Lemma 1, rule out singleton support intersections and more vectors than available coordinates in an orthogonal block. If every column support has size two and singleton intersections are absent, distinct supports are disjoint. At odd N there are at most (N−1)/2 distinct supports, so three of N columns share one two-set. These violate the strong-quadrangularity condition. This explains the phase-insensitive qualitative obstruction. Severini's support statement alone does not supply the positive numerical inverse-row gap. [Primary manuscript](https://arxiv.org/pdf/math/0205187).

3. **Ordinary linear algebra.** Cauchy–Schwarz, positive-semidefinite entry bounds, support padding, and rank/trace estimates should be presented as elementary tools. The candidate's exact identities and localized transfer, rather than these tools separately, are the part requiring direct predecessor comparison. This report does not award that transfer historical priority.

## Closest neighboring models and why they do not close the comparison

- **Sparse dual frames.** Krahmer–Kutyniok–Lemvig, *Sparsity and spectral properties of dual frames*, equation (2.3), Theorem 3.2, and Proposition 3.3, study exact duals of a fixed frame and characterize minimal sparsity through generalized spark. Their setting allows complex scalars. Set Φ=M* and Ψ=M⁻¹; then ΨΦ*=I and the candidate row sparsity is precisely row sparsity of Ψ. But their optimization holds Φ fixed. The candidate instead varies Φ near F* and minimizes ||Φ−F*||₂ under simultaneous row budgets. The read results give no uniform perturbation radius or candidate constant. Their total-entry sparsity statements cannot silently replace the every-row budget. [Primary manuscript](https://arxiv.org/pdf/1204.5062), §§2–3; [published record](https://doi.org/10.1016/j.laa.2012.10.016).

- **Sparse approximate inverses.** Holland–Wathen–Shaw, *Sparse Approximate Inverses and Target Matrices* (2005), formulate residual minimization ||T−PA|| with prescribed sparse P and discuss norms beyond Frobenius. Only the publisher abstract and bibliography were accessible, not the full theorem text. Setting A=F, P=B=M⁻¹, T=I yields R=I−BF=B(M−F); the candidate objective is ||B⁻¹R||₂, not ||R||₂. Therefore a residual result is not an exact matched bound without an additional valid transfer controlling B. The abstract cannot rule out all relevant results in the full article, which remains an explicit access limitation. [Publisher source](https://epubs.siam.org/doi/10.1137/030601132).

- **Earlier residual preconditioning.** Cosgrove–Díaz–Griewank (1992) explicitly discuss consistent residual norms, including the 2-norm, rather than only Frobenius norm. The same objective mismatch applies; it is incorrect to dismiss the entire literature merely as Frobenius-only. Publisher abstract read; full text not obtained. [Publisher source](https://www.tandfonline.com/doi/abs/10.1080/00207169208804097).

- **Inverse-sparsity title collision.** Xie's 2026 paper classifies bandwidths and positivity exponents of oscillatory matrices. Its abstract gives no Fourier/flat-unitary approximation problem or matched norm objective, so it is excluded at abstract screening rather than called a weaker predecessor. [Author preprint](https://arxiv.org/abs/2609.35846).

Ordinary sparse Fourier signal recovery, approximation of F itself by sparse matrices, low-rank approximation, inverse decay, and unrestricted support-graph existence were not used as competing numerical bounds.

## Search boundary and remaining gap

Eleven public search batches, containing 41 recorded queries, covered direct inverse-row formulations, sparse inverse approximation, flat/complex-Hadamard targets, sparse duals, inverse rigidity, and backward-error terminology. Relevant primary theorem sections were read for Welch geometry, unitary support obstructions, and sparse dual frames. The residual-preconditioning sources were abstract-only; inaccessible full text remains unreviewed. The search did not use private research content in public queries.

This bounded gate establishes attribution and model distinctions only. Historical-priority clearance would require a directly matched theorem or a broader theorem with an explicit norm/normalization/support map. No such implication was established here. Mathematical acceptance remains that of the independent review, and the owner should remain TO RESEARCH for optimum, best constant, broader budgets, and historical comparison.
