# Hero #0 — Phase 18 | Curvature energy & exact Fourier audit

**Date:** October 10, 2026.  
**Research status:** Three mathematically proved **necessary-condition** bounds for bounded-complexity Green networks, with independent complex and finite-field checks. **No new all-input exact O(N) or O(N log log N) Fourier transform.**

## Important: avoid repeating earlier discoveries

The eighth-root identity `V^4=-I` and the exact singular-value spectrum of the Fourier half-grid commutator were **already derived in Phase 15**. We reran them using an independent two-dimensional polyphase matrix over GF(65537). We do not claim they are new here.

## New research outputs relative to the saved chain

- **Continuous paired-weight obstruction:** a necessary `Omega(N)` total squared half-grid asymmetry energy for exact Fourier computation by a constant-depth, bounded-norm Green network. Unlike sparse edit-count bounds, all weights may change by arbitrarily small amounts.
- **Gauge-curvature energy obstruction:** a uniform lower bound on the weighted Euclidean distance to any admissible common-phase-gauge, symmetry-preserving Green reference. This detects networks that *look* asymmetric but are close to a flat connection.
- **Linear-time weight certificate:** inspect `E` edge occurrences and compute proved Fourier error floors in `O(E)` arithmetic operations, using the explicit `max|w|<1` resolvent norm bound. This is a rejection test, **not** a Fourier transform.
- **Holonomy-to-rank workflow:** exact spanning-forest gauge extraction and fundamental-cycle holonomies, followed by a modular rank certificate when desired; the underlying generic rank fact was established in Phase 16.
- **Refined rank-k Frobenius lower bound:** a piecewise explicit error floor from the already-known Phase 15 singular spectrum.

## Reproduction

```bash
cd fft_hero0_phase18_curvature
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_phase18 test_phase17
OPENBLAS_NUM_THREADS=1 python audit_phase18.py
```

There are **17 Phase 18 tests**, **15 inherited Phase 17 tests**, and **16 additionally rerun Phase 15 tests** (48 passing test methods in total). The exact finite-field polynomial/conjugation certificate has zero residuals at lengths 4, 16, 64 and 256. `RESULTS.json` records six independently calculated energy-bound examples and the spectrum checks.

## File map

| File | Contents |
|---|---|
| `THEOREMS.md` | Proofs, exact scope, all constants, and prior-art caution |
| `phase18_curvature.py` | Exact matrix gates, O(E) weight certificate, modular forest gauge and Weyl checker |
| `test_phase18.py` | 17 independently running Phase 18 tests |
| `test_phase17.py` and `phase17_gauge.py` | Recovered Phase 17 regression source |
| `prior_phase15_verification/` | Recovered unchanged Phase 15 test and verifier source |
| `RESULTS.json` | Central quantitative checks and illustrative costs |
| `CHAIN_HANDOFF.md` | Phase 19 target and do-not-repeat register |
| `prior_phase17_bundle.zip` | Complete unchanged prior Phase 17 package |

## Mathematical scope

`N=s²` with even `s>=4`; complex Green weighted-permutation resolvents on graph generators commuting with the low-digit half-grid involution; arbitrary per-edge weights, fixed scalar stage coefficients. Energy-based quantitative bounds assume uniform spectral control on the Green resolvents; the O(E) implementation uses max modulus <1 as an easy sufficient condition. These restricted lower bounds do not exclude other operators, arbitrarily ill-conditioned circuits, high-depth networks, or a universal faster FFT.
