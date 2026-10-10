# A four-stage collapse obstruction for low-crossing middle permutations

9 October2026UTC. This is an independently derived scoped extension of the approved three-stage discrepancy theorem. It does not modify the frozen earlier milestones.

## Definition

For a permutation Q of {0,...,N-1}, define

v_Q(t) = #{0<=i<N-1 : exactly one of Q(i),Q(i+1) is <t},
kappa(Q) = max_{1<=t<N} v_Q(t).

Thus v_Q(t) counts the changes between membership and nonmembership in Q^{-1}([0,t)) along the original natural line. It is also the number of edges of the permuted natural path crossing thresholdt.

## Conjugation lemma, including zero/degenerate cases

If S has upper and lower quasiseparable cut ranks at most r, then Q S Q^{-1} has both quasiseparable orders at most kappa(Q)*r.

Proof: at a fixed target cut let A=Q^{-1}([0,t)), B=A^c. Split A into its maximal natural intervals. For each such interval I, the block S[I,B] has rank at most r times the number of its nonempty exterior sides: one at a natural endpoint, two in the interior. Stacking these row blocks gives rank(S[A,B]) at most the sum of these budgets. That sum is exactly the numberv_Q(t) of A/B boundary changes. Repeating for B gives the same bound on S[B,A]. This uses only actual rank inequalities, with no generator normalization, invertibility or nonzero-transition assumptions.

The same lemma follows from a scalar-state cut in the scan realization: remove the state channels at each membership boundary. The matrix proof above also applies directly to higher quasiseparable orders without a particular scan parametrization.

## Exact collapse of four stages

Suppose

F_N = S4 P3 S3 Q S2 P1 S1,

where Sj has quasiseparable order at most rj. Define

T = S3 (Q S2 Q^{-1}).

Same-coordinate quasiseparable ranks are subadditive under multiplication, so T has order at most

r_T = r3+kappa(Q)*r2.

The factorization is therefore exactly

F_N = S4 P3 T (Q P1) S1.

Apply the approved three-stage discrepancy theorem. With natural Fourier endpoints it implies

D_grid(P3^{-1}) <= 2r1+r_T+r4,
D_grid(Q P1) <= r1+r_T+2r4,

and hence each right side is at least c log N-2 for an absolute c>0. If at least one Fourier endpoint is affine with coprime stride, the corresponding one of the two inequalities still suffices. At prime complex lengths, full spark permits both endpoint permutations arbitrary.

Consequently a four-stage family with bounded r1,r2,r3,r4 and bounded kappa(Q) cannot represent the growing Fourier family under those endpoint conditions. More quantitatively, if r2 is fixed positive and the other orders are bounded, kappa(Q)=Omega(log N) is necessary. If r2=0, middle conjugation contributes no off-diagonal rank and the collapse is immediate without any condition onQ.

There is also the opposite exact merge: T_left=(Q^{-1} S3 Q)S2, giving F_N=S4(P3 Q)T_left P1 S1 and order at mostkappa(Q^{-1})r3+r2. Thus, when all four orders are bounded and the two middle orders are positive, BOTH kappa(Q) and kappa(Q^{-1}) must beOmega(log N). A fixed small affine multiplier or its inverse cannot evade the result merely by reversing its orientation.

This is a necessary representation condition. It does not prove that a permutation with growing kappa yields compatible Fourier coefficients. It is not a general four-stage exclusion or an unrestricted arithmetic-operation lower bound.

## Fixed small affine multipliers are eliminated

Let Q(i)=a*i modN, with fixed positive integer a coprime toN. For each thresholdt, its preimage is the union, over k=0,...,a-1, of the integer intervals satisfying

kN <= a*i < kN+t.

There are at mosta such intervals, and the first nonempty one starts at coordinate0. Their membership changes number at most2a-1. Therefore

kappa(Q)<=2a-1,
rank_QS(Q S Q^{-1}) <= (2a-1)r.

For the current candidate A3(i)=3i modN at dyadic lengths, kappa(A3)<=5. Thus its four rank-one stages collapse to three stages of orders at most(1,6,1). The discrepancy theorem excludes an all-growing-size exact R-A3-R construction even though the selected finite capacity tests through8192 did not reject it.

This corrects the construction roadmap rather than the correctness of those finite tests: passing a finite family of rank tests never certified asymptotic viability. Replacing3 by another fixed odd multiplier cannot repair this specific obstruction. A multiplier or another middle permutation whose natural-path crossing count grows at least logarithmically is needed before investing in exact coefficient synthesis.

## Charged-computation caution

The original four-stage word can have a linear supplied-generator application schedule even when its collapsed middle matrix has growing quasiseparable rank. Replacing that executor by a generic high-rank scan can increase its cost. Thus the rank-collapse theorem rules out bounded-order representations for bounded-kappa middle layouts; it must not be paraphrased as a lower bound for every optimized evaluator of a growing-rank matrix.

## Concrete next question

The binary Gray permutation Q(i)=i xor(i>>1) has a growing threshold-crossing count, unlike a fixed small multiplier. The already tested R-Gray-R word survives the particular prefix-suffix probes through2048, but that remains finite routing evidence. Its precise next target is the complete exact four-stage system: U,V,W and Z=Q^{-1} W R U F_N V R must all be order-one quasiseparable, with det(U)det(V)det(W) nonzero. A useful construction must produce uniform coefficients and their charged preparation, rather than only more numerical fits.
