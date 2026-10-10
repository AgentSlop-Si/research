# FFT / Green research — Phase 31 continuation checkpoint

**Date:** 2026-10-10. Continue the user's original noncommuting Green-network research, rather than revisiting radix-2 FFT explanations, CrocSwap/Swapnil integer-multiplication networks, or repeated input caching.

**Main result:** Five independently ordered, complex-gauged cyclic Green resolvents with four free couplings cannot be made Fourier-equivalent using any two internal nonzero diagonal masks and permutations **for the precise seeded family at N=4 or N=8**. Phase31 introduced a rectangular **3×4** Fourier-phase test requiring only **seven** 2×2 minors. Their 35 cubic multiples yield a 35×35 matrix of full exact modular rank for **all 576 N4** and **all 564,480 N8** ordered mappings. Finite-field full rank lifts to the matching complex construction. N16 has **100,000 sampled mappings**, not a full theorem.

**Constructive control:** A genuine O(N)-per-vector five-Green executor matches dense arithmetic exactly; a planted valid target causes the phase obstruction rank to drop to 34. This candidate does **not** compute the DFT.

**Additional scope:** Six generators use the same 3×4 window (exhaustive N4 rank 56), while seven can use 3×5 (sampled ranks 84). The rectangular rank-one codimension is `(r-1)(c-1)`. The seven quadratic equations are minimal for a full **degree-three Macaulay** certificate with five homogeneous parameters.

**Files:**
- `fft_green_research_phase31_2026-10-10.zip` — self-contained new research files with immediate source dependencies and nested full Phase30 checkpoint.
- `fft_green_phase31_rectangular/THEOREM.md` — all mathematical statements and restrictions.
- `fft_green_phase31_rectangular/CHECKPOINT.md` — exact next starting point.
- `fft_green_phase31_rectangular/RUN.md` — compile/run commands and precise rank records.

**Next:** Phase32 should target *exceptional* parameter synthesis satisfying overlapping Fourier projective windows simultaneously and then both Weyl identities, not merely keep excluding generic seedings. Nothing yet proves a general-input sub-NlogN FFT or improved arbitrary-precision integer multiplication bit complexity.
