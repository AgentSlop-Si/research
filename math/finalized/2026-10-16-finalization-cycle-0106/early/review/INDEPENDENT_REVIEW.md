# Independent review: balanced-seed comparison

16 October 2026 UTC. Baseline: AgentSlop-Si/research commit `73528f9e7495b0614106dfc4cc5b5c42907daaf5`.

## Decision

**ACCEPT** the mathematical comparison and exact 15-cell proposal SHA-256 `9d414e6c93664a4a6a8365084d9a9bd1e687dd79352e1bc68ce968093dbdd5a2`. The reviewed author report has SHA-256 `fc7de68baf8d9314fe96ab4134a4658cbab78041ee8df50e4d9c27383b9fff10`. M-SEED-BALANCE can close at its existing one-internal-monomial, bi-regular-right-factor scope when the reviewed primary comparison is recorded. No external write has been made.

The independent live reads bind this record to Research overview row 95, Catalogue row 57, and novelity breakthough row 78. Its operative owner stop accepts a primary-theorem hypothesis/formula/cost mapping or a qualified nonmatch. The correctness proof is already accepted. Worldwide priority, unrestricted endpoint masks, inexpensive application of the sufficient right factor, and full equality inferred from first-cross calibration are expressly unestablished consequences. They are not selected successor obligations of this owner. Closing the bounded record must retain those limits and priority 42.

## Source identity

