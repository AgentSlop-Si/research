# Independent review of two Weyl line Fourier factorizations

## Result

Accepted for odd prime length and the stated ordered line-operator model. The dephased coefficient tensor has rank one exactly for the compatible direction pairs and rank N otherwise. Every successful two-factor product has at least one factor diagonally and permutation-equivalent to the full Fourier matrix. These identities supply no faster transform.

Two independent strengthenings are included. First, the local rational representation satisfies the stronger degree condition deg(q)+deg(p)>=N-1, rather than only the source's half-size recurrence bound. Second, adding more factors whose line coefficients remain full quadratic chirps does not remove the exposed Fourier-equivalent-factor issue. Both statements are restricted representation results, not general arithmetic lower bounds.

Source SHA256: e1d30f08aa720c4e492a0e268b343d08d52bd80ecb126ab3fbe6c27097f36906. The nested predecessor exactly matches the reviewed v21 archive, SHA256 d23a528d5beed5ba2d1635fab3b54ae0c572f9527fd892cdc7ee7a4a7cfe6f59. Its one-line and generic-parameter results remain unchanged. Uploaded scripts and bytecode were never executed or imported. The supplied mathematical claims retain source attribution; no publication-priority claim is made.

## Convention and scalar guards

Let N be an odd prime, omega a primitive Nth root, X e_j=e_(j+1), Z e_j=omega^j e_j, and F[i,j]=omega^(ij), unnormalized with positive sign. Use symmetric Weyl operators

    D_(a,b)=omega^(ab/2) X^a Z^b.

Fractions in exponents denote inverses in Z_N. With sigma(u,v)=bc-ad for u=(a,b), v=(c,d), direct multiplication gives

    D_u D_v=omega^(sigma(u,v)/2)D_(u+v).

The order is important: AB applies B first. Reversing u and v changes the compatibility condition. Over C the Weyl basis is Hilbert-Schmidt orthogonal. In a finite field the corresponding precise statement is the nondegenerate trace pairing Tr(D_-u D_v)=N delta_(u,v). The source's field controls require characteristic not dividing 2N, a primitive Nth root and a nonzero Gauss constant; the checker verifies these guards.

## Fourier Weyl coefficients

The coefficient at (a,b) is N^-1 Tr(D_(-a,-b) F). Expanding the trace gives

    N^-1 sum_j omega^(j^2+(a-b)j-ab/2)
       = gamma omega^(-(a^2+b^2)/4),
    gamma=N^-1 sum_j omega^(j^2).

Completing the square produces the displayed phase, including its sign. Over C the nondegenerate Gauss sum has magnitude sqrt(N), so gamma is nonzero. Thus

    F=gamma sum_(a,b) omega^(-(a^2+b^2)/4)D_(a,b).

The independent checker verifies every Weyl coefficient, including (0,0), by the trace formula and reconstructs every Fourier entry. It also verifies the multiplication cocycle using actual matrix products for every independent tested small ordered pair.

## Exact tensor rank and classification

Choose independent nonzero directions u and v, so det(u,v)=ad-bc!=0 modulo N. For arbitrary line operators A=sum_m alpha_m D_(mu) and B=sum_n beta_n D_(nv), the map (m,n)->mu+nv is bijective, and the coefficient of AB there is alpha_m beta_n omega^(sigma mn/2).

Removing this cocycle from the Fourier symbol gives

    T_(m,n)=gamma omega^(-||u||^2 m^2/4)
                     omega^(-||v||^2 n^2/4)
                     omega^(-kappa mn/2),
    kappa=u dot v+sigma(u,v).

The first two factors are invertible diagonal scalings. The final matrix is all ones if kappa=0 and a row-permuted Fourier matrix otherwise. Its rank is exactly one or N, with no intermediate case. The coefficient map is an isomorphism, so the minimum number of products on this same fixed ordered pair is exactly that tensor rank: a rank decomposition also constructs the required sum of line products. This is a product-count statement, not an operation count.

For nonzero u=(a,b), kappa=0 means (a+b)c+(b-a)d=0. Its solutions are

    v=t(a-b,a+b), t!=0.

