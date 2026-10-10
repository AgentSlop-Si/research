# Final focused publication assessment

10 October 2026, 02:08 UTC. Private research assessment; no submission or public release.

## Executive judgment

The strongest current manuscript is the exact-three Green theorem: an infinite arithmetic family of five-dimensional principal blocks has additive Green length exactly three, with a uniform quadratic-extension construction matching an all-order, boundary-inclusive exclusion of two summands. The full ambient matrices inherit a lower bound only. This distinction is essential to its title, abstract and theorem statement.

The sharp dyadic endpoint theorem is the cleanest independent short-paper candidate: its exact minimax is N/4+1, attained by double bit reversal, with an all-endpoint second-moment lower bound. Double bit reversal and its rank-one Fourier hierarchy are established prior art. The final 2008 Delvaux–Van Barel article still needs comparison against the official preprint before any priority claim.

The three-stage discrepancy obstruction and one-layer arbitrary-order Green obstruction are plausible substantial application theorems. The former supplies an Ω(log N) quasiseparable-order obstruction in its stated endpoint class; the latter supplies an Ω(log log N) additive branch lower bound in a different, one-layer model. They should not be blended into an arithmetic FFT lower bound.

The Phase21 resultant formula remains accepted mathematics, but it is lower priority as a standalone paper. Its entire factor/reciprocity package extends arbitrary diagonal-scaled square-matrix pencils and follows standard resultant/Newton-valuation mechanisms. Preserve the exact closed-form identity and its application, but do not advertise a new general elimination theory. The graph solver has a still sharper prior-art overlap: transfer maps, singular constraints and cycle consistency are already central to linear-time quantum 2-SAT algorithms over C.

These are evidence-based publication judgments, not certifications of worldwide novelty or predictions of journal acceptance. “Accepted” below refers to an internal independent proof/certificate review, not peer review by a journal. An original formula can be elementary, a useful tool can be established, and a correct finite certificate can fall short of a uniform algorithm.

## Scope and what changed since the initial report

- The accepted C_q review is incorporated with seal bcfd6469945506c291d025856353900654026159fe8ac434a189a10fa68abd5a. It settles the previously pending restricted-family upper bound, not a full B_N upper bound.
- The complete factor construction is fixed-dimensional. Its rational-coordinate heights are O(log q), with one genuine quadratic extension and all 27 guards uniform in q by localization. Application uses two five-entry solves and a diagonal correction.
- The same two-natural-cycle-plus-diagonal ansatz cannot represent the full B_N for odd N≥7 because its relevant cut rank is at most two while the target rank is floor(N/2). Other cycle-order choices are not excluded by that argument.
- The all-length Bluestein implication is conditional on a hypothetical full uniform transform family and compatible-field/root setup. The five-coordinate construction does not instantiate that premise.
- The resultant and endpoint comparisons are resolved as far as currently accessible primary evidence permits. The exact broader-pencil derivation and the final-paper access gap are documented in the preserved addendum.
- Eighteen actual proof/review documents were read for the focused claim set, with hashes rechecked at sealing. Twenty-eight primary references are recorded with differing inspection depths. Abstract-level comparisons are labeled as such. Source code from uploaded research packages stayed inert. Only freshly authored small corroborating controls were run for the assessment-level pencil derivation.

## Ranked evidence table

The compact table is a navigation aid. The full exact claim, prior-art delta, limitations, proof status, missing work and possible manuscript proposition follow for every row. Stable claim identifiers retain the initial categories; priority ranks have changed.

| Priority | Stable claim | Candidate | Assessment |
|---:|---|---|---|
| 1 | C01 | Exact additive Green length three for an infinite five-dimensional family | Plausibly original exact-minimum theorem package; strongest current Green manuscript core |
| 2 | C02 | Sharp endpoint-permutation quasiseparable order of dyadic Fourier matrices | Plausibly original sharp extremal theorem; clean short-paper candidate |
| 3 | C04 | Three-stage quasiseparable Fourier obstruction through discrepancy | Substantial new application of classical discrepancy theory |
| 4 | C05 | One-layer Fourier obstruction for independently ordered weighted-permutation Green sums | Substantial specialized application of classical combinatorics and Fourier minors |
| 5 | C06 | Exact recognition of common-quadratic-phase sparse Fourier sums | Plausibly original exact-recognition/elimination theorem; known signal model |
| 6 | C07 | Two-sided Green rectangle rank oracle and moving-interface certificates | New synthesis/certification application; most structural algebra already known |
| 7 | C08 | Marked-tree constant-input jets and exact forbidden-run frontiers | Useful specialized structural lemma and evaluator analysis |
| 8 | C03 | Universal reciprocal factorization of adjacent Hankel-pencil resultants | Possibly original explicit formula/application; modest standalone significance after broader-pencil comparison |
| 9 | C09 | Exact N16 coefficient existence certificate | New finite construction plus reproducible certification engineering |
| 10 | C10 | Projective graph constraint solver | Known core over C; possible new field-general implementation and Green application |
| 11 | C11 | Uniform sparse-inverse and low-rank perturbation gates | Elementary corollaries of known uncertainty and rank identities |
| 12 | C12 | Aggregate-fiber sparse recognizer | Known sparse-recovery tools with a useful fully charged promise |
| 13 | C13 | Fixed-direction completion and fixed-pencil exclusion certificates | Application/engineering evidence rather than a main new theorem |

