# Source 17: near_resonance.py

SHA-256: `130bfe85a14ec4cdc3c967df39cd1b64d33657c105206eeb8f05868308109ab2`

Original occurrence: `additions/1717/extracted/fft_green_phase20_weyl_shared_state/previous_full_phase19_checkpoint.zip.unpacked/fft_green_phase19_dual_green/near_resonance.py`

Snapshot: `snapshots/17_near_resonance.py`; 1113 bytes; 28 lines. Entire interval 1–28 read inertly. No execution, import, compilation or syntax/AST parsing.

## Mathematical and program scope

NumPy example of near-singular path resolvent norm growth escaping a simple norm budget while lacking primitive DFT phase coherence.

## Control/dataflow and mathematical assessment

B=I-(1-1/N)T/2 is invertible for the intended path. Computes condition via SVD, Green 1-norm and normalized GZ-DG Frobenius defect; it demonstrates norm growth is insufficient for Fourier structure.

## Input and guard coverage

N>=8 assertion only; no integer/finiteness or numerical-conditioning certification. Norm threshold and defect>0.1 are enforced as numerical sample assertions.

## Costs and scaling

Dense inverse/SVD/products O(N^3), O(N^2) space; no fast factorization is implemented.

## Test and acceptance assessment

Main checks N=8..256 powers of two. The docstring correctly labels this illustrative. No run occurred.

## Findings and dependency identity

F06, F08. See FINDINGS.json and DEPENDENCY_IDENTITIES.json. Dependency mapping is by exact frozen occurrence path; it is not a verified runtime import closure.
