# Mathematical claim dispositions and scope

This is a static review of the 45 exact assigned source hashes, plus explicitly identified fresh checks. A source containing an assertion or a historical PASS string is not a current successful execution. Programs describing themselves as independent reviewers are still supplied programs and were not run.

## C01. N2048 four-stage cut: accepted for the represented graph

The supplied inert certificate specifies 683 input indices J=1365,...,2047 and 683 output indices I=0,...,682. The fresh checker reconstructs each stage with input-to-output, input-to-lower/upper-state, state-chain and state-to-output edges, and connects stages with 11-bit reversal. It independently finds that the 676 listed vertices cut all designated paths; with no deletions all targets remain reachable.

For a linear scalar-state computation represented by this directed acyclic graph, cutting c internal/boundary scalar vertices factors the selected input/output transfer through at most c scalar values, so its rank is at most c. This requires the explicit graph representation; it does not cover unrepresented communication, arbitrary permutations, other state dimensions, or all four-stage algorithms.

With p=65537 and omega=3^32 mod p, primality and order 2048 are checked. The target block has entries (omega^j)^i for i=0,...,682. Its determinant is the Vandermonde product over 683 distinct omega^j, freshly calculated as 24105 modulo p. Thus the represented transfer cannot equal this finite-field Fourier block. Distinct roots also give the characteristic-zero Vandermonde conclusion analytically. Individual cut-node essentiality is unnecessary and was not rechecked.

## C02. Permutation displacement: accepted scoped theorem

On a cycle C of a genuine permutation, solving (D-P)x=0 determines all cycle coordinates from one coordinate. Consistency permits one free coordinate precisely when the product of diagonal values on the cycle is one. For D_jj=omega^j with omega of exact order N, this condition is sum(C)=0 mod N. Hence nullity is the number of zero-sum cycles.

Only the singleton {0} can be a zero-sum singleton; every other zero-sum cycle uses at least two labels. Their count is at most ceil(N/2). Negation fixes 0, pairs j with N-j, and in the even case fixes N/2 with a nonzero diagonal defect. It achieves exactly ceil(N/2) zero-sum cycles. Therefore the minimum displacement rank is floor(N/2). Inverting omega for the output-shift convention leaves the zero-sum condition unchanged. Fresh direct matrix rank checks exhaust 872 permutations for N=2 through 6. This is a statement about this displacement operator, not a general FFT lower bound.

## C03. Transcript and sequential-state barriers: accepted within the stated models

A list of M linear measurements of an N-vector has rank at most min(M,N). If rank<N, a nonzero vector in its kernel has the same transcript as zero but a different invertible Fourier transform. No decoder depending only on that transcript can be correct for both. For a deterministic adaptive procedure, freeze the measurements selected along the all-zero branch; a vector in their common kernel follows the same branch. This does not assume the decoder is linear, but it does assume each measurement on a fixed branch is linear and all information arrives through that transcript.

For a fixed input-independent scalar recurrence of order r generating all Fourier moments, applying it to each coordinate input produces a monic degree-r polynomial vanishing at all N distinct Fourier roots. Consequently r>=N. With all modal weights nonzero, the N-by-N Hankel matrix is V diag(x) V^T and has full rank. This is a fixed recurrence / linear time-invariant state bound, not an arbitrary computation or input-sensitive algorithm bound.

The separate-execution proxy R*N + N*log2(N/R) assumes R independent full scans and convexly equalized FFT sizes. For integer R>=1 the minimum occurs at R=1 or 2 and equals N*log2(N)+N. It is only a stipulated arithmetic proxy. It excludes fusion, alternative circuits and actual timing. Boundary API bugs recorded in S04 do not invalidate the positive-domain argument.

## C04. Separated Green-bank rectangles: accepted structural lemmas; complex prime theorem conditional

In the same-label setting, take equal lower/upper halves of one order. For each additional order, split their union in half; the two opposite-orientation cross-pairs have equal sizes, and one has size at least half of the old side. Swapping sides flips prior orientations without destroying separation. Thus each final side has at least floor(N/2^t) elements. For multiple cycles, first take a largest common cycle-label cell, losing at most a factor product(c_r).

