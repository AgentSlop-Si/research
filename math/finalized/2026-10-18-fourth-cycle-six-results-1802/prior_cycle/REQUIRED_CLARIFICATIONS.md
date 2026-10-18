# Qualifications required whenever these outcomes are summarized

## Correlated precision: mandatory summary correction

Ordinary integer-point interpolation needs exactly v2((2L−2)!) guard bits for arbitrary degree-at-most-(2L−2) integer polynomials; this is sufficient for the product service, with canonical-factor sharpness proved here only for sufficiently large H.

The source REPORT.md already contains the sufficiently-large-H hypothesis; its original README is preserved as historical evidence and must not be quoted without this correction. The review's SMALL_WIDTH_SCOPE_COUNTERCONTROL.json proves the explicit H=1, L=4 exception: canonical products require guard 3 although Gamma(6)=4. General-polynomial guard optimality does not establish optimality on the smaller bounded m-bit original-chunk Taylor image; only sufficiency is established there.

The 2L scalar-product lower bound is for L>=3 over Z/(2^H), with fixed separated-input ring-linear forms and fixed ring-linear reconstruction; it also holds on the bounded Taylor image by basis-pair identities. It excludes precision-changing division by powers of two, nonlinear digit/carry reconstruction, extension-ring products and arbitrary mixed-input circuits. Six products attain the lower bound at L=3; exact scalar rank at L>=4 is not settled.

The delivered 2L−1-product service uses extra precision and pays evaluation, all products, finite-difference interpolation, odd division, Taylor conversion, full coefficient arrays, carries, and outputs. The complete Karatsuba-backed route remains Theta_charge(N^alpha/L^(alpha−1)) in its product term, alpha=log2(3); it is not a general little-o multiplier. Its recursively reused small-L leaf-volume obstruction concerns the stated fully expanded schedule and uniform charge, not all multiplication algorithms or the unresolved odd native Q_s interface. Preserve the accepted source's general non-backend storage O(L(H+t+g)), g=ceil(log2 L), plus backend workspace; shorter specialized bounds retain their stated width hypotheses.

## Degree twenty-three: physical banks, GMP and continuation

Thirteen is the transform length; twenty-three is the extension degree. The field order uses 132 bits. The original free-cross-singleton grammar, arbitrary legal beta/raw weights and inherited universal lower theorem are essential. B(F_(53^23))=16 uses allocation (7,1,1,7). Physical banks are not scalar-operation counts. The inherited lower minor was not recomputed in this cycle, and first-split search minimality was not independently reexecuted. Transfer to degrees divisible by 23 is valid; the sufficient divisor list is not an iff classification.

All active field order/exponent/inverse/split/square-root paths use GMP mpz_class. The previous uint128 continuation warning is resolved for this witness. The next residual degree is 29. Its independent packed convolution needs at least 17-bit slots or ordinary convolution because 29*52²=78416>65535; coefficient-reduction bounds must be reassessed. GMP exponent representation itself remains suitable. Local verification of prior source receipts is not a fresh remote read.

## Mixed-prime rank three and N=1859

For distinct primes 5<=p<q, rank(F_(pq²)[R,C])<=3 implies min(a,b)<=4q OR max(a,b)<=max(6p,3p+2q−2,3q). Preserve this dichotomy; it does not give unconditional min(a,b)<=4q. At p=11,q=13 it is min(a,b)<=52 OR max(a,b)<=66.

For prime q>11, exact endpoint-incidence cost at N=11q² is 132q³. Every optimizer has exactly N full subgroup-coset × annihilator-coset rank-one tiles of unordered side sizes {q,11q}. The higher-rank-area penalty 1/(44q) is valid and is not claimed sharp. All ranks and phases are complex. The objective sums r(a+b) over a disjoint no-sharing Cartesian partition of all entries. Root/coefficient preparation, storage and I/O remain separate; literal zero-initialized accumulation may add the inherited N additions. No unrestricted Fourier-circuit, finite-field, overlapping/shared or arbitrary-basis conclusion follows. The accepted domain union covers through 2196, with residual 2197=13³ at rank three. The uncertainty comparison is established mathematics, not a novelty assertion.

## Sparse entrywise stability and polynomial gaps