The determinant is t(a^2+b^2), so independence is equivalent to ||u||^2!=0. The partner norm is 2t^2||u||^2, also nonzero. A compatible independent ordered pair becomes incompatible when reversed, since then kappa changes to -2 sigma!=0.

For a compatible pair the tensor entries are all nonzero and rank one. Its outer-product factorization is unique up to a nonzero reciprocal scalar. Define

    L_u=sum_m omega^(-||u||^2 m^2/4)D_(mu).

Then F=L_u (gamma L_v), and every successful pair of line factors is this one up to reciprocal scaling. Rescaling a direction by t!=0 merely reindexes the sum, so L_(tu)=L_u.

The source's 480 independent and 64 compatible pairs at N5, and 2016 independent and 288 compatible pairs at N7, are correct counts of ordered nonzero direction vectors. They count each ordered projective line pair (N-1)^2 times. The geometric line-pair counts are respectively 30 total with 4 compatible, and 56 total with 8 compatible. This is a terminology clarification, not a discrepancy in the enumerated data.

## Exact factor equivalence

If a=0 and b!=0, changing variable z=bm/2 in the sum gives the diagonal factor

    L_u[j,j]=G_minus omega^(j^2),
    G_minus=sum_z omega^(-z^2)!=0.

It applies in O(N) scalar work after preparing its phases and scalar.

If a!=0, the unique term reaching (i,j) has m=(i-j)/a, which gives

    L_u[i,j]=omega^(-(a-b)^2 i^2/(4a^2))
             omega^((a^2+b^2)ij/(2a^2))
             omega^(-(a+b)^2 j^2/(4a^2)).

For anisotropic u, the mixed coefficient is nonzero. The middle matrix is exactly F with a permutation of its rows, and both endpoint diagonal phases are invertible. Hence L_u=D_left P F D_right. Conversely F is obtained from L_u by undoing these O(N)-cost operations. This is an exact reduction in both directions, not a claim that F has a proved general arithmetic lower bound.

For isotropic u, the mixed coefficient is zero and L_u is rank one. Such a factor cannot occur in a successful independent pair. Two independent directions cannot both be vertical, so every compatible pair exposes at least one nonvertical anisotropic, Fourier-equivalent factor; if both are nonvertical, both are Fourier-equivalent.

## Stronger local rational degree theorem

The source's recurrence bound is valid, but the exact chirp coefficients give a stronger elementary statement. Let C=D_u, so C^N=I and I,C,...,C^(N-1) are linearly independent. Put Q=||u||^2!=0 and a_r=omega^(-Q r^2/4). Suppose

    L_u=q(C)^-1 p(C),
    deg q=d, deg p=e, q(C) invertible.

For d or e at least N-1 the claimed inequality below is already trivial. Otherwise q is nonzero and q(C)L_u=p(C) identifies cyclic polynomial coefficients. For every r=e+1,...,N-1,

    0=sum_(k=0)^d q_k a_(r-k)
     =a_r sum_(k=0)^d q_k omega^(-Q k^2/4)
                            (omega^(Q r/2))^k.

The second sum is a nonzero polynomial of degree d evaluated at N-1-e distinct points, because omega is primitive and Q/2!=0 modulo prime N. Therefore

    d >= N-1-e,  equivalently deg q+deg p >= N-1.

This works over C and every field with the stated root/unit guards. It avoids relying on a blanket prime-Fourier full-spark claim in finite fields. The source's argument using nonzero prime Fourier minors is a characteristic-zero argument; arbitrary finite-field specializations should not silently inherit that premise.

The new proof requires only a nonzero polynomial q of degree below N for the tail obstruction. The separate q(C) inverse guard is still essential to interpreting the rational representation. Degrees refer to ordinary, canonically represented one-sided polynomials in this specified generator; Laurent supports or other operator families require their own accounting. If p has high degree, the result allows small d, including the direct full chirp polynomial. It does not say every high-degree polynomial is expensive by every possible algorithm.

