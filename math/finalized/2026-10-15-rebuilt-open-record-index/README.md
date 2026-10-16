# Rebuilt open-record index — 16 October 2026

Updated **16 October 2026 at 2026-10-16T08:12:57.806Z**, from fresh native reads after the independently reviewed ALG-007, ALG-011 and ALG-013 comparison updates. The derivative now contains **254 open records, 73 closed records and 327 total overview records**. ALG-011 and ALG-013 changed to CLOSED in the native workbook; ALG-007 remains open with revised recorded work. All priorities, record positions and the index schema are unchanged. Earlier snapshots remain historical; the established derivative files are replaced in place and Git history preserves preceding versions.

This is a **fresh native-snapshot rebuild** of the live Google Sheets `Research overview` tab, read directly through the Google Sheets connector. It remains a separate derivative from the original 259-record category inventory and is not asserted byte-identical to it. This refresh does not reproduce or independently validate that inventory's semantic category counts.

The original inventory was previously inaccessible during an execution-workspace outage, then recovered and archived at [commit e5c9c53f7d34e8d858e781d2d5321393aec7e85c](https://github.com/AgentSlop-Si/research/commit/e5c9c53f7d34e8d858e781d2d5321393aec7e85c). Its [preserved original files](https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/archives/2026-10-15-recovered-pending-artifacts/original-category-inventory-2202/README.md) describe the historical 22:02:36–22:02:51 UTC snapshot. Earlier access-failure statements are superseded for those recovered files. That archival recovery is distinct from this later live-row derivative and does not establish recovery or verification of every mathematical source referenced by the records.

This is **not a full proof audit** and **not a claim of 254 independent theories**. Rows may be related views, parent tasks, child scopes, implementation/replay obligations, source-access gates or attribution work. Recorded acceptance language remains attributed to the Sheet; it was not newly proved or re-reviewed during this index refresh. Progress wording is copied from the Sheet at its stated scope; this derivative records the independently accepted native status changes without making status decisions. This derivative does not independently promote any mathematical scope, priority, novelty or speed claim.

## Source and snapshot

- Workbook: [Research cycle — accepted proofs and live fusion queue — 10 October 2026](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit)
- Tab: `Research overview`, sheet ID `1731260011`
- Header row: 4; populated stable-ID rows: 5–331
- Bounded reads covered rows 5–337, confirming no additional stable-ID rows in the remaining six rows.
- Native connector reads completed: **2026-10-16T08:12:57.806Z**, after the round's native write receipt and independent postwrite acceptance.
- Source columns: B stable ID; D title; E status; I source-row labels and links; J recorded evidence links; L numeric priority; P next bounded action; Q pass/stop condition.
- Link reads include `textFormatRuns`, whole-cell `userEnteredFormat.textFormat.link` and `hyperlink`. Whole-cell links normalized by Sheets are retained.
- These were bounded live reads, not an atomic version-pinned workbook export. A final ID/status/priority sentinel read confirmed the same census. Dates within individual fields remain those recorded in the workbook.
- The index refresh only read the original Sheet. Its complete rows and historical text were not changed by the refresh.

## Verified structural counts

- 327 populated overview records with 327 unique stable IDs
- 254 records with exact status `TO RESEARCH`, exported here
- 73 records with exact status `CLOSED`, not exported here
- All 254 exported IDs are unique, all priorities are finite numbers, and every exported record has a nonempty recorded next action and pass/stop condition.
- Exported priorities range from 8 to 60. These are work-priority scores, not probabilities of correctness or novelty.
- All 254 exported records have at least one recorded source URL; 640 URL occurrences remain after per-record deduplication. All also have an overview-row URL.
- Records with an empty `recorded_source_urls` array: **none**.
- Baseline: the 16 October 01:57:05 UTC snapshot at [commit 8172ebf0](https://github.com/AgentSlop-Si/research/commit/8172ebf0371ef83a6c5aaa2de778358c89088b22).
- Every one of the 327 stable IDs, priorities and row positions is unchanged. Exactly two statuses changed from `TO RESEARCH` to `CLOSED`: `ALG-011` (row 54) and `ALG-013` (row 55). Those two records leave the open index; no ID was added to or removed from the workbook.
- All 254 retained open records preserve their relative order, titles, statuses, priorities, source-row labels and overview URLs. Only `ALG-007` (row 50) changed extracted progress/evidence fields: `recorded_current_gate`, `recorded_pass_stop_condition`, `recorded_source_urls`; 1 added and 0 removed recorded URL occurrences under the unchanged extraction policy.
- The JSON scope disclaimer's current-record count changes from 256 to 254. All other scope wording and all selection, source and extraction metadata are unchanged.

`ALG-011` and `ALG-013` are recorded CLOSED following whole-record scope review. `ALG-007` remains open with its surviving recorded obligations. All three retain priority 42. The [published comparison round](https://github.com/AgentSlop-Si/research/blob/5e0c68bcb97f3ead9b02b782c4a24eefcc07b4d6/math/finalized/2026-10-16-comparisons-0743/README.md) contains the source-bound author reports and independent reviews. This index reports the accepted native dispositions without adding a mathematical proof, novelty claim or implementation claim.

## Historical and current counts

The original archived 15 October 22:02 inventory and rebuilt snapshots through 16 October 00:15 recorded 259 open rows and 68 closed rows. The 00:32 snapshot recorded 258/69 after the scoped `M-WEYL-TWIRL` closure. The 00:59 snapshot recorded 257/70 after the additional scoped `ALG-MONOMIAL-CENTRALIZER` closure. The 01:24 snapshot recorded 256/71 after the scoped `M-SEED-BALANCE` closure and progress for ALG-018, ALG-019, M-QUADRATIC-FEEDBACK and M-SPECTRAL-FEEDBACK. The 01:57 snapshot remained 256/71 and changed only the ALG-WEIL-LOCAL and ALG-009 progress/evidence fields; it added no closure. The current 2026-10-16T08:12:57.806Z snapshot records 254/73 after ALG-011 and ALG-013 were closed and ALG-007 received a remaining-work update; all priority scores were preserved. All are preserved historical snapshots. The directory name stays unchanged so the derivative keeps its established location.

### Previous 01:57 update, retained for historical context

`ALG-WEIL-LOCAL` and `ALG-009` remain open at priority 42. The former carries a bounded Weil-shear arithmetic correction; the latter carries a static resonance-guard candidate and a completed, qualified-nonmatch comparison with Kaltofen–Yang 2007. Their source-execution, applicable hybrid/field/root/accounting and broader historical-priority obligations remain separate and open. The [published scientific round](https://github.com/AgentSlop-Si/research/blob/0b6689043c922f1cbcd9f1f1acf0cbd408c4a588/math/finalized/2026-10-16-source-repairs-0126/README.md) contains the source-bound reports and independent reviews. This index attributes the native progress wording without establishing new mathematical acceptance, novelty or implementation coverage.

## Recorded URLs and their limits

The 22:56 refresh filled eight previously empty URL arrays with the actually recorded links to the owning `Incoming queue` rows. The current snapshot retains those owner-row navigation repairs. These links are read from native cell metadata rather than inferred from a label.

Owner-row navigation and exact source/audit evidence are different. An owning Sheet-row URL is a pointer to the row containing the record and its context; it is not a recovered proof body, an independent audit, or evidence that every referenced archive is accessible. The `recorded_source_urls` array deliberately preserves the existing schema and can contain both kinds of recorded URL. An empty-array count of zero does not establish complete exact-source coverage.

For `QTORUS-CONNECTED-MINOR-20261013` and `Q2-DENSE-TORUS-20261013`, the arrays also retain the commit-pinned audit or audit-archive links recorded by the 22:56 refresh. The six other formerly empty arrays contain owner-row navigation only: `STRUCTURED-RESIDUAL-EXECUTOR-20261012`, `PHASE56-COMPLEX-GREEN-N5-N8-20261011`, `ACWL-20261012`, `GTSL-20261012`, `GENERIC-FUSION-GATE-20261012`, and `BORROWED-FOURIER-COMPILER-20261012`. No exact source or audit URL is invented for them.

## Files

- `open-record-index.csv`: UTF-8, comma-separated, header plus 254 records; RFC-style quoting and CRLF record separators. Text fields can contain quoted newlines. `recorded_source_urls` is a JSON array encoded within the CSV field.
- `open-record-index.json`: UTF-8 JSON object with snapshot/source metadata, structural counts, and a `records` array containing the same 254 records in the same order.
- `README.md`: this provenance, scope, extraction, and schema note.

## Schema

| Field | Source / meaning |
| --- | --- |
| `stable_id` | Column B; exact stable ID, retained as a string |
| `title` | Column D, `Research or stage` |
| `status` | Column E; exact `TO RESEARCH` |
| `priority` | Column L; numeric work-priority value, unchanged |
| `overview_row` | One-based source row at snapshot time; not a permanent key |
| `recorded_current_gate` | Leading recorded block of column P, `Next bounded action`; attributed text, not an independently certified or necessarily complete current verdict |
| `recorded_pass_stop_condition` | Leading recorded block of column Q, `Pass / stop condition`; retained separately because its date can differ from P |
| `recorded_source_rows` | Column I source-row labels, unchanged |
| `recorded_source_urls` | Deduplicated HTTP(S) links actually recorded in I/J `textFormatRuns`, whole-cell `userEnteredFormat.textFormat.link`, or `hyperlink` metadata, plus HTTP(S) URLs in the retained J/P/Q prefixes; owning-row links do not imply source-body recovery |
| `overview_url` | Direct full source overview-row navigation built from the observed workbook URL, sheet ID, and row number |

## Derivative-only history removal

The current-action and pass/stop fields are a compact derivative of the source cells:

1. Retain text before the first exact historical-section marker `Earlier dated history (preserved verbatim):`, trimming only surrounding whitespace.
2. If more than one line-start bracketed ISO-date heading remains in that prefix, retain only the first dated block and any leading preface. This removes an older appended dated block without rewriting the retained wording.
3. Preserve date labels, qualifications, limitations, and wording in the retained block. Do not paraphrase them into new claims.
4. Apply the same prefix extraction to J only for finding current evidence URLs; the full J narrative is not exported into this compact index.

This removed historical suffixes from 91 action cells and 67 condition cells. Full source history remains in the original workbook. Source-row link positions are a snapshot; stable IDs are the durable matching keys.

A brief source-access reconciliation prefix can refer to unchanged engineering gates without restating them. In particular, `ENGINEERING-NTT-BASELINE-20261012` retains the recorded 15 October source-access prefix exactly as written. This index does not invent a remaining-gate list from that prefix or treat it as closure of the engineering parent. Follow `overview_url` to the complete row and its retained history.

## Dates and updated Q16 pass/stop text

For `STR-Q1`, `F016`, `FUS-09`, and `Q16`, P still contains the recorded 14 October update. Q now contains the recorded 15 October pass/stop reconciliation from the 14 October scoped reviews, including the production coefficient/association and authorized bounded real-API gate. The initial 22:25 index's 13 October Q prefix was superseded in the native cells before the 22:56 refresh and is preserved in their history; this refresh retains that later Q text.

P and Q remain separate attributed fields. Older dates elsewhere are retained as written; they are not silently recast as new acceptance requirements. No proof, implementation, or novelty conclusion is established by this refresh.

## Verification boundary

This refresh checks source-row counts, unique stable IDs, exact status filtering, finite numeric priorities, nonempty extracted action/condition fields, exactly the two accepted status changes against the prior snapshot, unchanged priorities and positions for all 327 records, retained open-record progress confined to ALG-007, exact recorded-link extraction and CSV/JSON round-trip content agreement. The companion validation receipt records file hashes and the structural delta; publisher readback is a separate verification step.

It does not reopen proof archives, run historical research programs, establish accessibility or validity of every linked source, deduplicate related theories, validate all scientific assertions or reconstruct the separately archived historical inventory. Workbook access remains governed by its existing permissions. Private native-cell snapshots, notes and preimages are not included in the publication files.
