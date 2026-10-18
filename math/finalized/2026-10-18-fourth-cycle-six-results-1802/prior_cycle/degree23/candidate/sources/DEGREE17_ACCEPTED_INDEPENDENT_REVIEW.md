# Independent final review: degree-seventeen original Fourier-bank attainment

18 October 2026 UTC. Verdict: **ACCEPT_SCOPE_LIMITED**. No scientific correction is required for the sealed candidate.

## Accepted conclusion

Fix N=13, q=16, characteristic 53, and the negative unnormalized Fourier target F[k,t]=16^(-kt). Let B(K) be the minimum physical-bank count in the original signed-resolvent grammar with exactly one independently free nonzero effective alpha node in each cross orientation, allowing arbitrary legal beta and raw weights. The supplied literal witness, together with the accepted field-uniform lower theorem, proves

    B(F_(53^17))=16.

The physical allocation is (7,1,1,7). Every one of the sixteen banks is nonzero. All 208 original inverse branches are legal. Both actual seven-node same-sign supports are non-Frobenius-stable, and both cross nodes are nonbase. Their equality in this particular witness is permitted by the independently free cross-node grammar; it is not a general restriction on that grammar.

Scalar extension proves B(F_(53^d))=16 whenever 17 divides d. Together with the accepted attaining degrees 2,3,5,7,11,13, the sufficient divisor list is {2,3,5,7,11,13,17}. Its product is 510510, and the least integer d>1 coprime to that product is 19. The already solved d=1 case remains separate. This is a sufficient classification boundary, not an iff or a nonexistence theorem for residual degrees.

## 1. Exact acceptance bindings

Acceptance attaches to the following final bytes:

- DEGREE17_LITERAL_CERTIFICATE.json SHA256: 58a76f5a919c73051aebb4a45defce4e238d7a3eb21bcce57d57bb961a1db3de.
- Candidate MANIFEST.json SHA256: b55cf6b58c043c7474fc8354b25dc152e6833ad67e937be2797008d39d3b0a3f.
- Candidate REPORT.md SHA256: e2067f61a030dd4e1ab98e58f36f242232d367ab00c1c5b8c3742d1542f34527.
- Candidate OPERATION_LEDGER.md SHA256: 744fb04e2fb04b41c500099ac37de18c358333504c64d2801b64e90b9d8f89a5.

All 36 candidate-manifest entries were independently checked for full byte length and SHA256. All nine source pins were checked for byte length, SHA256, Git blob SHA, and byte identity against their original local source paths. Immutable-commit read-only GitHub fetches additionally confirmed the exact source bytes of the inherited lower review, accepted degree-eleven review, and rank/chart report. CANDIDATE_BINDING.json and REMOTE_SOURCE_RECEIPTS.json retain these bindings; candidate_snapshot preserves the complete sealed source artifact.

The accepted degree-thirteen review is retained at SHA256 46685cd5cb92cfeb67684fcbfc5da80c76b8e076458e3d59ac8ab177b47e49a4 and was matched to its original local accepted-review file. This review does not describe that local verification as a fresh remote fetch.

The candidate's own files retain their dated “external review pending” status. This separate report supplies final independent acceptance without silently rewriting their sealed bytes.

## 2. Fresh arithmetic and field proof

Only newly authored review code was executed. No candidate or historical scientific code was imported, compiled, or executed. The input certificate is parsed as inert JSON, and all mathematical checks below are rebuilt from its coordinates.

The field is K=F53[u]/(u^17+u+6), using the basis 1,u,...,u^16. Every supplied field element is checked for exactly seventeen canonical integer residues between zero and fifty-two. The field order is

    53^17=205442259656281392806087233013,

which has 98 bits.

Before any extension inverse, separate prime-polynomial convolution and long division establish

    X^(53^17)=X mod (X^17+X+6),
    gcd(X^17+X+6, X^53-X)=1.

The checker verifies primality of 53 and 17. Because 17 is prime, every irreducible factor of a polynomial dividing X^(53^17)-X has degree 1 or 17. The gcd excludes degree 1; total degree 17 forces irreducibility. Divisibility by X^(53^17)-X also proves squarefreeness. All seventeen Frobenius remainders are retained in ARITHMETIC.json.

Extension multiplication uses carry-free integer convolution in radix 2^16, followed by u^17=-u-6 reduction. The bound 17*52^2=45968<65536 prevents coefficient carries in convolution. This multiplication was compared with separate ordinary coefficient convolution and general long division on all 289 ordered basis pairs and 100 deterministic dense pairs. Extension inverses use polynomial extended Euclid, rather than field-order exponentiation; each inverse is verified by multiplication. These arithmetic methods differ from both candidate implementations.

The order of q=16 is checked directly against every exponent 1 through 13. Multiplication of the seven actual linear root factors reproduces all eight supplied coefficients of the monic H. The roots are distinct and nonzero, the cross nodes have nonconstant coordinates, H has nonbase coefficients, and the seven 53rd powers form a different set from the original roots. The actual bank support lists are verified against these roots and cross nodes.

## 3. Independent reconstruction of every original branch

For each bank and each j=0,...,12, the independently constructed literal matrix is

    A=alpha S^epsilon+16^(epsilon*delta*j) T^delta,

where S e_t=e_(t+1), T e_t=16^t e_t, and indices are modulo thirteen. Every supplied beta is one. Its guard is freshly recomputed as

    Delta=1-alpha^13-1=-alpha^13,

and is checked against the supplied nonzero guard.

