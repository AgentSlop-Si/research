# Native negacyclic recursion with Mersenne-radix packing

## Result

A genuine improvement over recursively reusing the supplied **full-product** routine is to make the recursive object a **native modular product**. Its ideal aggregate recursive child volume drops from about `4n` to about `2n` per modular level. This is the classical Schönhage–Strassen direction, not a new sub-`n log n` algorithm.

There is also an exact way to retain an odd positional radix `p = 2^m − 1`, including a fixed Mersenne prime, throughout the native recursion: use the odd moduli

`Q_s = (p^s + 1)/2`, for even `s`,

and pack `d` radix-`p` digits into a block of radix `B = p^d`. This repairs the failure of inverse radix-two transforms in the even modulus `p^s+1`. The resulting recurrence still has aggregate child volume asymptotic to `2n`; it does not get below that threshold by digit grouping or matrix rearrangement alone. Binary/radix-`p` conversion remains an additional, paid operation.

The exact candidate and independent controls below establish useful algebra and a stronger recursive baseline. They do **not** establish `o(N log N)`, practical superiority to the supplied implementation, or novelty. The supplied archive was inspected without executing its code.

## 1. What changes relative to the supplied code

The supplied `enhanced.py` uses a linear convolution of two length-`L` digit vectors, padded to `K >= 2L−1`. It selects a Fermat exponent `r`, a multiple of `K/2`, sufficient to reconstruct the nonnegative coefficients, and calls native Python multiplication on each of the `K` transformed pairs.

Replacing each of those pointwise products by the same **full-integer-product** routine repeats the output padding at every level. In the favorable rounded square-root picture this gives about `K r ≈ 4N` child input bits per parent with `N`-bit inputs.

The proposed replacement is a native routine `M_F(n)` computing multiplication modulo `2^n+1`. Its recursive pointwise calls remain native modular products, instead of generating complete double-width integer products only to discard half of their information. A full product is obtained once, at the outside, by choosing `n >= bits(x)+bits(y)`. The distinction between outside padding and recursive native calls is essential.

