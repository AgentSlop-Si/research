# Reviewed Fourier contracts and sparse defect rank gate

10 October 2026

This static packet preserves two independently accepted results at their stated scopes: the Q01 all-length normwise Fourier consolidation and the fixed sparse-defect rank gate. Their accepted mathematical texts are byte-identical copies. The two results retain separate computational models and do not establish an unrestricted exact Fourier speedup or a general Fourier lower bound.

## Read the results

- [Q01 finalization](q01/Q01_FINALIZATION.md) and [independent acceptance](q01/review/INDEPENDENT_ACCEPTANCE.md): the corrected interpolation construction remains canonical. The approximate guarantee is deterministic relative Euclidean error on represented dyadic inputs under its charged growing-word RAM contract. All outputs, preparation, addressing, memory movement, precision generation, and fallbacks retain their stated costs. The Taylor construction remains an alternative at its weaker supported accuracy scope. The separate exact Necklace–Green transport is unconstructed.
- [Sparse defect proposition](schur/PROPOSITION.md) and [independent verdict](schur/review/PROOF_VERDICT.md): fixed rectangular factors over any field with a common nullity-one defect map have the stated rank and simultaneous-input weight constraints. The arithmetic conclusion requires additive independent literal charges on the actual common input. It does not constrain shared computation, adaptive or nonlinear decompositions, lookup/tabulation, or FFT fallback.
- [Scope and evidence](SCOPE_AND_EVIDENCE.md) states exactly what this export includes and what its saved control counts mean.

## Identities and reproducibility

[Accepted source bindings](ACCEPTED_SOURCE_BINDINGS.json) identifies the accepted notes, source proof decisions, and the original Q01 packet. [Source export transforms](SOURCE_EXPORT_TRANSFORMS.json) distinguishes copied bytes from the sole sanitized provenance file. The original Q01 ZIP is identified by hash but is not nested in this static packet.

The Q01 source tree and its acceptance files are unchanged. The Schur proposition, proof verdict, review receipt, reviewed identities, and saved mathematical outputs are unchanged. The Schur provenance JSON omits private conversation URL entries and local review paths; it retains source archive hashes and mathematical scope. Original review receipts may name source programs or tracking files not included here. Those names and hashes describe the historical reviewed source inventory, not the contents of this static export. Root ARTIFACT_MANIFEST.json and SHA256SUMS define the exported inventory.

No submitted program, predecessor verifier, or saved mathematical control was executed for this packaging step. Static hashing and link/archive checks are integrity checks. No historical tests are recounted as new mathematical tests; no discovery ranking, global proof count, historical-priority decision, production implementation certification, or practical crossover claim is added. The acceptance of source proofs and the separate acceptance of these export bytes are distinct records.
