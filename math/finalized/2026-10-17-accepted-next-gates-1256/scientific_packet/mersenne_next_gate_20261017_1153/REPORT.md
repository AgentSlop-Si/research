# Division-free Taylor packing for the Mersenne route: actual width and a missing fused transition

17 October 2026. New bounded candidate lemma and complete elementary invoice. Independent review is still required.

## Result

There is a genuinely different exact representation path from the previously reviewed repeated-divider and balanced-divider conversions: use `2^m=p+1` to Taylor-shift the binary-chunk polynomial, then pack its coefficients into powers of `p`. It uses no division in its input conversion. Its coefficients are **redundant, noncanonical integers**, not radix digits.

For `K` binary chunks of `m` bits each, and any divisor `s` of `K`, the exact worst-case total actual magnitude-bit volume of the resulting `K/s` separately materialized `p^s` blocks is

    Theta(mK + K^2/s).

The single input `X=2^(mK)-1` attains every block's maximum simultaneously. This is therefore a worst-case actual-output-size statement, not just a sum of incompatible fixed-buffer maxima. Under the smaller-matrix parameters `K=dM^2`, packing directly to `M` blocks (`s=dM`) gives `Theta(N+dM^3)` bits, where `N=mK`. Materializing the intervening `p^d` blocks first costs `Theta(N+dM^4)` bits. Dimensional compression can avoid that intermediate volume only if a fused producer is actually supplied.

A second exact lemma identifies why an especially simple fused producer fails: for `1<s<K`, the packed map does not intertwine polynomial multiplication by `z+1` with any linear map on only those packed blocks. A two-term witness proves this. It does not rule out nonlinear, factored, or time-dependent methods.

The full elementary construction below is correct but does not establish a faster multiplication algorithm. Its Horner Taylor shift already has a paid `O(K^2(m+K))` upper bound, and its stated full-width implementation costs that order; output reconstruction costs `O(NK)`. The precise successor gate is a faster fused producer **and** a fully paid product/readout interface. Neither a general DFT speedup nor a worldwide-new algorithm is claimed.

## 1. Source binding and novelty boundary

Latest inspected `AgentSlop-Si/research/main`: `7e13f9ff8c4f8bdd64d5068fcdc7ce03342078cb`. Four prior reports were retrieved at that immutable commit and preserved in `sources/`; exact paths and Git blob IDs are in `SOURCE_PINS.json`:

1. The finalized 15 October exact Mersenne-prime-power experiment.
2. The accepted grouped streamed-divider account.
3. The balanced conversion account with its `Theta(N^2/m)` full-scan cost.
4. The joint diagonal-sum account with its `2M-1` full-coefficient bilinear rank and fixed-capacity child-potential obstruction.

This report does not repeat those facts as new discoveries. It changes the input representation to a positive, redundant Taylor-shift representation, proves its width cost, and identifies a failed closed-linear-state shortcut. The chosen polynomial shift is classical. FLINT's official documentation describes Horner, divide-and-conquer, and convolution Taylor-shift routines. Its word-modular single-convolution routine requires a prime modulus at least the polynomial length; its ring-operation complexity is not an integer bit-complexity oracle for the representation here. Official source documentation was read on 17 October 2026:

- https://raw.githubusercontent.com/flintlib/flint/main/doc/source/gr_poly.rst
- https://raw.githubusercontent.com/flintlib/flint/main/doc/source/nmod_poly.rst

No FLINT routine is invoked or credited as a new speedup. The specialization and proof below are self-contained. This is not an exhaustive historical-priority search. No historical or uploaded script was executed, and no external state was changed.

## 2. Model and exact representation

We study exact multiplication of two arbitrary nonnegative integers `X,Y<2^N`. The input and requested output are ordinary binary bit strings. Additions, subtractions, copying and shifts that materialize a `b`-bit object cost `O(b)` bit operations. A recursive call on operands of at most `h` magnitude bits is charged `T(h)`, with signs, preparation, coefficient storage and decoding charged separately. We do not count an arbitrary-precision arithmetic instruction as unit work. This is a bit-array arithmetic account, not certification of a particular fixed-tape implementation.

