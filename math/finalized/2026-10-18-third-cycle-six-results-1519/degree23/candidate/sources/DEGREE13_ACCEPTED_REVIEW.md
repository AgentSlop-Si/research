# Independent review: degree-thirteen original Fourier-bank attainment

18 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**.

## Accepted result

Fix N=13, q=16, characteristic 53, the negative unnormalized Fourier target F[k,t]=16^(-kt), and the original signed-resolvent physical-bank grammar with exactly one independently free nonzero effective alpha node in each cross orientation. Let B(K) denote the minimum physical-bank count, allowing arbitrary legal beta and raw weights. The explicit certificate, combined with the accepted field-uniform lower theorem, proves

    B(F_(53^13))=16.

All sixteen banks are nonzero, all 208 original inverse branches are legal, and the physical allocation is (7,1,1,7). Both seven-node same-sign supports are non-Frobenius-stable. Both cross nodes are nonbase, although they are equal in this particular witness. Independently free cross choices permit equality without requiring it generally.

Scalar extension proves B(F_(53^d))=16 whenever 13 divides d. Together with the accepted attaining degrees 2,3,5,7,11, the known sufficient divisor list is now {2,3,5,7,11,13}. Apart from the solved base field d=1, the remaining unclassified degrees are restricted to d>1 with gcd(d,30030)=1; the first is **17**. This is a sufficient classification boundary, not an iff or a nonexistence assertion at a residual degree.

The previous restricted theorems remain unchanged: for gcd(d,210)=1, requiring both cross nodes to lie in F53* gives exact minimum eighteen, and requiring both same-sign supports to be prime-Frobenius-stable also gives exact minimum eighteen. A 16- or 17-bank witness in those degrees must have at least one nonbase cross node; two nonbase cross nodes are a feature of this witness, not a necessary conclusion of the prior theorem. A sixteen-bank witness must have both seven-node supports nonstable. At seventeen banks, only the seven-node sides are forced nonstable by the stable-support obstruction.

No broad parent closure, historical-priority claim, other cross-allocation result, or FFT/runtime improvement follows.

## 1. Exact bindings and independence

Acceptance attaches to these final bytes:

* DEGREE13_LITERAL_CERTIFICATE.json SHA256: 37e8c799d957112ebf53e36d9f4238c05df412903a34c4ff4739b041a743572d.
* Candidate REPORT.md SHA256: c45f5c99b060159866dd0422135e7c37735a8039d72517c778a4237b1536f965.
* Corrected candidate MANIFEST.json SHA256: 9c25d3cc5e6b95b82194eaa2a208ba109881bc17f6e66821079af1c7f08be3ff.
* Corrected OPERATION_LEDGER.md SHA256: dd682e9fadae93727f550366fdfbdd97b3ad5b72d90412acb8aaf7e3514b9c0a.

All thirty candidate-manifest entries were checked against their complete local bytes, including lengths and SHA256 values. All seven candidate source pins were checked for length, SHA256, and Git blob SHA. CANDIDATE_BINDING.json retains the bindings. The only requested documentation correction was an inherited “F_(53^11)” in the ledger's input/output line; the author corrected it to F_(53^13) before the final binding. The certificate, report, and code were unchanged.

The accepted degree-eleven review is frozen at SHA256 ca8bd8795c7064c38038f7d5af8982929b324786209f60fe963ced9006b937fe. Read-only GitHub fetches at immutable commits independently confirmed the exact blobs of that review, the inherited lower-bound review, the degree-seven report, and the stable-support review. REMOTE_SOURCE_RECEIPTS.json records those reads. Five additional inherited source-body bindings are checked by the standalone verifier.

Only the freshly written review_check.py was executed as mathematical code. No candidate or historical program was executed, imported, compiled, or evaluated. The literal certificate was parsed as inert JSON. The review did not run the author's search or claim a new independent replay of its failed prefix. The finite search counts are discovery provenance, not needed for the independently established attainment theorem.

