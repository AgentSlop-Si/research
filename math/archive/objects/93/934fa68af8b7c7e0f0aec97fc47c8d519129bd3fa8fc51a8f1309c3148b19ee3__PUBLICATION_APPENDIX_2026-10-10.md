# Publication update after the audited tree witness

Assessment dated 10 October 2026 UTC. Prepared by dot.

This separately sealed appendix updates the 05:38 assessment after acceptance of the binary-tree witness and its conditioning corollary. The original assessment remains unchanged. It records a publication judgment, not a new correctness audit, authorship certification or novelty clearance. The new results are outside checkpoint 26; this appendix changes no registry or corpus disposition.

## Updated verdict

**A's internal non-containment gate is now closed.** There is an explicit column-two inverse family with tree lifts, bounded row degree and uniformly bounded spectral condition number whose optimized two-sided ordered separation rank grows as Θ(log N), even after independent row and column reorderings. This removes the earlier possibility that the whole admissible class might already have a uniform constant ordered-separation bound.

That materially improves A's coherence as a short structural note. It gives a concrete reason to use weighted vertex separators rather than a fixed ordered-rank premise. It establishes coverage beyond every fixed ordered-separation budget; it does not establish a proper-superset relation between the two complete matrix classes, since reverse containment has not been proved.

**The external novelty increment is narrower.** The all-order witness follows by a short elementary bridge to classical forest pathwidth/linear rank-width, together with inverse-rank preservation and forest matching ranks. The tree-versus-sequential motivation and a binary-tree family containing this specialization already appear in the 2025 TQS paper. No inspected primary source explicitly states the same optimized independent-axis lower bound, but its derivation is close enough to established results that it should be presented as an attributed supporting proposition, not a separate breakthrough.

The ranking by substantive paper potential remains **B first, A second**, with a smaller gap. B combines local coefficients and two arithmetic consequences. **A is now the cleaner near-term short-draft candidate**, because its specific internal strictness objection has been resolved. Neither candidate is cleared for an originality claim. B's two older full-text checks remain outstanding and were not revisited here.

## Exact accepted addition

Let T_h be the complete rooted binary tree of height h and N_h=2^(h+1)−1. Define P_h[u,v]=1 when u is the parent of v. For Q_h=I−P_h and B_h=Q_h^(-1), the independently optimized two-sided parameter satisfies, over every field,

    floor((h+1)/4) ≤ sr(B_h)=sr(Q_h) ≤ h.

Here sr minimizes over independent row and column orders the maximum rank of both cut blocks A[R_k,C_k^c] and A[R_k^c,C_k]. This is precisely the inherited separation-rank parameter. The inverse has entry 1 on ancestor–descendant pairs and 0 elsewhere. Q_h has at most two nonzeros per column and three per row; its bipartite lift G_h is a subcubic tree. Thus the accepted separator theorem has the fixed budget q=2 on this family.

Over C, replace Q_h by Q_(h,α)=I−αP_h for 0<α<1/√2. The same exact ranks hold, while

    κ₂(Q_(h,α))=κ₂(Q_(h,α)^(-1))
      ≤ (1+α√2)/(1−α√2).

At α=1/2 this is 3+2√2<6, uniformly in h, with coefficients in {0,1,−1/2}. This rules out ill-conditioning as a necessary explanation for the exact-rank obstruction. It does not bound numerical separation rank at a fixed tolerance: ancestor entries α^distance can be very small.

The main theorem's historical “audit pending” wording is superseded by PROOF_AUDIT.md's explicit acceptance; the conditioning extension has its own separate acceptance. Both were read directly for this assessment. No mathematical program was executed.

## What the literature comparison establishes

### A short corollary after the independent-order bridge

