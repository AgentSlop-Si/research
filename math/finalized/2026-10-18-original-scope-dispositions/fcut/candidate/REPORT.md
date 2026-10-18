# M-FCUT: original-scope whole-owner disposition

18 October 2026 UTC. Repository evidence is pinned to `e3099aa1657e9b9fe8e053282c0cdb658d50e7d3`.

## Recommendation

**Recommend CLOSED for the existing M-FCUT owner, at its complete original accepted theorem-and-bounded-comparison scope. Retain priority 42 as historical triage metadata.** This is a disposition recommendation, not an externally applied status change.

All original mathematical clauses are covered by the accepted audit and reaffirmed in the accepted 17 October comparison review. The four specifically named primary-source comparisons have met their documented stopping condition. The native current record explicitly states that no proof obligation remains for the recorded density theorem. No exact unmet clause of that original owner is identified by the examined evidence.

The owner can close without resolving worldwide priority: its retained classification remains “specialized result; historical novelty unassessed,” and no publication-novelty claim is made. This recommendation closes the whole existing bounded owner, rather than counting the already-complete comparison as a new child activity or silently replacing the original theorem with a weaker statement.

## Exact owned statement

Let p >= 3 be prime, alpha and beta arbitrary Hamiltonian cycles, and a,b arbitrary complex edge-weight vectors, including zero entries. Let L and R be invertible monomial matrices. For

C = (I - D_a P_alpha) L^{-1} F_p R^{-1} (I - D_b P_beta),

every adjacent-alpha pair satisfies

|supp(C_i) union supp(C_alpha(i))| >= ceil(p/2),

and therefore nnz(C) >= ceil(p ceil(p/2)/2).

Neither difference factor must be invertible. Singular all-one cycle weights and all-zero edge vectors remain permitted. At composite N, the local premise is retained only when each relevant moved three-frequency profile is primitive-affine (an arithmetic progression with step coprime to N); a unit-step affine cycle and affine left endpoint permutation with coprime slopes suffice for the global bound. Arbitrary invertible right monomial factors remain harmless.

This is a density theorem for the intermediate matrix. It is not a quadratic arithmetic-work lower bound, a numerical-stability result, a production implementation, or an unrestricted faster Fourier algorithm.

## Clause-by-clause closure matrix

The machine-readable counterpart is CLOSURE_MATRIX.json.

| Original clause or recorded task | Disposition and evidence | Remaining owned obligation |
| --- | --- | --- |
| Complex prime p >= 3; arbitrary Hamiltonian alpha and beta | ACCEPTED. Original audit's theorem and independent proof review; 17 October independent review's FCUT proof-boundary check | None |
| Arbitrary complex edge weights, including zeros | ACCEPTED. Adjacent coefficient matrix has rank two for every weight choice; propagation uses multiplication only | None |
| Singular difference factors allowed | ACCEPTED. No inverse of either difference factor and no division by a cycle weight occurs; zero-mark case is explicitly disposed of | None |
| Arbitrary invertible monomial endpoints at prime length | ACCEPTED. Endpoint changes preserve distinct frequency labels and rank; column permutation/scaling preserves each three-column premise | None |
| Local pair union >= ceil(p/2) | ACCEPTED. m marked incoming edges partition the single Hamiltonian cycle into m directed paths when m>0. Every path has at most two vertices; m=0 contradicts rank-two premise | None |
| Global nnz >= ceil(p ceil(p/2)/2) | ACCEPTED. Sum the p pair-union inequalities; the sum of unions is at most twice the total row support | None |
| Composite primitive-affine extension | ACCEPTED at exactly that scope. Primitive-stride nodes give an invertible three-column Vandermonde; arbitrary composite non-affine triples were never included | None |
| Prime p >= 11 two-resolvent no-go consequence | ACCEPTED as an inherited consequence, already subsumed by earlier separator arguments. Five candidate support coordinates contradict ceil(p/2)>=6 | None; no additional discovery credit |
| Explicit p=11 certificate | ACCEPTED with the existing degree wording correction: -2z^2+z^4-z^7+2z^9 has degree 9, hence at most 10 | None |
| Conditional q-column path generalization recorded in audit | ACCEPTED as the conditional propagation argument: if every q-column restriction has rank two, paths have at most q-1 vertices | None; no arbitrary target full-spark premise added |
| Named Tao/Pernet/GIRS/nullity comparison | COMPLETE with accepted source-specific ingredient matches and qualified nonmatches; original proof guards preserved | None |
| Historical worldwide attribution | UNVERIFIED qualification, retained explicitly. The comparison does not certify novelty or rule out all other reductions | No finite unperformed original theorem/comparison clause is specified |
| Final Delvaux–Van Barel paper | Earlier completed comparison remains inherited evidence. Final 19-page primary body was not freshly recovered or reread in the 17 October pass | No mandatory fresh comparison is identified; a genuinely new attribution question would require the readable primary body |
| Arbitrary composite profiles, finite-field full spark, products of sums, fast dense centers | Outside the original accepted theorem's scope | Do not create replacement owner obligations from these exclusions |

