# Independent acceptance: ALG-036 thin-deficit endpoint

`REVIEW.md` gives the full mathematical and source audit. `VERDICT.json` records the scoped acceptance, frozen candidate hashes, and exclusions. No full-owner closure, unrestricted Fourier complexity result, arbitrary sphere-prior theorem, or every-fixed-input positive guarantee is asserted.

The candidate remains unchanged. Its seal is copied as `CANDIDATE_MANIFEST.sha256`; `controls/audit_sources.json` verifies every payload and all three original-source copies. The primary author-hosted theorem was independently read, with precise locations recorded, rather than represented as a locally archived PDF.

Two newly authored independent checkers and their results are in `controls/`. `controls/author_replay/` contains an inspected copy of the candidate's fresh checker and its byte-identical replay. No historical program was executed and no external write was made.

`MANIFEST.sha256` covers every review payload except itself. Replaying the author checker should be done only in its review copy, not in the sealed candidate.
