# Routed inverse-branch obstruction: source ledger and claim comparison

Prepared 2026-10-10 UTC; reconciled with the reviewed Hamiltonian rectangle antecedent at 04:53 UTC. Targeted literature assessment, not a global novelty certification. No publication, outreach, or supplied-code execution was performed.

## Bottom line

The restricted representation obstruction is mathematically meaningful: it rules out any fixed number of independently routed inverse branches for growing Fourier size, even with unrestricted scalar coefficients. Its natural scope is larger than diagonal-plus-permutation denominators: the same proof covers any invertible denominator with at most two nonzeros per column.

Important internal antecedent: the independently reviewed C04 rectangle-halving argument already gives an Omega(log N) obstruction for Hamiltonian Green branches with independent endpoints over the complex numbers. The new projective count is weaker asymptotically in that subclass; its benefit is wider denominator coverage and arbitrary-field validity. The all-pseudoforest logarithmic separator proposal remains unaudited and is not counted as an established result here.

The main structural ingredient has a particularly close classical antecedent in gain-graph contraction, in addition to the familiar inverse-bidiagonal and semiseparable literature. The Fourier ingredient is standard full-spark Vandermonde theory. I did not locate the exact additive, independently routed Fourier obstruction or its bound N <= r(r+1)^r in the targeted sources inspected. That negative search result leaves priority unresolved. The defensible candidate contribution is the combination/application, not discovery of inverse sparse-graph structure.

A reasonable assessment is a clean, potentially useful short structural lower-bound proposition. There is currently no basis to call it a breakthrough in Fourier arithmetic complexity, a sharp branch bound, or a fundamentally new theory of matrix inverses.

## Claim being compared

For a field K containing an element omega of multiplicative order N, let F[a,b] = omega^(ab). If

    F = sum_{i=1}^r L_i Q_i^(-1) R_i,

where Q_i is invertible and has at most two nonzeros per column and L_i,R_i have monomial support (zero weights permitted), then the proposed necessary condition is

    N <= r(r+1)^r.

The original diagonal-plus-permutation model is a subclass. Its independent audit accepted the argument and the improved constant. I also inspected the subsequently sealed `EXTENSION_AUDIT.md`, which accepts the column-two-sparse generalization and the row-sparse correction variant

    N <= delta(r+1) + r(r+1)^r,

when an added correction has at most delta nonzeros per row. The generalized audit includes exact checks with row degrees above two and bridge deletions leaving smaller surviving unicyclic components. I read its proof and results without executing its programs. Finite tests supplement the proof; they cannot establish priority or an unrestricted complexity result.

## Reviewed internal antecedent and pending proposal

The pre-existing argument reviewed in `green_geometry_source_review_0430/PROOF_AND_SCOPE.md`, claim C04, must be credited before describing the projective-column theorem as progress. C04 independently halves retained row and column sets for each Hamiltonian branch, preserving a rank-at-most-one restriction for every previously treated branch. With r branches it obtains side size m=floor(N/2^r) and sum rank at most r. For a complex normalized Fourier matrix, or any flat unitary target, rank(U[R,C]) >= m^2/N. Thus

    floor(N/2^r)^2 <= Nr.

In particular N <= 4r*4^r is a valid loose necessary bound: if N>4r*4^r, then x=N/2^r>2, floor(x)>=x/2, and the displayed rank inequality fails. Consequently r=Omega(log N). The proof does not require prime N. Endpoint routing is already independent in this reviewed antecedent; it must not be advertised as newly handled only by the projective theorem.

Comparison:

- Hamiltonian complex branches: C04 has the stronger asymptotic conclusion, Omega(log N).
- Arbitrary column-two-sparse denominators, including many-cycle and branched support: the projective theorem gives Omega(log N/log log N), with a field-general Vandermonde argument. This is the broadened scope established in the current analysis.
- A source variant first restricts to common cycle-label cells, losing factors depending on cycle counts. That does not by itself give a cycle-count-independent logarithmic theorem for all column-two-sparse denominators.
- `pseudoforest_separator_research_0452/PROPOSED_THEOREM.md` proposes such a broader logarithmic theorem via separators, with N<=12r*36^r for complex flat unitaries. At the time of this reconciliation it is an active proposal, not an accepted theorem. No result from it is used in the established comparison or the finite-N approximation corollary.

This internal antecedent comparison addresses progress relative to the supplied research, independently of unresolved public-literature priority. Source hashes are recorded in the package manifest.

## Source ledger

### 1. Closest structural antecedent: gain-graph contraction

Thomas Zaslavsky, *Biased graphs. IV. Geometrical realizations*, Journal of Combinatorial Theory, Series B 89(2), 231–297 (2003).

