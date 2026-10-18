# Independent review: dyadic norm transfer and the sixteen-point stage interval

Date: 18 October 2026. Owner: M-MULTISCALE-CHIRP / Q24.

## Verdict

**ACCEPT the scoped theorem and constructions. No mathematical correction is required.**

A legal length-L dyadic chirp representation descends to length L+e, where e counts even strides, with individual invertibility preserved. At sixteen points, the minimum is at least seven in characteristic zero and in characteristic 17 with zeta^2=3. Fifteen stages suffice over C, over a finite splitting extension of Q(zeta), and over F(17^12) in the stated characteristic-17 setting.

The conclusion remains **7 <= minimum <= 15**, not an exact sixteen-point minimum. It does not close the broader owner or establish attainment over Q(zeta), an FFT speedup, efficient coefficient discovery, bit complexity, numerical stability, or historical priority. No external write, catalogue update, status/score change, or census change was made.

Frozen reviewed REPORT.md SHA-256:

`0b966bf02a815e93a5437040d78ee97620906bea70279d59a57100eff39cc3c5`

All nine canonical manifest entries and all four inherited source bindings match their recorded hashes and byte lengths. The independent verifier reads candidate text and certificate data only. It imports and executes no candidate program, including no historical checker or certificate generator.

## Independent exact results

The separately authored `independent_verify.py` and `INDEPENDENT_RESULTS.json` establish:

- All 112 stored parity input polynomials are exactly the cyclic coefficient equations rebuilt by ordinary symbolic expansion of the grouped products.
- All fourteen rational unit identities sum to 1. The same fourteen identities reduce to 1 over F17.
- All 56 five-factor count vectors are covered by the fourteen rotation-orbit representatives.
- The multipliers contain exactly 182 nonzero terms; the maximum product degree is 13; denominator prime divisors are exactly 2, 3, 5 and 7.
- Independent multiplier and equation mutation controls reject all fourteen selected mutations of each type.
- All 256 entries of C Q_16(S)=16I hold in Z[a]/(a^16+1). The displayed expanded Q_16 is correct. All 256 coefficient shift-normalization identities and the sixteen-point parity identity hold.
- The integral norm identity holds at N=4,8,16,32,64 using an independent even/odd decomposition: if Q(x)=A(x^2)+xB(x^2), its norm is A(y)^2-yB(y)^2.
- Every original and descended factor is nonzero at every relevant root in all 6,663 legal parameter/stride cases over the three chosen fields. This gives 95,404 rootwise norm and legality checks and independently confirms the stride-sensitive pole guard.
- Independent polynomial factorization over F17 gives the stated degrees 1,4,4,6. The quadratic t^2-3 is irreducible, t has order 32, and Q_16(a z)=R(z) holds coefficient by coefficient. The independent gcd(R(z),z^16+1)=1 verifies the finite construction's pole exclusion.
- On all sixteen basis inputs for every legal alpha in F97, 1,296 independent in-place recurrence applications satisfy every cyclic equation and the exact 31-multiplication/30-addition count.

## Normalization and parity coverage

The original scalar Weyl-monomial grammar is preserved. Moving modulations through resolvents rescales parameters, and an invertible circulant target forces the remaining modulation to be scalar. The verified shift identity absorbs the remaining monomial using only a scalar and root-of-unity rescaling. Negative strides introduce only an allowed scalar and monomial, and zero parameters need no inversion.

For N divisible by eight, shifting the chirp coefficients by N/2 gives Q_N(-x)=x^(N/2)Q_N(x). At N=16, canceling the even-stride factor product is valid because each original factor, hence that product, is a unit.

Removing a monomial x^r from an odd-stride product changes the parity equation's sign by (-1)^r. A rescaling x -> lambda x with lambda^16=1 and lambda^8=-1 restores a negative sign. Such a lambda exists in the allowed field containing zeta, although passing to the algebraic closure for an exclusion would also be legitimate.

Substitution x -> x^3 preserves the parity equation because x^24=x^8 modulo x^16-1. Reducing negative stride classes then induces the cycle 1 -> 3 -> 7 -> 5 -> 1, with the same available sign correction. Thus the fourteen rotation representatives exhaust all 56 count vectors. Zero-padding includes every shorter odd product. Allowing arbitrary grouped coefficients enlarges the possible solution set, so their unit-ideal exclusion is safe.

The eight equations f_i=(-1)^i c_i-c_(i+8), 0<=i<8, are the full independent coefficient conditions: the other eight repeat them up to nonzero signs. Each stored certificate is bound to exactly these equations, in exactly the recorded variable and stride order. These are literal rational polynomial identities, not a finite-point search. No invertibility guard or nonzero grouped coefficient is needed for their contradiction. Their denominators are units modulo 17.

Consequently at least six odd factors are required. If total length were at most six, it would be exactly six and every stride would be odd.

## Norm identity, legality, and iteration

