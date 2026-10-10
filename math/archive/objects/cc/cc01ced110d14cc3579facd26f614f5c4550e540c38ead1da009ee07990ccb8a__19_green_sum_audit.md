# Source 19: green_sum_audit.py

SHA-256: `45f4f881eabc0e7e2044c4ce15c5b215e6837beea6dfa78ebcf6c8518a78fb49`

Exact bytes: 3579; fully read lines: 1-88.

Snapshot: `snapshots/19_green_sum_audit.py`

Inspection: complete inert first-to-last source reading. No source execution, import, compilation or syntax/AST parsing.

## Mathematical and operational scope

Finite-field audit of G3+G4 under two-stage interval and half-cut rank barriers. It supports fixed instances of a structured family; universal all-permutation statements rely on the decomposition proof, not sampled shuffles.

## Control/dataflow and algebra

tridiagonal_solve is a general Thomas recurrence. sum_green_matrix assembles basis columns of two inverse tridiagonals. actual_green_case computes four contribution rectangles and their ranks. actual_green_halfcut_case uses complementary halfcuts and checks at least one deficient product rank.

## Input/guard and acceptance review

Definite custom-modulus propagation bug at lines 25-31: sum_green_matrix(n,p) calls tridiagonal_solve(3,e) and tridiagonal_solve(4,e) without p=p, then only reduces the resulting default-field residues modulo p. That is generally not either requested-field Green inverse. The solver fails on empty RHS and on zero/nonunit pivots without fallback. Public case sizes are explicitly limited.

## Cost accounting

Dense Green construction O(N^2) arithmetic/storage; halfcut rectangles/ranks O(N^3); square-root interval rectangles O(N*m^2) plus rank costs. The generator is an audit, while a stage applies using two linear solves.

## Test coverage and limitations

test_minor_gate and test_halfcut exercise default modulus and concrete Green cases; both classes are located after unittest.main, so discovery includes them but direct invocation does not. No p!=MOD or empty RHS test.

## Dependency identity

Exact in-batch minor_certificate, halfcut_certificate and their rank/build helpers. Despite the word independent, primitive rank and decomposition code is shared with other audits.

## Finding references

F02, F03, F06, F09, F12, F13
