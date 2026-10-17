# Independent second challenge: normalized Newton quotient and signed carry

17 October 2026. Mathematical proof review, source inspection as text, and separately authored exact arithmetic.

## Verdict and binding

**Concur with the scoped acceptance of the integral normalized quotient, its CRT-compatible integer representation, its coefficient-height bound, and its signed local carry theorem. No acceptance-changing defect was found.**

This conclusion concerns the varying-evaluation representation family. It does not establish an improved all-size FFT or integer-multiplication complexity, a fixed-evaluation or fixed-Mersenne implementation, a production speed record, or historical priority. The result remains an **unbound supplemental representation update**; no catalogue owner, route, score, or status is assigned here.

This second review binds the first intake's `REPORT.md` at SHA-256:

`6da359e76d5783f098ace085ff264193946540984b45044585b5cd67c43c04df`

The mathematics and source interfaces reviewed are described in `transfer/COMPACT_BINOMIAL_CARRY_AND_COST.md`, `compact_newton/compact_binomial.py`, `compact_newton/modular_compiler.py`, and `transfer/local_carry.py`. Supplied programs were only read. None was executed, imported, or compiled. The controls below are independent arithmetic, not a replay of the supplied programs or their recorded large-product timings.

## 1. All-r integrality survives the challenge

For integer r>=2, let

- B_j(X)=X(X+1)...(X+j-1)/j!, with B_0=1;
- D=lcm(1,...,2r);
- B_r(X)=D Z in the quotient.

The product coefficient of B_(i+j-k) in B_i B_j is

`(-1)^k binom(i+j-k,i-k) binom(j,k)`.

It is an integral multinomial coefficient of magnitude at most `3^(2r-2)` for retained indices 0<=i,j<r. For 0<=t<=r-2, the quotient reduction is

`B_(r+t) -> Z sum_(a=0)^t [D/binom(r+t,r)] binom(r+t-a-1,t-a) B_a`.

This identity follows by factoring B_r out of B_(r+t) and applying Vandermonde expansion to the remaining shifted polynomial. For each prime p, Legendre's valuation formula writes v_p(binom(r+t,r)) as a sum of terms each equal to zero or one. Terms vanish for p^a>r+t. Consequently the valuation is at most floor(log_p(r+t)), which is no larger than v_p(D). Every denominator therefore divides D, for every allowed r and t.

Writing the fold constant as f_(t,a), its first entry and successive ratio are

`f_(t,0)=Dr/(r+t)<=D`,

`f_(t,a+1)/f_(t,a)=(t-a)/(r+t-a-1)<=1`.

All fold constants are positive integers no larger than D. Since log D=O(r), the exact multiplication and fold constants have O(r) bits. The integer span of the retained basis is closed under multiplication inside the rational quotient, and is free of rank r over the polynomial coefficient ring in Z. Associativity is inherited from that quotient, not inferred from one numerical specialization.

For at most B outer blocks and digit maxima T_a,T_b, the displayed bound

`K = r^2 3^(2r-2) B T_a T_b [1+(r-1)D]`

is valid: there are at most r^2 channel pairs, B outer collisions per unrestricted coefficient, and r-1 high degrees that can fold into a retained channel. Canonical digits yield `log K=O(r+log B)`. The collision term log B is essential.

The old monic factorial witness still applies to literal monic exact-coordinate reconstruction. It does not transfer to this different quotient. Conversely, this height reduction alone makes no assertion about every possible monic-coordinate algorithm or the full cost of multiplication.

## 2. Node conditions and the capacity debit

Let L=lcm(1,...,r). For each prime power p^e exactly dividing D, let m be the largest p-power dividing L, or m=1 when p does not divide L. Then m<=r and L/m is invertible modulo p^e. The CRT residue

`k0 = -(L/m)^(-1) mod p^e`

is well-defined. Choose 0<=k0<D and set k=k0+D and P=1+kL. For j=1,...,r,

`R_j=1+kL/j`

is an integer radix. The designated factor R_m is divisible by p^e, so D divides Q=product R_j=B_r(P). This establishes the exact integer block base beta=Q/D.

