# Restricted Taylor-image products: a smaller constructive guard and a linear lower bound

18 October 2026 UTC. Local research and exact controls only. No external write.

## Outcome

This package advances the actual restricted-input question left open by `mersenne_bilinear_guard_20261018_1502` and its independent review `review_correlated_precision_20261018_1515`.

Two conclusions concern the bounded binary-chunk Taylor image itself, rather than unrestricted canonical H-bit factors.

1. A height-aware, sample-only decoder uses exactly `2L-1` ordinary integer-point product samples at a provably smaller uniform precision. For `m>=2`, put `d=2L-2`, `Gamma=v2(d!)`, and `H=2m+ceil(log2 L)`. The sufficient precision is exactly

   `W_box = 2m + Gamma + delta`,

   where `delta=1` when `L>=4` is even and `m>=3`, and `delta=0` otherwise. Thus its nonnegative guard is `max(0,W_box-H)`, saving `ceil(log2 L)-delta` bits against the prior general-polynomial precision `H+Gamma` for `L>=2`. The formula is exact for the displayed sufficient height-envelope criterion; **it is not asserted to be the minimum information-theoretic guard for restricted products**.

2. Conversely, restricted products really can lose a linear number of precision bits. An explicit family of pairs of products of nonnegative m-bit length-L polynomials, even with the same left factor, has identical values at every integer at insufficient precision. The simple family proves a lower bound `(4/5)L-O(log L)` on the required uniform sample-only guard. A slightly richer, equally explicit family improves the coefficient to

   `c = (16-log2(200 sqrt(5)/27))/14 = 0.8535762332...`.

   For `L>=15` and sufficiently wide m (an explicit `m>=t` below), the minimum restricted guard is at least `c L-O(log L)`. This includes the accepted very-wide parameter regime. Translation preserves the collisions exactly.

The upper and lower bounds do not match. In particular, they do not close the restricted optimum. They show that the prior `Gamma=2L-O(log L)` upper bound can be improved by a logarithmic amount, while a logarithmic or zero guard cannot suffice uniformly on the actual restricted family.

The decoder has complete paid non-product bit cost `O(L^2 W_box log(L+1))`, the same order as the previous guarded interpolation, and storage `O(L W_box+L^3)` bits plus backend workspace. It uses a short high-part reconstruction to avoid an uncharged wide-by-large-coefficient triangular solve. All sample products use the same independently terminating, pinned Karatsuba backend. There is no general `o(N log N)` multiplier, improved product recursion, exact restricted optimum, or historical novelty claim.

## 1. Contract and inherited boundaries

Let `A(X)=sum_(i=0)^(L-1) a_i X^i` and `B(X)=sum b_i X^i`, where `0<=a_i,b_i<2^m`. Write `Q=AB` and `P(Z)=Q(Z+1)`. The Mersenne Taylor inputs are `A(Z+1)` and `B(Z+1)`; coefficient reduction modulo a requested power of two is permitted.

The final original convolution coefficients satisfy

`0 <= q_j <= M_j = tau_j (2^m-1)^2`,

`tau_j=min(j+1,2L-1-j,L)`, for `0<=j<=d=2L-2`.

They are strictly below `2^H`, where `H=2m+ceil(log2 L)`. Recovering all q_j exactly therefore supplies the accepted final convolution/carry interface. It also determines every coefficient of P modulo `2^H` by a paid forward Taylor shift, if a caller specifically requires the raw Taylor-product object.

The sample-only decoder receives the n=`2L-1` residues

`P(r-1) = Q(r) mod 2^W`, for `r=0,...,d`,

