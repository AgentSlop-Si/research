# FFT research: novelty and publication review (October 10, 2026)

**Scope:** Research materials available in this conversation/Library through Green Phase 42 and Schur-extension v28, reviewed against the prior project audit through checkpoint 26 and selected published literature. **Conclusions are not peer review or worldwide priority certification.** The new theorems in `NEW_THEOREMS_AND_PROOFS.md` are the most important additions from this review.

## Executive findings

The project contains real mathematics beyond implementation experimentation: several exact algebraic identities, a family of restricted Fourier-representation impossibility results, and correct-by-certificate structured-input Fourier algorithms. **None supplies an exact arbitrary-input O(N) FFT or an arbitrary-model Fourier lower bound.** OpenAI's September 2026 exact-complex DFT work already reports a uniform O(N(log N)^(1-10^-13)) algorithm in a model with unrestricted complex coefficients (with significant distinctions from floating-point and bit complexity): https://github.com/openai/math/blob/main/lean/docs/130.md.

### Two new deductions made in this review

1. **Unitary Green sum: all lengths, not just even lengths.** Phase 42 proved that every even N>=4 Fourier matrix is incompatible, up to row/column permutations and diagonal gauges, with any real-linear sum of unitary Hamiltonian-cycle Green resolvents. The parity assumption can be removed. For **all N>=4**, a constant-diagonal matrix with shifted skew-Hermitian off-diagonals cannot be monomially Fourier-equivalent. Applying G+G*=I proves the all-N Green theorem. Proof and runnable finite checks in `NEW_THEOREMS_AND_PROOFS.md` and `verify_new_lemmas.py`.
2. **Schur-extension terminal-treewidth constant doubled.** The source v28 proved that if F_p=P A^(-1)E with all injection/extraction edges included in K=[A E;P 0], then tw G(K)>=ceil(p/8)-1. A sharper component grouping proves **tw G(K)>=ceil(p/4)-1**. It applies to prime complex Fourier targets and more generally any invertible target with full-spark inverse. Full proof and enumeration in the accompanying files. It does not say a high-treewidth solver must take superlinear time.

These two results are **new relative to the project source versions**. The tools and identities in their proofs are classical. Their historical novelty requires a proper mathematical literature and reviewer audit before submission.

## Corpus inventory and what was actually inspected

- **279 accessible ZIP files** programmatically opened (includes historical snapshots and duplicates).
- **32,421 archive-member occurrences** and **28,693 text/code occurrences** at the first archive level were read and SHA-256 deduplicated.
- **7,545 distinct text/code contents**, including 1,746 distinct Markdown bodies, 1,604 Python files, 2,616 JSON bodies, 1,014 text bodies, 487 logs and smaller source types. There were **zero ZIP-read failures** in this pass.
- The checkpoint-26 master TAR was inventoried at **23,074 members**. A further full decompression/hash pass timed out, so it was **not** independently covered byte-for-byte. Many of its important source packages are included in the successfully indexed ZIP copies.
- The earlier full audit through Phase 41, publication assessments, archived proof registers and high-priority source bundles were read. This pass substantively examined **Phase 42**, **Schur extension v28**, and their predecessor theorem packages, including real proof details; relevant earlier material was cross-checked rather than restated as new discoveries.
- Freshly executed unmodified unit-test suites: **10/10 Phase 42, 10/10 Schur v28**, plus the separate Schur verifier and Phase 42 symbolic identity control. Independently written combinatorial checks: the paired-cross-ratio condition for N=2..8, and **498,790** component partitions through N=30.
- The file hashes demonstrate indexing, **not 7,545 independent theorem proofs**. Nested ZIP contents, files over the text-size cap, PDF figures, and every source-level mathematical dependency did not receive a fresh line-by-line review.

## Ranking: manuscript potential, not confirmed historical firstness

