# Next gate: synthesize, rather than reject, a uniform Green FFT

The new full-rank quadratic certificate kills generic and many exceptional candidate wirings, including some where the previous commutator already vanished. The *surviving* locus is `rank(Q_J) < N(N+1)/2`, a proper algebraic condition on the chosen weights for any wiring with a nonzero full-rank specialization.

1. Work on `N=4,8,16`, with the true power-of-two FFT conventions, and choose non-affine cycles that already pass the earlier dyadic/two-sided spectral-separator tests. **Do not repeat** affine-run Green ranks, subtree caching or CrocSwap work.
2. Parametrize Green weights symbolically or with exact cyclotomic coefficients. Compute the rank-deficiency minors of Q_J and eliminate selected parameters.
3. For each surviving parameter family, find `ker(Q_J)`, then impose the **Veronese decomposability relations** `v_ab v_cd = v_ac v_bd` (with appropriate indices) and require a vector `v(c)` for some `c` with all entries nonzero.
4. Enforce the remaining Fourier columns and both endpoint gauge nonzero conditions. A singular Q_J alone does **not** prove factorization exists.
5. Attempt a length-doubling formula relating the exceptional solutions for N to those for 2N. This is the missing scalable identity; fitting individual sizes cannot establish O(N).
6. If any positive all-length identity appears, independently verify Fourier Weyl covariance and basis vectors; cost **all** parameter preparation, root construction, arithmetic, indexing, memory, and precision. Applying a preselected weighted Green resolver takes O(N), but obtaining suitable parameters is unsolved.

**Stop rule:** no `exact O(N)` or `publication novelty` statement unless accompanied by an all-length charged construction and a defensible prior-art review.