## Why the original proof closes the full stated scope

Put H=(I-D_a P_alpha)L^{-1}F_p R^{-1}. Two adjacent left rows have coefficient matrix [[1,-a_i,0],[0,1,-a_alpha(i)]] on three distinct moved Fourier labels. Its rank is two even when either weight is zero. Prime Fourier full-minor nonvanishing makes every three-column restriction of these two H rows have rank two. Right monomial factors only select and scale distinct columns.

For a destination j=beta(k) outside the two output-row support union, the two-vector H[:,j] equals b_k H[:,k]. Delete the incoming beta edge at each marked destination. If m>0 destinations are marked, a single Hamiltonian cycle becomes exactly m paths covering all p vertices. Along any path, all vectors are scalar multiples of the first; no division is used, even through a zero edge. A path with three vertices would contradict the three-column rank-two premise, so p<=2m. If m=0, the same propagation around the whole cycle gives rank at most one, contradicting that premise. This closes singular and zero-weight cases rather than discarding them.

For all p adjacent pairs, p ceil(p/2) is at most the sum of pair-union cardinalities, which is at most 2 nnz(C). Taking the integer ceiling gives exactly the original global bound. At composite length the stated primitive-affine condition supplies the same local rank premise by a Vandermonde determinant; nothing requires or claims arbitrary composite full spark.

This reread is a reasoned synthesis of accepted proof evidence, not a new theorem or a replay of historical computation.

## Completed comparison and attribution boundary

The complete accepted report and its independent review are retained byte-for-byte in sources/.

- Tao's Lemma 1.3 supplies the complex prime nonzero-minor ingredient and credits Chebotarev.
- Pernet's definitions and algorithms describe fixed-order quasiseparable representations and matrix-vector upper costs once generators are available; dense entry count alone supplies no arithmetic lower bound.
- GIRS gives common-graph closure and complementary-cut inversion identities. Independently routed endpoints do not automatically provide a common useful graph or constructor.
- Nullity supplies an invertible-matrix complementary-submatrix rank identity. It cannot be applied through a singular difference factor in the FCUT theorem.

The inspected primary statements do not themselves supply the singular-safe two-vector marking/path-counting synthesis. This is a qualified nonmatch to those statements, not a proof of worldwide originality or of impossibility of another reduction. The accepted comparison and review both explicitly preserve this distinction.

## Reconciliation with the current open label

The current native row still reads TO RESEARCH, priority 42. Its recorded reason after the 17 October comparison is historical attribution; its pass/stop text simultaneously says the named stopping condition is met and the accepted theorem has no remaining proof obligation. The old “keep TO RESEARCH” language accurately records that earlier comparison pass's limited editing mandate and broader-attribution caution. It is not an additional mathematical clause of the original theorem.

The present original-scope disposition supersedes that worklist choice only in the recommendation. It does not erase the historical wording, claim a new external change, or reinterpret an unknown priority fact as known. An unbounded request to eliminate every possible prior-art overlap has no established finite stop criterion here and is not silently adopted as a perpetual owner obligation.

