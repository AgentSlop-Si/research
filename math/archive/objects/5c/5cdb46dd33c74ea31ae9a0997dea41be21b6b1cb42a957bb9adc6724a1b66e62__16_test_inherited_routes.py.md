# Source 16: test_inherited_routes.py

- SHA-256: `935ff170190decd88acf63a0c51026dd0a15f74b954ffe588da9d006ce0eb34f`
- Representative: `additions/1954/divisor_audit/source_evidence/test_inherited_routes.py`
- Assigned batch: `02_addition_1954_01.json`
- Exact snapshot: `snapshots/16_test_inherited_routes.py`
- Bytes: 3071; fully read lines: 1–76
- New coverage credit: yes, deduplicated against frozen inventory, additive registry and every prior COVERAGE.json.

Complete first-to-last inert text review. No supplied program was executed, imported, compiled, or parsed. Exact bytes and line coverage are recorded; this does not claim formal verification, fresh test execution, or complete dependency closure.

## Purpose

Five inherited offset/Bessel route regression tests.

## Complete logic and mathematical identity

Tests exact modulated lift for small lengths, complete small-state unbiasedness, streamed versus materialized Bessel row, finite fused row plus deterministic center bound, and exact scan-fusion rank. The test named fused_error explicitly compares the deterministic center, not the random row against target.

## Actual work and memory

Small full-state enumeration plus explicit reference FFTs and Fraction rank. Runtime is test workload; no throughput theorem.

## Guards, exceptions and limitations

The suite never tests planner parameters against execute_candidate, never compares quantized output to candidate tolerance, and never validates tail-only fused bias. Its own center bound correctly includes addition error, making the dispatch mismatch visible rather than fixed.

## Stored-evidence disposition

Saved pass log is consistent with these narrow assertions and does not contradict the counterexample. All imported module exact hashes resolved within this batch; no execution performed.

## Dependency and preservation boundary

Exact imported/sibling identities, including unresolved historical paths and hash-only nonassigned dependencies, are recorded in DEPENDENCY_IDENTITIES.json. Every preserved non-code artifact has a byte hash in EVIDENCE_IDENTITIES.json. Original/source/snapshot equality is recorded in PRESERVATION_RECEIPT.json. Matching bytes do not confer source review on other hashes.
