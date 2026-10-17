# A streamed fused Taylor-to-block producer and the exact cost of linear boundary state

17 October 2026. Bounded successor to the independently accepted Mersenne packing report. This packet has not yet been independently reviewed.

## Result

Two narrower questions now have explicit answers.

1. **A fused producer exists without first producing the shifted-coefficient array.** A streamed binomial-window algorithm produces precisely the required positive, redundant `p^s` blocks. It uses only shifts, additions, schoolbook short multiplication, and exact division by integers at most `K`. With

       B=K/s, N=mK, H=ms+K+1, L=ceil(log2(K+1)),

   its fully paid bit-work upper bound is

       F(m,K,s) = O((K^2/s)(m+L)(ms+K)),

   with `O(N+BH)` storage including the input and all final output blocks. It makes no recursive multiplication calls and assumes no fast multiplication library. This is an explicit fused producer, **not a fast-enough producer**: its declared full-width schoolbook implementation performs at least order `N^2` work when `s<K`. The endpoint `s=K` is copied directly in `O(N)` work.

2. **The additional-linear-state question has a sharp answer.** For `0<=h<s`, the map retaining the packed outputs after each of the next `h` degree-safe Taylor-Horner steps has exact rational rank

       B+(B-1)h.

   Consequently a fixed linear state that decodes the packed outputs and supports every degree-safe multiplication by `1+z` needs at least `K-s+1` scalar coordinates. This minimum is attained. When `K=dM^2`, `s=dM`, `M>=2`, this is at least `K/2+1` coordinates. A few boundary coefficients support a few steps, but a fixed closed linear state cannot preserve the matrix compression across all steps.

The dimension theorem is not an arbitrary-algorithm bit lower bound. Nonlinear decoding, time-dependent weighted accumulation, direct divide-and-conquer maps that do not retain every intermediate packed state, and other factored representations remain outside it. The explicit fused algorithm in item 1 is one time-dependent escape and does not contradict item 2.

## 1. Binding, domain, and what is not repeated

The predecessor definitions and accepted width theorem were read first:

- `../mersenne_next_gate_20261017_1153/REPORT.md`
- `../mersenne_independent_20261017/INDEPENDENT_REVIEW.md`

Their hashes are recorded in `SOURCE_PINS.json`. This report does not claim the predecessor's block-volume theorem, two-term nonintertwining witness, or elementary matrix/readout invoice as new results.

The supplied parameters are integers `m>=2`, `K>=1`, and `s|K`. Set `p=2^m-1`, `b=p+1=2^m`, `B=K/s`, and `N=mK`. The legal input is

    A(x)=sum_(i=0)^(K-1) a_i x^i,   0<=a_i<=p,
    X=A(b)<2^N.

The required output remains exactly

    U_r=sum_(t=0)^(s-1) p^t sum_(i=rs+t)^(K-1) a_i binom(i,rs+t),
    0<=r<B.

Thus `X=sum_r U_r p^(rs)`. The `U_r` are ordinary nonnegative integers with overlap; they are not canonical digits. No truncation, normalization, or binary concatenation of these blocks is allowed. In the matrix specialization, `K=dM^2` and `s=dM`, so each final block combines `M` adjacent `p^d` positions without materializing those positions.

Primality of `p` is not used. No prime selection, all-size padding theorem, DFT statement, historical-priority assertion, or external publication is supplied. All parameters are already supplied, and the actual padded input capacity `N` is charged.

The model is the predecessor's explicit bit-array arithmetic model. A materialized `q`-bit addition, subtraction, shift, copy, or scan costs `O(q)`. A schoolbook product of widths `q` and `t` costs `O(qt)`. Long division of a `q`-bit numerator by a positive `t`-bit divisor can be done in `O(qt)` bit operations: scan numerator bits, maintain a `t+1`-bit remainder, and conditionally subtract the divisor. Exactness does not make division free. Signs, scratch space, table generation, input reads, counters, and output writes are included below.

## 2. Fused algorithm: stream window weights instead of shifted coefficients

For each output block define the input-independent integer weight

    w_(r,i)=sum_(t=0)^(s-1) binom(i,rs+t) p^t,

