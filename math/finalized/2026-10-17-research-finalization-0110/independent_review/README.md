# Independent review of the 17 October new finalization batch

Accepted:

- ALG-049: the fixed N=8 prefix excludes arbitrary nonuniform Möbius-cycle final factors at the stated monomial last-boundary interface. Parent stays open.
- ALG-064: the supplied-dyadic-coefficient residual-aware numerical evaluator has an explicit absolute-error/bit-cost contract and at most r suspect bins. Parent stays open.
- M-AFFINE-STEP: close only the existing accepted-theorem-plus-qualified-primary-comparison stage. Priority and historical novelty limits remain unchanged.

No other record is accepted for closure. The exact proposed 27-cell application has one status transition and requires fresh application guards. Mathematical review and publication/native-state verification are separate.

Only reviewer-authored programs were executed. No author or historical research program was imported or executed. Formal certificate JSON was treated as data; polynomial expressions were parsed with a restricted arithmetic AST rather than evaluated as code.

## Reproduce reviewer controls

Run the following Python 3 standard-library programs in this packet:

- alg049/fresh_cut_review.py
- alg049/fresh_certificate_review.py PATH_TO_AUTHOR_CUT_CERTIFICATES.json
- alg049/fresh_mobius_controls.py
- alg064/fresh_numerical_review.py
- neglected/fresh_comparison_controls.py

The first ALG-049 program writes its independently reconstructed Laurent matrices and minors, which the second reads. Each program writes results beside itself. Runtime depends on the host; these are verification controls, not Fourier benchmarks.

AUTHOR_FILE_HASHES.json in each review folder binds the reviewed author artifact set. INTEGRITY.json binds this review packet. Native exports and exact private proposal bodies are intentionally not included in the publication allowlist.
