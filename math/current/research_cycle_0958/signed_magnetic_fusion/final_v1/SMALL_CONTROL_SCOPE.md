# Reproducible small symbolic controls and their exact scope

These are supplementary controls. They are not needed for the all-field support, bank-count, or N=9 theorems.

## Exact polynomial input

For N=5 or 7, take the characteristic-zero field K=Q[q]/Phi_N(q), with Phi_5=q^4+q^3+q^2+q+1 and Phi_7=q^6+q^5+q^4+q^3+q^2+q+1. SymPy represents a root by an exact `CRootOf`; because the cyclotomic polynomial is irreducible over Q, the selected complex embedding does not alter the ideal calculation.

For each integer a=2,...,N-2, the input polynomial in K[x,y] is the reduction modulo Phi_N(q) of

E_a=q^[((a+1)^2 * inverse_mod_N(4)) mod N] (1-q^2)(1-q^(N-2))
    -q x^(a-1)(1-q^(a+1))(1-q^(N-2))
    -y^(N-a-1)(1-q^(a-1))(1-q^2).

These are exactly the necessary S4 row equations after multiplication by the nonzero common denominator (1-q^2)(1-q^(-2)). All q exponents may be reduced modulo N. A primitive odd Nth root ensures both denominator factors are nonzero.

There is no guard localization in this computation. The ideal is formed in the full polynomial ring K[x,y], allowing x=0 or y=0 as well. A unit ideal there excludes the smaller allowed nonzero-parameter locus. Conversely, a non-unit ideal there is only an inconclusive necessary-condition check. Beta, Delta and remaining coefficient amplitudes are not variables in this row-only relaxation, so row consistency cannot prove a full legal representation.

## Reproduction and result

Run `python fresh_small_row_algebra.py` from the workspace root (the saved program uses the explicit task-relative result path). The script is freshly authored, imports SymPy rather than any research-supplied implementation, constructs the polynomials above anew, uses the exact cyclotomic coefficient field, and records the reduced Groebner basis in `fresh_small_row_algebra_results.json`.

- N=5: two input polynomials; non-unit reduced basis. No existence or nonexistence conclusion about the full Fourier representation follows.
- N=7: four input polynomials; reduced Groebner basis [1]. This is a reproducible exact symbolic control over characteristic zero. We have not supplied a standalone human-sized Bezout combination of the E_a, and do not promote it to a separately reviewed all-field theorem or reduce it to arbitrary finite characteristic.

The result is explicitly separate from the direct, all-admissible-field proof for every odd N>=9. The exact finite-field controls use original branch matrices and modular elimination; they neither validate nor invalidate complex realizability.
