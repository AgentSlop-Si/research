"""Build review documentation from manually authored findings and inert inventories."""
import json, hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
provenance=json.loads((P/'SOURCE_PROVENANCE.json').read_text())
notes={}
def add(sid,role,algorithm,disposition,limits,dependencies,findings='No additional correctness defect identified in the reviewed scope.'):
    notes[sid]={'source_role_from_static_content':role,'semantic_review':algorithm,'claim_disposition':disposition,'limitations':limits,'dependencies_and_side_effects':dependencies,'findings':findings}

add('S01','Graph-cut and Fourier-minor certificate verifier',
'L5–13 validate the exact N=2048, four-stage, 683-by-683 block and 676 distinct removed vertices. L14–35 construct directed Green-state and interstage bit-reversal edges, then test cut and empty-cut reachability. L36–47 count essential cut vertices and certify the Fourier block by a Vandermonde product.',
'Accepted for this supplied graph certificate and block. Fresh independent reconstruction confirms cut size 676, zero reachable targets, all 683 targets reachable without deletion, and determinant 24105 over F_65537. The rank upper bound requires the represented scalar-state factorization hypothesis.',
'Not a general four-stage, arbitrary-order or arbitrary-circuit FFT obstruction. Essentiality count was not rechecked and is unnecessary for an upper bound. Assertions disappear under Python -O.',
'Reads CONSTRUCTOR_N2048_CUT.json and writes N2048_VERIFICATION.json. No code imports beyond standard library. Exact input snapshot and current independent result are included.')
add('S02','Archive extraction and provenance helper',
'L5–7 index master files by byte hash. L9–23 inspect ZIP members, reject absolute/parent/backslash paths and symlink member modes, enforce declared size caps, extract read-only files, and record member/archive hashes.',
'Operational provenance utility only; neither hash matching nor extraction establishes semantic review or authorship.',
'Top-level code writes files and chmods archives. Assertions are not robust security checks under -O. No execution was attempted.',
'Requires fixed master path and original/*.zip; writes extracted/ and SOURCE_MANIFEST.json.',
'L15–20 do not ensure destination parents are free of existing symlinks, and duplicate detection uses literal member names rather than canonical destinations. Treat it as trusted-input extraction into a fresh directory, not a hardened arbitrary-archive sandbox.')
add('S03','Phase29 regression suite',
'L19–32 validate saved Bezout certificates and expected bounds. L34–62 test trace-polynomial evaluations and forbidden zero-entry roots. L64–95 inspect exhaustive/sample Macaulay records and a planted positive control. L97–112 compare the three-term executor with dense application and sample partial mappings.',
'Full source review of the test harness; its stored counts, complex solution bounds, exhaustive runs and executor passes were not re-executed. Sampled determinant checks and archived rank counts remain distinct from exhaustive recomputation.',
'The imported theorem/constructor/verifier implementations and certificate data are outside this 45-hash assignment. Runtime tests cannot be marked passed solely from assertions in this file.',
'Imports phase29_two_parameter, phase29_macaulay, phase29_executor, phase28_synthesis and phase28_polynomial; reads several certificate JSON files. Running the suite would execute those dependencies.')
add('S04','Linear measurement transcript and cost-model gates',
'L24–59 perform modular nullspace elimination with an explicit witness check. L66–140 build partition-supported measurements and compare a kernel witness with an invertible DFT. L143–153 explain the deterministic adaptive zero branch. L156–175 compute the continuous independent-row scan/FFT cost proxy. L178–210 test the shift-polynomial intertwining identity.',
'Accepted: fewer than N independent linear measurements cannot distinguish all inputs, including a deterministic adaptive zero path. The cost expression is only the stated separately executed-row model. Shift-polynomial identity is algebraic, not an FFT speedup.',
'No arbitrary adaptive policy is actually simulated. Requires a prime field, valid rectangular matrices and valid n/m. The cost model does not cover fused computation or general arithmetic circuits.',
'Imports SymPy and S06; script entry prints JSON.',
'Boundary defects: an empty measurement set returns a length-one null vector (L26–27), then transcript_certificate with n>=2 indexes it as an n-vector; complete_local_fourier_measurements(m=1) unnecessarily calls find_prime_root(1); separate_execution_lower_bound(1,1) divides by zero. These do not invalidate the supplied positive-domain theorem.')
add('S05','Sequential Fourier moment state bound',
'L16–31 form 2N-1 moments, an N-by-N Hankel matrix and its finite-field rank. L34–40 encode the polynomial root-count reason for a fixed input-independent recurrence to need degree at least N.',
'Accepted scoped mathematics: a nonzero monic recurrence polynomial annihilating all N distinct Fourier modes has degree >=N, and nonzero modal weights give H=V diag(x) V^T of full rank.',
'The lower bound concerns fixed scalar recurrences / linear time-invariant realizations for arbitrary inputs, not general algorithms or input-dependent descriptions. The recurrence function merely returns the already supplied inequality.',
'Imports S06 root/rank helpers; script prints finite test records, which were not rerun.')
add('S06','Permutation displacement rank gate',
'L24–68 count zero-sum cycles and construct negation minimizers. L71–176 find exact roots, eliminate finite-field matrices and handle the inverse-root shift convention. L179–214 enumerate predicted ranks or compare them to two direct matrix constructions.',
'Accepted scoped theorem: rank(D-P)=N minus the number of permutation cycles with sum 0 modulo N; min_P rank=floor(N/2). Fresh direct matrix checks cover all 872 permutations for N=2,3,4,5,6.',
'Exhaustive_minimum enumerates the predicted formula, not a new direct rank per permutation. General minimum follows the cycle-count argument in REVIEW.md. This is not a general FFT lower bound.',
'SymPy is used for primality, factors and roots; no external data writes in library functions; entry prints records.',
'cycles_of and matrix constructors assume valid permutations without enforcing bijection; rank_mod assumes a prime modulus and consistent row lengths. Preserve those API preconditions.')
add('S07','Numerical cosine/sine split of negation basis',
'L16–32 form kernel and complementary pair vectors, assigning the even fixed point to the complement. L35–57 compare Fourier images with cosine/sine identities. L58–66 report numerical ranks with tolerance 1e-9.',
'The pairwise trigonometric identities and dimensions are accepted algebraically. Numerical rank fields are diagnostics, not exact certificates or complexity lower bounds.',
'No execution or floating-point result reproduced. Two dense transform halves do not by themselves prove either an algorithmic lower bound or a speedup.',
'Uses NumPy; prints diagnostics for selected N; no source-data dependency.')
add('S08','v16 subprocess runner',
'L6–15 run unittest and persist its status; L16–26 run four component scripts and save stdout as result files.',
'Full static review of orchestration only. The final cold-run message is conditional on executions that this review did not perform.',
'No timeout, resource cap, isolation or exact dependency hash binding. Later-script failure exits before writing the final accumulated log.',
'Would execute S04–S07/S09 and overwrite result JSON/log files.')
add('S09','v16 regression suite',
'L20–43 cover sampled cycle ranks, formula-based exhaustive minima and exact minimizers. L46–91 cover transcript kernels, a complete local frame, an explicit cost proxy, moments, numerical reversal splits and polynomial shifts.',
'Test intent and assertions reviewed; test results not replayed. Exact field checks are separated from S07 tolerance-based numerical checks.',
'The exhaustive minimum check uses S06 predicted_rank. Fixed examples and recurrence/cost assertions do not enlarge the mathematical model.',
'Imports S04–S07 and standard test modules; running executes all imported dependencies.')
add('S10','Library transfer/materialization helper',
'L24–104 validate transfer objects and apply/verify extended attributes. L107–157 restrict ambient credential injection to a configured HTTPS Estuary origin/path. L160–211 disable redirects only for that ambient-auth path and download bytes. L214–251 use a sibling temporary file plus atomic replace; L254–303 implement CLI/error handling.',
'Operational helper, not mathematical evidence. Authentication-origin restriction and temporary-file replacement were inspected statically; no credentials, URLs or network transfers were accessed by this review.',
'Requires trusted transfer metadata and authorized destination. No expected checksum or byte limit is enforced. An absolute path requirement is not a containment restriction.',
'Would read authorization-related environment values / auth.json if needed, perform GET requests, set xattrs, possibly invoke macOS xattr, and replace a destination file.',
'For non-Estuary URLs, caller-provided headers use the ordinary urllib redirect handler; the special no-authenticated-redirect protection does not cover those headers. Do not treat arbitrary transfer JSON as safe input or run this archived helper merely to inspect it.')
add('S11','Green-bank simultaneous separation theorem and finite-field certificate generator',
'L25–140 implement primality/root and modular elimination. L145–270 analyze cycles, recursively halve separated sets and select a common cycle cell. L275–298 evaluate gauged cyclic Green / Fourier rectangles. L324–448 build Hamiltonian, bounded-cycle, exhaustive two-order and boundary controls.',
'Accepted scoped combinatorics: repeated separation yields at least floor(N/2^t) labels on each side, with rank <=1 per Green term; bounded-cycle partition pays product(c_r). The prime-length complex exclusion is conditional on the separate prime Fourier full-spark theorem. Finite-field examples do not prove that theorem.',
'Applies to sums of the specified gauged resolvents, not arbitrary products. Every relevant cycle denominator must be nonzero. is_prime_64 is justified only below 2^64, although the API does not enforce that bound. Selected finite-field minors may vanish even when the complex prime-length theorem holds.',
'Standard library only; entry writes results.json. Orders/universe dimensions and primality-related valid domains are assumed beyond partial checks.')
add('S12','Independent-by-content v18 finite-field verifier',
'L18–76 contain a separate elimination implementation; L79–116 reconstruct cycle positions, separated sets and Green blocks. L119–143 rebuild seven seeded cases, while L146–155 assert rank gaps and write records.',
'No import of S11 is present. This is useful algorithmic separation but not proof of independent authorship or execution in this review. Case assertions remain unrun.',
'Hard-coded moduli are assumed prime; inv(0,p) silently returns zero, and the generalized API lacks singular-denominator/root validation. Main seeded cases reject singular alpha values, so this is a domain caveat rather than a demonstrated failure of those cases.',
'Uses standard library; writes independent_results.json. It reconstructs cases but does not read and compare the saved results.json despite the phrase “saved v18 cases.”')
add('S13','v18 subprocess runner',
'L6–20 execute the main generator, independent verifier and unittest suite, copying combined output into run_all.log and stopping on a nonzero return code.',
'Orchestration reviewed; no runtime success or numerical claim accepted from the final print statement.',
'No timeout, sandbox or source-hash pinning; overwrites a log and relies on installed runtime/dependencies.',
'Would execute S11, S12 and S14 and their associated writes.')
add('S14','v18 regression suite',
'L22–40 check sampled separation sizes/orientations; L42–66 test seven Hamiltonian rank certificates, bounded-cycle cell bounds and all 8! second orders. L68–83 check threshold arithmetic and optionally compare regenerated results with an existing file.',
'Full test-source coverage, with no execution. Boundary tests correctly assert only that the universal threshold cannot force a larger rectangle; they do not claim every subthreshold instance is feasible.',
'The roundtrip comparison is skipped if results.json is absent. Most mathematical routines are the same implementation under test, not a distinct proof.',
'Imports S11; optional saved results.json dependency.')
add('S15','v18 inert-JSON certificate reconciliation program',
'L12–51 independently implement separation, cycle positioning, elimination and root construction. L54–73 compare every saved Hamiltonian row, L75–81 enumerate 40320 second orders, and L84–100 reconstruct bounded-cycle controls.',
'Program logic supports detailed same-seed reconciliation and correctly states the sums-only / prime-Fourier / nonsingular-cycle scope. Its top-level “passed” output is not a current-run result.',
'No assigned program was run. Input JSON must exist and match the intended artifact; assertions and seeded reconstruction alone do not prove characteristic-zero generalizations.',
'Reads bank_v18/.../results.json, imports SymPy and writes BANK_V18_INDEPENDENT_REVIEW.json at top level.')
add('S16','Phase31 higher-generator Macaulay and executor controls',
'L6–14 load six matrices and generate extra cyclic components. L15–42 build degree-three homogeneous minor multiples and incremental modular rank. L44–57 exhaust N4 q6 mappings but sample N8/N16 q6 and q7 mappings. L59–77 compare five-term scans on basis and two additional vectors with dense matrices.',
'Scoped finite-field rank/control harness. A full column-rank homogeneous Macaulay matrix excludes nonzero projective parameter solutions for the represented equations; deficient rank alone would not prove feasibility.',
'Only N4 q6 mapping coverage is exhaustive here; q6 larger cases use 24 samples and q7 uses 3. load checks the header but not the exact six-matrix length or trailing data. No current result replay.',
'Reads REBUILT_INPUT_N*.bin and PRIOR_REVIEW_FAMILY_SPECIFICATIONS.json; writes PHASE31_AUXILIARY_REVIEW.json. Matrix provenance/lift is external.')
add('S17','C++ seven-minor rectangular Macaulay rank audit',
'L11–44 implement bounded modular arithmetic, quadratic/cubic monomial indexing and 35-column elimination. L46–66 expand seven 3x4 target minor equations into 35 cubic rows. L68–90 load matrices, enumerate distinct ordered mappings, select cases, parallelize rank calculation and write rank bytes.',
'Algorithm is a finite-field rank audit with 35 columns; no binary was compiled or executed. Exhaustive versus sampled status is determined by actual index selection, not the filename.',
'Assumes native little-endian-compatible binary words and entries already reduced below P. General malformed input is not hardened. Missing output-write checks can allow a success-looking stdout without a valid rank file.',
'Requires OpenMP and input binary / optional uint64 case-index file; emits an unsealed raw rank stream.',
'L80 silently accepts a trailing partial uint64 index because eof is true after a short read. Duplicate indices are accepted. Caller must validate index-byte divisibility, uniqueness, expected count and output success before claiming exhaustive coverage.')
add('S18','Phase31 matrix/data reconstruction and sample provenance',
'L11–28 rebuild modular inverses and gauged Green matrices and decode exact-length binary inputs. L30–43 derive A^-1 F C^-1 and five components, compare stored matrices, then write rebuilt inputs. L44–56 regenerate the planted control, mapping 9682 and 100000 sampled N16 IDs.',
'Useful reconstruction/provenance harness; no execution. N16 is explicitly a 100000-case sample of 146764800 mappings, not exhaustive.',
'Root check at L32 assumes power-of-two n; generalized odd n would need exact-order validation. Invertibility and nonzero target checks apply to loaded specifications. Exact authorship/provenance is not established by the introductory docstring.',
'Reads prior family JSON and Phase31 certificates; writes reconstructed binaries, planted case ID and PHASE31_PREPARATION_REVIEW.json.')
add('S19','Phase32 separate reconstruction and metadata audit',
'L10–48 supply independent Gaussian/rank, recursive Fourier and cyclic-solve routines. L50–110 reconstruct seeded interpolation. L112–135 compare fingerprints, fitted columns, dense/probe/Weyl failures and sample residual ranks while recording overwritten probe labels. L138–158 check q=N controls, determinant monomial uniqueness and sparse-system comparisons.',
'Full source review of a scoped finite-field reconciliation program. Fresh inert-data inspection corroborates the reporting bug in 16 of 17 records, but fingerprints, full output vectors and residual ranks in this archived checker were not rerun.',
'Model supports only the intended extra=0/1 and nonempty small-domain choices; its cycle-selection while loop is unbounded. q=N controls are O(N^2) online, not fast FFTs. Monomial uniqueness is checked for one N8 q3 construction.',
'Reads four Phase32 audit JSON files and writes PHASE32_INDEPENDENT_REVIEW.json. No supplied imports, but executing this file would still execute an assigned program and was prohibited.')
add('S20','Paired-order weighted-Green separation reconciliation',
'L10–54 rebuild rank, random weighted branches, strict separated halves and arc-product entries. L56–74 compare 148 stored rank records; L76–97 handle zero-edge and shared-order controls; L99–110 expand small prime Fourier determinants as exact integer polynomials.',
'Separation/rank mechanics reviewed. The complex prime-order polynomial nonvanishing test is mathematically appropriate for the listed prime cases. General exact/approximate all-length norm claims are explicitly outside the finite-field computations.',
'Current review did not run the 148/30/20/48 assertions. Static literal counts must not be substituted for evidence of a successful run. The general norm theorem needs its own proof.',
'Reads VERIFY_RESULTS.json and writes SEPARATION_THEORY_INDEPENDENT_REVIEW.json; standard library only.')
add('S21','Partial Fourier interpolation constructor and audit',
'L28–70 validate power-of-two roots and implement exact cyclic solves. L73–104 perform small linear solves and rank. L109–177 choose distinct non-affine/noncommuting cycles, resample parameters and solve row gauges with q=k or k+1. L179–219 implement O(qN) application and a negative-exponent radix-two reference. L222–268 compare fitted columns, dense/probe responses and a Weyl relation.',
'Accepted conditional construction: successful row systems enforce exactly the designated k columns, and application uses O(qN) field operations. It is explicitly not a complete Fourier identity for the q<N instances. q=N costs O(N^2) online. Termination/generic success is not proved merely by retry loops.',
'Finite field and power-of-two valid domain; cycle search has a 10000-trial cap and alpha/gauge search has a 50-attempt cap. Setup/runtime bounds exclude bit complexity and successful-search guarantees. Empty columns and tiny non-affine cases are unsupported.',
'No nonstandard imports; CLI optionally writes audit JSON. Saved neighboring data snapshots are included only as inert metadata evidence.',
'Confirmed reporting bug: j is the first unused column at L238–240, overwritten by the cycle loop at L257, and reported at L264. Sixteen of 17 supplied saved records have a wrong label. L223 also says “nonconsecutive” although L224 uses range(k). L135–136 overstates equivalence between first-k invertibility and full-support null direction; the extra-direction branch separately enforces full support.')
add('S22','Phase32 regression suite',
'L13–39 compare a Green scan against a distinct Gaussian solve. L41–103 test finite fitted columns, window/Weyl behavior, augmented and residual ranks, and monomial uniqueness. L105–137 cover q=N, an extra null direction and no-permutation diagonal-rescaling failure. L139–144 count plan/gauge entries.',
'Finite-example tests reviewed without execution. The planted q=N identity and partial-column counterexamples have different complexity and scope.',
'The suite imports the implementation under test and does not detect the mislabeled audit probe field. Its generic-language tests use fixed seeds and sizes; parameter counts are not timing or a universal setup guarantee.',
'Imports S21 and unittest; no external certificate reads.')
add('S23','Weighted paired-order separation control generator',
'L18–86 implement modular rank, independently mapped row/column orders, half-selection and cyclic weighted entries. L89–142 test zero weights and shared orders. L145–176 expand prime-order determinant polynomials. L179–221 generate finite-field rank records and summarize their gaps.',
'Accepted scoped lemmas: each strict separated Green rectangle has rank at most one, and each branch halves the retained row/column sets. The prime cyclotomic test is valid only for prime order. All-N approximate/complex theorems are not proved by these tests.',
'L210 checks only frank>=0, so finite-field Fourier rank exceeding q is a reported statistic, not an asserted universal pass. Zero-edge validity requires the nonsingular full cycle denominator; listed controls force product zero.',
'Standard library; writes VERIFY_RESULTS.json. THEOREM.md is referenced but outside this source assignment. General helper APIs assume valid permutations and prime order.')
add('S24','C++ exhaustive four-generator cubic Macaulay audit',
'L11–23 construct degree-two/three monomials and coefficient slots. L24–36 enumerate ordered distinct triples and lift nine cross-minor quadrics to 36 cubic rows. L37–49 eliminate over the configured prime, emit ranks and deficient cases.',
'Finite exact-field audit logic reviewed; no compilation, execution or exhaustive pass is claimed. Not clearing entries in old pivot columns does not affect the forward-only elimination because those columns are never reused.',
'Configured AUDIT_PRIME must be prime and sufficiently small for signed 64-bit products; the supplied primes fit. Input residues, positive n and successful file opening require external validation.',
'Reads a text matrix file and overwrites rank/detail outputs; no linked source dependencies.',
'L15 reads uninitialized header variables before checking stream success; malformed/missing input can trigger undefined behavior. n<=0 is not rejected, and output file errors are not checked. These are robustness flaws, not evidence that a valid archived rank stream is wrong.')
add('S25','Phase30 supplemental data/checksum and five-generator controls',
'L6–11 compare serialized text matrices with binary inputs and hash manifest entries. L13–20 construct five generators, exhaust N4 4x4 mappings and sample 100 mappings each for N8 and N16.',
'Byte reconciliation and fixed finite-field rank tests only; checksum correctness is separate from semantic correctness or exhaustive replay.',
'The rank=35 assertions do not show a successful current run. Larger sizes are explicitly sampled. Manifest paths are trusted, not containment-validated.',
'Imports S27 macaulay and external independent_utils; reads matrix/certificate/checksum files and writes EXTRA_RESULTS.json at top level.')
add('S26','Phase30 regression and stored-stream checks',
'L22–45 test executor agreement, N4 ranks and planted controls. L47–59 inspect stored N8/N16 streams. L61–97 recompute selected witness determinants and inspect planted stream ranks. L99–133 distinguish dimension counts, exhaustive N4 five-term controls and larger sampled controls.',
'The test source is fully reviewed. Stored all-20 byte streams plus a checksum are not themselves independent exhaustive recomputation; selected determinant calculations remain samples.',
'External phase30 implementations and binary data are not executed in this review. Comments about all-N dimension obstructions require their separate mathematical proof.',
'Imports phase30_four_parameter, phase30_macaulay and phase30_dimension_gate; reads many certificate artifacts. Assertions were not rerun.')
add('S27','Phase30 homogeneous-minor builder and preparation',
'L6–24 enumerate homogeneous monomials, expand cross-multiplied 2x2 equations and lift to a requested degree. L26–44 reconstruct four-generator families, check selected minors, plant valid controls and measure anchored/five-term deficiencies. L45 separately labels the stored rank stream as data-only.',
'Correct structural role: a full column-rank lift is an infeasibility certificate for the represented homogeneous system; rank deficiency is not an existence certificate. Data-only rank stream language is appropriately limited.',
'macaulay uses equal-sized row/column mappings and degree>=2; it does not validate all generalized inputs. External family construction and arithmetic dependencies are outside this assignment. No checks executed.',
'Imports independent_utils; writes text matrices, preparation results and family specifications; reads saved JSON witnesses/rank stream.')
add('S28','Largest growing-fiber replay wrapper',
'L4–6 construct the N=262144, Q=M=512, b=18 mode profile, call own_algorithm.from_modes/check and assert 9216 discovered modes. L7 records an output hash and a claimed full-entry check count.',
'Full wrapper review only. The literal “independent_output_entries_checked=N” is not verified here because own_algorithm.check is outside this assignment and was not executed.',
'Cannot infer end-to-end correctness, O(N) runtime, portability or no source execution from self-reported JSON booleans.',
'Imports own_algorithm, which may have import-time behavior; writes LARGE_PROFILE_RESULTS.json relative to the working directory.')
add('S29','Growing-fiber arithmetic profile and test-cardinality ledger',
'L6–22 define a pruning cost recurrence and count Berlekamp–Massey-style recurrence arithmetic. L24–44 rebuild deterministic profile costs and compare them with saved arithmetic totals. L45–51 derive test-loop cardinalities arithmetically, not by executing those tests.',
'Operation-ledger source reviewed, not replayed. Fresh inspection of its corresponding inert RESULTS.json finds all six new_arithmetic counts above baseline; the largest ratio is 7516160/7340032=1.0239955357. No arithmetic speedup is demonstrated by these profiles.',
'Word proxy is a separate metric and is explicitly not reproduced by this source. Inversion, root/setup, bit operations, memory traffic and wall-clock cost need the declared model; test counts are not successful test runs.',
'Reads source/RESULTS.json and writes PROFILE_MODEL_RESULTS.json. Uses the standard library only; the existing result data were snapshotted and their arithmetic comparisons freshly checked.')
add('S30','Temporary-directory companion replay runner',
'L4–9 copy three programs plus RESULTS.json, run two Python scripts in a temporary working directory and require three byte-identical result artifacts.',
'Portability/byte-equality harness only. Source text does not establish a successful replay, standard-library dependency closure or a security sandbox.',
'TemporaryDirectory changes the workspace, not process permissions or network access. Executed copies and transitive imports remain executable programs; the “source_code_executed=False” field is a historical classification claim, not permission to run them here.',
'Would copy own_algorithm.py, S28 and S29; run S28/S29 with an unpinned python command; write PORTABILITY.json.')
add('S31','Phase11 evidence collector',
'L14–21 collect sampled sparse-plus-low-rank product gates; L25–34 test Fourier Vandermonde witnesses; L35–45 gather Green-sum escape, SWAP realignment and the N4 counterexample to rank>=N-s. L46–53 serialize a scoped theorem statement.',
'Collector source and restrictions reviewed. Its accepted mathematical content is the weaker floor(N/(s+1)) rigidity bound and telescoping rank/sparsity gate, proved separately in REVIEW.md.',
'No current assertions rerun; counts and escape records are dependent on S37. Dense inverse or high realignment rank alone does not imply absence of a sparse-plus-low-rank representation.',
'Imports NumPy and all of S37; writes AUDIT_RESULTS.json.')
add('S32','Phase11 finite-field regression suite',
'L7–35 test roots, Fourier inverses and consecutive-exponent Vandermonde witnesses even after endpoint permutations. L37–60 test telescoping/low-rank inverse changes. L62–81 test the false-stronger-bound counterexample, SWAP and sums of two Greens.',
'Suite reviewed without execution. All-N claims rest on algebraic reasoning, not these finite random examples.',
'Random low-rank perturbations are inverted without a resampling guard; a singular seeded/generalized instance would fail the test. Finite-field exactness does not convert numerical/complex assertions elsewhere into proofs.',
'Imports NumPy and S37; no external certificate data.')
add('S33','Phase11 separate exact rational/modular controls',
'L6–98 provide integer-field and rational matrix helpers plus a cyclic scan. L100–128 check the polynomially scaled escape and a Sherman–Morrison counterfamily whose inverse is sparse+rank-one. L130–145 verify finite rational inequalities. L148–201 test sparse rigidity, a noncommutative telescoping identity and sandwich expansion.',
'Algorithmic controls reviewed without running this file. A fresh exact rational N4 check independently confirms the important counterfamily: dense inverse, realignment rank 4 and nonconstant response coexist with inverse sparse row degree 2 plus rank 1.',
'The analytic function evaluates finitely many N; it is not a universal proof by enumeration. Many helpers presume nonsingular square matrices and valid roots. Its historical no-submitted-imports statement does not resolve the assignment’s origin classification.',
'Standard-library-only by inspection; output path can be supplied by argv; no supplied program execution occurred.')
add('S34','Polynomial-parameter uniform escape inequality checker',
'L18–56 set O(log N)-description scalar parameters, verify exact rational Neumann/entry/Schmidt/conditioning inequalities and return claimed structural properties. L59–95 construct dense small examples using 80-digit mpmath inverses.',
'Scoped escape construction and exact-versus-bit complexity distinction retained. Returned properties are conclusions of the analytic argument, not values directly measured by exact_gate. No Fourier identity is claimed.',
'The finite list of exact_gate calls alone does not prove the inequalities for every square N. Numeric checks are high precision but not interval certificates, and fixed 80-digit precision is not a uniform arbitrary-N guarantee.',
'Fractions/math in exact path; mpmath only inside numeric_check; script prints exact and numerical records. No current execution.')
add('S35','Exponentially scaled square escape checker',
'L22–55 test rational sufficient inequalities. L58–76 build a weighted-cycle inverse closed form with explicit wrap handling. L79–114 perform precision-scaled dense inverse/residual checks. L117–128 verify integer SWAP realignment identities.',
'Retained as a non-Fourier structural escape and finite verification program. Exponentially small parameters and dense diagnostic matrices do not establish a bit-complexity advantage.',
'Uniform theorem requires the analytic estimates, not merely successful listed assertions. Numerical residual tolerance is not an exact inverse proof. The linear-work application is described rather than implemented here.',
'Uses NumPy, optional mpmath and S37 for SWAP helpers; entry prints records only.')
add('S36','Scalar- and row-weighted permutation Green scan implementations',
'L16–45 decompose permutation cycles and solve each with a prefix accumulation plus backward recurrence. L47–94 build dense diagnostics and seek escape examples. L112–148 repeat the construction with row weights, correctly admitting zeros whenever cycle monodromy !=1. L155–186 add nonconstant-response / full-realignment search filters.',
'Accepted conditional O(N) field-operation apply routines after cycle preparation with nonzero denominators. Bounded seeded searches demonstrate candidates only if they return successfully; they do not construct a DFT.',
'apply assumes matching one-dimensional input length; arithmetic uses fixed field P=65537. Preparation’s scalar inversion cost and exact bit cost are not represented by preparation_ops.',
'Imports NumPy and S37; dense audits allocate arrays and call modular inverses. No program execution.',
'explicit_dense at L56/L63/L152 recreates eye(n) for each of n columns, adding O(N^3) allocation/work to the O(N^2) scan total. The cheap online apply claim remains separate and intact.')
add('S37','Phase11 exact finite-field rigidity and product gate',
'L14–81 implement primitive roots, int64 modular linear algebra and normalized Fourier inversion. L92–116 choose first m Fourier exponents and untouched columns to certify a Vandermonde minor. L119–158 build sparse-plus-low-rank products and compare rank budgets. L161–199 implement realignment/SWAP and dense-inverse Green-sum search.',
'Accepted mathematical gate: rank(F-S)>=floor(N/(s+1)); a product of inverse factors S_i+E_i has sparse row degree <=product d_i and correction rank <=sum r_i. Exact equality requires N<(1+product d_i)(1+sum r_i). This is model-specific.',
'Random factor_audit matrices are not explicitly checked invertible, so they are product-bound controls rather than actual inverse-factor realizations. General APIs require valid bounded residues and dimensions; the stated P and listed sizes keep int64 products safe.',
'Uses NumPy; no direct file output. root only admits divisors of 65536. Dense inverse search is finite and can return failure; it is not a Fourier construction.')
add('S38','Weighted Green escape regression suite',
'L7–21 compare scans with explicit sparse inverse identities and random dense application. L23–29 test weighted escape searches. L31–41 expose the shared constant eigenvector of scalar-weighted permutations, while L43–48 test dense inverse and full realignment rank.',
'Test logic reviewed; no current seeded-search or equality results claimed. Constant-eigenvector reasoning is accepted for scalar-weighted resolvents with alpha!=1.',
'Full inverse support and full Schmidt rank are structural properties only, not an FFT factorization or proof against every sparse-plus-low-rank inverse model.',
'Imports S36/S37 and NumPy; while-loop search for admissible weights is unbounded.')
add('S39','Two-Green sandwich residual checker',
'L11–32 build sparse denominators and expand A F B-A-B entrywise using four Fourier terms. L35–46 compare this expansion with dense products, report rank and call residual zero “full_equality_to_dft.”',
'Accepted identity only with invertible A and B: A(F-A^-1-B^-1)B=A F B-A-B. Without that guard the report is not a valid Green-equality certificate.',
'The direct four-term residual is O(N^2), but assert_sandwich_equivalence additionally performs dense products and modular rank, making that diagnostic O(N^3). Valid permutation/weight dimensions are assumed.',
'Imports NumPy/S37; main obtains nonsingular examples through S36, which protects that particular call path.',
'Public checker does not validate denominator invertibility. Independent counterexample: N2, both pi=identity and all weights=1 gives A=B=0, zero residual and a true equality flag although neither Green inverse exists. Saved valid-domain examples are not thereby disproved.')
add('S40','Phase11 subprocess and evidence orchestration',
'L6–23 run six named scripts/tests with status logs. L24–37 then directly import helpers and repeat analytic, numerical, identity, field-search and sandwich checks into a combined JSON file.',
'Runner reviewed statically; final all-passed text and combined evidence were not produced by this review.',
'No process timeout, sandbox or hash pinning; assertions in children are conditional on normal Python mode. Failure of find_weighted_escape may surface as a missing-key exception in later aggregation.',
'Would execute S31/S32/S34/S35/S38/S39 and import S36; writes multiple logs and EXPLICIT_ESCAPE_RESULTS.json.')
add('S41','Phase12 separation, cyclotomic and lifted-block controls',
'L6–60 provide exact field/permutation, monotone-subsequence and determinant-polynomial helpers. L62–93 test separated 3x3 blocks, a sharp 25-label boundary, small prime/p^2 cyclotomic minors and composite embeddings. L94–121 demonstrate product escape and Schur-complement block-rank equivalence. L122–124 compute stated threshold constants.',
'Scoped exact control source reviewed. Prime/p^2 coefficient grouping is valid for the listed powers. A product escaping a one-layer cut gate is a negative scope control, not a Fourier construction.',
'Cyclotomic helper’s power argument is implemented only for 1 or 2; other powers are unsupported. Threshold arithmetic and sampled degree checks alone do not prove the general external theorem. No execution.',
'Standard library; seeded tests and optional output path; no imports of supplied programs.')
add('S42','Phase13 capacity, hidden-cut and lifted-compatibility controls',
'L42–58 build torus permutations and prefix capacities. L63–88 exhaust small cuts, compare exact spectral constants and find a non-prefix bottleneck missed by all prefix cuts. L89–117 test exact Green off-diagonal ranks, product budgets and a non-Fourier 20-plan candidate. L118–147 build a lifted matrix and verify its Schur-complement rank identity.',
'Retained scope: passing prefix/capacity tests is necessary but not sufficient for Fourier equality; a hidden cut or full compatibility residual can still reject. Exact finite controls are not currently replayed.',
'Spectral/norm/error constants written at L148 are not all derived by executable assertions here. Finite torus side checks are not an all-size expander proof. Global helpers assume nonsingular valid matrices.',
'Standard library; outputs INDEPENDENT_RESULTS.json or an argv destination. No source imports or execution.')
add('S43','Phase14 transverse-fiber and rook-support controls',
'L29–37 construct torus lifts and Green sums. L40–64 check rank-one transverse blocks of polarized products against rank-s Fourier blocks, an exact s-term singular-path decomposition and floating complex Gram identities. L66–81 exhaust t2 capacity cuts, show mixed-axis escape and verify diagonal gauge / rook dimension arithmetic.',
'Accepted structural distinction: a single polarized two-stage path has rank-one transverse blocks; summing s singular paths can recover Fourier, while arbitrary mixed-axis stages need not retain that rank-one gate. No cheap full Fourier algorithm follows.',
'Complex Gram residuals use floating tolerance; exact spectrum claims need algebraic proof. L79 is dimension arithmetic with gauge examples, not a complete proof of generic image dimension or exclusion of a specific target. L84 uses floating sqrt despite the “exact normalization” comment.',
'Standard library only; mixed modular and complex arithmetic is explicit; writes an optional-path JSON report. No execution.')
add('S44','Phase15 symmetry and occurrence-charged perturbation controls',
'L31–39 construct commuting torus maps, involutive half-shifts and weighted Green matrices. L42–66 test centralizer identities, orbit exponents, modular Gram polynomials and group projections. L70–83 perturb solver occurrences, test rank/commutator bounds and exhibit rank two after reusing one edited parameter twice.',
'Accepted model-level distinction: rank perturbation is charged per solver occurrence; repeated reuse of one parameter need not cost rank one globally. Resolvent commutator identity is algebraic under nonsingularity. Finite spectra were not rerun.',
'Modular Gram identities by themselves do not establish complex singular values, norm gaps or characteristic-zero rank. The orbit formulas provide a separate route but need an analytic argument for all sizes. Singular random denominators are not resampled in every path.',
'Standard library; writes result JSON; no supplied imports. No execution.')
add('S45','Manifest integrity verifier',
'L6–15 hash the manifest and every listed file, comparing lengths and digests. L16–17 demand exact agreement with the directory’s set of regular-file paths, apart from the two seal files.',
'Integrity utility only. Byte/hash closure is useful but does not establish semantic review, authorship, execution or authenticity against an adversary able to replace both manifest and digest.',
'Immutable-by-convention is the appropriate term. Assertions disappear under -O; paths and symlink behavior are trusted and duplicate manifest entries are not explicitly rejected. An externally retained digest is needed to detect coordinated rewriting.',
'Standard library; reads local manifest and files, prints PASS; no modification. This supplied verifier was not executed.')

