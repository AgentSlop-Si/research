# Exact C8 upper witness: independent ACCEPT

All 746 original exact assertions passed. The full analytic review accepts the candidate without changes:

sin(3π/16) < δ_(8,0) ≤ ½√(1+√(√2−1)) = 0.641013699718185….

The lower inequality is inherited from the hash-bound, previously accepted C8 obstruction. The upper inequality is established by a legal explicit witness in the full arbitrary-complex-monomial, unrestricted-real-core, external-operator-norm model with correction rank zero. Its actual external residual has largest singular value ½√(1+h) with multiplicity six, h=√(√2−1).

- REVIEW.md: independent complete derivation and scope audit
- VERDICT.json: accepted statements and open question
- independent_exact_controls.py: freshly written symbolic controls
- INDEPENDENT_EXACT_RESULTS.json: completed exact results and cost
- SOURCE_BINDINGS_BEFORE.json / SOURCE_BINDINGS_AFTER.json: unchanged candidate and inherited sources
- MANIFEST.json / SEAL.json: review-file hashes and frozen binding

To reproduce with Python and SymPy installed, while the bound source directories remain available:

    python independent_exact_controls.py

The checker reads candidate files only for hashing and does not import or execute them. It writes its own result receipts in this review directory. No historical code was executed and no external state was changed. No numerical optimizer was used in this review.

The exact global optimum remains open. The four-periodic choice constructs a witness; there is no assumed all-phase periodicity reduction. Interval-width reduction is only a derived secondary comparison.
