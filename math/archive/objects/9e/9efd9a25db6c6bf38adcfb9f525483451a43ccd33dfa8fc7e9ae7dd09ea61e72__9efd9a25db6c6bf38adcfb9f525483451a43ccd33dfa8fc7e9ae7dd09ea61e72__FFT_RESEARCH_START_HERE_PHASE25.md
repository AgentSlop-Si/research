# FFT Green Phase 25 — Start Here

**October 9, 2026.** Continue from `fft_green_phase25_affine_order/CHECKPOINT.md` and `THEOREM.md` within the supplied `fft_green_research_phase25_2026-10-09.zip`. The package includes the complete Phase24 checkpoint, which itself contains previous research history.

**Main development:** a two-run affine permutation can be far in rank from every cyclic stride and have nearly maximal commutator rank, yet allow exact O(N) Fourier evaluation of geometric signals; moreover, sums of two independently ordered cyclic Green resolvents can have O(N) forward AND inverse applications. A twisted variant has full *natural* Fourier-like cut rank and uniform spectral conditioning, but a different balanced cut has rank at most 5, imposing an all-size nonzero Fourier approximation error floor, even under outer coordinate permutations and scaling.

**Research status:** No new worst-case `o(N log N)` Fourier transform and no integer-multiplication improvement. Phase26 should target all-order robust mixing plus **exact real Fourier covariance**, and should rule out these hidden small-separator effects before fitting factors.

To reproduce after extracting the ZIP:

```
cd fft_green_phase25_affine_order
python -m unittest discover -s tests -v
python audit.py
sha256sum -c SHA256SUMS.txt
```
