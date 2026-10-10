# Independent review of the matrix extensions

Date: 10 October 2026. Both proposals below are **accepted in their stated models**. The review rederived the improvements, read the inherited separator and endpoint proofs, and checked the integer and singular-value implications. No supplied research program was executed.

## M1. Improved separator selection and inverse-sum threshold

### Hypotheses

U is an N-by-N complex flat unitary. There are r≥1 branches L_i Q_i^(-1) R_i, with invertible Q_i and independently routed monomial-support endpoints; endpoint entries may vanish. In each branch's symmetric bipartite support lift, every relevant nonnegative marking admits a half-balanced vertex separator of size at most q, where q≥1 is an integer. Treewidth at most q−1 suffices. Column sparsity two gives q=2 through the improved pseudoforest argument below (the inherited treewidth shortcut gave q=3); higher column sparsity alone does not establish this hypothesis.

### Independent combinatorial proof

Start with m marked target rows and m marked target columns, m≥4q. Delete a separator of size at most q and trim each color to t=m−q surviving marks. Each remaining graph component contains at most m≤4t/3 marks; total surviving weight is 2t.

There exists a union A of components with weight in [2t/3,4t/3]. If one component has weight at least 2t/3, use it alone. Otherwise accumulate components until first crossing 2t/3; the previous partial weight and added component are each below 2t/3. Its complement B also has weight at least 2t/3.

Write the color counts in A as a,b and in B as t−a,t−b. At least one of (a,t−b) and (t−a,b) has both coordinates at least t/3. If both fail, the four combinations of failures either force one side's total below 2t/3 or force both a<t/3 and t−a<t/3 (or the analogous contradiction for b). Because counts are integers, the successful orientation supplies ceil(t/3) rows and columns.

The inherited complementary inverse-submatrix rank identity bounds this cross-component rectangle by q. Previously established branch ranks persist under restriction. Thus the exact guaranteed recurrence is

m_(j+1)=ceil((m_j−q)/3), provided m_j≥4q.

This improves the old floor((m−q)/6) guarantee. Three equally mixed components show that the abstract cross-color fraction 1/3 cannot be improved from only these hypotheses when q=0; this is sharpness of the grouping lemma, not an optimality claim for the entire representation threshold.

### Additional accepted refinement: q=2 for weighted pseudoforests

Let W be the total nonnegative graph weight. If no connected component has weight greater than W/2, no separator is needed. Only one heavier component can exist. A weighted tree centroid handles a heavy tree component with one deleted vertex. For a unicyclic component, aggregate the weight of the attached tree at each cycle vertex v into w_v. If some attached tree has w_v>W/2, place all outside mass W−w_v at its root v and choose a centroid of the augmented tree. If the centroid is not v, its component containing v reconnects precisely the outside graph represented by that mass; if it is v, the outside graph has weight below W/2. All resulting components obey the desired bound.

Otherwise every w_v≤W/2. Delete any cycle vertex x, then choose a weighted centroid y of the remaining cycle path with aggregated weights w_v. The two remaining arcs have aggregate weight at most half the remaining path weight, hence at most W/2. Attached branches severed at x or y have weight at most w_x or w_y, also at most W/2. Thus {x,y} is a separator of size at most two. Zero weights and disconnected graphs are covered. The bipartite lift converts singleton-loop components into trees, and other components into ordinary unicyclic graphs.

Consequently two-sparse-column inverse sums satisfy N≤2r9^r+2(3^r−1), or N≤8r9^r+4(3^r−1)+2 with a diagonal correction. This is a classical weighted-graph refinement, not claimed new separator theory.

### Exact global bounds and integer audit

Put a=3^r and c=q(a−1)/2. Iteration yields m_r≥(m_0−c)/a. Flatness and unitarity imply rank U[I,J]≥m_r²/N, while the branch sum has rank at most qr. Therefore an exact representation requires

- without a diagonal correction: N≤qr9^r+q(3^r−1);
- with an arbitrary diagonal correction: N≤4qr9^r+2q(3^r−1)+2.

For the second statement choose initially disjoint row and column sets of size floor(N/2); all subsequent restrictions retain disjointness and kill the diagonal. The floor gives the extra +1 in C=q(a−1)+1, and hence +2 in the threshold.

For completeness, if the first displayed bound were violated, every intermediate input satisfies m_j≥N/3^j−q/2>4q for j≤r−1. In the diagonal case the analogous bound is m_j≥N/(2·3^j)−(q+1)/2>4q. Thus recurrence use is noncircular. Finally, with b=qr a², (N−c)²−Nb=N[N−(b+2c)]+c²>0; the diagonal argument uses b=4qr a² and C in place of c. The contradiction includes odd N, q=1 and r=1.

### Explicit approximation extension

For any resulting m-by-m block B=U[I,J] and R=qr<m, its singular values are at most one and sum of squares is m²/N. Hence, if m²/N>R,

σ_(R+1)(B)²≥(m²/N−R)/(m−R).

Every branch sum in the specified grammar therefore has operator-norm error at least the square root of this expression; the same works with a diagonal on disjoint indices. The Frobenius error squared is at least m²/N−R. These bounds are uniform over branch coefficients and independently selected routes, because the proof selects a permitted rectangle after seeing the fixed approximating matrix. They do not apply to arbitrary input-dependent nonlinear evaluation.

