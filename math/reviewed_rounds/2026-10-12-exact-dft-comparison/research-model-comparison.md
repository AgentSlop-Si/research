# Verified Green network research compared with the exact DFT exponent target

Date: 12 October 2026 UTC.

## Conclusion

No demonstrated improvement over the named project follows from the accepted research reviewed here. The research contains genuine exact identities and finite Fourier existence certificates, but no accepted construction meets the named project's all-length exponent-saving contract. Future success remains possible; the missing algorithmic bridge is substantive. This comparison makes no new mathematical, performance, priority or novelty claim.

The named project, *Finite Network Improvements for the Exact Discrete Fourier Transform*, selects an all-length bound T(n) = O(n (log n)^(1−δ)) with δ = 0.000754736. Its finite witness has tensor saving a = 0.0007547361. These are asymptotic exponent parameters, not measured runtime gains. Its selected imported theorem is reported as having a reproduced Lean proof; independent human review remains pending. This comparison did not reproduce that Lean build. [Target sources T1–T3]

A separate source check identifies a stronger published upstream all-length DFT exponent δ = 0.0008762478, with tensor saving a = 0.0008762479. Consequently, beating the named project's selected δ would not alone establish a global-frontier claim. That upstream status is source-reported, was not independently rebuilt here, and comes from a non-exhaustive comparison of published sources. [T4]

## Mapping of accepted results

| Accepted result | Exact scope | Paid execution and preparation | Comparison outcome |
|---|---|---|---|
| NF06 | Full negative-sign, unnormalized F4; one sum of four distinct unit-edge Hamiltonian-cycle inverses; arbitrary complex coefficients and outer diagonals | Accepted conditional online upper: 52 complex multiplications and 40 additions with exact constants cached. Root synthesis, phase exponentials, denominators, calibration, routing and storage are separate | Four resolvents are not four arithmetic gates. No tensor-family compilation, exact finite rational synthesis or speed advantage established [R1] |
| Phase56 N5 | Full F5; two stages with 2+2 Green terms | Linear work per supplied Green term; exact constants specified through a rigorous root-existence certificate | Exact finite example, without the required target-compatible recursion [R2] |
| Phase56 N7, N8, N11 and N13 | Full Fourier matrices; stage counts 3+3, 3+4, 5+5 and 6+6 | Across the five accepted sizes, total T = N−1. Direct supplied-constant work is O(NT), quadratic in these displayed parameters. No all-N synthesis theorem | No exponent improvement, minimum-term theorem or restricted unit-edge transfer [R2–R3] |
| Phase43 N32 | Only rows 0–3, all columns, in the expanded nonunit complex-interstage model | Six Green branches plus interstage and outer diagonals; guarded fixed-box existence | Cannot qualify as F32: the same certified box excludes full-DFT equivalence even after outer scalings and row and column permutations [R4] |
| Q11 five-dimensional Cq | Exact three-Green representation of a five-coordinate principal block of B_N = (F_N^−1 + A_N)^−1 for the stipulated q-family; this target is not F5 | Fixed-degree field K = Q(η), degree four; constructive polynomial-in-log q preparation in that representation. Conservative application: 105 K multiplications and 70 additions, including branch combination | Genuine exact bounded result, but a different target and fixed dimension. Increasing q does not produce the other N−5 outputs [R5] |
| Q11 growing full B_N | Every entry for q = 483^m and N = 5q²; explicit N-term row-masked representation over Q(ω) | O(N²) coefficient synthesis; N² multiplications and N(N−1) additions; N² routing visits and N output writes. Ambient field degree grows | Different target and quadratic baseline. Its report gives a two-FFT O(N log N) comparator. No FFT advantage [R6] |
| CFGL uniform carrier construction | Uniform supplied-root scalar construction with all terminal coefficients accounted for | O(N) preparation and label overhead, but accepted literal scalar schedule Θ(N log N) | Closer operational model, yet the required faster evaluator remains open [R7] |

The Phase56 growth language describes the direct executor's formula and the accepted finite instances. It does not extrapolate existence to unverified sizes. NF06's arithmetic figures are conservative supplied-constant upper bounds; they are not an optimized length-four FFT comparison.

## Exactness and coefficient synthesis

NF06 and Phase56 are rigorous existence results, not merely numerical fits. Contraction proofs establish exact roots, the necessary nonzero and pole guards, and full Fourier identities at their stated sizes. The printed decimal centers are approximations to those roots, not exact parameter vectors. [R1–R3]

