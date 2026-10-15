# Valuation-adaptive Newton scalar producer

15 October 2026. Fresh construction, exact reference implementation and child-width audit. This is a distinct continuation of the recovered arithmetic-progression Newton route. It is not an imported multiplication engine.

## Result

**A genuine valuation-aware exact-low producer is obtained; no faster full multiplier is admitted.** Two actual improvements over the previous odd-start/even-step sampled construction are proved and implemented:

1. If `v2(p) >= v2(g)`, including every odd step `g`, scalar interpolation has integral 2-adic weights. It needs no coefficient-recovery precision guard. Its individual point products have precisely specified, possibly different, required precisions.
2. When the actual Newton positional weights acquire enough powers of two, high Newton channels and high outer block pairs really can be omitted. This is executed in the tests, rather than inferred from a formal degree cut.

Neither improvement supplies the missing cost saving. For the near-Mersenne start and odd step, a legal growing family retains every full sampled product even under the improved scalar precision rule. For the high-valuation progression `p=g=2^s`, actual channel pruning occurs, but the surviving evaluated operands grow to the input scale. A native full-product-wrapper recursion is not shrinking. The general adaptive-node formula below also explicitly accounts for negative weight valuations, nonunit denominators, repeated-node exclusions and outer specialization.

The report does not prove all adaptive Newton or shared-circuit methods impossible. It specifies one exact producer and identifies why its independent sampled-child recurrence fails. In particular, it does not call a dyadic filtration or binary-like grouping an asymptotic saving.

## 1. Canonical representation and all-length interface

Let `b_0,...,b_(r-1)` be integer radices at least two. Define

    E_0=1, E_j=product_(u<j) b_u, Q=E_r.

Every integer `0 <= X < Q` has one canonical expansion `X=sum_(j<r) a_j E_j`, with `0 <= a_j < b_j`. The implemented conversion obtains the digits by actual successive Euclidean divisions. It is charged; the digits are not assumed supplied. A periodic representation uses these radices repeatedly, so

    X=sum_(ell<L_A) Q^ell X_ell, 0 <= X_ell < Q.

For one-block interpolation extend the radix sequence to `d=2r-1` **distinct** positive radices, and set

    e_j(x)=product_(u<j)(x+b_u), A(x)=sum_(j<r) a_j e_j(x).

Then `A(0)=X`; this is just a shifted coordinate for the original source. In its arithmetic progression `b_j=p+gj`, the node `x=-b_t` here is the original node `-gt`, and `e_j(0)` here is the original `e_j(p)`.

The ordinary output contract is the exact low word

    R=XY mod 2^k, 0 <= R < 2^k,

plus a certified short-prefix high interval and its paid modulo-3 repair. Section 7 gives all binary lengths and the closed native wrapper recurrence. Canonical periodic output digits, when wanted, are obtained by actual Euclidean division of the reconstructed product; those additional divisions are charged and tested.

Distinctness is needed by this particular interpolation procedure. Repeated adaptive nodes need confluent interpolation/derivatives with their own costs. They are not silently accepted here. Periodic outer blocks are handled by Section 5; their repeated radices are not incorrectly fed into a distinct-node Vandermonde inverse.

## 2. Real Newton-tail pruning

The monic integral polynomials `e_j` form a triangular integral basis. Therefore the genuine product has integral coefficients

    A(x)B(x)=sum_(j<d) D_j e_j(x), D_j in Z.

Put `nu_j=v2(E_j)`. This is nondecreasing. Let `J` be the smaller of `d` and the first positive `j` for which `nu_j >= k`; if no such earlier index exists, take `J=d`.

Every omitted term `D_j E_j`, `j>=J`, vanishes modulo `2^k`. At the first `J` nodes, every `e_j(-b_t)` with `j>t` is zero. Consequently interpolation from the first `J` genuine product samples returns the same first `J` Newton coefficients as the unrestricted product. Thus it gives the correct scalar low word after the omitted tail vanishes.

This proves actual truncation, including for non-arithmetic adaptive radices. It does not assert that arbitrary high-degree terms vanish, or that high mixed-radix positions automatically have binary significance. The sufficient criterion is their actual valuation.

## 3. Exact scalar interpolation, including nonunits

For `0 <= t < J`, the scalar Lagrange weight is

    L_t = product_(u<J,u!=t) b_u / product_(u<J,u!=t)(b_u-b_t).

