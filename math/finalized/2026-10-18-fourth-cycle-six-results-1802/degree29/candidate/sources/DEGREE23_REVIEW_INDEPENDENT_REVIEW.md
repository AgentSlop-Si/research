# Independent final review: degree-twenty-three original Fourier-bank attainment

18 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**. No scientific correction is required for the sealed degree-twenty-three candidate. The previous review's unsigned-128 exponent warning is resolved by the active GMP implementation and independently checked boundary controls.

## Accepted conclusion

Fix N=13, q=16, characteristic 53, and the negative unnormalized Fourier target F[k,t]=16^(-kt). Let B(K) be the minimum physical-bank count in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation, allowing arbitrary legal beta and raw weights. The independently verified literal witness and inherited field-uniform lower theorem establish

    B(F_(53^23)) = 16.

The physical allocation is (7,1,1,7). All sixteen banks are nonzero, all guards are nonzero, and all 208 original inverse branches are legal. The two seven-node same-sign supports are non-Frobenius-stable, and both cross nodes are nonbase. Their equality in this witness is allowed by independently free cross parameters and is not imposed on the theorem's grammar.

Scalar extension proves the same equality whenever 23 divides d. Combined with the accepted attaining degrees 2,3,5,7,11,13,17,19, the sufficient divisor list is {2,3,5,7,11,13,17,19,23}, whose product is 223092870. Apart from the separately solved base case d=1, the residual degrees not covered by these attainments are d>1 coprime to that product; the least is 29. This is a sufficient coverage boundary, not an iff criterion or nonexistence claim at degree 29.

## 1. Sealed bytes and source provenance

Acceptance attaches to these exact candidate bytes:

- DEGREE23_LITERAL_CERTIFICATE.json SHA256: 083ec297a3fde29babcf2fe7a59abe9bc2c531d9ae91461a55b863b9b8858a4e.
- MANIFEST.json SHA256: 2cdb7fafbfd4e1338db3341bc1b27008c419e609253f43bd195bd7e7ce71bdf9.
- REPORT.md SHA256: 4242d6b1255afa6551d3a745fed2e323aa4a8aad4ebe52fe2fd22c8e68c9a0a2.
- OPERATION_LEDGER.md SHA256: ba5f0b0724964603a2483189950f77632d35e723df7de96e327ecd118b9e24f8.

All 52 candidate-manifest entries pass independent byte-length and SHA256 checks. All sixteen source pins pass byte-length, SHA256, Git blob SHA1, and byte-for-byte comparison with the original local source paths. CANDIDATE_BINDING.json records these checks. candidate_snapshot preserves the sealed artifact without compiler binaries or caches. The candidate's pending-external-review labels remain unchanged; this separate report supplies acceptance.

The accepted degree-nineteen report, verdict, arithmetic receipt, and manifest are explicitly pinned. The prior independent reviewer used below is bound to that accepted review manifest. Earlier retained immutable-GitHub responses for the inherited lower review, degree-eleven accepted review, and rank/chart report are independently matched to the current source bytes. This review performs no fresh remote read; the inherited response receipts are not represented as new fetches.

## 2. Independent field proof and arithmetic

The literal reviewer is a transparent adaptation of the degree-nineteen independent review method, whose source SHA256 is 3e86869cfd6c61af8767a52f989719e88078b902eb339d296fe45be5f67618f1. The exact prior source and adaptation program are retained. This is reuse of a prior independent method, not a claim that every line is newly authored. The mathematical checker reads inert certificate JSON and never imports or executes a candidate mathematical program.

Use K=F53[u]/(u^23+u+5), with basis 1,u,...,u^22. Every supplied element is required to contain exactly twenty-three canonical integer residues in 0,...,52. Ordinary prime-polynomial convolution and general long division establish, before any extension inverse,

    X^(53^23) = X mod (X^23+X+5),
    gcd(X^23+X+5, X^53-X) = 1.

Primality of 53 and 23 is checked. Since 23 is prime, divisibility by X^(53^23)-X confines irreducible factor degrees to 1 or 23; the gcd excludes degree 1, and total degree 23 forces irreducibility. The first polynomial is squarefree because X^(53^23)-X has derivative -1. All twenty-three Frobenius remainders are retained in ARITHMETIC.json.

The supplemental checker independently repeats the deterministic modulus search c=1,...,5. All final Frobenius remainders and gcds match FIELD_SEARCH.json; c=5 is the first irreducible member tested.

Extension multiplication uses carry-free integer convolution in radix 2^16, followed by reduction u^23=-u-5. The carry bound is 23*52^2=62,192<65,536. This arithmetic agrees with ordinary coefficient convolution followed by general polynomial division on all 529 ordered basis pairs and 100 deterministic dense pairs. Inversion uses polynomial extended Euclid and checks each result by multiplication. These methods differ from the candidate's coefficient-loop multiplication and exponentiation-based inverse.

The reviewer checks q=16 has exact order thirteen, all seven roots are distinct and nonzero, their linear factors multiply to the supplied degree-seven annihilator, and the actual bank supports agree with those roots and cross nodes. The annihilator has nonbase coefficients, the 53rd-power support differs from the stored support, and every support root and cross node has directly checked Frobenius orbit length exactly 23.

