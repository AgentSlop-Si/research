# Rebuilt open-record index — 15 October 2026

Updated **15 October 2026 at 2026-10-15T23:56:51.814Z**, from fresh native reads after the 23:42 source/gate cycle, including the F021, N256, ALG-028, and ALG-065 prefixes. This refresh replaces the existing three derivative files in place; earlier snapshots remain available through Git history.

This is a **fresh native-snapshot rebuild** of the live Google Sheets `Research overview` tab, read directly through the Google Sheets connector. It remains a separate derivative from the original 259-record category inventory and is not asserted byte-identical to it; this refresh does not reproduce or independently validate that inventory's semantic category counts.

The original inventory was previously inaccessible during an execution-workspace outage, then recovered and archived at [commit e5c9c53f7d34e8d858e781d2d5321393aec7e85c](https://github.com/AgentSlop-Si/research/commit/e5c9c53f7d34e8d858e781d2d5321393aec7e85c). Its [preserved original files](https://github.com/AgentSlop-Si/research/blob/e5c9c53f7d34e8d858e781d2d5321393aec7e85c/math/archives/2026-10-15-recovered-pending-artifacts/original-category-inventory-2202/README.md) describe the historical 22:02:36–22:02:51 UTC snapshot. Earlier statements that those inventory bytes were inaccessible describe the earlier outage and are superseded for the recovered files. That archival recovery is distinct from this later live-row derivative and does not establish recovery or verification of every mathematical source referenced by the records.

This is **not a full proof audit** and **not a claim of 259 independent theories**. Rows may be related views, parent tasks, child scopes, implementation/replay obligations, source-access gates, or attribution work. Recorded acceptance language remains attributed to the Sheet; it was not newly proved or re-reviewed during this refresh. No status, priority, mathematical scope, novelty, or speed claim is promoted here.

## Source and snapshot

- Workbook: [Research cycle — accepted proofs and live fusion queue — 10 October 2026](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit)
- Tab: `Research overview`, sheet ID `1731260011`
- Header row: 4; populated stable-ID rows: 5–331
- Bounded reads covered rows 5–337, confirming no additional stable-ID rows in the remaining six rows.
- Native connector reads completed: **2026-10-15T23:56:51.814Z**
- Source columns: B stable ID; D title; E status; I source-row labels and links; J recorded evidence links; L numeric priority; P next bounded action; Q pass/stop condition.
- Link reads include `textFormatRuns`, whole-cell `userEnteredFormat.textFormat.link`, and `hyperlink`. Whole-cell links normalized by Sheets are retained.
- These were bounded live reads, not an atomic version-pinned workbook export. The dates within individual fields remain the dates recorded in the workbook.
- This derivative refresh only read the original Sheet. Its complete rows and historical text were not changed by the refresh.

## Verified structural counts

- 327 populated overview records with 327 unique stable IDs
- 259 records with exact status `TO RESEARCH`, exported here
- 68 records with exact status `CLOSED`, not exported here
- All 259 exported IDs are unique, all 259 priorities are finite numbers, and all 259 records have a nonempty recorded next action and recorded pass/stop condition.
- Exported priorities range from 8 to 60. These are work-priority scores, not probabilities of correctness or novelty.
- All 259 exported records have at least one recorded URL; 628 URL occurrences remain after per-record deduplication. All 259 also have an overview-row URL.
- Records with an empty `recorded_source_urls` array: **none**.
- Against the preceding 22:56 version of this index, five exported records have changed recorded text or URLs: `F021`, `N256-FULL-MODEL-20261011`, `N256-SOLVER-SATURATION-20261011`, `ALG-028`, and `ALG-065`. This covers five next-action prefixes, two pass/stop prefixes, and three additional primary-source URLs across two records. Exported stable IDs, titles, statuses, priorities, row positions, source-row labels, and overview URLs are unchanged.

No semantic classification or independent-theory count is inferred from these counts.

## Recorded URLs and their limits

The 22:56 refresh filled eight previously empty URL arrays with the actually recorded links to the owning `Incoming queue` rows. The current snapshot retains those owner-row navigation repairs. These links are read from native cell metadata rather than inferred from a label.

Owner-row navigation and exact source/audit evidence are different. An owning Sheet-row URL is a pointer to the row containing the record and its context; it is not a recovered proof body, an independent audit, or evidence that every referenced archive is accessible. The `recorded_source_urls` array deliberately preserves the existing schema and can contain both kinds of recorded URL. An empty-array count of zero does not establish complete exact-source coverage.

For `QTORUS-CONNECTED-MINOR-20261013` and `Q2-DENSE-TORUS-20261013`, the arrays also retain the commit-pinned audit or audit-archive links recorded by the 22:56 refresh. The six other formerly empty arrays contain owner-row navigation only: `STRUCTURED-RESIDUAL-EXECUTOR-20261012`, `PHASE56-COMPLEX-GREEN-N5-N8-20261011`, `ACWL-20261012`, `GTSL-20261012`, `GENERIC-FUSION-GATE-20261012`, and `BORROWED-FOURIER-COMPILER-20261012`. No exact source or audit URL is invented for them.

## Files

- `open-record-index.csv`: UTF-8, comma-separated, header plus 259 records; RFC-style quoting and CRLF record separators. Text fields can contain quoted newlines. `recorded_source_urls` is a JSON array encoded within the CSV field.
- `open-record-index.json`: UTF-8 JSON object with snapshot/source metadata, structural counts, and a `records` array containing the same 259 records in the same order.
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

This removed historical suffixes from 78 action cells and 52 condition cells. Full source history remains in the original workbook. Source-row link positions are a snapshot; stable IDs are the durable matching keys.

A brief source-access reconciliation prefix can refer to unchanged engineering gates without restating them. In particular, `ENGINEERING-NTT-BASELINE-20261012` retains the recorded 15 October source-access prefix exactly as written. This index does not invent a remaining-gate list from that prefix or treat it as closure of the engineering parent. Follow `overview_url` to the complete row and its retained history.

## Dates and updated Q16 pass/stop text

For `STR-Q1`, `F016`, `FUS-09`, and `Q16`, P still contains the recorded 14 October update. Q now contains the recorded 15 October pass/stop reconciliation from the 14 October scoped reviews, including the production coefficient/association and authorized bounded real-API gate. The initial 22:25 index's 13 October Q prefix was superseded in the native cells before the 22:56 refresh and is preserved in their history; this refresh retains that later Q text.

P and Q remain separate attributed fields. Older dates elsewhere are retained as written; they are not silently recast as new acceptance requirements. No proof, implementation, or novelty conclusion is established by this refresh.

## Verification boundary

The refresh checks source-row counts, unique stable IDs, exact status filtering, finite numeric priorities, nonempty extracted action/condition fields, unchanged exported statuses/scores, exact recorded-link extraction, CSV/JSON round-trip content agreement, and UTF-8 Git blob readback. It does not reopen proof archives, run historical research programs, establish accessibility or validity of every linked source, deduplicate related theories, validate all scientific assertions, or reconstruct the separately archived historical inventory. Workbook access is still governed by its existing permissions.
