# Independent proof review: inverse-shift exact and border bank ranks

10 October 2026. Verdict: **accepted by independent mathematical proof review**. Source: sources/EXACT_BORDER_RANK_SEPARATION.md, SHA-256 791ca8ceeb4851059f73e841f11eeeef2d95f99a5de97ff1618fe4bf3fb75ea8. No supplied or fresh research program was executed in this review.

For every odd N>=3 over C, in the full accepted four-orientation legal bank dictionary,

R_N(S^(-1))=N-1, and border R_N(S^(-1))=1.

Border here means closure of the actual finite legal-bank sums, in either the Zariski or ordinary complex topology. This is not rank relative to the already closed projective scroll.

## Complete lower-bound check

At b=0 only ell=0 contributes. Every bank's Gaussian factor is 1, regardless of delta. For a=1,...,N-1, an alpha=0 bank contributes zero. Every nonzero-alpha forward bank gives A lambda^a with lambda=alpha. A backward bank gives the same form with lambda=alpha^(-1) and A=eta_0 alpha^N.

Thus any m-bank representation, including all signs, arbitrary legal beta, zero amplitudes and coincident effective frequencies, yields at most m distinct nonzero exponentials on the nonaxis row after combining equal frequencies. If their number s<=m<=N-2, the zero target entries a=1,...,s force all amplitudes to zero: det(lambda_i^a) is a nonzero Vandermonde determinant times the product of the lambda_i. This contradicts coefficient 1 at a=N-1. The case s=0 also contradicts that coefficient immediately.

Other sectors cannot repair this row, and cancellation elsewhere cannot invalidate its necessary equations. Therefore N-1 is a lower bound in the entire permitted dictionary, not merely in a preferred orientation.

## Exact upper and guards

Set M=N-1. For each distinct Mth root x, use orientation (-,+), beta=1, eta_0=x^(-1)/M and all other sector amplitudes zero. Since x^N=x, its guard is Delta=-x, nonzero. Multiplying eta_0 by Delta gives the constant raw weight -1/M for each of the N phases, exactly as stated.

The coefficient at S^(-r) is M^(-1) sum_(x^M=1) x^(r-1). In the range r=0,...,M, the exponent runs from -1 to M-1. Because M>=2, its only multiple of M is zero, at r=1. Hence exactly the S^(-1) coefficient survives. All weights and nodes lie in Q(q,zeta_(N-1)); no Q(q)-only assertion is needed. Finite-character orthogonality and the legal geometric inverse justify every original branch and the factor 1/[N(N-1)] in the literal double sum.

## One-bank degeneration

For t nonzero, alpha=t^(-1), beta=1 and constant raw weights -t^(-1) give guard -t^(-N) and sector amplitude eta_0=t^(N-1). All higher sectors vanish. The bank is therefore

A(t)=sum_(r=0)^(N-1) t^(N-1-r)S^r.

This is a polynomial matrix curve extending to A(0)=S^(N-1)=S^(-1). Its nonzero-t points are legal one-bank matrices, so the limit belongs to both closures. Rank zero only contains the zero matrix, and S^(-1) is nonzero, proving border rank exactly one. The diverging alpha and raw weights are used only along the curve; no illegal infinite node is claimed to be an exact bank.

## Significance and classical boundary

The theorem correctly exhibits an unbounded ratio of finite-legal bank rank to its closure rank. It is a useful warning that closing the dictionary changes the optimization problem even for a simple target. It does not establish a Fourier exact/border gap.

The main lower mechanism is classical rational-normal-curve independence after projection to the nonaxis row: dividing an exponential column by lambda gives (1,lambda,...,lambda^(N-2)), while the target is the excluded infinite endpoint. The full-bank root-of-unity witness supplies the matching upper construction. This is a concrete model-specific proposition, not evidence that the general finite-node/open-rank phenomenon is new.

The appropriate literature trail includes Jelisiejew's fixed-forbidden-set quantity Ork(F,V) and open Waring rank, Definition 2 in *An upper bound for the Waring rank of a form*, and Ballico's open X-rank, Definition 1.3 in *On the stratification by X-ranks of a linearly normal elliptic curve*. Those papers distinguish avoiding a prescribed closed set or all proper closed sets from unrestricted projective rank. Their definitions are relevant predecessors; the bank model is not automatically identical to either open-rank optimization.

Sources inspected for this comparison:

- https://arxiv.org/pdf/1305.6957, Definition 2, printed p.2.
- https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/1145/950/4334, Definition 1.3, printed p.20.

No mathematical blocker was found. No historic-priority, runtime, conditioning, or complexity claim is accepted.
