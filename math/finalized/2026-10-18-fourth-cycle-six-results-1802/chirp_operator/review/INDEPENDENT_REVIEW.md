# Independent review: ALG-043 operator cores and materialized application cost

Date: 2026-10-18 UTC.

Candidate: `../candidate`.
Frozen candidate result SHA-256: `0369a1901bbc643b3233d81f03852d8d1cbe93cc854e59ae2b22d01bb90cd380`.

## Verdict

**PASS for the stated bounded gate. No blocking defect found.**

The exact paired-cut convolution ranks, explicit signed-difference cores, paid preparation, complete arbitrary-input contraction, and scoped materialized-frontier obstruction are correct. The distinct DFT paired-cut rank theorem is also correct. The selected header mask preserves the asymptotic obstruction under the specified accepted parameters.

The lower bound applies only to implementations required to explicitly materialize the named frontier values. It does not cover all contraction orders, compressed or factored frontiers, FFTs, or arbitrary linear circuits. The `Theta(N W^2)` work and `Theta(N W)` live storage are charges for the specified literal executor; only the weaker `Omega(N W)` write/work obstruction is asserted for every implementation materializing that frontier, including chunked ones.

ALG-043 remains **TO RESEARCH, priority 34**. This does not establish `T_E(N)=o(N log N)`, a faster Fourier algorithm, numerical stability, bit complexity, historical priority, or a new research identity. No external write was made. The candidate and both accepted predecessor packages were left unchanged.

## 1. Contract, source identity, and exact cut ranks

The source kernel is `g(t)=omega^(-t(t+1)/2)` for signed integers `t`, with `N=2^n` and a supplied primitive `N`th root over a field. Triangular exponents are integers; no division by two in the field and no unprovided `2N`th root are used. Root existence excludes characteristic two. The executable's modulus is a supplied prime; field discovery is outside the constructor contract.

The paired physical site contains both output and source bits in the order `(0,n-1,1,n-2,...)`. This is a four-valued site, not a vector TT unfolding and not the ordinary matrix rank separating the complete output and input indices.

At cut `k`, put `j=ceil(k/2)`, `h=floor(k/2)`, and `m=n-k`. The exterior part has low integers `a` and high integers divisible by `2^(n-h)`; the middle has the form `2^j c`. Since `j>=h`, all processed-high/middle products vanish modulo `N`.

For the convolution tensor, removing nonzero row and column factors leaves

`(omega^(2^j))^(-alpha beta)`,

with consecutive signed differences `alpha` in `[-(2^j-1),2^j-1]` and `beta` in `[-(2^m-1),2^m-1]`. The reduced root has order `2^(n-j)`. Choosing consecutive exponents and distinct consecutive root nodes gives a nonzero Vandermonde determinant of size

`R_k=min(2^(j+1)-1, 2^(m+1)-1, 2^(n-j))`.

Dimensions and repeated root nodes give the matching upper bound. This argument is valid over every field satisfying the supplied-root contract. For `n>=3`, the root-order cap is inactive and `R_k=2 r_k-1`, where `r_k=2^min(j,m)`. Thus the minimum maximum width in this order is `2W-1`, with `W=2^floor((n+1)/3)`.

The `n=2` exception is necessary: its only paired-cut rank is 2, whereas the uniform reference uses width 3. The report discloses this and gives a correct two-state exception. I independently checked all 16 matrix entries of that exception. At `n=1`, there is no internal bond and width is conventionally one.

For the DFT, removing prefix-only and suffix-only factors instead leaves

`(omega^(2^j))^(a_ell c_s+a_s c_ell)`.

After swapping column components, this is a Kronecker product of two rectangular Vandermonde matrices, each of rank `r_k`. Its rank is exactly `r_k^2`, so the minimum maximum paired MPO width is `W^2`. Exact successive rank factorizations establish attainability, without establishing a cheap DFT core constructor.

The identity `C[ell,s]=g(ell)g(-s)omega^(ell s)` does not identify these two unfolding ranks: its diagonal chirps couple digits across the paired cut. Their action on a dense vector is cheap, but they are not scalar row/column factors of that unfolding. The candidate correctly preserves this distinction.

## 2. Signed-difference cores and preparation

Let `s` be the first stage with `ceil(s/2)>=n-s`.

Before the bridge, the state stores the difference of processed low integers. Adding physical difference `delta` at bit `p` multiplies by `g(2^p delta)omega^(-a 2^p delta)`. Earlier high bits have trivial interaction with the incoming digit. Updating the signed state on low stages and retaining it on high stages therefore preserves exactly the chirp of the processed difference.