## 3. Original operator reconstruction

Every bank is literally

    (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1),

where S e_t=e_(t+1), T e_t=16^t e_t, and indices are modulo thirteen. Every supplied beta is one. For each bank, the reviewer recomputes and verifies the supplied guard Delta=1-alpha^13-1=-alpha^13, including nonvanishing.

For each bank and branch, define A=alpha S^epsilon+16^(epsilon*delta*j) T^delta. Starting from I, literal sparse left multiplication constructs every power through A^13. Every entry of A^13 is checked against (alpha^13+1)I. Then

    V = Delta^(-1)(I+A+...+A^12)

is constructed, and both (I-A)V=I and V(I-A)=I are checked entrywise using the actual shift and diagonal positions. This method differs from both the candidate's Gauss-Jordan inverse and its Python backward-recurrence inverse. The q-binomial identity is not trusted in place of the explicit power and inverse checks.

Each V is multiplied by its supplied raw branch weight and the original 1/13. Each resulting bank is nonzero. The total is compared directly with 16^(-kt) in all 169 positions, and only then with the certificate's claimed matrix. Consequently the result is an exact operator identity on every input vector over K.

Successful independent checks include:

- 208 matrix-power identities, comprising 35,152 scalar equalities.
- 208 branch inverses and 416 one-sided inverse identities, comprising 70,304 scalar equalities.
- 208 forward raw-weight transforms and 208 inverse amplitude transforms.
- Direct gamma=(1/13) sum_t 16^(-t^2)=7 and all 169 target Weyl coefficients.
- Independent extraction of all 2,704 bank Weyl coefficients.
- All 169 full actual-root sector equalities.
- Fresh sector ranks 13,9,11,12,13,13,13,13,13,13,12,11,9.
- All 169 negative-sign Fourier entries, with zero mismatches.

Negative controls give 169 mismatches when 1/13 is omitted, 144 for the opposite Fourier sign, and 91 after adding one to the final raw weight. Deterministic hashes of all complete inverse and bank matrices are retained. No necessary recurrence gate substitutes for the literal bank sum. No trace bank, quotient-algebra primitive, derivative, singular limit, or uncharged pre/post transform is introduced.

## 4. Resolution of the unsigned-128 boundary

The exact field order is

    Q = 4553496434179608203397220101976502751677,
    bit_length(Q) = 132.

It exceeds 2^128. The degree-nineteen review explicitly warned that changing only the degree and modulus would overflow its prior fixed-width exponent type. Inspection of the complete active degree-twenty-three sources confirms that ORDER, field powers, inversion, polynomial powers, Frobenius splitting, the square-root exponent, and recursive factorization exponents all use unbounded GMP mpz_class. No narrowing conversion or residual 128-bit exponent type appears in those active paths. uint64_t is retained for intentionally wrapping xorshift state and bounded counters, not extension exponents. The separate prime-field power routine uses bounded small integer exponents.

The three important order-derived exponents are

    Q-2     = 4553496434179608203397220101976502751675,
    (Q+3)/8 = 569187054272451025424652512747062843960,
    (Q-1)/2 = 2276748217089804101698610050988251375838.

All three exceed 2^128-1. Q=5 modulo 8 and 23^2=-1 modulo 53 are checked. The square-root implementation squares its proposed result before acceptance.

The independent supplemental checker recomputes the inert GMP probe output using the reviewer's integer-convolution arithmetic and Python unbounded integers. It verifies multiplication, the inverse against polynomial extended Euclid, ten field powers around 2^127 and 2^128 and at all relevant order-derived exponents, a known seven-root split polynomial, and four exact/truncated splitting or factorization polynomial powers. Six falsification controls independently detect a wrapped order, the 2^128 exponent wrapping to zero, a truncated inverse exponent, a truncated splitting order, a truncated square-root exponent, and a truncated factor exponent. The false inverse fails multiplication by its input, the false square root fails squaring, the false splitting remainder is not X, and the false factor-character values fail the required squares-to-one test.

Separately from the independent literal checker, a fresh temporary directory rebuilds the candidate's small GMP implementation probe with GNU C++17, -fsanitize=undefined, -fno-sanitize-recover=all, -lgmpxx, and -lgmp. Its output is byte-identical to the independently checked sealed ARITHMETIC_PROBE.json, with exit code zero and no sanitizer diagnostics. No candidate discovery search or candidate literal verifier is executed by this review. The candidate's own full-literal sanitizer and failed-prefix/first-hit replay receipts are source-bound evidence, not recast as independently rerun here.

For coefficient arithmetic, an unreduced convolution coefficient is at most 62,192. Sparse reduction gives the conservative signed bound 7*62,192=435,344, below signed 32-bit range. Terms reduced from degrees 23,...,44 feed only degrees below 23, so there is no hidden repeated reduction growth. The prior exponent-overflow blocker is resolved for this certificate.

## 5. Lower bound and transfer scope

