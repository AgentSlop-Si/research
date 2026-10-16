# Independent review: multiple-port and q-kernel comparison gates

Date: 16 October 2026 UTC. Repository baseline: `0f3ef16aa4f38ef0c3aee37a296a954dfb7df2d4`.

## Disposition and exact scope

**ACCEPT both bounded comparison gates and the eighteen exact prefix-only targets identified in `ACCEPTED_TARGETS.json`.** The final author report and local proposal passed the mathematical, source, scope and native-preimage checks below.

These are two previously unfinished comparison gates, **not two parent closures**. ALG-016 remains `TO RESEARCH`, priority 34, with its fresh-transform constructor and production obligations open. ALG-020 remains `TO RESEARCH`, priority 34, with arbitrary-input fast convolution open. No source proof is reopened; no historical-priority, novelty, numerical, bit-complexity or unrestricted runtime result is created.

I independently read the live owner records and native comparison mirrors: Catalogue rows 127/131, Research overview rows 189/192, and novelty-attribution rows 120/123. Each owned stop requires an exact hypothesis/formula/cost mapping to a primary source, or a qualified nonmatch or access blocker. The earlier algorithm inventory explicitly classified both as `NEW_COMPARATOR_OR_CHANGED_MODEL_SCOPE_NOT_SELECTED`. The historical multiple-port proof already recognized ordinary finite-dimensional algebra; that recognition is preserved rather than relabeled as a new identity.

## Source binding and prior completed work

Both canonical sources were independently retrieved at the baseline commit and checked from the exact connector response bytes:

- ALG-016: 13,207 UTF-8 bytes, SHA-256 `322f0d1a5a76019fcd8102aaeab68f0302fe6effa83dc7fdc42339de552ec134`.
- ALG-020: 4,084 UTF-8 bytes, SHA-256 `added4a0f022537cb7c72a52e191a28a6eeb640575ba05af61d2e7eb6ef4f3f3`.

The earlier multiple-port independent review (6,106 bytes, SHA-256 `33247cdb1153f0205e9c15aeaa40e2d31183758e03322fb275a1509b5a00641b`) and single-port review (5,266 bytes, SHA-256 `ebaebdba4b83432857c81c741138ab32b14f3e806cc26d1cd53359024dfa6bba`) were read and byte-checked. Their historical executions remain attributed evidence; they were not rerun here. In particular, the multiple-port helper's removed sort does not repair the older checkpoint's gate-generation overhead retroactively.

## ALG-016: exact classical formula map

