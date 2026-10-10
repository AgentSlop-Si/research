# Source 06: offset_class_lift.py

- SHA-256: `faed217b4db4af2afb2ab8ff947e37fbde190618c7387fc525cf39af37424283`
- Representative: `additions/1916/source/offset_class_lift.py`
- Assigned batch: `02_addition_1916_01.json`
- Exact snapshot: `snapshots/06_offset_class_lift.py`
- Bytes: 5261; fully read lines: 1–140
- New coverage credit: yes, deduplicated against frozen inventory, additive registry and every prior COVERAGE.json.

Complete first-to-last inert text review. No supplied program was executed, imported, compiled, or parsed. Exact bytes and line coverage are recorded; this does not claim formal verification, fresh test execution, or complete dependency closure.

## Purpose

Exact fractional-offset-class lift over a prime-power sketch.

## Complete logic and mathematical identity

Prime radix checked by trial division; plan uses exact Python-integer nearest-grid indices and centered offset numerators, with int64 storage and distinctness assertions. h=N/gcd(N,Q). Each class modulates one padded input, applies one Q sketch under the same state, and retains only its frequency targets with sqrt(Q/N) scaling. Rows use independent states before coordinate median aggregation.

## Actual work and memory

O(h[Q+(Q/M)log(Q/M)]) row arithmetic, O(Q+N) streaming workspace, O(RN) robust buffer. classes() actually sorts via np.unique and scans N entries per class, adding O(N log N+hN); plan also sorts for injectivity. Hence the advertised ideal O(hQ) omits literal sorting costs, even though an arithmetic-progression implementation can remove them.

## Guards, exceptions and limitations

The optional class cap is enforced. N=1 is intentionally padded to the chosen prime here, unlike the later offset_core boundary behavior. Shape is flattened; invalid hand-made plans and nonfinite arrays are not fully validated. int64/float root limits persist.

## Stored-evidence disposition

Saved modulation identities and projection equivalence are valid finite support for exact expectation, not exact single-row recovery. Full-state covariance tests use a relabeled conjugated state distribution; see source 08. No stored error invalidation found.

## Dependency and preservation boundary

Exact imported/sibling identities, including unresolved historical paths and hash-only nonassigned dependencies, are recorded in DEPENDENCY_IDENTITIES.json. Every preserved non-code artifact has a byte hash in EVIDENCE_IDENTITIES.json. Original/source/snapshot equality is recorded in PRESERVATION_RECEIPT.json. Matching bytes do not confer source review on other hashes.
