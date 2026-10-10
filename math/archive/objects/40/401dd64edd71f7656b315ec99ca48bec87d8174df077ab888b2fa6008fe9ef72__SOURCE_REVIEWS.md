# Per-source inert inspection

All 46 exact hashes were read from first to last; no supplied source was run, imported, compiled or AST-parsed.

## S00 — adapter.py
- SHA-256: `35bdb1c4f216ba6f6a537188cb083b72ba4d5148f847dc34b4fbee18d5755f6c`
- Scope: lines 1–50, 2235 bytes; Sparse metadata FFT adapter
L13–31 trusts the supplied base spectrum and edit validity, and returns the linear sparse update; this is conditional metadata reuse, not discovery or arbitrary-input complexity. Direct mode reduces indices modulo n without validating nonempty one-dimensional input. L34–44 validates compact length and real edit amplitudes but computes a full sparse DFT before slicing, so it does not itself achieve selected-bin work. NumPy and exact archived adaptive_fft/hybrid_sparse dependencies must be matched; no execution.

No standalone result producer in this source. Associated archive evidence is historical, not a fresh correctness/execution certificate.

## S01 — adapter.py
- SHA-256: `586e5e5bf01946658f9b086421bab0a27af879be13c9f7aff0241c55ca68a386`
- Scope: lines 1–66, 3147 bytes; Extended lazy metadata adapter
L14–50 retains source 00's conditional sparse update behavior, while L52–65 constructs LazySpectrum, BufferedSpectrum and PreparedBinView from trusted metadata. These are wrappers, with dependency-owned validation, storage and cost. Preparation, reconstruction and flush costs cannot be omitted from speedup claims. Distinct byte hash adds lazy_spectrum dependency and is not interchangeable with source 00.

No standalone result producer in this source. Associated archive evidence is historical, not a fresh correctness/execution certificate.

## S02 — adaptive_fft.py
- SHA-256: `a1094fc0d69c382e5dd5b3f22899f2fb7860e88a73a66a029a44e8a3db57077d`
- Scope: lines 1–664, 27811 bytes; Adaptive real FFT cache and rank reuse engine
L24–45 validates finite real inputs; exact byte verification at L328–333 protects against fingerprint collision, but rank reuse at L113–115,142,159 is tolerance-based, not exact algebraic equality. Accepted coordinate errors can accumulate in Fourier outputs; cyclic/sparse phase cumproducts L250–262 accumulate numerical error. L277–313 bounds cached arrays but auxiliary frequency/sample caches and object overhead are outside cache_bytes. L543–565 has a concrete dependent-basis registration defect: fft_family(register=True) accepts two dependent rows; _make_span reduces to rank one but span.spectra receives both original spectra, so later one-coefficient multiplication has inconsistent shapes. L609–664 counts canonical DAG butterflies but builds every input tree and returns spectrum copies; counts omit hashing, discovery, memory and copies. Known-family speedups require supplied coefficients; no general FFT complexity improvement or novelty proof.

No standalone result producer in this source. Associated archive evidence is historical, not a fresh correctness/execution certificate.

## S03 — adaptive_fft_cpp.cpp
- SHA-256: `9b04f886385c7bb5e48d352ca9dec2b77ecbb03de9851d4f1acacd6309e01ac7`
- Scope: lines 1–306, 16318 bytes; C++ FFTW adaptive benchmark
L77–91 reads double storage through uint64_t pointers, a C++ strict-aliasing portability defect; as_bits instead uses memcpy safely. L52–67 reuses FFTW plans on new input/output arrays without explicitly checking new-array alignment compatibility or using FFTW_UNALIGNED. Requires C++20 rotl, FFTW ABI/linkage and nonstandard M_PI availability. Rank detection L214–238 uses tolerance, discards sufficiently small rows, and applies an absolute determinant guard after ignoring its computed scale. Finite tests cover only sizes 64/1024/4096 and one reconstructed rank row. L285 seeds structural references outside elapsed timing, but accumulated component timings include the seed; rep==2 components are not necessarily the median-total repetition. Cache limits count references, not total bytes. No supplied compilation or execution.

Archived C++ stdout and cpp_benchmark_results.json record TESTS PASSED/timings for the finite grids. Component timers are not an additive decomposition of the median elapsed run: seed setup and a fixed repetition are mixed. No recompilation, timing reproduction or portable ABI validation.

## S04 — additions/0155_material_coverage_and_new_results/constructions/compressed_retained_inverse/verify_compressed_schur.py
- SHA-256: `7876e93d5cafc2ab81ccc72a1e0987c24aba95e9955ccd5be68d3a61502ab3ef`
- Scope: lines 1–236, 9622 bytes; Finite-horizon compressed retained Schur checker
L33–51 compresses routes in a fixed finite field; root checks are specialized to power-of-two fixtures, not arbitrary orders. L89–132 prepares phase/route tables and explicitly charges r*d*(d+1)/2 routed visits, but this count is not all runtime or preprocessing. L170–227 checks N=2..128, all retained basis vectors for compressed equality, and specific polynomial/inverse/global-recovery inputs; rank results are measured only through N=64. The marker in L205–207 is recorded without independent expected-value comparison; recovery L215–223 uses full N-vectors and does not establish compressed global FFT work. L228–232 explicitly exhibits failure beyond H=log2 N. No all-N theorem or global FFT speedup follows from finite fixture assertions.

COMPRESSED_SCHUR_CONTROLS.json contains28 basis parameter sets/247 basis vectors,28 inverse/recovery sets and56 support cases. Fresh literal path enumeration confirms its N16,b2,H5 failure vector [0,57313,0,510], different from the naive zero vector.

