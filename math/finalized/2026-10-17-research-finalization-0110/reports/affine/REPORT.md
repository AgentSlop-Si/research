# Neglected finalization survey: one completed comparison and one next candidate

17 October 2026 UTC. Read-only baseline: repository `d844509088e022fc48d4f02ca378022a9ce67702`; live workbook 88 CLOSED + 239 TO RESEARCH = 327 views.

## Result

**M-AFFINE-STEP is nominated for closure of its existing accepted-theorem-plus-qualified-comparison stage after independent review.** The GIRS/nullity comparison below is now complete. It identifies exact classical rank ingredients and the additional dyadic geometry needed for this owner. Its current owner explicitly records no remaining proof obligation for the qualified theorem and allows a qualified primary-source nonmatch as its stopping condition. This is one existing record finalization, not a new theorem, novelty claim, implementation acceptance or unrestricted Fourier lower bound.

**M-POSITIVE-PHASE is the strongest second candidate.** Its complete current owners and accepted review likewise show no selected missing theorem. A precisely bounded primary comparison remains and is proposed below; it is not declared completed here. Keep its present status and score until that comparison and independent review are done.

Two apparent alternatives were rejected: M-CUT-EXPANDER still has a genuine coefficient-realization/stronger-obstruction question, while ALG-063 needs a chosen model-matched input-recognition comparison and retains separate implementation/field/bit/numerical questions. Neither is closed by this survey.

No external writes or supplied-program execution occurred. No new numerical experiment was run. Historical finite checks remain historical evidence. Full current owner histories were read for the two selected candidates; full accepted source audits were read for all four screened candidates. This does not claim full proof review of all 239 open views.

## 1. Why M-AFFINE-STEP can finish

Current owner bindings are Catalogue row35, novelity breakthough row57 and Research overview row74, with priority42. The live Catalogue Z35 says there are no remaining obligations for the qualified theorem, retaining strict-witness and finite-length implementation qualifications. AE35/AF35 require a primary theorem with an exact hypothesis, formula and cost-model mapping, or a qualified nonmatch/access boundary. Overview F74 identifies comparison as the leading open task. No all-routing construction, scalar-circuit lower bound or production executor is promised by these rows.

Read in full: the accepted Phase26 audit, the complete later M-AFFINE-STEP outcome in REVIEW-09, and all three current owner rows including their history. The accepted audit has a sanitized public derivative, whose exact bytes have SHA256 `c96ca40bf737883b3a5d6287a3a48d39c8a05919140c93890afa25ff3eead94d`, Git blob `aa063e77890b47fd38cc68f53de9a9d7abddaf60`. Its filename's `7a182b...` is the original historical identity, not the public derivative's content hash. Original archive/member recovery is not newly claimed.

