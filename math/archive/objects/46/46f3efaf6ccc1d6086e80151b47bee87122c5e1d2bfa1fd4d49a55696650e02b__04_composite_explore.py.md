# Source 04: composite_explore.py

- SHA-256: `51d892149c6d5d1789fad067d38a86d442380b7f7d7fc1728288ab7c92f8696b`
- Representative: `additions/1916/source/composite_explore.py`
- Assigned batch: `02_addition_1916_01.json`
- Exact snapshot: `snapshots/04_composite_explore.py`
- Bytes: 1238; fully read lines: 1–43
- New coverage credit: yes, deduplicated against frozen inventory, additive registry and every prior COVERAGE.json.

Complete first-to-last inert text review. No supplied program was executed, imported, compiled, or parsed. Exact bytes and line coverage are recorded; this does not claim formal verification, fresh test execution, or complete dependency closure.

## Purpose

Small dense covariance-spectrum exploration.

## Complete logic and mathematical identity

Cached totient enumerates all residues; Mobius uses trial factoring. profile constructs the real output-zero Ramanujan covariance from intersected signed displacement sets and reports largest Hermitian eigenvalue, trace and ratio to M/N. Its main loop supplies positive N and divisors M<=sqrt(N).

## Actual work and memory

Covariance formation has O(N^2 M) displacement visits, with cached number-theory costs, O(N^2) storage and O(N^3) dense eigensolve. Uncached totient takes O(q) gcd calls; this is not a fast transform.

## Guards, exceptions and limitations

profile does not independently validate divisibility, positivity or theorem regime. Those missing helper checks do not affect its listed driver inputs. Spectral values are floating diagnostics, not interval enclosures.

## Stored-evidence disposition

composite_ratios.txt is accepted only as saved finite exploration. It does not certify all-N spectral upper bounds or exact rank from float thresholds.

## Dependency and preservation boundary

Exact imported/sibling identities, including unresolved historical paths and hash-only nonassigned dependencies, are recorded in DEPENDENCY_IDENTITIES.json. Every preserved non-code artifact has a byte hash in EVIDENCE_IDENTITIES.json. Original/source/snapshot equality is recorded in PRESERVATION_RECEIPT.json. Matching bytes do not confer source review on other hashes.
