# Exact grouped Mersenne-prime radix experiment

2026-10-15. This experiment implements the user's precise representation: p=2^m-1 prime, grouped base Q=p^d. It is separate from arithmetic-progression Newton bases. No asymptotic speedup has been established.

## Exact bit-fold conversion

For x=A·2^m+B, 0<=B<2^m, the identity

    x=A p+(A+B)

gives exact quotient and remainder computation with shifts/additions. Repeatedly replace x by A+B while adding A to the accumulated quotient; finish with one subtraction if the remaining value is p. This computes divmod by p, not merely a residue. Repeating it d times obtains one base-p^d digit. Reconstruction uses multiply-by-p as (x<<m)-x, d times per grouped digit.

Thus the all-ones pattern is genuinely used. Primality is not required for these conversion identities. The current sequential conversion is a correctness/control implementation: repeated scans of shrinking long integers can remain quadratic. The ledger records those scans, rather than treating a shift or arbitrary-width addition as constant bit cost.

## What grouping changes

Let w=log2 Q=d log2 p. An N-bit operand has about L=ceil(N/w) grouped digits. An ordinary product coefficient has bound

    |c_j| <= L(Q-1)^2,

requiring about 2w+log2 L bits before carrying. Reshaping those L digits into an M-by-M matrix with M²≈L reduces visible dimensions, but each entry retains w bits and its intermediate products/carries are wider. Constant-cost scalars cannot be assumed.

Q is not the m*d-bit all-ones word: for p=7,d=2, Q=49=110001₂, whereas2^6-1=63. Multiplying by Q can nevertheless use d shift/subtract steps, or its explicit binomial expansion, with those steps and coefficient widths charged.

## Three distinct uses of p^d

1. Radix Q=p^d: exact positional grouping, implemented here. Arithmetic can use other exact convolution moduli. This use is not prohibited by any root observation below.
2. Residue ring Z/(p^d): for odd prime p, the unit group has order p^(d-1)(p-1). For a Mersenne prime with m>=2, p-1 has exactly one factor2. Hence there is no unit of order4 or any larger power of two. Merely increasing d does not create long radix-2 NTT roots in this ring.
3. Extension field F_(p^d): different arithmetic, with d field coordinates and an irreducible-polynomial representation. Its operations and reconstruction cannot be billed as single base-p operations. This experiment does not implement that alternative.

The group-order fact is standard; primary reference: Trinity College Dublin course notes, section4.2, https://www.maths.tcd.ie/pub/Maths/Courseware/428/Primes-II.pdf . The no-order4 conclusion follows immediately from Lagrange's theorem. It is not a lower bound against arbitrary transforms or this radix representation.

## Implementation and evidence

check.py tests exact folding/grouping, canonical digit carrying and reconstruction. Candidate control products use explicit shift/add arithmetic. It checks375 full products,375 roundtrips and215 exact divisions, plus small prime-power no-order4 controls. Ordinary multiplication in assertions is an oracle.

benchmark.py attaches the representation to the same conventional exact radix-2 NTT/CRT backend used by the binary-radix comparator. It searches m,d choices under the three-prime capacity bound, rather than hiding larger coefficients. This is an engineering comparison of representations, not a new transform algorithm. Native modular multiplication, coefficient division, CRT and reconstruction all appear in measured execution. Input arrays are preselected; ingestion is excluded. Root/setup calculations run inside each measured convolution.

The benchmark uses three-run medians of complete conversion+convolution+carry+reconstruction. It is pure Python and does not claim to beat optimized FFT/NTT libraries. The independent proof-team status of earlier packets does not extend to this root-authored experiment. Only the separately described tests and algebra apply.

No GitHub or spreadsheet update is claimed.

## Completed bounded parameter sweep

An initial wider sweep was interrupted before completion because sequential bit-fold conversion was taking too long; it yields no reported timing result. The completed sweep uses input lengths256,1024,2048, Mersenne exponents3,5,7,13,17,19 and grouping d in1,2,4 subject to m*d<=40, compared with binary widths4,8,12,16,20,24,32,40. Each setting uses three complete timed runs and exact output checks. The reported best is only among tested settings.

Best complete medians (milliseconds):

| Input bits | Mersenne-prime-power | Binary radix, same NTT/CRT backend |
|---:|---:|---:|
|256|0.221|0.156|
|1024|1.650|0.596|
|2048|5.905|1.239|

The best tested Mersenne settings were p=2^19-1,d=2. At2048 bits conversion alone was4.519ms, convolution1.250ms, and carry/reconstruction0.087ms. Both winning representations used128 NTT points and three primes: grouping did not reduce the transform work versus the tuned binary comparator.

This is a measured failure of this sequential Python bit-fold implementation to win end-to-end, not proof that every p^d construction is slow. The next necessary improvement is a genuinely cheaper conversion/carry or matrix kernel while preserving the full width invoice. It does not justify switching to a different multibase representation.

## Grouped folding improvement on the exact requested base

For d=2, Q=(2^m-1)^2=2^(2m)-2^(m+1)+1. Split x=A·2^(2m)+B. Then

    x=AQ+[B+(A<<(m+1))-A].

Repeated folding therefore computes exact divmod by Q directly with one shift/subtraction correction per fold, instead of extracting two separate base-p digits. This stays on the precise p^d representation. General d uses the paid binomial expansion of 2^(md)-Q; only d=2 has the particularly simple correction above. The final remainder is reduced below Q and each accumulated quotient contribution is exact.

Additional210 division/roundtrip controls pass. A separate matched38-bit-block comparison uses p=2^19-1,d=2, five complete runs per method, and identical inputs/backend:

| Bits | Sequential p folding, ms | Direct p² folding, ms | Binary base2^38, ms |
|---:|---:|---:|---:|
|256|0.261|0.201|0.155|
|1024|1.774|1.046|0.619|
|2048|6.477|3.487|1.266|
|8192|133.863|77.032|6.614|

The new fold improves this implementation but still loses to binary conversion end-to-end. At8192 bits both representations use512 NTT points, three primes and20,736 butterflies; the Mersenne representation's conversion is still dominant. These are bounded pure-Python measurements, not an asymptotic comparison, global parameter optimum, or fastest-library benchmark.

Files: grouped_fold.py, test_grouped.py, compare_grouped_full.py and their JSON results. The complete convolution benchmark uses native divmod for coefficient carrying; the separate check.py control uses repeated exact Mersenne folding for those carries. Both charge the executed operations in their respective ledgers/timings; no claim that every stage uses only bit tricks is made.
