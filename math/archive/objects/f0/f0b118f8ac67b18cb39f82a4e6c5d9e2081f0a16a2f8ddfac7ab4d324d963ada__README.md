# FFT stage-rigidity gate · October 10, 2026

**A new exact necessary condition** for the saved, fixed 256-point four-stage FFT candidate.

### Key result

If `F256=S4 P3 S3 P2 S2 P1 S1` with order-one two-sided quasiseparable stages and exact saved permutations, then for **every** choice of diagonal baselines `D1..D4`:

`rank(S1-D1)+rank(S2-D2)+rank(S3-D3)+rank(S4-D4) >= 234.`

In fact, 15 inequalities apply to every nonempty subset of those four rank terms. No generator is required to be nonzero; diagonal baselines may be singular.

### Run the proof certificates

```bash
python verify_rank_rigidity.py
```

Requires Python 3.10+ and `numpy`; verifies 15 polynomial/cut inequalities via 30 nonzero modular 128×128 Fourier determinants, plus 225 separate small-model rank tests. **No floating-point arithmetic is involved**.

Optionally, if `networkx` and `scipy` are installed:

```bash
python audit_all_parity_cuts.py
```

This exhaustively verifies 3,825 full-network min-cuts and 510 exact modular Fourier block ranks. The prior entire research ZIP is included unchanged as `prior_checkpoint_full.zip`.

### Files

- `PROOF_CERTIFICATE.md`: precise theorem, proof and limitations
- `RESEARCH.md`: research narrative, interpretation and next gate
- `EXACT_CERTIFICATES.json`: 15 witnesses including R/C index sets, masks, boundaries and both modular determinants
- `AFFINE_LAYOUT.json`: identical fixed shuffle matrices from the prior checkpoint
- `verify_rank_rigidity.py`: independent exact verifier
- `scan_flow.py`, `fast_mincut.py`, `audit_all_parity_cuts.py`: optional graph cross-check
- `SESSION_HANDOFF.md`: chain recovery and next target
- `prior_checkpoint_full.zip`: byte-for-byte preceding checkpoint

**Not an O(N) FFT. Not a proof that the four-stage network is impossible.**
