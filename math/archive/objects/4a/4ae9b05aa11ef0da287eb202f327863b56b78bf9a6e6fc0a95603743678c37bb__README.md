# Signed magnetic fusion package

## Main conclusions

`SIGNED_MAGNETIC_FUSION.md` provides direct all-field proofs, for every odd N>=3 with a supplied primitive Nth root and characteristic not dividing N:

1. Three signed orientations leave exact Weyl-support holes; all four cover the index square.
2. Fourier realization by finitely many legal weighted magnetic banks needs
   r_+,r_- >= ceil((N-1)/4), hence at least max(4,2 ceil((N-1)/4)) parameter-pair banks.
3. One pair per orientation is impossible for every odd N>=9. At N=9 the stronger bound r_+,r_- >=3 gives at least six banks.
4. N=3 has an explicit legal four-bank Fourier realization over every admissible field, so the four-bank minimum is exact there.
5. At most 4N legal banks realize any matrix by explicit root-Vandermonde interpolation. Combined with the lower bound, Fourier bank-count order is Theta(N). The naive construction and application cost O(N^3), with O(N^2) stored weights; this is not an FFT improvement.

Each counted bank contains N weighted phase-indexed literal inverse branches. The count is not the old F014 two-resolvent-product branch count, and it is not an application-time lower bound. See the grammar comparison in S8.

## Residual questions and exact-control boundary

- N=5 full coefficient realizability with one bank per orientation (four banks total) remains unresolved over C and in general admissible fields. The complete F11 control fails but is not extrapolated.
- N=7: the necessary row ideal over Q(zeta7) reduces exactly to [1] in a reproduced symbolic control, independently rebuilt by the reviewer. No all-characteristic theorem is claimed from that computation.
- Main next test: N=9 with at least three banks on each delta side, all four orientations present, and the entire coefficient system plus inverse guards enforced. Six is necessary, not known sufficient.
- Growing-bank existence is settled by the coarse 4N construction. The broader open algorithmic question is whether compact Fourier weights and shared evaluation give a genuine improved fully charged algorithm. Support coverage and parameter-bank count do not settle it.

## Reproduction

All Python files here are newly authored. No supplied research implementation was executed, imported, compiled, or AST-parsed.

From the workspace root:

- `python research_cycle_0958/signed_magnetic_fusion/fresh_signed_controls.py`
- `python research_cycle_0958/signed_magnetic_fusion/fresh_nine_certificate.py`
- `python research_cycle_0958/signed_magnetic_fusion/fresh_small_row_algebra.py`

The first script uses only Python's standard library; the other two use exact SymPy algebra. The saved results record 15 support lengths, 60 direct signed branch-matrix checks, four checks of the explicit N=3 construction, eight original-inverse checks of the 4N-bank interpolation construction, a separate positive F7 realization, exact small-field failures, and the N=9 integer-polynomial certificate. These support, rather than replace, the direct proofs.

`SMALL_CONTROL_SCOPE.md` gives the exact N=5/N=7 polynomial input, fields, denominator guards, and why the unit-ideal computation is kept separate. `PROPOSED_FUSION_ROW.json` records the proposed research transition. Historical priority remains unresolved.
