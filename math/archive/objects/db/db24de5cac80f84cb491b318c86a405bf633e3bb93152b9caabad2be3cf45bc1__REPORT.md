# Complete exact-source structure review

Read all 51 assigned exact hashes: 349,868 bytes and 7,419 lines. Source execution, imports, compilation and AST parsing: none. This worker made no changes to the central registry or earlier seals.

## Material findings

### F1: implementation_defect
Data-dependent head-tail plan reused on changed same-length input scales fresh residual draws with stale norm and old budget. Fresh deterministic all-ones to all-twos control violates requested error bound. Existing suite only reuses plans on original data.
Evidence: source18:399-421; INDEPENDENT_CONTROLS.json/stale_head_tail_plan

### F2: test_attribution_defect
unittest.main appears before later test classes, omitting lazy-adapter one test and prepared/buffered four tests in ordinary direct script invocation. Imported discovery can run all.
Evidence: source28:24-38; source31:93-134

### F3: api_guard_gap
Native benchmark null-pointer guards missing; Python benchmark ignores returned out allocation; low-level lookup requires binary bytes; dynamic sparse benchmark lacks valid length/repetition guards; empty pruned sparse output is compact empty; vectorized surrogate missing support domain guards. These do not by themselves refute intended valid-input mathematical identities.
Evidence: Per-hash exact line findings

### F4: evidence_attribution
Checkpoint and README mostly consume stored metrics; transparent swap emits no enforcing assertions; exclusion default main never calls verify_embedding; sanitizer reference shares FFT kernel, and leak-disabled report follows preserved LeakSanitizer failure. Adaptive results include post-change fields not emitted by reviewed main test script.
Evidence: STORED_EVIDENCE_RECONCILIATION.json and per-hash reports

### F5: scoped_positive_math_control
Fresh butterfly identity, fixed N64 inverse/sector minors and stored N16 rank9 minors pass independent controls. These support their fixed-model algebra, not general FFT impossibility or arbitrary mixing lifts.
Evidence: INDEPENDENT_CONTROLS.json

### F6: conditional_transfer_scope
Pair/frame sources certify finite GF2/support/profile and exact scalar recurrence arithmetic conditional on inherited compiler/semantic/analytic/routing/recovery proofs. Bounded integer-program optimality claims in pair_graph header are not solver certificates in that source.
Evidence: Per-hash source41/43/45/49/51 scope statements

### F7: serialized_artifact_identity
Original frame-word gzip paths and declared compressed hashes absent, but both exact decompressed words recovered under baseline word.json.gz alternatives in same archive. Carrier23 same; carrier25 different. No dirty word replay performed.
Evidence: FRAME_WORD_HASH_RECONCILIATION.json

### F8: provenance_closure
199 same-location digest references match and24 match other locations;90 references unresolved in same container, no mismatches. Local absence is not corpus-global absence. Runtime imports/ABI and all ancillary proof closure remain unverified.
Evidence: STORED_INTEGRITY_RECONCILIATION.json; DEPENDENCY_RECONCILIATION.json; LITERAL_FILE_REFERENCES.json

## Fresh independent work

Eight separately authored controls ran. The stale-plan counterexample has error 32 against allowed 128/5 at n=1024, epsilon=2/5, delta=1/20, irrespective of sampled indices. The two-scan butterfly was checked in 1029 finite-field cases. N64 eight resolvents were independently reconstructed by inverse(I−tau P), giving 64 matching sector minors and two matching direct-sum minors. Sixteen archived N16 rank-nine determinants match. Archived184 streaming rows and frame 47 strict rational constraints were internally reconciled. The script also records exact test-entrypoint ordering and a GF2/characteristic-zero scope counterexample.

These are independent controls, not executions of supplied source or a full replay of the archived compiler words.

## Preservation and evidence

42 exact archive snapshots,139 source archive occurrences and6 standalone occurrences checked. Preserved 432 adjacent stored-document occurrence records (216 distinct bytes). Complete per-hash reports identify source-line scope, cost, defects, tests, direct-read receipt, occurrences and static dependencies.

Stored output status is historical data. Checksums establish identity, not original authorship, historic execution or mathematical truth. Generic manifest reconciliation leaves 90 references unresolved within the same container; no claimed corruption or global absence. Both serialized baseline frame contents are available via exact decompressed hashes despite different gzip bytes and paths.

## Boundary

This completes this 51-source assignment. It does not finish every corpus material/proof, execute uploaded programs, establish native runtime/data closure, prove inherited general transfer hypotheses, or certify novelty/priority. Prepared updates, coarse all-bin approximations, restricted finite obstructions, ordinary FFT controls and conditional finite compiler witnesses remain distinct.

