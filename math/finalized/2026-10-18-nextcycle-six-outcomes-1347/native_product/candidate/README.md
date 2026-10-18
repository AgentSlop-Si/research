# Precision-targeted Mersenne product interface

Read REPORT.md for the exact service contract, precision proof, complete costs, and narrowly scoped barriers. This is not a new fast general multiplier.

Run `python fresh_controls.py` to reproduce finite checks. Production arithmetic uses the byte-identical pinned helper in `dependencies/kernel_stream.py`; independent native oracles appear only in the test harness. Run `python verify_package.py` for package hashes.

New results:
- Final-only reconstruction at H=2m+ceil(log2 L), with paid H+g shift guards.
- Canonical p^d product precision and an explicit odd-modulus mismatch.
- Exact q(q+1)/2 two-wide slab-pair schedule with bounded row carries.
- Homogeneous-charge slab optimization barrier and native exponent potential.

No external writes. Independent review still required.
