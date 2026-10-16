# ALG-071: full-source finalization and archival boundary

16 October 2026 UTC. Read-only source review. No supplied program was executed, imported or compiled, and no spreadsheet or GitHub state was changed.

## Decision

**Retain the whole ALG-071 owner as TO RESEARCH, priority 12.** Its accepted whole-ordered-block cache mathematics and exact supplement-source binding are complete at the recorded scope. They should not be repeatedly dispatched. Production qualification remains unfinished. Whole-owner mathematical-value archival is not yet justified, because an expressly linked owner source specifies an unresolved budgeted spectral-materialization successor that the short current row omits.

This is not a claim that the successor is novel, important, or already a well-posed theorem. Its precise optimization model and its relation to classical materialized-view selection remain unassessed. An old proposed extension is not automatically selected as a new active research task. Before whole-owner archival, it needs a scoped completion, an exact prior-theorem implication, or an explicit decision to exclude it from the continuation being archived.

The completed cache analysis can be retained as a finished substage. The proposed owner edits only make the scope boundary visible; status, priority, proof verdict, novelty class, accepted scope and all history remain unchanged. Conditional counts remain **83 closed / 244 open / 327 views**, provided no other owner changes concurrently.

## 1. Sources actually recovered and read

The live owners were read on 16 October: Catalogue A172:AF172, novelity breakthough A210:Z210, and Research overview A298:Q298. Native values, formulas, notes and hyperlinks are retained privately and excluded from this publication. Current repository main was verified as `e5d46232f0d819af518bff7dcbedbcbf2e3d0286`.

The complete manuscript and full independent review were recovered from a nested archive, not inferred from the row's summary:

