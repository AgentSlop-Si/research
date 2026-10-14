# Shared-cut rational QTGF: independent review and antecedent reconciliation

Review date: 2026-10-13 UTC. Candidate ZIP SHA-256: `d4904e5d02f44d8665789248f28d74b72282d0b70c90ad39eb8b5dc4ade4d3af`.

## Verdict

**ACCEPT the restricted theorem, with a minor correction to Countercontrol A. MERGE the result into the rational-QTGF architecture record and CLOSE the aligned constant-depth search.** The theorem does not close independently routed rational QTGF, shared alternative evaluators, or general Fourier algorithms. It is a useful model-specific application of established common-cut algebra and low-rank approximation, not a new matrix principle. The named Phase26/53 theorem-body comparison is now completed.

Required correction: Countercontrol A must choose **beta != 0 and beta^m != 1**. Its stated condition alone allows beta=0, for which the claimed full-rank cut is zero. Taking beta=2 over C repairs the example uniformly. This correction does not affect the main theorem or the existence of the routing counterexample.

For cost language, retain the explicit full-stage contract in every conclusion. Replace an unqualified “closes the aligned family as a route to sub-N log N” with “excludes constant-depth aligned representation and sub-N log N execution by the stated separately paid full-stage evaluator.” The representation theorem alone does not lower-bound a reorganized/shared algorithm.

## Correct theorem and independent proof

Let U be an N-by-N complex unitary with every entry of modulus 1/sqrt(N). Let V_1,...,V_k partition the coordinate labels. Let each Q_t be invertible, S_t=a_t I+b_t Q_t^{-1}, and

    W = D_d S_d D_(d-1) ... S_1 D_0,    T = L W R,

where all D_t are diagonal and each endpoint L,R is supported on a permutation matrix, allowing arbitrary coefficients and zeros. Write

    K_j = sum_t rank Q_t[V_j,V_j^c].

Then both ||U-T||_F^2/N and ||U-T||_2^2 are at least

    [1 - sum_j |V_j|^2/N^2 - sum_j K_j/N]_+.

The proof is valid without nonsingular principal blocks, coefficient bounds, conditioning, or nonsingular intermediate/end masks:

1. On a complementary cut V,V^c, the invertible map Q sends the kernel of Q[V,V^c] bijectively onto the kernel of Q^{-1}[V,V^c], viewed in the coordinate subspace on V^c. Hence their ranks agree. This argument does not invoke a possibly singular Schur complement pivot.
2. Block multiplication gives rank(AB)[V,V^c] <= rank A[V,V^c]+rank B[V,V^c]. Diagonal factors and identity summands have zero off-cut rank. Thus the actual product has cut rank at most K_j, regardless of cancellation.
3. Complete the endpoint supports to permutations. They relocate each rectangle to independent output row/column sets and scale its entries. Even zero scalings only reduce its rank. The k relocated rectangles have disjoint row sets, so their squared errors can be summed without double counting.
4. For one target rectangle B, ||B||_F^2=area/N and ||B||_2<=1. If A has rank at most K, project onto its column space P: ||B-A||_F^2 >= ||(I-P)B||_F^2 >= area/N-K. Summing and using ||E||_F^2<=N||E||_2^2 proves the statement. This direct projection proof covers the full complex quantifiers independently of finite-field experiments.

A harmless stronger version sums the individually clipped rectangle contributions rather than clipping only at the end. The candidate does not need that sharpening.

For m=2^r>=2, N=m^2, and the directed QTGF denominator

    (Q_t y)[a,c] = y[a,c] - alpha_t[a]y[a-1,c] - beta_t q^a y[a,c-1],

choose k|m, k>=2 equal consecutive a-slabs. Only the predecessor-a shift crosses each slab boundary, giving at most m nonzero cut rows. The c-shift stays inside the slab. Grid translations, axis reversals, coordinate swap and diagonal conjugation preserve this support argument. Consequently, whenever the **effective conjugated denominators** all satisfy this same-cut property,

    ||U-T||_F^2/N >= [1-1/k-kd/m]_+,
    ||U-T||_2^2   >= [1-1/k-kd/m]_+.

