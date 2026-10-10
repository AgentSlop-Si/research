# Source 07: unit_step_core.py

- SHA-256: `6a95e865e6489abd11d312d0b46336e7b2a21320ffff054ada74f145a5130182`
- Representative: `additions/1916/source/unit_step_core.py`
- Assigned batch: `02_addition_1916_01.json`
- Exact snapshot: `snapshots/07_unit_step_core.py`
- Bytes: 22739; fully read lines: 1–663
- New coverage credit: yes, deduplicated against frozen inventory, additive registry and every prior COVERAGE.json.

Complete first-to-last inert text review. No supplied program was executed, imported, compiled, or parsed. Exact bytes and line coverage are recorded; this does not claim formal verification, fresh test execution, or complete dependency closure.

## Purpose

Inherited 663-line prime-power core, streaming majority aggregator, probability/precision models and experiments.

## Complete logic and mathematical identity

Prime-power factoring, same-prime M and K>=M support the covariance projector formula. Local parity twist gives antiperiodic monodromy and a single-cycle balanced decoder. Sequential decoder uses an independently computed seed. Covariance utilities, worst-case active mode, three-grid Boyer–Moore counters, KL tails, conditional roundoff models and experiments were all read. The quantized aggregator returns median grid centers, not medians of the raw samples.

## Actual work and memory

Main row O(N+K log K) arithmetic/O(N) memory; streaming R rows O(R[N+K log K]) and O(N) retained memory. Dense covariance formation repeatedly calls prime_power inside O(N^2 M) displacement loops, potentially O(N^2 M sqrt(N)) trial operations, then O(N^3) eigensolve. draw_state has unbounded rejection trials. Tests and Monte Carlo are separate workloads.

## Guards, exceptions and limitations

validate_dimensions evaluates N%M before rejecting M=0. Sequential helper does not validate the state or summary shape, whereas balanced public path does. g must ultimately produce finite positive tau; advertised tail needs g>sqrt(2). int64 phase products and finite grid integer bins are bounded-machine assumptions. Wider dtype still starts with complex128 FFT/phases. M=1 has zero covariance, so the header claim norm=M/N is only an upper bound in this accepted boundary case.

## Stored-evidence disposition

Preserve saved finite recurrence, variance and precision diagnostics. Conditional error-model constants are not measured universal numerical certificates. The three-grid radius is compatible with its own theory, but cannot be substituted into a coordinate-median certificate; this causes the concrete source 14 contract failure.

## Dependency and preservation boundary

Exact imported/sibling identities, including unresolved historical paths and hash-only nonassigned dependencies, are recorded in DEPENDENCY_IDENTITIES.json. Every preserved non-code artifact has a byte hash in EVIDENCE_IDENTITIES.json. Original/source/snapshot equality is recorded in PRESERVATION_RECEIPT.json. Matching bytes do not confer source review on other hashes.
