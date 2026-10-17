# Compact Newton quotient: independent intake review

17 October 2026. Read-only source review plus separately authored exact-arithmetic controls.

## Decision

**Accept the integral normalized quotient, compatible integer encoding, coefficient-height bound, and local carry theorem at their stated scope.** The certified prime-budget comparison is independently reproducible. This is a representation improvement within the varying-evaluation Newton family. It does not establish a faster all-size FFT, a faster integer multiplier, or historical novelty.

The old factorial witness remains correct for literal monic exact-coordinate reconstruction. It must not be carried over as an obstruction to this changed quotient and encoding. Conversely, the compact coordinates do not discharge full channel mixing, auxiliary-prime setup, CRT, binary conversion, or any fixed-Mersenne-route obligation.

No uploaded program was run, imported, or compiled. The source programs were read as text. Newly written controls are in `independent_controls.py`; results are in `CONTROL_RESULTS.json`. The supplied large-product coefficient maxima, execution timings, and historical replay totals are not represented as fresh reruns.

## 1. Source integrity and deduplication

Source archive: `fft_compact_newton_progress_2026-10-17.zip`, 61,270 bytes, SHA-256 `cfa9456b4fcff00412675bc2d8f9a0fe7e7efb9589cf8ad4d390996205ebff93`.

All 26 entries in its manifest match the extracted bytes and hashes. Including the manifest itself, the archive contains 27 files. Safe extraction rejected absolute/traversal destinations and symbolic-link entries. The mathematical review focuses on:

- `transfer/COMPACT_BINOMIAL_CARRY_AND_COST.md`
- `compact_newton/compact_binomial.py`
- `compact_newton/modular_compiler.py`
- `compact_newton/monic_baseline.py`
- `compact_newton/compare_budgets.py`
- `transfer/local_carry.py`
- `compact_newton/budget_comparison.json`

Exact Git-blob comparison against 14,091 entries from ten fully returned repository subtrees found no byte-identical member. This is a bounded byte-deduplication result, not a full-history or semantic-originality result. The subtrees were archive, archives, current, finalized, intake, research-addenda, reproducibility, reviewed_rounds, reviews, and updates. `DEDUPLICATION.json` preserves member hashes and the explicit scope.

The existing family is identifiable, but no canonical catalogue/table owner was verified:

