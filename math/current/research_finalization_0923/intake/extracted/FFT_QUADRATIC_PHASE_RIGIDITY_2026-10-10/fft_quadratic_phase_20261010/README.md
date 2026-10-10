# FFT quadratic phase rigidity research package

**Objective:** build a provably stronger exact rejection gate for the user’s non-affine four-Green Fourier architecture, without recycling previous commutator or graph-cut results.

**Main result:** `THEOREM.md` proves a three-column symmetric-square certificate for all free diagonal gauges and a positive spectral-error gap at fixed complex stages. Real 4-Green examples at N=3 and N=4 have a singular old commutator but full-rank new quadratic certificate: exact finite-field data plus a simple-root Hensel argument certifies existence of such algebraic complex examples.

## Reproduce

From this directory run:

```bash
python verify.py
python independent_sympy.py
python hensel_lift.py
python numeric_gap.py
```

The first and third scripts need only Python standard library. The independent script requires SymPy; the numerical diagnostic requires NumPy and SymPy.

## What the files mean

- `THEOREM.md`: assumptions, theorem and complete proofs, exact examples, limitations.
- `verify.py`: stand-alone exact prime-field implementation, Green inverse via finite geometric series.
- `independent_sympy.py`: independent sparse-inverse reconstruction and polarization of quadratic coefficients.
- `hensel_lift.py`: explicit p-adic root lifts; supplementary to the all-orders Hensel proof.
- `numeric_gap.py`: floating-point checks of the operator-norm bound, **not interval-certified numerical evidence**.
- `CERT_N3.json`, `CERT_N4.json`: original integral branch weights/gauges/permutations and exact modular matrices.
- `RESULTS.json`, `HENSEL_RESULTS.json`, `NUMERIC_RESULTS.json`: actual test outputs.
- `PRIOR_ART.md`: literature and project nonduplication audit.
- `NEXT_GATE.md`: precise open all-length constructive conjecture.

**No exact fresh arbitrary-input O(N) FFT and no peer-reviewed novelty claim.**
