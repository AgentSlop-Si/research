# Verified singleton-scope and Q29 normalization table sync

Completed 14 October 2026, with final native readback verified at 11:55:47 UTC.

The existing research spreadsheet was updated in place: 19 text cells across six existing tabs, in three guarded batches. No replacement spreadsheet or tab was created.

## Results recorded

- Eleven signed-bank views now record the accepted source-bound logical synthesis: physical-bank minima 14 over F23, 13 over F23 cubed, and 12 over F23 to the fifth power, for N=11 and q=13 with exactly one effective alpha node per cross-sign orientation and independently free locations. Arbitrary legal beta is retained. The degree-five equality combines the accepted lower bound with its literal witness. Pinned-(4,4), unrestricted-allocation, novelty and FFT-speed claims remain separate or open.
- Eight Q29 views now record the independently accepted exact R843 kernel and shared-center normalization: the entire F(Y)=pi^(-60) U1687(-1-pi Y;q) modulo pi^140, justified by exact carry-basis conversion, reciprocal transfer, content 60 and guarded division. Discriminant/nonvanishing, repeated branches, the other 26 primary centers and full Q29 remain open.

## Preservation and verification

The live prewrite snapshot matched the saved 19,795-cell baseline and spreadsheet metadata exactly. Each batch re-read its cells and stable identifiers immediately before writing. The only field mask used was `userEnteredValue,textFormatRuns`.

The final full native comparison passed:

- 19,795 cells compared, exactly 19 intended text changes, no unexpected differences
- All earlier cell text preserved verbatim
- All 30 existing rich-text source-link spans in the edited cells preserved
- 49 new source-link spans, bound to five immutable GitHub source URLs
- No numeric, score, formula, native format, validation or note changes
- Spreadsheet metadata and the three earlier rich-link repairs preserved

The five immutable source paths were checked against publication receipts with exact text readbacks. Publication commits are e87b42a749a8b369aace3e0395a5f430e062d262 and 28c41ed94d7c433f56ee12b1fd311ec271f65c97.

## Visual boundary

A read-only XLSX export was rendered for the six edited tabs. The new notes are present. Established fixed row heights clip long content, including some tails of new overview notes; the full content remains stored and available by opening the cell. Native dimensions and styling were intentionally preserved. The export renderer does not faithfully reproduce every Google Sheets rich-text style, so the exact native cell and link-span comparisons are the authoritative preservation evidence. No layout or additional spreadsheet edits followed verification.

## Evidence

`FINAL_AFTER_VERIFICATION.json` is the final machine-readable result. `IMMUTABLE_SOURCE_VERIFICATION.json` records the five source bindings. The original full preservation archive contains the prewrite proposal, live and final snapshots, three exact requests, guard checks, receipts and readbacks, verification code, and sampled export renders. This public compact receipt contains selected verification records and hashes of the full original evidence; it does not publish the full spreadsheet snapshots or renders. Prewrite documents retain their historical not-applied status; this report and the final verification supersede that status.

Spreadsheet identity and private access URL are retained in the original preservation archive.
