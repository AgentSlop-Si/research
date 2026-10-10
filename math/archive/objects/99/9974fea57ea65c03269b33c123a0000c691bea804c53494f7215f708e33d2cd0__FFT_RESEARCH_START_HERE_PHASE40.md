# Phase 40 FFT–Green research: recovery entrypoint

Open `fft_green_phase40_four_middle/CHECKPOINT.md` for the current state, `THEOREM.md` for complete mathematical arguments and their limitations, and `RUN.md` for commands.

**New exact restricted theorem:** for one fully specified eight-resolvent Green family at N=8, five overlapping phase quadrics and a 20x20 cubic Macaulay certificate exclude all three tunable complex middle coefficients, both arbitrary intermediate permutations and both arbitrary invertible diagonal masks. Every one of the 376,320 local row/column mappings passed an exact full-rank certificate in two split finite fields. N>=16 audits are sampled and are not all-permutation theorems.

**New constructive direction:** union-find gauge normalization exposes N+1 independent nonzero complex holonomy parameters in the union of two weighted Hamiltonian cycles, while preserving O(N) Green application. An exact nonzero four-by-four Jacobian minor proves the four-local-cross-ratio map is dominant over C for fixed audited graph orderings at N=8,16,32. This is **generic local controllability**, not a proven solution for the particular Fourier phase target or any complete FFT.

**Current research status:** No proven general-input o(N log N) DFT algorithm, no faster integer multiplication bit-complexity bound. Main Phase 41 target: explicitly construct chord weights matching the actual Fourier cross-ratios for all rows/columns, verify both Weyl equations and prove total online/preprocessing/precision costs. Keep the nested Phase 39 archive for full historical recovery.
