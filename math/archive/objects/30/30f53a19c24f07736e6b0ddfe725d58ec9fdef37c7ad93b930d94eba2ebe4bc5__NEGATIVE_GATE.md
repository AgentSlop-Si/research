# Phase 23 negative gate — indistinguishable Fourier prefixes

**Claim rejected:** A short Fourier prefix, even with a Hankel resultant vanishing, proves that an arbitrary vector has the inferred sparse-rational representation.

Let `m=10`, `N=128` and primitive `N`th root `omega` in GF(2013265921). Given an exact two-factor/two-defect residual `r`, add the pure Fourier mode `eta_j=omega^(-19*j)`. Orthogonality gives:

- `F(r+eta)[k] == F(r)[k]` for all `0 <= k < 10`.
- `F(r+eta)[19] == F(r)[19] + N`.
- The compiled resultant, trace gcd and candidate parameters are identical, because they depend on the first ten Fourier samples.
- The **entire-vector cyclic certificate rejects both false candidates** (in this tested example) and the implementation falls back to the full exact FFT.

This is a robust architectural warning: sample-compression methods cannot transform all arbitrary dense inputs exactly unless a full-certificate or sufficient extra information is obtained. It is not a lower bound on all Fourier circuits; it only rules out claims that ten probes uniquely determine N arbitrary frequencies.

**Further generic barrier:** even if the first ten probes are linear functionals of all input entries and cost O(N), their joint rank is at most 10. For `N>10`, their common kernel is nonzero. Thus no fixed-prefix-only decoder can recover every exact `F_N x` without additional input access.
