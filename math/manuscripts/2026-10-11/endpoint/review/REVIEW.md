# Independent review of the Fourier endpoint manuscript

11 October 2026 UTC.

## Decision

The manuscript's two mathematical proof chains are accepted within their stated scope. No blocking proof gap was found. Acceptance is bound to the final manuscript SHA-256 in `RECEIPT.json`; this report is not approval of later unreviewed changes, a journal-acceptance decision, or a historical-priority certificate.

The accepted results are the all-size cyclic-dyadic endpoint minimax, with its separately proved half-square boundary, and the finite-abelian complex autocorrelation-deficit rank and indexed approximation-gap theorem. Neither is a new fusion in this packet. The critical noncyclic lower extension is supported; matching noncyclic endpoint orderings, exact all-size optimal cut-rank sums, finite-characteristic analytic transfers, and unrestricted FFT arithmetic conclusions remain excluded.

## Review method and dependencies

The reviewer read the entire manuscript as mathematical text and independently reconstructed every displayed proof. The five readiness-pinned sources MINIMAX_PROOF, DEFICIT_PROOF, R07, R08 and MINIMAX_PRIORITY were rehashed against the readiness manifest; every match passed. The original recurrence exposition and the final theorem source were inspected as inert text. Source-program execution and imports were not used.

The separately written `independent_checks.py` uses only Python's standard library. Its rank calculations take place exactly in cyclotomic fields represented as polynomial quotients over the rationals, with integral division-free elimination and row gcd normalization. They do not infer characteristic-zero rank from a modular sample. These finite controls support regression checking; the uniform results are accepted because of their complete proofs.

`INPUT_PINS.json` binds the accepted source inputs, including the recovered DV2008 comparison and its local final article. `EXACT_CHECKS.json` records the fresh controls. The final author packet identity, final deliverable hashes and any render-verification limitations are recorded in `RECEIPT.json`.

## The cyclic dyadic endpoint proof

### Universal lower bound

For N=4L with L at least 2, arbitrary row and column sets of sizes 2L-1 and 2L+1 give a complementary Gram contraction A with V*V=I-A. Thus the kernel of V is exactly the eigenvalue-one eigenspace of A. Its dimension is bounded by tr(A²), without a hidden full-spark or Vandermonde assumption on arbitrary selected sets.

Expanding the Gram entries by group differences gives the exact moment identity. Every nonidentity translation in a cyclic dyadic group has even order, so an odd-cardinality column set cannot be invariant under it. Therefore every nonzero-shift overlap is at most h-1. Character orthogonality gives the stated bound

B_L=L+3/4+1/(4L)+1/(16L²)<L+1.

The strict inequality uses L≥2. Integer nullity is consequently at most L, so every critical rectangle has rank at least L+1. Every independently reordered matrix has one such upper-right corner at k=2L-1. This establishes the full universal lower quantifier over independent endpoint permutations, rather than a claim only about some ordering.

### Constructive upper bound

The bit-reversal recurrence is fully justified. Below the middle cut, the selected even-frequency rows split into complete pairs and possibly one unpaired row. All odd natural columns survive. Their span has dimension ceil(k/2), because the distinct residue rows of a complete smaller Fourier table are independent.

The manuscript identifies that span as the kernel of the paired-row-sum map, with a dimension calculation. This is sufficient to justify adding its dimension to the quotient rank. The surviving even columns yield precisely the smaller Fourier suffix. In particular, at an odd cut k=2p+1 the surviving second member of the partially removed column pair supplies residue z_p. The suffix begins at p, not p+1.

Simultaneous index reversal gives invertible row and column scalings, and symmetry supplies reflection of the cut rank. The resulting recurrence

r_N(k)=ceil(k/2)+r_(N/4)(floor(k/2))

bounds even cuts by L and odd cuts by L+1. The latter is attained at k=2L-1 because the smaller nonempty one-column block has rank one. No induction hypothesis stronger than the stated rank recurrence is silently assumed.

### Small sizes and half squares

The direct minima q=0 at N=1 and q=1 at N=2,4 are correct. The recurrence at N=4 yields (1,1,1). Extending N/4+1 to N=4 would be false, and the manuscript explicitly avoids it.

