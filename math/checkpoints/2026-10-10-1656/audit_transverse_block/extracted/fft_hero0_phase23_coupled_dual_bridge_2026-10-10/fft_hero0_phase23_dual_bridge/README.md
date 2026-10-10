# Hero #0 Phase 23 — coupled dual-bridge research

**Result:** Exact two-layer rook-factor necessary conditions that remain valid when **both** Green paths are simultaneously complex and adjustable.

- **Fully complex rank-product gate:** For N=s², each crossed path's two transverse factor ranks must multiply to at least s−2 for a full exact Fourier transform.
- **Approximation gate:** If one transverse rank product is uniformly <=rho<=s−3, every candidate has full-matrix relative Frobenius error >=sqrt(1−(3+rho)/s+1/s²). At constant rho this tends to 1.
- **Homogeneous Green no-go:** Two fiber-replicated complex Green kernels in the crossed pair have rank product 1; no two-layer exact FFT for s>=4, even if the other path is arbitrary complex.
- **Paired complex phase budget:** Each crossed pair of effective factor matrices requires approximately N/2 nonreal off-diagonal entries to represent F_N, with a quantitative approximation theorem.

These are restricted architectural necessary conditions. **No exact universal O(N) or O(N log log N) FFT has been found. External novelty is not established.**

Run with Python 3, NumPy (already available):

```
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_phase23
OPENBLAS_NUM_THREADS=1 python audit_phase23.py
```

The modular certificates use GF(65537). `THEOREMS.md` gives full self-contained proofs; `RESULTS.json` records exact modular minors and numerical checks. `CHAIN_HANDOFF.md` sets the Phase 24 problem. The earlier Phase22 research and all predecessor lineage are preserved in `prior_phase22_bundle.zip`.

**Verification in this package:** 17 new tests and 88 inherited tests (105 total) pass. An additional direct complex-valued four-resolvent Green example was checked at grid sides `s=4,8,16`. The optional `exploratory_als.py` searches unrestricted rook-supported two-factor fits but provides *no* formal impossibility proof and is **not** needed for reproducing any theorem.
