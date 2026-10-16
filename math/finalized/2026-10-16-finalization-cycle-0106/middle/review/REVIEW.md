# Independent review: q-Weyl tail and sparse-grading comparison gates

Date: 16 October 2026 UTC. Repository baseline: `73528f9e7495b0614106dfc4cc5b5c42907daaf5`.

## Review scope and decision boundary

The two existing comparison tasks are ALG-018 (Research overview 190, Catalogue 129, novelty-attribution 121) and ALG-019 (overview 191, Catalogue 130, novelty-attribution 122). Fresh independent native reads establish that both primary-comparison gates are unfinished. Their exact stops permit a primary-theorem hypothesis/formula/cost mapping or a qualified nonmatch. The prior algorithm inventory also records each as `NEW_COMPARATOR_OR_CHANGED_MODEL_SCOPE_NOT_SELECTED`.

The full source and earlier review history preserve genuine unfinished parent work. ALG-018 still lacks the low-degree remainder and shared complete-transform construction; ALG-019 still lacks an improved complete graph with additional proved sharing. A comparison completion cannot close either parent, change priority 34, or promote proof, implementation, novelty or canonical counts. The already accepted tail implementations, grading identities and exact slower decimation are not new results in this review.

**ACCEPT the two named comparison completions and the final eighteen-cell prefix-only proposal.** The scientific mappings below meet the declared comparison scope. The final artifact hashes and native checks appear at the end. This acceptance contributes zero parent closures.

## Source identity and historical coverage

All seven owner-linked canonical source/review bodies were independently retrieved at the baseline commit and read in full. The source identity receipt lists their complete URLs, sizes and hashes. ALG-018's original block-tail README is `7bb8400c402dc65c0f741d0820bcc3ca3829261c853e8f2ac7a629fdd1463c60` (11,186 bytes); its repository sanitized export is `433f08d898ea3c403ff4da71e33e9e836f156584c64781dc3b81fca589f7eee1` (11,154 bytes). Both versions were read and the distinction is preserved. It is not a source corruption or a newly repaired historical hash.

The full ALG-018/019 entries of the earlier REVIEW-16 ledger were read; its complete-file SHA-256 is `46f76abe46263e0a4ef6a62eb4d017a33cc875b49f850fa073ee6ae0b5baf313`. Recorded historical audit counts remain attributed evidence. This review does not run or newly accept those implementations. The prior same-target full-similarity comparator, nested-tail comparison, and failed naive faster-recursion question are already completed and are not counted again.

## Primary passages independently inspected

