# Effective positive-sign chirp cutoff

The proof is `EFFECTIVE_POSITIVE_CHIRP_CUTOFF.md`.

Its conclusion is an explicit cutoff `N0 = 2^(2^534)` for the accepted two-Green obstruction at every eligible `N = 5m`, `gcd(m,5)=1`, `N = 1 mod 4`, with `N >= N0`. It covers every primitive additive character, including both real values of the Gauss sum, on the positive-epsilon curve. The negative-epsilon curve and unmatched endpoint permutations remain outside the conclusion. The existing `q = 1 mod 241` square-modulus family is preserved separately.

`source_inputs/` contains the exact two accepted input reports as inert text, with their original SHA-256 identities. No source program is included or executed.

`original_checks.py` is newly written standard-library Python. Run it with:

    python original_checks.py

It verifies the accepted input hashes, exact cyclotomic anchor identities for all four embeddings, chart coverage, determinant-degree counting, cutoff arithmetic, a fresh Macaulay rank-minor toy identity and a field-norm control. Its current output is `ORIGINAL_CHECKS.json`. It does not enumerate new finite-N targets or reproduce the accepted N=5 computer-assisted certificate.

The proof uses Kollár (1988), Theorem 1.5 and Corollary 1.9, only for the degree bound. A primary-source URL is in the proof. No copy of the copyrighted paper is distributed in this packet.

`MANIFEST.sha256` seals every other file in this packet. This packet contains local research artifacts only; no external service was modified.
