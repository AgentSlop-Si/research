# Endpoint rank prior literature addendum

10 October 2026

## Conclusion and scope

The checked sources establish substantial antecedents: subgroup Fourier hierarchies, sharp one-vector support frontiers, arbitrary-rectangle rank estimates, and the quasiseparable-order invariant. No exact match to the manuscript's autocorrelation-deficit and singular-value formulas or its general dyadic independent-endpoint minimax was identified in the statements inspected. This is a bounded comparison, not a worldwide priority finding or a claim of logical independence from the literature.

This addendum supersedes the earlier attribution and source-availability framing where specified below. It leaves the manuscript's proofs unchanged. The final 2007 journal text remains an access gap; the complete institutional author report was read instead. Report numbering must not be cited as final-journal numbering.

## Delvaux and Van Barel 2007

The exact article is *Rank-deficient submatrices of Kronecker products of Fourier matrices*, LAA **426** (2007), 349–367, [DOI 10.1016/j.laa.2007.05.009](https://www.sciencedirect.com/science/article/pii/S0024379507002182). The inspected [KU Leuven TW477 author report](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW477.pdf) is dated 15 November 2006; its printed pages are PDF pages minus two.

- Definition 2, p. 3: the support frontier uses “under the restriction that |J| ≤ d”. It concerns existence of a nonzero kernel vector.
- Lemmas 11–12 and Remark 13, pp. 10–11: annihilator-coset rank-one grids and simultaneous prime-power hierarchies; cyclic digit reversal is explicitly identified.
- Theorem 17, p. 13: H_(A⊗B)(d) = min_(ab≤d) H_A(a)H_B(b).
- Theorem 20 and Corollary 21, pp. 17–18: the exact Fourier support frontier depends only on total group order, including noncyclic groups.

Inference: for any abelian group of order 8, H(3)=4. Transposing a 3×5 block of rank at most 2 would produce input and output supports at most 3, a contradiction. Thus the order-eight lower bound is prior for all these groups. For N=4L≥16, H(L+1)=4≤2L−1; this direct substitution does not exclude rank L.

## Other primary comparisons

### Arbitrary rectangle ranks

Borodin, Razborov and Smolensky, *On lower bounds for read-k-times branching programs*, Computational Complexity **3** (1993), 1–18, [author-hosted final article](https://www.cs.toronto.edu/~bor/Papers/lower-bounds-read-k-times-branching.pdf): Theorem 10, pp. 12–13, gives

rank A[V,W] ≥ |V||W| / (2N log(2N/|W|))

for character tables over splitting fields; the dual bound interchanges |V| and |W|. Propositions 8–9 supply rank subadditivity and translation invariance. This is genuine universal rectangle-rank prior art, beyond one-vector uncertainty. In the complex setting its displayed bound is weaker than the elementary rh/N baseline and supplies no critical-rectangle +1. Its field coverage does not transfer the manuscript's analytic gap to finite fields.

### Sharp support uncertainty

Meshulam, *An uncertainty inequality for finite abelian groups*, European Journal of Combinatorics **27** (2006), 63–67: [author's arXiv text](https://arxiv.org/pdf/math/0312407), Theorem 1.2, printed p. 2, states

|supp f̂| ≥ N(d₁+d₂−k)/(d₁d₂),

where k=|supp f| and d₁,d₂ are its adjacent divisors of N. At k=L+1 and N=4L this gives 4−2/L, not the needed exclusion of rank L. The group setting and divisor improvement are established; this scalar statement has no translation-autocorrelation parameter or prescribed-nullity gap.

Bonami and Ghobber, *Equality cases for the uncertainty principle in finite Abelian groups*, Acta Sci. Math. (Szeged) **79** (2013), 507–528, [journal full text](https://acta.hu/download.phtml?id=3238): Lemma 5, p. 511, makes a fixed extremal-support solution space at most one-dimensional; Proposition 11, pp. 513–515, gives the tensor support formula and equality cases under a unique-minimizer hypothesis. These are stronger structural antecedents than support-cardinality bounds alone. They concern the extremal frontier, whereas the hypothetical critical-block kernel sits away from that frontier when N≥16. No general-rank conclusion follows from merely substituting its dimensions into these statements.

### Quantitative Fourier subspaces

Akemann and Weaver, *Detecting Fourier subspaces*, [arXiv:1503.06893](https://arxiv.org/pdf/1503.06893), Theorem 0.6, pp. 4–5: for a fixed Fourier projection Q, a standard coordinate projection P of prescribed rank k exists with both ||PQ||² ≤ k/N+O(√ε) and ||(I−P)Q||² ≤ (N−k)/N+O(√ε), where ε=rank(Q)/N. This confirms that quantitative projection and complementary-projection methods are prior art. The quantifier is existence of a suitable coordinate set. It is not the manuscript's explicit lower bound on an interior singular value for every specified rectangle.

Barnett, *How exponentially ill-conditioned are contiguous submatrices of the Fourier matrix?*, [arXiv:2004.09643v3](https://arxiv.org/pdf/2004.09643), Theorem 2, pp. 3–4, proves explicit exponential condition-number lower bounds for cyclically contiguous rectangles. This does not contradict a positive σ_(L+1) bound for a (2L−1)×(2L+1) block: the smallest singular value is σ_(2L−1), a different index for N≥16. Exact rank, interior-singular-value robustness, and full conditioning must remain separate claims.

### Ordering terminology

Pernet, Signargout and Villard, *Exact computations with quasiseparable matrices*, ISSAC 2023, [author-hosted paper](https://perso.ens-lyon.fr/gilles.villard/BIBLIOGRAPHIE/PDF/quasisep.pdf), Definition 1.1, PDF p. 1, defines s-quasiseparability by the two off-diagonal rank bounds at every cut. Therefore the manuscript's q(M) is exactly the least such s, namely its quasiseparable order. The definition is not new. The optimization over independent row and column permutations and its claimed Fourier value are the objects requiring separate comparison.

Graph linear rank-width is related terminology but a different optimization: An indexed primary-text excerpt of Kwon's [doctoral thesis](https://mathsci.kaist.ac.kr/~ojkwon/ojoungthesis.pdf), p. 21, uses one vertex layout and graph cut-ranks; a fresh full-PDF fetch was unavailable. It does not identify the manuscript's complex, independently permuted row/column invariant with ordinary graph cutwidth or establish its Fourier minimax value.

## Exact manuscript claims still requiring priority assessment

For its normalized character table V=U[R,H], the manuscript proves

rank V ≥ ceil(rh/N + d_H r(N−r)/N²),

where d_H=h−max_(s≠0)|H∩(H−s)|. With B_H=h(N−r)/N−d_H r(N−r)/N² it also proves

σ_(t+1)(V) ≥ sqrt(1−sqrt(B_H/(h−t))) for t<h−B_H.

The source comparison must target this precise parameter dependence, the universal row/column-set quantifiers, the singular-value index, and normalization. The generic use of Gram contractions, trace moments, character orthogonality, or best low-rank approximation is insufficient by itself to support a novelty claim.

For cyclic N=2^m≥8 the endpoint statement is min_(ρ,σ) q(P_ρF_NP_σᵀ)=N/4+1. The known hierarchy supplies the upper construction; the universal lower obstruction concerns offset rectangles of dimensions (N/2−1)×(N/2+1). Arbitrary half-size squares retain the different exact minimum N/4. None of these rank statements is an unrestricted FFT arithmetic lower bound.

## Existing record updates

Apply the companion delta only to the existing C02, FUS-03 and Q05 records. Preserve their proof status and the completed final DV08 comparison. Replace “2007 source not compared” with the precise report-read/final-unverified status. Record the expanded order-eight attribution and the standard quasiseparable terminology. Keep worldwide priority unresolved. No additional spreadsheet is required.

The frozen manuscript SHA-256 is 456ae5ab870ce002c5a4cfa80a6169ffb0defd87e38196011e09f4459206fdc7. It was checked before and after this work. No primary-source PDF or full extracted source text is included in this addendum's deliverables.
