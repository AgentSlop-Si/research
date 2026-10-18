# A precision-targeted Mersenne product interface, and the two-wide-product gate

18 October 2026 UTC. Fresh local research. No external write.

## Result and limitations

The accepted denominator-cleared converter can be composed with an exact polynomial-product service without reconstructing the large redundant product coefficients. For two `L`-chunk binary inputs with chunk width `m >= 2`, it is enough to run the entire polynomial-basis pipeline modulo

`2^H`, where `H = 2m + ceil(log_2 L)`.

The service must return the **ordinary polynomial convolution modulo this exact power of two**. After the inverse basis shift, every output residue is the actual nonnegative binary convolution coefficient. All bit guards, final carries, and output work are explicit below. This removes the need to give the downstream service an exact-integer output certificate of height `2m + 2L + O(log L)` merely because the intermediate radix-p coefficients are redundant.

This is a new precision/interface statement, not a fast implementation of that service. A native residue modulo an unrelated odd modulus cannot be substituted for it without additional reconstruction. A separate canonical `p^d` interface is also proved, with its different height contract.

The natural attempt to reuse the accepted narrow-kernel stream on **two wide inputs** now has a completely evaluated cost and a precise limitation. An exact row-carry construction uses

`q(q+1)/2` packed products, `q = ceil(H/t)`,

rather than `q` fixed-kernel products. Each packed argument has capacity `S = Theta(L(t + log L))`. With the same independently terminating Karatsuba upper-bound charge, and `log L <= t <= H`, its dominant charge is

`Theta_charge(L^alpha H^2 t^(alpha-2))`, `alpha = log_2 3`.

It is minimized in order by `t = Theta(H)`, which restores a same-scale `Theta(LH)`-bit product. Taking `t/H -> 0` worsens this specified charge by `(H/t)^(2-alpha)`. This is an optimization barrier for the explicit slab-pair recipe, not an integer-multiplication lower bound, a lower bound for all polynomial convolution, or a prohibition on exploiting correlated inputs.

A second exact scoped result is an exponent-potential barrier for the previously accepted independent native `Q_s = (p^s+1)/2` recursion. Its root and decoding conditions force `s' >= K` and `s' > 2d`, where `s=Kd`. Therefore `s log s` cannot decrease after summing over the `K` independent children. For a fixed native positional radix and constant exponent cutoff, an explicit homogeneous Karatsuba leaf ledger is at least

`Omega(N m^(alpha-1) log s)`, `N = sm`.

For very-wide supplied families this ledger is far above the desired `N log N`, even though the separately accepted outer conversion can be little-o of `N log N`. This claim is explicitly about the fixed-radix, fully expanded independent-child/charged-leaf model. Changing radix inside the recursion, using a different actual product method, or sharing point products is not ruled out.

No general sub-`N log N` multiplier is established. No faster multiplication backend is inherited and presented as a new gain. No growing suitable Mersenne-prime family is assumed.

## 1. Source contract and arithmetic model

The accepted source is `mersenne_kernel_stream_20261018_1243`, together with the mandatory qualifications in `mersenne_kernel_stream_review_20261018_1249`. The copied arithmetic helper is byte-identical and hash-pinned in this package. The new code and tests identify exactly where it is used; it is not presented as newly implemented arithmetic.

Use `alpha = log_2 3` and `a = alpha-1`. The inherited independently terminating difference-form Karatsuba implementation has proved upper bound `K(w)=O(w^alpha)` and shift/add leaves. Multiplication capacity expressions in a **homogeneous charge model** assign `Theta(w^alpha)` to a prescribed call; they are not lower bounds for the data-dependent Python routine, arbitrary multiplication, or specially structured operands.

As in the accepted result, the bit model charges bounded integer arithmetic and bounded-window array reads/writes by their bit volume. All explicit array outputs, setup, packing, carries and copies are charged. It is not a claim about Python interpreter, allocator, or address-manipulation timings. Optional explicit address-cost supplements are stated below.

