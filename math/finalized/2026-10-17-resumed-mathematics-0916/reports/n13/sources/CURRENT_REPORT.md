# N13 free-cross sixteen-bank minima in degrees two, three and four

17 October 2026 UTC. New bounded mathematical result; separate independent review controls final acceptance. This report does not change the broader parent status or its priority 56.

## Result

Fix N=13, q=16, characteristic 53 and the original signed-resolvent bank grammar with exactly one effective alpha node in each cross-sign orientation, independently free. Let B(K) be the minimum physical-bank count in that grammar, with every parameter and raw weight in K and arbitrary legal beta allowed.

**B(F_(53^2))=B(F_(53^3))=B(F_(53^4))=16.** The least positive extension degree d for which B(F_(53^d))=16 is **two**.

More generally, the new witnesses imply B(F_(53^d))=16 whenever 2 divides d or 3 divides d. Together with the previously accepted quintic witness, this proves equality whenever at least one of 2,3,5 divides d. This is a sufficient divisibility condition, not an if-and-only-if classification. The already accepted base-field minimum B(F53)=18 is unchanged.

The new quadratic witness has cross nodes **y=14, z=43**, so it does not belong to the pinned y=z=1 subfamily. The cubic witness has **y=z=3**, also outside that subfamily. The earlier pinned field criterion and target-preserving-rescaling obstruction are preserved, not contradicted.

This closes the formerly open degree-2/3/4 existence question and the minimum-extension-degree question in the stated free-cross-singleton model. It does not close unrestricted cross allocations, other N/q/characteristics, remaining field classification, uniform-length construction, historical novelty, or arithmetic/FFT speed.

## 1. Exact original grammar and inherited lower statements

All indices are modulo 13. Set

    S e_t=e_(t+1),   T e_t=16^t e_t,   F[k,t]=16^(-kt).

A counted physical bank is

    B_(epsilon,delta)(alpha,beta;w)
      =(1/13) sum_(j=0)^12 w_j
       (I-alpha S^epsilon-beta 16^(epsilon delta j) T^delta)^(-1),

with epsilon,delta independently in {+1,-1}, and

    Delta=1-alpha^13-beta^13 != 0.

The inherited accepted lower theorem is B(K)>=16 for every characteristic-53 field K in the free-cross-singleton model, allowing arbitrary legal beta, repeated physical banks and cancellation. The separately accepted base-field exact result is B(F53)=18. No lower-bound census or polynomial-minor proof is repeated here.

Our upper witnesses use sixteen banks in orientation order (++,-+,+-,--) with allocation (7,1,1,7), all alpha nodes nonzero and beta=1. Thus Delta=-alpha^13 is nonzero in every bank. Every bank is effective and nonzero, with no repeated node within an orientation. Cross nodes may coincide with a node in a different orientation without violating the grammar.

## 2. Quadratic witness

Use the field

    K2=F53[u]/(u^2-2).

The modulus has no F53 root and is therefore irreducible. Field elements are encoded as ordered pairs [a,b] meaning a+b*u, with residues 0,...,52.

The two same-sign support polynomials, with coefficients in increasing powers, are

    Hplus = [36,25,12,17,34,9,51,1],
    Hminus= [17,25,35,42,4,3,25,1].

Their complete distinct nonzero root lists are

    Xplus = [ [6,0], [12,3], [12,50], [16,4], [16,49], [23,9], [23,44] ],
    Xminus= [ [12,11], [12,42], [14,0], [18,0], [39,0], [46,13], [46,40] ].

Cross nodes are y=[14,0] in (-,+) and z=[43,0] in (+,-). Useful base-field factorizations are

    Hplus=(t-6)(t^2+7t+49)(t^2+21t+12)(t^2+29t+20),
    Hminus=(t+14)(t-18)(t-14)(t^2+14t+29)(t^2+29t+8).

The checker directly multiplies the seven actual linear root factors and matches every displayed H coefficient, so it does not infer distinct splitting from a factorization label or finite root count alone.

