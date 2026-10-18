# Native-matrix run-difference extension

Read `REPORT.md` for the theorem, proof, scope, and implementation details.

- `run_shared.py`: new complete budgeted front end and exact run-difference shared branch; imports the hash-pinned reviewed primitive module.
- `independent_controls.py`: newly authored independent formulas, endpoint/packing oracles, and certificate mutation tests.
- `RESULTS.json` and `RUN.log`: passing recorded controls.
- `SOURCE_PINS.json`: exact accepted dependencies, including the required prior erratum.
- `MANIFEST.json`: hashes of this package's deliverables.

Run from this directory with `python independent_controls.py`. The dependency path is intentionally explicit and SHA-256 checked. No external write was made.

This candidate establishes a larger structural linear-time regime; it does not claim a new arbitrary-dense multiplication bound or novelty for finite differences or run-length encoding. Independent review is still required.