The offset +D is doing useful work. It gives

`R_r/D >= L/r+1/D >1`,

and hence beta>w_(r-1), where w_j=product_(a<=j) R_a=B_j(P). Every retained weight therefore fits within a block. In general D does not divide R_r: the admissible top-digit region is a truncated mixed-radix interval. It is not a rectangular digit box with an invented integral top radix.

The elementary exponential bounds for L and D give O(r)-bit radices and `log beta=Theta(r^2)`. In particular, L>=2^(r-1), k>=D, and

`beta > D^(r-1) L^r/r! >= L^r >= 2^(r(r-1))`.

At the same point P, the monic block base is exactly

`beta_old=r!D beta`.

The capacity loss is therefore exactly log2(r!D) real-valued bits before rounding, which is Theta(r log r). Differences of integer bit lengths need not equal this nonintegral logarithm exactly. Both block capacities remain Theta(r^2), but a fair finite comparison must encode the same integers and charge their respective block counts.

This construction selects P as a function of r. It is not a proof that the same conclusions hold at an externally fixed node or modulus.

## 3. Signed carry and the one-additional-subtraction bound

The local theorem assumes integer radices at least two, integer D>=2, D|Q, and R_r>D. Start with arbitrary signed coefficients and an arbitrary signed incoming carry. Euclidean radix normalization produces

`S=q_Q Q+u`, with `0<=u<Q`.

If d is the top digit and w=w_(r-1), then `dw<=u<(d+1)w`. Define q0=floor(Dd/R_r). Since beta=R_r w/D,

`q0 beta<=u`, and `0<=u-q0 beta<beta+w<2 beta`.

Thus subtracting q0 times the prepared beta digit vector is nonnegative, lies below Q because D>=2, and can be normalized without an overflow. A comparison against the beta digit vector determines whether one further subtraction is needed. The final carry is `D q_Q+q0+e`, with e in {0,1}. This proof is independent of coefficient sign and magnitude. Euclidean, rather than truncating, signed division is important.

For original coefficient magnitudes at most U, the estimate `sum_(j<r) w_j<2 beta` gives

`|carry_out| <= |carry_in|/beta+2U+1`.

Since beta>=2, the invariant |carry|<=4U+2 holds from an initial zero carry. After the finite input ends, a nonnegative total has nonnegative final carry, and each zero block divides that carry by beta. A negative final carry exactly indicates a negative total. Rejecting it at the nonnegative array interface is consistent; the product sign must be handled separately.

Static inspection supports the claimed maximum of 3r+1 Euclidean divisions and 2r+2 multiplications per block. The online arithmetic does not form a large weighted block. Under an appropriate multiplication/division cost model its operand widths are O(H+r), where H bounds coefficient bits. This does not turn Python operation counts into a bit-complexity theorem.

## 4. Complete cost ledger: what remains to be paid

Use N=Theta(B r^2) for full input capacity, H=O(r+log B) for the reconstruction height, s auxiliary primes, b_i their bit lengths, W_i the accumulated CRT-modulus bit length after prime i, and M(n) the cost of n-bit integer multiplication. The following are conservative accounting bounds, not a newly established optimized implementation.

