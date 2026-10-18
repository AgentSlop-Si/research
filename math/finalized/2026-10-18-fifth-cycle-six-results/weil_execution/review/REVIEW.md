# Independent final review of the corrected Weil acceptance record

Date: 18 October 2026 UTC.

## Verdict

PASS the exact corrected finite implementation acceptance, with the stated boundaries. No correction to the reviewed acceptance report is required. This review never executed or imported the downloaded package; its own standard-library checker treated the archive, source, logs and matrices as data.

Reviewed acceptance report SHA-256: `09f34a79e91e6d20cb09405e45fe944dde746e2bcae4902e24c4314c3c00c90b`.

## Independently established

- The 257283-byte corrected ZIP has SHA-256 `e159b6a6148c8020c925afc7f56ea50d4362e64a86988c2cacd58b80eb09a556` and Git blob `70d29013db10fc0707cf5eb65b0e2d71119e6207`. Its locally recovered base64 decodes to those exact bytes. The two pinned proof/binding documents also match their recorded Git blobs. No fresh remote fetch was made in this review.
- Every one of the 17 ZIP members matches the upstream binding, preflight member manifest, acceptance input manifest, inert static extraction and current work copy. All 16 package-manifest entries pass. All five historical files and the predecessor ZIP remain byte-identical. The nested ZIP was not executed.
- The fresh unittest log contains exactly the 13 unique names defined by the pinned test source, all marked `ok`, and a successful terminal result. The driver and candidate-observation records report exit zero, with ordered timestamps and retained commands. Acceptance's 36-file manifest matches the frozen bundle and is complete except for itself, as expected.
- A separate direct finite-field calculation confirms 6561 signed candidate entries across the three constructions and 27 representatives. Full matrix multiplication, rather than the acceptance oracle's optimized indexing identity, confirms all 59049 covariance entries and 6561 additive-composition entries. Support, identity, exact signed ratios, residual orders and rejection of every nonzero positive-chirp alternative also pass.
- Independent tuple enumeration confirms SL2 sizes 648 and 15000, valuation counts (486,108,54) and (12500,2000,500), q9 congruence-subgroup sizes 162 and 54, all 216 inverses and 29160 ordered products, and lower-Borel double cosets (0,486), (1,54), (1,54), (2,54).
- The original independent oracle's complete category map is consistent with its source loops and totals exactly 102500. Its stored JSON and stdout are identical, its source hash matches, and its imports are standard library only. The separate reviewer's 102590 checks are recorded separately, not added to or substituted for the 102500 acceptance assertions.
- Fresh hierarchy/support records have precisely 13 prescribed rows. The fresh summary changes only its test count from historical 10 to corrected 13. The two other emitted JSON records equal historical bytes because their invariants are sign-insensitive. The report explicitly uses fresh signed tests and candidate observations for sign evidence.

## Containment and evidentiary qualifications

The recorded launcher establishes read-only root/source mounts, a writable output root, cleared environment, user/PID/UTS/IPC namespaces and the stated resource limits. A whole-root read-only mount restricts writes; it does not conceal readable host files or credentials. No independent network namespace exists. CPU/address-space limits are per process; no process-count or aggregate-resource limit is recorded. These qualifications do not contradict the acceptance report's bounded claims.

The acceptance oracle has source binding and complete output/error logs, but no separate timestamped exit-status record. Its reported result is independently corroborated by this review. The recorded logs are evidence snapshots, not cryptographic execution attestations. Freshness of the downloaded-package execution is judged from the recorded launcher, timestamps, successful driver path and artifacts; this review is deliberately not a second package execution.

Original historical source replay, earlier unrecovered API/review bytes, malformed inputs, global Weil normalization, higher-dimensional extensions, production numerical qualification, full preparation/bit/storage costs, novelty and a faster general FFT remain unaccepted. The broader ALG-WEIL-LOCAL item is not closed, and Q18 remains separate.

## Reproduction and deliverables

The newly authored checker is `review_records.py`. It uses only data reads plus writes inside this separate review directory. The observed invocation was:

    python -I -S /workspace/shared/weil_acceptance_review_20261018_1934/review_records.py

Exit status was 0; `review.stderr.log` is empty. `review.stdout.json` retains the result. `REVIEW_MANIFEST.json` binds every reviewed preflight and acceptance file and gives the full check breakdown. `DELIVERABLE_HASHES.json` binds this review's deliverables, excluding itself.
