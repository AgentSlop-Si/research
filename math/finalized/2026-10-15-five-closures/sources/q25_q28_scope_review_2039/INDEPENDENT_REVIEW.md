# Independent scope reconciliation for Q25 and Q28

14 October 2026. Verdict: ACCEPT_SCOPE_RECONCILIATION for the two named audit and reconstruction records, for the revised V2 semantic proposal, with publication guards below. This is not a new theorem acceptance, literature-priority finding, implementation review, or certificate replay.

## Decision and exact records

- Q25, “Audit two-sided gauge obstruction”: Research queue row 28 (stable ID in A), Research overview row 161 (stable ID in B). P09, R25 and R26 already complete the named mathematical audit.
- Q28, “Reconstruct outer-stability extension”: Research queue row 31 (stable ID in A), Research overview row 162 (stable ID in B). P07 §D, with §B dependency, and R35 already complete the named reconstruction.
- Both queue rows explicitly say “Proof closed” in C and D, “No additional constructive premise for the stated result” in G, and “Not applicable to abstract proof” in J. Q28's H entry Q22 is a dependency, not an uncompleted implementation demand; P07 §B and the recorded accepted fixed-layout gate supply that dependency.
- Their overview E cells still say TO RESEARCH. The generic leading attribution reason in F does not identify an unfinished mathematical obligation within either named audit. Q25's attribution remains unresolved and must remain visible. Q28's one specified final-paper comparison is recorded complete; worldwide attribution remains unresolved.

The legitimate change is therefore CLOSED / named audit stage complete for these two records. It is not “all research on these models is finished.” No theorem or discovery is newly counted. No broader record inherits closure by sharing a proof or dependency.

## Q25 source and mathematical boundary

P09 is the 4,728-byte proof/review `09-two-sided-gauge.md`, SHA256 `74e519a3d3d3ce8cc210252ba30bdd360d83848a90b67ee7dda554cd4f9baf2f`. R25 and R26 are ACCEPT records in `review/DECISIONS.json`, SHA256 `bdc860f29e131a0eeeb99e06a2c21506a0ef54a61ca7d1c6c121eaf569b20d0c`, each explicitly binding that P09 hash.

I read the actual P09 text, including its independently stated spectral derivation, operator sharpening, legal-edit interpretation and source-review limits. Its accepted exact impossibility permits arbitrary invertible **diagonal** endpoints, with even s≥4 and the s=2 exception retained. The metric floors require unitary diagonal endpoints. “Arbitrary invertible endpoints” without “diagonal” could incorrectly widen the theorem to arbitrary invertible matrices and must not be the new leading description.

The displayed argument has no uncompleted internal mathematical step: for the two commuting involutions X,Y, the four joint eigenspaces give the rank-four phase-ratio spectrum; the commutator has squared Frobenius lower bound N(1−rho), with rho=2/[s sin(pi/s)], and operator upper bound 2. A rank-k edit induces rank at most 2k in the commutator. Singular-value tail bounds therefore yield the accepted Frobenius floor and the sharpened operator floor

  (1/2) sqrt(max(0, [N(1−rho)−8k]/[N−2k]))

for 2k<N, with zero used for 2k≥N. The proof explicitly records closure of its earlier identity-gauge full-rank dependency by an all-size polyphase proof. That earlier dependency acceptance is inherited here, not a new reconstruction of its historical proof package.

Occurrence-wise edit telescoping requires each intermediate resolvent inverse used in the argument to exist. The source explicitly disclaims an unrestricted Fourier circuit lower bound and notes that linearly many edits may still have linear application cost. None of those restrictions is an unfinished task in the named audit. Historical priority remains unresolved. No numerical production validation is implied or required for this abstract audit's closure.

## Q28 source and mathematical boundary

P07 is the 17,620-byte `07-matrix-audits.md`, SHA256 `eaf8507f21bfbf28058008b49eb98b7aec4004669cd7e4d6360ca4816b9ec4df`. R35 in the same exact decisions file records ACCEPT for general and approximate outer-stability bounds and binds that hash. The original proof archive is `Research-cycle-proofs-and-fusion-queue-v1.zip`, SHA256 `cf3d923f105de9065a3426cb08b048e676d428fc4427998f8a098c724b1d723b`. I checked the archive hash and the exact P07, P09 and decisions member hashes against the local copies.

I read §B and §D. The retained model is N=256, U=F256/16 over C, the fixed saved binary-linear affine permutations, four order-at-most-one quasiseparable square stages, and the mask64 rank cap 16. The decisive input is sigma17(K)>alpha, alpha=3sqrt(2)/5, supplied by the accepted rational fourth-moment certificate. This pass does not replay that certificate or claim to possess a newly verified AFFINE_LAYOUT.json body. The recorded layout hash remains `77c5c0fcdcfa850dac44dd34dbe3188539aa9cb143f22978b86127add76b8e45`.

For invertible diagonal references D4,D1, §D retains the selected-coordinate minima m4,m1 and outer inverses C4,C1. The rank cap and best-rank approximation give

  ||C4 U C1 − D4 U D1||2 > m4 m1 alpha.

