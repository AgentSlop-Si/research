from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
QUEUE=ROOT.parent/'BASELINE_TEXT_REVIEW_QUEUE_2.json'
S=json.loads(QUEUE.read_text())['sources']
INDICES=[7,15,19,20,21,23,24,26,27,35,38,41,49,54,58,62,67,69,70,86,87]
R={}
def add(i,kind,claims,proof,corrections,dependencies,implication):
    R[i]={'classification':kind,'substantive_claims':claims,'independent_proof_scope':proof,
          'corrections_and_qualifications':corrections,'unresolved_dependencies':dependencies,
          'constructive_fft_implications':implication}
add(7,'graph_reuse_proof_and_source_corrections',[
    'Support influence W is weighted coverage/submodular and bounded by O(N(1+log(k+1))).',
    'Cyclic-coset correction admits an L-value representation; augmented MST optimizes fixed additive one-parent costs.',
    'Documents repaired O(E) retained-history scans, chronological suffix replay and missing-history rebuild accounting.'],
    'D1 independently proves coverage, coset and restricted MST statements; 256 exact influence identities and65,536 submodular pairs passed. The first50-source review independently checked45 cosets.',
    'Output copies add +1; missing history invalidates min(H,r+k). Old history timing gains are bug-removal gains. MST optimality needs retained outputs, symmetric fixed costs and no cache constraint.',
    ['Actual graph/replay implementation, instrumented regressions and raw timings.','External pinned integer-multiplication and prior-art claims not newly retrieved.'],
    'Producer-supplied sparse candidate graphs, quotient views and simple lineage are useful restricted-workload opportunities, without arbitrary-input FFT gains.')
add(15,'packing_and_shared_dag_findings',[
    'Two real transforms can be recovered from one complex FFT via Hermitian symmetry; packed squaring yields real convolution after padding.',
    'Known low-rank families and sparse edits save amortized work; joint DAG benefits are input-dependent.',
    'Contrasts finite-field lookup WHT bit bounds with exact complex FFT and fixed-power logarithmic savings.'],
    'D2 independently derives packing, convolution and linear-family identities; exact-collision limits are independently established by row49/54 proofs.',
    'Packing uses variable conjugation and real-input restriction; it is not a strictly complex-linear free primitive. Butterfly savings and preparation-excluding benchmark ratios are not end-to-end wins.',
    ['Historical implementation/tests and timings.','Actual Alman/Alman-Rao/CrocSwap primary sources and models for literature claims.','Rank detection conditioning and integer-rounding bounds.'],
    'A practical real-data constant-factor trick and relation-aware architecture; neither supplies a new general exponent.')
add(19,'dense_convolution_proof_and_coverage_barriers',[
    'Karatsuba saves one recursive multiplication; bilinear multiplicative rank2n-1 is optimal and attained with enough evaluation points.',
    'Binary affine-template/sparse-residual union bound and finite-complex-affine-union obstruction reject small universal covers.',
    'Reported dense interpolation achieves lower variable-product count but loses total runtime.'],
    'D3 independently checks bilinear rank, interpolation hypothesis, binary cardinality and moment-curve complex witness proof.',
    'Variable products exclude scalar preparation/additions and are not total-time lower bounds. Finite-field root/evaluation-point limitations remain; finite templates do not cover input-dependent infinite families.',
    ['Actual implementations, exact finite audits and timing harness.','External #130 model/formalization assertions remain attributed, not freshly verified.'],
    'Focus on cheaper evaluation/interpolation rather than reducing already-linear variable products.')
add(20,'exact_skeleton_architecture_proofs',[
    'Arithmetic-progression Fourier rank equals min(a,b,N/gcd(N,st)); rank-r approximation requires many entrywise residual nonzeros.',
    'Independent direct-dot skeleton decoder has Omega(N^1.5) work; periodic Fourier-column residual has sharp N²-Nr(1+t/2) sparsity.',
    'Bounded-coefficient unnormalized Fourier determinant bound requires growing constants for the proposed exponent saving.'],
    'D3 independently rederives the Vandermonde, residual-count, periodic-sharpness and determinant arguments. New controls checked405 rank cases and30 attained periodic bounds.',
    'Decoder lower bound assumes independent dot products and direct residual summation. Dense residuals can factor efficiently, as ordinary radix2 shows. Modular cheaper gates do not automatically lift to characteristic zero.',
    ['Exported cyclotomic graph certificates and operation conventions for source-specific counts.','Growing family of fused exact circuits and charged uniform preparation; numerical stability and external prior art.'],
    'Provides exact rejection gates while preserving shared/factored correction as a legitimate route.')
