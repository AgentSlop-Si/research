# Remaining-gate partial results

19 October 2026. Repository: `AgentSlop-Si/research`. Last independently verified input base: `91354fa579f1d463e355abfc056cd20576637f82`.

This packet preserves two independently accepted partial-result packets. Neither result closes its broader research owner. It makes no historical-novelty or worldwide-priority claim and performs no scientific rerun.

## Accepted outcomes

- **F020 / alias F023:** three exact obstructions rule out the proposed positive-metric mechanisms for the actual family. Diagonal similarity cannot make the residual matrices normal for every primitive odd order and `3 <= b < d`. At `b=4`, arbitrary affine similarity cannot make the matrix Hermitian for every primitive odd order `d >= 5`. Full-order positive metrics exist but cannot decouple any residual cut `2 <= b < d`, at any primitive embedding. **Ordinary kernel nonisotropy and unrestricted ordinary squarefreeness remain open.** Start with [the report](f020/candidate/REPORT.md), [independent review](f020/review/INDEPENDENT_REVIEW.md), [verdict](f020/review/VERDICT.json) and [checks](f020/review/INDEPENDENT_CHECKS.json).
- **Unrestricted C8 phase minimax:** the accepted global lower bound is `sin(pi/16)/sqrt(13+4*sqrt(3)*cos(pi/16))`, approximately `0.04384873791488374`. The existing `sin(pi/16)` upper witness is a strict local minimum across all 15 quotient phase directions, modulo scalar phase transfer. **The sharp unrestricted global value remains open.** The remaining universal spectral assertion concerns at most five eigenvalues in every open arc of width `pi/4`. Start with [the report](phase/candidate/REPORT.md), [proof](phase/candidate/PROOF.md), [independent review](phase/candidate/REVIEW.md) and [remaining lemma](phase/candidate/GLOBAL_LEMMA.md).

The F020 review preserves 19 replayed author assertions and 55 independent exact/source-integrity assertions, including 25 mathematical assertions. The phase review independently checks the analytic implications, constants, coefficient formulas, Gram determinant and spectral equivalences; it does not claim a full independent recreation of every exact field computation. These are inherited review results, not new packaging runs.

[FINAL_ACCEPTANCES.json](FINAL_ACCEPTANCES.json) binds the final acceptance scope and exact reviewed artifacts. Historical candidate status text, run logs, exploration records and the resolved initial F020 checker-interface failure are retained unchanged. No characteristic-zero counterexample, new root-order census, global-minimax classification, automatic all-A extension, owner closure, priority change or discovery-count change is claimed. No native record update or repository publication is asserted without a separate receipt.

## Evidence and privacy boundary

Every file declared by the three source manifests is represented. Proofs, checkers, already-produced outputs, review findings, prerequisite authored proofs/reviews and original source hashes are preserved. A single privacy-only metadata projection removes an internal reviewer identifier from phase provenance; all other JSON values remain unchanged. [COPY_BINDINGS.json](COPY_BINDINGS.json) maps accepted original hashes to publishable hashes, and [PROJECTION_DISCLOSURE.json](PROJECTION_DISCLOSURE.json) documents that operation. Private workbook material and licensed paper bodies are not included. See [OMISSIONS.json](OMISSIONS.json).

Nested source manifests are exact historical records of the accepted pre-projection bytes. They are not replacement root manifests for the projected directories. The root [MANIFEST.json](MANIFEST.json), [PRESERVATION_ALLOWLIST.json](PRESERVATION_ALLOWLIST.json) and [SEAL.json](SEAL.json) govern publication. Original source paths and historical run commands are retained as provenance; they may refer to the original local research workspace. Scientific scripts have not been rewritten for relocated execution, and their presence is not a claim of portable rerun verification.

## Check package integrity

Run `python3 -B verify_package.py` from this directory. This verifier checks only the exact file set, file hashes, copy bindings, accepted-source manifest correspondence, preserved acceptance boundaries and a limited privacy scan. It does not import or execute any research checker, rerun scientific certificates, recover external sources or independently repeat the scientific reviews. The root manifest excludes only itself and the seal. The seal binds the root manifest, allowlist and final acceptances without circular hashes; the local handoff separately binds the seal.

Publish exactly the allowlisted files under `math/finalized/2026-10-19-remaining-gate-partial-results`. Exclude the release parent, local builder, local gate, local verification receipt and handoff. The publisher must freshly guard the repository base and verify remote bytes; this local packet does not claim those steps occurred.
