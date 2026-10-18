# ALG-043: exact interleaved operator cores and the paid application frontier

Date: 2026-10-18 UTC. Owner: **ALG-043**, unchanged. This is a new proof and executable-control package; it does not modify the accepted packages or any external repository.

## Result

The changed-order kernel compression extends to an exact, cheaply prepared convolution **operator**, but the natural arbitrary-input contraction is expensive.

Let `N=2^n`, `g(t)=omega^(-t(t+1)/2)`, and use paired output/input digits in the order

`pi=(0,n-1,1,n-2,...)`.

Write `j=ceil(k/2)`, `h=floor(k/2)`, `m=n-k`, `r_k=2^min(j,m)`, and `W=2^floor((n+1)/3)`.

1. The exact operator unfolding rank of `C[ell,s]=g(ell-s)` at cut `k` is

   `R_k = min(2^(j+1)-1, 2^(m+1)-1, 2^(n-j))`.

   For `n>=3`, this is `2 r_k-1`, with maximum `2W-1`. The root-order cap matters at `n=2`, whose only rank is 2.

2. Explicit signed-difference cores attain these ranks for `n>=3` and have `O(W^2)=O(N^(2/3))` scalar slots and cold preparation work. They use the supplied root only. A uniform reference uses width 3 instead of the optimal 2 at `n=2`; this harmless small-size exception is explicit.

3. A complete left-to-right dense-input executor is given and tested, including ordinary-index input routing, intermediate initialization, selected outputs, and Fourier diagonals. Its charged scalar updates are exactly `N M_core/2` multiplications and the same number of additions. Thus its work is `Theta(N W^2)=Theta(N^(5/3))`, and its live working storage is `Theta(N W)=Theta(N^(4/3))`.

4. This expense is not only a loose allocation bound. Before the bridge, there are exactly `N A` structurally feasible, nonzero linear-form entries, where `W/2<=A<=W`. Any implementation required to materialize this frontier pays `Omega(NW)` scalar writes, even if the bridge is accelerated or impossible states are omitted. The original positive-density selected header mask preserves this bound asymptotically. This is a **materialized-frontier obstruction**, not a lower bound for arbitrary contraction orders, factored frontiers, FFTs, or general linear circuits.

5. The unscaled DFT operator has different exact ranks in the same paired order:

   `rank(F at cut k)=r_k^2`, hence minimum maximum MPO width `W^2`.

   The cheap dense-vector chirp diagonals do not preserve operator unfoldings, so there is no contradiction with item 1. A Fourier MPO cannot simply inherit the convolution MPO width.

**No sub-`N log N` selected convolution or DFT application is established.** This closes a specific subtraction-interface and literal-contraction gate, while locating a further representation change that would be needed to make it useful. ALG-043 remains TO RESEARCH, priority 34; no identity, priority, novelty, historical-priority, or census change is proposed.

## 1. Sources, contract, and tensor order

The accepted sources were read in full:

- `dependencies/chirp_interleaved_20261018_1504_REPORT.md`
- `dependencies/chirp_interleaved_review_20261018_1513_INDEPENDENT_REVIEW.md`
- the first package's `sources/ORIGINAL_SELECTED_CONVOLUTION.md`

Their complete directory hashes are bound in `SOURCE_BEFORE.json` and rechecked in `SOURCE_AFTER.json`. No predecessor program was imported or executed. The source reports identify ALG-043 and the precise triangular chirp, finite-field contract, positive-density header mask, and unresolved selected-convolution gate.

The exact scalar model is the inherited field containing a **supplied primitive Nth root** `omega`; the normalized Fourier interface also supplies `1/sqrt(2)`. For `n>=1`, characteristic two is excluded by root existence. Scalar reads, writes, additions, and multiplications by prepared constants are charged. Addresses have `O(n)` bits. No packed arbitrary inputs, root extension, full uncharged root table, or bit-complexity identification is used.