The checker verifies the tail-constraint matrix has full column rank for every forbidden pair d+e<N-1 at seven prime lengths and three nonzero quadratic coefficients. It also constructs the cyclic inverse with constant numerator: all N inverse coefficients are nonzero, giving the tight degree N-1 case. No source test covers this strengthened theorem; these are new independent controls.

## More full quadratic chirps do not change that particular issue

For the broader full-chirp line factor

    K=sum_m omega^(t m^2+s m)D_(mu),

a nonvertical direction a!=0 gives the exact entry formula

    K[i,j]=omega^((t/a^2+b/(2a))i^2)
           omega^((-2t/a^2)ij)
           omega^((t/a^2-b/(2a))j^2)
           omega^(s(i-j)/a).

If t=0, this matrix has rank one; if t!=0, it is again diagonally and permutation-equivalent to F. In a vertical direction t!=0 gives an invertible diagonal Gauss-chirp operator, while t=0 gives a rank-one diagonal projector. A product equaling invertible F cannot include rank-one factors, and a product of only vertical factors is diagonal. Therefore any number of these full quadratic-chirp line factors still exposes at least one Fourier-equivalent factor under separate evaluation.

This limited extension does not classify three or more arbitrary line operators with general coefficients, sums using varying line pairs, or genuinely shared evaluators. The source's three-line proposal remains a research direction only if it changes the relevant coefficient/evaluation restrictions; merely adding one more full quadratic chirp is insufficient. No general multi-factor no-go is asserted.

## Costs and connection to earlier results

The canonical chirp coefficients and endpoint phases can be generated by updating consecutive ratios in O(N) arithmetic; gamma can be formed by an O(N) Gauss sum. Permutation application costs O(N) indexing work once its modular parameters are fixed. These costs must be counted, but they do not remove the Fourier-equivalent dense factor. Conventional evaluation gives the usual FFT-scale cost, while direct dense or separately scanned full polynomial evaluation is quadratic.

For incompatible pairs, tensor rank N forces N nonzero products. A literal implementation evaluating and accumulating each complete length-N product separately is at least quadratic under that schedule. Tensor rank alone is not an unconditional arithmetic lower bound: a shared evaluator, special projections, reuse or another representation needs a fresh operation ledger. Likewise, high local rational degree rules out a short recurrence of the specified form; it does not exclude unrelated algorithms.

This does not invalidate v21's arbitrary-off-diagonal expressivity or explicit alpha guard, the accepted dyadic N16 eight-order coefficient seed, or the separately studied forced feedback inverses. These are different operator grammars. Nor does the suggested high-treewidth route revive the previously excluded model in which a sparse matrix has an inverse equal to a monomially gauged Fourier matrix; that inverse relation already forces the matrix itself to be dense.

## Primary literature boundary

Finite Weyl/Weil systems and quadratic Gauss sums are established background. [Gurevich, Hadani and Howe](https://arxiv.org/abs/0808.2447) explicitly connect Fourier, the Weyl element and Gauss sums. This supports the background attribution, not a novelty claim for the supplied classification.

The title of [Lopez and Dodin](https://arxiv.org/abs/2012.06028) concerns exactly unitary discrete metaplectic representations, but its abstract describes a linear-time near-identity approximation and convergence under iteration. Exact unitarity is not an exact arbitrary-input O(N) DFT theorem. The source cites it as adjacent work, and this review does not promote it into a missing fast Fourier primitive. The earlier classical chirp-convolution attribution remains as reviewed in v21.

## Independent controls and replay

The standard-library checker recreates all saved ranks and classifications, plus lengths 3 and 19. It checks every Weyl coefficient and full matrix reconstruction; explicit multiplication cocycles and tensor ranks for all independent direction pairs at N3, N5 and N7; every isotropic/anisotropic line matrix through N19; all compatible partners at three nonzero scales per anisotropic direction; and the exact factor entries and reciprocal order restriction. The stronger degree and general quadratic-chirp controls are separate additions.

These are full-entry finite-field corroborations of the written proofs, not a replacement for their guards. Run `python3 independent_checks.py`. PORTABLE_REPLAY.json records isolated replay with byte-identical results. No network or third-party Python dependency is required, and all uploaded programs remain inert.
