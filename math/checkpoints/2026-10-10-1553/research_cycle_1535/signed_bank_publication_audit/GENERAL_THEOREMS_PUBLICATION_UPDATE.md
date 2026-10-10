# Publication update after the two general-order proof reviews

10 October 2026. This addendum follows the baseline PUBLICATION_AUDIT.md. It records two subsequent independent proof acceptances without changing the frozen small-order or order-eleven packets.

## Revised strongest framing

The paper can now ask a broader intrinsic question: how many fixed signed-Weyl resolvent parameter configurations are needed to linearly synthesize every operator, and how does adapting the nodes to a special target change that count?

The exact universal answer U_k(N;q)=2N-2, for all odd N>=3 over every eligible field, materially improves the case beyond a collection of small-order examples. Its proof gives an explicit base-field architecture, handles all rows and axes, and proves optimality against every legal fixed architecture. The all-order answer concerns target-independent slots; it must be distinguished from the Fourier minimum, whose nodes can depend on the target.

Recommended title: “Universal and Fourier synthesis by signed Weyl resolvent banks.”

Recommended theorem hierarchy:

1. Sharp fixed universal architecture count U_k(N;q)=2N-2, with no extension field and guards -1.
2. Finite-node boundary example R_N(S^(-1))=N-1 but bank border rank 1 over C.
3. Exact target-adaptive Fourier counts 4,5,8 at N=3,5,7, with the accepted field scope.
4. Fourteen-bank N=11 upper construction and its fixed-order nonempty two-parameter family.

For Fourier matrices the general upper bound improves from 4N to 2N-2; the accepted N=11 example still improves its twenty-bank specialization to fourteen. Nothing yields a general Fourier equality or N=11 minimum.

## Suggested abstract core

We study exact additive representations of operators by phase-weighted resolvent banks of a fixed finite Weyl pair. For every odd order N and every field of characteristic not dividing N containing a primitive Nth root, we determine the minimum number of fixed parameter/sign configurations needed to synthesize all matrices by varying only their phase weights: it is 2N-2. We give an explicit base-field architecture attaining this bound. We also show why finite-node legality matters: the inverse shift has bank rank N-1 but lies in the closure of the one-bank set. For target-adaptive Fourier synthesis over C we determine the exact counts 4,5,8 at orders 3,5,7 and construct fourteen-bank realizations at order 11. The methods combine classical Weyl and moment identities with exact support and compatibility arguments. The results concern representation resources, not Fourier runtime.

## Significance discipline

The universal theorem is the better lead because it answers a natural quantified all-order problem exactly. Its proof is short support and interpolation algebra, so its existence alone does not certify journal significance or historical originality. The Fourier lower-bound obstructions remain valuable because they show what changes when configurations may adapt to a canonical target.

The border example is best used to justify the legal finite-node distinction. After projection, its lower bound is the ordinary Vandermonde independence of finite points on a rational normal curve against the omitted infinite endpoint. The unbounded ratio is mathematically valid but should not be marketed as a surprising gap for a closed projective variety: in the closed scroll dictionary the endpoint is itself rank one.

An additional direct priority trail is now established. Jelisiejew defines rank with an excluded closed set of linear forms, Ork(F,V), and then open Waring rank by taking the supremum over forbidden sets. Ballico defines open X-rank by requiring decompositions avoiding every proper closed subset. These are primary precedents for the restriction-versus-closure distinction, though the four-bank dictionary and fixed universal architecture are separate optimizations. [Jelisiejew, Definition 2](https://arxiv.org/pdf/1305.6957); [Ballico, Definition 1.3](https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/1145/950/4334).

Do not call the framework, common-node interpolation, root-of-unity filtering, or omitted-endpoint phenomenon new. Historical priority of the exact fixed-architecture count and the specialized Fourier classifications remains unresolved. The next priority comparison should examine finite-dimensional resolvent spanning systems, fixed block dictionaries, restricted simultaneous Waring decomposition, and common-node interpolation, with a count-preserving map rather than keyword absence.

## Evidence boundary

The independent review files are in ../signed_bank_architecture_review/. The universal source is bound at c2c30eac3bfcdbd0f7cc2a0c973c56f1821d4326300a1dc1baa2e5f937b273c1; the border source at 791ca8ceeb4851059f73e841f11eeeef2d95f99a5de97ff1618fe4bf3fb75ea8. Both have complete mathematical proof reviews and separate acceptance receipts. No source program or fresh computational verifier was executed by this reviewer. These proof acceptances do not confer historical-priority or publication acceptance.
