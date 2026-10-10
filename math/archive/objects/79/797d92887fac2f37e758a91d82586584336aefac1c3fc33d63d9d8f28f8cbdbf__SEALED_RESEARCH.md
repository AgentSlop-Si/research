# Routed packet fusion: a shared-state boundary and a routing-defect budget

Research date: 10 October 2026 UTC. Status: a bounded constructive attempt, exact scoped obstruction, and independent proof audit. No faster arbitrary-input Fourier transform is constructed. No publication-level novelty claim is made.

## Result first

The inherited cyclotomic identity really merges distinct inverse branches into one linear-work solve. This report extends the algebra to independently monomial-routed endpoints and identifies the obstruction to preserving that sharing:

- If the right routes commute with the shared stride permutation, a bank of r branches has one shared inverse state and a numerator with at most r² nonzeros in each column. For packet gain 0<|a|<1, representing any N-by-N flat unitary requires r² >= N. Arbitrary left endpoint permutations and zero endpoint weights are allowed.
- If all left routes are diagonal and the right route is common, the stronger necessary condition is r >= N.
- If right routes do not commute, let K be the sum of their commutator ranks with the stride permutation. For the Fourier target, exactness requires

      2 r² (K+1)² >= N,

  and, at complex prime order,

      (r²+2)(K+1) >= N+1.

Thus a logarithmic-width cyclotomic packet with only bounded-rank right-routing defects cannot be the missing construction. The conclusion is about this explicit family, not general sums of sparse inverses or general shared arithmetic DAGs. In particular it does not turn the accepted r=Omega(log N) branch theorem into an Omega(Nr) arithmetic theorem.

## 1. Fixed model and conventions

There are N scalar input registers and N explicit scalar outputs. Algebraic statements are over C. A flat unitary U has U*U=I and |U[j,k]|=1/sqrt(N). The normalized Fourier matrix is F[j,k]=omega^(jk)/sqrt(N), with omega a primitive Nth root.

A partial monomial matrix has at most one nonzero in every row and every column. Endpoint weights can vanish. P is any permutation matrix, with P e_j=e_(p(j)); it need not be one cycle. Fix an integer r>=1, a supplied primitive rth root zeta, and 0<|a|<1. Define

    B_i = I-a zeta^i P,       0<=i<r,
    Q = I-a^r P^r,
    H_i = sum_(s=0)^(r-1) (a zeta^i)^s P^s,
    T = sum_(i=0)^(r-1) L_i B_i^(-1) R_i.

All B_i and Q are nonsingular: P is unitary, so their Neumann series converge. Each denominator has at most two nonzeros per column. If r>1 all B_i are distinct. The proof identities are algebraic and remain valid over other fields when roots and all inverses exist; the flat-unitary, norm, and uncertainty conclusions below are specifically complex statements.

The constructive cost model is a sequential scalar algebraic RAM: +, -, multiplication, and legal division each cost one; reading/writing a scalar or O(log N)-bit index costs one. Only explicitly supplied roots and constants are free inputs; generating tables, routes, intermediate values, and N outputs is charged. A permutation is not a zero-cost full-vector operation. Section 7 separately exposes the precision/bit cost of the concrete rational positive control. No finite-precision exact-complex implementation is claimed.

## 2. Inherited mechanism, retained with accurate priority

The finite geometric identity gives

    B_i H_i = I-(a zeta^i P)^r = Q,
    B_i^(-1) = H_i Q^(-1).

For scalar character weights,

    (1/r) sum_i zeta^(-is) B_i^(-1)
      = a^s P^s Q^(-1),        0<=s<r.                 (1)

Every inverse in the sum is generally dense when P is an N-cycle. Formula (1) is genuine shared computation across distinct denominators, not repeated identical branches. It is already explicitly proved in the master corpus's v19 report. It must not be advertised as a new discovery of this pass.

Taking a=1/2, s=0, odd N, and r a power of two gives one dense stride-cycle inverse with bounded condition number, computable in O(N+r+log N+log r) fully charged scalar/index work, instead of separately materializing r dense vectors. For r<=N this is O(N). Each B_i has norm <=3/2 and inverse norm <=2. The fused Q has inverse norm <=1/(1-2^(-r)). This is a counterexample to assigning independent Nr work to arbitrary sums purely from the displayed branch count. It is not a Fourier transform.

## 3. Compatible independent right routes: exact shared-state identity

Assume R_i P^r=P^r R_i for every i. Then R_i commutes with Q and Q^(-1), including when R_i is singular. Therefore

    T = M Q^(-1),
    M = sum_i L_i H_i R_i
      = sum_(i,s) (a zeta^i)^s L_i P^s R_i.           (2)

A product of partial monomial matrices is partial monomial. There are r² summands in the last expression. Consequently every column (and every row) of M has at most min(N,r²) nonzero entries. This counts the whole merged numerator, including cancellations; no genericity is assumed.

Now suppose T=U, where U is flat unitary. Put b=a^r. For every j,k,

    M[j,k]=(UQ)[j,k]=U[j,k]-b U[j,p^r(k)].