and the public parameters m,L. These must be the samples of the original chunk polynomials, as supplied by the two forward Taylor shifts at precision W. Arbitrary lifts of already truncated H-bit Taylor residues need not satisfy this height promise. If only those H-bit Taylor arrays are supplied, first recover each original chunk array by a paid inverse Taylor shift at H (the chunks are below `2^m<=2^H`), then form the forward shifts at W. This adds `2 C_mod(L,H)` to that standalone input route. The integrated route already has the original chunks and needs no such recovery. The decoder itself does not inspect operand coefficients to disambiguate the result. The actual product calls evaluate both Taylor factors at `r-1`; the first node is -1. Modular signed Horner evaluation is explicitly implemented. Alternatively, a caller with the original chunks can evaluate A and B directly at r, avoiding both forward shifts. This latter simplification is ordinary integer-point polynomial multiplication, not a Mersenne-specific speed claim.

The inherited fixed-precision ring-bilinear rank obstruction is unchanged: for `L>=3`, fixed ring-linear preprocessing/reconstruction over `Z/(2^H)` needs at least `2L` separated-input scalar products. Our decoder changes precision, removes powers of two, and selects bounded integer lifts. It is outside that model. The prior unrestricted integer-polynomial guard theorem is likewise unchanged. This package uses the additional coefficient-height promise.

All bit costs use the same bounded-window arithmetic/array model as the accepted route. An explicit address-cost supplement is given below. A homogeneous backend charge is a prescribed schedule price, not a universal runtime lower bound.

## 2. A height-box reconstruction theorem

Let an unknown integer polynomial `Q(X)=sum_(j=0)^d q_j X^j` have specified bounds `0<=q_j<=M_j`. Suppose `M_d>=1` and define

`W_box = max_(0<=j<=d) [v2(j!) + max(1,bit_length(M_j))]`.

Then consecutive samples `Q(0),...,Q(d)` modulo `2^W_box` uniquely determine every coefficient exactly. The delivered code also supports zero bounds and degree zero, with harmless one-bit conventions.

### Direct correctness proof

Recover coefficients in descending degree order. If q_t is already known for t>j, subtract those terms from the sample residues. The j-th leading forward difference of the residual is

`Delta^j Q_residual(0) = j! q_j mod 2^W_box`.

Write `j!=2^v u` with u odd. Removing v zero low bits and dividing by u modulo `2^(W_box-v)` determines q_j modulo that power. Its upper bound satisfies

`M_j < 2^(W_box-v)`,

so there is exactly one permitted nonnegative lift, namely q_j itself. Descending induction proves the result. This proves a sufficient criterion, not its necessity.

A literal wide triangular solve would introduce larger short-coefficient products than the prior interpolation bill. The next section gives an implementation with the same asymptotic non-product cost as the existing guarded service.

## 3. Two-scale decoder with all arithmetic paid

Put `Gamma=v2(d!)` and `b=W_box-Gamma>=1` for the convolution envelope.

### Wide low part

Apply the pinned, accepted consecutive interpolation routine with output precision b and input precision `b+Gamma=W_box`. This returns

`r_j = q_j mod 2^b`.

Its finite differences, divisions by odd factorial parts, and Newton-to-monomial conversion are all explicitly implemented in the pinned source. Its cost is `O(L^2 W_box log(L+1))`.

Evaluate `R(X)=sum r_j X^j` at the same n nodes modulo `2^W_box`, using explicit multiply-by-small Horner actions. For each node form

`s_r = ((Q(r)-R(r)) mod 2^W_box) / 2^b`.

The canonical numerator has b zero low bits. Therefore s_r is exactly the sample, modulo `2^Gamma`, of

`U(X)=sum u_j X^j`, where `u_j=floor(q_j/2^b)`.

The bounds become `0<=u_j<=floor(M_j/2^b)<L`. In particular, these unknown high parts are only `O(log L)` bits each, independent of m.

### Short high part

All following sample arithmetic has width Gamma=`O(L)`. Build the table

`F_(j,k)=Delta^k X^j(0)=k! S(j,k) mod 2^Gamma`,

without a large-coefficient multiplication. Starting at `F_(0,0)=1`, use

`F_(j,k) = k [F_(j-1,k)+F_(j-1,k-1)] mod 2^Gamma`.

