Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 2b0a65f079b0c472c72668b3387141cf8d8e675ec4bb4a30225fe6b688181c2a

---

# NF-08 whole-target scalar resources: independent bounded review

Date: 2026-10-12. Verdict: **ACCEPT, bounded**. The final input binding and seal identify the exact reviewed candidate. No candidate/source executable was run or imported. No external writes were performed.

## Result

The candidate's general whole-target lower bound, quadratic equality, independent-input composition rule, exact nine-branch F3 identities, and stated algebraic operation ledgers are sound. The supplied example distinguishes three different targets:

1. Each of nine branch matrices separately: exact nonrational scalar optimum 3, giving a sum of isolated optima of 27.
2. All 27 branch-output coordinates on the same three inputs: exact optimum 3.
3. Their three-coordinate sum, F3 x: exact optimum 1.

The specified shared Green evaluator executes 31 nonrational and 32 rational wire scalings, 48 additions/subtractions, nine nonzero branch contributions, and six nontrivial cyclic solves. It is one explicit evaluator, not an optimal total-arithmetic algorithm or a scalar lower bound of 31. A one-gate evaluator of the final target executes no Green solves.

The canonical ordered-pair representation lower bound is separately 3 branches. The provided nine-branch representation does not establish sharpness. Multiplying this branch lower bound by a scalar-gate lower bound is unsupported.

## Independent proof audit

Fix the base field k and scalar-wire convention before measuring complexity. Represent a wire by its coefficient row in C^n. Let q_1,...,q_s be the coefficient rows at all charged non-k scaling outputs. All other operations are k-linear, so every wire row belongs to the k-span of the input rows and q_1,...,q_s. This remains true regardless of fanout, reuse, or scalar-linear depth.

Passing to C^n/k^n removes the uncharged input-row contribution. Thus the k-span of the target output row classes has dimension at most s. For T=T_0+sum_j theta_j T_j over a finite extension with basis starting with 1, the coordinate representation of these row classes is exactly the horizontal concatenation [T_1 | ... | T_d]. Its rank is therefore a lower bound on the total charged nonbase gates. This quotient proof also allows intermediate constants outside the target coefficient field. It does not assume an unjustified multiplicative property of coefficient extraction.

This is equivalent to the author's single whole-graph cut T=R+BH. The author's extension of coefficient functionals to the finite k-span of the relevant intermediate coefficients is valid. The basis-change argument is also valid: changing nonbase basis classes changes component blocks by an invertible k-linear block transformation.

The upper bound sum_j rank_k(T_j) follows from ordinary rank factorizations. In a quadratic extension there is only one nonbase component, so the upper and lower bounds agree. Every required input-dependent multiplication by theta is charged; coefficient preparation alone cannot substitute for those gates.

For disjoint-input, disjoint-output block-diagonal targets, a column permutation groups the horizontally concatenated coefficient matrices into disjoint blocks. Their ranks add. In a common quadratic extension this proves additivity of the exact nonbase scalar optima. It does not prove arbitrary higher-degree scalar-complexity additivity, a general bilinear direct-sum theorem, or additivity for shared-input stacks or serial compositions.

The higher-degree example (zeta_5 x, zeta_5^2 x) has concatenated rank 2n, while every one-functional specialization has rank at most n. The larger bound is legitimate: the complete output has 2n coordinates. Horizontal concatenation is essential; vertically stacking the component matrices would give a different, weaker invariant here.

## Frozen field and cost-model checks

The exact example uses Q[w]/(w^2+w+1), with the algebraic root and rational constants supplied. Arbitrary complex scalar input wires are not split into rational or real/imaginary coordinates. The rational coefficient pairs used for verification and constant compilation are descriptions of fixed constants only.

Permitted uncharged operations for the optimum theorem are arbitrary base-field linear operations and routing. Multiplication of a scalar wire by every nonbase constant is charged, even for a reused or precomputed constant. Input-dependent multiplication/division, conjugation, coordinate extraction, and vector gates disguised as scalar gates are excluded. Those exclusions are material.

The theorem supplies no lower bound on rational scalings or additions considered separately. It also supplies a lower bound on any inclusive scalar-gate measure, but cannot recover a nontrivial total-arithmetic bound from nonbase rank alone. The example's rational and additive counts are literal upper ledgers for particular evaluators, not lower bounds.

“Full I/O” here means all specified external scalar inputs are read and all specified scalar outputs are written. It does not mean a machine-memory traffic audit. Register copies, indexing, fanout, rational numerator/denominator arithmetic, field construction, root search, and bit/precision costs are outside the declared unit-cost algebraic model. No such excluded costs should be implied by an abbreviated row entry.

## Fresh exact controls

The reviewer authored `independent_controls.py` using SymPy 1.14 rational polynomial reduction, independently of the candidate's Fraction-pair implementation.

- Constructed each actual matrix (I-alpha S)^-1(I-beta T)^-1 for alpha,beta in {0,2,3}.
- Solved an independent 18-by-18 rational system for the real field-coordinate pairs of all nine branch coefficients directly from these Green matrices. The system has rank 18 and reproduces all supplied coefficients. This route does not reuse the candidate's Vandermonde construction.
- Compared every full branch matrix and their complete sum against F3 exactly. These are symbolic coefficient identities for arbitrary input, not sample-only verification.
- Independently reconstructed ordered S^i T^j coefficients. Their matrix has determinant -1-w and rank 3. Each legal branch coefficient matrix has rank at most one, establishing the separate canonical representation bound.
- Verified all nine rational nonbase-component determinants are nonzero, all nine ranks are 3, the 27-by-3 stack has nonbase rank 3, and F3 has nonbase rank 1.
- Ran a separately authored symbolic-wire DAG and stored every counted scaling and addition/subtraction in `EXACT_DAG_EVENTS.json`.
- Checked 189 generated rational rank-factorization cases, including zero and deficient rank.
- Checked 24 random reused scalar-linear circuits over Q[zeta_5], inspecting the quotient-rank invariant after every step.
- Checked nine shared-input repeated-output targets against nine independent-input direct sums, and nine higher-degree horizontal-concatenation controls.

