# N13 degree-29 operation and scope ledger

This is a physical-bank count theorem for fixed N=13 and characteristic 53. A bank is not one scalar operation.

## Exact arithmetic and preparation

- A field element has 29 prime-field coefficients, modulus u^29+u+8.
- The 167-bit field order and every order-derived C++ exponent use unbounded GMP mpz_class; all Python exponents use unbounded int.
- A schoolbook field product has 29^2=841 coefficient products before reduction. Modular reductions, coefficient additions, inversion, and exponent bit costs are additional.
- The convolution coefficient bound is 78,416. The conservative signed sparse-reduction bound is 784,160, within signed 32-bit int. No reduced term feeds back into degree >=29.
- The active Python literal verifier uses ordinary convolution. The separate 17-bit packing audit checks all 841 basis pairs, 100 dense pairs, and one worst-case dense pair. Deliberately using 16 bits corrupts the worst-case convolution and field product and is rejected.
- Sixteen banks contain thirteen original inverse branches each: 208 branches and 208 raw weights. Reusing same-sign nodes does not merge banks or weights.

The modulus search tests eight polynomials u^29+u+c. The final field proof retains all twenty-nine Frobenius remainders and a gcd. Exact arithmetic preflight checks ten powers, multiplication, inversion, a known split polynomial, and factor characters. Six exponent-truncation controls and three packing controls are paid preparation, not bank operations.

Discovery uses seed 202610181745, checks 10,426 nonzero cross nodes through trial 10,425, and reaches 10,497 nonzero-constant recurrence candidates. There are 302,354 PRNG coefficient draws with no zero cross node skipped. This finite run implies no runtime guarantee or nonexistence theorem. Factoring H, solving all thirteen full sectors, and constructing the raw weights are additional preparation.

## Literal verification

The C++ checker forms 208 inverses by Gauss-Jordan elimination and validates 416 dense left/right products, each with 169 entries. The explicit dense product loops have 416*13^3=913,952 extension-field multiplications and corresponding sums, including products by zero. The Python checker instead uses a zero-diagonal backward inverse recurrence and sparse two-entry products. Both then form the supplied raw-weighted original bank sum and compare every Fourier entry. The cold replay and sanitizer repeat selected preparation and verification; they are not free application work.

## One explicit unoptimized application budget

Once all 208 inverse matrices have been prepared, one application to a thirteen-entry input vector can use:

1. Dense inverse-matrix/vector products: 208*169=35,152 field multiplications and 208*156=32,448 additions.
2. Weight each branch result: 208*13=2,704 multiplications.
3. Sum the 208 branch-result vectors: 13*207=2,691 additions.
4. Multiply thirteen final entries by 1/13: 13 multiplications.

Total: 37,869 extension-field multiplications and 35,139 extension-field additions, excluding preparation and input/output. This is one unoptimized prepared-matrix budget, not a lower bound, optimal implementation, or speed claim. Sharing opportunities require separate analysis.
