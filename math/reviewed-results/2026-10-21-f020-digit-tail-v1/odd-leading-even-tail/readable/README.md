# F020: odd leading digits with positive even short tails

This package preserves an accepted mathematical proof and separate independent review for n=c p^r+d, prime p, odd 3<=c<p, even 2<=d<p, r>=2, s>r, and every characteristic-zero primitive p^s-th phase. New coverage is only even 4<=d<p. The d=2 theorem and all-leading d=0 theorem are inherited, not newly credited. The original P recurrence, Gaussian H, original ordinary derivatives, and original algebraic-square Christoffel-Darboux kernel are unchanged.

There are cN high roots and d shallow roots, where N=p^r. The high roots include one simple exact zero; the corresponding H root z=-1 is simple. Set beta=p^floor(r/2) and L=N/beta. Each of the beta disjoint high disks has cL roots, with (c-1)L boundary and L strict-interior roots. The central L interior roots consist of the exact zero and L-1 nonzero roots. Exact deeper individual nonzero interior valuations are not asserted.

Both P and H are squarefree, and the original kernel is nonzero at every P root. No mathematical exceptions remain inside this bounded sector. Small-prime auxiliary cancellations, including p=5,c=3,d=4, only improve error bounds and do not cancel the decisive unit. The complete derivative, predecessor, kernel and discriminant formulas are preserved in SCOPE.json and the unmodified scientific reports. SUMMARY_BINDINGS.json binds every public summary formula to literal statements in the accepted author report.

No arbitrary intermediate digits or degrees, c>=p, d>=p, r=1, s<=r, composite orders, global F020/F023 closure, historical novelty, or FFT/cost improvement is claimed. Odd tails and even-leading sectors are inherited scope boundaries, not new results here. Finite controls supplement the uniform proof; enumeration is not the proof. The independent controls retain the repeated reduction modulo 251 at phase 26, which is not a characteristic-zero exception. Modulo 4001 all 100 primitive 125th phases pass the original P/H and kernel tests for n=79. Separate mathematical acceptance does not self-certify public packaging acceptance.

## Read the evidence

1. author/REPORT.md and independent-review/INDEPENDENT_REVIEW.md are unchanged scientific reports. independent-review/VERDICT.json accepts the exact author report and manifest. provenance/ACCEPTANCE_BINDING.json records those exact identities.
2. provenance/DEPENDENCIES.json is the active reading map. Odd-adjacent and odd-plus-two sources provide accepted coefficientwise odd-parity authority. The even-leading even-tail source supplies the attributed parity-independent finite-tail method, not its even-parity root geometry. Odd-leading odd-tail sources supply an attribution boundary, not a mathematical dependency on their cancellation lifting.
3. Direct dependency snapshots are explicitly partial. Their unchanged full manifests describe the original packages, not these partial directories. Every historical inventory member is classified as retained, deliberately omitted, or absent from the supplied partial snapshot. Historical full-package closure and fresh dependency execution are not claimed.
4. The original zero-tail archive is omitted from this public export because it contains historical operational material. Necessary zero-tail proof, review, acceptance and inventory excerpts are supplied byte-for-byte under dependencies/zero-tail. provenance/ZERO_TAIL_ARCHIVE.json records the exact original archive identity, all original member identities and dispositions, and original-to-export locators. Its historical acceptance explicitly distinguishes the original report/review from their earlier public projections. This package preserves the already-public bytes unchanged and does not equate those identities.
5. provenance/SOURCE_INVENTORY.json accounts for every current author/reviewer source member, retained or omitted. Local-origin binding metadata is omitted in its original form and retained as separately named narrow projections, with each removed field identified. A projection never claims the original file's hash. All retained scientific reports, programs and results are byte-exact.
6. provenance/HISTORICAL_REFERENCES.json recursively classifies every retained/projected JSON array and string leaf, including nested binding, acceptance, verdict and full-manifest declarations, plus frozen Markdown filename references. Historical locators, runtime claims and replay instructions are inactive. provenance/LOCATOR_VALIDATION.json separately verifies all active reading/replay targets and metadata adapters. No old locator is guessed or rebound merely because a digest matches elsewhere.

Historical README/review-request instructions are not the public replay interface. Do not run their inventory/source-audit wrappers against this intentionally partial export. Runtime/environment/source-audit receipts, host-bound audit tools and original inventory wrappers are deliberately omitted. No raw runtime diagnostics are part of the delivery.

## Verify and reproduce

Integrity uses only the Python standard library. Exact scientific replay requires CPython 3.12, NumPy 2.3.5, SymPy 1.14.0, Linux x86-64, bubblewrap and kernel seccomp. There is no weaker isolation fallback.

From the extracted package directory:

    python -I -B tools/verify.py --negative-controls
    python -I -B -O tools/verify.py --negative-controls

Set ARCHIVE to the delivered canonical ZIP, DIGEST to its independently trusted SHA-256, and OUTPUT to a new directory outside the package. A digest calculated from an untrusted ZIP is not an independent trust anchor.

    python -I -B tools/verify.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST"
    python -I -B tools/replay.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST" --output "$OUTPUT"

Replay verifies exact canonical ZIP bytes, extracts safely, mounts the input read-only, hides original input locations, and blocks Python/native socket, network and io_uring calls. It executes both unchanged current mathematical programs, author controls and independent review controls, under actual normal and optimized Python. All four result/stdout comparisons are byte-exact and all four stderr streams must be empty. The adapter only captures stdout; it changes no scientific code or arithmetic. Optimization semantics, native network rejection, input-write rejection and final frozen identity are independently probed.

Runtime evidence remains outside the delivery. Only terminal REPLAY_RESULT.json status PASS establishes completion. Running, failed, interrupted and uncatchably killed executions do not. Existing output directories are rejected without changing any receipt or log.

Choose another new external directory to test real failure, interruption and no-clobber behavior:

    python -I -B tools/failure_controls.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST" --output "$FAILURE_OUTPUT"

The controls complete an actual successful replay, preserve successful and failed receipts on repeated calls, exercise real nonzero/timeout launchers, and interrupt real scientific children with SIGTERM and SIGKILL. Frozen input is never changed.

The canonical ZIP contains sorted regular files using ZIP_STORED, fixed 1980 timestamps and mode 0644. Comments, extras, duplicates, symlinks, prefixes, suffixes and hidden records are rejected. SHA-256 binds bytes, not theorem truth or author authentication.