add(21,'conditional_sparse_backend_composition',[
    'Grouped known-k sparse correction costs O(N+(N/b)A(b)) with b≈k, including all positions and twiddles.',
    'Substitution of external #130 primitive gives a conditional sparse-update exponent but does not improve the dense worst-case exponent.',
    'Prepared fixed-point edits show historical numerical gains with cached phases and charged initial FFT.'],
    'D4 independently derives decomposition and root-composition conditional logic;132 new exact modular cases/5586 output coordinates passed using a direct DFT backend.',
    'The Python prototype implements no #130 algorithm. Reported prepared-point accuracy checked final cached output, not every intermediate spectrum; fixed-position phase storage is charged.',
    ['External theorem and actual exact backend with specified roots/uniform cost.','Uploaded implementation/timing validation, accumulated error and all-output checks.'],
    'A correct black-box composition and useful dynamic interface, not a new independently built arbitrary-input FFT.')
add(23,'fixed_pair_proof_and_phase7_source_audit',[
    'Four kernels R,bR,aR,abR support ordered two-factor sparse updates, shifts and gains, with cross term captured automatically.',
    'Dense cost O(N(1+s_a+s_b)) follows after fixed-pair preparation; more editable factors require2^t maintained subset kernels.',
    'Reports tuple-hash, seed-scan, unbalanced-join, cache-warmth, memory and three-position benchmark-validation limitations.'],
    'D6 independently derives kernels and zero-safe shift/gain extension;180 new integer cases passed. Source line-specific code findings are historical audit evidence, not rerun here.',
    'Updated complement is essential for cross term; selected-time queries can regain s_a*s_b cost. O(logm) allocated nodes is not full operation latency, and warm root need not warm subtree caches.',
    ['Original persistent_chain source and subsequent exact-hash repairs.','Matched native/fixed-pair benchmarks, retained-state memory and numerical-stability analysis.'],
    'A concrete restricted two-factor implementation opportunity after repairing basic metadata/balance costs.')
add(24,'self_contained_linearization_gate',[
    'Division-free polynomial circuit for a linear map yields at most3s linear gates plus O(s) constants.',
    'Rational regular-basepoint/generic finite equality branches give nonuniform reductions with basepoint/path caveats.',
    'Binary and finite-field function identities evade formal differentiation; nonlinear k cancellation gives no automatic saving.'],
    'D5 independently verifies first-order propagation and domain caveats;150 new modular basis-direction controls corroborate nonlinear-k cancellation.',
    'Reciprocal derivative constants also require O(s) preparation. Equality as a finite function is insufficient; no bounded-coefficient or well-conditioned restriction is inherited automatically.',
    ['Uniform generic path/basepoint discovery for rational/branching algorithms.','Source-specific extracted graph and historical exact matrix checks; external prior art.'],
    'Narrows unrestricted fresh-input search to genuinely new charged linear evaluators rather than cosmetic nonlinear rewrites.')
add(26,'projected_graph_and_range_product_proofs',[
    'Projected ring evaluation, affected-ancestor bounds and zero-safe gap products support persistent selected-frequency queries.',
    'Disjoint sparse table trades O(mqlogm) setup/storage for constant-count interval products; projected Hasse jets query in O(q(k+d)).',
    'Repairs replay scans, missing-history estimates, group-wide republishing, cache budgets and update-boundary planner cost.'],
    'D6 independently checks ring homomorphism, affected-ancestor sum, interval split and Horner-jet costs under stated cache/index hypotheses.',
    'General DAGs are not balanced trees. Planner-at-update work prevents unconditional O(1) producer latency. Missing history forces rebuild; group cache caps exclude other memory.',
    ['Actual repaired implementation, imported symbolic graph correctness, measured cache/frontier behavior and all-output tests.','Modular/CRT bridge coefficient/root/carry details and bit complexity.'],
    'Useful explicit output-specific routes rather than a universal optimal dispatcher or transform exponent improvement.')
add(27,'coalesced_single_view_final_report',[
    'Coalesces pending snapshots by changed keys u rather than event count H; query arithmetic uses min(u,r+k).',
    'Full Python query additionally costs O(u) reclamation, with amortized cancellation compaction and owned projection storage.',
    'Final measurements give0/8 setup-inclusive wins, superseding preliminary1/8; known severe-cancellation failure remains.'],
    'D7 independently checks exact snapshot algebra, reclamation lower-bound case and binary64 cancellation mechanism; no benchmark replay or uploaded code execution.',
    'Use final zero-win result, not preliminary1.13x. One1.03x stream-only result is not robust. Passing16 tests includes a test documenting known error, not universal correctness.',
    ['Full implementation ownership/compaction review, stable rebuild policy, reproducible variability and meaningful application workload.'],
    'A specialized bookkeeping design with clearer costs, currently no convincing setup-inclusive performance advantage.')
