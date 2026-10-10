# Verified checkpoint addition through 18:07 UTC

9 October 2026. This addition can be merged into the authoritative master through 17:17 without waiting for the separate 17:42 mathematical supplement, which remains pending unless independently finalized. All paths here are relative to this 18:07 supplement. No exact arbitrary-fresh-input, all-output sub-N-log-N evaluator has been established.

## New exact structural facts

- Phase22's real one-mask connected-Gram obstruction is sound. A stronger exact characterization is available: for real invertible A, existence of real invertible B and one nonzero complex diagonal Q in F=A Q P B is equivalent to J A=A E for a diagonal reflection-parity matrix E with entries ±1. This characterizes the left factor when the right factor is free, not a specified pair or a fast evaluator. Positive real left Green sums fail it.
- The bilinear finite-field Gram screen is necessary for fixed A,B and every middle Q,P. The 24 sample vetoes and 12 deliberately valid recoveries are independently reproduced. Zero-diagonal/collision branches remain inconclusive; Gram equality and one calibrated entry are insufficient for Fourier equality.
- F=H Q C is an exact cheap parity/axis extraction with C a real orthogonal cosine/sine residual. C still requires at least N(log2 N-1)/2 two-coordinate unitary gates in that restricted model. The sparse covariance and full first column uniquely specify the linear C, but do not evaluate Cx cheaply.
- The finite-field covariance test requires a fixed deterministic linear oracle and independent uniform challenges. It uses one seed call plus two calls per challenge. The uploaded apply_R repeats modular exponentiation, so its advertised linear overhead is not met as written; an independently specified consecutive-power recurrence repairs the coefficient/application count. Root/field setup and precision remain separate costs.
- The all-length tail-rank theorem gives min(t,N-1-max(pi[-t:])) <= r_lower(C)+r_upper(B), with a mirror prefix inequality. It covers general quasiseparable ranks in the fixed endpoint order. The unchanged tail (1,2,5) is excluded for every N>=9 with two rank-one stages, but N=8 remains open.
- For a constant rank sum s, every suffix/prefix inequality reduces exactly to the corresponding first/last s+1 boundary test. At s=2, 28,584 of 40,320 N=8 permutations pass. A closed-form count and the disjoint-boundary uniform-permutation bound P(pass)<= (s+1)^4/[N(N-1)] are proved. Passing is only necessary.
- The inherited 11-by-9 rank gate has no independent extra maximal minors: 45 vanish identically and the remaining 10 are constant multiples of Dhat=-DB DH. All 55 were independently reconstructed. Rank<=8 is exactly DB DH=0 within this rescaled polynomial family; original feasibility equations and all exceptional branches remain required.
- DB's homogenized coefficient matrix has exact rank four, with the nonzero 11251 modulo 12289 witness reproduced, so the quadric is absolutely irreducible in characteristic zero. Its unique affine singular point has h0=h1=0, so it is smooth on the inherited regular h0!=0 chart. Its zero locus is not excluded.
- The six-column auxiliary boundary gate has rank 4+rank([[U3,-L3],[U4,-L4]]) for N>=9. Its leading determinant is -(U3 L4-U4 L3) times the six-node Vandermonde. N=8 remains a genuine rank-deficient exception. The report supplies the direct proof absent from the source's referenced proof file.

Reports and reproducible evidence: `TWO_LATEST_AUDIT.md`, `phase22_audit/`, `bilateral_audit/`, `tail_screen_extension/`.

## Provenance

Two new outer source archives; 691 recursive member occurrences; 507 distinct contents; 34 byte-new text/data/source-program contents against the declared source union through 17:42. All 833 embedded checksum entries pass. The embedded Phase21 and triple-intersection archives exactly match prior sources. No uploaded executable, source program or bytecode was run. The supplementary archive contains full inert sources, source identities, explicit hash comparison data and independently authored checks.

No unrestricted lower bound, new exact transform or novelty claim follows from these results. The earlier verified exact residual systems, exception coverage and model limitations remain in force. The 17:42 Prony, cycle-crossing and fused-summary additions keep their separate pending/completed status; their source hashes are used here only for deduplication, and this audit does not promote them automatically.
