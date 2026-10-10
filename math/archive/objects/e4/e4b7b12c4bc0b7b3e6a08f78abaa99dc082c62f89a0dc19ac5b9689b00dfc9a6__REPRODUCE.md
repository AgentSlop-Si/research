# Reproduction and audit boundary

Run from this directory:

    python check_joint_bank.py
    python check_characteristic_zero.py

Both checkers were authored independently for this deliverable and use only the Python standard library. They do not import or execute predecessor or uploaded code. No network, installer, symbolic algebra package, or numeric root finder is required.

The first command re-hashes the two predecessor directories named by the assignment and asserts byte equality before/after its run. It writes RESULTS.json and the source hash snapshots. Its wall-clock seconds field and CHECK_RUN.log timing line are intentionally runtime-dependent; mathematical result fields are deterministic. The second command writes CHARACTERISTIC_ZERO_RESULTS.json.

The theorem is in GLOBAL_MOMENT_CHIRP_BANK.md. Its scalar-resolvent model uses constant edge weight λ on the natural cycle, scalar branch coefficients, and no separate diagonal correction to the individual chirp circulant. The full B construction does include the prescribed global diagonal term. The exact minimum r=(N+1)/2 applies to the individual scalar-resolvent chirp model only.

The root-free application expands every operation in K[z]/(p), degree r, into K operations. Its certified elementary costs are O(N³) setup and O(N²) per application, and not O(N). No bit-complexity, stability, unrestricted FFT lower bound, or publication-priority claim is made.

The source documents and their existing manifests are preserved in place. SOURCE_HASHES_BEFORE.json and SOURCE_HASHES_AFTER.json must be identical. MANIFEST.sha256 seals this new deliverable and excludes itself. Re-running a timed check intentionally invalidates its old results/log hash until a new seal is generated; preserve the sealed copy when independently replaying.