Starting at the literal identity matrix, sparse left matrix multiplication constructs all powers A,...,A^13. Every one of the 169 entries of each A^13 is compared with (alpha^13+1)I. Thus 208 power identities are verified through 35,152 entry equalities. Define

    V=Delta^(-1)(I+A+...+A^12).

Both (I-A)V=I and V(I-A)=I are then independently checked entry by entry using the actual shift positions and diagonal entries. These are 416 one-sided inverse identities and 70,304 exact field equalities. The construction does not rely on the candidate's Gauss-Jordan or zero-diagonal backward-inverse algorithms, and it does not assume that the formal q-binomial identity alone makes an inverse valid.

Each resulting inverse receives its supplied raw branch weight and the original factor 1/13. All sixteen complete bank matrices are nonzero. Their sum agrees with 16^(-kt) at every one of the 169 matrix entries; the supplied claimed matrix is only compared after reconstruction. All complete inverse matrices and bank matrices have deterministic hashes in ARITHMETIC.json.

The following additional checks all pass:

- All 208 raw weights satisfy the forward character transform of the supplied amplitudes, and all 208 amplitudes are recovered by the inverse transform.
- Literal summation independently gives gamma=(1/13) sum_t 16^(-t^2)=7.
- Literal Weyl extraction from the target confirms all 169 normalized target coefficients 16^(10(a+b)^2).
- Ordered Gaussian coefficients are rebuilt by finite products. Literal Weyl extraction from every independent bank matrix agrees with all 2,704 predicted bank coefficients.
- All 169 actual-root sector equations hold. Fresh elimination gives sector ranks 13,9,11,12,13,13,13,13,13,13,12,11,9.
- Omitting 1/13 gives 169 mismatches; reversing the Fourier sign gives 144; adding one to the final raw weight gives 91.

This proves the operator identity on every input vector over K. Passing a recurrence gate or a support-splitting check is not used as a substitute for these literal checks. There is no trace-valued bank, quotient-algebra primitive, derivative, singular limit, or uncharged pre/post transform.

## 4. Matching lower bound and exact source scope

The [accepted inherited lower review](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md), section one, explicitly invokes the accepted universal theorem for every characteristic-53 field and every legal beta: each same-sign orientation requires at least seven distinct nonzero effective alpha nodes, and each cross orientation requires a nonzero effective node. Repeated, ineffective, zero-alpha, or cancellation-only physical banks do not lower that physical count. The source's section two supplies the arbitrary-beta normalized-amplitude bridge without dividing by beta.

The source's main pinned-cross iff is narrower. This review invokes its separately stated universal lower theorem in the free-cross-singleton grammar, not the pinned-cross necessity criterion. That universal scope is also explicitly preserved by the [accepted degree-eleven review](https://github.com/AgentSlop-Si/research/blob/c3a882a7e6e61af05fe1045145bc1a43038d77c6/math/finalized/2026-10-18-cycle-completions-1100/degree11/review/INDEPENDENT_REVIEW.md) and the byte-bound accepted degree-thirteen review. The large original lower-minor computation is inherited and was not recomputed here.

Consequently B(K)>=7+1+1+7=16 in the declared grammar. The independently verified literal witness supplies the matching upper bound over F_(53^17).

If 17 divides d, an embedding F_(53^17) into F_(53^d) preserves every node, raw weight, nonzero guard, inverse, and operator equality. The lower theorem remains valid after extension. A prime-field-valued total matrix does not descend its individual extension-valued bank parameters, and 17 not dividing d does not rule out a different witness.

The [rank/chart source](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-16-research-finalization-2101/n13_free_cross_rank/REPORT.md) states that the relevant fixed chart is nonsingular over F_(53^d) exactly when 37 does not divide d. This applies to d=17. Its degree-37 chart exception is inherited, not removed or treated as a physical-bank obstruction. The witness's literal validity does not require trusting the discovery chart.

## 5. Limits, operation accounting, and replay

The symmetric discovery subfamily y=z with common same-sign supports and beta=1 suffices for an upper bound in the full free-singleton grammar. Its finite failed prefix is not a census of the field or a general exclusion. Candidate logs and cold-replay receipts are byte-bound but the discovery search and first-hit claim were not independently reexecuted in this review. They are not premises of the accepted explicit attainment theorem.

The prior prime-field-cross and Frobenius-stable-support restrictions retain their original gcd(d,210)=1 hypotheses. Neither this witness nor the new sufficient-divisor modulus strengthens those obstruction hypotheses. Having two nonbase cross nodes is a property of this witness; this does not prove that every possible attaining witness needs both cross nodes to be nonbase.

The operation ledger correctly distinguishes sixteen banks from 208 inverse branches, and charges field representation, support discovery, factorization, preparation, raw-weight construction, and evaluation. Its stated unoptimized prepared-matrix evaluation uses 37,869 extension multiplications and 35,139 additions. These totals are arithmetically correct and are neither operation lower bounds nor FFT-speedup claims. Schoolbook degree-seventeen multiplication has 289 coefficient products before reduction.

No other cross allocation, transform length, characteristic, broad parent problem, general field classification, or historical novelty question is settled. No external write, commit, publication, research-register edit, or candidate-code execution occurred during this review.

An isolated fresh-directory replay containing only review_check.py and the inert certificate passes and produces byte-identical ARITHMETIC.json. COLD_REPLAY.json and COLD_RUN.log retain the evidence. To replay the independent arithmetic:

    python -I review_check.py inputs .

To repeat the isolated replay:

    python -I cold_replay.py
