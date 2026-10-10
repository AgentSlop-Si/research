# Full static source review: test_eliminant_extension.py

- Source: additions/1906_chirp/eliminant_extension/test_eliminant_extension.py
- SHA-256: 43766d08eaaceeee1ae0994d69a6c6c6dc80cd0d52dafaf7335c9a309a9d057c
- Bytes: 7784; lines: 166
- Read interval: 1–166 (complete)
- Supplied source execution/import/compile/parse: none
- New exact-hash full-read coverage: yes

## Full-source scope
Read lines 1–166, including three independent/reference helpers, all eight test groups, global results accumulation and the unittest entry point.

## Test design and correctness
leibniz (13–26) expands the original raw Hankel determinant with inversion parity and the exact minimum-exponent subtraction, avoiding the normalized Bareiss construction. det_scalar (29–43) performs row-pivoted modular elimination with swap parity and reduced pivot tests. primitive_root_of_order (46–50) exhaustively verifies exact order; it is intentionally test-only.

All groups were inspected: small characteristics 2,3,5,7,13,101 and ranks 1–5; scalar determinants through rank 10; structured true phases across six n,p,r tuples; folded geometric evaluation across eleven group orders and seven coefficient lengths; unbalanced/balanced Karatsuba products; sparse nonzero-center witnesses through rank 12; growing-rank Bareiss degree/division/inversion ledgers; and Toeplitz/Bareiss comparisons through rank 16. The latter compare an independently structured algorithm against Bareiss, while the lower-rank Leibniz checks anchor Bareiss itself. The tests correctly include p<D and characteristic two rather than relying on interpolation requiring more field points than exist.

## Limits and guards
This tests determinant/evaluation routines, not complete recognizer replacement, candidate recovery, arbitrary-rank numerical stability or FFT speed. Larger-rank scalar comparisons at every field value alone do not identify polynomials when degree exceeds p; they are supplemented by small-rank coefficient comparisons, structural proofs and separate Toeplitz/Bareiss comparisons. True-phase checks establish that generated structured signals yield eliminant roots, not full recognition soundness. Primitive-root inputs and the selected prime moduli are known valid; helper shape/field validation is minimal. The import is a bare adjacent module name, so the intended dependency identity must be preserved when rerunning.

unittest assertions remain active under -O, but assertions inside the tested module do not. RESULTS is mutable global state and would accumulate counters if the suite were run repeatedly in the same imported interpreter; the documented fresh-process invocation does not have this issue. Results are written even if tests fail, with success=false and a nonzero exit code. Partial counters therefore must not be mistaken for a passing report. Stored success=true is a historical record, not newly reproduced evidence.

## Costs and evidence
Permutation expansion is factorial; root search is exhaustive; repeated dense polynomial arithmetic is deliberately expensive. The recorded counters match the loop design: 210, 388, 108, 3,311, 72 and 123 comparisons respectively. The file writes adjacent test_results.json and would overwrite it if run in place. The package wrapper instead uses temporary copies. Exact local dependency is eliminant_extension.py SHA-256 e5a16a36790bd9eaa59857542b6cad1404cc35a6a67ca74ffa9370c47f713db0. No stored-result error was established; accept only as fully read test scaffolding with finite historical results, not a fresh pass.