Each multiplier k has `O(log L)` bits and is realized by shifts/adds. Compute the leading differences D_k of the short samples once. Descend j from d to zero. After already recovered terms have been removed,

`D_j = j! u_j mod 2^Gamma`.

The height criterion implies `u_j<2^(Gamma-v2(j!))`. Divide the canonical residue by its known power of two and then by the odd factorial part, obtaining the exact u_j. At zero remaining precision, the bound forces u_j=0; no division is made. Update every `D_k`, k<=j, by subtracting `u_j F_(j,k)` modulo `2^Gamma`. The multiplier u_j is below L, so every update is another declared multiply-by-small action. Finally return `q_j=r_j+2^b u_j`.

The proof is descending induction on the residual polynomial. No recovery table search, oracle, floating arithmetic, or uncharged wide product is used.

### Cost and storage

- Wide low-part interpolation: `O(L^2 W_box log(L+1))`.
- n residual Horner evaluations: `O(L^2 W_box log(L+1))`.
- Short Stirling-difference table and updates: `O(L^2 Gamma log(L+1))`.
- Short differences: `O(L^2 Gamma)`.
- Odd factorial parts have `O(L log(L+1))` bits. At most `O(L Gamma)` one-bit division steps cost `O(L^2 Gamma log(L+1))` in total. Their preparation has no larger cost.
- Coefficient bounds can be built without a wide square using `(2^m-1)^2=2^(2m)-2^(m+1)+1`, followed by multiplication by tau_j through short shifts/adds.
- All input, output, low-part, tail, carry, and temporary buffers are charged.

Since `Gamma=O(L)` and `W_box>=Gamma+1`, the total non-product time is

`O(L^2 W_box log(L+1))`.

The wide arrays cost `O(LW_box)` bits. The explicit short table costs `O(L^2 Gamma)=O(L^3)` bits, and the stored odd parts cost `O(L^2 log(L+1))`, absorbed in that term. Thus storage is `O(LW_box+L^3)` plus backend workspace. No `O(LW_box)`-only claim is made without a condition such as `W_box=Omega(L^2)` or a different storage schedule.

## 4. Exact closed form of the sufficient convolution-envelope precision

Assume m>=2. Let `d=2L-2`, `Gamma=v2(d!)`. For the envelope M_j above,

`W_box=2m+Gamma+delta`,

where delta is one precisely when L is even and at least four, and m>=3.

For L=1 the formula is immediate. For L>=2, the leading coefficient bound is `(2^m-1)^2`, which has exactly 2m bits. It supplies the lower bound `W_box>=2m+Gamma`.

Write `j=d-k`. Then `tau_j<=k+1`. Let

`V_k=v2(d!/(d-k)!)`.

We claim `V_k>=ceil(log2(k+1))` except possibly when k=2 and d is 2 modulo 4. For k=0,1 this is immediate because d is even. For k=2, it is exactly the stated exception. For k=3, the two even factors d and d-2 include one multiple of four, giving valuation at least three. For k>=4, divisibility of a product of k consecutive integers by k! gives `V_k>=v2(k!)`; the elementary inequality `v2(k!)>=ceil(log2(k+1))` holds for k>=4 (check 4 through 7 directly and use `floor(k/2)>=ceil(log2(k+1))` for k>=8).

Because `M_(d-k)<(k+1)2^(2m)`, all nonexceptional indices contribute at most `2m+Gamma`. At the exceptional index k=2, the contribution is at most one bit larger. It exists with tau=3 exactly when L>=4 is even. If m=2, `3(2^m-1)^2=27` has five bits, so even this index contributes only `2m+Gamma`. If m>=3, `3(2^m-1)^2` has exactly `2m+2` bits, making the contribution exactly `2m+Gamma+1`. This proves the formula.

The general arbitrary-polynomial service used W_old=`H+Gamma`. Hence the saving is `ceil(log2 L)-delta`. This is an actual exact-recovery precision improvement on the promised restricted image, not an optimality claim. Exhaustive small controls demonstrate that still smaller sample widths can be sufficient on actual product sets.