Section one of the [accepted inherited lower review](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md) explicitly states the universal theorem for every characteristic-53 field and every legal beta: each same-sign orientation requires at least seven distinct nonzero effective alpha nodes, and each cross orientation requires a nonzero effective node. Repeated, ineffective, zero-alpha, or cancellation-only physical banks cannot lower the total. Its arbitrary-beta normalized-amplitude bridge does not divide by beta. This review inherits that accepted theorem and does not rerun the large original lower-minor computation.

The source's principal y=z=1 iff criterion is narrower. The present conclusion uses its separately stated universal lower theorem in the free-cross-singleton grammar, not the pinned-cross necessity criterion. Accepted degree-eleven, degree-thirteen, degree-seventeen, and degree-nineteen reviews preserve the same distinction.

Thus B(K)>=7+1+1+7=16 in the stated grammar. The explicit verified network supplies equality over F_(53^23). Whenever 23 divides d, the finite-field embedding into F_(53^d) preserves every parameter, raw weight, nonzero guard, and operator equality; the universal lower theorem still applies. Twenty-three not dividing d does not exclude a different witness.

The [rank/chart report](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-16-research-finalization-2101/n13_free_cross_rank/REPORT.md) states that the chosen chart works at every cross node in F_(53^d) precisely when 37 does not divide d. It applies at degree 23. The degree-37 exception remains a chart exception, not a physical-network obstruction, and the independently checked literal certificate does not depend on discovery-chart completeness.

The older prime-field-cross and Frobenius-stable-support restrictions retain their original gcd(d,210)=1 hypotheses. Replacing that obstruction hypothesis with the enlarged sufficient-divisor product would be invalid. Both nonbase cross nodes and nonstable supports are properties of this witness; this does not establish that both cross nodes must be nonbase in every possible witness.

Applying each of the twenty-three prime-Frobenius automorphisms to the full parameter list gives another original network for the same prime-field target. The exact cross-node orbit distinguishes twenty-three parameter lists. A prime-field total matrix does not force individual parameters to descend. No claim follows about exclusion of different base-field parameters, cofinite existence, geometric irreducibility, or a general point-count theorem.

## 6. Discovery, operation accounting, and continuation caution

The constructive subfamily beta=1, y=z, and common seven-node same-sign support suffices for the upper bound in the larger grammar. The complete 15,548 xorshift coefficient draws through trial 675 were independently replayed, confirming 676 nonzero cross nodes, no skipped zero node, and the exact final cross node. The discovered H, literal H, and generated input header agree.

The candidate reports first split at trial 675 with 676 nonzero-constant recurrence candidates and an original cap of 100,000. Its exact failed-prefix, first-hit, adaptation, and chronology receipts are byte-bound. This reviewer does not independently rerun every recurrence gate or splitting test in the earlier search prefix, or infer original execution chronology from a timestamp. First-hit minimality and search timing are not premises of the accepted literal theorem. Finite failed prefixes imply no field-wide nonexistence or stable-support census.

The ledger correctly charges field arithmetic, modulus selection, discovery, factorization, full-sector solving, raw-weight construction, and inverse preparation. The stated unoptimized prepared-matrix evaluation budget is arithmetically correct: 37,869 extension multiplications and 35,139 additions. The dense inverse-validation loops require 913,952 extension multiplications. Schoolbook degree-23 multiplication uses 529 coefficient products before reduction. Sixteen physical banks are not sixteen scalar operations; no FFT speedup, practical runtime advantage, or historical-priority claim follows.

A continuation at the next residual degree 29 should retain the current GMP exponent representation: 53^29 has 167 bits. There is a separate boundary in this reviewer's packed multiplication: 29*52^2=78,416 exceeds 65,535. **The independent review method must widen its packed coefficient slots to at least 17 bits, or switch to ordinary convolution, before adapting it to degree 29.** The current checker explicitly asserts its carry bound and would reject such an unmodified adaptation. This limitation affects the reused reviewer implementation, not the accepted degree-23 witness or GMP exponent representation. Coefficient/reduction bounds must also be reassessed for the next chosen modulus.

No other cross allocation, transform length, characteristic, complete field classification, general parent problem, or novelty question is settled. No external write, commit, publication, register update, or additional agent was used in this review.

## 7. Reproducibility

The isolated cold replay contains only review_check.py and the inert certificate. It passes and reproduces ARITHMETIC.json byte for byte at SHA256 fc88dbe201877f30689edaf1d6c78e1c94f10d597bbc83478b9afe4a30c8b9d2. The separate GMP probe rebuild and sanitizer result are retained in COLD_REPLAY.json and FRESH_GMP_PROBE.json.

From this review directory:

    python -I review_check.py
    python -I supplemental_check.py
    python -I cold_replay.py

The first two checks need only Python's standard library. The optional implementation-probe portion of cold_replay.py requires GNU C++17 and GMP development headers/libraries; no software installation was performed. build_review_checker.py recreates the independent checker from its pinned accepted predecessor. bind_inputs.py rechecks exact original source locations where available. The isolated mathematical replay itself requires neither those original paths nor any candidate program. MANIFEST.json binds all retained review files and frozen inputs, excluding itself and disposable Python caches.