where a binomial coefficient outside `0<=j<=i` is zero. Then

    U_r=sum_(i=0)^(K-1) a_i w_(r,i).

We do not compute the individual shifted coefficients `c_j` of `A(1+z)`. We generate one output block's weight stream at a time and accumulate its weighted input chunks.

### 2.1 Exact weight recurrence

Put `R=p^s`, and introduce just two boundary streams for block `r`:

    l_i=binom(i,rs-1),
    t_i=R binom(i,(r+1)s-1).

Pascal's identity gives

    w_(r,i+1) = b w_(r,i) + l_i - t_i.                 (1)

Proof: the shifted-binomial contribution is

    sum_(t=0)^(s-1) binom(i,rs+t-1)p^t
      = p w_(r,i) + binom(i,rs-1)
        - p^s binom(i,rs+s-1).

Adding the unshifted contribution proves (1). Although (1) contains subtraction, its completed result is the nonnegative window sum by this identity. The actual implementation first materializes `b*w+l` and then subtracts `t`; no sign guess or discarded borrow is needed.

The apparent long multiplication `R*binom(i,j)` is not performed at every step. Its entire scaled stream is generated by exact small-integer ratios.

### 2.2 Scaled binomial stream without long multiplication

For a fixed `j>=0` and seed `C>=0`, maintain

    v_i=C binom(i,j).

Initialize `v_0=C` for `j=0` and `v_0=0` for `j>0`. Its update is

    if i+1<j:       v_(i+1)=0;
    if i+1=j:       v_(i+1)=C;
    if i>=j:        v_(i+1)=[v_i(i+1)]/(i+1-j).         (2)

The last quotient is exact because it is the binomial recurrence multiplied by the fixed integer `C`. The multiplier and divisor are positive integers at most `K` in every used update. The case `j=-1` is the identically zero stream and uses no division.

Use (2) once with `(j,C)=(rs-1,1)` and once with `(j,C)=((r+1)s-1,R)`. The second stream already contains the scale factor `R`, starting from the single seed `R`; it does not require a hidden multiplication by `R` later.

### 2.3 Complete pseudocode

If `s=K`, return the one block `U_0=X` by copying the input bit string. Otherwise:

    Read and retain the K m-bit input chunks.
    Construct R=p^s by s shift/subtract steps, starting with R=1.
    For r=0,...,B-1:
        w = 1 if r=0, otherwise 0
        l = binom(0,rs-1), using the zero convention
        t = R binom(0,(r+1)s-1)
        u = 0
        For i=0,...,K-1:
            u = u + a_i*w
            If i<K-1:
                w = (w << m) + l - t
                Advance l by (2), seed 1
                Advance t by (2), seed R
        Write U_r=u.

The initialization involving a binomial at zero is only a branch returning zero, one, or `R`; it invokes no general binomial routine. Each output can be written once and released, or all `B` outputs can be retained for the matrix stage. A variant processes all `r` in parallel per input chunk, retaining `O(BH)` states and reading the input only once; its bit-work order is the same. The checked implementation uses the one-block-at-a-time form.

### 2.4 Correctness

The initialization is the definition of `w_(r,0)`. Equations (1) and (2) inductively maintain all three weight and boundary values. After input indices `0,...,i` have been processed, the accumulator is precisely

    u=sum_(j=0)^i a_j w_(r,j).

At `i=K-1`, interchanging the two finite sums gives exactly the requested `U_r`. Recombining at `p^s` gives `A(p+1)=X` by the binomial theorem. No numerical approximation, residue reconstruction, inverse transform, factorial denominator, or normalization assumption enters this proof.

The only input-dependent objects apart from the original chunks are a current partial block accumulator and the finished redundant blocks. The boundary streams depend only on supplied parameters. In particular, no array of all `c_j`, no intervening array of `p^d` blocks, and no giant transform matrix is materialized.

## 3. Full integer-bit invoice

Let

    H=ms+K+1,
    L=ceil(log2(K+1)),
    G=H+m+L+3.

`G=Theta(H)` uniformly on the stated domain, because `H>=m+K+1` and `L<=K` for `K>=1`.