## S05 — additions/0155_material_coverage_and_new_results/constructions/five_point_exact_three/check_three_green.py
- SHA-256: `69dc09adada160d752859125ef187d59e1399903073672b6debb9b779c233664`
- Scope: lines 1–171, 7791 bytes; Exact five-point three-Green certificate producer
Implements rational arithmetic in Q(zeta5) and a separable quadratic algebra with norm-guarded inversion. L101–150 checks full 5x5 target and two weighted-cycle inverse formulas symbolically if executed; L153–167 uses reduction mod 241 and a nonsquare discriminant to support irreducibility and records nonzero endpoint/pole guards. This is a fixed N=5 construction in an extension field, not an unbounded FFT family or complete input/output complexity analysis. All arithmetic/assertions and JSON output execute at import/top level; source was kept inert. Stored PASS is historical evidence, not a fresh execution or authorship determination.

Exact result data reports25 target entries and50+50 inverse checks. Fresh reviewer arithmetic verifies its serialized N5 decomposition and forced inverse after all four primitive zeta5 reductions modulo241, plus the nonsquare discriminant. This bounded specialization is not a new full characteristic-zero execution.

## S06 — additions/0155_material_coverage_and_new_results/constructions/five_point_exact_three/verify_seal.py
- SHA-256: `be88a810ccffe530147a3c3d065fe94bb40352b22e2f8eb9e0bce2bcc4e085d1`
- Scope: lines 1–17, 924 bytes; Exact-three package seal verifier
L7–13 hashes the declared manifest and files; L14–16 additionally checks exact local file membership except pycache/manifest files. This is byte integrity, not mathematical correctness or execution reproduction. Manifest-controlled relative names lack an explicit path-containment check. Top-level asserts would disappear under optimized Python; no source was executed here.

Same exact seal-verifier hash occurs in multiple unrelated construction folders. All relevant standalone contexts are preserved; a seal PASS or shared checker hash must not merge their mathematical scope. Copied predecessor manifests retain old relative paths, so unresolved references are recorded rather than assumed missing current artifacts.

## S07 — additions/0155_material_coverage_and_new_results/constructions/five_point_fourier_reconstruction/check_fourier_reconstruction.py
- SHA-256: `640c30dc2d90eee391430f97b0c645a91d2a7000678267cd4d061e912c5677bc`
- Scope: lines 1–169, 7487 bytes; Five-point Fourier reconstruction checker
L118–123 reads an external certificate and sets the quadratic arithmetic from its coefficients; dependency is data, not an imported checker. L128–136 verifies full 5x5 algebraic identities, including the cubic closure and three-B reconstruction. L139–166 applies two cyclic Green scans per B and compares all five basis vectors plus two extra vectors, with six nontrivial Green solves per fixed transform. The result explicitly limits scope to N=5; counts do not include root/field construction, arbitrary-length recursion, or a speedup proof. Top-level parsing/read/check/write would execute on import, so source was kept inert.

source/CERTIFICATE_INPUT.json is byte-identical to source05's result a95e7fadaebcb91b11f86cf4336b9ca0b0ba745e6cc3212c05ae501daeddd205. Stored reconstruction counts are21 B calls/42 Green solves/14 A applications across7 inputs, i.e.3 B and6 Green solves per transform. Scope remains fixed N5.

## S08 — additions/0155_material_coverage_and_new_results/constructions/fourier_shear_lift/check_fourier_shear_lift.py
- SHA-256: `a63cfbf715ab8c4860e1c90b69eb31a3fcfba7133b1ca032a42880d32d032f9a`
- Scope: lines 1–261, 10360 bytes; Fourier two-shear lift finite control
L159–215 checks two primes, N=4..64, three signed-cycle routes and two poles; it distinguishes raw Fourier sector ranks from parity-shuffled recursive factors and explicitly detects n-dependent off-diagonal obstructions. L110–156 embeds two recursive half-size calls in a shear escape, so the construction retains FFT-like recursion. L216–253 validates seeded vectors through N=256 and selected nondyadic Bluestein reductions, charging all three transforms including kernel spectrum. Arithmetic ledger is a declared model, not literal Python cost: repeated pow/root generation, modular inverse, indexing/allocation and integer bit complexity are not represented. Stored finite PASS does not by itself establish the separate uniform proof, and the source explicitly claims no asymptotic speedup.

Stored EXACT_RESULTS.json self-binds checker_sha256 to assigned a63cfbf7… and has60 matrix fixtures,18 dyadic vector fixtures and9 nondyadic fixtures. Reviewer checks confirm declared arithmetic formulas for all16 N>=2 vector rows, not literal Python operation or bit counts.

## S09 — additions/0155_material_coverage_and_new_results/constructions/global_crt_lift/check_global_lift.py
- SHA-256: `8a3abeff3a3ddc550d336454087f8623cdd6a23f17b95983241b06e0df718436`
- Scope: lines 1–305, 16251 bytes; Global CRT lift and restricted pole-bank obstruction checker
L110–155 expands universal polynomial identities over integer polynomials, reduces a rational pole trace to degree 5/5 over Q(zeta5), and obtains a degree-eight squarefree exceptional guard. This bounds exceptions of the specific parametrization; it is not a general Green decomposition exclusion. L230–279 verifies CRT entries/cut ranks at four stated finite fixtures; two-sided inverse and spectral recursion are enabled only for N=15,45, not 65,245. L281–295 supplies a Q(zeta15) two-sided inverse and different-block trace witness. Spectral projectors use three cubic roots and recurse on m-sized kernels, leaving their work explicit. The output correctly restricts the obstruction to one reciprocal pair per block, not arbitrary global Green sums. No supplied execution; finite results must be distinguished from symbolic deductions and global complexity.

Stored finite controls N15/45 include full two-sided inverses and spectral projectors; N65/245 explicitly set full_two_sided_inverse=false. N65 has12 trace-only blocks rather than endpoint constructions. Distinct pole trace counts do not imply an obstruction to unrestricted global Green sums.

