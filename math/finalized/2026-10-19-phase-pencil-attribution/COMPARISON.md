# Attribution of the two-column Fourier phase test

Date: 19 October 2026. Scope: the fixed-stage phase test, its finite four-Green separation certificate, generic-rank interpretation and characteristic-zero consequence.

## Disposition

The general mechanisms are classical. The complete gauge test is diagonal similarity; the two-column determinant is an inverse-free necessary subtest of the same intertwining equations; generic interface rank is linear matroid intersection; and the characteristic-zero consequence uses good reduction of finitely many nonzero determinants.

The defensible project-specific object is narrower: an explicit, reproducible, fixed-topology four-Green certificate showing that maximal submatrix ranks and the tested one-sided Fourier capacity bounds can coexist with failure of every invertible middle gauge. No source inspected here establishes that exact restricted-family certificate. This is a **specific potential contribution with bounded, unresolved publication novelty**, not a new general solvability theorem or an established priority claim. The attribution comparison is complete at this scope. The original uniform-construction and total-cost questions remain open.

This note compares accepted mathematical claims rather than repeating their computational verification. Its reference checkpoint is the [accepted review, immutable revision](https://github.com/AgentSlop-Si/research/blob/6e401048dea59a1cf995ae06763f37d0ee826256/math/archive/objects/25/258fdfefc49efdfbd726c715edf273b253b1d470a8353c8fe002e2c3fe4de3e6__REVIEW.md). The underlying October 10 proof itself credits earlier diagonal-similarity and matroid-intersection work.

## 1. Exact object being attributed

Let K contain a primitive Nth root ω, with char(K) not dividing N. Let F[k,j]=ω^(kj), S e_j=e_(j+1 mod N), and Δ=diag(1,ω,…,ω^(N−1)). For fixed invertible A,B, write b_j=B e_j and

K_j=A diag(b_(j+1))−Δ A diag(b_j).

The accepted equivalence is

L A diag(d) B=F for invertible diagonals L,diag(d)

if and only if d has full support and K_j d=0 for every j. Equivalently, with X=B S B^−1 and Y=A^−1 Δ A,

diag(d) X diag(d)^−1=Y.

Hence det(K_0)≠0 rejects all middle gauges for those fixed A,B. The converse using K_0 alone is false. The output normalization follows from A diag(d) B e_0 once all column equations hold.

## 2. Claim-by-claim comparison

### C1. Full-support gauge feasibility and graph cycles: exact classical match

[Saunders–Schneider (1978)](https://people.math.wisc.edu/hans/paper_archive/scanned_papers/hs058.pdf), Theorem 2.1, pp. 209–210, characterizes diagonal similarity by common support and equality of products on all integer flows. Corollary 2.4, p. 211, reduces this to an integral flow basis. The hypotheses apply to the multiplicative group K* with zero adjoined; no irreducibility assumption is needed. Signed traversal permits reciprocal factors on backwards edges.

The substitution is their matrix pair ← (X,Y), their diagonal ← diag(d). On each supported edge, d_i X_ij=Y_ij d_j, so Y_ij/X_ij=d_i/d_j. Products must be one on every closed traversal. This is the accepted graph condition exactly, including disconnected support and loops.

[Engel–Schneider (1982)](https://people.math.wisc.edu/hans/paper_archive/scanned_papers/hs066.pdf), Corollary 3.11, p. 433, gives the complete spanning-forest decision procedure; Theorem 3.12 describes all diagonal solutions through one nonzero free factor per connected component. Thus gauge recovery and its componentwise ambiguity are inherited, not additional results. Their Theorem 4.3, p. 434, also covers simultaneous families.

Cost qualification: their §5, pp. 436–438, separately counts forest propagation and logical scanning; §6 additionally forms and verifies the entrywise quotient. These results do not provide a linear total-cost dense Fourier synthesis algorithm. Here O(N+E) describes the graph step only after X,Y are available; E can be Θ(N²), and obtaining those matrices is additional work.

### C2. Fourier covariance and the two-column determinant: classical implication, specialized presentation

Directly expand the jth column of M S−Δ M for M=A diag(d) B: it is K_j d. Since S cycles the basis, covariance forces each row of M to be a scalar multiple of the corresponding Fourier row. Invertibility makes every scalar nonzero. These elementary substitutions account for the Fourier-specific part of C1 without an additional classification theorem.

K_0 retains just one column equation. Its nonsingularity excludes a nonzero solution to the larger homogeneous system. This determinant inference is elementary linear algebra. Its useful implementation feature is avoiding the explicit inverses used to construct X,Y, not a new complete feasibility criterion. No inspected source was found displaying this exact two-column notation, but a notation-level nonmatch is not evidence of theorem-level novelty.

To locate it within displacement theory, suppose additionally that every entry of b_0 is nonzero and set R=diag(b_(1,i)/b_(0,i)). Then

K_0=(A R−Δ A) diag(b_0)=−∇_(Δ,R)(A) diag(b_0).

The Sylvester displacement ∇_(L,R)(A)=L A−A R is defined in [De Sa et al., §6, Definition 6.1](https://arxiv.org/html/1611.01569v3). Thus this instance of K_0 is a diagonally scaled standard displacement. The original formula remains valid when b_0 has zeros, where this ratio expression is unavailable. The paper's compressed reconstruction and fast multiplication results require additional conditions, including low displacement rank and uniqueness of the Sylvester solution. Neither is supplied here: the certificate has rank(K_0)=N, and S and Δ have identical spectra. Consequently its Theorem 6.2 cannot supply an O(N) determinant test or a Fourier executor for this construction.

### C3. The word “pencil”: a qualified nonmatch with eigenvalue balancing

[Dopico–Quintana–Van Dooren, “Diagonal scalings for the eigenstructure of arbitrary pencils”](https://arxiv.org/html/2009.00482v2), §§2–3 and Theorem 5, concerns diagonal scaling/balancing of a parameter pencil λB−A for eigenstructure computation. Its optimization and regularity hypotheses are different from exact Fourier factorization with an unrestricted complex middle gauge. K_j is a family of coefficient matrices for a restricted intertwining equation, not that eigenvalue-balancing problem. Shared vocabulary does not constitute a duplicate theorem or an applicable complexity result.

### C4. Generic rank of A diag(t) B: exact matroid-intersection mechanism

For A of size m×N and B of size N×r, set a_i=A[:,i] and q_i=B[i,:]. Then A diag(t) B=Σ_i t_i a_i q_i. This is a matrix space generated by rank-one matrices.

[Lovász (1989)](https://lovasz.web.elte.hu/morepapers/singular.pdf), §3, Theorems 1*, 2 and the immediately following proof, pp. 90–91, relates these rank-one generators to the common-independent-set min–max theorem, explicitly credited there to Edmonds (1970). Substitute the paired vectors a_i and q_i^T. The common-independent maximum becomes

rank_(K(t))(A diag(t) B)=min_(S⊆[N]) {rank A[:,S^c]+rank B[S,:]}.

The inspected Lovász presentation starts over the reals. The accepted all-field formal identity additionally uses Cauchy–Binet: distinct index sets produce distinct squarefree monomials, so a nonzero minor exists exactly when a common independent set does. Together with the abstract matroid-intersection theorem this is field-independent; it is not a verbatim arbitrary-field theorem statement attributed to Lovász. The original 1970 Edmonds chapter's full theorem text was not accessible in this pass; its [publisher reprint record](https://doi.org/10.1007/3-540-36478-1_2) was checked. This limits earliest-source precision, not the classical classification of the identity.

Formal generic rank must be distinguished from full-support rational-point attainment. Over an infinite field, finitely many selected nonzero minor polynomials and the coordinates t_i have a common nonvanishing point. Over F₂, A=(1 1) and B=(1 1)^T already give generic rank one, while the only full-support t=(1,1) gives rank zero. No unconditional finite-field full-support claim follows.

### C5. Rank strata and simultaneous genericity: standard determinantal geometry

A rank-at-most-k condition is the vanishing of all (k+1)-minors. Rank-at-least-k is a union of principal opens defined by nonzero k-minors. A modern exact formulation is [Stacks Project, Lemma 15.8.7, tag 07ZC](https://stacks.math.columbia.edu/tag/07ZC): apply the fiber-generator criterion to the cokernel of the matrix. Minors under specialization are covered by [Lemma 15.8.4(3), tag 07ZA](https://stacks.math.columbia.edu/tag/07ZA).

For the fixed Green wiring, clear the admissible rational denominators. The product of the selected nonzero minor numerators and the phase-determinant numerator is nonzero at the certified point, hence is not the zero polynomial on that parameter family. Its nonvanishing defines the claimed nonempty open set. This geometric consequence is classical. The substantive application-specific input is the point establishing nonemptiness; genericity in the space of all matrices would not establish nonemptiness on the restricted Green family.

For fixed A,B with det(K_0)≠0, a generic set of middle gauges can be totally nonsingular while every gauge remains Fourier-incompatible. Across parameters of the certified wiring, compatibility is contained in the proper phase-determinant zero locus. Neither statement rules out exceptional compatible parameters.

### C6. Finite-field certificate to characteristic zero: good reduction, not general solution lifting

Take the integer representatives of the saved weights and endpoint gauges and use ζ₈ for the Fourier phase. Localize Z[ζ₈] at the finitely many denominators required by the Green inverses and admissibility conditions. They reduce to nonzero elements under ζ₈↦4096 modulo 65537. [Stacks Project, Proposition 10.9.3, tag 00CP](https://stacks.math.columbia.edu/tag/00CP), gives the extension of this reduction map to the localization.

Determinants commute with that map. An element equal to zero before reduction must reduce to zero. The nonzero reduced minors and phase determinant therefore certify nonzero characteristic-zero elements at the explicitly lifted parameter point. This is a direct good-reduction argument. It neither invokes Hensel's lemma nor lifts an arbitrary finite-field solution to polynomial equations. The relevant conditions are finitely many inequations with verified denominators, rather than newly solved characteristic-zero equalities.

## 3. What remains specific to this certificate

The accepted N=8 example uses A=G₁+G₂ and B=G₃+G₄. Each G is an independently endpoint-permuted and diagonally gauged inverse of I−T, with T a genuinely Hamiltonian weighted cycle, all weights nonzero and cycle product different from one. Over F₆₅₅₃₇, ω=4096 and det(K_0)=55687. A saved middle gauge makes every one of the 12,869 nonempty square minors nonzero and passes 225 one-sided divisor-coset capacity inequalities.

“Totally nonsingular” describes this all-square-minor property more unambiguously than “full spark.” These values are inherited from the accepted exact certificate, not newly recomputed in this attribution pass.

The conclusion is specifically that those capacity conditions are insufficient for phase compatibility. It does not say that every possible rank test fails to reject the example: the exact Fourier rank profile already separates it on rows {0,4}, columns {0,2}, where Fourier rank is one and candidate rank is two.

The classical results above do not by themselves construct a point in this four-Green family satisfying all the inequations. The example supplies that input. A literal predecessor establishing this same restricted-family existence or an equivalent constructive theorem would settle the residual application-level attribution. No such predecessor was established by the inspected sources. This bounded nonmatch should not be expanded into a claim of worldwide originality.

## 4. Recommended use and stopping condition

Retain the result as a supporting finite separation certificate and an inverse-free diagnostic presentation of classical covariance. Attribute complete gauge recovery to diagonal-similarity theory; attribute the rank formula to matroid intersection; present the geometric and reduction steps as standard consequences. Do not promote it to a standalone new general theorem on the present evidence.

The mechanism-attribution question no longer needs an open-ended repeat search. Revisit the narrow certificate novelty question only with a concrete topology-matched predecessor or a new reusable result beyond this finite example. Separately, the original research target still requires an all-length exact family, one full-support gauge satisfying every K_j equation, O(N) generation of roots/weights/permutations/gauges, and O(N) total sequential application under its stated arithmetic model. This comparison provides none of those missing construction or cost proofs.

## Bibliographic identifiers

- B. D. Saunders and H. Schneider, *Flows on graphs applied to diagonal similarity and diagonal equivalence for matrices*, Discrete Mathematics 24(2), 205–220 (1978), [DOI](https://doi.org/10.1016/0012-365X(78)90200-5).
- G. M. Engel and H. Schneider, *Algorithms for Testing the Diagonal Similarity of Matrices and Related Problems*, SIAM Journal on Algebraic and Discrete Methods 3(4), 429–438 (1982), [DOI](https://doi.org/10.1137/0603044).
- L. Lovász, *Singular spaces of matrices and their application in combinatorics*, Boletim da Sociedade Brasileira de Matemática 20, 87–99 (1989), [DOI](https://doi.org/10.1007/BF02585470).
- C. De Sa, A. Gu, R. Puttagunta, C. Ré and A. Rudra, *A two-pronged progress in structured dense matrix vector multiplication*, SODA 2018, [DOI](https://doi.org/10.1137/1.9781611975031.69), arXiv:1611.01569v3.
- F. M. Dopico, M. C. Quintana and P. Van Dooren, *Diagonal scalings for the eigenstructure of arbitrary pencils*, arXiv:2009.00482v2 (2021).
- The Stacks Project, tags 00CP, 07ZA and 07ZC; current statements accessed 19 October 2026. These are exact modern algebra references, not assertions of earliest historical priority.