[Complete accepted audit](https://github.com/AgentSlop-Si/research/blob/d844509088e022fc48d4f02ca378022a9ce67702/math/archive/objects/7a/7a182b9a8073acd8ee16dfb711407de35ea04adff07a32f806e7b8d8bfb1195c__PHASE26_AUDIT.md).

### Exact accepted statement retained

Let N=2^k>=8. Every term is a diagonally gauged legal weighted Hamiltonian-cycle Green inverse. After all affine intermediate permutations are transported to the boundary, term q has at most d_q nonzero signed-step magnitudes and b_q exceptional directed edges. Let Q count occurrences in a sum/product expression tree, T=sum d_q, s the number of distinct transformed magnitudes, and r=floor((N-1)^(1/s)). For s>=1, a common balanced character cut gives

rank <= min(N/2, T floor((N-1)/r)+sum_q floor(b_q/2)).

The accepted proof handles s=0, d=0 and Q=0 separately. For fixed per-term d,b and fixed complex operator error epsilon<1/sqrt(2), the required occurrence count is at least (1-o(1)) log N/(d log log N). The finite-length large-exceptional-edge disjunction must be preserved before taking this asymptotic limit.

### Primary sources actually inspected

1. Chandrasekaran–Epperly–Govindarajan, [Graph-Induced Rank Structures and their Representations, arXiv:1911.05858v3](https://arxiv.org/pdf/1911.05858v3), entire section2.1, Definition1 and Propositions2.1–2.3, including proofs and the representation/construction discussion. Complementary off-diagonal rank survives inversion; sums/products add the cut-rank budgets on the same graph. Its graph-partitioned notation uses real blocks. The algebraic block/kernel arguments used here also hold over the complex field. Constructing a useful representation is separate from merely possessing rank structure.
2. Vandebril–Van Barel, [A short note on the nullity theorem, theorem section](https://people.cs.kuleuven.be/~raf.vandebril/homepage/publications/papers_html/nullity/node3.html), Theorem1, both proof approaches, and Corollaries1–2. The general formula specializes to rank(A^-1[I,J])=rank(A[I,J]) for complementary I,J and invertible A. The printed real notation does not require positivity; the kernel proof is field-algebraic. No principal-block invertibility is required by the general identity.
3. The older Boito–Eidelman lead was checked at its actual [arXiv:2308.02701v1 section2, Theorem2.1](https://arxiv.org/html/2308.02701v1): inverse lower-band structure is equivalent to lower-Green rank constraints in a specified order. This is a classical structure match, not a supplied common dyadic character cut for differently routed factors. No complete comparison of that paper's later QR/LU algorithms is claimed.

The following formulas and separation examples are deductions for this owner. They are not represented as additional printed primary theorems or new mathematical discoveries.

### Exact implication map

Fix complementary I,J after conjugating all legal interstage affine maps. For A_q=I-diag(gamma_q)W_q, global invertibility is exactly 1-product(gamma_q)!=0. Nullity gives

rank(G_q[I,J])=rank(A_q[I,J]).

Because W_q is a permutation, the off-cut nonzero entries occupy distinct rows and columns. Hence this rank equals the number of crossing edges with nonzero weights and is at most the unweighted crossing count c_q(I). Zero weights can decrease it. No generic-noncancellation, positivity or singular-value assumption is inserted.

For the same I,J,

(AB)[I,J]=A[I,I]B[I,J]+A[I,J]B[J,J].

Therefore off-cut ranks add under multiplication; the analogous sum statement is immediate. Diagonal gates contribute zero. Induction over the stated expression tree yields rank(M[I,J])<=sum c_q(I), with repeated term occurrences charged repeatedly. This is precisely the rank algebra supplied by the inspected GIRS statements. It does not count free shared-state or DAG reuse.

### What the primary rank statements alone do not supply

The source-specific additional argument is the existence of a single small cut for all transformed terms. The N points with coordinates (j a_i mod N)/N fall in r^s<N boxes. A collision gives 0<h<N and the strict inequalities r|h a_i|_centered<N. For dyadic N, gcd(h,N) divides N/2, so I={j:hj mod N<N/2} is balanced even for nonunit h. The directed translation crossing count is exactly |h a_i|_centered.

Hamiltonicity then improves the signed-edge budget: a cycle cannot use both orientations of an undirected edge, and incoming/outgoing cut counts agree. Thus c_q(I)<=sum_(a in S_q)|ha|_centered+floor(b_q/2). This is the exact bridge from arithmetic box geometry to the classical rank algebra.

The hypotheses cannot be dropped merely by citing GIRS. At N=6,h=2 the character threshold gives a 4:2 split, so the same proof is not an all-composite balanced-cut theorem. At N=8 the permutation with successor list [7,2,1,4,3,6,5,0] consists of two-cycles, uses only signed step1, but has two incoming crossings on {0,1,2,3}, exceeding the Hamiltonian step bound1. At N=16, strides[1,2,8], h=1 fails the strict predicate because r|8|=16. These are exact countercontrols already present in the accepted proof, not fresh machine tests.

An affine map j->uj+c preserves step complexity after changing each step to ua. Arbitrary independent permutations do not. A separate natural ordering for each factor supplies no common physical cut for the product. One can take a union graph for GIRS, but must then actually bound that graph's relevant cuts; the rank proposition does not produce a small boundary automatically.

### Fourier and norm comparison, with costs kept separate

After outer row/column routing, the certified block may use different balanced row and column sets. For any such subblock H of the fixed normalized complex Fourier matrix, ||H||_F^2=N/4 and ||H||_2<=1. If a candidate block has rank rho<N/4, the singular-value tail gives

||M-Fhat_N||_2 >= sqrt((N/4-rho)/(N/2-rho)).

For fixed epsilon<1/sqrt(2), this forces rho>=c_epsilon N, where c_epsilon=(1-2epsilon^2)/(4(1-epsilon^2)). Combining that requirement with the accepted common cut, not the GIRS rank statement alone, produces the occurrence lower bound. Even-row/first-half-column restriction has all singular values1/sqrt(2), so that constant cannot be improved from arbitrary balanced-block singular data alone. This does not prove the Green architecture attains it.

The source compares a matrix represented by an occurrence-counted expression with a fixed target. It is not a lower bound on scalar work, coefficient generation, field/root preparation or arbitrary algorithms. One legal weighted-cycle solve has a charged O(N) exact-field scan; representation length and the work of a specified eager evaluator are distinct quantities. The primary structure theorems do not discharge setup, bit complexity, floating stability or a production implementation. None of those excluded models is silently certified here.

### Older leads and honest stopping condition

The existing final Delvaux–Van Barel Fourier-minor lead is retained. Its complete final19-page paper was not newly acquired/read in this pass; no theorem-number substitution from another version is made. The Mans–Shparlinski circulant-bisection lead remains bibliographic/background evidence here, not a freshly completed full-paper comparison. The Boito–Eidelman result above is restricted to the inspected Asplund statement, without certifying all later algorithms. These boundaries remain explicit even if the current row is finalized.

The existing stage requires one primary hypothesis/formula/cost comparison and permits a qualified nonmatch. That is met by the GIRS/nullity map above. A broader exact-priority inquiry would require a separately selected theorem, and non-affine routing would require a different scope. Neither is invented as a perpetual successor. The accepted theorem, every implementation qualification, source-access limitation and historical-priority uncertainty remain preserved.

## 2. Second ready candidate: M-POSITIVE-PHASE

Current bindings: Catalogue56, novelity breakthough75, overview92; priority42. Full accepted Phase36 review and later REVIEW-12 outcome were read, as were all current owners. The selected theorem comprises first-cross positive scaling, approximate ideal-real preprocessing, the necessary phase-rank gate, the stronger doubled-character positive-middle bound, near-identity exterior transfer, and the fixed exact N4 cross-ratio rejection. Its exclusions are not automatically new promised constructions.

[Complete accepted review](https://github.com/AgentSlop-Si/research/blob/d844509088e022fc48d4f02ca378022a9ce67702/math/archive/objects/3f/3f22b6b411a54f1b20c05ff9341e97bf8980801cdaaaaf5520577faaf6de1f67__REVIEW.md).

Concrete next job: make one primary matrix-scaling/metric and monomial-invariant comparison. Map the exact positive marginal equations u*(Bv)=p and v*(B^T u)=q to a readable Sinkhorn/Hilbert theorem; distinguish it from two-sided complex-unitary balancing. Then map phase rank under monomial endpoints and the Fourier flat-spectrum rank tail, explicitly deriving the owner-specific doubled-character Gram norm sqrt(gcd(2,N)N). Retain that numerical convergence does not provide finite exact algebraic masks, and high phase rank costs only one linear scan for an admitted complex cyclic Green.

Required stopping artifact: a primary-theorem hypothesis map, exact implication/nonmatch, complete arithmetic/precision boundary, and a disposition explaining whether any selected original obligation remains. Do not repeat the already completed M-SEED-BALANCE/Idel–Wolf fixed-seed comparison as if it closes this different owner. The earlier seed report screened M-POSITIVE-PHASE but expressly did not complete it. Status/score unchanged in this deliverable.

## 3. Rejected closure candidates

**M-CUT-EXPANDER:** the complete accepted Hero0 Phase13 review separates classical cut algebra, the explicit20-plan graph-capacity survivor and its denominator-free lifted compatibility identity. The earlier all-record inventory correctly records a genuine remaining coefficient realization or stronger obstruction in the surviving grammar. Graph expansion does not force noncancelling Green ranks or the Fourier identity. Finalizing a primary graph comparison could be useful, but no whole-row closure is proposed.

**ALG-063:** the complete Woodbury audit contains a substantive all-z O(N(s+1)) permuted-geometric evaluator using sparse twisted differences and at most one resonant direct output. The old supplied code's resonant exclusion and repeated-power cost remain distinct. A good future comparison is to a named raw-input sparse rational/Prony result with supplied order, z, defect support, all-output verification and setup charged. Generic classical mechanisms do not settle that complete interface, and this survey does not declare the original repaired implementation or priority question finished.

## 4. Exact proposed disposition and preservation

After independent acceptance, change only M-AFFINE-STEP's overview status to CLOSED and prepend dated comparison/completion paragraphs to its existing action, scope, evidence and stopping cells across the three owners. Preserve every older string verbatim after a history separator. Leave priority42, proof classification, novelty/assessment band, stable ID, formula links, row order and all other owners unchanged. The private exact-before/after proposal is separate from publication-safe material and requires a fresh prewrite guard.

If applied without another status change, the view census becomes89 CLOSED +238 TO RESEARCH=327. This is one completion of an existing scoped stage. It does not close M-CUT-EXPANDER, M-POSITIVE-PHASE, non-affine research or any full-Fourier construction. The public deliverable is this report and its compact source/proposal manifest; raw native exports, private paths and copied source bodies are excluded from publication.
