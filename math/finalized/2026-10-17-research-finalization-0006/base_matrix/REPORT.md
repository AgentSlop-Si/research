# A paid streamed divider for the exact grouped Mersenne radix

17 October 2026. Bounded supplemental original-route result; independent review pending.

## Decision

For the requested radix `Q=p^d`, `p=2^m−1`, there is an exact high-to-low binary-block divider using only additions, a comparison and a conditional subtraction on `m+1` bits. Cascading `d` such dividers computes the quotient and a factored remainder by `Q` in one input pass. When `dm=O(N)`, the full interface, including postpass assembly of one binary-encoded grouped remainder, has `O(dN)` bit work and `O(dm)` working state, apart from the output stream. The general cost is `O(d(N+m)+d^2m)`. It needs no generic integer multiplication, modular inverse, primality premise, or transform.

This supplies a complete cost lemma that was absent from the inspected quotient-fold and geometric-reciprocal implementations. It is an elementary specialization of positional long division, with no historical-novelty claim. It is a different algorithm, not a retroactive complexity correction to historical code.

The complete repeated-extraction converter still has worst-case `Theta(N^2/m)` bit work in the explicit full-scan grammar, for `dm<=N/4`. Grouping does not divide this work by `d`. This closes that specific converter's cost account, not the broader adaptive-base route. The full matrix/product invoice below remains noncontracting for the independently executed block-pair implementation. No faster Fourier/tensor algorithm is substituted.

No exact existing Sheet record for the 15 October original-route experiment was identified. This is an explicitly unbound supplemental review, with an empty existing-cell change proposal. It does not reopen the different archived ALG-072 record, change any score, or create a new canonical claim.

## 1. Pinned starting scope

The current repository base is commit `b8b53a98e7a85bbc9a470cd86df3664080c7704c`. The directly reread source is:

- [Finalized exact Mersenne-prime-power experiment](https://github.com/AgentSlop-Si/research/blob/b8b53a98e7a85bbc9a470cd86df3664080c7704c/math/finalized/2026-10-15-experiment-reviews/mersenne_independent_finalization/FINAL_REPORT.md), especially Sections 1–2 and 6–7. SHA-256 `9066109bce2ddfa84dbff703337afe46ed4d5b21f34431b3f9d4e9ce6b20bc3e`.
- [Its independent bounded review](https://github.com/AgentSlop-Si/research/blob/b8b53a98e7a85bbc9a470cd86df3664080c7704c/math/finalized/2026-10-15-experiment-reviews/mersenne_independent_finalization/REVIEW.md). Its exact content hash is recorded in SOURCE_REGISTER.json.

That source accepts the exact positional base and finite tests, distinguishes `Q` from `2^(md)−1`, and specifically refuses a uniformly cheap general-`d` conversion claim. Its finite conventional NTT/CRT benchmark and the full original-route speed goal are separate. No historical programs were executed, imported, or compiled in this work. Additional local reports were read as context only; they are listed with hashes in the source register and are not represented as freshly verified remote files.

## 2. One Mersenne division in a single binary-block scan

Throughout the conversion statements, `N,m,d` are integers with `N>=1`, `m>=2`, `d>=1`, and `0<=x<2^N`. The full encoder handles `x=0` directly by emitting the canonical one-element digit list `[0]`; no repeated quotient loop is needed. The cases `m=1` or `d=0` would give the invalid positional base 1 and are outside the domain.

Let `B=2^m`, `p=B−1`, `m>=2`. Read an arbitrary nonnegative integer `x` in high-to-low base-`B` chunks. Leading zero chunks are allowed. Maintain the ordinary prefix invariant

    processed prefix = p * emitted quotient prefix + r,   0<=r<p.

When the next chunk is `a`, `0<=a<B`, the new residual numerator is

    rB+a = rp+(r+a).

Put

    s = r+a,
    e = 1 if s>=p, otherwise 0,
    quotient chunk = r+e,
    next remainder = s−ep.

Since `0<=s<2p`, `e` is exactly the quotient of `s` by `p`. Further, `0<=r+e<B` and `0<=s−ep<p`. Therefore one valid quotient chunk is emitted for each input chunk, and the invariant proves exact `divmod(x,p)` for every input. The threshold is `s>=p`, including equality; changing it to a strict inequality fails, for example `p=3,r=2,a=1`.

Every transition handles at most `m+1` payload bits. In a sequential bit-array implementation it costs `O(m)` work. Input and output chunks can be scanned/copied once; no growing integer is shifted at every iteration. Total work is `O(N+m)`, including `O(m)` initialization, and the temporary remainder/quotient-chunk state is `O(m)`. For `N>=m` this is `O(N)`.

A fixed finite number of tapes suffices for this divider: store the input/output streams separately and use sequential scratch tapes for the current chunk/remainder. Each transition uses a bounded number of scans of `O(m)` cells. This is a constructive interface for this primitive, not certification of the later whole matrix algorithm on a fixed-tape machine.

## 3. A fused d-stage divider by exactly p^d

Feed the quotient chunk from the first divider directly into a second, and repeat through `d` stages. Each stage maintains its own remainder `r_j<p`; only the final stage's quotient chunks are materialized. At end of input,

    x = p^d q + sum_(j=0)^(d−1) r_j p^j.

This follows by composing the `d` exact Euclidean division identities. The residual sum is in `[0,p^d)`, so it is the unique canonical remainder by `Q=p^d`. There is no need to construct `Q` to run the stream.

For `K=ceil(N/m)` input chunks, the deliberately full-width transition ledger is exactly

    V_div = d K m.

Reading/writing the outer streams adds `O(Km)`. Storing all remainder states uses `dm` bits. Scanning the `d` states and returning to their beginning for each input chunk also costs `O(dm)`, so the same order is available with sequential state storage; a unit-cost random access assumption is unnecessary.

If the caller wants one ordinary binary-encoded grouped remainder, assemble it from the `r_j` by

    v <- (v<<m)−v+r_j

in reverse stage order. This costs `O(d^2 m)` by a direct growing-buffer implementation and outputs at most `dm` bits. It is not a free multiplication by `p^d`. Thus the fully materialized single-call interface costs

    O(d(N+m)+d^2 m)

and `O(dm)` scratch bits besides input and quotient output. The `O(dN)` headline applies when `dm=O(N)`; otherwise the displayed initialization/group-assembly terms must be used. A caller accepting the factored remainder digits can omit assembly, but a downstream consumer must pay any later assembly.

Primality is irrelevant to this positional identity. If a different application requires Mersenne primality, selecting and proving the chosen prime is separate setup. No unproved supply of growing Mersenne primes is assumed here.

## 4. Exact repeated-extraction conversion and its scope-limited cost

Fix `m,d`. Repeatedly apply the fused divider to the current quotient, emit its grouped remainder, and stop at quotient zero. This gives the full canonical `Q`-radix expansion. Write `a=log2 p`, so `m−1<=a<m` and `a>=m/2`. Let `x_j=floor(x/p^(dj))`, `n_j=bit_length(x_j)`, and `J` be the number of nonzero quotient scans.

The explicit transition volume is

    V = dm sum_(j=0)^(J−1) ceil(n_j/m).

For inputs of at most `N` bits,

    n_j <= max(0,N−jd a+1),
    J <= N/(da)+1.

Hence

    V = O(N^2/m+dN+dm).

Grouped remainder assembly costs `O(J d^2 m)=O(Nd+d^2m)`. Under `dm<=N`, these terms are `O(N^2/m+N)`. This upper bound includes the division states, quotient writes, delimiter/control scans, and each grouped output's formation. No recursive multiplication child is hidden in conversion.

For a matching worst-case lower bound **on this implementation**, choose `x=2^N−1` and assume `dm<=N/4`. For `0<=j<=floor(N/(2dm))`,

    x_j >= floor((2^N−1)/2^(jdm)),

so the corresponding nonzero quotient has at least `N−jdm−1>=N/2−1` bits. There are `Omega(N/(dm))` such scans and each deliberately executes `d` full `m`-bit state transitions per input chunk. Consequently

    V = Omega(d * N * N/(dm)) = Omega(N^2/m).

Together with the upper bound this proves `Theta(N^2/m)` worst-case bit work for this explicit full-scan converter in the stated regime. Grouping divides the number of passes roughly by `d`, but multiplies the work per pass by `d`. The new divider removes the earlier repeated-fold overhead and the geometric-reciprocal logarithmic overhead, without making the complete conversion linear.

This is not a radix-conversion lower bound. Divide-and-conquer conversion, shared passes, output-adaptive shortcuts and different digit representations are outside the lower-bound grammar. In particular a known one-group input `x<Q` can simply be copied; the lower-bound regime does not contain that shortcut for its chosen worst-case input.

For this particular converter, a strict `o(N log N)` full-conversion budget in the moderate-group regime requires `m=omega(N/log N)`. With `m=Theta(sqrt N)` and bounded `d`, its cost is `Theta(N^(3/2))`. The conclusion applies only to the fixed full-scan implementation and parameter choice. An adaptive dispatcher can change its conversion algorithm or use shortcuts; its branch and selection costs would need their own proof.

## 5. Coefficient growth, carrying and binary output remain paid

For `L` canonical `Q`-digits per input, a full nonnegative convolution has `2L−1` coefficients with

    0<=c_k<=L(Q−1)^2,
    b=ceil(log2(L(Q−1)^2+1)) = 2 log2 Q+log2 L+O(1).

Since `log2 Q=d log2 p`, grouping does not replace `b` by a constant. If the carry before a step is at most `L(Q−1)`, then

    c_k+carry <= LQ(Q−1),

so the next carry is again at most `L(Q−1)`. The accumulator needs `O(log Q+log L)` bits beyond the coefficient interface, and every divisor call sees `O(log Q+log L)` or `O(2 log Q+log L)` bits as appropriate. Using the fused divider and materialized grouped remainder gives the direct carry upper bound

    O(d L (log Q+log L)),

up to constant factors and the one final group. The final carry is below `Q` for an actual length-`L` by length-`L` product because `XY<Q^(2L)`. For fixed `d` and `m>=log L`, this carrying work is `O(Ldm)`, but for growing `d` the displayed factor is real. A hypothetical faster carry primitive must be supplied explicitly.

Grouped Horner binary reconstruction can implement each multiplication by `Q` as `d` shift/subtract steps, then add the next grouped digit. Its straightforward upper bound is `O(N^2/m+N)` for an output of `O(N)` bits in the same parameter range. It may be cheaper on short or one-group data; no universal matching output lower bound is asserted. All `2N` requested padded output bits must finally be written, at cost `Omega(N)`. Python giant shifts in the checker are not timing evidence for the streaming bit account.

## 6. Complete smaller-matrix invoice

To make a genuine smaller matrix concrete, take `L=M^2` grouped digits and `R=Q^M`. Pack consecutive groups into `M` blocks `X_i,Y_j<R`. The sparse ordinary matrix factors with nonzero first column/row multiply to

    C[i,j]=X_i Y_j,
    XY=sum_(i,j) C[i,j] R^(i+j).

This identity is elementary block schoolbook multiplication; it is not claimed as a new mechanism. Unlike a bare digit reshape, it correctly reconstructs the entire integer. It does not need isolated original-digit convolution coefficients.

The exact per-child operand width is `h=bit_length(R−1)=ceil(M log2 Q)` for these odd radices. The actual invoice is:

- `M^2` independent arbitrary integer-product children, each with width at most `h`; their aggregate one-operand width is `M^2 h=Theta(M * L log Q)`.
- Up to `2h` bits for every separately materialized block product, giving `Theta(M^2 h)` worst-case eager output volume.
- Diagonal sums `S_k=sum_(i+j=k)C[i,j]` have bound `M(R−1)^2` and width at most `2h+ceil(log2 M)+O(1)`. Direct accumulation costs `O(M^2(h+log M))` bit work.
- Input formation, its exact p^d conversion, and binary reconstruction are charged separately. One explicit output evaluator uses Horner on the `S_k` with `dM` shift/subtract steps for multiplication by `R`, then an addition. It costs `O(Nbar^2/m+Nbar)` bits, where `Nbar=ceil(L log2 Q)` is padded input capacity. This direct evaluation handles overlap/carry through ordinary integer addition; no coefficient-isolation or free quotient oracle is assumed.
- Parameter setup and all input/output movement are additional paid terms. Forming needed powers by the same repeated shift/subtract route has `O(Nbar^2/m+Nbar)` upper cost, or powers can be avoided by the stated Horner evaluator.

Thus a full explicit account has the form

    T(Nbar) <= M^2 T(h)
               + O(Nbar^2/m + M^2(h+log M) + Nbar),

for the stated independently executed child routine and elementary representation interfaces. This is an upper account, not a theorem that those upper bounds are lower bounds for every alternative implementation. When a top-level input promise is `N` arbitrary binary bits, choose enough `Q`-digits to cover `2^N`, then square-pad and charge the actual `Nbar`; using `floor(N/log Q)` digits would silently lose input coverage.

For the unrounded capacity `n=L log2 Q=M^2 w`, `w=log2 Q>1`, the unrounded child width is `h0=Mw=n/M`. Its independent-child potential is `M^2 h0 log2 h0=M n log2(n/M)`. Since `n>=M^2`, this is at least `(M/2)n log2 n`. For fixed `M>=2` its asymptotic ratio to `n log2 n` tends to `M`; for growing `M` the displayed lower bound grows. Actual child-width ceilings can only increase the child potential, while rounding the parent capacity changes it by a lower-order term. Thus these independent children do not supply a fixed strict contraction. This is a recurrence-invoice statement, not a lower bound on algorithms with a different joint product interface.

The raw child expansion is proportional to `M`, not linear in parent width with a fixed constant as `M` grows. Naming the calculation an `M`-by-`M` product does not remove its `M^2` child multiplications. Any fast bilinear matrix algorithm would change this invoice and would need its own entry/coefficient-growth, conversion and full recovery proof. None is imported here. A jointly evaluated diagonal-sum kernel, carry-aware nonlinear decoder or shared recursion remains open; this result neither supplies one nor proves one impossible.

## 7. Evidence and disposition

`fresh_controls.py` is newly authored and standalone. It checks the single-stage divider, cascades for arbitrary tested grouping factors, canonical exact base-p^d conversion/reconstruction, genuine coefficient carries and block-matrix reconstruction, coefficient/child widths, moderate-group scan ledgers and four invalid-shortcut controls. Composite Mersenne bases are included to verify that primality is not needed for these identities. `CONTROL_RESULTS.json` records the exact totals and parameter rows. Tests support the formulas; the universal statements are proved above.

The code's Python arithmetic is an exactness oracle. It is not a production kernel, proof assistant, speed benchmark, or bit/tape timing experiment. No historical test suite was executed.

Status: a bounded candidate cost lemma and exact replacement divider, pending independent review. Broader original-route faster multiplication, adaptive parameter selection, all-size prime selection when required, a contracting joint matrix/product evaluator, physical implementation, practical speed and historical novelty all remain unresolved. Existing table identifiers, histories, priorities and scores remain unchanged.
