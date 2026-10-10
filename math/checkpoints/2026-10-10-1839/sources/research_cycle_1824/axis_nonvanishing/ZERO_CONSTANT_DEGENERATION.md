# A zero-constant degeneration certifies an axis minor

10 October 2026. Standalone elementary lemma. This is a new author derivation; it does not change the accepted bank bound. The zero-node polynomial below is a test point for a polynomial minor, not a legal bank witness.

Let F be a field and let N be a positive integer. For any monic polynomial g of degree m, including g(0)=0, define p_j to be the coefficient vector of t^j modulo g and define the N-row quotient matrix

    X_N(g)[a,:] = (p_a, 1, p_[−a]_N),  0≤a<N.

The exponent [−a]_N is a nonnegative residue in {0,…,N−1}; no negative power of t is being reduced. Thus all entries of X_N(g) are polynomial functions of the nonleading coefficients of monic g, even at zero-constant polynomials.

Define

    J_N A = t^N A(1/t)+A(0)(1−t^N),  deg A≤N−1.

Direct coefficient pairing gives the row-dependence space

    D_N(g)={A: deg A≤N−1, g|A, g|J_N A, A(1)=0}.

Assume

    g_0=t(t−1)f,  r=deg f=m−2,
    f(0)≠0,  gcd(f,H_f)=1,  H_f=t^r f(1/t),
    2m−2>N−1.

Then X_N(g_0) has full row rank N.

Proof. Coprimality implies f(1)≠0. If A belongs to D_N(g_0), then A(0)=0. Divisibility of t^N A(1/t) by f implies H_f|A, since f and H_f have nonzero constant terms. Also g_0|A. The factors t, t−1, f, H_f are pairwise coprime except that f itself may have repeated factors; their product still divides A because gcd(f,H_f)=1 and neither vanishes at 0 or 1. That product has degree

    deg[t(t−1)fH_f]=2+2r=2m−2>N−1.

Therefore A=0. This proves the claim without squarefreeness of f.

Now let U be any linear polynomial space of maximum degree m for which the monic slice U_1={g∈U: coefficient of t^m is 1} is nonempty. If U_1 contains such a g_0, one N-column minor of X_N(g) is a nonzero polynomial on U_1. Since U_1 is an affine linear space, its coordinate ring is an integral domain. This axis-minor open set therefore meets every finite intersection of other nonempty polynomial open sets on the same slice. Over an infinite field, their nonzero product has a rational coefficient point.

In particular, if the constant and squarefree guards are separately nonzero on U_1, there is a legal monic g∈U with nonzero constant, simple roots, and full axis rank. No bank is ever assigned the zero node in g_0. The full-rank minor is only specialized there to prove that it is not identically zero.