## Per-source index

- 01 729fcf18fc706087c77eff9d1d7a5c53354cd6ec48ee06e16078f9ee65c34e2d (319 lines): scan_hybrid.py
- 02 090d1a587762f27838f9a077cd7e6a16cdbd9f315c4284b3105c522d75212f12 (61 lines): sector_obstruction_milestone/check_sector_obstruction.py
- 03 7414919441e62cd7123d7bb3898c5d48567acc9272dc11b4ec4fd2714a0ed37c (183 lines): seed_lifting/check_hierarchical_lift.py
- 04 a12e3e520c54da15831946192808119608cd20065b4200f4738095c34161dddd (221 lines): seed_lifting/check_lift_defects.py
- 05 e0dab3fae4f42c15440bfc721c552f5d802c737ccb157d4a4b2947cbe6facf97 (248 lines): seed_lifting/check_n16_outer_gate.py
- 06 a8eecec6035e4aec32c1830dcbf86a8108e6df0d430b2d016b7c25c64bcb7cc9 (77 lines): selective_fft_experiment/c_experiment/adaptive_fft.c
- 07 3fc34239d786f2b99fbafa6ed663d515f0c202f11a9600bc9dd54a60f1a4a363 (223 lines): selective_fft_experiment/c_experiment/adaptive_fft.py
- 08 2fb8fe3e4583f8977b2022e0dca56e433fadbdba9abfdbbee81edded9dc4c2a9 (222 lines): selective_fft_experiment/c_experiment/benchmark.py
- 09 45564faf80294a9baa61822c9e4553d0eb79cfc503f7f2d8878cf99f5573a595 (186 lines): selective_fft_experiment/c_experiment/leaf_fft.c
- 10 91456b6dad4257479e8c6e8b6398ad1c31238f4cff319e3d9354dd57728c3712 (155 lines): selective_fft_experiment/c_experiment/test_adaptive.py
- 11 bdfd5079a07d45328330aa5129fc7e6583a071786a8742c8c7b17a175e939f82 (30 lines): selective_fft_experiment/c_experiment/test_adaptive_sanitizers.c
- 12 658bd3072e4692e4c67794ffaa9f709d361667c135740af16fd396b733141e43 (44 lines): selective_fft_experiment/c_experiment/test_api_guards.py
- 13 efaf1b28c39db0a210f7afdbd89a7aaa0e016b80f96e91b7a6102640de5abff0 (31 lines): selective_fft_experiment/c_experiment/test_sanitizers.c
- 14 104ac318c14192a0da814732dd86b7dedbe47680b15a1e3067fd3bcf8947a708 (157 lines): selective_fft_experiment/python_experiment/benchmark_python.py
- 15 251b8ec69f10a99902a7cb0e75029d8146ccac97baa759030a9bd0daf498aa01 (86 lines): signed_pole_milestone/check_signed_poles.py
- 16 0b41cd365213b8792dd239ffee1395faabb0875e579771864ca597a0ee731cfb (49 lines): sparse_delta_dynamic_bench.cpp
- 17 01610c5a7f44ccedd808470196d13dd05899d09cfcbacc0cfe2c51850a15a7da (127 lines): sparse_delta_pruned.cpp
- 18 92e8a55e835c851b04a9f8e9408162a20067fc890efa430df1d1f6933caca8df (487 lines): sparse_surrogate.py
- 19 105984b93a6aaf49a953eeebb9d232e7be4fd057543e2a7f19e9469a2bd03f1e (36 lines): sparse_surrogate_fast.py
- 20 5edac0ce6b978945926b50cf303bbc88dc502ebda65c5948cdf2262975aa4e08 (192 lines): spectral_boolean.py
- 21 66fc43fa655601fd9ab5a2e5e468914c445078bb7876b725718018097eb11ae5 (199 lines): streaming/streaming_fourier.py
- 22 8d5d6a551fcbbe1978ed38f5adebbbd87accd3ba5ba8ecb1e1c316866aecfbeb (22 lines): stress_sizes.py
- 23 bd6fa1acd898edc5f3553205a8d16f64cbef75927e2c3c0b76c9adcc4846cf1a (82 lines): test_checkpoint.py
- 24 088fc1d79c3ff517a2831e2fea34ec2eb507ae651090e772c65a65ce3cf8042a (428 lines): test_condition_reset_independent.py
- 25 14f0dea233876d45bfe74dec25a2695df4c858d2124032b533a8564b26acdaf5 (52 lines): test_experiment.py
- 26 d249150c219a63f67188b7ff4336db7cecac9db932f3f1d5ce486650874c882f (61 lines): test_sparse_surrogate_v2.py
- 27 88906c42bd91a9877c42b2c9e4cdf2208dcb32f3a93d5f688b3ef5cd092036ba (92 lines): tests/repetition_reference.py
- 28 d0753cf797ff8512a3b5563465d379355e39339d36e9e2f37856e955335fcd2b (38 lines): tests/test_adapter.py
- 29 452c91f6b8680f594134350662e4980f5760184b5916bdb585c00bca1e31b607 (62 lines): tests/test_exact_modular.py
- 30 0d9e1ac5b833d267487bfd67735a8edb005e8ea6ee27be08222b50edc80f33b8 (88 lines): tests/test_hybrid.py
- 31 5c8eeef5c2a92ed7adc4ab160a824ece00b9bafbe90f486548e6f10f94f374cc (134 lines): tests/test_lazy_spectrum.py
- 32 8ea491f2d7924881ac82371c7ec1156b056bca2c2b4b932e1e5a1d8785066c37 (81 lines): tests/test_orbit.py
- 33 021cbd19f454e3229df04f5ef5362d9472ce111db368829bc5e4a52956919b3e (21 lines): tests/test_prepared.py
- 34 cb59774ddb143c10ae8ac8f25826d3a3ace2f2b8f672387c61cb1ce385214f04 (84 lines): tests/test_spectral.py
- 35 5c89954a426578a15a1049f2e7da15c9bebcb4b69764b7ebb81642f07418b4c6 (75 lines): tests/verify_fast_decoder.py
- 36 94c62e1a0c9271ebf0042b2b2936bca42b985ae6addfa25407816f2967012087 (38 lines): tests/verify_reduced_chirp.py
- 37 5b61f1e29e33a6645eb4ba8cb9d3cf546b0b6980539dfe49dbee1e153186b46e (46 lines): tests/write_readme.py
- 38 97447b9003b928fc1b8efeda1b2d66ef9d839545afcc70e39ef2e8dc9ef0a984 (66 lines): transparent_swap_check.py
- 39 4a3d66dc2ecd2f8f3251da9ef7c61f1795ea9dce289f83f2fa893e552abea4a0 (396 lines): two_edit_engine.py
- 40 375a7ca6cac6d153c1880fd5ea5b4525e5dca9d4ee3018d24d679c219b59c5b3 (60 lines): upstream/references/frame-compiler/pr48/research/copied-fixed/changed_graph.py
- 41 44932182ce6c4d39776650311262ef0ac1ea9b5da7220bc0f728e2789881f84a (330 lines): upstream/references/frame-compiler/pr48/research/copied-fixed/verify.py
- 42 7e143eb75bb342ac8f0c82a60005e7c35c9ec827de479bf6fb773151f3af5fa1 (43 lines): upstream/references/frame-compiler/pr48/scripts/partial_swap/binary_io.hpp
- 43 4d27575dcad2b45a281a34054d311409ecd954f373c0c3a62c29bcc843f06a86 (196 lines): upstream/research/pair-assembly/balanced_assembly.py
- 44 12e3976daed5f90bb42750553d86802a27465ea875d3fc5b24ed824492df3ee7 (67 lines): upstream/research/pair-assembly/frame/frame_compile.py
- 45 fafe25d57166a747eeb847444a2e02dd7eed19038b93a2c495014d147d04a8fb (176 lines): upstream/research/pair-assembly/frame/frame_verify.py
- 46 3d47e89d2649c90800a276bdd0480131def50e0bdf92c122a19494b55bf17420 (248 lines): upstream/research/pair-assembly/pair_graph.py
- 47 31f5687abdacf80e9bde52af3ff7bc55a9c5a206e9f223e7035e04b3de55cde3 (216 lines): upstream/research/pair-assembly/producer.py
- 48 b9fbd71c746609948b60c441ba4601e88436956fe636d1810f270ce4ce6a63a6 (107 lines): upstream/research/pair-assembly/profiles.cpp
- 49 683ce7521b219ecde6aa47a01eaa61e0831c09632494c179fec7d4eb0ed71ca7 (358 lines): upstream/research/pair-assembly/verify.py
- 50 b253f9d7318becda1c1f3b24e2287ed44a9c27fcea00cf9d531afb950d0457a0 (184 lines): upstream/scripts/exclusion_circuit.py
- 51 bc6910c8bbe8224285164323d3c06e9035ad3eaa55416abc2867ae0066454a0c (235 lines): upstream/scripts/experiments/binary_frame_compiler.py
