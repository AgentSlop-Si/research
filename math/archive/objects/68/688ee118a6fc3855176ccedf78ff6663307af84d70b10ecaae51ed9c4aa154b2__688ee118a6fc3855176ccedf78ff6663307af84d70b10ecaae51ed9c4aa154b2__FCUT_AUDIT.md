# Independent FCUT sparse-sandwich audit

9 October 2026 UTC. Source: [private-id], FFT_FCUT_THEORY_AND_VERIFIER_2026-10-10.zip, version 0, 9,267 bytes, SHA-256 e34381edd1cb90d0a322514baadf5198e26d92d312c4e05818ccbcb6e06e761b. The two contained source files were safely extracted and preserved. No uploaded verifier was run or imported.

## Accepted result and genuinely additional content

The cycle-propagation proof and its quantitative entry-density theorem are sound. For prime p>=3, arbitrary Hamiltonian cycles alpha,beta, arbitrary complex diagonal edge weights, and invertible monomial endpoint factors, the sandwich

C=(I−D_a P_alpha) L^{-1} F_p R^{-1}(I−D_b P_beta)

satisfies every adjacent-alpha row-pair union bound

|supp(C_i) union supp(C_alpha(i))| >= ceil(p/2),

and consequently nnz(C)>=ceil(p*ceil(p/2)/2). A and B need not be invertible for this density statement; zero coefficients and singular denominator choices are retained.

This is a quantitative nonzero-count result for the intermediate matrix. It does not show that its application takes quadratic work, because a dense center might have a compact fast evaluator. It supplies no arbitrary-input faster Fourier algorithm, numerical-stability certificate or unrestricted arithmetic lower bound.

The prime p>=11 two-resolvent no-go consequence overlaps the already verified additive separator plus prime full-spark argument and v17's sparse zero-rectangle proof. The prior additive/v17 result permits termwise independent diagonal gauges and several permutation cycles, which this particular FCUT theorem does not claim. The quantitative sandwich-density estimate is the useful additional statement.

## Independent proof review

For a two-row restriction of H whose every three-column submatrix has rank two, write C=HB with B=I−D_b P_beta. At a destination j=beta(k) outside the union of the two row supports of C, the two-vector H[:,j] equals b_k H[:,k]. Delete the incoming edge at each marked destination. With m>0 marks, a single directed Hamiltonian cycle splits into exactly m directed paths covering all N vertices. Along each path, every two-vector is a scalar multiple of its first one, even if an edge weight is zero. Thus each path's restriction has rank at most one and cannot have three vertices. It follows that m>=ceil(N/2).

When m=0, the same propagation holds around the entire cycle, forcing rank at most one on all columns, again a contradiction. No division by edge weights is needed. The analogous q-column premise gives path length at most q−1 and the stated ceil(N/(q−1)) bound.

For adjacent rows i,alpha(i) of A=I−D_a P_alpha, the coefficient matrix on the distinct labels i,alpha(i),alpha²(i) is [[1,−a_i,0],[0,1,−a_alpha(i)]], which always has rank two. An invertible monomial L^{-1} preserves its rank and moves/rescales its three candidate coordinates. Every resulting three-column Fourier restriction is invertible at prime length by Chebotarev. Right monomial factors preserve this property. Thus the propagation premise holds for every adjacent-alpha pair. Summing pairwise support-cardinality inequalities counts every row twice and proves the density formula, including the exact ceiling.

For the no-go corollary, the two adjacent rows of A+B have support union contained in five coordinates. For prime p>=11, ceil(p/2)>=6, contradicting the density theorem. This is sound but not a new growing-size architecture exclusion relative to the previously approved results.

## Composite-length scope

If the three moved Fourier frequency labels form an arithmetic progression with step coprime to N, their restriction to any three distinct columns is a Vandermonde matrix on distinct nodes. The local pair-support theorem therefore holds at composite lengths too. A unit-step affine cycle and affine endpoint permutation with coprime slopes guarantee this at every adjacent pair, yielding the same global density bound.

Arbitrary non-affine cycles and arbitrary non-affine left endpoint reordering at composite N are not covered without checking the local full-spark profile. Arbitrary invertible right monomial transformations are harmless because they only select and scale distinct column nodes. The proof uses complex roots; it does not infer a universal finite-field full-spark theorem.

## Explicit p=11 certificate

The stated alpha and beta arrays are Hamiltonian cycles. At i=0, the candidate A+B support union is {0,2,4,5,9}. Cutting the incoming beta edges at these marks gives paths [0], [2], [4,3], [5,6,7,10], [9,1,8]. Their sizes are 1,1,2,4,3 as claimed.

For frequencies [0,2,9] and columns [5,6,7], independent six-term determinant expansion gives

−2z²+z⁴−z⁷+2z⁹ modulo z¹¹−1.

This polynomial has degree 9, not the source prose's literal “degree-10 polynomial”; the intended statement is degree at most 10. It is not a multiple of 1+z+...+z¹⁰, hence is nonzero at a primitive eleventh root. This minor wording correction does not affect the certificate.

## Independent exact controls

The reviewer-authored checker performs exact arithmetic in cyclotomic quotients, independently constructing cyclotomic polynomials by exact division rather than using modular-root nonvanishing as a proxy. It verifies:

- 72 exact prime-length sandwich support counts at p=3,5,7,11,13,17, with arbitrary endpoint permutations, signed nonzero endpoint scales, zero-weight controls and all-one singular-denominator controls;
- 10 exact composite-length sandwich controls at N=12,16,24,32,64,128 in the primitive-stride scope;
- 132 coprime-stride node profiles;
- the explicit p=11 path partition and determinant coefficients.

All pass. The uploaded verifier's larger enumerations are source-reported evidence, not rerun results. INDEPENDENT_RESULTS.json and INDEPENDENT_RUN.log record the independently executed controls.

The classical full-spark theorem was separately checked in Tao's primary paper, Lemma 1.3, https://arxiv.org/pdf/math/0308286 . The rank/propagation synthesis is reviewed here without a publication-novelty claim. Bounded additive Green banks are already constrained by the general separator; merely increasing a fixed additive term count is not an unchecked asymptotic escape. Products of sums and genuinely fast dense centers remain separate questions.
