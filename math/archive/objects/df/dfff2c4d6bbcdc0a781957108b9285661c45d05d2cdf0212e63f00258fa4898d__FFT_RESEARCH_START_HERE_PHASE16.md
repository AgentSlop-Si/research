# FFT research — current chain start: Phase 16

**Complete archive:** `fft_green_research_phase16_2026-10-09.zip`. Contains `fft_green_phase16_entropy_fusion/THEOREM.md`, `CHECKPOINT.md`, tests and all code; also `previous_full_phase15_checkpoint.zip` (which preserves all Phase15 and earlier work).

Our main goal remains an **exact, all-input, fully charged o(N log N) Fourier computation** using independent graph/Green/Haar/reuse ideas. **We have not achieved it.**

**Phase16 new result:** Phase15's exact Galois folding FFT reaches Ailon's two-coordinate-unitary-gate entropy lower bound **at every gate**: all three factors separately saturate it. It is already optimal within that circuit model. Moreover, each path Green Cayley has <=2N-3 unitary Givens gates; Haar uses N/2-1 gates; therefore the full arbitrary-strength Phase13 Haar–Green stage has <=11N/2-8 gates. Any exact Fourier product of t such stages/inverses plus phases/permutations requires `t >= N log2N/(11N-16)`. Explicit numerical Givens reconstructions and entropy audits passed.

**Next path:** avoid pairwise unitary-only rearrangements and pure path Green products. Investigate nonunitary shared-computation graphs based on noncommuting sums of resolvents; require exact Fourier covariance, Galois phases and all-cost accounting. Read `THEOREM.md` before research: it identifies what is already disproved and exactly which computation models remain outside the known entropy theorem.