### 3.1 Widths, including scratch

For `0<=i<K`,

    binom(i,j)<=2^i,
    R binom(i,j)<2^(ms+i),
    w_(r,i) <= 2^i sum_(t=0)^(s-1) p^t
              < 2^(i+m(s-1)+1).

The accepted block capacity gives `U_r<2^H`. Since all summands are nonnegative, every partial `u` and every completed `a_i*w_(r,i)` also fit `H` bits.

A separately materialized `w<<m`, the intermediate sum before subtracting `t`, and the numerator in (2) are allowed the explicitly padded `G` bits. A numerator in (2) adds at most `L` bits to its stream value. The small-division remainder uses `L+1` bits. No shifted temporary is incorrectly charged only at its completed-result width.

During construction of `R`, the completed `p^j` fits `mj` bits. Its shift temporary is allowed `mj+1` bits, including the first step from one. Summing these widths gives `O(ms^2)` work and `O(ms)` live space.

### 3.2 Work per block and total

Each of the `K` contributions to one block uses:

- One `m`-by-`G` schoolbook product and a `G`-bit addition: `O(mG+G)`.
- One materialized shift, addition, and subtraction for (1): `O(G)`.
- At most two `G`-by-`L` short products and two exact short divisions for (2): `O(GL)`.
- Input chunk reads and counters: `O(m+L)`, already absorbed.

The terminal iteration omits the recurrence updates. Zero and seed cases can skip division. Charging the displayed upper bound on every iteration is safe. With `C_i` the cumulative work after `i` input chunks of one block,

    C_0=O(G),
    C_(i+1)<=C_i+O((m+L)G),
    C_K=O(K(m+L)G).

Cold initialization, all blocks, input reads, and output writes therefore give

    F(m,K,s)
      <= O(N+ms^2+BH) + B O(K(m+L)G)
       = O((K^2/s)(m+L)(ms+K)).                       (3)

For example, `ms^2<=mK^2<=KBH`, so no power-setup term is omitted from the simplification. Re-reading the retained input for each block costs `O(BN)` and is also absorbed. This construction uses no multiplication children at all, so (3) cannot be relying circularly on the multiplication algorithm being sought.

Stored input, output, constants, current weights, numerators, and counters take

    O(N+BH+G+ms+L)=O(N+BH)

bits. If outputs are streamed to the next stage, their simultaneous residency can be reduced, but their writes remain charged. The bound is within a constant factor of the accepted worst-case payload bound for the required output, even though the time bound is much larger.

### 3.3 This implementation does not clear the speed gate

For a completely specified implementation, use the fixed `G`-bit work arrays above and the usual `m` rounds of shift/add schoolbook multiplication on every `a_i*w`. There are `KB` such products, giving actual work at least

    Omega(KB*mG) >= Omega((K^2/s)*m*(ms)) = Omega(N^2)

when the fused loop is used (`s<K`). This is an implementation-specific lower bound, not a lower bound for the fused map. Skipping zero weights only changes the count by a constant factor on the maximum legal input: there are `K(B+1)/2` positive `(r,i)` windows. The scalar endpoint uses the separate direct-copy branch.

Adaptive-length arithmetic, more sophisticated short products, or a different fused method could improve (3); any such change needs a new ledger. The output-size target is not established by having output-size storage.

## 4. Exact boundary-state growth

The predecessor showed that the packed outputs alone are not a closed linear Horner state. The question here is how much extra *linear* state is sufficient and necessary.

All vector spaces and ranks in this section are over the rationals. This choice includes integer-coordinate linear implementations as a special case. Put

    JF=(1+z)F,
    E_s(F)_r=sum_(t=0)^(s-1) f_(rs+t)p^t.

Degree restrictions below guarantee that no coefficient is truncated.

### Theorem 1: exact lookahead rank

For `0<=h<s`, let `V_h` be the polynomials of degree less than `K-h`, and define

    O_h(F)=(E_s(F), E_s(JF), ..., E_s(J^h F)).

Then

    rank(O_h)=B+(B-1)h.                               (4)

#### Proof

