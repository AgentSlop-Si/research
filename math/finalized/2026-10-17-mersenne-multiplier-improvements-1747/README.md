# Mersenne multiplier improvements: reviewed research packet

17 October 2026. Three completed source-and-review pairs, including all final review fixes and seals.

## Results and limits

- **Lazy Fermat transform:** exact signed lazy residues remove inner-stage canonical corrections. The saved matched experiment reports approximately **1.08–1.26× convolution-only** improvement. Original positional conversion and final reconstruction are excluded. The coefficient lift has O(N) live bit volume in the stated skewed regime, but the collective-layer/movement saving and recursive-cost saving remain open. Read [source](lazy/source/REPORT.md) and [final review](lazy/review/REVIEW.md).
- **Native negacyclic recursion:** the classical modular recursion lowers ideal child volume from about 4n to about 2n. A fixed Mersenne-prime positional radix, including p=3, and p^d grouping are compatible with the odd-modulus construction. The paid upper bound remains O(n log n log log n) under the stated regime, with binary/radix conversion separately charged. No practical-speed or new-asymptotic claim follows. Read [source](negacyclic/source/REPORT.md) and [final review](negacyclic/review/REVIEW.md).
- **Mersenne conversion:** exact factorial-Toeplitz shifts and local carry/grouping interfaces give a non-triangular converter, including the corrected single-group path and default-disabled recursive diagnostics. A same-scale general multiplication and the stated setup/diagonal costs remain paid. Read [source](conversion/source/REPORT.md) and [final review](conversion/review/REVIEW.md).

None of these results establishes multiplication in little-o(N log N), a growing family of Mersenne primes, or historical priority for classical ingredients.

## Integrity and reproducibility

Run `python verify_packet.py` for a read-only current-byte check. `PUBLICATION_MANIFEST.json` is the authoritative manifest of this publication. `SOURCE_REVIEW_BINDINGS.json` records both accepted-original and published hashes, and `ADAPTATIONS.json` identifies every changed copy. All accepted originals were retained privately, unchanged.

Nested manifests, SHA256SUMS files, verdict hashes, and seals retain their **original-review provenance meaning**: they name accepted original bytes, not a resealed scientific rerun of adapted publication copies. Some privacy/portability adaptations therefore intentionally make a nested original hash differ from a published copy. Use the root publication manifest to verify current bytes. The scientific kernels and final review corrections are preserved; there was no mathematical re-audit and no scientific program was executed during publication.

Portable review drivers resolve sibling source directories. The lazy and conversion review drivers use the root publication manifest for their current-byte gates. Review outputs and timings are the saved original runs, not outputs of a rerun of adapted drivers. Review drivers that write output should be run in a disposable copy, since overwriting saved evidence will change its manifest hashes.

The negacyclic and conversion reviews additionally require the original archive, and conversion requires two prior reports. These are **not bundled** here. Put `source.zip`, `prior_synthesis.md`, and `prior_binary_packing_report.md` in `external-inputs`, or set `MERSENNE_EXTERNAL_INPUTS` to their directory. The preserved source pins specify their exact hashes. Prefer an external directory via MERSENNE_EXTERNAL_INPUTS: the strict packet verifier rejects added files inside the packet. If using the default external-inputs subdirectory, verify the untouched packet first. Required provenance checks fail if those inputs are missing or different; nothing is silently skipped. Candidate-only controls do not need these historical inputs.

This is an additive research-preservation packet. No table, OPEN index, existing repository file, or existing README is changed by its publication.
