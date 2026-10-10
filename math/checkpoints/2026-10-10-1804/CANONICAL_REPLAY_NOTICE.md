# Canonical hashes and the publication copy

The review receipts bind the canonical source bytes that were actually reviewed. Those canonical digests are intentionally preserved even when a publication copy omits private delivery metadata. SOURCE_EXPORT_BINDINGS.json supplies both digests and the exact transformation type for every included source.

Five source files have privacy-only changes in this export: the four dated Sheet JSON records and the prior fixed-support review report. No mathematics, coefficient, proof, condition, result or verdict was changed. Exact original metadata values remain in the preserved canonical source records outside the public archive; their values are not disclosed here.

Some inherited reproduction programs verify canonical source digests before performing their mathematical computations. In particular, the symbolic checker checks the earlier fixed-support report. Such a canonical-hash gate will correctly distinguish this sanitized export from the original. Do not describe a direct rerun of an unchanged inherited checker against transformed inputs as already verified or turnkey. In a separate writable reproduction copy, inspect the transformation ledger and adjust only a metadata-only digest gate to the recorded export digest if appropriate. That is a new reproduction action, not an alteration of this frozen reviewed packet. Preserve every mathematical input and guard.

VERIFY_ARCHIVE.py is a newly written data-integrity helper for this archive. It verifies all shipped byte digests, the complete allowlist and both compressed certificate reconstructions without executing or importing any research program. It does not independently re-prove the mathematics.