assert len(notes)==45
rows=[]
for r in provenance['rows']:
    b=(P/r['snapshot_path']).read_bytes()
    assert hashlib.sha256(b).hexdigest()==r['sha256'] and len(b)==r['size_bytes']
    count=len(b.decode('utf-8').splitlines())
    rows.append({'review_id':r['review_id'],'sha256':r['sha256'],'size_bytes':len(b),'line_count':count,'representative_path':r['representative_path'],'snapshot_path':r['snapshot_path'],'full_static_inspection':True,'static_inspection_complete':True,'source_executed_in_review':False,'source_imported_in_review':False,'source_compiled_in_review':False,'source_ast_parsed_in_review':False,'coverage_basis':'Entire exact-byte UTF-8 source read as text and analyzed, not an AST or basename reconciliation.','reviewed_line_intervals':[[1,count]],'prior_coverage_present_in_snapshot':r['prior_coverage_present'],'origin_class_preserved':r['origin_class'],'origin_basis_preserved':r['origin_basis'],**notes[r['review_id']]})
review={'package':'green_geometry_source_review_0430','review_date':'2026-10-10','status':'45 of 45 assigned hashes fully statically reviewed','assigned_unique_hashes':45,'source_bytes':sum(r['size_bytes']for r in rows),'source_lines':sum(r['line_count']for r in rows),'prior_registry_snapshot_overlap':0,'additive_full_static_reads_against_snapshot':45,'source_execution_import_compile_AST_parse':'None','fresh_independent_check_program':'reviewer_checks.py','fresh_independent_result':'INDEPENDENT_CHECKS.json','central_registry_modified':False,'prior_artifacts_modified':False,'authorship_note':'Static roles and self-descriptions do not override the preserved inventory origin classes.','rows':rows}
(P/'SOURCE_REVIEW.json').write_text(json.dumps(review,indent=2)+'\n')
print('Wrote full per-hash review:',len(rows),'hashes,',review['source_bytes'],'bytes,',review['source_lines'],'lines')