This problem is separate from computing the DFT of arbitrary real, complex or field-valued vectors. No DFT circuit, numerical-precision contract, or Fourier lower bound is inferred from this integer representation.

Fix integers `m>=2`, `K>=1`, and put

    b=2^m, p=b-1, N=mK,
    X=sum_(i=0)^(K-1) a_i b^i, 0<=a_i<=p,
    A(z)=sum_i a_i z^i.

The integer `p` need not be prime for any theorem here. A version requiring Mersenne primes still owes prime selection/certification and an all-size parameter argument. We do not assume an infinite or sufficiently dense supply of Mersenne primes.

Define the exact Taylor coefficients

    C(z)=A(z+1)=sum_(j=0)^(K-1) c_j z^j,
    c_j=sum_(i=j)^(K-1) binom(i,j) a_i.

All `c_j` are nonnegative, and `X=C(p)`. For a positive divisor `s|K`, set `B=K/s`, `R=p^s` and

    U_r=sum_(t=0)^(s-1) c_(rs+t) p^t, 0<=r<B.

Then, exactly,

    X=sum_(r=0)^(B-1) U_r R^r.

The `U_r` can exceed `R-1`. Treating them as canonical base-`R` digits, truncating to `sm` bits, or concatenating their binary strings would be incorrect. No carries have been discarded. Overlaps are retained in the displayed integer sum. Apply the same map to `Y` to obtain `V_r`.

For zero, every coefficient and block is zero. Define the magnitude bit length `ell(0)=0` and `ell(u)=floor(log2 u)+1` for `u>0`. A concrete encoding can use a one-bit zero marker; doing so adds at most `B` bits and does not change any bound. Length/framing and index metadata can be represented by self-delimiting lengths or paid fixed-capacity layouts; they add at most a constant factor to the displayed payload orders. Input padding is explicit: an arbitrary `n`-bit promise can use any chosen `m,d,M` with `N=mdM^2>=n`; the recurrence must be charged at that actual `N`, and an end-to-end theorem must control `N/n`.

## 3. Simultaneous maximum and actual-volume theorem

### Theorem 1

Let

    W_s(a)=sum_(r=0)^(B-1) ell(U_r).

Uniformly for `m>=2`, `K>=1`, and `s|K`,

    max_(a in {0,...,p}^K) W_s(a) = Theta(mK+K^2/s).

Every `U_r` attains its maximum at the same vector `a_i=p`. At that vector

    c_j^*=p binom(K,j+1),
    U_r^*=p sum_(t=0)^(s-1) binom(K,rs+t+1)p^t.

### Proof

All coefficients of the map from `a` to every `U_r` are nonnegative integers. Increasing any input coordinate cannot decrease any output. Therefore `a_i=p` maximizes all blocks and hence their bit-volume simultaneously. The hockey-stick identity gives `c_j^*=p sum_(i=j)^(K-1)binom(i,j)=p binom(K,j+1)`.

For the upper bound, `c_j<=p 2^K`. Hence

    U_r <= p 2^K (p^s-1)/(p-1)
        < (3/2) 2^K p^s
        < 2^(K+ms+1),

because `p>=3`. A safe uniform magnitude capacity is `H_s=ms+K+1`. Thus

    W_s(a) <= (K/s)(ms+K+1)
            <= mK+2K^2/s.

For a lower bound at the simultaneous maximizing input, the highest term of each group has `c_(rs+s-1)^*>=p`, so `U_r^*>=p^s`. Therefore

    W_s(a^*) >= K log2 p >= K(m-1) >= mK/2.

For `K>=8`, consider indices `j` with `ceil(K/4)<=j+1<=floor(3K/4)`. There are at least `K/2-1>=3K/8` of them. Put `t=floor(K/4)`. Monotonicity and symmetry of binomial coefficients, together with

    binom(K,t) = product_(i=0)^(t-1) (K-i)/(t-i)
                >= (K/t)^t >=4^t >=2^(K/2-2),

give `binom(K,j+1)>=2^(K/4)` on this interval. Each group intersecting it consequently has `ell(U_r^*)>=K/4`. A group contains at most `s` indices, so at least `3K/(8s)` groups intersect the interval. Therefore

    W_s(a^*) >=3K^2/(32s).

