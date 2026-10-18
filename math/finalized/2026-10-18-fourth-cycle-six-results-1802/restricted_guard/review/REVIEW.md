# Independent final review: restricted Taylor-image product guards

18 October 2026 UTC. Candidate: `restricted_product_guards_20261018_1746`.

## Verdict

**ACCEPT the candidate's theorems, implementation, precision scope, and arithmetic/storage ledgers as stated. No mandatory correction remains.**

This acceptance binds to candidate manifest SHA-256:

`5eb8a2ca9cb85103d4da0833f63126b890820108823b07df673fae30a1f4f10b`.

The result establishes a sufficient exact-recovery precision improvement and an explicit linear-order sample-only guard lower bound on actual original-chunk Taylor products. It does not establish the exact restricted optimum, a new fast multiplier, an obstruction for arbitrary multiplication algorithms, or historical novelty.

These qualifications are essential and already present in the frozen report and README:

- The closed form `W_box=2m+v2((2L-2)!)+delta` assumes `m>=2`. It is exact for the displayed sufficient height-envelope criterion, not necessarily for the restricted-product information minimum.
- The asymptotic lower coefficient `0.8535762332103616...` assumes the explicitly constructed width threshold `m>=t`, where `t` is the bit length of the maximum absolute coefficient of the witness factor. It is not asserted uniformly for fixed small `m` as `L` grows.
- Samples must be honest `W`-precision evaluations of the original bounded chunks. Arbitrary lifts of already truncated `H`-bit Taylor arrays do not inherit the height promise. The standalone `H`-only input route adds two paid inverse shifts at `H`; the implemented integrated route starts with original chunks.
- The decoder is sample-only. The lower bound excludes operand readout, derivatives, evaluation at infinity, and extension/noninteger nodes. It is compatible with the fixed-precision ring-bilinear rank obstruction because the decoder changes precision and uses nonlinear bounded lifting.
- Time is measured in the inherited bounded-window arithmetic model. The stricter address supplement is not silently included in the little-o overhead claim. Backend workspace and the prescribed product schedule remain separately charged.

## 1. Binding and independent evidence

The candidate was copied after its author confirmed freeze. All 17 manifest payloads, three copied arithmetic dependencies, and two source reports passed verification. The mandatory prior review, `review_correlated_precision_20261018_1515/REVIEW.md`, was read in full and its distinction between unrestricted canonical factors and the actual chunk Taylor image has been preserved.

The candidate replay reproduced both its published result files byte-for-byte and digest:

`fad070a018994005873e0eb2f7f273c94fef243cbb41d124ddf4e77eb4f23c67`.

Fresh `independent_checks.py`, with separately implemented exact polynomial oracles, passed:

- 2,340 precision-envelope controls, through `L=1025` and `m=513`, including all even/odd and `m=2` versus `m>=3` boundaries.
- 432 arbitrary coefficient-box controls, including nontriangular boxes, even coefficient counts, zero trailing bounds, all-zero bounds, and surplus precision.
- 54 instrumented short-tail solves checking every multiplication and odd division, exact action counts, zero-tail precision, short update multipliers, and the factorial odd parts.
- 192 complete products with the pinned terminating backend, including independently checked forward Taylor shifts, phase-separated product call counts, sample capacity, exact convolution coefficients, direct/translated route agreement, final carries, and complete integer output.
- 195 freshly generated bounded-input witnesses, built by repeated polynomial multiplication rather than the candidate's binomial-sum formula. Checks include chunk bounds, degree, exact leading coefficient, signed and large integer nodes, exact valuation at both signs of 2 and 3, and four translation amounts.
- 27 improved-constant finite controls, with the maximum-coefficient inequality checked using exact integers.
- Eight full-residue-node information minima. These enumerate every node modulo the sample modulus, independently confirming the consecutive-node signature equivalence on the tested families.

Independent digest:

`160d9f465b3038d3a605a836d1232df2cdd6f1d2949ab42b10a655010fe46253`.

An additional five `lift_controls.py` cases verify recovery from canonical `H`-bit Taylor arrays by inverse shifting, and exhibit non-honest arbitrary lifts of the same arrays. Four include actual coefficient truncation at `H`; one covers wide chunks. No candidate source was edited. No external service was changed. Finite controls supplement the proofs and do not establish asymptotics by timing.

## 2. Height-envelope sufficiency and its exact closed form

For a degree-at-most-`d` polynomial with `0<=q_j<=M_j`, descending recovery is valid. After all higher coefficients have been removed, the leading `j`-th difference equals `j! q_j` modulo `2^W`. Writing `j!=2^v u`, with `u` odd, leaves `W-v` bits after removing the known power of two. Odd modular division determines `q_j` modulo `2^(W-v)`. The stated strict height inequality identifies its unique nonnegative lift.