## Detailed claim cards

### 1. Exact additive Green length three for an infinite five-dimensional family (C01)

**Classification:** Plausibly original exact-minimum theorem package; strongest current Green manuscript core

**Exact claim:** Let N=5q², q positive odd, gcd(q,5)=1 and q≡1 (mod 241); let F_N[i,j]=ω^(ij), A_N=diag(ω^((N+1)j²/2)), and B_N=(F_N^(-1)+A_N)^(-1). On S={0,q²,2q²,3q²,4q²}, the principal block C_q=B_N[S,S] has minimum exactly THREE terms D_L(I-W)^(-1)D_R, where W follows a Hamiltonian cycle, zero edge weights and singular endpoint masks are permitted, and every resolvent denominator is legal. The upper construction uses a genuine quadratic extension of Q(η), η=ω^(q⁴), and two reciprocal-closing-weight nontrivial branches plus a diagonal zero-weight branch. The lower bound permits all structural orders. Hence full B_N requires at least three terms, with no matching full-size upper bound established. q=1 is the accepted forced B5 case. A separate positive-Gauss-curve argument gives a non-effective finite-exception lower-bound statement.

**Closest primary prior art:** P01, P02, P03, P07, P08

**Precise delta:** A matched exact additive length, rather than a fast application formula or generic multiplicative factorization. The base obstruction exhausts all 576 ordered cycle pairs, including projective boundary charts. Principal restriction and proper specialization transfer it to an infinite arithmetic family. The new upper construction is uniform in q, with all 27 guards justified by localization and norm residues, at both quadratic roots and all primitive fifth-root embeddings. Existing cyclic-bidiagonal inverse and Green/quasiseparable representation theorems do not supply this exact minimum.

**Strength and limitations:** This is an infinite-parameter family of FIXED 5-by-5 matrices, not a growing-dimensional upper construction. Three summands means two nontrivial solves and a diagonal correction. Over the base field alone the same upper length has not been established. For full B_N only the lower bound is proved. Moreover the same two-natural-cycle-plus-diagonal ansatz is impossible at every odd N≥7: its complementary cut rank is at most two, while B_N has a half-cut of rank floor(N/2). This does not exclude three terms with other structural orders. The conditional Fourier/Bluestein bridge requires a full uniform family, charged setup and compatible roots; C_q supplies none of those missing premises.

**Proof status:** Accepted independent reviews E01–E03 and E18. The new review seal is bcfd6469945506c291d025856353900654026159fe8ac434a189a10fa68abd5a. Actual proof/review read; no source executables replayed in this novelty pass. The lower certificate establishes geometric-fiber emptiness, not merely an empty finite-field point scan; the upper guards are uniform local-ring arguments, not extrapolations from sample q.

**Missing work:** Package a compact theorem-and-certificate release with a standalone checker and a human-readable explanation of the finite obstruction. State the field of definition in every length claim. A further focused additive-resolvent/secant-literature comparison remains advisable before submission. A higher-dimensional upper construction is a separate research goal and not a missing premise of the five-dimensional theorem.

**Plausible manuscript proposition:** “Exact additive length in an arithmetic family of cyclic-resolvent decompositions.” Main theorem: ℓ_G(C_q)=3 for the stated infinite family; corollary: ℓ_G(B_(5q²))≥3. Supporting propositions: principal-restriction closure, closed-projective specialization, guarded reciprocal-pole synthesis.

**Local evidence:** E01, E02, E03, E18

### 2. Sharp endpoint-permutation quasiseparable order of dyadic Fourier matrices (C02)

**Classification:** Plausibly original sharp extremal theorem; clean short-paper candidate

**Exact claim:** For N=2^m>=8 over characteristic zero, min_{rho,sigma} q(P_rho F_N P_sigma^T)=N/4+1, where q is the maximum rank over all strict upper-right and lower-left complementary cuts. Double bit reversal attains it. Its upper-right cut ranks obey r_N(k)=ceil(k/2)+r_{N/4}(floor(k/2)) for k<=N/2, with reflection symmetry. Exact total-rank minima are also established at N=8,16.

**Closest primary prior art:** P15, P10, P22, P26, P27, P28

**Precise delta:** The all-independent-endpoint minimax value, with a second-moment/odd-cardinality lower bound matching a bit-reversal recurrence. Prior Fourier submatrix theory already contains double-digit-reversal rank-one block grids and sharp support uncertainty, so those ingredients must be credited.