## 5. Explicit lower bounds on the restricted image

### General witness family

Choose integers `a>=1`, `0<=b<=a` such that

`D=5a+3b <= 2L-2`, and `2(a+b)<=L-1`.

Let

`R(U)=(U-1)^a(U+1)^b`,

`C=max absolute coefficient of R`, `t=bit_length(C)`, and assume `m>=t`.

Write R as the difference of its nonnegative coefficient parts `R_+-R_-`. Put `A=3a+b` and choose `s=min(A,L-1)`. The degree assumptions ensure that each of

`F(X)=2^(m-1) X^s`,

`G_+(X)=2^(m-t) X^(A-s) R_+(X^2)`,

`G_-(X)=2^(m-t) X^(A-s) R_-(X^2)`

has degree at most L-1 and every coefficient in `[0,2^m)`. Both candidate products share the same F. Their difference is

`F(G_+-G_-)=2^e X^A (X^2-1)^a (X^2+1)^b`,

where `e=2m-1-t`.

For an even integer x, x^A contributes valuation at least A, and the other factors are odd. At x=2 its valuation is exactly A. For an odd x, `x^2-1` is divisible by eight and `x^2+1` has valuation exactly one, giving valuation at least `3a+b=A`. Thus the exact uniform 2-adic fixed divisor of the displayed difference is `2^(e+A)`. The value at x=3 also attains that valuation.

The two products are distinct modulo `2^H`: their difference has leading coefficient `2^e`, which is nonzero modulo `2^H`. Yet they agree at every integer sample modulo `2^(e+A)`. Translation `X=Z+1` gives the same collision for the actual Taylor products at every integer z. Because the Taylor map is invertible modulo `2^H`, their required Taylor coefficient vectors still differ.

Therefore the minimum uniform nonnegative sample-only guard G for the restricted family satisfies

`G >= max(0, 3a+b-t-ceil(log2 L))`.

The inequality includes nonlinear reconstruction, arbitrarily many finite integer nodes, and adaptive integer-node selection. It does not include reading operand coefficients, evaluation at infinity, derivative samples, extension-ring nodes, or other auxiliary information. No assertion is made about lower bounds for arbitrary multiplication circuits.

### Simple `(4/5)L-O(log L)` family

Take b=0 and `a=floor((2L-2)/5)`. The degree requirements hold whenever a>=1. Here `C=binomial(a,floor(a/2))`, so `t<=a+1`. The guard lower bound is at least

`2a-1-ceil(log2 L) = (4/5)L-O(log L)`.

All original chunks remain bounded by 2^m. This is not the prior unrestricted H-bit rising-factorial construction.

### Improved coefficient `0.8535762332...`

For L>=15 choose `s=floor((L-1)/14)`, `a=5s`, `b=s`. Then D=28s and the remaining degree condition is automatic. We bound the largest coefficient C of `(U-1)^(5s)(U+1)^s` by its maximum modulus on the unit circle. A coefficient is a Fourier average and is therefore at most that maximum. With U=`exp(i theta)`, the maximum is

`[2^6 (5/6)^(5/2) (1/6)^(1/2)]^s = (200 sqrt(5)/27)^s`.

(The maximum of `sin^5(theta/2) cos(theta/2)` occurs at squared sine 5/6.) Thus

`t<=s log2(200 sqrt(5)/27)+1`.

The exact witness bound gives

`G >= (16-log2(200 sqrt(5)/27))s -1-ceil(log2 L)`.

Since s is the floor of `(L-1)/14`, this is `cL-O(log L)` with the constant stated in the outcome. One may use the exact integer C to obtain a stronger finite bound. The supplied witness records do so. The condition m>=t is explicit and is eventually satisfied by every accepted family with `m/(L log(L+1))->infinity`.

This lower bound and the height-envelope upper bound leave a substantial gap. They establish linear-order restricted guard necessity, not the exact leading constant or minimum guard.