An operator tensor has physical site `(ell_pi[k],s_pi[k])` of size four. A cut partitions **both** indices into their processed exterior digits and their unprocessed middle digits. This is neither the vector TT unfolding of `g(t)` nor the matrix rank separating the complete input index from the complete output index.

At any cut, decompose

`ell = a_ell + b_ell + 2^j c_ell`,
`s   = a_s   + b_s   + 2^j c_s`,

where `0<=a_ell,a_s<2^j`, the processed high parts `b_ell,b_s` are divisible by `2^(n-h)`, and `0<=c_ell,c_s<2^m`. The remaining positions form one contiguous middle interval.

## 2. Exact convolution-operator ranks

Set `d=(a_ell+b_ell)-(a_s+b_s)` and `v=2^j(c_ell-c_s)`. The integer identity

`g(d+v)=g(d) g(v) omega^(-d v)`

holds for negative as well as positive arguments. Since `j>=h`, the product `(b_ell-b_s)v` is divisible by `N`. Multiplying unfolding rows and columns by nonzero scalars therefore reduces the operator unfolding to

`V[alpha,beta] = zeta^(-alpha beta)`,

where `zeta=omega^(2^j)`, `alpha=a_ell-a_s` ranges through all integers `-(2^j-1),...,2^j-1`, and `beta=c_ell-c_s` ranges through `-(2^m-1),...,2^m-1`. Repeated differences only duplicate rows or columns after the rescaling.

The order of `zeta` is `H=2^(n-j)`. The upper bound is the minimum of the two difference counts and `H`. For the reverse bound choose `R` consecutive alpha values and `R` consecutive beta values, with `R` equal to that minimum. The beta nodes are distinct because `R<=H`; shifting the starting alpha exponent only rescales the nodes. This gives an invertible Vandermonde minor over the supplied field. Hence

`R_k=min(2^(j+1)-1,2^(m+1)-1,H)`.

For `n>=3`, `H>=2^(min(j,m)+1)` at every internal cut. If `k>=2`, this follows from `n-j=m+h` and `h>=1` when `m<=j`, or from `m+h>=j+1` when `j<=m`. The remaining `k=1` case has `j=1` and `n-j>=2`. Thus `R_k=2r_k-1` throughout. At `n=2,k=1`, `H=2` instead, giving rank 2.

Every MPO bond factors its corresponding unfolding, so these are lower bounds on its bonds. The construction next attains them for `n>=3`. Maximizing gives exact width `2W-1`. For `n=1` there is no internal bond and width is conventionally one.

## 3. Explicit sparse difference-state cores

Let

`s_* = min{k : ceil(k/2)>=n-k}`

be the bridge stage. Define convenient uniform state counts `Rhat_0=Rhat_n=1` and `Rhat_k=2r_k-1` for internal cuts. This differs from the minimum only at `n=2`.

### 3.1 Prefix cores

Before the bridge, the state is the signed difference `a` of the processed low parts. At stage `k<s_*`, position `p=pi[k]`, and physical pair `(u,v)`, let `delta=u-v`. Multiply by

`g(2^p delta) omega^(-a 2^p delta)`.

At a low-bit stage, update `a <- a+2^p delta`; at a high-bit stage, keep `a` unchanged. There are four transitions per old state, including the two physical pairs with zero difference.

The accumulated coefficient is `g(d_processed)`. Previously processed high bits have trivial interaction with the next digit: their position sums are at least `n`. Therefore the discarded high-bit difference carries no unpaid interaction. Negative `a` and negative `delta` do not change this divisibility argument.

### 3.2 Bridge

Let `j_0=ceil((s_*-1)/2)`, `A=2^j_0`, `M=2^(n-s_*)`, and `j_1=ceil(s_*/2)`. Before the bridge, `a` ranges from `-(A-1)` to `A-1`. The outgoing state `d` is the signed difference of the remaining middle integers, so `-(M-1)<=d<=M-1`.

For position `p` and physical difference `delta`, put

`v = 2^p delta + 2^j_1 d`.

The bridge coefficient is

`B[a,u,v_bit,d] = g(v) omega^(-a v)`.

