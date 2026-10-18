# Independent final review: degree-nineteen original Fourier-bank attainment

18 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**. No scientific correction is required for the sealed degree-nineteen candidate. The degree-twenty-three continuation requires an exponent representation wider than unsigned 128 bits.

## Accepted conclusion

Fix N=13, q=16, characteristic 53, and the negative unnormalized Fourier target F[k,t]=16^(-kt). Let B(K) be the minimum physical-bank count in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation, allowing arbitrary legal beta and raw weights. The literal witness independently checked here, together with the inherited universal lower theorem, proves

    B(F_(53^19))=16.

Its physical allocation is (7,1,1,7). All sixteen banks are nonzero and all 208 original inverse branches are legal. The two seven-node same-sign supports are non-Frobenius-stable; both cross nodes are nonbase. Their equality in this witness is permitted by independently free cross-node parameters and is not a restriction imposed on the general grammar.

Scalar extension proves B(F_(53^d))=16 whenever 19 divides d. Combining this with accepted attaining degrees 2,3,5,7,11,13,17 gives sufficient divisors {2,3,5,7,11,13,17,19}, with product 9699690. Apart from the already solved base case d=1, the residual degrees are d>1 coprime to this product; the least is 23. This is a sufficient classification boundary, not an iff or a nonexistence assertion for any residual degree.

## 1. Exact acceptance bindings and provenance

Acceptance attaches to the following candidate bytes:

- DEGREE19_LITERAL_CERTIFICATE.json SHA256: b10199e01e9e7775c78bf34b6cac41ce8d1e90280a013f0a2b21b4c1dcd9a09e.
- MANIFEST.json SHA256: 414b772a213f7e897ad5f8cbc9e948573866d84d5491c36a826463a150ab9617.
- REPORT.md SHA256: 710d36dcb580d0124d5ccc43d90867f123f87af254410c5e9d118e8b2cf984dc.
- OPERATION_LEDGER.md SHA256: 6a94648c8eb3b5dd4e49eb58f9ee847e744cb11d84145d8ee20cbb07376b0af5.

Every one of the 50 candidate-manifest entries passes independent byte-length and SHA256 checks. Every one of the 19 source pins passes byte-length, SHA256, Git blob SHA1, and byte-for-byte comparison with its original local source path. CANDIDATE_BINDING.json records these checks. candidate_snapshot preserves the entire sealed source artifact without compiler binaries or caches.

The prior degree-seventeen reviewer fetched the inherited lower review, degree-eleven accepted review, and rank/chart report from immutable GitHub commits. Its retained response contents and receipts have been copied as inert inputs and independently matched to the current source bytes. This review performed no fresh remote read and does not mislabel the inherited remote receipts as new fetches. The accepted degree-thirteen and degree-seventeen reviews were likewise matched to their original local files.

The candidate retains its dated pending-external-review labels. This separate report supplies acceptance without changing those sealed candidate bytes.

## 2. Reviewer implementation and field proof

The review arithmetic is a transparent degree-nineteen adaptation of the independently authored degree-seventeen reviewer at source SHA256 020bec897a37b508602662400534cbcdb23b32e5021e5aaa524109fc73e14c7c. Its source and the exact adaptation program are retained. This is reuse of a prior independent review method, not a claim that every line is newly invented. No candidate mathematical program was imported, compiled, or executed. All supplied coordinates are inert JSON; the new field proof, inverses, matrix identities, and sector ranks are recomputed.

Use K=F53[u]/(u^19+u+12), with basis 1,u,...,u^18. Every supplied field element is checked to contain exactly nineteen canonical integer residues 0,...,52. The order is

    53^19=577087307374494432392299037533517,

with 109 bits. Before any extension-field inverse, separate ordinary prime-polynomial convolution and long division establish

    X^(53^19)=X mod (X^19+X+12),
    gcd(X^19+X+12, X^53-X)=1.

The primality of 53 and 19 is checked. Since 19 is prime, the first identity confines irreducible factor degrees to 1 or 19, and the gcd excludes degree 1. Total degree 19 therefore forces irreducibility. Divisibility by X^(53^19)-X also proves squarefreeness. All nineteen Frobenius remainders are retained in ARITHMETIC.json.