The families `1,J,...,J^h` and `1,z,...,z^h` are related by an invertible triangular binomial change of basis. Therefore replacing `J^t` by `z^t` does not change the row space or rank.

Write `W_t=E_s(z^t F)`. Directly shifting the block window gives, for `0<=t<h`,

    W_(t+1,r)-p W_(t,r)
      = f_(rs-1-t) - p^s f_((r+1)s-1-t),              (5)

with out-of-range coefficients zero. Starting with `r=0`, (5) determines `f_(s-1-t)`, then successively determines `f_(2s-1-t)`, and so on. The last-block coefficient `f_(K-1-t)` is zero because `F` has degree less than `K-h` and `t<h`.

Thus the information in `O_h` is equivalent, by linear transformations, to:

    E_s(F),
    f_((r+1)s-j) for 0<=r<B-1 and 1<=j<=h.            (6)

Conversely, (6) and (5) generate every `W_t`, so the equivalence is two-sided. There are `B+(B-1)h` displayed functionals. They are independent: the selected boundary coefficients are distinct; in each nonfinal block at least one unselected coefficient remains because `h<s`, and its nonzero coefficient in that block's packed evaluation cannot be canceled by the other rows. The last block also has `s-h>=1` available coefficients and its evaluation has disjoint support. This proves (4). Square.

In particular, each additional step through this family requires exactly `B-1` additional scalar linear observations, until `h=s-1`. A state supporting all these lookahead outputs cannot hold merely a fixed number of boundary layers independent of `h`.

### Theorem 2: minimum fixed degree-safe linear state

Suppose `S` is a linear map from the degree-`<K` coefficient space into a `D`-dimensional rational state space. Suppose fixed linear maps `P` and `L` satisfy

    E_s(F)=P S(F)                                     for degree(F)<K,
    S(JF)=L S(F)                                      for degree(F)<K-1.

Then

    D>=K-s+1.                                        (7)

This bound is attained.

#### Lower-bound proof

Restrict the input to `V_(s-1)`, whose dimension is `K-s+1`. The degree-safe transition can be iterated `s-1` times, so

    O_(s-1)(F)=(P S(F),P L S(F),...,P L^(s-1)S(F)).

It factors through the `D`-dimensional state. But (4) gives

    rank(O_(s-1))=B+(B-1)(s-1)=K-s+1.

Therefore `D>=K-s+1`.

#### Attaining state

Put `q=K-s` and keep

    S(F)=(f_0,...,f_(q-1), U_(B-1)).                  (8)

All earlier packed blocks can be decoded linearly from their retained coefficients; the final block is already present. For a degree-safe input, `f_(K-1)=0`, and

    f'_0=f_0,
    f'_j=f_j+f_(j-1)                  for 1<=j<q,
    U'_(B-1)=(p+1)U_(B-1)+f_(q-1).                  (9)

When `q=0`, the last term in (9) is zero. These are fixed linear updates, so (8) has exactly the required `K-s+1` coordinates. Adding the next input chunk is a known addition to the constant coefficient, or directly to the final packed coordinate if `q=0`.

For `s=1`, the minimum is `K`, consistent with retaining all coefficients. For `s=K`, it is one, consistent with scalar evaluation. These endpoints need no separate impossibility claim. Square.

### Legal-input relevance

No signed polynomial is being claimed as a collision between two legal chunk vectors. If a fixed linear state and transition are correct on every legal shifted unit input `(1+z)^i`, they are correct by linearity on their rational span. Those unit inputs are legal (`a_i=1`, every other chunk zero) and form a basis of the relevant degree-limited polynomial space. This is why the rank proof legitimately constrains a purported fixed linear implementation for the legal inputs.

The lower bound counts scalar dimensions. It does not assert that an arbitrary choice of rational linear coordinates must consume `Theta(N+K^2)` bits. Different coordinates can have very different coefficient magnitudes, and a nonlinear encoding of the finite legal input set can be compact.

