# Three source-bound mathematical refinements: ALG-040, ALG-043, ALG-044

Date: 2026-10-16 UTC. Baseline: `AgentSlop-Si/research` commit `2e57c6f739cb676b81a698736b1dc4baa00865ae`.

## Disposition first

Three genuinely new bounded deductions are proved below, using the actual archived source definitions. No parent record is exhausted: **ALG-040, ALG-043 and ALG-044 all remain TO RESEARCH, priority 34**. No new record, priority change, novelty claim, production acceptance or faster complete Fourier algorithm is proposed. Only the explicitly named bounded obligations are completed.

1. **ALG-040:** the accepted fresh-source schedule has a square-root marker choice with `Theta(N sqrt(n))` work and words. This improves its source time at the cost of more space than the earlier `O(N log n)`-space choice. It is asymptotically optimal for the displayed source slot ledger. More importantly, the combined source/joint-recovery structural ledger is exactly `N(n+1)` for every legal marker length, so retuning the marker alone never makes that complete schedule sub-`Nn`.
2. **ALG-043:** the ordinary binary chirp unfolding has a flat nonzero singular spectrum, not merely full rank. A relative Frobenius error `delta` at the middle cut needs width at least `(1-delta^2) 2^floor(n/2)`. This closes the approximate-small-width escape for this specific kernel representation, without addressing different digit orders, changed representations or selected-output algorithms directly.
3. **ALG-044:** sparse-numerator plus rank-`k` correction has operator error at least `sqrt(max(0,1-st(k+1)^2/N))` against a flat unitary. Routed packets give `s=2,t=r^2,k<=K`. Unlike the earlier entrywise compatible-family bound, this operator bound does not lose its constant as the packet gain approaches one. It is not a normalized-Frobenius bound or an arithmetic lower bound.

## Sources and non-repetition

All three internal bodies were fetched in full at the pinned baseline. The current open-index and live overview cells were also read: their active actions were still generic source/interface comparisons, and none recorded these refinements. Recent indexed finalizations of the expressly excluded IDs were not reopened.

