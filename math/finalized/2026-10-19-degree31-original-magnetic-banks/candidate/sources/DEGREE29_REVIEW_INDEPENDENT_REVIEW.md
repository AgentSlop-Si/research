# Independent final review: degree-29 original Fourier-bank attainment

18 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**. No scientific correction is required for the sealed candidate. The independent checker explicitly resolves the degree-29 packed-convolution boundary, retains arbitrary-precision exponents, and verifies the original operators rather than only discovery equations.

## Accepted conclusion

Fix N=13, q=16, characteristic 53, and the negative unnormalized Fourier matrix F[k,t]=16^(-kt). Let B(K) be the minimum physical-bank count in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation, allowing arbitrary legal beta parameters and raw weights. The literal upper witness verified here, together with the inherited accepted field-uniform lower theorem, establishes

    B(F_(53^29)) = 16.

The allocation is (7,1,1,7). All sixteen banks are nonzero and all 208 original inverse branches are legal. Both cross nodes are nonbase. Both seven-node same-sign supports are non-Frobenius-stable. The equal cross nodes and common same-sign support are properties of this constructive subfamily, not constraints imposed on the larger free-cross-singleton grammar.

Scalar extension establishes B(F_(53^d))=16 whenever 29 divides d. Combining with the previously accepted attaining degrees yields the sufficient divisor list {2,3,5,7,11,13,17,19,23,29}, with product 6,469,693,230. Apart from the separately solved base case d=1, the remaining degrees outside this sufficient coverage are d>1 coprime to that product; the least is 31. This is not an iff classification or a nonexistence theorem for degree 31.

## 1. Sealed inputs and provenance

This acceptance binds exactly to:

- DEGREE29_LITERAL_CERTIFICATE.json SHA256: 44a1ad9e58b847444e13d6fe72a6b90dc18f4e763f0e10377b973f25a9bf221c.
- MANIFEST.json SHA256: 38850b9975a9639b186dacf158f7c557ce663bcfb0b54fd7a9c0e9bb722edd98.
- REPORT.md SHA256: 5f275f92f519329281d21bf4f59dd18d378593e24ce6dc9803b7d734e66f244d.
- OPERATION_LEDGER.md SHA256: 6f61de062a57a578342ab7186d3659b8f84f8f8869792761533fa508081d076d.

All 74 candidate-manifest entries pass byte-length and SHA256 checks. All 27 source pins pass byte length, SHA256, Git blob SHA1, and byte-for-byte comparison with the original local paths. All 52 entries of the predecessor degree-23 candidate manifest and all 78 entries of its accepted review manifest also pass against the original local trees. The predecessor ACCEPT_SCOPE_LIMITED verdict is explicitly bound to its exact candidate manifest, independent report, and arithmetic receipt.

CANDIDATE_BINDING.json records this chain. candidate_snapshot preserves the sealed scientific artifact without disposable compiler binaries. The candidate's pending-review labels remain unchanged; this separate review supplies acceptance. No fresh remote retrieval occurred. Retained source links and accepted local bytes are not presented as freshly fetched material.

The mathematical review transparently adapts the prior independent degree-23 checker, whose exact source SHA256 is c0ad5870bc2800f5b524995944fca2af746e376a8d84809eea74be26c665daaf. Its source is independently bound to the accepted predecessor review manifest. CHECKER_ADAPTATION.json and build_review_checker.py retain the precise adaptation, including the essential widening from 16-bit to 17-bit coefficient slots. The supplemental GMP probe calculations likewise adapt the pinned prior independent review method. This is method reuse, not a claim that every line is newly authored. Neither checker imports or executes the candidate's discovery or literal-verification programs.

## 2. Independent field proof and arithmetic

