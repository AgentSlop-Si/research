# Research continuation — projected Jacobians and second-order FFT compatibility

**Date:** October 10, 2026  
**Target:** Exact, arbitrary-input Fourier computation in less than `N log N` fully charged arithmetic.  
**Architecture:** the unmodified `N=256` four-stage affine-permuted separated-generator scan network.

## Why this checkpoint was needed

The previous generation established 64 complementary half-block Fourier rank gates and their inverse-free Jacobi duals, but no contradictory coefficient assignment. The just-broken research turn reported a full-rank 16×16 output Jacobian. We independently reconstructed the stage coefficients and exact permutations to test which additional output entries can supply *genuinely new simultaneous polynomial constraints*.

## Verified results

1. **Previous project recovered:** both exact prime-field verifiers for the 64 Fourier-block constraints and Jacobi duals passed after extracting the saved ZIP.
2. **Full polynomial freedom on 28×28 leading outputs:** we obtained an explicit **784×784 nonzero Jacobian minor** in two fields using the same integer stage coefficients and parameter columns. This establishes over C that no nonzero polynomial identity can depend only on those 784 entries (Theorem A in `PROOF_CERTIFICATE.md`). It considerably extends the earlier 16×16 witness.
3. **Observed first-order boundary at larger blocks:** modular Jacobian rank on this specific parameter point was full at 16,20,24,28; became 831/841 at 29 and 906/1024 at 32, in the checked field. At 32, the value 906 repeated in both GF(12289) and GF(65537); a separate integer parameter sample in GF(12289) also gave 906. Do NOT turn these pointwise modular numbers into a universal complex-rank or algebraic-dimension bound.
4. **Not a matrix-rank defect:** the evaluated leading 32×32 *matrix* has exact full rank in GF(12289). The 32×32 center block's coefficient Jacobian had full rank 1024, while a different off-diagonal 32×32 block had rank 932 (mod GF(12289)). The local behavior depends on which rows and columns are chosen.
5. **Second-order coordinate directions are all present:** the exact Hessian identity `∂² M / (∂d4_i ∂d1_j) = K_ij E_ij` holds, and at the saved witness every `K_ij` in the leading 32×32 rectangle is nonzero modulo 12289. These second-order directions span all 1024 output coordinates even though the sampled modular first derivative has rank 906.
6. **All-length linear-relation theorem:** the independently variable outer diagonals and a dense invertible middle product prove there are no universal affine-linear output identities for this four-stage family at any length or any fixed shuffles.

## Exact determinant certificates

| Certificate | Prime | Dimensions | Determinant |
|---|---:|---:|---:|
| Leading 28×28 output Jacobian selected minor | 12,289 | 784×784 | 5,424 |
| Same integer selected minor | 65,537 | 784×784 | 42,512 |
| Combined Jacobians at two explicit parameter points | 12,289 | 1,024×1,024 | 4,142 |

The last certificate has 906 columns from point 1 and 118 from point 2. The first two establish the characteristic-zero polynomial-independence theorem. All witnesses are explicitly saved, not inferred from a random rank report.

## Honest limitations

- No coefficients realizing the Fourier transform have been found.
- We have **not** proved that a universal nonlinear compatibility identity first appears at 29×29, nor that the modular 906-dimensional tangent is the generic characteristic-zero dimension.
- Full second-order osculating space does not imply surjectivity of the full Fourier coefficient map, and does not eliminate higher-degree polynomial equations.
- The full `N=256` affine-layout experiment alone cannot establish a uniform sub-`N log N` complexity improvement, particularly because previous parity-routing bounds obstruct fixed-depth affine scan constructions for sufficiently large N.

## Next research experiment

Instead of testing a single 17×17 Fourier minor or an already-dominant 28×28 block, test **simultaneous, spatially separated Fourier blocks** and the 64 Jacobi-dual constraints on the *same outer-stage parameters*. An exact contradiction requires a polynomial/ideal certificate covering every exceptional branch (not modular optimizer failure). If the four-stage factorization is found, build a fresh-input exact executor and audit all arithmetic before any asymptotic claim.
