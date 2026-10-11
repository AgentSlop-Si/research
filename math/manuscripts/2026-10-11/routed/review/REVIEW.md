# Independent review of the routed inverse sum manuscript

11 October 2026 UTC

## Decision and binding

**ACCEPT within the stated mathematical scope.** No proof gap was found in Theorem O, its spectral corollary, Theorem C, the column-two specialization, Theorem F, or the stated scaling transfer. The final author seal, all 28 sealed artifacts, and all 18 original-to-copy source bindings have been independently recomputed and verified. The accompanying RECEIPT.json binds this review to the frozen author manuscript, SHA-256 429b1c39100e280e2e9ee0d7d47ce4f2db4e5a5283e9ac12cb56028fd8d8160d.

The reviewed statements preserve independent left and right endpoint routes, zero endpoint weights, disconnected denominator support, unbounded denominator row degree, and the distinction between exact fields and complex norm comparisons. The prior-art discussion is appropriately bounded and does not certify historical novelty.

## Evidence and method

The entire working manuscript was read mathematically. The sources in the readiness manifest identified as ROUTED_PROOF, CORRECTION, CORRECTION_RECEIPT, CORRECTION_IDENTITY, R07, R08, their relevant row records, and ROUTED_PRIORITY were inspected. Additional full proof sources for the current separator result and exact-field extension were read as text. Mixed-topic reviews support only their identified routed sections; this review does not accept unrelated material contained in them.

The older ROUTED_PROOF uses a sixth-retention argument and the factor 36^r. The current Section 2A in FINAL_THEOREMS.md proves third-retention, the 9^r cutoff, and the direct q=2 pseudoforest separator. Its current SHA-256 is 6a2a6424d82e313438058a2458cdbc8f555df0fcee6c534cfd7481633d527c6b. The manuscript correctly attributes the stronger proof to that current source rather than inferring it from the older sealed file.

The reviewer newly authored and ran fresh_exact_controls.py with python -I -S. It imports only standard-library modules and does not read or execute inherited research programs. Its exact finite tests supplement the all-size proofs and are not represented as proof of their universal quantifiers. No repository, spreadsheet, or other external write was made.

## Detailed mathematical findings

### Endpoints and quantifiers

Equation (3) fixes the right endpoint convention as R_i[s_i(b),b]=rho_i,b. Thus selected output rows become lower vertices of the bipartite support lift and selected input columns become upper vertices. These are distinct vertices even when their numeric labels coincide. Partial permutation supports can be completed with zero weights, so the proof is not restricted to invertible endpoints.

The all-equal-size-pairs marked-separator assumption is an explicit sufficient formulation of the accepted marking-specific hypothesis. It resolves any choice-dependent quantifier ambiguity without expanding the theorem. The rectangle may depend on the proposed representation. Each branch has its own separator and routing, and restrictions preserve all earlier rank bounds. No common graph, ordering, separator, or preselected universal rectangle is asserted.

### Ordered common rectangles

The two failed strict half-separations give the displayed contradictory chain because each of the individual row and column orderings has a strict gap between its low and high halves. Repeated floor-halving has final size floor(N/2^h). The zero-size outcome is expressly handled. Processing once per distinct specified order pair is legitimate because all branch rank hypotheses using that pair then hold on the same restricted rectangle.

The Green inverse arc factorization divides only by 1 minus the total cycle weight. It never divides by an individual edge, so zero edges do not invalidate it. Concatenated independent cycle components have at most one block crossing any strict separating cut. The manuscript correctly preserves the previously established ordered Hamiltonian specialization and does not claim that allowing many bare cycles is itself the attached-tree extension.

### Complementary inverse ranks and spectral comparison

The kernel correspondence in Lemma N is a bijection, and its rank-nullity calculation uses the swapped complementary block A[J^c,I^c]. Applying it to two component unions plus the separator gives rank at most |X| without requiring invertibility of principal blocks. The lower-row/upper-column block of H_Q inverse is exactly Q inverse.

For a normalized flat unitary, the selected m-square rectangle has Frobenius energy m^2/N and operator norm at most one. This implies its rank lower bound and the singular-value tail estimates. For a rank-R approximant, the operator estimate uses m>R and denominator m-R. The weaker ordered estimate divides block Frobenius error by m. The manuscript explicitly excludes the invalid denominator cases, complex-to-finite-field norm transfer, and unnormalized target use without scale factors.