## S10 — additions/0155_material_coverage_and_new_results/constructions/restricted_infinite_three_family/verify_seal.py
- SHA-256: `de24c15df8f8dae9fd305e41121a25ca29a6dc88544de5d5fa8da275e80c37a2`
- Scope: lines 1–14, 592 bytes; Restricted-family seal verifier
L5–13 verifies manifest bytes and each listed file's size/hash. Unlike source 06 it does not reject extra unlisted files. Integrity assertions do not establish algebraic correctness, source execution or completeness of dependencies; manifest-controlled paths are not explicitly confined to the root. Top-level execution was not performed.

The restricted infinite-family seal checks listed files only. No mathematical verification can be transferred from this14-line hash checker to the much larger extension checker not assigned in this batch.

## S11 — additions/0155_material_coverage_and_new_results/prior_artifact_components/4aa292c45b5484db__verify.py
- SHA-256: `4aa292c45b5484dbcac788731f3280407420fb6b0ef4de0317deea2e52a1c971`
- Scope: lines 1–599, 23878 bytes; Annihilator-closed Fourier feedback exact audit
L118–156 gives conditional polynomial inversion requiring a valid nonresonant annihilator. L178–267 implements linear Green scans and paired Horner evaluation with separately instrumented field-operation counts, explicitly excluding parameter synthesis. L305–335 derives A,B from a dense Fourier oracle, so passing those controls is not a cheap factorization. L404–427 verifies polynomial action of random pairs without claiming their polynomial is an annihilator. L452–539 separates finite Krylov rank samples from a Vandermonde witness for generic degree N; neither excludes specially designed low-degree families. L542–562 tests a restricted denominator support obstruction, not arbitrary endpoint-scaled Green sums. Nine finite test groups and stored statuses remain historical; no universal fast FFT construction is implemented or executed.

RESULTS.json records nine groups:36 dense-oracle Fourier cases,40 negative certificates,28 Green plans,96 polynomial-kernel vectors,40 finite full-degree Krylov witnesses,24 restricted feedback obstructions,32 residual/rank cases and10 generic degree witnesses. These counts agree with source loops and preserve conditional construction versus oracle controls.

## S12 — additions/0155_material_coverage_and_new_results/recovered_originals/8cf2a04fa6bc4551__fourier_compatibility_gate.py
- SHA-256: `8cf2a04fa6bc4551da137f97ea41c23fdaabc95b56d93ba890a9315257e8e7ae`
- Scope: lines 1–162, 6493 bytes; Nonlinear Fourier compatibility necessary-condition gate
For the external affine layout at N=256, L20–26 establishes boundary counts 3 and 13; L111–152 checks selected Fourier/control submatrices modulo 12289 and 65537 and a synthetic four-factor cancellation. The rank<=16 condition is necessary and nonlinear in outer inverse coefficients, not a solved feasibility system or impossibility theorem. Identity and random unitriangular outer inverses having rank 128 only reject those choices. rank_and_det_mod L43–45 returns a partial rank immediately on a missing pivot in a square matrix, although later columns may raise actual rank; determinant zero is still correct and the current successful full-rank minor case avoids this defect. NumPy int64 is safe for stated fixture products, not arbitrary p/N. Depends on verify_exact.affine and AFFINE_LAYOUT.json with exact occurrence identity required.

Stored N256 gate data gives boundary ranks3+13, middle rank16, outer-Fourier rank128 and nonzero17-minor determinants8799/20067 over12289/65537. It certifies nontrivial necessary equations and rejects named outer choices, not all possible outer inverse stages.

## S13 — algebra_fft.py
- SHA-256: `7d933dd7cc53a986d8e57686e3a19883f349278a0e9a75fd8eee4e702b565b8c`
- Scope: lines 1–821, 35244 bytes; Canonical convolution DAG and prepared polynomial jets
L46–262 interns sums/products modulo its limited associative/commutative grammar using float coefficients, not general polynomial equality or exact real arithmetic. Seeds and their FFTs are stored permanently; only derived spectrum cache L354–394 is bounded, and local memo can retain all reachable spectra. Imported spectra/Phase-7 objects L128–183 are explicitly trusted rather than certified. L474–624 builds degree-capped polynomial jets; preparation, seed FFTs, inverse kernels and k^h sparse edit expansion are real costs, and repeated squaring/flattening can grow the DAG. Selected queries cast index arrays to int64 without rejecting fractional inputs; single_frequency L786–793 similarly truncates t,k. PreparedEdit is frozen only structurally: frequency coefficient arrays and sparse dictionaries remain externally mutable. Forced shifts can enumerate exponentially many edit tuples; spectral fallback produces the full output before slicing. Exact algebraic identities are conditional on valid metadata/ring operations, whereas numerical evaluation is float64. No arbitrary-DFT complexity improvement.

Archive compiler tests and benchmarks are historical package-level claims and do not negate static mutability/index-validation limits. Associated SHA256SUMS.json is byte-reconciled; no JIT or interpreter ran here.

## S14 — analytic_certificate.py
- SHA-256: `67fd421ba9368d4b477a2d17c0343296d56322791b3e76d0bc472f82417142be`
- Scope: lines 1–95, 3764 bytes; N8 exact rank and cyclotomic determinant certificates
L57–73 enumerates all 56x56 3-by-5 Fourier submatrices over two primes and validates parity-order cuts; nonzero modular minors can witness corresponding characteristic-zero nonvanishing when the root specialization is valid. L74–78 checks the balanced 4x4 determinants exactly in Z[z]/(z^4+1), while other cut dimensions already bound ranks. L79–91 is only small-sign trinomial sampling, capped at N=32, not the characteristic-zero induction itself. Separate RESEARCH.md is needed for the all-dyadic three-term theorem. No supplied execution or novelty conclusion.

Stored analytic_certificates payload reports3136 rank-three3x5 matrices per prime, zero balanced cyclotomic determinants, and102 N32 trinomial samples. The sampling loop's cap can end at102 because it admits a complete three-sign batch; it is not all N32 supports.

