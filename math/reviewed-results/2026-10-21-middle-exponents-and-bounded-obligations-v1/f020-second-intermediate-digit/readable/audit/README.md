# Independent audit of the second intermediate digit public package

Accepted only for the exact main ZIP named in MAIN_BINDING.json. REPORT.md explains the independent byte, source-lineage, projection, scope, inventory and privacy review. VERDICT.json records its bounded acceptance. AUDIT_RESULTS.json summarizes the checks without private working files or raw diagnostics.

The theorem remains exactly n = 2p^3 + 2p, every odd prime p, integer s > 3 and every characteristic-zero primitive p^s-th phase, in the original P/H/kernel normalization. There are 2p^3 high roots and 2p outer roots, with no zero. Both the finite bad-reduction caution and the historical b = 2p original-byte mismatch remain explicit. This audit does not enlarge the theorem or accept the unrecovered historical original bytes.

Only root MANIFEST.json and SEAL.json inventory this detached audit. It contains no copied historical manifest. The optional, newly authored verify_binding.py is a read-only standard-library byte verifier, not a scientific program. It executes no archive member, changes no file and performs no external action.

After independently inspecting this verifier and obtaining the audit manifest hash from a separately trusted record, it can be run as:

    python verify_binding.py MAIN_ZIP_PATH --audit-manifest-sha256 TRUSTED_AUDIT_MANIFEST_SHA256

It first verifies the exact extracted audit files and manifest pin, then checks the main archive and its manifest against MAIN_BINDING.json. Hashes bind bytes, not authorship, signatures or mathematical truth. No package can supply its own external trust anchor. Any later revision needs a new review.
