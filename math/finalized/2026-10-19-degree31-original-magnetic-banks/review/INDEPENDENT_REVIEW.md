# Independent review: degree-31 original magnetic-bank certificate

19 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**. The fresh independent literal checker finds no scientific correction necessary. Acceptance is bound to the exact inert certificate and final source/document seals recorded in `VERDICT.json` and `CANDIDATE_BINDING.json`.

## 1. Accepted theorem and scope

Fix N=13, characteristic 53, q=16, and the negative unnormalized Fourier target F[k,t]=q^(-kt). Let B(K) denote the minimum physical-bank count in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation, allowing arbitrary legal beta and raw weights.

The explicit original-bank witness independently verified here, together with the inherited accepted field-uniform lower theorem, establishes

    B(F_(53^31)) = 16.

Every finite extension with 31 dividing its degree inherits the same legal witness, so 31 | d implies B(F_(53^d))=16. The construction has allocation (7,1,1,7), beta=1, a common seven-node same-sign support, and y=z. These equalities describe this sufficient constructive subfamily; they do not constrain the larger grammar in the theorem.

This closes the named degree-31 attainment gate only. It does not close all parent magnetic-span questions, classify all fields, exclude witnesses at other degrees, or establish uniform, generic, cofinite, or all-length existence. It gives no historical novelty, scalar-operation speedup, practical advantage, or general faster-FFT claim.

## 2. Exact field and arithmetic

The field is K=F53[u]/(u^31+2u+11), with each element an ascending list of 31 canonical residues in 0,...,52. The exact order is

    Q = 283499278281258657725525680568509306972713148562602397,
    bit_length(Q) = 178.

The new Python checker verifies primality of 53 and 31, then proves, before any extension-field inverse,

    X^(53^31) = X modulo h,
    gcd(h, X^53-X) = 1,
    h = X^31+2X+11.

All 31 Frobenius remainders agree with the candidate's inert receipt and are retained. Since h divides X^(53^31)-X, a squarefree polynomial whose irreducible factor degrees divide 31, and the gcd excludes degree one, its degree 31 forces irreducibility. No assumed field inversion is used to establish this result.

The reviewer independently repeats all 63 modulus-family tests: no X^31+X+c with c=1,...,52 is irreducible; the next lexicographic family X^31+2X+c first succeeds at c=11. The initial narrower representation rule and its explicit amendment are both retained. The amendment was recorded before extension inversion and support discovery, changed only the representation of the same field F_(53^31), and left seed 202610192024 and cap 100,000 unchanged. No new field or larger witness-search budget was substituted.

All reviewer field multiplication uses ordinary coefficient convolution, unbounded Python integers, and generic monic-polynomial reduction. Inversion uses polynomial extended Euclid, independently differing from the candidate's exponentiation inverse. The ordinary convolution is checked against generic prime-polynomial long division on all 961 ordered basis pairs, 100 deterministic dense pairs, and the all-52 worst case: 1,062 comparisons.

The degree-31 raw convolution maximum is

    31*52^2 = 83,824 > 65,535.

Sixteen-bit coefficient packing is therefore unsafe. A direct negative control produces both incorrect raw coefficients and an incorrect reduced field product. Seventeen bits would suffice for canonical raw convolution, but neither fresh reviewer field implementation relies on packing.

For the active C++ arithmetic, reduction is u^31=-2u-11. Degrees 31,...,60 reduce directly to degrees at most 30, so no high-degree feedback is omitted. Each low coefficient has its original term plus at most one contribution of each multiplier 11 and 2. The conservative signed bound is

    (1+11+2)*83,824 = 1,173,536 < 2^31.

The active C++ field order, element exponent, inverse, polynomial exponent, split test, square-root exponent, and recursive-factorization exponent use GMP mpz_class without narrowing. uint64_t is restricted to the wrapping PRNG and bounded counters. The new arithmetic reviewer independently checks all ten supplied boundary/order-derived power cases, Euclidean inversion, and polynomial splitting/factorization powers. The latter are checked by evaluation at seven distinct known roots: a polynomial remainder of degree below seven is uniquely determined by those seven values. This is different from repeating the candidate's polynomial modular-power algorithm.

