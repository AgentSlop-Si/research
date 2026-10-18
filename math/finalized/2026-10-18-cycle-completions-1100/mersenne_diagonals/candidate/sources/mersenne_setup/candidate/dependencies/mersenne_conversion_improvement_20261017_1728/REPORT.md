# An exact, division-free Mersenne conversion interface

17 October 2026. Fresh mathematical construction and bounded controls. No historical program was executed and no external files were changed.

## Result and precise scope

There is a constructive replacement for the attachment's division-tree input conversion and radix-power output evaluation:

1. Convert between binary chunks and redundant base-`p` coefficients by an exact modular factorial-Toeplitz shift. For `p=2^m-1`, the required polynomial shifts are just `+1` and `-1`. Only `O(log L)` extra bits are needed to handle powers of two in factorial denominators. No Pascal/Taylor triangle is materialized, and full factorial integers are never built.
2. Normalize base-`p` coefficients, when canonical digits are required, with a local exact divider. Its state is one `m`-bit remainder, and it writes every quotient limb. It uses comparisons, additions and subtractions rather than repeated long division or repeated whole-operand folding.
3. Keep redundant coefficients through the matrix convolution if desired, and reconstruct the binary result by the inverse shift and a bounded binary carry stream. Canonical base-`p^d` input/output and raw grouped convolution readout are also covered.

With `L` binary chunks, `N=Lm` padded input bits and `m=Omega(L)`, all represented arrays have `O(N)` bits. If `M(s)` is the **paid cost** of an independently supplied integer multiplication algorithm, the conversion cost is

`O(M(CN) + L M(Cm) + N log(L+1))`,

for a constant `C` determined by the fixed bound on `L/m` (an absolute constant when, for example, `m>=L`). Thus an `O(s log s)` multiplication backend yields an `O(N log N)` conversion bound, rather than the usual balanced-conversion `O(M(N) log L)` upper bound. This is an upper-bound comparison of specified constructions, not a runtime improvement over the attachment.

The delivered implementation imports no fast multiplication oracle: it supplies explicit Karatsuba recursion with shift/add leaves. Its fully instantiated conversion bound is `O(N^(log_2 3))` in this regime. It is an exact control implementation, with no claimed practical speed advantage.

**The sub-`N log N` objective is not obtained.** Each shift invokes one ordinary convolution whose packed integer arguments have `Theta(N)` bits, often more bits than the input. It also invokes `O(L)` general products on `Theta(m)`-bit values and has an explicitly charged `O(N log L)` short-factor setup. Replacing these operations by the proposed multiplier without a new, contracting construction is circular. The outstanding work is now a specified factorial-Toeplitz convolution and diagonal-scaling task, together with the attachment's matrix-transform cost; it is not an unexplained carry or radix-power bill.

Primality of `p` is unnecessary throughout. These formulas work for prime and composite Mersenne numbers alike. They do not supply a growing family of Mersenne primes or repair the separate Newton-interface compatibility restrictions from earlier work.

## 1. The local quotient/carry primitive

Let `B=2^m`, `p=B-1`, `m>=2`. Process the binary base-`B` limbs of a nonnegative integer from high to low. If the processed prefix has remainder `r`, with `0<=r<p`, and the next limb is `a`, with `0<=a<B`, put

`s=r+a`, `delta=[s>=p]`, `q=r+delta`, `r_new=s-delta*p`.

The identity

`r*B+a = r*p+(r+a) = q*p+r_new`

proves the step. Since `0<=s<=2p-1`, `delta` is zero or one, `0<=r_new<p`, and `0<=q<=p<B`. Therefore `q` is a legitimate binary quotient limb and can be written immediately. Induction gives the exact Euclidean quotient and remainder of the whole integer by `p`.

For a negative integer, divide its magnitude. If the magnitude gives `(q,r)`, return `(-q,0)` when `r=0` and `(-q-1,p-r)` otherwise. This is the exact floor-division convention needed by signed carry propagation.

All work inside a step is on `O(m)` bits. With bounded byte/bit windows for extraction and assembly, a value of `H` bits is divided in `O(H+m)` bit operations and `O(H+m)` bits of output/storage. When `H>=m`, this is `O(H)`. There is no growing Horner integer and no sequence of `H`-bit division calls. This is specialized ordinary long division, not a claim of a new number-theoretic principle.

