# FFT Research v33

Exact 99-edge three-layer support, characteristic-zero gauge-dimension certificate, full finite-field all-minor verification and bounded/unbounded coefficient model audit.

## Cold replay

`python run_all.py`

Needs Python 3, `networkx`, `sympy`, `numpy`, `scipy` for the optional heuristic script, and `g++` for the exact 705431-minor certificate. The cold runner does not invoke the numerical heuristic; the recorded `heuristic_results.json` is explicitly noncertifying.

Proofs: `RESEARCH.md`. Fixed graph: `topology_11.json`. Fixed weights and field transfer: `weights_11.json` and `transfer_11.txt`. Exact dimension witness: `jacobian_certificate.json`. Exact no-linear-relation witness: `affine_invariant_certificate.json`. Independent tests: `independent_verifier.py` and `all_minors_certificate.cpp`.

The package preserves v32 in `PRIOR_v32_COMPLETE.zip` with its original SHA-256. **No exact sub-`N log N` Fourier algorithm is claimed.**