Work in A_N=K[x]/(x^N-1), with characteristic not dividing 2N and zeta primitive of order 2N. The map x -> -x is an automorphism and the even subalgebra is K[y]/(y^(N/2)-1), y=x^2.

For coefficient x^(2u), shifting the summation index t by u gives

`sum_t (-1)^t a^(t^2+(2u-t)^2) = (-1)^u a^(2u^2) H_N`.

Odd coefficients vanish because the norm is even and characteristic is not two. This proves the displayed normalized target H_N Q_(N/2)(-y), with the smaller chirp root zeta^2. The nonzero value of H_N follows from the original chirp being a unit and the norm being a product of units. No unproved Gauss-sum square-root normalization enters.

For odd s, the descended binomial is 1-alpha^2 y^s. For even s, it is two copies of 1-alpha y^(s/2). Evaluation on each smaller root, lifted to the pair x,-x, proves individual invertibility. Equivalently, the precise original guard is alpha^(N/gcd(N,s)) != 1. The substitution y -> -y preserves invertibility and remains in the same coefficient field. Thus the length is L+e in the original grammar; the normalization scalar becomes only an allowed scalar gauge.

At each further descent an even stride halves and doubles its multiplicity; an odd stride stays odd and does not double. After k descents the multiplicity is therefore 2^min(v_2(s),k). Rescalings change parameters but not these multiplicities. The stated iterated inequalities are necessary lower-bound obstructions and are not claimed sufficient or free implementations.

## Seven-stage consequence and characteristic restrictions

A hypothetical six-stage sixteen-point representation has only odd strides, so its norm descends to a legal six-stage eight-point representation over the same coefficient field. This contradicts the hash-bound accepted eight-point theorem.

In characteristic zero, zeta^2 is the required primitive sixteenth root and the accepted lower bound applies to every containing coefficient field. In characteristic 17 with zeta^2=3, the descended root is exactly the one covered by the accepted algebraic-closure exclusion. The old F17-rational minima 10 and 11 are not used. The new rational parity identities reduce directly modulo 17 and do not require a specialization argument.

No claim is made here for the other characteristic-17 primitive roots or for arbitrary positive characteristics. Although the new parity identities have broader reductions away from their denominator primes, the full seven-stage conclusion also requires the applicable inherited eight-point lower bound.

## Fifteen-stage attainment

In characteristic zero, Q_16 has degree fifteen and constant coefficient one. Its roots are nonzero. In a splitting field, taking their reciprocals produces fifteen normalized shift-one factors with product exactly Q_16. The inverse-matrix identity excludes every sixteenth root of unity from Q_16's zero set, so every individual resolvent is legal. The allowed scalar 16 then gives C. The degree bound 15! for a splitting extension is valid in characteristic zero. No assertion of splitting over the original cyclotomic field is needed.

In characteristic 17, the independent factorization confirms R=-(z-1)G1G2G3 and irreducibility degrees 1,4,4,6. Their roots lie in F(17^12), which also contains the quadratic extension holding zeta. The Frobenius conjugates of one root of each factor give all its roots. Rescaling a root beta of R to a beta as a root of Q gives alpha=zeta/beta, exactly the parameter list in the report. The linear root beta=1 gives alpha=zeta.

The finite-field splitting and Frobenius facts agree with Keith Conrad's primary reference, [Finite Fields](https://kconrad.math.uconn.edu/blurbs/galoistheory/finitefields.pdf), especially its splitting-field discussion and Frobenius-conjugate statement. This validates the exact algebraic witness without pretending that a coordinate-level root table or a coefficient-discovery implementation was supplied.

## Complete cost and memory audit

For one factor, Horner evaluation takes 15 multiplications and 15 additions. Multiplication by the precomputed d adds one multiplication. Recovering the other fifteen outputs takes 15 multiplications and 15 additions. The count is therefore exactly 31M_K+30A_K for the stated straight-line procedure, including alpha=0 if the procedure is run without shortcuts.

Fifteen applications cost 465M_K+450A_K. The final scalar gauge uses sixteen further multiplications, giving 481M_K+450A_K. Computing alpha^16 by four squarings for each of fifteen parameters adds 60 multiplications; computing each 1-alpha^16 and its inverse adds fifteen subtractions and fifteen inversions. Setup plus one vector is exactly the declared 541M_K+465A_K+15Inv_K.

This bill presupposes the fifteen alpha values. Field selection/construction, root discovery, reciprocals, embeddings and conversion remain in the explicitly separate F_coeff. General extension-field operations are not silently treated as base-field or constant-time bit operations. The report does not present the arithmetic bill as bit complexity or a numerical algorithm.

The Horner pass reads the original buffer before replacing its last element. Subsequent recovery overwrites entries in increasing order, using only the preceding recovered output and the still-unmodified current input. A sixteen-element data buffer and at most two scalar work registers suffice once parameters are loaded. The thirty parameter/precomputed-inverse elements are correctly listed separately. A final scalar pass is included in the arithmetic count. No runtime, memory advantage over FFT, conditioning, precision or stability conclusion follows.
