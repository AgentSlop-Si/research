# Independent review: streamed Mersenne division and base conversion

17 October 2026

## Decision

ACCEPT the exact division/cascade identities and the stated bounded implementation-cost theorem in the final report "A paid streamed divider for the exact grouped Mersenne radix," SHA-256 `65e790f2716a467e45994629e25fee5855592377be94d6dcf7f3dde7eff3fee3`.

The accepted domain is integer `N>=1`, `m>=2`, `d>=1`, `0<=x<2^N`. The complete converter's worst-case `Theta(N^2/m)` claim applies only to the deliberately full-width scan grammar and the regime `dm<=N/4`. The conversion upper bound and reconstruction upper bound apply in the stated `dm<=N` regime. There is no lower bound for arbitrary radix-conversion algorithms, no unconditional prime-supply assertion, and no integer-multiplication speedup theorem.

Two wording corrections requested during this review are present in the accepted version:

1. The opening distinguishes the factored remainder emitted by the one-pass cascade from subsequent binary remainder assembly. The materialized-interface `O(dN)` shorthand is restricted to `dm=O(N)`; its general bound is displayed.
2. Positive integer parameter domains and the canonical zero output `[0]` are explicit. Bases `p=1` or `Q=1` are excluded.

## Independent identity proof

Set `B=2^m` and `p=B-1`. At a division step, the incoming remainder satisfies `0<=r<p`, and the next input block satisfies `0<=a<B`. Therefore

    rB+a = rp+(r+a),
    0<=r+a<=2p-1.

With `e=1` exactly when `r+a>=p`, put `c=r+e` and `r'=r+a-ep`. Then `0<=c<B`, `0<=r'<p`, and `rB+a=pc+r'`. Appending `c` to the quotient stream therefore preserves the exact prefix invariant. Equality at the comparison threshold requires correction. The input's partial top binary block may be left-padded; leading zero blocks do not affect the proof.

Apply this divider to successive quotient streams. After `d` stages the exact identities telescope to

    x=p^d q + r_0+p r_1+...+p^(d-1)r_(d-1).

All `r_j` lie in `[0,p)`, so the residual is nonnegative and strictly below `p^d`. It is the unique Euclidean remainder. The identities hold for composite `p` as well as prime `p`; no field arithmetic is involved. With `m=1`, division by one exists but the quotient is unchanged, so repeated extraction cannot define the claimed positional conversion. Likewise `d=0` gives invalid positional base one.

## Independent bit-cost review

The primitive uses a constant number of full scans of `O(m)` bits per transition. A streaming bit-array implementation avoids repeated growing-integer shifts. On `K=ceil(N/m)` blocks, a full-width `d`-stage cascade has transition volume `dKm`; sequential traversal and reset of the `dm` state bits add the same order. The current chunk and scratch state use `O(dm)` bits, excluding input and output storage. This requires no unit-cost random access.

A binary materialized remainder is assembled by reverse Horner evaluation, using `(v<<m)-v+r_j`. The intermediate widths grow at most linearly with stage count, so direct assembly costs `O(d^2m)`. Consequently the fully materialized division interface is

    O(d(N+m)+d^2m),

with `O(dm)` scratch space. Under `dm=O(N)`, this is `O(dN)`. Factored remainders alone need no assembly, but later consumers must pay it if needed. For extremely large `d`, the general formula, initialization and output representation cannot be discarded.

For repeated grouped extraction, let `a=log2 p`, so `m/2<=m-1<=a<m`. The number of nonzero quotients is `J=O(N/(dm)+1)`. Each quotient bit length is at most `N`, and the exact full-width volume is

    V=dm sum_j ceil(n_j/m).

Summing the shrinking lengths yields `O(N^2/m+dN+dm)`. Group assembly adds `O(Nd+d^2m)`. For `dm<=N`, the total is `O(N^2/m+N)`. Delimiters, stream movement and quotient writes are bounded by the same full scans.