**Strength and limitations:** An exact all-size formula is substantially stronger than a finite screen and does not require source code. It is a rank-structure theorem, not an arithmetic lower bound: high cut rank alone does not make matrix application expensive. Characteristic-zero positivity is essential to the supplied lower-bound proof; arbitrary finite fields are outside it.

**Proof status:** Accepted E04; actual proof read. The official Delvaux–Van Barel TW470 preprint was inspected at Lemma 8, Theorem 10 and Sections 3–4. Accessible later primary universal-sampling/full-spark/conditioning papers were compared in the addendum. The final 2008 journal version remains unavailable in full; this is an unresolved comparison, not evidence that it lacks the theorem.

**Missing work:** Obtain a legitimate full copy of the final Delvaux–Van Barel 2008 article and check any changes from TW470. Make the new universal second-moment lower bound central, credit the existing double-bit-reversal hierarchy, and distinguish exact q-minimax from unproved larger-size total-rank minima.

**Plausible manuscript proposition:** “The minimum quasiseparable order of a dyadic Fourier matrix under independent endpoint permutations.”

**Local evidence:** E04

### 3. Three-stage quasiseparable Fourier obstruction through discrepancy (C04)

**Classification:** Substantial new application of classical discrepancy theory

**Exact claim:** For F_N represented as S3 P2 S2 P1 S1 with q(S_i)<=r_i, arbitrary independent internal permutations, and at least one affine-coprime Fourier endpoint ordering, the other endpoint arbitrary, necessarily 2r1+r2+r3>=c log N-2; transposition gives r1+r2+2r3>=c log N-2. Repeated bit reversal additionally yields r1+r2+r3>=ceil(log2(N)/2), excluding rank-one stages for dyadic N>=128.

**Closest primary prior art:** P03, P16, P17, P22

**Precise delta:** The bridge from cyclic-window full-rank conditions to grid discrepancy of an internal permutation. Averaging all cyclic windows gives the exact centering Wt/N; applying Schmidt then excludes every fixed-order three-stage family in this scope.

**Strength and limitations:** This is an infinite-family obstruction with a conceptual connection beyond the original search. Schmidt’s lower bound and quasiseparable rank calculus are prior art. Both endpoints arbitrary and non-affine are not covered; no general arithmetic lower bound or arbitrary-depth exclusion follows.

**Proof status:** Accepted E05. Rank proof and cyclic averaging read. Schmidt’s original publisher record was located; its precise theorem/normalization was verified in primary paper P16 because the original PDF was inaccessible.

**Missing work:** Compare permutation discrepancy and low-rank factorization literature beyond keywords; decide whether to combine with the endpoint minimax theorem; extend endpoint scope or stage count if possible; do not invent an explicit c or finite cutoff from the existential discrepancy constant.

**Plausible manuscript proposition:** “Permutation discrepancy as an obstruction to shallow quasiseparable Fourier factorizations.”

**Local evidence:** E05

### 4. One-layer Fourier obstruction for independently ordered weighted-permutation Green sums (C05)

**Classification:** Substantial specialized application of classical combinatorics and Fourier minors

**Exact claim:** Over C, F_N cannot equal a sum of r diagonally ended legal weighted-permutation resolvents, plus rank-t, row-degree-s sparse and arbitrary diagonal corrections, once N>2(m-1)(B-m)(B-1), where m=r+t+1, L=m(s+2), B=(L-1)^{2^{r-1}}+1. Independent structural cycle orders, zero weights and singular diagonal masks are allowed. Fixed t,s imply r=Omega(log log N).

**Closest primary prior art:** P01, P03, P10, P11

**Precise delta:** Combines rank-one separated rectangles for each independently ordered resolvent, simultaneous monotone-subsequence extraction and a short-arc Schur-polynomial Fourier-minor argument. The arbitrary-order one-layer obstruction does not follow from the separate sparse-inverse/rank gate.

**Strength and limitations:** Useful theorem for restricted linear representations; explicit r=2 threshold N>2300 and r=3 threshold N>34,545,588 are large but rigorous. Unmatched independent row/column permutations on each term are excluded. Products of layers escape the proof; the term lower bound is very weak compared with FFT arithmetic complexity.

**Proof status:** Accepted E14. Full all-size argument and threshold derivation read. The broad ingredients are classical; their precise combination remains a plausible new application, not confirmed historical priority.

**Missing work:** Search additive rank-structured decomposition and simultaneous-order/Ramsey literature; sharpen thresholds or growth if feasible; formulate general target-minor hypotheses to give a theorem beyond Fourier; explain explicitly why product grammars are not covered.

**Plausible manuscript proposition:** “Additive obstructions for independently ordered cyclic resolvents and Fourier matrices.”

**Local evidence:** E14

### 5. Exact recognition of common-quadratic-phase sparse Fourier sums (C06)

