# F018: source-bound finite comparison and partition-energy lemma

15 October 2026 UTC. No external write. This is a bounded proof-scope comparison, not a novelty certificate or a new theorem count. It does not change the user's p^d constructive route.

## Result

The historical F018/C05/Q04/TH-04 additive-cutoff comparison is already complete. The accepted bare/all-weight fragmentation successor is separate. Its missing HERO0 Phase26 theorem body has now been recovered and compared in full. The STABLE-ARC original A1/A2 body was also recovered and read, but it is not the hash-pinned reviewed v2 manuscript. That exact-byte gate remains unresolved.

A useful clean presentation of the accepted fragmentation argument is the following elementary lemma. It makes clear that the energy step is classical, and that the potentially distinctive part is the simultaneous area/rank/count guarantee for incompatible branch partitions.

## Elementary independent-partition energy lemma

Let U be an N-by-N complex flat normalized unitary, and T=sum_{i=1}^r T_i. Suppose entry-disjoint coordinate rectangles E_j=R_j x C_j, j=1,...,p, have total area A, and rank(T_i[R_j,C_j])<=k_{ij}. Put k_j=sum_i k_{ij}. Then

||U-T||_F^2 >= sum_j max(0, |R_j||C_j|/N-k_j)
                  >= max(0, A/N-sum_j k_j).

Consequently

||U-T||_F^2/N >= max(0, A/N^2-(sum_j k_j)/N),
||U-T||_2^2 >= max(0, A/N^2-(sum_j k_j)/N).

Proof. Rank subadditivity bounds the rank of the actual summed approximant on cell j by k_j, irrespective of coefficient sizes or cancellation. Let P_j project onto that cell approximant's column space. The target restriction V_j is an operator contraction. Thus tr(P_j V_j V_j*)<=rank(P_j)<=k_j, whereas ||V_j||_F^2=|R_j||C_j|/N. Projection onto the orthogonal complement gives the displayed cell error bound. Sum squared errors on disjoint entries, then use ||E||_F^2<=N||E||_2^2. The argument needs neither a common row partition nor a common column partition across branches once the rectangles and ranks have been established.

This is a reformulation of the classical low-rank-tail estimate, not an originality claim.

## Specialization to the already accepted fragmentation theorem

At recursive depth h, use b=3^h, Qsep=q(b-1)/2, R=rqh and P=[b(b-1)]^r. The accepted all-weight separator argument supplies:

- at most r Qsep excluded output row/column coordinates in total;
- same-leaf entry loss at most r N^2/2^h;
- a common refinement with at most P good entry-disjoint rectangles;
- rank at most qh per branch on each good rectangle, hence R for their actual sum;
- good area at least N^2(1-r/2^h)-r Qsep N.

Substitution gives both squared relative-Frobenius and squared operator lower bounds

max(0, 1-r/2^h-(r Qsep+R P)/N).

For bounded q and fixed error tolerance less than one, the accepted consequence is r=Omega(log N/log log N). For fixed r,q the best errors tend to one. It is not an Omega(log N) fixed-positive-error result. The stronger statement assumes the bare additive model and all nonnegative weightings; it is not a replacement for the correction-inclusive theorem under its weaker marking contract.

## Actual predecessor comparison

### HERO0 Phase26 Theorem 26.6: exact missing body recovered

Source: `sources/HERO0_PHASE26_THEOREMS.md`, SHA256 872d5cc65d9dec4a0b09760309ca95964fe289f031f2510cc1f12ba66603dfd8. It is byte-identical to the THEOREMS.md member of the original archive, SHA256 c790508658a55ca935f694451f7927a5da7d8acdefcb6371100569f49e54ebee. The later shared-cut review independently pins the same theorem body.

The actual model is N=s^2, T=(Y_H+Y_V)(X_H+X_V), arbitrary vertical rook matrices and horizontal sums of weighted Hamiltonian Green inverses. Theorem 26.6 requires every horizontal term to use one shared permutation order or its reverse. On oriented siblings of that order's binary tree it obtains

||F_(s^2)-T||_F^2/s^4 >= (1/s^4) sum_(X,A) [s(s-1)|X||A|-s^2(|A|r_Y+|X|r_X)]_+.

Each off-diagonal (x,a) lies in exactly one oriented sibling rectangle. If r_X+r_Y=o(s), the norm lower bound tends to one. The text explicitly says this does not apply unchanged to two distinct stage-specific orders, because a common low-rank sibling partition is then missing.