The inherited actual-height correction is retained: actual shift width need not exceed the fixed kernel width merely because the ambient digit width is large. This package's `shift_mod` instead declares its target precision explicitly. Its unsimplified ledger always applies. The simplified conversion bound uses the ambient premise `m/(L log(L+1)) -> infinity`, or a sufficiently large fixed width inequality, rather than inferring a premise from the values of input coefficients.

## 2. A modular Taylor shift with a prescribed output precision

Let `T_sigma` act on a length-n vector by

`(T_sigma x)_j = sum_(i>=j) binom(i,j) sigma^(i-j) x_i`, `sigma in {-1,+1}`.

Let `H >= 1` be any requested output precision. Algebraically there is no height restriction on integer representatives `x_i`; the computational input contract is their canonical H-bit residues. If a caller supplies arbitrarily longer encoded representatives, reading/reducing those encodings is additional input work and is not hidden in the nH-bit ledger. The reference function accepts such representatives for correctness testing, while the product pipeline supplies only bounded residues.

For `n >= 2`, retain the accepted exact common-denominator tables:

- `g = ceil(log_2 n)`;
- `u_i` is the odd part of `i!`, `U=u_(n-1)`;
- `K_i = 2^popcount(i) U/u_i`;
- `t = round8((n-1)g + g + 1)`, so `u_i, U, K_i < 2^t`.

The internal ring precision is now **`W = H + g`**, rather than a width inferred from input height and an exact-output height bound. Apply the accepted scaled diagonal, reverse-convolution, and two odd modular-division streams at this `W`. Their exact algebra gives

`R_j = 2^g (T_sigma x)_j (mod 2^(H+g))`.

Every canonical `R_j` has its low `g` bits zero. Return the unsigned integer `R_j >> g`, lying in `[0,2^H)`. This is precisely `(T_sigma x)_j mod 2^H`.

Why arbitrary representatives are safe: replacing one input by `x_i + z 2^H` changes the exact scaled output by `z binom(i,j) sigma^(i-j) 2^(H+g)`, which vanishes in the internal ring. There is no need to reconstruct either that input representative or the Taylor coefficient as an ordinary integer. The proof operates on the complete map, not on an assertion that each intermediate division preserves arbitrary missing high bits by itself.

For `n=0` return the empty list. For `n=1` return the sole residue directly. For larger n the logarithmic guard remains essential: running the same scaled construction only modulo `2^H` and then removing `g` low bits would retain only `H-g` output bits.

### Complete shift bill

Set `q=ceil((H+g)/t)`, `b=round8(2t+g)`, `S=nb`. The accepted algorithm supplies:

- exactly q packed narrow-kernel calls of capacity S;
- exactly `5nq` t-bit local diagonal/division calls;
- three paid short-factor table passes and one t-bit odd inverse;
- explicit bounded input/output/carry arrays.

Its unsimplified bit-cost bound is

`C_mod(n,H) = O(q K(S) + nq K(t) + nt(log(n+1))^a + t^alpha + nqt + nH + n log^2(n+1))`.

Storage is `O(n(H+t))` plus backend workspace. For `H >= t`, or more generally an ambient `m >= t` and `H+g=O(m)`, this is

`O(nm [n^2 log(n+1)]^a)`.

No wide inverse, full-width factorial kernel, or uncharged output scaling is introduced by the precision-targeted modification.

## 3. Complete ungrouped product-interface theorem

Let `m>=2`, `L>=1`, `B=2^m`, `p=B-1`, `N=Lm`, and `0<=X,Y<2^N`. Extract exactly L binary chunks and define

`A(Z)=sum a_i Z^i`, `Bpoly(Z)=sum b_i Z^i`, with `0<=a_i,b_i<B`.

Put `H=2m+ceil(log_2 L)` and work in the coefficient ring `R=Z/(2^H)`. Form

`C=T_+(a) mod 2^H`, `D=T_+(b) mod 2^H`.

Call a product service with the following exact contract:

