# Degree-29 source and claim ledger

All dependencies below are retained locally and bound in SOURCE_PINS.json by byte length, SHA256, and Git blob SHA1. Original local paths are explicit. The source rebuild compares available originals byte-for-byte. No fresh web or GitHub retrieval was made by this task.

## Accepted immediate predecessor

- sources/DEGREE23_REPORT.md, DEGREE23_OPERATION_LEDGER.md, DEGREE23_MANIFEST.json: the exact degree-23 construction and its scope/costs.
- sources/DEGREE23_REVIEW_INDEPENDENT_REVIEW.md, DEGREE23_REVIEW_VERDICT.json, DEGREE23_REVIEW_MANIFEST.json, DEGREE23_REVIEW_ARITHMETIC.json: the separate accepted degree-23 review. Its verdict is ACCEPT_SCOPE_LIMITED. The source checker binds the acceptance to the exact candidate manifest, independent review report, and arithmetic receipt.
- All 52 candidate-manifest entries and all 78 independent-review-manifest entries are checked against their original available local trees. Those original trees are provenance inputs, not runtime dependencies of the isolated mathematical certificate checker.
- The degree-23 accepted review specifically warns that degree-29 packed multiplication needs at least 17-bit slots or ordinary convolution. The new active literal checker uses ordinary convolution, and the separate new boundary audit explicitly rejects 16-bit corruption before support search.

## Reused code and exact adaptation

adapt_source.py reproduces these seven active sources byte-for-byte from pinned degree-23 sources:

- search_degree29.cpp: degree, modulus constant, and deterministic seed changed; GMP exponent type retained.
- verify_literal.cpp: field metadata and degree references changed; original Gauss-Jordan matrix reconstruction retained.
- independent_literal_check.py: field metadata changed; ordinary-convolution and backward-recurrence inverse method retained. It does not import the discovery/C++ implementation.
- field_verify.py and search_field.py: exact prime-polynomial proofs and deterministic modulus family changed to degree 29 and u^29+u+8.
- arithmetic_probe.cpp and check_arithmetic.py: exact order/bits and field metadata changed; all six 128-bit truncation falsification controls retained.

The new packing-boundary auditor, witness-structure checker, source/chronology harnesses, report, and operation ledger are separately authored here. The accepted degree-23 packed reviewer source is retained for provenance; it is not run as a degree-29 checker and is not used to claim new external independent-review acceptance.

## Inherited lower and chart theorems

The retained ACCEPTED_LOWER_REVIEW.md states the field-uniform characteristic-53 lower theorem for arbitrary legal beta in the original grammar: seven effective same-sign nodes in each same-sign orientation and a nonzero node in each cross orientation. This task relies on that statement, not on its narrower y=z=1 criterion, and does not rerun the large lower-minor computation.

Immutable source locator:

https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md

The retained RANK_REPORT.md supports the discovery chart at degree 29 because 37 does not divide 29. The final literal identity does not require any assertion that the chart is exhaustive.

Immutable source locator:

https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-16-research-finalization-2101/n13_free_cross_rank/REPORT.md

The retained accepted degree-eleven, degree-thirteen, degree-seventeen, and degree-nineteen reviews preserve the lower-bound and free-cross scope distinctions. Their provenance chain is also retained in the degree-23 source-pins ledger. These are inherited source links and local accepted bytes; the present task does not describe them as new remote fetches.

## What is newly proved and what is inherited

New exact checks establish irreducibility of u^29+u+8, the explicit original sixteen-bank upper witness over F_(53^29), safe coefficient/exponent arithmetic, full literal target identity, nonstable supports, exact node Frobenius orbits, and cold reproducibility. The matching lower bound is inherited. Scalar extension and prime-Frobenius conjugacy are standard algebraic consequences of the new exact identity.

The combined sufficient divisor list and residual coverage boundary are not a complete existence classification. No finite witness list establishes generic or cofinite existence, and no failed discovery prefix establishes nonexistence. The new certificate remains pending external independent review.