Earlier high differences have no nontrivial interaction with any part of this remaining integer. Multiplying the prefix and bridge therefore gives the complete kernel coefficient as soon as the suffix difference is correct.

### 3.3 Suffix cores

After the bridge, states describe differences of the still-unread middle integers. At a low stage, the old and new states obey

`d_old=(u-v)+2 d_new`.

At a high stage, with `M_new=2^(n-k)`, they obey

`d_old=(u-v) M_new+d_new`.

These cores have coefficient one on consistent transitions, zero elsewhere. At the end the state is zero. For every fixed complete pair `(ell,s)`, exactly one suffix-difference sequence and exactly one prefix sequence survive. Their contraction is exactly `g(ell-s)`, without cancellation or division.

This works directly with differences; no free subtraction/borrow oracle is assumed. In particular, the earlier missing difference interface can be supplied without multiplying the width by a power of `N`.

For completeness, the optimal `n=2` width-2 exception can use first state `a=(u-v) mod 2`, first coefficient `g(u-v)`, and last coefficient `g(2(u-v))(-1)^(a(u-v))`. The executable deliberately retains the uniform width-3 signed-difference version instead.

## 4. Cold preparation and scalar/address ledger

The scalar core-slot count of the uniform construction is exactly

`M_core = 4 sum_(k<s_*) Rhat_(k-1)
          + 4 Rhat_(s_*-1) Rhat_(s_*)
          + 4 sum_(k>s_*) Rhat_k`.

The last sum uses the new-state count, since each new difference and physical pair gives one old difference. All transitions are nonzero. Geometric sums and `Rhat_k<=2r_k` give

`M_core <= 16 W^2+32 W`.

The bridge alone has `Theta(W^2)` slots, because `W/2<=A,M<=W`. Thus `M_core=Theta(W^2)`. The dense state dimensions obey the exact rank profile for `n>=3`.

The constructor first checks root order and prepares, by repeated squaring,

`q_p=omega^(-2^p)`, `qinv_p=omega^(2^p)`,
`cplus_p=g(2^p)`, `cminus_p=g(-2^p)=cplus_p qinv_p`.

The `cplus` recurrence is `cplus_(p+1)=cplus_p^2 q_(2p)`, with `q_t=1` for `t>=n`. This costs `O(n)` operations, including root guards and inversion by `omega^(N-1)`.

Prefix signed phase powers use simultaneous geometric progressions in `q_p` and `qinv_p`, costing `O(Rhat_(k-1))` per stage.

For the bridge write the unprocessed integer as `2^j_0 c`, with signed `c` in `-(2M-1),...,2M-1`. Prepare the table

`T[a,c]=g(2^j_0 c) omega^(-a 2^j_0 c)`.

Both signs of the chirp are generated by ratio recurrences. For `D=2^j_0`, the positive and negative sequences start at one, have initial ratios `g(D)` and `g(-D)`, and both ratios advance by multiplication by `omega^(-D^2)`. Both signs of `omega^(-D c)` are generated geometrically. For each `c`, generate positive and negative `a` powers from `T[0,c]` with those two phase factors. Every coefficient therefore costs constant amortized field work. There are exactly

`(2A-1)(4M-1) <= 8W^2`

table entries. Each bridge slot is a table lookup with the explicit integer index in section 3.2. The table is temporary and can be discarded after the bridge is written. Suffix cores require charged unit and index writes only.

All constants, cores, temporary tables, transition indices, and stage metadata fit `O(n+W^2)` scalar/address words and are constructed with the same order of work. Addresses and exponent words are `O(n)` bits. The Python dictionary is an executable reference, not a worst-case RAM claim: these signed intervals can be offset-indexed dense arrays, and the core transitions can be emitted sequentially. No hashing assumption is needed for the mathematical bound.

The largest executed construction has `n=16`: width 63, 16,808 nonzero scalar core slots, 8,001 temporary bridge table entries, 64 constant slots, and 8,919 counted modular multiplications including 35 root-guard multiplications. This does not count modular multiplication as unit-cost bit work.

