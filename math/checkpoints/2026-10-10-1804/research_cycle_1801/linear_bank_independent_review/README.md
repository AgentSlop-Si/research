# Independently reviewed linear Fourier bank bounds

Verdict: PASS, 10 October 2026.

- Stronger step-one result: 2N−2floor((N+13)/10)+2 banks for every odd N≥27, with leading coefficient 9/5. See STEP_ONE_REVIEW_RECEIPT.json.
- Preserved step-two result: 2N−2floor((N+19)/16)+2 banks for every odd N≥45, with leading coefficient 15/8. See STEP_TWO_REVIEW_RECEIPT.json.

Both results use a monic defining polynomial in Q(q), with actual banks realized over its splitting field. No scalar FFT runtime or historical-priority claim is made.

LINEAR_BANK_INDEPENDENT_REVIEW.md contains the complete reconstructed elimination proofs and the monic, squarefree, nonzero, incidence, axis, descent and legal-bank checks. SOURCE_BINDINGS.json identifies frozen input copies. FRESH_LINEAR_SAVING_RESULTS.json records fresh exact supporting controls. Only fresh_linear_saving_check.py was executed; no inherited research program was imported or run.