The reverse triangle inequality gives

    |M[j,k]| >= (1-|b|)/sqrt(N) > 0.                 (3)

This also holds when p^r(k)=k. All N² entries of M are nonzero. Comparing with (2) proves

    r² >= N.                                         (4)

This proof allows arbitrary P, arbitrary independent left permutations, arbitrary endpoint magnitudes, and zero endpoint weights. The right-route commutation premise is essential.

### Common right route and diagonal left routes

If R_i=R for all i, R commutes with P^r, and every L_i is diagonal, fix an input column k. For each s all matrices L_i P^s R have their possible nonzero in that column at the same output coordinate, independent of i. Thus M has at most r nonzeros per column, and (3) gives r>=N. The common R need only be partial monomial; unitarity is unnecessary. Exact equality with U will of course itself force enough rank.

### Robust version

More generally let M have at most t nonzeros per column and T=M Q^(-1). The N(N-t) missing locations when t<N obey (3) for UQ-M. Since ||Q||_2<=1+|b|,

    ||U-T||_2 >= eta sqrt(max(0,1-t/N)),
    ||U-T||_F/sqrt(N) >= eta sqrt(max(0,1-t/N)),
    eta=(1-|a|^r)/(1+|a|^r).                          (5)

Indeed ||UQ-M||_F² >= (N-t)(1-|b|)², whereas this norm is at most (1+|b|)||U-T||_F and at most sqrt(N)(1+|b|)||U-T||_2. This proof does not assume any bound on the endpoint gains or conditioning of M. For a=1/2 and r tending to infinity with r=o(sqrt(N)), the r²-support compatible family has asymptotic operator error at least 1-o(1). If |a| approaches 1 too rapidly, eta can degenerate; do not assert the same uniform error gap in that regime.

## 4. Arbitrary right routes: the exact correction that sharing leaves behind

No commutation is now assumed. The elementary identity

    Q^(-1) R_i = R_i Q^(-1)
                 + Q^(-1)[R_i,Q]Q^(-1)

has the sign shown, where [R_i,Q]=R_i Q-Q R_i. Inserting it gives

    T = M Q^(-1)+E,                                   (6)
    M = sum_i L_i H_i R_i,
    E = sum_i L_i H_i Q^(-1)[R_i,Q]Q^(-1).

The numerator still has at most r² nonzeros per column. Since a is nonzero,

    rank E <= K := sum_i rank([R_i,P^r]).              (7)

No inverse of L_i or R_i, no Schur complement, and no genericity are used. This is a constructive split: the only algebra discarded by an attempted common-state evaluator is the explicit E. In particular, changing a route and continuing to reuse the old solve without evaluating E is incorrect. Fresh exact negative controls exhibit that failure.

## 5. Sparse-numerator plus low-rank repair lemma

Let U be any flat unitary. Suppose

    U=A Q^(-1)+E,

where Q is nonsingular with at most s nonzeros per column, A has at most t nonzeros per column, and rank E<=k<N. Choose any k+1 coordinates. The restriction of EQ to those columns has a nonzero kernel vector v supported there. Let z=Qv. Then z is nonzero, has support at most s(k+1), and

    Uz=Av

has support at most t(k+1). For any nonzero z and flat unitary U,

    |supp z| |supp Uz| >= N.                          (8)

A one-line proof is |(Uz)_j|<=sqrt(|supp z|/N)||z||_2; square and sum over supp(Uz), using unitarity. It follows that

    s t (k+1)² >= N.                                  (9)

If U is the Fourier matrix of complex prime order N, the established additive uncertainty theorem gives the stronger necessary condition

    (s+t)(k+1) >= N+1.                               (10)

Only (10) uses the prime Fourier theorem. It is not true for arbitrary flat unitaries or arbitrary finite-field reductions. Formula (9) applies to every complex flat unitary.

Applying (9)-(10) to (6), with s=2, t=r², k=K, proves

    2r²(K+1)² >= N,
    (r²+2)(K+1) >= N+1       [prime complex Fourier]. (11)

If K>=N these inequalities already hold trivially; otherwise the preceding kernel proof applies. Thus K>=sqrt(N)/(sqrt(2)r)-1 in general, and K>=(N+1)/(r²+2)-1 at prime order. These are lower bounds on the rank budget required by this family, not on arithmetic operations. Correlated summands may make rank E much smaller than K, which can only strengthen the necessary condition when the actual rank is known.

## 6. What was attempted and exactly what remains constructive

Attempt: use the inherited roots-of-unity bank collapse while retaining independently routed endpoints, hoping to pay for one full solve and cheap routing/aggregation even with r around log N.

Outcome: preserving the stride denominator leaves a sparse numerator that cannot equal Fourier unless r is at least sqrt(N), or N in the common-right/diagonal-left slice. Allowing a bounded-rank commutator repair does not rescue logarithmic r. This is a clean falsification of that particular extension, including arbitrary-input exact equality.

