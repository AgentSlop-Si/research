# Independent review: ALG-043 interleaved chirp cores

Review date: 2026-10-18 UTC.

Reviewed package: `retained-source-history/chirp_interleaved_20261018_1504`.

## Verdict

**PASS for the stated bounded gate.** The report proves the exact rank at every cut of its specified low/high interleaved digit order, supplies cores attaining those ranks, and pays their uniform preparation and address/storage costs in the inherited ideal scalar/address model. Its canonical-complex approximation statement is also valid as an existence/error consequence of classical TT-SVD. It is not a fast, certified approximation implementation.

There is no blocking mathematical or implementation defect. A minor provenance normalization is recorded below: each retained Markdown source adds one terminal newline to the upstream Git blob. The declared local SHA-256 hashes are accurate; the source text is otherwise identical.

ALG-043 must remain **TO RESEARCH, priority 34**. This review does not establish selected-convolution cost `T_E(N)=o(N log N)`, a faster Fourier algorithm, causal recovery, global optimality over bit permutations, numerical production readiness, or historical priority. No external write or source-package change was made.

## 1. Source identity and mathematical contract

I read the original selected-convolution source and the ALG-043 section of the accepted ordinary-order refinement. The source chirp is exactly

`N=2^n`, `g(t)=omega^(-t(t+1)/2)`.

Its exponent is an integer triangular number; it does not use an unprovided `2N`th root or division by two inside the field. The inherited field contains a supplied primitive `N`th root, and the original transform also supplies `1/sqrt(2)`, which this kernel representation does not need. For `n>=1`, a field containing the required root cannot have characteristic two. All exact statements are valid over any such field, including positive characteristic. Finite-field norms are not asserted.

The original source's section 7 explicitly limits its `2^min(k,n-k)` rank obstruction to an ordinary high/low digit cut and leaves other orderings open. The accepted refinement proves the flat spectrum only for that ordinary-order unfolding and likewise expressly excludes changed orders. Consequently the present result does not contradict either source.

The source bindings were checked locally. For both Markdown sources, removing exactly one final LF from the retained copy reproduces the listed upstream Git blob SHA:

- Accepted report: `c2d8c182413d44b32dccb83ebae906f291be66bd`
- Original selected convolution: `a6a1425e846108fb72aacc6c16fe17297b9094aa`

`INDEPENDENT_RESULTS.json` records both retained-copy SHA-256 values, the retained-copy Git-blob hashes, and this exact normalization. This is an editorial provenance note, not a failure of the source binding or a mathematical revision request.

## 2. Every-cut rank and width

At cut `k`, let `j=ceil(k/2)`, `h=floor(k/2)`, and `m=n-k`. A processed index is `p=a+b`, where `0<=a<2^j` and `2^(n-h)` divides `b`. The remaining index is `y=2^j c`, with `0<=c<2^m`. Since `j>=h`, the product `by` is divisible by `N`. Direct expansion of integer triangular exponents gives

`g(p+y)=g(p) g(y) omega^(-a y)`.

After nonzero row/column scaling, rows with different high-bit assignments but the same `a` are equal. The remaining matrix is

`V[a,c]=(omega^(2^j))^(-a c)`.

Set `R=min(2^j,2^m)`. The root `omega^(2^j)` has exact order `2^(n-j)`, and `R<=2^m<=2^(n-j)`. Thus the first `R` columns supply distinct Vandermonde nodes. The first `R` rows have powers `0,...,R-1`, so that square minor is invertible over the supplied field. Dimensions give the matching upper bound. This proves every claimed cut rank, including late cuts with repeated additional rows:

`r_k=2^min(ceil(k/2),n-k)`.

A TT bond factors the corresponding unfolding, so it cannot have smaller dimension. Maximizing the exponent gives `floor((n+1)/3)`, including all three residue classes of `n mod 3`. The `n=1` case has no internal cut; its single-core width is conventionally one. The explicit construction below simultaneously attains all internal ranks, so `W_n=2^floor((n+1)/3)` is exactly the minimum maximum width in this order. No claim about the best possible order follows.

## 3. Construction and exact coefficient recurrences

Let `s` be the first stage with `ceil(s/2)>=n-s`.

