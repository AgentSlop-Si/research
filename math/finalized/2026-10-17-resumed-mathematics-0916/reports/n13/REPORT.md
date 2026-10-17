# N13 sixteen-bank attainment in degree seven

17 October 2026 UTC. New bounded field-degree result. Independent review controls final acceptance.

## Result

For N=13, q=16, characteristic 53, and the original signed-resolvent grammar with exactly one effective alpha node in each cross-sign orientation, independently free, let B(K) be the minimum physical-bank count with all raw parameters and weights in K and arbitrary legal beta allowed. Then

    B(F_(53^7)) = 16.

Consequently B(F_(53^d))=16 whenever at least one of 2, 3, 5, or 7 divides d. The 2/3/5 cases and B(F53)=18 were already accepted; the new contribution is degree seven and its scalar extensions. The previous least positive attaining degree, two, is unchanged.

This is a sufficient divisibility condition, not an if-and-only-if classification. The remaining finite-field classification, apart from solved d=1, is at degrees d>1 relatively prime to 210. No exclusion there follows from this search.

The parent owners M-MAGNETIC-SPAN, NEW-17, Q35 and NEXT-MAGNETIC-SIGNED remain TO RESEARCH, priority 56. Only this degree-seven gate closes. Unrestricted cross allocations, uniform lengths, other parameters, historical novelty and any Fourier-runtime improvement remain outside the result.

## 1. The declared finite family

Before search, this worker declared the following bounded family to the parent and reviewer:

* y=z in F53*, giving 52 cross-node choices;
* the same monic degree-seven support polynomial H_(y,lambda) in (++) and (--);
* lambda in F53, giving 53 affine choices for each y;
* the accepted forced-recurrence chart h6=lambda;
* allocation (7,1,1,7), beta=1, and support roots in F_(53^7).

The 2,756 pairs exhaust that declared family, not all cross nodes, support polynomials or extension-valued coefficients. The accepted rank-six theorem guarantees that the six forced recurrence equations have exactly this one-parameter monic solution family. Its h6 chart is nonsingular for every y in F53 because its exceptional polynomial is irreducible of degree 37. Neither rank six nor the affine parameterization alone is treated as a sufficient bank certificate.

The fresh census reconstructs the forced equations from Gaussian factors, checks the necessary b=3 equations without division by a parameter expression, rejects zero or repeated roots, tests H dividing X^(53^7)-X, and solves every row of all thirteen quotient-sector systems. Its sequential counts are:

* 2,693 fail the necessary b=3 equations;
* 2 have a zero support root;
* 1 has a repeated support root;
* 52 fail degree-seven splitting;
* 8 pass all guards, splitting and every full-sector system.

The eight passing (y,lambda) pairs are (2,40), (4,40), (13,8), (14,36), (24,49), (30,0), (43,2), and (43,30). No full-sector failure occurs among the eight splitting survivors. This describes the exact finite-family census. The first survivor receives the full literal original-bank certificate below.

## 2. An explicit degree-seven support

Take

    H(t)=t^7+40t^6+9t^5+25t^4+31t^3+4t^2+25t+25,
    K=F53[u]/(H(u)),
    y=z=2.

The fresh verifier proves u^(53^7)=u and gcd(H,t^53-t)=1. Since 7 is prime, every irreducible factor of H has degree 1 or 7; the gcd removes degree 1. Hence H is irreducible of degree 7. In particular, K is a field. This argument is established before any inversions in K are used.

Encode sum_(i=0)^6 a_i u^i by [a0,...,a6]. The complete roots u,u^53,...,u^(53^6) are

    [0,1,0,0,0,0,0]
    [42,22,45,47,8,27,48]
    [48,43,24,18,1,18,51]
    [37,4,8,2,49,45,29]
    [43,41,28,48,28,50,10]
    [51,48,21,1,15,49,20]
    [4,0,33,43,5,23,1].

All seven are distinct and nonzero. Their seven linear factors are multiplied out in K and match every coefficient of H. Use this root list in each same-sign orientation and the single node 2 in each cross orientation. Every beta is 1, so every original inverse guard is Delta=-alpha^13, which is nonzero.

## 3. From all sectors to actual weights

Write S e_t=e_(t+1), T e_t=16^t e_t and F[k,t]=16^(-kt), with indices modulo 13. A physical bank is exactly

    B_(epsilon,delta)(alpha,beta;w)
      =(1/13) sum_(j=0)^12 w_j
        (I-alpha S^epsilon-beta 16^(epsilon delta j) T^delta)^(-1).

