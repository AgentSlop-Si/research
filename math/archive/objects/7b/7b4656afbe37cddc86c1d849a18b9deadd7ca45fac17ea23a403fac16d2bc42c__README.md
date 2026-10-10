# FFT/Green Phase 33 — two-sided gauge completion

Continue of the user's independently ordered Hamiltonian Green-FFT research.

- `THEOREM.md`: exact two-resolvent all-gauges certificate, 25-dimensional first-missing-column map, explicit cyclic specialization of Phase17 rank obstruction, limitations and complexity.
- `phase33_two_sided.py`: **standalone Python stdlib** exact modular implementation; no prior archives required to run the new tests.
- `tests_phase33.py`: independent controls, both-prime exclusion witnesses, exact cyclic solver and Jacobian tests, common-cut rank witnesses.
- `audit.json`: detailed reproducible finite-size certificates, including six pivot rows and modular determinants at two primes.
- `CHECKPOINT.md`: no-loss handoff to next research phase.
- `previous_full_phase32_checkpoint.zip`: entire prior research chain (nested).

**Status: no sub-`NlogN` general FFT**, but the attempted Phase32 two-sided *additive* escape is now restricted by exact algebra and a uniform rank argument. The genuinely surviving branch is a non-additive shared-state architecture.
