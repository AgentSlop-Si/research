# An unbounded exact bank rank and border rank separation

10 October 2026. New author theorem, pending independent review. The theorem concerns the full accepted four-orientation bank dictionary. It is not a Fourier-rank assertion.

## Statement

For odd N≥3 and any primitive complex Nth root q, retain the accepted signed Weyl bank grammar and let R_N(A) be the minimum number of legal whole banks whose sum is A. Let border R_N(A) be the least m for which A lies in the Zariski closure of the matrices with R_N≤m. The same conclusion below holds if closure is taken in the usual complex topology.

THEOREM. The inverse cyclic shift satisfies

R_N(S^−1)=N−1, whereas border R_N(S^−1)=1.

The exact construction uses N−1 banks of orientation (−,+), all β=1, all distinct nodes x satisfying x^(N−1)=1, and the same raw phase weight

w_(x,j)=−1/(N−1),  j=0,…,N−1.

Every guard equals −x≠0. The construction is over Q(q,ζ_(N−1)), and hence over C. No claim of attainment over Q(q) alone is made. The lower bound allows every legal complex α,β, all orientations, zero nodes and all possible cancellations.

Consequently the exact/border ratio is unbounded in this bank model. Exact legal finite-node rank cannot be replaced by rank in the projective closure of the scroll dictionary or its secant closure.

## Exact lower bound in the full signed dictionary

The target S^−1=W_(N−1,0) has coefficients 0 at (a,0) for 1≤a≤N−2 and coefficient 1 at (N−1,0).

On b=0 the Gaussian factor is 1 and every bank contributes η_0 α^[εa]_N. A zero node contributes zero for all nonaxis a. For a nonzero node, on a=1,…,N−1 this is

η_0 α^a if ε=+1,

η_0 α^N(α^−1)^a if ε=−1.

Thus a sum of m banks, with any signs and legal β, restricts on the whole nonaxis b=0 interval to a sum of at most m ordinary exponentials Σ_(i=1)^s A_i λ_i^a, with distinct nonzero λ_i after equal frequencies are combined. Here s≤m. Neither δ nor other sector amplitudes can change this row; β=0 does not create another free parameter on it.

If m≤N−2, the first s target entries, at a=1,…,s, all vanish. The matrix (λ_i^a)_(a=1,…,s; i=1,…,s) is an invertible Vandermonde matrix times diag(λ_i). Therefore every A_i=0, contradicting the nonzero target entry at a=N−1. The case s=0 is immediate. Hence R_N(S^−1)≥N−1.

This argument does not assume different nodes across orientations, nonzero amplitudes, or generic parameters. Coincident effective frequencies are combined before the Vandermonde argument.

## Exact upper bound and original weights

Let M=N−1 and let x range over all Mth roots of unity. Use orientation (−,+), β=1, and give its sector-zero amplitude η_(x,0)=x^−1/M, with every other sector amplitude zero. All these nodes are nonzero and distinct. Since x^M=1, the guard is Δ_x=−x^N=−x. Thus the raw phase weights are precisely

w_(x,j)=Δ_x η_(x,0)=−1/M,

with no additional factor N; the factor 1/N is in the original bank definition.

Summing the coefficient expansions gives

Σ_(x^M=1) B_(-,+)(x,1;w)
 = Σ_(r=0)^(N−1) ((1/M) Σ_(x^M=1) x^(r−1)) S^(−r).

For 0≤r≤N−1=M, the exponent r−1 ranges from −1 to M−1. The root sum vanishes throughout this range except at r=1, where it equals M. Therefore the sum is exactly S^−1.

Equivalently, the literal resolvent identity is

S^−1 = −1/[N(N−1)] Σ_(x^(N−1)=1) Σ_(j=0)^(N−1) (I−xS^−1−q^(−j)T)^−1.

The accepted finite inverse identity applies to every displayed branch because Δ_x=−x≠0. This proves exact attainment with N−1 legal banks and, together with the lower bound, exact rank.

## A one-bank curve with the stated limit

For every nonzero complex t take one ( +,+ ) bank with α=t^−1, β=1, and constant raw phase weights w_j=−t^−1. Its guard is −t^−N, which never vanishes for t≠0. Finite-character orthogonality gives only the sector-zero amplitude η_0=t^(N−1). Consequently that legal bank is exactly

A(t)=Σ_(r=0)^(N−1) t^(N−1−r) S^r.

The right side is a polynomial matrix curve, and A(0)=S^(N−1)=S^−1. Its nonzero-t values all have bank rank at most one. Hence S^−1 lies in both the ordinary and Zariski closures of the one-bank set. Since S^−1 is nonzero and the rank-zero set is {0}, its border rank is exactly one.

The degeneration uses a finite-node parameter tending to infinity and compensating weights. No infinite node or divergent parameter is declared to be an actual legal bank at t=0. The target is reached only as a limit; its exact rank remains N−1.

## Interpretation and scope

The asymptotically large exact/border gap is a concrete reason the finite legal-node restriction matters. The one-bank parameterization is nonclosed. Allowing its projective boundary changes the optimization problem dramatically even for a simple cyclic shift, before studying the special Fourier target.

This also explains why a scroll-secant dimension or generic-border-rank theorem cannot silently certify exact legal bank counts. This result does not assert a large Fourier exact/border gap, an arithmetic complexity lower bound, physical resource lower bound, numerical ill-conditioning theorem, or new historical priority. The degeneration itself has unbounded α and raw weights; conditioning of any actual implementation is outside this statement.
