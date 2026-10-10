# Reproduce the independent mathematical controls

Use Python 3.10 or newer. Four verifiers use only the standard library. The Schur-refinement verifier additionally uses SymPy; its accepted run used SymPy 1.14.0. No NumPy dependency is present. These are dependency descriptions, not installation instructions.

Run from this packet root in a disposable copy so the distributed certificates remain unchanged:

```sh
work=$(mktemp -d)
cp -R programs/. "$work/"
python "$work/necklace/independent_controls.py"
python "$work/unitary/fresh_exact_controls.py"
python "$work/unitary_phase/independent_exact_checks.py"
python "$work/schur/fresh_controls.py"
python "$work/schur_refinement/fresh_review_controls.py"
```

Each writes its result JSON beside itself. Compare those results with the corresponding certificates directory. Only the unitary base result's elapsed_seconds and the phase verifier's Python-version string may vary by execution environment; mathematical entries must match. The frozen certificate records retain their measured metadata.

No submitted source implementation, bytecode, runner or archive is required or executed. Three verifiers are byte-identical to independent authored controls. Necklace and phase verifiers are portable derivatives: original archive/source-note hash operations have been removed, with provenance preserved separately. Their mathematical operations and assertions are unchanged. All five distributed programs were run in disposable copies; their mathematical JSON results matched the included certificates.

## Expected results and limitations

- Necklace: eight mathematical groups, 180 weighted traces, 72 mixed Hessians including zero baselines, 24 Gram comparisons, 60 locality plans, 24 Green recurrence cases, 12 finite carrier-rank cases, the characteristic-three zero-Hessian certificate, least-period negative control and two algebraic F4 controls. The historical ninth group was source-integrity checking, now in provenance. F4 controls use a broader affine grammar, not a four-Green Fourier factorization.
- Unitary base: 409,112 permutation checks for N=2 through 9; 36 exact legal-cycle controls, 45 signed-real sums, singular-holonomy and nonunitary guards; exact N2/N3 witnesses and an N4 noncollinear construction. Arithmetic is rational cyclotomic in Q(zeta_12).
- Phase addition: exact Fourier identities at N=2,3,4,5,6 with 3,9,27,81,243 displayed terms; asymmetric constant-diagonal targets at N=2,3,4; N2/N3 actual real witnesses; character distinctness through N8; the N4 13-by-13 character Gram matrix; singular-holonomy, binary-aliasing, disconnected-cycle and gauge-sign negative controls. Arithmetic is rational cyclotomic, without floating tolerances.
- Schur base: reverse-order enumeration through N8; 3,682 full-spark minors; 5,160 order/LIS checks; rationally motivated modular Cauchy controls at N2 through 40, 80 endpoint-gauge controls, five natural-order Fourier constructions, nine two-branch cases, 683 general-separator systems including 187 with singular principal sides, and 676 same-branch systems including 407 with singular A. Bit-reversal rank data remain exploratory and are not promoted to a general theorem.
- Schur refinement: both completion proofs at rational Cauchy N1 through 16, 30 independently gauged/permuted targets, 40 full Schur two-sided inverse checks, 16 reversed-half-block examples, 60 singular-branch systems, the exact complex N4 five-coordinate realization, all 3,682 full-spark minors and three explicit zero-minor certificates.

The all-size assertions are established by the scientific proofs. These deliberately small or slow exact oracles corroborate identities and guards; their operation counts are not fast-algorithm benchmarks, bit-complexity results or numerical-stability certificates.
