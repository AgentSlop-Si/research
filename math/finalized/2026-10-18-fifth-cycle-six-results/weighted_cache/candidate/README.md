# ALG-070 weighted complete-view result

Read `REPORT.md` for the exact theorem, full potential proof, sharpness,
attribution, and charged ledger. This resolves only fixed unequal tariffs
for immutable complete equal-size views, not the entire ALG-070 owner.

Fresh source:

- `weighted_cache.py`: deterministic rational-credit reference policy.
- `offline_oracle.py`: independent subset DP and individual-action oracle.
- `validate.py`: exhaustive, potential, convolution, and mutation controls.

Reproduce in this directory with Python 3 standard library:

    python -B validate.py

This rewrites only `VALIDATION.json`. The captured acceptance command was:

    python -B validate.py > REPLAY_OUTPUT.txt 2>&1

No inherited research code, optional packages, network fetches, or external
writes are needed. The source hashes in `VALIDATION.json` bind its tests.
`MANIFEST.json` binds every deliverable except itself. `SOURCE_BINDING.json`
binds retained controlling text and the inspected classical source URLs.
The source folder contains inert text, not executable inherited packages.

Outcome: strict optional-build bound `M_online <= K M_OPT`, sharp
deterministically over the class, and full charged bound
`G + M_online + E <= G + K M_OPT + E`.
