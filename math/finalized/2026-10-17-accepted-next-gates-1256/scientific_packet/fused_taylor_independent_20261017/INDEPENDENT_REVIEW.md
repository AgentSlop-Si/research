# Independent review: streamed fused Taylor producer and linear-state rank

17 October 2026. Independent mathematical and fresh-code verification.

## Verdict

**Accepted within the stated model and scope. No mathematical correction is required.**

The reviewed construction produces the specified redundant blocks without materializing the Taylor-coefficient array. Its exactness, paid bit-work upper bound, storage bound, implementation-specific quadratic lower bound, observation rank, minimum fixed-linear-state dimension, and inherited matrix recurrence are sound on their stated domains.

This is an explicit fused producer, not an asymptotic multiplication improvement. The report correctly leaves near-output-size conversion, faster paid readout, parameter selection, and the original speed objective open. No historical-priority judgment is made.

The frozen reviewed report is `../fused_taylor_producer_20261017_1205/REPORT.md`, SHA-256:

    6168f5834b69465c9c457e5f3b66a5a0653f3a9da6a771aedac9414a6f801db6

`SOURCE_PINS.json` records the reviewed report, accepted predecessor, and this review's independently written control script. No author or historical program was executed, and no external state was changed.

## 1. Exact producer and arithmetic domain

The required domain is integers `m>=2`, `K>=1`, positive `s|K`, legal chunks `0<=a_i<=p`, and `p=2^m-1`. Put `B=K/s`, `N=mK`, and `R=p^s`. Primality is unnecessary.

Define the window weight

    w_(r,i)=sum_(t=0)^(s-1) binom(i,rs+t)p^t.

Direct use of Pascal's identity gives

    w_(r,i+1)=(p+1)w_(r,i)+binom(i,rs-1)
              -p^s binom(i,(r+1)s-1).

The initialization is `w_(0,0)=1`, with all other initial windows zero. The two boundary streams have the independently checked invariant `v_i=C binom(i,j)`, with `C=1` or `R`. The zero/seed branches handle the onset at `i=j`; afterward

    v_(i+1)=v_i(i+1)/(i+1-j)

is an exact quotient. The denominator is positive and at most `K` whenever used. The `j=-1` boundary is identically zero and must be handled separately, as the report does.

Accumulating `sum_i a_i w_(r,i)` gives the exact requested `U_r` by swapping two finite sums. Recombination `sum_r U_r R^r=X` follows from the binomial theorem. No normalization or canonical-digit assumption is used. The apparent multiplication of a binomial by `R` is not hidden work: it is already present in the seed and retained by the scaled recurrence.

Terminology caution: this is not a literally division-free algorithm. It uses paid exact small-index divisions. A denominator may happen numerically to equal `p` or `p^s` for some parameters. The precise useful distinction is that it avoids radix quotient/remainder conversion of the input and divides only by the stated index denominators. The frozen report states the operations accurately and does not make the problematic literal claim.

## 2. Width and time audit

The declared capacities are

    H=ms+K+1,
    L=ceil(log2(K+1)),
    G=H+m+L+3=Theta(H).

The following bounds are sufficient and consistent:

- `binom(i,j)<=2^i` and `R binom(i,j)<2^(ms+i)` for `0<=i<K`.
- `w_(r,i)<2^(i+m(s-1)+1)`.
- Each final `U_r`, partial nonnegative accumulator, and individual contribution `a_i w_(r,i)` fits `H` magnitude bits.
- Materialized `w<<m`, the addition before boundary subtraction, and the exact-division numerator fit the padded `G` bits.
- The small-division remainder uses at most `L+1` bits.
- Constructing `p^s` by repeated shift/subtract costs `O(ms^2)` and uses `O(ms)` space. The stated `mj+1` guard for its j-th shifted temporary includes the first shift of one.

A contribution costs `O(mG)` for the chunk-by-weight schoolbook product. Each boundary update costs `O(GL)` for a short product and exact short division; materialized shifts/additions/subtractions cost `O(G)`. Thus `KB` iterations cost

    O(KB(m+L)G)
      = O((K^2/s)(m+L)(ms+K)).

The omitted-looking terms really are absorbed: `ms^2<=mK^2<=KBH`; input rereads cost `BN=KBm`; initialization and output writes are at most `O(N+BH)`. No multiplication child or fast-arithmetic oracle is used. Long division's bit cost is paid, not replaced by an operation count.

Retained input costs `N` bits; all outputs cost `BH`; the current block's streams, accumulator, numerator, temporary arrays, constants, and counters cost `O(G+ms+L)`. Since `G=Theta(H)`, total storage is `O(N+BH)`.

## 3. Quadratic-work caveat and endpoints

For the specified implementation using fixed `G`-bit arrays and `m` schoolbook rounds per chunk product, the loop costs at least

    Omega(KB mG)>=Omega((K^2/s)m(ms))=Omega(N^2).

This applies to the loop implementation for `s<K`, not to the fused mathematical map or every possible implementation. If zero windows are skipped, there are still exactly `K(B+1)/2` positive windows on the maximum input, so the worst-case lower bound remains. The report's explicit qualifier is important and correct.

