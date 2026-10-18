# Canonical affine-run extension

New candidate, pending independent review. No external writes were performed.

Start with `REPORT.md`. The complete new multiplier is `affine_shared.multiply(a,b)`. Its affine branch is followed by the unchanged portable accepted jump branch and its accepted fallback. The reported theorem is a strict recognized-class extension, not an arbitrary-dense multiplication improvement or a lower-bound separation from the prior dispatcher.

The key lemma is that greedy canonical digit vectors are integer points of a convex polytope. A numerical affine run can therefore be certified by canonical first/second/last blocks and one endpoint extrapolation test. This avoids dense canonical conversion. Sparse second differences, shared native product interpolation, and four full prefix scans give a complete bound O(N+r^12+R_A R_B r^4), including recognition and output.

Run author controls from this directory:

    python controls.py

The script overwrites `RESULTS.json`; use a disposable copy to preserve the recorded run. It uses only Python's standard library. `affine_shared.py` hash-checks the portable accepted jump source, which in turn hash-checks the original reviewed arithmetic primitive source. The accepted primitive is byte-exact; the portable jump copy changes only an absolute dependency path, as disclosed in `sources/COPY_BINDINGS_EXTRACT.json`.

Files:

- `REPORT.md`: theorem, proof, complete bit-cost ledger, strict family, and precise higher-order obstructions
- `affine_shared.py`: new production branch and full multiplier wrapper
- `controls.py`: fresh author tests with independent exact arithmetic oracles
- `RESULTS.json`, `controls.log`: recorded completed author run
- `run_shared.py`, `dependencies/`: pinned inherited implementation
- `sources/`: immutable repository evidence and adaptation bindings
- `MANIFEST.json`, `verify_manifest.py`: local packet integrity

The result is limited to the actual recognizer's certified affine pieces. A numerical affine or polynomial block sequence alone is insufficient because canonical carries can create dense vector differences. Higher-degree pieces and arbitrary dense input remain unresolved.
