# Independent root review of the new bounded ALG-007 adapter

2026-10-16 UTC. Verdict: ACCEPT the newly authored bounded adapter and its stated event ledger. This is not acceptance of execution or integration of the historical implementation, nor a general FFT improvement.

Reviewed source SHA-256: b41f85a2492d6d47749aff4f57188fa5872dd0c77c027b6a93ccefeaee216bd8.

## Independent evidence

The reviewer read the implementation and contract, then authored separate direct-definition and accounting checks. Only this session's newly written module was imported; no supplied or patched historical research program was executed.

- 3,252 calls and 108,224 output coordinates agree with direct negative-sign DFT evaluation over the declared prime field. These include 2,166 budget fallbacks, 546 Green acceptances and 540 cap fallbacks, varying length, block size, chirp parameters, caps, budgets and supplied primitive-root orientation.
- Seventeen separate controls verify exact fallback butterfly schedules, invalid-domain rejection, built-in-type checks preventing user hooks, and preservation of recognition work when decoding is interrupted.
- Sixty exact accounting controls independently verify the cold/setup formula and complete cumulative fallback formula, including both supplied-root and generated-root branches.

These finite controls do not replace the written correctness argument or establish novelty.

## General contract checks

The fixed modulus certificate is valid: the complete prime factorization of p-1 and full-order witness imply a unit of order p-1, hence phi(p)=p-1 and primality. Exact dyadic root-order checks are sufficient. The same root table, sign, field, raw snapshot and output order are used on both routes.

Complete per-block reconstruction certifies the vector-valued support. New columns have zeros in earlier blocks because those blocks were already fully certified. Successful discoveries grow support, bounding their number. Cap rejection or a budget exception never returns partial output as an accepted transform. The budget applies to both recognition and decoding, and fallback retains every charged prefix.

DIF butterflies followed by explicit bit reversal implement the full unnormalized negative-sign DFT. A fresh copy of the canonical raw input is used on fallback. The accepted Green formula has the necessary odd-slope and even-length antiperiodic closure; all seed additions and final normalization are paid.

Independent event derivation agrees with the report: each butterfly contributes eleven event units, explicit bit reversal contributes n log2(n), and the complete kernel has T(n)=(13/2)n log2(n)+9n+log2(n)+1. Cold validation/setup contributes 15Q+11+H(Q). Fallback total adds attempted work, one dispatch, T(Q), and 4Q final output units. These are declared algorithmic events, not exact Python instruction counts or bit complexity. The text explicitly accounts for constant-vocabulary bookkeeping and O(Q) simultaneous field-word storage, including interrupted decoding.

## Limits and disposition

The fixed prime and Q<=2^27 make this a bounded executable contract. No unbounded asymptotic saving, wall-clock superiority, optimal budget constant or worldwide novelty is established. Invalid-domain requests are rejected, not padded into a different transform. Memory availability at the largest allowed algebraic length is not guaranteed.

The original rejection-only source and incomplete historical counter remain historical evidence. The new implementation is an independently authored realization, not a tested wrapper around that old executable. Any literal historical integration obligation remains unrun and must be separately resolved. Parent closure requires reading the full owner scope; this review alone authorizes only recording the new bounded implementation result.

All accompanying checks and JSON results are reproducible with the standard library. Source bytes were pinned before review. A first local results summary omitted twelve additional-root calls from route totals only; the test summary was corrected and the final suite rerun. The delivered route totals sum to all 3,252 calls.

For portable replay, each checker accepts the new adapter's source path as its first argument and writes results beside the checker. For example: `python check.py /path/to/alg007_bounded_adapter.py`. Only that newly authored, reviewed source should be supplied. All three portable checkers were rerun successfully after this path-only adjustment.