- Publisher: https://doi.org/10.1016/S0095-8956(03)00035-2
- Author manuscript: https://people.math.binghamton.edu/zaslav/Tpapers/bg4.pdf
- Inspected: §2.1, definition preceding Theorem 2.1 and Theorem 2.1(a),(b), manuscript pp. 8–9; Corollary 2.2; §3 two-term equations.
- The canonical vectors have two coordinate positions, with half-edges covering single-position vectors. The contraction map identifies coordinates within balanced components and annihilates unbalanced components. The theorem establishes the represented matroid and its behavior under contraction.
- Precise connection (our deduction): A=Q^(-1)[S,:] has kernel span(Q[:,S-complement]); thus it realizes that quotient, up to an invertible change of output basis. Original coordinate vectors become one line per surviving balanced component or zero. This gives the proposed projective-column lemma. For an independent retained edge set, balanced components are trees, and their number is |S|.
- Priority consequence: the structural lemma should be presented as an elementary specialization of classical gain-graph machinery, or proved directly with an explicit acknowledgement. This source does not supply the Fourier sum bound.

A direct terminology check is Peter Nelson and Stefan H. M. van Zwam, *On the existence of asymptotically good linear codes in minor-closed classes*, §2, pp. 4–5: https://www.math.uwaterloo.ca/~apnelson/asympgood.pdf . This primary paper defines a frame matrix exactly by at most two nonzeros per column. It also flags the binary-field difficulty with representing a singleton column as a nonidentity-gain loop. The direct support-graph proof in the accepted extension avoids that convention issue. This source confirms the established matrix class; its main coding theorem is not being invoked here.

### 2. Generalized-network incidence and binet matrices

Gautam Appa and Balazs Kotnyek, *Optimization with binet matrices*, working paper LSEOR 03.59 (2003).

- Primary repository PDF: https://eprints.lse.ac.uk/22768/1/optimization_with_binet_matrices03.59_LSEROVERSION.pdf
- Inspected: §§2–3, printed pp. 2–3 (PDF pp. 3–4).
- Defines binet matrices by B=R^(-1)S for a basis R in a bidirected incidence matrix. Its generalized-network discussion explicitly relates real matrices with at most two nonzeros per column to weighted network incidence form.
- This is another direct reason not to describe column-two-sparse inverse structure as newly discovered. The arbitrary-field formulation is more naturally handled by Zaslavsky's gain-graph representation.
- Caution: arbitrary weighted column-two-sparse matrices are not all binet matrices in the narrow signed-incidence sense. Do not use “binet” as an exact synonym for the proposed denominator class.
- Related published primary article: Appa and Kotnyek, *A bidirected generalization of network matrices*, Networks 47(4), 185–198 (2006), https://doi.org/10.1002/net.20108 . Publisher abstract inspected; full text not reliably retrieved.

### 3. Graph-induced rank structures, including cycles

S. Chandrasekaran, E. N. Epperly, N. Govindarajan, *Graph-Induced Rank Structures and their Representations*, arXiv:1911.05858v3 (2021 revision; initial submission 2019).

- https://arxiv.org/abs/1911.05858
- https://arxiv.org/pdf/1911.05858
- Inspected: §§2.1–2.2 and the cycle-representation description in §3; Propositions 2.1–2.3.
- Establishes preservation of appropriate off-diagonal block ranks under inversion, graph-induced rank bounds, and sum/product closure on a common graph. Develops cycle-semiseparable representations.
- Close conceptual antecedent for graph-based inverse rank structure. Independent branch routing is an important distinction: its common-graph addition rule does not immediately establish the proposed bound for unrelated branch graphs/orders. Passing to the union graph can substantially change its connectivity.
- No exact Fourier branch-count claim was located in the inspected material or targeted full-text searches.

### 4. Classical inverse-minor correspondence

Wayne W. Barrett and Philip J. Feinsilver, *Inverses of banded matrices*, Linear Algebra and its Applications 41, 111–130 (1981).

- https://doi.org/10.1016/0024-3795(81)90092-6
- Publisher abstract inspected; full article not obtained in this pass.
- Establishes correspondences between vanishing minors of a matrix and its inverse, including banded-inverse characterization. Relevant to the claim's foundational inverse-rank mechanism, not evidence of the exact additive Fourier obstruction.

Raf Vandebril and Marc Van Barel, *A note on the nullity theorem*, Journal of Computational and Applied Mathematics 189, 179–190 (2006).

- https://doi.org/10.1016/j.cam.2005.02.007
- Accessible manuscript section: https://people.cs.kuleuven.be/~raf.vandebril/homepage/publications/papers_html/nullity/node3.html
- Inspected: statement and proofs of complementary-block nullity, and source discussion.
- The nullity identity is established prior work; it is not the new part of the proposal.

### 5. Bidiagonal inverse formula

Nicholas J. Higham, *The Power of Bidiagonal Matrices*, arXiv:2311.06609 (2023).

