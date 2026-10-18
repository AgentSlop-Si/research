# Selected triangular-chirp convolution: constructive routing and exact compression limits

## Outcome

No sub-`N log N` algorithm is obtained. The constructive block route below is fully charged and still costs `Theta(N log N)`. The useful refinements are:

1. The marker set is a union of equal contiguous blocks, with a header mask of size `N^o(1)` at the accepted parameter choice. This makes the address structure substantially smaller than the transform itself.
2. The natural block factorization does **not** gain the output-density factor on its long transforms: it first performs `Q` complete transforms of length `B=N/Q`, costing `N log B = N(n-O(L))` work.
3. A single simplest marker gives a stronger ordinary-packet-graph obstruction: all `N` packet nodes occur at every depth through `n-2b-1`. Thus at least `N(n-2b-1)` non-input nodes are required, without using the positive-density lemma.
4. Exact compression shortcuts have explicit rank limits: the complete chirp window has Hankel rank `N`; a natural binary-digit unfolding has rank `2^min(k,n-k)`; and closing the first-order chirp recurrence after convolution produces an `N`-dimensional modulation orbit.

The last three statements concern precisely stated representations or algorithms. They are not universal Fourier or selected-convolution circuit lower bounds. There is no novelty or near-breakthrough claim.

## 1. Interface, model, and inspected input

The report `normalized_packet_escape_0358/NORMALIZED_PACKET_ESCAPE.md` was read in full. No predecessor program was executed or imported. Its setup is retained:

- `N=2^n`, `L=2^(b-1)`, `b>=7`, `L+2b<=n`;
- asymptotically `b=floor(log2(n/(4 ln n)))`, hence `L=Theta(n/ln n)`;
- selected labels at depths `h in [n-L,n]` have most-significant-bit pattern `0^b rev_t(k) 0^b [free bits]`, where `1<=t<=L`, `h>=2b+t`, and `k` starts and ends in `1` and avoids `0^b`;
- `E` is the union of their low-bit frequency cylinders;
- the high-time normalized packet bank and `F_unitary x |_E` interconvert in paid `O(NL)` work with `O(N)` storage.

The exact scalar model is a field containing the given primitive `N`th root `omega` and `1/sqrt(2)`. A scalar addition, subtraction, multiplication by a prepared field constant, and a scalar read/write count as operations. Address words have `O(n)` bits and are charged. Input scalars are arbitrary. Packing several input values into an uncharged wide scalar/word is not permitted. All tables used below are prepared and charged. The constructive Fourier implementation uses only roots that are powers of `omega`, so no root extension is hidden.

This is **not** a bit-complexity theorem. Exact complex scalars are idealized field elements; an algebraic-number or finite-precision realization must additionally pay representation and arithmetic costs. In particular, `Q(omega)` can have degree `N/2`; exact field operations cannot simply be declared constant-time bit operations. No new finite-precision accuracy claim is made.

## 2. A small header mask for a large set of outputs

Let

    K = min(n, 2L+2b), Q=2^K, B=2^(n-K).

Every selected-prefix condition inspects only bit positions at least

    h-(2b+t) >= n-L-2b-L = n-(2L+2b).

Cylinder extension above bit `h` does not impose any additional condition. Consequently there is an explicit `A subset {0,...,Q-1}` such that

    E = {Bv+u : v in A, 0<=u<B}.                               (1)

This is an exact statement about the union, not only a contained subset. One obtains `A` by testing each header `v`, with all lower bits set to zero, against the allowed high-depth prefixes. Equivalently a pattern automaton can recognize it. The uncomplicated enumerative implementation tests at most `(L+1)L` choices of `(h,t)` and at most `2b+L` header bits per choice, hence costs `O(Q K^3)` charged word work and `O(Q+K)` storage. At the accepted asymptotic choice,

    K=Theta(n/ln n),  Q K^3 = N^o(1) = o(N).

This removes mask preparation as a potential asymptotic bottleneck. It does not shorten the linear forms associated with accepted words.

