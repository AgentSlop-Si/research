# Combined phase13–16 decision matrix

| Candidate | Verified benefit | Hard obstacle / known identity | Status |
| --- | --- | --- | --- |
| Phase13 mixed-radix randomized sketch | O(N) arithmetic per row at fixed odd cofactor with coordinatewise MSE | Rank N/M; exact full vector reconstruction costs M phase passes | Approximation only |
| Phase14 adaptive phase bank | Exact full-vector projection error certificate | Worst-case inputs fill all banks | Exact on structured subspaces |
| Phase14 noncommuting local Gram frames | Full-rank exact representations, certified Gram residual | Generic exact reconstruction still M long scans | Structured approximations / full-rank representation |
| Phase15 stationary Toeplitz charts | Eliminate M redundant Green scans | Collapses into gauged Cooley–Tukey O(NlogN) | Constant-factor improvement only |
| Phase15 nonstationary chirp family | Full-rank local frames with variable block period | Exact lower bound on condition number can grow exponentially | Precision obstruction |
| Phase16 global Weyl–Green L | Noncommuting, cond<=2.5, exact O(N) inverse, dense forcing | LF=FP and F=L^-1B; FFT-equivalence O(N) both ways | Exact negative gate |
| Phase16 arbitrary permutation Green | Irregular cross-block graph with O(N) cycle inversion, union-find verification, cond<=2.5 | Forcing remains dense and FFT-equivalent by the fast inverse reduction | Exact negative gate |
| Phase16 finite q-term graph union | Exact F conjugation for all signed-exponent Weyl atoms | Remains q-term input preconditioning F P | Exact negative gate |
| Pair/local unitary graph union | The radix-2 FFT saturates all pair-unitary entropy gates | Prior art Ailon 2013 Ω(NlogN) in this restricted model | Prior-art lower-bound gate |
| General nonunitary nonlocal all-input FFT circuit | Not resolved | Must expose genuinely cheap forcing / non-Weyl low-complexity algorithm, charge all precision/work | OPEN |

No row in this table establishes an unrestricted Ω(NlogN) lower bound or a novel o(NlogN) upper bound. Do not conflate phase13 stochastic error with uniform operator norm or exact output.
