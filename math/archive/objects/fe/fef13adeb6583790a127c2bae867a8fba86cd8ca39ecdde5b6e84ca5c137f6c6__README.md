# HERO #0 — Phase 11

**Research status:** Exact **restricted network lower bound** + explicit **infinite family of cheap high-rank noncommuting Green-sum layers**. The general exact O(N) Fourier problem remains unsolved. No mathematical priority/novelty claim.

Run from this directory:

```sh
python verify_all.py
```

Requires Python 3, `numpy`, and `mpmath`. Finite-field tests use `GF(65537)`, `3` as a primitive generator. Proofs do not rely on those tests. The report is `THEOREMS.md`, next-session resume file is `CHAIN_HANDOFF.md`.

The all-square constructive escape uses polynomial-size rational parameters and has a uniformly well-conditioned matrix, but **its exact coefficient powers need not fit a fixed word**. It is not the Fourier transform, and the O(N) assertion is only for applying **that graph layer** in unit-cost exact scalar arithmetic.

Contents:

- `phase11_gate.py`: modular Fourier/rigidity certificate, matrix inversion/rank, factor audit.
- `test_phase11.py`, `audit_phase11.py`: proof gate exact checks.
- `green_sum_linear.py`: linear-work weighted graph cycle solver and escape examples.
- `test_phase11_escape.py`: independent Green-sum checks.
- `explicit_poly_escape.py`: all-square polynomial-parameter construction and 80-digit numerical checks.
- `explicit_square_escape.py`: earlier exponential-parameter construction (superseded).
- `two_green_sandwich_gate.py`: exact polynomial identity for single-sum Fourier factorization search.
- `AUDIT_RESULTS.json`, `EXPLICIT_ESCAPE_RESULTS.json`, `*.log`: evidence.
- `prior_phase10_bundle.zip`: previous checkpoint archive.

The next task is to find an *actual exact all-input Fourier factorization* in the larger Green-sum grammar, not merely demonstrate that its factors can be dense or high rank.