- ALG-040: [Independent marker-cut audit](https://github.com/AgentSlop-Si/research/blob/2e57c6f739cb676b81a698736b1dc4baa00865ae/math/archive/objects/ae/ae3357205b8a8b30b0057c07fbe4063038b8d5adbbffec871efb1eecfc82a209__INDEPENDENT_MARKER_CUT_AUDIT.md), especially §§5–6 and 9. Git blob SHA `b25eb789ad5464dde4664d8f074b93f978245927`.
- ALG-043: [Selected-convolution construction](https://github.com/AgentSlop-Si/research/blob/2e57c6f739cb676b81a698736b1dc4baa00865ae/math/archive/objects/73/73ecbac161e81d64951d26f86806cbfa03238425c6adae956922a7f3a8d35279__SELECTED_CONVOLUTION_CONSTRUCTION.md), especially §§5–8. Git blob SHA `a6a1425e846108fb72aacc6c16fe17297b9094aa`.
- ALG-044: [Routed-packet sealed research](https://github.com/AgentSlop-Si/research/blob/2e57c6f739cb676b81a698736b1dc4baa00865ae/math/archive/objects/79/797d92887fac2f37e758a91d82586584336aefac1c3fc33d63d9d8f28f8cbdbf__SEALED_RESEARCH.md), especially §§3–7. Git blob SHA `07ffb31d3422be29ac3d79c0e813f793ecd80778`.

Not repeated: the accepted marker identities and original asymptotic choice; the exact chirp Hankel and digit-unfolding ranks; the roots-of-unity packet identity; the exact sparse-plus-low-rank support obstruction; and the earlier `eta sqrt(1-t/N)` compatible-family error bound.

For classical context, [Tao's primary paper, arXiv:math/0308286v6](https://arxiv.org/pdf/math/0308286), pp. 1–2, derives the standard support-product inequality from Cauchy–Schwarz and Plancherel and states the stronger prime-order theorem. The new operator-error argument below is a direct restricted-energy application of that classical method. The prime additive theorem is not promoted to a uniform approximate bound. [FFTW's primary pruned-transform account](https://www.fftw.org/pruned.html) was read for the unchanged blocked-transform cost boundary. No claim of worldwide novelty follows from these limited comparisons.

## 1. ALG-040: the complete marker-choice tradeoff

### 1.1 Exact inherited quantities

Let `N=2^n`, `1<=b<n`, `x=2^b`, `d=n-b`, `r=N/x`. Let `a_b(j)` be the number of length-`j` binary words avoiding `0^b`. The retained set is the disjoint union of suffix-marker states and avoiding states, so

`m = r + a_b(n)`.

For marker ages `1<=h<=d`, the accepted layer size is

`e_h = 2^(d-h) a_b(h-1)`.

Set

`M_b(n)=sum_(h=1)^d h e_h`,  `|E|=sum_h e_h=N-m`.

The displayed source schedule pays dense retained-jet initialization `m(n+1)` and eliminated polynomial slots `M_b(n)`. Its work is bounded above by a constant times

`N + m(n+1) + M_b(n)`.

Each initialized or transferred scalar slot is charged. Consequently the same expression, up to constant factors and the separately linear setup, is also its structural work count. Two adjacent eliminated layers use `O(N)` slots; retained jets need `m(n+1)` slots. This concerns this specified executor, not every circuit for the source map.

The accepted exact moment bound and avoiding-word majorant give

`M_b(n) <= N(2x-b-2)`,

`a_b(n) <= 2N(1-1/(2x))^n <= 2N exp(-n/(2x))`.

Hence for every legal `b`, a sufficient charged work/storage envelope is

`W_source = O(N[1+(n+1)/x + 2(n+1)exp(-n/(2x)) + 2x])`,

`S_source = O(N[1+(n+1)/x + 2(n+1)exp(-n/(2x))])` words.

The original legal root/field, scalar-operation and address-word conventions remain unchanged. This is not a bit-cost claim.

### 1.2 A time-faster, space-larger legal choice

For `n>=16`, choose `b=floor((log2 n)/2)`; thus `sqrt(n)/2 < x <= sqrt(n)`. Both `b>=1` and `b<n` hold. The envelope has

`(n+1)/x=O(sqrt(n))`, `2x=O(sqrt(n))`,

`(n+1)exp(-n/(2x)) <= (n+1)exp(-sqrt(n)/2)=O(sqrt(n))`.

Therefore `W_source=O(N sqrt(n))` and `S_source=O(N sqrt(n))`. Conversely `m>=r=N/x` implies `m(n+1)>=N sqrt(n)`, so both the actual displayed dense-jet storage and its source work are `Theta(N sqrt(n))`.

This does **not** dominate the original choice. That choice gave `O(Nn/log n)` source work with `O(N log n)` words; the square-root choice buys faster source preparation with larger memory. If the original memory cap is mandatory, retain it and the associated unresolved sharing problem.

### 1.3 Optimality within the displayed source slot ledger

For every legal marker choice, the source slot ledger `H_b=m(n+1)+M_b(n)` is `Omega(N sqrt(n))` as `n` grows. This is schedule-specific.

If `x<=sqrt(n)`, the retained term alone proves it.

If `x>=2n`, a union bound shows `a_b(n)>=N(1-n/x)>=N/2`; therefore the retained term is at least `N(n+1)/2`.

It remains to consider `sqrt(n)<x<2n`. For `n>=16`, `b<log2(2n)<=n/2`, so `d>=n/2`. Put `H=min(x/2,d)`, an integer. Since `x<2n`, `H>=x/4`. For `1<=h<=H`, a union bound on an `(h-1)`-bit word gives

`a_b(h-1) >= 2^(h-1)(1-(h-1)/x) >= 2^(h-2)`.

(The last lower bound is also harmless for `h=1`.) Thus `e_h>=N/(4x)`, and

`M_b(n) >= [N/(4x)] sum_(h=1)^H h >= N H^2/(8x) >= N x/128 > N sqrt(n)/128`.

These cases establish the asserted schedule-specific optimum, attained by the square-root choice. No unrestricted source-computation lower bound is asserted.

### 1.4 Exact no-gain identity for marker retuning alone

The accepted joint inverse/recovery schedule has

`V_joint = sum_(h=1)^d e_h(n-h+1) = (n+1)(N-m)-M_b(n)`.

Consequently, for **every** legal marker length,

`m(n+1) + M_b(n) + V_joint = N(n+1)`.

This is an exact identity between displayed structural slot/visit ledgers. It is not an exact machine-instruction count. In the unchanged source-then-joint-recovery pipeline, these are paid stages, so selecting a different `b` cannot give sub-`Nn` total work. At the square-root choice the first two terms are `O(Nsqrt(n))`, and the joint term is `(1-o(1))Nn`.

### 1.5 Exact remaining obligation

A faster complete method must replace sharing/evaluation in the causal solve or combine source and recovery differently; marker retuning alone is exhausted. The source's concrete finite-field target remains an all-input paid batch for

`g_k = sum_(1<=t<=min(L,kappa)) C_t Q_r^t u_(k-b-t)`

on arbitrary retained coefficient vectors, together with a source-bound causal composition and complete output recovery. A bound on mask enumeration, source rank or the new source-only optimum does not provide that lemma. For the original complex, unnormalized complete target under bounded scalar multipliers, the inherited determinant boundary remains in force. No claim is made that finite-field circuits satisfy that determinant argument.

## 2. ALG-043: flat spectrum of the ordinary binary chirp cut

### 2.1 The precise representation

Specialize to complex roots of unity. Let `N=2^n`, `omega` be any primitive `N`th root, and

`g(t)=omega^(-t(t+1)/2)` for `0<=t<N`.

At the ordinary high/low binary cut `t=2^k a+d`, put `M=2^(n-k)`, `D=2^k`, so `MD=N`. The unfolding is

`G_k[a,d]=g(2^k a+d)`, `0<=a<M`, `0<=d<D`.

The source already established the factorization

`G_k[a,d]=g(2^k a) g(d) zeta^(-ad)`, `zeta=omega^(2^k)`.

Here `zeta` has order `M`. Both exterior diagonal matrices are unitary, so they preserve all singular values, not only rank.

### 2.2 Exact singular spectrum

Let `V[a,d]=zeta^(-ad)`.

If `D<=M`, distinct columns are distinct characters on the complete group of order `M`; summing their geometric progression gives `V*V=M I_D`.

If `D>=M`, then `M` divides `D`. The columns consist of `D/M` complete character periods, so `VV*=D I_M`.

Thus, in both cases, `G_k` has exactly `R=min(M,D)` nonzero singular values and each equals `sqrt(H)`, where `H=max(M,D)`. In particular `||G_k||_F^2=RH=N` and `||G_k||_2=sqrt(H)`.

### 2.3 Approximate width, with a self-contained rank argument

Let `B` have rank at most `w<R`. Let `P` project onto its column space, whose dimension is at most `w`. Since `(I-P)B=0`,

`||G_k-B||_F^2 >= ||(I-P)G_k||_F^2 >= H(R-w)`.

For the second inequality, `G_k G_k*` has `R` eigenvalues equal to `H` and the rest zero; a rank-`w` projection captures at most `wH` of its trace. This argument requires no assumption about the conditioning or entry magnitudes of `B`.

The bound is attained for a single cut by retaining any `w` singular directions. Therefore

`min_(rank B<=w) ||G_k-B||_F/||G_k||_F = sqrt(max(0,1-w/R))`.

If `w<R`, also `||G_k-B||_2/||G_k||_2 >=1`: on the `R`-dimensional right singular subspace there is a nonzero vector killed by `B`, and `G_k` multiplies its norm by `sqrt(H)`. The zero approximation attains relative operator error one.

Any linear weighted automaton or tensor train in this ordinary digit ordering factors the unfolding through its state at the cut. If its represented vector approximates the one-sided `g` window with relative Euclidean error at most `delta`, reshaping preserves that norm and its cut rank is at most its state width. Consequently

`width_k >= (1-delta^2) 2^min(k,n-k)`.

At the middle cut the necessary width is `(1-delta^2)2^floor(n/2)`. For every fixed `delta<1`, polylogarithmic middle width fails in this representation.

### 2.4 Boundaries and remaining lemma

This closes only the approximate-tiny-linear-state proposal for the **same ordinary binary chirp vector**. It does not assert an operator-error guarantee for a selected convolution algorithm, or identify kernel-entry error with selected-output error. It does not cover changed digit order, reparameterization, approximate QFT operators, nonlinear constant-index generation, changed intermediates, or algorithms that never approximate this vector through these states. The ordinary variable-coefficient recurrence still generates all constants in `O(N)` operations.

For a full `2N-1` chirp window, a necessary restriction can be stated if desired: relative Euclidean error `epsilon` over that window bounds error on this `N`-entry restriction by `epsilon sqrt((2N-1)/N)` in relative norm. Hence a factorization restricting to this ordering must have width at least `max(0,1-epsilon^2(2-1/N))R`. No converse is asserted.

The exact faster selected-output cost `T_E(N)=o(Nn)`, with all input work, preparation, routing and output charged, remains missing. The accepted blocked construction still pays `N(n-K)/2` long-transform butterflies before selecting the short outputs. A new algorithm must change those intermediates or provide a separately justified representation; this spectral result is no unrestricted circuit lower bound.

## 3. ALG-044: robust sparse-inverse plus low-rank correction

### 3.1 General statement

Let `U` be any `N`-by-`N` complex flat unitary. Let `Q` be invertible with at most `s` nonzeros per column, and let `A` have at most `t` nonzeros per column. Let `E` have rank at most integer `k`, `0<=k<N`. Define

`T=A Q^(-1)+E`.

Then

`||U-T||_2 >= sqrt(max(0,1-s t (k+1)^2/N))`.             (R)

This concerns the operator norm of the full linear map. It does not by itself give the same lower bound for normalized Frobenius error. There is no condition-number bound on `Q`, no gain bound on `A,E`, and no arithmetic-complexity assertion.

### 3.2 Proof

Choose any `k+1` coordinate columns. The corresponding restriction of `EQ` has rank at most `k`, so it has a nonzero kernel vector `v` supported on those coordinates. Put `z=Qv`. Invertibility gives `z!=0`, and column sparsity gives

`|supp z|<=s(k+1)`.

Also `EQv=0`, so

`Tz=Av`, with `|supp(Av)|<=t(k+1)`.

Let `S=supp(z)` and `J=supp(Av)`. For each output coordinate, Cauchy–Schwarz and flatness give

`|(Uz)_j|^2 <= |S| ||z||_2^2/N`.

Thus `||P_J Uz||_2^2 <= |J||S| ||z||_2^2/N`. Since `U` is unitary and `Av` vanishes outside `J`,

`||(U-T)z||_2^2 >= ||P_(J^c)Uz||_2^2 >= (1-|J||S|/N)||z||_2^2`.

Replace the right side by zero if negative and use the two support bounds. Dividing by `||z||_2^2` proves (R).

The kernel must be taken in `EQ`, not in `E`; using `Ev=0` is generally wrong. If `Q` were singular, the constructed `z` might vanish, so that guard is essential.

### 3.3 Actual routed-packet specialization

The source's exact decomposition is

`T=M Q^(-1)+E`, `Q=I-a^r P^r`,

where `0<|a|<1`, `M` has at most `r^2` nonzeros per column and `rank E<=K=sum_i rank([R_i,P^r])`. Here `Q` is invertible and has at most two nonzeros per column. If `K<N`, (R) yields

`||U-T||_2 >= sqrt(max(0,1-2r^2(K+1)^2/N))`.           (P)

For `K>=N` the displayed right side is already zero, so the same harmless formula can be retained. The actual correction rank can replace the larger budget `K` for a stronger bound. If endpoints are diagonal on the left with a common commuting right route, use `t=r` instead of `r^2`.

For any desired operator error `delta<1`, the necessary budget is

`2r^2(K+1)^2 >= (1-delta^2)N`.

In particular, if `r(K+1)=o(sqrt(N))`, operator error is at least `1-o(1)` regardless of how closely `|a|` approaches one, provided the source's invertibility guard holds. When `K=0`, the source's existing `eta sqrt(1-r^2/N)` bound and the new `sqrt(1-2r^2/N)` bound are both valid; use their maximum. Neither uniformly dominates the other for every gain and support budget.

The source's earlier normalized-Frobenius statement retains its own `eta` factor. Removing that factor in (P) does not remove it from that other norm claim. The stronger exact prime-order support inequality also remains unchanged; its nonvanishing minors alone do not supply a uniform quantitative approximate version.

### 3.4 Remaining constructive obligation

A family attaining constant error below one must exit the new small-product budget, but high correction rank or large support does not make the arithmetic expensive by itself. The original exact all-output task still needs a uniform generator and a paid shared circuit for the genuinely noncommuting correction, or a different-denominator construction. It must verify actual Fourier identity, all preparation, input/output access and legal root/inverse guards. No such circuit is supplied here.

## 4. Verification, application and archival scope

`fresh_controls.py` is newly written from the formulas in this report. It does not import, execute, compile or AST-parse any historical program. Its exact integer and rational controls check the parameter ledger, character Gram identities, and witness-level robust inequality, including near-unit gains and negative controls. Finite checks support indexing and guards; the all-size claims rest on the proofs above. No floating-point experiment is used as a proof.

The accompanying proposals prepend only new current-action and pass/stop blocks to the existing `Research overview` cells `P202:Q202`, `P205:Q206`, preserving their full prior text. Status E, priority L, proof N and novelty O are untouched. Source links should be replaced with the immutable accepted report URL only after independent acceptance/publication; no unresolved placeholder may be written to the live sheet. A fresh exact-cell re-read is mandatory before later application.

No parent ID is proposed for archival. The exhausted **bounded activities** are marker-parameter-only optimization of this schedule, low-width approximation in the stated ordinary kernel ordering, and the small sparse-support/rank operator-approximation regime. Broader constructive and historical-attribution questions remain open. No external write was made by this work.
