# Source and attribution ledger

Accessed 17 October 2026 (UTC).

## Supplied research

- Supplied source archive: fft_R30_graph_fusion_2026-10-18.zip, retained privately.
- Read README.md, PROOF.md, REPORT.md, and SOURCES.md.
- The supplied code was not executed or imported. The original archive is
  retained privately unchanged and its SHA-256 is recorded in verification.json.
- Relevant original result: the constructed rho = ±3 tensor/Green/inverse
  window is two-sparse, and no eligible family inside a cyclic FFT was shown.

## Classical primary/authoritative references

1. James W. Cooley and John W. Tukey (1965), "An Algorithm for the Machine
   Calculation of Complex Fourier Series", Mathematics of Computation 19,
   297–301, DOI 10.1090/S0025-5718-1965-0178586-1.
   Author paper hosted by Stanford:
   https://web.stanford.edu/class/cme324/classics/cooley-tukey.pdf
   Used for attribution of the classical sparse FFT factorization. The
   exact factorization and counting proof are written out in PROOF.md.

2. Ryan O'Donnell, Analysis of Boolean Functions, Chapter 1.
   Author-hosted book:
   https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf
   Used for attribution of the classical Fourier-Walsh character basis on
   the binary cube. No novelty claim is made for that conjugacy framework.

3. IBM Quantum / Qiskit SXGate documentation, version 2.2.
   https://quantum.cloud.ibm.com/docs/en/api/qiskit/2.2/qiskit.circuit.library.SXGate
   Explicitly gives the same C matrix as the standard square-root-of-X
   gate. The resolvent and butterfly identities are derived independently
   and checked with exact Gaussian rational arithmetic.

No supplied program was executed, no broad re-audit was performed, and no
external service was written to during this completion.
