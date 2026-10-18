# Independent focused proof and cost audit

Date: 2026-10-18 UTC.

## Verdict

**PASS for the exact retained outer-stage contract and explicitly fixed-family complexity scope.** No mathematical counterexample was found to formulas (1) or (2), the signed-width bound, complete retained-incidence coverage, or the exact `t<M` classification. The numerical coefficient certificate and centered interpolation/tail theorem remain inherited premises; this review does not upgrade them into a new recovery or original-signal provenance theorem.

The fixed-family qualifications must accompany the cost/storage statements. In particular, equation (5) is not a parameter-uniform storage assertion for arbitrarily varying `d` or `D`; see the explicit scope note below. This is already consistent with the distinction in manuscript sections 2 and 6, rather than a counterexample within its fixed-family scope.

This audit was read-only with respect to the candidate and dependencies. No candidate program or test was executed. The parent review owns fresh independent numerical checks.

## Material inspected and hashes

Candidate directory: `../candidate`.

- `MANUSCRIPT.md`: `ae04070f8c3184e4d917b53ed43a0228d81a41772cf68fb92ac341da18157b69`
- `full_transfer.py`: `40d90da471b62fc9ac268b78cbe9f080b149be3789253bb1dbbe43837d5c534a`
- `DEPENDENCY_COST_ERRATUM.md`: `1ed29c90ff1f231c70347c0083ee5165d72f3decfa77dd141ec7c0fc69c039d0`
- `outer_wrapper.py`: `d26c4cfe6d6c1430ce59b682f24bf69e2560fae81e8de60c63fc435b69b0637e`
- `sparse_output.py`: `92577edf07395237940aad94326a8d1e5c4a18b194a9162af84ada2d826edafa`
- `production_scalar.py`: `73b3bb0bebf41f7a810bf2470e9ae520bdc3e7593516850d8933dd307500091e`
- Accepted theorem `../candidate/dependencies/q16_scalar_completion_20261017_2129/sources/evidence/accepted/ALL_LENGTH_THEOREM.md`: `0a7733e2ac1d1c32cf70609ba0db151a13a73765107907aec44045daaf0a58f5`

The three source hashes stated in manuscript section 1 match the files read.

## 1. Incidence geometry and guard

For an integer lift `r`, retaining column `k` is equivalent to

`-h <= k-floor(rM/N) <= h+1`.

Equivalently, `k-h-1 <= rM/N < k+h+1`, which gives exactly

`ceil(N(k-h-1)/M) <= r < ceil(N(k+h+1)/M)`.

Replacing `r` by `r+qN` shifts `floor(rM/N)` by `qM`, so reducing the lift modulo `N` recovers the declared modular row stencil. When `t<M`, the underlying real interval has length `Nt/M<N`. Its integer points cannot include two values differing by `N`. This proves injectivity even when its integer-point count happens to equal `N`. A row has exactly `t` distinct retained column indices before intersection with the distinct support, so it has at most `t` contributions after that intersection.

For any real interval of length `L`, its half-open integer-point count is at most `ceil(L)`. Thus `E <= S ceil(Nt/M) <= St` is sound. This is a complete enumeration, not a relaxed candidate window requiring further filtering.

The strict integer guard is

`32Dm+4 < 2^m` iff `32Dm <= 2^m-5` iff `D <= floor((2^m-5)/(32m))`.

Here `m>=2`. Equality `t=M` is impossible: for `m>=5` the residues modulo 32 disagree, and for `m=2,3,4` already `D>=5` makes `t>M`. For fixed `D`, consecutive values of `(32Dm+4)/2^m` decrease strictly because `32D(m+1)+4 < 2(32Dm+4)`. They tend to zero. For `D=5`, `m=10` fails (`1604>1024`) and `m=11` passes (`1764<2048`); the first passing block is exactly `257<=N<=512`.

The `N=256` dense witness is exact on paper: `h=801`, endpoints are `-200` and `201`, giving 401 consecutive lifts and only 256 row residues. The manuscript correctly excludes this branch from the executable transfer. The `q>=4` implication and nonnegative final-rounding shift also follow from the displayed guard and `b<=3m`.

## 2. Every-prefix signed allocation and arithmetic

The cap implies `|a|,|b| < 3*2^(P+2m) < 2^w` for `w=P+2m+2`. The inherited complex certificate and `|C|<3` give `|Ctilde|<4`, hence each coefficient numerator has magnitude below `2^(p+2)`.

Each Cartesian exact complex-product sum contains two products, so its magnitude is strictly below `2^(p+w+3)`. Any prefix has at most `t` terms. Therefore its magnitude is strictly below `2^(p+w+3+ceil(log2(t))) = 2^(W_acc-1)`. Since the value is an integer, this fits the ordinary signed range, including its asymmetric positive endpoint. The source's check `abs(accumulator)<2^(W_acc-1)` is slightly stricter than allowing the most negative representable integer, but the proved strict bound means no valid input is lost.

`full_transfer.py` lines 155-165 compute all four integer products and both sums exactly, update both accumulators, then check the prefix and term-count bounds. Its rounding uses mathematical floor and nonnegative remainder, so the nearest-even rule is valid for negative numbers as well as positive ones. Each Cartesian error is at most half a grid unit, and the complex error is at most `sqrt(2)/2 * 2^-b <= 2^-b`. The scale-back branches preserve the represented dyadic value exactly.