For a raw coefficient list `c_i`, propagate `q_{i+1},a_i=divmod(c_i+q_i,p)`, starting with `q_0=0`. The invariant after position `j` is

`sum_i c_i p^i = sum_{i<j} a_i p^i + p^j(q_j + sum_{i>=j} c_i p^(i-j))`.

It proves exact normalization, including negative intermediate carries. If the represented integer is nonnegative, the final outgoing carry is nonnegative. It can be drained in the same manner.

If `|c_i|<A`, the bound `|q_i|<=A/(p-1)+2` is preserved, since floor division adds less than one to the absolute quotient. Hence the processed values have only `O(log(A+1)+m)` bits. For all conversion and convolution inputs below, coefficient height is `O(m+L+log L)`; the whole normalization, including the final tail, costs `O(L(m+L+log L))`. In the wide-digit regime this is linear in `N`. The final tail is explicitly included: at most `O(1+(m+L)/m)` digits are emitted, and their declining-width divisions sum to `O((m+L)^2/m)`, absorbed by `O(L(m+L))` for `m>=2` and `L>=1`.

Binary carry propagation is simpler: `a_i=(c_i+q_i) mod B`, `q_{i+1}=floor((c_i+q_i)/B)`, implemented by masks and arithmetic shifts. It also works with signed raw coefficients. Remaining positive binary carry is extracted in bounded windows.

## 2. Exact basis shifts with logarithmic factorial guards

For a length-`n` integer coefficient vector `a`, define

`(T_sigma a)_j = sum_{i=j}^{n-1} binom(i,j) sigma^(i-j) a_i`, where `sigma=+1` or `-1`.

This is the coefficient vector of `f(X+sigma)` for `f(X)=sum a_i X^i`. Suppose `|a_i|<2^h`. Set

`H=h+n+1`, `K=ceil(log_2 n)` (zero for `n=1`), `W=H+K`.

The hockey-stick identity gives

`|(T_sigma a)_j| <= (max |a_i|) binom(n,j+1) < 2^(h+n) = 2^(H-1)`.

It is therefore enough to compute the result modulo `2^H` and choose its centered integer representative.

Write `s(i)=popcount(i)` and `u_i=i!/2^(i-s(i))`, the odd part of `i!`. The valuation formula follows directly by counting multiples of powers of two:

`v_2(i!)=sum_{k>=1} floor(i/2^k)=i-s(i)`.

The middle equality can also be verified digit by digit from the binary expansion of `i`. Consequently `i!/2^i = u_i/2^s(i)` has at most `K` powers of two in its denominator, even though the full factorial has `Theta(n log n)` bits. In the ring modulo `2^W`, all `u_i` are invertible. Define

`A_i = 2^(K-s(i)) u_i a_i mod 2^W`,

`G_i = 2^s(i) u_i^(-1) mod 2^W`,

`J_i = sigma^i G_i mod 2^W`.

Reverse `A` and convolve it once with `J`. If the resulting convolution is `D`, then the relevant correlation is

`D_(n-1-j) = sum_{i=j}^{n-1} A_i J_(i-j) mod 2^W`.

Now compute

`R_j = G_j D_(n-1-j) mod 2^W`.

In rational arithmetic, and hence in the corresponding 2-adic congruence after clearing denominators,

`G_j A_i J_(i-j) = 2^K binom(i,j) sigma^(i-j) a_i`.

Summing proves `R_j = 2^K (T_sigma a)_j mod 2^(H+K)`. Its low `K` bits are zero. Divide **exactly by the power of two** by shifting right `K` bits, then take the centered representative modulo `2^H`. The coefficient-height bound proves that the reconstructed integer is the exact answer.

Only ordinary bounded integer residues are stored. No p-adic infinite object is allocated. No even factorial is inverted modulo a power of two. Omitting the `K` extra bits loses high result bits after division, so those guards are a correctness requirement.

### Preparing the odd factorials and their inverses

Let `o_i=i/2^v_2(i)`, the odd part of `i`. Prepare

`u_0=1`, `u_i=u_(i-1)*o_i mod 2^W`.

The multiplier `o_i` has `O(log n)` bits. Compute a single inverse `v_(n-1)=u_(n-1)^(-1) mod 2^W` by precision-doubling Newton iteration