For the explicit attaining state (8), however, the cost is concrete. When `1<s<=K/2`, its retained ordinary coefficients have worst-case total magnitude volume `Theta(N+K^2)`: at the legal all-maximum input, the retained first `K-s` coefficients include a constant fraction of central binomial coefficients of order `K` bits and also at least `K/2` coefficients of at least order `m` bits. The upper bound follows from `K` capacities of `m+K` bits plus the one final block. This is an implementation-specific materialization fact for (8), not a new general lower bound.

### What this says about divide-and-conquer

A batched step `J^h` can use the `h` boundary layers in (6) to produce the next `h` packed states. Equation (4) gives the exact linear information cost of retaining that entire family. As the batch reaches `s-1` steps, this particular boundary-state repair expands to essentially the whole coefficient space.

A divide-and-conquer algorithm may instead compute only selected final states, change its representation at every level, or use nonlinear operations. The theorem does not say such an algorithm needs every intermediate packed state, nor that every divide-and-conquer scheme has the same rank requirement. It rules out the precise fixed-closure shortcut and gives a sharp invoice for the specified lookahead cache. No broader impossibility claim is made.

## 5. Matrix integration and paid recurrence

Set `K=dM^2`, `s=dM`, `B=M`, and `N=mdM^2`. The fused producer outputs exactly the `M` blocks required by the accepted smaller matrix interface. The `p^d` grouping is respected algebraically, and no `p^d` intermediate block array is written.

Its cost becomes

    F = O(KM(m+L)(N/M+N/m+1))
      = O(N^2(1+L/m)(1+M/m)),                        (10)

where constants absorb the harmless `+1`, and `L=ceil(log2(K+1))`. This is an upper bound for the newly supplied construction, not a fast-conversion claim.

Keeping the predecessor's directly paid outer-product matrix and binary readout unchanged gives the complete recurrence

    T(N) <= M^2 T(H)
      + O((K^2/s)(m+L)(ms+K)
           + M^2(H+log M) + KN + N),                (11)
    H=ms+K+1,  K=dM^2,  s=dM.

The two input transforms only change the constant in the first overhead term. The second term pays diagonal accumulation with the redundant block widths. The `KN` term is the accepted repeated-`p` binary reconstruction, including its one-bit shift guard. Recursive products must fall back to a paid base case if their capacity is not smaller than the parent; nothing in this packet changes that requirement. Output-product and readout work have not been declared free or removed.

The minimum fixed linear state dimension in these parameters is

    K-s+1=dM(M-1)+1,

while the desired output has only `M` coordinates. Hence a fixed linear Horner update cannot retain that coordinate compression merely by appending a small boundary cache. A genuinely different fast producer could still exist.

Equation (11) does not imply a strict `N log N` potential contraction, nor any multiplication speedup. The supplied fused implementation's quadratic scalar-product work already blocks that conclusion, independently of the still-paid product/readout interface.

## 6. Fresh controls and bounded stopping condition

`fresh_checks.py` is newly authored standard-library-only code. It was executed in this packet; no historical program or predecessor script was executed. It checks the weight recurrence, scaled boundary recurrence, agreement with an independently evaluated binomial formula, binary reconstruction, scratch-width ceilings, exact rational observation ranks, the attaining linear state, and the full `p^d`-grouped matrix path.

Completed counts in `CONTROL_RESULTS.json`:

- 2,880 producer cases, including exhaustive small legal domains
- 243,136 window-weight comparisons
- 486,272 boundary-stream comparisons
- 831 exact rational rank checks
- 2,088 degree-safe attaining-state checks
- 54 full matrix multiplication/reconstruction checks

Tests include `m=2,3,4,7,13,31`, composite Mersenne radix `p=15`, zero and maximum input, random and alternating chunks, `s=1`, `s=K`, and intermediate grouping. Ranks were checked through `K=18`; producer/product examples through `K=48`. Exact Python integers are arithmetic oracles, not timing evidence or a bit-complexity implementation. The universal results rely on the proofs above.

This bounded investigation stops with an explicit fused construction, its paid bit ledger, and a sharp obstruction for fixed linear boundary-state closure. A near-output-size fused producer, faster paid product/readout, all-size parameter selection, and the original multiplication-speed goal remain open. No external repository, canonical status, ownership, score, or priority was changed.