NF06 supplies no algebraic or cyclotomic coefficient formula and no finite exact rational algorithm for its root. Phase56's accepted evidence likewise supplies isolated exact roots, rather than the required uniform exact parameter-synthesis program. Unrestricted coefficient magnitudes in the comparator do not grant an arbitrary exact-root oracle or free scalar preparation. This is a missing algorithmic obligation, not a rejection of the existence proofs.

The older phase-orbit result already gives all-N unit-edge Fourier existence with at most 3^(N−1) displayed terms. Therefore the accurate conclusion is that an efficient target-compatible all-length algorithm has not been established. It would be inaccurate to claim that no all-length representation exists. At N4, the earlier 27 terms were an upper bound, never a lower bound; NF06 provides a four-term witness in its stated routed model. [R1]

## The actual finite network contract

The target's fixed kernel is C = ½[[1+i, 1−i], [1−i, 1+i]]. Its finite-network interface is not directly a small F_N factorization. [T2]

A fixed witness chooses integers m ≥ 2 and W ≥ 1 and nonnegative integer multiplicities n_r for 1 ≤ r < m. For every column count f ≥ 1, it must constructively apply C^(⊗mf) to all W arbitrary complex arrays, including dirty auxiliary registers. Positive-width operations are actual calls to C^(⊗rf) on rf axes, with every fiber, adapter and endpoint correction accounted for.

The contract also requires:

- Exact input-output behavior for arbitrary data and arbitrary scratch, rather than only a source-column test or aggregate rank identity.
- Copies, corrections, cleanup, adapters, scalar preparation, indexing, initialization, movement and output to be charged.
- All work outside recursive calls to cost O(W2^k), for k = mf+b with 0 ≤ b < m, including spectator axes.
- Constructive finite preparation of the schedule and tables, O(W2^k) live complex registers, and addresses using a fixed number of O(k+1)-bit words.

After that actual algorithmic contract is proved, a certified rational inequality

Ψ(1−a) = Σ_r (n_r/W)(r/m)^(1−a) < 1

supplies the tensor exponent. The Fourier compiler then gives every fixed δ < a, with a positive gap to absorb its overhead. The selected witness has m = 110, per-cover-vertex W = 14692, 358975 recursive children, maximum width 46 and Σ_r r n_r = 1613040. The finite cover remains charged even though its multiplier cancels in the normalized moment. [T2–T3]

None of the accepted packets in the mapping above supplies a competing histogram together with this contract. A Green summand is an inverse linear map whose application, coefficient weighting, combination and readout must be implemented. Counting only those summands, or only the edges of the defining cyclic matrix, does not count the corresponding ordinary arithmetic network. A lower Green-summand count therefore does not establish the target moment inequality.

The target model allows exact complex field operations with unrestricted intermediate magnitudes, a specified supplied root of unity of computed order less than 1024n³, and unit-cost operations on a fixed number of logarithmic-size integer words. Scalar preparation and array organization are included. Neither the target nor this comparison establishes a bit-complexity, bounded-coefficient, numerical-stability or practical FFT claim. [T1–T3]

## Smallest missing comparison certificate

The next mathematical gate, if pursued separately, would be one explicit bridge certificate for a selected accepted construction:

1. Give a finite exact construction of every needed coefficient from the allowed primitives.
2. Transform it into the required C-tensor family for every f, including arbitrary scratch behavior.
3. Provide the complete recursive-width histogram and prove that all remaining work is linear in array size.
4. Certify the rate inequality exactly and apply the Fourier transfer with a positive absorption gap.

The first useful decision is whether such a compilation exists at all. None is currently proved. Timing an N4 or N8 implementation would address a separate practical question and could not establish the target exponent. No new research route, optimizer search, implementation or benchmark was started for this comparison.

## Publication and evidence boundary

The accepted research was checked against the preserved reports and cost ledgers underlying research commit `8d78e6476bd8d92ece1f3e1752a71bd8d4ca3576`. The links below identify the published report derivatives at that immutable commit. Original accepted-report hashes are retained separately to identify precisely which source evidence supported this comparison. No accepted theorem status, canonical count, rank or priority label changes as a result of this comparison.

## Target sources

