# Finite-N approximation corollary

Proved within this priority review on 2026-10-10 UTC. This is a direct corollary of the accepted rank-one column-class obstruction, not an independently attributed literature theorem and not a consequence of the not-yet-sealed pseudoforest separator proposal. No already-sealed correctness-audit file was changed.

## Scope and statement

Let U_N be the normalized complex Fourier matrix,

    U_N[a,b] = N^(-1/2) omega^(ab),  0<=a,b<N,

with omega a primitive complex Nth root of unity. Let r>=1, put k=r+1, and suppose

    N > r*k^r.

Let M be any sum of r independently monomial-support-routed inverse branches with invertible denominators having at most two nonzeros per column. Zero endpoint weights are permitted. Then

    ||U_N-M||_2 >= epsilon_(N,r),
    ||U_N-M||_F >= epsilon_(N,r),

where

    epsilon_(N,r) = N^(-1/2) [2 sin(pi/N)]^[k(k-1)/2] / k^(k-1) > 0.

Here ||.||_2 is the global spectral/operator norm, not the entrywise Euclidean norm. The statement is over C; it is not a finite-field approximation statement.

## Proof

1. Restrict M to the fixed first k output rows. The accepted column-class lemma and common-refinement argument produce at most k^r cells, each having rank at most r in the sum. Since N>r*k^r, one cell contains k distinct columns C. Therefore B=M[0:k-1,C] is singular.

2. Set V=U_N[0:k-1,C]. For column indices b_1,...,b_k, the Vandermonde determinant has magnitude

       |det V| = N^(-k/2) product_(u<v) |omega^(b_v)-omega^(b_u)|.

   Distinct Nth roots on the complex unit circle have chord distance at least 2 sin(pi/N). Hence

       |det V| >= N^(-k/2) [2 sin(pi/N)]^[k(k-1)/2].

3. The k-by-k matrix V has k^2 entries of magnitude N^(-1/2), so

       ||V||_2 <= ||V||_F = k/sqrt(N).

   The product of its k singular values is |det V|. Bounding each of the largest k-1 singular values by k/sqrt(N) gives

       sigma_min(V)
       >= |det V| / (k/sqrt(N))^(k-1)
       >= N^(-1/2) [2 sin(pi/N)]^[k(k-1)/2] / k^(k-1).

   This verifies the normalization and all powers of N and k in the stated bound. Since V is a submatrix of a unitary, ||V||_2<=1 also holds and can sometimes sharpen the estimate; the displayed Frobenius-based estimate is always valid.

4. Choose a unit vector x in the kernel of the singular matrix B. Then

       ||V-B||_2 >= ||(V-B)x||_2 = ||Vx||_2 >= sigma_min(V).

   Row and column coordinate selections are contractions for the spectral norm, so

       ||U_N-M||_2 >= ||V-B||_2.

   Finally ||U_N-M||_F >= ||U_N-M||_2. This proves both claims.

## Closure interpretation

For the same fixed row set, every admissible M has at least one singular k-column minor. There are finitely many k-column subsets. Their determinantal zero sets form a finite closed union, containing the representation class and its closure. Fourier lies outside that union. This gives a second, purely qualitative proof of positive finite-N separation, without imposing bounds on branch coefficients or preventing them from diverging in a sequence.

## Relation to the inherited approximation theorem

The inherited `FFT_SEPARATION_RANK_THEORY/THEOREM.md` already proves, for r separation-rank-one branches and m=floor(N/2^r),

    ||U_N-M||_2^2 >= max(0, m/N-r/m).

For fixed r this gives liminf error >= 2^(-r/2) as N grows. Disjoint bare-cycle blocks also belong to that class by concatenation of their orders. Thus the present finite-N statement is not a stronger or first approximation barrier for Hamiltonian/bare-cycle branches. Its relevant extension is to the accepted full column-two-sparse denominator class, including attached-tree/high-degree support where a uniform constant separation-rank hypothesis has not been established here.

## Limits of the conclusion

- The bound is uniform over candidates for fixed N and r. It is not a positive bound uniform in N.
- Even for fixed r, it decays rapidly as N grows: the displayed expression is of order N^(-1/2-k(k-1)/2), with constants depending on k. For growing r the bound can be much smaller still.
- It does not exclude practically useful fixed-error approximations, approximate butterfly/HSS algorithms, products, arbitrary shared arithmetic, or broader matrix representations.
- It gives no general runtime lower bound.
- The argument uses complex normalization, singular values, and roots on the unit circle; the exact algebraic obstruction alone is more field-general.
