# Fourier research checkpoint 18: constructive routes and exact rejection gates

10 October 2026 UTC, continuing the 9 October research session. This is a bounded, independently reviewed continuation. No general fresh-input sub-N log N FFT, stable numerical speedup, or historical novelty claim is established by this project checkpoint.

## What genuinely moved forward

### 1. A route family escapes one previously blocking cut budget

Eight explicitly generated Hamiltonian orders, obtained from classical Margulis–Gabber–Galil covers, have enough incoming edges across every balanced common subset that a three-layer edge-count budget exceeds N/2 for every dyadic N at least 2^17. The construction and enumeration cost O(N) word operations and O(N) words. The spectral expansion theorem is credited to prior work; the derived splice and layout certificates are recorded with their independent proofs.

This removes a necessary common-cut obstruction. It does not prove that any endpoint coefficients achieve Fourier, that actual ranks saturate the budget, or that every stage-varying separator is large. Twenty-four Green terms occur across three layers; that count is explicit.

A hierarchical splice variant preserves exact four-fiber route quotients and the same large-size capacity guarantee. Its base lengths are 2^17 and 2^18. It does not lift the separate N16 coefficient experiment. Proper active Fourier banks still have a nontrivial folding discrepancy.

### 2. Feedback has real low-degree controls, with Fourier synthesis still missing

A common weighted cycle with parity reversal admits an exactly quadratic feedback loop and an O(N) dense transfer evaluator. Its Fourier compatibility is excluded in the stated larger-size ranges by a sparse-annihilator/uncertainty argument. Cheap noncommuting conjugation also gives quadratic closure, but its supplied B is a longer composition, with no proof of a sum-of-two-Green realization. A scoped contiguous-cut theorem rejects that explicit construction from even N12 onward.

These controls establish that low loop degree alone is attainable. They do not establish simultaneous cheap factors, exact Fourier phases, legal architecture and cheap preparation.

### 3. An explicit odd-length chirp satisfies the missing spectral shape

For every odd N≥3, the positive Fourier matrix F and a uniformly generated diagonal quadratic phase A obey (FA)^3=NG·I, where G is the quadratic Gauss sum. A and G are generated in O(N) field operations. For N≥5 the degree is exactly three; N3 is an exception. The associated feedback loop has an explicit cubic annihilator whose value at one is nonzero.

This is a positive Fourier-compatible spectral specification, grounded in classical chirp/Gauss-sum identities. Its uniquely forced B=(F^-1+A)^-1 is still not cheaply constructed: the available formula contains Fourier actions. The small difference B−A^-1 is full rank and cannot simply be dropped, since doing so makes the feedback singular. Complex, finite-field and normalized-transform resonance conditions remain separate. Independent checks cover prime and composite odd lengths through63.

### 4. Phase20 makes a conditional structured-input advance, with a reproducible bug correction

Eight Fourier probes, bounded-degree Hankel elimination and a full time-domain certificate recover certain unknown shifted two-defect models in O(N) exact field work. The resultant degree is at most 45. Nonzero resultant, linear specialized gcd and the complete defect scan are essential; arbitrary dense inputs are not covered by the promise.

The source's noncoprime resonance test rejects too much. Actual resonance is alpha^(N/gcd(N,delta))=1, not merely alpha^N=1. An exact N8 example over GF97 satisfies the stated algebraic nondegeneracy conditions and has no poles, yet the source rejects it. The independent corrected gate accepts it and reproduces every Fourier output. Across 8,352 parameter triples, the corrected predicate matches actual pole counts; the old predicate falsely rejects 702 nonresonant triples. These are predicate counts, not a claim that every triple yields a nondegenerate fast-path input.

Accepted-output soundness survives the guard bug because of full certification and fallback within the implementation's domain. The shared-probe hybrid separately needs an N≥8 guard, and its arithmetic proxy omits root-table rebuilding and other operations. The uploaded source remains unchanged; the proposed fix and independent controls are included.

### 5. The fixed bank exterior is equivalent to the missing Fourier batch

For the fixed Cooley–Tukey interface, Weyl transport determines the exterior P up to one calibrated scalar. A full active bank makes P one-call equivalent to an unrestricted batch of shorter Fourier transforms. For an active interval of j out of q bank blocks, ceil(q/j) forward P calls recover the entire batch using masks, shifts and phases, without inverse transforms. At square splits, one additional P call yields the full transform; the independently checked fixed-radix extension here is m=rq. This is a conditional reduction and does not construct cheap P. The original odd-k orientation m<q needs its own explicit routing reduction before that scope is claimed.

### 6. Phase33 and v19: useful certificates plus a closed shortcut

Phase33 supplies exact two-Green instance exclusions and valid q²-dimensional nonsingular interpolation charts. Its local Jacobian failure is not a global nonlinear exclusion; matching five full columns and part of a sixth is not a full transform.

