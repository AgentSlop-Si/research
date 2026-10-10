# Primary-source and antecedent checks

Inspected 10 October 2026 UTC. This is a correctness/reference audit, not a novelty search.

1. **Adler and Kanté, Linear Rank-Width and Linear Clique-Width of Trees.** Author manuscript https://perso.isima.fr/~makante/articles/kanteA13.pdf, directly opened as a 17-page PDF. Theorem 2, PDF page 2, states forest linear rank-width equals pathwidth. PDF pages 3–4 define graph cuts, graph linear layouts and path decompositions; page 4 states the rooted binary-tree pathwidth formula. Bibliographic record independently checked at https://eprints.whiterose.ac.uk/id/eprint/101098/: Theoretical Computer Science 589 (2015), 87–98, DOI 10.1016/j.tcs.2015.04.021. The field-independence bridge in the candidate is proved independently rather than presumed from the graph theorem. The original Scheffler thesis cited for binary-tree pathwidth was not inspected; the candidate's elementary proof eliminates reliance on that secondary attribution.

2. **Vandebril and Van Barel, A Short Note on the Nullity Theorem, TW397 (2004).** https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf, directly opened as a 12-page PDF. Corollary 1 on PDF page 7 has the correct swapped-complement rank identity and cardinality correction. Its displayed statement uses real matrices and nonempty proper index sets. The candidate's independent kernel proof supplies its claimed any-field and endpoint versions. No new nullity theorem is claimed.

3. **Chandrasekaran, Epperly and Govindarajan, Graph-Induced Rank Structures and their Representations.** https://arxiv.org/pdf/1911.05858, directly opened as a 58-page PDF. Proposition 2.1 on PDF page 5 gives inverse Hankel-block rank preservation; Proposition 2.3 on pages 7–8 gives inverse/additive/product GIRS closure; Example 2.4 on page 7 describes arrowhead support with a different useful graph structure. These are attribution/context references, not the proof of the new strictness witness. The candidate's additional Proposition 2.6 reference concerns SSS algebra and is not needed for the accepted argument.

4. **Actual inherited separation-rank theorem.** Read in full from the protected project path in INPUTS_BEFORE.sha256. Its abstract definition explicitly includes both orientations and independent row/column orders. The audit does not rely on the assessment's paraphrase for this crucial point.

5. **Accepted routed pseudoforest separator theorem.** Read the sealed proof's construction, separator and inverse-rank portions at pseudoforest_separator_independent_audit_0452/SEALED_PROOF.md. Its arbitrary endpoint-monomial factors allow identity endpoints; its bounded-treewidth form allows q=2 for a tree lift. The new witness meets the exact structural hypothesis.

6. **Govindarajan–Chandrasekaran–Dewilde, Tree Quasi-separable Matrices.** Directly inspected section 3.5 and footnote 4 in the final 2025 PDF and arXiv v2. The exact parameter distinctions and verified links appear in PROOF_AUDIT.md, section 10.

The public source summaries here are limited to the statements needed for the audit. No public source was used as negative evidence of originality. No external communication, posting, submission, or account action occurred.