- `s=1`: the output is the entire Taylor-coefficient list. The construction and ledger remain valid; the minimum linear state has dimension `K`.
- `s=K`: `U_0=X`, so the report correctly chooses an `O(N)` direct-copy branch. It does not apply the loop's quadratic lower bound to that branch. The minimum linear state has dimension one.
- `K=1`: only `s=K=1` occurs; the direct-copy and one-dimensional statements remain valid.

## 4. Independent rank proof

All claims here are over the rationals, with nonzero `p`, and therefore apply to the report's `p>=3`.

Let `J=1+z`. For `0<=h<s`, restrict `F` to degree `<K-h` and stack `E_s(J^tF)` for `0<=t<=h`. The unitriangular change between `J^t` and `z^t` leaves its rank unchanged. Write `W_t=E_s(z^tF)`. Then

    W_(t+1,r)-p W_(t,r)
      =f_(rs-1-t)-p^s f_((r+1)s-1-t).

In the kernel of the stacked map, the first-block equation forces the first boundary coefficient to vanish; proceeding block by block forces every internal-boundary predecessor to vanish. Repeating for `t=0,...,h-1` forces precisely the `h` coefficients immediately preceding each of the `B-1` internal boundaries. The top `h` coefficients are already zero by the domain restriction.

Conversely, these boundary zeros together with `E_s(F)=0` force every `W_t=0`. Consequently the stack has the same kernel as `B` block-evaluation functionals plus `(B-1)h` distinct boundary-coordinate functionals. They are independent because each block retains at least `s-h>=1` available unselected coordinates with nonzero evaluation weights. Therefore

    rank O_h=B+(B-1)h.

Equivalently, the domain has dimension `K-h`, and its kernel has dimension `B(s-h-1)`. At `h=s-1`, the stack is injective on a space of dimension `K-s+1`.

## 5. Minimum fixed linear state

If fixed rational-linear maps `S,P,L` satisfy

    E_s(F)=P S(F),
    S(JF)=L S(F) for degree(F)<K-1,

then all `s-1` transitions are degree-safe on degree `<K-s+1`. The injective lookahead map factors through `S`, proving `dim S>=K-s+1`.

The proposed matching state is valid: retain `f_0,...,f_(K-s-1)` and the final packed block. All earlier blocks decode from the retained coefficients, and degree-safe multiplication gives

    f'_0=f_0,
    f'_j=f_j+f_(j-1),
    U'_(B-1)=(p+1)U_(B-1)+f_(K-s-1).

For `s=K`, the last added coefficient is zero by convention. The missing top-boundary subtraction vanishes because `f_(K-1)=0` for the allowed transition. This attains dimension `K-s+1`.

The legal unit inputs `(1+z)^i` span the relevant polynomial spaces, so extending fixed linear identities to their rational span is legitimate. The theorem is a scalar-dimension lower bound for a fixed degree-safe linear transition and decoder. It does not exclude nonlinear, time-dependent, or final-state-only methods, nor does it itself imply a bit-volume lower bound for every possible choice of state coordinates.

The report's separate `Theta(N+K^2)` worst-case volume claim for its explicit attaining state when `1<s<=K/2` also checks: the retained prefix includes a linear number of central binomial coefficients and at least `K/2` coefficients of magnitude at least `p`. This is correctly limited to that concrete materialization.

## 6. Matrix integration

Substituting `K=dM^2`, `s=dM`, `B=M` gives

    F=O(N^2(1+L/m)(1+M/m)).

The direct matrix recurrence retains `M^2 T(H)` children, `O(M^2(H+log M))` diagonal accumulation, and `O(KN+N)` binary reconstruction. These widths and costs match the accepted redundant-block interface. No extra Taylor-coefficient or intermediate `p^d` block array is required.

The prescribed fallback when a child capacity fails to shrink is necessary and is present. The resulting recurrence makes no speedup claim; the declared producer itself already incurs quadratic worst-case work for the matrix domain `M>=2`.

## 7. Fresh controls

`independent_checks.py` was written for this review from the formulas and proofs, without importing or executing the author's script or any historical program. Exact Python arithmetic is used only as a correctness oracle, not timing evidence.

All controls passed:

- 1,108 exact rational observation-rank cases
- 2,784 signed degree-safe state-transition/readout cases
- 13,888 initial independently derived window-recurrence values
- 2,660 producer input cases
- 475,108 producer row/weight/boundary comparisons, including product-path invocations
- 423,296 exact-ratio update checks
- 756 direct scalar-copy endpoint cases, also cross-checked against the recurrence
- 72 complete matrix multiplication and binary-reconstruction cases

Tests cover exhaustive small legal inputs, zero, all-maximum, alternating and seeded-random inputs; `m=2,3,4,7,13,31`; composite `p=15`; producer cases through `K=48`; ranks through `K=18`; and all divisors in the tested ranges. Rank controls also test `p=1` as an additional nonzero-rational-base sanity check outside the report's radix domain. Scratch guards use exact `L=K.bit_length()`, including values where `K+1` is a power of two. `INDEPENDENT_RESULTS.json` preserves the counts.

No new blocker was found. The bounded fused-construction and linear-state claims are accepted; the fast-conversion and multiplication-speed gates remain open.
