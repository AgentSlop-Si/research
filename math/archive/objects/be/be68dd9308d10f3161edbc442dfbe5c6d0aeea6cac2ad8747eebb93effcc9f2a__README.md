# Hero #17 — Phase 5 Gauge-Union Research

**Core result:** an exact new-to-this-project counterexample to the proposed cross-channel rank-sharing shortcut: the same arbitrary-input Fourier transform permits orbit gauges with transition-mask ranks 1 through M. Additional exact scoped results: \(M/\gcd(M,\Delta)\) rank law for the canonical gauge, an all-divisor weighted MST formula, a rigorous complex conditioning warning, and a prime-index rigidity theorem for the orthogonal gauge.

**Status:** Proven identities plus executable checks; not a universal O(N) FFT and not a newly claimed priority result.

Files:
- `RESEARCH.md` — definitions, theorems, full proofs, model caveats, literature boundary.
- `phase5.py` — finite-field construction, full charged direct DFT calculation, minimal Schur decomposition, MST, orthogonal-gauge controls.
- `test_phase5.py` — eight test groups.
- `independent_audit.py` — separate direct reference transforms, separate field ranks, independent Prim MST checks, and 130-digit condition number checks.
- `AUDIT_RESULTS.json` — measured test counts and high-precision results.
- `CHAIN_CHECKPOINT.md` — exact recovery context, novelty boundary and next research target.
- `SHA256SUMS.txt` — file checksums.

Requirements: Python 3.10+ for the finite-field package; `mpmath` additionally required for the independent complex-conditioning audit.

```sh
python -m unittest discover -v
python independent_audit.py
```

The implementation deliberately inverts dense matrices and evaluates kernels directly; it is a rigorous cost-**negative** research experiment, not a claimed fast FFT. The standard FFT remains a better algorithm for arbitrary input under usual computation models.
