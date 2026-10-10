"""Review-owned artifact writer. This creates reports only; supplied source is inert data."""
from pathlib import Path
import json
O=Path(__file__).resolve().parent
sources=json.loads((O/'SOURCE_INDEX.json').read_text())
reports={
1:'''## Verdict and evidence impact
Full static read complete. The finite audit driver is coherent for its fixed configurations. It does not prove all-input complexity, complex numerical stability, or a universal random-instance rank lower bound. No stored-result contradiction was found for this source.

## Complete control-flow audit
- Lines 1–7: standard-library setup plus star import of phase24_ordering and explicit RealGreenFourier import. The exact sibling modules are recorded in DEPENDENCIES.json; a successful imported name alone would not bind a source hash.
- Lines 8–20: enumerates all binary words for N=2,…,16, computes the permutation-cycle rank, compares it to the transition formula, and checks each observed rank count by integer cross multiplication against its rational probability. Summing all observed counts rules out extra positive probability mass if the formula is normalized; the separately assigned unit test also checks every even rank bucket. This is 131,068 finite words, not an all-N proof.
- Lines 21–34: seeded fair-bit samples at (N,samples)=(64,24),(256,12),(1024,4),(4096,2); computes every nonzero stride for each sample, including noncoprime strides. This records minima; it does not assert the probabilistic bound succeeds, and all four saved lower-probability bounds are explicitly 0.0. The saved positive minima therefore give empirical observations only.
- Lines 35–42: the transposition of positions 5 and 37 changes four successor edges and compares one finite-field Woodbury output with the adaptive Phase23 reference. z=13 is not assumed a singular-root test; the dependency rejects singular roots. Both paths share engine/root conventions, so this is a differential control, not wholly independent mathematical proof.
- Lines 43–58: assembles limitations, writes audit.json relative to the working directory, and prints pass text only after assertions have succeeded in normal Python. Main guard prevents the audit loop on import, though importing sibling modules would still execute their module setup.

## Guards and failure behavior
All dimensions and samples are fixed positive values; no user-input API is exposed. Missing imports, division/inversion failures, or filesystem errors propagate. Assertions are removable under Python -O, so a future optimized invocation is not an enforcing audit. The archived run instructions use ordinary Python; this is a conditional invocation hazard, not evidence that stored results bypassed checks. The helper's permutation validation calls sorted, adding a general O(N log N) comparison upper bound despite its O(N) traversal docstring.

## Cost and coverage limits
Rank traversal is O(N), but the exact dependency sorts permutations when validating both the order and successor. A conservative source-level upper bound is O(sum N log N·2^N) for exhaustive rank enumeration and O(sum samples·N² log N) for all strides, with O(N) working vector storage. The finite-field Woodbury branch costs O(Ns²+s³) plus preparation, here s=4. Inversions and integer arithmetic are not unit-cost bit operations. These are audit costs, not a fast transform algorithm. Small singular-root inputs, malformed permutations, empty inputs, and floating-point conditioning are not tested here.

## Stored evidence reconciliation
Preserved audit.json has 15 distributions totaling 131,068 words; all histogram totals match declared sequence counts. Saved minima are 25,113,487,2018 and saved changed-edge count is 4. These metadata checks were done without running the source. VALIDATION.md distinguishes 31 freshly reported tests from 265 historical tests. No new execution attestation is issued.
''',
2:'''## Verdict and evidence impact
Full static read complete. Seven unittest methods provide coherent finite rank and finite-field differential controls. Coverage limitations do not invalidate the saved seven-test claim, but they prevent treating it as exhaustive API, numerical-stability, or asymptotic validation.

## Complete control-flow audit
- Lines 1–12: inserts the package parent at sys.path[0], then imports exact sibling names. This is suitable for the archived directory layout but is not an installation/version lock.
- Lines 13–21: exhaustive binary rank-vs-transition formula comparison at N=2,…,16.
- Lines 23–31: initializes every even rank bucket, enumerates transition-formula values, and compares complete bucket counts to the rational probability formula by exact integer multiplication. This directly closes the missing-zero-bucket concern of audit.py.
- Lines 33–41: verifies mean N/2−1 and variance N/4 for N=3,…,16. The half/quarter-valued quantities and bounded sums are exactly representable in binary64 here, so the float equality is not an actual finite-range rounding defect.
- Lines 43–51: four seeded samples at each of N=32,64,128,256 check all strides against N/8. These are fixed-seed regression outcomes, not a proof that every binary word has this rank; constant words give obvious exceptions to any such universal claim.
- Lines 53–67: 4 sizes × 2 swap counts × 3 seeded permutations × up to 3 z values, skipping singular z^N=1. Repeated swaps can undo each other; this does not invalidate differential checks but does not guarantee a distinct two-defect case each time.
- Lines 69–74: identity-order Woodbury controls at N=8,16,32.
- Lines 76–85: inputs consist of zeros followed by ones, so every stable order is already the identity. These are 30 identity-order comparisons (3 sizes × 5 split points × 2 nodes); they add no nonidentity stable-sort coverage. Arbitrary nonidentity orders are instead exercised by the swap test.
- Line 87: normal unittest entry point; no stored result is manufactured by importing this module.

## Guards and failure behavior
unittest assertion methods survive Python optimization, unlike plain assert in audit.py. Fixed positive valid dimensions satisfy the known engine guards. Root singularity is skipped using hardcoded 998244353; that matches the exact sibling dependency, but would silently become the wrong guard if the field constant changed without the test changing. No current field mismatch exists. Invalid binary values, malformed permutations, engine mismatch, and deliberate rejection paths are not tested.

## Complexity and dependencies
The exhaustive rank test has conservative O(sum N log N·2^N) comparison/work upper bound because dependency validation sorts; the other exhaustive loops have O(sum N·2^N) work. The mean/variance method retains 2^N values, unlike a streaming aggregate. All-stride tests cost at most O(samples·N² log N). One/two swaps imply bounded changed-edge count, so their small Woodbury controls are O(N) for fixed s apart from modular inversion costs. Both actual and reference share Phase23 engine conventions and may share the Green branch on identity inputs; independence is limited.

## Stored evidence reconciliation
The source contains seven named test methods, consistent with VALIDATION.md and the lineage wrapper's Phase24 count. This review did not run them. A frozen checksum match identifies the source version but does not establish execution.
''',
3:'''## Verdict and evidence impact
Full static read complete. The default path checks two archive manifests, runs Phase24 tests and audit, and runs Phase23 tests. It does not default to rerunning every historical suite. Its printed 31/265 counts are hardcoded bookkeeping rather than runtime test-count assertions. The preserved VALIDATION.md states this distinction correctly; no current false full-lineage acceptance was found.

## Complete control-flow audit
- Lines 1–16: resolves the provided archive, creates a temporary directory, checks CRC via testzip, extracts, opens the expected fixed top-level directory, and compares each listed file SHA-256. The archive supplies its own manifest, so these are internal consistency checks, not authenticity against an independently trusted manifest.
- Lines 17–22: sets PYTHONPATH and OPENBLAS_NUM_THREADS, runs unittest discovery in Phase24 with capture and a 180-second timeout, raises on nonzero exit, and prints the last stderr lines. A zero-test discovery is not explicitly rejected.
- Lines 23–29: loads saved audit JSON, runs audit.py, then compares parsed objects. Object comparison intentionally ignores JSON whitespace and object-key order; numeric and list content must agree. It is not a byte-for-byte output check.
- Lines 30–44: extracts the embedded Phase23 checkpoint into a separate older directory, checks its manifest, runs its tests, and prints 7+24=31 plus the separately labeled historical 234. A recursive hash chain is not an execution record.
- Lines 45–51: only full=True invokes the predecessor lineage runner with a 600-second timeout. Success is its process return code, followed by a hardcoded combined count; test names/counts are not parsed.
- Lines 53–55: accepts two or three command-line arguments. A third argument other than --full silently selects the fast path rather than rejecting the typo. This could mislead a future operator but no archived invocation with that mistake was found.

## Safety, guards, and invocation scope
This is an executable test runner, not a safe inspector of arbitrary untrusted archives. If invoked it intentionally executes extracted Python and recursively supplied runners. It was never invoked here. Standard zipfile extraction behavior must not be mislabeled automatically as a zip-slip flaw; the concrete concern is unvalidated manifest paths and lack of explicit resource/entry-count limits for untrusted input. Manifest-relative paths can be absolute or contain parent traversal in a hostile archive. Current archived entries are ordinary relative paths and match exact files, so this is a hypothetical generalization hazard, not a stored evidence defect. Plain assert guards disappear under -O. Subprocess failures/timeouts propagate; temporary-directory cleanup is automatic.

## Complexity
CRC checking, extraction, and hashing cost O(total decompressed bytes), plus disk space proportional to extracted contents. Default tests/audit include exponential finite enumeration and all-stride scans; the full path additionally pays nested runners. capture_output retains child output in memory. Timeout values are operational cutoffs, not asymptotic guarantees or proof of suite completion.

## Stored evidence reconciliation
Reviewer-owned archive metadata checks found all 13 Phase24 manifest entries match exact members and the predecessor ZIP matches e226c6b5…. The predecessor's test source method count is recorded in EVIDENCE_RECONCILIATION.json. Seven Phase24 test methods and 24 predecessor methods agree with the default count, without running either. VALIDATION.md says precisely 31 tests were freshly reported and 234 older tests retained as history. This source review certifies that scope distinction, not the historical execution itself.
''',
4:'''## Verdict and evidence impact
Full static read complete. The exact finite-field rank checker and deterministic rational controls are internally coherent for the hardcoded dyadic sizes and three prime fields. The source explicitly treats these as regression controls; it does not derive a universal complex-field theorem from finite-field examples. No stored-count inconsistency was found.

## Complete control-flow audit
- Lines 1–13: standard-library-only imports, explicit separation between finite controls and the analytical endpoint proof.
- Lines 15–31: incremental row echelon basis. Each installed pivot is normalized to one; eliminating earlier pivots yields a correct exact rank over a field for rectangular rows. Empty row/column selections correctly yield zero.
- Lines 34–46: scans candidates for an n-th root, accepting w^n=1 and w^(n/2)≠1. This proves exact order for n a power of two, which covers every call here. It is not a general composite-n primitive-root test. For fixed prime and dyadic n≥2, the condition is candidate^((p−1)/2)≠1, so the first successful candidate is shared across sizes; independently built q-root matrices are compatible powers of the n-root matrix in coset checks. n=1 produces the single trivial root. All three listed primes support n≤128.
- Lines 49–87: submatrix extraction, bit-reversal generation, exact cut-rank recurrence, ceiling lower bounds, and exact integer sum formula. The recurrence reflects k>N/2 before reducing (N,k) to (N/4,floor(k/2)); N=2 supplies the nonzero base. All-N/dyadic proof is not supplied by evaluating the function.
- Lines 89–150: 435 direct bit-reversal cuts, 288 seeded random critical minors, 336 whole-coset decompositions, 336 consecutive-coset controls, and every 3-by-5 critical N=8 minor in each field (9,408 total). The larger minors are sampled, not exhaustive. The finite-field comparison to a complex-derived number is an observed control, not a proof of a field-uniform lower bound.
- Lines 152–179: recurrence/profile/sum/maximum checks at N=2,…,32768 and exact Fraction second-moment algebra at every odd cut. These large-N profiles are recurrence evaluations, not dense matrix ranks at N=32768.
- Lines 181–190: independently ordered N=16 rank-8 counterexample to replacing arbitrary Fourier submatrix ranks by min(rows,columns); explicit field/proof limits in return data.
- Lines 193–200: guarded main writes sibling CHECK_RESULTS.json and prints summary.

## Guards and complexity
Helpers assume a positive dyadic size, prime modulus, consistent rectangular rows, and valid indices. Violating those assumptions can return a wrong root/rank or raise; all actual call sites meet the assumptions. pow(value,-1,prime) correctly fails on nonunits. Plain assert enforcement vanishes under -O; no evidence of an optimized historical invocation exists. Dense Fourier matrices use O(N²) storage; echelon rank on a-by-b input costs O(a·b·min(a,b)) arithmetic in the worst case. Repeating over O(N) cuts can cost O(N⁴), while each generated recurrence profile costs O(N log N) integer work and O(N) storage. Root search also pays modular exponentiation. These are research controls, not an improved FFT runtime.

## Stored evidence reconciliation
All six saved count fields equal independent arithmetic counts from the source loop bounds. The result contains 15 recurrence-profile sizes; the saved max rank and total rank are not relabeled direct ranks outside the explicitly tested sizes. ENDPOINT_AUDIT.md preserves the characteristic-zero positivity assumptions and the no-factorization/no-runtime inference boundary. Stored logs/results are preserved, not freshly rerun.
''',
5:'''## Verdict and evidence impact
Full static read complete. The exhaustive N=8 permutation enumeration and cached necessary-screen comparison are coherent at GF(12289). Its survivor counts count necessary-screen passes, not actual matrix factorizations. No stored-result contradiction was found.

## Complete control-flow audit
- Lines 1–12: imports standard library plus the exact assigned independent_checks.py (fe537349…). This is a dependency of this checker; its historical phrase “source_programs_executed_or_imported=False” refers to the original research programs, not literally zero module imports. In this review neither checker was imported.
- Lines 14–25: precomputes all 256 subsets and noncyclic transition counts; caches rank(F[complement(missing_rows), columns]). XOR is correct because all masks are restricted to 0,…,255.
- Lines 27–34: interval masks include endpoints and the whole interval; all-subset screen considers equal-sized proper nonempty row/column masks and charges both transition boundaries.
- Lines 35–48: finite-window and first-trace uncertainty necessary inequalities, with exact integer arithmetic and explicit left/right endpoint costs.
- Lines 49–72: enumerates every extra subset of the complement of the chosen columns. Starting at outside includes the full support and the final zero subset includes the original support. The zero check precedes the usual descending submask update, so it terminates. For each excluded maximal run, ccost counts only sides where the original chosen-column interval exists. Required dimension is size−|support|+rank(F[outside rows,support]). Early exit upon one violation preserves the universal-support predicate.
- Lines 74–88: enumerates all 8!=40,320 orders, builds all mapped masks recursively from the least significant bit, and checks every proper subset or interval as appropriate. Since each permutation preserves cardinality, the precomputed table keys exist. Tallies marginal and joint outcomes.
- Lines 89–99: asserts window=15,728, subset=31,384, support=15,728; checks no window survivor fails the other candidates and that uncertainty is strictly weaker. Combined equal counts and inclusion establish equal window/support survivor sets at this finite size. It does not assert the exact uncertainty count 40,320, but the saved output records it.
- Lines 102–105: writes sibling SCREEN_CHECK_RESULTS.json and prints the full result under a main guard.

## Guards and cost
N and prime are fixed valid values and no generalized argument API is offered. Changing N alone would leave the constants 255/256 and asserted counts inconsistent; this is a deliberately fixed N=8 auditor, not an existing bug in that run. Assertions are removable under -O. Cache/table memory is exponential; distinct rank requests are at most O(4^N) and each dense rank is at most O(N³) arithmetic. Support supersets contribute a conservative O(N²·3^N·N) mask/boundary overhead before rank caching; enumerating permutations and all mapped subsets costs O(N!·(2^N+N²)) apart from table construction. The stored 17,978 distinct submatrix ranks show reuse, not polynomial asymptotics.

## Stored evidence reconciliation
SCREEN_CHECK_RESULTS.json equals SCREEN_RUN.log as parsed JSON. Every joint table totals 40,320. Window/support: 15,728; subset: 31,384; uncertainty: 40,320. The joint cells establish the declared inclusion and equality relations. These are inert result consistency checks, not a repeated search or a claim of factorization existence.
''',
6:'''## Verdict and evidence impact
Full static read complete. Thirteen fixed-seed v11 regression methods are retained inside the centered-v12 package. Their saved 13-pass log is consistent with the source method list. They test inherited v11 functions, not all centered-v12 functionality. In particular the precision stress is mixed-precision decoder-storage stress, and the allocation/work tests inspect formulas rather than measured runtime or peak memory.

## Complete control-flow audit
- Lines 1–16: imports NumPy, SciPy jv, prototype, and unit_step_core; setUp resets the same RNG seed for each unittest method, providing deterministic per-test streams.
- Lines 18–26: all n=2,…,299 exact nearest-grid maps; uniqueness and integer residual constraint checked. The floating reference k*q/n+0.5 is accurate enough at these small bounded integers. This does not cover large fixed-width index overflow or near-large-integer tie behavior.
- Lines 28–37: selected decoder vs full decoder on arbitrary summary vectors at three q/block pairs; useful interface test, but shared primitives/root conventions limit independence.
- Lines 39–47: streamed Clenshaw vs retained reference at five n values, rank=10.
- Lines 49–63: 900 seeded pointwise Bessel-addition controls for nonnegative z and delta; expected tail is from the same prototype, so this is finite numerical support.
- Lines 65–78: 8 fusion-center comparisons (four n values, H=0,1), comparing implementation error to deterministic bound times norm.
- Lines 80–91: six scalar parameter evaluations at n=2^exp−1 show a declining halfwidth-zero ratio for sampled exponents; this is not an asymptotic proof or allocation of those enormous arrays.
- Lines 93–109: 250 randomized rows at one n/state-family measure empirical squared deviations around the deterministic fused center. Correlations across outputs are allowed; maximum empirical variance below a conservative formula is not unbiasedness, a confidence interval, or a universal variance certificate.
- Lines 111–122: one fixed-seed n=61 end-to-end randomized sample with nine rows; its success does not establish the stated global failure probability.
- Lines 124–135: complex64 vs complex128 call-path stress at n=257 and ranks 4,8,12. Inspection of exact prototype.py shows complex128 input, phase/Bessel compression and Clenshaw stages; SelectedDecoderPlan casts summaries/storage while its FFT explicitly promotes to complex128. Thus this test does not exercise a uniformly binary32 end-to-end implementation or certify every primitive assumed by the analytic precision model. It also calls streamed_bessel_chirp_row, not the fused path requiring the separate decoder-on-summaries theorem.
- Lines 137–146: four scalar sufficient-mantissa formula evaluations; observed ratio behavior is a formula regression, not proof of Theta(log N) or a verified arbitrary-precision implementation.
- Lines 148–165: allocation_model returns accounting formulas, including literal zero rank-dependent full-length storage. The work-ratio test independently forms q+R(q/block) divided by Rq. Neither instruments real allocations or operations, nor includes all Bessel/phase preparation, FFT, scan, aggregation, and bit costs.
- Lines 167–175: exact zero-signal invariant for one valid configuration.
- Lines 178–179: unittest entry point.

## Guards, dependencies, and cost
All configured sizes/blocks are valid and fixed. Invalid dimensions, empty/nonfinite signals, degenerate state rejection, overflow/underflow, difficult boundary classifications, and malformed summary shapes are not directly tested here. The dependency snapshots identify prototype=25590a19… and unit_step_core=6a95e865…; they are not full reviewed by this package and no installed NumPy/SciPy versions were validated. Largest actual vector length is small (q≤512 for transform tests), while n≈2^120 occurs only in scalar model calculations. Per row the retained path pays rank-many short FFTs plus full scans/Clenshaw; sampled model savings in input fusion alone do not remove those terms.

## Stored evidence reconciliation
The exact saved log lists all 13 methods and reports “Ran 13 tests … OK”; the enclosing run_all.py sets cwd to the sibling directory. This review neither repeated that run nor certifies the logged runtime. Prior V11_FP_CONTRACT_REVIEW.md explicitly supplies a conditional summary-interface repair and declines to certify NumPy/SciPy/BLAS. The narrowed interpretation above is consistent with that existing caveat, not a newly demonstrated numerical failure.
''',
7:'''## Verdict and material finding
Full static read complete. **F01: concrete source/report/result version mismatch.** Exact source dd56291f… cannot emit the exact saved CHECK_RESULTS.json ddd6a933… on any successful ordinary execution: line 110 unconditionally inserts source_centered_envelope, absent from the saved object; line 111 assigns centered_envelope=2 exp(pi/4)−1≈3.3865601014760305, while the saved result and log report 4.248775573118824. At H=0, lines 160–165 similarly use tighter factorial majorants with mass tending to 3.3865601; the saved mass is 4.24877557. The difference is far larger than truncation/rounding. This is a version-binding defect; it is not evidence of fabricated output, a failure of either safe envelope, or a demonstrated error in the saved FFT implementation.

## Complete control-flow audit
- Lines 1–11: imports mpmath and sets global 110-decimal precision; explicitly disclaims interval certification. Loads an inert summary relative to __file__.
- Lines 13–36: exact-integer nearest-grid construction; factorial Bessel-tail majorant with infinity when the geometric bound denominator is unsafe; old/new rank search through r=299; finite parameter optimization over R=1,…,49 and H=0,…,11. Tie selection is the first strict-minimum proxy, not proof of a globally optimal algorithm. K=q//M assumes positive valid divisibility; saved configurations satisfy it. rank may exhaust and choose may return None outside the fixed inputs, but neither is a current failing call.
- Lines 38–62: binary-significand nearest rounding of real and imaginary components; explicit four rounded real products/two additions; Taylor term generation and rounded accumulation. Exponent range is unbounded, with no IEEE underflow/overflow model. Global high precision is a reference mechanism, not directed rounding.
- Lines 64–85: exact residuals, bounded-angle anchors and two transition roots, reanchoring every B terms with p+guard-bit arithmetic. Ratios follow r[k+1]−r[k]=q−d*n for d in {1,2}; this is the correct carrier sign. Pi is taken from mpmath and the code expressly isolates certified pi construction, so it does not implement the report's complete outward-rounded pi contract. The diagnostic max error uses mpmath exp, not interval containment.
- Lines 87–91: factorial Bessel series uses successive terms −z²/[4j(m+j)] and the leading (z/2)^m/m!; handles negative/zero/tiny real z by integer parity and zero powers correctly.
- Lines 93–111: compares 24 saved rank choices and 28 proxy choices against high-precision formulas, then emits both the looser source envelope and sharper centered envelope. The copied SOURCE_RESULT_SUMMARY.json exactly matches the retained extracted original. This comparison is a finite reproducibility check, not an implementation benchmark.
- Lines 112–123: exact small grids and 32,896 carrier transition relations; code records the largest high-precision discrepancy but does not assert a numerical tolerance on max_phase. The underlying identity is algebraic, as above; the stored tiny discrepancy remains numerical support, not a hard test gate.
- Lines 124–137: twelve allowed-error product-model controls showing accumulation proportional to k rather than tree depth. They model coherent local/leaf perturbations, not an actual recorded IEEE execution or a proof SciPy makes these errors.
- Lines 138–142: twelve explicitly rounded reanchored controls at p=24,53,80 and four n values. Each asserts error below the target against the high-precision reference. No certificate covers all p,N or primitive implementations.
- Lines 143–155: 287 Bessel controls at orders 0,…,40 and seven signed/zero/tiny arguments; truncated-series tail comparisons are numerical checks around an analytic sufficient bound.
- Lines 156–168: four symmetric factorial-envelope convolutions. Truncation at r=99 omits a tiny positive tail; it is correctly checked as near equality, not literally finite exact equality. The computed convolution mass differs materially from the saved old-envelope data (F01).
- Lines 169–181: three forward-order recurrence seed-amplification examples. They concern a proposed recurrence substitute; the retained v12 code evaluates Bessel functions separately, so this is not an observed v12 runtime failure.
- Lines 182–186: writes CHECK_RESULTS.json and prints summary only after preceding assertions in an unoptimized run. Current output necessarily has the new envelope field/value.

## Envelope correctness and precise impact
Both the tighter and looser majorants are mathematically safe in the stated **real-argument** domain. Poisson's integral for integer m≥0 gives |J_m(z)|≤(|z|/2)^m/m!, because |cos(zt)|≤1 and the beta integral normalizes to 1/m!. Integer-order parity covers negative z and negative orders. With |z|≤pi/2, the symmetric majorant mass is 1+2 sum(m≥1)(pi/4)^m/m!=2 exp(pi/4)−1. The report's extra exp(pi²/32) factor and corresponding positive local factors are ≥1, so they remain looser safe bounds. This implication is derived here from [NIST DLMF 10.9.4](https://dlmf.nist.gov/10.9.E4); it must not be extended to arbitrary complex z. Thus F01 withdraws exact-run attribution of the saved envelope/convolution receipt to dd56291f…, not the validity of either envelope or all unrelated analytical results.

## Search for the generating version
PRECISION_VARIANT_SEARCH.json records the bounded search: frozen code-byte corpus marker search plus all standalone independent_precision_checks.py and named centered-independent-supplement ZIP occurrences under shared storage. All 25 located occurrences use dd56291f…. No exact older checker was recovered. Saved results match the looser formula in the preserved report at the formula level; that is not enough to invent an older source hash or execution history. The archive's manifests successfully seal the current source, old-envelope report, and old-envelope result together; checksums do not establish that one generated the other.

## Cost, guards, and next step
The checker uses bounded finite searches and many high-precision reference transcendental calls. Reanchored carrier construction has O(N+B+L_gamma) scalar-work form for its simulator, but all reference exp calls, precision-dependent costs, source-grid search, factorial/Bessel checks, and output storage are additional audit work. N-sized lists consume O(N) reference-number storage. There is no uniform runtime proof over arbitrary precision. Assertions disappear under -O; installed mpmath is unpinned and the global reference precision is fixed. Safe next step is to retain all sealed originals, mark the mismatched receipt as historical/unbound to this source, and produce a separately authorized new receipt or recover a genuine older source. No such source execution or original rewrite was performed here.
'''
}
findings={1:['F03'],2:['F03','F04'],3:['F02'],4:['F05'],5:['F05'],6:['F06'],7:['F01','F07']}
for i,body in reports.items():
 s=sources[i-1];name=Path(s['row']['representative_path']).name
 header=f'# Full-source review {i:02d}: {name}\n\n- SHA-256: {s["row"]["sha256"]}\n- Exact bytes: {s["row"]["size_bytes"]}; complete lines read: 1–{s["lines"]}\n- Assigned batch: {s["batch"]}\n- Representative path: {s["row"]["representative_path"]}\n- Snapshot: ../{s["snapshot"]}\n- Method: complete first-to-last inert reading, dependency-context inspection, and stored-evidence reconciliation. No supplied execution/import/compilation/syntax parse.\n- Findings: {", ".join(findings[i])}\n- New exact-hash full-review credit: yes, subject to final concurrent deduplication check.\n\n'
 (O/'per_source'/f'{i:02d}_{name}.md').write_text(header+body)