Write `lambda_t=v2(L_t)`, permitting negative values. Let

    h=max(0,-min_t lambda_t), q_t=k-lambda_t.

A term with `q_t<=0` can be skipped. For every other term:

1. Obtain the genuine signed sample product `f_t=A(-b_t)B(-b_t)` modulo `2^q_t`.
2. Separate `L_t=2^lambda_t n_t/d_t`, with odd integers `n_t,d_t` and `d_t>0`.
3. Compute the odd inverse `d_t^(-1) mod 2^q_t`, multiply by `n_t` and the sample residue modulo `2^q_t`.
4. Shift the result by `lambda_t+h`, and accumulate modulo `2^(k+h)`.
5. The accumulated representative is divisible by `2^h`; divide by that exact power of two to obtain the canonical `k`-bit low word.

Indeed the lifted sum is `2^h` times the scalar interpolant modulo `2^(k+h)`. Its exact scalar value differs from `XY` by a multiple of `2^k`, by Section 2. No inverse of an even integer is used. The guard is a sufficient termwise one, not a proof of optimality among all correlated decoders.

The reference explicitly evaluates signed samples, uses only their needed magnitude residues for the product, records both operand widths and the resulting full-product wrapper capacity, and charges odd inverses and constant modular multiplications separately. A low product is not treated as a free oracle: it is implemented using an ordinary full scalar product followed by reduction.

### Integral scalar weights for odd step, or a shared power of two

Suppose `p=2^a p0`, `g=2^a g0`, with `g0` odd and integral `p0`; equivalently, `a=v2(g)` and `v2(p)>=a`. The powers `2^a` cancel from `L_t`, giving

    L_t=(-1)^t product_(u<J,u!=t)(p0+g0 u)
                    / [g0^(J-1) t! (J-1-t)!].

Every such weight belongs to `Z_2`. One elementary proof starts with the polynomial

    ell_t(z)=binom(z,t) binom(J-1-z,J-1-t).

It equals the Lagrange cardinal polynomial at nodes `0,...,J-1`, takes integer values at every nonnegative integer, and extends continuously to the 2-adic integers. Nonnegative integers are dense there. Hence `ell_t(-p0/g0)` is 2-adically integral. This value is exactly `L_t`.

The equivalent finite-difference identity is

    C(p)=sum_j Delta^j f(0) binom(-p/g,j),

interpreting `p/g=p0/g0` in `Z_2`. This explains precisely why coefficient recovery can require guards while scalar recovery does not: multiplying the recovered coefficients by their positional weights cancels the bad denominators before the low word is produced. The source's field factorial-convolution compiler is still not licensed to invert even factorials modulo `2^k`.

