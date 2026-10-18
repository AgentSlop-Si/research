# Independent final structural review: bounded outer transfer

## Verdict

**PASS for the local Cartesian-median refinement, immutable-context semantic binding, lazy retained-incidence iterator, and three concrete coefficient forwarding/binding checks, with the mandatory hash-bound cost clarification in ERRATUM.md.** The unqualified unrestricted producer cost bound in the candidate's PROOF.md is not accepted. The numerical truth oracle and full scalar recurrence acceptance belong to the separate scalar review.

The candidate is pinned by MANIFEST.json SHA-256 `f14e4bbd92c98063902e262ce699bfa58c6ba4333562bbbe683deb97714dff8f`. All 13 listed files matched their size and SHA-256, and all eight inert-source pins matched. No candidate file was modified. No historical program was executed. No remote publication or native-table write was made by this review.

## Actual independent execution

After complete source inspection and the pre-execution review recorded here, a new test program imported only the fresh outer_wrapper.py, sparse_output.py and production_scalar.py. The separate capped subprocess exited 0 in 6.150524 seconds with empty stderr, unchanged reviewed source hashes, 120/125 s CPU limits, 180 s wall limit, 512 MiB address-space limit, 32 MiB per-file limit and 64-descriptor limit.

The independent run passed:

- 384 deterministic median cases with R in {1,3,5,7,9,15,17,31} and S in {0,1,2,3,7,16}; expected results use built-in column sorting rather than either source's merge sort;
- 42 direct row-first incidence/guard cases covering small valid headers and both dense-required and sparse branches;
- all 9,123 incidences in the requested D=5, m=57 four-support fixture, including ordinal order, no duplicates, exact per-support counts and equality with the saved incidence evidence;
- three freshly recomputed coefficient records, exact equality with the saved records and source-origin/field forwarding checks;
- 52 malformed-input, frozen-context, substituted-binding/header/incidence/coefficient and consumed-prefix controls;
- cumulative repeat-validation/preparation charges, a 16,385-bit consumed integer before a later boolean rejection, and empty-support operation with no scalar setup.

The full evidence is INDEPENDENT_RESULTS.json and PROCESS_EXIT.json. Tests are independent structural evidence; the three numerical records were reproduced from the production kernel, so reproduction alone is not claimed as an independent transcendental oracle.

## 1. Precise accepted-median refinement

The historical phase_medians.py with SHA-256 `45c0c6a59cac18912278dcda183fe8e5bea2a19398cb61fc1bf8ec97cac5a788` was inspected as inert text. It requires dyadic M>=4, P>=8, exact sorted distinct in-range tuple candidates, a positive odd tuple of exact EstimateResult rows on grid P, and exact signed integer Cartesian pairs. It selects the middle of independently sorted real and imaginary columns and retains zero entries without another rounding step.

The fresh implementation has those same numerical semantics under the explicit representation mapping:

`fresh row tuple -> historical EstimateResult(numerators=row, bits=P)`.

This is a refinement after eliminating the historical row wrapper, not drop-in runtime-class compatibility. The fresh API has no separate row.bits field to mismatch. Its sorted/distinct/range checks imply S<=M; the omitted explicit S>M check changes rejection order, not the valid domain. Bottom-up merge sorting is correct for partial final runs: each position chooses the unexhausted smaller head, then swaps source/destination arrays. Signed values, duplicates and zero estimates are preserved.

## 2. Genuine computation and binding, not object echo

produce_medians actually reads the supplied immutable rows, runs both median sorts, and constructs the numerical output. Its frozen origin retains the original M, P, candidate tuple and row tuple, not a caller-supplied descriptive label or digest. Exact tuples and exact built-in integers provide deep immutability within the stated trusted-program model.

Outer.__init__ calls verify_produced(..., replay=True) on the same cumulative ledger before accepting the binding. Replay reruns the median computation from the original context and compares every output field. Independently replacing both the output and the origin's output pointer, while leaving the original rows unchanged, was rejected by semantic replay. Replacing only the output was rejected by identity. The original input tuple identities and frozen origin were separately checked.

This establishes a genuine local computed-output association in trusted execution. It does not authenticate upstream signal, WINDOW, BUCKETS, phase estimates, random tapes, successful recovery or a historical PipelineRun. A coherently different immutable context describes a different local run. Hostile private-capability forgery, monkeypatching and arbitrary memory mutation remain outside the expressly stated model.

## 3. Header, geometry and exact lazy iterator