## 5. Complete arbitrary-input application algorithm

### 5.1 Input and output

Input: the supplied field/root, `n`, an ordinary-order arbitrary dense vector `x[0..N-1]`, and requested output indices `E`. If the original marker set is used, its already established header constructor costs `O(QK^3)` word operations, with `Q=2^K`; this cost is retained rather than hidden.

Output: every requested scalar

`c_ell = sum_(s=0)^(N-1) x_s g(ell-s)`, `ell in E`,

in the requested ordinary-index order. There is no assumption that `x` has a small TT representation.

Build the digit-permutation array by starting with `[0]` and appending a shifted copy for each bit position in `pi`. The cumulative lengths form a geometric sum, so the permutation and its `N` entries are prepared in `O(N)` word work. Route the input in `O(N)` scalar/address operations. This is a paid full-length array, used only for application; it was not hidden in the sublinear operator preparation.

### 5.2 Intermediate and update

After `k` paired sites, keep

`F_k[output_prefix, source_suffix, operator_state]`.

Its dimensions are `2^k`, `2^(n-k)`, and `Rhat_k`. In particular it has `N Rhat_k` scalar slots. Initially `F_0` is the routed dense input, with the only state zero.

For every nonzero core entry `(alpha,u,v,beta,w)` and every old output prefix `P` and remaining source suffix `S`, update

`F_k[P+u 2^(k-1), S, beta]
 += w F_(k-1)[P, v+2S, alpha]`.

The source and output codes here are packed in the selected reading order, so the formulas are ordinary shifts and offsets. This is just distributivity with all input and output legs explicit; its correctness follows by induction on the contracted sites.

For each fixed core slot, there are exactly `2^(k-1) 2^(n-k)=N/2` contexts. The reference charges a multiplication and addition even for unit weights or zero data. Consequently its exact arithmetic ledger is

`multiplications = additions = N M_core/2`.

Initialization is exactly `N sum_(k=1)^n Rhat_k` zero writes. This is `O(NW)` because the ranks grow geometrically before the bridge and shrink geometrically after it. The two rolling frontiers require at most `N max_k(Rhat_(k-1)+Rhat_k)=O(NW)` slots. The permutation, input, cores, routed output, and selected output add `O(N+W^2+|E|)` slots. Core reads, input reads, accumulation reads/writes, and address arithmetic cost constant work per scalar update.

At `k=n`, state and source suffix are singleton dimensions and the vector is complete. Route it back through the prepared permutation in `O(N)` work and write all `|E|` requested entries. The reference uses this simple full-output route; it does not pretend that selecting fewer outputs reduces an earlier full contraction.

Thus, including cold preparation and mask work, this explicit executor costs

`Theta(NW^2) + O(QK^3)` work and `Theta(NW)+O(Q)` working words.

At the accepted asymptotic mask parameters, `QK^3=N^o(1)`, so the leading work is `Theta(N^(5/3))`, substantially worse than an FFT. This is an accounting result, not a candidate fast algorithm.

### 5.3 DFT conversion, fully charged

Expansion of the integer triangular exponent gives

`C[ell,s]=g(ell) g(-s) omega^(ell s)`.

For arbitrary Fourier input `z`, set

`x_s=z_s omega^(s(s-1)/2)`.

Apply the convolution executor and multiply each requested output by `omega^(ell(ell+1)/2)`. The result is exactly the unscaled positive-sign DFT of `z` on `E`. Both diagonals have first-order geometric-ratio recurrences, so their constants and all scaling work cost `O(N+|E|)`; one may scan all `N` diagonal entries. For the unitary transform, prepare `(1/sqrt(2))^n` in `O(n)` work and multiply the requested outputs, also charged. Changing the sign of the supplied root changes the Fourier convention in the usual direct way.

There is no supplied `2N`th root or division by two in the field: all exponents above are integer triangular numbers. The tests compare this diagonal conversion with a separately computed direct DFT.

## 6. Scoped obstruction: the frontier itself is large

