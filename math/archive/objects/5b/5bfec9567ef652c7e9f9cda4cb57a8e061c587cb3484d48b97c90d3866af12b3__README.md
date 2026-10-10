# FFT Hero #1 — Phase 28 verified checkpoint

**Result:** `N=60·2^t` exact all-input DFT over suitable root-rich fields, nested 15- and 60-point Winograd diagonal kernels fused into the existing Phase 27 CRT/dyadic graph.

**Warm arithmetic theorem:** `C28(N)=90H log2(H)+498H+15`, `H=N/60`, exactly `46H` fewer scalar operations than the Phase 27 comparator. **Cold saving:** `46H−29` charged field operations for the two concrete one-shot plans. In particular at `N=61440`, Phase 27 uses `1,478,671` warm operations and Phase 28 uses `1,431,567`.

**Verification:** 10 new tests, 7 original Phase 27 tests, 2,455,200 exact Fourier matrix entries each compared through 3 independent implementations (7,365,600 comparisons); independent exact cyclotomic proof of factor codelets and 60-point diagonal identity counts; warm and cold benchmark through `N=61440`.

**Important limits:** Established Winograd/Good–Thomas prior art, not a new Fourier complexity upper bound or optimal FFT. Generic inputs are handled exactly, but work remains `Θ(N log N)`. Prime-field arithmetic is not a floating-point benchmark or bit-complexity theorem. Genuine noncoprime `(4,H)` coupling remains in the graph and is paid.

Read `THEOREM.md`, `COST_LEDGER.md`, `PRIOR_ART.md`, `NEXT_GATE.md`, and `RUN.md`. `PRIOR_PHASE27_COMPLETE.zip` is a byte-for-byte copy of the supplied previous checkpoint.
