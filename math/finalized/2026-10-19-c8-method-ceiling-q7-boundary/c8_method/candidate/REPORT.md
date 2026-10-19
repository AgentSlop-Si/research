# C8 fixed-chain parameter optimization: complete

The accepted quantitative-gap chain has one limiting numerical condition:

`(6498 + 1800 cos(3pi/8+epsilon)^2)(sqrt(10epsilon)+epsilon)^2 < cos(3pi/8+epsilon)^2`.

Its left-minus-right expression, divided by the positive cosine square, is strictly increasing on `0<epsilon<pi/8`. The unique zero epsilon_star is rigorously bracketed by

- 0.00000216382078575297666905178343251032596362320361;
- 0.00000216382078575297666905178343251032596362320362.

Every auxiliary condition holds uniformly through epsilon=0.000003, beyond this root. Consequently the strict feasible set is exactly `(0, epsilon_star)`. The equality endpoint is a supremum, not an admissible endpoint of the strict sufficient conditions.

Using the lower rational bracket endpoint epsilon_minus certifies

`delta_8,0 > sin(3pi/16 + epsilon_minus/2)`

with lower endpoint approximately **0.555571132594891979835779216476**, improving the previously accepted endpoint by approximately **6.81059552378028e-8**. The sine's angle increment is epsilon/2, not epsilon. A non-strict bound at the implicit method ceiling follows by continuity.

This is a finished optimization certificate, not a proposed sequence of smaller parameter iterations. The rational result is less than 5e-51 below the fixed-chain residual ceiling. Any substantial future improvement requires a changed estimate or different argument.

The original all-phase model and actual potentially non-invariant compressions are preserved. The inherited upper bound remains approximately 0.6410136997181851621. The method ceiling does not establish the true optimum, and no literature novelty is claimed.

Files:

- `PROOF.md`: complete reduction, maximality, normalization, exact interval proof, scope, and endpoint distinction.
- `certify_method_ceiling.py`: standard-library rational checker; no historical code is imported/executed.
- `CHECK_RESULTS.json`: PASS, 142 exact assertions, rational endpoints, outward-rounded enclosures.
- `ASSERTIONS.json`: every exact assertion, including destructive controls.
- `SOURCE_BINDINGS.json`: unchanged accepted proof/review source hashes.
- `MANIFEST.json`: this packet's file hashes.

No external state was changed, no worker was spawned, and no calculation remains pending.
