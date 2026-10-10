# Source 14: green_product_audit.py

SHA-256: `ab494a808995e86eee84e3bd6f6ea71d364f4df47fefc43021858890f39b371c`

Original occurrence: `additions/1717/extracted/fft_green_phase20_weyl_shared_state/previous_full_phase19_checkpoint.zip.unpacked/fft_green_phase19_dual_green/green_product_audit.py`

Snapshot: `snapshots/14_green_product_audit.py`; 1875 bytes; 53 lines. Entire interval 1–53 read inertly. No execution, import, compilation or syntax/AST parsing.

## Mathematical and program scope

Seeded phase19 fixed outer-stage rejection: each stage is a sum of two independently permuted, two-sided chirp-gauged tridiagonal inverses.

## Control/dataflow and mathematical assessment

For fixed invertible A,B, joint_gate can exclude all possible middle monomials by a necessary signature mismatch or exhaustive gauge contradiction. The result explicitly says for fixed stages; it does not exclude every possible Green parameter choice. l/r phases are nonzero, but tridiagonal offdiagonals 1+w^a can vanish, so samples need not have every path edge present.

## Input and guard coverage

Dense inverse throws if a denominator or outer sum is singular; the random constructor does not guarantee or retry invertibility. Assertion forces impossible and will fail on inconclusive rather than claiming exclusion, which is conservative in normal mode.

## Costs and scaling

Cubic dense oracle generation/inversion plus joint-gate cost; the comment about a tridiagonal forward solve describes an underlying alternative, not the actual code path.

## Test and acceptance assessment

Twelve size/seed combinations in main. No separate tests for singularities or cap exhaustion; current execution none.

## Findings and dependency identity

F06, F08, F10. See FINDINGS.json and DEPENDENCY_IDENTITIES.json. Dependency mapping is by exact frozen occurrence path; it is not a verified runtime import closure.
