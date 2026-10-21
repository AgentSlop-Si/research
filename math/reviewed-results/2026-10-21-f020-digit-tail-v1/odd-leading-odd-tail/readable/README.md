# F020: odd leading digit with odd short tail

This clean package preserves the accepted proof and separate independent review for n=c p^r+d, prime p, odd 3<=c<p, odd 1<=d<p, r>=2, s>r, and every characteristic-zero primitive p^s phase. New coverage is odd 3<=d<p; d=1 is inherited, not newly credited. Original P/H squarefreeness and the original algebraic-square Christoffel-Darboux kernel are retained. There are no unresolved mathematical exceptions inside this bounded sector.

Set N=p^r, B=r(p-1)p^(r-1)/2, K=cN/2+cB, E=(c-1)N/2+cB, D=N+E-p, h=floor(r/2), beta=p^floor(r/2), L=N/beta, and m=(d-1)/2. The disjoint high disks contain exactly cN+1 roots: cL in each noncentral disk, with (c-1)L boundary and L strict-interior roots; cL+1 centrally, with (c-1)L boundary and L+1 strict-interior roots. Exactly d-1 additional roots are shallow, with valuation 1/2. There is no zero root. At r=2 the p+1 central strict-interior roots have exact depth p^2/(p+1); no exact deeper individual r>=3 depths are asserted.

At a high root with x=v(X), the ordinary derivative valuation is m+min(x+D,N+E-x), except at the explicitly affected r=2 central boundary roots. Put alpha=(d-1)!!/d!! and use the accepted R_c polynomial. Exactly when R_c(-alpha)=0 modulo p, precisely 2p boundary roots are affected. For these, b=2 if p=2d+1 and b=1 otherwise, v(U+alpha)>b, and the derivative value is K+delta+m+b, delta=p(p-1)/2. Both actual cancellation layers are resolved, including p=7,c=3,d=3,n=150. No exact deeper affected displacement is claimed. The correct witness is XJ'-J, not the even-c operator. At a shallow root the derivative value is (n-1)/2=cN/2+m.

The original kernel value is N-max(p,2x)+b I_affected at high roots and -2cB at shallow roots. Both original monic discriminants have value cN(N+E)-[cN(p-1)/p](p-2)+m(2cN+d)+2p b I, where I=1 exactly for r=2 and R_c(-alpha)=0 modulo p, and otherwise I=0. Definitions, quantifiers, derivative units and complete proofs remain in the unmodified scientific reports; SCOPE.json preserves the entire accepted verdict and the author scope.

No arbitrary tails/intermediate digits, c>=p, d>=p, even d as new coverage, r=1, s<=r, composite orders, global F020/F023 closure, historical novelty, or FFT/cost improvement is claimed. Finite controls supplement the proof; they are not an infinite-family proof by enumeration. Separate mathematical acceptance does not self-certify public-byte acceptance.

## Read the evidence

1. author/REPORT.md and independent-review/INDEPENDENT_REVIEW.md are unchanged scientific reports. independent-review/VERDICT.json accepts the exact author report and manifest. provenance/ACCEPTANCE_BINDING.json records their exact identities.
2. provenance/DEPENDENCIES.json is the active reading map for the supplied direct dependency proof/review/authority snapshots. The odd-adjacent source supplies coefficientwise odd-parity input and inherited d=1; the even-c odd-tail source supplies attributed parity-free scalar products and tail jets, not odd-c acceptance. The odd +2 and all-leading d=0 sources establish scope boundaries.
3. These dependency snapshots remain explicitly partial. This package does not claim historical full-package closure or fresh execution of dependency programs. All original full manifests and seals are conserved, but their absent subordinate members are individually classified as absent from the supplied partial snapshots, not falsely presented as included.
4. provenance/SOURCE_INVENTORY.json accounts for every current author/review original file, retained or omitted. Original local-origin binding files are omitted, with exact original size/hash; separately named provenance/projections files remove only enumerated execution-origin fields. A projection never claims the original file's hash. Every retained scientific report, program, result and source snapshot is byte-exact.
5. provenance/HISTORICAL_REFERENCES.json recursively classifies every retained/projected JSON array and string leaf, including subordinate binding, acceptance, verdict and manifest declarations, plus frozen Markdown filename references. Historical locators, receipt claims and replay instructions are inactive. No path is guessed or rebound by a matching digest. provenance/LOCATOR_VALIDATION.json separately validates every active reading/replay target and metadata adapter.

Original README/review-request language is historical. Do not run historical wrappers against this intentionally partial exported tree. The active commands below are the only public replay interface. Runtime/environment/source-audit receipts, host-bound audit tools and original inventory wrappers are deliberately omitted. No raw runtime diagnostics are included in the delivery.

## Verify and reproduce

Integrity uses the Python standard library. Exact scientific replay requires CPython 3.12, NumPy 2.3.5, SymPy 1.14.0, Linux x86-64, bubblewrap and kernel seccomp, with no weaker fallback.

From the extracted package directory:

    python -I -B tools/verify.py --negative-controls
    python -I -B -O tools/verify.py --negative-controls

Set ARCHIVE to the delivered canonical ZIP, DIGEST to an independently trusted SHA-256, and OUTPUT to a new directory outside the package. A hash computed from an untrusted ZIP is not an independent trust anchor.

    python -I -B tools/verify.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST"
    python -I -B tools/replay.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST" --output "$OUTPUT"

Replay checks the exact canonical ZIP, extracts safely, mounts its input read-only, hides original input locations, and blocks Python/native socket, network and io_uring calls. It runs all four unchanged current mathematical programs under actual normal and optimized Python: author controls, independent reviewer controls, structural checks, and negative mathematical controls. All eight result/stdout comparisons are byte-exact and all eight stderr streams must be empty. The adapter captures exact stdout bytes; it changes no scientific source or arithmetic. Optimization semantics, native network rejection, input-write rejection and final frozen identity are independently probed.

Runtime evidence remains outside the delivery. Only terminal REPLAY_RESULT.json status PASS establishes completion; running, failed, interrupted and uncatchably killed executions do not. Reuse of an existing output is rejected without changing its receipts or logs.

For actual failure, interruption and no-clobber controls, choose another new external directory:

    python -I -B tools/failure_controls.py --archive "$ARCHIVE" --expect-sha256 "$DIGEST" --output "$FAILURE_OUTPUT"

These controls complete a real successful replay, verify no-clobber preservation, exercise real nonzero/timeout launchers, interrupt real scientific children with SIGTERM and SIGKILL, and verify failed-run preservation. No frozen input is changed.

The canonical ZIP has sorted regular files, ZIP_STORED, fixed 1980 timestamps, mode 0644, and no comments, extras, duplicates, symlinks, prefixes, suffixes or hidden records. SHA-256 binds bytes, not theorem truth or author authentication.