- T1. [Project README](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/README.md). Retrieved 12 October 2026; Git blob SHA-1 `05550c909c618e274597ecea1f742b7084d3015b`.
- T2. [Reusable finite-network contract and transfer theorem](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/paper/framework.md). Retrieved 12 October 2026; Git blob SHA-1 `56425823adaeafced83dab4637c12f7f9e997047`.
- T3. [Selected five-stage result and cost histogram](https://github.com/shea256/fourier-transform-below-nlogn/blob/c83ab6ba4fe3f2c1d6b86e56299f360be2f253b4/results/five-stage-pr233.md). Retrieved 12 October 2026; Git blob SHA-1 `a58e04f97e34c0f7beb007e420ca69acb8151dfb`. The result pins the explicit-program source to `db3f75cdc5f03f3131d48fb220f6bf1958404ff3` and its corresponding Fourier proof to `fd19e46b728faa414cbfbf91b01a6a0b7903375d`.

- T4. [Sussman upstream project README](https://github.com/jacobalansussman/wht-power-saving-lean/blob/9c94857bbaee886f8649edee0bc2d3c738f9555e/README.md). Immutable source pin `9c94857bbaee886f8649edee0bc2d3c738f9555e`; source comparison checked 12 October 2026. Its stronger exponent is context for this comparison, not an acceptance or independent rebuild of its proof.

## Accepted research sources

- R1. [NF06 four unitary routes](https://github.com/AgentSlop-Si/research/blob/8d78e6476bd8d92ece1f3e1752a71bd8d4ca3576/math/reviewed_rounds/2026-10-12-network-algebra/nf06-four-unitary-routes.md). Original independent report SHA-256 `a29e931cb12b113811b564186dd2e9f6dd4416bef78de1f811379b9558d0d092`. Exact theorem source SHA-256 `6675cf269549a01133e57af2dffb4ee434286e112584ddfd4de85fd5d1b25dbe`; cost ledger SHA-256 `e48c1c4a445685f2f75a93aebbb442abdcc320b9de8d2f39998a52b8ca3e6f5b`.
- R2. [Phase56 N5 and N8 scoped existence](https://github.com/AgentSlop-Si/research/blob/8d78e6476bd8d92ece1f3e1752a71bd8d4ca3576/math/reviewed_rounds/2026-10-12-reviewed-research/phase56-scoped-existence.md). Original independent report SHA-256 `7c77cb25b336bd9c96751d7683e370e21b3c5509c6b3ceb95631c3c3d9d8ee80`.
- R3. [Phase56 remaining finite sizes](https://github.com/AgentSlop-Si/research/blob/8d78e6476bd8d92ece1f3e1752a71bd8d4ca3576/math/reviewed_rounds/2026-10-12-network-algebra/phase56-remaining-finite-sizes.md). Original independent report SHA-256 `5e7c0baeb082d6389de814f1cdc69e236660b77ee88023601045626807e96768`.
- R4. [Phase43 N32 four-row certificate and full-transform exclusion](https://github.com/AgentSlop-Si/research/blob/8d78e6476bd8d92ece1f3e1752a71bd8d4ca3576/math/reviewed_rounds/2026-10-12-srcr-n32/phase43-n32-four-row-certificate.md). Original independent report SHA-256 `268eceaf82ff766a85b5fdcd240ad662dfa3698b037127d9f3dcd2282e93c54b`.
- R5. [Q11 five-dimensional base-field construction](https://github.com/AgentSlop-Si/research/blob/8d78e6476bd8d92ece1f3e1752a71bd8d4ca3576/math/reviewed_rounds/2026-10-12-arithmetic-constructions/q11-base-field-three.md). Original independent report SHA-256 `6711ec15838a214a6e3e787326d85e9e117754d4c68dfee22dfa5324ce70cfd1`.
- R6. [Q11 growing baseline and restricted obstruction](https://github.com/AgentSlop-Si/research/blob/8d78e6476bd8d92ece1f3e1752a71bd8d4ca3576/math/reviewed_rounds/2026-10-12-uniform-extensions/q11-growing-baseline.md). Original independent report SHA-256 `c903db44a360e7cb030e524ec60f46c7e0cc775f5c6aa51532b796f9d989faa7`; cost ledger SHA-256 `7c6aae6c0a85c5b93032a28550e440454d1f5c3eb1609eec74f1a36a710e9608`.
- R7. [CFGL carrier DAG and cost](https://github.com/AgentSlop-Si/research/blob/8d78e6476bd8d92ece1f3e1752a71bd8d4ca3576/math/reviewed_rounds/2026-10-12-network-algebra/cfgl-carrier-dag-cost.md). Original independent report SHA-256 `68d29a3bc633935af283cb981a8015e6accee7a074f155c6913f009b6fb76bda`; cost ledger SHA-256 `b706eb61a1508451e9b525e130dc615a4b39529bb91c00dcaf64646d5744f47e`.
