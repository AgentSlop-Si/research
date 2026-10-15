# Source and novelty audit — 11 October 2026

## Inspected research

- Latest library `FFT_Phase43_Theorems.md`, including the arc-rank theorem, independently gauged two-layer parameter counting, four-row interval interpolation at N=8,16, and failing fifth-row certificates.
- Phase 42 `THEOREM.md` on triple Green signatures, Jacobian submersions, and partial Fourier interpolation.
- Phase 37 Hero #1 support-tree exact structured-input FFT and Hero #17 Phase 27 independent-slope structured chirp research, to avoid mistaking restricted input families for arbitrary-input Fourier algorithms.
- The prior phase-defect, stable inverse-dimension, projective-state, rewiring, and twirled-chirp theory packages in the current container.
- Indexed **35** accessible FFT-related ZIP archives (1,606 top-level README/theorem-like `.md/.txt` member occurrences under a 140 KB size cap). This was a targeted search over relevant mathematical claims, **not** a bytewise or proof-level audit of all user files. The Phase43 archive is referenced through the current Library theorem file rather than represented as locally reverified source code.

## Do not repeat

- One-layer q-cycle exact bound `N<=q(q+1)^q`: **already Phase 43** (with common outer monomial gauges).
- q=1 two-projective-state spectral barrier: **already earlier Phase21/projective-state work**, with a considerably stronger constant than our generic q=1 corollary.
- Classical exact sub-N-log-N DFT (in its specified arithmetic model): OpenAI Math #130 is the benchmark, not this project's discovery.

## Extension under investigation

`THEOREM.md` proves a uniform positive operator-norm error for fixed q even with independent monomial dressing on each branch. This is **new relative to the specifically inspected project checkpoints** and follows from a self-contained elementary argument. It may be recoverable from known discrete Remez inequalities or subspace approximation results. No historical priority, journal acceptance, or original FFT upper bound has been established.

## Public literature context

- Yomdin, *Remez-type inequality for discrete sets*, Israel Journal of Mathematics 186 (2011/2012), DOI 10.1007/s11856-011-0131-4.
- Tikhonov and Yuditskii, *Sharp Remez inequality*, arXiv:1809.09726.
- OpenAI Math #130, https://github.com/openai/math/blob/main/lean/docs/130.md (all-length exact arithmetic statement in its documented model).
