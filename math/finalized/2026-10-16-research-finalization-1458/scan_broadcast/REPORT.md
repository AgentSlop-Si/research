# ALG-050: completion of the scan/broadcast source-comparison gate

Date: 2026-10-16. Repository baseline: `35d9dcdc3f3869de75b33b2b09705222e8d09e8d`.

## Decision

Recommend **CLOSED for the current comparison/one-way obstruction activity**, with numerical priority **42 retained as historical/inactive**. This is an activity archive under the mathematical-value criterion, not completion of all mathematics associated with ALG-050. The earlier rational-degree/nullity comparison is already completed; this pass addresses only its previously unreviewed second source. The specified comparison now has a model-matched primary-source mapping, the written scan/broadcast proof is sound, and repeating unchanged one-way/full-pass constructions cannot evade its proved obstruction.

**Preserve source section 5 as an unsolved constructive alternative:** uniform factorizations into nonunitary overlapping bidirectional-sum maps, with scalar arithmetic, coefficient preparation, memory and outputs fully charged. This report does not prove or refute that route. It supplies no fast transform, general arithmetic lower bound, historical-priority clearance, or engineering completion. A concrete proposal in that different interface is an explicit reopening condition.

No external state was changed. No historical research program was executed. All computational checks below were newly authored for this review.

## 1. Exact source and owner binding