### Improved two-color selection

After at most q marks of either color are removed, trimming to u=m-q per color is possible. For m>=4q, each remaining component has at most m<=4u/3 marks. Greedy component grouping produces side totals in [2u/3,4u/3]. If both cross-color orientations failed, one side would have total below 2u/3 or one color's complementary counts would both be below u/3. Hence an orientation retains at least ceil(u/3) marks of each color. The rank conclusion follows from the inverse-separator argument.

The sharpness remark is confined to the available abstract component-count information. It is not used to assert optimality of 9^r or of the matrix theorem.

### Corrections, legality, and cutoff

For d=s+1+delta and p=floor(N/d), any p selected rows touch at most (d-1)p columns through E and the optional diagonal. At least p columns remain; both terms vanish on the resulting square. Column degree and coefficient size do not enter. K remains with rank at most t.

Let R=qr+t, a=3^r, c=(d-1)+dq(a-1)/2, and B=d^2Ra^2. The recurrence lower bound and floor bound give m_j >= (N-d+1)/(d3^j)-q(1-3^(-j))/2. Under N>B+2c, induction validates each input size before its separator call: the manuscript's weaker lower estimate 9q-1-q/2 is at least 4q for every integer q>=1. This is not circular use of an unverified recurrence.

The final m >= (N-c)/(da) is positive. Equality to U would imply (N-c)^2<=NB, whereas (N-c)^2-NB=N[N-(B+2c)]+c^2>0. Expanding B+2c gives exactly d^2(qr+t)9^r+dq(3^r-1)+2(d-1). The uncorrected and diagonal-only substitutions agree with the accepted formulas. The numerical example 3697 is correct.

For fixed q,r,s,t and delta, legal recurrence sizes satisfy m/N -> 1/(d3^r). The stated operator and relative Frobenius limits follow from the finite-size inequalities. For exact equality with fixed q,s,t the cutoff is bounded above by C r9^r, giving the logarithmic branch lower bound. These statements are not extended to growing structural budgets or arbitrary fixed positive error tolerance.

### Column-two support and q equals two

Column independence gives e<=v for each support component; equality of global row and column counts forces equality componentwise. A connected multigraph with e=v is unicyclic, including loops and parallel cycles. Passing to the bipartite lift subdivides two-entry edges and turns a singleton loop into a leaf, yielding a pseudoforest.

The weighted q=2 proof covers all necessary cases. If a unique heavy component is a tree, its weighted centroid works. In a unicyclic component with an attached tree heavier than half the global weight, moving all outside weight to its attachment root makes a single tree centroid valid for the original graph. Otherwise every attachment weighs at most half the total; deleting one cycle vertex and a centroid of the remaining aggregated path suffices. Detached branches and other components remain within the half-weight bound. Zero weights and disconnected supports cause no omission. A forest lift permits q=1. No claim is imported for arbitrary column degrees greater than two.

### Exact-field projective directions

Selecting k rows of Q inverse deletes k denominator constraint columns. The retained pseudoforest has exactly k tree components, by summing v-e. Local column independence gives left-nullity one for each tree and zero for each unicyclic component. Consequently the selected inverse rows form a basis of the direct sum of k one-dimensional disjoint-support nullspaces. The change-of-basis matrix is invertible, giving exactly k independent nonzero projective directions before masks.

A surviving unicyclic component need not be untouched; the manuscript correctly allows removal of an attached-tree edge. Actual support is distinguished from the older permutation superpattern. No division by an edge or gain convention excludes characteristic two.

After endpoint masks, k rank-one classes still suffice, with zeros absorbed into any class. Refinement across r branches has at most k^r cells. For k=r+1 consecutive Fourier rows, any k selected columns are Vandermonde-independent over every stipulated field. Deleting at most delta_0 k sparse-correction columns proves N<=delta_0(r+1)+r(r+1)^r. The r>=N and r=0 cases are handled separately. Arbitrary-row full spark at composite length and an uncharged low-rank correction are expressly absent.

### Scaling and additive grammar

