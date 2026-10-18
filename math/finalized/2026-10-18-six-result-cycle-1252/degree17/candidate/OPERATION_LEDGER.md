# N13 degree-seventeen operation and scope ledger

This is a bank-count theorem for one fixed length and characteristic. It
does not identify a bank with one scalar arithmetic operation.

## Stored representation

* Field: seventeen prime-field coefficients per element, modulus u^17+u+6.
* 16 physical banks, each containing 13 inverse branches: 208 branches.
* 208 raw branch weights, plus nodes, beta values and guards.
* 13 input and 13 output elements of F_(53^17).
* Seven distinct same-sign nodes are reused between the two orientations;
  the banks and their weights still count separately.

## Preparation and verification

Field irreducibility is established by seventeen exact 53rd-power modular
steps and a polynomial gcd. Root discovery, polynomial splitting,
factorization, extension arithmetic, thirteen full sector solves, and raw
weight construction are charged preparation work, not free bank operations.
The search makes no complexity or runtime advantage claim.

The C++ literal verifier prepares 208 complete 13-by-13 inverses by
Gauss-Jordan elimination. It checks 416 dense left/right matrix products,
each with 169 entries. Its straightforward product loops perform
416*13^3=913,952 extension multiplications and the corresponding sums,
including multiplications by zero. These are validation costs.

The independently implemented Python checker uses the zero-diagonal
backward recurrence to prepare each inverse. It then checks the same
416 inverse identities with the two nonzero entries per row/column of
the original branch matrices. Both checkers evaluate all 208 weighted
inverse matrices and compare the final 169 target entries. Neither
algorithm treats field inversion or degree-seventeen multiplication as free.

## One explicit, unoptimized evaluation budget

If all 208 inverse matrices are already prepared, a literal evaluation on
one input vector can use:

1. 208 dense inverse-matrix/vector products: 208*169=35,152 field
   multiplications and 208*156=32,448 field additions.
2. Weight all 208 resulting thirteen-entry vectors: 2,704 field
   multiplications.
3. Sum the 208 vectors: 13*207=2,691 field additions.
4. Multiply the final thirteen entries by 1/13: 13 field multiplications.

Thus this unoptimized interface uses 37,869 extension-field multiplications
and 35,139 extension-field additions after preparation. Factoring the common
1/13 outside the bank sum is exact distributivity. This budget is provided
to avoid confusing sixteen banks with sixteen scalar operations; it is not
a lower bound and does not claim an efficient implementation.

A schoolbook degree-seventeen field multiplication has 289 coefficient
products before reduction. Reduction and modular arithmetic are additional
paid work. Bit cost, input/output, memory, preparation, and possible shared
evaluation improvements require separate analysis. No FFT speedup follows
from the attainment certificate.
