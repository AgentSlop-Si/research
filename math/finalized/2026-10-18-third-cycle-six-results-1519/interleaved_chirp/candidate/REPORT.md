# ALG-043: a changed-bit-order chirp representation with exact paid cores

Date: 2026-10-18 UTC. Existing owner: **ALG-043**. Baseline repository commit: `b68c06608e61955365ebf5542e1ae18a321d143a`.

## Result and scope

For the actual one-sided triangular chirp

\[
N=2^n,\qquad g(t)=\omega^{-t(t+1)/2},\qquad 0\le t<N,
\]

read the binary digits in the low/high interleaving

\[
\pi=(0,n-1,1,n-2,2,n-3,\ldots).
\]

The exact rank at the cut after digit `k`, for `1<=k<n`, is

\[
\boxed{r_k=2^{\min(\lceil k/2\rceil,n-k)}}.
\]

Consequently the smallest possible maximum tensor-train (TT) width **in this specified order** is

\[
\boxed{W_n=2^{\lfloor(n+1)/3\rfloor}}.
\]

An explicit sparse-core constructor attains every one of these ranks simultaneously. It prepares at most `2 W_n^2+8 W_n` nonzero scalar core slots, with `O(n+W_n^2)=O(N^(2/3))` field/coefficient-address work and storage, including root checks and coefficient preparation. No `N`-entry root table, dense chirp array, matrix factorization or root extension is hidden.

There is a separate approximation consequence for the **canonical complex embedding** `omega=exp(±2 pi i/N)`: a width-`R` TT approximation with relative vector Euclidean error at most epsilon exists whenever

\[
\sqrt{n-1}\,(4\pi)^R/R!\le\epsilon.
\]

This is an existence/error statement obtained from explicit low-rank cut approximations and the classical TT-SVD theorem. It is not a certified fast approximation executor. In particular, for `n=30` and `epsilon=10^-6`, the rational certificate below gives width at most `46`, while exact width in this order is `1024` and exact ordinary-order middle width is `32768`.

This completes the chosen **changed-order exact kernel representation and its preparation** gate. It does not settle the original selected-convolution cost `T_E(N)=o(N log N)`, nor the Fourier, causal-recovery, numerical-production or historical-priority parents. ALG-043 remains open; no ID, status, priority, novelty, or census change is proposed. No external write was made.

## 1. Exact source and why this is a new gate