Consequently the maximum of `v2(j!)+max(1,bit_length(M_j))` is a sufficient width. Zero bounds and degree zero are handled conservatively by the one-bit convention; the implementation's wider zero-bound cases were also checked.

For the triangular convolution box, the leading bound `(2^m-1)^2` has exactly `2m` bits when `m>=2`, giving the base width `2m+Gamma`. At index `j=d-k`, the product of the last `k` factorial factors supplies at least `ceil(log2(k+1))` powers of two, except possibly `k=2` with `d=2 mod 4`. The small cases and the inequality `v2(k!)>=ceil(log2(k+1))` for `k>=4` are correct.

The exceptional `k=2` index has multiplicity three precisely when `L>=4` is even. For `m=2`, its bound is 27, with five bits, and the base width suffices. For `m>=3`, the bound has exactly `2m+2` bits while the factorial valuation drops only one, forcing one additional bit in this criterion. Thus the report's delta condition is exact.

The precision saving against `H+Gamma`, with `H=2m+ceil(log2 L)`, is exactly `ceil(log2 L)-delta`. This is a constructive saving. The independently enumerated binary length-four family, for example, has minimum sample width four while its sufficient box width is five; there is no optimality claim to correct.

## 3. Two-scale decoder and complete arithmetic ledger

Put `b=W-Gamma>=1`. The inherited guarded interpolation returns every coefficient modulo `2^b` at input width `W=b+Gamma`. Subtracting the polynomial formed from those residues and dividing each canonical sample residue by `2^b` gives the high-part polynomial's samples modulo `2^Gamma`.

Its coefficients are `floor(q_j/2^b)`, bounded by `floor(M_j/2^b)`. For the triangular product box these bounds are below `L`. The original envelope inequality implies the stronger indexwise bound below `2^(Gamma-v2(j!))`, exactly what the short descending solve needs. At zero remaining precision, this bound forces the coefficient to zero, so skipping the division is correct. At `L=1`, the whole short tail has zero precision and is handled without table construction or division.

The short table recurrence is correct:

`F(j,k)=k(F(j-1,k)+F(j-1,k-1)) = k! S(j,k)`.

It builds every entry modulo `2^Gamma` by multiplication by the short index `k`. Removing recovered terms from the leading differences uses only multiplication by a high-part coefficient below `L`. There is no hidden wide-by-large-coefficient solve.

The ledger covers:

- Low-part interpolation and residual Horner evaluation: `O(L^2 W log(L+1))`.
- Short-table construction and triangular updates: `O(L^2 Gamma log(L+1))`.
- Short differences: `O(L^2 Gamma)`.
- Odd divisions: at most `O(L Gamma)` one-bit iterations with `O(L log(L+1))`-bit odd factorials, giving `O(L^2 Gamma log(L+1))`.
- Exact odd-factorial preparation: `O(L^2 log^2(L+1))`, absorbed because `Gamma=Theta(L)` away from the constant-size boundary.
- Bounds preparation by the sparse expression for `(2^m-1)^2` and declared short multipliers; all masks, source/output conversion, residual buffers, and coefficient assembly.

Since `W>=Gamma+1`, these are within the claimed `O(L^2 W log(L+1))` non-product cost. Wide arrays occupy `O(LW)` bits. The explicit short table requires `O(L^2 Gamma)=O(L^3)` bits, and the stored odd factorials require `O(L^2 log(L+1))`, absorbed by that term. Inherited shift preparation and temporary buffers also fit `O(LW+L^3)`; backend workspace remains additional. The report correctly does not replace this with `O(LW)` without an extra condition.

The address supplement is properly qualified. The odd-division bitstream performs `O(LW+L Gamma)` indexed iterations. Paying separately for addresses can add `O(LW log(LW+L^3))`, with table-loop indexing also charged. The report does not extend its little-o conclusion to that stronger model.

## 4. Lower witnesses on actual bounded chunks

For the stated `a,b`, write `R(U)=(U-1)^a(U+1)^b`, with coefficient maximum `C` and `t=bit_length(C)`. The condition `m>=t` ensures that all coefficients of the scaled positive and negative parts are strictly below `2^m`. The common monomial factor has coefficient `2^(m-1)`, also permitted.

The degree split is valid in both cases. If `A=3a+b<=L-1`, the monomial factor takes all of `A` and the other factor has degree at most `2(a+b)<=L-1`. Otherwise the monomial degree is `L-1`, and the other degree is `D-(L-1)<=L-1` by `D=5a+3b<=2L-2`.

Their difference is exactly

`2^(2m-1-t) X^(3a+b) (X^2-1)^a (X^2+1)^b`.

For even integers, the monomial contributes at least `3a+b` powers of two and the remaining factors are odd. For odd integers, the two even factors contribute at least `3a+b`; `v2(x^2+1)=1` for every odd integer. Values at both 2 and 3 attain this valuation exactly. The same parity argument applies to negative integers. Zero values cause no exception.

