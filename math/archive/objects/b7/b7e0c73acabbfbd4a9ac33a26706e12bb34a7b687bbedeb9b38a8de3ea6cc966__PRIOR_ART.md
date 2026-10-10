# Research-source and prior-art audit — October 10, 2026

## Project material consulted

A targeted content audit was performed of the master `fft_research_master_20261009.zip` (3,532 members), the phase 22/26 Green branches, Hero #0/#1/#17 archives, and the last ten `FFT_*` theorem packages. The latest `FFT_HADAMARD_SEGRE_EIGEN_GATE_2026-10-10.zip` already proves the rank-one Hadamard quotient and the sufficient `[T1,T2]` determinant obstruction. **Those are inherited results**.

Earlier master `fft_inverse_quartic_gate_2026-10-09/README.md` describes an unrelated **complete quadratic lift** with 176 equations and 184 variables for rank-one separated-generator charts. The new construction linearizes the 2x2 minors of the first three columns of the later *full diagonal-gauge Hadamard quotient*. Its coordinate map and circuit class differ. Mere use of the word "quadratic lift" is not novel.

Earlier files also address Fourier Weyl covariance, global Green cuts, non-affine permutations, subgroup singular values, phase pencils, and one-/two-sided gauges. None of these should be independently resold as new.

This audit does **not** assert that every historical source was formally checked; thousands of archive members are duplicate nested prior checkpoints.

## External literature

1. **D. Shemesh (1984),** "Common eigenvectors of two matrices", *Linear Algebra and its Applications* **62**, 11–18, DOI `10.1016/0024-3795(84)90085-5`. Necessary/sufficient common-eigenvector criteria; zero first commutator determinant is not enough.
2. **J. Dastidar, T. Weicht, A. S. Wein (2025),** "Improving the Threshold for Finding Rank-1 Matrices in a Subspace", `arXiv:2504.17947`. Symmetric tensor rank-one subspace lifting; a substantial prior-art warning for publication claims.
3. **Johnston–Lovitz–Vijayaraghavan (FOCS 2023)**: earlier planted rank-one subspace intersection algorithms, as cited in the 2025 work.
4. **OpenAI Math #130 (2026),** `https://github.com/openai/math/blob/main/lean/docs/130.md`: reported uniform exact arithmetic FFT bound `O(N(log N)^(1-1e-13))` in a permissive model. Does not supply or invalidate the target exact O(N) Green implementation.
5. **J. Morgenstern (1973),** "Note on a Lower Bound on the Linear Complexity of the Fast Fourier Transform", JACM 20(2), DOI `10.1145/321752.321761`: bounded-coefficient lower bound for unnormalized DFT circuits. Not an all-model lower bound.

## Novelty assessment

- **Soundness of project-specific theorems:** complete conditional proofs, with exact modular certificates and independent replication.
- **Improvement over immediately previous project:** yes; singular-commutator but full quadratic-certificate examples are certified in characteristic zero.
- **Unpublished mathematical novelty:** NOT VERIFIED. The algebraic lifting and Hensel tools are classical; the specific application requires a broader bibliographic investigation by a field specialist.
- **An exact sub-NlogN FFT breakthrough:** no; the results are fixed-stage rejection/approximation certificates.