add(35,'compiled_polynomial_jet_research',[
    'Formal Hasse coefficients yield exact single-impulse shift formula; symbolic impulses allow sparse point corrections.',
    'Fused generated loop costs O(N d_dense+s), but cold JIT and seed/kernel preparation are substantial.',
    'Reports near-hand-native warm timing and much worse isolated cold timings.'],
    'D6 independently verifies formal identity and charged execution shape; first50-source controls checked144 exact single-edit instances. Generated/Numba execution was not inspected or run.',
    'Kernel immutability/fixed-base contract, requested output type and all preparation matter. Tiny float errors are not worst-case stability certificates; native performance sometimes reverses.',
    ['Generated-source validation and compiler environment, signature cache behavior, full code review and matched fresh-process timings.'],
    'An engineering reduction in allocations/dispatch for persistent bounded-degree workloads only.')
add(38,'original_projected_view_research',[
    'Projects fixed bases into q requested frequencies, replays H relation updates or rebuilds r+k terms.',
    'Classical prefix/band output pruning and conditional #130 registration composition reduce selected-output work.',
    'Historical C++/Python timings demonstrate workload changes and projected storage savings.'],
    'D1/D4/D6 independently validate Fourier linearity and scoped pruning/composition ideas; this original document is superseded in implementation-level costs by rows7/26/27.',
    'Correct query bound includes q output copy; retained-log scan and event payload were omitted, and missing history forces rebuild. Pruning bound needs1+logq at q1. Do not claim integrated-design priority without the literature review this source itself requests.',
    ['Original-versus-repaired source binding and actual deployed implementation.','Projected-buffer ownership, event storage, calibrated timings and external backend/prior-art verification.'],
    'A strong explicit producer/consumer abstraction, with historical costs corrected rather than accepted wholesale.')
add(41,'integer_translation_and_cover_proofs',[
    'Near powers of two, A-k gives linear-bit special cases with detector/correction included.',
    'Universal improvement requires a cheap full additive cover; |S||K|>=2^n is necessary.',
    'Flat signed-power splitting cannot beat w(A)<=w(A-k)+w(k); small offsets cannot freely alter high bits.'],
    'D3 independently checks covering, representation concatenation and carry logic. NAF optimality attribution and historical exhaustive values are not newly established by code here.',
    'Flat-term lower bound excludes shared/factored addition chains. Calling growing k a constant is invalid. Detector plus fallback preserves, rather than improves, baseline asymptotic order.',
    ['An actual broad fast family with uniform cheap selection and correction.','Exact source/timing validation and cited primary proof of NAF minimality.'],
    'Keeps the user’s proposal as a precise constructive covering problem instead of dismissing valid restricted gains.')
add(49,'exact_collision_dag_proof',[
    'Canonical ordered-child IDs certify equal FFT subproblems; butterfly cost is sum(m/2)U_m.',
    'Fixed-period input uses O(pN) butterflies, while iid binary large levels remain unique with high probability.',
    'Prepopulated lookup tradeoff pays exponential/subexponential space for reduced online merges.'],
    'D2 independently verifies inductive identity, occupancy expectation, union bound and fixed-period work argument.',
    'Expected hash-table complexity assumes word-RAM keys; full intermediate storage can be O(NlogN). Empty unlimited memory is not a precomputed-answer oracle.',
    ['Prototype and benchmark execution, bit precision, dictionary overhead and memory-access model for huge tables.'],
    'Restricted repetitive-input reuse is valid; exact random collisions cannot deliver general asymptotic saving in this algorithm.')
add(54,'equivalence_cache_proof_and_findings',[
    'Shift/reversal/affine-index/complement/sparse-edit Fourier recovery formulas allow orbit reuse.',
    'Even the larger affine/complement orbit has at mostm² variants at dyadic lengthm, leaving iid large blocks unique with high probability.',
    'Historical prototype saved butterflies but lost all displayed wall-clock comparisons; cached single edits exclude seed FFT setup.'],
    'D2 independently derives substitution identities and orbit-count collision bound.',
    'Recovery formula does not make recognition free. The no-go concerns this finite orbit-DAG class, not general nonlocal circuits or arbitrary equivalences.',
    ['Canonicalizer/Booth implementation, exact reconstruction counters and current native baselines.','Historical external repository comparison and model-specific prior art.'],
    'Directs effort toward supplied relations or symbolic circuit sharing rather than ever-larger input-symmetry caches.')