The v19 same-order roots-of-unity packet fusion identity is correct. General packet weights leave a numerator whose Fourier preparation and application must still be paid. Its separator lemma strengthens to an inverse cross-rank bound without principal-block invertibility or diagonal dominance.

However, a sparse denominator whose inverse is monomially Fourier is already impossible: the denominator must be dense. A denominator I−sum of g scaled permutations requires g≥N−1 in this direct-inverse model. High treewidth alone cannot rescue its constant-degree version. Products, auxiliary-variable Schur complements and different input/output maps are separate models.

### 7. A precise obstruction survives every scalar normalization

For the specific square/near-square two-dimensional four-fiber fold Q, compatible Fourier roots and any scalar γ, the matrix QF_(4N)−γF_NQ has full row rank N. An explicit choice of N columns reduces the determinant to det(F_N)(−γ)^N for nonzero γ: after Fourier conjugation, the remaining matrix strictly lowers the within-block binary valuation and is nilpotent. The zero-scalar case follows separately from invertibility.

Consequently scalar-only copying of layer coefficients cannot produce Fourier identities at both sizes through the specified proper active bank, even with normalized Fourier targets. A genuine lift needs aggregate layer-descent defect rank at least N minus the active-bank size. This is useful guidance for construction, not a work lower bound: one nonconstant fiber-character mask already supplies full defect rank in O(N) work. Actual Fourier-compatible four-channel coefficient laws remain open.

The accompanying hierarchical route refinement proves exact fourfold edit growth, preserving positive capacity margins at every later level.

## Other accepted results and corrections

- Repeated bit-reversal quasiseparable stages: an exact central partition gives total order Ω(sqrt(N)); four order-one stages fail at all dyadic N≥128. This is a restricted stage-order result, distinct from the earlier paired-Green layer bound. It is not an unrestricted operation lower bound.
- Any fixed finite bank of GF(2)-affine cycle orders has a parity-cut obstruction when the active-bank block partition is preserved. Its bound counts total Green occurrences, not only distinct orders.
- Character-profile middle-path compression has exact linear-time coefficient recurrences and diagonal/paired-block plus bounded-rank closure. The zero-edge identity projects to I, including rectangular layouts; substituting the repeated Gram matrix there was incorrect. Only the projected path is covered, not the whole Fourier product.
- A proper active Fourier bank cannot satisfy exact Weyl transport when both required transported actions have uniformly too-small row degrees. Maximum row degree matters; O(N) total nonzeros alone does not imply that hypothesis. The fourteen-wire extension retains a nonzero central forcing term.
- Hero17 Phase8: every balanced complementary remainder transfer difference is invertible. Its unique minimum literal monomial-basis support is the classical even/odd radix-2 split. The optional invertible-baseline rank-sharpness claim has an N2/GF3 exception. Quadratic setup in the generic polynomial builder is paid, and modular support lower bounds are not automatically complex support equalities.
- A sparse inverse prefix followed by a single additive separated-order tail obeys floor(N/(s·2^d))≤R for a totally nonsingular target. Prime complex Fourier corollaries exclude one individual-Green prefix plus two branches from prime29, and two prefixes plus two branches from prime53. Composite Fourier, products of additive sums, adaptive inputs and general circuit models require separate arguments. The package’s bridge reformulation is being audited separately.
- Hero0 Phase11: its inverse sparse-plus-low-rank obstruction is inherited project work. Its well-conditioned high-Schmidt-rank Green sum is valid, but those properties do not prove inverse rigidity. A new independent countercontrol has dense inverse, maximal Schmidt rank, nonconstant response and condition number below two while its inverse is row-2-sparse plus rank one. The source's SWAP Green is not a Hamiltonian cycle.
- The N16 all-ones inner prefix is exactly ruled out by nonzero augmented minors. The complete 384-parameter coefficient problem is still open. Verifying a generated product is a test of the verifier, not a Fourier construction.
- The earlier norm-gap folding proof and its normalization limitation are preserved historically. The new explicit-minor proof above closes the scalar-normalization gap, while genuine four-channel coefficient laws remain outside that exclusion.

## Cost model and evidence

Field-operation statements presume the specified roots and legal denominators, with generation and root scans charged where stated. They do not imply fixed-bit or numerically stable runtime bounds. Word-RAM routing costs are distinct from exact field arithmetic. Dense finite matrix calculations are verification oracles, not hidden production algorithms.

Independent reviewers authored their own checkers. Uploaded and construction code was kept inert during those independent reviews. Source logs remain source-reported unless specifically reproduced independently. Each included frozen review has exact results and a hash seal. Eight direct 23:44 uploads are retained with their separate Library identities and byte hashes, including genuine identical resends; equal filenames alone were never used to declare duplicates.

The existing master version17 and every inherited file are preserved. Earlier root summaries are archived before replacement. Three construction and three review tracks continue; unresolved synthesis obligations are listed separately rather than presented as completed algorithms.