**Classification:** Plausibly original exact-recognition/elimination theorem; known signal model

**Exact claim:** For x_j=omega^{a j^2} sum_{ell<=r} c_ell omega^{b_ell j}, over a supplied prime field/root subgroup with N>=3r, there is a sound and complete exact recognizer, with zero-vector handling. A centered normalized (r+1)-Hankel determinant has a provably nonzero constant coefficient, degree <=binom(r+2,3), and every true common phase supplies a root. Candidate recurrence recovery and full verification cost O_r(N). An accepted ring-Toeplitz extension yields a conservative uniform O(N r^4+r^{2+3 log_2 3}) bound.

**Closest primary prior art:** P14, P18, P19, P21

**Precise delta:** The nonzero eliminant guaranteed for every nonzero promised input, a degree bound limiting candidate phases, parity-aware phase quotient, and charged exact membership verification. Common chirp models, rank constraints, Prony/Berlekamp–Massey and Toeplitz/Bareiss/Levinson tools are not new.

**Strength and limitations:** This can support an exact symbolic/signal-recovery paper. The structured family is small; N>=3r is a sufficient bound, not established optimal identifiability. Growing r=o((log N)^{1/4}) gives a sub-N log N bound only on that structured class with a supplied field/root, not generic DFT data or stable floating point.

**Proof status:** Accepted E06–E07 and linked growing-rank corollary. Actual normalization, constant-term and ring-pivot reasoning read; source code not executed.

**Missing work:** Finish comparison with polynomial-phase Prony and finite-field sparse interpolation; make the representation equivalence classes explicit; sharpen dependence on r or show it matters practically; include rejection costs, field construction and numerical limitations.

**Plausible manuscript proposition:** “A nonvanishing phase eliminant for exact common-chirp sparse Fourier recognition.”

**Local evidence:** E06, E07

### 6. Two-sided Green rectangle rank oracle and moving-interface certificates (C07)

**Classification:** New synthesis/certification application; most structural algebra already known

**Exact claim:** For a legal Hamiltonian-cycle resolvent K^{-1}, rank K^{-1}[A,B]=|A|+|B|-N+rank K[B^c,A^c]. Proper support deletions leave bipartite paths, so structural rank equals maximum matching and is computable in O(N). Independent endpoint permutations/masks can be tracked. Product certificates use arbitrary intermediate sets and rank(AB)[R,C]<=rank B[S,C]+rank A[R,S^c]. The two-stage cut objective is submodular and polynomially optimizable by known oracle methods.

**Closest primary prior art:** P03, P04, P09, P22

**Precise delta:** A usable exact support-aware oracle and moving-cut certificate specialized to the branch grammar, including a concrete Fourier spectral-error witness. Nullity duality, graph rank closure and submodular minimization are prior results.

**Strength and limitations:** Potential framework section or software-assisted certification paper if demonstrated on a broad class. A single oracle/certificate can be linear time, but optimization is not thereby linear. Exact ranks with singular endpoint masks require deleting their supported coordinates rather than silently retaining equality.

**Proof status:** Accepted E08. Exact support/forest proof and optimization scope read.

**Missing work:** State the distinct costs of oracle, optimization and matrix execution; compare directly with graph-induced rank structures; add a general separation or an algorithmic improvement rather than recasting known inequalities.

**Plausible manuscript proposition:** “Support-aware cut certificates for products of cyclic resolvents.”

**Local evidence:** E08

### 7. Marked-tree constant-input jets and exact forbidden-run frontiers (C08)

**Classification:** Useful specialized structural lemma and evaluator analysis

**Exact claim:** For the doubling-tree A0 and stationary root projector E, (I-z A0)^{-1}=K(z)+E/(1-z), with K=sum_{t<n}z^t(A0^t-E). Constant-input full polynomial jets have total coefficient capacity <=2N-2 and can be formed in O(N). For a retained suffix 0^b, the explicit frontier evaluator has exact F_L=2^{n-d_L} A_b(d_L), d_L=min(n,b+L), and total cost Theta(N min(n+1,2^b)), where A_b counts binary words avoiding 0^b.

**Closest primary prior art:** P12, P03

**Precise delta:** The precise cancellation/valuation ledger for this marked tree and the exact b-dependent count for this evaluator. Finite nilpotent resolvents, tree dynamic programming, Schur complements and forbidden-word recurrences are established mathematics.

**Strength and limitations:** The linear constant-input jet is real positive progress. It does not imply a linear solver for polynomial-valued unknowns or an inexpensive inverse of the border. The frontier lower bound applies to the specified explicit representation, not every algorithm.

**Proof status:** Accepted E09 and its linked root-pole proof. One next-pivot constant-input closure was accepted; arbitrary repeated polynomial-input closure is not.