add(58,'bivariate_jet_and_aot_research',[
    'Two impulse edits require mixed Hasse coefficients; displayed A²B+AB+B²+CD expansion includes K11 and K21.',
    'Prepared dense/sparse kernels yield O(ND+S) output work; generated AOT signature contains degrees, not data.',
    'Historical native timing excludes predeployment compilation, which must be charged for first build.'],
    'D6 independently checks bivariate formal expansion and costs, not uploaded binary safety/correctness. First50 row101 reports a separate symbolic float-cancellation defect.',
    'Formal exact identity does not make float graph canonicalization exact. Scalar folding (2^53)+1-(2^53)=0 can destroy exact coefficients; new independent scalar control confirms the mechanism, not the uploaded code. Native timings remain unexecuted reports.',
    ['Exact symbolic coefficient representation or bounded-input guard; AOT/source ABI/security and full code audit.','Preparation/deployment cost, numerical stability and exact backend.'],
    'Useful simultaneous-edit automation after preserving cross terms and coefficient correctness; no fresh-input exponent consequence.')
add(62,'adaptive_engine_readme',[
    'Documents verified exact-input caching, research shift/sparse/span detection, known-family reconstruction and fresh returned output arrays.',
    'Optional shared DAG and packing are educational; optimized real FFT fallback remains central.'],
    'D2 supports algebraic formulas and restricted complexity, but API ownership, full hash verification, cache budget and detection behavior require actual source.',
    'Dense detection and output copies cannot disappear. LRU excludes some auxiliary structures; finite floating tests do not imply arbitrary exact integer multiplication.',
    ['Implementation/tests, cache-lifetime/memory accounting, rank-detection conditioning and realistic compiled comparator.'],
    'Prefer producer-known structure and conservative fallback; unrelated fresh input receives no new asymptotic bound.')
add(67,'original_phase5_research',[
    'Shifted-basis plus sparse relation gives direct selected-bin or dense reconstruction and tracked subscriptions.',
    'Grouped sparse transform has O(N(1+log(k+1))) work; #130 substitution is explicitly theoretical.',
    'Describes shape-based warm profiler and partial memory categories.'],
    'D4 verifies grouped identity and scoped conditional composition;132 new exact modular cases passed. State operations and dispatcher implementation were not run.',
    'Exact-hash row91 specifically corrects this source’s claimed benchmark seed and documents spectrum-only auto, admission and backing-allocation defects. Work-array eligibility is not hard RSS. Same-four-bin methods are the appropriate comparison, despite this source’s awkward comparison sentence.',
    ['Patched source and regression binding, original benchmark driver/seed, honest live-buffer estimates and cache-warmth-sensitive calibration.'],
    'Useful relation-aware state interface only after separating algebraic promise from historical implementation bugs.')
add(69,'self_contained_phase_state_rank_proof',[
    'Paired input/output-bit unfolding rank is2^min(s,L-s) by exact Vandermonde factorization.',
    'Subtracting Walsh raises interior-cut rank to r+1 when both sides have at least2 paired bits.',
    'Short MPO description and dense sweep costs are distinguished from optimal circuit cost.'],
    'D5 independently checks phase composition, exact rank, outside-row/column-space correction argument and scoped contraction accounting.15 new exact F257 cut cases passed.',
    'Fixed paired ordering and linear chain state are essential. High rank does not prove high arithmetic work; approximate low-bond and structured-input methods have different contracts.',
    ['Historical checker/source binding and targeted current primary-source comparison for novelty.','Any alternative topology/contracted evaluator would need its own charged analysis.'],
    'A valid architecture-specific exact-width obstruction, not an all-FFT lower bound.')
add(70,'native_adaptive_binary_fft_readme',[
    'Documents uint8/bool binary validation, output ownership, fixed explicit methods and cached-plan autotuning.',
    'Selector compares codelets and tiny lookups with8%/75% guards; tuning can take hundreds of thousands of calls to amortize.',
    'Historical ASan/UBSan claims exclude leak checking.'],
    'The API/cost/lifecycle contract was fully read; no C source compiled, shared library loaded or sanitizer executed in this review.',
    'Finite codelets/tables give constant-factor choices, not a new asymptotic FFT. Calibration and public-call overhead are distinct from warm C batches; leak safety is unverified.',
    ['C/wrapper source and build provenance, buffer-overlap/lifetime guards, sanitizer receipts, benchmark variance and true break-even.'],
    'Fixed-method explicit plan is a sensible low-setup API; automatic tuning only makes sense for enough repeated work.')
