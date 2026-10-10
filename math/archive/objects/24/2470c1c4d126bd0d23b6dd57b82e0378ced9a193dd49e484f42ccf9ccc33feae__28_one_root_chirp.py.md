# Source 28: one_root_chirp.py

- SHA-256: `30a8baaca1975333a8b18710a2cabff136a33456527a12db2862949df514de0e`
- Representative: `additions/2020_2027/hero1_phase14/new_source_files/one_root_chirp.py`
- Assigned batch: `02_addition_2020_2027_01.json`
- Exact snapshot: `snapshots/28_one_root_chirp.py`
- Bytes: 2373; fully read lines: 1–61
- New coverage credit: yes, deduplicated against frozen inventory, additive registry and every prior COVERAGE.json.

Complete first-to-last inert text review. No supplied program was executed, imported, compiled, or parsed. Exact bytes and line coverage are recorded; this does not claim formal verification, fresh test execution, or complete dependency closure.

## Purpose

Dyadic one-root phase/gauge table and compact chirp decoder.

## Complete logic and mathematical identity

Generates root table recursively from one primitive G-root, indexes local exponents, compresses blocks, performs one K FFT, uses half-total closure and balanced prefix scan. All caller-dependent arrays and shapes inspected. For even dyadic G/unit a the parity-free monodromy is -1.

## Actual work and memory

O(G+K log K) arithmetic per decode with O(G) table and buffers; root setup O(G) must be charged once when shared. Claim concerns algebraic roots/arithmetic, not exact binary root generation.

## Guards, exceptions and limitations

Table creator requires dyadic G>=2; lower helpers only verify shape and inherited dimensions, not that table entries really are powers of the right primitive root. Intended callers supply correct table. Sequential multiplication causes O(Gu) drift; inverse root indexing and conjugation are only algebraically exact. int64 exponent overflow remains unguarded.

## Stored-evidence disposition

Source warning explicitly disclaims certified numeric implementation. Finite comparisons with np.exp and modular all-basis controls retained; no universal fixed-precision or exact integer-index certificate inferred.

## Dependency and preservation boundary

Exact imported/sibling identities, including unresolved historical paths and hash-only nonassigned dependencies, are recorded in DEPENDENCY_IDENTITIES.json. Every preserved non-code artifact has a byte hash in EVIDENCE_IDENTITIES.json. Original/source/snapshot equality is recorded in PRESERVATION_RECEIPT.json. Matching bytes do not confer source review on other hashes.
