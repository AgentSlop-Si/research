# Independent review of the fixed sparse defect rank gate

Review date: 10 October 2026.

## Verdict and scope

Accept the proposition as written, with no required mathematical correction. The accepted identity is `PROPOSITION.md`, SHA-256 `50efdeaac116385e1680598b62a96427d561b4b81431de0f963887a870b12aac`.

The three rank statements hold over every field, including small finite fields, for fixed rectangular linear factors with a common output defect map of nullity one. The common-input conclusions are genuine simultaneous-input statements. The arithmetic conclusion is accepted only under the stated additive, literal operation-charging hypothesis. It is not a lower bound for arbitrary algorithms computing the represented linear map, for the full adaptive Phase21 implementation, or for the Fourier transform generally. The rank argument is elementary; no historical novelty is certified.

The abstract dimensions are understood as integers n≥1, d≥0, p≥1, with nonnegative integer sparsity budgets k_j. Explicitly writing n≥1 and d≥0 would be a harmless editorial clarification. It is not a repair to the proof: the displayed codomain F^(n−1) already requires n≥1. This review does not alter the reviewed file.

## Independent proof verification

Let M=Σ C_j and r=rank(M). The only field assumption is that F is a field.

### The subspace weight lemma

If W⊆F^m has dimension s, select a basis of W as the columns of an m-by-s matrix B of rank s. Some s rows form an invertible matrix B_I. Therefore projection W→F^I is onto, and there exists w∈W with w_I=(1,…,1). All s of those coordinates are nonzero, so wt(w)≥s. For s=0 take the zero vector. This argument uses only the nonzero element 1 and an invertible minor. It is valid over F2 and over arbitrary finite extensions; no avoidance-of-hyperplanes or large-field assumption appears.

### Uniform sparsity and the common-map improvement

Apply the lemma to im(DC_j). A bound wt(DC_jx)≤k_j for every input gives rank(DC_j)≤k_j. The restriction of D to im(C_j) has a kernel of dimension at most one, so rank(C_j)≤rank(DC_j)+1≤k_j+1. Rank subadditivity gives r≤Σ(k_j+1).

Because the same D acts on every piece, DM=Σ DC_j. Hence

r−1≤rank(DM)≤Σ rank(DC_j)≤Σ k_j.

This proves r≤1+Σ k_j. If r=0 the first lower bound is merely −1≤rank(DM), and all stated conclusions remain valid.

### A single input for the defect count

Let A be the vertical stack of DC_1,…,DC_p. Block summation maps Ax to DMx, so rank(A)≥rank(DM)≥r−1. Since rank(A) is nonnegative, rank(A)≥max(0,r−1). The weight lemma gives some vector in im(A) of weight at least rank(A), and by the definition of image that vector equals Ax for one common input x. Its weight is precisely Σ wt(DC_jx).

This proof does not sum separately attained maxima. Individual sparsity capacities k_j need not all be attained at the same input, and the statement never requires that stronger assertion.

### Seed and defect coordinates

Choose a linear functional ℓ whose restriction to ker(D) is nonzero. Such an ℓ exists because ker(D) is one-dimensional. For E(a)=(ℓ(a),Da), if E(a)=0 then a∈ker(D) and ℓ(a)=0. A nonzero linear functional on a one-dimensional vector space is injective, so a=0. As E is an n-by-n linear map, it is invertible.

The stack B of EC_j is obtained by multiplying the stack of C_j by a block-diagonal invertible matrix. Thus rank(B)=rank(stack C_j). Block summation of the latter stack gives M, so rank(B)≥r. The subspace weight lemma supplies one input with Σ wt(EC_jx)≥r. This input need not be the same one that witnesses the previous defect-only assertion; no cost conclusion combines those two different witnesses.

### Degenerate and boundary cases

- If d=0, the input space consists of its zero vector and every factor has rank zero. Both existence statements hold with total weight zero.
- If n=1, D maps to the zero-dimensional space, every defect count is zero, and r≤1. A nonzero ℓ makes E invertible. All statements remain valid.
- Zero factors and complete cancellation M=0 are allowed. A zero factor need not consume nonzero features, while the literal fixed-overhead cost hypothesis, when invoked, still explicitly charges that piece.
- A coordinate seed is not automatically valid for a general D. For example, with D=(1,0), choosing ℓ(a)=a_0 fails. The stated nonzero-on-kernel condition is necessary and sufficient, and is correctly imposed.
- Uniform bounded weight over a finite field does not imply a fixed support. The binary two-dimensional example in the proposition correctly distinguishes those assertions.
- With different maps D_j, stack C_j has rank at least r, and applying the block-diagonal map diag(D_j) loses at most p dimensions. This gives max(0,r−p) for stacked defects. The common-D improvement cannot be retained: coordinate projections in dimension two can each land in its own D_j kernel while summing to the identity.
- For larger nullity h, the corresponding individual bound is rank(C_j)≤k_j+h, and with a common D the sum bound is r≤h+Σ k_j. Nullity one is an actual hypothesis, not a cosmetic convention.

## q defect map and source provenance

For odd n≥3 and η of exact order 2n in the actual field, the order of q=η^8 is 2n/gcd(2n,8)=n. Consequently 1−q^t is nonzero for 1≤t<n. The submatrix of D in columns 1,…,n−1 is lower triangular with those nonzero diagonal entries, proving rank(D)=n−1. The equations Da=0 recursively determine all coordinates from a_0; if a_0=0 they force a=0. Thus the particular seed ℓ(a)=a_0 is valid.

