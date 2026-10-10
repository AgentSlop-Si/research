# Phase 34 independent audit

- New tests: `tests_phase34.py` (11 checks), all passed in the current container and again from a fresh archive extraction.
- Inherited Phase 33 tests: 13 passed when rerun in their original directory.
- Deterministic exact finite-field modulus: `998244353`; Fourier and cyclic Green identities checked without floating point.
- Near-order cycle swaps: rank difference 2; inverse-residual rank exactly 2 in each stage; N=64 two-stage rank 4, Vandermonde exclusion floor 12.
- Sparse input/output phase patches: N=64 stage ranks 4 and 4, combined inverse residual 8; Fourier floor 12.
- Three-stage two-Green product: N=64 rank 6; Fourier floor 7.
- Rank-distant far-order controls: N=32,64,256; two Weyl residuals nonzero in every output coordinate for the seeded test input. This is **only a fixed-candidate test**.
- Additional positive controls: exact modular Green inverse identity, exact Fourier covariance, nonzero Fourier Vandermonde minors, and exact rank conservation under inverse of the Green sum.
- The full package ZIP and all included SHA-256 hashes are checked after creation. Never count preserved historical tests as newly run.