## S15 — arbitrary_output.py
- SHA-256: `b0f64933f147d6b62ac69b0d2fe441b4469f2bf66e8d042e2636aa7238b2c8b0`
- Scope: lines 1–307, 13892 bytes; Arbitrary-bin classical output-pruned DFT planner
L99–135 implements the stated Cooley–Tukey split and q-by-M phase contraction; O(N log q) relies on a divisor K near q and does not uniformly follow at prime N. Memory budgets count phase bytes but omit indices, temporaries and coexistence of candidates. The no-sample path L169–175 still constructs a plan when none fits the budget, and can construct a discarded pruned plan. project_stream_with_sample L217–224 silently reuses the constructor sample_result even when its new sample argument differs, producing a stale first projection unless the caller enforces equality. productive_radices L247 returns at least one radix even for limit=0, defeating the planner's zero-trial intent. All bin/radix integer casts permit truncation; auto rejects q>N even if bins are valid duplicates. Timings are empirical and do not certify correctness or global optimality.

No standalone result producer in this source. Associated archive evidence is historical, not a fresh correctness/execution certificate.

## S16 — audit.py
- SHA-256: `b02c767b41d59d29771cc1efcb7768408d4f8b543880b73852baae016fd84328`
- Scope: lines 1–125, 6046 bytes; Boolean completion audit driver
L64–76 checks idempotence/recovery exhaustively only at N=8 and on 32 generated inputs at larger sizes; singular recovery cases are separately counted. L77–92 requests degree<=3 conjugate-pair noncompletion rank certificates and independently checks their supplied witness minor modulo one prime, relying on graded_certificate's exact construction/lift semantics. L93–103 verifies the N8 single-omitted-bin cubic identity on all 256 inputs over Q(zeta8), while explicitly observing that ordinary conjugation already recovers that bin for real inputs. L104–114 gives an actual 2^(N/2)-input ambiguity family for even bins. These restrictions do not prove a general FFT lower bound or speedup. Imports exact spectral_boolean and graded_certificate versions; no execution here.

Stored audit reports70 balanced singular cases among all256 N8 inputs, pair-omission determinant witnesses atN8/16/32 and exact single-bin cubic verification. The one-bin positive identity is not a computational improvement over real-input conjugacy.

## S17 — auto_dispatch.py
- SHA-256: `c3880ca0bde44e120723a7a3981148896113ce91713d4a62074772fecde28b8f`
- Scope: lines 1–88, 4440 bytes; Cold-JIT-aware heuristic dispatcher
L40–68 checks expected reuse and an array-memory estimate before compiling, then L69–88 times NumPy followed by JIT on six fixed updates and charges planning time to breakeven. It tests only output finiteness, not equality; timings are ordered/noisy and specific to optional output_bins. compile_prepared may allocate/compile both full and partial kernels, beyond the simplistic data-byte budget. Selected backend remains fixed if later queries use a different output shape. Reuse can justify empirical savings but not guaranteed optimality or asymptotic improvement; compilation dependency inspected separately, not invoked.

No standalone result producer in this source. Associated archive evidence is historical, not a fresh correctness/execution certificate.

## S18 — barrier_audit.py
- SHA-256: `a5b66df0c43c329a85b52d5f357a5adf125f477a2e415f5a6f28e4b159127101`
- Scope: lines 1–39, 1301 bytes; Binary bounded-annihilator counting demonstration
L7–25 evaluates lower-triangular binary convolution with constant coefficient one and exhaustively checks all eight degree<=3 filters on 256 arrays, consistent with unit-diagonal bijectivity. L28–35 checks one seeded n=1024 input against 256 degree<=8 filters and reports union Hoeffding 2^d exp(-n/18). The theorem depends on uniformly random bits and a union bound; the demonstration is not all inputs/fields or unrestricted annihilators. No source execution.

No standalone result producer in this source. Associated archive evidence is historical, not a fresh correctness/execution certificate.

## S19 — benchmark.py
- SHA-256: `ce55de696191cfae81144c0f1a7b92dd7390d8bf7b67e458e169d8f58b6c3ed5`
- Scope: lines 1–34, 1697 bytes; Sparse-factorization timing driver
Top-level loops test three sizes and six support sizes, five timing repetitions, and allclose to SciPy/NumPy full FFT. Inputs are sparse metadata already prepared; metadata discovery and construction of the dense reference vector lie outside timings. It counts classical butterflies from dependency plan metadata rather than all operation/memory costs. Fixed working-directory JSON writes would occur on import. No fresh timing or execution claim.

Matching historical sparse benchmark data has18 rows for the3x6 grid. Existing timing ratios are machine-specific and can be below1 despite fewer classical butterflies; no new measurements were made.

## S20 — benchmark_buffered.py
- SHA-256: `c3d795227f834f18149c4704ead8c703b68e4365ebfa78c8e89e1039c6568e20`
- Scope: lines 1–62, 2493 bytes; Buffered streaming threshold benchmark
Top-level driver times each fresh/lazy/threshold candidate exactly once, then selects the minimum on the same workload; this is in-sample tuning with no uncertainty estimate. Initial FFT and copy are inside timing. Only the final query is compared against truth, and only the winning buffered threshold is checked; errors at earlier queries/nonwinning candidates can escape. Source depends on lazy_spectrum exact version. Performance scope is two sizes, 512 known edits, 64 bins and three query cadences, not arbitrary transforms.

Stored buffered results have six2x3 workload rows. Winner thresholds are chosen in-sample from single timings; for N262144,H64 buffered_vs_never is about0.543, so the selected buffered strategy can lose to never-flush on that workload.

## S21 — benchmark_key_results.py
- SHA-256: `c75e44c9392ed9fc1ccf62a9f8e7db1b3850bb0a9f440daf5162c9b1fb74968f`
- Scope: lines 1–65, 3561 bytes; Selected prepared/lazy benchmark scenarios
L17–36 compares full FFT per update, full phase-table eager update and selective PreparedBinView including setup in median-of-three timings, for one fixed workload. Correctness checks only final results. L37–55 fixes buffered threshold 128 rather than independently tuning it. L56–63 compares two partial-query methods after basis FFTs and metadata were constructed outside timings, so the headline low-rank speedup excludes registration. All scenarios reuse trusted edits/bases and cannot support an ordinary FFT complexity claim. Top-level JSON writes were kept inert.

