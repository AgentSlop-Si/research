# FFT Green research — Phase 24 start here

**Status at 2026-10-09:** Exact binary stable-sorting shift-defect theorem; exact rank distribution; high-probability all-stride lower bound; working modular Woodbury Green correction for locally modified input orders. **No arbitrary-input sub-NlogN FFT yet.**

The current source tree and the prior full history are bundled in `fft_green_research_phase24_2026-10-09.zip`. The first document to open is `fft_green_phase24_ordering_defect/CHECKPOINT.md`; the mathematical proofs are in `THEOREM.md`.

To reproduce from a fresh extraction:

```bash
cd fft_green_phase24_ordering_defect
python -m unittest discover -s tests -v
python audit.py
python verify_full_lineage.py ../fft_green_research_phase24_2026-10-09.zip
# optional, slower: append --full to re-execute every inherited suite
```

**Key finding:** Sorting a binary vector changes the shift that defines its Fourier transform. For the stable sorting permutation, the exact rank of the shift correction is `2 floor(T/2)`, with `T` the number of internal bit transitions. For random binary inputs the expected rank is `N/2-1` and the rank is simultaneously `Omega(N)` against *every* cyclic stride with high probability. Thus simple sorting plus a low-rank Green repair does not extend the Phase23 linear-time special-input executor to random data.

**Positive control:** Fixed-size local coordinate reorderings admit an exact `O(N)` Woodbury-corrected Green query for a permuted geometric input. The general query cost is `O(Ns^2+s^3)` for `s` changed successor edges, and all costs are accounted for in the restricted field-operation model.

**Next target:** truly independent and noncommuting sparse Green reference graphs, not merely perturbations of cyclic shifts. Preserve exact covariance and seed, and count all solve/update work.