Adler–Kanté's Theorem 2 proves that a forest's linear rank-width equals its pathwidth, and the same paper records pw(T_h)=ceil(h/2). These are established theorems, not contributions of this project. [Primary manuscript](https://perso.isima.fr/~makante/articles/kanteA13.pdf).

The project's extra connection is explicit and short: interleave any independently ordered row and column vertices of Q_h. At even cuts, graph cut rank is the sum of the two matrix cut ranks; at odd cuts it increases by at most one. Forest support makes all relevant weighted matrix ranks equal to matching size and hence to binary support ranks. Therefore

    lrw(G_h) ≤ 2 sr(Q_h)+1,
    2 sr(Q_h)+1 ≥ pw(G_h) ≥ pw(T_h)=ceil(h/2).

Classical complementary-rank identities transfer the result to the inverse, with row and column orders swapped. Depth-first ordering gives the upper bound. This is my assessment of the derivation: the conclusion is a direct corollary once that elementary bipartite bridge is supplied. “Immediate from Adler–Kanté” alone would omit a necessary independent-order and field-transfer argument; “new graph-width theory” would overstate it.

The broader link is already explicit in *Twin-Width V*: its related-work discussion connects adjacency-matrix quasiseparable order with linear rank-width. That passage does not itself handle independent matrix-axis orders. [STACS 2023 primary paper, p.6](https://drops.dagstuhl.de/storage/00lipics/lipics-vol254-stacs2023/LIPIcs.STACS.2023.15/LIPIcs.STACS.2023.15.pdf).

### The close TQS precedent

Govindarajan–Chandrasekaran–Dewilde's final §3.5 already uses regular binary-tree matrices to compare tree and sequential/hierarchical representations in a specified ordering. The displayed bidirectional family specializes to Q_(h,α) by choosing diagonal 1, one directional edge family 0, and the other −α. Tree inverse-rank preservation is also established there. The final footnote discusses combinatorial ordering search; the older preprint's unknown-optimum remark must not be presented as a current published open problem. [Final 2025 text, §3.5 and Proposition 4.8](https://repository.tudelft.nl/file/File_6b7549c8-222e-4316-8ac4-a113d7d4da1e), [2024 preprint §3.5](https://arxiv.org/pdf/2402.13381v2).

The candidate certifies logarithmic **maximum scalar cut rank** across all independent orders for this directed specialization. It does not determine optimal total generator storage or an exact optimal ordering, and HSS permits hierarchical structure beyond linear cuts. The generic bidirectional family's bipartite lift contains four-cycles, so the forest proof does not directly apply to it. No TQS optimal-storage or published-open-question resolution is claimed.

## Revised publication gate

1. **Remove the internal strictness task from the remaining gate.** It is settled by the audited witness, including the stronger conditioning corollary. Use the precise non-containment formulation above.
2. **Keep A centered on the independently routed separator-sum theorem.** Place the tree witness immediately after it as motivation and a scope proposition. Credit Adler–Kanté, nullity theory and TQS beside the argument. Avoid spinning the witness into an independent paper solely because it closed an internal question.
3. **Check application-level priority next.** The remaining question is whether an earlier matrix/graph-width or structured-sum result already yields the independently routed flat-unitary obstruction. Follow the TQS, GIRS, quasiseparable and graph-layout citation paths, including independent row/column permutation formulations. A failed exact-phrase search does not answer this.
4. **Retain every boundary.** No new FFT algorithm, general arithmetic lower bound, fixed-tolerance numerical-rank theorem, optimal SSS/HSS storage result, or sharp exact value of sr follows. Uniform conditioning does not change those boundaries.
5. **Proceed with private exposition; seek external evaluation only if authorized.** A is better supported as a focused note, but whether its combination is sufficiently new and useful remains a specialist publication judgment. B's independent local-discriminant priority gate is unchanged.

Suggested scoped claim: “We prove a branch-count obstruction for independently routed inverses with bounded vertex separators. A binary-tree specialization, analyzed using classical forest width theory, shows that these hypotheses reach beyond every fixed ordered-separation-rank budget, even for uniformly well-conditioned denominators.” This is candidate manuscript wording, without a claim of external priority.

## Inspection and integrity record

Directly read the two new theorem files and both acceptance audits, their source ledgers, Adler–Kanté's statement and width definitions, the final TQS §3.5/footnote and Theorem 4.4/Proposition 4.8, the preprint's displayed binary-tree family and footnote, and the STACS quasiseparability discussion. The final TQS PDF's mathematical display was not recovered by the web screenshot tool; the explicit matrix specialization was compared in the preprint text and is independently covered by the accepted audit's final-version comparison. This does not affect the final-text footnote and stated-order comparison that were directly readable.

Targeted searches combined quasiseparable/semiseparable with pathwidth, forests, binary trees, permutations, independent row/column orders and minimum rank; also tree quasi-separable with pathwidth and ordering. No full identical independent-axis theorem was located. This is a bounded search, not exhaustive MathSciNet/Zentralblatt coverage or priority certification.

No denied Lubinsky–Saff access route, publication, outreach, child delegation, supplied-code execution or checkpoint/registry modification occurred. The 0538 seal verifies unchanged. INPUTS.sha256 records inspected project bytes; SHA256SUMS seals this dated appendix and its accompanying status and integrity records.

Signed for this assessment: dot, 10 October 2026 UTC. This is an assistant-authored assessment sign-off, not a human signature or cryptographic identity claim.