The next constructive obligation is explicit, not a proposed theorem: find a uniformly generated family with genuinely noncommuting right routes for which the correction E in (6), together with M Q^(-1), has an all-output scalar circuit of o(N log N), and prove its exact Fourier identity. For r=O(log N), that E must have growing rank as quantified in (11); it must nevertheless be applied faster than a dense rank-factor implementation. One must give the actual shared intermediate values, coefficient/route generator, and operation ledger. A rank budget, a branch count, or the label "shared DAG" is not such a circuit.

Alternatively one may abandon the common cyclic packet and fuse different denominators directly. That leaves the present family, so none of (4), (5), or (11) automatically applies. The accepted pseudoforest branch-count theorem still supplies only its stated representation constraint.

This report makes no assertion that a dense numerator, high-rank correction, or large K has high unrestricted arithmetic complexity. Fourier and circulant non-rigidity results are an additional reason not to promote these elementary uncertainty bounds into a universal circuit lower bound.

## 7. Complete work and precision accounting for the attempted mechanism

### General routed input description and direct schedules

With explicitly listed endpoints, reading r pairs of monomial routes/weights costs O(Nr) words. Constructing P^r from the cycles of P costs O(N) index operations after reducing r modulo each cycle length. Computing a^r and the r scalar pole values uses O(r+log r) scalar work from supplied a,zeta. Verifying a symbolic uniform route family is a separate construction task; no arbitrary N-by-r table is silently free.

Each first-order cycle solve costs O(N) scalar work and O(N) reads/writes. Hence the separate-branch schedule, including endpoint action and accumulated outputs, costs O(Nr) after O(Nr) ordinary preprocessing. Reusing the one Q solve but explicitly applying the numerator in (2) costs O(Nr²), with O(Nr²) explicit numerator construction/storage if it is compiled entrywise, or O(Nr) endpoint storage and O(N) working registers if its r² summands are streamed. This generic rewrite by itself is not faster. Only further algebraic compression such as inherited (1) removes the numerator work.

For a low-rank E=VW of rank k, a dense stored-factor evaluator costs O(Nk) scalar work per input, O(Nk) stored coefficients, plus actual factor generation. No assumption that every rank-k map must cost Nk is made. The expression (6) can always be evaluated by the original branches at O(Nr); evaluating its correction term separately without a new compression need not improve anything.

### Concrete positive-control implementation

For (1) with s=0, a=1/2, P a natural cycle, and gcd(N,r)=1, prepare a^r, one cycle order, and the closure factor 1/(1-a^(rN)); this costs O(N+r+log N+log r) scalar/index work including an optional explicit pole list. A cycle of length N uses exactly 2N-1 scalar multiplications and 2N-2 scalar additions with the direct closure/forward recurrence used in fresh_checks.py. It reads the input and writes N outputs. No matrix inversion primitive or Fourier call occurs. Plan preparation is excluded from the displayed sample counters but is charged here. The result is O(N) scalar work when r<=N, not an O(N) bit claim.

### Exact rational precision is not free

For integer inputs of at most B bits and a=1/2, the fused denominator on a cycle of length ell is D=2^(r ell)-1. All outputs can be represented with that shared denominator. Numerators have at most O(B+r ell+log ell) bits. Build the first numerator as the corresponding geometric integer sum, then update successive numerators by the exact recurrence

    n_t = (n_(t-1) + 2^r D x_t)/2^r.

The division is exact for these numerators. With conventional binary integers and schoolbook arithmetic, a conservative bound is O(N(B+rN+log N)^2) bit work and O(N(B+rN+log N)) bits for explicit outputs. Working storage can be streamed beyond the input and outputs. The small finite-field checks instead use modulus 1009; their field operations have fixed-size cost only at the tested sizes. Neither model provides an exact finite-bit encoding of arbitrary complex inputs or an exact floating-point FFT.

Arbitrary routed endpoint magnitudes and cancellations may require much more precision in an approximate numerical realization. Formula (5) is a norm obstruction, not a forward-error certificate for the constructed evaluator. No finite-precision practical speedup is asserted.

## 8. Verification and prior-art boundary

Fresh controls use only newly authored standard-library Python. No supplied program was executed, imported, compiled, or AST-parsed. EXACT_RESULTS.json and EXACT_RUN.log record 55 field cases and 37,368 exact matrix-entry equalities, including compatible independent routing, common-route diagonal endpoints, noncommuting correction identities, correction ranks, and an explicit singular guard. Ninety-six exact characteristic-zero controls check 11,166 nonzero UQ entries by reduction modulo freshly constructed cyclotomic polynomials. Four separate operation-count controls compare the inherited distinct-branch bank against its actual single-solve evaluator. These support indexing and implementation, not the all-size proofs or complex norm inequalities.

AUDIT.md records a separate proof review of the identities, bounds, and assumptions. PRIMARY_SOURCE_COMPARISON.md distinguishes established uncertainty and inverse-update ingredients and the inherited packet identity from this scoped routed-packet synthesis. The SHA256 manifest attests the sealed bytes, not publication novelty, exhaustive priority review, or correctness by itself.