summary='''# Centered/chirp-adjacent source review, 03:57 batch

## Result
Seven assigned exact hashes were fully read: 39,509 bytes and 870 source lines across 02_addition_1845_01.json, 02_addition_1848_01.json, and 02_addition_1906_centered_01.json. All seven are new full-static-read credits relative to the frozen inventory, additive registry, and completed coverage manifests checked. The separately named 1906_chirp batch was not assigned and is not included. No supplied program was executed, imported, compiled, or syntax-parsed. Frozen inputs and the central registry were not edited.

## Main finding
F01, material reproducibility issue: independent_precision_checks.py (dd56291f…) is paired with saved results from a different envelope/report state. The exact current source requires a key absent from the saved JSON and a tighter envelope ≈3.38656010, while saved JSON/log/mass report ≈4.24877557. Full hashes and data-only diagnostics are in EVIDENCE_RECONCILIATION.json. This is a source/report/result version mismatch with unresolved generating-source identity, not an allegation of fabricated output.

Both envelopes are safe for the report's real-argument domain. The tighter factorial bound follows from [Poisson's Bessel integral](https://dlmf.nist.gov/10.9.E4); the older positive inflation factors only loosen it. No correctness downgrade to that analytical envelope, the carrier theorem, or the saved FFT implementation follows from the receipt mismatch. Current-source reproduction must remain unverified until a separate authorized run or exact prior generating source is available. The bounded search found only the current exact source in 25 standalone/named-supplement archive occurrences.

## Other findings and scope
- F02: lineage runner counts are hardcoded, and an unknown third CLI argument silently selects the fast path. Its current archive has seven Phase24 plus 24 Phase23 test methods. VALIDATION.md already correctly distinguishes 31 freshly reported tests from 265 historical tests. These are robustness risks, not proof the stored run was false.
- F03: Phase24 rank/sort controls are finite; recorded probability lower bounds are 0 at every sampled size. Permutation-validation sorting adds a general N log N comparison upper bound to helpers described as linear traversal. Nothing here supplies a worst-case faster transform.
- F04: “stable single run” test cases are all identity orders; nonidentity Woodbury controls come from the separate swap test. Assertions/guards beyond valid fixed inputs are not comprehensively tested.
- F05: endpoint counts and N=8 screen joint tables are internally consistent. Finite-field regression and necessary-screen passes do not establish a characteristic-zero theorem, unrestricted circuit lower bound, or existence of factorizations.
- F06: retained 13-test v11 suite checks mixed-precision decoder storage and scalar accounting formulas, not uniform binary32 arithmetic, peak memory, wall-clock speed, or a certified end-to-end precision implementation. Existing interface caveats already acknowledge this boundary.
- F07: precision controls are high-precision corroboration and explicit rounding simulations, without outward interval pi/transcendental certification. Modeled coherent errors and proposed forward-recurrence failures are not recorded IEEE/SciPy failures.

## Package contents and verification
- per_source/: seven complete reports covering every source range, correctness, guards, cost, dependencies, and stored-result impact.
- source_snapshots/: byte-identical inert .txt copies of assigned code.
- dependency_snapshots/ and DEPENDENCIES.json: exact dependencies, targeted/full contextual read scope, no extra coverage credit.
- input_manifests/: byte-exact assigned batches, frozen inventory, additive-registry snapshot.
- evidence_snapshots/, EVIDENCE_INDEX.json, EVIDENCE_RECONCILIATION.json: preserved result/report/log inputs and reviewer-owned metadata reconciliation.
- DEDUP_SCAN.json, PRECISION_VARIANT_SEARCH.json, COVERAGE.json: exact scope, historical coverage search, and coverage credit.
- PRESERVATION_RECEIPT.json and SHA256SUMS.txt: before/after input preservation and complete output seal.

Only review-owned metadata/artifact writers ran. They read JSON, text, and ZIP members; they did not load supplied Python as code. No global research completion or dependency-closure claim is made.
'''
(O/'REVIEW.md').write_text(summary)
(O/'FINDINGS.json').write_text(json.dumps([
 {'id':'F01','severity':'material_reproducibility','source_indices':[7],'summary':'Current source and saved envelope/convolution results belong to different version states; generating source identity unresolved. Both old and new real-domain envelopes are safe.','actual_stored_evidence_impact':True},
 {'id':'F02','severity':'robustness_and_scope','source_indices':[3],'summary':'Hardcoded test totals, silent unknown-option fallback, removable assert integrity guards. Current preserved validation correctly distinguishes fresh vs historical scope.','actual_stored_evidence_impact':False},
 {'id':'F03','severity':'cost_and_evidence_limit','source_indices':[1,2],'summary':'Finite/random controls and comparison-sorting validation costs must not be represented as universal rank/linear-work or FFT speedup certification.','actual_stored_evidence_impact':False},
 {'id':'F04','severity':'test_coverage_gap','source_indices':[2],'summary':'Stable zero-then-one cases all induce identity order; rejection/singular-path coverage limited.','actual_stored_evidence_impact':False},
 {'id':'F05','severity':'evidence_boundary','source_indices':[4,5],'summary':'Exact finite field ranks/screens are consistent controls only; no inference of universal complex-field theorem or factorization existence.','actual_stored_evidence_impact':False},
 {'id':'F06','severity':'validation_scope','source_indices':[6],'summary':'Mixed-precision and formula regression tests do not certify end-to-end arithmetic, speed, allocation or probability bounds.','actual_stored_evidence_impact':False},
 {'id':'F07','severity':'numerical_model_scope','source_indices':[7],'summary':'High-precision reference simulations are not outward-rounded full-primitive certificates; modeled counterexamples are not observed library failures.','actual_stored_evidence_impact':False}
],indent=2)+'\n')
print('Wrote seven full-source reports, summary, and findings.')