| Rank | Candidate | Specific contribution; not the already-known ingredient | Audit verdict | Closest priority issue |
|---:|---|---|---|---|
| **1** | Rogers–Szegő *ordinary discriminant* at moving cyclotomic roots | Guarded local splitting, exact order and leading coefficient, residue squarefreeness/content arithmetic | Substantive algebra/number theory; project-proof and small symbolic controls; requires journal comparison | Lubinsky–Saff 1987 supplies recurrence, static factorization and chirp Padé formulas; Sawa–Uchida quasi-Hermite discriminants |
| **2** | **All-N unitary Green obstruction (new strengthened statement)** | For every N>=4 and any q, no real-collinear combination of unit-phase Hamiltonian-cycle resolvents is monomially Fourier-equivalent | **Full short mathematical proof supplied in this review**; strong short-note prospect | Hadamard/conference equivalence and resolvent identities already known; exact combined statement unlocated in targeted search |
| **3** | Independently routed bounded-separator inverse sums | Explicit N vs branch/width necessary conditions for representations of flat unitary matrices, with independent endpoint orders | Strong source proof for a restricted grammar; older certificates accepted in project audits | Asplund/Green rank structure, nullity rank and tree-quasiseparability |
| **4** | Exactly three legal Green terms on arithmetic 5x5 blocks | Matching lower algebraic certificate and upper construction for a parameterized five-coordinate family | Proof/certificate-intensive yet promising | Additive length/secant varieties of structured inverses; does not construct a 3-term full-N Fourier circuit |
| **5** | **Prime Fourier Schur-extension treewidth (new strengthened constant)** | For K=[A E;P 0] with F_p=P A^-1 E, complete support graph has tw>=ceil(p/4)-1 | **Full short mathematical proof supplied**; potentially useful graph+matrix paper | Jacobi complementary minors, treewidth separators, Chebotarev Fourier minors are classical; check sparse realizations literature |
| **6** | Dyadic Fourier endpoint rank minimax | Sharp N/4+1 for the project's precise endpoint rank/cut functional under independent coordinate orders | Source all-size proof, priority incompletely resolved | Delvaux–Van Barel 2008 Fourier rank-deficient submatrix hierarchy; do not re-claim their classical bit reversal grids |
| **7** | Universal reciprocal Hankel/diagonal-pencil resultant factors | Explicit w- and (w-1)-factors, reciprocal grade and polynomial in w+w^-1, including arbitrary diagonal-pencil extension | Exact-looking symbolic algebra and multiple bounded controls | Classical Sylvester resultant, Newton polygon, Hankel interpolation, symmetric Laurent invariant methods |
| **8** | Weyl–Green fixed-pair branching | Lower bounds for ordered two-Green paths sharing a fixed Weyl generator pair; quadratic chirp Hankel obstruction | Valid looking restricted representation lower bound | Weil/Heisenberg algebra, Gauss sums and Prony/Hankel rank are classical |
| **9** | Certified growing-fiber transform | Exact full outputs in O(N log(b+2)+sqrt(N)b²) on recognized fiber-sparse inputs; growing polylog budgets give O(N log log N) on that family | Fully specified promise, recognition, certificates and charged operation model; no generic improvement | Existing Prony, sparse FFT, and FFT pruning |
| **10** | Blind quadratic-chirp and sparse graph recognition | Linear or near-linear recognition/application for fixed-rank structured sequences, with all-coordinate exact certificate | Algorithmic application candidate with substantial restrictive input promise | Polynomial-phase sparse interpolation and rational reconstruction |
| **11** | Phase 42 phase-budget/rank saturation | Generic local parameter constraints q>=2r-1 and nonreal phase slots k>=r-2; finite-size exact Jacobian witnesses | Genuine local algebraic geometry study; numerical partial fits do not prove an all-N Fourier factorization | Common gauge dimension counting, Hadamard phase equivalence |
| **12** | Finite-word approximate Fourier tables and Gaussian/divisor surrogates | Particular all-length/accuracy/setup contracts, possible numerical compiler benefits | Incomplete practical validation and close prior art; not exact full DFT | Four Russians, fast approximate FFT, NUFFT, tabulation |

Some source results serve as **negative controls** rather than separate publications. Examples: v26-v27's Weyl-covariant additive-group embedding obstruction follows heavily from Stone–von Neumann/Weil and finite-abelian character theory; Phase 25 Good–Thomas CRT and unitary matrix-entropy FFT bounds are classical; dense inverse ≠ expensive solver; rank-feasible or numerically fitted first rows ≠ an exact full Fourier factorization. Explicitly credit these ingredients if used.

## New mathematical results: exact restrictions

### A. All-length real-collinear Green theorem

For any finite q>=0, N>=4, Hamiltonian weighted cycle matrices W_j with edge moduli one and I-W_j invertible, and coefficients c_j=lambda*r_j with r_j real and a common complex scalar lambda,

    sum_j c_j (I-W_j)^(-1)

cannot equal any left/right invertible diagonal/permutation gauge of F_N. The proof uses a general *constant diagonal + shifted skew-Hermitian* Fourier obstruction; it works at odd, prime, composite and even lengths alike.

**This theorem does not** restrict sums with genuinely distinct complex coefficient phases, nonunit edge magnitudes, or multistage products. It never proves a runtime bound against arbitrary FFTs.

### B. Complete-extension treewidth obstruction

