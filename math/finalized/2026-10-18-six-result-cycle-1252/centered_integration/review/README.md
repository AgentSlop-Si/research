# Independent restricted integration review

Verdict: ACCEPT_RESTRICTED_CENTERED_ORIGINAL_COMPLETE_OUTER_EXECUTION.

Read REVIEW.md for exact scope and VERDICT.json for the machine-readable decision. The frozen candidate is under candidate_snapshot/. The real complete rerun and regenerated receipts are under reproduction/. REPRODUCTION_COMPARISON.json verifies all deterministic data and numerical receipts against the frozen candidate.

INDEPENDENT_AUDIT.json checks original-target errors, every retained receipt and disjoint ledger sums. INDEPENDENT_RETAINED_INTERVALS.json contains a second fresh 320-bit independent oracle check of all 5,733 coefficients and 512 rows. Neither finite test changes the inherited general error theorem or closes ALG-034.

Run independent_audit.py and independent_oracle_crosscheck.py for fresh exact oracle verification. The former also checks original local evidence paths and therefore requires those source packets on the review host. To reproduce full numerical execution, copy reproduction/ to a disposable directory and run run_integration.py and check_boundary_controls.py; expected deterministic outputs and receipts are recorded in REPRODUCTION_COMPARISON.json. Original author seals are preserved separately from freshly timed reproduction outputs.

No external writes were performed. Generated Python bytecode is excluded from the review manifest.
