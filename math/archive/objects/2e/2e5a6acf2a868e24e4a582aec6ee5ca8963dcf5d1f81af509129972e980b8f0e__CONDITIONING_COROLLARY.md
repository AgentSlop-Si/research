# Optional uniformly conditioned counterexample over the complex numbers

10 October 2026 UTC. A separate analytic corollary to THEOREM.md; independent audit status is recorded separately.

Fix a real number α with 0<α<1/√2, and replace the theorem's denominator by

    Q_(h,α) = I − αP_h.

All supported entries are nonzero and its bipartite support is exactly the same tree G_h. The forest-matching lemma makes every submatrix rank of Q_(h,α) equal to the corresponding rank of Q_h=I−P_h. Thus every independent ordering pair has the same separation width. Inverse-rank invariance gives, over C,

    floor((h+1)/4) ≤ sr(Q_(h,α)^(-1)) ≤ h.

The inverse entry on an ancestor–descendant pair at distance d is α^d; all other entries are zero.

Nevertheless the spectral condition numbers are bounded independently of h. Distinct rows of P_h have disjoint child supports, so P_h P_h* is diagonal with entries equal to the number of children. For h≥1 its largest diagonal entry is two, giving ||P_h||₂=√2. For every vector x,

    (1−α√2)||x||₂ ≤ ||Q_(h,α)x||₂ ≤ (1+α√2)||x||₂.

Therefore

    κ₂(Q_(h,α)) = κ₂(Q_(h,α)^(-1))
               ≤ (1+α√2)/(1−α√2).

The rational choice α=1/2 gives the explicit uniform bound κ₂≤3+2√2<6. The h=0 denominator is the scalar identity, with condition number one.

This strengthens the exact-rank counterexample, but says nothing by itself about numerical rank at a fixed tolerance: exponentially small distant-ancestor entries may be discarded in an approximate representation. Exact and tolerance-dependent numerical rank must remain distinct.
