# Independent review: current research finalization

16 October 2026 UTC. Baseline repository commit: `2e57c6f739cb676b81a698736b1dc4baa00865ae`.

## Verdict

**ACCEPT the five bounded mathematical refinements and the single activity-only archival disposition described below.** No full Fourier algorithm, unrestricted lower bound, production qualification, or historical novelty conclusion is accepted. ALG-040, ALG-043, ALG-044, ALG-049 and all four N13 parent views remain open at their existing priorities. M-CRT-TRANSFER may become CLOSED only as an exhausted current activity, retaining its unresolved broader questions and historical evidence. The resulting record census is 88 CLOSED, 239 TO RESEARCH, 327 existing views.

This report accepts the mathematical content and the precisely scoped proposed update. It does not certify a future external write. Exact prewrite guards and terminal remote/native readback remain mandatory.

## 1. Independently checked source identities

The marker, chirp, routed-packet and ALG049 predecessor bodies were independently fetched from the pinned repository commit and read as text. The pinned N13 descent and covariance reviews were separately fetched from their immutable accepted commit. `INDEPENDENT_SOURCE_PINS.json` records exact URLs, Git blob identities, byte counts and current SHA256 values.

The historical archive-name hashes for ALG040 and ALG043 are not their present published byte hashes. Their verified current SHA256 values are respectively `6d9c0057e386f133fd97538ddce9327977e264079f3917a5c9177366258c4ff9` and `0dde3943e7c5bd0ac34a8132690e568ffa2487e24f044f43cca13debbb66c210`. The immutable source URLs and fetched Git blob identities remain unambiguous. No archive basename is substituted for a current byte-integrity assertion.

No historical scientific program or author checker was executed, imported, compiled or evaluated by this reviewer. The independent controls below are newly authored standard-library Python. Author result logs are retained as author evidence only.

## 2. ALG040: parameter optimum and complete-schedule ledger

The inherited exact layer sizes imply `m+sum e_h=N`. Thus `m(n+1)+sum h e_h+sum(n-h+1)e_h=N(n+1)` is an exact structural ledger identity for every legal cut. It is not an exact instruction count and not a lower bound for a changed shared circuit.

For `2^b` within a factor two of `sqrt(n)`, the accepted moment bound is `O(N sqrt(n))`; retained initialization has the matching lower bound, and avoiding-word tails are exponentially small in `sqrt(n)`. The source schedule and its dense retained storage therefore have the claimed Theta bound. This is a time-space tradeoff against the older low-space choice.

The schedule-specific lower bound over every legal b is sound. If `2^b<=sqrt(n)`, retained storage suffices. If `2^b>=2n`, the avoiding-word union bound gives at least N/2 retained avoiding words. In the middle regime, ages through `H=min(2^(b-1),n-b)>=2^b/4` have `e_h>=N/(4*2^b)`, so their moment is at least `N*2^b/128`. Together these prove optimality only within the displayed source ledger. Causal batching, integration and full recovery remain separate open obligations; the complex bounded-coefficient limitation does not transfer to arbitrary finite fields.

## 3. ALG043: exact flat spectrum and approximate width

The exterior chirp diagonals have unit modulus. The central M-by-D character matrix has orthogonal columns of squared norm M when D<=M. When D>=M, dyadic divisibility gives repeated complete periods and orthogonal rows of squared norm D. Hence every nonzero singular value is exactly `sqrt(max(M,D))`.

Projection onto a rank-w column space captures at most w of the equal singular energies, establishing the exact best relative Frobenius error `sqrt(max(0,1-w/min(M,D)))`. A kernel vector in the nonzero right singular subspace establishes relative operator error at least one whenever w is too small. Reshaping the same one-sided kernel vector preserves Euclidean norm, so the ordinary-order linear-state width consequence is valid. The statement does not equate kernel-vector error with a selected-convolution operator guarantee and does not cover arbitrary digit reorderings or alternative algorithms.

## 4. ALG044: robust sparse-plus-low-rank operator obstruction

For `T=A Q^-1+E`, choose a nonzero vector v in the kernel of any k+1 selected columns of EQ. The order EQ is essential. Invertibility of Q gives nonzero z=Qv, with support at most s(k+1), while Tz=Av has support at most t(k+1). Flatness bounds the unitary output energy inside that latter support by `st(k+1)^2/N` times the input energy. The complementary output proves the stated operator-norm bound.

No conditioning hypothesis is hidden. This is an operator bound and does not remove the gain-dependent factor from the predecessor's separate normalized-Frobenius result. The routed-packet substitution s=2, t=r^2 and actual correction rank bounded by K is correct. Large support or rank is not claimed to imply large unrestricted arithmetic complexity.

## 5. ALG049: nonuniform-cycle deficient-difference-support exclusion

The reviewer reconstructed both accepted cycles directly from their column-edge definitions. Instead of the author's direct inversion route, the fresh program uses the accepted polynomial identities `K=(3I+M+...+M^7)/2` and `K^-1=(129I-64M-...-M^7)/257`. It verifies the inverse identities, all four prefix products, both correct Gram orientations, and every one of the 56 supplied Laurent entries and positive bounds.

