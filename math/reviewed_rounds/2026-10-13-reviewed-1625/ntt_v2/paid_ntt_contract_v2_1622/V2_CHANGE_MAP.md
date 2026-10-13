# v2 change map

Scope: close R1–R5 from paid_ntt_contract_audit_1613/INDEPENDENT_PROTOCOL_REVIEW.md, SHA-256 ff43683d04cf5493afc84196938bcfcb695374ec284f84501b66d56a40f1f0f2. v1 remains unchanged at paid_ntt_contract_1546. No NTT implementation or oracle was executed, and no timings or external edits were made.

- R1, contract §5.2–5.3 and PROTOCOL sink/interval fields: warm-ups are dense_0..dense_3; warm and useful accumulators/publications are distinct; both start from the pinned seed, with resets and every publication inside explicitly named timers. Useful requests restart at dense_0. EXPANDED_PILOT_TRIALS.json includes every trial's cases and seeds.
- R2, contract §5.1–5.3 and PROTOCOL fixture/request/plan/interval fields: ordinary request guards and repeated per-plan root checks are paid. The one workflow loads an independent eight-vector pool per method/trial, checks its concatenated-byte SHA-256 and canonical range, serves H=K useful outputs and destroys it. No cross-method/trial amortization or alternate provenance route remains open. Historical corpus/oracle/certificate audits are separate. Primary paid-warm and workflow totals are direct enclosing intervals; fine stage sums are diagnostics only. FIXTURE_POOLS.json pins the exact input slices and aggregate hash per n.
- R3, contract §6 and PROTOCOL statistics: the unchanged pooled 48-block percentile resampler is explicitly nominal/exploratory under exchangeability. Coverage under serial/session dependence is unestablished. Require session/block-order and lag-1 diagnostics; opposite session-median signs imply inconclusive stable ordering. No pooled significance/stability claim alone.
- R4, contract opening/§5.2 and PROTOCOL corpus/pilot fields: K=1 is dense_0 only; K=64 gives eight copies of each dense case. n=8192 is the first tested power above the existing n<=4096 cutoff, not an optimal boundary or crossover. The timing pilot retains the full preflight correctness corpus through n=2^18.
- R5, contract §6, PAIRED_ORDER metadata and generator comments/description: replace the misleading name-string “lexicographic” description with permutations in the frozen algorithm-index order [radix2,fused4,splitradix,dif4]. All 48 actual ordered algorithm lists are unchanged.

Additional explicit gates from the same review: CHAR_BIT/type sizes; timed release-binary correctness and input immutability; VM/container/CPU-quota disclosures; clock overhead separate from resolution. These clarify the existing domain and environment contract, not new NTT claims.

Unchanged accepted bytes: SOURCE_IDENTITIES.json, corpus_inputs.bin, CORPUS_MANIFEST.json, MODULUS_ROOT_CERTIFICATE.json and STATIC_COUNTS.csv. Source CPP/CSV identities are unchanged. The generator's descriptive text changes but its corpus formula and seed remain v1; v2 does not regenerate or reinterpret the pinned inputs.

The expanded pilot remains 768 workflow/service batches, 24,960 useful transform calls, 1,536 discarded warm-up calls and 384 nested conditional-warm intervals. No extra workflow transform runs were introduced. Implementation/oracle/build binding and separate execution authorization remain required before any timing.

Status: repaired definitions sealed for independent delta recheck; do not infer acceptance until that review returns.
