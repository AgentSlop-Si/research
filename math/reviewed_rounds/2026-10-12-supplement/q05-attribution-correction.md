Publication derivative of an independently reviewed research report. Private tracking and delivery details are omitted; mathematical attribution, assumptions, costs and remaining work are preserved. Original dated source-report SHA-256: ac064dcbc1f44b988a0c4ce9d97f3717a7028f16a4a01be794b55ac05c004d46.

# Independent review of the Q05 prior work bridge

Verdict: ACCEPT the attribution correction for the frozen candidate. The matching upper and its full cut profile are elementary consequences of the earlier dual-subgroup-flag construction. No mathematical correction to the accepted Q05 equality is required. Independent novelty credit for the upper ordering should be removed; worldwide priority of the full equality and its universal lower remains unresolved.

Reviewed 12 October 2026 UTC. The candidate checker was read as inert text, never executed or imported. All new computation uses the independently written checker.

## Frozen target and verification

- Candidate archive: Q05_Dual_Flag_Prior_Work_Bridge_2026-10-12.zip
- Candidate SHA-256: 2dd4bb923c6331ae79bbaf76a736df61181d3a21a7f862311f7df06ea2e1b11f
- Candidate manifest SHA-256: af4728598b5a8e355ef5f87b3001606d700aaae5ba01fbdc69ba824493050943
- Candidate BRIDGE.md SHA-256: b9e9163e4c62f93aaa9d5b43db1547afc03f8c290d2057b55485528823dd691a
- Candidate REPORT.md SHA-256: c6475d1bb6c03aae4db813693db0f7a781e1086f1ef037086c07f508edba9f3c

All 13 manifest-listed members were checked against their recorded sizes and hashes and against the live candidate directory. All six project-source bindings were also freshly checked. The accepted mathematical proof and its prior independent verdict were read. The preceding endpoint-priority report and final-2008 comparison were examined as chronological project evidence, not substituted for fresh primary-source inspection. The final cold read repeated all candidate member and project-input checks.

## Primary text and version distinctions

The decisive source is [Delvaux and Van Barel, TW477, November 2006](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW477.pdf). Fresh text inspection confirmed Lemma 11 on printed pp. 10–11/PDF pp. 12–13, and Lemma 12 with proof on printed p. 11/PDF p. 13. The latter proof explicitly selects arbitrary subgroup flags and annihilator flags for independent coset-sortings. Remark 13 identifies digit reversal in the cyclic case. Theorem 20 and Corollary 21 on printed pp. 17–18/PDF pp. 19–20 give the same-order Hamming-profile transfer used below. TW477 is the preprint of the 2007 Kronecker-product paper, not of the 2008 single-Fourier paper. Final-2007 body and numbering were not independently verified; the accessible 2006 text suffices for the earlier construction.