No new specific readable source, purported competing theorem, hypothesis mismatch, or outstanding accepted-proof defect has been identified. The conditional instruction to undertake a new owner-specific comparison if such a question arises does not itself instantiate one. The inaccessible final Delvaux–Van Barel PDF is therefore retained as an exact reread limitation, not used to reopen its inherited comparison or fabricate a missing theorem clause.

## Explicit pass/stop criterion

Close this existing owner when all three tests hold:

1. Every original theorem clause, including zero weights, singular difference factors, endpoint freedom and the exact composite restriction, has accepted proof evidence.
2. Each specifically assigned bounded primary-source comparison has either an exact ingredient mapping, a qualified nonmatch, or a precisely recorded access limitation consistent with the task's permitted stopping condition.
3. No concrete original-scope proof or comparison obligation remains, and all unproved novelty, computational, numerical and out-of-scope extensions are retained as qualifications.

**All three tests pass on the pinned sources and fresh native receipts.** Stop further generic research for this owner. Reopen only on a concrete challenge to an accepted clause or a specifically assigned new source/theorem comparison with a defined question; neither is currently established in the inspected evidence.

Missing evidence required for original-scope closure: none. Missing evidence for a new worldwide-priority conclusion or fresh final-paper reread: not supplied, and not claimed.

## Evidence and integrity

- [Original accepted audit, pinned](https://github.com/AgentSlop-Si/research/blob/e3099aa1657e9b9fe8e053282c0cdb658d50e7d3/math/archive/objects/68/688ee118a6fc3855176ccedf78ff6663307af84d70b10ecaae51ed9c4aa154b2__688ee118a6fc3855176ccedf78ff6663307af84d70b10ecaae51ed9c4aa154b2__FCUT_AUDIT.md): exported SHA256 24708f0c38135ac7630eb9bff1e0b68059e4b553074fc5eff019b9643b161977; Git blob 860160eb3df2e6b5afeab3e26254792f05a2787d. The original source SHA256 in its filename, 688ee118..., is different; original unsanitized bytes were not recovered in this pass.
- [Completed comparison, pinned](https://github.com/AgentSlop-Si/research/blob/e3099aa1657e9b9fe8e053282c0cdb658d50e7d3/math/finalized/2026-10-17-research-finalization-0006/structural/REPORT.md): SHA256 b16cbf5570b35aa64c8e6e7d428e8b693babb302ae39cc286213b85fd539a62e, exactly the report hash accepted by the independent review.
- [Independent comparison review, pinned](https://github.com/AgentSlop-Si/research/blob/e3099aa1657e9b9fe8e053282c0cdb658d50e7d3/math/finalized/2026-10-17-research-finalization-0006/independent_review/structural/INDEPENDENT_REVIEW.md): SHA256 1b3889cef38b536cab14bfb092451dee31678dbd2a2616b3889395bbd7460226.
- Fresh native metadata and bounded current cells: Catalogue header and owner row, novelty header and owner row, Research overview header and owner row. The exact receipts are preserved separately. Their current fields agree on accepted theorem scope, priority 42, completed named comparison, and retained historical-priority uncertainty.
- Catalogue's REVIEW-09 and its 15 controls are accepted as attributed native history. That review's full separate packet and historical programs were not recovered or rerun here. Original audit control counts are likewise historical evidence, not current execution.

All three retained remote file bodies have independently recomputed Git blob hashes matching the connector receipts. No external writes, new generic literature search, historical code execution, imports, compilation or mathematical test replay occurred. New local scripts only extracted source/receipt data, computed hashes and checked this packet's consistency.

## Proposed minimal application

After independent acceptance of this disposition, update only the existing owner's current status to CLOSED and prefix its current action/pass-stop fields with this original-scope disposition. Preserve priority 42, stable identity, all historical text, accepted proof scope, source hashes, and novelty classification. Remove only this existing owner from any synchronized open-owner index. Do not create a child, extension owner or new canonical discovery. Native edits, exact postwrite readback, index changes and aggregate counts are outside this read-only deliverable and are not asserted here.

