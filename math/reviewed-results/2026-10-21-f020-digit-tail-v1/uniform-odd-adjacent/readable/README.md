# F020: uniform odd-leading adjacent degrees

This clean package preserves the separately accepted proof and independent review for n=c p^r+1, p prime, odd 3<=c<p, r>=2, s>r, and every characteristic-zero primitive p^s-th root q. It concerns the original P/H polynomials, ordinary derivatives, and original algebraic-square Christoffel-Darboux kernel.

Both original polynomials are squarefree and the original kernel is nonzero at every P root, including every genuine r=2 exceptional residue. The accepted c=3 result and single-leading-digit inputs are inherited, not newly credited. The even second-layer scalar mechanism is attributed; all odd-parity adaptations are proved anew. The off-root operator is J=XP'_n-P_n=t^S(2U f_U-f). A global bound on f_U alone would be false; the stated f_U bound is at roots only.

No c>=p, even leading digit as a new result, r=1, s<=r, arbitrary tail or intermediate digits, exact individual r>=3 strict-interior depths, composite order, global F020/F023 closure, historical novelty, or FFT/complexity improvement is claimed. Finite controls are falsification diagnostics, not an infinite-family proof. Mathematical acceptance and independent public-byte audit are separate; this package does not self-accept its packaging.

## Reading order and exact authority

1. SCOPE.json reproduces the entire final accepted verdict and author claim. provenance/ACCEPTANCE_BINDING.json binds both immutable scientific packages, reports, and verdict.
2. author/REPORT.md is the complete proof. independent-review/INDEPENDENT_REVIEW.md supplies the separate argument and audit; independent-review/VERDICT.json states the exact accepted scope, conclusions and exclusions.
3. provenance/DEPENDENCIES.json provides the full active reading map. It includes the inherited c3 proof and review, accepted single-leading-digit authority, and attributed even scalar-mechanism reports. Its archive-reading adapter points to the actual expanded original historical tree.
4. provenance/LOCATOR_VALIDATION.json exhaustively checks every declared active proof target, scope-reference directory, archive/metadata reading adapter, review snapshot, replay script, replay input/reference, and public helper. Every target exists with its exact delivered identity. The verifier and this ledger are bound through the root manifest rather than an impossible circular self-hash.
5. provenance/SOURCE_INVENTORY.json records original and delivered identities, all deliberate omissions, all separate metadata projections, and every retained JSON files/source_files/sources inventory including renamed snapshot manifests. provenance/HISTORICAL_ARCHIVE_LEDGER.json qualifies every original archived member and JSON files inventory. Historical original and later public report hashes remain distinct.

## Preservation and omission policy

Every retained proof, review, script, mathematical result, manifest and seal is byte-for-byte original. No scientific code or result is edited. Historical author-era pending-review language is retained, and the later independent verdict resolves it only within its stated scope.

The original author SOURCE_BINDINGS.json, reviewer SOURCE_BINDING.json, and duplicate reviewer author-binding snapshot contain local execution-origin metadata. Those original files are omitted with their exact original sizes and hashes recorded. Three separately named files in provenance/projections retain their nonprivate metadata and mathematical source identities, removing only the explicitly listed local-origin fields. They are reading projections, not replacements for the omitted original bytes, and they never claim the original hashes.

The original accepted comparison ZIP envelope contains raw runtime logs and is omitted. All 455 original members are classified: 407 non-log members are expanded verbatim and 48 runtime logs are omitted. No replacement archive hash, fresh historical execution, or closure of partial historical source trees is claimed. Other omitted files are runtime/environment/source-audit receipts or host-bound audit tooling. Every omission is identity-accounted. No raw runtime logs or private coordination are included.

The independent review's unchanged path named private/ contains only six public scientific-evidence files: three new control scripts and their deterministic result JSONs. The historical directory name is preserved to avoid silently rewriting references. Actual private runtime metadata and logs are omitted. Reviewer source_records, author sources, renamed snapshot manifests and all historical inventory gaps remain explicitly accounted for.

Do not run original source inventory wrappers against these intentionally partial exported trees. Use the public verifier below. The original review wrapper's replay command is also superseded by this package's read-only isolated adapter. Original source wrappers and original statements remain evidence, not new active public instructions.

## Read-only reproduction

Use CPython 3.12 with NumPy 2.3.5 and SymPy 1.14.0 as listed in requirements.txt. Integrity checks use only the standard library. Isolated replay additionally requires Linux x86-64, bubblewrap and kernel seccomp; no weaker fallback is allowed.

From the extracted package directory:

    python -I -B tools/verify.py --negative-controls
    python -I -B -O tools/verify.py --negative-controls

Set ARCHIVE to the supplied canonical ZIP, DIGEST to its trusted SHA-256 supplied separately, and OUTPUT to a new directory outside this package. A digest computed from the same untrusted ZIP is not an independent trust anchor.

    python -I -B tools/verify.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST"
    python -I -B tools/replay.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST" --output "$OUTPUT"

Replay verifies and extracts the exact ZIP, mounts it read-only, hides original host input paths, and blocks Python and native network/socket/io_uring calls. It runs all four unchanged scientific programs in both normal and actual optimized Python. The author reference is copied beside its script solely so its existing read-only comparison works. The three reviewer scripts write only inside disposable work directories. All eight JSON comparisons are byte-exact against separately sealed mathematical results. Author stdout is byte-exact against its result plus the additional newline emitted by its unchanged print(encoded); reviewer stdout matches deterministic sealed-reference digests. There are no timing, numeric or content exceptions. Actual optimization semantics, input-write denial, native network denial and final input identity are independently tested.

Fresh results and raw runtime receipts remain outside the delivery. Success requires a terminal REPLAY_RESULT.json with status PASS. A running, failed, interrupted or uncatchably killed replay is never represented as successful.

Choose another new external output directory for real failure/interruption/no-clobber controls:

    python -I -B tools/failure_controls.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST" --output "$FAILURE_OUTPUT"

These controls complete a real successful replay, then prove a rejected reuse preserves all prior success receipts. Actual nonzero launchers, timeout, termination and uncatchable interruption are exercised. Killed-run receipts and logs are likewise preserved after a rejected retry. Resource limits are disclosed in REPLAY_POLICY.json. Additional independent auditing may exercise scientific-child kills and archive/locator adversarial cases without changing the frozen input.

The canonical stored ZIP uses sorted regular files, fixed timestamps/modes, and no hidden records, comments, duplicate names, symlinks, prefix or suffix bytes. SHA-256 establishes byte identity, not theorem truth or cryptographic author identity.