Fifty-five bounds follow by coefficient dominance. The remaining `(-,+)` entry is `(-27z+55+28/z)/514`; its real part is at least 27/257 on the entire unit circle. No finite phase sampling is used to establish these continuum bounds.

For a cycle-supported Q, h(Q) has only cyclic offsets in E; both Gram orientations have support within E-E. This support statement remains true with zero weights, since they only remove entries. A proper difference set leaves an off-diagonal zero in every row. Invertible monomial congruences preserve this property, even with nonunitary amplitudes. For B=TSC the correct equalities are `L=c S^-* C^-* C^-1 S^-1` and `L^-1=c^-1 S C C* S*`. Each contradicts its independently certified dense row in the relevant branch.

The quantitative inverse-polynomial inequality has the correct squared denominator `||C^-1 S^-1||^2`; the Frobenius extraction uses the conjugate pair and gains sqrt(2). It is not uniform under scaling or ill conditioning. No extension to arbitrary nonuniform rational factors, full-difference support, general separators, changed first boundaries or dimensions other than the fixed N=8 prefix is accepted.

## 6. N13: independent reconstruction and all-extension scope

The separate independent packet in `n13_independent_review/` is accepted and incorporated by reference. It reconstructs the actual G factors using a Weyl recurrence, rather than the author's Gaussian product, and reconstructs the seven determinant polynomials using scalar Gaussian elimination and justified interpolation of degree below 53, rather than polynomial permutation expansion. It independently verifies all formal coefficient identities, four corruption controls, and a byte-identical fresh replay.

The Bezout identity for D0 and D6 proves rank six over every characteristic-53 extension, not merely the 53 base-field points. The two complete prime-degree irreducibility tests establish that D6 is 48 times an irreducible degree-37 polynomial. The h6=lambda chart is therefore valid everywhere in F_(53^d) exactly when 37 does not divide d. Singular chart nodes in the other extensions do not cause rank failure. The nonvanishing polynomial kernel and polynomial particular vector provide the claimed global affine family.

The original-bank forced-window source was checked against the pinned accepted descent/covariance scope. Arbitrary legal beta and independently free nonzero cross nodes remain; no normalization to y=z=1 is assumed. Support splitting, distinct nonzero roots, both sides and all original sectors remain necessary unresolved conditions. No sixteen-bank existence or exclusion, minimum extension degree, unrestricted allocation or FFT speedup is accepted.

## 7. M-CRT-TRANSFER: activity archival, with no new proof credit

The original exact N16 report and independent review/verdict were read in full. Their current hashes agree with the supplied source register. They establish the earlier finite result over Q(zeta16), fixed ascending monomial quotient bases, and all 12,800 eligible subsets: minimum combined support 112, 64 minimizers, one odd-affine/complement orbit. Those earlier exhaustive executions are attributed evidence, not newly replayed checks.

Fresh native reads confirm the specific current owner action says the accepted N16 fixed-basis task is exhausted and requires selection of a genuinely new size, basis or application. The older generic attribution-leading wording in F77 is explicitly reconciled, not ignored: historical priority remains unestablished and deferred; no specific new primary-source comparison is selected. The existing activity can therefore be archived under the current scope-finalization instruction without claiming to settle a broader theory.

F015 and the four CHIRP aliases are correctly retained: their accepted comparison/preparation subcomponents do not discharge the concrete sharpened-solver or caller/root-order/shared-budget obligations. No changes to those records are proposed. A new named contradictory same-scope fact or selected genuinely new scope would justify reopening M-CRT; a blanket promise of worldwide priority does not become a theorem by archival.

## 8. Fresh controls and preservation requirements

`check_independent.py` and its deterministic replay pass 8,128 marker cardinality/moment/complete-ledger cases, 54 exact dyadic chirp Gram cases comprising 1,470 entries, 676 exact rational flat-unitary energy controls, two sparse-proof guard negatives, all 56 ALG049 Laurent certificates, and 912 exhaustive deficient-support row checks. Finite controls corroborate the displayed algebra; the general proofs supply their universal claims.

The prepared native plan must bind full current preimages, stable IDs and exact source/target rows. New findings are prepended with the entire old text intact, shifting existing rich/chip offsets by the exact UTF-16 prefix length. All other metadata, formulas and cells are preserved. Only E77 changes status to CLOSED and receives the existing CLOSED red background; H77 changes to the explicit archival lane. Dashboard current census text is updated while dated historical narratives are retained. All numerical priorities and proof/novelty classifications remain unchanged.

Publication may include only the explicitly staged safe research reports, controls, formal certificates and seals. Raw native reads, complete private cell plans and unrelated material are excluded. Before mutation the publisher must reread the full guard and require an exact match; after mutation it must verify the expected entire guard, 327 unique IDs, unchanged priorities/classifications, exactly one status change, census 88/239 and all retained histories/links. Remote commit/file bytes and terminal native readback are separate completion conditions.
