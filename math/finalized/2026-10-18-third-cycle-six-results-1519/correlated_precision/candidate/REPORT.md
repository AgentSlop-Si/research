# Correlated Mersenne products: fixed-precision bilinear rigidity and the exact interpolation guard

18 October 2026 UTC. Local research and checks only. No external write.

## Result, and what remains open

Two exact interface results close a gap left open by the accepted final-only product service.

1. **Fixed-precision sharing has a stronger obstruction than a dimension count.** For `L >= 3`, ordinary length-`L` polynomial multiplication over `Z/(2^H)` requires at least `2L` scalar products in the separated-input, ring-bilinear model defined below. The usual `2L-1` interpolation count is impossible in that model. This remains true when correctness is required only on the bounded binary-chunk Taylor images used by the Mersenne route. If every prescribed scalar call has a fixed capacity valid on that image, at least `2L` calls each need capacity at least `m`; their aggregate capacity is at least `2Lm = 2N`.

2. **The precise way integer-point interpolation escapes is now quantified.** Recovering all coefficients of an arbitrary integer polynomial of degree at most `d`, modulo `2^H`, from its values at ordinary integer points needs exactly

   `Gamma(d) = v_2(d!) = d - popcount(d)`

   uniform guard bits in the worst case. Consecutive points `0,...,d` suffice. With one fewer bit, even arbitrarily many integer sampling points cannot distinguish a certain nonzero coefficient vector from zero. This is an information-loss statement about the sampled values, not merely a failure of a particular interpolation formula. For the product service, `d=2L-2`; this linear-in-`L` guard is different from the accepted logarithmic Taylor-shift guard.

A complete reference implementation realizes the guarded interface with exactly `2L-1` explicit evaluation products, paid finite-difference interpolation, short odd-divisor streams, and all output coefficients. A division-free six-product implementation at `L=3` matches the first theorem, while five guarded products illustrate the escape. These are standard algebraic mechanisms used here as constructive controls; no historical novelty or new fast multiplication saving is claimed.

With the already accepted, explicitly terminating Karatsuba backend, the integrated Mersenne route has complete upper bound

`O((2L-1) h^alpha + N ([L^2 log(L+1)]^(alpha-1) + L log(L+1)))`,

where `alpha=log_2 3`, `h=m+O(L log(L+1))` in the very-wide regime, and `N=Lm`. Its non-product work can be `o(N log N)` on the accepted small-`L` families. Its product term is still `Theta_charge(N^alpha/L^(alpha-1))`, so this construction does not supply the requested general little-o multiplier. Recursively reusing this particular small-`L` guarded construction also has a separately proved leaf-volume obstruction below.

These theorems do not prohibit nonlinear bit extraction, carry-aware output reconstruction, packed products with nonlinear unpacking, extension-ring products, precision-lifted divisions, or other jointly structured algorithms. They do not settle correlated sharing in the odd native `Q_s` family. The first theorem specifically concerns the accepted power-of-two coefficient interface; the second identifies a paid way to leave that restricted model.

## 1. Accepted contract and scope of the scalar model

The input sources are the accepted `mersenne_product_interface_20261018_1333` report and the mandatory corrections in `mersenne_product_cost_review_20261018_1343`. The latter's storage qualification is retained. The copied arithmetic helpers are byte-identical, hash-pinned dependencies; they are not new arithmetic.

Let

`B=2^m`, `p=B-1`, `N=Lm`, `H=2m+ceil(log_2 L)`.

Let `a,b` be length-`L` vectors with coordinates in `[0,B)`. The Taylor map `T_+` sends a polynomial `A(Z)` to `A(Z+1)`; `T_-` is its inverse. Both coefficient matrices are triangular with diagonal entries one, hence invertible over every `Z/(2^H)` and modulo 2. The accepted pipeline asks for every coefficient of the ordinary linear product of `T_+a` and `T_+b` modulo `2^H`, and applies `T_-` before binary carries.

A **separated-input ring-bilinear scalar algorithm** over `R=Z/(2^H)` has a fixed list of products