Combining this with the `mK/2` bound gives, for example,

    W_s(a^*) >= (3/64)(mK+K^2/s).

For `1<=K<8`, `K^2/s<=7K` and `m>=2`; the bound `W_s(a^*)>=mK/2` implies the same conservative `3/64` bound. The uniform upper and lower estimates prove the theorem. Square.

This is an output-volume lower bound only when those integer blocks are explicitly materialized or transferred as ordinary binary objects. A compressed symbolic, modular, delayed-carry or fused product interface can avoid such materialization, but then it is a different interface and needs its own exactness and cost proof. The theorem is not a lower bound for integer multiplication or for all radix conversion.

### Boundary checks

- `s=1`: the blocks are the full Taylor coefficients; their worst-case total width is `Theta(N+K^2)`.
- `s=K`: there is one block `U_0=X`; its exact worst-case width is `N`, consistent with `Theta(N+K)`. This boundary provides no smaller multiplication child.
- Small `m`, including composite `p=15`, is covered. No prime-field assumption is hidden in the proof.
- The coefficient bound is simultaneous and data-dependent on a valid worst-case input. It does not imply that the zero input or every input has this volume.

## 4. The smaller-matrix specialization and what fusion would save

Set `K=dM^2`, `M>=2`, `d>=1`, so `N=mdM^2`.

1. Materializing all `K` Taylor coefficients (`s=1`) has worst-case width `Theta(N+d^2M^4)`.
2. Materializing the `M^2` redundant `p^d` blocks (`s=d`) has width `Theta(N+dM^4)`.
3. Producing only the final `M` redundant `R=p^(dM)` blocks (`s=dM`) has width `Theta(N+dM^3)`.

The third representation still respects the requested `p^d` grouping algebraically: it fuses groups of `M` such positions, without requiring the intervening values to exist as separate objects. It avoids a factor `M` in the redundant part of the grouped output volume. This is a statement about a permitted destination representation, not an algorithm achieving its output-size bound.

For an `o(N log N)` nonrecursive budget, materializing the `p^d` intermediate blocks requires

    M^2/(m log N) -> 0,

whereas the final `M`-block materialization alone requires only

    M/(m log N) -> 0.

If all Taylor coefficients are materialized first, the additional necessary condition is `dM^2/(m log N)->0`. These are necessary output-size conditions, not sufficient running-time conditions. The constant-size and small-`N` cases can be handled directly.

## 5. Why a closed linear packed-state Horner update fails

Let `E_s` be the linear map that sends the coefficient vector of a degree-`<K` polynomial `F` to its `B` packed values defined as above. Suppose `1<s<K`. There is no linear map `L` on the `B` packed values such that

    E_s((z+1)F)=L E_s(F)

for every `F` of degree at most `K-2`.

Indeed choose

    F(z)=z^(s-1)-p z^(s-2).

Its degree is at most `K-2` since `s|K` and `s<K`. Both terms are in the first packed group and `E_s(F)=0`. But

    E_s((z+1)F)=E_s(zF)=(-p^s,1,0,...,0),

which is nonzero. This contradicts linearity.

The signed witness does not incorrectly assume that a legal binary input has negative digits. If a fixed linear update were correct on every legal Taylor-state basis vector `(z+1)^i`, `0<=i<=K-2`, then by linearity it would be correct on their span. Those vectors arise from legal binary-chunk unit inputs and form a basis of the relevant polynomial space. The signed witness lies in that span and therefore refutes that fixed linear update.

More explicitly, if `F(z)=sum_j f_j z^j`, the update for a nonfinal block is

    U'_r=(p+1)U_r-p^s f_(rs+s-1)+f_(rs-1),

with `f_(-1)=0`. The missing boundary coefficients are exactly what the packing forgets as a linear map. Retaining some of them can support a step, but a complete multi-step state and its size/cost must still be supplied.

