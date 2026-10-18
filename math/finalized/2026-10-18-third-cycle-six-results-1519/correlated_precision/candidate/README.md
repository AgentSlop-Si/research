# Mersenne correlated-product interface: rank and guards

Read REPORT.md for the exact theorems, restrictions, complete cost ledger, and unresolved gate.

- Fixed-precision separated-input ring-bilinear sharing needs at least 2L scalar products for L>=3, even on the bounded Taylor images.
- Ordinary integer-point interpolation needs exactly v2((2L-2)!) uniform guard bits for the unrestricted product-coefficient interface.
- A fully paid guarded implementation and optimal six-product length-three control are included.
- No general little-o multiplier or historical novelty is claimed.

Run `python fresh_controls.py` for the deterministic controls and `python verify_package.py` for source/package hashes. Dependencies are copied and pinned accepted arithmetic, not newly claimed work. No external writes were made.
