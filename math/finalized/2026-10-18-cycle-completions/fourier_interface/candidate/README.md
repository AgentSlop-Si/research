# Two-shear R30 Fourier interface

An exact full cyclic Fourier construction now contains eligible instances of
the implemented rho=3 R30 rewrite. It needs two nonmonomial boundary shears;
a modulo-3 proof shows that one cannot suffice over Gaussian dyadics.

This closes the proposed local-boundary route as an optimization attempt:
the fully charged literal kernel uses 12 real additions per pair versus 4
for the ordinary butterfly. Rescaling and batching do not remove that excess
in the stated separately evaluated scalar model.

For N>=8, an explicit cyclotomic coefficient-lane representation supplies exact
roots without silently broadening R30's coefficient class. Its expanded
storage and runtime are charged; it worsens complexity rather than improving
it. No new FFT speedup or global lower bound is claimed.

Files:
- PROOF.md: exact interface, minimality, complete DFT, representation contract.
- OPERATION_LEDGER.md: scalar, full-transform, lane, width, and conversion costs.
- verify_interface.py: fresh exact tests, no supplied R30 program execution.
- verification.json: actual run results.
- eligible_window.json: exact guarded interior descriptor.
- SOURCES.md: reviewed inputs, attribution, and mandatory erratum handling.
- MANIFEST.json: reproducible file hashes.

Reproduce with Python 3 (standard library only):

    python3 verify_interface.py

The default run takes about one minute in the task environment. It checks
all Fourier coefficients through N=64, all expanded real matrix coordinates
through N=16, and dense exact lane inputs through N=256, as well as 294,912
finite-field one-shear controls. Finite tests corroborate the proofs; they
are not substitutes for them.

No external repository, table, or service was modified.
