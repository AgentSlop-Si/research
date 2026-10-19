# Quantitative sketch rank and the order-5q first interior

This local publication packet preserves two independently accepted, limited results. It has not been published, and independent packaging review is still pending. Both owners remain **TO RESEARCH, priority 42**.

## 1. ALG-076: quantitative retained-rank obstruction

For input-independent complex linear measurements of rank at most k<N, with independent random seeds and arbitrary measurable nonlinear decoding, a standard complex Gaussian input has absolute-error success probability at most G_(N-k)(a²). This bound is sharp at fixed rank. The relative-error consequence is necessary and is not claimed sharp: fixed 0<epsilon<1 and nonvanishing uniform success require liminf k/N >= 1-epsilon².

The source-bound unaugmented v6 interface has k<=RK and N=KM. The resulting R/M constraint restores order-N-log-N executed butterfly work only for its stipulated ordinary dyadic evaluator. This is not a general Fourier lower bound or an FFT improvement. Adaptive information, uncounted side information, finite discrete inputs and changed evaluators require separate analysis.

The almost-everywhere exact-recovery endpoint was already accepted. Classical Gaussian conditioning and Anderson's centered-ball inequality retain their attribution; the original Anderson paper was not reread due to access limits. The complete elementary derivation and the checked source qualifications remain in the unchanged proof and review.

Read `alg076/candidate/REPORT.md` and `alg076/review/REVIEW.md`.

## 2. M-SPARSE-DEFECT: order-5q first-interior exclusion

For every prime q>=11 and integer q<d<2q, no binary square mask R makes D[r,c]=R[r,c] zeta_(5q)^(rc) satisfy both complete Gram identities dI. The five-coordinate triangle/near-pencil incidence repair is preserved in the proof.

This does not settle q=7, the interval 2q<=d<=4q, or a complete N=5q classification. The exact q=7 control is a rectangular 7-by-35 row block with row Gram 11 I7, never a square equality mask. The inherited inverse-row consequence is strict separation above sqrt(d/(5q)), with the inherited nonsharp squared bound d/(5q)+1/[50q d^(4q-5)]. No exact optimum or optimal rate is asserted.

Classical cancellation is credited to de Bruijn and Lam–Leung. The earlier N=3q, N=2q and prime-power classifications, divisor constructions, connected order-eight countercontrol, and all other accepted sparse-inverse results remain intact.

Read `fiveprime/candidate/REPORT.md` and `fiveprime/review/REVIEW.md`.

## Integrity, privacy and historical labels

- The four original manifests and both final review bindings are unchanged. All scientific source content is preserved. There are 63 exact source-file copies and one explicitly recorded reversible gzip/base64 representation; no scientific text is redacted. Pending-review labels in candidate documents record their historical creation stage; final reviews determine current scoped acceptance.
- One administrative ALG-076 owner snapshot is omitted publicly because it contains private workbook identifiers and row locations. Its original manifest entry and review receipt remain unchanged. `OMISSIONS.json` records its exact hash and size, and the verifier explicitly validates the omission. The complete original file and all 65 source files are preserved in a separate local recovery tree. That private tree is not part of this public payload.
- Original research paths are retained inside immutable source documents. `SOURCE_REFERENCE_MAP.json` maps preserved file bytes into this tree. The embedded earlier N=3q manifest is a historical reference; it is not a claim that every deeper historical dependency is republished here.
- `LARGE_FILE_NOTICE.json` and `LOSSLESS_REPRESENTATIONS.json` identify the 27,522,877-byte negative-control JSON represented as 498,413 bytes of gzip/base64 text. The full original remains unchanged locally. The verifier decodes in memory and checks the original SHA-256 and byte length against the unchanged candidate manifest. External upload and actual-body readback remain unperformed.
- Existing mathematical programs and saved control outputs are inert evidence. No mathematical program was rerun or imported during packaging. Historical reproduction commands in source READMEs are preserved as text; running them in a sealed tree would change its evidence.

Run `python verify_package.py` from this directory for the read-only packaging checks. The verifier uses Python's standard library only, checks the exact allowlist, original source anchors, omission ledger, scientific acceptance bindings, scope limits and owner dispositions, and does not import research code. Use the externally recorded manifest and seal hashes to identify this exact packet.

To restore the full negative-control JSON without modifying this packet, run `python restore_controls.py /path/outside/this/packet/NEGATIVE_CONTROLS.json`. The destination must not exist. The standard-library script verifies encoded and decoded hashes and byte lengths before writing. Preserve the encoded file as the publication artifact; a restored JSON is a separate exact research copy. The historical ALG-076 checks script also expects the omitted administrative owner record, so full historical reruns require the complete local recovery tree rather than this privacy-limited publication tree. No rerun is needed for package verification.

There is no worldwide-priority, world-first, general FFT gain, owner-closure or production-implementation claim.
