# Independent C10 public package audit

21 October 2026 UTC

## Verdict

PASS for the exact inert public package c10_prime_field_cost_public_20261021_v1.zip: 188,311 bytes, SHA-256 6dcc3f39ce82d8ba3407705991cc9302db10580d0a675a1a4d1347af11b7201a. No repair is required. This detached audit verifies the archive, retained acceptance and source identities, disclosed transformations, historical inventory qualifications, bounded export boundary, and preservation of the accepted mathematical scope. It does not publish the package, alter any native record, or close the C10 owner.

The public manifest is 5,700 bytes, SHA-256 84c7e0150aad9d7f2b93d8536b2adfd25e9b26b838058eb4336f283ac7077d49. The public seal has SHA-256 88074f1b38aa7d8eb0cd2b725df03c54b46b8606378de76916fa3de362ec5a29. INPUT_BINDINGS.json records their measured sizes and all accepted-source pins. This verdict applies only to those bytes, not a subsequently edited archive with the same name.

## Archive and payload integrity

The actual ZIP, not merely its producer inventory, contains exactly the independently enumerated 35 permitted members. There are 33 manifest payloads plus MANIFEST.json and SEAL.json. Every archive member is an ordinary non-executable mode-0644 regular file containing valid UTF-8 text; JSON members have no duplicate keys or nonfinite constants. No directory, symlink, unexpected member, research/control program, or executable payload is present.

All members use stored compression and the fixed timestamp 2026-10-21 00:00:00. CRCs, local headers, central-directory metadata, names, sizes and data boundaries agree. The archive has no prefix, suffix, inter-member gap, extra field or comment. The ZIP payload is byte-identical to the supplied public tree. Every active manifest size and SHA-256, the seal-to-manifest binding, the seal-to-allowlist binding, and the independently supplied archive, manifest and seal digests pass.

All 14 active README links resolve to delivered members. All four active source-map targets resolve. References in historical proofs or inventories to missing programs and predecessor packages are explicitly historical references, not live file-inclusion or execution claims.

## Exact accepted sources

The complete accepted author v3 report, contract and input-domain freeze are unchanged. The complete independent mathematical review, acceptance and normal/optimized recorded result files are unchanged. The acceptance binds the delivered author report to SHA-256 2a0d28168c92d2738985d57a879e79879d5112d493a86a26943f90aeda973447 and the author manifest to ebe8cbde5ecc6fa51e5915e0f107ec7bc927fc40a7d146bbf3a57f8c465d3214. The mathematical review seal is 4300e34df5a36eb4f7853afaff112fc6a1ad29805b7ad8652d17cd49d50f51f7. The acceptance itself is 2,912 bytes with SHA-256 04fc115d4d36098d1e435a2e9820fc56f1b9e1b29928d990bf03131c796bece4.

Every retained review export belongs to the exact historical review seal, with that seal itself separately preserved as provenance. The recorded normal and optimized outputs agree byte-for-byte in both the author and independent-review pairs. Their numerical controls remain historical evidence; this public-package audit does not claim to have replayed them.

The identity ledger has exactly 24 source records: 21 byte-identical copies, two administrative locator projections, and one exact contiguous excerpt. All original and public lengths and hashes were checked against actual retained bytes, rather than trusted solely from the ledger.

The two projected reference files replace only their single predecessor-directory locator strings. The old-string size, hash and occurrence count match the disclosure. Replacing that one string in each retained original reproduces the entire delivered file exactly; no other byte changes. Each public projection has its own identity and is not presented as its original.

The prior independent review is a multi-topic original of 11,719 bytes, SHA-256 f8536528b7637caa0eac54e069e5f70a06559f349aa99a77508ab7d9fbfa7230. Only its exact C10 section, lines 47 through 61 inclusive with original line endings, is delivered. The excerpt is 3,518 bytes, SHA-256 3b55d9416809138b0a9d09bf6c397a2eb4a82b5e91170e158d976d3104784692. The excerpt's identity is never substituted for the complete original identity.

The original selected-system reduction review, sorting/sequential-2SAT report, source register and full prior multi-topic review all match their retained SHA-256 and independently recomputed Git blob identities. Their source-map locators use immutable repository commit URLs. No network refetch was performed in this packaging audit; the original independent mathematical review documents its earlier remote retrieval. This audit verifies local retained source bytes and the recorded origin bindings, not current remote repository state.

## Historical inventory and correction lineage

All four historical inventories are preserved exactly. Their 15 author-v1, 19 author-v2, 22 author-v3 and 13 review entries total 69 independently verified and exhaustively qualified entries. Original payloads were checked against each historical inventory, including byte-hashing excluded program bodies without parsing, importing, compiling or executing them.

Delivered members resolve to their current public paths. Omitted entries are explicitly distinguished as superseded candidate bodies, private owner snapshots, raw connected-service retrieval wrappers, or program payloads. The locator projections and C10 excerpt are separately classified. None of these historical inventories is promoted to the active package inventory or a claim of a complete original-directory export. Original bodies classified as omitted are not present as archive members under another name.

