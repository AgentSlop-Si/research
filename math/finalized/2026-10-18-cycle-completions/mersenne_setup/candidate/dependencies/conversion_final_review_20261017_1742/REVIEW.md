# Independent final review of the Mersenne conversion candidate

Review date: 17 October 2026. Candidate: `mersenne_conversion_improvement_20261017_1728`. This review reads historical material only as text; no historical uploaded program was executed. Fresh controls execute only the inspected candidate and newly written independent checks.

## Verdict

The final candidate's exact conversion construction and stated arithmetic-core upper bounds are sound under their explicit assumptions. It supplies a genuine, non-triangular binary/base-p interface, signed quotient/carry propagation, canonical grouped conversion, and raw grouped readout. It does not prove sub-N-log-N multiplication or a runtime improvement over the attachment. No uncharged large-product oracle is hidden in the delivered arithmetic core.

Two review observations were corrected before the stable version was sealed:

1. A single canonical p^d digit now uses the actual digit width for validation and returns directly, rather than padding to an arbitrarily large d. The public grouped decoder also checks d >= 1.
2. Global recursive Karatsuba diagnostic counters are disabled by default. The report expressly excludes optional recursive instrumentation from the arithmetic-core bit bound; outer metadata is charged within the existing scan/setup terms.

## Verified mathematical points

### Exact odd-factorial shift

For s(i)=popcount(i), the valuation v2(i!)=i-s(i) gives the odd factorial u_i=i!/2^(i-s(i)). For 0<=i<n, s(i)<=K=ceil(log2 n), including n=1 with K=0. Thus every exponent K-s(i) used in the initial scaling is nonnegative.

For k=i-j, the valuation identity gives

2^(s(j)+K-s(i)+s(k)) u_i/(u_j u_k) = 2^K binom(i,j).

All odd denominators are invertible modulo 2^W. Consequently the reverse convolution and final diagonal multiplication recover 2^K times each exact signed Taylor-shift coefficient modulo 2^(H+K). The low K bits vanish; shifting those bits away recovers the coefficient modulo 2^H. Since the hockey-stick estimate bounds the absolute coefficient strictly below 2^(h+n)=2^(H-1), centered reconstruction is unambiguous. Both signs of the shift, zero coefficients, and n=0/1 cases are covered by the implementation.

The forward odd-factorial recurrence and reverse inverse recurrence are correct. Newton precision doubling inverts only odd values and uses the supplied multiplier. No even factorial is inverted and no full factorial is constructed.

### Convolution and complete costs

With b=8*ceil((2W+ceil(log2 n))/8), each unreduced convolution coefficient is strictly below n*2^(2W)<=2^b. Thus all slots are carry-free before reduction. The two argument capacities are S=nb, approximately 2nW bits, rather than merely the original input size. Bounded byte packing and extraction cost O(nW).

The ledger O(M(S)+n*M(W)+n*W*log(n+1)) accounts for the one packed product, two full-width diagonal maps, the inverse, and the short-factor prefix/reverse products. Here W=h+n+1+ceil(log2 n). The scalar products and same-scale packed product remain paid operations. The multiplication regularity assumptions suffice for precision doubling and the stated grouping aggregation.

For m=Omega(L), W=O(m), S=O(Lm), and all conversion arrays occupy O(N) bits for N=Lm. Canonical normalization and final carry tails are within O(L(m+L+log L)). The stated bound O(M(CN)+L*M(Cm)+N*log(L+1)) follows. The code's normal multiplication core is explicit Karatsuba with shift/add leaves, giving the stated O(N^(log2 3)) instantiation. Enabling optional recursive diagnostics is expressly outside that bound. Ordinary quadratic convolution in the control harness is a correctness test, not a claimed fast implementation of the attachment's matrix multiplication.

### Local quotient and signed carry

For B=2^m, p=B-1, 0<=r<p, and 0<=a<B, s=r+a lies in [0,2p-1]. With delta=[s>=p], q=r+delta and r'=s-delta*p satisfy rB+a=qp+r', 0<=q<B, and 0<=r'<p. Every quotient limb is emitted; this is exact division rather than remainder-only folding.

