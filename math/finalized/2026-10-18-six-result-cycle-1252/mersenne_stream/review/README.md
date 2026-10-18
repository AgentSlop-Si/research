# Final independent Mersenne conversion review

ACCEPT with the two mandatory qualifications in REVIEW.md. Preserve that file beside the candidate.

The complete conversion bound is O(N [L² log(L+1)]^(log₂3−1)) in the stated sufficiently wide supplied families; L=O((log N)^(4/5)) gives o(N log N). The construction is exact and independently terminating. General multiplication, FFT/matrix transforms, correlated point products and growing-prime selection remain open.

Mandatory qualifications:
1. Small actual coefficient values can give W<t even when ambient m is huge. Use declared padding or the unsimplified ledger with q<=1+W/t=O(m/t), W=O(m) and m>=t. The standalone simplified shift bound still requires W>=t.
2. If an unrestricted grouping parameter d has an arbitrarily long encoding, add O(bitlength(d)) for reading/comparing it. No d-sized table is needed for a lone short group, but its scalar input is not free.

- REVIEW.md: independent proofs, complete ledger, scope and binding
- independent_checks.py: fresh deterministic controls
- INDEPENDENT_RESULTS.json / INDEPENDENT_RUN.log: completed checks
- reviewed_candidate/: unchanged source snapshot; all 11 manifest entries and five source pins verified
- CANDIDATE_RERUN.log: original harness reproduced its results exactly

No external write was performed.
