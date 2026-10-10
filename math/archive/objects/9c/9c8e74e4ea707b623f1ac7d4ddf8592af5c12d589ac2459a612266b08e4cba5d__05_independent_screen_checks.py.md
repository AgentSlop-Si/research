# Full-source review 05: independent_screen_checks.py

- SHA-256: d6f34b13698552d629beb409cfe9e3c8023cab0e3c9d8c4db15faf3f0867fb8f
- Exact bytes: 4858; complete lines read: 1–105
- Assigned batch: 02_addition_1848_01.json
- Representative path: additions/1848/independent_screen_checks.py
- Snapshot: ../source_snapshots/05_independent_screen_checks.py.txt
- Method: complete first-to-last inert reading, dependency-context inspection, and stored-evidence reconciliation. No supplied execution/import/compilation/syntax parse.
- Findings: F05
- New exact-hash full-review credit: yes, subject to final concurrent deduplication check.

## Verdict and evidence impact
Full static read complete. The exhaustive N=8 permutation enumeration and cached necessary-screen comparison are coherent at GF(12289). Its survivor counts count necessary-screen passes, not actual matrix factorizations. No stored-result contradiction was found.

## Complete control-flow audit
- Lines 1–12: imports standard library plus the exact assigned independent_checks.py (fe537349…). This is a dependency of this checker; its historical phrase “source_programs_executed_or_imported=False” refers to the original research programs, not literally zero module imports. In this review neither checker was imported.
- Lines 14–25: precomputes all 256 subsets and noncyclic transition counts; caches rank(F[complement(missing_rows), columns]). XOR is correct because all masks are restricted to 0,…,255.
- Lines 27–34: interval masks include endpoints and the whole interval; all-subset screen considers equal-sized proper nonempty row/column masks and charges both transition boundaries.
- Lines 35–48: finite-window and first-trace uncertainty necessary inequalities, with exact integer arithmetic and explicit left/right endpoint costs.
- Lines 49–72: enumerates every extra subset of the complement of the chosen columns. Starting at outside includes the full support and the final zero subset includes the original support. The zero check precedes the usual descending submask update, so it terminates. For each excluded maximal run, ccost counts only sides where the original chosen-column interval exists. Required dimension is size−|support|+rank(F[outside rows,support]). Early exit upon one violation preserves the universal-support predicate.
- Lines 74–88: enumerates all 8!=40,320 orders, builds all mapped masks recursively from the least significant bit, and checks every proper subset or interval as appropriate. Since each permutation preserves cardinality, the precomputed table keys exist. Tallies marginal and joint outcomes.
- Lines 89–99: asserts window=15,728, subset=31,384, support=15,728; checks no window survivor fails the other candidates and that uncertainty is strictly weaker. Combined equal counts and inclusion establish equal window/support survivor sets at this finite size. It does not assert the exact uncertainty count 40,320, but the saved output records it.
- Lines 102–105: writes sibling SCREEN_CHECK_RESULTS.json and prints the full result under a main guard.

## Guards and cost
N and prime are fixed valid values and no generalized argument API is offered. Changing N alone would leave the constants 255/256 and asserted counts inconsistent; this is a deliberately fixed N=8 auditor, not an existing bug in that run. Assertions are removable under -O. Cache/table memory is exponential; distinct rank requests are at most O(4^N) and each dense rank is at most O(N³) arithmetic. Support supersets contribute a conservative O(N²·3^N·N) mask/boundary overhead before rank caching; enumerating permutations and all mapped subsets costs O(N!·(2^N+N²)) apart from table construction. The stored 17,978 distinct submatrix ranks show reuse, not polynomial asymptotics.

## Stored evidence reconciliation
SCREEN_CHECK_RESULTS.json equals SCREEN_RUN.log as parsed JSON. Every joint table totals 40,320. Window/support: 15,728; subset: 31,384; uncertainty: 40,320. The joint cells establish the declared inclusion and equality relations. These are inert result consistency checks, not a repeated search or a claim of factorization existence.
