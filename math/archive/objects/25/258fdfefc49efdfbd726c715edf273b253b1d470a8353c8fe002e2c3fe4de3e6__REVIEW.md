# Independent review: two-column Fourier phase pencil

## Verdict and important scope correction

**Accept the fixed-stage gauge equivalence, determinant rejection gate, exact N8 four-Green witness, its characteristic-zero nonvanishing lift, and the classical generic diagonal/matroid rank formula.** All 12,869 nonempty square minors and the determinant55687 were independently verified.

The witness defeats **one-sided rank-capacity tests** requiring candidate ranks at least the Fourier ranks. It does not defeat every rank test. At composite N8, Fourier has singular minors while this candidate is full spark. Our explicit rows {0,4}, columns {0,2} have Fourier rank1 and candidate rank2. Thus exact rank-profile equality already rejects this particular product. The claimed limitation should be stated for capacity/min-cut sufficiency, not all rank information.

No uniform Fourier executor, unrestricted impossibility, or global novelty claim follows.

## Provenance and prior attribution

Library file [private-id], version0; ZIP SHA-256 9c8ab62b0fd55eec0647c0d9c0951fea229a42f9d2f0205a8f512c879ae093d2, 21,867 bytes. CRC passes. The standalone source contains no checksum manifest or embedded predecessor ZIP. Its historical source inventory is not treated as an independent audit of every archive.

We directly inspected and snapshotted the actual prior Phase18 and Phase19 theorems. Phase18 already states the fixed-stage Weyl monomial-similarity condition; Phase19 already gives spanning-forest graph-cocycle recovery and consistency tests. Those ingredients receive inherited credit. The two-column arrangement and finite counterexample are evaluated here without assigning publication priority. Uploaded code remained inert.

## Algebra and guards

For M=A diag(d) B, its jth column covariance residual is

A diag(B[:,j+1])d − Delta A diag(B[:,j])d = K_j d.

Hence all K_j annihilate d exactly when MS=Delta M. This forces row k to be c_k times Fourier row k. When A,B and diag(d) are invertible, every c_k is nonzero, and L=diag(c_k^{-1}) gives LADB=F. Conversely L commutes with Delta, so equality implies covariance. Multiplying by A^{-1},B^{-1} gives the stated diagonal-similarity equation D(BSB^{-1})=(A^{-1}Delta A)D. No additional genericity is needed.

The all-nonzero requirement on d and invertibility assumptions are essential for the sufficiency/normalization statement. det K0≠0 is a valid rejection without such a search, but det K0=0 is not acceptance. Our control keeps the first two Fourier columns and modifies B[0,2]; then K0=0 while K1 forces d0=0. It is invertible B but has no allowed full-support gauge.

The complete graph-potential test is valid with exact support equality, self-loop equality, and consistency around all underlying closed walks, permitting reciprocal traversal of directed edges. Those conditions recover nonzero vertex potentials per component. O(N+E) applies after X,Y and their entries are available. Dense formation/inversion and O(N²) entry verification must be charged. K0 itself can be applied with two A applications when the needed columns are supplied, but computing or certifying its determinant has not been shown to take linear work. This source is a synthesis/rejection gate, not an application algorithm.

The fixed-stage theorem permits a free output diagonal L and middle diagonal D. It does not additionally quantify over arbitrary new input/output permutations; those already in the saved branches are fixed. A different target ordering needs the corresponding transformed pencil.

## Exact witness and characteristic-zero lift

Our own unique-path cyclic Green formula reconstructs each of the four branches from the saved structural successor permutation, nonzero weights, independent endpoint permutations and diagonal scales. It is independently checked against direct matrix inversion. The aggregate A,B are invertible and exactly reproduce the saved matrices.

Both Gaussian elimination and an independent 8! Leibniz sum give det K0=55687 over F65537, with omega4096 of exact order8. The saved middle gauge produces a full-spark M: all 12,869 nonempty square minors are nonzero. All225 divisor-coset row/column profiles dominate the exact Fourier rank, but the exact-rank mismatch noted above is retained.

Lift every saved weight and diagonal scale to its ordinary integer representative. All cycle inverse denominators and every nonzero scale remain units at the selected prime because their modular values were checked. Therefore the rational Green branches and their aggregate operators are defined in characteristic zero. The root4096 defines a valid specialization of Z[zeta8], since it satisfies Phi8 and has order8. If a recorded minor or the pencil determinant vanished over Q(zeta8), its good reduction would vanish. The nonzero reductions therefore certify a corresponding complex full-spark, phase-incompatible four-Green network. This is a nonvanishing lift, not a lift of arbitrary finite-field solutions.

For the fixed wiring, the nonzero determinant numerator is a nonzero polynomial in parameters. Fourier-compatible parameters lie on its proper algebraic zero set within the admissible domain, so they have measure zero under a distribution with a density in the full complex parameter coordinates. This says nothing about deliberately designed points on the exceptional locus. For the fixed A,B, finitely many minor polynomials in D are simultaneously nonzero on a nonempty Zariski-open set because the saved D witnesses it; det K0 independently rejects every invertible D for the stated Fourier ordering.

## Generic diagonal rank

For formal independent t_i, Cauchy–Binet expresses each minor of A diag(t) B as a sum of distinct squarefree monomials. Its nonzero coefficients are products of matching A and B minors. Thus generic rank equals the maximum size of a set simultaneously independent among A's columns and B's rows. The classical Edmonds matroid-intersection min–max theorem gives min_S(rank A[:,S^c]+rank B[S,:]); see the precise statement in the primary [MIT combinatorial optimization lecture notes](https://ocw.mit.edu/courses/18-997-topics-in-combinatorial-optimization-spring-2004/e987389ab7a39eac57490805adcec8bc_co_lec11.pdf).

The formal rational-function identity actually works over any base field; an infinite field ensures a nonempty finite intersection of such open sets has suitable rational points. Finite-field success probabilities require explicit degree/field-size accounting, as the source says. Optimized capacity bounds describe the generic attainable rank, not Fourier-specific coefficient equality. The source's random stress samples provide no universal probability theorem.

## Independent controls and replay

Fresh standard-library code verifies all four branches, A,B, both determinant computations, all square minors, all225 coset capacities and Fourier ranks, eight exhaustive 256-interface min–max comparisons, hidden nontrivial middle/output-gauge positives at N4,8,16, and the singular-K0 false-accept control. It includes the concrete exact-rank-profile rejection omitted from a broad reading of the source's stop-rule language.

Replay reads only two JSON files as inert parameter/certificate data and executes only our own checker. No uploaded implementation is imported. The report preserves all previous seals and makes no claim that these finite controls establish a new asymptotic algorithm.