> Given two length-L arrays in R, return all `2L-1` coefficients of their ordinary linear polynomial product in R. The service reports and pays its own bit cost and workspace. Cyclic or negacyclic convolution without sufficient padding is not the same output contract.

Let `z` be that service result. Return

`v = T_-(z) mod 2^H`,

then perform ordinary binary radix-B carries on the nonnegative v coefficients.

### Proof

Translation by 1 is a polynomial-ring automorphism over every commutative coefficient ring; its inverse is translation by -1. It preserves multiplication. Thus

`T_-((T_+ a) * (T_+ b)) = a*b` in R.

Every exact coefficient of `a*b` is nonnegative and satisfies

`(a*b)_j <= L(B-1)^2 < L B^2 <= 2^H`.

The canonical residues v therefore equal the exact ordinary coefficients, with no signed reconstruction ambiguity. Their positional value at B is exactly XY. The final carry stream and bounded-window assembly return that integer, which has at most 2N bits.

The reference implementation uses nonnegative final representatives, so no additional centered-sign bit is needed. A centered reconstruction convention would need its own extra bit or equivalent signed interval rule. `H` is a convenient safe width; the exact maximal-coefficient width is `bit_length(L(B-1)^2)`, which may be smaller for some parameters. For powers-of-two L and `m>=2`, reducing the stated H by one fails on all-maximal input chunks.

### What is and is not a base-p representation

Over the integers, `A(p+1)=X`, so the exact `T_+ a` vector is the accepted redundant base-p expansion. If coefficient reduction wraps, its residues alone no longer constitute that exact integer expansion. They are a residue-certified polynomial object whose exact final meaning is supplied by the homomorphism and final coefficient bound above. This distinction is part of the interface.

In the sufficiently wide regime the forward coefficients often fit without wrapping, but the theorem does not need this. The raw product may wrap substantially; reconstructing it as an exact integer is deliberately unnecessary.

### Complete composition and cost

If the service cost is `P(L,H)`, the total is

`2 C_mod(L,H) + P(L,H) + C_mod(2L-1,H) + O(L(m+log(L+1)))`.

The last term pays binary extraction, all carries including the terminal carry, and the full binary output. The carry is bounded by `L(B-1)` before the next coefficient, because a coefficient is at most `L(B-1)^2`. Thus each step has `O(m+log(L+1))` bits. Under the ambient very-wide premise these streams cost O(N), including the final tail.

For supplied families with `m/(L log(L+1)) -> infinity`, the non-service part is

`O(N [L^2 log(L+1)]^a)`.

This includes both directions at the actual length `2L-1` of the product, not only the input shifts. For `L=O((log N)^(4/5))` it is `o(N log N)`, with the inherited bounded-L/direct and address-accounting qualifications. The same input-encoding qualification applies to any externally supplied parameters. The product service remains a separate obligation. A symbolic `P` is not advertised as a completed multiplier improvement; section 5 supplies an explicit complete, slower instantiation.

## 4. The grouped canonical p^d interface and the odd-modulus mismatch

### Canonical grouped digits

Let `R_d=p^d`, `1<=d<=L`, and suppose the actual inputs are length-k canonical block arrays satisfying `0<=a_j,b_j<R_d`. Their raw block convolution has

`0 <= z_j <= k(R_d-1)^2 < 2^(2dm+ceil(log_2 k))`.

Consequently a service returning ordinary block convolution modulo

`2^H_d`, `H_d=2dm+ceil(log_2 k)`,

returns the exact nonnegative raw block coefficients as canonical residues. The accepted raw-grouped conversion then expands each coefficient into p digits, places it at offset jd with bounded overlap, and performs the global binary reconstruction. No general division by or freely constructed power of `p^d` is required.

For original L-chunk binary inputs, first use the accepted canonical p converter, retaining its actual digit length `L_p=O(L)` and possible extra digit. Set `k=ceil(L_p/d)` and pad only the final partial block. Since `kd=O(L)` for `d<=L`, the total conversion/reconstruction bill remains

`O(N [L^2 log(L+1)]^a)`,

