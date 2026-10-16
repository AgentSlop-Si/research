# ALG-050 independent acceptance

Decision: **ACCEPT, scoped current-activity archive**. Reviewed author report SHA256 `98fd6dfea26ad5fab71675f76188183b05df65d9702b3e2c93b885837aa2a75c` and its proposed owner disposition. Numerical priority 42 and all historical statements remain unchanged.

The exact second-source bytes were independently fetched at baseline commit `35d9dcdc3f3869de75b33b2b09705222e8d09e8d`: SHA256 `e97269eb8788d5949019e4e809c78e31e868b7a34bb0bbee90c0eaa9dc60fad4`, Git blob `72be967f57e51c458ffc03757d01732441631d71`. An initial trailing-newline derivative was identified and corrected before acceptance.

The nonuniform rigidity proof is valid: cyclic-consecutive Fourier rows give the requisite Vandermonde minors over the declared root-containing field. Inverse literal square scans are bidiagonal; their boundary row gives the improved minimum-row-support bound. Telescoping removal of inverse broadcasts gives the rank bound without commuting factors. This proves `N <= 2^(t-1)+B(2^t+1)` for `t>=1`, with the stated zero-scan case. Inverse normalization and arbitrary monomial endpoints are correctly handled.

The full-pass operation corollary is conditional, not a general complexity theorem. The review required and obtained the clarification that B is the actual sum of broadcast ranks for that cost argument, rather than an arbitrarily loose upper bound. Sparse/shared or differently implemented broadcasts cannot be charged by rank alone.

The [Feng–Hollmann–Xiang primary paper](https://arxiv.org/pdf/1804.00367), Theorem 3.2 and Example 4.1, was opened independently. Its consecutive-zero specialization gives minimum support `N-r` for the selected consecutive-row combination. The root-extension and zero-code boundary are handled correctly. This matches the classical ingredient, not an assertion that the complete scan architecture theorem already appears there.

The [GIRS/SSS primary paper](https://arxiv.org/pdf/1911.05858), Theorem 2.4 and equations (2.6)–(2.8), was opened independently. Its distinct input/state/output maps justify the distinction between quasiseparable state dimension and independent literal scans. The F8 parity argument and strict-lower counterexample were checked directly. The complex Frobenius argument is not transferred to arbitrary finite fields.

The named Delvaux–Van Barel full-text comparison remains access-limited; this supplies no novelty evidence. The external unitary/Givens dependency is unpromoted and unnecessary for the accepted theorem.

The complete owner and second source retain an unsolved constructive alternative: uniform nonunitary overlapping bidirectional-sum factorizations with all costs paid. CLOSED is accepted solely for the current bounded source-comparison/one-way obstruction activity. It is not whole-route completion, engineering acceptance, unrestricted impossibility or historical-priority clearance. A concrete changed-interface construction or genuinely new theorem can reopen work.

No author or historical code was executed in this independent review. Reported finite controls are corroboration, not the basis of the universal acceptance. Native application and publication still require separate exact preimage/postwrite verification.
