# Source 09: expander_audit.py

SHA-256: `45b1ef1f7b6a11c28fb8f6db05b6c3496c0c3a22433732599abbae8e540ea24b`

Exact bytes: 2042; fully read lines: 1-53.

Snapshot: `snapshots/09_expander_audit.py`

Inspection: complete inert first-to-last source reading. No source execution, import, compilation or syntax/AST parsing.

## Mathematical and operational scope

Random-path finite samples with a floating Laplacian lambda2 estimate, sampled balanced cuts, and two small finite-field executor checks. A floating eigensolver output is not an exact spectral-gap certificate; the later exact integer certificate source provides a separate stronger method for its own sizes.

## Control/dataflow and algebra

laplacian_lambda2 counts both paths as a multigraph, including repeated edges with multiplicity. run builds seeded permutations for N=32,64,128,256, computes lambda2*N/4, samples 16 cuts, and checks three full vectors only for N<=64.

## Input/guard and acceptance review

No eigensolver error enclosure or explicit finite-result check; the meets flag compares an approximate value directly to .25. Sampled cut assertion is not universal. lambda2 needs N>=2 but helper has no guard. Fixed pseudorandom seed is reproducibility, not proof of a uniform random graph distribution.

## Cost accounting

Dense N^2 Laplacian storage and O(N^3) numerical eigensolve; sample cut checks are linear per sample. Dense exact executor comparison costs O(N^2) after construction. This does not inherit the O(N) per-input stage cost as an audit cost.

## Test coverage and limitations

Main driver lists finite sizes and 16 cuts per size; no adverse small-gap instance, threshold-near rounding test or exact interval enclosure. The source correctly says a failed spectral threshold does not certify that sample.

## Dependency identity

NumPy runtime/version and LAPACK implementation are unpinned; local expander_stage, exact_audit and linear_inverse hashes are bound.

## Finding references

F03, F07, F09, F12
