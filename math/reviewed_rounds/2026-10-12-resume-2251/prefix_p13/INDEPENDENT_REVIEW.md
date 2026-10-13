# Independent bounded PREFIX review: D8 × C13 × C17

12 October 2026 UTC. Decision: **ACCEPT at the finite scope below**, using the explicitly inherited accepted subgroup theorems. This is an independent project mathematical/computational review, not external peer review or proof-assistant certification.

## Accepted statement

For G = D8 × C13 × C17, of order N = 1768, let T_j be the first j elements of an arbitrary labeled permutation and S_j its left stabilizer. Score all nonempty prefixes, including the full prefix exactly once, by Z = sum_j (|S_j| − 1). Let B be generated only by the proper-prefix stabilizers.

- The unrestricted maximum is **5948**.
- The maximum with full escape B = G is **5506**.
- The sharp deficit is **442**.

The proof combines a sound compatibility-graph upper bound, exact independent graph optimization, actual group witnesses, and the previously accepted abelian/two-Sylow proper-subgroup maxima. It proves one finite pair. It does not prove the p=13 parameter-uniform conjecture, an equality classification or optimizer count, external novelty, an algorithmic speedup, or a Fourier lower bound.

## Mathematical reduction checked

Coprime powering splits every subgroup into its D8 part and central odd cyclic factors. The maximal subgroups have orders 884, 136 and 104 and are normal of prime index. If a nonempty proper prefix is invariant under such a maximal J, every earlier proper prefix has support in a nonempty proper subset of the prime quotient; an outside stabilizer would make that support the whole quotient. Every later proper prefix already contains a full J coset; an outside stabilizer would translate that coset through the whole quotient and fill G. Therefore all proper-prefix stabilizers lie in J, and escape excludes these three stabilizer orders.

For actual stabilizers at positions i<j of orders d,e, put L=lcm(d,e). If the earlier two-part order is at least the later one, saturate the earlier set by the later central odd factor. Otherwise intersect the translates of the later set by the earlier central odd factor. Either construction lies between the two prefixes, is invariant under a subgroup of order L, and has size divisible by L. No nesting of arbitrary D8 subgroups is assumed. Equality at i or j is possible only when L=d or L=e, respectively.

Thus the allowed vertices (j,d), weighted d−1, have an edge exactly when no L-multiple occurs between i and j with those endpoint permissions; distinct types at the same position also conflict. Every escaping permutation gives an independent set with exactly its proper-prefix score. A reverse realization of every independent set is unnecessary.

The reviewer reconstructed this argument from the current candidate and the pinned accepted p=11 review. Its reasoning uses only the stated group structure and applies to the named pair without importing a parameter-uniform graph bound.

## Independent graph computation

The new reviewer program `independent_review.py` does not import or execute any author or predecessor program. It generates absolute-position vertices and all unordered pairs independently. Conflict detection uses a residue-based first-multiple test, rather than the author's implementation. The allowed orders are 2,4,8,13,17,26,34,52,68,221,442.

The exact graph has:

- 1968 vertices
- 1,935,528 pair checks
- 41,901 edges
- maximum independent-set weight **3739**

The reviewer optimizes by a **descending-position grouped dynamic program**. At each position it chooses no type or one legal divisor type. The state is the set of forbidden unprocessed earlier vertices; states with the same continuation restrictions retain their greatest score. Every legal continuation is represented, and merging is exact. This differs from the author's increasing per-vertex shifted-mask recurrence. It uses exact Python integers, reaches 350 peak states and performs 453,372 transitions. Six endpoint controls pass, including the essential period-104 edge (104,8),(208,52).

Adding the full-prefix contribution 1767 gives the escape upper bound 3739+1767 = **5506**.

One reviewer control was corrected during development: an initially labeled “both endpoints forbidden” example actually permitted its left endpoint. The example was replaced by (4,2),(6,3), where both endpoints really are forbidden. This was a test-example error; the graph rule and optimization were unchanged. Final results come from the corrected complete run.

## Independent actual group witnesses

The reviewer realizes D8 as actual permutations of the square and composes those permutations to obtain its multiplication table. This is separate from the author's direct tuple-sign multiplication. It then checks prefix stabilization by maintaining **exact translated-image bitsets**, not the author's pair-difference hit counters.

With D8 encoded by i+4b and odd coordinates C13 then C17, the last coordinate fastest:

- Outer order [0,4,2,6,1,5,7,3] gives score **5948** and |B| = **884**.
- Outer order [0,4,1,5,2,6,3,7] gives score **5506** and |B| = **1768**.

Each witness receives 1768² = **3,125,824** translated-prefix equality decisions. Every one of its 1768 stabilizer sizes matches the author JSON after independent computation. Each stabilizer size divides the prefix size. The proper stabilizers are separately closed under group generation, with the full prefix excluded from B.

A separately computed negative control uses the natural encoded order [0,1,2,3,4,5,6,7]. It has the escape-sized score 5506 but |B|=884, so it is rejected as an escape witness. Score alone is insufficient. These witnesses establish attainment by actual labeled group orders; they are not graph-only search witnesses.

## Unrestricted upper bound and inherited premises

If B is proper, choose a maximal J containing it. Summing the active local-prefix bounds in right J cosets gives [G:J] M(J) + N − |J|. The accepted abelian/two-Sylow subgroup baselines retained in the p=11 review give:

- |J|=884, M(J)=2532: 2×2532+884 = 5948
- |J|=136, M(J)=332: 13×332+1632 = 5948
- |J|=104, M(J)=252: 17×252+1664 = 5948

The escaping case is at most 5506, so the unrestricted upper bound is 5948 and is attained above. The reviewer checked this reduction and arithmetic. The full earlier sealed proof archives for the general subgroup baselines were **not** reaudited; they remain explicitly inherited accepted premises, rather than newly proved results.

## Source and scope

Pinned repository source: AgentSlop-Si/research, commit 95419a2bd5d0bf6d3b78747bf163a62a7b9e4b5d, `math/reviewed_rounds/2026-10-12-prefix-p11-uniform/prefix-p11-uniform.md`, SHA-256 904de3c19294d7a30dac0694d0fae7670519277a0c9401829fbe9307b18789f9.

The current candidate is `REPORT.md` with its exact computation in `p13_r17_check.json`. The reviewer result binds that candidate JSON and its own source by SHA-256 in `INDEPENDENT_REVIEW_RESULTS.json`. Complete independently computed stabilizer profiles are retained there. `independent_review_run.log` records the final successful run.

The next parameter-uniform p=13 target would need alpha≤226r−103 for every prime r>13, with matching unrestricted 356r−104 and escape 330r−104 values. One verified pair supplies no such induction. Both-prime-variable bounds, full-escape optimizer classification/count, EFK source gaps, historical priority and every practical/asymptotic speed claim remain open.