At prime p, if F_p=P A^(-1)E, A invertible, E/P arbitrary, define K=[A E;P 0] and its undirected support graph. Then

    tw G(K) >= ceil(p/4) - 1.

**This theorem does not** force every high-treewidth solve to be hard: an acyclic orientation of a bounded-degree expander admits exact linear-time triangular substitution with high support-graph treewidth. The premise includes every injection and extraction edge, so the claim is about the **combined extension graph** rather than just A.

The two complete proofs, classical ingredients, model boundaries and independent finite checks are frozen separately in `NEW_THEOREMS_AND_PROOFS.md`.

## Prior-art checks (targeted; no absolute priority conclusion)

1. Lubinsky & Saff, *Convergence of Padé Approximants of Partial Theta Functions and the Rogers–Szegő Polynomials*, Constr. Approx. 3 (1987), 331–361. Static root factorization, recurrence, shifted chirp Hankel determinants precede our project; moving ordinary-discriminant leading coefficients remain an explicit comparison target. URL: https://www.math.vanderbilt.edu/saffeb/texts/76.pdf
2. Sawa & Uchida, *Discriminants of classical quasi-orthogonal polynomials...* (2018/2019) establishes quasi-Hermite discriminant machinery. URL: https://arxiv.org/abs/1802.00605
3. Delvaux & Van Barel, *Rank-deficient submatrices of Fourier matrices*, Linear Algebra Appl. 429 (2008) 1587–1605: classical rank-deficient Fourier hierarchy. URL: https://doi.org/10.1016/j.laa.2008.04.043
4. Boito & Eidelman, *Computation of quasiseparable representations of Green matrices*, Linear Algebra Appl. 721 (2025), 47–80. URL: https://doi.org/10.1016/j.laa.2024.04.034
5. Östergård & Valtonen, *Equivalence of complex Hadamard matrices*, J. Algebraic Combinatorics 64 (2026), article 20. URL: https://link.springer.com/article/10.1007/s10801-026-01568-x
6. Tao, *An uncertainty principle for cyclic groups of prime order*, Mathem. Research Lett. 12 (2005), 121–127; prime-Fourier minors derive from Chebotarev. URL: https://arxiv.org/abs/math/0308286
7. OpenAI, *An explicit power saving for the exact discrete Fourier transform* (September 2026), exact-unrestricted-coefficient complexity vs numerical complexity boundary. URL: https://github.com/openai/math/blob/main/lean/docs/130.md

Searches using the exact distinctive language for the two newly strengthened statements did not locate a matching prior theorem. Negative search results are not priority proofs. A scholarly referee, MathSciNet/zbMATH lookup and source-by-source comparison remain required.

## Publication recommendation and next falsification gates

**Paper A: `Fourier matrices, constant-diagonal shifted skew-Hermitian forms, and unitary cycle resolvents`.** First publishable-quality direction for a concise, self-contained theorem. Prove the abstract paired-cross-ratio lemma independently, show sharp small-N exceptions or classify them, check literature on skew-Hadamard/conference matrices, and evaluate whether the result extends to more than real-collinear weights.

**Paper B: `Full-spark Schur complements require large terminal treewidth`.** General abstract full-spark theorem (not tied to Fourier), its constant-1/4 proof, counterexample warning that high treewidth does not imply costly inversion; compare matrix realization/graphical model/semiseparable literature. Seek sharper constants or all-terminal rank-profile generalizations.

**Paper C: `Local discriminants of Rogers–Szegő polynomials at roots of unity`.** Highest mathematical depth, but the most delicate priority, complex proof guards and algebraic certificates. Concentrate on moving-root ordinary discriminant leading terms and arithmetic corollaries; state Lubinsky–Saff's static and Padé identities as prior art.

**Paper D: `Independent Green paths and Fourier rigidity`.** Combine the bounded-separator and representation-branch gates only with precise model separation: not every branch sum is a product and arithmetic rank is not arithmetic cost.

Always provide independently executable certificates, exact hypotheses, negative controls, and a page-by-page prior-art comparison. Do not represent "internally proof-closed" as "historically discovered first".

## Audit limitations and reproducibility

The SHA-256 catalogue is a source-content deduplication index. The full master TAR byte-pass timed out (after successfully listing 23,074 member names). Systematic reading of ZIP text and proof-level mathematical inspection are different standards. Source programs were not all executed; the new finite checks and selected latest tests were. The source PDFs and earlier DOCX summaries were considered as targeted references, not as 1:1 proof validations for every file. The full report and ZIP output preserve both newly strengthened proofs and their test program so another session can restart without claiming unverified historical novelty.
