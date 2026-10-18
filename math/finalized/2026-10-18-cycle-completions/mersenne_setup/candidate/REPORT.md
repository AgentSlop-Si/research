# A strictly sub-N-log-N setup bound for the Mersenne converter

18 October 2026. Local mathematical continuation of the accepted conversion interface. No historical program was executed, no external state was changed, and no growing-prime assumption is made.

## Result

The previously explicit `O(N log(L+1))` **odd-factorial prefix/reverse setup** can be replaced by

`O(N (log(L+1))^(log_2(3)-1))`.

Here `N=Lm`, `m=Omega(L)`, and the logarithmic exponent is about `0.584963`. The construction is unconditional, uses a separate explicit Karatsuba routine only on `O(log L)`-bit operands for this setup, and includes every resulting recursive call, carry, input/output scan, and table entry. It is an elementary blocked-multiplication improvement, not a claimed new multiplication principle.

Consequently the complete existing shift/conversion interface now has the paid bound

`O(M(CN) + L M(Cm) + N (log(L+1))^(log_2(3)-1))`,

where the same-scale convolution and the full-width diagonal products still use the explicitly paid backend `M`. With `L=Theta(sqrt N)`, the revised independent setup term is `o(N log N)`. More generally its ratio to `N log N` tends to zero uniformly for `1<=L<=N`, with the constant-size cases treated directly.

This closes the **setup-scale obstruction** identified as item 2 in section 5 of the accepted conversion report: that particular independent term no longer forces the N-log-N scale. It does not close the convolution/diagonal gate, the matrix-transform gate, or the requested complete sub-N-log-N multiplication target. It does not improve the fully Karatsuba-instantiated overall `O(N^(log_2 3))` bound; that bound remains dominated by the same-scale packed product.

## 1. Exact local streaming lemma

Let `W>=1`, `U>=2`, `0<=x<2^W`, and `0<=k<U`. Put

`t = 8 ceil(max(1,ceil(log_2 U))/8)`,

`R=2^t`, `q=ceil(W/t)`.

Thus `k<R`, `t=Theta(log(U+1))`, and byte rounding adds at most seven bits. Write the zero-padded input as

`x=sum_(j=0)^(q-1) a_j R^j`, with `0<=a_j<R`.

Starting at `c_0=0`, process the limbs from low to high:

`z_j=a_j k+c_j`,

`b_j=z_j mod R`,

`c_(j+1)=floor(z_j/R)`.

Output the low W bits of `sum_j b_j R^j`; ignore the final outgoing carry.

### Correctness and carry width

Induction gives

`k sum_(j=0)^(r-1) a_j R^j = sum_(j=0)^(r-1) b_j R^j + c_r R^r`.

At `r=q`, the ignored term is divisible by `2^W`, so the output is exactly `xk mod 2^W`. The last limb can be partially occupied; taking only the low W bits remains exact.

For `k>0`, the invariant `0<=c_j<k` implies

`0<=a_j k+c_j <=(R-1)k+(k-1)=Rk-1`.

Therefore `0<=c_(j+1)<k`, each carry has at most t bits, and each pre-split `z_j` has at most 2t bits. When `k=0`, every value is zero. No carry is propagated through an ever-growing result integer.

### Paid bit cost

Let `K(t)` denote a supplied cost for multiplying two t-bit nonnegative integers. There are exactly q local products, at most q additions on at most 2t bits, and linear input/output scans. The cost is

`O(q (K(t)+t) + W+t)`.

When `W>=t`, this is

`O((W/t) K(t) + W)`.

The general form with q is used when `W<t`; this edge case is not suppressed.

The input must be scanned in bounded windows rather than repeatedly right-shifting a W-bit integer. Likewise the output must be written into bounded windows rather than repeatedly adding a shifted term to a growing whole integer. The supplied core converts x to a byte buffer once, reads each fixed-size window once, writes each output window once, and converts the finished buffer once. The buffers have `O(W+t)` bits. The proof uses the usual sequential-bit/array arithmetic model; sequential cursors suffice, and it assumes no unit-cost W-bit multiplication, table lookup, or arbitrary-length arithmetic. Host-language object allocation and timings are not a separate machine-performance claim.

## 2. Explicit independent short-product recursion

The implementation uses a difference-form Karatsuba routine with a fixed 16-bit leaf. For t>16 put `h=ceil(t/2)` and split each argument into low/high h-bit parts. Compute

`z0=x0*y0`, `z2=x1*y1`, `zd=(x1-x0)*(y1-y0)`.

The last product is evaluated on magnitudes, with its sign restored. Then

`xy=z0 + 2^h (z0+z2-zd) + 2^(2h) z2`.

All three recursive argument pairs have at most h bits: differences of two integers in `[0,2^h)` have magnitudes less than `2^h`. This avoids an unaccounted extra-bit middle child. Additions, signs, bounded shifts, splitting and concatenation cost `O(t)`. Consequently

