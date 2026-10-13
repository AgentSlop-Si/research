# Independent novelty and significance review: separator fragmentation

13 October 2026 UTC. Read-only external research and local comparison. No repository, Sheet, or other external writes. This review does not replace the separate mathematical audit.

## Verdict

**A distinct, useful local successor theorem is supported; historical originality is unresolved. Classify it as a specialized synthesis of classical rank, separator, and disjoint-error tools.** The defensible increment is the uniform near-unit error obstruction for a bare additive sum of independently routed inverse branches, obtained by keeping almost all matrix-entry area simultaneously across their different recursive partitions. Neither recursive separators, common refinement, summing disjoint Frobenius errors, nor even an error floor tending to one is new on its own, including within this project's earlier work.

The exact candidate statement was not found in the primary results inspected below. That is a bounded nonmatch, not proof of world priority or of nonimplication by the broader literature. The branch lower bound is a representation-size result, not an FFT runtime lower bound. Its fixed-error consequence is Omega(log N/log log N), not Omega(log N). The limit one is sharp through the zero approximant; the finite formula and convergence rate are not shown optimal.

Candidate identity: `Separator_Fragmentation_Candidate_20261013.zip`, verified SHA-256 `a3c374a9a8f1c23f1d4911c90cc8cc2f3b47843ce97318ee4e635b14d2ff5f34`. REPORT and CONTRACT are the reviewed claim sources.

## The strongest adjacent primary results

### 1. Inverse rank and algebra on compatible structures: established ingredients

Chandrasekaran, Epperly and Govindarajan, *Graph-Induced Rank Structures and their Representations*, v3, Proposition 2.1 and Proposition 2.3, printed pp. 5–8, establish complementary inverse-cut rank invariance and rank algebra on the same graph. The candidate uses this classical identity separately on each branch. Proposition 2.3 does not supply a common small-separator graph after unrelated endpoint permutations. GIRS itself uses edge-cut rank bounds; the candidate's vertex-boundary argument is a direct support-rank specialization, not a new inverse-rank theorem. [Primary manuscript](https://arxiv.org/pdf/1911.05858v3).