Before the bridge, the state records the processed low-bit integer `a`. When reading position `p` and bit `x`, multiplying by `g(2^p x) omega^(-a 2^p x)` pays the full new interaction. Earlier high-bit products with a newly read low bit are multiples of `N`; products of earlier and new high bits are also multiples of `N`. Therefore the running coefficient is precisely the chirp of the entire processed partial integer. The absence of high bits from the stored state loses no unpaid interaction.

At the bridge, write `v=2^p x+y`. The entry `g(v) omega^(-a v)` completes the chirp. Earlier high bits again have trivial interaction with the entire remaining interval. The outgoing state names a full future digit assignment. Later unit selection cores consume that assignment in reading order. For a fixed complete input string, exactly one bridge assignment survives, so the contraction equals `g(t)` without relying on cancellation or division. The supplied Python indexing matches this order, including a bridge occurring on a high-bit stage, the `n=1` boundary, and all three residue classes of `n`.

The cold constants are also correct. With `q_p=omega^(-2^p)` and `c_p=g(2^p)`,

`q_(p+1)=q_p^2`, `c_(p+1)=c_p^2 q_(2p)`.

When the index is at least `n`, its `q` value is one. For the contiguous bridge integer `v=2^j c`, the ratio between successive chirp values is

`g(2^j(c+1))/g(2^j c)=c_j q_(2j)^c`.

The reported `G`, ratio, and `zeta` updates follow exactly. The bridge's inner geometric progression generates `g(v) omega^(-a v)` for consecutive `a`. No dense root table, chirp vector, inverse Vandermonde, SVD, or field extension is needed.

Root validation by `omega^N=1` and `omega^(N/2)!=1` is sufficient because `N` is a power of two. Field and root discovery are properly outside the supplied-input contract. The prime-field executable assumes its supplied modulus is prime and does not mislabel primality discovery as free.

## 4. Preparation, addresses, and storage

Let `P=2 sum_(k<s) r_(k-1)`, `B=2 r_(s-1) r_s`, and `S=sum_(k>s) r_(k-1)`. These are exactly the prefix, bridge, and suffix nonzero scalar slots. Writing `W=2^floor((n+1)/3)` yields the following sharper identities, which also establish the stated bound:

- `n=3q`: `s=2q`, `P=4W-6`, `B=2W^2`, `S=2W-2`, hence `M=2W^2+6W-8`
- `n=3q+1`: `s=2q+1`, `P=6W-6`, `B=2W^2`, `S=2W-2`, hence `M=2W^2+8W-8`
- `n=3q+2`: `s=2q+1`, `P=3W-6`, `B=W^2`, `S=2W-2`, hence `M=W^2+5W-8`

These include `n=1,2`. Thus the package's simpler `M<=2W^2+8W` bound is sound.

The exact reference multiplication count is

`7n + P + B + 6 r_s`.

Indeed, the two root powers cost `2n+3`, inversion by `omega^(N-1)` costs `2n`, and the `q,c` tables cost `3n-3`, totaling `7n`. Prefix construction pays `P`; the bridge pays one multiplication per entry plus three per each of its `2r_s` integer values. Even final progression updates, whose result is unused, are charged. My controls verify this exact formula rather than merely an asymptotic upper bound.

The index setup is linear in its explicit size. The future subset-sum list doubles at each added digit, so its cumulative writes form a geometric sum. There are `r_s` final subset sums and `2r_s` mapping entries. Each mapping entry contains a constant-size pair of indices; each sparse core entry has a constant-size index triple. Consequently the reported number of mapping entries is not a bit count or a literal count of every individual machine word, but it supports the stated `O(n+M)` address bound. Order arrays, stage metadata, powers, shifts, loop counters, and transient subset-list storage fit the same bound. Addresses and exponents use `O(n)` bits as stipulated.

The Python dictionary is a convenient finite checker, not a worst-case RAM implementation certificate. This does not defeat the mathematical construction: sparse tuples can be generated sequentially without dictionary lookups, or dense core arrays can be used. Dense core dimensions have geometric square sums and also require `O(W^2)` words and initialization. Thus no expected-time hash-table assumption is needed for the theorem.

Since `n+W^2=O(N^(2/3))`, the claimed uniform ideal-field/address preparation and storage bound follows. It is not a bit-complexity theorem. Selecting one entry has a known unique path and costs `O(n)`; writing the full vector still costs at least its `N` outputs and can use the original `O(N)` recurrence.