The accepted normalized sector target is f(a,b)=16^(10(a+b)^2). The orientation factor is the ordered Gaussian coefficient with r=[epsilon a]_13, ell=[delta b]_13, omega=16^(epsilon delta), zero when r+ell>=13. A bank contributes G_(epsilon,delta)(a,b) alpha^r A_b. The discovery checker computes G from its finite product; the literal checker independently recomputes it through the Pascal recurrence.

For each same-sign support let V(k,i)=x_i^k, 0<=k<=6. Distinct roots make V invertible. Convert the complete solved quotient-sector vector c into actual root amplitudes by A=V^(-1)c; retain the two solved cross amplitudes. All thirteen full actual-root sector systems are then checked directly, comprising 169 equalities. Their ranks are

    13,9,11,12,13,13,13,13,13,13,12,11,9.

For each bank with first sign epsilon use the accepted inverse character transform, with gamma=7:

    w_j=(-alpha^13)*7*sum_(b=0)^12 A_b 16^(-epsilon*b*j).

The checker also inverts this transform and recovers all 208 sector amplitudes. The resulting sixteen orientation/alpha/beta records, guards, all sector amplitudes, all 208 raw weights and the complete matrix are stored in DEGREE7_LITERAL_CERTIFICATE.json. These are original field-valued physical banks. No trace primitive or quotient-algebra replacement is used.

## 4. Literal original-matrix verification

For each bank and each j, the verifier builds the actual branch matrix

    M[t,t]=1-16^(epsilon*delta*j+delta*t),
    M[t+epsilon,t]=-alpha.

Fresh Gauss-Jordan elimination computes all 208 inverses. Separate exact sparse left and right matrix products verify all 416 inverse identities. The original raw weight and original factor 1/13 are applied; all sixteen physical-bank matrices are nonzero. Their sum agrees with the literal target 16^(-kt) in all 169 entries. Thus the representation is valid on every input vector over K.

Falsification controls produce 169 mismatches when 1/13 is omitted, 144 for the opposite Fourier sign, and 91 after perturbing the final branch weight of the final bank. These controls supplement, rather than replace, the positive identities.

The inherited universal lower theorem is B(K)>=16 for every characteristic-53 field in this free-cross-singleton grammar, allowing arbitrary legal beta, repeated physical banks and cancellation. Combining it with the explicit upper witness proves B(F_(53^7))=16. Embedding F_(53^7) into F_(53^d) whenever 7 divides d preserves every raw parameter, guard and matrix identity. This proves the new divisible-by-seven cases.

## 5. Reproduction and boundaries

Run the two newly authored standard-library programs, in order:

    python search_degree7.py
    python verify_literal_degree7.py

The first recreates the complete census and first witness from its exact formulas. The second consumes only inert witness JSON and independently constructs field roots, weights, sectors and literal inverses; it does not import the discovery program. No historical scientific program was executed, imported or compiled. A clean-directory replay is bound by REPLAY.json. SOURCE_PINS.json records immutable Git source pins and local content hashes; SHA256SUMS.json binds the candidate packet.

This is a fixed-instance bank-count theorem. Sixteen banks still use 208 inverse branches over a degree-seven field. Root construction, extension-field arithmetic, raw weights, inverse evaluation and output costs are not free. No FFT-speed, joint-evaluation or bit-complexity improvement is claimed.

The exact next gate is an explicit characteristic-53 degree d>1 with gcd(d,210)=1, or a sound exclusion for a declared family in such a degree. Examples begin at d=11 and d=13. Any global field classification must allow extension-valued cross nodes and annihilator coefficients, and handle the accepted degree-37 chart exceptions by the alternative chart or global polynomial parameterization. The present finite-family census does not restrict those possibilities.

## Sources

* [Accepted degree-2/3/4 result and preceding field boundary](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-17-research-finalization-0006/n13/REPORT.md).
* [Accepted rank-six and global affine parameterization](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-16-research-finalization-2101/n13_free_cross_rank/REPORT.md).
* [Accepted arbitrary-beta bridge, pinned criterion and lower-bound scope](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md).
* [Accepted exact base-field minimum](https://github.com/AgentSlop-Si/research/blob/bcbc3854c9af6bac7ccaf8378c1629ae63889fbb/math/finalized/2026-10-15-frontier-boundaries/n13_eighteen_independent_review_2034/INDEPENDENT_REVIEW.md).

No external write was performed by this worker.
