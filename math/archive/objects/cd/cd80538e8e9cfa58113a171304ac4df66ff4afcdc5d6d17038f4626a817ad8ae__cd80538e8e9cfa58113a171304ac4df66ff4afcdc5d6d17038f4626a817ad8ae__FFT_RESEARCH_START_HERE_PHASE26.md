# FFT Green Research — Phase 26 start here

**October 10, 2026.** Resume the research from `fft_green_phase26_simultaneous_cuts/CHECKPOINT.md` and `THEOREM.md` inside `fft_green_research_phase26_2026-10-10.zip`.

**Verified development:** simultaneous modular-character separators impose `rank(M[I,J]) <= 2*d*Q*N/r + B` on products of weighted cyclic Green sums whose coordinate cycles use boundedly many affine increments, including **arbitrary affine internal permutations, diagonal gauges and near-resonant edge weights**. Consequently, any exact DFT in this architecture needs `Q=Omega(log N/log log N)` Green terms. The concrete eight-term `N=256` circuit family has a certified rank-38 block, while the corresponding Fourier block has rank 128. Outer monomial gauges cannot fix the deficit.

**Constructive escape gate:** non-affine independently ordered Green cycles evade the fixed-stride hypothesis, but currently fail exact Weyl/real Fourier covariance. Phase 27 must address that **phase equation**, not merely matrix density or commutator rank.

**Status:** No new worst-case sub-`N log N` Fourier algorithm; no new integer-multiplication bound. All claims are restricted-model deductions and executable checks, with classical prior art explicitly identified.

```
cd fft_green_phase26_simultaneous_cuts
python -m unittest discover -s tests -v
python audit.py
sha256sum -c SHA256SUMS.txt
```