1. **Representation setup.** Building the integer node, large Q and beta, and the prepared carry digits uses large integers. The stated safe `O(r M(r^2))` preparation allowance does not disappear because online carries are short.
2. **Full-plan storage.** The carry-only radices and beta digits use O(r^2) bits. The current full plan also retains r growing weights, each w_j having Theta(jr) bits, for **Theta(r^3) bits in total**. This is a different storage claim. Optional direct reference multiplication tables have further costs and are not required by the modular compiler.
3. **Input reduction and kernels.** Encoded coefficients must be reduced modulo every prime. D, modular factorials, inverse factorials, fold scales, kernels, and transform roots must be prepared. Arithmetic is modular, so this does not recreate exact factorial-sized intermediates; it is still paid work.
4. **Both transform axes.** The conventional compiler has `O(r B(log(2B)+log r))` field operations per prime. In bit operations the transform portion must be summed over the actual primes, for example `O(r B(log(2B)+log r) sum_i M(b_i))` with suitable prepared modular arithmetic. Field inversions and root/prime preparation also need their appropriate costs. A smaller prime count does not erase either transform axis.
5. **CRT reconstruction.** There are O(rB) integer coefficients to reconstruct. The source uses incremental CRT with growing accumulators. A conservative accounting is `O(rB sum_i M(W_i))`, plus shared modulus and inverse preparation. A different product/remainder-tree implementation can use bounds of the form `O(rB M(W_s) log(2s))` plus setup. Neither reconstruction method is free or just one constant-time operation per output.
6. **Carry normalization.** Its conditional bound is `O(B r M(H+r))`, plus the final O(1+H/log beta) carry blocks. Preparation, conversion, and coefficient reconstruction are not included in that line.
7. **Both conversion directions.** Standard balanced binary/base-beta conversion admits conservative bounds of the form `O(M(N) log(2B))`. Converting every beta-sized binary block to or from mixed-radix digits adds `O(B M(r^2) log r)` via product trees. These are possible algorithms; the current reference instead uses repeated exact division and evaluation. A recurrence for a new multiplier must specify and pay the actual conversion algorithms, rather than silently treating an appeal to M(N) as a solved cheaper primitive.
8. **Data movement and output.** All residue arrays, accumulated coefficients, encoded digits, and the final ordinary binary answer must be read or written. Dense reconstructed coefficients alone can involve O(rB W_s) bits; all ordinary output bits must be written. This is an accounting budget, not a universal traffic lower bound for every possible implementation.

The capped trial-division prime producer is a finite-capacity reference. It does not supply an all-size prime/root construction theorem. No complete sub-N-log-N recurrence follows from this packet. These qualifications do not invalidate the representation theorem or the smaller coefficient-height bound.

For a concrete storage check, at r=128 the sum of the retained weight bit lengths is 4,404,340, versus 138,495 bits for the short radix/D/beta-digit data. At r=512 those totals are 289,778,767 and 2,267,387 bits. These are mathematical payload-bit sums, excluding language-object overhead; they are not peak process-memory benchmarks.

## 5. Fresh independent controls

All completed controls passed:

- 505 generic mixed-radix plans, including ranks 1, 2, and 3 independently of the CRT construction;
- every one of their 44,373 possible ordinary remainders u in [0,Q);
- 6,060 additional generic arbitrary-signed coefficient/carry cases;
- 5,736 exhaustive cases genuinely requiring the optional second subtraction, with no case requiring more than one under the hypotheses;
- 76 CRT constructions: every rank 2 through 64, followed by selected ranks through 512;
- 614,837 fold entries checked for integral recurrence, positivity, monotonicity, and the D bound, with direct binomial checks and denominator divisibility for every fold row;
- 608 additional signed carry cases on those CRT plans, using coefficients up to 4,096 bits;
- exact block-capacity and node divisibility checks for every constructed plan.

Two negative controls isolate meaningful hypotheses:

- With radices (6,2), D=6, beta=2, and u=5, the top-digit estimate is q0=0 while the true quotient is 2. Dropping R_r>D can therefore defeat the one-additional-subtraction guarantee. The strict inequality is sufficient, not asserted necessary in every isolated radix configuration.
- At r=2, omitting the CRT offset +D gives k0=7, P=15 and beta=10, below the retained weight 15. The offset cannot simply be deleted while retaining the stated channel-fit proof.

The finite checks corroborate the preceding all-parameter reasoning. They do not establish asymptotic speed, historical novelty, full-source replay, or the supplied large-product timing claims. An earlier oversized exploratory control was stopped without a result; only the completed bounded run is counted here.

## Disposition

Retain the normalized quotient and signed carry result at the stated scope. Retire the old monic factorial witness only as an objection to this changed representation. Keep the full mixing, prime/root production, CRT, preparation, capacity, conversion, movement, and binary-output obligations open. No external state was changed by this review.
