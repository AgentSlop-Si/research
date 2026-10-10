# Next exact Fourier factorization gate: from necessary ranks to actual parameters

**Goal:** Prove or disprove the existence of uniformly generated, exact `F_N=L(A_1+A_2)D(B_1+B_2)` Green resolvent constructions with `O(N)` charged sequential evaluation on every *fresh arbitrary input*. This remains unsolved by the project.

## Staged falsification before parameter optimization

1. Fix N, cycle permutations, endpoint gauges, and branch weight parameterization. Count all free parameters, including phase/root generation. Reject the wiring by Phase 26 Green-cut / two-sided rank budgets where applicable.
2. Generate the first two B columns via `O(N)` Green applications. Build the `N×N` phase pencil K symbolically for very small N or matrix-free for probing larger N.
3. Demand rank(K)<N. For any surviving singular K, apply **all 2N rank augmentation tests** from Theorem II. This rejects cases where every kernel vector has forbidden zeros or a vanishing first Fourier column.
4. In the generic corank-one case, eliminate middle d using any nonzero cofactor column of K. Substitute this expression into K_j d=0 for *all* j, with exact arithmetic. Handle K-rank<=N-2 and exceptional factor branches separately. The resulting polynomial system contains only the original Green weights/gauges, not independently free interface gauge variables.
5. For numerical exploratory fitting only, minimize the O(N)-work two-column *projective* loss with the exact analytic gradient. At a promising candidate, run the full Weyl covariance test and seed normalization. Use exact cyclotomic or sufficiently safe modular algebra to obtain an actual proof, not just a small floating-point residual.
6. Require an explicit all-length formula for permutations/weights and prove full computational cost `o(N log N)` (preferably `O(N)`) in a single stated arithmetic model. Distinguish stability and bit complexity. Compare against the already-published exact sub-N-logN arithmetic benchmark.

## A concrete potentially decisive test

For N=4,8,16, select the least symmetric non-affine four-Green wiring that survives moving-interface rank tests. Form K over an exact cyclotomic representation or a split large finite field. If rank K=N-1, obtain the cofactor gauge d, then substitute in K_1,...,K_(N-1). Seek:

- a symbolic *positive identity*, or
- a reproducible nonzero minor/resultant **excluding all coefficient choices for the fixed wiring**, with exceptional denominator branches covered.

A single generic nonzero determinant specialization excludes *generic* coefficients, **not all coefficients**. Likewise, finite-field absence of solutions does not automatically exclude complex solutions. Any universal no-go must quantify over all admissible non-affine permutations/weights or carefully state its smaller family.