**Missing work:** Extract a general theorem for a nontrivial class of functional graphs or valuation-weighted trees; compare total path-length/output-sensitive algorithms; resolve polynomial-input closure for a stronger algorithmic contribution.

**Plausible manuscript proposition:** “Output-sensitive polynomial jets on marked functional trees and their frontier growth.”

**Local evidence:** E09

### 8. Universal reciprocal factorization of adjacent Hankel-pencil resultants (C03)

**Classification:** Possibly original explicit formula/application; modest standalone significance after broader-pencil comparison

**Exact claim:** Let m=s+1, P_e(a,w)=det[T_{e+i+j}(1-a w^{e+i+j})] for e=0,1 and 0<=i,j<m, with formal independent T_0,...,T_{2s+1}. With fixed-degree-m Sylvester resultant R_s=Res_a(P_0,P_1), D=m^2(2m-1), v=s(s+1)(4s+5)/6 and b=s(s+1)(2s+1)/6: w^D R_s(1/w)=(-1)^{m^2}R_s(w), R_s=w^v(w-1)^{m^2}U_s, w^{2b}U_s(1/w)=U_s(w), and U_s=w^b V_s(w+w^{-1}) with deg V_s<=b. The valuation v is generically exact; all identities survive singular and zero-resultant specializations.

**Closest primary prior art:** P20, P21, P24, P25

**Precise delta:** The explicit factors, closed-form generic zero valuation and compressed degree are the identifiable formula-level delta. The same complete package holds for arbitrary coefficient matrices A,B in det(A−aDAD), det(B−awDBD), so adjacency and Hankel structure are unnecessary for these identities. Standard resultant transformation laws, mixed-minor expansions and unequal-slope Newton valuation rules provide the mechanism. No inspected primary source literally states this exact formula; that is not a global novelty conclusion.

**Strength and limitations:** Correct and useful all-s algebra, but the broad-pencil derivation is short once standard machinery is recognized. Compression reduces a degree with cubic growth in s by a constant factor; it does not establish an asymptotic elimination breakthrough. A standalone substantial manuscript would need a stronger recovery theorem, broader classification or demonstrated algorithmic advance. Its supplied fixed-s application is conditional on nonzero probes, a nonzero resultant, a linear gcd and spectral invertibility. It is not an all-input generic FFT.

**Proof status:** The Hankel specialization is accepted E17. The arbitrary-matrix generalization and its symbolic proof are assessment-level work in ADDENDUM_20261010_0149.md, corroborated by six fresh small fixed-degree Sylvester controls, and are NOT separately independently reviewed. No submitted research program was executed.

**Missing work:** Keep the precise universal identity as a lemma or compact note; do not frame it as a new elimination method or intrinsically Hankel phenomenon. Independently check the broader-pencil derivation before incorporating it into a manuscript. Establish a stronger application or structural classification before assigning standalone publication priority.

**Plausible manuscript proposition:** “Universal factors in diagonally scaled matrix-pencil resultants.” A short theorem/technical appendix with the explicit exponents; the sparse-rational recovery application must carry its guards and cost model.

**Local evidence:** E17

### 9. Exact N16 coefficient existence certificate (C09)

**Classification:** New finite construction plus reproducible certification engineering

**Exact claim:** An exact F16 exists in the fixed model H2 H1 B H0 with eight fixed Hamiltonian routes/poles per layer, 24 branch occurrences and 384 complex endpoint parameters. In a 256-dimensional affine chart, a rational contraction certificate isolates a unique root within radius 10^{-9}; it proves nonzero endpoint margins and the full matrix equality.

**Closest primary prior art:** P13, P01

**Precise delta:** An exact reproducible witness for this particular constrained architecture, replacing a floating residual. Rational nonlinear-root certification itself is established.

**Strength and limitations:** Worth preserving as a benchmark/counterexample and appendix. The parameters exceed N^2, and the result has no uniform coefficient generator, growing-size theorem, synthesis complexity bound or cost advantage. “Positive coefficient certificate” means affirmative existence, not positive real coefficients.

**Proof status:** Accepted E10 with exact rational contraction bounds, not just supplied optimizer output. This novelty pass read the audit, without rerunning it.

**Missing work:** Find a compact algebraic pattern, parameter compression, minimality or an infinite lift; otherwise do not build the main publication claim around one overparameterized N16 fit.

**Plausible manuscript proposition:** “A certified finite Fourier factorization in a fixed cyclic-resolvent architecture,” as an example within a broader theorem paper.

**Local evidence:** E10

### 10. Projective graph constraint solver (C10)

**Classification:** Known core over C; possible new field-general implementation and Green application

**Exact claim:** Solve selected constraints u_k^T L_e u_i=0 on P1: invertible edges transport projective directions; cycle closures restrict a component to all P1, at most two points, or empty; rank-one edges become equality-literal disjunctions treated by 2-SAT and domain consistency. The accepted treatment includes infinity, repeated roots, characteristic two and algebraic-closure rejection by polynomial gcd.

