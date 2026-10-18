# N13 degree-23 operation and scope ledger

This is a bank-count theorem for one fixed transform length and characteristic. A physical bank is not one scalar operation.

## Representation and exact arithmetic

- Field elements have 23 prime-field coefficients, modulus u^23+u+5.
- The 132-bit order and every order-derived exponent use unbounded GMP mpz_class in C++; the separate Python implementations use unbounded int.
- A schoolbook multiplication performs 23^2=529 coefficient products before sparse reduction. Reduction, modular arithmetic, inversion, and exponent bit costs are additional.
- The convolution coefficient bound is 62,192, and the reduced signed bound is at most 435,344. The active field coefficient arithmetic fits signed 32-bit int; undefined-behavior sanitization also passes.
- There are 16 physical banks, each containing 13 inverse branches, for 208 branches and 208 raw weights. Reusing seven same-sign nodes does not merge the banks or their weights.

## Preparation and verification

The first-irreducible search tests five moduli u^23+u+c. Each uses twenty-three Frobenius steps and a polynomial gcd. The final irreducibility proof uses the same exact criterion without extension-field inversions.

Before support search, an independent unbounded-integer preflight checks ten boundary and order-derived powers, field product/inverse, a known seven-root splitting polynomial, and quadratic-character factor exponents. Six deliberately truncated calculations are rejected. This validation is paid preparation, not a bank operation.

The discovery seed is 202610181502. It examines 676 nonzero cross nodes through trial 675 and reaches 676 nonzero-constant recurrence candidates. This finite search establishes no impossibility or runtime guarantee. Factoring H, solving all 13 full sectors, and constructing raw weights are charged preparation.

The C++ literal verifier constructs 208 inverses by Gauss-Jordan elimination and checks 416 dense left/right products, with 169 entries each. Its direct product loops perform 416*13^3=913,952 extension multiplications and corresponding sums, including zero products. The Python checker uses a different zero-diagonal backward recurrence and sparse two-entry matrix products. Both evaluate the raw weighted bank sum and compare all 169 Fourier entries.

## One explicit unoptimized application budget

After all 208 inverse matrices have been prepared, applying the literal network to a single 13-entry input vector can use:

1. Dense inverse-matrix/vector products: 208*169=35,152 field multiplications and 208*156=32,448 additions.
2. Weight each result: 208*13=2,704 multiplications.
3. Sum all 208 thirteen-entry vectors: 13*207=2,691 additions.
4. Multiply thirteen final entries by 1/13: 13 multiplications.

Total: 37,869 extension-field multiplications and 35,139 extension-field additions, excluding preparation and input/output. This is an unoptimized interface budget, not a lower bound or efficiency claim. Shared evaluation opportunities require separate analysis.
