# Reproduce the independent review controls

The verdict is in `REVIEW.md`. All computations use exact arithmetic.

Requirements: Python 3 and SymPy, with the original candidate packet and its bound prior source packets present at the paths recorded in `fresh_controls.py` and the candidate's `SOURCE_BINDINGS.json`.

Run from any directory:

```sh
python fresh_controls.py > FRESH_RUN.log 2> FRESH_RUN.stderr
```

The checker revalidates every candidate manifest member and source copy before and after testing, and writes `FRESH_RESULTS.json`. It does not import or execute the candidate checker. Successful output ends with `All exact controls passed; candidate bytes unchanged.` Stderr is empty on the recorded successful run.

`MANIFEST.json` seals the review files except itself and `SEAL.json`; the latter binds the manifest, review, and checker hashes. A rerun should preserve the checked mathematical results and source bindings. No network access or external writes are needed.
