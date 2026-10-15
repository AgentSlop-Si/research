# M-TREE-WITNESS: bounded primary-source comparison

Date: 2026-10-15  
Repository baseline: AgentSlop-Si/research, commit 21aac668f52b5680b8b22eb99d53a850ae0cd394  
Owner: Catalogue!A31:AF31; Research overview!A43:Q43, stable ID M-TREE-WITNESS  
Disposition: bounded witness clarification complete; wider owner comparison OPEN; Q04 previously complete and unchanged.

## Outcome

The accepted tree family has exact directed TQS edge ranks 1 toward the parent and 0 toward the child, over every field and every nonzero α. It and its inverse are GIRS-1 on the original tree, while their optimized independent-row/column separation rank grows with height. This is a precise model clarification, not a new representation framework or priority claim. The wider owner task remains OPEN: the branch-specific correction-compatible author manuscript was recorded as recovered previously but was not located and re-read in this pass.

## Evidence boundary

The existing owner rows were read in [the research Sheet](https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit). Repository sources were pinned to the commit above. The original THEOREM.md, CONDITIONING_COROLLARY.md, both accepted audits and the reviewed-candidate manifest were read. No numerical, program or formal-proof replay was performed. Previously recorded check counts remain historical evidence. The source proof audit already records the TQS §3.5 specialization and disclaims resolution of a published TQS problem; those findings are not newly discovered here.

## 1. Accepted model and independent orders

Let T_h be the perfect rooted binary tree with N=2^(h+1)−1 vertices, P[parent,child]=1, Qα=I−αP, and Bα=Qα⁻¹. For independent row and column prefixes R_k,C_k, sr(A) minimizes over both orders the maximum of rank A[R_k,C_kᶜ] and rank A[R_kᶜ,C_k]. The accepted result is

floor((h+1)/4) ≤ sr(Bα)=sr(Qα) ≤ h

for every field and α≠0.

Complementary nullity gives rank A⁻¹[I,J]=rank A[Jᶜ,Iᶜ]+|I|+|J|−N. Consequently the inverse order pair must be swapped:

- rank A⁻¹[C_k,R_kᶜ]=rank A[R_k,C_kᶜ];
- rank A⁻¹[C_kᶜ,R_k]=rank A[R_kᶜ,C_k].

This requires neither equal row/column orders nor invertible principal submatrices. The accepted all-field proof supplies these algebraic statements. The [original Vandebril–Van Barel PDF](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf) and a primary-paper mirror timed out this pass, so no fresh full-paper inspection is claimed for that source.

## 2. Exact original-tree edge map, derived here

For any nonroot child v, let S be its descendant subtree and p its parent. Qα[V∖S,S]=−α e_p e_vᵀ has rank 1, whereas Qα[S,V∖S]=0.

Since Bα[a,b]=α^dist(a,b) exactly when a is an ancestor of b, Bα[V∖S,S]=f gᵀ, where f(a)=α^dist(a,v) for ancestors a of v outside S and 0 otherwise, and g(b)=α^dist(v,b) for b∈S. Its (p,v) entry is α, so its rank is 1; the reverse block is zero.

Direct TQS states make the field scope explicit:

- For Qα, send h_v=−αx_v from each nonroot v to its parent, and output y_v=x_v+Σ_children h_child.
- For Bα, use h_v=α(x_v+Σ_children h_child), with the same output formula.

No downward state is required. A cut-factorization lower bound makes these dimensions minimal: child→parent 1, parent→child 0. For h=0 there are no edges and Qα=Bα=I. These coordinate block formulas avoid an apparent index-transposition inconsistency in the printed TQS unit-Hankel definition.

## 3. GIRS and final TQS comparison