This finite binomial interpolation is classical structure, not a novelty claim. Mahler's original interpolation work is available through the [publisher's primary-source reprint and abstract](https://ems.press/books/dms/252/4989). Only the elementary finite-polynomial assertion proved above is needed here. The large PDF could not be fully fetched in this pass; no uninspected differentiability theorem is used.

### An explicit guard control

With radices `(3,7,11)`, legal input digits `(0,1)` represent `X=3`. The three samples are `(0,-4,-8)`. All sample squares vanish modulo 16, but `X^2=9` is odd. The three scalar weight valuations are `(-5,-4,-5)`, so the generic termwise method obtains sample precisions `(6,5,6)` for a one-bit output. It returns that bit correctly. Thus arbitrary adaptive choices do not inherit the odd-step no-guard theorem merely because some positional valuations increase.

## 4. What the two constructive choices actually buy

### 4.1 Near-Mersenne start, odd step: guards disappear, long low work remains

Take powers of two `r>=4`, and

    m=r(log2 r)^2, p=2^m-1, g=1,
    A=B=(p-2)+e_(r-1) in the original source coordinate.

These are legal canonical digits. The input is `(p-2)+E_(r-1)` and has `(r-1)m+O(1)` bits. The full block capacity is `N=ceil(log2 Q)=rm+O(1)`.

For `2<=j<=2r-1`,

    v2(E_j)=m+v2((j-2)!).

These valuations are far below `N`. At every cut `k>=N`, the producer retains all `d=2r-1` channels. Scalar Lagrange weights have valuation zero at `t=1`, and at most `m+O(log r)` at every other node. This follows directly by removing the single factor `p+1=2^m` from the product formula and using factorial valuations; one convenient bound uses `v2 binom(d-1,t)<=floor(log2(d-1))`.

Each sample is

    A(-t)=p-2+(-1)^(r-1)(r-1)! binom(t,r-1).

It is odd, and has exactly `m` magnitude bits in the tested and eventual family: the factorial-sized correction is `2^O(r log r)`, much smaller than `2^m`. The required precision `q_t=k-lambda_t` exceeds `2m`. Thus every retained sample request is its full exact product. No power of two can be stripped from either input, and no ordinary sample product is shortened by the improved precision rule.

The full-product-wrapper subinvoice is `d` calls of capacity `2m`. Against even the favorable ordinary-parent wrapper capacity `2N`, its beta-potential tends to

    2 * (1/2)^beta = 2^(1-beta).

At the pinned `beta0=0.998327339802923082`, this is `1.0011600720632914>1`, before conversion, sampling, scalar projection, high-prefix multiplication or checksum work. This is the same favorable diagnostic used by the prior lane; it does not assume a matching native recurrence that has not been supplied. The actual canonical native closure in Section 7 is more expensive: against native parent width `N`, this point-product subinvoice tends to `4*2^(-beta)=2^(2-beta)`, before its separate prefix child. Multiplying `m` by any fixed positive constant leaves these limits unchanged; the all-length dispatcher below has the same `log(m)/log(N) -> 1/2` shape.

Fresh `r=4,8,16,32,64` ledgers give optimistic ratios approximately `1.22755,1.32006,1.34181,1.34032,1.32998`. They are finite operation-width diagnostics, not runtimes. Their nonmonotonic approach is harmless; the asymptotic expression, not extrapolation from these rows, establishes the failed strict gate for this schedule.

### 4.2 High valuation: genuine tail omission, expensive surviving samples

Choose

    p=g=2^s, b_j=2^s(j+1), E_j=2^(sj) j!.

Here the criterion `sj+v2(j!)>=k` is genuine and useful for correctness. At `s=4r^2`, `k=N=ceil(log2 Q)` or `N+1`, the first vanishing index is `J=r+1`; the unrestricted compiler would use `2r-1` samples. Thus `r-2` high channels truly disappear.

The scalar weights simplify to

    L_t=(-1)^t binom(J,t+1),

and so have valuations only `O(log J)`. For the valid input with every digit `a_j=b_j-1`, one has `X=Q-1`. For `t<r`, the sample has leading magnitude

    2^((t+1)s) (t+1)!,

with relative error `O(2^-s)`; its low constant term is odd. Thus surviving operand widths increase with `t` instead of staying near one digit's width. In particular, the retained node `t=r/2` has width roughly `(r/2+1)s`, which is less than its required sample precision but greater than `N/2` when `s=4r^2`. Its ordinary-product wrapper has capacity greater than the native parent `N`. This already prevents a shrinking native recursion using these independent full-product wrappers.

The reference logs **actual widths after reducing the magnitudes to the permitted sample precision**, not merely the minimum of two capacity upper bounds. At the `k=N` cut, the sums of those native child widths divided by `N` are approximately `6.973,10.984,18.991,34.995` for `r=4,8,16,32`, respectively. Each row has a child at least as wide as its native parent. The `N+1` cut and the complete high-prefix interface cut `k=2N-floor(N/4)` are also tested; the problem remains. The latter keeps more samples and pays more width.

The high valuation is therefore real, but its dyadic contribution is not free compression. Scaling `x=2^s y` rewrites the input coefficients as `2^(sj)a_j`; the bit volume reappears in evaluations. No binary-grouping saving is claimed.

### 4.3 Adaptive, non-arithmetic valuation order

For arbitrary distinct radices with strictly increasing valuations `s_t=v2(b_t)`, their odd parts may vary independently. Since `v2(b_u-b_t)=min(s_u,s_t)`,

    lambda_t=sum_(u>t)(s_u-s_t).

All scalar weights are integral and early samples can have large vanishing weights. The last weight is always a unit. This is an exact adaptive formula, tested with non-power-of-two odd parts. It shows why accumulated positional valuation alone does not imply every sample becomes cheap: it must be compared with the denominator and with the width of the surviving unit-weight sample. It is not a universal impossibility statement for every adaptive choice.

## 5. Periodic outer reduction is explicitly paid

For actual outer blocks, the exact identity is

    XY=sum_(ell,m) Q^(ell+m) X_ell Y_m.

Put `v=v2(Q)`. A pair with `(ell+m)v>=k` vanishes modulo `2^k`. Every other pair is sent to the local scalar producer at precision

    k_(ell,m)=k-(ell+m)v.

Its result is multiplied by the actual scalar `Q^(ell+m)` modulo `2^k`, and accumulated. Powers, modular products, additions, moves and all retained pair producers are charged. The reference performs these operations and actually skips vanishing pairs. This is a complete, deliberately straightforward outer compiler, not a claim that its quadratic pair grid is cheap.

There is no omitted frequency-boundary operation: the method specializes the exact scalar identity globally, where the source boundary relation `e_r(p)=Q` is already true. It does not construct quotient coordinates and then omit their boundary. Conversely, the source four-convolution field schedule cannot be substituted here without separately proving a compatible bit-valid modular implementation.

## 6. High interval and canonical final output

For `0<=X,Y<2^N`, choose `1<=a<=N-1`, set `t=a+1` and `k=2N-a`, and obtain a separately paid prefix product

    V=floor(X/2^(N-t)) * floor(Y/2^(N-t)),
    H=floor(V/2^(2t-a)).

The established tail bound gives

    H <= floor(XY/2^k) <= H+1.

After the exact `R` is supplied by Sections 2–5, scan the original binary inputs modulo 3, multiply those two fixed-size residues, and determine `delta in {0,1}` from

    R + 2^k(H+delta) == XY (mod 3).

The ordinary product is exactly `R+2^k(H+delta)`. The prefix consumes an actual `G(t)` child, or a full-product wrapper `F(2t)`, with padding and movement paid. The checksum is not obtained from an unpaid carry payload. Canonical mixed-radix output, if requested, is then obtained by additional charged Euclidean divisions. The reference checks all its resulting digit bounds and reconstructs the same full product.

## 7. Full invoice and a closed, unfavorable all-length recurrence

Let `F(n)` return the canonical residue of a product modulo `2^n+1`. A signed full ordinary product with magnitude operand widths `u,v` can be obtained using `F(u+v)` on magnitudes: the ordinary product is strictly below that modulus. Signs and reduction are explicit linear work. A precision-`q` sample request uses actual magnitude residues with widths `u,v<=q`; it is not one unexplained `F(q)` call.

A conservative fully elementary invoice for a one-block low producer is

    L(N,k) <= C_in(N;r,b) + P(b,J,k)
              + E(a,b,J) + sum_retained_t F(u_t+v_t)
              + O(sum_retained_t q_t^2 + J(k+h) + N).

Here every named term has an implementable elementary bound:

- With `B=max bitlength(b_j)`, successive binary long divisions give `C_in=O(r N B)` for two inputs, and the same form for optional canonical output conversion at its output length.
- Let `D=max(1,bitlength(|b_i-b_t|))` over retained nodes and input indices, and `W=B+(r-1)D+ceil(log2 r)+2`. Exact triangular Horner sampling costs `E=O(J r W D)`, including signed adds and data movement. For arithmetic progressions `D=O(log(gr))`; for scaled high-valuation progressions it contains `s`.
- Weight products, exact fraction reduction, odd-unit modular preparation and inverses can all be performed with schoolbook integer algorithms in the coarse bound `P=O(J(JB+k+h)^2)`. This includes preparation and cannot be dropped because weights are input independent. The reference explicitly records preparation factor counts and all inverse precisions; its use of Python exact arithmetic is a mathematical reference for these paid operations, not a constant-time machine model.
- Constant multiplication and assembly are bounded by the displayed quadratic precision sum and linear movement. Faster structured preparation or projection would need a supplied algorithm; it is not assumed.

The periodic outer invoice is the sum of these local invoices over retained pairs at their actual `k_(ell,m)`, plus the initial periodic conversion, modular powers/scalings and accumulation. A direct implementation of those last constant operations has an elementary `O((L_A+L_B+L_A L_B)k^2)` bound. Reusing prepared weights within the call is permitted but does not eliminate their first preparation.

For an all-length canonical native implementation, handle an input equal to `2^n` as the residue `-1` in linear work. Otherwise both canonical inputs have at most `n` bits. Choose, for example,

    r=max(2,floor(sqrt(n)/(8 max(1,ceil(log2(n+1)))))),
    m=ceil(n/r)+1, p=2^m-1, g=1,
    a=max(1,floor(n/4)), t=a+1, k=2n-a.

One block has `Q>2^n`, so conversion is always defined. Compute the full product by the low/high construction, then reduce it canonically modulo `2^n+1` by splitting at `n` and subtracting the high half. Treat small lengths, or any shape whose conservative child capacities are not strictly below `n`, by elementary schoolbook multiplication and reduction. For sufficiently large `n`, the displayed arithmetic-progression sample bound is `W=O(sqrt(n) log n)<n/2`, and `2t<n`, so the branch terminates recursively at smaller arguments. This yields a genuine closed recurrence for every length:

    F(n) <= sum_t F(u_t+v_t) + F(2t)
            + the complete low-producer overhead above + O(n),

with the schoolbook branch at nonshrinking shapes. Unbalanced widths can be padded to the exact `u_t+v_t` native capacity; all copies and signs are included. Zero sample products are skipped. The code checks the algebra on every binary length from 2 through 129, while the elementary small-length branch covers lengths zero and one.

This is an exact but unfavorable recurrence. Its stated coarse overhead is already far too large for the target; independently, the concrete odd-step child family fails even the more favorable wrapper comparison in Section 4. The high-valuation progression cannot replace it as a shrinking branch under these full-product wrappers, and falls back to elementary multiplication if inserted into this all-length dispatcher. Neither fact is hidden under a low-product oracle or a free conversion claim.

## 8. Relationship to prior barriers and established work

- The previous odd-start/even-step parity barrier is genuinely escaped: some `E_j` are now even. It must not be applied unchanged to this lane.
- The previous coefficient guard is genuinely reduced for the scalar target when `v2(p)>=v2(g)`. It was a sufficient coefficientwise recovery rule, not a claimed minimal scalar rule.
- The factorial coordinate-size witness is bypassed by direct scalar projection. No `D_j` vector is materialized here. The surviving samples and scalar constants are still paid.
- The source field factorial convolution still has nonunit-denominator issues over powers of two; the present odd-unit recipe replaces, rather than informally reuses, that compiler.
- Global scalar specialization correctly accounts for the periodic boundary. It does not justify quotienting out a whole carry image at generic frequencies.
- A bounded high quotient still requires a paid low word and paid prefix product. The tiny checksum only removes the final one-bit ambiguity.
- The failure is for independent sampled products with the specified wrappers and elementary surrounding compiler. A proved shared-DAG scalar producer, correlated truncation, or a different native low-product recursion could change that invoice; naming it is not a completed construction.

The recovered primary source is `latest_multibase_material_audit/source_multibase_report_1640.md`, tied to the [16:40 continuation](https://chatgpt.com/c/6ad0f357-890c-83ed-9f2f-60373c069365?messageId=38cb35aa-daf1-44a0-b471-b6e370246d1c). The existing attribution audit in `newton_producer_prior_art/REPORT.md` establishes the classical Newton/factorial-convolution background. General p-ordering theory is related to adaptive integrality, but no theorem from an uninspected source is required or used here.

## 9. Fresh checks and limits

Run `python valuation_adaptive_newton/check_valuation_adaptive.py` from any directory. It imports no supplied implementation and uses only the Python standard library. The full output reports:

- 5,220 exhaustive small exact low products;
- 864 progression low products, including odd steps, shared valuations and incompatible valuations;
- 420 arbitrary distinct adaptive-radix low products;
- 540 complete periodic low/high/checksum products, with canonical output conversion;
- 19 outer block pairs actually skipped;
- 37,696 integral odd-step scalar weights;
- 1,155 increasing-valuation adaptive scalar weights;
- 512 arbitrary-binary-length full reconstruction controls;
- 483 progression/adaptive cases needing negative-weight guards;
- 315 progression/adaptive cases with actual Newton-tail pruning;
- the explicit sample alias, five odd-step adverse-family ledgers and twelve scaled-family precision/width ledgers.

All pass in the final run. These are exact finite controls and operation/width accounting, not proof-assistant certification, a wall-time benchmark, a historical-priority claim, or a universal lower bound. The scope-complete conclusion is an exact valuation-adaptive producer and a failed cost gate for its supplied sampled implementation. Broader original-route work remains open.
