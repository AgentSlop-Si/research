# Fourier Gram and two-sided tail-rank audit

Independent synthesis of the two archives received at 18:07 UTC on 9 October 2026. These add useful exact structural restrictions and certification tools to the authoritative master through 17:17. The separate 17:42 mathematical supplement is still pending final sealing and is not promoted to completed status here. They do not establish a fully charged exact transform of arbitrary fresh inputs with all outputs below N log N.

## Source changes

The new sources are Phase22 Gram/parity research and the bilateral Fourier-tail-rank archive. The latter's external filename says `fft_fourier_tail_rank_gate_2026-10-09(1).zip`, while its internal root is `fft_bilateral_gate_2026-10-09`. Content was compared by SHA-256, not filename. Their embedded Phase21 and triple-intersection checkpoints are identical to previously supplied source bytes. The triple-intersection mathematics already verified through 17:17 carries forward. Phase21 source identity was verified at 17:42; that byte match does not itself complete the separate pending Phase21/v11 mathematical supplement.

The pair contains 691 recursive member occurrences, 507 distinct member contents and 34 byte-new contents relative to the declared source union through 17:42. All new contents are text/data/source-program files, with no new nested archive or bytecode content. All 833 embedded checksum entries pass, and extracted bytes match their containing archives. Uploaded programs, binaries and bytecode were never executed. See `SOURCE_PROVENANCE.md` and its JSON records.

## Phase22 real one-mask structure

The source's connected-Gram obstruction is correct for a factorization F=A Q P B in which A and B are real invertible, Q is one nonzero complex diagonal and P is any permutation. The real and imaginary Fourier ranks force Q onto real or purely imaginary axes. Orthogonality then forces the corresponding cross block of A^T A to vanish. A strictly positive real left mixer is excluded, including the specified positive cyclic Green sums under independent coordinate orders.

An immediate exact sharpening identifies the entire left-mixer condition. For the source’s even N>=4 setting, let J reverse coordinates modulo N. Because conjugate(F)=J F, conjugating the factorization and cancelling F gives

    J A = A E,    E = diag(conjugate(q_i)/q_i) in {+1,-1}^N.

Every column of A must have definite reflection parity. Conversely, for a real invertible A with this property, choosing q_i on the appropriate real/imaginary axes makes Q^-1 A^-1 F real, giving some real invertible right factor. This is a necessary-and-sufficient condition on A when the right factor is free. It does not certify a specified B, make the resulting B cheap, or exclude architectures with complex mixers or multiple complex masks. The disconnected Gram graph is therefore a weaker consequence of the complete parity condition.

## Bilinear screening and the real covariance gate

The bilinear Gram identity is valid over the stated odd-characteristic field with the required roots and normalization:

    B^-T J B^-1 = P^T Q (A^T A) Q P.

Pairwise squared-entry invariants provide an exact necessary screen for fixed A and B against every middle diagonal/permutation. Distinct row fingerprints can determine the only candidate permutation; full rank-one ratio and square-root checks recover its diagonal up to sign under the stated nonzero-entry hypotheses. Repeated fingerprints and zero-diagonal cases need the report's inconclusive branches. Finite-field exclusions of sampled A,B pairs are not a universal real/complex Green-sum theorem. Materializing and inverting the dense matrices costs cubic arithmetic in the supplied diagnostic. The source also conflates basis-call and scalar costs: reconstructing one matrix takes N basis-vector oracle calls, which cost O(N²) scalar work for a linear-work oracle, before the separate dense diagnostic work.

Gram equality and a single entry calibration do not certify Fourier equality. The exact counterexample S F, with a nonconstant diagonal sign matrix S and S_00=1, also passes the first Weyl equation but fails the second. It must remain a negative control.

The exact parity factorization F=H Q C is correct: H is a linear-work reflection-pair change of basis, Q is a simple axis mask, and C is a real orthogonal cosine/sine matrix. Its entropy remains at least N(log2 N-1), yielding at least N(log2 N-1)/2 two-coordinate unitary gates in that circuit model. This is not a lower bound on arbitrary nonunitary Green arithmetic.

The equations C Z=R C and C e0=v, with sparse rotation R and explicit v, uniquely identify the linear matrix C. A fixed deterministic linear oracle can be checked by a seed call and two oracle calls per independently uniform finite-field trial. Over F_p, if the seed column matches and the covariance residual has rank rho, t independent challenges pass with exact probability p^(-t rho); a wrong seed is rejected deterministically. Fixed test seeds are regression controls; the gate does not prove linearity or protect against an adaptive test-aware oracle.

