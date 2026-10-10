# Accepted base-field Fourier bank constructions

10 October 2026. All predecessor files remain unchanged.

## Results

- BASEFIELD_FOURIER_UPPER_BOUND.md: for every odd N≥7, at most 2N−4 legal Fourier banks with every node and raw phase weight in Q(q). This gives 10 at N=7 and 18 at N=11.
- SMALLER_SPLITTING_FIELDS_ADDENDUM.md: eight banks at N=7 over an extension of degree exactly 2, and fourteen banks at N=11 over a splitting field of degree at most 24. The canonical N11 specialization forces rational roots 7 and 8.
- K-only attainment of the smaller counts 8 and 14 remains unresolved. There is no minimality, arithmetic-speedup, or historical-priority claim.

Both notes were independently accepted. RESULT.json gives their fixed hashes and independent acceptance receipts. The review folders are ../basefield_bank_review/ and its smaller_fields_addendum_review/ subfolder.

## Controls

CONTROL_SCOPE.md distinguishes exact characteristic-zero controls, justified good reduction, independent finite-field controls, and unsuccessful bounded exploratory searches. The explicit base-field N7/N11 witnesses have exact raw weights and passed every literal branch inverse and original matrix entry.

The q,q²-root N11 specialization is separate exploratory material. Do not substitute its parameters or residues into the canonical 7,8-root construction.

Fresh scripts import only standard/SymPy libraries and this packet's own arithmetic helper. They do not run or import predecessor research programs. If reproducing, first make a writable copy because controls write their outputs beside themselves.
