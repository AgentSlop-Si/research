# Adaptive packing completion

Read `REPORT.md` first.

Completed:
- A legal, exact-size adaptive invariant, closed for Theta(log n/log log n) levels by an exact parameter-cell/divisibility construction.
- A full n exp(Theta(log n/log log n)) complexity theorem for the explicitly defined independent-call adaptive Newton executor.
- Explicit elementary linear-time escapes for the witness: content extraction, and a shared leading-term construction even after the first-level children have been made distinct and many of them odd.
- Fresh endpoint and parameter controls, with no historical code execution.

Still open:
- A general shared/adaptive construction for arbitrary inputs, or a closed hard family resistant to a precisely specified sharing policy. The independent-call theorem is not a lower bound for the user's full shared-graph route.

Files:
- `REPORT.md`: precise policy, lemmas, complete proofs, scope and source evidence
- `fresh_controls.py`: newly written reproducible controls; standard library only
- `CONTROL_RESULTS.json`: full fresh exact outcomes
- `RUN.log`: completed run transcript
- `SOURCE_PINS.json`: intact successor archive and relevant source-member hashes
- `VERDICT.json`: machine-readable scope boundary
- `MANIFEST.json`: hashes of the principal deliverables

Reproduce locally with:

    python3 fresh_controls.py

This public package includes the six exact cited successor members under `source/`, plus the exact predecessor `source/predecessor/packed_outer.py`. The portable control script hashes these members as inert bytes instead of opening private source archives. The mathematical controls are unchanged. The recorded results are from the original reviewed script; the portable script has not been rerun during packaging. See the package `PORTABILITY.md` for exact changes and provenance.

Fresh run: 10 exact parameter cells, 19 aligned levels, 56 materialized aligned node controls, 9 complete recursive products / 958 executor calls, 33 shared perturbed-node products, and 64 strict-width boundary controls. All passed. Controls through rank 1024 include six closed adaptive levels. The materialized 162,372-bit example has 33 children of 7,884 actual bits and 759 level-two calls of 1,036 actual bits.