**Closest primary prior art:** P05, P06

**Precise delta:** The finite-field/arbitrary-characteristic details and extraction from Green off-support equations may be useful additions. Over C the same bilinear product-vector constraints, transfer matrices, cycle eigenvectors and singular-edge logic already occur in quantum 2-SAT algorithms.

**Strength and limitations:** Do not claim a new general projective constraint-solving paradigm. The result solves a selected necessary row subsystem only; it does not finish column compatibility or scales, so success is not a Green factorization. This is the clearest novelty downgrade of the pass.

**Proof status:** Accepted E11 as a mathematical/algorithmic result. Its historical novelty was not certified by the local review. Primary quantum-2SAT texts were compared directly.

**Missing work:** Write an explicit reduction and theorem-by-theorem comparison with quantum 2-SAT; identify a genuinely absent characteristic/domain/complexity guarantee; position as a specialization unless that delta is substantial.

**Plausible manuscript proposition:** “Projective constraint propagation over general fields for cyclic-resolvent feasibility,” with quantum-2SAT attribution.

**Local evidence:** E11

### 11. Uniform sparse-inverse and low-rank perturbation gates (C11)

**Classification:** Elementary corollaries of known uncertainty and rank identities

**Exact claim:** If F=product_i H_i, H_i=G_i+R_i with invertible H_i,G_i, rank R_i<=r_i and column sparsity of G_i^{-1} at most s_i, then with r=sum r_i and s=product s_i, s(r+1)^2>=N. For a prime complex Fourier transform, (s+1)(r+1)>=p+1. Stage-count/work consequences require the stated fully materialized per-stage executor.

**Closest primary prior art:** P10, P11

**Precise delta:** A clean scope ledger and reusable test for a proposed circuit grammar. Inverse-difference telescoping, a sparse kernel vector and classical support uncertainty give the inequalities directly; no new general uncertainty theorem is supplied.

**Strength and limitations:** Useful lemmas and guards, unlikely standalone publication substance. Dense structured high-rank corrections and other executors remain outside the cost inference; prime complex additive uncertainty must not be copied to arbitrary finite fields.

**Proof status:** Accepted E12, including field limitations. The proof was read.

**Missing work:** Attribute the standard ingredients and retain as a proposition supporting a genuinely new representation theorem; avoid upgrading a restricted rank/cost gate into a general FFT lower bound.

**Plausible manuscript proposition:** “Uncertainty-based necessary conditions for sparse-inverse perturbation circuits,” as a supporting proposition.

**Local evidence:** E12

### 12. Aggregate-fiber sparse recognizer (C12)

**Classification:** Known sparse-recovery tools with a useful fully charged promise

**Exact claim:** With N=QM and total fiber modes <=K0, exact recognition and full output can be charged O(N+M K0+Q K0+K0^2). If K0=O(Q) and Q^2<=N, this becomes O(N), with rejected-input processing explicitly bounded.

**Closest primary prior art:** P14, P20

**Precise delta:** An aggregate rather than per-fiber promise and careful heavy/light accounting. Recurrence recovery, root enumeration, Vandermonde recovery and exact verification are standard.

**Strength and limitations:** Potential application or corollary; no generic-input transform improvement. Novelty is more likely in the precise recognition guarantee and accounting than the core algorithm.

**Proof status:** Accepted E13; reviewed theorem and scope.

**Missing work:** Compare closely with block sparse interpolation and sparse Fourier recovery; show a meaningful regime or new worst-case dependence beyond reassembling standard primitives.

**Plausible manuscript proposition:** “Exact aggregate-sparsity recognition for Fourier fibers,” as a corollary or applications section.

**Local evidence:** E13

### 13. Fixed-direction completion and fixed-pencil exclusion certificates (C13)

**Classification:** Application/engineering evidence rather than a main new theorem

**Exact claim:** For fixed projective row/column directions, full off-support vanishing plus supported affine scale equations and nonzero scale/cycle guards characterize invertible branch completion. Separately, several fixed-mask, one-parameter Green pencils are excluded by exact projective cross-ratios and modular nonzero resultants at specified finite sizes.

**Closest primary prior art:** P05, P06, P21

**Precise delta:** The exact specialization to these search grammars and independently checkable certificates. Sparse affine graph solving, projective invariants, resultants and saturation/guard discipline are established techniques.

**Strength and limitations:** Valuable reproducibility and search-space reduction. Fixed directions do not solve the full nonlinear problem, and fixed-pencil exclusions do not exclude the encompassing family. These belong with the successful construction/lower-bound paper rather than being promoted individually.

**Proof status:** Accepted E15–E16 within their exact scopes. No broad representation theorem inferred.

**Missing work:** Unify into a compact certificate format, preserve all guards, document verification versus discovery cost, and demonstrate a reusable mathematical consequence.