- Manuscript `research_cycle_1453/random_dag/RESULT.md`: 23,539 bytes, SHA-256 `60efd612850f431a13e29f31cc3019b8b3539e54ccce0d5130dfa8a5713b833d`.
- Full review `research_cycle_1453/random_dag_review/INDEPENDENT_TRADEOFF_REVIEW.md`: 15,633 bytes, SHA-256 `eae4107b2a7366b7df44932be688cf491e90d59ae686fbcaeca8843842478890`.
- Both are inside [the pinned accepted checkpoint ZIP](https://github.com/AgentSlop-Si/research/blob/e5d46232f0d819af518bff7dcbedbcbf2e3d0286/math/checkpoints/2026-10-10-1553/prior_checkpoints/accepted_fourier_research_checkpoint_2026-10-10.zip). The local nested ZIP is 335,871 bytes, SHA-256 `300218ec63ef4bfe0bb3a428b3697f3d3964e82b98367627f915ab1a85a0bc9e`; its independently calculated Git blob ID `1430dfa18f0d8f38412f907aed2f85dbc25a498f` matches the connector's pinned repository identity.
- The separate receipt is the declared normalized export, SHA-256 `0473a03072b549a95228eb5f57aa7a2ec0fc0b3f403db88777a8bb691eb73cde`. It is not the canonical original receipt `02ace1b320ce070dcf956e772cba200d2000b98f127f5493d246abf097ee3a81`. The original receipt remains unrecovered; no original-versus-normalized semantic comparison is claimed. Exact manuscript/review recovery does not depend on pretending these receipts match.

All three original owner-listed engineering texts were fully read and hash-checked: selective FFT README `e5e5c4d…` (5,288 bytes), query-engine README `4bdb965b…` (5,056 bytes), and HARDENING_NOTES `e00564ed…` (4,990 bytes). The latter README explicitly links the full research, relation-view, arbitrary-query and adaptive-organizer texts. Those were fully read too, along with the native adaptive API README. The organizer and its linking README were independently fetched at the repository seal and match the local bytes exactly.

This closes this review's evidence-access gap. It does not newly close a scientific gap that the owner had already recorded closed on 10–11 October. Earlier REVIEW-20 source absence remains preserved as dated history.

## 2. Exact mathematical value of the accepted cache supplement

For N=2^L and independent uniform symbols from a fixed alphabet of q>=2 distinct values, the size-m strided ordered subproblems partition the input. There are N/m independent words drawn from q^m types. Thus

    E U_m = q^m [1 - (1 - q^(-m))^(N/m)],
    B(x) = (1/2) sum_{m=2,4,...,N} m U_m(x),
    E B = (N/2)(log2 N - log2 log_q N) + O_q(N).

This is a genuine additive Theta(N log log N) saving against the explicitly stipulated full radix-two butterfly count NL/2. Remaining expected butterfly work is Theta(N log N), and the saved fraction tends to zero. The result does not bound every algorithm on binary inputs.

For the largest dyadic t with t q^t<=N (N>=q), set H=(N/2)(L-log2 t). The low-level cost is at most 4N/7; the upper-level duplicate deficit is at most 2N/7; hence H-2N/7 <= E B <= H+4N/7. Dyadic rounding contributes O(N); no fixed linear correction or o(N) remainder follows.

Further accepted content, all present in the full review:

- Dense child-pair IDs and two counting-sort passes per level give deterministic O(N) planning on the stated logarithmic-word RAM. Naively rescanning all whole words costs Theta(N log N) symbol visits. Hash matches need exact collision resolution.
- Expected structural-node count is Theta(N/log N). Retaining every spectrum requires U_1+2B cells, expected Theta(N log N); evaluating two adjacent levels instead keeps at most 2N live spectrum cells plus separately charged O(N) roots, input, IDs and buffers.
- The cold universal leaf table at t has setup O(N) and all-input leading butterfly count equal to the iid-DAG expression up to O(N). Its gap from E B is between 0 and 6N/7 for the t q^t<=N constant-factor payload convention.
- With the distinct strict numerical payload cap T_b=q+sum_{m<=b}m q^m<=N, b may be t/2; the proven conservative gap is 9N/7. Roots and work buffers lie outside that strict table cap. These constants are not interchangeable.
- For every input, the DAG count is no greater than the cold table count. On an all-equal input B=N-1, so an O(N) expectation gap does not extend to arbitrary structured inputs. A hardware-fixed table size saves only O(N) butterflies.
- The same leading expression holds for fixed nondegenerate nonuniform iid distributions, with distribution-dependent constants using rho=sum p_i^2<1. It is not uniform as rho approaches one with N. The degenerate one-symbol case gives B=N-1.
- Sharing a scalar cache between two independent inputs gains only O(N) beyond two separately shared transforms. Joint ordered-pair keys have alphabet q^2 and require two scalar transforms. Genuine two-real-input packing uses one complex transform plus O(N) conjugate unpacking and is classical; the four-symbol occupancy for two binary inputs must not be replaced by a binary one.
- The exact pre-execution butterfly ledger is available in O(N) planning, but does not yield a verified wall-time or heap oracle.

The value is a rigorous, useful specialization and cost-accounting consolidation of FFT recursion, finite occupancy, tree compaction and tabulation. The full review explicitly grants SCOPED_PASS and declines historical novelty, a new research identity, sub-N-log-N complexity, bit complexity and practical speed. This finalization preserves that verdict rather than upgrading it.

Historical numeric/control records were recovered and hash-checked, but neither their programs nor any earlier benchmarks were rerun. The proof-scope judgment comes from the full mathematical text, not new finite tests.

## 3. Engineering obligations are still genuinely unfinished

The hardening report explicitly leaves global forward/backward numerical stability unproved. Cancellation controls diagnose one phase-generation defect only. A numeric-payload counter is not heap/RSS/allocator accounting; optional unbounded history remains unbounded; promotion, union formation, output copies, projection registration, calibration and losing-plan preparation all cost work.

Preserve the corrected query bounds O(q[1+min(H,r+k)]) with available history, and O(q[1+r+k]) after history loss. The missing +1 matters even for zero lag, since q outputs cost Omega(q). Existing single-view files retain separately identified defects. Fingerprints are probabilistic guards, not collision-free proofs. Native dtype/stride, lifetime and stale-plan tests are historical evidence, not present production certification. Leak detection was explicitly unverified.

Fair cold/warm comparison needs the actual workload, implementation revision, full input/output contract, allocation/traffic and tuned real-FFT or pruned-output baselines. No historical timing ratio establishes universal speed. These are useful engineering tasks, but they are neither completed by source recovery nor proof of additional mathematical novelty.

## 4. Why whole-owner archival is premature

The owner-bound [query-engine README](https://github.com/AgentSlop-Si/research/blob/e5d46232f0d819af518bff7dcbedbcbf2e3d0286/math/archive/objects/4b/4bdb965b811b5f29167fb816ea2a6269c5e541a18eff5eb5bd37bb7f6e4c2365__README.md) explicitly names its newest adaptive-organizer layer. The exact [organizer research text](https://github.com/AgentSlop-Si/research/blob/e5d46232f0d819af518bff7dcbedbcbf2e3d0286/math/archive/objects/96/965a2b512b3a8abf3f3d200cd4ac3325637c7e386d72c15ca93df6c8593ec9f5__ADAPTIVE_VIEW_ORGANIZER_RESEARCH.md), SHA-256 `965a2b512b3a8abf3f3d200cd4ac3325637c7e386d72c15ca93df6c8593ec9f5` (8,981 bytes), says in section 10 that the current greedy grouping is memory-unconstrained and proposes a budgeted spectral-materialization problem:

- Candidate groups have union-bin storage and optional contiguous basis-projection storage.
- Their maintenance/query benefit depends on the workload.
- Possibly overlapping groups must be selected under a memory budget.
- Hysteresis and migration costs must be included to avoid thrashing.

The source's current greedy heuristic is explicitly not globally optimal. The accepted occupancy theorem analyzes a different object: repeated ordered input words inside one fixed FFT recursion. Its cold-table memory bound says nothing about choosing overlapping consumer groups or reacting to a changing workload. Likewise, an exact replay-versus-rebuild cost comparison for one existing view does not solve online group selection.

The broader RESEARCH section 6 also identifies direct output-subset/dynamic updates inside the hypothetical #130 base circuit as an open theoretical/engineering project. Its existing black-box corollaries do not establish that extension; this report neither selects it nor certifies the hypothetical backend.

The budgeted-materialization direction is sufficiently explicit to defeat an inference that the source contains only benchmarking. It is insufficiently formal to assert a new theorem or promise of significant research value. A bounded finalization gate would specify: finite candidate family and encoding, workload/adversary model, accounting for group refresh and explicit output, shared-versus-duplicated storage, cold construction and migration costs, and a desired exact/approximation/competitive guarantee. Then compare that exact problem with a primary materialized-view theorem, prove the stated result, or explicitly de-scope it. Do not launch an unlimited optimization project from this review.

The primary records for [Aouiche–Jouve–Darmont](https://arxiv.org/abs/cs/0703114) and [Mistry–Roy–Ramamritham–Sudarshan](https://arxiv.org/abs/cs/0003006) confirm that workload clustering, merged views, storage-aware selection and shared maintenance are established antecedents. Only their abstracts were freshly checked here; that is not a theorem-level implication for the proposed Fourier workload, nor proof that a competitive migration contract is already covered. The [FFTW pruning documentation](https://fftw.org/pruned.html) separately supports the classical O(N log q) arbitrary-output mechanism and warns that operation reductions do not establish wall-time gains.

## 5. Exact owner proposal and stopping boundary

`OWNER_ORIENTATION_PROPOSAL.json` contains the proposed new prefixes and exact target addresses. Complete native preimages and preserved-history payloads remain private; the published artifact is a **proposal only**. It changes nine orientation cells, if independently accepted: Catalogue AE172/AF172; novelty O210/Y210/Z210; overview C298/F298/P298/Q298. It changes no status, lane, score, proof/novelty cell, accepted-scope cell, source link, note, formatting, validation or formula. Every new text carries its complete previous value verbatim.

The proposal preserves engineering as the currently recorded action while adding a whole-owner archival warning tied to the exact source. It does not silently choose the old possible extension as new work. Fresh preimages must be checked before any application.

No other stable ID, including ALG-070 or the separately reviewed ALG-025/026 comparisons, is closed or reopened. No supplementary research identity or discovery count is created. The missing original receipt is a bounded provenance gap, not evidence against the accepted theorem and not the reason for retaining the owner open.

**Stop reached:** complete source recovery, full mathematical and linked-owner-text review, precise completion/archival boundary, and reviewable orientation proposal. A production implementation, new optimizer theorem or complete primary-theorem comparison requires a separately fixed scope.
