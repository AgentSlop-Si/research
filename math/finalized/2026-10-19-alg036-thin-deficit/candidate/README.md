# ALG-036 thin-deficit endpoint candidate

The self-contained proof is in `REPORT.md`. It proves the proposed sharp complex Gaussian projector/translation bound and derives the N/log N endpoint transition, exact equal-block critical window, and norm-envelope transfer. It keeps arbitrary sphere-prior algorithms, nondivisible exact extrema, worst-case achievability, Fourier arithmetic complexity, and whole-owner closure outside its claims.

The candidate does not change ALG-036 ownership or priority 34. It has not been published by this task. Independent review is recorded separately so that this candidate can remain frozen.

## Fresh reproducible controls

Run:

    python controls/check_thin_deficit.py

Dependencies: Python 3, NumPy, SciPy, SymPy. The program is self-authored, has a fixed seed, makes no network requests, and does not execute historical programs. It writes `controls/RESULTS.json`. Finite exact identities and numerical diagnostics supplement, rather than replace, the all-dimension proof.

## Source and integrity records

`SOURCE_MANIFEST.json` maps copied controlling documents to their source locations and hashes; the BCCT primary theorem was read in the author-hosted PDF, with precise printed pages identified. `MANIFEST.sha256` covers all payload files except itself. Verify it with `sha256sum -c MANIFEST.sha256` from this directory.
