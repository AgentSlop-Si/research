# Accepted independent review: restricted product guards

The frozen candidate passes independent mathematical and implementation review. See REVIEW.md for the binding, proofs, complete cost review, and essential width/input/model qualifications.

- Candidate manifest: `5eb8a2ca9cb85103d4da0833f63126b890820108823b07df673fae30a1f4f10b`
- Candidate replay digest: `fad070a018994005873e0eb2f7f273c94fef243cbb41d124ddf4e77eb4f23c67`
- Independent controls digest: `160d9f465b3038d3a605a836d1232df2cdd6f1d2949ab42b10a655010fe46253`

The sufficient envelope is not claimed optimal. The linear lower bound requires the explicit `m>=t` witness width. Honest W-bit samples are required; arbitrary lifts of H-bit Taylor arrays do not suffice without recovering the original chunks first. This is not a new fast multiplier.

Reproduce using `python independent_checks.py`, `python lift_controls.py`, and, in `candidate`, `python verify_package.py` then `python exact_controls.py`. Run `python verify_review.py` to check the frozen payloads. All work was local; the original candidate was not edited.
