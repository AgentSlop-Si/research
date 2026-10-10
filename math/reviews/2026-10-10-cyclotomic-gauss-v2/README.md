# Cyclotomic path and Gauss synthesis audit

This local export candidate reviews Schur/path v32 and the proposed Gauss–Superconcentrator construction. The restricted v32 statements survive the audit. No uniform sparse Gauss graph or faster exact Fourier algorithm is established. Historical novelty is unverified.

Read `TECHNICAL_AUDIT_v2.md` first. Revision 2 explicitly chooses the fifth-root embedding required for the positive-real-amplitude counterexample. Two private conversation links have been removed from this public copy; the technical wording is otherwise identical to corrected v2.

## Included files

- `SOURCE_RESEARCH_v32.md`: the complete original v32 research text, byte-for-byte unchanged and clearly labeled as source material. Its claims are reviewed by the audit rather than adopted indiscriminately.
- `fresh_controls.py` and `FRESH_RESULTS.json`: portable mathematical controls and regenerated results. Run with Python 3.8 or later using `python3 fresh_controls.py`. The source archive/provenance checks from the original private review are separated into `SOURCE_PROVENANCE.json`; this portable runner does not redo those checks.
- `check_positive_real_palette.py` and `POSITIVE_REAL_PALETTE_CERTIFICATE.json`: separately authored exact 25-entry, 33-edge fifth-root certificate, using the conjugate positive embedding.
- `SOURCE_PROVENANCE.json` and `SOURCE_HASH_LEDGER.csv`: exact source hashes, integrity receipts, revision scope and primary paper links.
- `MANIFEST.sha256`: hashes of every other file in this candidate.

No uploaded source program was executed or imported. Both included programs are newly authored audit controls. Finite controls supplement the proofs and do not certify all-length construction or novelty. Original source ZIPs and private conversation transcripts are not included.

This folder is a local review candidate. Its existence does not indicate upload, publication, or a change to any external research tracker.
