# FFT Green Phase 23 — chain-safe research recovery

**Date:** 2026-10-09  
**Latest checkpoint:** `fft_green_phase23_real_resolvent/CHECKPOINT.md`  
**Status:** Reproducible exact algebra, working finite-field adaptive Green executor, quantified binary-collision obstruction. **No new arbitrary-input `o(N log N)` FFT.**

## What changed

1. Derived `C_N g(z)=(1-z^N)(I-z R_N)^-1 v` from Phase 22's real Fourier covariance. Exact O(N) field-work application for one geometric input; O(rN) for r nodes, O(N) preparation plus one batch inversion per node. Handles Nth-root singular inputs without division-by-zero.
2. Added a true O(N) raw-input detector for exponential rank 0/1/2. Added an independent sparse-cyclic-difference Green solver for inputs with at most two transitions or second-difference kinks. The combined adaptive executor uses an ordinary NTT fallback on arbitrary data.
3. Proved a sharp restriction from the **classical full distribution** of finite-field Hankel ranks: for fair random binary input, probability of complex exponential rank <= r < N/2 is at most `2^(2r-N+1)`. For two terms this is `2^(5-N)`.
4. Proved the exact binary cyclic-transition law and used it to show the implemented linear-time paths cover at most `(N(N-1)+34)/2^N` of fair random binary inputs, for N>=8. This is a limitation of *these two* structurally adaptive routes, not of arbitrary FFT algorithms.
5. Verified the exact sparsity profile of `C_N^-1=C_N^T` and its sparse-inverse product depth limitation.

## Files

- `fft_green_phase23_real_resolvent/THEOREM.md`: proofs, complexity counting, classical result attribution, limits.
- `fft_green_phase23_real_resolvent/phase23_resolvent.py`: full standard-library-only executable implementation.
- `fft_green_phase23_real_resolvent/tests/test_phase23.py`: 24 new regression tests.
- `fft_green_phase23_real_resolvent/audit.py` + `audit.json`: GF2 Hankel distribution exhaustive counts and binary cyclic-transition counts.
- `fft_green_phase23_real_resolvent/previous_full_phase22_checkpoint.zip`: **entire inherited research chain** through Phase 22.
- `fft_green_phase23_real_resolvent/verify_full_lineage.py`: nested archive integrity + test verification.

## Fastest reproduction

```bash
cd fft_green_phase23_real_resolvent
python -m unittest discover -s tests -v
python audit.py
```

**Next research direction:** build an *independently ordered, noncommuting* real Green network satisfying `MZ=R_N M` and `Me0=v` for all raw inputs. Do not reclassify a restricted-input transform as a general FFT speedup.
