# FFT GREEN RESEARCH — START HERE (Phase 28)

**Last updated:** 10 October 2026. This checkpoint directly continues Phase 27 and preserves all earlier research through a nested Phase 27 full ZIP.

## Files

1. `fft_green_phase28_internal_phase_synthesis/CHECKPOINT.md` — research state and next gate.
2. `fft_green_phase28_internal_phase_synthesis/THEOREM.md` — rigorous project-specific results, all limitations and full proofs.
3. `fft_green_phase28_internal_phase_synthesis/phase28_synthesis.py` — exact two-sided monomial phase/permutation test and algebraic Green-family generators.
4. `fft_green_phase28_internal_phase_synthesis/phase28_polynomial.py` — scalar coupling polynomial constraints and exact gcd/Bezout verification.
5. `fft_green_phase28_internal_phase_synthesis/phase28_executor.py` — O(N)-work Green-sum forward executor.
6. `fft_green_phase28_internal_phase_synthesis/certificates/` — self-contained modular Bezout coefficient certificates at N=4,8,16.
7. `fft_green_phase28_internal_phase_synthesis/previous_full_phase27_checkpoint.zip` — complete previous chain.

## Outcome

- Arbitrary two internal diagonals and two permutations can be eliminated symbolically when the three Green mixers are fixed.
- Any fixed Hamiltonian Green orderings generically fail the 3-mixer/2-mask exact DFT condition; specially tuned couplings are not ruled out.
- With a single scalar middle coupling, at most N^2 admissible complex values can pass one trace constraint, unless its polynomial vanishes identically.
- For the exact seeded non-affine Green triples at N=4,8,16, two explicit polynomial constraints admit **no common admissible complex root**. For N=16 a known singular-denominator root is factored away, then Bezout coprimality is verified.
- This is **not** a sub-NlogN Fourier algorithm, nor an unrestricted lower bound.

## Minimal tests

```bash
cd fft_green_phase28_internal_phase_synthesis
python -m unittest discover -s tests -v
python verify_certificates.py
python audit.py
```

### Phase 29

Design an exact exceptional-parameter synthesis method for two or more independently tunable noncommuting Green parameters, then check all Weyl identities and the full execution cost. Do not return to caching or butterfly-count tricks already exhausted in earlier phases.
