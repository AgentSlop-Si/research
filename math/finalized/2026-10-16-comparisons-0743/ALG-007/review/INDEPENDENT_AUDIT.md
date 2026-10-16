# ALG-007 independent comparison audit

Date: 16 October 2026 UTC. Status: ACCEPT for the named comparison and eight-cell proposal; parent record remains open.

## Current finding

The final selected common-support comparison completes the recorded bounded comparison, with a qualified nonmatch for the full ALG-007 package. It does not certify the entire algorithm as historically new, provide a new all-input FFT, repair the supplied executors, or establish a floating-point membership guarantee.

The final author proposal correctly separates whole-record closure. The owner text contains an implementation obligation about a compatible, charged fallback. Completing the comparison does not itself implement that fallback. The proposal leaves this obligation open, preserves parent status TO RESEARCH and priority 42, and does not invent broader obligations. Count delta is zero: the supplied parent baseline of 71 closed, 256 open, 327 total is unchanged by this proposal; this audit does not recensus unrelated rows.

## Independent owner and source reads

- Native spreadsheet: https://docs.google.com/spreadsheets/d/1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU/edit
- Stable ID: ALG-007. Live owner rows are Catalogue 72, novelity breakthough 33, and Research overview 50.
- Native priorities are 42 in Catalogue AA72, novelty U33, and overview L50.
- Full native CellData preimage was captured independently, including formulas, formats, notes, validation, and hyperlinks.
- Original Phase6 audit was fetched independently at pinned repository commit 8172ebf0371ef83a6c5aaa2de778358c89088b22. Its documented sanitized export is distinct from the original audit-byte identity. No source hash is silently relabeled.
- Primary comparator read independently: Barbotin, Hormati, Rangan, and Vetterli, Estimation of Sparse MIMO Channels with Common Support, arXiv:1107.1339v1, especially Section II.B, Lemma 1, Proposition 1, and Algorithms 1 and 4. https://arxiv.org/pdf/1107.1339v1
- Secondary context read independently: van der Hoeven and Lecerf, Sparse polynomial interpolation: Faster strategies over finite fields, final version 2 May 2024, Section 3.2 and Algorithm 4. https://www.texmacs.org/joris/ffsparse/ffsparse.pdf

The primary paper supplies a noiseless common-node annihilation relation and numerical support-estimation procedures. Its algorithms take a model-order estimate and use matrix decompositions, roots, and coefficient solves. Neither this result nor the secondary sparse-interpolation discussion supplies the full ALG-007 raw-input cost contract. The latter also charges polynomial evaluation, root recovery, discrete logarithms, and coefficient reconstruction separately. These summaries do not establish earliest attribution for any mechanism.

## Independent mathematical derivation

Use the owner's Q=KM, K>=M>=2, even Q, fixed unit slope and shift, supplied compatible root zeta, and characteristic not dividing 2Q. Let xi=zeta^K, lambda_u=xi^(-u), and c[b,u]=D[b,u]/M. Then the dechirped raw blocks satisfy

    y[b,t]=s[b,t] x[bM+t]=sum_u c[b,u] lambda_u^t.

Their coefficient vectors c[:,u] have union support S. This is an exact vector-polynomial representation: P(Z)=sum_u c[:,u] Z^u, evaluated at Z=xi^(-t). The fixed-support dimension is K|S|. It does not assert low recurrence rank of the original concatenated raw coordinates.

The forward characteristic polynomial is

    A(Z)=product_(u in S)(Z-lambda_u).

Writing A(Z)=sum_j a_j Z^j gives the shared recurrence

    sum_j a_j y[b,t+j]=0

for every block b and integer t, using M-periodic extension. This fixes the reciprocal-polynomial convention without relying on the primary paper's potentially inconsistent displayed filter-root convention. A delay polynomial instead has reciprocal roots; it must not be interchanged silently.

For joint minimality, suppose a polynomial B of degree less than |S| annihilates all blocks. For each b, the |S| consecutive equations at t=0,...,|S|-1 give a Vandermonde system for c[b,u] B(lambda_u). Since all lambda_u are distinct, every product vanishes. Every active u has some nonzero c[b,u], so B vanishes at all |S| nodes, a contradiction. This uses union support and does not assume that every mode is nonzero in each block. The zero input has empty support and is handled separately.

