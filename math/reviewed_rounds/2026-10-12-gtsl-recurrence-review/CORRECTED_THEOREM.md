# Corrected conditional GTSL recurrence theorem

12 October 2026. This is a new expository derivative of the scoped review and independent rate audit. It does not replace the preserved candidate manuscript. No growing Fourier compiler is supplied or certified.

## Hypotheses

Let w be a positive integer, N = 2^w, and f(w) = C(2^w)/2^w. Assume nonnegative finite base costs, a fixed finite kappa >= 0, and a nonnegative factor rho(w). For every sufficiently large integer w, require the same cost family to satisfy

    f(w) <= rho(w) [f(floor(w/2)) + f(ceil(w/2))] + kappa.

For a Fourier application this scalar inequality must itself be proved for an explicit exact all-input family, under one consistent gate and preparation ledger. The recurrence calculation does not construct that family. Results here concern transform lengths N = 2^w only.

## Fixed eventual factor

Suppose rho(w) <= r eventually, where r is fixed and 0 <= r < 1. Then

- 1/2 < r < 1: C(N) = O(N (log N)^(log_2(2r)))
- r = 1/2: C(N) = O(N log log N)
- 0 <= r < 1/2: C(N) = O(N)

For an explicit proof when the recurrence holds for w >= 2, set d(w) = ceil(log_2 w), f(1) <= B, and q = 2r. Both rounded children have depth at most d(w)-1. If q >= 1, the nondecreasing depth envelope is

    A_d = B q^d + kappa sum_(i=0..d-1) q^i.

Induction gives f(w) <= A_(d(w)). For q > 1, q^d <= q w^(log_2 q), so the first conclusion follows. For q = 1, A_d = B + kappa d. For q < 1, M = max(B, kappa/(1-q)) is a constant inductive upper bound. A finite exceptional base region changes constants only. No monotonicity of f is assumed.

## Quantitative repair at the half threshold

If fixed parameters 0 <= r_* < 1, c >= 0 and gamma > 0 satisfy

    rho(w) <= r_* + c/w^gamma

eventually and uniformly, then the same three conclusions hold with r_* in place of r, including the exact exponent log_2(2r_*) above one half.

To prove the endpoint, at shell depth d the positive excess of 2rho(w) above 1 is at most 2c 2^(-gamma(d-1)). The sum of these bounds converges. Every product of the shell factors is therefore bounded, and the accumulated constant overhead is O(d). Above one half, divide the factors by 2r_* to obtain a bounded perturbation product; the geometric overhead sum is O((2r_*)^d). Below one half, eventually choose a fixed upper factor q < 1. The assumption gamma > 0 is necessary for this rate argument.

A more general sufficient endpoint condition is summable positive shell excess. A different, nonsummable sufficient condition is

    0 <= 2rho(w) <= 1 + c/d(w), with fixed 0 <= c < 1.

Choose M >= max(f(1), kappa/(1-c)). Both children are bounded by M d(w), giving f(w) <= M(d(w)+1). For eventual hypotheses, enlarge the finite base envelope.

## What convergence alone supplies

The hypothesis rho(w) -> 1/2 does not imply O(N log log N). It implies only the weaker uniform upper bound: for every fixed eta > 0,

    C(N) = O_eta(N (log N)^eta).

For each eta, eventually 2rho(w) <= 2^eta, and the shell recurrence proves the bound. It is sometimes abbreviated N (log N)^(o(1)) as an upper bound. COUNTEREXAMPLES.md shows why no fixed polynomial in log log N follows from the limit alone.

## Exact envelope and zero overhead

On w = 2^j let q_j = 2rho(2^j), base b >= 0, P_j = product_(k=1..j) q_k, and

    S_j = sum_(i=1..j) product_(k=i+1..j) q_k.

Then the maximal equality envelope is B_j = b P_j + kappa S_j. Empty products are 1. This remains valid with zero factors. For kappa > 0, B_j = O(j) if and only if S_j = O(j), since P_j <= q_1 S_j for j >= 1. For kappa = 0 and b > 0 the criterion is P_j = O(j). If both kappa and b vanish, the nonnegative solution is zero.

This is a worst-envelope statement on the dyadic subsequence; arbitrary non-dyadic factors need their own control. The full reports provide the exact weighted recursion-tree condition and sufficient all-integer shell bounds.

## Algorithmic boundary

A uniform compiler, exact output certificate, scale-uniform saving bound, predeclared overhead, and charged coefficient generation and routing remain missing. These conditional theorems do not prove faster DFT evaluation, a Fourier lower bound, practical acceleration, bit complexity, numerical stability, or novelty. Pointwise inequalities cannot replace the fixed margins in the theorem.
