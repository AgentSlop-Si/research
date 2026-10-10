# Reproducibility and results — 9 October 2026

This pass intentionally pursues the **fresh full exact transform** goal; it does not update/copy old convolution engines or search CrocSwap's network constants.

## Exact field audit

The 998244353-modulus verifier tests a radix-2 FFT against its *entire linear matrix*, one basis vector per column, not only arbitrary example input arrays. It checks a rank-one displacement, exact submatrix ranks and a pole-series identity.

| N | FFT basis columns | Rank-one displacement | Full-rank rectangle tests | Radix-2 butterflies | Exact normalized support entropy (bits) | Rational representation direct extraction multiplies |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 4 | passed | 9 | 4 | 8 | 12 |
| 8 | 8 | passed | 18 | 12 | 24 | 56 |
| 16 | 16 | passed | 27 | 32 | 64 | 240 |
| 32 | 32 | passed | 36 | 80 | 160 | 992 |
| 64 | 64 | passed | 45 | 192 | 384 | 4,032 |
| 128 | 128 | passed | 54 | 448 | 896 | 16,256 |

For a sample N=128 rational encoding, storing ~2N field values is enough to describe the pole terms, but directly extracting all coefficients used N(N-1) modular residue updates, versus the verified FFT's 448 butterflies. The counts are not all the same type of operation; do not compare them as hardware timings.

## Independent complex check

An unrelated complex-number implementation builds the Fourier matrix, its normalized two-register unitary network, and a Gaussian determinant. It checks `|det F|=N^(N/2)`, its normalized entropy `N log2 N`, and actual matrix agreement for N=2,4,8,16,32, to floating-point tolerance. At N=32 the numerical DFT matrix error was below 6e-15. The analytic proofs do not depend on float agreement.

## Charging a fused FFT block honestly

At N=4096, L=12 radix-2 levels:

| Levels per macro | Block size b | Macro calls if each is counted as 1 | Minimum det<=2 primitive two-register gates inside **each** macro | Total primitive gates |
|---:|---:|---:|---:|---:|
| 1 | 2 | 24,576 | 1 | 24,576 |
| 2 | 4 | 6,144 | 4 | 24,576 |
| 3 | 8 | 2,048 | 12 | 24,576 |
| 4 | 16 | 768 | 32 | 24,576 |
| 6 | 64 | 128 | 192 | 24,576 |
| 12 | 4096 | 1 | 24,576 | 24,576 |

This is the exact stage-fusion cost for the stated **primitive-gate model**; it says nothing about a fundamentally new powerful operation with a justified different cost model.

## Final interpretation

- **Positive:** O(N)-size exact displacement and rational representations exist for the full Fourier operator and its outputs.
- **Negative:** Neither representation alone provides O(N) explicit evaluation.
- **Negative:** Contiguous Fourier subblocks are full-rank, ruling out standard exact bounded-rank block approximations there.
- **Negative:** For unnormalized F in a det<=2 in-place two-register circuit, and for normalized F in a unitary in-place two-register circuit, the N/2 log2 N lower bound is tight; this is established old theory in the stated restricted models.
- **Open:** General unrestricted-coefficient exact arithmetic, other data structures/operations, and numerical stable/bit models. No universal exact O(N) claim.

All tests are invoked with `python -m unittest discover -s tests -v`. Exact tests and approximate float diagnostics are intentionally separate.
