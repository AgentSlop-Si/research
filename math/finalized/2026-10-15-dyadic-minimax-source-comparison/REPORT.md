# Dyadic minimax: bounded primary-source comparison

Date: 2026-10-15 UTC.
Intended repository path: math/finalized/2026-10-15-dyadic-minimax-source-comparison/REPORT.md.

## Result

No earlier primary implication was established in this pass for the universal N≥16 lower bound. Three direct-specialization failures and the limited Beelen–Datta scope check were independently checked. C02 remains OPEN52 for attribution. Its accepted proof, classical upper bound, and classical N=8 endpoint remain unchanged.

## 1. Exact obligation checked

For every finite abelian 2-group G of order N=4L≥16, with normalized complex Fourier matrix U_G, and every character selection I of size 2L+1, establish

d_(L+1)(U_G E_I) ≥ 2L+2,

where d_r is the minimum union-of-support size of an r-dimensional complex subspace.

Equivalently, every critical (2L−1)×(2L+1) Fourier rectangle has rank at least L+1. The group/dual formulation with every J of size 2L−1 is d_(L−1)(U_G E_J)≥2L.

This is the gate in the pinned [C02 current-obligation note](https://github.com/AgentSlop-Si/research/blob/21aac668f52b5680b8b22eb99d53a850ae0cd394/math/finalized/2026-10-15-top-theorem-boundaries/C02_CURRENT_OBLIGATION.md). Fresh table reads confirmed Catalogue row18 and Research overview rows22–25. This pass concerns their shared C02-dependent slice, not every separate NEW-05/Q05/TH-05 obligation.

## 2. Completed primary comparisons

### A. Borodin–Razborov–Smolensky, 1993, Theorem 10

Section 5 defines the character matrix for any finite abelian group over a splitting field, including C. Theorem 10, printed p12, applies to arbitrary t-row/u-column selections and gives rank≥tu/[2N ln(2N/u)]; the following dual argument exchanges t and u.

At t=2L−1, u=2L+1, N=4L, both numerical lower bounds are <L/2 for L≥4: 8L/(2L+1)≥32/9>e, and tu/(8L)<L/2. Thus these clauses have the required group and subset quantifiers but do not reach L+1. Their separate finite-field branching-program applications do not supply an unrestricted FFT conclusion.

Source: [author-hosted 1993 paper](https://www.cs.toronto.edu/~bor/Papers/lower-bounds-read-k-times-branching.pdf), §5, printed pp11–13 and Appendix 2. This URL was read on 2026-10-15; no immutable version identifier or local byte hash was obtained.

### B. Alagic–Russell, “Uncertainty principles for compact groups,” Theorem 3.1.1 and Corollary 1

The Hilbert–Schmidt identity applies to coordinate and Fourier projections in the complex finite-group setting. For coordinate and Fourier spaces both of dimension h=2L+1, it gives trace(PQP)=h²/N=L+1+1/(4L). Counting eigenvalues equal to one yields intersection dimension≤L+1. The target requires ≤L.

Likewise, on the critical rectangle, the basic contraction/trace estimate yields rank≥ceil((2L−1)(2L+1)/(4L))=L. The missing unit is not supplied by this direct specialization.

Source: [arXiv:math/0608702v2, 29 August 2008](https://arxiv.org/pdf/math/0608702v2), Theorem 3.1.1, printed p4, and Corollary 1, printed p2.

### C. Akemann–Weaver, “Detecting Fourier subspaces,” Proposition 0.3 and Theorems 0.5–0.6

These results fix a Fourier subspace and select a suitable standard subspace existentially. Theorems 0.5–0.6 control projection norms with an O(sqrt(ε)) term, ε=dim(F)/|G|. They do not assert the required exact intersection-dimension obstruction for every critical standard subset. Here ε is near one half, rather than a vanishing parameter. This is a quantified mismatch for the named clauses.

Source: [arXiv:1503.06893v1, 24 March 2015](https://arxiv.org/pdf/1503.06893v1), Proposition 0.3, printed p2, and Theorems 0.5–0.6, printed p4.

The independent comparison review accepted A–C as bounded direct-specialization failures. This does not establish that the entire papers, their techniques, or all possible combinations cannot imply the target.

## 3. Generalized-Hamming-weight lead

### D. Beelen–Datta: independently checked limited scope boundary

“Generalized Hamming weights of affine Cartesian codes,” Theorem 4.6, printed p8, works over an arbitrary field. Consequently, using C and Cartesian products of roots of unity is legitimate. Its maximization, however, is over independent polynomials in the full total-degree-cutoff space S_≤d(A). Theorem 5.4 gives the corresponding generalized-weight formula in the finite-field coding section.

For G=∏ Z_(n_i), arbitrary character selections correspond to arbitrary selected monomials on ∏μ_(n_i), not necessarily a total-degree cutoff. The earlier footprint inequality is broader, but a uniform shadow/combinatorial estimate for every such I would still have to be supplied. This pass did not establish that bridge. Therefore the named formulas do not directly close the attribution gate.

Source: [arXiv:1706.02114v2, 1 August 2017](https://arxiv.org/pdf/1706.02114v2), Theorems 3.9, 4.6 and 5.4 and the preceding footprint argument.

The independent reviewer accepted this limited scope check after inspecting those theorems and their dependencies. This is not a claim of nonimplication from all footprint methods.

### Auxiliary arbitrary-monomial source: author check only

López–Matthews–Soprunov explicitly defines finite-field monomial-Cartesian codes for arbitrary exponent sets. Its inspected Theorem 3.3 describes duals and Proposition 3.1 treats minimum distance of product codes; these are not the missing universal complex higher-weight inequality. No finite-field transfer is claimed.

Source: [“Monomial-Cartesian codes and their duals, with applications to LCD codes, quantum codes, and locally recoverable codes”](https://personal.math.vt.edu/gmatthews/Monomial_Cartesian.pdf), author-hosted PDF read on 2026-10-15. No immutable version identifier or local byte hash was obtained. This auxiliary comparison has not been independently reviewed in this pass.

## 4. Sharpened scalar check and remaining source barriers

### Feng–Hollmann–Xiang: author check only

Theorem 7.2 covers all finite abelian groups in characteristic zero and sharpens scalar support-product uncertainty using support stabilizers. Its Lemma 7.1 implies that an odd-sized subset of a 2-group has trivial stabilizer. Nevertheless, inserting both full support sizes h=2L+1 only requires h²≥N+h−1=6L, which is compatible with the critical parameters. No r-dimensional generalized-weight bridge was established. This does not reopen or replace the already completed scalar comparison.

Source: [arXiv:1804.00367v1, 2 April 2018](https://arxiv.org/pdf/1804.00367v1), Lemma 7.1 and Theorem 7.2, printed p11. This auxiliary comparison has not been independently reviewed in this pass.

### Targeted source barriers

- Shibuya–Sakaniwa, 2001, “A Note on a Lower Bound for Generalized Hamming Weights,” pp3138–3145. The official page describes a generalized bound with arbitrary cyclic-code applications, but supplied an abstract and purchase route rather than readable theorem text in this pass. Its exact field hypotheses and specialization remain unchecked. [Official article page](https://globals.ieice.org/en_transactions/fundamentals/10.1587/e84-a_12_3138/_p)
- Janwa–Lal, 1997, “On the generalized Hamming weights of cyclic codes,” DOI10.1109/18.567719. Primary full text was not retrieved; the DOI endpoint failed in the reading tool. Abstract-level descriptions do not justify a nonmatch classification. [Article DOI](https://doi.org/10.1109/18.567719)

These are access limits of this pass, not claims that the papers are globally unavailable or irrelevant.

## 5. Exact original proposed cell additions

These are append-only proposal texts, not applied edits. Preserve existing history, numerical priorities, proof acceptances, and the prior COMPLETE15 bounded comparison. Any later synchronized native proposal must be separately reviewed; the following preserves the original authored proposal.

### Catalogue AD18; Research overview O22–O25

[2026-10-15; resumed primary-source comparison] For the C02-dependent all-finite-abelian-2-group N≥16 slice, historical attribution remains unresolved (parent OPEN52). Direct specializations of BRS Theorem 10, Alagic–Russell Theorem 3.1.1/Corollary 1, and Akemann–Weaver Proposition 0.3/Theorems 0.5–0.6 do not supply the required L+1 rank bound. Beelen–Datta Theorem 4.6/5.4 concerns total-degree Cartesian spaces; its application to every arbitrary character selection is unproved. These are bounded clause-level findings, not global nonimplication or worldwide novelty certification.

### Catalogue AE18; Research overview P22–P25

Retain the exact universal gate: every finite abelian 2-group |G|=4L≥16 and every |I|=2L+1 must satisfy d_(L+1)(U_G E_I)≥2L+2, equivalently every critical (2L−1)×(2L+1) rectangle has rank≥L+1. Next targeted source work: obtain primary theorem text for Shibuya–Sakaniwa2001 and Janwa–Lal1997, or complete an explicit arbitrary-character footprint specialization. Basic trace gives only rank≥L. Do not repeat the closed generic scalar/Hamming comparison.

### Catalogue AF18; Research overview Q22–Q25

Close attribution only with an earlier primary theorem plus a complete field/group/subset/endpoint specialization reaching L+1 for every critical rectangle, or record a precisely bounded nonmatch/source barrier. Preserve accepted mathematics, classical TW477 Lemma12 upper/N=8 Corollary21 endpoint, and parent OPEN52. No new theorem count, finite-field lower transfer, arbitrary FFT bound, or collapse of broader NEW-05/Q05/TH-05 scopes.

## 6. Evidence and execution limits

The primary comparisons used readable source text and proofs. Independent review covered A–C and D only, as explicitly described above; auxiliary monomial-Cartesian and sharpened-scalar checks remain author research pending independent review. Source-access observations are not negative theorem findings.

ArXiv links are pinned to the versions actually displayed in the inspected PDFs. Author-hosted, nonversioned URLs are recorded with the read date and without a fabricated byte hash.

No local binary hashing, original-candidate-byte recovery, Lean execution, or replay occurred. No sheet or repository ref was changed during the research pass. The requested durable preservation creates only authored UTF-8 Git blobs in AgentSlop-Si/research; it does not itself create a path, tree, commit, or ref update. No full copyrighted primary paper is copied into this report.
