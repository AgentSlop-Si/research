# Fourier–Green Gram Phase Lock & Sharp Realification (10 October 2026)

This package combines an exact **single-mask impossibility** theorem for *positive/projectively-positive* Green mixers with a **sharp all-length Fourier realification identity** and a stable spectral obstruction for candidate matrices that are exactly unitary.

## Result

For `N>=3`, a normalized Fourier matrix cannot be represented as `L A D B R` with arbitrary complex outer monomial gauges `L,R`, one unrestricted complex diagonal `D`, and invertible real `A,B` when either `A` or `B` is entrywise strictly positive. All non-affine Hamiltonian-cycle permutations are allowed in positive Green sums.

For `g=gcd(2,N)`, the exact minimum over *unitary* row/column rephasings and real `X` is:

`min ||diag(u) U_N diag(v) - X||_F^2 = (N - sqrt(g*N))/2`.

Consequently any **exactly unitary** candidate satisfying the Gram-lock hypothesis has operator distance at least `sqrt((1-sqrt(g/N))/2)` from `U_N`.

## Reproduce

```bash
OPENBLAS_NUM_THREADS=1 python verify.py
python verify_positive_gauge.py
```

`verify.py` performs numeric matrix identities, an exact-formula chirp witness, random rephasing checks, independently permuted positive Green checks, and the `N=2` exception. `verify_positive_gauge.py` checks positive dephasing on Green mixtures and deliberately frustrated complex Green cycles.

`THEOREM.md`: full rigorous proof, explicit assumptions, prior-work attribution, and surviving construction target. `SOURCE_AUDIT.md`: provenance and originality boundaries. `ARCHIVE_INVENTORY.json`: 30 accessible ZIPs actually integrity tested (4,033 member occurrences including large nested/duplicated archives).

**No exact linear-time FFT has been constructed and no global publication novelty is claimed.**

## Additional finite-abelian theorem

For every finite abelian group `G`, `N=|G|`, `g=|G[2]|`, the exact minimum squared Frobenius distance of its Fourier table from row/column-rephased real matrices is `(N-sqrt(gN))/2`. See Theorem 6 and `verify_abelian.py`; Walsh-Hadamard groups `(Z/2)^d` give the zero-error boundary.
