# Proposed logarithmic branch obstruction via weighted separators

Root analytical proposal, 2026-10-10. Requires independent proof audit. This may strengthen the accepted N<=r(r+1)^r branch obstruction to r=Omega(log N) for complex flat-unitary targets. It is not a general arithmetic-runtime lower bound.

## Proposed statement

Let U be any complex N-by-N unitary with every entry of magnitude 1/sqrt(N). Suppose U=sum_{i=1}^r L_i Q_i^{-1} R_i, with arbitrary independent monomial-support endpoints (zeros allowed), and each Q_i invertible with at most two nonzeros per column. Proposed necessary inequality: N<=12 r 36^r, hence r=Omega(log N). Constants deliberately loose. An extra arbitrary diagonal correction should be covered with N<=48 r 36^r by starting with disjoint half-size target row and column index sets.

## Structural graph and inverse separator

For each Q, the support graph on row variables with each two-support column an edge and singleton column a loop is a disjoint union of unicyclic components by invertibility and column independence (accepted preceding audit). Define H=[[0,Q],[Q^T,0]], so H^{-1}=[[0,Q^{-T}],[Q^{-1},0]]. Its undirected bipartite support graph is a pseudoforest: subdividing ordinary column edges preserves cycles, while a singleton column becomes a leaf. Thus it has treewidth<=2.

For arbitrary target row and column sets R,C of common size m, independent endpoint permutations map them injectively into the second and first halves respectively. Ignore scalar endpoint values for rank upper bounds, keeping zero-weight rows/columns if needed. Give these 2m vertices unit weight. A weighted treewidth-two separator X of size<=3 leaves every component with weight<=m (centroid of a tree decomposition, assigning every vertex's weight to one bag).

For a partition of remaining components into A,B, no H edges join A and B. The general inverse nullity theorem gives rank H^{-1}[A,B]<=|X| even if H[A,A] or H[B,B] is singular. Direct rank form: rank H^{-1}[A,B]=rank H[B^c,A^c]+|A|+|B|-2N. H[B^c,A^c] has zero A-by-B block and rank<=2|X|, while |A|+|B|=2N-|X|. Thus rank<=|X|.

## Two-color selection with a constant loss

Assume m>=12. Removing X leaves at least m-3 marked R vertices and at least m-3 marked C vertices. Trim each color to m'=m-3. Each remaining component's total retained weight is <=m<=4m'/3. Total weight is2m'. Partition components into A,B each of total retained weight >=m'/3: if a component has weight>=m'/3, use it alone (it has weight<=4m'/3); otherwise greedily accumulate components to reach m'/3, stopping below2m'/3.

Write R_A=a,C_A=b, so R_B=m'-a,C_B=m'-b. If both A and B have total weight>=m'/3, at least one orientation has both cross-color counts >=m'/6. Otherwise either one side has combined weight<m'/3 or the total of one color would be<m', contradiction. Select equally sized R',C' from that orientation, size at least floor((m-3)/6). These inverse-submatrix rows and columns lie in separated sides, so the branch restriction has rank<=3.

Apply this selection successively to all r branch graphs. Previously obtained rank<=3 restrictions stay valid under further restriction. The common target row/column sets finally have size m_r, with every branch rank<=3 and hence sum rank<=3r. Recurrence m_{j+1}>=floor((m_j-3)/6)>=m_j/6-3/2 yields m_j>=N/6^j-(9/5)(1-6^{-j}), provided each step has m_j>=12.

## Fourier/flat-unitary rank comparison and constants

Any m-by-m submatrix V of U has Frobenius norm squared m^2/N and operator norm<=1. Therefore rank V>=m^2/N. No full-spark or prime-order assumption is needed.

If N>12 r36^r, the recurrence remains above12 at every required step and final m_r>=N/(2*6^r). Thus rank U[R,C]>=N/(4*36^r)>3r, contradiction. Independently verify all constant/rounding details.

With an added diagonal correction, begin with disjoint target row/column sets of size floor(N/2), on which that correction is identically zero. A conservative threshold N>48 r36^r should ensure final m_r>=N/(4*6^r) and the same contradiction. Check floor(N/2) carefully rather than assume this constant sufficient. Further subsets preserve disjointness.

## Context, caveats, audit questions

The just-reviewed source package green_geometry_source_review_0430/PROOF_AND_SCOPE.md C04 already proves constant-factor rectangle separation for Hamiltonian Green branches and derives the same flat-unitary rank comparison. That gives an Omega(log N) branch obstruction in its Hamiltonian setting; do not claim our weaker projective bound is a new improvement there. The proposed separator proof aims to extend the logarithmic conclusion to arbitrary two-column-sparse denominators (trees/many cycles) and independent endpoints.

Graph-induced rank structures (Chandrasekaran–Epperly–Govindarajan, arXiv1911.05858) and weighted treewidth separators are classical. Combined-application priority unresolved. No Omega(Nr) general evaluation lower bound, no barrier for arbitrary sharing, products, higher-column-sparsity, or approximate computation follows from this statement alone.

Audit especially: H graph really pseudoforest with singleton columns; existence and proof of weighted half-balanced separator<=3; inverse rank formula orientation; two-color partition lemma with trimmed weights; recurrence and thresholds; singular endpoint weights; free diagonal case; whether any inherited source already proves the full generalization.