`u_t = ell_t(c) * r_t(d) in R`, `1 <= t <= r`,

where `ell_t` is an `R`-linear form in only the left input, `r_t` is an `R`-linear form in only the right input, and every output is a fixed `R`-linear combination of the `u_t`. Linear setup and reconstruction may be arbitrary and need not be sparse. Odd modular divisions are allowed as multiplication by units. A product returning an extension-ring element is not one scalar product in this definition.

This model excludes divisions by powers of two followed by a precision change, input-dependent branching, digit extraction, value-dependent product selection, and nonlinear output carries. It also excludes multiplication gates whose two operands both mix left and right inputs. The theorem is deliberately not a lower bound for arbitrary arithmetic circuits or integer multiplication.

All costs use the accepted bounded-window bit/array model. We count setup, every scalar product, full output arrays, reading, carries, and bounded arithmetic. Homogeneous capacity charges are prices of a specified schedule, not universal inputwise running-time lower bounds for the data-dependent Karatsuba implementation.

## 2. Bounded Taylor images do not evade bilinear identities

Suppose an algorithm of the stated form is correct on all pairs

`c=T_+a`, `d=T_+b`, with `a,b in {0,...,B-1}^L`.

Compose its input forms with `T_+` and its output with `T_-`. This is still a separated-input ring-bilinear algorithm and must return `a*b` on the bounded cube. The cube contains every basis vector `e_i`. Correctness at all pairs `(e_i,e_j)` fixes every coefficient of the bilinear map. Therefore that same bilinear identity holds on all of `R^L x R^L`.

In particular, reducing this identity modulo 2 gives a bilinear algorithm for ordinary polynomial multiplication over `F_2` with no more scalar products. There is no assertion that bounded inputs themselves fill the large ring. The extension follows because a bilinear identity is determined by its values on basis pairs.

This observation also applies if the algorithm is supplied the original chunks directly, or if other invertible linear maps are inserted before or after the service. A restricted-input saving must use something beyond a fixed ring-bilinear identity.

## 3. The rank-one Hankel obstruction

### Theorem

For `L>=3` and any `H>=1`, every algorithm in the model above computing the ordinary length-`L` convolution has at least `2L` scalar products. The same holds on the bounded Taylor image whenever `m>=1` and `m<=H`.

### Proof

Work modulo 2. The `k`th convolution coefficient is the bilinear form with matrix

`(M_k)_(i,j) = 1 if i+j=k, and 0 otherwise`, `0<=k<=2L-2`.

The `2L-1` matrices `M_k` are linearly independent. Their span is exactly the space `mathcal H_L` of all `L x L` Hankel matrices, meaning matrices constant on each anti-diagonal.

Each scalar product has a rank-one coefficient matrix `a_t b_t^T`, after deleting zero terms. Since the outputs are linear combinations, `mathcal H_L` lies in the span of these rank-one matrices. Dimension first gives `r>=2L-1`.

Suppose equality held. The span of the `r` rank-one matrices would then equal `mathcal H_L`, so each one would itself have to be Hankel. But over `F_2` there are only three nonzero rank-one Hankel matrices for `L>=2`:

- `e_0 e_0^T`;
- `e_(L-1) e_(L-1)^T`;
- the all-ones matrix.

Here is a direct proof of this classification. A Hankel matrix is symmetric. A nonzero rank-one symmetric matrix over `F_2` has the form `v v^T`. Hankelness gives

`v_i = v_(i-1) v_(i+1)` for `1<=i<=L-2`.

If an interior coordinate equals one, the relation forces its two neighbors to equal one, and propagation makes every coordinate one. If all interior coordinates are zero, only the two endpoints can be nonzero. Both endpoints cannot be one when `L>=3`, because the anti-diagonal entry `(0,L-1)` would be one whereas `(1,L-2)` would be zero. Thus only one endpoint is nonzero. For `L=2`, the three nonzero vectors give the same stated classification directly.

The three matrices span dimension three. For `L>=3`, `3 < 2L-1`, so they cannot span `mathcal H_L`. Equality `r=2L-1` is impossible, and hence `r>=2L`.

