# Scope, privacy and replay boundaries

## What is included

- The accepted scientific report, with four explicitly recorded public-export edits only. Its original SHA-256 remains f3fac36a41302dcbb1f354efc9d1ef6c781c2a5a3dfa75c909d86b60b5d38828.
- The original null-cost ledger, independent sealed review and frozen-packet result receipt, byte for byte.
- A public projection of the independent verdict, selected source-role/identity records, the original/export hash map, and a build-time source-verification receipt.
- A self-contained, standard-library public verifier and negative-control suite.

## What cold public checks reproduce

`verify_packet.py` checks every included payload file against an exact allowlisted root-relative inventory. Only the root MANIFEST.json and SEAL.json are excluded from that payload inventory; their relationship is checked separately. Extra files, missing files, duplicate paths, traversal, symlinks, wrong byte lengths, wrong SHA-256 values, duplicate JSON keys and nonstandard numeric constants are rejected. Fixed scientific/status fields receive strict type checks, so booleans cannot stand in for integer widths or priority, and numeric zero/false cannot stand in for null costs. Selected exact evidence digests and original/accepted identity anchors are fixed in the verifier.

`verification/test_controls.py` cold-copies the packet and confirms rejection of resealed false completion, zero/false costs, changed or wrongly typed widths/priority, changed source identities, changed report/evidence, extra private capture and missing nested evidence; it also checks malformed manifests, a duplicate JSON key and symlinks. Resealing here means the manifest and seal were updated after mutation, so key semantic/identity controls are not merely hash-mismatch tests. Tests never mutate the baseline packet.

A PASS establishes only those finite checks. The unsigned seal is a hash commitment, not a digital signature or proof of authorship. Anchor the ZIP or manifest digest through an independent trusted channel. An attacker who replaces both verifier and all anchors is outside the protection of an unauthenticated, self-contained bundle.

## Omitted deliberately

Original recovered archives and extracted research programs, manuscripts/PDFs and upstream source fulltexts are omitted for compactness and to avoid unnecessary reproduction. Raw native API captures, private table URLs, local environment paths, Library identifiers/download URLs, coordination messages and approval state are not included. Original full manifests and detailed recovery/search records are omitted too; selected role/hash projections do not pretend to be their full contents.

At export, all 85 candidate source-manifest files and all 21 review-manifest files were checked for exact inventory, lengths and hashes, and 62 ZIP members were checked against extracted bytes. These facts are build-time receipts about omitted originals, not repeatable cold checks from this ZIP alone. The exported report's transformation from the original was checked at export; reproducing that transformation requires the original report bytes. Pinned GitHub locators identify source bodies but are not fetched by the verifier and no present-day accessibility promise is made.

The independent review's historical 112-record replay, 62 member checks, structural recurrence and five controls remain attributed results of that review. This packet does not rerun them, execute the inherited compiler, test algebra/coefficient correctness, verify Lean kernels or reproduce whole-source/mathematical evidence. It also cannot reconstruct the original source manifest merely from its digest.

## Unchanged scientific boundary

The older matched manifest d42781f8737b83c1e886eb70560128169ae39aa057da7f43325d12bfb868d060 is not the accepted later matched-review manifest 4e5e75b8e1fd946a3224900231e732f2768180285696c9e09cd06faba618b9f3. The accepted semantic-audit manifest is 937b256ad983a6a23ddc024d7d2bd8f11a6d1d7b3e0ccdbd83dddb35dfd16a32; both later bodies remain unrecovered in the bounded search. Their stated conclusions are attributed native evidence, not a fresh body verification.

The old literal q=8, a=4, e=5 layer count 162 is obsolete; the accepted correction is 170. Legal cancellation reduces prior FFT calls from 16 to 12. Local candidate 89 versus optimized prior 90 layers is not a factor-two depth advantage or a complete-program comparison.

All eight complete costs remain null. No cost-advantage or no-advantage, novelty, asymptotic, bit-complexity, stability, kernel-verification or completed-pilot claim is issued. Exact-r emitted data width is not peak total memory. The exact-complex scalar model, finite implementation checks and bit/numerical model remain distinct. Missing source extraction does not imply free advice in the formal theorem; the accepted imported tensor dependency is not reopened as a conjecture.