The classical attribution is explicit. GMP documents native multiplication modulo `2^N+1`, negacyclic interpolation, and recursively modular pointwise products; its description also distinguishes the full-product padding cost. See [GMP FFT multiplication](https://gmplib.org/manual/FFT-Multiplication). The original paper's publisher abstract states the `O(N log N log log N)` result: [Schönhage and Strassen, Computing 7, 281–292 (1971)](https://link.springer.com/article/10.1007/BF02242355). No claim here requires adopting another fast multiplication routine as a black box: the fresh prototype uses schoolbook shift/add leaves.

## 2. Exact negacyclic identity and economical signed reconstruction

Let `K` be a power of two and let the digit base be any integer `B >= 2`. Write

`A(X) = sum_{i=0}^{K−1} a_i X^i`,  `Bpoly(X) = sum_{j=0}^{K−1} b_j X^j`,

with digits in `[0,B−1]`. Define the length-`K` negacyclic coefficient vector by

`c_t = sum_{i+j=t} a_i b_j − sum_{i+j=t+K} a_i b_j`.

Then

`A(X) Bpoly(X) ≡ sum_t c_t X^t (mod X^K+1)`

and, exactly,

`A(B) Bpoly(B) ≡ sum_t c_t B^t (mod B^K+1)`.

Put `S=(B−1)^2` and `D=K S`. The useful asymmetric interval is

`−(K−1−t) S <= c_t <= (t+1) S`.

Its width is `D`, independent of `t`. Therefore a modulus `Q>D` suffices for exact coefficient recovery; the stronger condition `Q>2D` is unnecessary. If `u_t` is the canonical residue in `[0,Q−1]`, recover

`c_t = u_t` if `u_t <= (t+1) S`, and `c_t = u_t−Q` otherwise.

Proof: a negative admissible coefficient maps to at least `Q−(K−1−t)S`, which is strictly greater than `(t+1)S`; a nonnegative coefficient is already at most that upper endpoint. This is a constant-bit improvement in the required width, not a multiplicative reduction below the leading `2 log_2 B` term.

### Exact twist and inverse

Suppose `K` is a unit modulo `Q`, and there is an element `theta` with `theta^K=−1` such that `omega=theta^2` is a principal `K`th root. Transform the twisted inputs `a_j theta^j` and `b_j theta^j` with the ordinary `omega` DFT. Multiply the corresponding transformed entries modulo `Q`, apply the inverse DFT, and multiply position `t` by `theta^(−t)`. The result is `c_t mod Q`.

For a wrapped term, `theta^(i+j−t)=theta^K=−1`, giving the required sign. The unwrapped terms have no extra factor. No full polynomial product is assumed by this identity.

## 3. Binary native variant: exact parameters, carries, and recurrence

Let `n=Km`, `B=2^m`, and let the parent modulus be `2^n+1`. Handle the exceptional canonical residue `2^n=−1` directly; all other residues have exactly `K` ordinary `m`-bit chunks.

Choose

`b = bit_length(K(2^m−1)^2)`,

`r = K ceil(b/K)`,  `Q=2^r+1`,  `theta=2^(r/K)`,  `omega=2^(2r/K)`.

Here `2^r>D`, and `K|r`. The twist needs a `2K`th root, so the root-width restriction is `r>=K`; this is stronger than the supplied cyclic-transform restriction `r>=K/2`.

For `0<ell<K`, write `ell=2^v u` with `u` odd. Pair terms in the sum `sum_j omega^(ell j)` at a separation `K/2^(v+1)`. The ratio is `2^(ru)=−1`, so they cancel. As `Q` is odd, `K` is a unit and the inverse DFT is valid even when `Q` is composite.

### Signed carry does not need a multiplication oracle

For the exact signed coefficients, start `carry_0=0` and compute

`z_j=c_j+carry_j`,

`digit_j = z_j mod B` in `[0,B−1]`,

`carry_(j+1)=floor(z_j/B)`.

Then

`sum c_j B^j = low + carry_K B^K`,

where `low=sum digit_j B^j`. Hence the parent residue is `low−carry_K mod (2^n+1)`. Binary chunk streaming, bounded signed carries, and final correction cost `O(n+K(m+log K))` bits; there is no balanced multiplication tree in this binary reconstruction. Chunk extraction must also be streamed, rather than repeatedly shifting a growing whole integer.

### Paid recurrence

In the supplied style of full-width materialized-residue evaluation, a radix-two DFT has `K log_2 K/2` butterflies. Three transforms therefore have `3K log_2 K` addition/subtraction operations. The twists, normalization, comparisons, coefficient decoding, folding, table setup, and materialized data movement are all charged.

One native level has the bound

`M_F(n) <= K M_F(r) + C K r log K + C K r + C(n+K log n)`.

All `K` child calls target modulus `2^r+1`, with exceptional `−1` handled in linear time. The `C K r log K` term pays for the transforms, power-of-two actions, copying, and index work under the explicit bit-cost array model. It is also `Omega(K r log K)` for this fixed, full-width butterfly schedule. This is a scoped schedule claim, not an integer-multiplication lower bound.

The exact rounded width satisfies

`r = 2m + log_2 K + O(1) + O(K)`

and therefore

`rho(n) := K r/n = 2 + O(log K/m + K/m)`.

When `m` grows and rounding is controlled, this tends to `2`, rather than the approximately `4` of recursive full products.

### Rounding must be controlled, not suppressed

Simply taking `K≈sqrt(n)` can leave a constant-sized `K^2/n` rounding term. A sufficient asymptotic rule is to choose a power of two

`K = Theta(sqrt(n)/log n)` dividing `n`,

and stop at a fixed sufficiently large basecase size. Then

`r = Theta(sqrt(n) log n)`,

`rho(n) = 2 + O(1/log^2 n + log n/sqrt(n))`,

`log r = (log n)/2 + O(log log n)`.

At the outside, round the modulus exponent up to a suitable multiple of such a `K`, adding only `O(K)` bits. A child exponent `r` is itself a multiple of the preceding `K`; for all sufficiently large parents that power of two is larger than the next desired transform length, so the divisibility condition continues. Small sizes are handled by the basecase. This is why arbitrary rounding to a power of two at every child would be the wrong complexity argument.

Normalize by `n log n`. The child coefficient becomes

`K r log r/(n log n) = 1 + O(log log n/log n)`.

Along a recursion chain the logarithms decrease geometrically up to the displayed lower-order term. Above a fixed basecase, the sum of those relative errors is bounded, so products of the normalized coefficients stay bounded. There are `Theta(log log n)` levels. The displayed upper recurrence therefore gives the classical upper bound

`M_F(n) = O(n log n log log n)`.

For a fully expanded fixed schedule that performs every prescribed recursive child call, with a matching positive `Theta(K r log K)` toll at each nonleaf node, the normalized toll contributes a bounded positive amount per level and the schedule cost is `Theta(n log n log log n)`. That matching bound is not inferred from the one-sided recurrence alone. It is not asserted for every input of a routine that shortcuts special residues. The independent prototype is an exact small-instance control, not an implementation of this asymptotic parameter rule or a benchmark establishing either estimate.

## 4. Strict-prime-p-compatible candidate using p^d blocks

Keep any fixed odd positional radix `p=2^m−1`; `p=3` is already a Mersenne prime, so no assertion about infinitely many Mersenne primes is needed. Let the parent digit exponent `s` be even, and define

`Q_s=(p^s+1)/2`.

This is an integer and is odd because even `s` gives `p^s≡1 (mod 8)`. Its radix-`p` digits are particularly simple:

`Q_s = (p+1)/2 + ((p−1)/2) sum_{j=1}^{s−1} p^j`.

Thus its representation can be built in `O(s m)` bit work without computing a giant power by general multiplication.

At every recursive nonleaf odd-radix level, choose `K|s` with `K>=2` a power of two, and group `d=s/K` digits into blocks of radix `B=p^d`. Cases below the recursion cutoff are handled by the leaf routine, not by a `K=1` recursive transform. Select a child exponent `s'`, a multiple of `K` and therefore even, such that

`(p^(s')+1)/2 > K(p^d−1)^2`.

Equivalently, one can round a sufficient exponent above `log_p(2K(p^d−1)^2)` up to the next multiple of `K`. Set

`theta=p^(s'/K) mod Q_(s')`,  `omega=theta^2`.

Then `theta^K=p^(s')=−1 mod Q_(s')`. The same paired-sum proof makes `omega` principal, and the odd modulus makes `K` invertible. The transform is exact whether or not `p` or `Q_(s')` is prime.

Each pointwise product is recursively a product modulo `Q_(s')`, in the same fixed radix `p`. Exact signed coefficient recovery gives the parent product modulo `p^s+1`, hence also modulo its divisor `Q_s`. This supplies a closed native recursive family compatible with `p^d` grouping.

### Twiddles, normalization, and carry are paid

Multiplication by a power of `p` is a split/rotation of radix-`p` digits with the identity `p^(s')=−1`. The temporary lies within a constant number of moduli of zero; a constant number of radix-`p` additions or subtractions canonicalizes it. Cost: `O(s' m)` per action, including moving digits.

Inverse scaling by `K=2^k` is no longer a power-of-`p` rotation. It can nevertheless be done without general multiplication: repeat `k` times the operation

`u <- u/2` if `u` is even, otherwise `u <- (u+Q_(s'))/2`.

Each modular halving costs `O(s' m)` by a radix-`p` digit pass. Its total `O(K s' m log K)` cost is included, not declared free.

Signed coefficient carry in radix `p^d` is a digit-block split; after the last block, reduce `low−carry` using `p^s=−1`. The explicit modulus digits support the required constant-number final corrections. All reconstruction passes cost `O(K s' m+s m)`.

Let `S_p(s,m)` be the native cost in this representation. A fully charged recursive bound is

`S_p(s,m) <= K S_p(s',m) + C K s' m log K + C K s' m + C(s m+K log(s m))`,

with explicit schoolbook digit multiplication at the leaves. For fixed `p`, `m` is constant. Selecting `K=Theta(sqrt(s)/log s)` with the same divisibility discipline gives

`s' = 2d + log_p K + O(1+K)`,

`K s'/s -> 2`.

The native radix-`p` arithmetic therefore has the same classical asymptotic recurrence. If `m` varies with problem size, the `m`-dependent leaf work and every radix change must be charged; the fixed-`p` conclusion cannot simply be reused unchanged.

This variant is offered as an exact, independently checked construction, not as a claimed new algorithm. Its relevance is that keeping a prime positional `p` and packing `p^d` blocks does not force one to abandon native modular recursion. It also demonstrates that the parity objection to `p^s+1` is repairable and should not be advertised as a general impossibility.

## 5. Full product and conversion costs cannot be erased

For binary input and output, the binary native construction needs only linear outer extraction/reconstruction, and a parent exponent large enough to contain the complete product.

For the fixed odd-radix candidate, choose an admissible `s` with `Q_s > 2^(2N)` for two inputs shorter than `2^N`. Then the native residue is the full product. But the end-to-end cost is

`T_p(N) <= 2 E_p(N) + S_p(s,m) + J_p(2N+O(1)) + parameter_cost`,

where `E_p` is binary-to-radix-`p` conversion and `J_p` is radix-`p`-to-binary conversion. Their cost is not absorbed into the native product unless separately proved.

The archive's balanced routines have the schematic paid costs

`E_p(t) <= 2 E_p(t/2) + D(t,t/2) + O(t)`,

`J_p(t) <= 2 J_p(t/2) + M(t/2) + O(t)`,

plus the cost of building the required powers. Here `D` is the actual division algorithm and `M` the actual multiplication algorithm; neither is a unit-cost operation. With schoolbook primitives there is an elementary `O(N^2)` complete bound, but that is no sub-`N log N` result. Better conversion bounds require their own construction and payment. The elementary identity `z p=(z<<m)−z` does not prove that general conversion is linear.

This distinction is consistent with the primary [GMP radix-to-binary documentation](https://gmplib.org/manual/Radix-to-Binary), which treats power-of-two concatenation separately from general-radix conversion and describes the latter's multiplication tree. That documentation warns that its historical implementation description needs updating; it is cited only for this algorithmic distinction.

An alternate practical integration is to retain the supplied outer Mersenne-radix pipeline and replace only the pointwise multiplication backend by `M_F`. Its bound is

`2E_p(N) + K M_F(r) + O(K r log K) + J_p(2N) + setup`,

with the original outer linear-convolution padding unchanged. This is a legitimate backend improvement, not a proof that base conversion or outer padding vanished.

## 6. Why the proposed shortcuts do not yet improve the leading volume

### A. A single negacyclic result does not encode the full linear product

If the ordinary product coefficients are `z_0,...,z_(2K−2)`, the negacyclic channel gives `z_j−z_(j+K)`. A cyclic channel gives `z_j+z_(j+K)`. Together they recover

`z_j=(cyclic_j+negacyclic_j)/2`,

`z_(j+K)=(cyclic_j−negacyclic_j)/2`.

But the two length-`K` channels have `2K` pointwise products. Without an additional sharing identity, replacing one length-`2K` transform by these two channels does not halve aggregate recursive work. A single channel computes only the quotient-ring product unless the inputs are padded so no wrap occurs.

### B. Mersenne grouping does not change the leading coefficient width

For `B=p^d`, an interval-based exact coefficient recovery needs a modulus exceeding `K(B−1)^2`. Its size is

`2d log_2 p + log_2 K + O(1)`.

The parent has approximately `K d log_2 p` bits. Therefore this construction still has aggregate child width approximately

`K · 2d log_2 p = 2N`.

Adaptive choices of `p`, `d`, or matrix aspect ratio affect rounding, conversion, leaf cost, and constants. They do not, by themselves, remove the factor two from this coefficient-recovery construction. This is a statement about this scheme, not a lower bound against correlated or shared pointwise multiplication.

### C. The quotient relation must match the actual positional base

Wrapping a radix-`p` polynomial of length `K` computes modulo `p^K+1`; replacing it by `2^(mK)+1` is invalid when `p=2^m−1`. A tiny counterexample is `p=3`, `K=2`: multiplying the two polynomials `X` gives the negacyclic representative `−1`. At `X=3`, `9≡−1 (mod 10)` but `9` is not `−1 (mod 17)`.

### D. Matrix row carry is not an independent second wrap

For row-major blocks write `X=p^W`, `Y=p`, so `Y^W=X`. An independently negacyclic transform on both axes would instead impose `Y^W=−1`, losing the carry from a column overflow into the next row. Already for `W=2`, the product `Y·Y` must be `X`, not `−1`. A correct factored transform retains the cross phases or the equivalent relation. Merely drawing the digits as a matrix cannot change the underlying convolution dimension.

### E. Positional primality and transform-field primality are distinct

No construction above requires the positional `p` to be prime. If it must be prime, fixing `p=3` is valid and grouping by `p^d` is still possible. If one instead requires growing Mersenne primes with a prescribed adaptive size, their availability and selection cost must be justified; this report assumes no unproved density or infinitude statement.

Only if one additionally chooses the transform field to be `F_p` is the following restriction relevant: for `p=2^m−1` and `m>=2`, `v_2(p−1)=1`, so `F_p` itself has no power-of-two root of order greater than two. Extension fields and other rings are not excluded. That restriction is not a reason to reject a prime *positional* radix.

## 7. Precise remaining lemma for the user's little-o target

The present materialized transforms alone cost `Theta(N log N)` at the balanced scale. The independent native products have `rho(N)` tending to two from the non-saving side in this construction. Signed coefficients save at most constant bits here; `p^d` grouping preserves the leading width.

A successful next construction must supply an exact mechanism that changes these paid totals. One concrete sufficient route in an ideal square-root recurrence is:

1. Reduce the complete transform/conversion/carry/data-movement overhead to `O(N (log N)^beta)` with `beta<1`.
2. Compute the correlated pointwise products with an effective recursive aggregate factor uniformly below two, without charging the saved work elsewhere.

For a constant-factor ideal recurrence, this gives normalized exponent `max(beta,log_2 rho)`; equality adds a `log log N` factor. Uniform `rho<2` is sufficient, not universally necessary. Scale-dependent savings approaching two from below may accumulate. The exact requirement is that the total recursive leaf cost **and** every accumulated overhead term are `o(N log N)`.

The transformed inputs originate from only two parent inputs, so their global structure can potentially be exploited. Counting `K` separately stored child pairs is not an information-theoretic or algebraic impossibility proof. What is absent is a proved **shared-product identity and paid implementation** on that structured image, together with a sub-`N log N` transform/conversion schedule. This report supplies neither and does not manufacture them from the storage count.

## 8. Independent exact controls

`fresh_controls.py` was written independently and imports no supplied source. Its recursive binary native kernel uses schoolbook shift/add multiplication leaves. The additional odd-radix checks use small direct DFTs as algebraic test oracles, explicitly not as a fast implementation.

All controls passed:

- 5,718 exhaustive small modular products
- 360 larger boundary modular products
- 250 larger randomized modular products
- 160 complete integer products
- 432 signed negacyclic coefficient/evaluation cases
- 216 odd-radix native identities, including prime `p=3,7,31` and composite control `p=15`
- One negative control detecting the wrong positional modulus

Finite controls establish neither asymptotic complexity nor novelty. The source-level proof and its stated model supply the recurrence; no timings are reported.

## Review checklist

- Verify the asymmetric signed interval and its threshold decode.
- Verify `K|r`, rather than only `K/2|r`, for the negacyclic twist.
- Verify oddness and principal roots for `Q_s=(p^s+1)/2`.
- Verify modular halving and final carry folds are paid.
- Keep outside full-product padding separate from recursive native products.
- Keep fixed-prime positional radix, growing-prime selection, and transform field as different assumptions.
- Do not promote the native arithmetic bound to an end-to-end odd-radix bound without proving conversion cost.
- Do not interpret aggregate child volume as a general lower bound or this baseline as new prior art.