## 3. Formula (1)

Let `Q` denote the exact sum using generated coefficients. For every row,

`|Q_l-(CZ)_l| <= sum_{k in I_l}|Ctilde_lk-C_lk| |Z_k| <= eta sum_{k in I_l}|Z_k|`.

The only rounding follows the full sum and contributes at most `2^-b`. Exact positive real scaling by `2^sigma` gives (1), including negative `sigma`. No recovery event is used. The Cartesian estimate cap gives the claimed strict uniform envelope `3 sqrt(2) t M^2`. The l1 numerator expression used for tests is a valid upper bound on the complex estimate norm and does not alter the coefficient certificate's complex interpretation.

## 4. Formula (2)

Write `A=D_phase B_full`, with exact retained matrix `C`. The normalized error decomposes into

- final rounding;
- `(Ctilde-C)Z` on active support;
- `C(Z-z)` on the complete retained row;
- `(C-A)z`.

The simultaneous premise gives `||Z-z||_infinity <= E_M R`. Centering preserves norm and the unitary transform gives `||z||_2=R`, hence `||Z||_infinity <= (1+E_M)R`. The four displayed terms are then bounded by `2^-b`, `t eta(1+E_M)R`, `3t E_M R`, and `12*4^-s R`. Finally `R>1/2` makes `2^-b <= 2^(1-b)R`. This proves (2).

No hypothesis `E_M<=1` is needed for this unsimplified bound. Other sparse-front-end guards failing at the finite fixture size therefore do not invalidate the stated conditional algebra. They do prevent reading the fixture as a successful full sparse-recovery experiment, as the manuscript says. The tail is correctly applied to exact `z`, rather than an uncontrolled failed-tape `Z`.

## 5. Source completeness and retained state

The sequential ordinal check, the accepted incidence validator's endpoint/prefix relation, identity binding of the returned coefficient, matching `p`, and terminal equality with the sum of all endpoint lengths jointly enforce a complete stream in the stated trusted local model. The implementation does not accept an external coefficient list or callback. Every supported zero is still processed. The terminal suffix check occurs before any completed output is returned.

Frozen data and owner identities are ordinary trusted-program invariants, not hostile Python-runtime security. No stronger security property was used in this audit. The live production path retains only a bounded number of incidence/coefficient records, the `N` arrays/output, the support/endpoints, the original producer context, and scalar state. It does not accumulate an `E`-record list.

## 6. Costs, storage, and necessary scope

The producer/replay bounds reproduce the mandatory erratum: their event count includes `R_rows`, sorting, parsing, and output comparison; actual widths must include addresses, old counter encodings, and cumulative event growth. Retained original rows contribute `O((S R_rows+S+R_rows+1)H)` bits and cannot be reduced to `O(Sm)`.

For fixed `D,beta,d`, fixed parameter encodings, `O(m)` original-data widths, and `O(m)` prior counter widths, accumulator/output/outer-control widths are `O(m)`. The scalar code uses `O_D(m)` events per evaluation with `O_D(m^2)` maximum integer width: factorials and exact powered endpoints are included. Schoolbook simulation therefore gives the conservative `O_D(m^5)` work and `O_D(m^3)` cumulative-bit bounds. Its number of simultaneously live large integer temporaries is bounded. The stated additional work (3) and peak storage (5) follow under these qualifications, in addition to the separately retained producer/replay receipts.

The dense output pass has a bounded number of growing-word operations per row. Although the Python helper spells rounding as `divmod(value,1<<shift)`, its divisor is a power of two, so the mathematical word-model implementation can use shifts and a remainder mask; an arbitrary unit-cost division assumption is unnecessary. The scalar work can conservatively be simulated by one or more word steps per bit step, establishing (4). Under the external support and row-count premises, the positive exponent gap `1/2-beta` absorbs every fixed power of `m`; the separate `N` output pass remains linear word work. This does not imply linear bit work or useful crossover constants.

**Scope note:** Equations (3)-(5) must not be advertised as parameter-uniform bounds for the full callable interface. For example, with `D` fixed but a varying arbitrarily large positive `sigma<=dm`, every nonzero rounded output can gain `sigma-b` numerator bits. Consequently the general output storage is not uniformly `O(Nm)`. A fully general width-aware version must use actual output/accumulator width in the `N` term (a conservative `NH` term if `H` is enlarged to cover all reached outer fields), and must retain actual scalar widths if `D` varies. The current manuscript explicitly fixes `D,beta,d` for the family claim and pays actual reached widths at the callable boundary; this audit accepts that scope only. Making “for the same fixed family” explicit immediately before (5) would remove a possible standalone misreading.

## Boundary of acceptance

This audit accepts a complete retained outer transfer conditional on the inherited coefficient certificate and exact matrix target. It does not establish original-source binding, full recovery/probability, independent amplification, a dense/all-length executable, practical speed, or novelty. The typed dense requirement correctly marks the missing input/interface dependency; it is not a returned transform or an all-length dispatcher.