Use the complex unitary Fourier normalization, spectral norm, invertible approximants, and a simultaneous support cap on every inverse row; N>=2 and 1<=s<=N−1. Put d=N−s, q=s/N, a=sqrt(d/N). No condition-number restriction is imposed.

When no column-weight-d complementary mask is a scaled unitary, Delta_(N,s)² >= d/N + 1/[10N d^(phi(N)−1)]. The stronger radical bound is retained in the report. For N>=4 with 3 not dividing N, Delta_(N,N−3)² >= 3/N+1/(30N³). For odd N>=3, Delta_(N,N−2)² >= 2/N+1/(5N³). These are squared-error lower bounds, not exact nonsharp optima or optimal rates. Weight-two/three no-mask classifications are accepted inputs, not new classifications or fresh recomputations. Weight four, general composite budgets and the broader owner remain open.

## Dyadic norm transfer and sixteen-point chirp

The grammar uses individually invertible pure-shift resolvents, arbitrary integer strides, and interspersed nonzero scalar Weyl-monomial gauges, with the literal full chirp target. Arbitrary diagonal gauges, additive branches, selected-output weakening and target changes are excluded. Factorwise poles use alpha^(N/gcd(N,s)) != 1.

For N=2^m>=4, norm descent gives L+e factors at N/2, e the number of even strides. Iteration pays multiplicity 2^min(v2(s),k). This is a mathematical reduction, not a free runtime operation. At N=16, every legal representation has at least six odd-stride factors; the accepted eight-point minimum then excludes total length six. At least seven stages are required in characteristic zero and in characteristic 17 with zeta²=3.

Fifteen stages suffice over C, over the stated finite splitting extension of Q(zeta), and over F_(17^12) in the stated characteristic-17 setting. Attainment over unextended Q(zeta) is not claimed. The result is 7 <= minimum <= 15, not an exact sixteen-point minimum. Certificate identities and the projective reduction justify the characteristic-zero transfer; finite search alone would not. Coefficient discovery, bit cost, numerical conditioning, implementation cost and FFT speed are not bounded by this stage theorem.

## Interleaved chirp representation and approximation

The exact kernel is g(t)=omega^(−t(t+1)/2), N=2^n, with integer triangular exponent and a supplied primitive Nth root. The order is specifically (0,n−1,1,n−2,...). Exact results hold over any containing field; characteristic two is automatically excluded for N>=2. The exact width is optimal in this order only, not among all permutations.

The explicit construction prepares O(n+W²)=O(N^(2/3)) ideal field/coefficient-address work and storage, including root checks, coefficient preparation, maps and core writes. Addresses have O(n) bits. This is not bit complexity. Dictionary use in the finite Python checker does not certify worst-case host operation cost; sequential sparse tuples or dense O(W²) arrays support the mathematical bound. Root/field discovery is outside the supplied-input contract, and the checker assumes its supplied modulus is prime.

For canonical omega=exp(±2pi i/N), a width-R TT approximation exists with relative vector Euclidean error <=epsilon if sqrt(n−1)(4pi)^R/R!<=epsilon. The n=30, epsilon=10^-6 example gives sufficient R=46; exact interleaved width is 1024 and ordinary middle width 32768. This is a classical TT-SVD existence/error consequence, not a paid fast approximate-core constructor, stable rounding implementation, operator-error certificate, or selected-output-error bound. Other embeddings require their stated additional |u| factor; no finite-field norm assertion is made.

A compact fixed kernel does not settle convolution on arbitrary inputs. Subtraction/borrows, input representation, selected masks, contraction, recovery and output charges remain unresolved. Full vector/window output still pays its output size. ALG-043 remains TO RESEARCH, priority 34; no global ordering optimality or faster Fourier algorithm follows.

## Acceptance and provenance

Final acceptance binds original source bytes. Public-copy locator, private-snapshot and integrity-metadata changes are disclosed in COPY_BINDINGS.json. Original route manifests/checksum lists are retained where supplied; all final reports and exact scientific payloads remain bound. The interleaved Markdown source copies contain exactly one extra terminal LF relative to their upstream Git blobs; both copies are retained byte for byte, and the normalization is explicit in SOURCE_NORMALIZATION.json. Private raw research-register snapshots are replaced with original-byte/hash stubs, so historical statements that those records were retained verbatim describe the source packet, not the public replacement. No scientific work was rerun during packaging.
