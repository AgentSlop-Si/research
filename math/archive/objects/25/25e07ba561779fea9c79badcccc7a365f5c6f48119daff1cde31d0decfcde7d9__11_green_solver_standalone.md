# Source 11: green_solver_standalone.py

SHA-256: `0a3c26181bbe589dcbc34113e9a2f621bca12e2706a0b3c1dffa0f823212988f`

Exact bytes: 494; fully read lines: 1-20.

Snapshot: `snapshots/11_green_solver_standalone.py`

Inspection: complete inert first-to-last source reading. No source execution, import, compilation or syntax/AST parsing.

## Mathematical and operational scope

Thomas elimination for T=tridiag(-1,3,-1) over a field where every elimination pivot is invertible. Empty input returns an empty vector. A real SPD matrix can still have a zero leading pivot modulo a prime, even when the full modular matrix is nonsingular.

## Control/dataflow and algebra

Lines 9-16 build normalized superdiagonal and right-hand side, then lines 17-20 back-substitute. Signs match the offdiagonal -1 system. There is no pivoting fallback.

## Input/guard and acceptance review

pow(...,-1,p) raises if a pivot is noninvertible; no precheck that p is prime. Example p=3,N=2 yields an invertible matrix [[0,-1],[-1,0]] but fails at the first attempted inverse of 3. That is a missing admitted-domain/pivoting limitation, not evidence that the default tested cases fail.

## Cost accounting

O(N) inversions and modular arithmetic, O(N) temporary memory. For variable p, inverse arithmetic has nonconstant bit complexity; denominators are recomputed for each right-hand side.

## Test coverage and limitations

Used by multiple dense/fast audits, so agreement of callers can share this solver error. No standalone residual T*x=b test or zero-pivot fallback test is in these assigned files.

## Dependency identity

Self-contained with fixed MOD constant; no supplied imports.

## Finding references

F06, F09, F12