The following is a lower bound only for algorithms that explicitly materialize the named frontier entries (possibly in chunks), with or without removing structurally impossible entries. It permits fast algebra inside a stage but does not permit replacing the frontier by a factored or otherwise compressed representation. No claim is made about other contraction orders or unrestricted algorithms.

Before the bridge, at cut `k`, let `A_k=2^j`. Fix an output prefix `p_ell` and a source suffix `y_s`. Its state `alpha` is feasible exactly when the processed source low integer

`a_s = a_ell-alpha`

belongs to `0,...,A_k-1`. There are exactly `A_k` such states for every `(p_ell,y_s)`. Hence there are exactly

`2^k 2^(n-k) A_k = N A_k`

feasible entries. Each is the nonzero linear form

`sum_(processed source high parts b_s)
 x_(a_s+b_s+y_s) g(p_ell-a_s-b_s)`.

The source indices in this sum are distinct and all coefficients are nonzero. Thus these are genuinely required entries of this representation, not structurally zero slots. They need not be linearly independent of one another, and no such claim is used.

At `k=s_*-1`, `A_k=A` satisfies `W/2<=A<=W`. There are therefore `Theta(NW)` feasible entries. Over an infinite field, some input makes all finitely many nonzero forms nonzero, by avoiding their zero hyperplanes. Over a finite supplied field of size `q`, a uniform input makes each such form nonzero with probability `1-1/q`, so some input makes at least that fraction nonzero. This establishes the same worst-case order of scalar writes even for data-zero skipping. The first cut is nontrivial for `n>=3`; the asymptotic claim is unaffected by the two tiny exceptions.

After the bridge, for source middle value `c_s` and suffix state `d`, a valid remaining output exists exactly when `0<=c_s+d<2^(n-k)`. Thus there are `N 2^(n-k)` completable entries at that cut. The literal reference also stores nonzero dead entries outside that range: these cannot reach a valid final output, but they need not be zero numerically. The independent intermediate checks deliberately distinguish these notions. Removing them only changes constant factors near the bridge; it does not cure the prebridge lower bound.

Consequently any explicitly materialized pass through this frontier pays `Omega(NW)=Omega(N^(4/3))` work, already larger than `N log N`. This conclusion does not depend on charging the bridge by its dense nested loops. The straightforward core-slot loop does additionally pay `Theta(NW^2)` work, as proved in section 5.

### 6.1 The selected header mask does not remove this obstacle

The original source proves `E={Bv+u : v in H, 0<=u<B}`, with `Q=2^K`, `B=N/Q`, density `rho=|H|/Q>=1/4096`, and `K=Theta(n/ln n)` at its accepted asymptotic parameters.

At a cut whose processed high count `h` is at least `K`, selection depends entirely on the processed output high bits. Exactly `rho 2^k` output prefixes survive. All their low bits and their remaining middle output bits are free. Therefore the preceding feasible prebridge entry count becomes exactly

`rho N A`.

Since `h=floor((s_*-1)/2)=Theta(n)` and `K=o(n)`, this condition holds eventually for the accepted regime. The positive density gives the same `Omega(NW)` bound for an early-mask-pruned materialized frontier. The finite toy-mask tests validate the selected-output implementation only; they are not evidence for the original asymptotic density theorem.

At any cut with `h>=K` and a nonempty header set, the masked, zero-padded convolution operator also retains its **full** rank `R_k`. Fix one accepted processed high output assignment and one input high assignment; all output/input low values and both middle values are still available. This recovers the Vandermonde minor of section 2. The mask is a row factor of this unfolding, which gives the reverse upper bound. Thus it also preserves the maximal operator-width requirement asymptotically. The analogous assertion holds for the DFT ranks below.

## 7. The DFT MPO width is the square of the vector chirp width

For the unscaled DFT tensor `F[ell,s]=omega^(ell s)`, remove the nonzero prefix factor `omega^(p_ell p_s)` and suffix factor `omega^(y_ell y_s)` from a paired cut. The high/middle products are multiples of `N`. The residual matrix is

`zeta^(a_ell c_s+a_s c_ell)`.