At the bridge, the new state is the signed difference of the unprocessed middle integers. The bridge coefficient completes the chirp, including its interaction with the old low difference. Previously discarded high bits have no unpaid interaction. Afterwards, unit-valued consistency cores implement the exact low-digit recurrence `d_old=delta+2d_new` or high-digit recurrence `d_old=delta M_new+d_new`. Each complete input/output bit pair has exactly one surviving suffix-difference path. There is no free subtraction, borrow, or input-compression oracle.

The cold constants are valid for both signs. In particular, `g(-2^p)=g(2^p)omega^(2^p)`, and the positive and negative bridge chirp sequences both advance their ratios by `omega^(-2^(2j))`. Consecutive signed `a` powers fill the bridge table with constant amortized scalar work per entry. The table's signed range covers both bridge parities: its integer coordinate is `delta+2d` at a low bridge or `delta M+d` at a high bridge.

All stored transitions are nonzero and unique as physical/state tuples. The independent checker reconstructs their complete key/value sets rather than only checking supplied entries, so omissions and duplicates would be detected.

### Exact slot and multiplication ledgers

Write `Rhat_0=Rhat_n=1` and `Rhat_k=2r_k-1` internally. The exact nonzero core slots are

`M_core=4 sum_(k<s) Rhat_(k-1) + 4 Rhat_(s-1)Rhat_s + 4 sum_(k>s) Rhat_k`.

Independent summation gives sharper closed forms, valid also for `n=1,2`:

- `n mod 3=0`: `M_core=16W^2+8W-4n-24`
- `n mod 3=1`: `M_core=16W^2+16W-4n-24`
- `n mod 3=2`: `M_core=8W^2+8W-4n-24`

These imply the reported `Theta(W^2)` and its simpler upper bound. The bridge alone supplies the matching lower bound.

Let `A=2^floor(s/2)` and `M=2^(n-s)`. The bridge table has exactly `(2A-1)(4M-1)` entries. The constructor's exact modular multiplication count is

`9n-1 + 3 sum_(k<s) Rhat_(k-1) -(s-1) + 2(A-1)(4M-1) + 12M`.

Here `9n-1` pays root guards, root inversion, and constant arrays; a prefix stage pays `3Rhat_(k-1)-1`; the bridge pays its two signed state progressions and six updates for each of its `2M` nonnegative coordinate iterations. Even unused final progression updates are charged. Runtime scalar instrumentation and this independent formula agree in all tested cases.

The largest independent construction, `n=18` over `GF(786433)` with odd embedding 7, has width 127, 65,952 scalar core slots, and 33,765 paid modular multiplications. It requires no dense `N` or `N^2` object during construction.

Signed intervals admit offset-indexed dense tables. Sparse transitions can be emitted sequentially. Thus the asymptotic `O(n+W^2)` field/address work and storage do not rely on Python dictionary expected-time behavior. Address words have `O(n)` bits. The claim remains an ideal-field/address count, not modular multiplication bit complexity.

## 3. Full arbitrary-input application

The application explicitly routes an ordinary-order dense input into the interleaved order. The permutation is prepared by repeated list doubling, whose cumulative size is geometric. It costs `O(N)` word work and storage; it is not hidden in the sublinear operator setup.

After stage `k`, the frontier has one output-prefix, one unread source-suffix, and one MPO-state coordinate. Its size is exactly `N Rhat_k`. The update indices correctly consume the next source digit and append the next output digit in the packed reading order. The independent checker compares individual intermediate values with direct linear forms in the original input, not with another contraction implementation.

For each core slot there are exactly `N/2` prefix/suffix contexts. Therefore the deliberate literal loop pays exactly

`multiplications=additions=N M_core/2`.

I instrumented the actual scalar multiplications and additions, including suffix unit weights and operations on zero data. The resulting counts agree exactly. Zero initialization costs `N sum_(k=1)^n Rhat_k`; two rolling frontiers peak at `N max_k(Rhat_(k-1)+Rhat_k)` slots. The geometric rank profile gives `O(NW)` initialization and `Theta(NW)` literal frontier storage. Input/output routing, selected output writes, core reads, accumulation accesses, and addresses add their stated costs and do not improve the leading `Theta(NW^2)` work.

At `n=9`, the independent application over `GF(12289)` pays 263,168 multiplications, 263,168 additions, and 31,232 initialization writes, peaking at 15,360 frontier slots. Output selection is tested in unsorted order with duplicate indices; the requested order and multiplicities are preserved.

The Fourier reduction is correct: multiply the input by `omega^(s(s-1)/2)`, run the convolution, then multiply output `ell` by `omega^(ell(ell+1)/2)`. Independently generated ratio-recurrence diagonals agree with direct integer powers and produce the direct positive-sign DFT. These diagonal preparations/scalings cost `O(N+|E|)`; the separately supplied unitary scaling costs `O(n+|E|)` if requested. No favorable all-input TT rank is assumed.

