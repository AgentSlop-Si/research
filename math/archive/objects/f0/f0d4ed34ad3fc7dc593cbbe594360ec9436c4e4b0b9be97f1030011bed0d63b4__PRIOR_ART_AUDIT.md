# Prior-art boundary — v23

Classical background used here:

1. The finite Weil representation of `SL(2,F_p)` and the discrete Fourier transform as the operator associated with the Weyl element.
2. Bruhat decomposition of `SL(2,F_p)` into a Borel cell and a big cell.
3. Chirp multiplications, coordinate dilations/permutations, and Fourier kernels as standard generators of the finite Weil representation.
4. Three-shear decompositions of linear canonical/metaplectic transformations.

Useful references include:

- S. Gurevich, R. Hadani, *The finite harmonic oscillator and its applications to sequences, communication and radar*, arXiv:0808.1495.
- W. Wang, *On the Construction of Finite Oscillator Dictionary*, arXiv:1010.2831.
- S. Gurevich, R. Hadani, R. Howe, *Quadratic reciprocity and the sign of the Gauss sum via the finite Weil representation*, arXiv:0808.2447.

Project-specific contribution and framing:

- a complete computational dichotomy for this FFT research: lower-Borel Weil stages are monomial `O(N)` operators, while every big-cell stage is explicitly diagonally/permutationally equivalent to one full DFT;
- the deduction that **every** factor-by-factor metaplectic decomposition of Fourier must expose at least one Fourier-hard stage;
- the exact unique `L(1) U(-1) L(1)` three-shear decomposition in the project conventions and its operation audit;
- exhaustive projective group-law certificates over all `14,400` pairs in `SL(2,F_5)` plus larger-field regression.

The group-theoretic ingredients are classical. This package makes no mathematical-priority claim. Its purpose is to close a proposed algorithmic route without confusing an exact metaplectic factorization with a faster FFT.