- [Massey, Shift-Register Synthesis and BCH Decoding (1969)](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf), Section II equation (2), Section III Theorem 3, Section IV equation (17), Theorem 4 and its corollary, and Section V equations (24), (26)–(27). The paper distinguishes a finite-prefix recurrence from an infinite rational generating series. For a reduced rational series A/B with B(0)=1, the register length is max(deg B, deg A+1). This supports the recurrence dictionary, rather than a free operator-evaluation algorithm.
- [van der Hoeven and Lecerf, Sparse polynomial interpolation (2024)](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf), Section 5, Algorithm 4 and equation (10), plus Sections 5.1–5.3. The inputs are a black-box polynomial and degree/sparsity bounds; the procedure obtains suitable-order nodes, samples, a rational representation, roots, exponents and coefficients. The displayed fast Padé/coefficient bounds cover specified stages; root finding, logarithms, extension arithmetic and sampling are additional obligations.
- [FFTW authors, Pruned FFTs](https://fftw.org/pruned.html), opening discussion and the first-K-outputs construction. The stated selected-output and sparse-input interfaces differ from arbitrary full-transform inputs and all outputs. Its arithmetic discussion is not a finite-field stability or production certificate, and the practical caveats cannot be converted into an arithmetic impossibility theorem.

## ALG-018: supplied tail coefficients versus unknown-mode recovery

Retain the finite-corner identity C=TBT^-1, supplied primitive Nth root, invertible N, dyadic dimensions, and the distinction between two targets. The original fused target P(C)T with top-r-supported P is evaluated in O(Nr). The block target L=C^(N-r)p(C), deg p<r, uses dyadic 1<=r<=N/2 and costs O(N log(r+1)) including cold preparation. Neither is the full invertible H_q(C) for small r.

An exact comparison dictionary is P(z)=z^(N-r)p(z). If J is the set of nonzero coefficients p_k, then

P(q^j)=sum_(k in J) p_k (q^(N-r+k))^j.

These are distinct nonzero modes because the exponents lie in one interval of length r<=N. The generating denominator is product_(k in J)(1-q^(N-r+k)u), normalized to constant one. It is proportional to the monic denominator used by Algorithm 4. For these complete infinite scalar samples, the reduced denominator has degree |J|. This is a precise classical Prony/rational-series match for samples of the supplied coefficient polynomial.

Those samples are not the arbitrary vector x, the suffix of T^-1 x, or the output Lx. The operator construction is already given the coefficients. Recovering them from scalar samples would add work and would not supply the paid arbitrary-input projection or full decoding. The rank statement is instead rank(L)=r-v for nonzero p of valuation v, with the zero polynomial handled separately. For constant nonzero p, coefficient-polynomial samples have one mode while L has rank r. Neither number may replace the other in the cost ledger.

For the block action, the first projection reads all N input coordinates. Length-2r transforms use q^(N/(2r)); every window, normalization, middle action, decoding and output write remains charged. The source's preparation and online butterfly counts P=(2N+r)log2(2r) and V=(2N+4r)log2(2r), other scalar operations and O(N) storage remain unchanged. The excluded r=N endpoint needs an additional root or another multiplication backend. The nested same-input rule keeps its actual noncommuting order and r+s-1 state bound; independent source vectors cannot share that proof.

No input sparsity or unknown-mode promise is needed for correctness of the fixed tail map, so no Prony membership test is hidden in its implementation. Conversely, a small sample fit cannot certify an unrelated arbitrary input as a member of a sparse class. All-coordinate operator equality comes from the retained algebra, not a sampled tail comparison. Q07's separate recognition interface does not replace these application costs. No lower bound on polynomial degree alone is a time lower bound.

## ALG-019: sparse coordinate motion versus temporal recurrence order

Retain R's nonzero weighted N-cycle, product of weights one, R^N=I, HR=DH and invertible H=H_q(C). The sequence x_j=R^j x_0 is the only declared reusable family. The sparse recurrence D=R(I-C) propagates a previously computed full y_0=Hx_0; it does not compute that anchor for free or cover independent new inputs.

The formal vector generating series is

sum_(j>=0) y_j u^j = H(I-uR)^-1 x_0
 = H(sum_(j=0)^(N-1)u^j R^j)x_0/(1-u^N).

Take x_0=e_0. Its first N iterates under R are nonzero multiples of different coordinate vectors, hence a basis. Multiplication by invertible H preserves their independence. No common scalar constant-coefficient recurrence of order below N can generate the complete vector sequence: its first recurrence equation would be a nontrivial relation among at most N of those independent vectors. The period-N relation supplies an order-N recurrence. Equivalently, the cyclic operator R and its conjugate D have minimal polynomial z^N-1.

This is an exact qualified nonmatch to an automatically small-mode Prony model. Every x_j remains one-sparse in the original coordinates for this example, yet the full output's common temporal recurrence order is N. A particular scalar coordinate or linear functional may cancel modes and have smaller order; no lower bound for every projection is asserted. The argument is not an arithmetic lower bound, and the source itself supplies O(N) updates after the paid anchor.

The author's additional scalar witness is also correct: e_0^T R^j e_0 equals one when N divides j and zero otherwise. Its generating series is 1/(1-u^N), and root orthogonality represents it as the sum of all N distinct q-grid modes with coefficient 1/N. Massey's reduced-fraction rule gives scalar register length N. Algorithm 4 with sparsity bound N would require order at least 2N; the supplied root has order N. This is a limitation of that invocation, not a barrier to known-grid N-point reconstruction or another paid algorithm.

Each complete input/output update retains 3N-1 multiplications and N-1 additions; writing or storing every queried output remains paid. The full fresh-input evaluator is a different construction: D_r=p_r(J_n)diag(q^-ri), with filter degree r doubling and dimension n halving. Its first child has three nonzero entries per row for N>=8, so a monomial change cannot restore the original two-sparse family. The three-call even/odd scheme and node cost min(rn,n²) give the retained Theta(N^(1+0.5 log2 3)) online bound, O(N log N) preparation and O(N) live storage. This is slower than the source's O(N log N) complete-operator comparator. Neither Prony recovery nor FFT pruning supplies the missing sharing rule or removes filter growth.

## Independent controls and limitations

A small new reviewer-written exact checker passed eight configurations over F_17 and F_97, N=2,4,8,16. It checks the finite-corner nilpotence, H invertibility, HR=DH, full output-orbit rank N, the raw scalar periodic-series/all-mode identity, and 48 tail rank/coefficient-sample recurrence controls including zero and high-valuation polynomials. It imports no supplied research programs. These controls corroborate the mapping and edge cases; the all-length conclusions use the algebra above. No implementation, numerical-stability, bit-cost or historical-priority promotion follows.

## Exact-cell review boundary

Only comparison-completion/evidence prefixes may be appended through the agreed history-preserving prefix convention. Parent statuses, scores, stable IDs, proof qualifiers, source hashes and earlier text must remain unchanged. A valid final proposal must match independent native preimages and contain precisely prefix plus the complete previous string for every target. Full native preimages stay private; the publication-safe receipt contains targets, prefixes and hashes only. No external write is performed by this reviewer.

## Final artifact and exact-cell acceptance

The author report is accepted at SHA-256 `96efb3ac2f3089c229d7d25f861c3e0082a78f0c4ecc490b6a07f6c870fc764a`. The final local proposal is accepted at SHA-256 `de8f1b5a5f8ef2a8dfab5aade7ab9b6523c6febde8ae24007e3a3ccf509a7450`. One wording correction was made before acceptance: 1/(1-z^N) is now correctly described as a generating series. No unresolved scientific condition remains.

All eighteen target values were independently retrieved as native CellData and match the proposal's complete preimages. Every after-value is exactly its accepted prefix plus the full earlier string. Stable IDs, parent statuses and priority 34 all pass. The allowed targets are Catalogue AE/AF on rows 129/130; novelty-attribution O/P/Y/Z on rows 121/122; and Research overview F/P/Q on rows 190/191. This is the minimal consistent existing comparison-action/evidence mirror set, not a set of renamed substitute parents.

All targets have existing formats. Research overview F190 and F191 also have existing notes. Preserve those metadata objects and every other unlisted cell property; a text-only value update must not remove them. There are no target formulas in the reviewed snapshot. Fresh preimage and metadata checks remain necessary immediately before application, because an accepted local snapshot does not lock the workbook.

`ACCEPTED_TARGETS.json` records the exact accepted prefixes, before/after hashes, source metadata hashes and artifact identities without publishing raw native preimages or notes. `INDEPENDENT_CONTROLS.json` and `SOURCE_IDENTITIES.json` are also publication-safe. The exact applied receipt and any verified publication links are separate later work.
