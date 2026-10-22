# Independent public-package audit

Accepted only for the exact first-intermediate-digit public ZIP identified in MAIN_BINDING.json. Read REPORT.md for the inspection scope and VERDICT.json for the bounded acceptance. AUDIT_RESULTS.json contains structured independent byte, lineage, inventory, privacy, and rejection-control results. This is not a fresh scientific replay or a global novelty certificate.

The main archive is an inert documentary selection. This detached audit includes one newly authored standard-library byte-verification program, verify_binding.py. It executes no archive member or scientific program, performs no external write, and does not prove the mathematics. Running it is optional; all bindings can be checked independently.

After extracting this audit, one may run: python verify_binding.py MAIN_ZIP_PATH --audit-manifest-sha256 TRUSTED_AUDIT_MANIFEST_SHA256

Supply the audit manifest SHA-256 from a separately trusted delivery record, not a value merely recomputed from an untrusted archive. The verifier first checks this audit's exact local file set and all hashes against that pin, then reads the main ZIP and checks its exact archive and manifest pins. It writes no files. Hashes bind bytes, not signatures or mathematical truth.

Only the root MANIFEST.json and SEAL.json inventory this audit. It contains no original research manifest snapshots, private source locations, working directories, or raw private diagnostics. Any later revision requires a new review.
