# Verification scope and independent reproduction guide

This collection contains mathematical prose and result data. It includes no executable code or executable archive. The preserved source manuscript is a candidate with superseded claims. The two full review derivatives and CORRECTED_THEOREM.md give the corrected scope.

## Check byte integrity

FILE_MANIFEST.json records the byte count and SHA-256 of every other file in this collection. Hash the raw bytes, without changing line endings or Unicode normalization. The manuscript hash must remain 68b161ca9880853d38bcf060587a2813cf8b702e5a2c1d75f59f7ae599c42ad1. The two reviews are expressly labeled derivatives and are not byte-identical to their original reports.

ORIGINAL_CONTROL_RESULTS.json is byte-identical to the independent audit's archived output, SHA-256 f1dda81906a33adbc8080d9a93d8ec04f76fe68ef26f8de9e61544ec0e0d1cb9. Its 11 passing groups are historical results. The associated script is not distributed here, and publication preparation did not rerun it.

## Reproduce the direct checks

Use exact rational arithmetic rather than floating-point comparison. Define g_0=b and iterate g_j=q_j g_(j-1)+kappa. Independently expand b times the full product plus kappa times the sum of suffix products, with empty product 1. Compare the two forms, including zero factors and kappa=0.

For a constant q, compare against b q^j + kappa (q^j-1)/(q-1) if q!=1 and b+kappa j if q=1. For rounded recurrences, start at f(1)=1 and evaluate increasing integer w, using the already-computed floor(w/2) and ceil(w/2) values. Compare against the shell or constant envelopes in CORRECTED_THEOREM.md.

For the endpoint counterexamples use b=kappa=1 and compare the exact formulas:

- q_j=1+1/j gives (j+1)H_(j+1)
- q_j=1+2/(j+2) gives (j+1)(j+3)/3
- q_j=j/(j+1) gives (j+2)/2
- q_j=1+1/(floor(sqrt(j))+1) gives floor(g_256/256)=2,227,256,085

For all-integer pointwise saving, evaluate rho(w)=1-1/w and verify f(w)=w. For the matrix-test blind spot, compute 21x_0-7x_1=0 modulo 257 and 21!=0 modulo 257. No source algorithm needs to be executed for these checks.

MINIMAL_VERIFICATION.json records the finite ranges checked with freshly written exact-arithmetic calculations during publication preparation. The proofs in the reports establish the asymptotic statements; no finite check alone proves them.

## What remains unverified

No growing tensor-union compiler, uniform all-input fused DAG family, setup bound, scalar-height certificate, or Fourier speedup is established. The public-result comparisons and project-phase claims in the original manuscript were not independently verified by this review. No novelty clearance is asserted. The original verifier was inspected statically and never executed during either review or this publication preparation.
