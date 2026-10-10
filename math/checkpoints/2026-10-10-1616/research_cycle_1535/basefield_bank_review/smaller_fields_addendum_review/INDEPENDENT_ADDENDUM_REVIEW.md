# Independent acceptance: smaller splitting fields

10 October 2026. Verdict: **accepted as stated**.

Frozen source: `sources/SMALLER_SPLITTING_FIELDS_ADDENDUM.md`, SHA-256 `b80923aea609f9474acf160398dc37a9aa5156545670e793dc87cee089ae1429`.

The accepted all-order base-field theorem and its separate receipt are unchanged. This addendum preserves the eight/fourteen bank counts using new witnesses with smaller extension fields; it does not descend either original frozen witness.

## Accepted order-seven refinement

The source's new cubic factors as (t−q)(t²+A t+B), with the displayed A,B in K=Q(q). Fresh independent exact arithmetic modulo Phi_7 verifies every displayed cubic and quadratic coefficient, the discriminant formula, and both moment recurrences. In particular, this nondepressed cubic satisfies exactly the two equations required for the five edge moments. The recurrence proof remains valid with a nonzero quadratic coefficient; no formula dependent on the old depression condition is reused without adjustment.

At the good prime (43,q−4), the fresh control obtains the cubic t³+18t²+9t+42 and quadratic t²+22t+11. Its discriminant is 10, its value at q is 29, and the cubic constant is 42. Hence all three characteristic-zero nodes are distinct and nonzero. The independently rebuilt selected row minors at b=0,2,3 are 27,19,3. This proves the remaining rows are solvable over K in moment coordinates. The explicit edge recurrence, shared node set, simultaneous reflection, and original phase-weight conversion give the actual eight-bank representation in the unchanged grammar.

For additional literal control, the reduced roots are 4,18,3. The reviewer constructs all eight actual bank slots, solves all sectors, converts every raw phase weight, directly inverts all 56 original branch matrices, checks both inverse products, and verifies all 49 original Fourier entries over F43. These finite-field checks are supplementary; the characteristic-zero existence proof is the exact recurrence plus nonvanishing argument above.

At (43,q−16), the quadratic discriminant is 12, with 12^21=−1 mod43. Since it is a unit nonsquare residue, the exact discriminant is nonsquare in K. Thus the displayed quadratic is irreducible over K, and the new cubic's splitting field has degree **exactly two**. Eight legal banks are therefore attained over this quadratic extension. The accepted all-extension lower bound at N7 remains eight. This result does not prove eight-bank attainment over K itself.

A minor arithmetic typo was corrected before freezing: h(q) at (43,q−4) is 29, not 25. The frozen note uses the corrected value.

## Accepted order-eleven refinement

The canonical construction forces the **rational roots 7 and 8** in the already accepted two-parameter sextic family. The separate exploratory q,q²-root data are not part of this accepted construction.

Write g=g0+lambda·g_lambda+mu·g_mu. The reviewer independently reconstructs the family's 4-by-4 defining moment system over the exact degree-ten cyclotomic field, obtains all three affine coefficient vectors, and solves the 2-by-2 constraints g(7)=g(8)=0. Every rational-basis coefficient of lambda, mu, g, and the quotient quartic matches `N11_RATIONAL_ROOT_SPECIALIZATION.json`. Both root equations, the three s-recurrences, the u-recurrence, and the exact factorization g=(t−7)(t−8)h4 are independently verified.

At the good prime (23,q−2), independent modular derivation gives

- g_lambda=(11,22,12,16,1,0,0), ascending coefficients
- g_mu=(5,2,21,20,0,1,0)
- the root constraint matrix [[17,13],[18,6]], determinant 6
- lambda=mu=0 in the residue field

The exact parameter pair therefore lies in the same local ring and reduces to the accepted good basepoint. All already accepted exceptional factors survive: c0=12, resultant=6, row minors=(5,3,18,8), and product=17. The full accepted fourteen-bank parametric-family theorem applies to this exact K-defined parameter pair. No row formula is changed and no modular point is assumed to lift.

The residual quartic reduces to t⁴+15t³+8t²+20t+15. The reviewer separately enumerates every field element and every monic quadratic divisor to verify irreducibility over F23. It is therefore irreducible over K. Its splitting field contains the two forced roots already in K and has degree at most 4!=24 over K. Each quartic root has degree four, so 4 divides the splitting-field degree. No exact degree-24 assertion is accepted.

This specific fourteen-bank witness is genuinely not K-only, because its remaining quartic is irreducible. It does not rule out a different fourteen-bank K-only witness.

## Count and field boundary

Both same-sign orientations still contain every actual root as an individual bank. A K-defined sum of conjugate banks is not recounted as one bank. The N7 construction has eight banks and 56 original branches; N11 has fourteen banks and 154 original branches. There is no trace/orbit discount, new operation, field-cost-free evaluation, or FFT speedup claim.

The earlier frozen N7 depressed cubic still has splitting-field degree exactly six, as independently established in the core review. The new degree-two witness is a different cubic. Likewise, the N11 canonical two-root specialization is a different sextic within the accepted family. The all-order 2N−4 K-only upper bound and its combined bounds 8≤M_K(7)≤10 and 6≤M_K(11)≤18 are unchanged.

## Independence and scope of executable checks

Four freshly written controls are included. No author or predecessor research program was imported, executed, compiled, or parsed. Mathematical source notes and inert JSON coefficients were read. The exact computations use rational polynomial arithmetic; the literal branch checks are explicitly finite-field computations. The N11 transfer relies on the already accepted complete parametric-family proof, supported here by new exact membership, factorization, and guard checks; this review does not relabel that inherited proof as a new independent 154-branch exact run.

These are accepted explicit arithmetic refinements, not historical-priority findings. The inspected Reznick/Sylvester literature supplies the relevant classical field-sensitive decomposition framework. No external write or publication was performed by this reviewer.