and the separately paid product term is `P(k,H_d)`, with `H_d=O(dm+log L)`. The arbitrary encoding of an unrestricted d is not free; this theorem deliberately states `1<=d<=L`. Any wider extension must add the inherited `O(bitlength(d))` input cost and use actual lengths.

The bound `H_d` is for **canonical grouped input values**. It cannot be transferred unchanged to groups of the unnormalized redundant Taylor coefficients, which may exceed the canonical radix range. Either use the modular polynomial interface in section 3 at digit level, canonicalize before grouping, or prove/pay the larger actual grouped height.

A concrete warning: with `m=2, p=3, a=b=[3,3]`, the exact forward Taylor vector is `[6,3]`. Its raw product is `[36,36,9]`. Reducing modulo 32 gives `[4,4,9]`, whose ordinary evaluation at p is 97, while the true product is 225. Applying the modular inverse Taylor shift gives `[9,18,9]`, whose binary evaluation is 225. The two output interfaces are genuinely different.

### An odd-modulus product is not a power-of-two product

A backend computing z modulo an odd Q has not fulfilled the service contract modulo `2^H`. In general the same odd-modulus residue represents z and z+Q, whose residues modulo `2^H` differ. There is no well-defined identity-on-integers map `Z/Q -> Z/(2^H)` unless the required divisibility condition holds; for odd Q it does not.

On the same example, reducing `[36,36,9]` modulo 17 and feeding those values to the modular inverse shift yields `[9,16,9]` modulo 32, rather than `[9,18,9]`. The finite control catches this exact invalid substitution.

An odd-modulus transform is still usable if its own decoding interval determines every required exact coefficient before reduction, or if a separately proved reconstruction/CRT mechanism produces the needed power-of-two residue. That precision and its bit cost must be paid. The new H lemma does not silently improve the precision of the inherited odd native transform.

## 5. A complete two-wide product implementation

The delivered `two_wide_convolution` is a fully evaluated service. It uses the same explicit inherited Karatsuba backend; there is no call to a proposed faster Mersenne multiplier.

Let both length-L input arrays have entries in `[0,2^H)`. Choose a byte-aligned `t>=8`, set `R=2^t`, `q=ceil(H/t)`, and expand

`x_i=sum_(r<q) x_(i,r) R^r`, `y_i=sum_(s<q) y_(i,s) R^s`.

A term with `r+s>=q` vanishes modulo `2^H`, since `qt>=H`. The algorithm enumerates exactly the triangular set `r+s<q`, giving `q(q+1)/2` packed products. For a pair (r,s), its ordinary polynomial convolution coefficients are

`c_(j,r,s)=sum_i x_(i,r) y_(j-i,s) <= L(R-1)^2`.

Set `g=ceil(log_2 L)`, `b=round8(2t+g)`. Packing each slab into L base-`2^b` slots gives a product without inter-slot carries. The argument capacity is `S=Lb`; all `2L-1` output windows are extracted, not just a prefix.

### Row-carry schedule with no growing log(q) accumulator

Process r from 0 to q-1. For each output coefficient j, start a carry `e=0`. For `s=0,...,q-r-1`, read the current stored result limb `o` at position `r+s`, and compute

`z=c_(j,r,s)+o+e`, `new_limb=z mod R`, `new_e=floor(z/R)`.

The invariant `0<=e<=L(R-1)` holds. Indeed,

`z <= L(R-1)^2 + (R-1) + L(R-1)`
`  = L R(R-1) + (R-1)`,

so `new_e<=L(R-1)`. Every pre-split value has `O(2t+log(L+1))` bits, independently of q. This is an actual row-carry schedule, not an assumption that a sum of q convolution coefficients remains narrow.

At the end of row r, its final carry occurs at digit q and can be discarded modulo `R^q`, hence modulo `2^H`. The telescoping carry identity proves that this row added

`R^r sum_(s<q-r) c_(j,r,s) R^s`

to the existing coefficient modulo `R^q`. Induction over r includes every contributing pair. A final partial-limb mask gives the required residue modulo `2^H`.