An internal permutation must be pushed through the word and the transported denominator tested; checking each untransported stage separately is insufficient. Independent external permutations are allowed by the theorem and do not require a shared ordering with U.

For exact equality, k=2 forces d>=ceil(m/4). For positive d=o(m), a dyadic k within a factor two of sqrt(m/d) gives a lower bound at least [1-3sqrt(d/m)]_+; the d=0 case follows separately using k=m. Therefore the best achievable relative-Frobenius and spectral errors tend to one when zero masks are allowed. With invertible endpoints the same statement holds for the infimum by scalar shrinkage. For any fixed eta<1, a fixed dyadic k with 1/k<1-eta^2 gives d=Omega_eta(m). None of these claims asserts finite-size sharpness.

## Countercontrols

**Arbitrary routing:** With alpha=0, beta=2 and even m, group coordinates by parity of c using the candidate's permutation. Every predecessor-c edge crosses the half-cut. The cut matrix has exactly one nonzero in each of its N/2 rows and columns, hence rank N/2. Since beta^m!=1, Q is invertible; inverse cut-rank invariance and the nonzero scalar 2 give the same rank for 2Q^{-1}-I. For m>2 this exceeds m. It defeats the claimed cut certificate at that partition, not every conceivable common partition and not Fourier compatibility.

**Failure of constant-separator product closure:** For open-grid shifts H,V, Q_h=I+H and Q_v=I+V are invertible and their bipartite lifts are unions of paths. Each has an all-nonnegative-weight half-component separator of size at most one. The unique bare denominator of T=Q_h^{-1}Q_v^{-1} is Q_v Q_h=I+H+V+VH. Deleting s lift vertices damages at most s grid coordinates. Entirely undamaged rows and columns form a connected union of at least m^2-s^2 coordinates, lifting to at least 2(m^2-s^2) vertices. For s<m/sqrt(2), that component exceeds half the original 2m^2 vertices. Thus the separator budget is at least ceil(m/sqrt(2)). This only refutes the asserted bare-inverse closure premise; it is not a lower bound for every representation of the product.

## Exact local antecedent comparison

The two Phase26 projects must not be conflated. The separate Green Phase26 simultaneous-character-cut audit is relevant background, but it is **not** the HERO0 shared-order theorem requested here.

### HERO0 Phase26: exact original recovered

Archive `fft_hero0_phase26_permutation_bridge_2026-10-11.zip`, Library ID `libfile_b49f6a4d940c81919ede76bfcfa8e8b8`, SHA-256 `c790508658a55ca935f694451f7927a5da7d8acdefcb6371100569f49e54ebee`. All 13 manifest entries verified; no archive program executed. Its full `THEOREMS.md` is preserved in evidence.

Theorem 26.6 explicitly uses one globally shared order or its reverse, constructs all oriented sibling rectangles of a binary tree, and sums their error energies with no double counting. Under sublinear horizontal Green term count, its relative-Frobenius and normalized-spectral lower bounds approach one. This is a positive local antecedent for shared-partition, disjoint-energy and near-unit-error reasoning.

Its model is exactly two mixed-axis rook stages `(Y_H+Y_V)(X_H+X_V)`, with arbitrary vertical rook matrices and one-dimensional horizontally fibered Green sums. The fusion candidate instead permits an arbitrary-depth product of genuinely two-dimensional rational-QTGF resolvents and has a direct m-rank budget on equal slabs. Neither theorem statement directly contains the other architecture. In particular, the candidate's d>=ceil(m/4) statement does not appear in Theorem26.6. The later common-bipartition floor tending to 1/sqrt(2), recorded in the current row, is a distinct result and must not replace the original limit-one theorem in this comparison.

### Green Phase53: exact original recovered

Archive `Phase53_Green_FFT_Research.zip`, Library ID `libfile_452252b4619881918ced10963dea5500`, SHA-256 `b7734dd2637f6bd96152cc8448ae9bbd489316121de8dcf2b84da5aee5396f6f`. Its 8 listed manifest entries verify. `Phase53_Lightweight_Fresh.zip` contains the identical theorem body. No archive program executed.

