# ALG-049: nonuniform-cycle support exclusion after the fixed N=8 prefix

Date: 16 October 2026. Author candidate; independent review is required before application.

## Result and precise disposition

For the already accepted eight-dimensional prefix T below, every sign pair and every unit phase z, neither T* T nor its inverse can have a zero off-diagonal entry in every row. Each has a specified row whose seven off-diagonal entries are uniformly nonzero.

Consequently, T S C cannot be a nonzero scalar-unitary matrix if:

- S is any invertible monomial matrix, including nonunitary diagonal amplitudes;
- Q is any weighted directed eight-cycle in any coordinate order, without an equal-modulus assumption; and
- either C=h(Q) or C^-1=h(Q), where h has exponent support E contained in {0,...,7} and E−E is a proper subset of Z/8Z.

Invertibility of C is required for the inverse-polynomial branch; singular C in the direct branch already fails by rank. The cycle weights can be arbitrary complex values, including zero for the degenerate supported-cycle extension. No inverse of Q is used.

This covers every degree-at-most-three polynomial h and every polynomial with at most three nonzero coefficients after reduction to these eight residues. It includes arbitrary nonuniform shifted-cycle factors aI−Q and their inverses when defined. This is a new bounded exclusion relative to the recorded ALG-049 frontier, using off-diagonal support rather than the previously accepted constant inverse-Gram diagonal. It is not a historical novelty claim. The new class complements, rather than subsumes, the previous all-degree uniform-modulus rational-cycle class.

Only this explicitly selected subgate is resolved by the candidate proof. ALG-049 remains TO RESEARCH at priority 42; the 87 closed / 240 open / 327-view census is unchanged. General nonuniform rational functions, longer changing-cycle words, a changed first boundary or prefix, general separators, and complete Fourier synthesis remain unresolved.

## 1. Source-bound prefix

The current repository index at commit 2e57c6f739cb676b81a698736b1dc4baa00865ae identifies ALG-049 at Research overview row 61, Catalogue row 83, and novelity breakthough row 44. Its current gate expressly permits a distinct nonconstant inverse-Gram-diagonal final-factor direction. The native rows were reread for this candidate; no external writes were made.