On a strictly separated rectangle within a nonsingular cycle, the Green distance has a fixed wrapping choice. The entry factors into a row factor times a column factor; diagonal gauges preserve rank at most one. Zero couplings can give rank zero. A sum of t terms has rank at most t. Consequently a target that has full-rank square minors is excluded once floor(N/2^t)>t (or the bounded-cycle adjusted size exceeds t). The all-prime complex conclusion in S11 relies on the separately invoked prime Fourier full-spark theorem; finite-field examples are not a proof of that theorem. The source explicitly concerns sums, not arbitrary products.

With independent row/column endpoint permutations, sort the retained row and column images separately. For equal side size at least two, either the low row half lies strictly below the high column half or the low column half lies strictly below the high row half. If the first strict inequality fails, injectivity and the gap between each low/high half force the second. Repeating this independently for each branch retains floor(N/2^q) rows and columns and rank at most q on the sum. Arc-product factorization handles zero edge weights without division by individual edges, provided the full cycle denominator is nonzero.

A useful all-length exact consequence can be derived without prime full spark: for normalized Fourier U, an m-by-m submatrix has Frobenius norm squared m^2/N and operator norm at most 1. Its rank is at least m^2/N. Thus equality with a rank-q separated bank requires m^2<=Nq. This elementary consequence is distinct from unreviewed broader approximation theorems. No numerical rank tests alone establish those broader theorems.

## C05. Macaulay gates: valid one-way certificates under coefficient provenance

For q homogeneous parameters, degree-three monomials form a vector of length binomial(q+2,3): 20 for q=4, 35 for q=5, 56 for q=6, and 84 for q=7. At a nonzero projective solution of the original quadratic minor equations, every degree-three monomial multiple vanishes under the associated coefficient matrix. The degree-three evaluation vector is nonzero because a nonzero coordinate has a nonzero cube. A full-column-rank matrix therefore excludes any nonzero solution over the relevant field or its algebraic closure. A rank-deficient matrix does not establish a solution.

The source expansion correctly includes both ordered cross terms for unequal parameter indices and uses injective monomial multiplication for each fixed variable. T is anchored at the target rows/columns while source generator indices vary; those are intentionally different roles. Cross-multiplied equations can introduce spurious zero-entry candidates, so passing a necessary gate is not enough to construct a valid diagonal/permutation equivalence.

A modular rank certificate must be tied to the actual family coefficients and any characteristic-zero reduction/lift before making a complex-family claim. That dependency closure is not supplied by reviewing these harnesses alone. Stored streams, finite samples, complete mapping enumerations and full determinant witnesses are separately labeled throughout SOURCE_REVIEW.json.

## C06. Phase32 interpolation: accepted conditional construction; reporting bug confirmed

At each output row i, solving the k-by-k response system enforces the k designated Fourier entries. With an extra branch, solve for a particular vector and a nonzero-support null direction; each of the k solved coordinates forbids at most one choice of the free scalar. The listed field and k range allow the candidate search to avoid these zeros when its preconditions hold. After successful setup, each branch is a cyclic scan and diagonal row scaling, giving O(qN) field operations per input. The finite retry limits are not a proof of universal setup success.

For q=N, the construction can fit every column, but its online cost is O(N^2). For the q<N audited constructions, source code deliberately tests a fresh missing column, dense input and a Weyl defect. No full arbitrary-input FFT speedup is claimed or proved.

The audit's j variable is first assigned to the missing probe at line 238, reused as a cycle label at line 257, and returned as the probe label at line 264. The computations at lines 239–240 occur before overwriting. Fresh inert-data inspection finds wrong labels in 16 of the 17 saved audit records; one label coincides by chance. This review has not re-executed the stored mismatch counts or fingerprints. The comment claiming nonconsecutive columns is also inconsistent with range(k).

## C07. Fourier row-sparse rigidity and product gate: accepted scoped theorem

If S has at most s nonzeros per row, choose m=floor(N/(s+1)) consecutive Fourier exponent rows. At most ms columns are touched by S in those rows; at least N-ms>=m remain untouched. On any m such columns, F-S equals a Vandermonde matrix with distinct nodes, so rank(F-S)>=m. Independent endpoint permutations simply require selecting rows by their original Fourier exponents. Nonzero endpoint scaling does not change the rank argument. The stronger claim rank(F-S)>=N-s is false; the N4, s2, rank-one residual example in the source is a valid counterexample.

For inverse factors A_i=S_i+E_i, the ordered telescoping identity writes product A_i - product S_i as a sum with exactly one E_i in each summand, surrounded by sparse/full products. Therefore its rank is at most sum r_i. The sparse product has at most product d_i nonzeros per row. Exact Fourier equality requires floor(N/(1+product d_i))<=sum r_i, equivalent to N<(1+product d_i)(1+sum r_i). Invertibility is required when interpreting these A_i as inverses of actual layers, although the algebraic product inequality itself does not require it.

