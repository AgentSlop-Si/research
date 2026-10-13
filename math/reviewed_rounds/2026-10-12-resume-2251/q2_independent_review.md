# Independent review of the Q2 solver-domain correction

12 October 2026 UTC. ACCEPT only the documentation/interface correction.

The original recovered THEOREM.md row-elimination paragraph and verify_recovery.py were independently read as text. The code already asserts beta^m !=1 and 1-beta^m-alpha^m !=0. The prose states the second inverse-domain condition but omits the first when using individual row inverses. The earlier guarded theorem is preserved; no imported code was run.

Independently checking the algebra: D_a=I-beta q^a T has determinant 1-beta^m, and product D_a=(1-beta^m)I. Two sweeps therefore require row invertibility as well as the full cyclic closure denominator delta. The boundary equation and factor (1-beta^m)/delta in q2_solver_guard_audit.md are correct. Each cycle solve and the complete input/output accounting yield the stated O(m^2) exact-field cost under supplied-root assumptions.

For m=2,q=-1,alpha=beta=1, anticommutation gives (A+B)^2=2I. Thus (I-A-B)[-(I+A+B)]=I. Direct substitution of the displayed vector (-1,-1,-1,0) into the displayed matrix gives e_0, while both displayed row blocks have determinant zero. This is a valid counterexample to extending that particular row-elimination method to the entire full-inverse domain. It is not a counterexample to the inverse identity or a lower bound against other algorithms.

For alpha=beta=1/4 and every m>=2, 1-beta^m>=15/16 and delta>=7/8. The fixed non-Fourier construction is unaffected. No full-output program replay, numerical-stability theorem, historical novelty or general Fourier synthesis is certified here. Original archives remain unchanged.