**Plausible manuscript proposition:** “Exact feasibility certificates for fixed cyclic-resolvent directions,” as a methods appendix.

**Local evidence:** E15, E16

## Manuscript decisions

1. Prioritize a Green-length paper built around exact ℓ_G(C_q)=3, with full B_(5q²)≥3 as a corollary. State the coefficient field, admissible structural orders, zero-edge convention and legal denominators before the theorem. A compact independently replayable finite certificate is part of the proof artifact, not a substitute for the specialization and guard arguments.
2. Develop the dyadic endpoint theorem as a separate short mathematical paper after obtaining the final Delvaux–Van Barel text. Its lower-bound invariant is the focal point; bit reversal is credited construction machinery. Exact larger-size sum-rank minima remain open unless separately proved.
3. The discrepancy and one-layer results could support a scoped obstruction paper if their models and prior-art deltas are presented separately and sharply. They are structural/rank statements, not universal FFT circuit lower bounds.
4. Keep the resultant formula, marked-tree jets and finite coefficient certificate as supporting material or targeted notes until an additional theorem elevates their standalone significance. The constant-input and fixed-dimensional promises are material, not implementation details.
5. Treat the projective solver and uncertainty gates as established mechanisms or applications unless a genuinely stronger field-general, complexity or recognition theorem is isolated. Test coverage and reproducibility are valuable engineering contributions, but source test counts do not establish novelty.

## Remaining bounded checks

The largest remaining priority check is the legitimate final copy of Delvaux–Van Barel (2008). For the Green-length package, the useful remaining literature question is narrowly additive: whether a previously published cyclic-resolvent/semiseparable sum-length classification already gives this exact family. Generic multiplicative diagonal-circulant factorization is not a substitute for that comparison. No amount of negative search results proves worldwide originality.

The next internal task is a source-claim crosswalk against the post-master queues, so that accepted corrections, new applications and duplicate source revisions are not counted as fresh theorems. That crosswalk will be a separate dated artifact rather than a silent change to this seal.

## Primary references and inspection depth