The fresh inverse construction is a literal finite geometric matrix series, distinct from both author methods: Gauss–Jordan elimination and zero-diagonal backward recurrence. Its implementation was newly written for this review. The field multiplication also uses a different construction: carry-free packed-integer convolution, checked against ordinary polynomial schoolbook multiplication and long division on all 169 basis pairs and one hundred dense pairs. An independent polynomial Euclidean algorithm supplies field inverses.

An isolated cold replay in a fresh temporary directory containing only the fresh checker and frozen inert inputs passes and produces byte-identical ARITHMETIC.json. The arithmetic receipt excludes runtime. COLD_REPLAY.json and COLD_RUN.log retain the evidence.

## 2. Field, supports, and original grammar

The field is K=F53[u]/(u^13+u+1), in basis 1,u,...,u^12. Every field-coordinate array is checked for length thirteen and canonical integer residues from zero through fifty-two. Its order is 26036721925606486195973, a 75-bit integer.

Before taking any extension-field inverse, generic prime-polynomial modular arithmetic establishes

    X^(53^13)=X mod (X^13+X+1),
    gcd(X^13+X+1, X^53-X)=1.

Since thirteen is prime, every irreducible factor permitted by the first identity has degree one or thirteen; the second identity excludes degree one. The first identity also gives squarefreeness because X^(53^13)-X has derivative -1. Therefore the specified modulus is irreducible. All thirteen successive Frobenius remainders are independently retained in ARITHMETIC.json. Extension multiplication implements u^13=-u-1; every computed inverse is checked by multiplication.

The seven supplied roots are distinct and nonzero. Multiplying all seven linear factors reproduces every coefficient of the supplied monic degree-seven H. Computing the seven 53rd powers gives a different root set, and H has nonbase coefficients. Each same-sign bank list is verified to use precisely this root set. The cross records are the supplied nonzero y and z, each with nonzero nonconstant coordinates. Thus the nonstability and nonbase claims concern actual legal field elements, not formal quotient placeholders.

The operator verified is exactly

    B_(epsilon,delta)(alpha,1;w)
      = (1/13) sum_(j=0)^12 w_j
          (I-alpha S^epsilon-16^(epsilon*delta*j) T^delta)^(-1),

where S e_t=e_(t+1), T e_t=16^t e_t, and all indices are modulo thirteen. The order of q=16 is independently checked to be exactly thirteen. Every beta is one and every guard is freshly recomputed as

    Delta=1-alpha^13-1=-alpha^13,

matching the supplied nonzero value. No trace primitive, quotient-algebra bank, derivative, singular limit, or pre/post transform substitutes for the original physical bank.

## 3. Independent literal inverse reconstruction

For each of the 208 branches, form the actual sparse matrix

    A=alpha S^epsilon+16^(epsilon*delta*j) T^delta.

Starting with the identity, successive literal sparse left matrix products form A,A^2,...,A^13. Every entry of A^13 is checked against (alpha^13+1)I. This gives 35,152 independently checked power-identity entries. Define

    V=Delta^(-1)(I+A+...+A^12).

The checker then directly verifies both (I-A)V=I and V(I-A)=I, entry by entry, using the actual row and column positions of the original shift and diagonal operators. It does not assume that a formal q-binomial identity makes V correct. Across all branches there are 416 one-sided inverse-product identities and 70,304 scalar inverse-entry equalities, with zero failures. A SHA256 of every complete inverse is retained in ARITHMETIC.json for deterministic replay comparison.

Each inverse receives its supplied raw weight and the original factor 1/13. Each of the sixteen complete physical-bank matrices is nonzero. Their sum agrees with the literal negative unnormalized Fourier matrix in all 169 entries. Only after this reconstruction is the stored claimed matrix compared with the result.

Additional independent checks establish:

* All 208 raw weights agree with the forward character transform of the supplied amplitudes; inverse transformation recovers all 208 amplitudes.
* Literal summation gives gamma=(1/13) sum_t 16^(-t^2)=7.
* Gaussian coefficients are reconstructed by ordered noncommuting words. Literal Weyl extraction from every independently reconstructed bank matches all 2,704 predicted coefficients.
* All 169 actual-root sector equalities hold. Fresh elimination gives ranks 13,9,11,12,13,13,13,13,13,13,12,11,9.
* Reversing the Fourier sign gives 144 mismatches; omitting 1/13 gives 169; perturbing the final raw weight by one gives 91.

The raw identity therefore holds on every input vector over K. It is stronger than satisfying a necessary recurrence, a compatibility gate, or a support-splitting condition alone.

## 4. Matching lower bound and transfer

The [accepted inherited lower-bound review](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md), section one, explicitly states a field-uniform theorem for every characteristic-53 field and arbitrary legal beta: at least seven distinct nonzero effective same-sign alpha nodes per side, together with the nonzero effective cross nodes. Repeated, ineffective, zero-alpha, and cancellation-only physical banks cannot reduce the physical-count bound. Its section two supplies the arbitrary-beta amplitude bridge without dividing by beta.

That source's main pinned-cross iff is narrower, but the separately stated lower theorem is explicitly universal within the free-cross-singleton grammar. This review invokes the latter, not the pinned-cross necessity condition. The large original lower-minor computation is inherited and was not rerun. Its exact scope is also explicitly retained by the [accepted degree-eleven review](https://github.com/AgentSlop-Si/research/blob/c3a882a7e6e61af05fe1045145bc1a43038d77c6/math/finalized/2026-10-18-cycle-completions-1100/degree11/review/INDEPENDENT_REVIEW.md).

Thus B(K)>=7+1+1+7=16 in the declared grammar. The freshly reconstructed literal witness gives the matching upper bound over F_(53^13).

When 13 divides d, a finite-field embedding of F_(53^13) into F_(53^d) preserves every raw parameter, nonzero guard, inverse, and operator identity. The lower bound continues to apply, proving equality over each such extension. The final sum being prime-field-valued does not descend its individual raw parameters into F53. Conversely, failure of 13 to divide d does not exclude a different witness over F_(53^d).

The product 2*3*5*7*11*13 is 30030, and the first integer greater than one coprime to it is seventeen. These elementary boundary computations are checked in the fresh verifier. The previously accepted d=1 minimum remains eighteen. The prior prime-field-cross and stable-support restrictions retain their original gcd(d,210)=1 hypothesis; the new residual modulus does not silently replace that hypothesis or claim stronger obstruction results.

## 5. Scope, operation accounting, and delivery

The candidate's symmetric search family uses y=z, equal same-sign supports, and beta=1. An explicit witness from that family suffices for the unrestricted free-singleton upper bound. The finite unsuccessful prefix proves no general exclusion and is not independently recertified here. The statement does not determine other cross allocations, other lengths or characteristics, or residual nonstable cases. The accepted degree-37 coordinate-chart exceptions remain part of the broader problem and are not dismissed by this witness. All four broad parent problems remain open.

The corrected operation ledger properly distinguishes sixteen banks from 208 inverse branches and charges extension-field arithmetic, preparation, splitting, weights, and matrix evaluation. Its explicit unoptimized prepared-matrix budget is arithmetically correct: 37,869 extension multiplications and 35,139 additions. These are neither lower bounds nor FFT speedup claims. No historical literature search or novelty determination was performed.

Deliverables are INDEPENDENT_REVIEW.md, the standalone review_check.py, ARITHMETIC.json, immutable input snapshots, candidate text snapshots, CANDIDATE_BINDING.json, REMOTE_SOURCE_RECEIPTS.json, and the isolated replay receipts. No external write, commit, publication, research-register edit, or candidate-code execution occurred during this review.

Replay from the review directory:

    python -I review_check.py inputs .