The [final 2008 article](https://doi.org/10.1016/j.laa.2008.04.043), LAA 429, 1587–1605, was independently read on PDF pages 1 and 7–13. Its Eq. (15) is on printed p. 1594, with setup on p. 1593; Definition 6 is on p. 1594; Lemma 7 is on p. 1596; Theorem 9 is on pp. 1598–1599; Remark 10 is on p. 1599. Its rank-one hierarchy is cyclic prime-power. Theorem 9 concerns one nonzero supported vector, not prescribed nullity. Its interval parameters cover d<N; H_F(N)=1 is the separate trivial endpoint. No fresh final-PDF byte hash is claimed. TW470 retrieval failed in this pass, so its previously recorded Lemma 8/Theorem 10 numbering is inherited rather than freshly certified here.

Fresh primary inspection of [Pernet and Storjohann, arXiv 1701.00396v2](https://arxiv.org/pdf/1701.00396), Definition 1, PDF p. 2, confirms that Q05's q is the maximum of the two quasiseparable orders. The unversioned URL returned the version visibly marked v2, 21 October 2019. The versioned URL initially had a cache miss. No new invariant claim is warranted.

Primary inspection was textual. The TW477 screenshot tool returned no usable image; this report makes no visual-page inspection claim. No full third-party primary text is bundled.

## Mathematical bridge review

The independent proof in INDEPENDENT_BRIDGE.md establishes every substantive step of the candidate without relying on the finite controls:

1. Binary representatives of any index-two subgroup flag and its reversed dual flag give permitted endpoint permutations, including mixed cyclic factors and representatives with higher order.
2. The quotient pairing (X_(m−1)/X_1) × (Y_(m−1)/Y_1) is perfect and has order N/4 on both sides.
3. At cut k≤N/2, outside columns span exactly the kernel of the complete row-pair sums. Its dimension is ceil(k/2).
4. After quotienting, the remaining column suffix starts at floor(k/2), even at odd cuts because the second member of the partial column pair survives.
5. Transposition proves the other orientation's recurrence. Simultaneous binary complementation supplies reflection. Equality of both profiles follows inductively, without assuming the two endpoint orders coincide.
6. Bases N=1,2,4 and the attaining cut N/2−1 for every N≥8 are correct. The recurrence is used only for N≥4, and endpoints have rank zero.
7. The accepted isotropic recursion produces a self-dual flag, so it is a specialization of the older independent dual flags.

The conclusion is deductive: neither the endpoint recurrence nor the minimax objective is being misquoted as a printed theorem in TW477. The older construction plus elementary character independence and rank bookkeeping already gives the complete uniform upper. Thus the completed project obligation remains useful and correct, while separate historical credit for discovering that upper is not supported.

## Lower bound and remaining priority

For N=4L≥8, a hypothetical critical (2L−1)×(2L+1) rectangle of rank at most L would yield a supported nonzero dependence of size at most L+1. Applied to the matrix and its transpose, the direct Hamming tests require H_F(L+1)≤2L+1 and H_F(L+1)≤2L−1. The earlier dyadic profile gives H_F(L+1)=4. At N=8 the second inequality is impossible, establishing the lower for every abelian group of order eight via TW477 Corollary 21. For N≥16 neither direct test contradicts the hypothetical rank. Final Remark 10's equality hypothesis is not met at these complement sizes.

This checks the candidate's exact limited assertion. It does not prove that stronger consequences of the older papers, generalized support weights, or other literature cannot imply the larger-size lower. Preserve the universal critical-rectangle lower as the remaining model-matched comparison obligation. Preserve the accepted overlap-sensitive rank/gap estimate separately, with its existing classical antecedents and unresolved global priority.

The accepted minimax remains 0 at N=1, 1 at N=2,4, and N/4+1 at N≥8 for all finite abelian 2-groups in characteristic zero. The half-square minimum N/4 is a different statement. No all-size minimal rank-sum claim, positive-characteristic universal lower, stronger approximation result, nonabelian/mixed-prime result, or FFT/circuit/runtime consequence is created.

## Independent regression evidence

The fresh checker enumerated all subgroup flags for every abelian group type of orders 1,2,4,8,16, then sampled five flags for every type of orders 32 and 64. It independently selected row and dual-column representatives and computed all corner ranks over GF(193), distinct from both author fields.

- 30 group types and 512 flag pairs
- 23,222 corner-rank computations including empty endpoints
- 2,297,033 exact multiplicative identities verifying the complementary rank-one block grids
- Every corner profile, both orientations, reflection, base case and maximum matched the proof
- The naive C2×C4 factorwise ordering retained middle rank 4 rather than the achievable 3

These finite-field computations are regression checks of the algebraic construction. They neither prove its uniform scope nor establish a finite-field minimax lower or any singular-value bound.

## Scope and remaining work

This corrects attribution for the existing Q05/C02/TH-05 result without changing accepted mathematics or creating a new theory.

Accepted conclusion:

"The exact independent-endpoint minimax is accepted for every finite abelian 2-group: 0,1,1 at N=1,2,4 and N/4+1 for N≥8. Its matching upper and common cut profile follow by elementary rank bookkeeping from Delvaux–Van Barel's TW477 Lemma 12 dual flags. The symmetric isotropic recursion is a self-dual specialization. The N=8 lower is already a Hamming-profile corollary; historical priority of the accepted universal N≥16 critical-rectangle lower and full minimax equality remains an unresolved comparison question."

The general-group upper comparison is resolved as a classical corollary. Historical priority of the accepted universal N>=16 lower and full minimax equality remains unresolved. Original dated reports are preserved; this later correction supersedes their attribution only.

See [the independent dual-flag proof](q05-dual-flag-proof.md) and [the earlier dated minimax report](../2026-10-12-reviewed-research/q05-noncyclic-minimax.md). The earlier report remains unchanged.

Editorial clarification, 12 October 2026: the remaining question above concerns historical attribution. The universal lower bound and minimax equality remain mathematically accepted. The original reviewed source report is unchanged.