This proves only the failure of the stated closed linear packed-state transition. It does not exclude a nonlinear decoder, a time-dependent streaming algorithm using the original chunks, additional state, recomputation, or a factored representation. On the actual admissible Taylor images, the full packed output determines `X`, so this is not an information-theoretic collision between two legal inputs. At `s=1`, all coefficients are retained; at `s=K`, evaluation at `p` intertwines degree-safe multiplication by `z+1` with scalar multiplication by `p+1`. Those endpoints are intentionally excluded.

## 6. Complete paid elementary algorithm

Here `s=dM`, `K=dM^2`, and `H=ms+K+1=N/M+N/m+1`.

### Input preparation

Read the binary inputs as `K` chunks each: `O(N)` bits. Form `A(z+1)` by coefficient-array Horner: successively multiply the current polynomial by `z+1` and add the next input chunk. This uses `O(K^2)` additions. Every intermediate coefficient is bounded by `p2^K<2^(m+K)`. A full-width implementation therefore has `Theta(K^2(m+K))` bit work and `O(K(m+K))` coefficient storage. A shorter adaptive implementation can improve individual inputs; no general lower bound for all Taylor-shift algorithms is asserted.

Within each block, compute `U_r` in reverse coefficient order by `u <- (u<<m)-u+c_j`. There are `K` steps; completed values fit `H` bits and a separately materialized shifted temporary fits `H+1` bits, costing `O(KH)` in total. This forms the final `M` blocks directly from the Taylor coefficient array and does not materialize intermediate `p^d` blocks. It **does** materialize all `K` Taylor coefficients, and therefore does not achieve the stronger fused-producer goal of Section 4.

The constants `p` and the parameters need no huge power construction. Counter initialization, array movement and constant preparation fit the displayed bounds. Any search for input-dependent parameters or primality is a separate, presently unspecified cost; this account uses supplied integers `m,d,M`.

### Products and coefficient growth

An elementary smaller outer-product matrix uses `M^2` recursive products `U_i V_j` on operands of at most `H` bits. Their eager outputs use at most `2M^2H` bits. Accumulate the diagonal sums

    S_k=sum_(i+j=k) U_i V_j, 0<=k<=2M-2.

They satisfy `0<=S_k<M 2^(2H)`, so `2H+ceil(log2 M)+1` bits suffice. Direct accumulation costs `O(M^2(H+log M))` bit work. No coefficient is assumed to fit in `R`, and no canonical-radix carry bound is imported from the earlier reports.

There is also a matching actual eager-product-volume statement. For the pair of maximizing inputs `X=Y=2^N-1`, every block is positive and `ell(uv)` lies between `ell(u)+ell(v)-1` and `ell(u)+ell(v)`. Summing over all `M^2` pairs gives volume `Theta(M W_s(a^*))`, hence

    Theta(MN+dM^4).

Thus the extra redundant coefficient growth survives actual eager block multiplication; the volume is not merely `Theta(MN)` unless the additional term is absorbed in the chosen regime. This statement concerns explicitly storing the `M^2` products; a diagonal-only, streaming, bilinear or fused nonlinear executor need not store those objects.

### Binary reconstruction

The exact answer is `XY=sum_k S_k R^k`. Evaluate it high-to-low by Horner. Multiplication by `R=p^s` is `s` successive operations `v<-(v<<m)-v`, followed by the next coefficient addition. There are at most `2M-2` such grouped multiplications. Since every coefficient is nonnegative, every completed partial Horner value is at most the final `XY<2^(2N)`; each completed repeated-`p` multiplication is also bounded by the following completed partial value. These completed values fit `2N` magnitude bits. A separately materialized `v<<m` can require `2N+1` scratch bits: its size is `(p+1)/p<=4/3` times the completed product `pv`. That extra scratch bit is charged; it changes no asymptotic term.

This costs `O(MsN+M(H+log M)+N)=O(KN+M(H+log M)+N)`. Ordinary exact integer additions resolve all coefficient overlap. There is no separate unpaid carry pass. A caller requesting canonical `p^d` digits as well would incur a new normalization interface; this algorithm requests only binary `XY` and writes the full `2N` padded output bits.

### Full direct recurrence invoice

For the specified supplied-parameter, full-width algorithm,

    T(N) <= M^2 T(H)
            + O(K^2(m+K) + KH + M^2(H+log M) + KN + N),
    K=dM^2, N=mK, H=ms+K+1, s=dM.

