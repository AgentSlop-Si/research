# Source 06: independent_finite_fiber_check.py

SHA-256: a6727f60c7686960d60b77ae06de7f3a75e425d85e97b982e846c51126318c49

Representative: additions/1717/triple_audit/independent_finite_fiber_check.py

Read: all 50 lines / 2658 bytes. Full inert inspection; no import, execution, compilation or syntax parse.

## Flow and complete-read coverage

All50 lines: read W and extract W2,W1,W0 (5–18), polynomial division and gcd assertions (19–21), coefficient/exterior determinant (23–34), fixed 5×5 Sylvester certificate (35–41), and rational coefficient serialization/results (42–50).

## Mathematical scope

On the actual input, W2 uniquely determines h0, r1 has fixed nonzero leading h1² coefficient, and nonzero degree6 h2 resultant gives at most12 exceptional base points. Adding free h6 gives dimension≤1 for this exceptional stratum; the full necessary locus remains dimension≤2.

## Input guards and acceptance

The code checks absence of h0/h6 in remainders and a constant nonzero leading h1 coefficient. It does not explicitly guard W2 linearity/nonzero h0 coefficient or upper h1 degrees before fixed-degree extraction. Those conditions were inspected in stored data and hold, so this is defensive hardening rather than a stored witness failure.

## Cost

Small exact symbolic determinant, polynomial division and gcd. No global complexity consequence.

## Tests, records, dependencies and actual impact

Saved finite_fiber_results.json gives the explicit W2 coefficients, leading h1 coefficient, and degree6 resultant. This completed certificate is independent of the unfinished exploratory factorization path.

Finding references: F06 F07.