One left slab is packed once per row. Each right slab and result is handled through bounded windows. Input buffers are prepared once. There is no repeated whole-H-bit shifting, or repeated addition into a growing H-bit output. Memory is `O(L(H+t))` plus backend workspace; for `t<=H` it is O(LH). The code pays all `2L-1` result arrays.

### Complete bit ledger and exact recipe barrier

The complete upper ledger is

`P_pair(L,H,t) = O(q(q+1) K(S) + q(q+1) L(t+g) + L(H+t))`.

Packing, reads, output writes, carry updates and repeated slab scans are included. With `t>=max(8,g)`, `t<=H`, and the homogeneous Karatsuba charge,

`q(q+1)/2 * S^alpha = Theta(L^alpha H^2 t^(alpha-2))`.

Since `1<alpha<2`, the expression decreases in order as t grows. More formally, `q>=H/t` and `S>=2Lt` give the lower charged bound

`c L^alpha H^2 t^(alpha-2) >= c (LH)^alpha`

for every `t<=H`. Taking the byte-rounded `t=H` gives q bounded by a constant, `S=Theta(LH)`, and the matching upper order. If `t>H`, one call already has capacity `Omega(LH)` and cannot improve this charge. Thus optimization of this recipe cannot reproduce the fixed-kernel gain. For the declared full-H service at the one-slab choice, `S>=2LH>=4N` in the product interface. Literally substituting the proposed N-bit multiplier at that packed call is noncontracting. Exploiting the smaller actual forward-coefficient height can change this constant, but does not by itself supply a contracting recurrence or remove the paid product.

At the accepted small kernel scale `t=Theta(L log(L+1))` with `H/t -> infinity`, its dominant upper-bound charge is worse than the one-wide-packed-product charge by

`Theta((H/t)^(2-alpha))`.

The fixed-kernel converter needed q slab products because only one operand varied across the wide limb axis. General product operands have two limb axes. The simple but invalid diagonal-only replacement misses cross terms: with `x=y=257`, `t=8`, `H=24`, the correct result is 66049; keeping only matching limb pairs gives 65537.

There may be better bilinear combination schemes, shared-product identities, carry-aware specializations, or recursion on the structured Taylor images. This theorem does not exclude them. In fact, the modular Taylor maps are invertible on the whole coefficient ring; any argument that relies only on that invertible linear change of coordinates has not yet explained a restricted image. The particular bounded binary-chunk image is smaller and remains a possible source of structure, not a proved saving.

If an implementation charges `O(log(L(H+t)))` per bounded-window address, add conservatively

`O(q(q+1) L log(L(H+t)))`

to the product ledger. This extra nonnegative term cannot invalidate the recipe obstruction or supply a saving. It must be included if proposing a stronger machine-model upper bound.

## 6. A native-product exponent potential: what independent recursion cannot erase

This section uses the earlier accepted native family as a precisely stated model. Fix `p=2^m-1>=3` within one recursive tree. At a node of even exponent s, let `K>=2` be a power of two dividing s, `d=s/K`, and choose the child exponent s' as a positive multiple of K satisfying

`Q_(s')=(p^(s')+1)/2 > K(p^d-1)^2`.

The radix-two twist root is `p^(s'/K)`. The schedule materializes and separately calls all K native children. It does not shortcut them based on values or replace their products by a shared product.

### Exact size inequalities

The multiple-of-K root condition implies `s'>=K`. Also `s'>2d`. To see the latter, write `z=p^d>=3`. If `s'<=2d`, then

`Q_(s') <= (z^2+1)/2 < 2(z-1)^2 <= K(z-1)^2`,

where the strict middle inequality follows from `3z^2-8z+3>0` for `z>=3`. This contradicts the decoding condition.

Therefore

`K s' >= 2s`, and `(s')^2 >= 2s`.

For `Phi(s)=s log_2 s`, these yield

`K Phi(s') >= 2s * (1/2)log_2(2s) = s log_2(2s) >= Phi(s)`.

