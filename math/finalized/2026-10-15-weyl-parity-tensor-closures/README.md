# Three scoped Fourier research closures

15 October 2026. Prepared for `AgentSlop-Si/research` at `math/finalized/2026-10-15-weyl-parity-tensor-closures/`.

## Accepted conclusions

The author and independent reviewer accept finalization of three existing theorem records at their stated scopes:

- **M-WEYL-RESIDUAL:** the two Weyl equations characterize the scalar Fourier family over a supplied-root field, without requiring the candidate matrix to be invertible. Over the complex numbers, the sharp Frobenius residual gap is `2 sin(pi/N)`. After deterministic scalar calibration, a fixed linear finite-field candidate passes `h` independent uniform common probes with exact probability `q^(-h rho)`, where `rho` is the stacked defect rank, using `1+3h` candidate calls. This does not test linearity or cover adaptive/stateful candidates; preparation and full evaluation work remain charged.
- **M-PARITY-DEPTH:** for complex dyadic Fourier matrices, parity half-blocks have rank `N/4` or `N/2` according to the highest mask bits. The moving GF(2)-affine quasiseparable-stage argument gives a weighted quota obstruction and, for uniform order `r>=1`, `k<=t ceil(log2(4rt))`. Arbitrary invertible external monomials are allowed for the coarse depth theorem; internal routing remains GF(2)-affine. The all-zero-order case includes singular weighted-permutation products. Preserve the historical capacity correction: boundaries `31,31` at `r=2` mean **124**, not 62. No finite-field universal-sampling theorem is inferred.
- **M-TENSOR-CUT:** with `N=QM`, input `j=t+Qu` and output `k=h+Ms`, the three labeled paired tensor cuts have ranks `N`, `min(Q,M)`, `N`, and CP rank is `N`. Separate invertible changes on the `s` and `u` legs have support at least `N`, with equality precisely when `AF_Q` and `F_M B^T` are monomial. Endpoint Fourier conversions retain their cost; a growing middle-cut obstruction requires both radices to grow.

These are closures of already accepted scoped results. They do not establish new discovery, worldwide priority, unrestricted Fourier lower bounds or a faster all-input Fourier algorithm. The complete proofs, guards and comparisons are in the [author report](reviews/AUTHOR_FINALIZATION_REVIEW.public.md) and [independent review](reviews/INDEPENDENT_SCOPE_REVIEW.public.md).

## Primary-source attribution

- Tyson, Theorem 5, attributes the invertible-complex Weyl characterization to Weyl. The match covers that subdomain; the supplied reports prove the additional singular-candidate, quantitative and calibrated finite-field statements directly. [Primary source, section 2](https://arxiv.org/html/quant-ph/0306144#S2)
- Freivalds, Theorem 3 (1979), supplies the fixed linear-defect random-vector testing antecedent. Its random-sign real-matrix theorem is distinct from the exact finite-field joint-kernel probability. [Primary proceedings, printed pp. 59–60](https://raganwald.com/assets/fractran/Mathematical-Foundations-of-Computer-Science-1979-Proceedings-8th-Symposium-Olomouc-Czechoslovakia-September-3-7-1979.pdf#page=68)
- Osgood–Siripuram–Wu, Theorem 4, is the explicitly imported characteristic-zero universal-sampling theorem used for the parity-rank application. The moving-affine depth argument is proved separately. [Primary theorem](https://arxiv.org/html/1204.0992v1#S4.SS2)
- Cooley–Tukey's mixed-radix substitution gives the phase identity with `r1=M,r2=Q,j0=h,j1=s,k0=t,k1=u`, conjugating for the negative sign. Tyson's Definition 12/Corollary 15 matches specifically the `(s,u)|(h,t)` rank-`N` cut. These mappings do not attribute the full local support-rigidity package to either paper. [Cooley–Tukey](https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Cooley65.pdf), [Tyson, section 5](https://arxiv.org/html/quant-ph/0306144#S5)

Exact mappings, overlap and bounded nonmatches appear in [the author comparison record](attribution/PRIMARY_COMPARISONS.json) and [independently checked attribution](attribution/PRIMARY_SOURCE_CHECKS.json). An incomplete prior-art match is not evidence of novelty.

## Evidence and application status

The independent metadata review accepts **66 value updates and three status-background updates**, including three status transitions, with **63 historical prose suffixes retained** and **160 sampled preservation cells unchanged in simulation**. The [public verdict](reviews/PUBLIC_PAYLOAD_VERDICT.public.json) binds the exact reviewed request and report hashes. It requires immediate live preflight, exact reviewed bytes, post-write verification and recomputation of actual dashboard counts.

The separately verified preceding batch was reported as **64 CLOSED / 263 TO RESEARCH**, among 327 records. These three transitions would produce **67 / 260** if there are no intervening changes. This package itself proves neither external application nor repository publication. Actual commit and workbook outcomes require separate verified receipts.

## Contents and integrity

- `sources/`: the pinned scientific reports and accepted historical outcome ledgers. The complete historical reports discuss other records; their inclusion grants no additional closure.
- `reviews/`: explicit public derivatives of the completed author, independent scientific and exact-payload reviews. No worksheet dumps, complete historical cell values or raw service responses are included.
- `checks/`: the newly independently authored small checker and its results, rerun during packaging.
- [REPRODUCTION.md](REPRODUCTION.md): dependencies, commands, control scope and source limitations.
- [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json): exact scientific input/export identities and source locations.
- [PUBLIC_PROVENANCE.json](PUBLIC_PROVENANCE.json): transformations and both hashes for every copied or derived input.
- `SOURCE_TO_GIT_PATH.json`, `FILE_MANIFEST.json`, `SHA256SUMS`: the source/publication map and whole-package integrity.

The tensor review is an explicitly named sanitized derivative removing four private Library identifiers. Its pinned input already carries historical sanitized-export/original-byte qualifications; neither this package nor its hash erases those distinctions or recovers missing original archives. Other unchanged scientific sources retain their exact bytes. Run `python -I -S verify_package.py` to verify the complete package.