The Header is an exact frozen class with exact built-in integers. The expression 1 << bit_length(4N-1) is exactly 2^ceil(log2(4N)) for N>=1. The independent tests reject bool/float fields, bad range values, inconsistent M and estimate-grid mismatch. Output support is independently rechecked for strict order, uniqueness, range and exact immutable signed Cartesian fields.

For a support frequency k, row-first membership is k=floor(ell M/N)+j modulo M, with -h<=j<=h+1. Lifting ell by integer multiples of N gives integer r with:

`ceil(N(k-h-1)/M) <= r < ceil(N(k+h+1)/M)`.

The code's signed-floor formulas implement these endpoints exactly. For t<M, the real interval has length Nt/M<N, so distinct retained lifts cannot coincide modulo N. Thus no deduplication or dense row scan is needed. Endpoint prefixes are prepared once per support frequency; ordinal verification uses a direct tuple lookup and constant arithmetic, not a scan of previous support entries.

At N=2^55-1, M=2^57 and D=5, the independent run obtains h=4561, t=9124 and counts 2281, 2280, 2281, 2281 for support {0,1710,2^55+1,2^57-1}. All 9,123 records match an independently formulated centered-offset inverse construction, and the finite small cases also match a literal direct row-first oracle. Enumeration leaves the kernel unset. The dense guard returns OUTER_DENSE_REQUIRED without scalar setup; it is a dispatch condition and does not supply a dense transform.

The complete AST loop inventory is preserved in the results. Production outer iteration is over support, fixed-size fields or the retained endpoint intervals. Median iteration is over supplied sparse candidates/rows and bounded merge-sort runs. There is no hidden production range(N), range(M), dense vector, all-phase cache or E-record collection.

## 4. Selected coefficient source binding

The wrapper calls the fresh scalar kernel only after checking exact incidence fields, binding ownership, support position, lift/row arithmetic and ordinal prefix. It forwards the returned grid integers and enclosure objects without re-rounding, and the private origin binds the current owner, the identical incidence and the identical kernel result.

The selected pairs are (ell,k)=(0,0), (2^53,2^55+1), and (0,1710). The first uses the zero-residue limit, the second has exact residue 1 and positive denominator lower endpoint, and the third retains negative F and R before the odd power. The three certificate records exactly match the candidate's saved evidence; their current wrapper/incidence/result identities and field values all validate. Only one pi setup and one square-root setup occur. A later prepare call is charged without repeating either setup.

Foreign wrappers, cloned bindings, substituted output, changed incidence fields, changed rounded integers, changed p, replaced enclosure objects and replaced certificate objects are rejected. Numerically equivalent incidence records can be validated by arithmetic; that is intentional and does not imply authentication of external serialized provenance.

## 5. Accounting and required clarification

Within the reviewed bounded run, the ledger covers header/input parsing, both original computation and semantic replay, actual-width signed integer fields, sparse-output copies, endpoint/prefix construction, loop/address bookkeeping, returned incidences, validations and coefficient wrapping. Scalar arithmetic has its own additive cumulative ledger. Failed validation preserves the already-spent prefix. In the malformed-prefix control the ledger records max_bits=16386, events=53 and bit_work=68,755,255,552 before rejecting the boolean imaginary component.

Copies/reference storage, fixed-length record construction and schoolbook endpoint arithmetic fit the conservative constant-count width-squared envelopes. Event-counter width is explicitly included. The original input rows remain retained for replay and are additional state beyond the endpoint table. The test driver's retained record list, JSON artifacts, ledger snapshots and host runtime are separately bounded test-harness work, rather than silently treated as part of the production stream's O(Sm) state.

The candidate's general O(S R log(R+1) H_e^2) producer statement omits arbitrary row-address/counter widths if H_e means only supplied numerical widths. It also cannot suppress an arbitrary prior cumulative event count. ERRATUM.md supplies the required corrected bound and memory/observation boundaries. That clarification must accompany publication; the unqualified general formula is rejected. The R=3, fixed-width target and existing source receipts are unaffected.

## 6. Exact accepted scope and remaining work

This closes only the local numerical producer/refinement, semantic association and bounded outer iterator/three-record binding subgate, subject to ERRATUM.md and the separate numerical review. It does not establish:

- accepted full sparse-pipeline or input/tape provenance;
- complete coefficient-stream evaluation;
- multiplication by estimates, scatter, every-tape finite accumulators, N outputs, final rounding or scale-back;
- dense fallback/all-length dispatch or independent J-call amplification;
- a parent recovery theorem or completion of ALG-034/ALG-038.

Q16 and STR-Q1 archival status and all original norms, probabilities, scopes and trust assumptions are unchanged. The work is an engineering subresult for the open ALG-034/ALG-038 dependencies only.