- [Precision-adaptive Newton channels](https://github.com/AgentSlop-Si/research/blob/e27b834ee8f1c5ba31b49118c45b34d4f212ac05/math/finalized/2026-10-15-experiment-reviews/precision_adaptive_channels/REPORT.md) already distinguishes coordinate reconstruction budgets from the full modular-transform invoice. Its one-block monic, coordinate-adaptive, and scalar-low-word interfaces are different from this new outer quotient.
- [Block-carried Newton tree](https://github.com/AgentSlop-Si/research/blob/e27b834ee8f1c5ba31b49118c45b34d4f212ac05/math/finalized/2026-10-15-experiment-reviews/block_carried_newton_tree/REPORT.md) already separates proper-block factorial expansion from the complete-period pure-shift exception. Its affine descriptor and data-product cost are not replaced by the present normalized-coordinate result.
- [Independent finalization of the Newton follow-ons](https://github.com/AgentSlop-Si/research/blob/e27b834ee8f1c5ba31b49118c45b34d4f212ac05/math/finalized/2026-10-15-experiment-reviews/newton_followon_independent_finalization/REPORT.md) explicitly keeps these ancillary lanes separate from the fixed Mersenne route. That separation remains intact.

ALG-006 and ALG-062 refer to different recognition problems and are not owner matches merely because their titles contain Newton. Disposition: retain as an unbound supplemental representation update pending an explicit owner mapping. No status, priority, score, route, or catalogue row is changed.

## 2. Integral quotient and height proof

Write `B_j(X)=X(X+1)...(X+j-1)/j!`, take `r>=2`, and set `D=lcm(1,...,2r)`. Retain `B_0,...,B_(r-1)` in the rational polynomial quotient with relation `B_r=D Z`.

The signed product coefficient at degree `i+j-k` is

`(-1)^k (i+j-k)!/[k!(i-k)!(j-k)!]`.

This is an integer trinomial coefficient with magnitude at most `3^(2r-2)`. This product rule is established binomial-basis algebra; the [Sage integer-valued-polynomial documentation](https://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/integer_valued_polynomials.html) gives the shifted basis and its product operation. Correctness of the present composition does not confer novelty on that ingredient.

For `0<=t<=r-2`, Vandermonde expansion gives the fold

`B_(r+t) -> Z sum_(a=0)^t f_(t,a) B_a`,

where

`f_(t,a)=D/binom(r+t,r) * binom(r+t-a-1,t-a)`.

For each prime ell, Legendre's factorial-valuation formula bounds the valuation of `binom(r+t,r)` by the number of nonzero base-ell positions up to `r+t`. Each floor-difference is zero or one, giving at most `floor(log_ell(r+t)) <= floor(log_ell(2r))`. Hence the denominator divides D. The fold is integral.

The stronger height estimate is essential: `f_(t,0)=Dr/(r+t)<=D`, and the successive ratio is `(t-a)/(r+t-a-1)<=1`. Thus every fold constant is positive and at most D. Closure of the integer `Z[Z]`-span follows from the product and fold rules. Associativity follows from the ambient rational quotient; it is not inferred merely from evaluating at one P.

For inputs of at most K outer blocks and digit magnitudes at most A and B, at most r² channel pairs contribute to one unrestricted degree and at most K outer pairs collide. At most r-1 high degrees fold into any retained coordinate. Therefore

`C_new = r² 3^(2r-2) K A B [1+(r-1)D]`

is a valid bound. With the canonical digit sizes below, `log C_new=O(r+log K)`. The `log K` term is genuine and must remain.

For the comparison, the sharpened monic bound

`C_old = 2 r² 3^(2r-2) K A B (r-1)!`

is also valid. In a low term, rescaling multiplies the normalized product constant by `i!j!/d! <= (r-1)!`. In a folded term, using the fold estimate with rational scale `1/r!` gives at most `3^(2r-2) i!j!/(r!a!)`; summing fewer than r high degrees stays below `3^(2r-2)(r-1)!`. The two outer-degree sources explain the final factor two.

The monic unit-digit product `E_(r-1)^2` retains coefficient `(-1)^(r-1)(r-1)!` in its unshifted `E_(r-1)` channel. That remains a literal exact-coordinate height witness. It is not a lower bound for early normalization, scalar decoding, adaptive reconstruction, or the present changed quotient.

## 3. Exact encoding and capacity

Let `L=lcm(1,...,r)`. For every prime power ell^e exactly dividing D, let m be the largest ell-power dividing L, including m=1 when ell>r. Then m<=r and L/m is an ell-adic unit. The CRT condition

`k0 = -(L/m)^(-1) mod ell^e`

has a unique solution modulo D. Take its representative `0<=k0<D`, set `k=k0+D`, and `P=1+kL`.

The adjacent weight ratios `R_j=1+kL/j` are positive integers. For each ell, the factor R_m is divisible by ell^e, so D divides `Q=product R_j=B_r(P)`. Thus `beta=Q/D` is an integer. Also `R_r>D`, since `R_r/D >= L/r+1/D >1`; consequently `beta>w_(r-1)`.

The source's elementary exponential lcm bounds suffice. The lower bound `L>=2^(r-1)` follows from `r*binom(r-1,j) | L` and the largest entry in that binomial row. With D<=k<2D and exponential upper bounds for D,L, all radices have O(r) bits, while

`beta > D^(r-1)L^r/r! >= L^r >= 2^(r(r-1))`.

Hence `log beta=Theta(r²)`. Every block in `[0,beta)` has a unique ordinary mixed-radix expansion restricted to that interval, with r O(r)-bit digits.

The top interval is genuinely truncated: D need not divide R_r. The r=2 check has D=12, P=39, R_2=20, beta=65. Replacing the top range by a fictitious integral radix is invalid. At the same P the old base is exactly `r!D beta`; the lost real-valued block capacity is `log2(r!D)=Theta(r log r)`. This loss is charged in the matched comparison.

This is a varying-evaluation family: P depends on r and has O(r) bits. No transfer to a fixed evaluation point, fixed modulus, or the fixed Mersenne route has been proved here.

## 4. Signed local carries and paid costs

For arbitrary signed coefficients and incoming carry, first normalize through the r ordinary radices. This gives `S=q_Q Q+u`, `0<=u<Q`. If d is the top digit, put `q0=floor(Dd/R_r)`. Since u differs from `d*w_(r-1)` by less than `w_(r-1)`,

`0 <= u-q0 beta < beta+w_(r-1) < 2 beta`.

Subtracting q0 times the prepared digit vector of beta is therefore safe. One comparison and at most one further subtraction produce the canonical remainder. The output carry is `Dq_Q+q0+e`, with e in {0,1}. Euclidean remainders cover negative intermediate coefficients without a sign exception.

The multi-block interface requires a nonnegative total and handles the product sign separately. A negative final carry is rejected rather than silently returning a finite negative canonical expansion. For coefficient bound U and incoming carry at most 4U+2 in magnitude, `sum w_j<2 beta` preserves the same carry bound. A positive tail then contracts by division by beta.

Static inspection agrees with the claimed at-most `3r+1` divisions and `2r+2` multiplications per block. The online normalizer uses radices, D, and the prepared beta digits; it does not assemble a weighted Theta(r²)-bit block. Its operand widths are O(r+log K), and its conditional bit bound is `O(K r M(r+log K))`, plus the final carry blocks, using appropriate division algorithms. Python operation counters do not themselves certify that bit-complexity model.

The modular compiler uses the signed Pascal transform at `0,-1,...,-(2r-2)`. Three evaluation/interpolation convolutions plus one reversed fold convolution are sufficient. Inspection confirms modular factorial/inverse-factorial construction, p>2r, valid inner padding, outer length at least `la+lb` to include the fold's extra outer degree, exact power-of-two root checks, and strict CRT modulus `>2*C_new`.

The complete conventional compiler still costs `O(r K(log K+log r))` field operations per CRT prime. A field multiplication is not one bit operation. Its 31-bit-capped trial-division prime search is a finite reference producer, not a fast all-size prime/root theorem. Setup, CRT, movement, and binary/non-power-of-two-base conversions remain paid. The normalizer's preparation also accesses large Q and beta. No complete sub-N-log-N recurrence is supplied.

In a bit invoice, the transform work is summed over the actual primes and charged at each prime's residue width. Input reduction and growing-width incremental CRT updates are data-dependent operations in addition to the transforms. Neither the prime count nor the CRT products can be discarded because the final coefficients have a short proved bound.

The storage scopes also differ. The carry-only plan holds r short radices and r short beta digits, using O(r²) bits. The current full representation plan retains every weight `B_j(P)` for j<r; their total size is Theta(r³) bits for this parameter family. The matched comparison disables optional dense reference multiplication tables, but still retains these growing weights for conversion. The carry-only storage statement must not be advertised as the entire prototype's storage bound.

## 5. Independently reproduced finite evidence

Fresh controls passed:

- 127 parameter constructions, all ranks 2 through 128
- 349,504 fold-integrality, positivity, monotonicity, and height checks
- 1,536 rational monomial-quotient comparisons, ranks 2 through 10 and four Z specializations
- 2,790 signed carry cases, with the optional second subtraction exercised 171 times
- 240 composed exact integer products, ranks 2,3,5,8; one, two, and four blocks; zero, maximal, and signed random inputs
- Negative controls detecting omission of the outer fold shift and the false integral-top-radix assumption
- Independent regeneration of the seeded input encodings, both certified bounds, and actual prime-product stopping counts for every matched record

| r | Input bits each | Monic primes | Normalized primes | Monic/new bound bits |
|---:|---:|---:|---:|---:|
| 8 | 610 | 6 | 6 | 103 / 112 |
| 16 | 2,959 | 12 | 13 | 234 / 243 |
| 32 | 12,553 | 25 | 24 | 499 / 478 |
| 64 | 51,040 | 53 | 48 | 1,051 / 949 |
| 128 | 206,716 | 110 | 94 | 2,222 / 1,881 |

Both encodings use three blocks per operand in these five particular cases. The rank-128 reduction is 16/110, about 14.55%, in certified modular passes. Neither bound is proved optimal, and rank 16 regresses. Rank 8 also has a larger normalized bound despite equal rounded pass count.

The source's reported rank-128 actual coefficient widths 1,803/1,638 and Python online timings about 5.90/4.86 seconds were not rerun. The baseline includes its own modular rescaling overhead, so these single-run reference timings are especially unsuitable as a general speed claim. This review independently certifies the budget arithmetic and bounded algebra/carry composition, not a production benchmark.

The matched baseline is the archive's reconstructed `monic_baseline.py`, using the shared conventional compiler. It is not a replay of every earlier saved Newton implementation, and it is not a comparison against an optimized production multiplication library.

The geometric-Newton, cyclic-dilogarithm, and Hensel appendices are separate research branches. This intake does not promote their historical controls to fresh validation or claim their unresolved full actions are solved by compact carrying.

## 6. Retained boundary and next gate

Keep the scoped representation/carry result and corrected scope of the old monic witness. Keep the result supplemental and unbound until its owner is verified. Do not merge its status with fixed Mersenne work, recognition-family Newton titles, or the older adaptive-precision and affine-block interfaces.

A meaningful successor must lower the complete arbitrary-input mixing/refinement cost or otherwise provide a fully paid alternative, preserving conversion, setup, prime/CRT widths, carries, and output. A smaller coefficient display, fewer primes in a matched finite test, or a short kernel recurrence alone does not satisfy that gate. Historical priority remains unverified.
