# Independent paid NTT v2 delta acceptance

Date: 2026-10-13. Decision: **ACCEPT the v2 source-only benchmark protocol definitions. R1–R5 are resolved; no remaining protocol repair is required by this review.**

This acceptance is specifically against the original sealed review paid_ntt_contract_audit_1613/INDEPENDENT_PROTOCOL_REVIEW.md, SHA-256 ff43683d04cf5493afc84196938bcfcb695374ec284f84501b66d56a40f1f0f2. It is not acceptance of an implemented adapter, execution authorization, evidence that an NTT passes correctness tests, measured speedup evidence, or a novelty claim.

## Exact accepted v2 identity

Directory: paid_ntt_contract_v2_1622.

- PAID_NTT_CONTRACT.md: 0cefd28b3548a2368ca87b6429b4775aff7e8e16d28913dfaaf4c2a324ca2301.
- PROTOCOL.json: e97f0f3da08ed17804169262fb8f31872032f53ab708091419af4b2eec28f3dd.
- FILES_SHA256.json: def2f742943cc2a50b15c785cf1a14b4605f9a93a6d48e3ed9e029688be676ff.

All 16 entries in that v2 file manifest were independently checked for byte length and SHA-256. All 11 original v1 manifest entries still match their sealed pins. Both original recovered CPP/CSV source files remain pinned. No accepted source arithmetic/domain assertions were changed by v2.

## R1–R5 dispositions

**R1: RESOLVED.** Contract 5.2–5.3 and PROTOCOL sink/interval fields fix discarded warm-ups to dense_0 through dense_3, distinct warm/useful accumulator state, fixed seeds, exact reset placements, per-vector volatile publications, request buffer destruction, and the restart of useful inputs at dense_0. The expanded manifest explicitly fixes warm-up/useful input sequences and seeds for every trial.

**R2: RESOLVED.** Checked request size/representation/canonical scans are paid; fresh-plan guards and repeated omega/order/imag checks are charged separately from nominal source root-generation counts. Mathematical/oracle audit work is separated. There is one measured fixture route: read and decode eight dense vectors from the existing pinned corpus into a fresh per-method/per-trial pool, perform its specified SHA-256/range checks once, and tear it down after service. H=K useful outputs, with no cross-algorithm/trial amortization and no denominator credit for discarded warm-ups. K=1's deliberate eight-vector pool overhead is disclosed. Paid-warm and workflow totals are directly enclosed intervals; conditional warm is nested in its paid-warm trial, and fine-grained diagnostics are separate.

**R3: RESOLVED.** The unchanged pooled whole-block percentile bootstrap is explicitly nominal/exploratory under exchangeability; unestablished coverage under serial/session dependence is stated. Session-specific estimates, block-order results and lag-1 diagnostics are required. Opposite session-median signs require an inconclusive stable-ordering conclusion, and the pooled interval alone cannot establish significance or stable ordering. The design does not claim random-input population inference.

**R4: RESOLVED.** The opening, case definitions and machine-readable protocol explicitly say K=1 uses dense_0 only and K=64 uses each dense input eight times. n=8192 is described as the first tested power above the existing n<=4096 dispatch cutoff, not an established optimum/crossover. The full correctness preflight through n=2^18 remains distinct from the single-size timing scope.

**R5: RESOLVED.** The permutation descriptions now use the frozen algorithm-index order rather than claiming alphabetical algorithm-name sorting. All 48 actual block/session/algorithm-order records are unchanged from v1.

## Independent expansion and byte checks

The accepted immutable SOURCE_IDENTITIES.json, corpus_inputs.bin, CORPUS_MANIFEST.json, MODULUS_ROOT_CERTIFICATE.json and STATIC_COUNTS.csv are byte-for-byte identical to v1. The prior complete independent reconstruction of all 288 corpus vectors therefore carries forward on identical bytes.

Fresh delta code independently reconstructed every one of the 18 fixture pools from the original serialized slices and checked exact cases, offsets, lengths, concatenation size and SHA-256. The 8192 pool contains 262,144 serialized bytes and has SHA-256 7609373072dd8cc474fbccc493b14ad2140fc0c532e7a4304b1685454d9197de.

Every one of the 768 expanded trial records was checked against the frozen session/block/K/mode/algorithm nesting. Trial IDs are contiguous, identities unique, algorithm positions match the paired-order file, and each condition/algorithm has 48 observations. Every fixture hash, independent-ownership flag, H value, useful case, warm-up case and accumulator seed matches the contract.

Exact design totals, not observed runtime results:

- 768 directly timed workflow/service batches
- 24,960 useful transform calls
- 1,536 discarded warm-up transform calls
- 384 conditional-warm intervals nested within the 384 warm trials

No extra workflow transform executions or independent observations are introduced by nested metrics.

## Acceptance boundary and remaining execution gates

The accepted document is a frozen evaluation specification. Before timing, the original requirements still apply: separate execution authorization; reviewed source-to-adapter diff; independent oracle and expected-output files; timed-release and separate diagnostic correctness gates; pinned hardware/toolchain/flags/binary/sink; valid clock/resource preflight; and complete raw/diagnostic records. The nominal source operation counts exclude the newly charged guard work, as v2 explicitly states.

At implementation review, enforce the already accepted distinction between primary enclosing timing and separate fine-grained diagnostics. Do not fill primary-trial phase fields with fabricated values or add fine-grained instrumentation contrary to section 5.3. Any diagnostic values must retain their separate-run identity. The radix2 plan need not retain an unused imag field; its common runtime root checker can derive the temporary quarter-root value from the root table and charge that check.

The historical review-body gap remains unresolved. Neither v1 nor v2 was modified by this delta reviewer. No inherited C++ was imported, compiled or run; no NTT oracle was executed; no expected transform outputs or new timings were produced; and no external Sheet/GitHub writes were made.

Supporting artifacts in this audit directory: V2_INDEPENDENT_DELTA_CHECKS.json and check_delta.py. The script is newly authored byte/data validation only; it does not execute the original generator, NTT source or oracle.
