# Source 07: independent_modular_audit.py

SHA-256: ee2c48cf4e58e0c1aed64781d5f52b5ce441b1295462a6b0c5a27bf25ba6d628

Representative: additions/1717/triple_audit/independent_modular_audit.py

Read: all 142 lines / 7059 bytes. Full inert inspection; no import, execution, compilation or syntax parse.

## Flow and complete-read coverage

All142 lines: matrix rank/determinant/inverse/product (12–49), cyclotomic JSON reduction/evaluation/lift/gate/root selection (51–79),256 random determinant checks (81–89), guarded GF17 enumeration (91–101),630 invertible positive controls with seven modes (103–133), and literal-wording counterexample/output (134–142).

## Mathematical scope

Rebuilds the complete gate independently of uploaded modules and compares its selected minor to Dhat. Uses the explicit gather identity D[:,j]=(Q C)[:,P[j]], avoiding shorthand permutation ambiguity. The final zero-C counterexample has intentionally retained nontrivial generators and only refutes omitted invertibility wording.

## Input guards and acceptance

Moduli are fixed primes with order8 roots; elimination uses modular inverses. Exhaustive enumeration enforces s≠0,W=0,ΔT≠0. Random spot tests do not guarantee every singular stratum; positive controls explicitly cover fourth/other selected upper zeros and one zero diagonal while retaining invertibility.

## Cost

Θ(p⁴) exhaustive chart search for p17 and bounded-size exact linear algebra; random invertibility loops have no worst-case attempt cap.

## Tests, records, dependencies and actual impact

Saved rank counts total4596 and match source gate counts. Positive controls total630 and fourth-multiplier-zero modes have zero cofactor normals. Historical result labels are not current execution evidence.

Finding references: F01 F07.