## 6. Complete Mersenne-route bill and remaining obstruction

The implemented route extracts chunks, computes the two accepted forward Taylor shifts at W_box, evaluates at nodes -1 through d-1, makes exactly n=`2L-1` sample products, runs the two-scale decoder, and carries the resulting exact original coefficients in radix `2^m`.

Let K(w)=`O(w^alpha)`, `alpha=log2 3`, be the pinned terminating backend. The actual sample operand capacity obeys

`h <= min(W_box, m+ceil(log2 L)+(L-1)ceil(log2(2L-2)))`

for L>=2, and h=m at L=1. This follows from `A(r)<2^m L(2L-2)^(L-1)` and the identity `A(Z+1)|_(Z=r-1)=A(r)`. Reducing modulo `2^W_box` cannot enlarge a nonnegative value. The code verifies the supplied h bound in counted controls.

The complete cost is

`2 C_mod(L,W_box) + (2L-1)K(h) + O(L^2 W_box log(L+1) + L(m+log(L+1)))`.

The last term pays all final coefficients, carry transitions, terminal tail, and complete binary output. The inverse Taylor operation is fused into height-aware reconstruction from the shifted sample nodes; there is no omitted inverse-shift bill. If a raw Taylor-product output is required, add a paid `C_mod(2L-1,H)` forward shift of the recovered q_j. It is then returned modulo `2^H`. If the inputs consist only of H-bit Taylor arrays, also add the two input-recovery inverse shifts described in Section 1. The implementation here deliberately exposes the final-only interface and does not label it a generic ring convolution service.

In the accepted very-wide regime, W_box=`Theta(m)`, h=`m+O(L log(L+1))`, and N=Lm. The bound simplifies to

`O((2L-1)h^alpha + N((L^2 log(L+1))^(alpha-1) + L log(L+1)))`.

For the accepted small-L choices, the non-product terms can again be `o(N log N)` in the declared model. The prescribed product charge remains `Theta_charge(N^alpha/L^(alpha-1))`. Reducing a logarithmic number of guard bits does not change that conclusion. The already accepted fully expanded small-L recursion obstruction continues to apply when no calls are shared or combined. This package does not propose independent slabs, import a faster backend, or claim that this finite precision improvement breaks that obstruction.

Address supplement: the wide and short odd divisions perform `O(LW_box+L Gamma)` one-bit iterations. Charging an additional `O(log(LW_box+L^3))` for each explicit address yields a possible `O(LW_box log(LW_box+L^3))` supplement, plus indexed table-loop charges. The little-o overhead statement is not promoted to that stricter model. As in the accepted implementation, Python object allocation or timing is not the arithmetic-cost model.

## 7. Evidence, provenance, and review boundary

`restricted_guards.py` is the new implementation. `exact_controls.py` uses independent direct polynomial arithmetic only as a correctness oracle, including factor and full-integer products. Production represented-value multiplication goes through the pinned backend; every other production multiplication is explicit multiplication by a declared short integer.

The copied accepted helper files are byte-identical and hash-pinned. The original candidate and review directories were not edited. The report's scope retains the review's correction: the old general guard is sharp for arbitrary degree-bounded integer polynomials and for sufficiently wide unrestricted canonical factors, not universally for all small-width product families.

The controls include closed-form precision checks, arbitrary coefficient-box reconstruction, exhaustive actual bounded products, exact sample-product counts, complete Taylor-route products with carries, explicit all-integer null witnesses and finite residue-function distinctions, and exhaustive minimum-information sample widths on small families. See RESULTS.json and WITNESSES.json for exact counts, witness arrays, and the deterministic digest.

A first harness run found an omitted zero-width statistics field, not an arithmetic failure. That log is retained as INITIAL_CONTROL_FAILURE.stderr; the field was repaired before the complete replay. Finite controls supplement the proofs and do not prove asymptotic costs or novelty. This package requires independent review before being labeled accepted.