The bounded-image conclusion follows from Section 2. Products annihilated modulo 2, including products whose output weights all vanish modulo 2, can be discarded first; at least `2L` terms survive. This does not assume the ring `R` is a field.

### Exact small control

At `L=3`, six scalar products suffice over every commutative ring. Set

`u_i=a_i b_i` for `i=0,1,2`,

`v_ij=(a_i+a_j)(b_i+b_j)` for `ij=01,02,12`.

The five outputs are

`u_0`,
`v_01-u_0-u_1`,
`v_02-u_0-u_2+u_1`,
`v_12-u_1-u_2`,
`u_2`.

No division or extra precision is used. Thus the scalar bilinear rank is exactly six for length three over `Z/(2^H)`. The delivered `six_product_three` realizes all six products, all five outputs, and the additions, with cost `O(6 K(H)+H)` and `O(H)` non-backend storage at this fixed length. `K(w)=O(w^alpha)` is the inherited terminating backend.

For `L=1`, one product suffices; for `L=2`, three division-free Karatsuba products suffice and the dimension bound is sharp. The theorem makes no exact-rank claim for `L>=4` beyond its stated lower bound.

## 4. Aggregate capacity on the actual bounded input family

A prescribed product surviving modulo 2 has a nonzero left linear form modulo 2 after composition with `T_+`. At least one coefficient is odd, and therefore a unit modulo `2^H`. Vary only that original input coordinate over the `B=2^m` possible chunk values. The form takes `B` distinct values modulo `2^H`.

A fixed canonical binary capacity smaller than `m` bits could encode fewer than `B` possible residues. Thus the left argument's declared capacity must be at least `m`. The same argument applies to the right form. Every surviving product consequently has maximum argument capacity at least `m`.

There are at least `2L` such products, so their summed fixed capacities obey

`sum_t h_t >= 2Lm = 2N` for `L>=3`.

This is a barrier to obtaining a uniform aggregate factor below two from this specific scalar sharing interface, even though the input arrays are correlated Taylor images. If all calls are instead charged at full ring width `H`, their aggregate capacity is at least `2LH >= 4N`.

The capacities are uniform scheduled capacities, with maxima possibly attained on different inputs. This is not an assertion that every numerical input realizes all maxima simultaneously, nor a universal runtime lower bound. Variable-width branching, decoding packed products, different output interfaces, and precision lifting fall outside the proof. A lower bound of `2N` aggregate capacity by itself is also not an `N log N` lower bound: the recursion shrinkage, repeated overhead, and leaf costs remain essential.

## 5. Exact guard theorem for ordinary integer-point samples

Let `P in Z[Z]` have degree at most `d`, let `H>=1`, and suppose we want every monomial coefficient modulo `2^H`. A sample at an integer `z` supplies only

`P(z) modulo 2^(H+G)`.

### Theorem

The smallest uniform nonnegative guard `G` that always permits reconstruction from ordinary integer-point samples is

`Gamma(d)=v_2(d!)=d-popcount(d)`.

The `d+1` points `0,...,d` suffice with this guard. When `Gamma>0`, any guard `G<=Gamma-1` fails even if values at every integer point are available, and even if the reconstruction rule is nonlinear.

### Sufficiency

Let `W=H+Gamma`. From the consecutive samples compute all leading forward differences

`D_k = Delta^k P(0) modulo 2^W`, `0<=k<=d`.

For an integer-coefficient polynomial, `D_k` is divisible by `k!` as an ordinary integer. Write

`k! = 2^(v_k) u_k`, with `u_k` odd and `v_k<=Gamma`.

The canonical residue of `D_k` has its low `v_k` bits zero. Removing those bits leaves `D_k/2^(v_k)` modulo `2^(W-v_k)`, which includes at least `H` bits. Dividing by the odd `u_k` modulo `2^H` gives

`b_k = D_k/k! modulo 2^H`.

Newton interpolation then gives

