# GTSL recurrence counterexamples and verifier limitation

12 October 2026. These scalar equality recurrences refute overly strong deductions from the proposed cost inequality. They are not Fourier circuit constructions or Fourier lower bounds. Each recurrence has nonnegative costs and constant overhead kappa = 1.

Set d(w) = ceil(log_2 w), f(1) = 1, and for w >= 2 define

    f(w) = rho(w) [f(floor(w/2)) + f(ceil(w/2))] + 1.

The children are smaller positive integers, so this is well-defined. At w = 2^j, write g_j = f(2^j), q_j = 2rho(2^j); then g_0 = 1 and g_j = q_j g_(j-1) + 1.

## Half limit with an extra harmonic factor

Take rho(w) = (d(w)+1)/(2d(w)). Then rho(w) -> 1/2, but q_j = 1+1/j and

    g_j = (j+1) H_(j+1), where H_m = sum_(k=1..m) 1/k.

The base value is 1, and multiplying j H_j by (j+1)/j and adding 1 proves the formula. Thus g_j = Theta(j log j), not O(j). Along N = 2^(2^j), this permits Theta(N (log log N)(log log log N)). The single factor rho(2)=1 is a finite exception; rho(w)<1 eventually.

## Half limit with quadratic depth growth and all factors below one

Take rho(w) = (1+2/(d(w)+2))/2. Every rho(w) is strictly below 1 and tends to 1/2. The dyadic formula is

    q_j = 1+2/(j+2), g_j = (j+1)(j+3)/3.

It follows directly by substitution and has base 1. Therefore an inverse-depth approach to the half limit can produce quadratic normalized depth growth.

## Half limit exceeding every fixed polynomial in depth

Take q_j = 1+1/(floor(sqrt(j))+1) and rho(w) = q_(d(w))/2. Every rho(w)<1, and rho(w)->1/2. If P_j = product_(k=1..j) q_k, then

    P_j <= g_j <= (j+1) P_j, log P_j = Theta(sqrt(j)).

Indeed, each excess lies between 1/(sqrt(j)+1) and 1/sqrt(j), while x/2 <= log(1+x) <= x for 0 <= x <= 1. Summing proves g_j = exp(Theta(sqrt(j))), which exceeds j^A for every fixed A. The archived exact-rational witness at j=256 gives floor(g_j/j) = 2,227,256,085. The asymptotic failure follows from the proof, not that finite value.

## Pointwise below one is insufficient for sub N log N

Take rho(w) = 1-1/w and f(w)=w for every w>=1. The child sizes sum to w, so for w>=2,

    (1-1/w) [floor(w/2)+ceil(w/2)] + 1 = w.

Thus every rho(w)<1 but C(2^w)=2^w w. A fixed eventual gap below one is necessary for the stated fixed-saving implication.

## Pointwise below one half is insufficient for linear cost

Take rho(w) = d(w)/(2(d(w)+1)). Every rho(w)<1/2, yet

    q_j = j/(j+1), g_j = (j+2)/2.

Substitution proves the formula. The normalized dyadic costs are unbounded, so the hypotheses do not force O(N). A fixed eventual gap below one half gives the linear theorem; a vanishing gap need not.

## One test vector cannot certify a linear map

The original verifier uses x_j = 7+11j+3j^2 modulo 257. For every tested size, x_0=7 and x_1=21. Set

    E = e_0 (21 e_0^T - 7 e_1^T).

Then E is nonzero, E x = 0, and E e_0 = 21 e_0 != 0 in the field with 257 elements. Hence F_N+E agrees with F_N on the tested vector and fails on e_0. This shows a coverage limitation; it does not show an error in the classical Cooley-Tukey implementation.

A full basis test certifies that finite-field specialization only. A characteristic-zero or cyclotomic theorem needs exact symbolic identities or a justified lifting argument. With explicit primitive-root and index conventions, MX=ZM and M e_0=1 provide an all-input Weyl certificate, but the original script does not perform it.