`K(t)<=3 K(ceil(t/2))+O(t)=O(t^alpha)`, `alpha=log_2 3`.

Leaves use only binary shift/add multiplication. This is a complete independently terminating recurrence, not a recursive call to the proposed Mersenne multiplier. The local streaming cost becomes

`O(W t^(alpha-1)+t^alpha)`.

For `W>=t` it is `O(W t^(alpha-1))`. Counting all recursive nodes at every limb is exactly what the displayed `q K(t)` charge does. No optional growing global instrumentation counter is present inside this recursion.

## 3. Apply the lemma to the factorial setup

For a length-n Taylor shift with signed coefficient height `<2^h`, retain the accepted exact widths

`H=h+n+1`, `g=ceil(log_2 n)`, `W=H+g`.

Let `s(i)=popcount(i)` and `u_i=i!/2^(i-s(i))`. Define `o_i` as the odd part of i. The required tables obey

`u_0=1`, `u_i=u_(i-1) o_i mod 2^W`,

`v_(n-1)=u_(n-1)^(-1) mod 2^W`,

`v_(i-1)=v_i o_i mod 2^W`.

Since `o_i<=i<n`, every one of the `2(n-1)` forward/reverse recurrence products meets the streaming lemma with `U=max(2,n)`. For n>=2, `t=O(log(n+1))` and `W>=n+2`, which is sufficient to absorb both the ceiling and the fixed byte padding into constant factors. Thus all forward/reverse short-factor products together cost

`O(n W (log(n+1))^(alpha-1))`.

The table stores `2n` W-bit residues and has `O(nW)` bits. Constructing the o_i values by removing trailing zero bits costs at most `O(n log^2(n+1))`, which is absorbed because `W>=n` and `log^2(n+1)=O(n)`. Array allocation, masks, reading and writing entries, and the signed/shift bookkeeping also fit in `O(nW)`.

For n=1 there are no short-factor products. The width and storage statements still hold. Empty shifts are handled separately and allocate no table.

There is still **one paid W-bit modular inversion**. Newton precision doubling performs two products at each precision and costs `O(M(W))` under the same standard multiplication regularity used by the accepted report. The present result improves only the sequential forward/reverse products; it does not reclassify inversion as a short product or hide it in the improved setup term.

## 4. Preserve exact shift reconstruction and charge everything

The change to table production does not change the tables' residues. For completeness, the shift uses

`A_i=2^(g-s(i)) u_i a_i mod 2^W`,

`G_i=2^s(i) v_i mod 2^W`,

`J_i=sigma^i G_i mod 2^W`, for `sigma in {+1,-1}`.

Reverse A, convolve with J modulo `2^W`, and set

`R_j=G_j D_(n-1-j) mod 2^W`.

The exact valuation identity gives

`G_j A_i J_(i-j)=2^g binom(i,j) sigma^(i-j) a_i (mod 2^W)`.

Thus `R_j` is divisible by `2^g`, and its quotient is the Taylor-shift coefficient modulo `2^H`. The bound

`|sum_(i>=j) binom(i,j) sigma^(i-j) a_i| < 2^(h+n)=2^(H-1)`

makes centered reconstruction unique. All g guard bits remain. Signed inputs, negative output coefficients and partial final binary chunks receive the same treatment as before.

For the convolution set

`b=8 ceil((2W+ceil(log_2 n))/8)`, `S=nb`.

Each unreduced coefficient is less than `n 2^(2W)<=2^b`; the packed product has no inter-slot carry. Exactly one integer multiplication with argument capacities S bits is paid. Bounded byte extraction costs `O(nW)`.

The full ledger is therefore:

- One packed convolution: `M(S)`.
- 2n full-width diagonal products: `O(n M(W))`.
- One odd inverse by paid precision doubling: `O(M(W))`.
- `2(n-1) ceil(W/t)` short-limb products, all recursive work included: `O(n W (log(n+1))^(alpha-1))`.
- Carry/sign/guard extraction, scans, table storage and reconstruction: `O(nW)`.

Consequently

`C_new(n,h)=O(M(S)+n M(W)+n W (log(n+1))^(alpha-1))`,

with exactly the preceding W, b and S. A more general independent short-product backend `K(t)` gives the explicit setup expression

`O(n ceil(W/t)(K(t)+t)+nW)`.

The chosen Karatsuba backend makes this sub-N-log-N setup improvement unconditional. The general expression should not be read as an unproved promise about K.

## 5. Binary, p^d and matrix interfaces

Let `p=2^m-1`, `m>=2`, input length L, padded bit capacity `N=Lm`, and `m>=cL` for a fixed c>0. Since `2^m=p+1`, binary-to-redundant-p is the `+1` shift; raw signed p coefficients to binary use the `-1` shift followed by binary carries. Canonical p digits use the accepted local exact Mersenne quotient/carry pass.