`P(Z) = sum_(k=0)^d b_k (Z)_k modulo 2^H`,

where `(Z)_k=Z(Z-1)...(Z-k+1)` and `(Z)_0=1`.

Conversion of this falling-factorial basis to the monomial basis uses only integer additions and multiplication by the small indices. All operations are explicitly realized in the code.

The exact identity `v_2(d!)=sum_(j>=1) floor(d/2^j)=d-popcount(d)` supplies the guard. Empty divisions and degree-zero/degree-one cases need no guard.

### Necessity at all integer points

For `Gamma>0`, consider

`P_*(Z)=2^(H-1) (Z)_d`.

Its leading coefficient is `2^(H-1)`, nonzero modulo `2^H`. For every integer `z`, including negative integers, `(z)_d=d! binom(z,d)` is divisible by `d!`. Therefore

`P_*(z) = 0 modulo 2^(H+Gamma-1)` for every integer z.

At insufficient precision, the entire sampled function is indistinguishable from the zero polynomial, despite the differing required coefficient vector. More integer nodes, different integer nodes, and adaptive selection of integer nodes cannot recover the information. At least one stronger source of information is necessary.

This theorem concerns reconstruction from values alone. An algorithm allowed to inspect and use the original operands outside the samples is not constrained to be a sample-only reconstruction algorithm. Derivative samples, non-integer/extension-ring evaluation, and separate coefficient information change the model.

### The obstruction can be factorable, with canonical inputs

For the product degree `d=2L-2`, the guard obstruction is not only an irreducible-polynomial artifact. Set

`F(Z)=product_(j=0)^(L-2) (Z+j)`,
`G(Z)=product_(j=L-1)^(2L-3) (Z+j)`.

Their product is the rising factorial `Z(Z+1)...(Z+d-1)`, also divisible by `d!` at every integer. Take `u=floor((H-1)/2)` and `v=H-1-u`; multiply `F` and `G` by `2^u` and `2^v` respectively. Their product has a nonzero leading coefficient `2^(H-1) mod 2^H`, but every integer sample vanishes modulo `2^(H+Gamma-1)`.

All coefficients are nonnegative. If `t=bit_length(d!)` and `H>=2t+2`, both scaled factor arrays have coefficients strictly below `2^H`: each unscaled coefficient is at most the value at one, which is at most `d!`, and the displayed margin is sufficient. Thus the obstruction already occurs among products of two canonical `H`-bit length-`L` input arrays for sufficiently large `H`.

This does **not** prove the same optimal guard on the smaller `m`-bit original-chunk Taylor image. The factorable witness is for the unrestricted product service. The guard is sufficient on the smaller image, while its optimality there remains unproved here. The fixed-precision bilinear obstruction in Sections 2–4 does apply to that smaller image.

## 6. Complete guarded product service

Let both input arrays have length `L`; put

`n=2L-1`, `Gamma=v_2((2L-2)!)`, `W=H+Gamma`.

Choose canonical `W`-bit lifts of the inputs. Evaluate both polynomials at `0,...,n-1`, reducing modulo `2^W`. Make exactly `n` ordinary integer product calls on the two corresponding residues and retain each product modulo `2^W`. Interpolate by Section 5, returning all `n` coefficients modulo `2^H`.

Changing a lift by a multiple of `2^H` changes the true polynomial product by coefficients divisible by `2^H`; the final reconstructed vector is therefore independent of that lift. It is legitimate for the integrated route to supply more informative lifts when they permit smaller actual product arguments.

### Paid arithmetic, not an inverse oracle

The implementation does the following work explicitly:

- `2nL` Horner multiply-by-small actions, with points of `O(log(L+1))` bits;
- exactly `n` evaluation-product calls;
- exactly `n(n-1)/2` forward-difference subtractions at width `W`;
- short-factor construction of the odd parts `u_k` of `k!`, each of `O(L log(L+1))` bits;
- exactly `nH` one-bit odd-division steps;
- exactly `n(n-1)/2` multiply-by-small actions to convert the Newton basis, plus output additions;
- all `n` final coefficient writes.