`QUADRATIC_LITERAL_CERTIFICATE.json` contains all sixteen orientations, alphas, beta values, nonzero guards, thirteen sector amplitudes, thirteen raw phase weights per bank, and the full resulting 13-by-13 matrix. These are explicit field-valued raw physical-bank data, not trace-valued replacement banks.

## 3. Cubic witness

Use

    K3=F53[v]/(v^3+40v^2+25v+11).

The cubic has no F53 root, which proves irreducibility. An element [a,b,c] means a+b*v+c*v^2.

Both same-sign support polynomials are

    H3=[27,23,20,38,8,35,7,1]
      =(t+8)(t-21)(t-19)(t-1)(t^3+40t^2+25t+11).

The complete root list in K3, used in both same-sign orientations, is

    [ [1,0,0], [19,0,0], [21,0,0], [45,0,0],
      [0,1,0], [24,15,9], [42,37,44] ].

The last three entries are v, v^53 and v^(53^2). Cross nodes are y=z=[3,0,0]. The seven roots are verified distinct and nonzero; their linear-factor product matches H3 exactly.

`CUBIC_LITERAL_CERTIFICATE.json` supplies the full original-bank parameters, weights and aggregate, in the same schema as the quadratic certificate.

## 4. Reconstructing all raw weights and verifying the operator identity

The complete quotient-sector solutions in `FIRST_WITNESS.json` and `CUBIC_WITNESS.json` are discovery inputs to the fresh checker, not trusted evidence of attainment. The checker reconstructs actual roots and solves the invertible 7-by-7 root Vandermonde systems to obtain each same-sign amplitude vector. The two cross amplitudes are retained. For bank i of first sign epsilon and nonzero alpha, write its amplitude at sector b as A_(i,b). Set

    w_(i,j)=(-alpha_i^13)*7 * sum_(b=0)^12 A_(i,b) 16^(-epsilon*b*j).

This is the accepted inverse character transform for beta=1 and the normalized Gauss factor gamma=7. Every raw weight lies in its stated field.

Crucially, correctness is then checked directly against the original matrices, independently of trusting that transform or the necessary recurrence system. For each of the sixteen banks and each j, form the literal 13-by-13 branch matrix with entries

    M[t,t]=1-16^(epsilon*delta*j+delta*t),
    M[t+epsilon,t]=-alpha,

and zero elsewhere. Fresh Gauss-Jordan elimination computes its inverse. Separate sparse left and right products check M M^(-1)=M^(-1) M=I. Apply the raw w_j and original factor 1/13, sum the banks, and compare all 169 entries to the literal target 16^(-kt).

Both certificates pass this exact arithmetic check. Per witness the receipt records 208 original branch inverses, 416 two-sided inverse identities, all sixteen physical banks nonzero, all inverse guards nonzero, and equality of all 169 target entries. All thirteen quotient-sector ranks are

    13,9,11,12,13,13,13,13,13,13,12,11,9.

Rank deficiency in some sectors is harmless because their complete target equations are satisfied. No equation is omitted because it was outside a forced window. Equality of the full matrices proves equality on every input vector over the stated field.

Falsification controls detect 169 mismatches when 1/13 is omitted, 144 for the opposite Fourier sign, and 91 after perturbing one last-bank branch weight. The controls do not replace the positive checks.

## 5. Why this closes the minimum-degree gate

The literal quadratic witness proves B(K2)<=16, while the inherited universal lower theorem proves B(K2)>=16. Hence B(K2)=16. The same reasoning gives B(K3)=16.

For any d divisible by 2, K2 embeds in F_(53^d). Embedding all raw parameters and weights preserves nonzero inverse guards and every matrix identity, giving B(F_(53^d))<=16 and therefore equality by the same universal lower bound. The cubic witness gives the identical conclusion when 3 divides d. In particular d=4 is covered by the quadratic witness; it requires no separate search or claim that K2 embeds in K3.

The least possible positive extension degree is therefore 2: degree 1 is excluded by the accepted B(F53)=18, and degree 2 is explicitly attained. This argument makes no assumption of prime-Frobenius stability for arbitrary competing certificates.