The original [selected-convolution construction](https://github.com/AgentSlop-Si/research/blob/b68c06608e61955365ebf5542e1ae18a321d143a/math/archive/objects/73/73ecbac161e81d64951d26f86806cbfa03238425c6adae956922a7f3a8d35279__SELECTED_CONVOLUTION_CONSTRUCTION.md), especially sections 5–8, defines precisely this chirp. Its section 7 proves the ordinary high/low digit-cut rank `2^min(k,n-k)` and expressly excludes changed tensor order from that obstruction. Git blob: `a6a1425e846108fb72aacc6c16fe17297b9094aa`.

The [accepted 16 October refinement, section 2](https://github.com/AgentSlop-Si/research/blob/324e5ad245c2c1f53b477140353565f8ced28d6b/math/finalized/2026-10-16-research-finalization-2101/source_obligations/REPORT.md) proves the ordinary-order flat singular spectrum and approximate-width floor. It expressly leaves different digit orders and changed intermediates outside its conclusion. Git blob: `c2d8c182413d44b32dccb83ebae906f291be66bd`.

Both complete bodies were read and retained under `sources/`. The current catalogue derivative contains ALG-043 at overview row 205, TO RESEARCH, priority 34. Its recorded gate and pass/stop are retained verbatim in `sources/CATALOGUE_ROW.json`. This work changes the digit order, proves exact attainability with a paid constructor, and identifies a genuine approximation escape; it does not repeat the accepted ordinary-order theorem.

The exact theorem works over **any field containing the supplied primitive `N`th root**. Characteristic two is automatically excluded for `N>=2`. The norm result is complex-only and has the additional embedding guard stated above. The ideal scalar/coefficient-address model is retained. Exact field work is not asserted to be bit work.

## 2. Exact ranks at every interleaved cut

At the cut after `k` digits, write

\[
j=\lceil k/2\rceil,\quad h=\lfloor k/2\rfloor,\quad m=n-k.
\]

The processed positions are the `j` lowest bits and `h` highest bits. Hence every processed partial integer has the unique form

\[
p=a+b,\quad 0\le a<2^j,\quad 2^{n-h}\mid b,
\]

where `b` ranges over all choices of the processed high bits. The unprocessed middle is

\[
y=2^j c,\qquad 0\le c<2^m.
\]

For all integers `u,v`, direct expansion of the integer exponent gives

\[
g(u+v)=g(u)g(v)\omega^{-uv}.
\]

Since `j>=h`, `b y` is divisible by `2^(n-h+j)`, hence by `N`. Therefore

\[
g(p+y)=g(p)g(y)\omega^{-ay}
       =g(p)g(2^j c)(\omega^{2^j})^{-ac}.                 \tag{1}
\]

All exterior factors are nonzero. After row/column rescaling, every high-bit assignment duplicates the same row indexed by `a`. The cut rank is exactly that of

\[
V[a,c]=\zeta^{-ac},\qquad
0\le a<2^j,\quad 0\le c<2^m,\quad \zeta=\omega^{2^j}.
\]

Set `R=min(2^j,2^m)`. Since `R<=2^m<=2^(n-j)`, the first `R` nodes `1,zeta^-1,...,zeta^-(R-1)` are distinct. The first `R` rows and columns form a Vandermonde matrix with nonzero determinant. Thus `rank V>=R`, while dimensions give the reverse inequality. This proves the asserted rank formula, including late cuts where some other rows may repeat modulo the order of zeta.

A TT in the selected order factors each unfolding through its corresponding bond; consequently its bond dimension is at least this cut rank. Maximizing `min(ceil(k/2),n-k)` gives `floor((n+1)/3)`: for `n=3q,3q+1,3q+2`, the maxima are respectively `q,q,q+1`. Section 3 supplies simultaneous attainability, without appealing to a generic decomposition algorithm.

This is **not** a minimum over all permutations of the bits. No such global ordering optimality is claimed.

## 3. Explicit exact cores

Let

\[
s=\min\{k\in\{1,\ldots,n\}:\lceil k/2\rceil\ge n-k\}.
\]

For `k<s`, the state stores only the processed low-bit integer `a`. For `k>=s`, it stores a complete assignment of the still-unprocessed bits, in their future reading order. The state counts are exactly the ranks in section 2.

### 3.1 Prefix cores, before the bridge

At digit `k<s`, put `p=pi[k]` using one-based stage numbering, and let `x` be its input bit. The transition coefficient is

\[
g(2^p x)\omega^{-a2^p x}.                                  \tag{2}
\]

If this is a low-bit stage, replace `a` by `a+2^p x`; at a high-bit stage retain `a`. Each state has two transitions.

To verify (2), maintain the invariant that the accumulated prefix coefficient is `g(u)` for the actual processed integer `u`. Every already processed high bit has trivial cross interaction with the next digit: for a new low bit the exponents sum to at least `n`, and for a new high bit its interaction with all earlier high bits is also a multiple of `N`. The cross factor is thus determined by the stored `a`. The identity preceding (1) proves the invariant by induction. No processed high-bit information is being discarded before its interaction is paid.

### 3.2 One dense bridge core

Immediately before stage `s`, let `a` be the stored low-bit integer. Given its bit `x` at position `p`, and a suffix assignment encoding the remaining integer `y`, write `v=2^p x+y`. The bridge entry is

\[
B[a,x,y]=g(v)\omega^{-av}.                                  \tag{3}
\]

Prior high bits have no cross interaction with any part of `v`, by the same divisibility argument as (1). Multiplying (3) by the accumulated prefix factor therefore gives the complete `g(t)`.

### 3.3 Suffix selection cores

Thereafter a state is a proposed future bit string. At each stage there is precisely one nonzero transition for each old state: accept its first bit, discard it, and give coefficient one. All inconsistent assignments vanish. At the final stage only the empty state remains.

For each fixed complete input digit string exactly one bridge suffix assignment survives. The contraction is therefore exactly `g(t)`, with no cancellation, division or conditioning hypothesis. At `n=1`, the bridge is the sole core and the same construction applies.

### 3.4 Scalar-slot count

Write `r_0=r_n=1`, and use the ranks already proved for the other bonds. The exact number of nonzero core entries is

\[
M_n=2\sum_{k=1}^{s-1}r_{k-1}
       +2r_{s-1}r_s
       +\sum_{k=s+1}^{n}r_{k-1}.                            \tag{4}
\]

Before the bridge, state powers of two double every two stages; afterwards they halve each stage. Their geometric sums give

\[
2\sum_{k<s}r_{k-1}<6W_n,\qquad
\sum_{k>s}r_{k-1}<2W_n,\qquad
2r_{s-1}r_s\le2W_n^2.
\]

Thus `M_n<=2W_n^2+8W_n`. This counts every nonzero core coefficient, including stored ones. Sparse index triples require the same order of address storage. Even dense core storage is `O(W_n^2)` by the corresponding geometric sums, but the reference stores sparse cores.

## 4. Cold coefficient preparation and complete representation ledger

The constructor receives `n`, the field operations and a supplied `omega` of order `2^n`. It can check `omega^N=1` and `omega^(N/2)!=1` by `O(n)` repeated-squaring multiplications. This is enough to certify the order because `N` is a power of two. Finding the field or the original root is not an uncharged part of the contract.

Prepare `omega^-1=omega^(N-1)` by repeated squaring. Define

\[
q_p=\omega^{-2^p},\quad q_p=1\ (p\ge n),\qquad c_p=g(2^p).
\]

The recurrences

\[
q_{p+1}=q_p^2,\qquad c_0=q_0,\qquad c_{p+1}=c_p^2q_{2p}
\]

prepare the needed `O(n)` constants with `O(n)` field multiplications and slots.

For a prefix core, enumerate the consecutive states `a`; generate `q_p^a` by a geometric progression. Formula (2) takes two charged multiplications per old state in the deliberately conservative reference, including the final progression update. Across prefix cores this is `O(W_n)`.

For the bridge put `j=ceil((s-1)/2)`. Before that stage the entire unprocessed integer has the form `v=2^j c`, with consecutive `0<=c<2^(n-s+1)`. Set

\[
G_c=g(2^j c),\quad z_c=q_j^c.
\]

Then `B=G_c z_c^a`, and

\[
G_0=z_0=1,\quad G_{c+1}=G_c\rho_c,\quad
\rho_0=c_j,\quad \rho_{c+1}=\rho_c q_{2j},\quad
z_{c+1}=z_c q_j.
\]

Enumerate `a` geometrically for each `c`. This costs one multiplication per bridge entry plus three per `c`, with all writes charged. Mapping `c` to the physical bit and future-order suffix state uses an explicitly prepared array of `2 r_s` entries, plus `r_s` subset sums. These subset sums are generated by doubling a list and adding the next bit weight, so preparation is linear in the number of entries; no full-`N` permutation table is needed.

Suffix cores require only their charged unit entries and index writes. Root guards, constants, index maps, all cores and all preparation therefore cost `O(n+M_n)=O(N^(2/3))` ideal field/coefficient-address operations and words. Address and exponent words have `O(n)` bits. All complex core coefficients have modulus one. No SVD, inverse Vandermonde, hidden root extension or scan of all `N` chirp values is used in this exact constructor.

`prepare_cores.py` implements these preparation recurrences over a supplied prime field and counts every modular multiplication, root-check multiplication, core slot, bridge-map slot and power/one-bit slot. It assumes the modulus is a supplied prime; primality discovery is outside the supplied-field contract. Python instruction counts, host memory, coefficient bit lengths and finite-precision certification are separate. In the largest executed case `n=11`, it writes 328 core coefficients, prepares 48 explicit bridge-map slots and 22 power/one-bit slots, and pays 471 modular multiplications including 25 root-guard multiplications, for each tested embedding.

The representation describes a fixed kernel, not an arbitrary input/output computation. Evaluating an isolated entry by its selected path costs `O(n)` reads and multiplications; the original direct chirp recurrence still produces the explicit full vector in `O(N)` work. If all `N` entries are requested, their `N` writes are paid. There is no faster full-vector-output claim.

## 5. Complex approximation escape in the canonical embedding

This section assumes `omega=exp(±2 pi i/N)`, `n>=2`, and `0<epsilon<1`. It does not apply a uniform constant to arbitrary odd root embeddings.

In (1), the residual interaction is `exp(∓2 pi i a y/N)`. The actual integer ranges give

\[
0\le ay/N <2^j 2^{n-h}/2^n=2^{j-h}\le2.
\]

Thus its real phase magnitude is less than `4 pi`, uniformly at every interleaved cut, regardless of `n`. Truncate its exponential series after `R` terms. For real phase `theta`, the integral Taylor remainder has absolute value at most `|theta|^R/R!`, because the relevant exponential derivative has modulus one. The truncated expression is a sum of `R` separated products of a function of `a` and a function of `y`. Multiplying by the exterior phases `g(p),g(y)` preserves that rank bound and its entrywise absolute error.

Each cut consequently has a rank-at-most-`R` approximation with Frobenius error at most

\[
\sqrt N\,(4\pi)^R/R!.
\]

The classical TT-SVD error theorem, [Oseledets, 2011, Theorem 2.2, printed pages 2299–2300](https://users.math.msu.edu/users/iwenmark/Teaching/CMSE890/TENSOR_oseledets2011.pdf), combines rank-bounded approximations to every unfolding into one TT. Its squared error is at most the sum of their squared Frobenius errors. Apply it to the `n` binary modes in the specified interleaved order. Since the target vector has squared norm `N`, the stated sufficient condition follows. Bond dimensions may be capped by the exact dimensions when smaller.

For an integer-only sufficient test use `pi<22/7` and check

\[
(n-1)(88/7)^{2R}\le\epsilon^2(R!)^2.                         \tag{5}
\]

The exact rational controls verify `R=46` for `epsilon=10^-6` and each of `n=18,30,64,128`, and `R=47` for `n=1024`. Asymptotically the sufficient width is `O(1+L/log(2+L))`, where `L=log(sqrt(n-1)/epsilon)`, by `R!>=(R/e)^R`. These bounds are sufficient, not optimal.

This is a special-function application of classical low-rank Taylor approximation and TT-SVD, without a novelty claim. A certified approximation implementation with paid rounding and a numerically stable preparation path is not delivered. Running ordinary full-array TT-SVD would itself require the full array and its costs. The finite modular constructor above tests the **exact** representation only, not this complex approximation.

For `omega=exp(2 pi i u/N)` with another odd integer representative `u`, the same argument has `4 pi |u|` in place of `4 pi`. The constant-46 example is not transferred to arbitrary embeddings or finite fields.

## 6. Full chirp window and the unresolved convolution interface

For even `N` and a primitive `N`th root,

\[
g(t+N)=-g(t),
\]

because the exponent difference is `Nt+N(N+1)/2`, congruent to `N/2` modulo `N`. Thus the full `-(N-1)..N-1` window is determined by this one-sided kernel and a sign. Explicit expansion still pays its `2N-1` outputs.

This does not make the convolution operator cheap. The desired entries involve `g(ell-s)` and arbitrary input coefficients. Subtraction, borrows, selected-output masks, summation over all source indices, and output recovery do not become free when the fixed vector has small TT ranks. No compatible low-rank representation of the arbitrary input or a paid contraction through that difference interface is proved. The original `T_E` gate remains open.

The accepted ordinary-order lower bound is not contradicted: digit permutation changes the unfolding ranks. Its flat-spectrum statement simply cannot be transferred to this new order. Conversely, the new vector-norm approximation is not an operator-norm or selected-output error certificate.

A precise possible next gate, if selected separately, is a full all-input contraction through the subtraction/borrow interface in this order, including the selected mask, preparation and output charges, or a model-matched obstruction to that contract. The present representation alone does not pre-approve a speed claim or a new research identity.

## 7. Fresh exact controls and reproducibility

`check_exact.py` imports only the newly written `prepare_cores.py`; it does not import, execute or modify historical implementations. It builds a second direct-formula core reference and compares all entries with the recurrence-based paid constructor.

Results in `CHECK_RESULTS.json`:

- 33 primitive-root/core instances: `n=1..11`, each in embeddings `u=1,3,5` over `GF(65537)`
- 2,832 scalar core entries compared exactly between the two constructors
- 12,282 complete input-digit contractions compared to the direct chirp formula
- 84 full-unfolding rank computations and 84 complete cut-factorization checks, `n<=8`
- 300 exact integer cut-profile, maximum-width and slot-bound checks, `n=1..300`
- Three negative controls: the ordinary-order width cannot use the new formula, dropping the cross phase fails, and a nonprimitive root is rejected
- Five exact rational Taylor-degree certificates using (5)

Finite modular checks do not prove characteristic-zero ranks or numerical error. Those conclusions follow from the all-size algebraic proof and the separate complex argument. The checks validate guards, indexing, constructor equality and the declared finite ledgers.

Run: `python check_exact.py`. Re-running produces byte-identical `CHECK_RESULTS.json`. File hashes, source bindings and the fresh execution receipt are retained alongside this report. Independent review is still required before any accepted catalogue update. No source file, catalogue cell, status, parent identity or repository content was changed by this worker.