The exact difference decomposition gives the two-term perturbation bound with ||C1||2 and ||D4||2. The approximate bound also pays e||C4||2||C1||2, where e=||U−M||2. When e<1, invertibility of M, and therefore all square stages, follows; the e≥1 corollary is trivial because alpha<1. For unitary diagonal references with both outer-inverse distances at most epsilon, the retained corollary is

  e ≥ max(0, alpha−epsilon(2+epsilon))/(1+epsilon)^2.

These are completed conditional inequalities. The selected minima, inverse norms and exact affine layout cannot be discarded. Nonlinear Toffoli-composed layouts, general N, off-neighborhood outer synthesis and full four-stage feasibility are outside the accepted conclusion.

The actual current broader record M-OUTER-STABILITY remains TO RESEARCH at Research overview row 235, Catalogue row 120 and novelty-table row 166. Its explicit outer-stage synthesis and full-complex-feasibility tasks remain open. Q22 or any other broader/related record is not closed by this review.

## Q28 source-comparison evidence

The local full comparison `DELVAUX_FINAL_COMPARISON.md` has SHA256 `596cbc312fdb89224470905dcb8e188e86b050e7cdac6a9e84e17a3556883817`. I read its source/scope, fixed-layout paired-Jacobi/outer-stability subsection, conclusion and remaining questions. Its `STATUS_DELTA.json` explicitly binds the same report hash and declares the final 2008 article comparison complete for that article, not worldwide priority complete.

The Source comparisons row 13 value `af33370c7d4b8f3853d36c01b512b007512886431af4963cdc6d7638af89aae4` identifies the primary PDF, **not** the comparison report. That distinction is preserved. This review verifies the recorded comparison and its local report; it does not claim a new independent reading of the primary PDF. The report's unresolved 2007/general-specialist comparisons remain separate literature questions and are not silently marked completed.

## Current stop conditions and count impact

The current stop field requires resolution only of the explicitly named scope with source-bound evidence and independent review, without global closure, novelty or runtime inference. P09/R25/R26 and P07/R35 satisfy that named audit/reconstruction condition. Treating every general priority reservation as a new mathematical failure would repeatedly reopen already accepted audits; treating the reservations as solved would also be wrong. The proposal must retain them as unresolved and separate.

The independently decoded 20:00–20:01 snapshot has 331 records: 45 CLOSED, 282 TO RESEARCH and 4 INTAKE_ALIAS. Those remain the observed counts until authorized writes and readback succeed. This proposal contributes only a **+2 CLOSED / −2 TO RESEARCH / 0 alias** scoped-record delta if both target records are still open when applied. New theorem, new discovery and new canonical mathematical-result counts are all zero. Cumulative future totals must be computed from the ordered, deduplicated publication batches; this review does not assert a future global total.

The numerical priority 37 on each of Q25 and Q28 is unchanged by this review. No novelty promotion or automatic priority change is justified.

## Publication guards

1. Resolve Q25 and Q28 by exact stable ID and reread all destination preimages immediately before an authorized write. The inspected data is an existing snapshot, not a fresh live read.
2. New Q25 leading text must say invertible **diagonal** endpoints and unitary **diagonal** endpoints, retain even s≥4 and the s=2 exception, and retain the rank/edit/inverse guards.
3. New Q28 leading text must retain the fixed N256 affine layout, rank16 gate, selected minima, inverse norms, approximate-error split and off-neighborhood parent obligations.
4. Preserve historical text byte-for-byte, existing notes, formulas, styles, links and numeric priorities. Update current proof-status summaries consistently so that “recorded follow-up open” is not left as an unexplained leading description after scoped closure.
5. The semantic draft is not an executable Sheets request. It must be rebuilt against live cells, including correct UTF16 rich-link offsets, then read back. This review grants no external write authority.
6. Preserve Q25 exact-application/worldwide priority and Q28 worldwide/other-source comparison gaps. No implementation, speed, global four-stage infeasibility or unrestricted lower-bound conclusion follows.

## Exact proposal reviewed

The active proposal is `global_status_consistency_2031/Q25_Q28_NONEXECUTABLE_SEMANTIC_DRAFT_V2.json`, SHA256 `8d82d604c3fbc25b4a594f60d9a002e4b5d47ae14abffdb278b406a9d8668d41`. All 12 semantic cells at overview rows 161/162, columns C/E/F/N/P/Q, match the independently decoded exact preimages. The ten narrative additions preserve their full old text as a verbatim suffix; the two status cells propose TO RESEARCH to CLOSED. No other cells or numerical priorities are touched. V2 explicitly supplies the endpoint and model guards above and updates N161/N162 consistently.

V1, SHA256 `fa37dedbb89b732a9c053291c4393413244a0f7936b754eacb18669a0e79a307`, is superseded: its new endpoint shorthand and missing current proof-status addenda required clarification. The active V2 repairs those presentation issues without changing the accepted mathematics. This verdict does not approve the unrelated findings in the broader global-status ledger. The remaining “independent review pending” draft labels should be changed to an accurate dated acceptance label only in the eventual separately guarded publication request.

## Verification depth

Fresh read-only bookkeeping independently rehashed five source objects, matched three original ZIP members, rehashed all 17 recorded input snapshots, decoded eight selected native rows directly, and checked all three review-to-proof bindings. No historical program was run, imported or compiled. No new mathematical test or finite census was used to relabel old acceptance as a new theorem. All external state is unchanged.