Both correction diff files are inert text and match independently regenerated unified diffs of the actual successive report and contract versions. Version 1's empty-input fixed-cost omission is repaired in v2. Version 3 preserves that repair and clarifies the existential witness statement and the binary notation. Historical pending-review headers remain unchanged and are superseded by the later exact acceptance, not silently rewritten. The separate reviewer proposal is superseded, non-authoritative and excluded.

## Mathematical scope preservation

The retained proof and independent acceptance establish an existential statement about the selected bilinear subsystem over a promised prime field: every closure-feasible selected system has at least one solution with all row directions in one common F_(p^2). They do not assert that every particular algebraic-closure solution lies in that field. An unrestricted one-vertex system may have higher-degree solutions while still admitting the required bounded-field witness.

The existing forest, degree-at-most-two component domains, canonical-label sorting, sequential at-most-one 2SAT and all-false repair are unchanged. Cross-component named points lie in F_p. Every required quadratic splits in the same chosen quadratic extension; all-false repair either selects a named base point or a nonbase point equal to no base-field name. Base-field transports preserve nonzero vectors in that extension. This supports common-field existence for the whole selected subsystem without promoting it to an all-solutions or whole-factorization theorem.

The preserved deterministic decision ledger is

D = O((N+M+1)(b^2+ell) + M b^3 + M log2(M+1)(b+ell)),

where b=ceil(log2(p+1)) and ell=ceil(log2(N+M+2)). The +1 covers fixed field-descriptor, initialization and decision-output work at N=M=0. Storage is O((N+M+1)(b+ell)) in the expressly charged record-random-access bit model. Untrusted primality and oversized/unreduced input costs are additional.

For supplied certified eta at odd p, the preserved witness surcharge is O(b^3+W(b^3+s^2 b^2)), with W<=min(N,M) and s=v2(p-1). The standard Tonelli-Shanks routine and its explicit modular-product budget are retained rather than replaced by an unpriced root oracle. Without supplied eta, witness setup is separately expected Las Vegas O(b^3), or a deterministic O(p b^3) scan surcharge; neither decision requires eta. At p=2, s=0 in the displayed uniform bound, the field is F4, no nonsquare is required or tested, and setup/root work is O(1+W).

Target extraction remains the separate same-model charge S_B^bit + O((N+1)ell+b+M E_B^bit+M b^2). Scalar setup or entry-access counts are not substituted for bit costs. The output is nonzero coordinate pairs, with O(Nb) row payload and O((N+1)b) total including the field descriptor and decision bit. Canonically normalized outputs incur the separate O(N b^3) surcharge.

Concrete target preparation/extraction, column compatibility, supported-entry scales, legal Green parameters and denominators, fixed endpoints, full two-Green factorization, Fourier application complexity and whole-C10 closure all remain open. Neither historical novelty nor an arbitrary-field bit theorem is claimed. This package audit preserves the earlier bounded mathematical acceptance; it is not a new whole-C10 proof or a fresh mathematical control execution.

## Export boundary and negative controls

All public member text was inspected under the exact inert allowlist, checked against source bytes and transformations, and scanned for known private locators, local absolute paths, native document/account/runtime locator patterns, and common secret patterns. Private owner-record bodies and raw retrieval envelopes are absent. The known private locator comparison produced no hits. Public repository source URLs, historical program names, source hashes and ordinary mathematical provenance remain intentionally visible. The assessment is bounded to these inputs and checks, not a universal assertion that every possible privacy or malicious-content pattern is detectable.

Twenty-one independent in-memory negative controls were rejected by their intended detectors: duplicate/missing/extra/traversal/absolute archive members; symlink and executable metadata; payload and manifest tampering; altered accepted proof bytes; a nonlocator projection change with updated public identity; an altered excerpt with updated public identity; a known private locator injected into prose; whole-owner closure promotion; universal rather than existential wording; removed empty-input overhead; free or scalar extraction; removed descriptor/normalization charges; omitted binary convention; removed integration exclusions; and duplicate JSON keys. Semantic/source controls were called directly where necessary so that a manifest mismatch could not conceal which detector rejected the mutation. The exact cases and rejection reasons are in NEGATIVE_CONTROLS.json. These are bounded controls, not exhaustive adversarial assurance.

## Audit execution and use

Only independently authored local byte, archive, inventory and metadata checks were run. No supplied research/control program was executed, imported, compiled or parsed. All four private source trees were byte-identical before and after checking, and the public subject archive remained unchanged. No repository, native table or other external state was written.

The subject package's producer-era statements that independent public auditing had not yet occurred are left untouched. This detached, exact-byte verdict supplies the later audit gate without retrospectively editing the evidence.

This audit archive contains only this report, VERDICT.json, CHECK_RESULTS.json, NEGATIVE_CONTROLS.json, INPUT_BINDINGS.json, MANIFEST.json and SEAL.json. Its manifest inventories the five substantive files; its seal binds the manifest. Its separately supplied final ZIP digest is the external trust anchor. A hash seal is not a digital signature. Retain the final ZIP, manifest and seal pins with this verdict; any later subject edit requires a newly bound audit.
