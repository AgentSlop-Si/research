# Green FFT research — Phase 32 recovery

**User objective:** Pursue a mathematically valid general-input improvement to FFT/integer multiplication by computation-graph reuse, rather than copying OpenAI/CrocSwap/Swapnil constructions. **No sub-NlogN general FFT has been discovered in this research.**

Current checkpoint: `fft_green_phase32_constructive/CHECKPOINT.md`; mathematical proof: `fft_green_phase32_constructive/THEOREM.md`. Standalone exact executor and validation: `phase32_interpolation.py`, `tests_phase32.py`.

**New result:** For arbitrary independently ordered Hamiltonian cyclic Green inverses `G_s=(I−α_sW_s)^{-1}`, q generators with independently fitted nonzero *left* diagonal gauges can interpolate any q complete Fourier columns, generically and with O(qN) online field work. This is proved by distinct exponent monomials in generalized Vandermonde determinants and their Cramer numerators. With q=5, exact checks match 5 complete Fourier columns through N=4096 while failing the sixth. q=N gives exact Fourier factors at N=8,16, but quadratic online cost and much greater setup.

**New restriction:** The q+1-column augmented determinant is a nonzero polynomial for any q<N and any Hamiltonian cycle orders: fixed Green row spans cannot generically interpolate more than q nonzero target columns with only left-diagonal gauges.

**Phase 33 next target:** Test *two-sided*, independently ordered Green sums `sum L_s G_s R_s` with consistency across overlapping Fourier-phase windows, exact Weyl identities, and complete cost/precision accounting. Do not treat finite selected columns, partial covariance, matrix density, or rank mixing as a general FFT.

The archive includes `previous_full_phase31_checkpoint.zip` containing the complete earlier preserved research chain through Phase 31. Reproduction commands are in `RUN.md`.