For input shifts, inverse shifts of canonical products, and the accepted lazy redundant product, n is `O(L)` and W is `O(m)`. Their coefficient bounds stay unchanged: redundant inputs need `m+L` bits and raw lazy outputs need `2m+2L+log L+O(1)` bits. The full conversion charge is therefore

`O(M(CN)+L M(Cm)+N (log(L+1))^(alpha-1))`.

Here C depends only on the fixed wide-digit constant c and on the fixed number of conversions; it does not grow with N. The separate matrix-convolution work is not included in this conversion bound. If the matrix consumes redundant rather than canonical p digits, its coefficient-cap proof must still use the enlarged heights.

For `1<=d<=L`, a local grouped shift has length at most d and W=`O(m)` since `d<=L=O(m)`. There are `O(L/d)` such shifts. The additional canonical p^d grouping/ungrouping charge is

`O((L/d) M(Cdm)+L M(Cm)+N (log(d+1))^(alpha-1))`.

Under the accepted regularity `M(t)/t` nondecreasing, the first term aggregates to `O(M(CN))`; `log(d+1)<=log(L+1)` controls setup. Partial groups, a possible extra p digit, signed coefficient expansion and bounded-overlap raw grouped readout change constants only under the same premises as the accepted interface. A lone digit with d larger than its actual length continues to use actual-width validation; this result does not allocate an artificial length-d table. No powers p^d, p^(2^j) or full factorials are constructed by the revised setup.

The fresh grouped controls verify the positional product identity using independent direct arithmetic. They are **not** a new fast grouped-matrix implementation or a proof by experiment of the grouped cost; the aggregation argument above and the accepted grouping interface provide that part.

### Prime assumptions

No step of the improved setup uses primality. For strict-prime positional p, it applies to every supplied Mersenne prime satisfying the stated width conditions. A growing family with `m=Omega(L)` cannot be claimed available without a separate prime-size/existence/selection argument. Fixing p=3 is a legitimate prime radix, but does not permit unbounded L while satisfying the wide-digit premise. Thus this wide-digit converter has not silently solved fixed-p binary conversion for the native odd-radix recursion.

## 6. What is closed and what is still open

The accepted conversion report isolated three independent obligations. This continuation discharges the N-log-N-scale forward/reverse short-factor setup obligation. At the balanced scale its ratio to the former setup bound is

`(log L)^(alpha-2)`,

which tends to zero because `alpha<2`. The ratio to `N log N` is at most a constant times `(log N)^(alpha-2)`, and also tends to zero. The improvement is at the level of a proved construction upper bound, with no universal lower-bound claim.

The following remain explicitly paid and unresolved for the user's desired little-o target:

1. The `Theta(N)`-bit packed factorial-Toeplitz convolution arguments. Calling the target multiplier here still requires a new contracting or fused construction.
2. The full-width diagonal maps and the modular inverse. The displayed `L M(Cm)` term is still present.
3. The Mersenne/matrix transform schedule and correlated point-product work. The setup lemma changes neither their aggregate recursive work nor their transform toll.
4. Prime selection if growing Mersenne primes of specified sizes are required; fixed-prime native arithmetic and wide-digit binary conversion are separate premises.

No accepted classical native-recursion bound is being relabelled as a new result, and no matrix-dimension or independent-child counting argument is used as an impossibility proof.

## 7. Fresh bounded evidence and source boundaries

`fresh_controls.py` is newly written, self-contained, standard-library-only code. It implements the streamed short multiplier, the independent recursive backend, exact odd-factorial tables, guarded Taylor shifts and local Mersenne quotient/carry steps. Historical source was read only as text and never imported or executed.

The saved run passes:

- 260 independent Karatsuba controls across split/leaf boundaries.
- 17,464 modular short-factor products, including exhaustive small input values, partial limbs, zero factors, carry boundaries, and up to 8,193 input bits.
- 40 odd-factorial/inverse tables, checked against independent full-factorial oracles in the harness only.
- 128 signed Taylor shifts, independently compared with direct binomial sums; each is also inverse-shift checked.
- 40 binary/canonical-p conversion cases, including composite Mersenne controls.
- 120 canonical grouped positional-product identities.
- 400 local quotient/remainder controls.
- One negative control showing that dropping the inter-limb carry fails.

The harness uses native Python arithmetic for expected answers only. Core represented multiplication uses the supplied shift/add and Karatsuba routines. Small index/length arithmetic is not treated as a represented wide product. No timings, benchmark claims, or asymptotic claims inferred from finite samples are reported.

`SOURCE_PINS.json` pins the four reports read for this continuation. Their accepted conclusions and attribution remain distinct from the present elementary implementation improvement. No historical novelty claim or external literature lookup is needed for the self-contained local lemma. `MANIFEST.json` seals the deliverable files.
