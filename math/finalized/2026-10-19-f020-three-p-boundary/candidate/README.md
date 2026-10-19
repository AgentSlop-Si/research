# F020: resolve the b=3p boundary

Read REPORT.md for the full two-case proof and RESULT.json for its exact scope. Independent review is required.

- p>=5: new three-whole-block residual, explicit derivative test, degree-2p irreducible factor and ordinary discriminant valuation.
- p=3: fixed-degree P9 quartic-discriminant certificate, uniform over all s>=3.
- 74 fresh exact assertions passed; no source checker was executed.

Reproduce the controls with `python check_boundary.py` and `python check_p3_certificate.py`. The first uses only the Python standard library; the second uses installed SymPy. No network is used. The final scripts read no exploratory outputs.

The owner remains open at priority 58. No broader theorem, historical priority, or performance claim is made.