Stored selected-view result contains three scenarios, including384.57x versus fresh FFT and402.60x low-rank partial-query ratios. These use selective/metadata-aware workloads; the latter excludes basis FFT preparation, so neither is an arbitrary full FFT speedup.

## S22 — benchmark_lazy.py
- SHA-256: `80a756fa963096e766ebc5ae5d7379e1c9cf1ea3e152229b8fc2d521dd49efa4`
- Scope: lines 1–159, 5887 bytes; Deferred spectrum benchmark
L29–116 includes initial FFT/setup for fixed-location and partial-then-dense streams, but validates only the final output or final dense flush, not every intermediate partial query. The comment says every 10 edits while the actual cadence is 16. L119–134 compares three dense correction methods after sparse vector/metadata construction. L137–156 computes basis FFTs outside the low-rank timing, contradicting the unconditional header statement that all methods pay initial FFT. Repetitions are three, not statistical performance guarantees. All source remains inert.

The shared benchmark_lazy_results.json contains18 rows with200/128 updates and2x5 crossover cases. These are incompatible with this full source's default500/256 updates and3x11 grid (41 expected rows). Do not credit this stored result as a run of source22.

## S23 — benchmark_lazy_quick.py
- SHA-256: `af49f72866a8ab265534a1d78f60bbd8f881e459f0dbdcb364f25a8680ef49a9`
- Scope: lines 1–159, 5861 bytes; Quick deferred spectrum benchmark variant
Fully read distinct byte variant: A uses 200 updates, B 128 updates, crossover grid shrinks to two sizes and five supports, and every timed call explicitly uses one repetition despite the helper default of three. It retains source 22's excluded low-rank registration costs and final-only checks. Both variants write the same benchmark_lazy_results.json basename, so a stored result requires configuration/hash reconciliation and cannot be assigned from filename alone.

The same18-row stored benchmark_lazy_results.json matches the quick variant's200/128 updates and2x5 crossover grid. This is configuration consistency, not proof of execution against an identified environment or stronger-than-single-run performance evidence.

## S24 — benchmark_prepared.py
- SHA-256: `400050659b7c7a1168210650b9f959f19e6b5f1d5a05e31ed93c82864fabe92e`
- Scope: lines 1–43, 2028 bytes; Prepared single-location update benchmark
L23–35 charges initial rFFT and phase construction for the prepared path, and compares forty updated rFFTs in baseline; input copy is outside each timing. Three repetitions/four sizes and final-only allclose assess one fixed-support streaming workload. The code explicitly distinguishes the structured application from algorithm #130. Depends on SciPy without fallback and prepared_update exact hash. No fresh benchmark execution.

Historical prepared-point file has four rows at prescribed sizes with40 updates and includes initial spectrum/phase preparation. Ratios roughly4.58–10.72x apply to the structured repeated known-location workload; final-only error checks remain a coverage limitation.

## S25 — benchmark_prepared_bins.py
- SHA-256: `18d505efca0b5692ead55d29ec812b0aa1fd5ab0e0bc673efbd7a0f594c0e916`
- Scope: lines 1–71, 2713 bytes; Prepared selective-bin streaming benchmark
Single timing per method at three sizes includes initial FFT and phase/view setup; evaluates 500 supplied updates on 32 known editable positions with 64 selected bins. L58–64 checks only final outputs. Reported memory reduction compares phase tables alone, omitting source spectrum, update state and temporary memory. Avoiding unrequested outputs explains much of the possible gain; no arbitrary full-transform improvement is established.

Stored three-row selective-bin results agree with500 updates,32 support positions and64 bins. Phase-memory ratios alone do not bound total process memory.

## S26 — benchmark_view_optimizer.py
- SHA-256: `fadf85c032c1b12716fc60d29faa00b765b58260dbf53d628be03e6610caba96`
- Scope: lines 1–134, 5692 bytes; Multi-view optimizer benchmark
L33–48 constructs random projected basis entries directly, explicitly excluding Fourier registration; this measures replay/grouping, not transforms. Timed run_one includes setup and the generated operation schedule. L89–103 compares sequential, known-batch oracle and inferred grouping, including periodic compaction. Only the real part of the first output per query enters checksum, and L121–122 merely reports checksum differences without asserting equality; errors in other entries or cancellations can be hidden. Five repeated medians on four fixed scenarios cannot establish universal planner performance.

Stored organizer result has sync/two_clusters/async/shift scenarios and zero scalar checksum differences, but that checksum does not validate all bins. The same driver hash appears with two different multi_view and view_optimizer dependency hashes across archives, so driver identity cannot unify execution closures.

## S27 — boolean_overlap.py
- SHA-256: `763804fe7fc399d0acff48060f8cb5927a223089b0671a17fc28ec90834353e7`
- Scope: lines 1–246, 9567 bytes; Boolean one-hot linear extraction circuit
L71–112 propagates constant/singleton Boolean coefficients, correctly including the overlap product da*db, with an explicitly labeled dictionary-work proxy. L114–154 produces only constant-input multiplication gates and preserves shared upstream linear components while separately charging metadata preparation. A valid projection agrees at 0 and e_i but need not equal a general nonlinear Boolean function; its equality to Fourier requires that original behavior on Boolean inputs is established. L171–207 assumes the hardcoded primitive generator is valid for the chosen modulus but does not primality/order-test arbitrary p. Finite tests N=4..64 are illustrative, not a general circuit-size lower bound or fast FFT. Node indices and externally passed audit objects are trusted.