There is a concrete source implementation gap: `apply_R` recomputes root powers independently in its loop, so its additional field-arithmetic work is O(N log N) as written, rather than the advertised O(N). Preparing consecutive root powers by recurrence, together with their inverses, repairs the mathematical O(N) coefficient/application bound. Root discovery, square roots, the candidate oracle, storage and precision are still separate charged costs. The sparse intertwiner is a correctness constraint, not a cheap evaluator of Cx.

Full proof qualifications, reconstruction controls and the small repair are in `phase22_audit/`.

## The two-sided all-length tail-rank obstruction

For B[:,j]=(F_N C)[:,pi[j]] with C invertible, let the final t output columns correspond to J={pi[N-t],...,pi[N-1]}, and put ell=N-1-max(J). Then

    min(t,ell) <= r_lower(C) + r_upper(B).

The mirror prefix inequality is

    min(t,min(pi[:t])) <= r_upper(C) + r_lower(B).

The proof combines rank-nullity with the full Vandermonde rank of consecutive Fourier-character restrictions. It holds over the complex numbers, and over fields of characteristic not dividing N with a primitive Nth root, for general quasiseparable rank bounds. It does not need the more restrictive globally separated generator chart, conditioning assumptions or nonzero generators.

For the fixed last-three-column shuffle (1,2,5), the necessary rank sum is min(3,N-6). Two rank-one stages are therefore excluded for every N>=9. The bound permits N=8; it neither constructs a factorization there nor applies unchanged after arbitrary endpoint reorderings.

For a constant rank sum s, the entire suffix family is equivalent to its t=s+1 instance; the prefix family has the analogous reduction. Thus only the first and last s+1 entries need inspection. At s=2 the two three-entry boundary tests reproduce exactly 28,584 survivors among all 40,320 eight-point permutations. An independent closed-form inclusion-exclusion count and probability bound are supplied in `tail_screen_extension/TAIL_SCREEN_SHORTCUT.md`. Passing this inexpensive necessary test remains far from a Fourier construction.

## The old 11-by-9 gate is exhausted

The independent symbolic reconstruction confirms the uploaded collapse in the inherited rescaled polynomial family. All six columns of the first block lie in one fixed three-dimensional Fourier subspace. Of the 55 maximal 9-by-9 minors, exactly 45 vanish identically and the remaining 10 are nonzero constant multiples of the previously selected polynomial Dhat=-DB DH. Consequently the old matrix has rank at most eight exactly on DB DH=0 within that polynomial family.

This means computing more maximal minors of that same gate cannot provide another independent exclusion. It does not settle the full F8 Fourier feasibility system. Exceptional polynomial points may fail to correspond to normalized valid stages, so the original equations, saturation conditions and zero-generator branches must remain intact.

The homogeneous symmetric coefficient matrix for the quadratic DB has exact rank four. Its stated 4-by-4 minor is 11251 modulo 12289 at zeta8=8246. In characteristic zero, a product of two linear forms would have symmetric matrix rank at most two; DB is therefore absolutely irreducible. Irreducibility does not make DB=0 empty or justify discarding that branch. The exact matrix also has a unique affine singular point with h0=h1=0, so the quadric is smooth on the inherited h0!=0 chart; this does not remove any regular points.

The auxiliary boundary-lock statement also has a direct proof, replacing the source's reference to a missing proof file. For N>=9 the six-column Fourier coefficient matrix has rank

    4 + rank([[U3,-L3],[U4,-L4]]),

and its leading six-row determinant is minus (U3 L4-U4 L3) times the six-node Vandermonde determinant. Thus rank at most five is exactly the displayed boundary matching equation. N=8 genuinely has too few rows and admits rank five with nonzero boundary determinant; that exception is preserved.

Exact symbolic certificates and independent finite-field controls are in `bilateral_audit/`.

## What this changes for the exact objective

The new gates make the search more selective. Real one-mask candidates must already align with Fourier reflection parity. Constant-rank two-stage candidates can be rejected using just two boundary checks. The old 11-by-9 minor search yields only its existing product equation and should not be mistaken for an inexhaustible source of new constraints.

These facts leave the separate pending 17:42 common-order/Prony and fused-approximation work at its existing status. A comparison against its source hashes is not a mathematical completion claim. None of the newly verified facts turns a representation into a fully charged fast evaluator. The unresolved target still needs a scalable exact identity for arbitrary input, every output, all required branches, and a shared evaluator whose preprocessing, coefficients, output work, workspace and chosen scalar/bit model genuinely meet the claimed complexity. Dense diagnostic inversions, a cheap covariance test and finite valid examples do not supply that evaluator.

Primary attribution for the classical Gram/entropy ingredients is recorded in `PRIMARY_REFERENCES.md`. No mathematical novelty or publication-priority claim is made.