This proof is uniform in K and includes all upward rounding. It does not replace an exact constraint by an unqualified asymptotic aggregate factor of two.

### Finite-tree consequence and paid wide leaves

Assume the recursion terminates and every leaf exponent is at most a fixed `s_0>1`; all internal children are paid as stipulated. Summing the potential inequality down the tree gives

`sum_leaves s_leaf log_2(s_leaf) >= s log_2 s`,

and consequently

`sum_leaves s_leaf >= s log_2 s / log_2 s_0`.

These exponents represent `m s_leaf` bits of digit capacity. A model charging `Theta((m s_leaf)^alpha)` for each explicit homogeneous Karatsuba leaf therefore has leaf charge at least

`Omega(m^alpha s log s) = Omega(N m^a log s)`, `N=ms`.

This is solely a charged-schedule statement. The delivered inherited Karatsuba routine can shorten branches on numerical values, so its universal inputwise running-time lower bound is not inferred. A fixed-width, fully expanded implementation realizes the homogeneous model. Independent schoolbook leaves have their analogous larger ledger. A claimed general upper bound obtained by summing these homogeneous Karatsuba prices cannot become sub-N-log-N in the very-wide polylogarithmic-s family.

For fixed m, even linear leaf volume already yields `Omega(N log N)` for this fixed-width schedule. For growing m, volume alone gives only `Omega(N log s)`, and **does not** establish an N-log-N barrier. The extra wide-leaf charge is essential. This is why the fixed-radix classical conclusion cannot simply be transported to the adaptive very-wide setting without charging its m-dependent leaves.

Changing positional radix at recursive calls, using a new product backend with an actual proved cost, or exploiting correlations changes the model and requires a new, paid interface. Nothing here forbids that. Counting separately prescribed children is not an information-theoretic lower bound on their joint product.

## 7. Deliverables, checks and the remaining exact gate

`product_interface.py` implements the modular Taylor adapter, the row-carry two-wide service, bounded-window binary extraction/reconstruction, and the complete product pipeline. Its production default multiplication is the explicitly pinned inherited Karatsuba routine. There is no native wide Python multiplication in those new production functions.

`fresh_controls.py` uses independent native arithmetic, binomial formulas, exact powers and direct convolutions as correctness oracles. It checks:

- modular shifts at prescribed precisions smaller than coefficient height, both signs, arbitrary signed representatives, and inverse identities;
- every tested two-wide coefficient, carry transition, packed call count, and argument capacity;
- byte-boundary and non-byte-aligned binary extraction/reconstruction;
- complete products against independent integer multiplication, including wide supplied m and prime/composite Mersenne controls;
- canonical p^d coefficient precision at every tested block size;
- exact native exponent-potential size certificates;
- three negative controls: insufficient output precision, odd-modulus substitution, and missing cross-limb products.

Finite checks do not prove asymptotic complexity or novelty. The proofs above establish only their specified arithmetic and schedule statements. `RESULTS.json` and `RUN.log` contain completed counts and a deterministic digest; `SOURCE_PINS.json` and `MANIFEST.json` bind the package.

The remaining service needed by the ungrouped route is now unambiguous: produce all coefficients of the ordinary convolution of the two Taylor images modulo the specified `2^H`, at a fully paid cost which, together with the already sub-N-log-N interface, meets the target. An odd native backend must instead deliver its separately proved exact-reconstruction bridge. The two-wide stream and independent native tree analyzed here do not provide the desired saving. Any successful next result must change their product organization, not merely reuse the small conversion kernel or rename its digit grouping.

### Completed finite results

The final harness passed 990 modular-shift cases, 792 two-wide convolution cases with 203,928 checked carry transitions, 1,008 binary-window round trips, 4,789 small complete products, 175 larger/wide complete products, 80 canonical grouped-precision cases, 1,024 exact native-potential certificates, and all 14 negative-control instances. The deterministic transcript digest is `727f3415ad1166e13d70597634806d458f6abae81f0833edc71aebb8ddebd9b8`. The final standard-error log is empty. These are candidate self-checks; independent review remains required.
