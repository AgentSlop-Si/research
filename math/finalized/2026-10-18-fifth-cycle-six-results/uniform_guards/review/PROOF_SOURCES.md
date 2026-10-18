# Proof and source bindings

## Reviewed candidate

- Author manifest SHA-256: `291b57db309bfb44cf8f056f9c7677e5375e59026dcb1e14cfd1fc20e33bd1ca`.
- Author REPORT.md SHA-256: `0635b3ce3d9cfffd13ef108cf4d1423ed0f3b007d29cbc5dce07cf8c3b53eebe`.
- Direct proof of node separation, half-lattice exclusion, and Newton monicity: frozen REPORT.md Sections 1-5.
- Exact residual ordinary-squarefreeness boundary: frozen REPORT.md Section 6.
- Inherited factorization and composition are sourced below; the review does not reclassify those inherited results as newly proved.

## Freshly verified controlling sources

1. [Accepted residual-boundary report, pinned commit a4dacc1](https://github.com/AgentSlop-Si/research/blob/a4dacc1f15eb910ec7d494f1572bc044e2d0533b/math/finalized/2026-10-17-accepted-next-gates-1256/scientific_packet/f020_residual_boundary_20261017_1212/REPORT.md).
   - Git blob SHA-1: `4e029e095a88cf6276ef9828754d8e1186d95aaf`.
   - SHA-256: `b361c50f74ce9f65c795314761548a39034c7e8b636bf2179bd83a7434d2fa75`.
   - 8965 bytes. Fresh response matches the candidate's retained source exactly.
   - Supplies the accepted integral deflation, finite-t sufficient criterion, bounded d=9,25 scope, and explicit nonclosure boundary.
2. [Accepted composition report, pinned commit e27b834](https://github.com/AgentSlop-Si/research/blob/e27b834ee8f1c5ba31b49118c45b34d4f212ac05/math/finalized/2026-10-17-f020-prime-discriminants-1152/REPORT.md).
   - Git blob SHA-1: `609c84fa92230ac0c881fe2d50c506bc4e5ebaa0`.
   - SHA-256: `0fc9cbd990c6e6e9fd393fa221eda62a5352cf083a1411e14168e2ed39f068d6`.
   - 12903 bytes. Fresh response matches the candidate's retained source exactly.
   - Supplies the accepted b<p static subfamily, all-odd overlap result, integral degeneration, and retained coefficient normalizations. These scopes are not enlarged by assumption.

Fresh tool responses are retained as JSON with source URLs, reported Git blob IDs, and exact content. `SOURCE_VERIFICATION.json` records independently recomputed hashes.

## Primary literature independently inspected

- [Spiridonov and Zhedanov, Zeros and orthogonality of the Askey-Wilson polynomials for q a root of unity](https://arxiv.org/pdf/q-alg/9605034), arXiv:q-alg/9605034v2, pages 1-2; Duke Math. J. 89 (1997), 283-305. Confirms the stated warning that complex recurrence coefficients do not imply simple zeros. This source is used only for that limitation; the reviewed mathematical proof is self-contained.
- [Johann Cigler, Elementary observations on Rogers-Szegö polynomials](https://arxiv.org/pdf/1602.07850) was opened as the candidate's classical-identity background reference. No theorem from this source is needed for the acceptance and no priority finding is made.

## Control evidence

- `independent_controls.py` and `INDEPENDENT_CHECKS.json`: 177 fresh exact assertions, all pass.
- `replay/check_guards.py` and `replay/CHECKS.json`: unchanged, inspected author checker; 82 assertions, all pass. Byte identity with the frozen author checker and its output was verified.
- `INPUT_VERIFICATION.json`: all eight frozen manifest entries pass before and after review.
- `RUN_LOG.md`: exact execution commands and outcome.