Finite controls supplement the written proofs; they are not proof-assistant formalization or historical evidence.

## Count reconciliation

The shared diagonal Green preprocessing uses six scalings, four nonbase and two rational. Six rational S-solves each use five rational scalings and four additions. Nine branch coefficients, all nonrational, are applied to three coordinates each, costing 27 nonbase scalings. Summing the nine vectors costs 24 additions. This gives 63 scalings = 31 nonbase + 32 rational, and 48 additions. Input reads are 3; summed-output writes are 3. Materializing the branch stack instead costs the same scalings, 24 additions, and 27 output writes.

The setup source was inspected inertly and its exact loop sizes were audited, not replayed. The static accounting is:

- Root power: 1 multiplication.
- Parameter squares: 3 multiplications.
- Three-by-three augmented Gauss-Jordan inverse: 54 multiplications, 36 subtractions, 3 inversions.
- One third: 1 inversion.
- Nine three-term Weyl coefficients: 9 multiplications, 18 additions.
- Two three-by-three matrix products: 54 multiplications, 36 additions.
- Three cubic denominators: 3 multiplications, 3 subtractions.
- Nine branch weights: 18 multiplications.
- Six diagonal reciprocals: 6 multiplications, 6 subtractions, 6 inversions.
- Two cyclic normalizations: 2 inversions.

Total: 148 field multiplications, 54 additions, 45 subtractions, 12 inversions. These are setup field operations, not additional input-dependent nonbase gates.

Compiling all branch matrices by three fixed basis-input evaluations adds 189 field multiplications and 72 additions, giving 337 multiplications, 126 additions, 45 subtractions, 12 inversions, and 162 fixed coefficient-component extractions. The direct three-nonbase-gate stack reconstruction then uses 162 rational scalings, 135 additions, three input reads, 162 coefficient-record reads, and 27 output writes. This cheaper nonbase count has larger total arithmetic; no speed conclusion follows.

The explicit one-nonbase-gate F3 formula has seven additions/subtractions, three input reads and three output writes. With its supplied w, it needs no further arithmetic setup. Compiling an arbitrary general representation into that formula is a different, unproved compiler-cost question.

## Classical antecedents and novelty boundary

Primary/institutional records verified during this review:

- S. Winograd, *On the multiplicative complexity of the Discrete Fourier Transform*, Advances in Mathematics 32 (1979), 83–117, DOI [10.1016/0001-8708(79)90037-9](https://www.sciencedirect.com/science/article/pii/0001870879900379). The publisher's indexed abstract describes DFT multiplicative lower bounds and attainment at prime lengths. Direct full-page retrieval was denied, so theorem-level correspondence was not checked.
- L. Auslander and S. Winograd, *The multiplicative complexity of certain semilinear systems defined by Polynomials*, Advances in Applied Mathematics (1980), DOI 10.1016/0196-8858(80)90013-5. [IBM's publication record](https://research.ibm.com/publications/the-multiplicative-complexity-of-certain-semilinear-systems-defined-by-polynomials) verifies title, authors, year, and publication link; it supplies no abstract. This is bibliographic context only.
- L. Auslander, E. Feig, S. Winograd, *The multiplicative complexity of the Discrete Fourier Transform*, Advances in Applied Mathematics (1984), DOI 10.1016/0196-8858(84)90005-8. [IBM's publication record](https://research.ibm.com/publications/the-multiplicative-complexity-of-the-discrete-fourier-transform) states that the paper computes DFT multiplicative complexity for arbitrary data-point sets. No theorem-level identification is asserted here.

The quotient-span/gate-cut argument and rank factorization are elementary classical machinery in a long-established subject. This packet may be accepted as a useful project theorem and resource-accounting correction. The review does not establish that this exact joint-invariant formulation is historically new or identify its earliest publication. No “new lemma” or global priority promotion is supported. Bibliographic and abstract matches are not a novelty clearance.

## Scope and remaining work

Accepted scope: “Whole-target nonbase-scalar rank theorem and quadratic exactness; disjoint-input composition rule; exact F3 shared-output counterexample and separated algebraic ledgers independently accepted.”

Keep the broader NF-08 resource gate **progressed/open**, not complete. The next obligation is an actual proposed growing-length fused target with one frozen base field, scalar-wire graph and permitted branch grammar; prove a lower bound for its complete target, account for actual shared evaluation, and pay coefficient construction, rational preparation, endpoints, and complete readout in the chosen total-cost model. Apply relevant bit/precision costs if a numerical or machine claim is intended. Do not sum isolated stage ranks, multiply unrelated resource lower bounds, or silently change coefficient fields at the interface.

Unsupported promotions include general-N FFT superiority, universal Omega(N log N), o(N log N) full DFT evaluation, the original warm-CSE counts, optimal rational-operation counts, sharp canonical branch representations, higher-degree exact scalar complexity, and historical priority. The candidate's existing rejection of unrelated I26/I29 aggregation claims must remain intact.
