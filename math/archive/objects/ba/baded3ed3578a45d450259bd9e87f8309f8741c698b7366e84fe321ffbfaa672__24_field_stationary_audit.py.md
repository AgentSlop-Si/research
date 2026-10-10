# Source 24: field_stationary_audit.py

- SHA-256: `6f07d26cd7c663e147ff7fad02c3b3e4155a2b46ea0a7804b692ac462dcfbc67`
- Representative: `additions/2020_2027/hero1_phase14/new_source_files/field_stationary_audit.py`
- Assigned batch: `02_addition_2020_2027_01.json`
- Exact snapshot: `snapshots/24_field_stationary_audit.py`
- Bytes: 4645; fully read lines: 1–110
- New coverage credit: yes, deduplicated against frozen inventory, additive registry and every prior COVERAGE.json.

Complete first-to-last inert text review. No supplied program was executed, imported, compiled, or parsed. Exact bytes and line coverage are recorded; this does not claim formal verification, fresh test execution, or complete dependency closure.

## Purpose

Exact finite-field stationary full-rank chart verifier.

## Complete logic and mathematical identity

Constructs distinct exponent nodes E(u), inverts Vandermonde W with pivoting, verifies W inverse and Toeplitz Gram, caches per-channel per-summary impulse responses only for verification, and compares all N^2 Fourier entries. Wrong-node mutation checks inverse coefficient differences.

## Actual work and memory

O(M^3) inversion; basis cache has m*M*K*G=mG^2 scalar entries and its construction repeatedly uses the quadratic direct-K decoder. All-basis composition is high polynomial. Explicit verifier cache is not charged as a fast fresh-input transform.

## Guards, exceptions and limitations

Known finite fields and compatible dyadic M supplied; helper guards do not independently require M|G, but cases satisfy it. Wrong mutation proves the inverse differs, rather than directly comparing its full transformed outputs; stronger independent audit later checks actual output mutations.

## Stored-evidence disposition

FIELD_STATIONARY_RESULTS.json reports 202,240 exact Fourier entries over five cases. Accept stored finite exact algebra with formal inverse-root convention; it is not a complex norm proof or sub-FFT algorithm. No reported result contradicted.

## Dependency and preservation boundary

Exact imported/sibling identities, including unresolved historical paths and hash-only nonassigned dependencies, are recorded in DEPENDENCY_IDENTITIES.json. Every preserved non-code artifact has a byte hash in EVIDENCE_IDENTITIES.json. Original/source/snapshot equality is recorded in PRESERVATION_RECEIPT.json. Matching bytes do not confer source review on other hashes.
