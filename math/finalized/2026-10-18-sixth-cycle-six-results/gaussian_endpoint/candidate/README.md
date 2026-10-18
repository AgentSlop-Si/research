# ALG-036 critical endpoint packet

The constant-fraction alpha=1/2 Gaussian measurement endpoint is proved with an explicit exponential success upper bound. This is a candidate theorem packet for independent review, not a claim that review has already occurred.

- `REPORT.md`: complete theorem, self-contained disk and cube proofs, adaptive/stopping posterior, norm-event handling, fixed-input quantifiers, and original block-local application.
- `SOURCE_MANIFEST.json`: exact controlling source identities and verified source hashes.
- `sources/`: unchanged byte copies of the task and two controlling mathematical sources.
- `controls/fresh_controls.py`: newly authored exact and numerical transcription controls. No historical program is executed.
- `controls/RESULTS.json`: recorded checker result.
- `VERDICT.json`: machine-readable candidate scope and explicit exclusions.
- `MANIFEST.sha256`: payload hashes.

Run fresh controls with:

    python controls/fresh_controls.py

Scope stays fixed: terminal pathwise complex rank deficit at least delta N, fixed C>0 and delta>0, and no input information beyond independent coins and the charged adaptive linear transcript. This does not settle thin deficits, full-input computation, arithmetic complexity, or broader owner closure.
