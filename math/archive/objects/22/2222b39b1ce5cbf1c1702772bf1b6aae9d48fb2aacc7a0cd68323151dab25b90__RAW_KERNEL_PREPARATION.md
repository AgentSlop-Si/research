# Linear-work raw preparation of the orbit kernels

9 October 2026 UTC. Independently derived during paired review. This improves kernel preparation, not arbitrary-input kernel application or the final Fourier complexity.

## Theorem and model

Let M>=2, N=M^2, and let omega have exact order N in a field. Set eta=omega^M and let S act on M-vectors by (Sv)[u]=v[u-1 mod M]. Represent X=omega S, so X^M=eta I. In this raw cyclic-shift basis, all M coefficient vectors of

    D_X(z)=sum_(s=0)^(M-1) k_s(X)z^s,
    k_s(X)=X^binom(s,2)/product_(r=1)^s(1-X^r),

and all M+1 coefficient vectors of

    P_M(X,z)=product_(j=0)^(M-1)(1+X^j z)

can be explicitly prepared in O(M^2)=O(N) field operations and O(N) words, with one shared scalar inversion. The root and field are supplied; root/field discovery and bit complexity are outside this exact-arithmetic statement. All root-table construction, cycle discovery, intermediate coefficients and outputs are charged. The theorem is valid for non-dyadic M as well.

## Coefficient recurrences

Put p_s=[z^s]P_M, with p_0=k_0=1. The q-binomial identities give

    (I-omega^s S^s) p_s
        = (omega^(s-1)S^(s-1)-eta I)p_(s-1),  1<=s<=M,
    (I-omega^s S^s) k_s
        = omega^(s-1)S^(s-1)k_(s-1),         1<=s<M.

Here each coefficient is an M-vector representing a polynomial in S. A multiplication by a scalar times S^j is a cyclic route plus M scalar products. The remaining inverse is a weighted permutation-cycle solve.

For fixed s, write d=gcd(s,M), L=M/d, alpha=omega^s. S^s has d disjoint cycles, all of length L. The sole closing denominator is

    delta_s=1-alpha^L=1-eta^(s/d).

For 1<=s<M, 0<s/d<M, so delta_s is nonzero. At s=M, L=1 and delta_M=1-eta is also nonzero. Thus every solve is admissible, including the non-coprime steps and the full top coefficient p_M.

## Explicit solve and charged preparation

For (I-alpha S^s)v=b, enumerate one cycle u_r=u_0+rs mod M, r=0,...,L-1. Then

    v[u_0] = (b[u_0]+sum_(r=1)^(L-1) alpha^(L-r)b[u_r])/delta_s,
    v[u_r] = alpha v[u_(r-1)]+b[u_r],  r=1,...,L-1.

All d cycles together take O(M) arithmetic and accesses. Every scalar power comes from a charged N-entry omega table; exponents fit O(log N)-bit indices. Euclidean gcd work for all s is O(M log M), absorbed by O(M^2), or cycles can be discovered explicitly in O(M) per step.

Generate delta_1,...,delta_M and batch-invert them with prefix products, one inversion, and a reverse pass. The denominators depend only on s and are reused for all cycles and both kernels. This costs O(M), not one independent inversion per coefficient. Each right-hand side and solve costs O(M); there are 2M-1 steps. Store all coefficient vectors in O(N) words, or stream one kernel in O(M) live coefficient storage when its past rows are not needed later.

This method avoids a Fourier conversion entirely. The previous O(N log N) product-tree/Fourier preparation remains valid but is unnecessary for these specific coefficient tables.

## What remains expensive

For arbitrary input a(z), y=D_X(z)a(z) does not satisfy y(z)=P_M(X,z)y(eta z): the latter substitutes a(eta z) for a(z). The source counterexample a(z)=z already fails at its linear coefficient. Arbitrary input may also have nonunit constant term, so division by a(z) cannot repair this uniformly.

Preparing N kernel coefficients is distinct from applying their dense two-dimensional convolution to N arbitrary coefficients. The reviewed compiled FFT application still costs O(N log N). The sparse q-difference/intertwining identity alone does not provide a cheaper application. No general arithmetic lower bound is asserted.

## Independent controls

check_raw_preparation.py independently implements the cycle solve and one-batch preparation. It does not import any uploaded or constructor code. Across M=2,...,20,24,32, all 4,734 raw product coefficients agree with a separate direct sparse-factor expansion, and all 4,469 inverse-kernel values after direct spectral evaluation agree with their q-factorial formulas. Non-coprime shifts, M composite, the top product coefficient, and every closing denominator are checked. These finite exact controls corroborate the all-size proof; they do not certify floating-point stability.
