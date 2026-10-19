# C8 numerical-test ceiling and order-35 first-interior exclusion

This packet preserves two independently accepted, narrowly scoped results. It is a local publication candidate; independent packaging review and a separate release decision remain required. No external publication is claimed by this packet.

## Results

1. **C8, correction rank zero.** The maximal feasible parameter set for the declared relaxed strict numerical sufficient-condition test is exactly `0 < epsilon < epsilon_star`. Its unique positive limiting root is rigorously bracketed by `0.00000216382078575297666905178343251032596362320361` and `0.00000216382078575297666905178343251032596362320362`. The lower rational endpoint gives the strict bound `delta_(8,0) > sin(3*pi/16 + epsilon_minus/2)`, whose endpoint is approximately `0.555571132594891979835779216476`. Continuity gives the non-strict bound at the implicit method ceiling. The strict test does not admit the equality endpoint.
2. **Order 35.** No original binary fixed-Fourier-phase square mask has either full Gram equal to `dI` for `d=8,9,10,11,12,13`. With the separately accepted prime-`q>=11` theorem, this excludes the first interior `q<d<2q` at `N=5q` for every prime `q>5`. The valid rectangular degree-eleven row Gram is retained; its exact extension obstruction does not turn it into a square solution.

The C8 result finishes parameter tuning of the stated numerical test. It does not determine the actual global optimum, optimize every possible use of discarded proof slack, or prove non-equality between the optimum and the method ceiling. The order-35 result does not classify all order-35 or order-`5q` degrees or all support patterns. Both broad research owners remain open; no status, priority, score, discovery count, or canonical record is changed.

## Evidence and acceptance

- `c8_method/candidate/PROOF.md` and `c8_method/review/REVIEW.md` contain the new C8 proof and final independent review.
- `q7_boundary/candidate/REPORT.md` and `q7_boundary/review/REVIEW.md` contain the order-35 proof and final independent review.
- `FINAL_ACCEPTANCE.json` binds each proof, source manifest, final review, and final verdict by the exact original SHA-256 and byte count.
- `supporting_sources/` preserves complete manifested C8 strict-lower, upper, quantitative-lower, and prime-`q>=11` candidate/review evidence.
- `HISTORY_AND_SCOPE.md`, `CLAIM_SCOPE.json`, `OWNER_DISPOSITIONS.json`, and `ACCEPTED_RESULT_PRESERVATION.json` retain attribution, earlier results, and open work.

Immutable candidate files sometimes say that review is pending. That describes their creation stage. The exact final independent reviews bound in `FINAL_ACCEPTANCE.json` supply the current scoped scientific acceptance. The earlier prime-`q>=11` packet still says the `q=7` case is open; this new boundary result resolves only that historical open interval.

## Exact source preservation and transport

All twelve selected source manifests and their complete declared payloads are preserved. No proof, code, review, manifest, control, or source text is rewritten. Original local research-directory references inside scientific sources remain unchanged. `SOURCE_REFERENCE_MAP.json` maps the research package name and relative filename to the preserved content. It does not require access to those original directories.

Six source files are stored as lossless gzip+base64, including the complete 27,522,877-byte inherited negative controls, both copies of the complete 3,095,250-byte order-35 original-phase Grams, and two historical C8 review archives. `RESTORATION_LEDGER.json` lists every source's logical path, original SHA-256/length, stored path, and transport SHA-256/length. Decode base64, decompress gzip, then verify the original source hash. No evidence is shortened or replaced by a summary.

Run `python verify_package.py` from this directory for package integrity, source-manifest completeness, final acceptance, retained scope, and decoded-content privacy checks. This performs no mathematical experiment and imports or executes none of the scientific programs. To reconstruct the complete selected source trees in a new directory, run `python restore_sources.py OUTPUT_DIRECTORY`. Restoration verifies every source hash and rejects an existing output directory. Scientific scripts retain their original execution-path assumptions; source-tree restoration itself does not promise automatic relocation of every historical script.

`PRESERVATION_ALLOWLIST.json` defines the complete permitted public payload. `MANIFEST.json` binds every public file other than itself and `SEAL.json`; `SEAL.json` binds that manifest. `OMISSIONS.json` explicitly lists unmanifested exploratory/intermediate exclusions and the nonrecursive historical boundary. There are no omissions from the twelve selected manifests, no private administrative source snapshots, and no private document or conversation identifiers in the selected scientific bytes.

The local recovery tree, build scripts, source-path receipts, incomplete build staging, and operational handoff are outside this public allowlist. Only the allowlisted public directory is a publication candidate.