Govindarajan, Chandrasekaran and Dewilde, *Tree Quasi-separable Matrices*, final 2025 paper, Theorem 4.4 and Propositions 4.6–4.8, characterize ranks on a specified tree and compose compatible tree partitions. Both the arXiv text and the final author-hosted PDF were opened; the detailed displayed algebra was checked in arXiv v2, pp. 13–14. These representations permit flexible row and column block assignments, so calling them merely a common simultaneous permutation would understate the prior art. The missing matched statement is uniform approximation across independently chosen branch structures. [Final paper](https://repository.tudelft.nl/file/File_6b7549c8-222e-4316-8ac4-a113d7d4da1e), [arXiv v2](https://arxiv.org/pdf/2402.13381v2).

Pernet, Signargout and Villard, *Exact computations with quasiseparable matrices*, Section 5, also explicitly discusses sum rank bounds and the same-grid restriction of its SSS addition algorithm. A different block grid in Bruhat format is not arbitrary independent permutation of the underlying linear order. This is an important near match, not the candidate's independent-hierarchy theorem. [Primary author PDF](https://perso.ens-lyon.fr/gilles.villard/BIBLIOGRAPHIE/PDF/quasisep.pdf).

### 2. Hierarchical error aggregation: a closer precedent than only SMASH

Chen, Duman Keles, Halikias, Musco, Musco and Persson, *Near-optimal hierarchical matrix approximation from matrix-vector products*, Definition 1.1 and Problem 1.1, pp. 2–3, describe fixed-hierarchy HODLR approximation. The introduction explicitly obtains its exact optimum by optimal rank-k approximation of off-diagonal blocks and recursion. Thus decomposition of Frobenius approximation into disjoint hierarchical cells is established practice, including lower-bound information through the best approximation error. Their main lower bound is a matrix-vector query bound for recovering a near-optimal approximation, not a target-specific obstruction for an independently routed sum. [Primary manuscript](https://arxiv.org/pdf/2407.04686).

Cai et al., *SMASH*, Theorem 4.5 and Corollary 4.6, printed pp. 20–21, analyze aggregate HSS Frobenius construction error. These are upper-error estimates under local compression assumptions on one hierarchy. They establish another classical aggregation antecedent, but the Chen et al. fixed-hierarchy optimum is the more direct comparison for the candidate's disjoint-cell logic. [Primary author PDF](https://math.emory.edu/~dcai7/smash.pdf).

### 3. Flat-unitary rectangle energy and matrix rigidity: established mechanism, different class

Li and Strang, Theorem 1, pp. 1–3, cover best low-rank approximation for complex rectangular matrices in unitarily invariant norms. For a p-by-l submatrix V of a flat unitary, the candidate's `||V-B||_F^2 >= pl/N-rank(B)` is an immediate consequence of that theorem and `||V||_2<=1`. [Primary author PDF](https://cklixx.people.wm.edu/uinorm-note.pdf).

De Wolf, *Lower Bounds on Matrix Rigidity via a Quantum Argument*, Theorem 1 (credited to Lokam), printed p. 5, gives `rank(H[A,B]) >= |A||B|/N` for a Hadamard matrix. Theorem 2 bounds Hamming rigidity, while Section 5.1 explicitly aggregates disjoint Hadamard subblocks in Midrijanis's proof. This positively matches both the flat-submatrix rank mechanism and an older disjoint-block counting idea. The candidate's summed matrix can have full global rank and uses a norm metric and structural cell constraints, so this is not an identical theorem. [Primary author PDF](https://homepages.cwi.nl/~rdewolf/publ/qc/qr-icalp06.pdf).

Malykhin, introduction, p. 2, explicitly states the classical Frobenius rigidity of orthogonal matrices and distinguishes it from Hamming rigidity and p<2 approximation. Its global low-rank conclusion alone does not apply to the full-rank inverse-sum class. [Primary manuscript](https://arxiv.org/pdf/2010.14801).

Dvir and Liu, Theorem 1.10, p. 6, prove that complex DFT matrices are quasipolynomially nonrigid in their Hamming-rigidity sense. This neither refutes the candidate nor turns it into a rigidity breakthrough: arbitrary sparse-plus-low-rank decompositions have a different grammar, and entry-edit counts do not supply the candidate's Frobenius/operator guarantee. [Primary manuscript](https://arxiv.org/pdf/1902.07334).

### 4. Separator strength and circuit scope

Bodlaender et al., Section 2.1 and Lemma 2.9 (restated as Lemma 6.2), supply weighted half-component separators and three-way edge-separated packing. The latter is an explicit positive prior-art match. Recursive separator decomposition and the rank of a matrix with only q boundary columns are classical/elementary ingredients. [Primary author PDF](https://sites.cs.ucsb.edu/~daniello/papers/treewidthApproxJ.pdf).

Dvorak and Norin, introduction and Theorem 1, pp. 1–2, give the precise relationship to treewidth: `tw(G)<=15 sn(G)` for hereditary two-sided 2/3-balanced separations, and recall a stronger weighted converse. The candidate's half-component all-weight hypothesis implies their balanced-separation hypothesis by grouping components; bounded treewidth conversely gives bounded weighted half-component separators. Thus fixed q is a bounded-treewidth-type restriction up to constants, not a weak sparsity assumption. Do not substitute the same numerical parameter without the balance/conversion step. [Primary manuscript](https://arxiv.org/pdf/1408.3869v2).

Jansen and Sarma, *Balancing Bounded Treewidth Circuits*, Theorem 1.1 and the arithmetic statements in the introduction, study circuit simulation and balancing. Their object is a computation graph, not the support graph of each denominator's bipartite lift. No conversion from the candidate branch count to an unrestricted circuit-work lower bound was found or established. [Primary manuscript](https://arxiv.org/pdf/0910.1427).

### 5. Apparent Fourier/HSS counterexamples use a different interface

Li and Liu's September 2026 FIO paper, Section 1.1–1.2 and Section 2.2, approximates `(K* K)^-1` by HSS and then multiplies by a butterfly representation of `K*`. It explicitly notes that FIO matrices typically fail ordinary hierarchical low-rank admissibility. The butterfly factor and dense transform interface are outside permutation-contained endpoints, so this is not a fixed-r counterexample. [Primary manuscript](https://arxiv.org/pdf/2609.11520).

Hydra's quasiseparable matrix-mixer framework was inspected as an expressivity adjacency. It has data-dependent/multilayer modeling and no inspected theorem matching the candidate. No statement about all SSMs, attention, or nonlinear architectures follows from this review. [Primary manuscript](https://arxiv.org/pdf/2407.09941).

## Wider local duplication findings

1. **M-ROUTED-FIELD already has the independent-branch common refinement.** Its `SEALED_PROOF.md`, lines 135–187, partitions columns on k selected rows into k rank-one classes per branch, refines into k^r cells, and derives `N<=r(r+1)^r`. `EXTENSION_AUDIT.md` extends the denominator class to all invertible column-two matrices. Hence independent routing, masks, common refinement, cancellation-safe rank subadditivity, and the asymptotic log/log-log form are prior local ingredients. This theorem is exact over fields, while the new fixed-positive-error result is complex analytic.

2. **HERO0 Phase 22 already sums entry-disjoint Fourier block errors and obtains a limit one.** Theorem 22.3, lines 115–151 of its recovered `THEOREMS.md`, gives relative error at least `sqrt(1-3/s+1/s^2)` for a two-stage rook/fiber grammar with diagonal fixed backgrounds. It explicitly adds errors over all off-rook rectangles. Its hypotheses are very different; it does not imply the candidate's arbitrary independently routed inverse-sum theorem. It does prevent claiming that the project first discovered disjoint-cell energy or a near-unit approximation floor here.

3. **HERO0 Phase 26 has another recorded 1-o(1) approximation barrier under one common order or reverse.** The current recovered row explicitly preserves that order restriction. The full original theorem body was not recovered in this pass, so this is a source-recorded antecedent, not a fresh complete theorem-level comparison. The shared order is precisely what the candidate avoids. The row also records a later common-bipartition result tending to 1/sqrt(2); those are distinct scopes.

4. **STABLE-ARC A1/A2 are recorded earlier partition-based spectral and summed-Frobenius diagnostics.** Its current source row records that A3 is inherited from M-ROUTED-FIELD and A4/A5 are subsumed by M-SEPARATION. The full reviewed v2 manuscript (recorded hash `159ff2e8a081fbff81d977b023b3bce08561ded1b395dd0924a48df3e5802631`) was not located among the material inspected here. A precise statement-by-statement comparison to A1/A2 remains an identifiable local gap; do not declare all-local priority cleared from this negative scan.

5. **F018's earlier one-retained-rectangle robustness is a weaker conclusion under a weaker allowed marking contract.** The candidate is a new bare-model successor, not an unconditional replacement of the corrected sparse/rank/diagonal theorem. The all-weight/induced-recursion separators and `S=K=D=0` must remain visible.

Exact local source locations, hashes, matching excerpts and duplicate copies are in the scan files. No local scientific program was imported or run; newly written scripts only read, hash, search and extract text.

## Scope and publication value

A plausible specialist note or strengthened section is justified if mathematical acceptance holds. Its value is a clean architecture-expressivity barrier uniform over coefficients, independent endpoint routings, masks and flat unitary targets, with no conditioning bound. The proof is short and its core tools are elementary/classical, so importance should come from a convincingly relevant model and a precise theorem, not from novelty adjectives.

The hypothesis is strong: exact low boundary rank at every invoked recursive partition, bounded q as N grows, and a bare additive layer. It says nothing directly about products, auxiliary-state representations with altered dimensions, dense endpoint transforms, a shared evaluator's work, or approximations by numerically low-rank branches unless those errors are explicitly paid. It also does not claim fixed error is impossible when r grows; it gives a necessary lower growth bound.

The proof suggests a useful presentation: state an abstract independent-partition energy lemma first. If entry-disjoint coordinate rectangles cover area A, each has approximant rank at most R, and there are P rectangles, then `||U-T||_F^2>=A/N-RP`. This is a classical-tail corollary. The actual specialization is the simultaneous area/rank/number guarantee from r incompatible separator hierarchies. Framing the paper that way exposes exactly what needs comparison rather than hiding classical ingredients in graph notation. A broader HSS/HODLR corollary requires its own precise balance and rank hypotheses; it is not certified by terminology alone.

## Concrete next gate and stopping condition

Do not carry forward the author's 66/100 mathematical-review priority after that review is complete. Do not raise all F018/C05/Q04/TH-04 aliases from their completed-comparison status.

The bounded next gate is **publication-positioning/antecedent closure**, not rerunning controls:

- Recover and read the pinned STABLE-ARC v2 A1/A2 and the full HERO0 shared-order Phase 26 theorem.
- Write the exact independent-partition lemma and its separator specialization side by side with those statements and the fixed-hierarchy HODLR optimum.
- Follow the relevant GIRS/TQS/HODLR references for independently permuted sums, recording a theorem-level reduction if one exists.
- Stop at either a direct implication/duplication with checked hypotheses, or a documented narrow unmatched quantifier: fixed positive error across incompatible branch partitions. Only then decide whether to prepare a short specialist manuscript.

No worldwide-priority certificate or broad FFT significance claim is supported now.

## Search bounds

The companion `SEARCH_LEDGER.json` lists the actual query families, inspected primary URLs and read scope. The local search covered the two authorized workspace roots: 6,401 standalone Markdown/text/TeX files (2,159 unique contents), 581 unique ZIP archives including nested archives with 3,396 unique searchable text/TeX/Markdown/DOCX members, and 75 unique standalone PDF/DOCX files. The final archive pass recorded zero size/depth skips; the standalone document pass recorded zero extraction failures. These counts are snapshots and include historical copies. They do not mean every manuscript was read in full, all PDFs inside ZIPs were extracted, all potential synonym matches were found, or unavailable cloud-only files were covered. No source absence is an originality proof.
