# F020: uniform odd-leading +2 degrees

This clean package preserves the separately accepted proof and independent review for n=c p^r+2, prime p, odd 3<=c<p, r>=2, s>r, and every characteristic-zero primitive p^s-th root q. The original P/H polynomials, ordinary derivatives and original algebraic-square Christoffel-Darboux kernel are retained. The accepted c=3 +2 theorem is inherited, not newly credited; new coverage is odd 5<=c<p.

Both original polynomials are squarefree and the original kernel is nonzero at every P root. There are exactly cN high roots, including exactly one simple zero, plus exactly two shallow simple roots of valuation 1/2. Every high disk contains cL roots: (c-1)L boundary and L strict-interior roots; the central L includes the one zero. There is no extra zero outside the cN count. High ordinary derivative and kernel values are D+1 and N-p; shallow values are (cN+1)/2 and -2cB. Equal original monic discriminant valuations are cN(D+2)+1. Definitions and all quantifiers are preserved in SCOPE.json and the scientific reports. No r=2 exception remains, including c=11,p=13.

No arbitrary tails/intermediate digits, c>=p, r=1, s<=r, composite orders, exact deeper nonzero interior valuations, global F020/F023 closure, historical novelty, or FFT/complexity improvement is claimed. Finite controls are falsification diagnostics, not an infinite-family proof. Three of the author's five cyclotomic cases are low-X sections, not complete coefficient scans; the separate reviewer controls exclude omitted coefficients using raw edge-count bounds. Mathematical acceptance and independent public-byte acceptance are separate gates.

## Reading order and authority

1. SCOPE.json reproduces the entire accepted verdict and author scope. provenance/ACCEPTANCE_BINDING.json binds the exact frozen scientific packages, reports, independent derivation and verdict.
2. author/REPORT.md gives the proof. independent-review/INDEPENDENT_DERIVATION.md and INDEPENDENT_REVIEW.md give the independent argument; VERDICT.json states exactly what is accepted.
3. provenance/DEPENDENCIES.json is the active reading map. The accepted uniform odd-adjacent proof and review supply complete coefficientwise A, M, ordinary A-prime and M-prime profiles across the disks. Adjacent simplicity alone is not an input. Neither its exceptional second layer nor its deeper central-interior depths are imported into this +2 proof. The c3 +2 theorem is inherited. Additional historical authorities are explicitly inherited or attributed.
4. provenance/LOCATOR_VALIDATION.json exhaustively records active proof targets, comparison directories, actual historical archive expansion, separately named metadata projections, review snapshots, replay inputs/references, runtime outputs and public helper files. Every active delivered target has its exact identity checked. The verifier and ledger are root-manifest-bound to avoid circular self-hashes.
5. provenance/SOURCE_INVENTORY.json records every original retained file and deliberate omission, all named metadata projections and every retained or projected source inventory, including nested snapshot manifests. provenance/HISTORICAL_ARCHIVE_LEDGER.json classifies every original archived member and historical JSON files inventory. Every missing entry is qualified, rather than asserting closure of a partial tree. provenance/HISTORICAL_AUXILIARY_ROLES.json recursively inventories every historical JSON array carrying path, hash, byte-count, script, output, URL, URI or manifest declarations, including root arrays, nested verification receipts and historical replay mappings. Original declared identities are matched only by actual archived digest/size equality; literal historical paths are never guessed or rebound. Unresolved original identities, older/later public distinctions, inactive historical replay/omission/projection records and bibliography are explicitly classified. No such historical declaration creates a fresh execution, source-closure or retrieval claim.

## Preservation and explicit omissions

Every retained proof, review, scientific program, deterministic result, original manifest and seal is byte-for-byte original. No scientific code or mathematical result was edited. Historical pending-review language is preserved and resolved only by the later exact accepted verdict.

All source-binding files containing local execution-origin metadata, including nested and duplicated snapshots, are explicitly omitted with original sizes and hashes recorded. Separately named provenance/projections files preserve their nonprivate metadata and scientific source identities, deleting only enumerated local-origin fields. These are reading projections, not replacements claiming the omitted originals' hashes. Their inventories are exhaustively qualified as well.

Named runtime/environment/cold-replay/source-audit receipts, raw logs and host-bound source-audit tooling are omitted. The original historical comparison ZIP envelope is omitted because it contains raw runtime logs. All 455 original members are accounted for: 407 non-log members are expanded unchanged and 48 logs omitted. No replacement original archive hash or fresh historical execution is claimed. Historical original and later public report identities remain distinct.

Some inherited independent controls retain a directory named private/ because that is their original scientific source path. Only their six unchanged scientific scripts/results are included there; actual private execution diagnostics are excluded. Do not run original inventory or negative-control wrappers against intentionally partial exported source trees. Such wrappers and their historical instructions remain evidence, not the active public replay interface. Only the two current mathematical control programs below are replayed.

## Read-only reproduction

Use CPython 3.12, NumPy 2.3.5 and SymPy 1.14.0. Integrity uses the standard library. Replay additionally requires Linux x86-64, bubblewrap and kernel seccomp, with no weaker fallback.

From the extracted package directory:

    python -I -B tools/verify.py --negative-controls
    python -I -B -O tools/verify.py --negative-controls

Set ARCHIVE to the supplied canonical ZIP, DIGEST to its independently trusted SHA-256, and OUTPUT to a new directory outside this package. A hash computed from the same untrusted ZIP is not an independent trust anchor.

    python -I -B tools/verify.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST"
    python -I -B tools/replay.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST" --output "$OUTPUT"

Replay verifies and safely extracts that exact ZIP, mounts input read-only, hides original host input locations, and blocks Python/native socket, network and io_uring calls. It runs both unchanged current scientific programs under actual normal and optimized Python. The author emits its sealed JSON to stdout; the adapter captures those exact bytes as its result without altering the scientific program. The reviewer writes its requested JSON, emits no stdout, and emits five fixed completion lines to stderr. All four result comparisons and all stdout/stderr comparisons are byte-exact, with no timing, numeric, formatting or content exceptions. Optimization semantics, native network denial, input-write denial and final frozen input identity are independently checked.

Fresh results and raw runtime receipts stay outside the delivery. Success requires terminal REPLAY_RESULT.json status PASS. Running, failed, interrupted and uncatchably killed runs never establish success.

Choose a different new external directory for real failure/interruption/no-clobber controls:

    python -I -B tools/failure_controls.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST" --output "$FAILURE_OUTPUT"

These controls complete a real successful replay and then reject reuse without changing earlier receipts. Actual nonzero launchers, timeout, termination and uncatchable interruption are exercised. Failed-run receipts are also preserved on rejected reuse. Resource limits are disclosed in REPLAY_POLICY.json. Independent auditing may additionally kill an actual scientific child and exercise archive/locator adversarial cases without altering the frozen input.

The canonical ZIP uses sorted regular files, ZIP_STORED, fixed 1980 timestamps and regular mode 0644, with no comments, extras, duplicates, symlinks, prefix, suffix or hidden records. SHA-256 establishes byte identity, not theorem truth or author authentication. This producer package does not self-certify independent public-byte acceptance.
