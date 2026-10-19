# Independent endpoint review

PASS for the N=3q,d=2q exclusion at every prime q>3. Read REVIEW.md and VERDICT.json for the exact theorem, candidate binding, and remaining scope.

Reproduce fresh independent controls with:

    python independent_checks.py

Recheck the frozen candidate witness data and all source bindings with:

    python audit_candidate_data.py

Both scripts use Python 3 and SymPy. Candidate and historical research programs are never imported or executed. Outputs contain exact integer/rational cyclotomic arithmetic only. The fresh original inverse matrices are retained in ORIGINAL_MODEL_WITNESSES.json; the separate audit of all candidate matrices is in CANDIDATE_AUDIT.json.

The independent local-multiset check deliberately keeps the global support-equality prerequisite separate from the weaker local scalar-product condition. The counterexample to that weaker shortcut appears in INDEPENDENT_RESULTS.json.

No external state was changed. The theorem is not a novelty or owner-closure claim.