Stored Boolean-overlap audit has20 rows (five sizes times four variants). Preparation-work proxy and projected-gate count are separate; the projected circuit's field-domain validity is conditional on the input Boolean Fourier identities.

## S28 — bounded_printer_selector_demo.py
- SHA-256: `a1ae19511b456154ef4064a248819dc7f198796201c7cd1db7f33d3ea558c78a`
- Scope: lines 1–68, 1909 bytes; Bounded-printer selector toy
L16–25 invents six finite records with adversarial print and conditioning costs. L34–43 filters by print_steps<=k, m²<=k and khat<=R, then selects the last eligible record, relying on list order. It never prints an actual transform or verifies condition estimates; astronomical N is represented by k only. No assertions or exhaustive selector correctness checks are made. Its stated limitation that this is not the Fourier theorem is essential.

Stored six selector rows match the toy parameters and select record4 only by p=70000. No actual astronomical transform or coefficient printer was executed in this program.

## S29 — check_certificate.py
- SHA-256: `2cef1e2f17f2baddbfc412c025dd9f0d2b06a9c1544be306dcea4faf71365238`
- Scope: lines 1–129, 5984 bytes; Bounded exact network/exponent certificate
L17–69 computes the h=24 candidate, exhausts 4,096,576 triple pairs for RG+JV=I, and uses rational Taylor/log inequalities for the stated exponent margin. The saving is conditional on transferring the source's nested-label lemma and the full arbitrary-register/network recurrence, not established by local arithmetic alone. L91–118 performs useful formal noncommutative eight-row restoration and signed bank exchange checks; L119–127 adds pointwise scalar/shear charges that must not be confused with a free global replacement. Generic odd-q scan rows are explicitly candidates until rank/residual premises are justified. Pinned-source provenance and novelty beyond it remain separate; no Lean proof, astronomical network or supplied checker execution occurred.

No certificate_results.json was present in the chosen exact-hash archive context. Fresh reviewer arithmetic independently agrees with the stated h24/W/Delta/padding constants and rational local exponent inequality; this does not establish absent global premises.

## S30 — check_cyclic_rational_fusion.py
- SHA-256: `e2d19ebaf6600394a42d75e848a8de00e3929ff73e5770c88997d59bb80583aa`
- Scope: lines 1–88, 3846 bytes; Cyclic rational sample correction checker
L45–83 uses exact F97 arithmetic for 960 finite fixtures, including resonant poles. L59–63 verifies the numerator correction modulo the annihilator; L69–75 explicitly supplies the removable singular value b*S at resonance. Uncorrected pole-free samples decode an aliased weighted target, not the desired sequence. Direct quadratic sums are oracles, not fast transforms, and fixed field/root fixture restrictions matter. No execution here.

Stored960 cases split into760 pole-free and200 resonant cases, with384 resonant values and758 uncorrected-target mismatches. Fresh reviewer confirms fixture count only; no supplied replay.

## S31 — check_decoded_tree.py
- SHA-256: `6e3b7a0e9f2dd98d4d3bed6edabaac9818cee6816fe961ebc083e8d46aaea86f`
- Scope: lines 1–44, 2012 bytes; Decoded recurrence subtree fusion checker
Imports P/root/mul from an exact sibling checker; source identity alone does not prove that sibling import closure. L11–15 extends a length-L recurrence state using truncated product/inverse, then L19–38 repeatedly deinterleaves while roots square and may collide. Checks three periods, k<=8, depths0..4, three trials; dense reference sequence generation and naive multiplication are fully present. Algebraic fusion correctness of those fixtures does not eliminate recurrence/convolution work or prove a faster FFT.

Stored360 cases/1872 branch nodes/11997 output coefficients. Fixture count independently matches three periods,eight k values,five depths,three repetitions; other outputs remain historical claims.

## S32 — check_displacement.py
- SHA-256: `09578b2c89e4f0b89b8bc62dd4e1bb37d9fbb446b6d7555d90262115b1719892`
- Scope: lines 1–44, 1937 bytes; Cyclic Vandermonde displacement rank checker
For prime periods 5,7,11, exhausts nonempty nontrivial-root subsets, B<N and t<=B. L30–36 validates a wrapped-row defect and rank min(t,support), relying on z^B!=1 and distinct nodes. The root selection is safe for these prime N fixtures but is not a general primitive-root algorithm. Finite algebraic rank is not a runtime lower bound, and full-read coverage does not imply supplied execution.

Stored57738 cases split150/1323/56265. Reviewer independently verifies counts from the exhaustive subset/B/t grid; the rank theorem and finite correctness are distinct from runtime lower bounds.

## S33 — check_fixed_bridge.py
- SHA-256: `054699949c7ecc3d7fc5d94501f2e5957f90a86bb0f50650568f722453012688`
- Scope: lines 1–203, 8931 bytes; Integer fixed-point bridge and posterior-bound experiment
L9–123 implements fixed-point source/target solves and exact rational residual calculations. Root generation returns an asserted formula rho=8N/Q; its adequacy is numerically tested with mpmath, not interval-certified for all inputs/lengths here. L143–150 deliberately substitutes a direct high-precision DFT decoder oracle and injected error, so the program does not implement the claimed packed O(N) decoder. Final error checks and isolated conjugacy oracle use mpmath100-digit numerical values, while source residual checks use exact rational tridiagonal solves. The linear-work claim remains conditional on external packed-decoder/root-error theory and bit complexity; stored numerical PASS is not a formal global stability proof.

Stored33 bridge checks comprise15 random,5 structured,12 isolated target and1 zero control, matching source loops. Direct-DFT decoder oracle and high-precision numerical comparison remain explicit, so these do not evidence a packed linear-time implementation.