### Novelty

The new-to-corpus contribution is an elementary sharper grouping step, the resulting base 9 rather than 36, and the sharpened singular-value denominator. Inverse rank closure, separator theory and low-rank approximation inequalities are established. This is a genuine strengthening of the existing scoped theorem, not an arithmetic lower bound or priority-cleared standalone graph-width result.

Primary antecedents retained: graph-induced inverse rank structure, https://arxiv.org/html/1911.05858 ; classical nullity identity, https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf . The matrix lead owns the expanded primary comparison.

## M2. Quantitative critical-cut gap for dyadic Fourier matrices

### Exact statement and proof checked

Let N=4L=2^m≥8, U the normalized Fourier matrix, R any 2L−1 row indices and H any 2L+1 column indices. Set I=R^c and A=U[I,H]^*U[I,H]. Then V=U[R,H] satisfies V^*V=I−A.

For h=2L+1 and c_H(s)=|H∩(H−s)|,

tr A²=N^(-2)Σ_s c_H(s)|Σ_(i∈I)ω^(is)|².

Every nonidentity cyclic translation has even-length cycles. Since h is odd, c_H(s)≤h−1 for s≠0. Parseval and the zero-frequency term give

tr A²≤[(h−1)Nh+h²]/N²=B_L,

B_L=L+3/4+1/(4L)+1/(16L²)<L+1.

If a_1≥...≥a_h are A's eigenvalues, then σ_(L+1)(V)²=1−a_(L+1), because h=2L+1. Also (L+1)a_(L+1)²≤tr A². Consequently

σ_(L+1)(V)≥δ_N=sqrt(1−sqrt(B_L/(L+1)))>0.

The asymptotic δ_N~1/sqrt(2N) is correct. Every independently reordered Fourier matrix is therefore at operator distance at least δ_N from any matrix whose critical-cut rank is at most L.

The same lower-bound proof works for a normalized character table of any finite abelian 2-group of order N≥8: translations still have even orbit size and character Parseval still holds. The matching bit-reversal upper construction remains a separate cyclic theorem.

### Product and rescaling boundaries

Common-order products inherit critical off-diagonal rank at most the sum of factor ranks. Any interstage permutation must be counted as a factor with its actual cut rank. Nonsingular diagonal endpoints change the lower error scale by min_i|D_ii| min_j|E_jj|. Neither statement charges arithmetic evaluation cost, and freely moving coordinate systems invalidate an uncharged product inference. The gap decays with N and must not be called a fixed-tolerance lower bound uniform in dimension.

### Novelty

The explicit gap is a straightforward quantitative corollary of the existing second-moment proof plus singular-value approximation theory. It is a useful scoped robustness extension. Its status is not a new unrestricted FFT lower bound, and worldwide priority remains unresolved.

## Fresh controls

The self-authored `independent_checks.py` checks threshold boundary cases with exact integer arithmetic and all 3,136 critical N=8 submatrices numerically. Results appear in `independent_check_results.json`. These controls supplement the proofs and do not convert floating calculations into exact certificates.

## M3. Strengthened fixed-stage quadratic-phase gap

**Status: accepted analytic strengthening; supplied modular examples and exceptional-locus certificates not freshly executed or independently reconstructed here.** The source is the newly supplied *Quadratic Fourier–Green Phase Rigidity*, Theorem B, inspected as inert text.

Retain fixed invertible A,C, an entrywise nonzero B, the three-column maps P_j, and the full-column-rank quadratic lift Q_J with smallest singular value s>0. Put M_P=(Σ_(j=0)^2||P_j||²)^(1/2), b_*=min|B_uj|, and beta_N=sqrt((N+1)/(2N)). Then every invertible diagonal gauge L,D,E satisfies

||LADBEC−F||_2 ≥ beta_N s b_*/[M_P ||A^(-1)||_2 ||C^(-1)||_2].

For the source's unscaled symmetric monomials,

||v(c)||²=(||c||⁴+Σ|c_i|⁴)/2 ≥ [(N+1)/(2N)]||c||⁴.

Thus the Euclidean vector of two-by-two minors has norm at least beta_N s||c||². The Cauchy–Binet and rank-one-distance inequalities in the source give dist_F(Z_J(c),rank≤1)≥beta_N s||c||/M_P. Normalize ||c||=1 by the gauge scaling L→tL,D→D/t. Finally,

||diag(c)(F−M)||_F²=Σ_i|c_i|²||row_i(F−M)||²≤||c||²||F−M||_2².

This weighted-row inequality removes the source's unnecessary ||F−M||_F≤sqrt(N)||F−M||_2 step. Multiplying the fixed A^(-1),C^(-1) norm factors and the entrywise-division factor 1/b_* gives the displayed bound. Relative to the source constant, the improvement is exactly sqrt(N+1).

The constant still depends on fixed stages and may tend to zero across a varying family. This does not obstruct every possible wiring or input-dependent evaluator and does not establish an arithmetic lower bound. Its mechanism is an elementary strengthening of existing norm estimates, not a priority-cleared new algebraic geometry theorem.
