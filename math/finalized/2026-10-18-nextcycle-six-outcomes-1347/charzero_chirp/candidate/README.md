# Exact seven-stage eight-point chirp theorem

Existing owner M-MULTISCALE-CHIRP / Q24. The candidate proves exact minimum seven in characteristic zero over a splitting field (in particular C), and gives a full explicit seven-stage witness over F(17^3) at zeta=3. Independent review is still required before a publication or table promotion.

Read REPORT.md for the complete proof, literal grammar, guarded specialization and limits.

Verification:

- `python verify_exact.py`: standard-library integer verification of five explicit polynomial identities, the exact chirp inverse, gauges, case coverage and six corruption controls.
- `python finite_witness.py`: standard-library field arithmetic and all 64 entries of the concrete F(17^3) witness.
- `python check_derivations.py`: SymPy-only binding of the stored certificate inputs to the necessary equations in the proof.
- `python make_certificates.py`: optional SymPy/NumPy regeneration of the arithmetic certificates, not needed for verification.

Canonical deliverable files are the files listed in MANIFEST.json. Exploratory scripts/logs are excluded. No supplied historical checker or old finite-field search was executed. No repository, spreadsheet, score, ID or census write was made.