The two input transforms change only the hidden constant. An `H>=N` choice is not a shrinking recurrence and must fall back to a separately paid basecase. This is a valid finite exact construction; it is not a faster algorithm, and `M^2` is not treated as a constant.

### Optional sharp-count classical coefficient kernel

The previously accepted evaluation/interpolation kernel can replace the `M^2` products by `r=2M-1` products without any new rank claim. Its former block width must be replaced by the present `H`, because the inputs are redundant. Put

    ell=ceil(log2 r),
    J=H+ceil(log2 M)+(M-1)ell+1,
    kappa=(r-1)(ell+1)+1,
    W=2J+kappa+ceil(log2 r)+2.

Evaluating at integer points `0,...,r-1` fits `J`-bit operands. Integer-scaled Lagrange coefficients and the exact common denominator fit `kappa` bits; signed decoder accumulators fit `W` bits. The fully paid inherited construction gives

    T(N) <= r T(J)
            + O(K^2(m+K) + KH + KN + N
                 + M^2 J ell + M^2 W kappa + M^3 kappa^2).

The last three terms pay both input evaluations, all signed decoder products/additions/exact divisions, and cold interpolation-table setup respectively. Table storage is `O(M^2 kappa)` and recursive outputs cost `O(rJ)` bits; these fit the invoice. Any unbalanced or adaptive child invoice must replace these capacities with proved actual sizes. If `J>=N`, this is not a shrinking recurrence. This is classical Toom-style evaluation/interpolation, already documented in the source packet; its use cannot be credited as a new discovery.

Neither invoice establishes a strict `N log N` potential contraction. The elementary preparation term contains `K^2m=NK=N^2/m`, and the reconstruction is paid separately. The new work is the changed representation and its exact obstruction, not a new asymptotic conclusion from recycling those old cost terms.

## 7. Precise next lemma and stopping condition

The next useful constructive target is the following fully specified fused map, not another count of visible matrix entries:

    F_(m,K,s):(a_0,...,a_(K-1)) -> (U_0,...,U_(K/s-1)),
    U_r=sum_(i=0)^(K-1) a_i
        sum_(t=0)^(s-1) binom(i,rs+t)p^t,

where `binom(i,j)=0` for `j>i`, preferably with `s=dM` and without writing all Taylor coefficients. Prove an exact uniform algorithm with declared coefficient representation, bit costs and any recursive multiplication children. Then combine it with a paid joint-product/decoder and binary readout. Producing the map in roughly its output size would be useful, but is **not supplied or asserted here**.

For a fixed-contraction strategy, the combined real children, including any used inside the fused producer and readout, must have widths below the actual parent and satisfy a justified inequality such as

    sum_t h_t log2 h_t <= (1-eta) N log2 N,

for fixed `eta>0`, together with an explicitly sufficient nonrecursive budget. Alternatively provide a different complete recurrence proof. Replacing `F` by a named fast Taylor-shift or generic multiplication library is not a proof unless its bit widths, modulus/setup if any, conversion, recursion and reconstruction are all paid. A prime-field `O(M(K))` polynomial-operation count cannot be substituted for that ledger.

The stopping condition for this bounded investigation is reached: the exact redundant-block volume is proved, the closed-linear-state shortcut is refuted, and a complete elementary fallback invoice is supplied. The fused fast producer, faster readout, adaptive parameter selection and the original multiplication-speed goal remain open. No canonical research owner, status, score or priority change is proposed.

## 8. Verification boundary

`fresh_controls.py` is newly written, standard-library-only arithmetic code. It checks Taylor identities, separate-block maxima, zero/maximum/random cases, end-to-end redundant matrix reconstruction, the stated upper/lower volume inequalities, and the signed nonintertwining witness. It includes `s=1`, `s=K`, small `m`, and composite Mersenne bases. `CONTROL_RESULTS.json` records the bounded checks. Python big integers are exact arithmetic oracles only; tests do not prove the universal formulas or a complexity bound. The proofs above do.

All source reports and historical programs remain unchanged. This packet has not been independently reviewed or externally published by this worker.