The density remains positive: the supplied proof gives `|A|/Q=|E|/N>=1/4096`. The representation does not imply a constant translate cover, an arithmetic subgroup, or a cheap Fourier bit permutation. No cover improvement is claimed here.

## 3. Fully charged block construction and the exact point where it stalls

Use (1), write the source index as `s=a+Qj`, and define

    z_a[u] = (1/sqrt(B)) sum_(j=0)^(B-1) x[a+Qj] (omega^Q)^(ju).

Then direct expansion of the Fourier exponent gives

    ybar[Bv+u] = (1/sqrt(Q)) sum_(a=0)^(Q-1)
                   (omega^B)^(av) omega^(au) z_a[u],   v in A.  (2)

The cross term `Qj Bv=N jv` disappears. This explicit derivation matters: swapping the roles of the high and low output digits would incorrectly put pruning in front of the expensive stage.

### Executable algorithm

1. Read and route the `N` input scalars into `Q` strided vectors of length `B`.
2. Compute their complete normalized `B`-point transforms, producing every `z_a[u]`.
3. Multiply each of these `N` values by `omega^(au)`.
4. For each `u`, compute the `Q`-point normalized transform of the resulting vector over `a`, retaining indices `v in A`.
5. Route those `m=|E|` values and apply the already-paid `O(NL)` conversion if the high-time packet bank is wanted.

A conservative implementation computes all the short transforms in step 4. Pruning them or applying a more elaborate automaton there can only reduce that step, which is already `O(NK)=o(Nn)`.

### Arithmetic and storage bill

A standard normalized radix-2 butterfly uses at most two additions and three scalar multiplications (one twiddle and two factors `1/sqrt(2)`). Such butterflies are counted even when a constant is trivial.

- Root table `1,omega,...,omega^(N-1)`: at most `N-1` multiplications, `O(N)` storage.
- Input reading/routing: `O(N)` word operations.
- Step 2: exactly `N(n-K)/2` radix-2 butterflies, plus their charged memory traffic.
- Step 3: at most `N` scalar multiplications.
- Conservative step 4: exactly `NK/2` butterflies.
- Header preparation: `O(QK^3)` word operations.
- Output selection/writes: `O(m)`.
- Optional packet conversion and explicit packet writes: `O(NL)`.
- Working storage, root table, selected outputs, and packet output: `O(N)` scalar/address words in total. An in-place transform or reusable scratch array avoids a separate copy per stage.

All transform roots are powers of the supplied `omega`; normalized butterflies use the supplied `1/sqrt(2)`. All multipliers can have modulus at most one. Thus this baseline also has a bounded-coefficient realization; it does not hide a large precomputed kernel-spectrum coefficient.

Before step 4 begins, step 2 alone has cost `Theta(N(n-K))=Theta(Nn)`. The hoped-for cost `O(NK+|E|(n-K))` is not the cost of (2). The long transforms produce the inputs to the short selected transforms, and arbitrary input data gives no permission to omit them.

