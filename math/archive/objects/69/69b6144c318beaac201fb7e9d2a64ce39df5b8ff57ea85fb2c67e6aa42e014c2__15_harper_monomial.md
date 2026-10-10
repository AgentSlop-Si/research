# Source 15: harper_monomial.py

SHA-256: `d163cf558a82fb75cabf71eccb9da70bd38b90a68e0dacbe174ab34f91a838c7`

Original occurrence: `additions/1717/extracted/fft_green_phase20_weyl_shared_state/previous_full_phase19_checkpoint.zip.unpacked/fft_green_phase19_dual_green/harper_monomial.py`

Snapshot: `snapshots/15_harper_monomial.py`; 1677 bytes; 35 lines. Entire interval 1–35 read inertly. No execution, import, compilation or syntax/AST parsing.

## Mathematical and program scope

Finite-field Harper monomial symmetry enumeration and a fixed-pole (7,11) resolvent sandwich obstruction.

## Control/dataflow and mathematical assessment

allowed_symmetries keeps permutations preserving V values and cycle adjacency and asserts precisely identity/reflection at the checked sizes. no_single_harper_sandwich verifies invertible H-7I,H-11I and computes the uniquely necessary middle C=(H-7I)F(H-11I); any row count differing from one rejects monomiality for that pair. It does not quantify over all poles.

## Input and guard coverage

Domain is inherited from cyclic_operators; inverse failures are explicit. Assertions are decisive. No separate guard restricts factorial enumeration to small N.

## Costs and scaling

Theta(N!*N) enumeration upper model; dense cubic inversion/products for each fixed-pole check. The uniform complex theorem mentioned in the docstring was not supplied/read in this source batch.

## Test and acceptance assessment

phase19 caller enumerates N=4,8 and tests fixed poles at N=8,16,32. No source execution.

## Findings and dependency identity

F06, F08, F10. See FINDINGS.json and DEPENDENCY_IDENTITIES.json. Dependency mapping is by exact frozen occurrence path; it is not a verified runtime import closure.
