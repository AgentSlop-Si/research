# Phase 40 exact validation record

Date: 10 October 2026. Tools: Python 3, NumPy, C++17 `g++ -O3`.

- **New tests:** 16/16 passed after compiling the native checker. Includes exact online eight-Green execution against independently built dense matrices, deliberately planted projective equivalence controls, known rank-19 false-survivor mappings, alternate-cycle rank-20 rescue, holonomy normal form, gauge invariance, Green defining equations, Jacobian rank, exact determinant residues and both Weyl positive/negative controls.
- **Inherited Phase 39 tests:** 18/18 passed after clean extraction of Phase 39 archive and compilation of Phase 39's C++ native verifier. This is not a rerun of every prior Phase 12–38 test; those are preserved historically.
- **Full `N=8` audit:** 376,320 ordered 2-row/5-column assignments per prime (998244353 and 2013265921), all of rank 20/20; zero exceptions. Reproduced using the final native Phase 40 verifier (`phase40_native_full_N8_*.json`). This is the only **fully enumerated** Phase 40 transform length.
- **Sampled `N>=16` audits:** See `phase40_mapping_audit.json` for exact per-prime sample counts and `rescued` counts. The N=16 first-cycle rank-19 witnesses were resolved using the alternative five-cycle. The total mapping space for N>8 was not exhaustively checked.
- **Weighted Green/union-find:** Exact field arithmetic round trips and common diagonal conjugacies pass at N=8,16,64,256, in both fields; one cycle has 1 gauge chord, two labelled cycles N+1. Each weighted Green recurrence satisfies its defining sparse equation independently.
- **Local Jacobian:** Four logarithmic projective cross-ratios have rank-four Jacobian at N=8,16,32. The same labelled cycle orders and small integer weights were reduced in two prime fields. Explicit common 4x4 minors, pivot edge indices and nonzero determinant residues are in `phase40_jacobian_certificates.json`.
- **Fourier covariance:** Exact reference radix-two transform has zero defects for both Weyl equations. Tested six-resolvent weighted Green products have nonzero defects, at every output coordinate in the sampled tests N=8–128; this is finite-instance rejection only.
- **No sub-NlogN algorithm or exact full Fourier Green factorization established.**

All assertions and checks can be independently rerun from source; `RUN.md` contains the commands.

**Fresh extraction check:** Extracted the packaged Phase 40 ZIP into an independent directory, recompiled `phase40_exact_audit.cpp`, reran all 16 Phase 40 tests, verified all `SHA256SUMS.txt` entries, and recomputed both complete N=8 enumeration certificates (376,320 mappings each, zero deficiencies). The nested Phase 39 ZIP passed integrity validation. This check was repeated after the source and documentation reached their final contents.
