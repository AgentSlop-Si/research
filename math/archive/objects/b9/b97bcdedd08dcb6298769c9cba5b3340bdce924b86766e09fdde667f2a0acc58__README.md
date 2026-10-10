# HERO #0 — Phase 17

## What was actually proved

For `N=s^2` and **even** `s>=4`, let `Pi` be the Margulis half-grid translation and let a Green-sum/product reference `T0` commute with `Pi`. No matrix `D_out T0 D_in^-1`, even with two **independent complex invertible diagonal gauges**, equals the Fourier transform. For unit-modulus gauges, its operator-norm and relative-Frobenius error from the unitary DFT is at least

`g_s = 0.5 sqrt(1-2/(s sin(pi/s)))`, asymptotically `0.301405...`.

Even permitting a **rank-k correction** to the two-sided gauged reference, the error remains at least

`0.5 sqrt(max(0,1-2/(s sin(pi/s))-8k/N))`.

Hence an exact Fourier factorization in this grammar requires at least `ceil((1-2/(s sin(pi/s)))*N/8)` rank-one corrections/individual edge edits, under the carefully stated phase-gauge hypotheses. This is a *uniform* linear defect budget without the previous genericity caveat, but a smaller constant than the generic `N/2` restriction.

The proof also computes an exact rank-four singular-value spectrum for the half-grid Fourier phase-ratio matrix, gives the Frobenius-optimal intertwiner for fixed gauges, and checks the `N=4` exception exactly.

## How to reproduce

```bash
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_phase17
OPENBLAS_NUM_THREADS=1 python audit.py
python phase17_gauge.py
```

The previous Phase 16 source is included unchanged as `prior_phase16_bundle.zip`. The new tests and saved inherited test logs cover 72 passing test methods (15+19+16+22). Exact finite-field verification uses GF(65537).

## Important limitations

- This is **not** an O(N) FFT on arbitrary inputs or an improvement to a general Fourier upper bound.
- The exact no-go applies to two-sided diagonal gauging of a half-grid-symmetric operator; **arbitrary internal non-flat curvature** escapes it.
- The positive error and uniform rank-budget constants require **phase-only external diagonal gauges**. Arbitrary nonunitary gauges are covered for *exact impossibility* but not by the numerical constants.
- FFT monomial-normalizer identities have extensive prior art. Neither the spectral conjunction nor any project originality has been independently established for publication.
- `T_star` is the best approximation for a fixed intertwiner symmetry but is not shown to admit a fast executable circuit.

See `THEOREMS.md` for all derivations and precise quantifiers, `RESULTS.json` for the reproducible checks, and `CHAIN_HANDOFF.md` for the next unresolved target.