## 4. Scope of the frontier obstruction and selected mask

At a prebridge cut, each fixed output prefix and source suffix permits exactly `A_k=2^j` low-difference states. Their linear forms sum over distinct processed high-source assignments, with nonzero coefficients. There are exactly `N A_k` feasible, nonzero linear forms. At `k=s-1`, `W/2<=A_k<=W`, so their count is `Theta(NW)`.

No independence among these forms is required or claimed. An implementation required to explicitly write each named frontier value pays that number of scalar writes. Over an infinite field, a single input avoids all of their zero hyperplanes. Over a finite field of size `q`, each nonzero form is nonzero with probability `1-1/q`; averaging supplies an input with that fraction of nonzero values. This supports the worst-case write lower bound even if data-zero entries can be skipped.

After the bridge, some stored states cannot lead to an output within the legal range. They can nevertheless contain nonzero numbers. The candidate correctly distinguishes such dead states from impossible prebridge states, which are structurally zero. Pruning dead states does not remove the prebridge obstruction. The independent tests explicitly find nonzero dead suffix states.

The original accepted source supplies `E={Bv+u:v in H,0<=u<B}`, density `rho>=1/4096`, header width `K=Theta(n/ln n)`, and paid header work `O(QK^3)=N^o(1)`. When the processed high count satisfies `h>=K`, exactly `rho 2^k` output prefixes remain; their lower and middle bits are free. Thus the prebridge frontier count is exactly `rho N A`. At the bridge neighborhood `h=Theta(n)`, so the condition holds eventually because `K=o(n)`.

At such a cut, a nonempty header mask also retains both full operator ranks. Fix any accepted processed output high assignment and any input high assignment. All low and middle values needed for the convolution Vandermonde or DFT Kronecker minor remain. Conversely, the mask is only a row factor of that unfolding, so rank cannot increase. Positive density is needed for the stated frontier-size asymptotic; rank preservation itself needs only nonemptiness and `h>=K`.

This is a representation-specific obstruction. It neither rules out algebraic compression of these values nor proves a lower bound for unrelated elimination orders or general algorithms. A chunked materialization still incurs the write bill, but its peak storage need not equal the literal executor's simultaneous-frontier storage.

## 5. Independent evidence, preservation, and qualification

A frozen candidate snapshot is retained under `reviewed_candidate/`. Its own checksum list passed and its cold replay exactly reproduced the declared result digest.

`independent_review.py` imports only the frozen constructor/executor under test. It does not import the submitted checker or any historical implementation. It independently implements streaming exact elimination, full operator unfoldings, direct signed triangular exponents, complete coefficient-set comparison, backward pair contractions, direct intermediate linear forms, header counts, scalar instrumentation, and closed-form ledgers.

The final independent controls include:

- 23 constructor/root instances across primes 193, 769, 12289, and 786433, through `n=18`, plus separate small-characteristic controls
- 75,212 independently reconstructed core coefficients and 3,451 backward physical-pair contractions
- 56 full operator-unfolding ranks and 10 independently generated masked ranks
- 12 dense-input/selected-output applications with exact runtime arithmetic metering and direct Fourier comparisons
- 10,426 individual intermediate values, distinguishing zero prefix entries from dead suffix entries
- 1,500 all-size integer slot/storage controls and the exact preparation formula on every constructed instance
- All 9 input vectors in a small `GF(3)` case and all 16 entries of the optimal `n=2` exception
- Five targeted negative controls: wrong root order, false optimality of the uniform `n=2` width, transferring convolution width to the DFT, omitted chirp diagonals, and treating dead suffix states as zero

An initial review-only instrumentation attempt missed multiplications whose two operands were plain constant ones. The failure is retained in `INITIAL_METER_INSTRUMENTATION_FAILURE.log`. The meter was corrected to include those calls, and independently derived exact arithmetic formulas were added. This was a checker-instrumentation issue, not a candidate counter discrepancy. The corrected complete suite and its replay pass.

Finite checks validate indexing, guards, reconstruction, and the finite ledger. The general field-rank and lower-bound conclusions rest on the algebraic arguments above. Source-package hashes and their preservation are checked in `BINDINGS.json`; the final review is sealed with `SHA256SUMS`.

The bounded conclusion is useful: the difference interface admits a paid low-width operator, but the specified explicit all-input frontier cannot deliver `o(N log N)`. Further progress needs a different contracted representation/order or another independently paid application strategy. The package makes no broader impossibility claim.
