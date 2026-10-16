# Independent review: ALG-014 and M-CHIRP-CUBIC comparison gates

Date: 16 October 2026 UTC. Base repository commit: `07455df33fd8243bc0e7facb92af6c6a5830ae2a`.

## Disposition

**ACCEPT the two existing bounded comparison gates and the eighteen exact completion-prefix targets below.** This is comparison completion only. Both parent records remain `TO RESEARCH`, priority `34`; this review contributes zero parent closures, no new theorem, no implementation acceptance, and no historical-priority claim.

## Scope and source identity

I independently read the live native Catalogue rows 126 and 106, Research overview rows 188 and 221, and novelty-attribution rows 119 and 152. The owner stop for each permits an exact primary-source hypothesis/formula/cost mapping or qualified nonmatch. The already-owned implementation/construction obligations remain substantive and open. The earlier algorithm inventory marks ALG-014's comparison unselected; the matrix inventory identifies M-CHIRP-CUBIC's accepted identity and real constructor successor. The comparison gates are therefore not repeats of already-completed owner work. Previously cited recurrence/Prony or Fourier-convention material is context, not a new result merely because it is read again.

Both canonical source files were independently fetched from the pinned commit. Their UTF-8 byte hashes match the native owner identities:

- ALG-014 README: 13,529 bytes; SHA-256 `f1b1856375df9240f253a4e1f124c455b5b22e92bb26df544c7f5f01abffda1c`.
- Odd-chirp accepted review: 7,696 bytes; SHA-256 `c6c30444abc7563e8b02ee613abdd61103c1ce18ded3d39cff6fdb38452dad76`.

Exact pinned URLs are in `INDEPENDENT_CHECKS.json`. The ALG-014 later narrow review also matches its recorded hash `3169d820665e2ae7fafd929bb053d1d7320418ffaa3cae09fde8a58fd290f632`. Its accepted recurrence and online instruction counts must not be broadened into planner/cold-cost/fallback acceptance. Its historical README mismatch remains historical, not repaired or erased here. Full native preimages remain local and are excluded from publication artifacts.

## ALG-014: supplied-mode recurrence and classical recovery interfaces

Primary sources independently read:

