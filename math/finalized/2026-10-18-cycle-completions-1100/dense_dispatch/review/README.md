# Independent review package

Read REVIEW.md for the final decision and exact scope. INTEGRITY.json binds the frozen candidate and all nine retained dependency blobs. CONTROL_RESULTS.json records the final fresh independent scientific and rejection-prefix controls; CONTROL_RUN_LOG.txt is its process observation.

Reproduce only the new independent controls with:

    PYTHONDONTWRITEBYTECODE=1 python independent_controls.py

The script imports dense_dispatch.py only from candidate_snapshot. It does not execute the author's scientific driver or any predecessor implementation/test suite. The target oracle uses an independent exact pi identity, trigonometric power sums, and integer-bisection root intervals.

CONTROL_HARNESS_CAP_CORRECTION.txt records an earlier review-harness assumption corrected before the final rerun: comparison cap 40 did not fail because the valid N=1 comparison has 35 scalar records. Final rejection controls use caps 12, 16, 24 and 32. This was a test expectation correction, not a production change.

No external write was performed. All claim qualifications in REVIEW.md remain attached to the acceptance.
