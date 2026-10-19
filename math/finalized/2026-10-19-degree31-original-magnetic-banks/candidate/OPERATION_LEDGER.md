# N13 degree-31 operation and scope ledger

The objective is the number of physical banks in the stated original grammar. A physical bank is not a scalar operation, and a 16-bank certificate is not a fast Fourier transform complexity bound.

## Paid preparation

- A field element has 31 prime-field coordinates. A schoolbook field multiplication has 961 coefficient products, followed by additions and reduction modulo U^31+2U+11. The ordinary-convolution bound is 83,824; the conservative signed-reduction bound is 1,173,536. No high-degree feedback occurs.
- Field orders and exponents are 178-bit or smaller unbounded integers, rather than a unit-cost machine integer. Binary exponentiation, inverse preparation and polynomial arithmetic are charged preparation. For positive exponent e, the specific element-power loop uses popcount(e) nonsquaring products and bit_length(e)-1 squarings, including its initially trivial accumulator product.
- The modulus scan tests 63 trinomials. Each test computes 31 Frobenius steps and one prime-polynomial gcd; it uses no extension inverse.
- Arithmetic preflight includes ten powers, an inverse/product, seven-root polynomial splitting and character probes, six truncation controls, and 1,062 ordinary-convolution differentials with three packing controls. These checks are not free application work.
- Discovery uses seed 202610192024 and a frozen limit of 100,000 nonzero cross nodes. It stops after 1,114 nodes, 34,534 coefficient draws, zero skipped zero nodes, and 1,117 nonzero-constant recurrence candidates. The first split is trial 1113 (zero-based). Search costs are recorded in `SEARCH_RESOURCE.json`: about 11.15 wall seconds, 11.16 user CPU seconds and 10,240 KiB maximum child RSS in this environment. Timing is an observed run, not an asymptotic claim.
- Every cross node requires powers through degree 13, six-window affine-line solving, the quadratic compatibility gate and any resulting splitting tests. `PREFIX_LEDGER.jsonl` retains every tested node, gate root, candidate polynomial and split result. The two cold runs ending at 1,113 and 1,114 nodes reexecute the complete failed prefix and first hit; both are additional paid computation.
- Factoring the successful degree-seven polynomial, preparing its actual roots, solving thirteen full 13-by-16 sector systems, and constructing 208 raw weights from 208 amplitudes are paid preparation. Root finding uses the full (Q-1)/2 exponent. None of this is part of a single primitive bank application.

## Literal verification

There are sixteen separate banks, thirteen branches per bank, 208 branch inverses, 208 raw weights and 208 supplied sector amplitudes. Sharing roots between same-sign orientations does not merge banks or eliminate charged weights.

The C++ literal reconstruction uses Gauss-Jordan inverses and checks both dense products for every branch. The product loops explicitly execute 416*13^3=913,952 extension-field multiplications, including zero products, and the corresponding accumulation additions. The 416 matrix identities contain 70,304 scalar equalities.

The standalone Python check uses a distinct zero-diagonal backward recurrence and sparse two-term products. It independently checks all thirteen full sectors (169 equations), all 208 raw/amplitude identities, the sixteen pole guards and the literal weighted original bank sum against all 169 target entries. The C++ and Python implementations have the same author; the separately assigned reviewer supplies actual independent review.

Mutation tests, source rebuild, cold prefix replay and sanitizer checks are additional verification work. They do not imply a practical runtime advantage. Runtime fields can vary between repetitions and are not cryptographic mathematics claims.

## Explicit unoptimized prepared-matrix application

After all 208 inverse matrices are prepared, one application to an arbitrary thirteen-coordinate input can use:

1. 208 dense 13-by-13 matrix/vector products: 35,152 field multiplications and 32,448 additions.
2. Weight the 208 branch outputs: 2,704 multiplications.
3. Sum all branch vectors: 2,691 additions.
4. Apply the final factor 1/13: 13 multiplications.

Total: 37,869 extension-field multiplications and 35,139 additions, excluding preparation, storage, input and output. Prepared dense branches occupy 35,152 field elements; raw weights add 208 elements, in addition to parameters, amplitudes and temporary storage. Each element occupies 31 base-field coordinates in the literal encoding. This is one explicit unoptimized implementation, not an optimality or speed claim. Any sharing improvement needs its own accounting.
