# Full-source review 04: independent_checks.py

- SHA-256: fe53734936068ff1a34e14522102a7956b1eb233b3f167a4dbf90a253d88c092
- Exact bytes: 8364; complete lines read: 1–200
- Assigned batch: 02_addition_1848_01.json
- Representative path: additions/1848/independent_checks.py
- Snapshot: ../source_snapshots/04_independent_checks.py.txt
- Method: complete first-to-last inert reading, dependency-context inspection, and stored-evidence reconciliation. No supplied execution/import/compilation/syntax parse.
- Findings: F05
- New exact-hash full-review credit: yes, subject to final concurrent deduplication check.

## Verdict and evidence impact
Full static read complete. The exact finite-field rank checker and deterministic rational controls are internally coherent for the hardcoded dyadic sizes and three prime fields. The source explicitly treats these as regression controls; it does not derive a universal complex-field theorem from finite-field examples. No stored-count inconsistency was found.

## Complete control-flow audit
- Lines 1–13: standard-library-only imports, explicit separation between finite controls and the analytical endpoint proof.
- Lines 15–31: incremental row echelon basis. Each installed pivot is normalized to one; eliminating earlier pivots yields a correct exact rank over a field for rectangular rows. Empty row/column selections correctly yield zero.
- Lines 34–46: scans candidates for an n-th root, accepting w^n=1 and w^(n/2)≠1. This proves exact order for n a power of two, which covers every call here. It is not a general composite-n primitive-root test. For fixed prime and dyadic n≥2, the condition is candidate^((p−1)/2)≠1, so the first successful candidate is shared across sizes; independently built q-root matrices are compatible powers of the n-root matrix in coset checks. n=1 produces the single trivial root. All three listed primes support n≤128.
- Lines 49–87: submatrix extraction, bit-reversal generation, exact cut-rank recurrence, ceiling lower bounds, and exact integer sum formula. The recurrence reflects k>N/2 before reducing (N,k) to (N/4,floor(k/2)); N=2 supplies the nonzero base. All-N/dyadic proof is not supplied by evaluating the function.
- Lines 89–150: 435 direct bit-reversal cuts, 288 seeded random critical minors, 336 whole-coset decompositions, 336 consecutive-coset controls, and every 3-by-5 critical N=8 minor in each field (9,408 total). The larger minors are sampled, not exhaustive. The finite-field comparison to a complex-derived number is an observed control, not a proof of a field-uniform lower bound.
- Lines 152–179: recurrence/profile/sum/maximum checks at N=2,…,32768 and exact Fraction second-moment algebra at every odd cut. These large-N profiles are recurrence evaluations, not dense matrix ranks at N=32768.
- Lines 181–190: independently ordered N=16 rank-8 counterexample to replacing arbitrary Fourier submatrix ranks by min(rows,columns); explicit field/proof limits in return data.
- Lines 193–200: guarded main writes sibling CHECK_RESULTS.json and prints summary.

## Guards and complexity
Helpers assume a positive dyadic size, prime modulus, consistent rectangular rows, and valid indices. Violating those assumptions can return a wrong root/rank or raise; all actual call sites meet the assumptions. pow(value,-1,prime) correctly fails on nonunits. Plain assert enforcement vanishes under -O; no evidence of an optimized historical invocation exists. Dense Fourier matrices use O(N²) storage; echelon rank on a-by-b input costs O(a·b·min(a,b)) arithmetic in the worst case. Repeating over O(N) cuts can cost O(N⁴), while each generated recurrence profile costs O(N log N) integer work and O(N) storage. Root search also pays modular exponentiation. These are research controls, not an improved FFT runtime.

## Stored evidence reconciliation
All six saved count fields equal independent arithmetic counts from the source loop bounds. The result contains 15 recurrence-profile sizes; the saved max rank and total rank are not relabeled direct ranks outside the explicitly tested sizes. ENDPOINT_AUDIT.md preserves the characteristic-zero positivity assumptions and the no-factorization/no-runtime inference boundary. Stored logs/results are preserved, not freshly rerun.
