# ALG-036 nondivisible equality and gap packet

REPORT.md proves the equality classification of the accepted Gaussian projector bound, a strict fixed-parameter nondivisible gap, and exact counterexamples to rounded blocks being globally optimal. It leaves the exact nondivisible optimizer open, explicitly reduced to a compact simplex integral for rank two in three coordinates.

The full geometric Brascamp-Lieb equality theorem is credited to Valdimarsson and checked in the primary author-hosted preprint. The starting inequality is credited to the earlier reviewed ALG-036 packet.

Fresh finite controls:

    python controls/check_nondivisible.py

They use Python and SymPy, make no network calls, and execute no inherited programs. The controls are not a replacement for the general proofs or a global optimization certificate. RESULTS.json records their scope and counts.

This is a local proof candidate. No external writes or changes to inherited artifacts were made. Independent review belongs in a separate packet. Verify integrity with:

    sha256sum -c MANIFEST.sha256