Thus this is a positive antecedent for disjoint-error summation and a near-unit error floor, but the displayed theorem does not state the F018 all-weight separator theorem for a bare sum of arbitrary independently routed denominators. Conversely, F018's additive theorem does not subsume this two-stage product grammar. The shared-order 1-o(1) result must also remain separate from the later common-bipartition 1/sqrt(2) result.

Disposition: the F018 successor's named Phase26 full-source comparison is COMPLETE as a bounded nonmatch with explicit hypotheses. No need to retrieve or audit that body again.

### STABLE-ARC A1/A2: original mathematics recovered; exact v2 remains blocked

Source recovered from Library: `FFT_STABLE_ARC_SIGNATURE_THEORY_2026-10-11.zip`, library ID libfile_22711a5fa29881918efbdaf3ef7b660f, archive SHA256 40ea2d2101072723fbbb8dc637c33072666f39b57315edda245348f739dfcae8. Original THEOREM.md SHA256 50ae0ea5f9cd099ab8e0d2dc30872dbce663515e541a8ef853cd48be13a15172.

The source has q nonsingular Hamiltonian Green branches with nonzero edge weights and invertible independent monomial endpoints. For n=q+1 consecutive Fourier rows, at most n^q column signature classes C have rank at most q. If G_C=U[R,C]U[R,C]*, its actual diagnostics are

(A1) ||M-U||_2^2 >= max_C lambda_min(G_C),
(A2) ||M-U||_2^2 >= (1/n) sum_C lambda_min(G_C).

The proof of A2 explicitly sums disjoint-column Frobenius residuals and divides by n using the selected row slab. Therefore independently routed common refinement and summed residuals are already present here. They are not new ingredients of F018 fragmentation.

The distinction is precise: these diagnostics work on an n-by-N strip. Fragmentation constructs a family of good cells covering nearly all N^2 entries while keeping every branch's cell rank controlled, for arbitrary flat normalized unitary targets and a larger denominator class. A2 alone cannot give a fixed-q operator floor tending to one: since sum_C G_C=I_n, sum_C lambda_min(G_C)<=1 and its squared certificate is at most 1/n. This does not prove nonimplication by every other STABLE-ARC argument; it identifies the limit of the displayed A2 diagnostic. The A1 eigenvalue diagnostic is retained as a useful partition-specific certificate.

The live STABLE-ARC source row says Theorem A and A1-A5/L were unchanged by editorial v2, but the newly recovered original is not v2. Required exact manuscript hash remains 159ff2e8a081fbff81d977b023b3bce08561ded1b395dd0924a48df3e5802631; exact review ZIP hash is 8f501088cc53117e957de008b50d99967b0f9aac68c134d750047949ca6d685d. Neither exact object was recovered in this pass. Do not substitute the original hash or reopen STABLE-ARC's own already-closed editorial-credit task.

Disposition: mathematical comparison to original A1/A2 is COMPLETE; reviewed-v2 byte binding remains a precise provenance blocker for the F018 comparison successor.

### External fixed-hierarchy comparisons freshly checked

Chen et al., *Near-optimal hierarchical matrix approximation from matrix-vector products*, Definition 1.1 and introduction p.3, fix a recursively halved HODLR hierarchy and describe optimal approximation by separate low-rank approximations on its off-diagonal blocks. This directly credits the disjoint-block optimization principle. It does not state the simultaneous nearly-full-area cover for sums with unrelated branch hierarchies. [Primary paper](https://arxiv.org/pdf/2407.04686).

Govindarajan, Chandrasekaran and Dewilde, TQS v2, Proposition 4.6, compose rank profiles on the same specified acyclic connected graph. The inspected clause requires that common structure; it does not itself construct a common bounded-rank hierarchy after arbitrary independent endpoint routings. No general nonimplication from all TQS theory is claimed. [Primary paper](https://arxiv.org/pdf/2402.13381v2).

## Remaining gate and stopping condition

Do not repeat the historical F018 cutoff proof review or its completed GIRS/TQS comparison. For the distinct fragmentation positioning successor, retrieve only the pinned STABLE-ARC reviewed-v2 body or its exact sealed review archive, compare unchanged A1/A2 against the concrete formulas above, and retain the narrow unmatched simultaneous-area quantifier unless a checked predecessor implication is found. The Phase26, original-A1/A2 and displayed fixed-hierarchy comparisons have finite outcomes now. Global priority remains unresolved regardless of source recovery.