Section53.4 already proves additive cut-rank accumulation for products of sums, arbitrary diagonal interstages, affine routing transported to the exterior, and independent relocation of outer row/column sets. Section53.5 supplies a one-rectangle spectral approximation floor, approaching 1/sqrt(2) for fixed term count. Section53.8 explicitly gives non-affine routing failures. Its work statement already qualifies the separately paid Green evaluator and excludes a general circuit lower bound.

Phase53 concerns weighted one-dimensional translation Hamiltonian cycles at prime length, a simultaneous Dirichlet cut, and total term/step budgets. It does not state the square-dyadic two-dimensional rational-QTGF slab bound. The new result is therefore a **scoped specialization/application**, with antecedents for every main proof mechanism and caveat. Global priority remains unestablished; this bounded comparison is not a literature-clearance claim.

## External primary-source check

Freshly inspected [GIRS, Proposition2.1 and Proposition2.3](https://arxiv.org/pdf/1911.05858v3) explicitly supply inverse cut-rank invariance and product/addition rank budgets on a common graph. [Tree Quasi-Separable Matrices, Proposition4.7](https://arxiv.org/pdf/2402.13381v2) gives compatible-tree product rank-profile addition. [Li and Strang, Theorem1](https://cklixx.people.wm.edu/uinorm-note.pdf) states the classical best low-rank approximation result. These positive matches independently rule out portraying the common-cut algebra as a newly discovered principle.

## Paid-cost classification

The inspected QTGF exact-search `RESULT.txt` records 14N+3m operations per literal primitive and a prepared-word upper ledger (15d+1)N+3dm. This review did not execute or independently recount that historical primitive. Conditional on the stated fixed-count full-stage execution contract, d>=ceil(m/4) implies at least ceil(m/4)(14N+3m) primitive-call work, hence Omega(N^(3/2)). Preparation, routing/root validation and other costs remain additional. Substitution into an arbitrary upper bound would not prove this lower bound; the paid-stage contract is essential.

## Fresh checks and disposition

The newly authored standard-library checker passes:

- 96 inverse cut-rank checks on all invertible 2-by-2 matrices over GF(3), including singular principal blocks.
- 198 actual-q-torus cut checks at m=2,4,8 and depths1–3, with nonzero beta, variable alpha, grid symmetries and possibly singular diagonal interleavings.
- 198 independently routed endpoint checks, including zero endpoint coefficients.
- Routing ranks 2,8,32 for the nonzero-beta parity examples, and rank0 in each beta=0 negative control.
- 21,586 exhaustive lift-deletion checks below the proved separator threshold at m=2,3,4,5.

Finite fields check algebraic ranks and supports only. The independent complex proof, not those tests, establishes the norm theorem. Candidate and historical scientific programs were never imported or executed. No external write occurred.

**Keep / merge / close:** Keep the accepted proposition and corrected countercontrols. Merge them into the existing QTGF/shared-cut obstruction exposition rather than creating a new independent discovery entry. Close further constant-depth aligned parameter grids. Arbitrary internal routing is outside the closed scope; it requires a new actual common-cut certificate or a genuinely different invariant before invoking this theorem.

**Comparable work priority:** 15/100 for this now-completed mathematical-audit/antecedent-comparison scope, using the current table's 1–15 completed/inactive band. The previous44 was a next-audit score, not an enduring result score. If editorial integration or a shared-cut prefilter is retained as a separate optional implementation task, recommend28/100 (low-leverage optional follow-up, source-ready and bounded). Neither score measures correctness, novelty, publication worth or success probability. No broad parent-row priority change follows automatically.

**Publication:** suitable as a proposition/counterexample section within a rational-QTGF or restricted-architecture report. The evidence does not support a standalone new-principle paper. Stopping condition is met: independent theorem verdict and the named Phase26/53 comparisons are sealed; no further parameter search or global priority claim is warranted by this task.
