# Fourier research checkpoint 26

## Conclusion

The available-material static review is complete within the frozen scope described below. The frozen program-source universe is fully accounted for by 1,684 accepted first-to-last exact-hash source reads plus two complete generated-source semantic/template audits: 1,686 complete static inspections, with no available program hash still awaiting static inspection. This is a review of the frozen supplied collection, not proof that every mathematical assertion is true or that every historical experiment can be reproduced. No supplied research program was executed, imported, compiled or AST-parsed in this review cycle or in checkpoint packaging.

The collection contains useful exact identities, restricted constructions, finite certificates and scoped representation obstructions. It does not establish an exact arbitrary-input, full-output Fourier transform using o(N log N) fully charged work. Its most promising publication candidates remain carefully bounded mathematical statements; external priority is unresolved.

All original research files and earlier audit material are preserved. Exact-hash deduplication is used only to count review coverage. Different filenames, versions and archive occurrences are retained, even when their contents coincide.

## What the completed static coverage means

The frozen inventory contains 906 material identities, 1,686 distinct program-source hashes and one separately classified build-metadata hash. There are 184 inherited full-read hashes and 1,500 accepted additive full-read hashes. Checkpoint 25 held 785 full reads; this checkpoint adds 899 full reads and the two generated-source template audits. The independent closure audit finds no duplicate additive hashes, no baseline/additive overlap, no template/literal overlap and no out-of-universe credit. All cached source bytes and all checked package seal entries match their recorded identities.

The 477 selected text hashes also have sealed complete-read records and verified bytes. This closes those planned text queues, not every prose file mentioned anywhere in the archive graph. All 380 explicitly hash-bearing in-corpus dependency candidates have accepted static coverage; actual runtime resolution and environment versions remain unverified.

Each ordinary source review is bound to exact bytes, provenance, complete read intervals and line-referenced findings. The two generated SMT-LIB files are credited separately: independent template reconstruction accounts for every byte and line, with mathematical semantic checks. This is complete static template verification, not literal first-to-last reading of every repeated character. Their 16-gate positive-control witness checks exactly; the 15-gate historical result is unknown because of timeout. Timeout proves neither impossibility nor optimality, and the common final normalization has a separate cost.

The private inventory's included verification receipt remains the older 785-read update. The saved full predecessor is checkpoint 25 as a separate lossless archive, not a new version of the older ZIP master. This checkpoint's local verification and any subsequent save receipt must be distinguished.

## Accepted bounded separator theorem

The new independently audited result concerns a complex flat unitary U of order N and r >= 1 inverse branches. If

U = sum from i = 1 to r of L_i Q_i^(-1) R_i,

where every Q_i is invertible with at most two nonzero entries per column and each endpoint has support contained in a permutation matrix, then

N <= 12 r 36^r.

Endpoint permutations can differ between branches, and endpoint weights can vanish. There is no row-degree restriction. An additional arbitrary diagonal gives N <= 48 r 36^r. More generally, a half-balanced vertex-separator budget q gives N <= 4 q r 36^r, or N <= 16 q r 36^r with an arbitrary diagonal. A lift of treewidth w is sufficient with q = w + 1.

The proof uses the pseudoforest support of an invertible column-two matrix, a weighted separator in its symmetric bipartite lift, complementary inverse-submatrix ranks and repeated selection of a common rectangle under independent routings. These necessary conditions imply logarithmic branch growth for exact representations in the stated class. The separately proved approximation bounds exclude vanishing error for fixed branch count. They do not establish logarithmic growth at every fixed positive error tolerance, a general runtime lower bound, or a faster FFT.

The historical separation-rank theorem already covers independently routed Hamiltonian and bare cycle-block inverses, including an operator-norm accuracy gap. Independent routing, arbitrarily many bare cycles and those older accuracy conclusions must not be advertised as new. The new argument establishes uniform coverage for attached-tree/high-degree column-two support and more general bounded-separator families. It has not proved that this class strictly exceeds the inherited abstract ordered-separation-rank class. Classical nullity, graph-rank and treewidth ingredients are explicitly credited; priority of their combined application remains unresolved.

Read packages/pseudoforest_separator_independent_audit_0452/SEALED_PROOF.md and PRIMARY_SOURCE_COMPARISON.md. The accompanying author proposal is retained as history. The earlier arbitrary-field N <= r(r+1)^r representation theorem remains preserved in checkpoint 25 and has a different field/scope tradeoff.

## Other mathematical results and publication candidates

The previously accepted Rogers–Szego results remain intact. The five overlap families with bases 3, 7, 11, 15 and 19 retain their prime and excluded-order conditions. The exact content valuation and the fixed-base 17, 21 and 25 corollaries retain their nonvanishing, divisibility and exceptional-order guards. The strongest surviving candidate contribution is the explicit shared-root local coefficient at a fixed nontrivial odd root of unity, its ordinary-discriminant coefficient and arithmetic applications. Classical Hermite/quasi-Laguerre, Wronskian and cyclotomic ingredients are not new. Legitimate full comparisons with Lubinsky–Saff and Zhedanov remain outstanding.

