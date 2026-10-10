# Replay and dependency boundaries

Run with Python 3.10 or newer; only the standard library is needed.

    python check_certificate.py --out-dir infinite-chirp-replay
    cmp EXACT_RESULTS.json infinite-chirp-replay/EXACT_RESULTS.json
    python verify_seal.py

The checker writes only into the explicitly selected output directory. Its deterministic JSON should reproduce byte for byte. It does not run or import any predecessor program. The transcript line in CHECK_RUN.log records the output hash and aggregate counts.

INFINITE_CHIRP_EXCLUSION.md is the finished theorem and proof. The report deliberately isolates the explicit family from the additional generic-parameter theorem in the prior draft, which is preserved unchanged under source/.

The accepted N5 all-order computational exclusion and accepted odd-chirp identities are named dependencies. Their report snapshots and manifest snapshots are included under source/; full predecessor replay packages remain separately frozen in review_n5_all_orders and review_chirp_feedback. The new script independently rechecks the formula and restriction arithmetic but does not claim to repeat all 576 N5 order pairs.

PREDECESSOR_INVENTORY.json and PREDECESSOR_INVENTORY.md list manifest-covered construction and review files in this feedback/chirp lineage for checkpoint assembly. Only manifest-covered files and the manifest files themselves are listed; mutable scratch, caches, and undeclared extras are excluded. SHA-256 validates archival integrity, not mathematical correctness.

The package's SEALED_MANIFEST.json covers every regular file except the two manifest files themselves. SEALED_MANIFEST.sha256 covers that JSON. verify_seal.py hashes data only, rejects missing, changed and extra regular files (excluding Python bytecode caches), and does not execute snapshot code.