Use K=F53[u]/(u^29+u+8), with coordinates in the basis 1,u,...,u^28. Every supplied field element is required to contain exactly 29 canonical integer residues in 0,...,52. Primality of 53 and 29 is checked. Before any extension-field inverse, ordinary prime-polynomial convolution and general polynomial division establish

    X^(53^29) = X modulo X^29+X+8,
    gcd(X^29+X+8, X^53-X) = 1.

The modulus therefore divides X^(53^29)-X, whose derivative is -1 and which is squarefree. Since 29 is prime, its irreducible factors could have only degrees 1 or 29. The gcd excludes degree 1, and total degree 29 forces irreducibility. All 29 Frobenius remainders are retained in ARITHMETIC.json. The supplemental checker separately repeats the family u^29+u+c for c=1,...,8; every Frobenius remainder and gcd matches the inert candidate field-search data, with c=8 the first irreducible member tested.

Extension multiplication uses integer convolution in radix 2^17. The exact carry bound is

    29*52^2 = 78,416 < 131,072 = 2^17.

Reduction uses u^29=-u-8. The packed implementation is checked against ordinary prime-coefficient convolution and general long division on all 841 ordered basis pairs, 100 independently seeded dense pairs, and the all-52 worst-case pair: 942 exact differential comparisons. Inversion uses polynomial extended Euclid and verifies each result by multiplication, differing from the candidate's exponentiation inverse.

The 16-bit negative control is substantive. The all-52 convolution fits 16 bits at degree 24 but fails at degrees 25 and 29. Both raw coefficients and the reduced degree-29 field product are corrupted by 16-bit packing. The review records the incorrect and correct reduced products. A separate cold execution reinstating the unmodified 16-bit carry guard fails before any literal bank work. A second execution forces 16-bit packing while leaving the widened guard in place; the ordinary-convolution differential catches the actual corruption, also before literal bank work. Both expected failures are retained. Safe 17-bit packing is also checked on the degree-31 all-52 convolution; its maximum is 83,824. That boundary test is not an existence result in degree 31.

The seven roots are independently checked distinct and nonzero, and their seven linear factors multiply to the exact supplied monic annihilator. The stored bank supports agree with these roots and the cross nodes. The 53rd-power support differs from the original support; annihilator coefficients are nonbase. Direct Frobenius iteration gives period exactly 29 for each of seven support roots and both cross nodes.

## 3. Literal original-bank reconstruction

With indices modulo 13, S e_t=e_(t+1), and T e_t=16^t e_t, each supplied bank is exactly

    (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1).

Every supplied beta is one. The general guard 1-alpha^13-beta^13 is recomputed as Delta=-alpha^13 and checked against the stored nonzero value. The reviewer proves q=16 has exact order 13 and directly computes gamma=(1/13) sum_t 16^(-t^2)=7.

For each of 208 branches define A=alpha S^epsilon+16^(epsilon*delta*j) T^delta. Starting with the identity matrix, sparse literal matrix multiplication constructs all powers through A^13. Every entry of A^13 is checked against (alpha^13+1)I. The reviewer then constructs

    V = Delta^(-1)(I+A+...+A^12)

and checks both (I-A)V=I and V(I-A)=I in every entry using the actual shift and diagonal positions. The power identity is evaluated, not trusted as an abstract q-binomial substitution. This geometric-power inverse differs from both the candidate C++ Gauss-Jordan inverse and the candidate Python backward recurrence.

The raw weights are checked against Delta*7*sum_b A_b*16^(-epsilon*b*j), and the inverse character transform independently recovers each supplied amplitude. Each original branch is then weighted by its actual raw weight and the original 1/13. Every bank is nonzero. The complete sum is compared with the negative unnormalized Fourier target in all 169 entries, then with the certificate's claimed matrix. Consequently the result is equality of operators on every input vector over K, not sampled-vector agreement.

Independent checks comprise:

- 208 branch-power identities: 35,152 scalar equalities.
- 208 branch inverses and 416 left/right identities: 70,304 scalar equalities.
- 208 raw-weight forward transforms and 208 inverse amplitude transforms.
- Direct extraction of all 169 target Weyl coefficients.
- Independent extraction and checking of all 2,704 bank Weyl coefficients.
- All 169 full actual-root sector equations.
- Fresh sector ranks 13,9,11,12,13,13,13,13,13,13,12,11,9.
- All 169 Fourier target entries, with zero mismatches.

Negative controls detect 169 mismatches if 1/13 is omitted, 144 for the opposite Fourier sign, and 91 after increasing the final raw weight by one. ARITHMETIC.json retains deterministic hashes for all 208 inverse matrices and all sixteen full bank matrices. No recurrence gate replaces the literal identity. No trace bank, quotient-algebra primitive, derivative, singular limit, or uncharged pre/post transform is introduced.

## 4. GMP exponent paths and fresh implementation probe

The field order and relevant exponents are

    Q         = 100925339366770615067826870974905413660631238363333,
    Q-2       = 100925339366770615067826870974905413660631238363331,
    (Q+3)/8   = 12615667420846326883478358871863176707578904795417,
    (Q-1)/2   = 50462669683385307533913435487452706830315619181666.

Q has 167 bits. All three order-derived exponents exceed 2^128-1. Inspection of the complete active C++ sources confirms that ORDER, element powers, inversion, polynomial powers, splitting, square-root exponentiation, and recursive factorization exponents use unbounded GMP mpz_class. No narrowing conversion or fixed-128 exponent type occurs in those paths. uint64_t is used for the deliberately wrapping PRNG and bounded counters; the prime-field exponent routine uses bounded small exponents. Q=5 modulo 8 and 23^2=-1 modulo 53 are independently checked. The candidate square-root routine verifies its answer by squaring.

The supplemental reviewer independently recomputes the inert arithmetic probe with 17-bit carry-free multiplication, Python unbounded integers, and polynomial-Euclidean inversion. It checks multiplication, inversion, ten powers around the 2^127 and 2^128 boundaries and at the order-derived exponents, a known seven-root splitting polynomial, and four exact/truncated splitting and factorization polynomial powers.

Six controls independently detect wrapped order, the 2^128 exponent truncating to zero, truncated inverse, truncated splitting order, truncated square-root exponent, and truncated factor exponent. The false inverse fails multiplication by its input; the false square root fails squaring; the false splitting remainder is not X; and the false factor characters fail the required squares-to-one test.

Separately from the independent mathematical checker, a fresh temporary directory builds the small supplied GMP implementation probe with GNU C++17, undefined-behavior sanitization, -fno-sanitize-recover=all, -lgmpxx, and -lgmp. It exits zero with no sanitizer diagnostics and reproduces the independently checked inert ARITHMETIC_PROBE.json byte for byte. GMP reports version 6.3.0. This is the only candidate scientific program executed by the review; neither discovery nor the supplied literal verifier is executed.

The unreduced convolution bound is 78,416. Each low C++ coefficient receives its initial term and at most one contribution with each of multipliers 1 and 8, giving conservative signed bound 784,160, well below 2^31. Reduction from degrees 29,...,56 feeds only degrees below 29, so no repeated high-degree feedback is omitted.

## 5. Inherited lower bound and scope

Section 1 of the retained accepted lower review explicitly states the field-uniform characteristic-53 theorem: for every legal beta, each same-sign orientation requires at least seven distinct nonzero effective alpha nodes and each cross orientation requires a nonzero effective node. Repeated, ineffective, zero-alpha, or cancellation-only physical banks cannot reduce that count. Its normalized-amplitude bridge does not divide by beta. This review inherits that accepted theorem and does not rerun the large original lower-minor computation.

Immutable inherited locator:

https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md

That source's principal y=z=1 iff criterion is narrower. The accepted conclusion here uses its separately stated universal lower theorem, not its pinned-cross necessity criterion. The retained degree-eleven, degree-thirteen, degree-seventeen, degree-nineteen, and degree-twenty-three accepted reviews preserve that distinction. Thus B(K)>=7+1+1+7=16 in the stated free-cross-singleton grammar, while the newly verified original network gives equality over F_(53^29).

