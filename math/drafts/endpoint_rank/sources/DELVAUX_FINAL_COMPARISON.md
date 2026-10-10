# Comparison with the final Delvaux and Van Barel paper

## Conclusion

The full final article closes the specific source-availability gap. It establishes the digit-reversal rank-one hierarchy, prime Fourier full spark, exact prime-power one-vector support extrema, their equality-set restriction, and an FFT interpretation. Those mechanisms and results must be credited as prior art.

The final article does not state the all-independent-endpoint cut-rank minimax `N/4+1`, the autocorrelation-deficit rank and singular-value estimates, or the specified Fourier–Green, fixed-Weyl-pair, and independently routed separator obstructions. The incremental statements below therefore remain distinct from the statements and proof mechanisms in this particular article. This is a bounded source comparison, not a finding of worldwide novelty or a proof that no deeper deduction from prior results is possible.

Two important qualifications sharpen the comparison:

1. For `N=8`, the critical-rectangle rank lower bound already follows from the article's Theorem 9, after transposition. The general dyadic result is not wholly disjoint from that theorem.
2. The `+1` lower bound concerns every `(N/2−1) × (N/2+1)` rectangle. Arbitrary `N/2 × N/2` Fourier blocks need only have rank `N/4`; the even-row/even-column block attains it.

No frozen matrix artifact was changed. No supplied research program was executed or imported. This comparison re-examined mathematical statements and proofs, not their full finite certificate datasets.

## Source and scope

