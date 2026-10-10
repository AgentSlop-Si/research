# Fourier research supplement: 16:28 UTC batch

9 October 2026. This supplement adds three explicitly identified source archives to the existing research master. It preserves the source bytes and supplies independent audits; it does not claim an exact arbitrary-input sub-N-log-N Fourier transform.

## Read first

1. CURRENT_CHECKPOINT.md is the updated all-branch checkpoint, intended to replace the master root checkpoint after review.
2. THREE_ADDITIONS_AUDIT.md compares new claims with the inherited results and explains model boundaries.
3. audits/v9, audits/phase18 and audits/dual_onion contain independent branch proofs, fresh checker code and results. composite_extension/ adds a bounded arbitrary-modulus variance theorem, keeping its sharper numerical conjecture separate.
4. SOURCE_ARCHIVES.json records the three Library identities. SOURCE_MEMBER_INVENTORY.json distinguishes inherited versus unseen bytes recursively. NEW_CONTENT_INDEX.md lists byte-new contents.

## Source preservation and safety

The three unmodified uploaded ZIP files are in source_archives/. They recursively contain inherited archives. The compiled v9 benchmark and all uploaded Python/C++/shell code were treated as inert source data. None was executed, imported or compiled. Only independently written audit scripts were run.

The current batch contains 562 recursive member occurrences and 381 unique member-byte hashes. Of these hashes, 90 are absent from the declared prior comparison sets: 88 text/data contents, one new nested-archive byte stream and one compiled binary. Two other nested archive streams are byte-identical to prior top-level source archives and are correctly classified as inherited. The baseline remains its dated inventory of 349 Library items and 528 canonical text contents. The 14:50 and 15:20 additions remain separate; no mathematical novelty is inferred from byte novelty.

All 714 embedded hash-manifest entries pass. This verifies source consistency, not mathematical correctness.

## Portable provenance check

Run python3 audit_provenance.py from any working directory. It locates its local source_archives and PRIOR_HASH_REFERENCE.json. It performs bounded recursive ZIP reading, rejects unsafe member paths and links, and verifies all source manifests.

The comparison file contains hashes and prior inventory provenance, not the full earlier source corpus. For full historical context, retain this supplement inside additions/1628/ of the master archive.

Branch scripts specify their own dependencies and portable invocation in their reports. Their checks support the written proofs; finite-field tests alone do not establish complex infeasibility or all-length claims.

## Research stopping condition

This is a bounded audit and synthesis of the supplied batch. It stops after source accounting, theorem reconstruction, independent checks, corrections and a sharply scoped new consequence. The exact unrestricted project target remains open; no indefinite search is implied.

