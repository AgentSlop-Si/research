# Rebuilt open-record index — 15 October 2026

This is a **fresh native-snapshot rebuild** of the live Google Sheets `Research overview` tab. It was read directly through the Google Sheets connector after the earlier execution environment became unavailable. It is **not recovery of the original local 259-record category artifact**, is not asserted byte-identical to that artifact, and does not reproduce or independently validate its former semantic category counts.

This is **not a full proof audit** and **not a claim of 259 independent theories**. Rows may be related views, parent tasks, child scopes, implementation/replay obligations, source-access gates, or attribution work. Recorded acceptance language remains attributed to the Sheet; it was not newly proved or re-reviewed during this rebuild. No status, priority, mathematical scope, novelty, or speed claim is promoted here.

## Source and snapshot

- Workbook: [Research cycle — accepted proofs and live fusion queue — 10 October 2026](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit)
- Tab: `Research overview`, sheet ID `1731260011`
- Header row: 4; populated stable-ID rows: 5–331
- Bounded reads covered rows 5–337, confirming no additional stable-ID rows in the remaining six rows.
- Native connector reads completed: **2026-10-15T22:25:21.846Z**
- Source columns: B stable ID; D title; E status; I source-row labels and links; J recorded evidence links; L numeric priority; P next bounded action; Q pass/stop condition.
- These were bounded live reads, not an atomic version-pinned workbook export. The dates within individual fields remain the dates recorded in the workbook.
- The original Sheet was read only. Its complete rows and historical text remain unchanged.

## Verified structural counts

- 327 populated overview records with 327 unique stable IDs
- 259 records with exact status `TO RESEARCH`, exported here
- 68 records with exact status `CLOSED`, not exported here
- All 259 exported IDs are unique, all 259 priorities are finite numbers, and all 259 records have a nonempty recorded next action and recorded pass/stop condition.
- Exported priorities range from 8 to 60. These are work-priority scores, not probabilities of correctness or novelty.
- 251 exported records have at least one recorded source URL; 602 URL occurrences remain after per-record deduplication. All 259 have an overview-row URL.
- Eight records have no source URL in the inspected link fields/current evidence prefix: `STRUCTURED-RESIDUAL-EXECUTOR-20261012`, `PHASE56-COMPLEX-GREEN-N5-N8-20261011`, `QTORUS-CONNECTED-MINOR-20261013`, `ACWL-20261012`, `GTSL-20261012`, `Q2-DENSE-TORUS-20261013`, `GENERIC-FUSION-GATE-20261012`, `BORROWED-FOURIER-COMPILER-20261012`. Their empty URL arrays are explicit missing data, not fabricated links.

No semantic classification or independent-theory count is inferred from these counts.

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
| `recorded_current_gate` | Leading recorded block of column P, `Next bounded action`; an attributed next-action/gate, not an independently certified current verdict |
| `recorded_pass_stop_condition` | Leading recorded block of column Q, `Pass / stop condition`; retained separately because its date can lag P |
| `recorded_source_rows` | Column I source-row labels, unchanged |
| `recorded_source_urls` | Deduplicated links actually recorded in I/J link metadata, plus HTTP(S) URLs in the retained current J/P/Q prefixes; no missing source bodies inferred recovered |
| `overview_url` | Direct source overview-row navigation built from the observed workbook URL, sheet ID, and row number |

## Derivative-only history removal

The current-action and pass/stop fields are a compact derivative of the source cells:

1. Retain text before the first exact historical-section marker `Earlier dated history (preserved verbatim):`, trimming only surrounding whitespace.
2. If more than one line-start bracketed ISO-date heading remains in that prefix, retain only the first dated block and any leading preface. This removes an older appended dated block without rewriting the retained wording.
3. Preserve date labels, qualifications, limitations, and wording in the retained block. Do not paraphrase them into new claims.
4. Apply the same prefix extraction to J only for finding current evidence URLs; the full J narrative is not exported into this compact index.

This removed historical suffixes from 73 action cells and 50 condition cells. Full source history remains in the original workbook. Source-row link positions are a snapshot; stable IDs are the durable matching keys.

## Known date mismatch: Q16-related rows

For `STR-Q1`, `F016`, `FUS-09`, and `Q16`, P contains a later 14 October update saying the static/reference gate is complete and naming the production-wrapper/sparse-output and bounded real-API next action. Q still carries a 13 October condition. Both are preserved under separate **recorded** field names; the older Q text is not promoted to a newly current acceptance requirement. This rebuild does not silently repair the source or establish a later scientific verdict.

## Verification boundary

The rebuild checks source-row counts, unique stable IDs, exact status filtering, numeric priorities, nonempty extracted action/condition fields, and CSV/JSON content agreement. It does not reopen proof archives, run historical research programs, establish accessibility or validity of every linked source, deduplicate related theories, validate all scientific assertions, or recover the missing local artifact. Workbook access is still governed by its existing permissions.

