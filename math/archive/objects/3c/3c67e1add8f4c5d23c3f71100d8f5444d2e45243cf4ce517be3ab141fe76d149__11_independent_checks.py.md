# Source 11: independent_checks.py

- SHA-256: `80201c9c34b74bdc3141b7e07242867888fb2f6e407145974a3b099209a479f1`
- Representative: `additions/1930_sparse/independent_checks.py`
- Assigned batch: `02_addition_1930_sparse_01.json`
- Exact snapshot: `snapshots/11_independent_checks.py`
- Bytes: 13101; fully read lines: 1–251
- New coverage credit: yes, deduplicated against frozen inventory, additive registry and every prior COVERAGE.json.

Complete first-to-last inert text review. No supplied program was executed, imported, compiled, or parsed. Exact bytes and line coverage are recorded; this does not claim formal verification, fresh test execution, or complete dependency closure.

## Purpose

Exact rational/modular sparse-defect, scan-inverse, repair and Woodbury verifier.

## Complete logic and mathematical identity

All 251 lines read. Pivoted determinants/ranks/inverses, exact primitive roots, closed S inverse, sparse support witness and product telescoping are checked. Witness picks separated row/column intervals and a low-degree independent set, certifying ceil(floor(N/(q+2))/(2q+1)). Boundary q=0 and q>=N handled by driver/empty witnesses. Exact rational scans, modular exceptions, NTT sparse stages, Woodbury singular K and no-pivot chart exceptions are distinct controls.

## Actual work and memory

Dense multiplication/elimination is cubic; support adjacency and greedy scans are at least quadratic in witness size. Exhausting per-row supports costs (sum_{j<=q} binom(N,j))^N. NTT check materializes dense stage matrices and is a verifier, not the fast NTT execution cost. Rational integer bit growth is outside unit-field operation counts.

## Guards, exceptions and limitations

Utilities trust rectangular/square compatible shapes and prime moduli; zip truncation is not general shape validation. Root/order and invertible denominators are checked for driver choices; arbitrary modular parameters can invalidate formulas. pow(...,-1,p) correctly refuses zero denominators.

## Stored-evidence disposition

INDEPENDENT_CHECKS.json embeds exactly this source hash and reports 23,042 exhaustive support patterns, 444 Fourier cases, 305 repair cases. Those historical records are accepted within finite scope; no replay claim. The source itself includes characteristic exceptions, so they do not refute its rational/complex theorem.

## Dependency and preservation boundary

Exact imported/sibling identities, including unresolved historical paths and hash-only nonassigned dependencies, are recorded in DEPENDENCY_IDENTITIES.json. Every preserved non-code artifact has a byte hash in EVIDENCE_IDENTITIES.json. Original/source/snapshot equality is recorded in PRESERVATION_RECEIPT.json. Matching bytes do not confer source review on other hashes.
