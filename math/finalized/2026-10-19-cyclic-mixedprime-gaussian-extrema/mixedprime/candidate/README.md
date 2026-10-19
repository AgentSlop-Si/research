# Two-prime Fourier equality-mask progress

This frozen candidate proves the complete N=2q classification for every odd prime q, plus two uniform partial ranges for all distinct primes p<q: d<q permits only d=1,p; (p-1)q<d<pq is impossible. Full mixed-prime divisibility and M-SPARSE-DEFECT remain open.

Read REPORT.md for the complete fixed-phase proofs, scope, inherited original-model consequences, and exact obstruction to a naive weighted CRT extension. THEOREM.json states the precise claims. The candidate is pending independent review and does not self-accept.

Run `python verify_mixedprime.py` to reproduce only the newly written standard-library exact controls. It executes no historical program. RESULTS.json reports the checks; POSITIVE_MASKS.json and NEGATIVE_CONTROLS.json preserve the exact masks and failures; ORIGINAL_MODEL_CONTROLS.json contains full rational cyclotomic inverse/error witnesses. All outputs were generated successfully with empty RUN.stderr.

Source reports were copied as inert data under sources/ and bound in SOURCE_BINDINGS.json. MANIFEST.json records file hashes; SEAL.sha256 binds the manifest. No external service, owner row, status, priority, or repository was changed.