- Owner: **ALG-050**, “Whole-word rational degree and scan-broadcast gates”; historical family references F041/F042 are not additional owners.
- Catalogue: sheet ID 214001001, row 84, stable ID in A84; novelty sheet ID 214001003, row 45, stable ID in C45; overview sheet ID 1731260011, row 62, stable ID in B62.
- Fresh bounded native reads on 2026-10-16 confirmed overview E62 = TO RESEARCH and priorities Catalogue AA84, novelty U45, overview L62 = 42. The leading native action records that the rational comparison was completed while this second source remained unreviewed. Catalogue Z84 describes general bidirectional sums, changed geometry, nonlocal ports and efficient high-degree evaluation as outside its accepted scope. Overview F62 identifies historical attribution/primary comparison as the leading activity.
- Second source: [Independent macro review and a stronger scan–broadcast bound](https://github.com/AgentSlop-Si/research/blob/35d9dcdc3f3869de75b33b2b09705222e8d09e8d/math/archive/objects/e9/e97269eb8788d5949019e4e809c78e31e868b7a34bb0bbee90c0eaa9dc60fad4__53_e97269eb8788d594.md), 8,276 bytes, SHA256 `e97269eb8788d5949019e4e809c78e31e868b7a34bb0bbee90c0eaa9dc60fad4`, Git blob `72be967f57e51c458ffc03757d01732441631d71`. Complete retrieved bytes were checked against the recorded digest.
- First source `a4dcf5…` and the [earlier completed report](https://github.com/AgentSlop-Si/research/blob/e3368ff3a44ca7c4bcea7b9fb838ce92e77fa000/math/finalized/2026-10-16-research-finalization-1412/algebra/ALGEBRA_FINALIZATION_REPORT.md) are inherited background, not claimed as newly re-reviewed work.

Raw native cell preimages stay private and are not publication material. Any later application needs a fresh stable-ID/scope/value read and must preserve intervening edits and dated history.

## 2. Exact theorem and independent proof audit

Let K contain a primitive Nth root w, with characteristic not dividing N. Let F have entries w^(ij), or be its inverse. The allowed factorization consists of invertible square literal scalar one-way scans, arbitrary invertible monomials between factors and at endpoints, and invertible broadcasts I+UV^T. Let t count scans and B bound the sum of the broadcast ranks. Forward and backward orientations may be mixed. No bounded coefficient or complex-unitary premise is needed for this theorem.

For t >= 1 the necessary condition is

    N <= 2^(t-1) + B(2^t+1) = (2B+1)2^(t-1)+B.

For t = 0 it is B >= floor(N/2). For B = 0 and N >= 2 it is t >= 1+ceil(log2 N).

### 2.1 Nonuniform rigidity

For any N-by-N S put u = min row support size, s = max row support size, and r = rank(F-S). Then

    N <= u + r(s+1).

If r=N there is nothing to prove. Otherwise select r+1 cyclic-consecutive Fourier rows including a row whose S-support has size u. Their combined S-support has at most u+rs columns. If that were <= N-r-1, at least r+1 columns would be identically zero in those rows of S. The corresponding square submatrix of F-S would be a nonzero column-scaled Vandermonde matrix on distinct roots, hence invertible. This contradicts rank r. Cyclic wrap merely changes exponents by multiples of N. Replacing w by w^(-1) and multiplying by N^(-1) proves the inverse-Fourier case.

Equivalently, a nonzero linear combination of r+1 consecutive Fourier rows is a nonzero monomial times a degree-at-most-r polynomial on N distinct roots. It has at least N-r nonzero values. A nonzero left dependence among the same rows of F-S therefore forces u+rs >= N-r. This also gives the precise coding-theoretic comparison in section 3.

### 2.2 Inverting the architecture

A literal forward scan y_i = a_i y_(i-1)+b_i x_i is invertible exactly when all b_i are nonzero. Its inverse is x_i = b_i^(-1)y_i-a_i b_i^(-1)y_(i-1), so the inverse matrix is bidiagonal; the backward version is the transpose-oriented analogue. Each has a boundary row with just its nonzero diagonal entry.

For an invertible K_j = I+U_j V_j^T,

    K_j^(-1)-I = -K_j^(-1)U_j V_j^T,

so rank(K_j^(-1)-I) <= rank(U_j V_j^T). This argument does not presume that a smaller auxiliary matrix is invertible. Invert the entire word and replace each inverse broadcast by identity. A telescoping product expansion gives rank(F^(-1)-S) <= B, including arbitrary interleaving; no factors are commuted.

Every row of S has support at most 2^t. The boundary row of the leftmost bidiagonal factor, moved/scaled by any monomial to its left, has support at most 2^(t-1) after the remaining factors. Thus u <= 2^(t-1), s <= 2^t. Inserting the actual residual rank r <= B into the rigidity inequality proves the formula. When t=0, S is an invertible monomial and u=s=1, giving N<=1+2B.

The N=64 integer lower bounds for B at t=0,...,7 are 32, 21, 13, 7, 4, 2, 1, 0. These are necessary conditions, with no claimed matching constructions or optimal general tradeoff.

### 2.3 Costs must be stated separately

The theorem counts representation primitives and ranks. **For this cost corollary, set B to the actual sum of broadcast ranks**, rather than an arbitrarily loose upper bound. If an implementation additionally charges a full length-N pass for every scan and every independent rank-one broadcast contribution, then work is at least a constant times N(t+B). For integer B>=0, 3B+1 <= 4^B. For t>=1 the theorem implies

    N <= (3B+1)2^(t-1) <= 2^(t+2B-1),

so t+B >= (1+log2 N)/2 and this expressly charged implementation has Omega(N log N) work. The t=0 case already requires B>=floor(N/2). This elementary accounting consequence is not a new general lower bound. Sparse or shared broadcast application, fast high-rank operators, retained state, fusion, different primitives, and other accounting models cannot be charged by rank alone.

## 3. Primary-source comparisons

### 3.1 Exact classical ingredient: BCH/shift bound

[Feng, Hollmann and Xiang](https://arxiv.org/pdf/1804.00367), Theorem 3.2 and Example 4.1 (pages 5–6), give the shift bound and its consecutive-zero BCH specialization over fields of characteristic zero or positive characteristic coprime to the group order. Their section II supplies the root-extension convention. Take G=Z_N and use the root-containing field as the base field. A nonzero combination of r+1 consecutive Fourier rows has Fourier support in a cyclic interval of length r+1, hence N-r-1 consecutive zero Fourier coefficients. Example 4.1 with d=N-r gives support size at least N-r; the auxiliary all-zero-spectrum code contributes no nonzero exception. Combined with support at most u+rs, this gives exactly the rigidity ingredient above. Their Theorem 6.2 also gives the support-product uncertainty principle, but the consecutive-zero form is the precise match here. The scan boundary row and telescoping architecture accounting are the source-specific application, not claims that the paper already states the displayed scan/broadcast tradeoff. No historical-priority conclusion follows.

### 3.2 Exact representation distinction: GIRS/SSS

[Chandrasekaran, Epperly and Govindarajan](https://arxiv.org/pdf/1911.05858), Theorem 2.4 (page 11), identify optimal sequentially semiseparable state dimensions with the two off-diagonal cut ranks on the line. Equations (2.6)–(2.8) use separate state transitions and input/output maps. Thus source section 2's quasiseparable optimum 3 for F8 corresponds to general generators of dimension at most 3, not automatically three independent literal scalar scans. The published presentation uses real blocks; the finite-dimensional rank-factorization construction carries over to complex blocks, while no general finite-field extension is needed for this comparison. Arbitrarily permuted multi-stage scan words do not maintain one common line graph, so this theorem alone is not the main interleaved scan bound. This is an exact match for the representation caveat and a qualified nonmatch for the full circuit grammar.

### 3.3 Named Delvaux–Van Barel comparison: access-limited

The [official KU Leuven record](https://lirias.kuleuven.be/1537109) confirms the 2008 paper's study of maximal rank-deficient submatrices at prime-power order. Full-text DOI/publisher retrieval failed, and the official TW470 report route redirected to inaccessible institutional SSO. The accessible abstract is insufficient to certify an exact theorem match or nonmatch to this all-N, arbitrary-interleaving, field-algebraic bound. Record this precise access limitation; do not infer novelty from it. The completed positive primary mapping above independently satisfies the recorded “identify a primary theorem … or record a qualified nonmatch or specific access blocker” gate.

## 4. Other claims in the second source

The parity induction for at most three nonzero dyadic characters is sound in characteristic different from two. In the mixed-parity case, the parity class with one monomial prevents both z and -z being zeros. In the one-parity case, squaring reduces the root set and exponent classes by a factor of two. Consequently a nonzero combination cannot vanish on five of the eight roots. Every 3-by-5 F8 submatrix has rank 3. The parity order (0,2,4,6,1,3,5,7) has both cut-rank sequences (1,2,3,2,3,2,1), so optimum quasiseparable order is exactly 3.

The 3-by-3 lower-bidiagonal matrix H with diagonal and first subdiagonal equal to 1 supplies the stated strict-lower literal-scan counterexample: a1*b0=1 and a2*b1=1 imply a2*a1*b0 != 0, inconsistent with H20=0. Adding a diagonal or a same-order backward scan cannot repair that strict-lower entry. This fixed-order caveat must not be inflated to a claim about all representations or all endpoint permutations. A broader scalar state system h_i=x_i with output x_i+h_(i-1) already realizes H, illustrating the distinction constructively.

The complete-length independent-channel macro work statement remains conditional on its specified visit accounting. Its complex Fourier submatrix estimate uses Frobenius/operator norms, which is not by itself a finite-field rank proof. The source expressly does not verify the external unitary/Givens theorem; this review leaves that dependency unpromoted. No missing Givens theorem is needed for the scan/broadcast theorem or its classical comparison.

## 5. New checks and replay limits

`checks.py` imports only Python standard-library modules and contains newly written exact modular arithmetic. Results in `CHECK_RESULTS.json`:

- All 6,859 N=3, F7 matrices with at most one nonzero per row satisfy nonuniform rigidity.
- All 6,272 F8 3-by-5 minors over F17 and F97 have rank 3; both parity witnesses have the claimed cut ranks.
- 252 random inverse words at N=2,3,4,6,8,12 over F97, with t=0,...,6 and interleaved nonsingular monomials/broadcasts, satisfy support, boundary-row, telescoping-rank and rigidity checks.
- 2,505 cyclic-consecutive Vandermonde minors across N=2,3,4,6,8 are nonsingular.
- All 2,401 relevant F7 parameter tuples support the literal-scan counterexample.
- Integer threshold formula and the old-versus-refined comparison were checked for 2<=N<=512 and 1<=t<=11; the N64 table matches.

These consistency checks support the all-N proofs; they are neither a proof by sampling nor a transform implementation. Historical N64 network/determinant certificates and the source's original checker remain unexecuted and unclaimed as replayed.

## 6. Guarded proposed native disposition

Close the current comparison/one-way obstruction activity; preserve all source history and proof text, priority 42, and the earlier rational-degree result. Leading action/pass-stop text must name both completed comparison substages and the unsolved section-5 alternative. Preserve the explicit distinctions between exact fields, complex norm arguments, representation budgets and paid execution costs. No deletion is proposed.

Reopen only for a concrete changed-interface construction, a genuinely different theorem, or an appropriately scoped attribution question with new primary evidence. In particular, keep nonunitary overlapping bidirectional sums, shared computations, extra-state/nonlocal ports, changing geometry and efficient growing-degree evaluation unproved. Do not turn a CLOSED workflow status into a statement that these alternatives are impossible or that historical novelty is settled.