## C08. Dense inverse / high realignment escape: structural properties only

A permutation Green solve is linear work in the scalar-field model when each cycle denominator is nonzero. A sum of two such solves remains linear work. Its inverse can be dense and its operator realignment full rank without computing Fourier. The rational/exponentially scaled programs provide structural escape constructions and carefully distinguish exact scalar arithmetic from bit complexity; finite inequality and high-precision diagnostics are not, on their own, all-size proofs.

Dense inverse plus full realignment rank also does not prove the inverse lies outside a sparse-plus-low-rank class. The fresh exact rational N4 control constructs an inverse equal to a row-degree-two sparse matrix plus rank one. The inverse is entrywise nonzero, while the operator has nonconstant response to ones and realignment rank four (certified by a nonzero finite-field reduction of its rational entries). This rejects the stronger inference, not the individual structural properties.

## C09. Two-Green sandwich: accepted identity with missing implementation guard

For invertible A,B,
A(F-A^-1-B^-1)B = AFB-A-B.
Multiplication by invertible endpoints preserves the equivalence of zero residual and Fourier equality. The public source checker does not establish invertibility. With identity permutations and unit weights, A=B=0, the polynomial residual vanishes for every F while both Green inverses are undefined. Its “full_equality_to_dft” flag therefore needs an explicit nonsingularity precondition. The main path's find_weighted_escape supplies valid denominators, so this guard defect does not invalidate those particular intended examples.

The four-term residual alone is O(N^2). The wrapper additionally calculates dense products and a rank, so that whole wrapper is O(N^3). Neither path applies a new fast Fourier transform.

## C10. Prefix/capacity, transverse-fiber and symmetry gates: retain restricted scope

A capacity or prefix-cut test is a necessary condition, not a factorization. S42 deliberately exhibits non-prefix bottlenecks and non-Fourier candidates despite passing coarse gates. The lifted compatibility matrices require full residual/rank identities, not merely enough edges.

For a polarized product YX preserving opposite coordinate fibers, fixing a transverse row/column block leaves only one intermediate state; the block is an outer product and has rank at most one. The corresponding s-by-s Fourier block has rank s. The source's s-term singular-path decomposition demonstrates that a sum of enough paths can recover Fourier; it does not show linear work for a complete transform. Mixed-axis stages do not preserve the single-path rank-one restriction. Parameter-count arithmetic and sample diagonal-gauge invariance are not sufficient proofs that a particular Fourier target is outside a nonlinear image.

For a resolvent G=(I-Q)^-1 and fixed shift J, [G,J]=G[Q,J]G. A change in k solver occurrences yields a rank-change bound charged to occurrences through telescoping. Reusing a single parameter in two factors may contribute rank two, as the source explicitly tests. Modular Gram polynomial identities and characteristic-zero norm/singular-value statements remain different evidence levels; no general complex spectral theorem is accepted merely from finite-field checks.

## C11. Growing-fiber profiles: no demonstrated arithmetic speedup

All six stored profile rows have new_arithmetic greater than baseline_arithmetic. For N=262144 the figures are 7516160 and 7340032, a ratio of 1.0239955357142858. The separate word proxy can favor a candidate without changing this arithmetic comparison. Neither metric is wall-clock performance, and neither is a general worst-case FFT speedup.

The source operation ledger is not a replay of random tests. Its computed test cardinalities do not certify that those tests pass. The largest-profile wrapper delegates its full-output check to own_algorithm, outside this assignment. Temporary-directory replay tests byte reproducibility only when actually executed; it is not a security sandbox.

## C12. Provenance, integrity and runners: no theorem elevation

Archive/library helpers, test runners and seal checkers receive full static source coverage because their entire exact contents were read and assessed. They do not receive mathematical theorem credit. Hash equality establishes byte identity; an archived PASS string establishes only that the string exists. Runner code is not a successful run. A read-only mode and hash manifest provide immutable-by-convention, tamper-evident snapshots when their digest is independently retained, not absolute filesystem immutability or authorship authentication.

No broad novelty, arbitrary-circuit lower bound, complete worst-case sub-NlogN FFT, end-to-end measured speedup or universally successful random setup is established by this review.