The directly read published source is [Hager, Updating the Inverse of a Matrix (1989)](https://people.clas.ufl.edu/hager/files/update-1.pdf), printed pp. 221–224, equations (1), (2), (5a), (6), and Section 2. It provides the inverse-update formulas, Schur invertibility relation and a solve sequence that pays the base solve and preparation. It is a direct source for the displayed identities, not certification that any particular named mathematician had sole historical priority. Its numerical conditioning caution is not an exact-field complexity theorem.

Here is the independently checked dictionary. Stack all R vertex states. Let D be the unit block lower-bidiagonal difference operator with subdiagonal blocks −J, and let E_r inject one N-vector at vertex r, so Eₕᵀ extracts the final vertex. Then the full graph operator is

`D − (E₀ U Λ)(Vᵀ Eₕᵀ)`.

The matrix D is invertible and its inverse propagates J along the chain. Its small closure is exactly `I − Vᵀ Eₕᵀ D⁻¹ E₀ U Λ = I − GΛ = S`. The correction therefore yields the owner's `z_r = w_r + J^r UΛS⁻¹g`. No inverse of Λ is needed: duplicate/dependent ports and singular Λ are permitted when S is invertible. Conversely, a nonzero vector in ker S gives a nonzero homogeneous graph solution, so singular S cannot be replaced by a selected regularized answer under the existing contract.

For the coupling edit, substitute `A=S`, `u=Ga`, `v=bᵀ`. The scalar denominator is `θ=1−bᵀS⁻¹Ga`. Direct multiplication gives the owner's updated inverse and the rank-one difference of `ΛS⁻¹`. This is reuse for identical source values and injections with the old solution already accumulated. It does not compute a fresh arbitrary transform.

All charged layers remain: root/field contract; known kernel-row preparation; shared Krylov walks and their storage; `O(NL+Nd²+d³)` initial preparation plus injection contractions; one implemented quadratic ADD_T per injection; both graph sweeps; scalar-gate construction, reciprocals and historical sorting caveats. The initial word still contains `3MN(N+1)/2`. Edit preparation is `O(d²+dMN+RN)` and online work `O(QN+RN)`. Every RN output is charged. Arbitrary dense observations are not free; a small matrix inverse does not erase a missing small-port fresh-Fourier representation. The arbitrary dirty-register compiler contract is additional structure, not supplied by a bare inverse identity.

The report's complementary matrix-function qualifications were also checked against [Higham–Lin (2013)](https://eprints.maths.manchester.ac.uk/2067/1/covered/MIMS_ep2013_73.pdf), Definition 3.2, Section 3.2 and Sections 6.3–6.7. Its complex Hermite/minimal-polynomial and Schur formulations do not supply the missing cheap action. The report separately derives the inverse polynomial over the owner field and correctly retains the splitting/squarefree requirements for a diagonal spectral sum; numerical Schur routines are not silently converted into finite-field algorithms.

## ALG-020: finite Padé, recurrence and Prony interfaces

[Massey (1969)](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf), Sections III–IV, Theorems 3–4 and equation (20), was independently read. It distinguishes finite-prefix synthesis from a full rational generating series. For a reduced series p/r with r(0)=1, full-series register length is `max(deg r, 1+deg p)`, not the sum of these degrees. This provides the appropriate recurrence dictionary; it does not supply the owner's special q-factorial determinant or an arithmetic lower bound.

The source owner assumes dyadic N≥2, primitive q, N invertible, `minpoly(C)=z^N`, and a unit denominator r(0)≠0. Thus operator equality is equivalent to the **all-N-coefficient** congruence `rH_q ≡ p mod z^N`. Under `m+d≤N−2`, the displayed Hankel system is nonsingular in the first degree ordering; the inverse-kernel identity handles the other ordering. No field, boundary or degree guard may be discarded.

The following is a comparison corollary of that accepted determinant, independently checked algebraically. Write N=2n. A length L<n recurrence for the N-term prefix would yield degrees at most (L−1,L), contradicting the accepted sum bound. For L=n, the n recurrence equations have coefficient matrix that becomes `[t_(i+j)]` after column reversal. Its determinant is nonzero. Therefore a unique normalized solution exists; the degree bound forces numerator degree n−1 and denominator degree n. A common factor would contradict the same degree bound, so the pair is reduced. The finite prefix has minimal length n. The zero-extended polynomial H_q instead has full-series register length N. These two inputs must not be conflated.

For s distinct active nonzero modes, a Prony generating series has numerator degree at most s−1 and denominator degree s. Matching the complete N-term prefix consequently requires s≥n. This does not establish that s=n is realizable: the extremal denominator need not split into distinct linear factors in the coefficient field.

[van der Hoeven–Lecerf (2024)](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf), Section 5, Algorithm 4 and equation (10), was independently read. Its input is a black-box polynomial with degree and sparsity bounds; its sequence comes from geometric evaluation. Element construction, evaluations, Padé recovery, roots, discrete logarithms and coefficient recovery are separate steps. The `O(M_K(T) log T)` statement there applies to steps 3 and 6, not the entire pipeline. This is a qualified interface nonmatch to the fixed q-kernel operator action. It supplies no free representation, all-coordinate verification or runtime transfer.

Keep the accepted obstruction limited to bounded-total-rational-degree expressions in the same commuting operator C. Sparse high powers, noncommuting factors, shared subgraphs and other convolution algorithms remain outside the inference. The original tail-fusion counterboundary remains intact. Degree is not an application-cost measure.

## Independent controls and application boundary

Small, newly written reviewer controls passed 80 exact Schur cases, including 27 redundant-port/singular-coupling representations, 5 singular initial closures, 73 nonsingular rank-one updates and 2 singular edits. Eight q-kernel configurations over F17/F97 at N=2,4,8,16 passed 200 Hankel determinant checks, reciprocal-series identities and the unique finite-prefix recurrence equations. The maximum dense system size was 8. These are algebraic controls, not production replay, arbitrary-size experimental proof or speed measurements. Results are in `INDEPENDENT_CONTROLS.json`.

No supplied research program was run, no software was installed, and no external state was changed. Complete native preimages remain local and are excluded from publication artifacts. Any later application must preserve all old strings after an explicit history delimiter, retain status/priority/identity/proof qualifiers, and freshly compare exact target preimages before writing. Only completion/evidence prefixes for the two existing comparison gates are admissible.

## Final artifact check

The final author report is accepted at SHA-256 `520a13a1d8e381f82be38e5b12ac5ed40745fe32191ffe47bee54bf36299eb63`. The local eighteen-cell proposal is accepted at SHA-256 `2f4523f62adaae415b564043083666bd2377c21a83c2f03823a0a487dc34a195` (47,062 bytes). One wording repair clarified that the zero-extended sequence has minimal register length N; it does not require an infinite-sized register. No substantive mathematical repair was needed.

I freshly retrieved all eighteen target cells as native string values and independently verified every exact preimage, prefix concatenation, preimage hash and stable-ID guard. Parent statuses and all corresponding priority mirrors are unchanged. The minimal consistent target set is Catalogue AE/AF on rows 127/131; Research overview F/P/Q on rows 189/192; and novelty-attribution O/P/Y/Z on rows 120/123. The O/P comparison task/evidence mirrors need the same narrow completion prefixes so they do not retain obsolete leading instructions.

`ACCEPTED_TARGETS.json` contains those exact accepted prefixes, cell coordinates, guards and before/after hashes, without native preimage text. The complete application proposal must remain local. Any later writer must perform its own immediate native preflight and restrict the field mask to the intended text values, preserving unrelated metadata. This review authorizes no additional target, no count/status change, no reclassification and no wider mathematical claim.
