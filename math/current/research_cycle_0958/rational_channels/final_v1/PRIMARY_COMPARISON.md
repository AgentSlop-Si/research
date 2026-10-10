# Primary-source comparison and novelty disposition

10 October 2026. Research correctness, direct prior-art overlap, and historical novelty are separate questions. The mathematical proof is self-contained in THEOREMS_AND_AUDIT.md. This is a targeted comparison, not an exhaustive priority search. No supplied program was run.

## 1. Closest DFT-complexity antecedents

### S. Winograd, 1979

*On the multiplicative complexity of the Discrete Fourier Transform*, Advances in Mathematics 32(2), 83–117, DOI 10.1016/0001-8708(79)90037-9.

Verified primary author-institution record: https://research.ibm.com/publications/on-the-multiplicative-complexity-of-the-discrete-fourier-transform . The abstract establishes a DFT multiplicative lower bound and attainability for prime lengths. It explicitly deals with algebraic relations among quantities used in computation. This is decisive evidence that algebraic scalar-multiplication lower bounds for DFTs are established territory. The full article was not obtained in this pass; no exact theorem/model equivalence is asserted. The publisher page's direct read returned 403.

### L. Auslander, E. Feig, S. Winograd, 1984

*The multiplicative complexity of the Discrete Fourier Transform*, Advances in Applied Mathematics 5, 87–109. Primary author-institution record: https://research.ibm.com/publications/the-multiplicative-complexity-of-the-discrete-fourier-transform . Its abstract states that the multiplicative complexity can be computed for arbitrary sets of data points. The separate paper *Abelian semi-simple algebras and algorithms for the Discrete Fourier Transform*, 5(1), 31–55, DOI 10.1016/0196-8858(84)90003-4, is verified at https://research.ibm.com/publications/abelian-semi-simple-algebras-and-algorithms-for-the-discrete-fourier-transform . It uses abelian semisimple algebras to organize a two-dimensional DFT algorithm. Only these abstracts/metadata were inspected; the full multiplication models remain an explicit comparison task.

### R. Tolimieri, 1986

*Multiplicative characters and the discrete Fourier transform*, Advances in Applied Mathematics 7(3), 344–380, DOI 10.1016/0196-8858(86)90039-4.

Primary publisher abstract: https://www.sciencedirect.com/science/article/pii/0196885886900394 . Author identity also appears in the publisher's Richard Tolimieri record: https://www.sciencedirect.com/author/6701538709/richard-tolimieri . The abstract describes rational-subspace decomposition of Fourier transforms using multiplicative characters, to rederive Auslander–Feig–Winograd results. This is particularly close to the source's Galois permutation / character-isotypic calculation. It prevents presenting that general mechanism as new. Search returned the primary abstract, while direct full-page access returned 403; the exact all-abelian generic projection formula was not compared theorem by theorem.

### Exact resource/model boundary

The present gate-cut result counts nonrational scalar multiplications on complex scalar wires while rational complex-linear combinations are free. Standard DFT tables may instead count real multiplications, permit real/imaginary rewiring, allow a larger free field, or count all nontrivial constants. Those are different models. N=4 exposes the difference: the present Q-base count is at least one because i is nonrational, while a real-expanded F_4 uses only 0,±1 coefficients. No numeric Winograd bound is imported without matching these conventions.

## 2. Galois/rational character algebra

### Chien–Flynn–Waldron, 2015: full relevant section inspected

*Tight frames for cyclotomic fields and other rational vector spaces*, Linear Algebra and its Applications 476, 98–123, DOI 10.1016/j.laa.2015.02.021. Author-hosted final paper: https://www.math.auckland.ac.nz/~waldron/Preprints/Rational-frames/1-s2.0-S0024379515001275-main.pdf .

Theorem 6.1 and equations (6.17)–(6.18), printed pages115–116, construct rational orthogonal projections from Fourier characters indexed by units and use Galois action and Ramanujan sums. Theorems6.2–6.3 discuss irreducibility and cyclotomic dependence spaces. Their projection has rank φ(n), and the complementary dependence space has dimension n−φ(n). Those are different objects from entrywise L(F_n), whose generic annihilating-Q rank is n−τ(n). The paper is direct prior art for the Galois/Fourier/Ramanujan mechanism, not an inspected assertion of the identical n−τ(n) theorem.

### Tóth, 2012: full text inspected

*On the number of cyclic subgroups of a finite abelian group*, Bull. Math. Soc. Sci. Math. Roumanie 55(103), 423–428: https://arxiv.org/abs/1203.6201 ; full HTML https://arxiv.org/html/1203.6201v2 . The paper gives explicit cyclic-subgroup enumeration formulas for products of cyclic groups and their coprime multiplicativity. This supports the classical status of c(A) and the product-group counting step. It does not itself assert the projected-character-table rank law.

### Source's 2008 link: identity resolved, scope retained

The source cites https://www.sciencedirect.com/science/article/pii/S0166218X08000486 without its title. It is A. Silverberg's *Applications to cryptography of twisting commutative algebraic groups*, Discrete Applied Mathematics156(16),3122–3138, DOI10.1016/j.dam.2008.01.024. The publisher text identifies a survey of Galois-module twists and points to Mazur–Rubin–Silverberg, *Twisting commutative algebraic groups*, Journal of Algebra314(2007),419–438, as a main source. The author-hosted PDF was discovered at https://www.math.uci.edu/~asilverb/bibliography/silverbergsas.pdf but its full read returned502. Therefore this pass does not certify an exact lemma number in that paper for the source's rational-character-orbit assertion. The assertion is proved directly in our audit instead.

## 3. Source claims and responsible classification

- Generic rank formula: proved here in full, with exact field and parameter definitions. It is a clean consequence of standard Galois/finite-character decomposition. Historical novelty unverified.
- One-layer channel corollary: proved; arbitrary-depth scalar-linear gate-cut strengthens its stated scope. The gate-cut argument is elementary multiplicative-complexity reasoning. Do not label it a new general complexity method.
- Nonzero-scalar normalization lemma: complete proof and independent reviewer agreement. It supplies a useful missing fusion interface. Project-level derivation does not establish publication novelty.
- Isolated diagonal optimality: a direct rank argument. It remains valid at arbitrary scalar-linear depth, but cannot be added through a fused product.
- F014 / Weyl extraction / inverse fusion: only hypothesis-matched consequences in THEOREMS_AND_AUDIT.md §7. No branch-to-gate conversion or unrestricted runtime implication is asserted.

## 4. Concrete next literature action

The most valuable remaining comparison is lawful full-text acquisition of Tolimieri1986 and both relevant Auslander–Feig–Winograd1984 papers, followed by matching their base fields, circuit classes, rational-subspace invariants, and exact formulas. The current evidence is enough to withhold novelty; it is not enough to attribute the exact generic |A|−c(A) statement to a particular earlier theorem. No access restriction was bypassed and no full-text inspection is claimed where only an abstract was visible.