The separate supplemental review repeats the entire deterministic field search for constants c=1,...,12. Every recorded final Frobenius remainder and gcd matches, and c=12 is independently verified as the first irreducible member tested.

Extension multiplication uses carry-free integer convolution in radix 2^16 and the reduction u^19=-u-12. Its carry bound is 19*52^2=51,376<65,536. This multiplication agrees with ordinary coefficient convolution followed by general polynomial division on all 361 ordered basis pairs and 100 deterministic dense pairs. Inversion uses polynomial extended Euclid, with every result checked by multiplication. These methods differ from the candidate's coefficient-loop multiplication and exponentiation-based inverses.

The reviewer verifies the exact order thirteen of q=16. The product of all seven actual linear root factors equals the supplied monic degree-seven annihilator in all eight coefficients. The roots are distinct and nonzero, the annihilator has nonbase coefficients, and the set of 53rd powers differs from the actual support. Each of the seven roots and each cross node has a directly checked Frobenius orbit of length exactly nineteen. The actual bank support lists match those roots and cross nodes.

## 3. Independent reconstruction of all original inverses and the Fourier sum

Every physical bank has the original form

    (1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1),

with S e_t=e_(t+1), T e_t=16^t e_t, and indices modulo thirteen. Every supplied beta is one. Its guard is recomputed as

    Delta=1-alpha^13-1=-alpha^13,

and checked against the supplied nonzero value.

For every bank and branch j, form the actual sparse matrix

    A=alpha S^epsilon+16^(epsilon*delta*j) T^delta.

Starting from I, sparse left multiplication constructs A through A^13. All 169 entries of A^13 are checked against (alpha^13+1)I. The inverse is then reconstructed as

    V=Delta^(-1)(I+A+...+A^12).

Both (I-A)V=I and V(I-A)=I are independently checked at every entry using the literal shift and diagonal positions. This method differs from both the candidate's Gauss-Jordan inverses and its second implementation's zero-diagonal backward recurrence. The formal q-binomial identity is not trusted as a substitute for the entrywise checks.

The resulting V receives its supplied raw weight and the original factor 1/13. All sixteen reconstructed bank matrices are nonzero. Their total equals 16^(-kt) in all 169 positions, and only then is compared to the certificate's claimed matrix. Thus the result is an operator identity on every input vector over K.

The exact successful checks are:

- 208 matrix-power identities, comprising 35,152 scalar equalities.
- 208 branch inverses and 416 one-sided inverse products, comprising 70,304 scalar equalities.
- 208 raw-weight forward transforms and 208 inverse amplitude transforms.
- Direct gamma=(1/13) sum_t 16^(-t^2)=7 and all 169 target Weyl coefficients.
- Literal Weyl extraction for every bank, matching all 2,704 predicted coefficients.
- All 169 complete actual-root sector equations.
- Fresh sector ranks 13,9,11,12,13,13,13,13,13,13,12,11,9.
- All 169 negative-sign Fourier entries, with zero mismatches.

Negative controls give 169 mismatches if 1/13 is omitted, 144 for the opposite Fourier sign, and 91 if one is added to the final raw weight. All complete inverse and bank matrices have deterministic hashes in ARITHMETIC.json.

No support recurrence or quadratic compatibility gate substitutes for the original inverse-matrix sum. No trace bank, quotient-algebra primitive, derivative, singular limit, or uncharged pre/post transform appears.

## 4. Matching lower bound and field-criterion scope

Section one of the [accepted inherited lower review](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md) explicitly states the accepted universal theorem for every characteristic-53 field and every legal beta: each same-sign orientation requires at least seven distinct nonzero effective alpha nodes, and each cross orientation requires a nonzero effective node. Repeated, ineffective, zero-alpha, or cancellation-only physical banks do not lower this count. The arbitrary-beta normalized-amplitude bridge in its section two has no division by beta.

The source's main pinned-cross iff is narrower. The current conclusion uses its separately stated universal lower theorem in the free-cross-singleton grammar, not its y=z=1 necessity criterion. The accepted degree-eleven, degree-thirteen, and degree-seventeen reviews preserve that same universal scope. The large original lower-minor certificate is inherited and is not recomputed here.