- **P01** [Huhtanen and Perämäki (2015), Factoring Matrices into the Product of Circulant and Diagonal Matrices](https://math.aalto.fi/~mhuhtane/manu.pdf). Full author manuscript; Proposition 2.5, Theorem 2.10 and main factorization compared.

- **P02** [Boito and Eidelman (2025), Computation of quasiseparable representations of Green matrices](https://arxiv.org/abs/2308.02701). Primary abstract and publication metadata; inverse-band/Green context, not a complete theorem-by-theorem comparison.

- **P03** [Chandrasekaran, Epperly and Govindarajan, Graph-Induced Rank Structures and their Representations](https://arxiv.org/html/1911.05858). Full text; Propositions 2.1–2.3 and cycle semiseparable discussion.

- **P04** [Strang (2010), Fast transforms: Banded matrices with banded inverses](https://pmc.ncbi.nlm.nih.gov/articles/PMC2906572/). Primary full-text search extract on nullity theorem; direct page intermittently blocked.

- **P05** [de Beaudrap and Gharibian (2016), A linear time algorithm for quantum 2-SAT](https://arxiv.org/html/1508.07338). Full text; transfer matrices, cycle eigenvectors, singular constraints and algebraic complexity.

- **P06** [Arad, Santha, Sundaram and Zhang (2018), Linear-Time Algorithm for Quantum 2SAT](https://theoryofcomputing.org/articles/v014a001/v014a001.pdf). Full text; Proposition 2.3, Theorem 2.4, product constraints and algorithm.

- **P07** [Stacks Project, projective morphisms are proper](https://stacks.math.columbia.edu/tag/01WC). Theorem checked; standard algebraic-geometric ingredient, not original to this project.

- **P08** [Gurevich, Hadani and Howe, Quadratic reciprocity and the sign of the Gauss sum via the finite Weil representation](https://arxiv.org/html/0808.2447). Primary text on odd-modulus Gauss sums and finite Weil representation.

- **P09** [Iwata, Fleischer and Fujishige, A combinatorial, strongly polynomial-time algorithm for minimizing submodular functions](https://arxiv.org/abs/math/0004089). Primary abstract; polynomial oracle-based optimization baseline.

- **P10** [Tao, An uncertainty principle for cyclic groups of prime order](https://arxiv.org/abs/math/0308286). Primary abstract/PDF and full-spark/support-sum statement.

- **P11** [Dvir and Liu (2019), Fourier and Circulant Matrices Are Not Rigid](https://arxiv.org/abs/1902.07334). Primary abstract and conference paper; comparison to unrestricted rigidity claims.

- **P12** [Guibas and Odlyzko (1981), String overlaps, pattern matching, and nontransitive games](https://doi.org/10.1016/0097-3165%2881%2990005-4). Publisher abstract; classical forbidden-pattern counting framework.

- **P13** [Hauenstein and Sottile (2012), alphaCertified: certifying solutions to polynomial systems](https://arxiv.org/abs/1011.1091). Primary abstract; exact rational certification baseline, distinct from the project’s particular Banach box.

- **P14** [Massey (1969), Shift-register synthesis and BCH decoding](https://crypto.stanford.edu/~mironov/cs359/massey.pdf). Original paper; shortest recurrence synthesis baseline.

- **P15** [Delvaux and Van Barel (2008), Rank-deficient submatrices of Fourier matrices](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW470.pdf). Official full 2006 preprint TW470; Lemma 8, Theorem 10, Sections 3–5. Final 2008 version not fully compared.

- **P16** [Bilyk, Lacey, Parissis and Vagharshakyan (2009), Exponential Squared Integrability for the Discrepancy Function in Two Dimensions](https://arxiv.org/pdf/0810.5544). Primary paper pp.1–2 equation (1.2) verifies Schmidt’s classical logarithmic star-discrepancy theorem.

- **P17** [Schmidt (1972), Irregularities of distribution VII](https://doi.org/10.4064/aa-21-1-45-50). Publisher record; original PDF access unsuccessful, theorem verified through P16.

- **P18** [Shukla, Kundu, Mitra and Grover (2023), On estimating parameters of a multi-component Chirp Model with equal chirp rates](https://arxiv.org/abs/2302.07098). Primary abstract; established common-chirp model, statistical rather than exact finite-field setting.

- **P19** [Yang, Ge and Wang (2025), Pursuing the Limit of Chirp Parameter Identifiability: A Computational Approach](https://arxiv.org/html/2507.01286v1). Full primary model/identifiability formulation; continuous-parameter structured-rank approach.

- **P20** [Grigoriev, Singer and Karpinski (1990), Interpolation of sparse rational functions without knowing bounds on exponents](https://archive.mpim-bonn.mpg.de/id/eprint/2068/1/preprint_1990_10.pdf). Original preprint, introduction and algebraic interpolation construction; general sparse rational interpolation is old.

- **P21** [Uteshev and Baravy (2016), Solution of Interpolation Problems via the Hankel Polynomial Construction](https://arxiv.org/html/1603.08752). Full text; Theorems 2.2 and 6.2 distinguish classical Hankel/resultant interpolation from the new adjacent multiplicative pencils.

- **P22** [Pernet, Signargout and Villard (2023), Exact computations with quasiseparable matrices](https://perso.ens-lyon.fr/gilles.villard/BIBLIOGRAPHIE/PDF/quasisep.pdf). Full primary paper; exact quasiseparable definition, representations and arithmetic costs.

- **P23** [Hwang, Lahoti, Dao and Gu (2024), Hydra: Bidirectional State Space Models Through Generalized Matrix Mixers](https://arxiv.org/abs/2407.09941). Primary paper/abstract; optional application context only, no transfer of project lower bounds to nonlinear networks.

- **P24** [Sturmfels (1994), On the Newton Polytope of the Resultant](https://www.maths.tcd.ie/EMIS/journals/JACO/Volume3_2/m4496732732u7744.fulltext.pdf). Original paper, especially Theorems 2.1 and 4.1; extreme terms and initial-form resultants compared to the explicit diagonal-pencil valuation.

- **P25** [Nart (2014), Local computation of differents and discriminants](https://arxiv.org/pdf/1205.1340). Original Section 3 and Definition 3.1; Newton-side resultant contributions and unequal slopes. Algorithm-specific finite-residue/local-field assumptions not transferred.

- **P26** [Osgood, Siripuram and Wu (2012), Discrete Sampling and Interpolation: Universal Sampling Sets for Discrete Bandlimited Spaces](https://arxiv.org/html/1204.0992). Primary text, Theorems 4 and 9; balanced residue classes, universal sampling and one-vector support uncertainty, distinguished from all-endpoint cut-rank minimax.

- **P27** [Alexeev, Cahill and Mixon, Full Spark Frames](https://arxiv.org/html/1110.3548). Primary text, Theorem 9; full-spark prime-power Fourier submatrices characterized by uniform residue distribution. Different invariant from the endpoint minimax.

- **P28** [Barnett (2022), How exponentially ill-conditioned are contiguous submatrices of the Fourier matrix?](https://arxiv.org/html/2004.09643). Primary text; contiguous Fourier-block conditioning, distinguished from exact rank under independent arbitrary permutations.

## Evidence and preservation

LOCAL_EVIDENCE_FINAL.json gives each inspected proof/review path and content hash. RANKED_EVIDENCE_FINAL.json contains the structured evidence table. The initial report and focused addendum are included under historical/ and supporting/ without alteration; their earlier provisional judgments are superseded where this final assessment says so. SEALED_MANIFEST.json covers all deliverables below it and is itself hashed in SEALED_MANIFEST.sha256. This seal records reproducibility and provenance, not independent peer review.
