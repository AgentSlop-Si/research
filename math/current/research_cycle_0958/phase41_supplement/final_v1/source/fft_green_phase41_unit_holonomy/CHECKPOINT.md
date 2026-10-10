# Chain recovery: start Phase 42 here

## Proven all-size statement

**For every N>8**, `F_N != L P_row [a (I-W1)^(-1) + b (I-W2)^(-1)] P_col R` whenever W1,W2 are admissible weighted Hamiltonian cycles with **unit-modulus weights on every edge**. Outer invertible complex diagonals/permutations and arbitrary complex scalars a,b are allowed. Proof: each cycle has only two row-ratio signatures; a sum of two has four signatures; a constant-modulus row ratio takes at most two values per signature; an adjacent Fourier row pair takes N values. This is a project-specific exact mathematical result; its novelty has NOT been externally established.

The theorem does **not** cover three or more cycle sums, non-unit gains, independently masked products, or general FFT complexity.

## Phase-only degrees of freedom

For two cycles, fixed scalar coefficients, rows 0/1 and columns 0..k, real rank <= min(2k,k+2). Exact rational-Gaussian unit-gain two-prime minors attain 4,5,6 for k=2,3,4 at N=8/16/32; k=4 attains6 at N=64.

For **three** independent cycles, N=8/16/32/64, exact two-prime certificates demonstrate full real rank **2(N-1)** for the complete projective signatures of two Fourier rows. This is local controllability at SOME targets, not all targets. Independent numerical searches also hit actual Fourier two-row ratios (N=8/16/32, around 1e-11 max error), but fail the third row. Offline search is expensive.

For **two cycles with arbitrary complex amplitudes**, complete N-1 complex Jacobian rank is proven for the explicit graph orders at N=8/16/32/64/128. Numerical actual two-row fits at N=8/16/32, high-precision residual <1e-80 at N=8/16; no rigorous root-existence certificate or full matrix identity. Conditioning grows seriously for N=32.

## Phase 42 priorities

1. Explore **three** independently ordered unit-phase Green cycles (or their noncommuting products) for exact **multi-row** Fourier coherence, not another two-row fit. Parameter degrees: 2N+1 independent circle holonomies. At finite N, check more than two rows and always validate both Weyl equations.
2. Explore whether the explicit local amplitude-asymmetric Möbius map `(2 + t/2)/(1+t)` can arise in globally consistent weighted Green cycles with bounded edge magnitudes, and whether exact target parameters can be generated cheaply for every N.
3. Seek a **uniform**, constructive, all-N correctness theorem and a complete complexity accounting (parameter computation, precision, arithmetic and memory). A local Jacobian rank or a 1e-90 numerical residual is *not* such a theorem.
4. Do not repeat scalar-coupling random searches, generic cross-cut rank tests, or phase-only two-cycle sums.

## Reproduce

Run `bash RUN.sh` at the top of the extracted package. A nested Phase 40 ZIP preserves the complete prior history. `THEOREM.md` has exact statements and proof.
