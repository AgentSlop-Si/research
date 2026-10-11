# Research log: from 550 necessary minors to exact coefficient feasibility

**Original objective.** Discover a scalable exact FFT-like construction with fewer than `N log N` arithmetic operations for arbitrary fresh inputs. **Not achieved.**

## Starting point

The previous research generations supplied a fixed `N=256` four-stage quasiseparable architecture with three affine GF(2) shuffles. The `fft_solver_saturation_checkpoint_2026-10-11.zip` checkpoint identified 550 algebraically independent necessary determinant equations, a normalized singular common zero, arbitrarily small false-positive determinant residuals at invertible ill-conditioned points, and a division-free linear-work stage determinant recurrence. It did **not** solve the joint zero fiber.

## Findings this round

**Pivot-safe exact inverse.** The scan matrix becomes a `3N×3N` block-tridiagonal augmented system with lower/upper bandwidth bounded by 4/3 and determinant exactly equal to that of the original matrix. Exact finite-field Gaussian elimination and local pivoting solve it in linear work even on invertible zero-diagonal charts. This enables inverse-stage operations without building dense inverse matrices.

**Exact middle-operator black box.** Write `G=P1 S1 U^-1 S4 P3`. If the outer stages are invertible, `H=G^-1=P3^-1 S4^-1 U S1^-1 P1^-1`. The program applies `H` to a vector using the two banded solves and an ordinary `N=256` radix-2 NTT, using the saved affine shuffles exactly. Round-trip with `G` passed over `GF(12289)` and `GF(65537)`.

**Complete sparse quadratic model.** Introduce prefix and suffix auxiliary states on every input basis vector at every stage. Encode the 4×256×256 stage computations as quadratic equations. The resulting system has 723,968 unknowns and 784,384 equations of total degree ≤2, each supported on at most four monomial terms. **A complex solution is equivalent to complete Fourier factorization.** Invertibility follows automatically from equality to the invertible Fourier target; separate determinant saturation is unnecessary for this formulation. This corrects the incompleteness of treating the 550 selected minors as the full problem, but increases solver size substantially.

**Smallest most restrictive rank gate.** For the mask-64 `128×128` block whose permitted rank is 16, replace large minors by a rank-112 kernel witness `Z`. On each row-pivot chart, require `BZ=0` with `Z[K,:]=I`. There are 1,792 free entries of Z and 14,336 equations on that fixed chart, degree ≤5 in raw separated-generator parameters. Introducing `X=S4P3[:,J]Z` gives an equivalent degree-≤3 lifted chart with 28,672 extra variables and 43,008 equations (28,672 plus 14,336), with bilinear outer-matrix products. Union all charts to cover degenerate cases. Nontrivial rank-16 synthetic controls passed both prime fields; saved Fourier-witness coefficients have rank 128 and fail, as expected.

## Exact verification summary

| Verification | Result |
|---|---:|
| Dense determinant vs augmented exact determinant | 252/252 |
| Invertible stage solution roundtrips | 246/246 |
| Fully zero-diagonal invertible stage solves | 8/8 (N up to 1024) |
| Exact middle inverse/forward compositions | 30/30 |
| Positive all-basis lifted-system checks | 512/512 basis vectors (256 per field) |
| Nonmatching entries of saved witness vs Fourier, mod 12289 | 65,532 / 65,536 |
| Nonmatching entries of saved witness vs Fourier, mod 65537 | 65,535 / 65,536 |
| Kernel gate rank on synthetic middle inverse | 16 in both fields |
| Fourier-target gate rank at saved outer coefficients | 128 in both fields |
| Kernel-chart polynomial residual | 0 in both fields |

The nonmatching-entry count is specific to one archived parameter point, **not** an impossibility result. A finite-field witness is not a complex factorization proof.

## Next actionable research gate

Start with the strongest mask64 rank condition and a **single normalized kernel chart**, jointly optimizing both outer generators with a saturation-aware solver. After finding a candidate, certify its rank exactly, switch pivot charts if needed, and add further masks168/156. A candidate satisfying all 64 rank gates still needs a compatible middle-stage decomposition and the full quadratic/basis verification. Keep exceptional zero-diagonal branches.

An independent architecture-design track must also address the earlier asymptotic GF(2)-affine depth lower bound: even if this single `N=256` problem has an exact solution, that does **not** imply an all-length sub-`N log N` transform.

## External theoretical baseline

Linear-work structured solves for quasiseparable matrices, determinant transfers, and low-rank incidence varieties are established tools. These checkpoint results are engineering and algebraic reformulations for a specific fixed network; external novelty and publication suitability remain unverified.