- https://arxiv.org/abs/2311.06609
- https://arxiv.org/html/2311.06609v1
- Inspected: §2, Lemma 3 and equation (3), plus scope of the paper.
- Gives the exact entrywise inverse formula for an invertible bidiagonal matrix. It exposes the multiplicative/semiseparable structure in the ordered path case, including vanishing off-diagonal entries.
- Does not state the arbitrary-routed branch sum obstruction. Its results about products and numerical perturbations have different hypotheses and conclusions.

Raf Vandebril, manuscript section *Theoretical proof of the structure*, webpage dated 2007-07-17.

- https://people.cs.kuleuven.be/~raf.vandebril/homepage/publications/papers_html/trideig/node3.html
- Explicitly treats inverse lower bidiagonal matrices as known triangular semiseparable objects. Useful corroboration; insufficient by itself for precise priority attribution of the full proposal.

### 6. Exact Fourier/full-spark ingredient

Boris Alexeev, Jameson Cahill, Dustin G. Mixon, *Full Spark Frames*, Journal of Fourier Analysis and Applications 18(6), 1167–1194 (2012).

- https://arxiv.org/abs/1110.3548
- https://arxiv.org/pdf/1110.3548
- Inspected: Lemma 2, §2, PDF pp. 5 and 7.
- Distinct-node Vandermonde matrices are full spark; the first k rows of a DFT are explicitly identified as that construction.
- Therefore composite N is no obstacle for consecutive selected rows. Arbitrary row subsets of a composite-order DFT need not be full spark. No prime-only Fourier-minor theorem is needed.
- The paper itself identifies the Vandermonde fact as old. It does not give the inverse-branch application.

### 7. Products of bidiagonals can represent Fourier

Paul D. Gader, *Bidiagonal factorization of Fourier matrices and systolic algorithms for computing discrete Fourier transforms*, IEEE Transactions on Acoustics, Speech, and Signal Processing 37(8), 1280–1283 (1989).

- Author-hosted PDF: https://faculty.eng.ufl.edu/computing-for-life/wp-content/uploads/sites/68/2020/07/Bidiagonal-Factorization-of-Fourier-Matrices-and-Systolic-Algorithms-for-Computing-Discrete-Fourier-Transforms-.pdf
- Inspected: introduction, equation (1), and Algorithm 1 discussion.
- Fourier admits a product of 2N−2 bidiagonal factors, with a permutation. The paper distinguishes parallel regularity from serial operation savings.
- This does not contradict an additive branch-count lower bound. Products are a different representation class.
- Bibliographic caution: the supplied PDF contains a following, unrelated article on page 1284. Also its reference to the preceding Gader paper has corrupted/inaccurate extracted volume/page text; use the verified publisher record below.

Paul D. Gader, *Tridiagonal factorizations of Fourier matrices and applications to parallel computations of discrete Fourier transforms*, Linear Algebra and its Applications 102, 169–209 (1988).

- https://doi.org/10.1016/0024-3795(88)90325-4
- Publisher abstract inspected. Again concerns products, including Fourier matrices of all orders; it is not an additive-routed-inverse representation claim.

### 8. Graph separation and inverse rank: related but different

Seth Sullivant, Kelli Talaska, Jan Draisma, *Trek separation for Gaussian graphical models*, Annals of Statistics 38(3), 1665–1685 (2010).

- https://arxiv.org/abs/0812.1938
- https://arxiv.org/pdf/0812.1938
- Inspected: Theorems 2.8 and 2.15 and proof setup.
- Gives graph separation characterizations of rank constraints for covariance submatrices, including inverse-concentration models. Illustrates longstanding graph-to-minor methodology.
- Covariance positivity/symmetry and the relevant graph constructions differ from arbitrary-field independently routed inverses. Do not cite its theorem as directly proving the proposed branch bound.

### 9. Modern recurrence/semiseparable context

Tri Dao and Albert Gu, *Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality* (2024).

- https://arxiv.org/abs/2405.21060
- https://arxiv.org/html/2405.21060v1
- Inspected: §3.2.2 scalar SSM recurrence, Theorem 3.5 and remarks on semiseparable conventions.
- Scalar recurrences are presented through diagonally scaled 1-semiseparable matrices. This gives a contemporary application context for parallel first-order recurrence branches.
- It does not identify all modern SSMs with the proposal: larger state, multilayer composition, input-dependent coefficients, and other mixing can exceed the restricted model. No proposed Fourier branch bound located.

Erwan Fagnou, Paul Caillon, Blaise Delattre, Alexandre Allauzen, *Trading Complexity for Expressivity Through Structured Generalized Linear Token Mixing* (2026).

