# Primary-theorem comparison record

16 October 2026. Full-text theorem comparison for the ALG-071 model. Bibliographic facts and theorem assumptions below were checked in the linked primary texts by the literature reviewer. This record does not claim an exhaustive historical novelty search.

## Monotone submodular knapsack

Maxim Sviridenko, *A note on maximizing a submodular set function subject to a knapsack constraint* (Operations Research Letters 32, 2004), Theorem 1, pp.41–43.

https://thibaut.horel.org/submodularity/papers/sviridenko2004.pdf

Nonnegative, monotone, submodular and polynomially evaluable objective; one additive knapsack with nonnegative integer costs and budget. Guarantee `1−1/e`. Enumerate feasible one/two-element solutions and three-element seeds; complete seeds using marginal-gain/cost greedy. The published complexity is `O(n^5)` value evaluations. Normalization is sufficient but not required. Zero-cost items need preprocessing. A greedy score or storage-overlap heuristic by itself is not this theorem.

## Materialized views and shared maintenance

H. Mistry, P. Roy, K. Ramamritham, S. Sudarshan, *Materialized View Selection and Maintenance Using Multi-Query Optimization*, March 2000 preprint, §6, pp.14–17, especially §6.2. The SIGMOD publication is 2001.

https://arxiv.org/pdf/cs/0003006

The paper jointly chooses materialized intermediates/indices and maintenance plans, allowing recomputation versus incremental maintenance. Its benefit is set dependent: `cost(M,M)−cost(M∪{x},M∪{x})`. The benefit-recomputation shortcut assumes marginal benefit cannot increase as more views are materialized; the paper explicitly says that assumption need not hold. Benefit per space appears in its storage-budget extension. This is an antecedent for shared-maintenance complementarity, not a theorem that the present sequential Fourier objective is submodular or admits a particular approximation ratio.

## Metrical task systems

A. Borodin, N. Linial, M. Saks, *An optimal on-line algorithm for metrical task system* (JACM 39, 1992), definitions pp.746–747 and Theorems 1.1–1.2.

https://www.cs.toronto.edu/~bor/Papers/optimal-online-algorithm-for-metrical-task-systems.pdf

There are finitely many fixed states, fixed positive off-diagonal movement distances satisfying triangle inequality, and a revealed processing-cost vector for each task. The algorithm chooses a state after seeing the current task. For symmetric distances, the optimal deterministic competitive ratio is `2n−1`, with a sequence-independent additive constant. The directed upper bound involves an additional cycle-asymmetry parameter. The general lower bound ranges over arbitrary task vectors; it need not apply to a restricted Fourier task family. Warm cache contents, free eviction, asymmetric builds, and changing freshness need a separate reduction.

## File caching

Neal E. Young, *On-Line File Caching* (SODA 1998), Theorem 1.1 and p.83 footnote 1.

https://www.cs.ucr.edu/~neal/Young98Online.pdf

Each request names a particular file; sizes are positive integers, fetch costs are fixed nonnegative values, and the requested file must be fetched if absent. Landlord's ratio is `k/(k−h+1)` relative to the optimal cache of capacity `h≤k` when its own capacity is `k`. The footnote excludes changing retrieval costs and consistency/invalidation issues; treating changed versions as new files is discussed. Substitute overlapping groups and shared refresh do not satisfy this model automatically.

## Optional historical randomized caching reference

N. Bansal, N. Buchbinder, J. Naor, *Randomized Competitive Algorithms for Generalized Caching* (STOC 2008), Theorem 1.1 and §2.

https://www.tau.ac.il/~nivb/download/webcaching-stoc08.pdf

The inspected conference PDF gives `O(log² k)` for arbitrary page costs/sizes and `O(log k)` for bit/fault models, with normalized sizes in `[1,k]`. Requests still name particular pages and fetch charges are additive. These are historical results, not a current-best assertion. A later journal version was not accessible in the review and was not used for a claim. This optional reference is not needed for any proof in the main report.

## Classical hardness premise

Richard M. Karp, *Reducibility among Combinatorial Problems* (1972), authorized reprint in *50 Years of Integer Programming 1958–2008* (2010), original pp.95–100.

https://sites.math.washington.edu/~thomas/teaching/m514_web/50YearsIP.pdf

The primary reprint's indexed text contains the exact-cover to three-dimensional-matching reduction and attribution to Lawler. The mirror at https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Karp.pdf was opened and verified as the authorized reprint; its scanned body did not extract as text. The original Berkeley link redirected to an inaccessible path and the GWU scan exceeded the tool's size limit. The main report uses only the classical NP-hardness of perfect 3DM plus its own complete, explicitly scoped reduction.
