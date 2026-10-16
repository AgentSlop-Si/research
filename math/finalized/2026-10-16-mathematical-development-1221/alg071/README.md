# ALG-071 budgeted-materialization formalization

**SCOPED_PASS, 16 October 2026.** Exact owner-source formalization and theorem comparison, independently reviewed. Baseline: `de5dc664448d8e3e219df9651b2805d5a2cecbb1`.

## Accepted results

1. A finite trace/state model explicitly accounts for overlapping groups, output, replay/rebuild, storage modes, cold construction, peak migration memory, and planning charges.
2. The independent single-request-plan surrogate is monotone submodular and inherits the classical one-knapsack `1−1/e` theorem under stated hypotheses.
3. Actual lazy union-refresh savings need not be submodular: an exact four-consumer witness has values `1,1,1,2`.
4. A homogeneous pair-only synchronous case equals a maximum-matching objective and is exactly solvable.
5. Finite-candidate triple selection is NP-hard under an explicit cold-construction ledger, by a complete 3DM reduction.
6. General online migration has a finite offline dynamic-programming specification. Classical MTS/caching ratios require additional hypotheses not supplied by the source.

No new historical novelty, numerical speedup, full-engine certification, general approximation/competitive theorem, or whole-owner closure is claimed. Existing owner status/priority and accepted cache supplement remain unchanged.

## Files

- `MODEL_AND_THEOREMS.md`: specification, full proofs, limitations, and bounded next decision.
- `PRIMARY_THEOREM_COMPARISON.md`: primary sources and exact theorem assumptions.
- `INDEPENDENT_REVIEW.md`: independent proof/source review and incorporated clarifications.
- `verify_model.py`, `CONTROL_RESULTS.json`: self-authored finite controls; no owner-supplied code executed.
- Exact owner-linked source URL, byte count and Git blob identity are recorded in MODEL_AND_THEOREMS.md; the raw connector response is excluded.
- The containing round publication manifest binds these safe copies; original local manifests are excluded.

This package is a research deliverable; it does not mutate the spreadsheet or repository by itself.