Individual-block uniqueness cannot be imported when some amplitudes vanish. Nor can a fixed scalar projection replace vector data: over F17, a mode with coefficient vector (1,16,0,0) is active but disappears under sum projection. Numerical TLS and exact finite-field recurrence are distinct interfaces.

The M grid values determine the degree-less-than-M polynomial exactly and can be repeated periodically. Therefore a raw shortage of 2r distinct samples is not, by itself, a nonmatch argument here. For the secondary Algorithm 4, its explicit order restriction still belongs to that published algorithm; relaxing it by periodic algebra is a separate derivation. Arbitrary new-node or extension-field evaluations are not free.

## Cost and hypothesis review

The recorded complete accepted ledger is

    O(Q+rQ+rK log K+(r+1)M log M), storage O(Q).

Its comparison must retain reads, root table and chirps, every raw-coordinate certificate, at most r full support discoveries, coefficient storage, all r Green decoders, seed sums, accumulation, normalization, and all Q writes. The source's displayed proxy omits at least r(Q-1) seed additions and other setup; it is not a complete end-to-end operation count.

Cap-R rejection costs O(Q+RQ+(R+1)M log M) before decoding. The supplied executors return rejection. Any proposed ordinary-FFT fallback must be compatible and its cost added after recognition; its absence is not cured by an external support-recovery theorem.

The fast-transform ledger retains its declared suitable-transform assumptions. In a root-only abstract field, use explicit transform costs T(K), T(M) until their fast bounds are justified. The even-composite identity itself is broader than the shipped dyadic, fixed-field implementation. Likewise M=Theta(log Q) is an eligible-factorization specialization, not a padding theorem.

Root/field discovery, a growing chirp or factorization search, floating-point recognition, bit complexity, and hardware advantage do not follow. They should not become invented completion requirements for the current comparison.

## Fresh finite controls

The independently authored standard-library-only checker passes 224 cases over F17 and F97, with Q=12,16,24,32. It checks the exact raw/dechirped coefficient map, forward annihilation with wrap, and joint minimality rank for all-block, one-block-only, disjoint-block, late-only, empty, and full-support patterns. A scalar-projection cancellation control also passes. It neither imports nor runs supplied research programs and makes no optimized implementation certification.

## Final native proposal and candidate acceptance

Novelty R33 contains a dynamic stable-ID hyperlink formula. It must be preserved. Overview notes exist in A50,B50,C50,F50,G50,I50,J50. The I50 note contains a stale novelty-row anchor A49:Z49; the live owner is A33:Z33. An optional correction must be an explicit note-only edit with its own preimage. Untouched note, format, formula, validation, and history fields must not be discarded.

The final proposal was matched against a second independent live native read after candidate completion. All eight exact preimages match. The scope is Catalogue AE72/AF72, novelty Y33/Z33, and overview C50/F50/P50/Q50. Each update changes userEnteredValue only and preserves its prior text verbatim as dated history. Stable IDs, all priorities, parent status, dynamic formula, and untouched metadata are preserved. No external write has been performed by this audit.

Accepted report SHA-256: 7c7cbf3a8f8933bcadcbd941f7baef963625f238a65506f0b6e2bbcf9c86b094.

Accepted proposal SHA-256: d871e66cdcbaf66319fd8ed4a5f18a18340b25e8262d267fe6484d585dba4f62.

The report's original archive identity and all 22 supplied manifest entries were independently verified as data, including the exact original theorem text. No supplied program was run. The full-support runtime wording was repaired before acceptance: the full-bank algebraic endpoint is the ordinary transform, while the literal r-fold scan cost can exceed FFT scale outside the logarithmic-block specialization.

The deliberately nonoptimized derived comparison in the final report is mathematically consistent. On a promised support of size t<=R, an R-by-R moment matrix factors as V diag(c) V^T and has rank t; its leading t-by-t matrix is invertible. Solving and scanning the known root grid, followed by complete reconstruction and union checks, costs O(Q+KR^3+QR) in the declared field model. Negative candidates may be rejected, but cannot be accepted without reconstructing every coordinate. This is a separately derived paid comparator, not a claim that the cited numerical method implements ALG-007.

Acceptance is for these exact file hashes. A publisher or native integrator must recheck final live stable-ID/preimage equality immediately before any external update and verify readback afterward. Any drift or substantive report revision requires reconciliation rather than blind application.