The leading coefficient is `2^(2m-1-t)`, nonzero modulo `2^H`. Thus the two required coefficient vectors differ, but all finite integer-point samples agree at width `2m-1-t+3a+b`. Any uniform sample-only recovery must use at least one more bit. Subtracting `H` gives precisely

`G >= max(0,3a+b-t-ceil(log2 L))`.

Translation is an integral invertible map with integral inverse, so it preserves both all-integer sample collisions and distinction modulo `2^H`. Arbitrarily many samples, adaptive integer-node selection, and nonlinear reconstruction cannot distinguish these pairs. This is genuinely a restricted original-chunk construction, not a reuse of the prior unrestricted canonical-`H` witness.

For `b=0` and `a=floor((2L-2)/5)`, both degree inequalities hold, and `t<=a+1` yields the stated `(4/5)L-O(log L)` bound under `m>=t`.

For the improved family, `a=5s`, `b=s`, `s=floor((L-1)/14)`, both degree inequalities hold and `s>=1` when `L>=15`. The unit-circle coefficient bound gives

`C <= (200 sqrt(5)/27)^s`.

It follows by maximizing `64 |sin(theta/2)|^5 |cos(theta/2)|`; squared sine `5/6` is the maximizer. The exact integer control `C^2 729^s <= 200000^s` confirms finite instances without floating-point reliance. Consequently

`G >= (16-log2(200 sqrt(5)/27))s -1-ceil(log2 L)`.

The leading coefficient after substituting the floor is exactly

`(16-log2(200 sqrt(5)/27))/14 = 0.8535762332103616...`.

The integer rounding costs only a constant, leaving the claimed logarithmic additive loss. The condition `m>=t=O(L)` is explicit; the accepted regime `m/(L log(L+1))->infinity` eventually satisfies it. The theorem does not claim this linear lower bound for every small-width family.

## 5. Sample-only information and inherited scope

Consecutive `d+1` sample residues determine all integer evaluations modulo the same modulus. The Newton-binomial identity expresses any integer-node value as an integer linear combination of the leading differences. Generalized binomial coefficients at negative integers are integral, so negative nodes do not need an extra argument about rational division.

The fresh full-residue-node enumerations confirm the candidate minima on their overlapping families. These are finite information minima, not efficient algorithms. Because every original convolution coefficient is below `2^H`, distinct exact coefficient vectors also distinguish the target vectors modulo `2^H`.

The prior mandatory scope correction remains intact: the old `Gamma` theorem was exact for arbitrary integer polynomials and sufficiently wide unrestricted canonical factors, not universally for actual chunk-image products. The new construction supplies a different, explicitly bounded-image lower bound and leaves a substantial gap below the constructive upper bound.

The fixed-precision ring-bilinear obstruction is also unchanged. This reconstruction uses precision-changing even division and bounded integer lifts, so the existence of `2L-1` guarded evaluation products does not contradict the `2L` fixed-ring-linear lower bound for `L>=3`.

## 6. Complete Taylor-route bill and remaining obstruction

The implemented route starts with original chunks, performs two forward shifts at `W`, evaluates at `-1,...,d-1`, and makes exactly `2L-1` sample products. The first negative node is handled correctly by signed modular Horner evaluation. Evaluating the translated factors at `r-1` gives the original factor values at `r`, so interpolating at original coordinates legitimately combines reconstruction and inverse translation. No independent inverse-shift bill is omitted from this final-coefficient interface.

For `L>=2`, nonnegative sample operands obey the stated bound

`h <= min(W,m+ceil(log2 L)+(L-1)ceil(log2(2L-2)))`.

Reduction modulo `2^W` cannot increase the nonnegative represented value. At `L=1`, the bound is `m`. The independent instrumentation verifies the capacity and separates sample products from every backend call made by the paid shifts.

All final exact coefficients, carry transitions, terminal tail, and complete binary output are covered by `O(L(m+log(L+1)))`. If the caller requests the raw Taylor-product coefficient object, the report correctly adds a length-`2L-1` forward shift at `H`. If only truncated Taylor operands are supplied, the separate two inverse shifts at `H` are also paid before resampling at `W`.

The complete integrated cost is therefore correctly stated as

`2 C_mod(L,W)+(2L-1)K(h)+O(L^2 W log(L+1)+L(m+log(L+1)))`.

Under the accepted very-wide hypothesis, `W=Theta(m)` and `h=m+O(L log(L+1))`, so its simplified ledger follows from the already accepted shift bound. The prescribed Karatsuba product charge remains of order `N^alpha/L^(alpha-1)`, rather than becoming a general sub-`N log N` algorithm. The prior full-expansion obstruction still applies under its own no-sharing and small-`L` schedule hypotheses. The logarithmic precision saving does not change that conclusion.