Primary source: Steven Delvaux and Marc Van Barel, *Rank-deficient submatrices of Fourier matrices*, Linear Algebra and its Applications 429 (2008), 1587–1605. DOI: [10.1016/j.laa.2008.04.043](https://doi.org/10.1016/j.laa.2008.04.043). The uploaded file is the 19-page final journal article, including its final numbered statements, proofs, FFT section, block-diagonalization section, and references. The title page records acceptance on 17 April 2008 and online availability on 13 June 2008.

All citations below use printed journal pages. PDF page `j` corresponds to printed page `1586+j`. Theorem 9 and Remark 10 were also checked on rendered PDF pages 12–13, not only extracted text.

Compared project sources:

- `matrix/final_v1/CORE_THEOREMS_SECOND_AUDIT.md`
- `matrix/final_v1/FOURIER_DEFICIT_SEPARATOR_FUSION.md`
- `matrix/final_v1/NEW_COMPOSITE_WEYL_THEOREM.md`
- `matrix/final_v1/MULTISCALE_CHIRP_AUDIT.md`
- `matrix/final_v1/OMITTED_MATRIX_THEOREMS_AUDIT.md`
- `matrix/quadratic_supplement/QUADRATIC_CERTIFICATES_AUDIT.md`
- The complete retained C02/F018 proofs in `research_finalization_0923/matrix/FINAL_THEOREMS.md`.

The other uploaded paper, `76.pdf`, is outside this comparison. No claim here closes any separate comparison involving it.

## What every numbered result in the final article establishes

| Final article item | Printed pages | Actual content and proof | Relevance to the project |
|---|---:|---|---|
| Theorem 1 | 1588 | For a Kronecker product of normalized Fourier matrices, `H(Fv) H(v) ≥ N` for nonzero `v`. | Classical support uncertainty. The article explicitly credits Matolcsi–Szucs and earlier developments. Not a matrix-minor rank minimax. |
| Lemma 2 | 1589 | If `||Av||₂ ≥ ||v||₂` and every entry has modulus at most `M`, then `H(Av)H(v) ≥ M⁻²`. Proof: Cauchy–Schwarz on each nonzero output coordinate. | Same elementary norm/flatness background as stable-rank arguments, but not the project's fourth-moment deficit calculation. |
| Theorem 3 | 1591–1592 | Generalized Vandermonde determinant factors into a Vandermonde factor and a symmetric polynomial; its coefficient sum is `∏(m_i−m_j)/∏(i−j)`. Proof uses divided differences, complete symmetric polynomials, and evaluation at all ones. | The Vandermonde/Schur/cyclotomic primitive is prior art. It supports the final paper's full-spark and Hamming results. |
| Theorem 4 and Remark 5 | 1592–1593 | For prime `p`, every square submatrix of complex `F_p` is nonsingular. A rectangular block is full column rank whenever it has at least as many rows as columns. | Direct prior art for C04's complex prime-length, two-arbitrary-endpoint variant. This is Chebotarev's theorem, explicitly credited in the article. |
| Equation (15) and its derivation | 1593–1594 | For general `mn`, the sort-modulo permutation produces an `n × m` grid of rank-one blocks. Entries factor as a row factor times a column factor. | Direct prior art for permuted Fourier low-rank blocks, including composite lengths. |
| Definition 6 and Eq. (18) | 1594–1595 | `H_A(d)` minimizes the number of retained output coordinates supporting a nonzero `Av`, with `H(v)≤d`; equivalently the complementary submatrix has a nontrivial kernel. | Crucial quantifier: existence of one nonzero null vector. It is not a prescribed nullity or rank function. |
| Lemma 7 | 1596 | For `N=p^m`, double digit reversal simultaneously exposes a `p^(m−k) × p^k` grid of rank-one blocks for every `1≤k<m`. | The main antecedent of C02's matching upper ordering. Neither double bit reversal nor its multiscale rank-one hierarchy can be claimed new. |
| Lemma 8 | 1597–1598 | The prime-power cyclotomic polynomial is `1+x^(p^(m−1))+...+x^((p−1)p^(m−1))`. | Standard cyclotomic ingredient. Not a Fourier–Green or separator theorem. |
| Theorem 9 | 1598–1599 | If `cp^k≤d<(c+1)p^k`, `1≤c≤p−1`, then `H_(F_(p^m))(d)=(p−c+1)p^(m−k−1)`. Lower proof extracts uniformly distributed row residues to obtain a nonsingular generalized Vandermonde submatrix; upper proof uses Lemma 7's blocks. | Exact one-vector support frontier, stronger than the basic product uncertainty principle. Relevant but different from all-critical-rectangle rank lower bounds and endpoint minimax. |
| Remark 10 | 1599 | At the extremal output size from Theorem 9, the output support `I` must be a union of `p−c+1` residue classes modulo `p^(k+1)`, all within one residue class modulo `p^k`. | This is genuine equality-case information, not merely an extremal cardinality formula. It must not be omitted from a fair comparison. It still concerns existence of a null vector at the extremal support size. |
| Remark 11 | 1599 | The prime case specializes to `H_(F_p)(d)=p−d+1`. | Reconnects Theorem 9 with prime full spark. |
| Remark 12 | 1599 | Discusses the stronger divisor-polyline uncertainty bound attributed to Meshulam. | Additional prior art for support uncertainty; not the project's autocorrelation-deficit formula. |
| Remark 13 | 1599 | Refers to the authors' other paper for arbitrary `N` and another proof, while noting the equality-set information in Remark 10 was not recovered by that approach. | The 2007 Kronecker paper is a concrete remaining related source for wider priority work. |
| Section 4 and Remark 14 | 1599–1603 | Gives an elementary-unitary compression interpretation of the usual radix FFT, including `N log₂(N)/2` Givens factors for radix two and Eq. (27). | Constructive FFT prior art. It is not a lower bound for arbitrary algorithms or for the project's different Green grammars. |
| Theorem 15 | 1603–1604 | For odd `N`, pairwise Givens rotations on coordinates `k,N−k` give a unitary similarity splitting Fourier into cosine/sine-type blocks of sizes `(N+1)/2` and `(N−1)/2`. | Related negation-pair symmetry, but a different equivalence relation from endpoint permutations or diagonal scaling. It does not state the displacement minimum or the Green branch bounds. |
| Section 6 | 1604–1605 | Summarizes the support/hierarchy/FFT results and explicitly refers to the 2007 general Kronecker-product paper. | The article itself does not present an unrestricted FFT lower bound or a general-rank classification of all Fourier minors. |

The interval parametrization in Theorem 9 covers `1≤d<N`; the endpoint `d=N` has `H_F(N)=1` directly. This harmless endpoint bookkeeping should be stated when reproducing the formula rather than forcing `d=N` into nonexistent interval parameters.

## C02 and arbitrary Fourier rectangle ranks

### The exact distinct project statement

For unnormalized cyclic `F_N`, define `q(A)` as the maximum rank of either off-diagonal block across every common-coordinate cut. For `N=2^m≥8`, C02 states

`min_(independent ρ,σ) q(P_ρ F_N P_σ^T) = N/4+1`.

The lower quantifier is universal over both endpoint permutations. The upper construction is a single double-bit-reversal ordering. The minimax is over cut ranks, not arithmetic operations.

Write `N=4L`. Its lower proof establishes, for every `(2L−1)`-row set `R` and `(2L+1)`-column set `H` of a normalized character table of any finite abelian 2-group,

`rank U[R,H]≥L+1`.

The quantitative form is

`σ_(L+1)(U[R,H]) ≥ sqrt(1−sqrt(B_L/(L+1)))`,

`B_L=L+3/4+1/(4L)+1/(16L²)<L+1`.

Thus the lower statement is a universal large-nullity exclusion, and its analytic form prevents close rank-`L` approximation. The final paper's Theorem 9 measures the first occurrence of a nonzero kernel vector instead.

### Why Theorem 9 is not the same rank statement

For any `r × h` block of rank `k<h`, a dependence among at most `k+1` selected columns yields the necessary condition

`H_F(k+1)≤N−r`.

Apply the same argument to the transpose when `k<r` to get

`H_F(k+1)≤N−h`.

For the critical rectangle and the allegedly possible rank `k=L`, the final paper's dyadic formula gives `H_F(L+1)=4`. For `N≥16`, the two complements are `2L+1` and `2L−1`, both larger than 4. The scalar support constraints therefore do not exclude rank `L`. Remark 10 also does not apply at equality to these complement sizes.

This is a precise failure of the direct Hamming-number substitution, not a claim of logical independence from every possible consequence of the article.

At `N=8`, there is a real overlap: transpose a `3 × 5` block to a `5 × 3` block. Theorem 9 gives `H_(F_8)(3)=4`. If the transposed block were column-rank deficient, it would supply a nonzero vector with input support at most 3 and output support at most `8−5=3`, a contradiction. Thus the `N=8` lower bound 3 is already a corollary of the paper.

### Balanced squares have a different answer

For every `N=4L`, take the `2L` even rows and the `2L` even columns. The restricted unnormalized Fourier entries are

`ω_N^((2a)(2b))=ω_L^(ab)`, for `0≤a,b<2L`.

This is `F_L` with each residue represented twice in each axis, so its rank is exactly `L`. Conversely, the flat-unitary Frobenius/operator bound gives rank at least `(2L)²/N=L` for every half-size square. Therefore the minimum over arbitrary half-size row and column sets is exactly `N/4`.

Accordingly, never describe C02 as saying that every balanced half-size minor has rank `N/4+1`. The offset dimensions in its critical rectangle are essential. In prime dimension, Theorem 4 gives full rank for every square minor; composite dimensions require the more careful statements above.

### What the upper construction overlaps with

The final paper, Lemma 7 (p. 1596), already gives the double-digit-reversal hierarchy. The project adds explicit cut bookkeeping, expressed in the retained proof by

`r_N(k)=ceil(k/2)+r_(N/4)(floor(k/2))`, for `k≤N/2`,

together with reflection and the odd-cut surviving-residue convention. This proves the global upper bound and its attainment at `k=N/2−1`.

The defensible increment is the explicit cut-rank calculation combined with the universal matching lower bound. The ordering and rank-one hierarchy themselves are established. The upper bound is a closely derived use of that hierarchy, not a separate unexplored Fourier structure.

### Proof mechanisms and scope

The lower proof uses the complementary Gram contraction `A=U[R^c,H]^*U[R^c,H]` and a fourth-moment identity. Odd `|H|` in a 2-group prevents invariance under a nonidentity translation, lowering the nonzero-shift autocorrelations. This bounds the multiplicity of eigenvalue 1 of `A`, hence the full nullity of `U[R,H]`, and supplies a positive singular-value gap.

The final paper's proof instead chooses residue-balanced row indices, applies a generalized Vandermonde determinant, and rules out cyclotomic divisibility. No fourth-moment bound or positive singular-value constant is stated there.

The C02 exact statement is justified over characteristic-zero fields containing the relevant primitive root by extension to the complex numbers. Its complex analytic lower proof does not by itself cover finite fields. The abelian-2-group lower result does not include a matching upper minimax construction for every noncyclic group.

## The autocorrelation deficit theorem and separator fusion

For a complex normalized character table of a finite abelian group `G`, `|G|=N`, let `V=U[R,H]`, `|R|=r`, `|H|=h`, and

`d_H=h−max_(s≠0)|H∩(H−s)|`.

The project proves

`rank V ≥ ceil(rh/N+d_H r(N−r)/N²)`.

With `B_H=h(N−r)/N−d_H r(N−r)/N²`, a rank-at-most-`t` approximation has operator error at least

`sqrt(1−sqrt(B_H/(h−t)))`, whenever `t<h−B_H`.

The transpose may improve the estimate. When `p∤h` in a finite abelian `p`-group, `d_H≥1`; the same holds for `gcd(h,N)=1` in any finite abelian group. For a square block of side `s` with `p∤s`, this yields

`rank V≥ceil(s²/N+s(N−s)/N²)`.

Theorem 1/Lemma 2 and Theorem 9 of the final article are essential uncertainty antecedents but do not state these deficit-sensitive all-rectangle or quantitative approximation formulas. The project argument estimates `tr(A²)` to control an entire eigenspace, not just one nonzero vector. The group's full abelian structure is used directly, whereas the final paper's main exact Hamming theorem is cyclic prime-power.

This is not a uniform strengthening of the final paper. For prime `N=7`, its Theorem 4 gives rank 3 for every `3 × 3` block, whereas the project's cardinality-only formula with `d_H≥1` gives only 2. The results answer different questions and can be combined; neither should be presented as replacing the other's sharp regime.

For separator-selected blocks, the preserved incremental statement is the legal restriction/trim interface: previous branch rank bounds survive restriction, and trimming to an admissible cardinality allows a `p`-group deficit improvement. At `N=64`, side 21, it gives 8 instead of the ordinary stable-rank ceiling 7. The selection recurrence need not return an odd side, and trimming is not guaranteed to improve the overall cutoff. No improved universal asymptotic branch exponent is proved by this fusion.

## Independently routed Green inverse sums

The F018 model is

`T=Σ_(i=1)^b L_i Q_i⁻¹ R_i`,

with each `Q_i` invertible, each symmetric bipartite support lift admitting the specified weighted half-separators of size at most `q`, and endpoints supported on independent permutation graphs, including zero weights.

For an exact flat unitary target, the retained theorem gives

`N≤qb9^b+q(3^b−1)`.

With a free diagonal correction it gives

`N≤4qb9^b+2q(3^b−1)+2`.

Invertible matrices with at most two nonzeros per column admit `q=2` in the proof. The selection is `m_(j+1)=ceil((m_j−q)/3)` with its explicit validity condition. Its mechanism is complementary inverse-block nullity, a two-color weighted separator argument, branchwise restriction, and a flat-unitary rank bound.

The final Delvaux–Van Barel paper contains no such inverse-sum model, no support-lift separator theorem, no independent branch routing, and no `9^b` cutoff. Its Section 4 is a product factorization into elementary unitaries, a different model. The existence of that FFT does not contradict these lower bounds, and these lower bounds do not obstruct an arbitrary FFT implementation.

The specific model-level thresholds, `q=2` refinement, and stated approximation/conditioning consequences remain distinct relative to this article. Complementary inverse ranks, graph separators/treewidth, low-rank approximation, and flat-unitary stable rank remain classical mechanisms whose broader literature is not settled by this comparison. Neither the 9-base nor the thresholds are proved optimal. At fixed nonzero error tolerance, the retained fixed-branch error floors do not by themselves imply `b=Ω(log N)`.

## Remaining project families

### C04 three-stage discrepancy

The project statement bounds `2r₁+r₂+r₃` and `r₁+r₂+2r₃` below by `c log N−2` for the specified three-stage product. Its target has at least one affine endpoint ordering; in the complex prime case both endpoints can be arbitrary. Its contribution is the rank-to-cyclic-window-discrepancy argument combined with the classical planar discrepancy lower bound.

The arbitrary-minor full-rank premise in the complex prime variant is exactly classical Theorem 4, pp. 1592–1593. Affine-endpoint Vandermonde nonsingularity is also elementary prior structure. The final paper contains no three-stage discrepancy reduction or either displayed inequality. No general composite two-arbitrary-endpoint version or approximation version follows merely from the final paper.

### C01 exact additive length three

For the fixed five-coordinate block `C_q` described in CORE §4, the project asserts exact additive length three in diagonally masked Hamiltonian-cycle Green resolvents, with arbitrary complex coefficients in the lower bound and a guarded quadratic-extension upper construction. The full growing target inherits only a lower bound of three.

This target is a submatrix of `(F_N⁻¹+A_N)⁻¹`, not a Fourier submatrix. The final paper's theorems classify neither this transformed target nor secants of the Green-resolvent family. There is no direct C01 theorem overlap beyond Fourier background. The certificate dependency and unreplayed full dataset remain as stated in the original audit; obtaining the final paper does not constitute a new certificate reconstruction.

### F014 fixed-pair Weyl–Green branches

The project fixes one ordered generating Weyl pair for every branch and disallows extra branch-dependent Weyl endpoints in its composite/Hankel theorem. It proves the explicit maximum of the three gcd-dependent ranks, giving `(N+1)/2` branches at every odd prime power and `ceil(sqrt N)` at every odd length. A separate canonical-pair theorem with a different endpoint grammar must remain separate.

The final paper has no Weyl-coordinate coefficient flattening, two-resolvent branch grammar, or nonwrapping Hankel/geometric-sum argument. Its prime-power Hamming result does not establish this branch bound. The exact arithmetic combination and grammar-specific consequences remain distinct relative to it; Weyl/Gauss and Hankel/Vandermonde primitives are classical. For mixed composite lengths, the project does not prove a universal half-length bound. Branch count is not runtime.

### Displacement rank and negation

The project proves `rank(ZF−FP)=N−z(P)`, minimum `floor(N/2)`, and uniqueness of the negation permutation, with `z(P)` counting zero-sum cycles. The final article's Theorem 15, pp. 1603–1604, uses the same natural `j↔−j` pairing for a cosine/sine split.

This pairing is genuine shared structure and should be acknowledged. However, the article does not state the cycle-monodromy rank formula, optimization over every permutation, or uniqueness theorem. Conversely, its unitary similarity block diagonalization is not an endpoint-permutation cut-rank bound. Freely weighted monomial permutations are outside the stated displacement minimization.

### Fixed-layout paired Jacobi and outer stability

At the saved `N=256` affine layout, the project gives selected-block rank at most 16, a certified seventeenth singular value above `3sqrt(2)/5`, paired Frobenius/trace-norm thresholds, and conditional outer-stability estimates. The final paper's support/hierarchy statements do not give this saved layout's transition counts or moment certificate.

The applications remain distinct. The cosine–sine singular-value relation and complementary inverse nullity used in their proofs are classical and must not be relabeled as innovations because the final paper does not give the same application. Its Theorem 15 is related symmetry but is not the same arbitrary-partition cosine–sine identity or fixed-layout certificate. The affine-layout/Toffoli distinction, invertibility guards, and absence of a full four-stage infeasibility conclusion remain essential.

### Hadamard–Segre and quadratic Fourier–Green obstruction

For fixed stages `A,B,C`, invertible diagonal gauges require the Hadamard quotient `(A⁻¹diag(c)FC⁻¹)⊘B` to be rank one with the specified nonzero coordinates. The commutator gate is sufficient rejection, not a converse. The quadratic supplement instead builds the coefficient matrix `Q` of the two-square minors in degree-two monomials. Full column rank `N(N+1)/2` excludes every invertible diagonal gauge over the base field and every extension.

The final paper is about submatrices of `F` itself. It does not transform a diagonal-gauge feasibility question into a rank-one Hadamard quotient, a common-eigenvector condition, or a symmetric-square/minor lift. Its cyclotomic determinant arguments and the project's modular nonvanishing methods share classical algebra, but they are not the same statement or certificate.

The surviving exact application comprises the fixed-stage rejection theorem, the rebuilt `N=3,4` finite instances, their algebraic complex exceptional-locus realizations where one commutator is singular but `Q` is injective, and the conditional all-gauge operator gap with factor `sqrt((N+1)/(2N))`. These are not contained in this final paper. They still do not establish that Segre/symmetric-square lifting, diagonal equivalence, common eigenvectors, or Hensel lifting are new; the project's separate comparisons already identify classical and recent antecedents.

The local Hensel root is an algebraic parameter `α` reducing to 1, not asserted to equal 1 over the complex numbers. Full-rank modular evidence with unit denominators is a nonvanishing certificate, not an exhaustive complex feasibility classification. Neither the final-paper comparison nor the supplement supplies uniform-in-size conditioning or failure for all Green wirings.

### Multiscale Weyl support and dyadic chirp

The project has a literal sparse-inverse product support bound and, for `N=2^m`, the stricter pure-shift-resolvent chirp requirement `L≥m+1` with Weyl-monomial gauges. It uses an equality-case subset-sum argument and a violated chirp parallelogram identity.

The final paper's Section 4 also discusses multiple levels, but in the standard elementary-unitary FFT factorization. Its factors are not the same permitted circulant resolvents. Thus its `m` FFT layers neither prove nor contradict the project's extra-stage obstruction. The distinct increment is the equality-case exclusion within the literal grammar, not the existence of multiscale Fourier structure. Arbitrary diagonal gauges and dense basis changes are excluded; `m+1` sufficiency and unrestricted runtime lower bounds remain unproved.

## Exact status change justified by the uploaded source

The proper update is:

- Final 2008 primary source obtained and read in full: complete.
- Numbered theorem/proof comparison against the specified matrix packages: complete for this article.
- Digit reversal, the nested rank-one hierarchy, one-vector Hamming extrema, prime full spark, and standard FFT interpretation: established prior art.
- C02 at `N=8`: lower bound already follows from the paper's Theorem 9; matching ordering comes from established Fourier hierarchy.
- General dyadic endpoint minimax, abelian-2-group critical-rectangle singular gap, deficit-sensitive all-rectangle theorem, and the specified Green/separator applications: distinct statements relative to this article, with the qualifications above.
- Worldwide priority: unresolved. A missing-source argument is no longer applicable, and a source's silence is not a novelty certificate.
- Mathematical validity of the retained project proofs: not changed by this comparison; existing evidence-depth limits remain.
- Runtime/algorithmic claim: none newly established.

The frozen README and status files truthfully describe their earlier state but now contain superseded source-access blockers. Preserve their immutability and attach this dated comparison as the resolving addendum. In any current summary, remove the claim that access to the final Delvaux–Van Barel article is still blocked. Do not replace it with “novelty proved.”

## Remaining bounded literature questions

The final article itself gives a concrete next source: Delvaux–Van Barel, *Rank-deficient submatrices of Kronecker products of Fourier matrices*, LAA 426 (2007), 349–367, cited as reference [1] on p. 1605. Its arbitrary-order/general-group Hamming results must remain in the wider comparison. This report does not claim it was freshly compared in full.

Other unresolved comparisons concern generalized support weights or rank bounds for character-table restrictions; quantitative uncertainty/moment methods; cut-rank or quasiseparable minimization under independent orderings; inverse sums with independently routed low-width support; and the precise additive Green/Weyl/gauge grammars. These are distinct priority questions. Their unresolved status does not negate the mathematical proofs, and the present source comparison does not settle them.

## Evidence receipt

Date: 10 October 2026.

Primary PDF SHA-256: `af33370c7d4b8f3853d36c01b512b007512886431af4963cdc6d7638af89aae4`.

Extracted text SHA-256: `557addab85850457387bbb3d4030cda7ff0bb19b8d0a35c3842111049506449a`.

Inspection: all 19 pages through the extracted final text; direct PDF rendering and visual inspection of printed pp. 1598–1599 for Theorem 9 and Remark 10; title and journal metadata checked. All compared project mathematics was read as text. No supplied program was executed/imported, and no claim of a new certificate replay is made.
