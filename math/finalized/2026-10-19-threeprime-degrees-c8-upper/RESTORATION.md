# Reversible transport representation

Only two oversized JSON control files use a different publication representation. Their original complete bytes remain unchanged and recoverable. The other 97 scientific/support files are literal exact copies. Proofs, verdicts, original scientific manifests, owner dispositions, histories, priorities and scores are unchanged.

The logical source paths are threeprime/candidate/NEGATIVE_CONTROLS.json and threeprime/review/NEGATIVE_CONTROLS.json. Each is published at the same path with .gz.b64 appended. Decode RFC 4648 standard base64, then decompress gzip. SOURCE_REPRESENTATIONS.json gives the SHA-256 and byte length of the encoded text, compressed stream and exact original JSON. Base64 uses 76-character LF lines and a final LF. Gzip uses DEFLATE level 9, MTIME 0, no filename, and OS byte 255; the builder's Python/zlib versions and repeat-encoding check are recorded. No JSON is parsed and reserialized during encoding or restoration.

Run `python verify_package.py` to validate the physical transport package and every original source-manifest entry against its decoded bytes. The source manifests themselves retain their original filenames, byte counts and hashes. A generic filesystem-only source-manifest checker requires restored sources first.

Run `python restore_sources.py /path/to/new-source-directory` to restore all 99 scientific/support source files, including both complete original JSON files, at their original relative paths. The destination must not exist. This command first verifies the entire transport package, then verifies every source before writing it and checks every write. It executes no research program. It restores the source trees, not the transport package's newly authored README or top-level transport metadata. Those remain in this publication directory.

For manual restoration, base64-decode the .gz.b64 text, gzip-decompress the resulting stream, save under the logical .json name, and compare its SHA-256 and byte length with SOURCE_REPRESENTATIONS.json and the unchanged source MANIFEST.json. Do not run any scientific program merely to verify packaging integrity.

This change is solely a reversible publication transport adjustment after the direct large-file verification route failed. It changes no mathematical statement, original data byte, acceptance, cost claim, scope, attribution, owner score or priority. Whole originals are also retained locally outside the publication allowlist. The previous reviewed packet remains untouched.