Magnitude division plus the stated negative adjustment implements floor division. For normalized coefficients the positional invariant proves exactness even with negative intermediate carries. A nonnegative represented value cannot have a negative final carry. The carry-height estimate and diminishing final tail justify the linear wide-digit normalization bound. The domain m>=2 is necessary for this stated interface; no p=1 claim is made.

### Binary, canonical, redundant, and grouped interfaces

B=p+1 proves the forward +1 shift, and p=B-1 proves the reverse -1 shift. Signed binary normalization correctly reconstructs every nonnegative represented value and rejects negative totals. Canonical p-digit counts can exceed binary chunk counts, and this is handled.

Polynomial substitution is multiplicative, so the lazy-carry conjugation identity is exact. The report properly requires enlarged matrix coefficient bounds and does not infer a new multiplication law from this identity.

Grouping canonical p-digits gives canonical p^d digits without dividing by p^d. The reverse decoder validates each group's canonical length. Raw signed grouped coefficients can be expanded independently and accumulated at offset jd. For canonical grouped products, the stated m=Omega(Gd) condition makes each expansion O(d) digits with bounded overlap; the sum of local and global costs is absorbed by the displayed bound. Correctness outside this wide-digit regime is supported without extending the asymptotic claim.

Primality is not used: all modular inversion takes place at powers of two on odd factorial parts, and the positional identities use only p=2^m-1. Composite Mersenne bases are valid.

## Prior-art audit

The attribution is appropriately narrow. These are classical ingredients combined for this interface, and the report disclaims historical priority for the combination.

- The [University of Maryland record](https://drum.lib.umd.edu/items/6c219ff5-0480-4c51-8a29-f50905e7309c) verifies the Tang–Duraiswami–Gumerov 2004 report and its structured Pascal-matrix algorithms.
- [Potter and Duraiswami, section 3.2, Theorem 2](https://arxiv.org/html/1711.08453v1#S3.SS2) gives the alpha^k/k! diagonal–Toeplitz factorization. Transposition and alpha=2 match the candidate's algebra. Floating-point stability claims are correctly separated from exact modular arithmetic.
- [Andreica, sections 7–8](https://onlinelibrary.wiley.com/doi/10.1155/2013/751358) covers odd factorial parts and separation of powers of two in modular binomial computation. It is not evidence for this candidate's batched-conversion cost. The original PDF fetch was unreliable during this review; the publisher text and [PMC copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC3856163/) identify the same article.
- [GMP factorial documentation](https://gmplib.org/manual/Factorial-Algorithm) confirms the established odd-part/final-shift technique; [GMP conversion documentation](https://gmplib.org/manual/Binary-to-Radix) confirms power-of-two extraction and recursive nonbinary division conversion.
- [Johansson's 26 February 2026 discussion](https://fredrikj.net/blog/2026/fast-nonbinary-arithmetic/#fast-radix-conversion) supports the conventional O(M(n) log n) divide-and-conquer conversion comparison. It is not a lower bound on all conversion algorithms.

## Execution and integrity evidence

`INDEPENDENT_RESULTS.json` records exact candidate-manifest and source-pin verification, reproduction of the complete saved control output, and additional independently seeded edge checks. `INDEPENDENT_RUN.log` is the execution output, and `independent_controls.py` is the fresh test driver. The inspected candidate code, report, and manifest are retained in this review directory to pin what was reviewed. Historical archive members were hashed and read only; they were never imported or executed.

The initial integrity check occurred while the author was applying the requested corrections and therefore detected a transient mismatch. That incomplete state was not accepted as a final artifact. The stable resealed candidate was then copied, rechecked, and tested.

## Remaining limitations

The factorial-Toeplitz convolution is still a same-scale general integer product, and the diagonal maps and O(N log L) setup remain explicit. The attachment's transform schedule and point-product recurrence remain separate obligations. The review validates a constructive conversion upper bound, not a sub-N-log-N multiplier, universal lower bound, practical speedup, or discovery of a growing Mersenne-prime family.