For odd divisor `u`, the division step at bit `j` reads input bit `x_j`, chooses

`q_j=(x_j-carry_j) mod 2`,

and updates

`carry_(j+1)=(carry_j+u q_j-x_j)/2`.

The invariant is `0<=carry_j<u`, and the telescoping identity is

`u sum_(i<j) q_i 2^i = sum_(i<j) x_i 2^i + 2^j carry_j`.

After `H` steps this gives the desired odd modular division. The implementation reads a fixed byte source and writes a byte output. It does not repeatedly shift a full-width source or grow a whole-width quotient at each bit. Every carry action costs `O(bit_length(u))`; no wide modular inverse is hidden.

The complete non-product bit cost is

`O(L^2 W log(L+1))`.

This includes the `O(L^2 log^2(L+1))` factorial-odd preparation: for this guard, `W` is already at least a constant multiple of `L` when `L>=2`, so preparation is absorbed. Non-backend storage is `O(LW)` bits. The current odd divisor uses `O(L log(L+1))` bits and is also absorbed; all packed/sample/product output buffers are included. Backend workspace is additional.

For a generic service use, each product can be charged at width `W`. When the actual input family has a proved smaller evaluation capacity `h<=W`, the product term is instead exactly `n` calls of capacity at most `h`, giving

`P_guard = O((2L-1) K(h) + L^2 W log(L+1))`.

There is no assumption of a faster product oracle. The production default is the copied, explicitly terminating Karatsuba routine with `K(h)=O(h^alpha)`. These formulas are arithmetic-model bounds, not Python timing claims. A conservative explicit address-cost supplement is

`O((L^2 log(L+1)+LH) log(LW+2))`,

covering the small-action and bitstream loops; include it if the machine model charges each bounded-window address separately. It does not provide a saving or invalidate the stated obstructions.

## 7. Integration with the accepted Mersenne route

Use final precision `H=2m+ceil(log_2 L)` and internal sample precision `W=H+Gamma`. Run both forward Taylor shifts at requested output precision `W`, not merely `H`; their own accepted logarithmic guard is additional and is already included in `C_mod(L,W)`.

The exact coefficients `c_j` of `C(Z)=A(Z+1)` satisfy

`0<=c_j<2^(m+L)`.

Also `Gamma=v_2((2L-2)!)>=L-1`, so for `m>=2` we have `W>=m+L`. Consequently the canonical forward residues at precision `W` are the exact integer Taylor coefficients. This is a proved actual-height fact for this particular lift, not an assumption that arbitrary modular residues remain short.

At sample point `j`,

`C(j)=A(j+1)`.

For `L>=2` and `0<=j<=2L-2`,

`C(j) < 2^m L (2L-1)^(L-1)`.

Thus both canonical sample residues have capacity at most

`h=min(W, m+ceil(log_2 L)+(L-1)ceil(log_2(2L-1)))`.

For `L=1`, take `h=m`. If a nonnegative exact sample wraps modulo `2^W`, reduction cannot increase it, so the capacity bound remains valid in every regime.

After the guarded convolution returns all raw product coefficients modulo `2^H`, apply the accepted inverse Taylor shift at requested precision `H`. The resulting canonical coefficients are the exact nonnegative binary-chunk convolution coefficients, by the accepted final-only precision theorem. Carry and output assembly are unchanged and fully paid.

The complete, unsimplified integrated bill is

`2 C_mod(L,W) + (2L-1) K(h) + O(L^2 W log(L+1))`
`+ C_mod(2L-1,H) + O(L(m+log(L+1)))`.

All three shifts use the copied accepted code. There is no free full-width factorial inverse, omitted interpolation, or uncharged output map.

When `m/(L log(L+1)) -> infinity`, we have `W=Theta(m)` and `h=m+O(L log(L+1))`. With `a=alpha-1`, the complete upper bound becomes

`O((2L-1)h^alpha + N([L^2 log(L+1)]^a + L log(L+1)))`.