`x <- x*(2-u*x) mod 2^t`,

starting with `x=1 mod 2` and doubling `t` to `W`. Recover every previous inverse by

`v_(i-1)=v_i*o_i mod 2^W`.

Thus there are `2(n-1)` short-factor products, one paid inversion, `2n` full-width diagonal/correlation products, and one convolution. The implementation regenerates these data per shift; no cache or free parameter table is assumed.

## 3. The bit-cost theorem, including the convolution

Assume an integer multiplication backend has bit cost `M(t)`, with standard regularity sufficient for precision doubling: `M(t)/t` is nondecreasing and `sum_j M(ceil(t/2^j))=O(M(t))`. Karatsuba and standard quasi-linear backends satisfy this. The statement below retains every use of `M` as a paid operation.

Represent all modular convolution inputs by numbers in `[0,2^W)`. Choose a byte-rounded slot width

`b=8 ceil((2W+ceil(log_2 n))/8)`.

An unreduced convolution coefficient is less than `n*2^(2W)<=2^(2W+ceil(log_2 n))`, so no coefficient spills to the next slot. Pack both length-`n` arrays in base `2^b`, perform one integer product, and extract fixed byte windows. Reduce each extracted coefficient with a mask to `W` bits. The two argument capacities are `S=nb=Theta(nW)` bits, and the full result has fewer than `2S` bits. Byte rounding and all extraction/assembly cost `O(nW)`.

The total shift cost is

`C(n,h) = O(M(S) + n M(W) + n W log(n+1))`,

where `W=h+n+1+ceil(log_2 n)` and `S=n*8 ceil((2W+ceil(log_2 n))/8)`.

The terms are, respectively:

- one same-scale exact convolution product;
- the `2n` full-width scalar products and the precision-doubling inverse;
- the short-factor prefix/reverse products, plus masks, signs, scans, bounded shifts, indexing and storage.

Short factors use elementary shift/add multiplication costing `O(W log(n+1))` each. This logarithm is real and is not suppressed. The result is valid without importing an unproved fast division routine.

The algorithm uses `O(nW)` coefficient storage plus the backend's workspace. It never constructs `n!`, an `n`-by-`n` binomial matrix, a division tree, or powers `p^(2^j)`. Pointer arithmetic can be implemented as sequential scans; even the reference implementation's bounded index arithmetic is absorbed by the displayed bound because `W>=n`.

### A fully concrete, noncircular instantiation

`fresh_conversion.py` supplies explicit Karatsuba integer multiplication. Each recursive call splits the arguments at approximately half their width, computes three smaller products, and pays for all shifts, masks, sums and differences. Calls of at most 32 bits use binary shift/add multiplication. The recursion is therefore bounded by

`M(t)<=3 M(ceil(t/2)+1)+O(t)=O(t^(log_2 3))`.

The finite 32-bit base case terminates the recursion, including the one-bit expansion of the middle product. This is an independent conventional multiplier, not the Mersenne matrix algorithm calling itself. It yields

`C(n,h)=O((n(h+n+log(n+1)))^(log_2 3))`.

The program's full-width products are routed through this implementation; the usual Python product, division, binomial and power functions appear only in independent controls. Optional global counters at every recursive Karatsuba node are disabled by default, including in the saved controls, because their growing integer updates would add a bookkeeping cost outside the arithmetic-core bound. If `collect_recursive_metrics` is explicitly enabled, its diagnostic overhead is not included in the displayed Karatsuba theorem. Outer-call, short-factor and carry metadata updates occur only at the higher-level steps and are absorbed by the displayed setup/scan bounds. The reported zero native-wide-product count concerns represented arithmetic, not small loop/index arithmetic.

## 4. Binary, redundant p, canonical p, and grouped p^d interfaces

### Binary to redundant p

Extract binary chunks `b_i` with `0<=b_i<B`, so `X=sum b_i B^i`. Since `B=p+1`,

`X=(T_+1 b)(p)`.

The returned coefficients are genuine positional coefficients at powers of `p`; they are deliberately allowed to exceed `p-1`. Their height is at most `m+L` bits. They may be stored directly in the attachment's digit matrix, provided its convolution bounds are enlarged to cover these coefficients. This changes the input certificate, so one cannot reuse the old canonical-digit bound without modification.

