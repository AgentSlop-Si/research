# F020: completion of the adjacent leading-two family

This additive source collection records the independently accepted central-root theorem for n = 2p² + 1. For every odd prime p, every integer s > 2, and every characteristic-zero primitive p^s-th root q, the original H and P polynomials are squarefree and the original algebraic-square Christoffel–Darboux kernel is nonzero at every P root.

Combined with the unchanged prior theorem for r >= 3, the completed family is n = 2p^r + 1, with odd prime p, r >= 2 and s > r. This is a scoped algebraic result, not a global F020/F023 closure, arbitrary-degree or other-digit theorem, odd-composite-order result, novelty claim, or FFT-speed/complexity claim. Derivatives are ordinary characteristic-zero derivatives; the squares in the kernel are algebraic, not absolute-value squares. No all-root constant derivative valuation is asserted.

## Read the evidence

- [Exact claim boundary](SCOPE.json) and [contribution disclosure](ATTRIBUTION.md).
- [New central proof](author/REPORT.md), [fresh whole-proof review](independent-review/INDEPENDENT_REVIEW.md), and [accepted verdict](independent-review/VERDICT.json). The unchanged proof retains its candidate-era wording. Final accepted status comes from the exact fresh review, not a rewritten source manuscript.
- [Unchanged prior proof](prior/REPORT.md), [prior separate review](prior/INDEPENDENT_REVIEW.md), and [historical partial scope](prior/SCOPE.json). The prior proof establishes every r >= 3 and the zero/noncentral r = 2 roots. The new proof resolves its remaining 2p central nonzero roots. Historical partial wording is intentionally preserved.
- The author and independent-review control directories provide exact readable programs and their fixed results. Finite-prime/field controls are auxiliary checks, not a substitute for the uniform proof. The fixed p = 3 integer-polynomial identities and uniform all-e >= 18 bound are explained in the proof and review.
- [SOURCES.json](SOURCES.json) maps each readable copy to an exact archive member. [SOURCE_LEDGER.json](provenance/SOURCE_LEDGER.json) records original identities and the public-only source-locator projection. No mathematical text, program, certificate, or result was changed by this wrapper.

## Complete reproducible release

[release.zip](release.zip) is the complete 40-file public release, exactly 1,379,178 bytes, SHA-256 667b37740cd2229082899e726a6efdb7e2be8b2e5d177eed5d3869bbcb79ec4e. It retains the complete earlier adjacent-degree ZIP and all nested source dependencies unchanged. [validation.zip](validation.zip), SHA-256 4ce62ff03bef6e9868f22329085ba3f0e52af4fc93e02729dbc2d03b025a71ba, retains all cold validation receipts and their checksums. Key receipts are also readable in [receipts/](receipts/).

The readable subset here is for browsing, not a standalone reconstructed release. Historical manifests are exact source inventories and will refer to additional files inside release.zip. To reproduce, extract release.zip into a fresh directory. With assertion-enabled Python 3.12 and SymPy 1.14.0, run its root verify.py with --integrity-only, --controls, and --negative-controls. Validation itself uses no network. The root verifier handles the public locator projection; the review's optional historical --author check instead expects the original unprojected author source.

The retained cold receipts record four current mathematical programs, five deterministic outputs, and 45 rejected mutations. They record zero rerun inherited mathematical programs. Publication of these records does not claim a new mathematical review or a new execution of those controls. SHA256SUMS covers every file in this collection except itself. Hashes identify bytes; they do not establish truth, authorship, priority, or a cryptographic signature.