1. [Massey, Shift-Register Synthesis and BCH Decoding (1969)](https://www.isiweb.ee.ethz.ch/archive/massey_pub/pdf/BI411.pdf), Section IV, Theorem 4 and corollary; Section V, equations (26)–(27), Theorem 5. A connection polynomial and finite initial state generate the rational series P/C. The shortest-register assertion uses a reduced fraction; its objective is order, not tap count. The weighted power sums provide the exact modal dictionary. BCH recovery starts from syndromes and includes recovery of locators/magnitudes, unlike a supplied-mode evaluator.
2. [van der Hoeven and Lecerf, Sparse polynomial interpolation (2024)](https://www.texmacs.org/joris/ffsparse/ffsparse.pdf), Section 5, Algorithm 4 and equation (10). Its black-box input includes degree/sparsity bounds; the algorithm obtains a suitable-order element, samples, recovers a rational representation, roots, logarithms and coefficients. The stated O(M_K(T) log T) costs cover the Padé and coefficient-recovery steps, not every step. This is a qualified interface nonmatch with supplied roots and fresh amplitudes, not a nonexistence result.
3. [Bostan and Mori, A Simple and Fast Algorithm for Computing the N-th Term of a Linearly Recurrent Sequence (2020)](https://arxiv.org/pdf/2008.08822), Theorems 1 and 3 and Section 2.1. Theorem 1 gives the single-term cost; Theorem 3 separately gives a block of d consecutive terms. Neither may be described as a universal full-output lower bound or as a free substitute for the owner's discovery/conversion/output ledger.

Independent mapping: write S(t)=sum_s a_s/(1-z_s t). The supplied distinct nonzero roots imply that Q(t)=product_s(1-z_s t) divides C(t)=R_b(t^b). Thus C(t)S(t) is a polynomial of degree below b d_b, yielding the owner's recurrence after its paid initial prefix. Q is a common denominator for all amplitudes on the supplied support. For a particular vector with zero amplitudes, cancellation can make its minimal denominator smaller. No minimum-degree claim is imposed on those inputs.

The setup must still include every tested stride, powering, exact-equality grouping, polynomial products, coefficient tests, candidate selection and failed candidates. The prefix M0=min(N,b d_b) is charged. Its fixed online instruction counts are k(M0−1)+(N−M0)tau multiplications and (k−1)M0+(N−M0)(tau−1) additions. These counts are not universal minima; zero or special-value arithmetic may be optimized. All N output values and traffic remain charged. A few taps alone do not bound the prefix or discovery costs. The FFT fallback's additional root contract is separate. There is no free numerator-to-modes conversion, bit-complexity result, numerical-stability result, or arbitrary-support o(N log k) conclusion.

Small reviewer-authored controls verify five exact finite configurations, including the stated N=4096 two-tap example in two fields, powered-root collisions, zero amplitudes, N=1 and N<k. The two-tap case has prefix 32 and counts 8,624 multiplications plus 4,544 additions. These corroborate the comparison dictionary; they do not replay or newly certify the production planner, cold totals or fallback.

## M-CHIRP-CUBIC: matrix functions and a missing cheap operator

Primary sources independently read:

1. [Higham and Lin, Matrix Functions: A Short Course (2013)](https://eprints.maths.manchester.ac.uk/2067/1/covered/MIMS_ep2013_73.pdf), Definition 3.2, Theorem 3.4 and Section 6.7. The complex-field Hermite/minimal-polynomial formulation explains the low-degree rational-function representation when the denominator is nonzero on the spectrum. It does not give an inexpensive way to apply an otherwise expensive matrix, and it is not a finite-field Schur theorem.
2. [Davies and Higham, A Schur–Parlett Algorithm for Computing Matrix Functions (2003)](https://eprints.maths.manchester.ac.uk/156/1/paper.pdf), Section 1.1, equations (1.3)–(1.4), and Sections 2 and 5. Schur/reordering and block Sylvester work are actual computational steps. The scalar recurrence has repeated/close-eigenvalue issues. The general atomic-block Taylor procedure is principally for entire functions; the reciprocal function used here requires appropriate specialization. No generic stability guarantee or O(N) constructor transfers.

Direct algebra, independent of complex spectral theory, gives (I+M)(I−M+M²)=(1+c)I for M=FA and M³=cI. Under 1+c≠0, B=(I+M)⁻¹F and K=M(I+M)⁻¹. With mu(z)=z³−c(1−z)³ and p(z)=(1+c)+(1−2c)z+(1+c)z², the polynomial identity (1−z)p(z)=1−mu(z) proves the recorded inverse. This argument retains characteristic 3, where the permitted cubic may be inseparable. A distinct-root spectral-projector argument would instead require extra splitting and characteristic assumptions. It cannot replace the accepted general-field proof.

Preserve all original guards: odd N≥3, primitive Nth root, characteristic not dividing 2N, and feedback nonresonance 1+c≠0. Exact minimal degree three is asserted only for N≥5; N=3 may have smaller degree. Chirp signs and Fourier normalization cannot be interchanged. The unnormalized complex nonresonance argument is not a finite-field claim. Finite-field resonance remains excluded. No floating-point or bit-complexity result follows from the exact identities.

The Horner identity uses three B calls and two diagonal A calls plus vector work. A and c are cheaply generated in the accepted model, but the displayed B formulas still call F, its inverse-sign counterpart or FAF. Neither matrix-polynomial notation nor precomputed dense projectors erase those operations or their preparation. The true successor is still a uniformly generated cheap B without a Fourier oracle, or the specified admissible realization with all costs paid. The specific full-rank correction does not establish arithmetic hardness or impossibility of every other constructor.

The reviewer also checked the scalar polynomial inverse identity for 110 admissible finite-field (characteristic,c) pairs, including characteristic 3. These are limited algebraic controls, not an all-length implementation test.

## Publication/update boundary

Only the named comparison completion, exact source locators, and the already-owned remaining obligations may be added. Preserve all earlier native text behind the agreed history delimiter. Preserve stable identities, source hashes, proof qualifications, scores and statuses. Do not rename either parent as a comparison-only task or close a substitute record. A fresh equality check against each exact preimage is required immediately before any later application.

No external state changed in this review. No supplied research code was run, and no software was installed. Publication-safe artifacts are this report and `INDEPENDENT_CHECKS.json`, plus the final accepted-prefix receipt when available.

## Final artifact check

The final author report is accepted at SHA-256 `7b750cf6008060ec9a2c73897809800280378ca645ace28a07054288cc2310ba`. The local eighteen-cell proposal is accepted at SHA-256 `648f90c7d4e7e7716106f964205db19d1bf50e7de2671745044a66b80797c5f3`.

I independently retrieved all eighteen target cells as native string values and verified exact equality with every proposal preimage. Every proposed result is precisely its accepted prefix followed by the entire old string. Stable-ID, parent-status and priority checks passed. No target changes a status, score, proof acceptance, novelty classification, row identity or source bytes.

The accepted minimal consistent mirror set is Catalogue AE/AF on rows 126 and 106; Research overview F/P/Q on rows 188 and 221; and novelty-attribution O/P/Y/Z on rows 119 and 152. The four O/P cells belong to the existing comparison-task/evidence view and would otherwise retain visibly obsolete leading instructions or lack the newly completed mapping; their narrowly scoped prefixes are accepted. All exact prefix texts, targets, preimage hashes and output hashes are in `ACCEPTED_TARGETS.json`. It contains no raw native preimages. The complete application proposal must remain local.

The final report includes the active-mode denominator qualification and the nonzero scalar normalization between Algorithm 4's monic denominator and the owner's constant-one denominator. It explicitly includes Bostan–Mori's consecutive-term theorem. Its complex-field, characteristic-3, reciprocal-function analytic-domain and paid-Fourier-operation boundaries are correct. The unread Cornell body is excluded from reliance. These qualifications resolve the review comments; no conditional substantive acceptance remains.