Whenever 29 divides d, the finite-field embedding into F_(53^d) preserves parameters, weights, nonzero guards, and the original operator identity. Nondivisibility does not exclude another witness. Applying the 29 prime-Frobenius automorphisms to the whole network gives 29 conjugate parameter lists for the same prime-field target; the exact cross-node orbit distinguishes those lists. This witness does not descend to F53, but that does not exclude different prime-field parameters.

The older prime-field-cross and Frobenius-stable-support restrictions retain their original gcd(d,210)=1 hypotheses. The enlarged sufficient-divisor product cannot replace those obstruction hypotheses. Both cross nodes being nonbase is a property of this witness, not a new universal necessity theorem. The inherited rank/chart report applies because 37 does not divide 29, but the literal identity needs no completeness claim for that chart. The degree-37 exception remains a chart exception, not a physical-network obstruction.

## 6. Discovery, costs, and limits

The candidate reports first split at zero-based trial 10,425, with 10,426 nonzero cross nodes and 10,497 nonzero-constant recurrence candidates, within an initial cap of 100,000. The review independently replays all 302,354 PRNG coefficient draws, confirms no zero node was skipped, and recovers the exact final cross node. Candidate, certificate, and generated C++ header bind to the same node and annihilator.

The supplied failed-prefix, first-hit, source-adaptation, and chronology receipts are byte-bound. This review does not independently reexecute every earlier recurrence gate or splitting test, does not independently time the original run, and does not infer chronology merely from timestamps. First-hit minimality and discovery timing are not premises of the accepted literal theorem. A finite failed prefix proves no field-wide nonexistence, stable-support census, other-node obstruction, or complete classification.

The operation ledger correctly separates physical banks from scalar cost. Schoolbook degree-29 multiplication has 841 coefficient products before reduction. Field arithmetic, modulus selection, discovery, factorization, full-sector solving, weight construction, inverse preparation, and verification are additional work. The explicit unoptimized prepared-matrix application budget is arithmetically correct: 37,869 extension-field multiplications and 35,139 additions. The candidate's dense left/right inverse-validation loops require 913,952 extension-field multiplications. These are not optimality or runtime claims.

At residual degree 31, 53^31 has 178 bits, so the existing unbounded exponent path should be retained. Seventeen-bit coefficient slots remain sufficient for canonical degree-31 convolution, but the reduction bound must be checked for whatever new modulus is chosen. This observation neither constructs a degree-31 witness nor predicts its existence.

No complete field classification, generic or cofinite existence, other-allocation theorem, historical novelty, general faster FFT, or practical speed advantage follows. A finite list of exact prime-degree witnesses does not establish a geometric existence or point-count theorem. No external write, commit, publication, register change, or additional agent was used.

## 7. Reproducibility

From this review directory:

    python -I bind_inputs.py
    python -I build_review_checker.py
    python -I build_supplemental.py
    python -I review_check.py
    python -I supplemental_check.py
    python -I cold_replay.py

The mathematical checkers use only the Python standard library. bind_inputs.py verifies the original local provenance trees where supplied; frozen candidate_snapshot and inputs retain the reviewed scientific material. The standalone review_check.py requires only itself and the inert certificate in inputs. The cold replay independently repeats that isolated check and produces ARITHMETIC.json byte for byte. It also runs the fresh GMP/UBSan implementation probe and the two executable unsafe-16-bit negative controls. Compiling the optional implementation probe requires the existing GNU C++17 compiler and GMP development libraries; no installation was performed.

VERDICT.json binds this report, mathematical receipt, supplemental receipt, cold replay, and exact candidate seals. MANIFEST.json records every retained review file except itself and disposable caches. The final manifest is independently read back and verified before delivery.
