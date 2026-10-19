# Independent effective chirp cutoff review

**Verdict:** Accept `N0 = 2^(2^534)` for the stated positive-epsilon, fixed-coordinate two-Green family, conditional on the two accepted N=5 and principal-restriction inputs.

Start with `INDEPENDENT_REVIEW.md`. The original independent exact controls and their result are in `independent_controls.py` and `INDEPENDENT_CONTROL_RESULTS.json`.

Replay with Python 3.10 or newer, using only the standard library:

    python independent_controls.py

An isolated replay is preserved under `replay/`; its result matches the top-level result byte-for-byte. The checker performs no network operations, executes no historical code, and writes only its results next to itself.

The accepted source reviews and final constructor proof are preserved as inert text under `source/`. The reviewed final proof has SHA-256 `a3c758d9016ac5bbc7c78d1133e135d7714a81adf14e8dbc541d18ed7aab7b38`.

The controls do not replace the accepted N=5 emptiness certificate or materialize the enormous Macaulay matrix. The new cutoff is a proved arithmetic bound, not a computed exceptional list. The negative-epsilon branch and unmatched endpoints remain outside scope.

`MANIFEST.sha256` seals this review's files. No copyrighted paper PDF is included; the primary theorem is linked in the review.
