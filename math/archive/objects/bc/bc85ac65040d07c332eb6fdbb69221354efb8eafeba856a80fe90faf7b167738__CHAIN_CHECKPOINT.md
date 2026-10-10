# HERO #17 — PHASE 9 CHAIN RECOVERY

**Date:** 2026-10-10  
**Canonical artifact:** `fft_hero17_phase9_root_exchange_union_2026-10-10.zip`  
**Mission:** Exact full Fourier transform for arbitrary fresh inputs in uniform, sequential, fully charged O(N); **NOT SOLVED**.

## Previous branch

Phase 7: exact optimal non-sharing Fourier rectangle incidence. Phase 8: polynomial CRT bridge full rank for every Fourier-root partition; classical parity split uniquely minimizes literal monomial transfer support; 13 Phase 8 tests. Yet sparse entries were not proven equivalent to scalar gate complexity.

## New Phase 9 mathematics

1. If t roots are exchanged between the even and odd halves of an N=2m Fourier root set, the remainder transfers R_A,R_B are involutions.
2. `rank(R_A-I)=rank(R_B+I)=t`, and stacked correction rank exactly `min(m,2t)`.
3. **Basis-invariant reflection theorem:**
   `rank([R_A,R_B])=rank(R_A R_B+I)=rank(R_A+R_B)=2 min(t,m-t)`;
   `rank(R_A-R_B)=m`. Thus the transfers commute exactly at parity splits, t∈{0,m}. Assumes field with N distinct roots and char≠2.
4. Forward child remainder formulas use exactly 2t Lagrange corrections and charge all root evaluations.
5. Inverse exact CRT coefficient recovery uses two nonsingular t×t diagonally-scaled Cauchy systems, prepared with charged inversion. For constant t, full plan and each local forward/inverse transfer are O(N).
6. **Critical accounting:** This is only one split. Hybrid full DFT still uses two m-point FFTs and O(tN) additional work: Θ(N log N) for fixed t, and is slower than classical radix2 in the measured implementation. No universal O(N), no numerical stability result, no integer multiplication claim.

## Audits

- 15/15 Phase 9 regression groups; Phase 8 predecessor rerun 13/13.
- 60 independent complete child remainder pairs = 1,744 exact pointwise comparisons.
- 101 correction-rank cases + 34 independent involution/commutator-rank cases.
- N=16 balanced partition histogram = [1,64,784,3136,4900,3136,784,64,1].
- Complete N=65,536 fresh arbitrary DFT verified vs separate radix2; 38 bins separately checked by direct O(N)-per-bin computation.
- Fixed one-swap local plan+forward N=65,536 = 1,179,664 scalar ops + 8 counted field inversions; full hybrid 2,981,902 scalar ops vs classical 1,638,399.
- For the same nonperiodic N16 split, this hybrid 801 vs prior generic root-division 883, but classical 111; no relevant FFT speedup.

## Next genuine research problem

Seek a **basis-invariant multistage scalar arithmetic-circuit synthesis** where the actual full global circuit (including every conversion) shares work across *different* CRT child evaluations. Require uniform fresh arbitrary input, full outputs, exact field/complex model, charged plan and roots, certified scalar recurrence, adversarial random values, and a fair optimized FFT baseline.

Do **not** repeat low-rank individual bridges as universal proof, fixed-structure input recognition, huge truth tables, pure gauge changes, or the older CrocSwap/kappa optimization route under a new name.

## Reproduction

```bash
python -m unittest discover -v
python independent_audit.py
```

No external dependencies. Read `PROOF_CERTIFICATE.md` for complete algebraic proof. `AUDIT_RESULTS.json` for precise measurements. `README.md` for package contents.