- https://arxiv.org/html/2605.31367v1
- Inspected: Proposition 3.2, §§3–4, theoretical scope.
- Uses (I−B)^(-1)A to organize causal recurrences, then studies graph path/congestion and complexity properties. The direct mixing A and recurrent sparsity class are more general and differently constrained. No exact Fourier branch obstruction located. Relevant context, not a priority match.

### 10. Approximate methods are separate

Yingzhou Li and Jingyu Liu, *Approximate Inversion of Discrete Fourier Integral Operators via Hierarchically Semiseparable Matrices*, arXiv:2609.11520 (2026).

- https://arxiv.org/abs/2609.11520
- Abstract inspected only.
- Combines approximate butterfly and HSS constructions for Fourier integral operators. Neither exact Fourier equality nor the proposed one-layer additive inverse class is its premise. It cannot be treated as a contradiction or as support for the proposed bound.

## Mathematical claim comparison

1. **Inverse graph structure:** classical. In the expanded model, gain-graph contraction is a closer fit than ordered semiseparability alone. The elementary direct graph proof is still valuable for readability and arbitrary zero handling.
2. **Independent routing:** genuinely addressed by the common-refinement argument, but already addressed in reviewed C04 for Hamiltonian branches. The broader denominator class, not routing alone, is the distinction relative to that internal antecedent.
3. **Counting step:** after selecting k=r+1 rows, each branch supplies at most k rank-one column classes. There are at most k^r common cells, each of rank at most r in the sum. A full-spark target permits at most r columns per cell. This is elementary finite-union-of-subspaces counting, not a general matrix-rigidity theorem.
4. **Matroid language:** before endpoint degeneracies, the selected inverse rows represent exactly k independent parallel classes plus possible loops. The Fourier restriction represents the uniform matroid U_(k,N). Entrywise matrix addition is not, in general, the matroid union operation; avoid claiming that Edmonds's union theorem proves this application.
5. **Generality of the target:** the same count works for any matrix with an (r+1)-row full-spark restriction. Fourier is a useful explicit family, but no uniquely Fourier-specific number theory is used.
6. **Sparse correction:** deleting the union of correction supports on those k rows removes at most delta*k columns, giving the stated extension. This is a straightforward robustness corollary, not a proof of conventional rank-r rigidity of the full Fourier matrix.
7. **Strength:** in the enlarged class, constant r is excluded as N grows; r is at least order log N/log log N. This does not improve C04's stronger Omega(log N) Hamiltonian-subclass conclusion. Bounds for r>=2 are not shown sharp. One branch permits at most N=2, a sharp cutoff in the admissible Fourier fields. Two branches are ruled out at N>=19, not merely N>=33.
8. **Runtime:** no general Omega(Nr) conclusion follows. O(Nr) is an upper bound for independently applying r branches. Shared arithmetic, products, larger-state recurrences, and arbitrary preprocessing are not controlled by branch count alone.
9. **Approximation:** a separately proved finite-N corollary is included in `FINITE_N_APPROXIMATION_COROLLARY.md`. For normalized complex Fourier, k=r+1, and N>r*k^r, spectral and Frobenius error are at least N^(-1/2)*(2sin(pi/N))^(k(k-1)/2)/k^(k-1). This tiny positive bound proves exclusion from the closure at fixed N,r. It has no positive accuracy guarantee uniform in N and does not exclude practical approximate methods. It is a new deduction within this review, not a result attributed to a cited paper or the still-unaudited separator proposal.

## Suggested claim wording

“We extend the class of inverse-branch sums for which exact Fourier representation can be excluded, obtaining N <= r(r+1)^r for independently routed inverses of arbitrary column-two-sparse matrices over suitable fields. The proof combines classical sparse-graph inverse structure with full-spark column counting. A previously reviewed rectangle argument already yields the stronger Omega(log N) bound in the complex Hamiltonian subclass; the present result broadens coverage rather than improving that subclass asymptotically. This is not an unrestricted Fourier arithmetic lower bound. Public-literature priority for the precise application remains unresolved.”

## Search coverage and remaining uncertainty

Search families included permuted semiseparable sums; cyclic bidiagonal inverse matrices; Fourier sparse-inverse representations; low-rank column partitions; full-spark Vandermonde frames; graph-induced inverse rank; gain-graph incidence, contraction, and frame matroids; generalized networks and binet matrices; scalar recurrence/SSM expressivity; and approximate HSS/Fourier transforms.

Several initial exact-phrase queries produced no useful match. This does not establish absence. The gain-graph branch was opened after the audit's column-two-sparse generalization and yielded a much closer source. A publication-grade priority review should follow older generalized-network basis/contracted-potential literature, citations to Zaslavsky's contraction theorem, and work on sparse dictionary/union-of-subspaces representation lower bounds. Such a review might identify the counting application under different terminology. No exhaustive database, citation-network, or unpublished-literature search was performed.
