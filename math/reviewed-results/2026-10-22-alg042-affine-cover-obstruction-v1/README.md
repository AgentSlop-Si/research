# A lower bound for odd-affine covers of the normalized-packet marker set

Independently verified, 22 October 2026. This closes one specific constant-cover question in ALG-042, not the broader research programme.

For N=2^n and the exact inherited marker set E, with L=2^(b-1), every cover by odd-affine images needs at least 2^floor((b+1)/2) >= sqrt(2L) images. At the specified growing-b parameter choice, no fixed number of such images can cover. The inherited upper bound is O(L); the remaining gap is Omega(sqrt L) versus O(L).

- [Proof and precise hypotheses](THEOREM.md)
- [Independent mathematical review](INDEPENDENT_REVIEW.md)
- [Immutable source locators and current-content hashes](SOURCES.json)
- Independent finite verifier: independent_review_checks.py and INDEPENDENT_CHECKS.json.
- Author controls: fresh_controls.py and CONTROLS.json.

The proof handles carries, arbitrary size-dependent odd multipliers and shifts, terminal partial digit blocks, inverse maps and a quantitative uncovered-point count. Finite checks corroborate the all-size proof; they are not its foundation.

This is not an FFT operation lower bound, a faster FFT algorithm, a proof of exponent optimality, or a historical novelty claim. Faster selected transforms, early-time outputs, causal/full recovery and numerical/bit costs remain unresolved. ALG-042 remains TO RESEARCH at priority 34.

The independent review identifies the original proof by SHA-256 e52c8dc40400dd31e9d6d4a09956b6a88ca839acd6f46b090d63c1a1430b38bc. The publication copy changes only the status/disposition wording and removes an irrelevant read-access diagnostic; all mathematical definitions, statements and proofs are unchanged. The complete editorial diff is separately checked before publication. Source filenames encode historical hashes, not the current published-content hashes.
