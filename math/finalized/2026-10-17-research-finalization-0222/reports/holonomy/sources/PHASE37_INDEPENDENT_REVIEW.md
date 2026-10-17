# Independent review: Phase37 projective curvature and complex Green pencils

## Verdict

**Accept the primitive-holonomy single-cycle curvature theorem and all twelve modular certificates for the specified fixed-mask pencil at N4,8,16,32,64,128.** The two reductions at each size rigorously exclude every complex scalar lambda for that one circuit, even up to arbitrary nonzero external diagonal scalings and independent permutations. Neither freely tunable internal masks nor all lengths are excluded. No faster general Fourier algorithm follows.

Minor cost correction: the displayed three-stage circuit has **three** two-branch vector sums, not two. It still uses six Green solves, two internal diagonal masks, a constant number of scalar multiplications and O(N) total arithmetic per application with supplied parameters. Polynomial certification is separate research work.

## Provenance and duplicate identities

The Phase37 ZIP has SHA-256 96ad7b12122e2160c8cc104eefe9b1ab93f7da054881610a37d2c91325218430. CRC and all 33 manifest entries pass. The embedded Phase36 ZIP is byte-identical to the directly reviewed preceding upload, SHA-256 2e4caa636ed9f83fad58227eb1aa5e80e19b22aaedd9a62dfdac867036951fe9.

The separately uploaded `THEOREM (1).md`, SHA-256 41e33de3d9eccd79df4ae2ff04f851eb52b0df0e584f36a3d83a08ae096b1bc4, is byte-identical to the archive theorem. Both source identities are preserved; there is one proof review, not two independent confirmations. Source metadata and comparison are in `PROVENANCE.json`. Uploaded code remained inert. Our checker reads only the serialized cycle orders and polynomial certificate arrays as data.

## 1. Curvature proof

For cycle positions p_i, G_ij=alpha^((p_i−p_j) mod N)/(1−alpha^N). Writing T(u,v)=1_(u<v) separates the ordinary linear exponent from its wrap. The linear row/column terms cancel in anchored ratios, leaving c times the double difference of T when alpha^N=omega^c.

With both anchors zero, the (N−1)-square double-difference matrix is −c times the lower triangular all-ones matrix; its determinant is (−c)^(N−1). At arbitrary row and column anchors, the vectors e_i−e_a and e_j−e_b form integer bases of the same zero-sum lattice. Their change-of-basis matrices are unimodular. Hence every anchored determinant remains a unit modulo N when c is coprime to N. Independent row/column permutations are separate unimodular reorderings.

For Fourier, the anchored exponent is (r_i−r_a)(c_j−c_b), an outer product. At even N, each permuted label set has both parities, so neither reduced vector is zero: its rank over F2 is exactly one. For N=2^m>=4 the primitive-holonomy Green has rank N−1. This proves the stated non-equivalence. The source does not improperly generalize the parity claim to nonprimitive holonomy.

Over an odd finite field, the parity shortcut R^(N/2)=(-1)^E is legitimate only after confirming nonzero entries and R^N=1. Our exact controls check this membership before assigning bits. F2 is the derived exponent-parity field, not the original coefficient field. The result concerns projective ratio structure, distinct from the previously reviewed entrywise phase-matrix rank.

## 2. Fixed circuit and necessary polynomials

The source fixes all six Hamiltonian traversal orders, all rational Gaussian alpha values, both outer branch weights, and both internal masks. Only lambda remains variable in A D1 (G2+lambda G3) D2 C. Every entry is affine in lambda.

Fourier up to arbitrary invertible external monomial gauges is entrywise nonzero and every 2-by-2 cross ratio is an Nth root. Thus the two cleared polynomial conditions

(m00*m1j)^N − (m0j*m10)^N = 0, j=1,2,

are necessary without knowing the external permutations or gauges. Clearing the ratios introduces no false exclusion: a Fourier-equivalent candidate cannot have a zero denominator. Exceptional zero-entry pencil members are already incompatible with Fourier, and are not accepted through division.

Each polynomial has degree at most 2N. The circuit constants lie in Q(i). Since all |alpha_s|<1, every characteristic-zero Green denominator is legal. For the two finite specializations, the checker independently verifies i²=−1, nonzero rational coefficient denominators, and all six 1−alpha_s^N guards. Thus there is a well-defined reduction of the coefficient ring; no bad denominator is silently inverted.

## 3. Exact modular reconstruction and complex lift

For both primes 998244353 and 2013265921, and all six listed sizes, our own dense kernel formula independently builds the required three pencil columns. It reproduces every source polynomial coefficient, including nonzero leading coefficients of degree exactly 2N. The source's stored u,v satisfy u*f1+v*f2=1 in every case. Our separate polynomial Euclidean algorithm also returns gcd one.

Because the degrees are preserved under reduction, the Sylvester matrix specializes with the same dimensions. Gcd one over the residue field implies a nonzero resultant there. The resultant over Q(i) therefore cannot vanish. Consequently the original polynomials have no common complex root. One good prime suffices; the second is a useful redundant check, not a requirement that finite-field solutions be complex solutions.

No numerical root fitting, bounded lambda search, or base-field-only test is used. The modular Bézout identity excludes roots over the entire algebraic closure. We did not need to execute the constructor's separate Q(i) symbolic N4 program, or complete an N8 symbolic expansion, to establish this characteristic-zero proof.

## 4. Cost and architecture boundaries

The own one-pass recurrence agrees with the independently built kernel for all 72 branch/field/size controls. It confirms the linear application schedule, with the three-sum correction stated above. A constant number of basis columns costs O(N) applications, but raising entry polynomials to N and obtaining Bézout/resultant certificates has additional polynomial-arithmetic cost. This certification cost is not an FFT preprocessing shortcut: the candidate is excluded rather than constructed.

For N4, two of the six structural successor maps are affine; for every certified N>=8 all six are distinct and non-affine. Our checker regenerates the seeded traversal list independently and confirms this statement. The all-complex-parameter conclusion belongs to these serialized orders and fixed masks. It does not settle a different seed, freely varying alpha values, independent internal masks, or an unbounded all-N family.

## 5. Fresh controls and replay

All checks passed:

- 12 complete two-prime certificates at N4 through N128, independently rebuilding 2,040 polynomial coefficients;
- 72 dense-kernel versus one-pass Green controls;
- every serialized seeded cycle and its affine/non-affine classification;
- 340 exact integer anchored lattice determinants at N2,4,8,16;
- 30 gauged/permuted finite-field curvature tests through N128, yielding Green rank N−1 and Fourier rank one;
- three planted Fourier pencils, whose necessary polynomials retain their planted common root.

The replay uses standard-library Python and inert JSON certificate data only. The all-anchor and characteristic-zero conclusions rest on the proofs above, rather than extrapolated finite tests. All inherited seals remain unchanged.