Therefore B(K)>=7+1+1+7=16 in the stated grammar. The independent literal witness supplies the matching upper bound over F_(53^19).

If 19 divides d, the finite-field embedding into F_(53^d) preserves every parameter, weight, nonzero guard, and operator equality, while the lower theorem remains valid. A prime-field-valued total matrix does not force individual bank parameters to descend. Nineteen not dividing d does not exclude a different witness.

The [rank/chart report](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-16-research-finalization-2101/n13_free_cross_rank/REPORT.md) states that the chosen chart works for every cross node of F_(53^d) precisely when 37 does not divide d. It applies to d=19. Its degree-37 chart exception remains a chart exception, not a physical-network obstruction. The independently verified literal witness does not depend on that discovery chart.

The older prime-field-cross and Frobenius-stable-support restrictions retain their original gcd(d,210)=1 hypotheses. The sufficient divisor product 9699690 does not strengthen those obstruction hypotheses. Both nonbase cross nodes and nonstable supports are properties of this witness; the result does not show that both cross nodes must be nonbase in every possible witness.

Applying each of the nineteen prime-Frobenius automorphisms to every bank parameter and raw weight gives another original network with the same prime-field target. The exact nineteen-element cross-node orbit proves these nineteen parameter networks are distinct. This does not prove nonexistence of a different base-field network or establish a cofinite field-existence theorem. In particular, a necessary recurrence gate or a finite list of prime-degree examples does not establish geometric irreducibility or the point-count estimates that a stronger general existence argument would need.

## 5. Discovery boundary, cost accounting, and continuation warning

The symmetric y=z subfamily with common seven-node same-sign supports and beta=1 is sufficient for an upper bound in the larger declared grammar. All 64,828 xorshift coordinate draws through trial 3411 were independently replayed, confirming 3,412 nonzero cross nodes, zero skipped all-zero nodes, and the exact stored final cross node. The discovered H, literal H, and input header agree byte for byte in the relevant coordinates.

The candidate's first-split and failed-prefix records are byte-bound. This reviewer did not independently reexecute the recurrence-gate search or all earlier splitting tests. Their first-hit claim is not a premise of the accepted explicit theorem. The prefix is finite and cannot imply field-wide nonexistence or a stable-support census.

The operation ledger correctly charges field arithmetic, discovery, factorization, actual-root solving, raw-weight preparation, and inverse preparation. Its unoptimized prepared-matrix evaluation count, 37,869 extension multiplications and 35,139 additions, is arithmetically correct. The dense inverse validation count is 913,952 extension multiplications. Schoolbook degree-nineteen multiplication has 361 coefficient products before reduction. The conservative signed convolution/reduction bound 719,264 lies below 2^31. Sixteen banks are not sixteen scalar arithmetic operations; no FFT speedup, practical efficiency, or historical novelty follows.

The current field order and needed exponent increments fit unsigned 128-bit storage. However,

    53^23=4553496434179608203397220101976502751677

has **132 bits** and exceeds 2^128. A degree-twenty-three continuation must replace the fixed unsigned-128 exponent representation with verified wider or multiprecision arithmetic, including field order, inverses, square-root exponents, splitting, and factorization. Simply changing D and the modulus would silently overflow the current C++ order computation. The degree-nineteen certificate is unaffected by this future limitation.

No other allocation, transform length, characteristic, full field classification, general parent problem, or historical-priority question is settled. No external write, commit, publication, or register edit occurred in this review.

## 6. Reproducibility

An isolated fresh-directory replay containing only the adapted independent reviewer and the inert degree-nineteen certificate passes and produces byte-identical ARITHMETIC.json at SHA256 1d996f020097a3c3649e7096cf31b1b7c15ed4b0367a8cae28e8a14ccfedfd89. COLD_REPLAY.json and COLD_RUN.log retain the evidence.

From this review directory:

    python -I review_check.py
    python -I supplemental_check.py
    python -I cold_replay.py

build_review_checker.py reproduces the checker from the pinned prior independent reviewer. bind_inputs.py rechecks the original candidate and source locations where available. The isolated scientific replay itself needs neither those original paths nor any candidate program. MANIFEST.json binds all retained review artifacts and frozen inputs; generated Python caches are disposable and excluded.
