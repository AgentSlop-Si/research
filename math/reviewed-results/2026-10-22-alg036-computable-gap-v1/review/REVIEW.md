# Independent review: computable nondivisible Gaussian gap

Date: 22 October 2026 UTC.

Verdict: **ACCEPT, for the computable positive compact-interval gap theorem only.**

Reviewed proof: `PROOF.md`, SHA-256 `1e500b954a851cc9243cd29a72292e5bbeb9ef1df06bfee0255e5f0f58b39988`.

## Accepted contract

For every input consisting of integers `1 <= d <= N` with `d` not dividing `N` and rational endpoints `0 < r0 <= r1 < infinity`, the specified algorithm terminates and returns a positive rational `gamma` such that

    Pr(||CN(0,P)-b||_infinity <= r)
      <= (1-exp(-N r^2/d))^d-gamma

for every orthogonal complex rank-`d` projector `P`, every `b in C^N`, and every `r in [r0,r1]`. The proper-complex normalization is `pi^(-d) exp(-||g||^2)` and the norm uses complex moduli.

Acceptance is conditional on the accepted centering, equality classification, and compactness dependencies specified in the assignment. The reviewer read their exact source, rather than replacing them with the already completed `N=3,d=2` optimizer:

- [Inherited report, exact commit dc3fdc](https://github.com/AgentSlop-Si/research/blob/dc3fdc543c9688dfed3afb5c58797d8655c3db9d/math/finalized/2026-10-19-cyclic-mixedprime-gaussian-extrema/gaussian/candidate/REPORT.md), especially Sections 4 and 5.
- [Current scope boundary, exact commit e6ff668](https://github.com/AgentSlop-Si/research/blob/e6ff6681109d94ffe21248f92a5a0823d6b71cf4/math/finalized/2026-10-20-alg036-gaussian/README.md).

## Mathematical audit

### 1. Translations and degenerate coordinates

The inherited centering result is applied before continuity or covering. This is essential: arbitrary-translation continuity can fail at a zero-leverage coordinate whose translation has modulus equal to the radius. No such continuity claim is used.

For variance `p>0`, the radial density is `2t exp(-t^2/p)/p <= 2/(e t)`. On the shell used in the proof, `t >= r0/2`, giving the stated `8h/r0` scalar bound. A zero-variance coordinate is identically zero and cannot meet this positive-radius shell. The union bound therefore remains uniform at zero leverage and under rank-degenerate coordinate marginals. It needs no coordinate independence.

The ambient coupling `PG,QG` has the correct law because projectors are Hermitian and idempotent. On `max_j |G_j| <= T`, the perturbation is at most `eta N T`; its complement has probability at most `N exp(-T^2) <= N 2^(-T)`. The resulting modulus and all radius restrictions are valid.

### 2. Rational covering

The frame enumeration is finite, and the two Hermitian definiteness conditions are exact rational tests. Each retained `W` has full column rank and produces the exact rational orthoprojector `Q = W(W*W)^(-1)W*` of rank `d`.

Rounding an isometry to the stated grid gives Frobenius error `e <= eta/4 <= 1/16`; hence the rounded matrix is retained. Its polar isometry `S` obeys `||S-W||_op <= e`, `||S-V||_op <= 2e`, and `||SS*-VV*||_op <= 4e <= eta`. Thus the enumeration genuinely covers every projector. The polar factor is not an unimplemented irrational operation in the algorithm. The coordinate isometry ensures the retained family is nonempty at every stage.

### 3. Gaussian normalization, tail, and integrand regularity

For `A=W*W`, the density `det(A) pi^(-d) exp(-y*Ay)` is the proper-complex law with covariance `A^(-1)`, not a real-Gaussian density with an extra factor of one half or a square-root determinant. Its pushforward by `W` has covariance `Q`.

The filter gives `||W||_op < 2` and `A^(-1) <= 4I`. Consequently the event function is 2-Lipschitz, the real-cube tail is bounded by `d exp(-B^2/4) <= d 2^(-m)`, and the global density gradient is bounded by `4^(d+1)`. All three constants are conservative but correct.

### 4. Classification, quadrature, and rounding

Every real cell has center distance at most `dh`, so `rho=2dh` is a valid event margin. The IN and OUT tests are exact rational squared-modulus comparisons. Every uncertain cell lies in the output shell with half-width `2rho`, whose probability is at most `32Ndh/r0`.

The selected mesh ensures `2rho <= r0/2` and allocates at most `epsilon/4` to each of: the cube tail, uncertain-cell probability, scalar interval widths summed over the cube, and the density-variation term summed over the cube. The volume factor is explicitly charged. For an uncertain cell, subtracting its true integral from its upper estimate leaves at most its interval width times cell volume; therefore the stated upper-minus-lower calculation does not omit a quadrature term. Clamping to `[0,1]` is safe.

The exponential series tail bound follows from omitted-term ratios at most one half. Reciprocation uses positive intervals, and Machin's identity with alternating arctangent remainders gives rational enclosures of pi. The exact determinant, quadratic form, interval products, powers, and stopping comparisons preserve outward enclosure. Every scalar subroutine terminates. No floating-point numerical oracle is used.

### 5. Soundness and all-input termination

Radius monotonicity permits comparison of `U(a_i)` with `F(P,b_i)` without pretending the same endpoint suffices for both. Net coverage and the centered modulus prove that every computed `gamma_k` is a sound lower bound for the gap, whether or not it is positive.

For termination, each retained center is itself an exact rank-`d` projector, so its true gap is at least the inherited positive compact-interval minimum `Delta`. The radius discretization costs at most `epsilon`, the two enclosures cost at most `2epsilon`, and the net modulus costs at most `2epsilon`. Hence `gamma_k >= Delta - 5epsilon`, as claimed. This guarantees a strictly positive rational return for every admissible input without supplying Delta to the algorithm. The singleton radius interval is handled explicitly.

This is an all-input proof, not evidence inferred from testing finitely many `(N,d)` values. No full numerical search, historical program, or supplied program was executed during this review.

## Cost caveat and correction resolved

The stated bounds count candidate frames and integration cells. Exact summation of independently denominated rational intervals may substantially grow accumulator denominators. The reviewed version explicitly excludes accumulator growth and full bit runtime from both the cell-count and gap-dependent expressions. Its polynomial-log accuracy overhead statement is limited to individual scalar and form evaluations at fixed numeric inputs. This resolves the only wording concern identified in the audit.

No efficient implementation, useful dimensional rate, useful endpoint rate, or input-only quantitative formula for Delta is accepted. The method is a deliberately crude effective-compactness construction.

## Disposition

The narrow computability gate may be recorded complete. General maximizing projectors, changing-dimension critical-window refinements, practical quantitative bounds, efficiency, information-model questions, historical novelty, and complete attribution remain unresolved. ALG-036 remains TO RESEARCH at priority 34. The completed `N=3,d=2` optimizer is neither reopened nor used as a substitute for this proof.

The reviewed README and SCOPE metadata accurately preserve those restrictions and their historical candidate-at-creation status. This review supersedes that pending review status only for the bound proof hash and the accepted contract above. Any mathematical change requires renewed review. No external write, repository publication, or native table edit was performed by the reviewer.