The accepted source is [the 13 October independent rational-cycle review](https://github.com/AgentSlop-Si/research/blob/2e57c6f739cb676b81a698736b1dc4baa00865ae/math/reviewed_rounds/2026-10-13-reviewed-1820/alg049/INDEPENDENT_REVIEW.txt), 16,521 bytes, SHA-256 61c4898f0596509a48e8c18a06c73c9c5e3c8d88eb17367e4c6ae87a902ed74c. Its source candidate proof has SHA-256 a5b888fd82b0b584011edcc782770eb7229eb3e97030010bbe49e9672697bdec. Both were read. No historical program was executed or imported.

Use the column convention Q e_order[j] = w_j e_order[(j+1) mod 8]. The fixed cycles are:

- M1: order (0,1,2,3,4,5,6,7), weights (1,1,1,1,1,1,1,−1).
- M2(z): order (0,1,3,4,5,6,2,7), weights (z,1,1,1,1,1,z^-1,−1), with |z|=1.

Set K(M)=(2I−M)(I−M)^-1, including its numerator, and T=K(M1)^e1 K(M2(z))^e2 for e1,e2 in {−1,+1}. There is no separator between these two factors. Both cycles satisfy Mj^8=−I, so all prefix inverses exist. In particular det(I−Mj)=2 and det(2I−Mj)=257. Define L=T* T and L^-1=T^-1 T^-*. The order in the latter identity matters.

The all-dimensional support lemma in section 3 is not an all-dimensional prefix theorem. The obstruction here is N=8 only.

## 2. Exact dense-row certificates

ROW_CERTIFICATES.json supplies every upper-triangle Laurent entry used below, the row it certifies, and a positive absolute lower bound for that entry. These are identities in Q[z,z^-1], with conjugation z-bar=z^-1 on the unit circle. There are exactly eight rows, seven edges per row, and 56 identity/bound records.

For each sign pair, a dense row and a common lower bound delta on all seven of its off-diagonal entries are:

| Signs | L row | delta for L | L^-1 row | delta for L^-1 |
| --- | ---: | --- | ---: | --- |
| −− | 1 | 172/16974593 | 0 | 3/2 |
| −+ | 2 | 27/257 | 2 | 5544/66049 |
| +− | 1 | 2940/66049 | 3 | 16/257 |
| ++ | 0 | 1/2 | 0 | 37632/16974593 |

Indices are zero-based. Except for one entry, the certified inequality is the reverse triangle inequality: for f(z)=sum a_k z^k and |z|=1,

|f(z)| >= max_k |a_k| − sum of the other |a_k|.

The certificate's right side is strictly positive for 55 entries. The remaining entry, for signs −+ in L at (2,3), is

L_23 = (−27z + 55 + 28z^-1)/514.

Its real part is (55+Re(z))/514 >= 54/514 = 27/257, so its absolute value has the asserted positive lower bound. Using only coefficient dominance here would incorrectly yield zero; the separate real-part argument is essential.

As a short illustration, for signs ++ the seven entries in row zero are:

(13z+51)/(4z), (2z−13)/(2z), (z+22)/(2z), (25−3z)/(4z), (2−3z)/(2z), (−7z−17)/(4z), (−6z²−61z+3)/(4z).

Their reverse-triangle bounds are 19/2, 11/2, 21/2, 11/2, 1/2, 5/2, and 13. The full certificate gives similarly explicit entries for the other seven rows. The executable checker builds M1 and M2 from their edge data, computes the true K factors and inverses, and verifies every identity and bound. Finite phase samples are not being extrapolated to a continuum theorem.

## 3. General support lemma

Let Q be a weighted directed N-cycle on a specified ordering, and let pos(i) be the position of coordinate i in that ordering. Weights need not be nonzero or have common modulus. For any k>=0, Q^k has support only at (i,j) with pos(i)−pos(j)=k modulo N. Zero weights can delete such entries; they cannot add others.

Let h(Q)=sum_(k in E) a_k Q^k for E contained in {0,...,N−1}, and let D=E−E modulo N. Both h(Q)*h(Q) and h(Q)h(Q)* have support only at pairs satisfying pos(i)−pos(j) in D.

Indeed, an entry of h*h can be nonzero only if some row coordinate l belongs to the supports of columns i and j. Their two cyclic offsets belong to E, so their difference belongs to D. For hh*, use a shared column instead. This is only a necessary support condition: coefficient cancellation can create additional zeros.

If E is nonempty and D is proper, choose d outside D. Since 0 belongs to D, d is nonzero. For each coordinate i there is a distinct j at displacement d, and both Gram entries (i,j) vanish. Thus each Gram has at least one zero off the diagonal in every row. The empty polynomial is singular and separately incapable of completion.

For N=8 and deg h<=3, D is contained in {0,±1,±2,±3}, omitting 4. For |E|<=3, D has at most 1+3·2=7 elements, so it is proper. A shifted exponent interval with four consecutive residues also qualifies. These are sufficient grammar conditions, not claims that every other polynomial can work.

## 4. Congruence obstruction, with the nonunitary separator order

Let S be any invertible monomial, let C be invertible, and set B=TSC. If B*B=cI with c>0, then

L = c S^-* (C^-1)* C^-1 S^-1,

and, on inverting,

L^-1 = c^-1 S C C* S*.

These are invertible congruences; they do not assume commutativity or S unitary. The first identity is NOT L=c S H S* unless S is unitary.

Congruence by an invertible monomial permutes the zero pattern of off-diagonal entries and multiplies surviving entries by nonzero scalars. Therefore the property “every row has some zero off-diagonal entry” is invariant under either displayed monomial congruence.

If C^-1=h(Q), section 3 forces that property on (C^-1)* C^-1, contradicting the dense row of L in section 2. If C=h(Q), it forces the property on C C*, contradicting the dense row of L^-1. This proves the stated theorem. Singular C gives rank(B)<8 and cannot satisfy the nonzero scalar-unitary target either.

An overall nonzero scalar and arbitrary unitary factors at the two outside endpoints preserve scalar unitarity and hence preserve this exclusion. No new separator is inserted between M1 and M2.

### A guarded quantitative version

For the inverse-polynomial branch, let delta be the stated L-row bound, let E_B=B*B−cI for any real c, and put X=C^-1 S^-1. Then

X* E_B X = L − c S^-* (C^-1)* C^-1 S^-1.

Some off-diagonal location in the certified dense row is a forced zero of the second term, and so the right side has an entry of absolute value at least delta. Consequently

||E_B||_2 >= delta / ||C^-1 S^-1||_2²,
||E_B||_F >= sqrt(2) delta / ||C^-1 S^-1||_2².

The Frobenius bound uses the two conjugate off-diagonal entries. These are parameter-dependent inequalities, not uniform conditioning or finite-word guarantees. No analogous bound for the direct Gram is silently inferred from an inverse-Gram estimate in the direct-polynomial branch.

## 5. Boundary controls and remaining gates

The new class can genuinely have nonconstant inverse-Gram diagonal: choose ordinary-order Q with weights (2,1/2,1,1,1,1,1,−1) and C=(I−Q)^-1. Then C^-1=I−Q is in the new class, and its Gram diagonal contains 1+|w_j|², which is not constant. The old constant-diagonal theorem alone does not cover this case.

Full difference support is a substantive boundary. With the unweighted eight-cycle P, h=I+P+P²+P³+P⁴ is invertible and h*h has every off-diagonal entry in row zero nonzero. The support lemma supplies no missing edge. This is a countercontrol to extending the support test, not a successful completion of the ALG-049 prefix.

An arbitrary invertible separator is outside the result: C=I and S=T^-1 give TSC=I, with S generally nonmonomial. The older arbitrary-unitary-separator counterexample for the broader rational-cycle class remains separate and unchanged. No assertion about all arbitrary-unitary separators in this new deficient-support class is made.

The result does not settle arbitrary nonuniform Möbius K(Q), because its polynomial residue and that of its inverse can have full cyclic difference support. Nor does it settle all polynomial degrees >=4, arbitrary rational functions, unrelated products of cycles, nonmonomial separators, changes to the first boundary, other dimensions, historical priority, Fourier circuit complexity, or practical speed. A dense or sparse matrix support condition is not an arithmetic circuit lower bound.

The supplied prefix and candidate factors require their own paid preparation, routing and application costs in any algorithmic use. This proof asserts an algebraic impossibility for the stated class; it does not assert a cheap Fourier construction or any operation-count advantage.

## 6. Reproducibility and candidate limits

Run Python 3 with installed SymPy:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 timeout 300 python check_nonuniform.py

The checker is freshly authored. It reconstructs the prefix; validates all 56 Laurent identities and continuum bounds; verifies both Gram orientations; checks all 256 exponent-support masks in two distinct cycle orders with nonuniform integer weights, both Gram directions and all forced zeros; checks zero-weight support; and exercises nonunitary-monomial congruence, nonconstant diagonal, full-difference, arbitrary-separator and singular-factor boundary controls. Eleven deliberately corrupted certificate variants must be rejected. CHECK_RESULTS.json records the actual run and check counts.

The resource limits are 240 CPU seconds, 2 GiB address space and a 300-second external wall cap, with one BLAS/OMP thread. These finite checks support the displayed proof; they do not replace its universal support argument. No historical source code, network operation, package installation, GitHub write or Sheet write occurs in the checker. Author verification is not independent acceptance.
