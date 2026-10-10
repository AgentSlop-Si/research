# Source and Certificate Index

10 October 2026. Companion to **Fourier Rectangle Rank and Dyadic Endpoint Minimax**.

## Deliverable status

- Main deliverable: [manuscript.md](manuscript.md), a self-contained mathematical **DRAFT for review**.
- Frozen manuscript SHA-256: 456ae5ab870ce002c5a4cfa80a6169ffb0defd87e38196011e09f4459206fdc7.
- Every theorem asserted in the manuscript is proved there. None depends on an unreproduced numerical or finite algebraic certificate.
- No supplied research program was executed, imported, compiled, or parsed as executable code.
- The only executed control program was newly authored for this draft: [controls/check_endpoint_rank.py](controls/check_endpoint_rank.py).
- No worldwide priority or publication-readiness certification is asserted. Independent review is scoped to the reviewed file hashes.

## Primary published source

Steven Delvaux and Marc Van Barel, *Rank-deficient submatrices of Fourier matrices*, Linear Algebra and its Applications 429 (2008), 1587–1605.

- DOI: [10.1016/j.laa.2008.04.043](https://doi.org/10.1016/j.laa.2008.04.043)
- Original supplied final PDF: research_cycle_0958/uploaded_primary_1040/1-s2.0-S0024379508002164-main.pdf
- PDF SHA-256: af33370c7d4b8f3853d36c01b512b007512886431af4963cdc6d7638af89aae4
- Original extracted text: research_cycle_0958/uploaded_primary_1040/delvaux_final.txt
- Text SHA-256: 557addab85850457387bbb3d4030cda7ff0bb19b8d0a35c3842111049506449a
- The publisher PDF is **not redistributed in this deliverable**. Use the DOI for public access and the supplied original for authorized local inspection.

| Manuscript topic | Final article location | Role |
|---|---|---|
| Double digit reversal and rank-one hierarchy | Lemma 7, p. 1596 | Established antecedent of the upper ordering |
| Support frontier | Definition 6, equation (18), pp. 1594–1595 | One-vector quantity being compared |
| Prime-power support formula | Theorem 9, pp. 1598–1599 | Includes the order-eight rank corollary |
| Extremal support restriction | Remark 10, p. 1599 | Equality-set information retained explicitly |
| Prime full spark | Theorem 4 and Remark 5, pp. 1592–1593 | Classical stronger statement in the prime regime |
| Basic support uncertainty | Theorem 1 and Lemma 2, pp. 1588–1589 | Classical norm/flatness antecedents |
| General Kronecker extension | Remark 13, p. 1599; reference 1, p. 1605 | Broader comparison still required |

The completed supplied comparison is copied verbatim as [sources/DELVAUX_FINAL_COMPARISON.md](sources/DELVAUX_FINAL_COMPARISON.md). Its original location is research_cycle_0958/uploaded_primary_1040/delvaux_comparison/DELVAUX_FINAL_COMPARISON.md. It reports a full nineteen-page comparison and direct rendering checks of printed pp. 1598–1599. This manuscript preparation independently rechecked the title, journal metadata, Lemma 7, Theorem 9, Remark 10, and the bibliographic reference to the 2007 paper in the final extracted text. It does not claim a new full nineteen-page comparison or a new rendering of the primary paper.

The related paper is Steven Delvaux and Marc Van Barel, *Rank-deficient submatrices of Kronecker products of Fourier matrices*, Linear Algebra and its Applications 426 (2007), 349–367. Those bibliographic details were verified in reference 1 of the final 2008 article. The full 2007 paper was not freshly compared in this preparation.

## Supplied mathematics and theorem mapping

The source copies preserve their original wording and dates. The manuscript is the current self-contained exposition.

| Manuscript result | Supplied source | Evidence used |
|---|---|---|
| Theorem 2.1, deficit rank and approximation | [FOURIER_DEFICIT_SEPARATOR_FUSION.md](sources/FOURIER_DEFICIT_SEPARATOR_FUSION.md), §1 | Complete moment/contraction proof, expanded here |
| Corollary 2.2, cardinality implications | Same, §2 | Translation-orbit argument |
| Theorem 3.1, critical rectangle and gap | [FINAL_THEOREMS.md](sources/FINAL_THEOREMS.md), Theorem 1B; [CORE_THEOREMS_SECOND_AUDIT.md](sources/CORE_THEOREMS_SECOND_AUDIT.md), §1 | Unified with the deficit proof |
| Proposition 4.1 and Theorem 4.2, exact minimax | FINAL_THEOREMS.md, Theorem 1A and upper proof; CORE_THEOREMS_SECOND_AUDIT.md, §1 | Paired-row quotient, surviving odd-cut residue, reflection |
| Proposition 5.1, balanced-square countercontrol | DELVAUX_FINAL_COMPARISON.md, balanced-square discussion | Repeated Fourier block and stable-rank lower bound |
| Products and diagonal scaling | FINAL_THEOREMS.md, Corollary 1C | Full proofs reproduced |
| Rectangle interface and legal trimming | FOURIER_DEFICIT_SEPARATOR_FUSION.md, §3 | Actual deficit and admissible-cardinality restriction |
| Routed inverse-sum selection | FINAL_THEOREMS.md, Theorem 2A; CORE_THEOREMS_SECOND_AUDIT.md, §2 | Inverse nullity and two-color separator argument reproduced |
| Final-article comparison | DELVAUX_FINAL_COMPARISON.md | Classical hierarchy, order-eight overlap, worldwide priority open |

Original source paths:

1. research_cycle_0958/matrix/final_v1/FOURIER_DEFICIT_SEPARATOR_FUSION.md
2. research_cycle_0958/matrix/final_v1/CORE_THEOREMS_SECOND_AUDIT.md
3. research_finalization_0923/matrix/FINAL_THEOREMS.md
4. research_cycle_0958/uploaded_primary_1040/delvaux_comparison/DELVAUX_FINAL_COMPARISON.md

The first two source documents contain historical statements that the final 2008 article was unavailable. Those access blockers are superseded by the completed comparison, not endorsed as current. Source copies are intentionally unchanged. Resolving the access gap does not establish worldwide novelty.

## Newly authored controls

Run command: python endpoint_rank_note/controls/check_endpoint_rank.py

Outputs: [controls/results.json](controls/results.json) and [controls/run.log](controls/run.log).

The run passed using NumPy 2.3.5:

- 4,095 exact rational critical-algebra and positivity checks, for every integer \(2\le L\le4096\)
- 67 cut-recurrence and 134 reflection checks through order 64
- 4 attained-upper-value checks at \(N=8,16,32,64\)
- 16 tight balanced-square examples at \(N=4,8,\ldots,64\)
- 10,768 rectangle moment and rank checks
- 34,605 singular-gap comparisons
- 9,568 critical-rectangle checks: every \(3\times5\) rectangle in each of the three abelian groups of order eight, plus deterministic samples in four abelian groups of order sixteen

The controls also include prime, odd-prime-power, mixed-order, cyclic, noncyclic, full-row, and full-column examples. The random seed is 20261010. The largest moment-identity residual was approximately \(7.11\times10^{-15}\); the largest signed gap violation was below \(10^{-15}\), against tolerance \(2\times10^{-9}\). Numerical rank uses threshold \(10^{-8}\).

These are regression tests, not exact nonvanishing certificates or proofs of universal claims. Exact rational arithmetic checks the displayed algebra at the tested parameters. The manuscript's analytic proofs establish the universal results.

## Scope gates

- Complex analytic normalization is explicit; unnormalized gaps scale by \(\sqrt N\).
- Exact cyclic rank equality extends to characteristic zero through the cyclotomic field. No all-finite-field theorem is asserted.
- The abelian \(2\)-group result is a lower bound and gap; matching upper orders for every noncyclic group are not supplied.
- The balanced-square minimum is stated for cyclic Fourier matrices and equals \(N/4\).
- The hierarchy is classical, and order eight is already covered by Theorem 9 of the final article.
- General minimax and deficit formulas are distinct statements relative to that article. Worldwide priority is unresolved.
- The separator application proves its own selection hypotheses and never assumes that the final side is odd.
- No unrestricted FFT lower bound, optimal separator exponent, or logarithmic branch requirement at fixed nonzero tolerance is claimed.

File hashes and byte lengths are recorded in [MANIFEST.json](MANIFEST.json), excluding the manifest itself. Any later manuscript change requires renewed hash-scoped review.
