# Polynomial preparation of the accepted NF-03 family

The accepted polynomial family and its severe conditioning are unchanged. The new theorem replaces exhaustive root-grid preparation by the Mehlhorn–Sagraloff–Wang certified root algorithm, with a separately constructed and fully charged cyclotomic coefficient oracle. An explicit rational local check certifies all returned disks.

Main bound: O~((N^8+Np)^3) bit preparation, including coefficient generation, retries, all disks/labels, weights, residues and endpoint constants. The smaller O~(N^9+Np) figure is the root-engine model only. The unscaled moment Vandermonde remains exp(Omega(N^4))-conditioned; application remains O(N^2) rational operations.

Read POLYNOMIAL_PREPARATION.md for the full algorithm, proof and ledger. The original check program is controls/check_preparation.py; results are in evidence/CHECK_RESULTS.json. It does not implement the MSW/Pan root engine, and its numerical candidate generation is confined to a subsequently exact-certified N=4 diagnostic.

This is a scoped candidate continuation pending independent review. No external write, historical executable run, practical timing claim, h-pole optimum, t=1 theorem, fast-FFT claim or novelty claim is included.