GIRS §2.1 Definition 1 and Propositions 2.1–2.3 give a graph-boundary cut-rank property and inversion closure. Qα is GIRS-1 on T_h by its sparse edge support; complementary nullity gives the same property for Bα. For h≥1 the constant is minimal because an edge cut has rank 1. Applying this conclusion over arbitrary fields uses the explicit algebra above, rather than silently broadening the paper's real-field setup. GIRS §2.4 Definition 3 additionally requires a Hamiltonian path for that paper's G-SS representation. T_h has none for h≥2, because a tree with a Hamiltonian path must itself be a path. Thus that definition cannot be applied to the branching tree. [GIRS v3](https://arxiv.org/pdf/1911.05858v3)

In the final TQS paper, §3.5 is exactly specialized by k=h+1, postorder indexing, d^v=1, b^(child,parent)=−α and p^(parent,child)=0. This overlap was already recorded in the accepted audit. Theorem 4.4 identifies minimal edge-state dimensions with unit-cut ranks, Corollary 4.5 relates the maximum profile to tree GIRS, and Proposition 4.8 handles inversion with square node blocks. The direct states above establish the needed all-field special case without importing the SVD-based proof's field scope. Constant tree-edge ranks and unbounded optimized linear-layout sr are compatible; they measure different cuts. The fixed-order storage discussion in §3.5 does not establish optimal storage over all orders. [Final TQS paper, SIMAX 46(2), 1562–1586, 2025](https://repository.tudelft.nl/file/File_6b7549c8-222e-4316-8ac4-a113d7d4da1e)

## 4. Lift, half-component normalization and conditioning

The scalar bipartite support lift has row vertices ρ_v and column vertices γ_v. Each nonroot γ_v subdivides its original parent edge, and γ_root is pendant. It is a subcubic tree. Contracting diagonal edges recovers T_h; the accepted forest matching-rank/interleaved-layout argument, together with forest linear rank-width=pathwidth, gives the sr lower bound. The inherited treewidth separator allowance q=2 remains unchanged. Adler–Kanté Theorem 2 and the binary-tree pathwidth discussion are the classical graph inputs. [Linear Rank-Width and Linear Clique-Width of Trees](https://perso.isima.fr/~makante/articles/kanteA13.pdf)

The weighted-separator statement in §2.1 preceding Lemma 2.1 of Bodlaender et al. bounds every remaining component by one half of the original total nonnegative vertex weight, with separator size at most treewidth+1. The routed marked row/column sets must determine the weight at each application. Lemma 2.2's algorithmic 2/3 balance is not interchangeable with this hypothesis. [A c^k n 5-Approximation Algorithm for Treewidth, author version](https://sites.cs.ucsb.edu/~daniello/papers/treewidthApproxJ.pdf)

For the symmetric lift H=[[0,Qα],[Qαᵀ,0]], H⁻¹=[[0,Bαᵀ],[Bα,0]]. External inverse rows select the γ half and columns the ρ half. If A,B,X partition the lift and H[A,B]=0, complementary nullity gives rank H⁻¹[A,B]≤|X|, without invertible principal-block assumptions. Each independently routed branch has its own mapped sets. This single-branch calculation does not by itself select a simultaneous common rectangle or specify correction quantifiers for multiple branches; no claim about that unread author interface is added here.

With D[v,v]=α^(−depth(v)), Qα=DQ1D⁻¹, so all exact submatrix ranks are preserved for every nonzero α over every field. Conditioning is separate: over C and real 0<α<1/√2, PP*=diag(2 on internal vertices,0 on leaves) for h≥1 gives

κ₂(Qα)=κ₂(Bα)≤(1+α√2)/(1−α√2).

At α=1/2 this is 3+2√2<6, uniformly in h. At h=0 the condition number is 1. This says nothing about fixed-tolerance numerical ranks.

## 5. Separate frame comparison

Qα is already a frame matrix because each column has at most two nonzero entries. In Nelson–van Zwam §2, the graph representation uses links for two-entry columns and an unbalanced loop for a singleton. The singleton-loop convention has an exception over GF(2); Proposition 2.1 can add a parity row, but that changes dimensions and cannot silently alter the square physical matrix model. [On the existence of asymptotically good linear codes in minor-closed classes](https://www.math.uwaterloo.ca/~apnelson/asympgood.pdf)

Zaslavsky §2.1 instead permits a canonical half-edge vector for a singleton, so the root column has a direct all-field interpretation; Theorem 2.1 and equation (2.2) explain the classical gain-graph dependence mechanism. [Biased Graphs IV: Geometrical Realizations, author version](https://people.math.binghamton.edu/zaslav/Tpapers/bg4.pdf)

The inspected frame/matroid clauses do not themselves state the accepted independent-order sr bound, its conditioning, or the routed correction theorem. Invertible Qα has the free column matroid, just as I does; general row equivalence therefore loses the relevant physical row-submatrix ranks. It need not preserve independent-order sr, the original bipartite separator structure, or the scalar inverse grammar. Only explicitly justified transformations, such as the displayed diagonal scalings, may be transferred here.

## 6. Remaining source gate and disposition

The historical source record identifies the recovered correction-compatible manuscript by SHA-256 79a5f64c11c47e39eb1fe90f7f6d51743dc9e4f1a9d89a5c505ce17835a86c0f. Its exact body and the historical P2126 report were not found in the pinned archive index, bounded GitHub tree/text searches or Library filename searches available this pass. This is a current reinspection access limitation, not a reversal of the recorded earlier recovery. The original short receipt remains the separately recorded export-identity qualification.

Keep the owner status OPEN and score 42. Leave Q04 complete, all accepted scope/limitations and historical priority unresolved. The useful increment is the exact directed profile and model-preserving source map. No claim of reverse class containment, optimal SSS/HSS storage, fixed-tolerance numerical-rank lower bound, published-open-question resolution, general FFT lower bound or worldwide novelty is made.

## 7. Pinned author and audit sources

The following are author/review artifacts, not third-party full-paper reproductions. Hash labels below are recorded provenance; this pass did not run a fresh checksum computation.

- [Original THEOREM.md](https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/e2/e2b4f2e4f760e15e5b33dc88f6021d6ec84c340a096e8584ed8d5f4104cb3cbb__THEOREM.md). Recorded candidate SHA-256 e2b4f2e4f760e15e5b33dc88f6021d6ec84c340a096e8584ed8d5f4104cb3cbb.
- [Original CONDITIONING_COROLLARY.md](https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/2e/2e5a6acf2a868e24e4a582aec6ee5ca8963dcf5d1f81af509129972e980b8f0e__CONDITIONING_COROLLARY.md). Recorded SHA-256 2e5a6acf2a868e24e4a582aec6ee5ca8963dcf5d1f81af509129972e980b8f0e.
- [Accepted PROOF_AUDIT.md](https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/4d/4d66a0e697458f18016e7d6b54eb479b2213bdf11da061e7742977986821fbe9__PROOF_AUDIT.md). Recorded original SHA-256 4d66a0e697458f18016e7d6b54eb479b2213bdf11da061e7742977986821fbe9; attribution-normalized export SHA-256 97fceb6ebf4227c2e426a9771f413e01871b8d26bc63b01e945b69c34326a29b.
- [Accepted CONDITIONING_AUDIT.md](https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/02/0286fa16a796d30ee18f0cd3126a0439e45156d26f6b8ad181fbd72d2b4136ea__CONDITIONING_AUDIT.md). Recorded original/export SHA-256 0286fa16a796d30ee18f0cd3126a0439e45156d26f6b8ad181fbd72d2b4136ea.
- [Reviewed-candidate identity manifest](https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/archive/objects/c0/c08b26f471caec8d012e356d0a15950a923d76637935c63a6e2fb46ce9055fc3__CANDIDATE_REVIEWED.sha256).