The arbitrary half-square lower bound is the ordinary flat-unitary Frobenius/operator estimate. Even row and even column labels give the smaller Fourier table with each row and column repeated twice, so the exact half-square minimum is N/4 whenever N is divisible by 4. The stated dyadic special case is therefore sound. N=2 has nonzero scalar half-squares, and N=1 has no integral half-square size. The +1 lower bound is not imposed on central half-squares.

### Fields and roots

Exact Theorem 1 ranks depend only on minors over the cyclotomic subfield. Embedding that subfield into C and extending scalars preserves rank; the full ambient characteristic-zero field need not embed into C. A different primitive root corresponds to a unit residue relabeling, and the constructive recurrence works directly with that primitive root. No square root of N is needed for the unnormalized exact theorem.

The positivity proof and singular-value claims are not transferred to finite characteristic. No such transfer is used in this review's controls either.

## The finite abelian deficit proof

Rows are indexed by the full complex character group and columns by G. The positive Fourier convention gives A_xy=N⁻¹ f_I(y-x); complex conjugation in A* is properly accounted for. Orthogonality gives sum_s |f_I(s)|²=N(N-r), including the empty complementary row set when r=N.

The overlap bound produces

tr(A²)≤B_H=h(N-r)/N-d_H r(N-r)/N².

The nullity argument therefore gives rank(V)≥ceil(h-B_H), which is the displayed coefficient. All sets are fixed and arbitrary, without a hidden cyclic-group, p-group, odd-cardinality or location requirement.

For descending eigenvalues a_1,…,a_h of A, the correct index is sigma_(t+1)(V)²=1-a_(h-t). At least h-t eigenvalues are at least a_(h-t), so (h-t)a_(h-t)²≤B_H. The strict condition t<h-B_H makes the displayed radical positive, ensures a positive denominator and gives t<rank(V)≤min(r,h). The manuscript separately proves the usual rank-t approximation inequality by intersecting the kernel of W with the top right-singular subspace. No unsupported approximation theorem is needed.

The transpose is the dual-group character table under canonical biduality. It preserves rank, the nonzero singular values and operator norm. The two orientations use their own deficit, denominator and strict condition; the paper does not mix an index from one with the other orientation's hypothesis.

### Degenerate sets and normalization

The empty-restriction convention is stated outside the nonempty-set theorem. The trivial group is handled directly, without taking a maximum over an empty family. Full rows give orthonormal columns and exact gap one. Full columns give orthonormal rows; the transposed bound gives exact gap one. A singleton column has d_H=1, B_H=(N-r)²/N² and exact t=0 gap sqrt(r/N); the singleton-row case follows by transpose.

The gap is an operator-norm bound for the normalized table. Scaling to the unnormalized table multiplies it by sqrt(N), and a scalar multiplier contributes its absolute value. Failure of the strict gap condition is only failure of this sufficient estimate, not evidence that an exact rank-t representation exists.

## Existing consequences and exclusions

The stabilizer equivalence d_H>0 if and only if H has no nontrivial translation stabilizer is correct for nonempty H. Nondivisibility by p in a p-group, and more generally gcd(h,N)=1, are sufficient cardinality conditions. Neither is claimed necessary.

The N=64, side-21 calculation is 29127/4096, whose ceiling is 8; the ordinary ceiling is 7. The critical abelian-2-group rectangle bound and its sigma_(L+1) gap follow by substitution. The asymptotic delta_N~(2N)^(-1/2) is correct, so uniform-in-size conditioning is not asserted.

The odd-cut strengthening is correctly combined with the even-cut baseline. It matches double bit reversal pointwise at N=8 and N=16, giving exact upper-cut sums 14 and 48. Summing the recurrence gives the stated closed form and optimal leading N²/6 term. At N=32 the lower sum is 182 and the construction gives 192, so exact all-size sum optimality remains unsettled by these bounds. Representation cut rank is never charged as an unrestricted arithmetic complexity lower bound.

## Fresh exact controls

All controls passed:

- 26 nontrivial bit-reversal cuts at N=2,4,8,16, plus the empty N=1 profile, over exact cyclotomic fields. The maxima are 1,1,3,5 and the sums are 1,3,14,48.
- All 3,136 critical 3-by-5 blocks of F_8 have rank exactly 3.
- All 4,900 half-size 4-by-4 blocks of F_8 have rank at least 2: 20 have rank 2, 576 rank 3 and 4,304 rank 4. Explicit even-even blocks have rank N/4 at N=4,8,16.
- Every pair of nonempty row/column subsets for C_2×C_2, C_3, C_4 and C_6: respectively 225,49,225 and 3,969 rectangles, 4,468 total. Each deficit rank inequality passed; each direct complementary-Gram second moment exactly matched the overlap expansion and was at most B_H. Among these cases, the deficit ceiling strictly improves the baseline 24 times for C_4 and 1,020 times for C_6.
- Exact rational critical-bound and recurrence/sum identities for dyadic N from 8 through 4,096. The pointwise lower profiles match the construction at N=8,16 and retain the unresolved N=32 gap.

No floating-point threshold, finite-field-to-complex transfer or execution of an author/inherited verifier is used for these controls. They are finite regression evidence, not an exhaustive verification of the all-size theorems or their historical priority.

## Provenance and literature boundary

The recovered comparison report matches SHA-256 596cbc312fdb89224470905dcb8e188e86b050e7cdac6a9e84e17a3556883817. The local 19-page final journal PDF matches af33370c7d4b8f3853d36c01b512b007512886431af4963cdc6d7638af89aae4. The reviewer independently inspected Eq. (15), Lemma 7, Theorem 9 and Remark 10 in the final article; printed pp. 1598–1599 were also rendered and visually inspected. The final-paper source gap is closed. The review does not redistribute the paper or its full extracted text.

The hierarchy and N=8 lower-bound antecedents are properly credited. The final-paper comparison remains bounded to that article; the manuscript makes no claim of global novelty or logical independence from all consequences of prior work. The 2006 preprint's Lemma 8/Theorem 10 are kept separate from final Lemma 7/Theorem 9. [Final article](https://doi.org/10.1016/j.laa.2008.04.043); [TW470](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW470.pdf).

Fresh primary-source checks support the concise classical attributions. The de Wolf rank baseline is Theorem 1 on p. 4 with DFT scope on p. 2. FHX Lemma 7.1/Theorem 7.2 appear on PDF p. 11. Shkredov's maximum-overlap definition is Eq. (4) on PDF/printed p. 2; the inherited p. 1 pointer required correction. The projection/Hilbert–Schmidt antecedent is correctly identified. These checks are citation/provenance checks, not a new exhaustive priority search. [de Wolf](https://homepages.cwi.nl/~rdewolf/publ/qc/qrigid.pdf); [FHX](https://arxiv.org/pdf/1804.00367v1); [Shkredov](https://arxiv.org/pdf/2404.12469v1); [Alagic–Russell](https://arxiv.org/pdf/math/0608702v2).

## Nonblocking corrections resolved before final acceptance

1. The transpose paragraph now says “the same nonzero singular values,” consistent with the paper's h-entry zero-padded singular-value convention.
2. The half-square proof's explicit source provenance is assigned to MINIMAX_PRIORITY / DELVAUX_FINAL_COMPARISON rather than to MINIMAX_PROOF, which did not contain that proposition.
3. The Shkredov page pointer is corrected to p. 2, and the FHX location is given unambiguously as PDF p. 11.

These are precision/provenance changes, not repairs to either theorem. Final verification of their application and final hash binding is recorded in `RECEIPT.json`.

## Final rendered artifact verification

The final manuscript Markdown is SHA-256 569e8ee578e8ed43305024e3e95623e7b2d1d30bb42377cee79105798fcdfb7b. After the precision-corrected mathematical review, equation tags (8) and (22) were moved outside their aligned environments and one review-status phrase was shortened to “awaiting a separate independent manuscript review.” Exact text/hash comparisons verified that no formulas changed.

The final 12-page PDF is SHA-256 d216f5fdbdd02ebfcfa8b17614067237edf491158c31b5041c337724e91ec408. The reviewer independently rendered every page using Poppler and visually inspected all 12 pages. After the final review-status wording change, all pages were rendered again: 11 were byte-identical PNGs and changed page 10 was visually re-inspected. The statements, recurrence, ceiling/floor notation, two moment bounds, indexed gap, rank-sum formulas, source concordance and corrected citations are readable. No clipped equations, broken mathematical symbols or overlap were found. The PDF and Markdown are accepted; the earlier failed Word rendering is not an accepted deliverable.