The final publication assessment ranks the Rogers–Szego local-discriminant and arithmetic package first for manuscript development, and the bounded-separator inverse result second as a separate short structural note. The latter needs a precise strictness check: exhibit column-two inverse families with unbounded minimum ordered-separation rank, or identify a theorem giving a uniform constant bound for the whole class. High degree or a poor natural ordering proves neither. The corresponding manuscript outline and publication gate are editorial preparation, not a submitted or publication-ready proof package. See packages/final_publication_assessment_0538/ASSESSMENT.md. General content primitivity, broad composite and higher-ramification coverage remain open. See the preserved checkpoint 25 synthesis for full statements and primary package paths.

Finite Fourier/Green, Boolean-degree, rank and contraction certificates have useful positive or negative conclusions within their exact size, coefficient domain and architecture. They do not decide all-size coefficient synthesis, unrestricted circuits or the full N64 family. Conditional binary-frame transfers still depend on their compiler, routing, recovery and analytic hypotheses. The selected-convolution route still pays ordinary N log N work in the accepted block construction; the faster fully charged evaluator is missing.

## Practical findings that matter before code reuse

The detailed source reports separate valid mathematics from implementation defects. The highest-priority issues are:

1. Native memory contracts: one wrapper passes pointers without enforcing complex128 dtype, dimension and contiguity; wrong layouts can cause out-of-bounds access. Raw/generated sparse-position paths also permit negative C++ indices. These were diagnosed statically, without unsafe execution.
2. Incorrect state reuse: a spectrum-only fallback can discard the supplied base spectrum; dependent-basis registration can desynchronize basis and spectrum dimensions; changed samples or changed same-length inputs can reuse stale calibration or surrogate-plan state.
3. Numerical claims: naive norm calculations can underflow finite nonzero inputs to zero; global scaling can erase representable small components; exact cache reassociation changes floating answers; cancellation/rebase limitations survive passing tests. Ideal-arithmetic identities do not supply universal binary64 accuracy.
4. Certificate guards: empty output or witness lists can yield vacuous success, cut-capacity and root-order checks are incomplete in some generic APIs, and a malformed fixed-inner certificate can pass without q < 1. These defects do not automatically invalidate the specific archived certificates independently checked.
5. Accounting: replay may scan old history, promotion or greedy replanning may add uncharged work, and selected-array/cache budgets do not bound peak memory. Fixed-word claims need explicit packed-width bounds. Setup, discovery, output materialization, precision and growing integer operands must be charged.
6. Test and output attribution: unittest.main before later classes can omit direct-script tests while discovery includes them. Hardcoded PASS prose, shared output filenames and co-sealed source/output files do not establish exact-source execution. Some archived runs differ because of dependency failures or earlier versions.

Later archived-checker reviews also distinguish stored-matrix verification from reconstruction of its parent operator, record a companion-document manifest mismatch, and identify expression parsing in a purported data-only certificate route. These narrow findings neither erase valid fixed certificates nor upgrade historical checker outputs into fresh execution.


The complete bug and qualification details remain in each accepted package's main report and per-source records. This checkpoint does not silently patch supplied research code or claim that its tests were rerun.

## Stored timing evidence

The separate cache benchmark audit inspected all 19 cases, 266 runs and 45,546 scalar leaves. Its recorded medians, ratios and timing sums are internally consistent: 5 median wins and 14 losses, with a maximum recorded speedup of about 1.281. Input generation is excluded. These are historical timings, not a current benchmark or a general speedup result.

The native energy-pruning review likewise distinguishes useful native-baseline improvements from all-zero approximate outputs and marginal NumPy comparisons. No robust arbitrary-input NumPy speedup or asymptotic improvement follows from that record. Exact algebra, numerical accuracy, measured speed and originality remain separate questions.

## Remaining limits and how to use this checkpoint

The independent closure audit verifies 899 original-byte material identities and five matching-version text snapshots among the 906 frozen identities; two frozen document versions remain unavailable. It also verifies 269 archive containers and 19,932 archive-member occurrences. This closes the available-material static-inspection queue. It does not close missing historical versions, every proof or ancillary assertion, runtime dependency resolution, benchmark replication, account-wide access or publication priority. The unresolved-reference table retains those limits.

The final cross-package reconciliation records 71 unresolved historical/file/external digests and separately 13 missing exact Tensor–Weil v24 entries. Those figures are not an additive count of missing research files.

Read REVIEW_COVERAGE.md for the exact accounting, PRACTICAL_FINDINGS.md for actionable code risks, UNRESOLVED_REFERENCES.md for version/dependency limitations and PUBLICATION_CANDIDATES.md for publication gates. The full lossless archive contains every retained file. The supplement contains this checkpoint's new reviews and receipts. The compact findings archive is the convenient reading copy and is not a substitute for the complete source archive.