## S34 — check_fusion.py
- SHA-256: `30311ecc63733f2bedaff12ac3f87d68ec61e51656711b0e585c53760da61a0f`
- Scope: lines 1–133, 4690 bytes; Decoded BM fusion and convolution-embedding checker
Full top-level finite audit covers twelve divisors of96, random sparse root sets, three state-length choices, root collisions, one/macro steps, BM parity intertwining and full reconstruction. L104–115 checks Vandermonde action as transposed polynomial remainder; L117–128 embeds arbitrary convolution in a generic recurrence-extension operator. This supports an obstruction to treating the generic operator as free, not an unconditional FFT lower bound in a root-restricted model. All polynomial/oracle arithmetic is naive, and top-level JSON/print actions were not run.

Stored fusion counts are4890 one-step/macro/intertwining checks,542 full trees,216 remainder-transpose checks,2086 collision nodes and130 generic convolution embeddings. These are stored finite algebra controls, not fresh execution or a fast implementation.

## S35 — check_oversampled_subtrees.py
- SHA-256: `bad3c3e9acf087c07fa5049aebb3368422e5ddedf08d1af91391623e509c97d0`
- Scope: lines 1–102, 3318 bytes; Oversampled rational subtree checker
L65–100 covers dyadic grids S<=32 over F97, explicitly excludes resonant poles, applies the modular numerator correction, and checks parity leaf values/full decoded coefficients. Root helper assumes dyadic n, appropriate for this fixture grid only. Degree-limited numerator/remainder and all sample transforms are naive exact arithmetic. Positive finite identities do not give fast running time; resonance handling belongs to a separate source and cannot be credited here.

Stored540 oversampled cases and7230 parity/decoded coefficients match the grid's case count. Inputs exclude poles; resonant correctness is not covered here.

## S36 — check_spectral_bridge.py
- SHA-256: `7b9a687f04e81bb5aa748e926568e7ebc355a5fa9066242d846510d45c5df838`
- Scope: lines 1–53, 2615 bytes; Half-grid spectral extension checker
L16–24 constructs a dense Cauchy-type extension E and verifies E² is a cyclic shift on every basis column for five dyadic lengths. L25–35 checks full and degree-restricted commutation-defect ranks on ten polynomials per degree; L36–47 checks evaluation/parity splitting with100 random polynomials. Depends on exact rank from check_displacement. Dense rank/evaluation oracles certify finite identities only, with no performance, all-length or stability claim.

Stored five L fixtures have10L commutation/restricted checks and100 random polynomials each. No runtime or stability test is present.

## S37 — chirp_exact.py
- SHA-256: `958e263bb1e2d996f553cd7760af12cfae2855496515af85312eb38a6610f7ac`
- Scope: lines 1–196, 6800 bytes; Exact modular chirp algebra audit
L31–39 validates dyadic 2N roots and constructs chirp/recurrence phases. L48–80 is an ordinary radix-2 NTT; L98–104 explicitly expresses chirp convolution using this hidden FFT. L165–195 compares defining sums, chirp factorization, Gauss identities, moment and filtered ranks at N4..64. A recurrence for the chirp kernel does not imply a short recurrence for arbitrary convolution outputs; moment rank N and filtered rank N-1 demonstrate that boundary. Probability (1-1/p)^N assumes uniform field input and invertibility. General caller omega is trusted by dft_ntt; no supplied execution.

Associated chirp audit results/logs are historical finite-field tests; the source itself preserves the hidden NTT explicitly and does not make kernel recurrence into arbitrary-output O(N) work.

## S38 — compiled_kernels.py
- SHA-256: `d4bd2a7bda3223f73ee0dfb3a1e1ab0ab5d9af4ca2ba24ca290f511b4b49f2d5`
- Scope: lines 1–189, 8182 bytes; Bounded generated jet kernels
L35–69 generates specialized full/partial loops from internal degree literals; L74–85 explicitly compile/execs generated source and may Numba-JIT it if invoked, which this review did not do. compile_prepared trusts Phase-8 shape/sparsity data and caps degree<=16 and sparse terms, but does not validate full kernel shapes/finiteness or ensure immutable storage. It warms both full and partial functions, with compilation costs exposed separately. _FUNCTION_CACHE is unbounded by symbolic shape. Specialized selected-bin validation rejects fractional indices, stricter than the underlying PreparedEdit API. This accelerates known prepared convolution updates only; all preparation and cold JIT must be charged.

Compiler logs/tests are archived claims. No execution of compile_prepared, generated source, exec, compile or Numba occurred. Full-static coverage is only for the checked generator source, not every future generated program.

## S39 — condition_reset_experiment.py
- SHA-256: `47c51b59d0a9fad4baea916a4ec6743f19b1c77defb4d488cc0012267e9f1b6a`
- Scope: lines 1–120, 4206 bytes; Condition-reset numerical toy
L31–44 supplies a dense two-gate toy whose completed product is unitary despite an ill-conditioned prefix. L61–90 multiplies completed blocks and arbitrary dense unitary mixing; numerical condition values are recorded for six small cases, but no pass/fail bound is asserted. This illustrates unitary invariance of condition number and does not construct a fast primitive, prove existence of well-conditioned #130 circuits or model finite-precision error accumulation. Dense QR, Kronecker embeddings and SVD condition computations are not cheap implementation steps.

Stored six dense toy cases show max condition nearK and final condition near1, e.g.N64,K10^6 has max1000000.0001649464. These are numerical illustrations; source has no accuracy assertion for these bounds and no fast implementation.

## S40 — cost_aware_fft.py
- SHA-256: `150e8e4d461527059d77ec70cb97acc63e131426200fb2ee162214735ff69bd4`
- Scope: lines 1–606, 24728 bytes; Producer-metadata cost-aware rFFT engine
Hash cache L177–202 checks full arrays, and explicit states correctly carry known shifted bases and edits; float arithmetic and supplied relations remain conditional. Concrete correctness defect at L518–531: sparse_from_known_changes uses zero placeholder raw input and blocks only method='native', but method='auto' can select native (e.g. small edited signal under cutoff), dropping the supplied base spectrum. L90,111,341,357 silently truncate fractional edit/shift/bin arguments. combine checks each finite coefficient but not overflow of accumulated terms/edits. The pruned temporary budget counts one N-sized complex array while transformed/raveled arrays can coexist; calibrate's looser n*16 eligibility can then hit the stricter allocation guard. Explicit live states/bases are outside internal budgets as documented; output caching is caller-held. TrackedBins detects method mutations but public dictionaries/indices can bypass that discipline. No unconditional full FFT improvement.