Up to an exchange of its two column indices, this is the Kronecker product of two rectangular Vandermonde matrices

`V[a,c]=zeta^(a c)`, `0<=a<2^j`, `0<=c<2^m`.

Each has rank `r_k=min(2^j,2^m)`, by the distinct-node argument with the supplied root. Matrix rank is multiplicative under a Kronecker product over a field. The exact DFT operator cut rank is therefore `r_k^2`, and its exact minimum maximum MPO width in this order is `W^2`.

This is an exact representation-width theorem. A TT/MPO decomposition attaining its unfolding ranks exists by successive exact rank factorizations, but no cheap constructor of those DFT cores is asserted here. The explicit cheap operator construction in this package is for `C`, followed by dense-vector diagonal scaling if Fourier outputs are wanted.

The diagonal operators `diag(g(ell))` and `diag(g(-s))` themselves couple digits across this tensor cut. Hence their relationship to the DFT is not a nonzero row/column scaling of the **paired unfolding**. It is invalid to transfer the convolution MPO rank to the DFT MPO by overlooking those digit couplings. Their dense-vector action nevertheless costs only `O(N)`, which is why the Fourier application reduction in section 5 remains valid.

Finally, arbitrary input vectors do not inherit the fixed kernel's TT width: for any chosen digit order, an arbitrary input can have unfolding rank `2^floor(n/2)` at a middle cut (place an identity matrix in that unfolding). This is another reason a cheap kernel description does not certify a cheap all-input contraction. It is not an arithmetic lower bound.

## 8. Fresh controls, replay, and stop condition

`operator_cores.py` is a fresh paid finite-field constructor and full application reference. `check_application.py` does not execute or import either accepted package. Its independent calculations include signed integer triangular exponents, direct operator unfoldings, Gaussian elimination, direct DFT sums, exact closed-form intermediate arrays, and all-size integer ledgers.

Executed results:

- 63 constructor instances across supplied primes 3, 5, 17, 97, 257, and 65537, with varied primitive embeddings; larger operator-only cases reach `n=16`
- 6,232 individually checked scalar core coefficients in the exhaustive coefficient-control cases
- 15,032 full physical-pair contractions compared with direct `g(ell-s)`
- 75 paired-cut controls, each computing both convolution and DFT ranks independently, for 150 exact rank computations
- 9 additional header-masked paired-cut controls, checking both operators and exact preservation of the cut rank after the header is processed
- 9 full arbitrary-input selected-output applications, `n=1..9`, each also compared with the direct DFT after the two chirp diagonals
- 2,314 individual intermediate entries compared with independent prefix/suffix closed forms, distinguishing impossible-prefix zeros from nonzero dead suffix states
- 1,000 all-size rank/width/bridge controls
- 5 negative controls: nonprimitive roots; deleting bridge phases; transferring chirp width to the DFT; ignoring the `n=2` root-order cap; and omitting the Fourier diagonals

At `n=9`, the straightforward application uses exactly 263,168 multiplications and 263,168 additions, initializes 31,232 stage slots, and peaks at 15,360 slots for its two rolling frontier arrays. These finite controls support indexing, boundary cases, exact arithmetic, and the explicit accounting; the all-size proofs carry the mathematical conclusions. They do not prove floating-point stability, bit complexity, numerical approximation, or historical novelty.

Run `python check_application.py`. `RUN.log`, `REPLAY.log`, and matching result digests record reproducibility. `SOURCE_BEFORE.json` and `SOURCE_AFTER.json` agree; all accepted source-package files are unchanged. `SHA256SUMS` seals the new deliverables.

The bounded outcome is now established: the subtraction interface admits paid low-width exact cores, but the specified materialized all-input contraction cannot meet `T_E=o(N log N)`. A worthwhile subsequent gate would need a genuinely different contracted frontier, a different elimination order, or a separately paid approximation/application error contract. Merely accelerating coefficient generation, compressing the fixed kernel again, or pruning this same positive-density output mask does not address the demonstrated bill. No broader impossibility result is claimed.