Six controls detect truncated/wrapped order, the 2^128-to-zero exponent failure, truncated inverse, split, square-root, and factor exponents. The square-root conditions Q=5 mod 8 and 23^2=-1 mod 53 are checked, as are the supplied square roots by squaring.

A separately written C++ driver freshly compiles the exact active field source in a temporary directory with undefined-behavior sanitization. It checks 1,062 products, eleven powers (including a 257-bit exponent), and one inverse against the fresh Python implementation. It exits zero without sanitizer diagnostics. The candidate's discovery main is renamed and never executed by this probe.

## 3. Literal original-bank verification

With indices modulo thirteen, S e_t=e_(t+1) and T e_t=q^t e_t, each bank is literally

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-q^(epsilon*delta*j) T^delta)^(-1).

The inert certificate contains seven actual support roots, their complete monic degree-seven annihilator, sixteen orientation/alpha/beta records, all 208 amplitudes, all 208 raw weights, all sixteen guards, and all 169 target entries. The review checks every canonical coordinate, distinct nonzero root, factor-product coefficient, support/orientation binding, and pole guard. The guard is recomputed from its original formula Delta=1-alpha^13-beta^13; beta=1 gives Delta=-alpha^13, nonzero for every bank.

The reviewer wrote `literal_review.py` anew; it neither imports nor executes a candidate or historical scientific checker. The inversion method is a closed cyclic-bidiagonal adjugate, distinct from the candidate's Gauss-Jordan inverse and inherited backward recurrence.

For one branch set d_r=1-q^(epsilon*delta*j+delta*r). Its diagonal has exactly one zero and det(M)=product_r d_r-alpha^13=Delta. For r=c+epsilon*l, with 0<=l<=12, the independently constructed inverse entry is

    V[r,c] = alpha^l * product_(k=l+1)^12 d_(c+epsilon*k) / Delta.

Both actual sparse products M V and V M are checked entry by entry for all 208 branches. The inverse is not accepted merely because this closed formula was written down.

The raw weights are checked by both character-transform directions with the original normalization gamma=(1/13) sum_t q^(-t^2)=7. Every weighted branch uses its actual raw weight and the original factor 1/13. All sixteen resulting bank matrices are nonzero. Their complete sum equals the negative unnormalized Fourier matrix in all 169 entries and agrees with the stored certificate matrix.

The checker also independently extracts Weyl coefficients directly from every literal bank matrix:

    c(a,b) = (1/13) sum_t q^(-bt) B[t+a,t].

Gaussian coefficients are reconstructed by the Pascal recurrence, rather than the candidate's quotient-product formula. Every one of the 2,704 bank Weyl coefficients agrees with the supplied amplitude expansion. The target coefficients are extracted directly from the Fourier matrix and give gamma*q^(10(a+b)^2). This separately verifies all thirteen complete sector systems, comprising 169 equations at actual support roots.

Exact checked counts:

- Seven distinct nonzero actual support roots and eight factor-product coefficients.
- Sixteen nonzero original guards and sixteen effective bank matrices.
- 208 supplied raw weights and 208 supplied amplitudes, checked in both transform directions: 416 equalities.
- 208 branch inverses; 416 left/right inverse identities; 70,304 scalar entry equalities.
- 2,704 literal-bank Weyl coefficients; 169 full-sector equations.
- 169 negative unnormalized Fourier target entries, with zero mismatches.

Each of the seven support roots and both cross nodes has exact Frobenius orbit length 31. The common same-sign support is not Frobenius-stable. These are properties of this witness, not universal necessities or exclusions of different parameter lists.

## 4. Mutation tests and isolated replay

The fresh checker rejects inert-JSON mutations of a noncanonical coordinate, zero guard, one raw weight, one amplitude, one target entry, and a duplicated support root. A reducible X^31 modulus is rejected before any extension-field inverse.

Semantic controls produce 144 mismatches for the opposite Fourier sign, 169 when 1/13 is omitted, and 91 when the final raw weight is increased by one. Thus normalization, sign, and raw branch data are not decorative metadata.

A clean temporary directory containing only the new standalone checker and frozen inert certificate produces a byte-identical mathematical receipt. This cold literal replay uses Python's standard library only and does not need the candidate source, discovery code, interpolation logic, or historical programs. Its observed wall time was about 11.90 seconds, CPU time 11.88 seconds, and peak RSS 13,056 KiB. These are implementation measurements, not complexity or optimality claims.