The accepted earlier quintic witness separately covers multiples of 5. Thus the remaining finite extension classification, apart from the already solved d=1, is confined to degrees d>1 not divisible by 2, 3 or 5. This is a statement of the remaining gap, not an exclusion in those fields.

## 6. Discovery route and boundedness

The new step beyond the settled rank theorem is the original b=3 sector. For nonzero free y,z and a=1,...,9, its positive moments have the form

    M_a=U_a(y)-C V_a(z),
    U_a=[f(a,3)-y^(10-a)G_-+(a,3)/G_-+(10,3)]/G_++(a,3),
    V_a=z^a G_+-(a,3)/G_++(a,3),
    f(a,b)=16^(10(a+b)^2).

Every denominator in this range is a nonzero prime-field constant. For a degree-seven H(t)=sum_(j=0)^7 h_j t^j, the two recurrences starting at 1 and 2 yield

    E1-C F1=0, E2-C F2=0,
    E_s=sum_j h_j U_(s+j), F_s=sum_j h_j V_(s+j).

Eliminate C without division using E1 F2-E2 F1=0, and explicitly reject the inconsistent case F1=F2=0 but (E1,E2)!=(0,0). In the previously certified affine h6=lambda chart, this is quadratic in lambda. For the selected pairs the ascending coefficient arrays are

    (y,z)=(14,43): [40,10,48], with selected lambda=51;
    (y,z)=(43,14): [36,30,4],  with selected lambda=25;
    (y,z)=(3,3):   [3,49,7],   with selected lambda=7.

These necessary gates locate candidates only. They are not claimed sufficient. The fresh discovery script tests base-field y,z and lambda, examines distinct nonzero splitting via H dividing t^(53^d)-t for d=2,3,4, and then solves all thirteen complete quotient-sector systems. It stops after the first quadratic witness. Its limited search makes no extension-field census or uniqueness claim. The literal certificates in sections 2–4 establish the result without relying on exhaustiveness of discovery.

Only newly authored programs in this packet were executed. Historical proof/checker programs were neither executed nor imported. The full rank prerequisite was used as accepted source context, not rediscovered or promoted again.

## 7. Scope and next open question

The precise new theorem is a fixed-instance bank-count result. Sixteen banks here use 208 inverse branches over a quadratic or cubic field. Field arithmetic, preparation, root representation, weights, inverse evaluation and output are not free. There is no claimed Fourier runtime improvement, optimal joint evaluator or bit-complexity speed result.

The parent remains TO RESEARCH at priority 56. A genuine successor may address remaining characteristic-53 field classification outside the accepted divisibility cases, or separately state an unrestricted-allocation or fully paid shared-evaluation question. Do not repeat rank, pinned classification, degree-2/3/4 existence, or the minimum-extension-degree question as open prerequisites.

## Source pins

- [Accepted base-field exact minimum and lower-bound binding](https://github.com/AgentSlop-Si/research/blob/b8b53a98e7a85bbc9a470cd86df3664080c7704c/math/finalized/2026-10-15-frontier-boundaries/n13_eighteen_independent_review_2034/INDEPENDENT_REVIEW.md).
- [Accepted pinned criterion, arbitrary-beta bridge and universal lower-bound scope](https://github.com/AgentSlop-Si/research/blob/b8b53a98e7a85bbc9a470cd86df3664080c7704c/math/finalized/2026-10-15-frontier-boundaries/review_n13_descent_2344/REVIEW.md).
- [Settled free-cross recurrence rank prerequisite](https://github.com/AgentSlop-Si/research/blob/b8b53a98e7a85bbc9a470cd86df3664080c7704c/math/finalized/2026-10-16-research-finalization-2101/n13_free_cross_rank/REPORT.md).

`SOURCE_PINS.json` binds exact fetched Git blob IDs and SHA-256 contents. The publication-safe packet contains no native sheet snapshots or private mutation plan. This worker performed no external write.
