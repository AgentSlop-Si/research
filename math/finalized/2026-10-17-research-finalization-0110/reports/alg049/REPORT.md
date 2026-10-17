# ALG-049: arbitrary nonuniform Möbius final factors are excluded by a cut-rank obstruction

17 October 2026 UTC. New bounded result; candidate for independent acceptance.

## Result and disposition

For the unchanged accepted N=8 prefix T defined below, every sign pair and every unit phase z, the matrix T S C is not a nonzero scalar multiple of a unitary matrix whenever:

- S is any invertible monomial matrix, including arbitrary nonunitary diagonal amplitudes;
- Q is a weighted directed eight-cycle in any coordinate order, with arbitrary complex nonzero edge weights; and
- C=(aI+bQ)(cI+dQ)^-1 for arbitrary complex a,b,c,d, with cI+dQ invertible.

If the numerator is singular, the conclusion follows immediately by rank. Otherwise both numerator and denominator are invertible and the proof below applies. The same conclusion holds in the degenerate cycle-supported extension with some zero edge weights. No inverses of Q are taken unless Q is known to be invertible. The class is closed under inversion when C is invertible.

This resolves a specifically recorded residual beyond the earlier deficient-difference-support theorem: arbitrary nonuniform Möbius factors, including K(Q) and K(Q)^-1, whose reduced polynomial representations can have all eight coefficients nonzero. It is not an assertion of historical novelty.

ALG-049 remains TO RESEARCH, priority 42. General nonuniform rational functions of higher numerator/denominator degree, changed first boundary or prefix, nonmonomial separators, other dimensions, and longer changing-cycle words remain open. No parent record, alias or activity is archived, and no score or proof/novelty classification changes.

## 1. Current source binding and unchanged prefix

The actual native table was read on 17 October 2026: ALG-049 is Research overview row 61, Catalogue row 83, and novelity breakthough row 44. The current action/stop text accepts the 16 October deficient-difference-support result and explicitly leaves arbitrary nonuniform Möbius/rational factors open. The repository branch read returned commit d844509088e022fc48d4f02ca378022a9ce67702. Both the predecessor report and its independent acceptance were fetched at that immutable commit:

- [Predecessor report](https://github.com/AgentSlop-Si/research/blob/d844509088e022fc48d4f02ca378022a9ce67702/math/finalized/2026-10-16-research-finalization-2101/alg049/REPORT.md)
- [Predecessor independent acceptance, section 5](https://github.com/AgentSlop-Si/research/blob/d844509088e022fc48d4f02ca378022a9ce67702/math/finalized/2026-10-16-research-finalization-2101/independent_review/INDEPENDENT_REVIEW.md)

Use the column convention Q e_order[j]=w_j e_order[(j+1) mod 8]. The fixed prefix cycles are:

- M1: order (0,1,2,3,4,5,6,7), weights (1,1,1,1,1,1,1,-1).
- M2(z): order (0,1,3,4,5,6,2,7), weights (z,1,1,1,1,1,z^-1,-1), with |z|=1.

Define K(M)=(2I-M)(I-M)^-1 and T=K(M1)^e K(M2(z))^f, where e,f belong to {-1,+1}. There is no separator at the first boundary. Both Mj^8=-I; det(I-Mj)=2 and det(2I-Mj)=257, so all prefix inverses exist. Write L=T* T. The a,b,c,d parameters of the final factor do not modify this prefix.

## 2. New fixed-prefix certificate: separating balanced cuts have rank at least three

Let A be any four-element subset of {0,...,7} that contains 0 and excludes 1, and let B be its complement. There are exactly binomial(6,3)=20 such cuts. For each of the four sign pairs and every |z|=1,

    rank L[A,B] >= 3.                                      (1)

CUT_CERTIFICATES.json gives a finite exact algebraic proof of all 80 statements. With the formal involution z* = z^-1, each L is a matrix over Q[z,z^-1]. Define G=d z^2 L, using the positive denominator d recorded per sign pair:

- signs (-,-): d=16974593=257^3;
- signs (-,+): d=514=2*257;
- signs (+,-): d=132098=2*257^2;
- signs (+,+): d=4.

For each cut, the certificate supplies two nonzero 3-by-3 minors det G[R,C], their exact z-adic valuations v, and their normalized monic polynomials p(z)=monic(z^-v det G[R,C]). It also supplies rational-coefficient polynomials u1,u2 satisfying the exact identity

    u1(z) p1(z) + u2(z) p2(z) = 1.                         (2)

The two minors therefore cannot vanish simultaneously at any nonzero complex z. Since d z^2 and the removed z powers are nonzero there, (1) follows. Only on |z|=1 is this formal Laurent L asserted to equal the Hermitian Gram of the physical prefix. The algebraic certificate is stronger than the required unit-circle statement; no finite phase sample is extrapolated to a continuum result.

There are exactly 160 stored minor identities and 80 Bézout identities, two active terms per cut. Earlier construction-only zero-weight terms were removed before final verification. Each normalized minor is reconstructed from the actual prefix in the fresh checker, so an abstract gcd claim is not substituted for source binding.

The restriction to separating cuts matters. At z=1 for the mixed signs (-,+), the unseparated cut A={0,1,2,7}, B={3,4,5,6} has rank two. We do not claim that all 35 unordered balanced cuts have rank at least three.

## 3. Möbius-cycle cut-rank lemma

Let Q be a weighted directed N-cycle, permitting zero weights in the supported-cycle extension. Let A be any nonempty proper contiguous interval of its cycle order and B its complement. Each of Q[A,B] and Q[B,A] has rank at most one: exactly one directed cycle edge can cross each way, and a zero weight can remove it.

Suppose N0=aI+bQ is invertible and put F=(cI+dQ)N0^-1. Then

    rank F[A,B] <= 1,       rank F[B,A] <= 1.              (3)

The following cases cover all coefficients without a hidden nonzero assumption.

1. b=0. Invertibility forces a!=0. Then F=(c/a)I+(d/a)Q, so (3) follows from the crossing-edge observation.
2. b!=0 and a!=0. The blocks Q[A,A] and Q[B,B] are weighted directed paths and hence nilpotent. Thus N0[A,A] and N0[B,B] are invertible. In the block inverse formula,

       N0^-1[A,B] = -N0[A,A]^-1 N0[A,B] Schur_B^-1.

   The Schur complement is invertible because N0 is, and the cross factor N0[A,B]=bQ[A,B] has rank at most one. The reverse cross block has the same bound, using the other block formula. Since

       F = (d/b)I + (c-ad/b)N0^-1,

   (3) follows, including the constant-function case c-ad/b=0.
3. b!=0 and a=0. Now N0=bQ invertible forces Q invertible. The inverse Q^-1 is supported on the reverse weighted cycle, and

       F = (d/b)I + (c/b)Q^-1.

   Each cross block again has rank at most one.
4. a=b=0 is incompatible with invertible N0 and is already the singular-numerator case in the theorem.

Consequently H=F*F obeys

    H[A,B] = F[A,A]* F[A,B] + F[B,A]* F[B,B],
    rank H[A,B] <= 2.                                    (4)

This is valid for every contiguous cycle cut, without a common-modulus, total-cycle-product, positivity, normality or unitarity assumption. It is an algebraic cut-rank bound, not a circuit-complexity bound.

## 4. Every cycle supplies a suitable cut; monomial congruence preserves its rank

In any cyclic order of eight distinct coordinates and for any two distinct marked coordinates x,y, there is a contiguous four-element interval containing x and excluding y. The four length-four windows containing x have intersection {x}; therefore y cannot lie in all four.

Suppose, contrary to the theorem, B0=T S C satisfies B0*B0=tI for some t>0. The numerator must be invertible; put F=C^-1. Then

    L = t S^-* F* F S^-1.                               (5)

An invertible monomial consists of a permutation and a nonsingular diagonal matrix. Under its congruence, every cut block is obtained from the corresponding permuted cut block by invertible diagonal row and column scaling, so its rank is unchanged. Transport the Q cycle order through this permutation. The preceding window argument supplies a contiguous 4+4 cut of that transported order containing coordinate 0 and excluding coordinate 1. By (3)-(5), its block of L has rank at most two. By (1), the same block has rank at least three. Contradiction.

The transpose/adjoint order in (5) matters, especially for nonunitary monomial amplitudes. No unitarity of S, commutativity with T, or inserted first-boundary separator is assumed.

As in the predecessor, overall nonzero scalar factors and arbitrary unitary outside-endpoint factors preserve scalar unitarity and hence do not evade the obstruction. These endpoint factors are not interior separators.

## 5. Strict extension and explicit boundary controls

Take the ordinary-order weighted cycle Q with weights (2,1/2,1,1,1,1,1,-1), so Q^8=-I. Let C=K(Q). Then

    C = (3I+Q+Q^2+...+Q^7)/2,
    C^-1 = (129I-64Q-32Q^2-16Q^3-8Q^4-4Q^5-2Q^6-Q^7)/257.

Both reduced polynomial supports are all of Z/8Z; the earlier missing-residue test does not apply. The diagonal of (C^-1)*C^-1 is nonconstant; the earlier constant-inverse-Gram-diagonal test also does not apply. The fresh exact control checks these properties. The new theorem does apply, including with arbitrary invertible monomial S. Thus the result is not a repeat of either accepted mechanism.

The rank-one cross-block lemma cannot be extended without a degree guard. For an ordinary unweighted eight-cycle P, take F=I+2P^2. It is invertible, and

    F*F = 5I+2(P^2+P^-2)

has a rank-four block across {0,1,2,3}|{4,5,6,7}. This is a countercontrol to a universal Möbius-style rank cap, not a successful completion of the fixed prefix. Some higher-degree factors are already excluded by earlier results; that fact does not make the present lemma valid for them.

The nonmonomial-separator boundary is substantive: C=I and S=T^-1 give TSC=I, and the exact z=1 control verifies that this S is nonmonomial. No arbitrary-separator theorem is claimed.

## 6. Residual gate and cost scope

The next potentially different final-factor scope must leave the combined accepted classes: uniform-modulus rational factors at their earlier separator scope, deficient-difference-support polynomial/inverse-polynomial factors, and the arbitrary nonuniform Möbius class proved here. General higher-degree nonuniform rational functions remain a concrete residual; their cycle cut ranks may exceed two. No particular higher-degree constructor is accepted or promised here.

Changing the first boundary/prefix, nonmonomial separators, other N, and longer changing-cycle words are separate open scopes. No exact Fourier construction, global Fourier/FFT lower bound, practical speed claim, numerical executor, uniform conditioning estimate or historical priority follows. Any algorithmic use must separately pay factor representation, parameter preparation, routing and application. The finite certificate-checking resource budget is not an algorithmic complexity bound for a Fourier procedure.

## 7. Fresh verification and publication boundary

Run Python 3 with installed SymPy:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 timeout 300 python check_mobius.py

The checker was freshly authored for this task and uses direct symbolic inverses to reconstruct the fixed prefix. It validates all 160 normalized minor identities and 80 Bézout identities; all 5,040 cyclic orders up to rotation for the separating-window control; nonuniform, complex and zero-weight Möbius examples with coefficient-degenerate and singular cases; the full-support/nonconstant-diagonal strict-extension control; the higher-degree and unseparated-cut countercontrols; the nonmonomial separator boundary; and five deliberately corrupted certificate variants that must be rejected.

The checker reads only the formal certificate file; it executes or imports no historical program. It makes no network request or external write. Limits are 240 CPU seconds, 2 GiB address space, 300 seconds external wall time, and single-threaded BLAS/OMP. CHECK_RESULTS.json records the actual fresh run. Author verification is not independent acceptance. Only the safe report, source register, certificate, fresh checker, result, disposition and manifest are intended for publication; native reads and exact-cell preimages remain private to the application workflow.
