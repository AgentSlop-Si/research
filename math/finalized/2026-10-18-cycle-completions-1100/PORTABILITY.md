# Publication-copy identity and portability

This packet preserves scientific code, certificates, reports, and completed review evidence. It is a publication copy, not a fresh scientific execution.

## Original versus public bytes

`COPY_BINDINGS.json` records the SHA-256 and byte length of every original selected input and its public copy. Byte-identical files are explicitly marked. Complete original text/code/certificate bytes, original manifests and seals, and private source locators are retained locally outside the publication allowlist. Do not upload the private sibling directory.

Original author reports and final reviews retain their original hashes and statements wherever no explicit privacy change is needed. Review acceptance attaches to original inspected bytes. A regenerated public manifest or seal establishes publication integrity only; it does not retrospectively change the evidence in a historical results file.

## Executable path adaptations

Only the following review input-location expressions are adapted:

- Centering review: the live candidate path becomes the sibling `candidate` directory. The separately frozen `candidate_snapshot` remains distinct.
- Degree-eleven review: the default candidate input becomes the review's frozen inert `inputs` directory. An explicit command-line input path remains supported.
- Affine-run review: the candidate path becomes the sibling `candidate` directory.
- Fourier-rectangle review: the source path becomes the sibling `candidate` directory.

These changes affect paths, not scientific arithmetic, assertions, seeds, counters, or test domains. The original source text for each adaptation is retained locally and its original hash is public. Candidate production code is unchanged by packaging. The affine candidate already contains an inherited portable jump dependency; its existing source binding discloses that earlier adaptation separately.

## Omitted private source context

Two Fourier-rectangle source-context JSON files contained copied research-register cells and spreadsheet locators. Their public files are clearly labelled omission stubs with a pinned public repository index link and original file hash. The raw context is not published. Mathematical reports, independent scientific results, and the pinned Phase7 mathematical source remain intact.

Private absolute paths in inert traceback logs are replaced by package-relative spellings. The degree-eleven review candidate-directory metadata is also made relative. Review-assignment documents are omitted because they are not scientific deliverables. Compiled executables, bytecode, caches, and temporary runtime files are excluded.

## Manifests, seals, and reproduction

A source manifest is retained unchanged when its entire declared public file set is byte-identical. When a listed file is adapted or omitted, only the affected public manifest entries and any corresponding manifest-hash seal are rebound; each carries an explicit publication-copy notice. Historical dependency manifests remain original documentary evidence. Recorded receipts retain original scientific execution identities and must not be interpreted as runs against adjusted public manifests.

`PACKAGING_CHECKS.json` lists the actual modified code files and packaging checks. Packaging parses Python syntax but neither imports nor runs scientific programs. The top-level verifier checks file bytes and the exact publication allowlist only.

Run scientific reproduction in a disposable copy because checkers commonly overwrite receipts. Some retained historical dependencies are documentary flattened copies, not complete executable dependency distributions. The fresh candidate and review entrypoints are identified in their respective README or report. Any reproduction in a new environment is a new run and must be recorded as such.