For the accepted supplied family `L=O((log N)^(4/5))`, both displayed non-product terms are `o(N log N)`. If per-address charges are included, the additional bitstream cost is `O(N log N)` under the conservative supplement, so the little-o overhead statement is specifically for the same bounded-window arithmetic model as the accepted route; it is not silently promoted to a stricter per-bit-address model.

With the prescribed Karatsuba prices, the product term is `Theta_charge(Lm^alpha)=Theta_charge(N^alpha/L^a)`, which is much larger than `N log N` for such growing `N`. The implementation proves a complete product service, but not the desired fast one. The smaller count is obtained by a precision-changing interpolation mechanism, precisely outside the fixed-precision ring-bilinear model.

### Why the near-two aggregate is insufficient on this small-L recursion

Here `n=2L-1` children have capacity `h=m+O(L log L)`. If `m` is sufficiently large compared with `L^2 log L`, their aggregate may indeed be slightly below `2N`, approaching `(2-1/L)N`. That fact alone is not a little-o result: these children have scale about `N/L`, not a balanced square-root scale.

More precisely, consider any finite, fully expanded schedule recursively using `2L(v)-1` equal-width product children at a parent capacity `v`, with

`2<=L(v)<=C(log v)^beta`, `v/L(v)<=h(v)<=v`,

above a fixed terminal threshold, with fixed constants `C` and `beta>=0`. Assume all prescribed calls are made, no children are combined or value-shortcut, and the tree terminates. The upper condition `h(v)<=v` records nonincreasing capacities; it holds eventually for this guarded construction with polylogarithmic `L` and the indicated actual sample bound. Each level increases total capacity by at least `(2L-1)/L>=3/2`. At a root capacity `N`, a child can shrink by at most `C(log N)^beta` while above threshold. Therefore every path has at least

`D=Omega(log N / log log N)`

nonterminal levels before it can reach that threshold. Summing capacities at depth `D`, and using nondecrease through every remaining finite subtree, gives leaf capacity at least

`N (3/2)^D = N exp(Omega(log N/log log N))`.

This already exceeds `N log N` even if leaves were charged only linearly. Rounding `m=ceil(v/L)` and additional guards only strengthen the capacity inequality. This is a schedule result for the explicitly stated small-L full expansion; it is not a lower bound against different parameter scales, sharing across children, or arbitrary multiplication. In particular, it does not transfer the earlier fixed-radix native potential to a different model without proof.

## 8. Completed controls and remaining research choices

The independent-oracle harness uses native integer arithmetic only for correctness controls. New production functions call the pinned backend for represented-value products, use explicit small shift/add actions, and use bounded bit streams for odd division.

Completed results:

- 8 exhaustive nonzero rank-one Hankel classifications, at lengths 1 through 8;
- 520 odd modular divisions and 14,080 checked carry transitions;
- 198 multiply-by-small controls;
- 5,410 interpolation cases, including exhaustive small coefficient cubes;
- 116 one-bit-short null-polynomial witnesses, checked at positive and negative points;
- 11 canonical factorable guard-obstruction witnesses;
- 4,996 guarded-convolution cases, including exhaustive small product cubes and arbitrary canonical `W`-bit lifts;
- 4,460 optimal six-product length-three controls;
- 12 Taylor-image rank controls;
- 156 complete Mersenne-route products, with supplied digit widths through 257 bits and every final uncarried coefficient checked.

All passed. Deterministic transcript digest:

`4538cc815349354c3cc8f3d749f15c62fd6afb6dc9bb462faee0db4f86e4941d`.

Finite tests do not establish asymptotic bounds or historical novelty. The exact proofs and declared cost model carry those claims. Independent review is still required.

The useful new split in the remaining search is now precise. A saving below the fixed-precision scalar gate must use an operation the gate excludes, such as precision changes, nonlinear digit/carry organization, or richer product objects. Ordinary integer evaluation has an exact, paid precision cost and a complete small-L schedule analyzed here. It supplies no new general fast multiplier. The odd native ring's correlated products remain an independent unresolved route, rather than being ruled out by a characteristic-two theorem.