## 5. Canonical-complex approximation

For `omega=exp(±2 pi i/N)`, the only residual phase at a cut is `exp(∓2 pi i a y/N)`. The actual integer ranges imply

`0<=a y/N<2^(j-h)<=2`.

The real phase magnitude is therefore below `4 pi`. The order-`R` integral Taylor remainder of the exponential along this real phase has absolute value at most `(4 pi)^R/R!`; an extra `exp(4 pi)` factor is not needed because the derivative of the imaginary exponential has modulus one. The first `R` terms are separated powers of `a` and `y`, so they produce a rank-at-most-`R` cut approximation. The outer chirp factors have modulus one. Each unfolding has exactly `N` entries, giving Frobenius error at most `sqrt(N) (4 pi)^R/R!`.

I independently opened the primary [Oseledets 2011 paper](https://users.math.msu.edu/users/iwenmark/Teaching/CMSE890/TENSOR_oseledets2011.pdf), Theorem 2.2, printed pages 2299–2300. It supplies the simultaneous TT approximation with squared error bounded by the sum of the unfolding squared error bounds. Dividing by `||g||_2=sqrt(N)` gives exactly the reported sufficient condition

`sqrt(n-1) (4 pi)^R/R! <= epsilon`.

Capping bonds by their exact dimensions is legitimate. The complex formulation uses the usual unitary SVD version of the same argument. The rational certificates with `pi<22/7` pass exactly: the first passing degrees under that rational test are 46 for `n=18,30,64,128` and 47 for `n=1024`, all at `epsilon=10^-6`. For `n=30`, exact interleaved width is 1024 and ordinary middle width is 32768. The factorial estimate also supports the stated asymptotic sufficient rank.

These statements do not provide paid fast preparation of approximate cores, rounding certification, numerical stability, operator-norm error, or selected-output error. For another odd root embedding represented by `u`, the same elementary bound replaces `4 pi` by `4 pi |u|`; the uniform canonical constant is not asserted there. The package maintains all these distinctions correctly.

## 6. Full window and remaining interface

The integer exponent difference between `g(t+N)` and `g(t)` is congruent to `N/2` modulo `N`, giving `g(t+N)=-g(t)` for even `N`. This sign reconstructs the full negative-to-positive window from the one-sided kernel, while explicit output remains charged.

A low-rank representation of a fixed kernel vector does not yet implement convolution with arbitrary input. The required difference `ell-s`, carries/borrows, summation, selected mask, data-dependent input representation, and output recovery remain unpaid by this result. The report correctly leaves this interface unresolved. The prior ordinary-order lower bound and the new changed-order representation can both be true.

## 7. Independent execution evidence

The fresh `independent_controls.py` imports only the submitted constructor as a target under test. It does not import or run the submitted checker or any historical implementation. Direct formula coefficients, a separately defined digit permutation, exact Gauss-Jordan ranks, unique-path evaluation, full TT contraction, exact ledger formulas, and source-byte checks are independently implemented.

Results:

- 154 constructor/root instances across primes 3, 5, 17, 97, 257, 12289, and 65537, with varied odd embeddings, through `n=16`
- 39,018 individually checked core coefficients
- 84,274 direct entry reconstructions; exhaustive through `n=12`, deterministic samples for larger cases
- 6,390 full TT contractions, exhaustive in the selected `n<=8` instances
- 140 full-unfolding ranks and 20,632 exact cut-factorization entries
- 84,274 full-window antiperiodicity checks
- 154 exact multiplication/storage ledgers
- 1,000 integer rank-profile, width, sparse-slot, and dense-storage controls
- Six negative controls, including nonprimitive roots, omitted interaction, and an improper ordinary-order width transfer
- Five exact rational approximation-degree certificates

The largest prepared case has `n=16`, width 32, 2,296 scalar core slots, and exactly 2,538 charged modular multiplications. Two independent executions produced byte-identical result JSON. All regular-file hashes of the supplied package are unchanged before and after review. The package's own `SHA256SUMS` also passed verification.

The controls are indexing and implementation evidence, not substitutes for the all-size field proof or the complex approximation proof. The preservation files, execution logs, source-normalization details, and this review are sealed in `SHA256SUMS`.