For invertible diagonal target scales D_L and D_R, normalization preserves branch support, row degree, diagonality, and correction rank. Exact bounds therefore transfer. Both norm inequalities acquire the product of minimum diagonal magnitudes; relative operator bounds can lose the product of diagonal condition numbers. Singular scales and arbitrary dense preconditioners are excluded. Products, interleaving, general mixing, and lower bounds on arbitrary shared evaluators remain outside every accepted theorem.

## Prior-art and provenance findings

The reviewer reopened the six primary references cited by the manuscript, and inspected the relevant extracted passages. This was a bounded citation-concordance check, not a new exhaustive priority search or a full proof audit of those papers.

- Vandebril and Van Barel, Section 3, Corollary 1, prints the swapped-complement identity and credits the older literature. The manuscript appropriately treats the identity as classical. [Institutional text](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf)
- GIRS Definition 1 uses border-edge counts; Propositions 2.1--2.3 provide inversion and common-graph algebra. The manuscript does not confuse an edge boundary with a vertex separator or claim a general non-implication. [Primary preprint](https://arxiv.org/pdf/1911.05858v3)
- TQS Section 4.1 explicitly uses separate left and right block-permutation matrices. Theorem 4.4 and Propositions 4.6--4.8 concern the specified graph partition and compatible same-tree algebra. The manuscript does not caricature this as one simultaneous permutation. [Final institutional copy](https://repository.tudelft.nl/file/File_6b7549c8-222e-4316-8ac4-a113d7d4da1e)
- Bodlaender et al. Section 2.1 states the weighted half-component separator and groups components into balanced sides. The manuscript credits these standard ingredients. [Author text](https://sites.cs.ucsb.edu/~daniello/papers/treewidthApproxJ.pdf)
- Zaslavsky's map immediately before Theorem 2.1 sends coordinate vectors to component directions or zero. This is an appropriate structural antecedent, without attributing the exact Fourier count to that paper. [Author text](https://people.math.binghamton.edu/zaslav/Tpapers/bg4.pdf)
- Nelson and van Zwam Section 2 supplies the frame-matrix context and the binary singleton caveat. The manuscript's direct proof correctly avoids making its field scope depend on an inapplicable graph-gain convention. [Author text](https://www.math.uwaterloo.ca/~apnelson/asympgood.pdf)

The correction theorem body has canonical matching bytes, SHA-256 79a5f64c11c47e39eb1fe90f7f6d51743dc9e4f1a9d89a5c505ce17835a86c0f. Its original-body absence is no longer current. The receipt supplied in the recovered archive is the declared attribution-normalized export ac60fadc696be34bdea08f521b59714b2137d1a4e3874fe763578cfa062d0dfd. The recorded canonical receipt identity eba23a76dd87fef48f9c5006bb416ee1756745874de212d83099ab1bc6af2b74 remains distinct; this review neither recovers nor reconstructs those missing original receipt bytes. The manuscript preserves this distinction.

## Fresh exact controls

All controls passed:

- 16,124 column-two matrices over GF(2), orders 1--4, and GF(3), orders 1--3
- 6,417 invertible instances and 68,685 nonempty inverse-row restrictions
- 2,418 invertible instances genuinely exceeding row degree two
- 876 swapped-complement nullity identities including empty and full subsets
- 192,524 valid balanced red/blue count pairs for totals up to 100 per color
- 5,400 strict cutoff tests, checking every legal recurrence input and final strict rank contradiction
- 2,052 consecutive-row Vandermonde minors, including composite orders and cyclic wrapping
- A negative control at N=4 over GF(5), where rows and columns {0,2} form a singular Fourier minor

No finite count above is evidence of all-size validity by itself. The detailed proofs and their exact model assumptions provide that validity.

## Review boundary

This review accepts the final hash-bound mathematical consolidation. All 15 available rendered PDF pages were visually inspected, and the PDF text was checked against the theorem-bearing manuscript; equations, tables, and source-identity prose are readable without clipping or overlap. The author packet retains its historical pending-independent-review wording; this separately dated receipt supplies the completed review rather than mutating those sealed bytes. Historical novelty, publication suitability, optimality, broader grammars, and all excluded algorithmic claims remain unestablished. No new fusion, discovery identity, or external publication is created by this review.
