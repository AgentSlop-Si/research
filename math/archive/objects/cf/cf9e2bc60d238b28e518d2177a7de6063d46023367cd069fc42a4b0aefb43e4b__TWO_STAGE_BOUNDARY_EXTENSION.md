# Boundary windows sharpen the complete two-stage exclusion

Independently derived 9 October 2026 UTC during review of v17. The paired constructor independently checked the proof and supplied additional exact controls. This is a restricted factorization theorem, not an unrestricted arithmetic lower bound or a publication-novelty claim.

## Theorem

Let T=S2 P S1, where S1 and S2 have quasiseparable orders at most r1 and r2 in their natural stage coordinates. Let R=r1+r2 and W=floor(N/2). Suppose both target blocks T[I,J0] and T[I,J1] have rank W, where

I=J0={0,...,W−1}, J1={N−W,...,N−1}.

Then N<=4R+1. Therefore two order-one stages cannot equal Fourier for N>=10 whenever either Fourier endpoint is affine-coprime and the other is arbitrary. Over C, at prime lengths N>=11, the same exclusion holds with both endpoint permutations arbitrary. Arbitrary invertible diagonal endpoint scales are allowed.

No invertibility of a stage or principal subblock, nonzero generator, adjacent minor, or genericity assumption is used. The statement applies to the full quasiseparable class, including singular/zero-transition branches.

## Proof

For either boundary input set J, split the product into three terms:

T[I,J] = S2[I,I] P[I,J] S1[J,J]
 + S2[I,I] P[I,Jc] S1[Jc,J]
 + S2[I,Ic] P[Ic,:] S1[:,J].

The last two terms have rank at most r1 and r2 respectively, because I and J touch endpoints and each has only one exterior side. The first has rank at most rank P[I,J]=|I intersect p(J)|. Consequently

rank T[I,J] <= R+|I intersect p(J)|.

The two input boundary windows J0,J1 are disjoint since 2W<=N. Their mapped sets are disjoint, so the two overlaps with I sum to at most W. At least one overlap is at most floor(W/2). The assumed full target ranks therefore imply

W <= R+floor(W/2),

so ceil(W/2)<=R, equivalently W<=2R. As W=floor(N/2), this is N<=4R+1.

For a natural Fourier output prefix, any W distinct selected columns are distinct Vandermonde nodes, so both blocks have rank W regardless of input endpoint permutation. Affine output indexing with a unit slope changes only the primitive root and column phases. Transposition handles the opposite endpoint convention. These arguments hold over any field with a primitive Nth root.

For arbitrary endpoint permutations at complex prime length, Chebotarev's full-spark theorem supplies both full-rank blocks. A primary statement/proof is Tao, Lemma 1.3, pp.3–4, https://arxiv.org/pdf/math/0308286 . This extension does not assume full spark at composite lengths or over arbitrary finite fields.

## Evidence and relation to earlier gates

The new independent checker in this directory tests 120 actual two-stage products at N=10,11,16,31 with randomly chosen permutations, full transition-generator stages, zero transitions and a diagonal-stage control. It verifies a selected boundary block has rank at most R+overlap<W while the corresponding Fourier block has full rank. This includes the exact N=10 threshold.

The paired constructor separately verified 1,980 matrix bounds and the exact three-term decompositions at N=3,...,20 and orders (0,1),(1,0),(1,1),(2,1),(1,2), plus 46,232 exhaustive permutation overlap checks for N=2,...,8 and 12 Fourier boundary controls including N=10 over F_241. Those files are in the separate constructor research directory; they are corroboration, not code imported by this reviewer.

The previous master retained an existential two-stage cutoff N>=17 and a later three-sparse explicit witness at N>=18 under their stated endpoint hypotheses. This direct boundary argument improves the existential exclusion to N>=10. It does not automatically give a three-sparse mismatch input: a rank-deficient selected block supplies a mismatch by linear algebra, and locating that vector has its own cost.

The v17 generic prime N>=31 theorem is subsumed, with stronger size and parameter-domain coverage. Small lengths N<=9 are not certified feasible by this necessary bound.