If canonical digits are required, apply the local quotient/carry stream from section 1. For `m=Omega(L)`, that stream costs `O(N)` and emits `O(L)` digits. Even a binary boundary value such as `2^(Lm)-1` may need one more p-digit; the implementation does not assume the counts are identical.

### Raw p coefficients to binary

For any raw signed coefficient vector `c` representing a nonnegative integer at `p`, use

`sum c_i p^i = (T_-1 c)(B)`.

Then apply signed binary carries and bounded-window assembly. Canonical p-digits are a special case. Canonical input digit convolution has coefficient height at most `2m+ceil(log_2 L)+O(1)` and length at most `2L-1`, so the same `O(M(CN)+L M(Cm)+N log(L+1))` bound applies when `m=Omega(L)`.

### Keeping carries lazy through the matrix product

If `A=T_+1 a` and `Bvec=T_+1 b`, ordinary polynomial convolution gives `C=A*Bvec`, followed by `T_-1 C`. The algebraic identity is exactly

`T_-1((T_+1 a)*(T_+1 b)) = a*b`.

Thus it is safe to delay canonical p-carries completely. With `m=Omega(L)`, redundant input height `m+L` and raw output height `2m+2L+log L+O(1)` remain `O(m)`; total materialized storage remains `O(N)`. The source's matrix convolution and its appropriate coefficient-cap proof are still required.

The identity also exposes the limitation: this is a conjugated binary convolution, not a new bilinear multiplication law. Simply canceling both shifts algebraically returns the binary route. This report does not present that cancellation as a solution to the requested Mersenne-interface problem.

### Canonical p^d

For `1<=d<=L`, first obtain canonical p-digits and group each consecutive `d` digits. To turn one group into its ordinary integer digit, apply the length-`d` inverse shift and binary carry operation. It returns a value in `[0,p^d)`. Conversely, convert each canonical grouped digit into p-digits using the same forward shift and local carries, pad to `d` positions, concatenate, and perform one global inverse shift.

These steps need neither a precomputed giant `p^d` nor ordinary division by it. A requested explicit value of `p^d` can be formed by applying the inverse shift to the vector with a single one in position `d`; its cost is charged by the same theorem. For a lone grouped digit, the implementation validates its canonical range by converting only that digit's actual binary chunks to p-digits and comparing their count with `d`; it then returns the original digit directly. Thus `d>L` does not cause an allocation of `d` zero positions. The scalar parameter itself still has to be read and compared.

In the wide-digit regime, the extra grouped work is at most

`O((L/d) M(Cdm) + L M(Cm) + N log(d+1))`,

which is absorbed by the global bound under the regularity of `M`. Partial final groups and padding add only constant factors.

### Raw grouped convolution readout

For completeness, raw coefficients at powers of `p^d` need not be normalized by repeated division by `p^d`. Convert each signed coefficient's magnitude independently into canonical p-digits, restore its sign, and add that short array at offset `jd`. Evaluate the resulting redundant p-array by the global inverse shift.

For a product of length-`G` canonical grouped inputs, a coefficient has at most `2dm+log_2 G+O(1)` bits. Under `m=Omega(Gd)`, each local conversion has `O(d)` digits, and each resulting p-position receives only a bounded number of overlapping arrays. The total local-plus-global cost is again absorbed by the preceding conversion bound. The implementation also supports smaller m correctly; the wide-digit cost statement is not asserted outside its premises.

## 5. What has improved, and what remains

Compared with the attachment, this supplies a concrete Mersenne-specific conversion interface that does not require growing-width repeated division, a recursive division tree, or multiplications by large radix powers. Compared with a direct Taylor triangle, it replaces quadratic coefficient updates by one paid modular convolution and diagonal maps. The factorial denominators cost only `O(log L)` guard bits, rather than requiring full factorials of `Theta(L log L)` bits.

This is **not** a new Taylor-shift principle: the diagonal-Toeplitz factorization is classical, and removing powers of two before inversion is classical as well. The contribution to this research chain is the combined explicit precision proof, carry/grouping interface, fresh implementation and full charge ledger for the given Mersenne task. Historical priority of this exact combination is not claimed.

