# Separate acceptance of the fixed-order parametric addendum

Verdict: accepted. This receipt concerns the two-parameter extension of the order-eleven upper-bound construction only. It does not change the frozen main witness, its fourteen-bank upper bound, or the accepted small-order results.

Let c_4=lambda and c_5=mu. The addendum solves the same constant invertible 4-by-4 matrix A for c_0,...,c_3 against an affine right-hand side. Hence those four coefficients belong to K[lambda,mu], with K=Q(q), and are affine in the parameters. The reviewer recomputed the constant, lambda, and mu coefficient vectors exactly and verified all four moment recurrence equations coefficient by coefficient. This is a polynomial identity check for arbitrary parameters, not inference from finitely many numerical examples.

The sextic remains monic. Therefore remainders of t^r modulo it are polynomial in its coefficients, and the selected row minors D_0,D_3,D_4,D_5 lie in K[lambda,mu]. Its derivative resultant is polynomial as well. Thus

P=c_0 Res(g,g') D_0 D_3 D_4 D_5

is indeed a polynomial with no parameter-dependent denominator. It is defined by the concrete determinant formulas in the frozen notes, rather than an unspecified generic nondegeneracy condition. At the base point (0,0), the independent main certificate gives the nonzero residue

12*6*5*3*18*8 = 17 modulo 23.

Consequently P is not identically zero, and P!=0 defines a nonempty Zariski-open subset of the two-dimensional parameter space. Since K is infinite, that open subset contains infinitely many K-rational parameter pairs. The two free coefficients are genuinely independent: they occur as the t^4 and t^5 coefficients of the defining monic sextic.

For every characteristic-zero extension E/K and parameter pair in E^2 with P!=0:

1. c_0!=0 and Res(g,g')!=0 give six distinct nonzero roots in a splitting field L/E.
2. The same four selected row systems are invertible.
3. The two explicit edge formulas remain valid: each formula in the main note retains the sums over all c_0,...,c_5, and its proof uses the four recurrences, not the extra base-point condition c_4=c_5=0.
4. Simultaneous reflection supplies the remaining five rows.
5. The same Lagrange amplitudes, sector-index bijection, raw-weight normalization and legal-inverse identities turn the row solutions into at most fourteen permitted whole banks over L.
6. The splitting-field degree remains bounded by 6!=720 over E.

The reviewer also tested four explicitly defined characteristic-zero specializations using exact field arithmetic. All twenty-two edge equations passed at each. The product P has nonzero residue 17 at (0,0), 15 at (0,1), and 9 at (1,1), which certifies those particular points as permitted. Its residue at (1,0) is zero; this is inconclusive at this prime and is neither an exclusion of that characteristic-zero point nor a failure of the addendum. The general proof relies on coefficientwise identities and P!=0, not these extra samples.

## Scope

This is an infinite collection of realizations at the single fixed order N=11. It is not an infinite family of transform orders, an exact minimum, a K-only node construction, a classification, or an arithmetic-speedup theorem. There remain fourteen whole banks and 154 original resolvent branches per realization, with the same algebraic preprocessing and field caveats as the main construction. The exact main literal control applies at the frozen base point; the all-parameter extension follows from the universal algebraic identities just reviewed, not from an unperformed symbolic expansion of every generic original matrix entry.

## Independent evidence

`../review_family_n11.py` was written independently and imports only the reviewer's own arithmetic and base reconstruction. It does not read or execute author programs. `FAMILY_CONTROL_RESULTS.json` contains all affine coefficient vectors and specialization results; `family_review.log` records the run. The frozen addendum and its hash are identified in `FAMILY_ACCEPTANCE_RECEIPT.json`.

Reproduce in a writable copy with `python review_family_n11.py` from the main review directory. This also refreshes the base reconstruction outputs by importing the reviewer's own first control. No external or publication writes were performed.