add(86,'cache_rewrite_readme',[
    'Uses exact bounded-integer symbolic difference to reuse a cached U*B in A*B=U*B+(A-U)*B.',
    'Bounds candidate/search/node visits and pins cached frontier; result cache is not total memory.',
    'Explicit cancellation example changes2.220446049250313 to2.0 under floating reassociation.'],
    'D6 verifies commutative-ring identity and boundary conditions; actual signature matcher, liveness pinning and48 witness checks remain implementation dependencies.',
    'e.one is an impulse, not all ones; no FFT butterflies inside SciPy are rewritten. Bounded integer certificates do not remove floating reassociation error or lifetime graph growth.',
    ['Exact cache/signature implementation and full finite-field witnesses.','Stable execution policy, peak/lifetime memory, same-scope benchmark including strongest specialized update.'],
    'A restricted related-product-graph optimization, with real arithmetic savings possible but no new transform theorem.')
add(87,'projected_graph_integration_readme',[
    'Combines projected persistent circuits, interval indexes, selected-frequency jets, repaired consumer grouping and modular/CRT reference.',
    'Registration stores only selected projections and cannot add bins later without source data; zero-safe routes avoid division.'],
    'D6 supports underlying projection/interval/jet algebra; row26 supplies the fully read detailed proof/correction report.',
    'Different output contracts require different APIs. Cache caps exclude projections, graph metadata, outputs and scratch; top-level historical reruns are not fresh receipts here.',
    ['Actual adapters/imported graph semantics, source/result bindings, numerical overflow/underflow and benchmark evidence.','Exact CRT coefficient/carry/bit-cost bridge beyond small reference cases.'],
    'A useful output-aware collection of restricted algorithms, not a universal optimal planner or integer exponent improvement.')

assert sorted(R)==sorted(INDICES)
(ROOT/'source_texts').mkdir(exist_ok=True)
rows=[]
for i in INDICES:
    s=S[i];p=Path(s['absolute_path']);b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
    assert h==s['sha256'] and len(b)==s['size_bytes']
    snap=Path('source_texts')/f'{i}_{h[:16]}{p.suffix}';(ROOT/snap).write_bytes(b)
    rows.append({'queue':'BASELINE_TEXT_REVIEW_QUEUE_2.json','queue_index':i,
                 'sha256':h,'filename':s['filename'],'size_bytes':len(b),'absolute_path':str(p),
                 'canonical_path':s['canonical_path'],'source_provenance':s.get('provenance',[]),
                 'inspection':'complete_text_read','full_read_scope':{
                     'bytes':[0,len(b)],'lines':[1,len(b.decode('utf-8').splitlines())],
                     'encoding':'utf-8','method':'Entire source printed and inspected in untruncated bounded batches.',
                     'later_evidence_substitution':False},
                 'source_execution':'not executed or imported','historical_logs_and_measurements':'source-reported, not fresh receipts',
                 'local_inert_snapshot':str(snap),'proof_reference':'PROOF_SCOPE.md',**R[i]})
x={'scope':'Second, separate reservation:21 dynamic-reuse/linearization texts in queue2.',
   'review_date':'2026-10-10','completed_rows':len(rows),'completed_bytes':sum(r['size_bytes'] for r in rows),
   'queue_indices':INDICES,'queue_sha256':hashlib.sha256(QUEUE.read_bytes()).hexdigest(),
   'all_hashes_verified':True,'uploaded_executable_run':False,'originals_and_other_ledgers_modified':False,
   'identity_policy':'Only exact full hashes establish duplicate content, not filenames or thematic overlap.',
   'independent_checks':'INDEPENDENT_RESULTS.json','rows':rows,
   'cross_review_references':[{'path':'../review_queue2_rows90_139/COVERAGE.json',
       'sha256':hashlib.sha256((ROOT.parent/'review_queue2_rows90_139/COVERAGE.json').read_bytes()).hexdigest(),
       'purpose':'Exact-hash prior source reviews, especially rows91/101 historical corrections.'}]}
(ROOT/'COVERAGE.json').write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
print('Reviewed',len(rows),'sources',x['completed_bytes'],'bytes')