The particular packed implementation still has a concrete large multiplication call. For example, the 32,768-bit boundary control at `m=256`, `L=128` creates an input-shift packed capacity of 101,376 bits. The recorded maximum actual general-multiplication argument for its round trip is 100,976 bits. This is direct evidence of the named implementation's residual multiplication cost, not a generic lower bound for conversion.

Three obligations remain before a sub-`N log N` multiplier could follow:

1. Replace or fuse the explicit factorial-Toeplitz convolution and its diagonal maps with a genuinely cheaper, fully charged method. Keeping them symbolic only moves the required evaluation to a later stage.
2. Remove the `O(N log L)` prefix/reverse short-factor setup charge if the desired target is below that scale in the `L=Theta(sqrt N)` regime. A bound expressed with an improved multiplication backend alone does not remove this independent term.
3. Close the attachment's matrix/Fermat transform schedule and point-product recursion. Linear carries and a non-triangular converter do not reduce its transform layer count.

No fixed-linear-state impossibility argument, independent-node volume theorem, or universal lower bound is used here. These are constructive upper bounds and explicit remaining operations.

## 6. Prior art and attribution

- Tang, Duraiswami and Gumerov, *Fast Algorithms to Compute Matrix-Vector Products for Pascal Matrices*, UMIACS technical report, 2004: structured Pascal matrix decompositions and fast products. [Primary institutional copy](https://drum.lib.umd.edu/items/6c219ff5-0480-4c51-8a29-f50905e7309c).
- Potter and Duraiswami, *Fast and Stable Pascal Matrix Algorithms*, 2017, section 3.2, Theorem 2: the family of diagonal-Toeplitz factorizations using `alpha^k/k!`. The shift here is the transposed version with `alpha=2`, interpreted through exact modular arithmetic. Their numerical-stability conclusions concern floating-point implementations, not these exact modular controls. [Author paper](https://arxiv.org/html/1711.08453v1#S3.SS2).
- Andreica, *A Fast Algorithm for Computing Binomial Coefficients Modulo Powers of Two*, 2013, sections 7–8: extracting odd factorial parts and separating powers of two in modular binomial arithmetic. That paper computes individual binomial coefficients with its own preprocessing; it is not cited as having proved this report's batched conversion bound. [Primary article PDF](https://downloads.hindawi.com/journals/tswj/2013/751358.pdf).
- GNU MP, *Factorial Algorithm*: odd factorial parts and final power-of-two restoration are established implementation techniques. [Official manual](https://gmplib.org/manual/Factorial-Algorithm).
- GNU MP, *Binary to Radix*: standard power-of-two extraction and division-tree nonbinary conversion. [Official manual](https://gmplib.org/manual/Binary-to-Radix).
- Fredrik Johansson, *Fast nonbinary arithmetic*, 26 February 2026, “Fast radix conversion”: multiplication- and division-based divide-and-conquer conversion both have the usual `O(M(n) log n)` bound, with different practical constants. [Author's implementation discussion](https://fredrikj.net/blog/2026/fast-nonbinary-arithmetic/#fast-radix-conversion).

The proofs in sections 1–4 are self-contained. No claim of a new asymptotic integer multiplication result depends on these references.

## 7. Fresh evidence and execution boundary

`fresh_conversion.py` is newly written standard-library-only code. The attachment and prior reports were read as text; none of their programs was run. The test program builds no NTT and makes no claim about the attachment's historical timings.

Controls cover exact signed shifts, round trips to canonical p and p^d, direct raw-p and raw-grouped-product readout, redundant/lazy product conjugation, signed quotient/remainder, exhaustive small local quotient transitions, guard/sign/carry negative controls, and the independent Karatsuba backend. Selected wide-digit round trips reach 32,768 input bits. Native integer arithmetic is used only for independent expected answers in these controls.

`CONTROL_RESULTS.json` and `RUN.log` record the fresh run. Nine additional single-group edge controls cover `d` beyond the actual digit count, `d=1,000,000`, zero, and rejection of a digit equal to `p^d`. These verify that the validation transform uses only the actual input's binary chunk count. `SOURCE_PINS.json` pins the inspected archive/text, and `MANIFEST.json` pins this deliverable. The earlier manifest is preserved verbatim in `MANIFEST.before_single_group_fix.json`, with its hash recorded in `REVISION.json`. Results are correctness evidence and exact operation/width metadata, not timing measurements or proofs inferred from samples.