The accepted Phase35 review was independently fetched at the pinned baseline from [the repository source](https://github.com/AgentSlop-Si/research/blob/73528f9e7495b0614106dfc4cc5b5c42907daaf5/math/archive/objects/b1/b1d13ce38ed662d9379e25ea0e87bed498174a56d161a84b7b20bbaaaee16de0__REVIEW.md). The complete retrieved body has 7,036 bytes, SHA-256 `bd23457a80045e091d0cc1b9a2f826a17d995120d1a13037716fb003dd9c9941`, and recomputed Git blob `77ccbaaec858859ab8ed25befa24d294e8036bbb`. The filename's historical hash identifies different original/export provenance and must not be called the current sanitized-byte hash. These values agree with the live evidence cell's export hash.

The new primary is Martin Idel and Michael M. Wolf, [*Sinkhorn normal form for unitary matrices*, arXiv:1408.5728v3](https://arxiv.org/pdf/1408.5728v3), 4 September 2015. Its bibliographic record identifies *Linear Algebra and its Applications* 471 (2015), 76–84, DOI `10.1016/j.laa.2014.12.031`. The independently read ten-page preprint contains Theorem 2 on printed pages 1 and 3, Lemma 1 on pages 2–3, Section 3 equation (2) on page 4, and its conclusion on page 6. The separate short 2016 version's Theorem 1.1 numbering is not used.

Theorem 2 guarantees two diagonal unitary factors that give a complex unitary matrix row and column sums one. Lemma 1 connects this to a vector whose coordinates, and whose image coordinates, all have modulus one. The proof is nonconstructive. Section 3 conjugates a unitary fixing the all-ones vector by normalized Fourier to obtain a `1` plus an `(N−1)`-dimensional unitary block. The conclusion leaves universal convergence of the cited iteration unresolved. This provides a model comparison, not a construction-time or finite-word theorem.

PDF text was accessible. Screenshot attempts on the already-read v2 theorem pages returned cache misses; no PDF screenshot or local primary-PDF hash is claimed. The v3 text was subsequently independently read. The following elementary algebra resolves any conjugate-transpose extraction ambiguity.

## Independently reconstructed owner criterion

Let `F` be the unnormalized complex Fourier matrix, `u` the all-ones vector, and `e0` its first coordinate vector. The owner fixes invertible `A` and allows a middle diagonal, or diagonal times a permutation, and an invertible bi-regular `B`. Write `Bu=b u` and `uᵀB=b uᵀ`. Invertibility implies `b≠0`.

The first Fourier row in `F=A D B` forces `A[0,i]D[i,i]=1/b`, so a zero first-row entry disqualifies `A`. Multiplying by `u` gives `A (1/A[0,*])=N e0`. Equivalently, every leverage `A[0,i](A⁻¹)[i,0]` equals `1/N`. Conversely, set `D=diag(1/A[0,*])` and `B=D⁻¹A⁻¹F`. The reciprocal-row condition proves both row and column sums of `B` are one. Thus sufficiency really allows an unrestricted right factor that can contain the Fourier computation itself.

A permutation can be absorbed into `B` because it fixes `u` on both sides; a general diagonal unitary cannot. Over the complex numbers, unitary `A` changes the leverage condition to `|A[0,i]|²=1/N`. This unitary specialization is not the arbitrary-invertible theorem and does not transfer complex spectral norms to finite fields.

## Exact bridge to the primary and strict nonmatch

Set `f=F/√N` and `U=A* f` for unitary `A`. Then `Uu=√N A*e0`. The owner condition is exactly that this particular vector has unimodular coordinates. That is equivalent to the one-sided decomposition `U=D0 B0`, with `D0` diagonal unitary and `B0` unitary fixing `u`: if the condition holds, choose `D0=diag(Uu)` and `B0=D0*U`. A unitary fixing `u` also has column sums one. Conversely, such a decomposition makes `Uu=D0u` unimodular. Fourier normalization and normalizing the original common sum merely redistribute scalar factors.

The primary allows a freely chosen right diagonal `R`, hence a freely chosen input vector `Ru`. The owner fixes that vector to `u`, up to a harmless global scalar. This is a strict difference, not a contradiction between the two results.

The author's exact separator was independently checked. For

    A = [[24/25, −7/25], [7/25, 24/25]],

`A` is unitary, both first-row entries are nonzero, and `(A−I)*(A−I)=(2/25)I`. Thus `||A−I||₂=√2/5<1/2`, inside the accepted weak-coupling regime. Its leverages are `576/625` and `49/625`, so the owned seed criterion fails. Yet

    U = A* f = [[31,17],[17,−31]]/(25√2)

admits `R=diag(1,i)`, `z=(31+17i)/(25√2)`, and `L=diag(conj(z),i conj(z))`. Their product is

    L U R = [[961−527i,289+527i],[289+527i,961−527i]]/1250.

Direct Gaussian-rational arithmetic verifies it is unitary and has row and column sums one. Meanwhile `Uu` has squared coordinate magnitudes `1152/625` and `98/625`, so one-sided balancing fails. Write the balanced factor as `V=LUR`. Absorbing `R*` would replace it with `VR*`; if `VR*u=b u`, multiplying by `V*` would force `R*u=b u`. But `R*u=(1,−i)` is not a scalar multiple of `u`.

An independently selected second rational rotation gives the same strict distinction, without the weak-coupling premise. Both checks supplement the algebra; neither is a numerical experiment establishing a uniform theorem.

## Preserved limits and costs

The accepted nonunitary weak-coupling estimate remains `|A00(A⁻¹)00| ≥ 1−δ²/(1−δ)>1/2` for `A=c(I+E)`, `||E||₂≤δ<1/2`. Positive real scalar combinations of permutation resolvents satisfy the stated reduction when all coupling magnitudes are below `1/3`. Signed combination weights, arbitrary masks, row-dependent weights, and independently gauged branches do not acquire this conclusion. The independent small checker also confirms the inherited `δ=7/24` value yields `359/408`.

The fixed N8/N16 common-coupling polynomial exclusions remain accepted only for the specified cycle pairs and nonzero-denominator, invertible regime. They were not replayed here. Distinct couplings, other cycles, extra masks, irregular right factors and independent endpoints remain outside that certificate.

The seed test pays for obtaining a row via transpose application, the forward application, guarded reciprocal operations, preparation, coefficient representation, storage, and input/output. A fixed number of structured Green applications may be linear in field operations after preparation; arbitrary dense `A` is not automatically cheap. First-cross calibration certifies only `2N−1` entries. Exact sorting needs a comparison/representation model, hashing needs its stated randomized/data assumptions, and finite moments do not prove multiset equality. The Idel–Wolf existence theorem supplies no free phase construction, exact root representation, stable numerical algorithm, bit-cost bound, or fast application of the remaining block. Its recursive Fourier decomposition cannot be used as evidence of a new fast Fourier implementation.

## Exact native proposal acceptance

All 15 proposed preimages match a second independent bounded native CellData read of the three owner rows. Fourteen edited strings preserve their complete prior contents after the explicit history marker; only Research overview E95 changes the enum from TO RESEARCH to CLOSED. All seven supplied unchanged guards match, including the three stable IDs, three numeric priorities, and the dynamic catalogue-link formula at novelty R78. Action and stop-condition mirror groups agree.

The accepted targets are Research overview C95, E95, F95, J95, P95, Q95; Catalogue AE57, AF57; and novelity breakthough N78, O78, P78, Q78, T78, Y78, Z78. The initial draft omitted T78, leaving a stale SCREENED ONLY current assessment. That was repaired before acceptance, preserving its old text as history. All updates use only `userEnteredValue`; no targeted cell has a formula, rich-text link run, or explicit whole-cell text-format link. Unchanged notes and metadata are not rewritten. The current primary-source locators are added while the prior repository locator remains in the preserved history.

This is one closure, with priority 42 unchanged. From the stated baseline and absent unrelated concurrent edits it would produce 71 closed and 256 open records. Those are conditional counts, not a full live recount or an external-write receipt. The applying parent must check exact preimages immediately before writing, then verify every target and unaffected field against readback and independently recount the complete overview.

## Execution and publication boundary

No supplied research program was executed, imported or compiled. No installation, large solver, external write or denied-network retry was used. Only the small reviewer-authored standard-library exact checker was run. Raw native preimages and full source snapshots stay outside this publication directory. The final cell proposal must preserve unrelated formulas, links, formats, notes, validation, priorities, accepted statements, and complete dated history, and must be checked against fresh unchanged preimages before application.
