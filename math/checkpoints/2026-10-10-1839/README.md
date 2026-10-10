# Accepted theorem checkpoint

Frozen 10 October 2026. This is a new checkpoint; earlier sources and delivery archives remain unchanged.

## Repository export

This is a repository privacy export of the frozen accepted checkpoint. Original-source audits describe the unchanged frozen delivery and retain raw source hashes; SOURCE_MANIFEST.json describes restored repository-export bytes. Three source files have only private metadata removed. The original package and all prior archives remain unchanged locally. No mathematical statement, certificate, verdict or research code has been rewritten, run, imported or compiled. The included DOCX/TXT overview and historical source-verification receipts describe the frozen delivery. See **REPOSITORY_EXPORT.json** for exact source/export hashes and **SOURCE_MANIFEST.json** for reproducible restoration.

## Start here

Read **THEOREM_OVERVIEW.docx** for the six-page theorem overview. **THEOREM_OVERVIEW.txt** contains the same text. **ACCEPTANCE_STATUS.json** records the current verdicts. **SOURCE_INDEX.md** links every included source and supporting record.

The current accepted results are:

- For every odd N ≥ 23, the negative Fourier matrix has a representation by at most **2N − 2 floor((N + 10)/8) + 2 = 7N/4 + O(1)** individual permitted signed banks. The representation is over the splitting field of one monic polynomial in Q(q)[t], where q is a primitive Nth root in characteristic zero. No base-field splitting or scalar FFT complexity claim is made.
- The prefix-stabilizer optimum and recursive equality/counting theorem hold for all finite p-groups and all finite groups whose subgroups pairwise permute. **S3 has 360 labeled optimizers, of which 144 are nonhierarchical**, so the unrestricted structural extension is false. General-group upper bounds remain outside this checkpoint.
- The guarded necessary circuit has an exact **9-coordinate, 52-residual, 17-guard** representation, bijective with the accepted 12-coordinate circuit. This is not a solution, contradiction, dimension theorem, or sufficiency result for the original Fourier equations.

## Current acceptance and historical source wording

The frozen author filename AXIS_NONVANISHING_CANDIDATE.md and its provisional wording remain unchanged. The later independent review expressly accepts the generic-axis theorem and the uniform 7N/4 bank corollary. Other pending-review labels in author files are likewise historical. The following reviews determine this checkpoint's status:

- [Fourier zero-node review](sources/research_cycle_1830/zero_node_axis_review/INDEPENDENT_REVIEW.md) and [acceptance receipt](sources/research_cycle_1830/zero_node_axis_review/REVIEW_RECEIPT.json)
- [Nonabelian prefix review](sources/research_cycle_1833/nonabelian_review/INDEPENDENT_REVIEW.md) and [acceptance receipt](sources/research_cycle_1833/nonabelian_review/REVIEW_RECEIPT.json)
- [Guarded reduction review](sources/research_cycle_1828/forced_denominator_review/REPORT.md) and [acceptance receipt](sources/research_cycle_1828/forced_denominator_review/RECEIPT.json)

The new axis proof evaluates a polynomial minor at a zero-node degeneration, then intersects nonvanishing guards on the same monic affine slice. No counted bank uses the zero node. The rejected shortcut that legal reciprocal coprimality automatically gives full axis rank remains false. The older 9N/5 theorem and corrected direct-axis criterion are preserved.

## Exact source restoration

All mathematical content and all 121 logical source paths are preserved. Exactly 118 sources remain byte-identical; three remove only the private metadata listed in REPOSITORY_EXPORT.json. Small files can be read directly under **sources/**. Large raw certificates may be stored as their exact supplied gzip counterpart, or as a deterministic lossless gzip stream. SOURCE_MANIFEST.json records the source SHA-256 and byte count separately from the stored representation. Decompression is not a mathematical rewrite.

To check all reconstructed repository-export bytes without creating a source tree, run:

    python3 RESTORE_AND_VERIFY.py --verify-only

To create the repository-export source tree in a new directory, run:

    python3 RESTORE_AND_VERIFY.py --destination restored_sources

The destination must not already exist. The helper validates safe relative paths and all source hashes and never imports or executes the preserved research programs. An actual restoration of all 121 original source files was tested before freezing the delivery archive. The repository export is independently restored and checked against its source manifest before publication. Package checksums are in SHA256SUMS and PACKAGE_MANIFEST.json.

## Research Sheet evidence

The [final verified receipt](sources/research_sheet_1838/FINAL_VERIFICATION_RECEIPT.json) records the 18:41 UTC update: six append-only cells, all 6,038 native cell objects preserved, both tables and 178 catalogue IDs retained, and 18 source-comparison rows unchanged. Only the heights of rows 19–21 were repaired for visibility.

[Exact append text](sources/research_sheet_1838/EXACT_APPEND_TEXT.md), [content readback](sources/research_sheet_1838/CONTENT_READBACK_RECEIPT.json), [visual QA receipt](sources/research_sheet_1838/VISUAL_QA_RECEIPT.json), and five final rendered views are included. These views were rendered from the Google-generated XLSX export; they are not native-browser screenshots. SHEET_REFERENCE_AUDIT.json distinguishes included evidence from supporting workbook/manifest hashes checked locally but not duplicated here. The spreadsheet itself remains the canonical live record; the receipts freeze this particular update.

## Limits and verification

Historical novelty is unresolved. No efficient preparation algorithm, scalar FFT runtime, unrestricted bank minimum, or new original-system Fourier feasibility or impossibility result is asserted. Later eight-coordinate and seven-coordinate author work and ongoing general-group proofs are excluded.

The frozen package verifies raw source bindings, safe paths, byte-for-byte restoration, and preservation of earlier delivery archives. This repository export retains those raw provenance records and separately records its three metadata-only source differences. It does not execute inherited research or review programs or re-prove the entire predecessor history. The mathematical claims are bounded by the accepted reviews above.

### Historical digest caveat

A retained predecessor development-failure log records the digest of an obsolete checker version that is no longer available. Its historical run is not reproduced. The CHECKER_DEVELOPMENT_FAILURE.json record and accepted final checker remain byte-identical. All 293 path-bound hashes were verified against the frozen sources before export. The separate traceback log omits only three machine-local absolute path prefixes; its raw hash is retained. NAMED_HASH_FIELD_AUDIT.json separates this historical marker and two derived canonical-equation digests from verified source-file bindings. No accepted theorem or final review receipt relies on treating the unavailable development version as the accepted checker.