## 5. Discovery provenance and bounded first-hit claim

The fixed seed is 202610192024 and the original cap is 100,000 nonzero cross-node trials. The first reported split is zero-based trial 1,113, after 1,114 nonzero nodes and 1,117 nonzero-constant recurrence candidates. The new provenance checker independently reproduces all 34,534 PRNG coefficient draws, verifies every before/after PRNG state, confirms zero skipped zero nodes, checks every ledger count and first-hit position, and binds the terminal node/polynomial to the inert witness.

The complete failed-prefix ledger is retained. The candidate also cold-compiles its search and reruns limits 1,113 and 1,114: the former exits exhausted with no candidate, and the latter reproduces the candidate and complete ledger bytes. The independent reviewer binds these receipts and source code but does not claim to have separately reexecuted every preceding recurrence gate and splitting test. Independent PRNG replay is explicitly distinguished from the candidate's arithmetic prefix replay. First-hit minimality and chronology are not premises of the accepted literal identity.

Discovery remained in the stated sufficient beta=1, y=z, common-support subfamily. Failure or exhaustion in that subfamily would not prove nonexistence in the full original grammar. Neither the successful finite prefix nor the degree-31 witness proves a generic or cofinite existence theorem.

## 6. Inherited lower theorem, transfer, and cost accounting

The source-bound accepted lower review explicitly states that, for every characteristic-53 field and every legal beta, each same-sign orientation requires at least seven distinct nonzero effective alpha nodes, and each cross orientation requires a nonzero effective node. The new review inherits that theorem; it does not rerun its original large-minor proof or any accepted degree<=29 witness.

The lower theorem gives B(K)>=7+1+1+7=16 in the stated free-cross-singleton grammar. The legal literal witness gives the matching upper bound over F_(53^31). An embedding of F_(53^31) into F_(53^d), when 31 divides d, preserves every parameter, nonzero guard, weight, and original matrix identity. This proves only the stated sufficient extension-divisibility transfer. Nondivisibility does not exclude another witness.

The degree-37 chart exception remains a limitation of that discovery chart, not a physical-network obstruction. No chart completeness assumption is needed for the literal theorem proved here.

The candidate's operation ledger charges field arithmetic, representation search, arithmetic preflight, finite discovery, factorization, full-sector solving, weight preparation, inverse construction, and literal verification. One schoolbook degree-31 field multiplication has 961 base-field coefficient products before reduction. Sixteen physical banks are not sixteen scalar operations. A dense prepared-branch application can use 37,869 extension-field multiplications and 35,139 additions, while explicitly storing 35,152 inverse entries and 208 weights; this is an unoptimized accounting example, not a speedup claim. Replacing the banks by a precomputed target matrix would be a different implementation and would not prove lower cost in this grammar.

## 7. Source binding and reproducibility

The three adapted core scientific sources and the degree-29 report match the exact SHA256/Git-blob pins supplied by the selection report. All sixteen candidate source-copy records also pass byte count, SHA256, Git-blob hash, and equality to their declared original local paths. These checks do not claim that mutable local SOURCE_PINS or MANIFEST files equal the whole historical published package. The predecessor's ACCEPT_SCOPE_LIMITED verdict is separately bound to its exact report and arithmetic receipt. Retained links and local bytes are not represented as fresh remote retrieval.

The independent package contains frozen inputs and these entry points:

    python -I literal_review.py inputs/DEGREE31_LITERAL_CERTIFICATE.json
    python -I arithmetic_review.py candidate_snapshot
    python -I provenance_review.py candidate_snapshot
    python -I implementation_probe.py candidate_snapshot
    python -I cold_replay.py

The mathematical checker is newly written and reads inert JSON only. The optional implementation probe compiles the exact active C++ field source under a fresh independent driver; it is the only candidate scientific implementation executed by the reviewer. No candidate discovery/literal main, historical accepted witness, external write, repository mutation, or additional worker was run by this review.

`CANDIDATE_BINDING.json` records the final exact candidate seal. `VERDICT.json` binds this report and all principal review receipts. `MANIFEST.json` seals the review package without temporary binaries or caches. Acceptance attaches to those exact bytes.
