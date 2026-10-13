# Independent final research-table review

**Verdict: PASS for coverage, score integrity, current-status wording, and preservation.**

Reviewed on 12 October 2026, 23:21–23:24 UTC, after the writer’s 23:20 UTC final-stable marker. This review made no live writes. It independently fetched the populated, bounded native ranges of all 13 tabs rather than relying on the writer’s read-back receipt.

Workbook: https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit

## Exact coverage and mapping checks

| View | Live data rows | Current overlay | Unique IDs |
|---|---:|---|---:|
| Catalogue | 4–181 | AA4:AF181 | 178 |
| novelity breakthough | 6–221 | U6:Z221 | 216 |
| Research overview | 5–329 | L5:Q329 | 325 |
| Incoming queue | 4–45 | G4:L45 | 42 |
| Next cycle | 4–13 | G4:L13 | 10 |

- The union of these five views is **329 exact IDs**: all **327 ranked base IDs** plus **NEXT-PREFIX-P13** and **NEXT-RS-RESIDUAL-B27**. No missing, unexpected, or within-view duplicate IDs were found. The two additions are parent-linked workflow tasks, not new canonical discoveries.
- The Catalogue and novelty identity sets exactly match `ranking/canonical_178_ranked.json` and `ranking/novelty_216_ranked.json`. The 216 novelty views include overlapping supplemental views; the canonical count remains 178.
- Every one of the **771 displayed scored rows** has a native numeric integer score in 1–100 and six nonempty current fields. All **4,626 current-field cells** exactly match `ranking/sheet_score_mapping.json`, supplemented only by the two explicit records in `new_workflow_tasks_delta.json`.
- All **879 source-row references** into the independently read tabs resolve to their stated exact IDs. Existing row order is preserved.
- All eight v1.1 current-status records exactly match `ranking/current_status_updates.json`. All 327 numeric scores are unchanged from the frozen v1.0 ranking.
- Top scores are **NEW-16 = 73**, **F020 = 67**, and **Q13 = STR-Q2 = 64**. The two new tasks inherit 73 and 67 from their stated parents.

## Priority, proof and novelty remain separate

The live headers clearly separate next-cycle priority, provisional rationale, attributed proof status, attributed novelty status, next action, and pass/stop condition. The Progress checkpoint says that scores prioritize work and are not truth, novelty, or breakthrough probabilities. Historical novelty bands, ordinal positions, and family ranks are preserved; the overview’s former `Priority` header is now `Historical order`.

The concise mapping is intentionally a projection of the fuller research records. Generic source-attribution labels, full source evidence, and long historical action text in `all_research_ranked.json` need not be verbatim duplicates of the compact live fields. The exact live-mapping comparison above uses the designated current mapping, not an incorrect raw-text equivalence assumption.

## Scope wording checked

1. **CHIRP:** Current Q13/STR-Q2 fields and Progress row 28 explicitly target a bounded exact rank-at-most-two unknown-common-phase **executor**, with phase filtering, recovery, supplied-grid scans, raw-coordinate verification, output, and full cost/refusal accounting. They state that the general-rank correctness theorem and dense reference already cover rank two, including the fixed-rank O(N) field-work theorem. The remaining task is implementation/accounting and independent replay, not a newly missing rank-two membership theorem. No general integration, production/bit-cost, speed, or historical-priority closure is claimed.
2. **Rogers–Szegő b27:** F020 and Progress rows 27 and 29 explicitly accept the guarded all-A **overlap** family. Ordinary residual squarefreeness remains a separate open task, including the stated finite residual domain. Overlap acceptance is not presented as ordinary squarefreeness, general-b acceptance, or FFT performance evidence.
3. **PREFIX:** The independently accepted finite D8 × C13 × C17 maxima 5948/5506 are recorded in the current fields and Progress row 33. The uniform p13/all-prime-r problem remains open; no optimizer classification, novelty clearance, or speed claim follows from the finite pair.
4. **General Fourier/FFT claims:** All 18 overview records marked CLOSED use explicitly scoped closure language and preserve related parent work. The restricted q-torus obstruction, generic-fusion gate, borrowed Fourier compiler, and engineering NTT baseline retain model, comparator, historical-priority, or practical-performance limits. No wholly closed general FFT problem, unrestricted Fourier lower bound, or blanket speed breakthrough was found in the current overlays and checkpoint.

## Checkpoint visibility and historical preservation

- The `Progress` tab remains first, with three frozen rows. Its native A1 value is the new dated 12 October checkpoint, listing 327 + 2 IDs and the 73/67/64 priorities. A1 is text-wrapped at 11-point Arial. Native score spot-checks use NUMBER format `0`; current-field headers are distinct and wrapped.
- Progress rows 25–31 contain the current coverage, top tasks, scoped scientific updates, and ranking method. Row 33 records the finite PREFIX acceptance.
- The old Progress A1 is preserved **verbatim at B32**, labelled as historical. All original Progress rows 2–24 are unchanged.
- Across all 13 tabs, **14,675 original cells** were compared. The only original-value changes were the intended Progress A1 replacement, overview A3/E3 count summaries, and overview A4 `Historical order` header. No unexpected original-cell changes were found. The old opening was relocated rather than discarded.

## Evidence and limits

Machine-readable independent checks and native read snapshots are in `independent_table_audit/`; `verify.py` reproduces the coverage, mapping, source-row, and preservation comparisons from those snapshots.

- Current mapping SHA-256: `3c2fa8d38a193a6109eec00ca992150024e8f22577fb458b798fc86e63ee39c1`
- Current-status delta SHA-256: `cb0733f521122872ed630f66276ae453bd9f2b4428625e086519270118d27b7e`
- Workflow-task delta SHA-256: `b24dd74d30f5a82687461a7cae0bbc0912c0aeabe3a342098ea89d787867e205`

No blocking gap was found in this read-only table QA. This is not a fresh proof review, literature-priority clearance, all-account file inventory, or benchmark certification. Native values and selected formatting were inspected; independent Google-rendered visual QA was not performed by this reviewer and remains separate from this content verdict.