Stored dispatcher benchmarks explicitly warn that four-bin comparisons use full FFT baselines and alternative selective methods may be cheaper. They do not test away the spectrum-only auto-fallback defect found statically.

## S41 — cut_budget.py
- SHA-256: `32902b1da3ffe86d537a31583d39270aea27ddee54d86e326230b1235af5a2bc`
- Scope: lines 1–180, 7292 bytes; Two-quasiseparable-stage cut-rank obstruction
L85–120 bounds cut ranks for M=S2 P S1 and computes necessary rank sums; the endpoint_certificate docstring calls it an upper bound although its returned quantity is a lower requirement. L138–168 tests dyadic N8..64 over two fields, random internal shuffles, and selected endpoint permutations at N8/16. The N/4 stage-rank-sum obstruction requires one naturally ordered endpoint; arbitrary both-endpoint layouts receive only the tested cut bound. Printed each-channel rank>=ceil(N/8) requires the equal-channel-rank interpretation and is not a bound on every individual unequal stage. Root validation checks only dyadic order. No general multi-stage or FFT runtime lower bound.

Stored data has eight Fourier endpoint certificates,24 random products and36 endpoint-pattern scans. One-natural-endpoint and two-stage restrictions must accompany the N/4 claim.

## S42 — cycle_bridge.py
- SHA-256: `a7ef561d89a2eab0833a904170c00be34cac919c598fa7d0c33bf266e8a5b4e5`
- Scope: lines 1–173, 6455 bytes; Bessel/Fourier cycle bridge audit
L40–84 validates the exact dense Fourier-conjugated differentiation/Cauchy matrix and disjoint minors in F998244353, then samples sparse-plus-rank bounds. L91–100 uses two ordinary FFTs for H, explicitly exposing the hidden work. Double-precision Bessel recurrence L103–118 has only its second-order error threshold asserted in main, while later orders are reported; independent65-digit dense checks cover N8/16/32. L147–153 verifies distinct fractional offsets for odd grids, not a fast odd-length transform. Exact finite Cauchy ranks and numerical Bessel identities do not prove O(N) FFT execution or uniform numerical stability.

Stored sixth-order Bessel error grows to1.284003605247524e-6 atK128, while main asserts only second-order error<1e-11. High-precision finite checks pass separately; uniform double-precision stability is not established.

## S43 — cyclotomic_bound_demo.py
- SHA-256: `00c9338401115fdc965d9bb051acfc357763ee0afeaffa88879b3abee792546b`
- Scope: lines 1–57, 1773 bytes; Cyclotomic coefficient-bound toy
L23–29 uses SymPy inversion modulo Phi_D for three fixed rational functions and computes an exact rational-coefficient l1 bound. Triangle inequality applies to primitive unit-modulus embeddings when denominators are units. Numeric validation L43–50 converts a60-digit evaluation to machine complex and records a Boolean without asserting it. This is an effectivity example, not extraction of actual #130 coefficients, a condition bound on that construction, or a complexity result.

Stored three toy l1-bound records have bound_valid=true. This is numerical corroboration of the triangle bound for those representatives, not extraction or conditioning of the actual large Fourier construction.

## S44 — cyclotomic_interpolation.py
- SHA-256: `e860dd50d00d4335f86b66844d92085585ba55629de960678975bc7364b9ac84`
- Scope: lines 1–197, 7138 bytes; Tiny exact cyclotomic interpolation utilities
Implements Fraction arithmetic in Q[z]/(z^m+1), a field only for power-of-two m, and uses exact Gaussian inversion. L74–109 limits interpolation to N4/8 through validate_n and m<=5, exhausts all2^m subset-sum nodes and verifies Newton values. L112–146 correctly says full column rank excludes degree-d rational maps, whereas nonfull rank alone does not ensure denominators. L149–197 searches only39 nullspace combinations for a nonvanishing rational candidate, so failure is not a general nonexistence proof. Public Cyclo binary operations use zip and do not validate equal field dimensions; rational helpers rely on imported subset-sum validation rather than directly calling validate_n. Exact small-domain interpolation may be exponential, not an efficient all-frequency algorithm.

Associated orbit-recovery audit records tiny exact interpolation and a degree-eight rational example. Rational nullspace candidates require denominator checks on every domain point; positive finite interpolation is not efficient general Galois scalar evaluation.

## S45 — cyclotomic_orbits.py
- SHA-256: `a28d79f0abcae1f1c86b8bc09cccf6ab3093fc30304ab724c8437ad49d8cb9e9`
- Scope: lines 1–122, 4339 bytes; Cyclotomic orbit descriptor
L29–44 stores N shared integer coefficients in exactly2(N-1) adds/subtracts, but int(v) silently truncates rational/noninteger input despite the header's rational-input scope. L52–67 materializes phi(m) signed-permuted coefficients per frequency and sorts absolute values in an assertion, adding superlinear implementation overhead. L90–96 evaluates one numerical scalar with a full coefficient sum; emitting all basis expansions costs (N²+2)/3 coefficients (L107–114). Galois descriptors are not constant-time complex scalar registers. evaluate_mod assumes p is prime and selects roots separately; the fallback at arbitrary p need not choose compatible roots across levels, and reference_dft_mod uses3 without order validation. Finite-field evaluation does not establish characteristic-zero Galois recovery or a global O(N) FFT.

Stored orbit_results.json has seven N2..128 rows and254 output values, with stored coefficient countN and expanded count(N²+2)/3. Reviewer checks these formulas independently; symbolic descriptor compression is not materialized scalar-output complexity.
