# Primary-source comparison and inspection ledger

Checked 10 October 2026 UTC. URLs below were opened as actual primary full texts; search-result descriptions alone are not the evidence. This is targeted scope checking, not an exhaustive priority search.

## A. Forest linear rank-width theorem

Isolde Adler and Mamadou Moustapha Kanté, *Linear Rank-Width and Linear Clique-Width of Trees*, TCS 589 (2015), 87–98, DOI 10.1016/j.tcs.2015.04.021.

- Full text: https://perso.isima.fr/~makante/articles/kanteA13.pdf
- Checked: Theorem 2 (PDF p. 2), definitions and binary-tree example (PDF p. 4).
- Imported fact: forest linear rank-width equals pathwidth. Our matching lemma handles field transfer. The binary-tree pathwidth formula is independently proved in the deliverable.
- Not imported: any theorem about independent matrix row/column orders.

## B. Nullity and inverse off-diagonal ranks

Raf Vandebril and Marc Van Barel, *A Short Note on the Nullity Theorem*, TW397 (2004).

- Full text: https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf
- Checked: introduction (PDF p. 3), Theorem 1 (p. 6), Corollary 1 (p. 7).
- The complementary inverse-rank identity is established prior theory; the deliverable includes its direct kernel proof over every field. Independent ordering pairs are swapped under inversion, as explicitly derived there.

Shivkumar Chandrasekaran, Ethan N. Epperly and Nithin Govindarajan, *Graph-Induced Rank Structures and their Representations*.

- Full text: https://arxiv.org/pdf/1911.05858
- Checked: Proposition 2.1, Example 2.4, and Proposition 2.6.
- These give established inverse Hankel-rank preservation and the arrowhead warning. High row degree alone does not certify large optimized separation rank; our counterexample is subcubic.

## C. Especially close binary-tree precedent

Nithin Govindarajan, Shivkumar Chandrasekaran and Patrick Dewilde, *Tree Quasi-separable Matrices: A Simultaneous Generalization of Sequentially and Hierarchically Semiseparable Representations*, SIMAX 46(2) (2025), 1562–1586, DOI 10.1137/24M1682348.

- Final full text: https://repository.tudelft.nl/file/File_6b7549c8-222e-4316-8ac4-a113d7d4da1e
- Earlier v2: https://arxiv.org/pdf/2402.13381
- Checked: §3.5, printed pp. 1571–1572; Theorem 4.4 and Proposition 4.8, p. 1575.
- The final version gives a binary-tree SSS/HSS comparison for a specified ordering. Its footnote discusses combinatorial ordering search; the older v2 instead says the optimum is unknown. Neither inspected passage proves our all-independent-orders lower bound. This is a scope distinction, not novelty clearance.

## D. Established quasiseparability/rank-width connection

*Twin-Width V: Linear Minors, Modular Counting, and Matrix Multiplication*, STACS 2023.

- Full text: https://drops.dagstuhl.de/storage/00lipics/lipics-vol254-stacs2023/LIPIcs.STACS.2023.15/LIPIcs.STACS.2023.15.pdf
- Checked: related-work discussion, PDF p. 6.
- It explicitly connects quasiseparable order on adjacency matrices to linear rank-width. Our use of graph width is therefore not a new general connection. The deliverable's additional step is the bipartite interleaving argument for independently ordered matrix axes.

## E. Definition cross-check, supplementary survey

Sang-il Oum, *Rank-width: Algorithmic and structural results*, arXiv:1601.03800v2.

- Full text: https://arxiv.org/pdf/1601.03800
- Checked: §2.1, PDF p. 2, explicitly defines graph cut rank over the binary field.
- This survey is only a convention cross-check. The proof's substantive imported theorem is from the primary Adler–Kanté paper; no survey-only theorem is needed.

## Search boundary

Targeted searches included combinations of “quasiseparable”, “independent row column permutation”, “pathwidth”, “tree inverse matrix”, and “tree quasi-separable”. They located the especially relevant 2024/2025 TQS paper and the STACS connection. The actual theorem does not depend on a claim that search found every relevant paper. Future manuscript work should compare the all-order strictness lemma and independently routed sum application against these papers and their citations. No outreach, submission, or public posting was performed.