This is a standard blocked Cooley--Tukey construction specialized and accounted for here, not a new fast algorithm. The primary [FFTW pruned-transform account](https://www.fftw.org/pruned.html) describes the same basic strided-transform/twiddle/output-combination structure. That source is used as context, not as a lower bound against all algorithms.

## 4. Nearly every ordinary packet level is forced by one marker

Take `t=1`, `k=1`, `h=n`. These values are valid under the assumed parameters. The selected full-depth frequencies include the aligned interval

    I = [2^(n-b-1), 2^(n-b-1)+2^(n-2b-1)).                    (3)

The prefix is exactly `0^b 1 0^b` and its remaining `n-2b-1` bits are free.

For every `0<=j<=n-2b-1`, projection of `I` modulo `2^j` is the whole residue set `{0,...,2^j-1}`. Applying the supplied ancestor lemma just to the full-depth outputs in `I` therefore gives every `(j,q,f)` packet node at that depth: `2^j` frequencies times `N/2^j` source residue classes, for `N` nodes.

There are at least

    N(n-2b-1)                                                  (4)

non-input nodes in the memoized backward closure. Counting a two-output butterfly as one gate divides this by at most two. Because `b=O(log n)`, this forces all but `O(log n)` ordinary packet layers.

This improves the earlier `N(n-L)/4096` graph-specific estimate and does not need density. It says nothing about a circuit that uses different intermediate linear forms or algebraically factors across those nodes without materializing them.

## 5. The fixed chirp does not have a short ordinary recurrence

Suppress the nonzero normalization, which does not affect ranks, and put

    g(t)=omega^(-t(t+1)/2),    -(N-1)<=t<=N-1.

The selected convolution operator is

    C[ell,s]=g(ell-s),    ell in E, 0<=s<N,

up to already-paid input/output diagonals and normalization.

### Full-window Hankel rank

Form the `N x N` matrix

    H[i,j]=g(i+j-(N-1)),    0<=i,j<N.

Since

    g(u+v)=g(u)g(v)omega^(-uv),

we have

    H[i,j]=[g(i)omega^(i(N-1))] * omega^(-ij) * g(j-(N-1)).     (5)

All diagonal factors are nonzero, and `(omega^(-ij))` is an invertible Fourier matrix. Therefore `rank(H)=N`.

If the full `2N-1`-entry window satisfied a homogeneous constant-coefficient linear recurrence of order `d<N` at every position where its terms fit in the window, each Hankel column from column `d` onward would be the same linear combination of its preceding `d` columns. That would force `rank(H)<=d`, a contradiction.

Consequences are narrowly stated:

- no homogeneous constant-coefficient recurrence of order below `N` generates this full window;
- no exact representation of the window as fewer than `N` pure geometric sequences is possible;
- repeated-root exponential-polynomial representations are likewise limited by their total recurrence order.

These statements do not forbid a variable-coefficient recurrence: one exists and generates the constants in linear work. They also do not lower-bound general convolution arithmetic complexity.

### Arbitrary selected rows and consecutive source columns

Diagonal chirp factors turn `C` into the Fourier submatrix `(omega^(ell s))`. For any distinct row indices `ell in E` and consecutive source columns `s0,...,s0+d-1`, the rank is

    min(|E|,d),                                                (6)

because, after a row scaling, this is a Vandermonde matrix on distinct nodes `omega^ell`. This proof deliberately uses consecutive columns: arbitrary minors of a composite-length Fourier matrix can be singular.

Thus routing all these outputs through `r` shared linear summaries of such a source block requires `r>=min(|E|,d)`. In particular, storing the entire answer after consuming the input requires at least `|E|` independent scalar summaries. That is a state-dimension limit, not an `N log N` arithmetic lower bound.

## 6. Why the first-order phase recurrence does not become a first-order convolution recurrence

The easy constant-generation recurrence is

    g(t+1)=omega^(-(t+1)) g(t).

For arbitrary input `a`, define `c_ell(a)=sum_s a_s g(ell-s)` and `Za` by `(Za)_s=omega^s a_s`. Then

    c_(ell+1)(a)=omega^(-(ell+1)) c_ell(Za).                    (7)

Dropping `Z` is an algebraic error. Repeated advancement creates the family

    R_r(a)=c_ell(Z^r a),   r=0,...,N-1.

Its coefficient matrix is `(omega^(rs) g(ell-s))`, a Fourier matrix times an invertible diagonal. The `N` forms are linearly independent. Any exact scheme that stores a fixed set of linear summaries and realizes the **entire modulation-closed family** from those summaries requires at least `N` summaries.

For a finite selected list of only `m` distinct outputs, row rank only gives the corresponding `m` requirement; it is not legitimate to demand all `N` states merely because a particular proposed implementation chooses global closure. Time-varying summaries, extra passes, other operations, or a completely different factorization are not excluded by (7).

The productive use of the order-one recurrence remains the inexpensive `O(N)` preparation of chirp constants. It does not supply free transforms of modulated copies of the original input.

## 7. A small recognizer for the mask is not a small linear weighted recognizer for the chirp

For `0<=t<N`, split its ordinary binary digits as `t=2^k a+d`, where `0<=a<2^(n-k)` and `0<=d<2^k`. The matrix of chirp values across this digit cut is

    G_k[a,d]=g(2^k a+d)
            =g(2^k a) g(d) (omega^(2^k))^(-ad).               (8)

The root `omega^(2^k)` has order `2^(n-k)`. The central matrix is Vandermonde, with distinct first columns until that order is reached. Therefore

    rank(G_k)=min(2^(n-k),2^k)=2^min(k,n-k).                   (9)

A linear weighted automaton (equivalently, a tensor-train factorization) reading these ordinary binary digits factors the prefix/suffix matrix through its state space at the cut. Its state width is at least this rank. In particular it needs width at least `2^floor(n/2)` at the middle cut.

This excludes the specific exact strategy of attaching a uniformly tiny linear-weight state to the small language recognizer and contracting away the convolution. It does not exclude nonlinear processing of constant indices, a different tensor ordering, approximate low-rank methods, or a circuit outside this finite-state representation. It also does not imply that **generating** the chirp requires large work: the ordinary scalar recurrence already generates it in `O(N)` time.

The distinction between exact rank and numerical compression matters. The primary [butterfly-factorization paper](https://arxiv.org/abs/1502.01379) concerns data-sparse approximations, while the primary [interpolative QFT matrix-product-operator paper](https://arxiv.org/abs/2404.03182) gives compression with controlled error. Their results are useful in their own accuracy models; they are not exact low-state representations of (8) for arbitrary inputs.

## 8. What remains open after these attempts

The original conditional estimate is unchanged:

    cost(high-time bank) <= T_E(N)+O(NL+N),

where `T_E` must be the fully charged exact selected-chirp-convolution cost. This report supplies neither `T_E=o(Nn)` nor a universal obstruction to it.

The concrete gaps are now more specific:

- Header-language recognition and output routing can already be prepared in `N^o(1)` work. Making those parts faster does not address the dominant bill.
- In the ordinary block factorization, the `Q` length-`B` input transforms must be bypassed or combined differently; merely pruning the short outer stage cannot do so.
- An exact constant-order kernel recurrence or polylogarithmic-width weighted binary automaton cannot supply the missing operation in the representations analyzed above.
- A proposed first-order convolution recurrence must pay for the independent input modulations it introduces.
- General linear circuits with different intermediates remain open. No extra constraint on their conditioning or unitary nature is silently assumed.
- A full-transform result would still require the separate early-time and causal-recovery obligations in the supplied report. No constant-size affine cover of `E` is established here.

Thus the present advance is a sharper constructive decomposition and a collection of exact, delimited rejection tests for tempting shortcuts, rather than a new fast Fourier algorithm.

## 9. Independent controls, replay, and preservation

`independent_selected_checks.py` is fresh standard-library Python. It reads no predecessor files and imports no predecessor implementations.

The exact finite controls use `GF(65537)` and verify primitive-root orders. They establish:

- 8 separately generated marker/header-set comparisons, interval inclusion, and all claimed full ancestor levels;
- 21 independently implemented blocked-transform cases, including their exact first-stage and total butterfly counts;
- 14 full Hankel/modulation-orbit rank cases across 7 sizes and 2 root embeddings;
- 24 binary-digit unfolding rank cases;
- negative controls detecting the omitted modulation in (7) and swapped output digits in (2).

The mask controls use explicitly smaller `b=1,2,3,4` to test the combinatorial identities at feasible sizes. They do not satisfy the report's asymptotic `b>=7` regime and are not evidence for the positive-density asymptotics. The symbolic arguments above, rather than modular testing, prove the characteristic-zero identities and ranks. The modular checks do not establish numerical conditioning or floating-point accuracy.

`EXACT_RUN.log`, `EXACT_REPLAY.log`, `FIRST_RUN_SNAPSHOT.json`, and `REPLAY_CHECK.log` document byte-identical replay. `SOURCE_MANIFEST.before.sha256` and `SOURCE_MANIFEST.after.sha256` cover every regular file in the supplied source directory and agree. `SHA256SUMS.txt` seals the report, verifier, and evidence; the seal is checked separately and does not include itself.

