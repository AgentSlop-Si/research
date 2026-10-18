# Verification and reproducibility boundaries

## Package verification

Run `python verify_package.py`. An optional first positional argument selects a relocated public root. This verifies the exact allowlist, manifest and seal, byte-copy/projection hashes, JSON validity, retained owner boundaries, and known private-locator/credential patterns. It runs no mathematical computation and needs no source-paper or private-register access.

## Scientific material

The only candidate scientific program supplied is finite_chirp/candidate/checks/check_mapping.py. It is preserved byte-for-byte. Its pre-existing RESULTS.json records six bounded exact normalization controls at N=3,5,7,9,11,13. Running that program requires SymPy and overwrites RESULTS.json. Use a separate working copy for any voluntary replay; do not mutate this frozen packet. A later run would be new execution evidence, not the original recorded result.

No archived programs, 250-certificate finite-chirp array, Harper finite suite, FCUT historical controls, or F015 implementation/tests were rerun during packaging. The accepted source/audit texts and comparison/disposition evidence retain their own historical and source-access limitations. Private documentary builders/verifiers are excluded because they require omitted native inputs; their original hashes and outputs are preserved as provenance. The public verifier replaces only public-package integrity checking, not those original source checks.
