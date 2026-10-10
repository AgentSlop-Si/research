# Verification and scope

1. Verify the immutable ZIP against its external SHA-256 receipt.
2. Extract to a new directory without overwriting earlier packets. Check every SHA256SUMS entry, and then the artifact manifest.
3. INTAKE_IDENTITIES.json records the original incoming file hashes. SOURCE_EXPORT_TRANSFORMS.json distinguishes those original bytes from publication-safe exports; a redacted export is not claimed to have the original hash.
4. The three recursive member inventories contain names and byte hashes only. They establish identity coverage, not execution, correctness or independent test counts. Embedded archive payloads are intentionally absent.
5. Read MATHEMATICAL_STATUS.md and the final Phase42 audit before interpreting source claims. The dated novelty report remains historical. Inert certificates can be checked from the mathematical definitions and witness data; source executable programs and raw logs are deliberately not distributed.
6. Distinguish source-supplied evidence, independently reconstructed reviewer evidence, and packet-integrity checks. No historical run is counted again in this intake.

This archive does not publish to any repository, replace Library files, edit a Sheet or change an earlier accepted packet. New Schur fusion and Q01 consolidation notes are outside this packet.