For the lower bound, take `x=2^N-1` and `dm<=N/4`. For `0<=j<=floor(N/(2dm))`, division by `p^(dj)` leaves at least the quotient obtained by division by `2^(jdm)`. Thus there are `Omega(N/(dm))` scans whose inputs have `Omega(N)` bits. The declared grammar charges all `d` full-width states on every block, so each such scan costs `Omega(dN)`. Their product is `Omega(N^2/m)`. Together with the upper bound, this proves the claimed worst-case `Theta` for this implementation.

This lower bound does not extend to a one-group copy shortcut, omitted zero states, shared/divide-and-conquer conversion, a different digit representation or any unrestricted algorithm. Also, an unqualified bound `Theta(N^2/m)` cannot hold uniformly when `m` is much greater than `N`, because merely reading an arbitrary `N`-bit input already costs `Omega(N)`.

Canonical grouped Horner reconstruction uses `O(N/m+d)` shift/subtract steps, each on at most `O(N+dm)` bits, plus grouped-digit additions. In the stated regime this gives `O(N^2/m+N)`. The author correctly claims only an upper bound. Finally writing a requested padded output incurs its linear output cost. Zero and short inputs may take less work than the worst case.

## Carry and matrix sanity checks

The nearby carrying account is consistent: `c_k<=L(Q-1)^2` and a carry bound `L(Q-1)` give `c_k+carry<=LQ(Q-1)`; division returns a carry bounded by `L(Q-1)`. Materialized division on these widths costs `O(dL(log Q+log L))` over the coefficient sequence. For an actual length-`L` by length-`L` product, its final remaining carry is below `Q` because the product is below `Q^(2L)`.

The elementary matrix/block identity and its potential observation also check algebraically. With `L=M^2`, `R=Q^M`, `C[i,j]=X_iY_j`, one has `XY=sum C[i,j]R^(i+j)`. Since odd `R>1` is not a power of two, `bit_length(R-1)=ceil(M log2 Q)`. These are `M^2` independently executed products; their widths cannot be replaced by constant-cost matrix entries.

For unrounded capacity `n=M^2w`, `w=log2 Q>1`, child width `h0=n/M` gives potential

    M^2 h0 log2 h0=M n log2(n/M)>=(M/2)n log2 n,

because `n>=M^2`. The fixed-`M>=2` ratio tends to `M`; the growing-`M` lower bound grows. Ceiling effects do not produce an asymptotic fixed strict contraction. This validates the report's recurrence-invoice observation, not a lower bound against joint/shared product algorithms. No separate claim about prior art, optimal matrix kernels or FFT methods is made here.

## Fresh independent evidence

Both verifier programs in this packet were authored independently for this review. No author-supplied or historical research program was run, imported or compiled. Python integer arithmetic is used as a correctness oracle, not as timing evidence for a bit-array implementation.

`fresh_verify.py` reports:

- 1,396,052 exhaustive single-step remainder/block transitions
- 46,221 exact single-division checks
- 7,429 grouped conversion/reconstruction checks
- 1,165 sequential scan-cost cases
- Composite `p=15`, zero, boundary values, widths through 2,048 bits and large grouping parameters

Its large-`d` controls deliberately use an independently designed unpadded top-group shortcut. They verify the identities outside the lower-bound regime and are not presented as tests of the author's deliberate all-state scan grammar.

`fresh_cascade_verify.py` separately tests the author's precise all-state cascade grammar and reports:

- 49,800 exact cascade divmods
- 648 complete grouped conversions and reconstructions
- 243 worst-case cost rows satisfying `dm<=N/4`

All controls pass. The last set's transition-volume ratio to `N^2/m` ranges from approximately 0.5083 to 0.9375. These finite ratios support the implementation ledger; the symbolic argument above establishes the asymptotic statement.

## Final scope

The accepted result is a complete paid account for an explicit specialized long-division converter, together with the elementary independently evaluated block-product invoice. Broad faster multiplication, optimized implementations, adaptive dispatch, all-size Mersenne-prime selection and joint product kernels remain unresolved. This review authorizes no spreadsheet score change and makes no external publication action itself.
