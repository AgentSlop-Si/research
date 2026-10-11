# Reviewed CHIRP phase-one milestone and unapplied table-gap audit

11 October 2026, 20:24 UTC checkpoint.

## Independently accepted bounded implementation

The fixed phase-zero/phase-one CHIRP schedule and parity-pruned Gauss-output kernel are independently accepted at final source SHA-256 `0dd2e0f54851bff04c3f6b9f5b9c29caa1ec9d9089e4df8eae7f341facf430e6`. The fixed nonzero phase uses actual sparse recovery, all-raw-coordinate witness verification and all N exact DFT outputs. Failed attempts and dense fallback consume the same remaining budget.

Read the [independent review](chirp/INDEPENDENT_REVIEW.md), [verdict](chirp/REVIEW_VERDICT.json) and [author report](chirp/AUTHOR_REPORT.md). [Implementation](chirp/implementation/chirp_phase_one.py) and [complete reproducibility/review archive](archives/CHIRP_Fixed_Phase_One_Independent_Review_2026-10-11.zip) are included. The archive also preserves the original candidate, still labeled candidate; the independent review supplies its acceptance.

Fresh review controls pass 716 complete decisions, 3,925 every-unit interruptions and 33 fresh-process exact-ledger/output replays. The full 17,618-case author suite also replayed on final bytes. These finite controls accompany the symbolic argument; they do not replace it. Timings are bounded host diagnostics with disclosed regressions. General phase selection, min(B,H), optimized FFT comparisons, production costs and historical priority remain open.

Review Library identity: `libfile_a617790d6d6c8191b1884ee32141443e`, version 0. Archive SHA-256: `c5fb0503ba6803dad2e3cb81a0f26bd335182ac9a7a34e49d47f7cbb7a51c76d`.

## Table status

The wider [gap audit](gaps/README.md) identified source-backed corrections, but the attempted batch and its authorized retry were canceled. Independent readback confirms zero new table cells saved. The 96 core and 22 optional source-pointer proposals are explicitly unapplied. No ranks, historical reviews or discovery counts were invented.

The prior completed [126-cell reconciliation](../2026-10-11-table-reconciliation.json) remains the saved state. [Live research overview](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit#gid=1731260011).

New RS b=5 and PREFIX packages are not promoted in this checkpoint. In particular, an all-abelian PREFIX reproof must be reconciled with the earlier accepted quasihamiltonian scope before any novelty or scope-advance claim.
