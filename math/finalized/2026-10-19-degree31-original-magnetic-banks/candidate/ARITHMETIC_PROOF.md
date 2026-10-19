# Exact arithmetic proof for degree 31

## Field representation and irreducibility

Let p=53, d=31, and m(U)=U^31+2U+11. Both 53 and 31 are prime (trial division through their square roots suffices). Coordinates [a0,...,a30] denote sum ai U^i, with every ai in {0,...,52}.

`field_preflight.py` uses only prime-polynomial arithmetic and unbounded Python integers, without any extension-field inverse. It computes all 31 successive Frobenius remainders and proves

- U^(53^31) = U modulo m;
- gcd(m,U^53-U)=1.

The polynomial X^(53^31)-X has derivative -1, so it is squarefree. Its irreducible factors over F53 have degrees dividing 31. The gcd excludes degree one; degree(m)=31 therefore forces m irreducible. `FIELD_IRREDUCIBILITY.json` preserves the exact remainders and gcd. The standalone literal checker repeats this proof before its first extension-field inversion.

The initial representation scan X^31+X+c, c=1,...,52, had no irreducible member. Before any support search or extension inversion, the representation scan was explicitly amended to lexicographic X^31+aX+c, a,c=1,...,52. The first success is a=2,c=11, the 63rd polynomial. `SEARCH_SCOPE_AMENDMENT.json` preserves this change. The field remains exactly F_(53^31); the support seed and trial cap never changed. `FIELD_SEARCH.json` retains all 63 tests. No broader field or larger support budget was used.

## Integer-width proof

Q=53^31=283499278281258657725525680568509306972713148562602397 has 178 bits. The principal exponents are

- Q-2 = 283499278281258657725525680568509306972713148562602395;
- (Q+3)/8 = 35437409785157332215690710071063663371589143570325300;
- (Q-1)/2 = 141749639140629328862762840284254653486356574281301198.

The C++ implementation uses GMP `mpz_class` for Q, element exponents, inversion, polynomial exponents, splitting, the quadratic gate and root factorization. No order-derived path narrows to 128, 64 or 32 bits. The Python implementations use unbounded integers. The 64-bit xorshift state is intentionally reduced modulo 2^64; bounded search counters are also 64-bit. These do not hold field exponents.

Since 53^31 is 5 modulo 8 and 23^2=-1 modulo 53, the usual exponent (Q+3)/8 with the optional factor 23 computes candidate square roots. Every proposed square root is checked by squaring before use. Zero denominators are excluded before inversion.

`ARITHMETIC_PROBE.json` and the separately implemented ordinary-polynomial `check_arithmetic.py` agree on multiplication, inversion, ten boundary/order-derived powers, a known seven-root polynomial, splitting and factor characters. Six negative controls reject wrapped Q, wrapping 2^128 to zero, and truncated inverse, splitting, square-root and factor exponents. Undefined-behavior sanitization checks the fresh arithmetic probe and literal reconstruction.

## Convolution and reduction bounds

For canonical coefficients, each unreduced schoolbook coefficient is a sum of at most 31 products, each at most 52^2. Therefore

    0 <= c_k <= 31*52^2 = 83,824.

This exceeds 65,535: 16-bit radix slots are unsafe. The active C++ and Python field implementations use ordinary coefficient convolution. A separate 17-bit packing audit is only a differential/negative control.

Reduction uses U^31=-2U-11. For high k in {31,...,60}, replace c_k U^k by -11 c_k U^(k-31)-2 c_k U^(k-30). Both new indices are below 31, so no high-degree term receives feedback and every high c_k retains its original nonnegative convolution value until reduced. A low coefficient receives at most its original contribution and one contribution of each multiplier 11 and 2. The conservative bound on its absolute magnitude is

    (1+2+11)*83,824 = 1,173,536 < 2^31-1.

Each intermediate product and partial sum is within this bound, so signed 32-bit C++ `int` is sufficient for the actual chosen modulus. Small prime-field arithmetic and Gaussian-binomial index arithmetic are also bounded far below int32. This bound does not inherit the degree-29 multiplier 8.

`check_convolution_boundary.py` checks all 31^2=961 ordered basis pairs, 100 deterministic dense pairs and the all-52 pair against ordinary convolution and generic long division. It explicitly rejects unsafe 16-bit carry assumptions and detects both raw and reduced-product corruption. All arithmetic preflight receipts precede the support search, as bound in `DISCOVERY_CHRONOLOGY.json`.