This step requires the admitted field/root hypotheses. A composite modulus that is not a field cannot substitute for F, even if an element passes a superficial root-order test. The abstract rank gate itself needs neither roots of unity nor total nonsingularity.

Fresh hashing verified the source identities recorded in the proposition's provenance:

- Schur v30 ZIP: `ce2fba707468da831596f7bd74653ac59221a43707559ccf80724d89f4bde916`.
- Schur v31 ZIP: `fdc0772ed669d6c486298bead2a80039ba85d6f96b0532af1537af687d58601f`.
- HERO17 Phase21 ZIP: `a0b6cda5ff04866afcfb050a4187c468c6c5eb1641bc7e06cf1dc6a42e6d80f7`.

Top-level ZIP CRC checks passed. The six declared hashes in the reviewed gate's manifest also passed. The actual Phase21 source member `phase21.py`, SHA-256 `635b2a72a98b9b43748a6bbd5fa8287cb2b0949ac85d5f9df74118dd9be0fc99`, was inspected as text, particularly lines 259–301. No submitted source program or predecessor control was imported or executed.

The prior accepted reviews were checked for the relevant factor-coordinate and cost boundaries. This review does not purport to re-prove every statement in those archives. Private conversation links were not fetched again; their identities remain provenance from the original record and are not reproduced in this public report. The [MIT linear-algebra background page](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/resources/lecture-10-the-four-fundamental-subspaces/) was checked as a relevant elementary reference. It is not a historical-priority source or an external proof of this particular gate.

## Exact cost audit

Under the displayed hypothesis that evaluation j on every actual input costs at least c n[1+wt(DC_jx)], with a positive c uniform in n and j, and with additive costs across pieces, the defect witness yields

cost(x)≥c n[p+max(0,r−1)]≥c n r.

The last inequality uses p≥1. This includes r=0 and r=1. Therefore rank r=Ω(n) forces Ω(n²) in this model. For a distinct size parameter N, the proposition correctly requires n=Θ(N) and r=Θ(N) before calling it quadratic in N. Otherwise the conditional result remains Ω(nr).

Static inspection independently gives the forced raw Phase21 sparse-path online ledger:

- Defect scan: 4(n−1) scalar operations.
- Each nonzero defect contributes three operations for each of 2n output positions: 6nw.
- Four Horner seeds: 8(n−1).
- Two boundary multiplications and one odd-orbit negation: 3.
- Two sets of n−2 recurrence updates, four operations each: 8(n−2).

The sum is 20n−25+6nw. For n≥3, this is at least 6n(1+w). It covers the literal schedule for an n-coefficient raw input and all 2n padded outputs. It does not claim those operations are irreducible in an optimized or shared implementation. Integer indexing, comparison, reads, writes and root setup are not silently equated with that scalar ledger.

If zero seeds or pieces are skipped, the fixed overhead contract may fail. The separate seed–defect claim still gives Ω(nr) only when every nonzero feature is charged at least c n and those charges add. The source's four Horner seed evaluations do not themselves prove that alternative per-feature charging contract; the proposition correctly keeps those models separate.

The following exclusions are essential and are correctly stated:

1. An O(n(k+1)) algorithmic upper bound cannot imply an intrinsic lower bound.
2. Separate worst-case inputs cannot be added; stacking supplies the actual common input used here.
3. Shared computation, aggregation before a common transform, cancellation shortcuts, structured solvers and shared recurrence updates are outside the cost contract.
4. Adaptive or nonlinear decompositions and finite-word lookup/tabulation algorithms are outside this fixed-linear, independently charged analysis.
5. Dense-input FFT fallback need not pay c n per defect. The source branch selecting an ordinary transform therefore prevents extending this quadratic statement to the entire adaptive implementation. Its actual radix2/3 fallback limitation remains a separate issue.
6. A support graph, interface size, or rank bound alone does not furnish the actual Fourier-compatible factors, endpoint coordinates, or their cost contracts.

The coordinate-projection example summing to the identity correctly demonstrates why independent dense piece materialization can impose avoidable quadratic work even though the represented map is computed by wires.

## Independent controls and receipt

The new standard-library verifier is `fresh_independent_controls.py`. It has no dependence on uploaded or predecessor programs. It exhaustively checked 12,177 admitted map/factor cases over F2, F3 and F4=F2[t]/(t²+t+1), totaling 42,373 common inputs. The cases include 847 rank-zero targets, 69 zero-dimensional domains, 1,694 zero-factor occurrences, and both tall and wide rectangular factors. Every claimed rank and common-input weight inequality passed.

All 662 seed-functional checks matched the exact criterion, including 403 valid and 259 invalid seeds. All 18 primitive-root q-defect maps at (n,F)=(3,F7),(5,F11),(7,F29),(9,F19) passed. The explicit binary varying-support and incompatible-maxima examples passed, as did the distinct-map negative control and 24 independently enumerated literal-ledger cases. Finite controls corroborate the proof; they do not establish a universal theorem by sampling.

The original gate control program and its saved outputs were inspected but not rerun. Its recorded 144 common-map cases, 27 distinct-map cases and two q maps are kept separate from this review's counts.

This acceptance is bound to the stated proposition hash and the reviewed source identities. It conveys no approval of a later unreviewed revision, no external publication or repository mutation, and no unrestricted Fourier lower bound. All review writes were local. See `PUBLIC_RECEIPT.json`, `REVIEWED_IDENTITIES.json`, `FRESH_RESULTS.json`, and `SHA256SUMS` for the machine-readable scope and evidence identities.
