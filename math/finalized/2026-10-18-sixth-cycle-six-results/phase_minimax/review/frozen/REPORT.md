# PHASE-DEFECT-RANK C8 positive-error gate: exact upper witness, periodic-sector theorem, and remaining global inequality

18 October 2026 UTC.

## Result and status

The original unrestricted continuous-phase minimax is **still open**. This research attempt delivers:

1. A rigorous upper bound delta_1 <= sin(pi/16) = 0.1950903220161282678..., with explicit diagonal phases, an unrestricted real core B, and a complex rank-one E.
2. A matching exact lower theorem for all phases whose squares are four-periodic, including every real-sign variant. This entire continuous restricted sector has optimum sin(pi/16).
3. An exact real semialgebraic formulation of the unresolved nonperiodic-phase component. Proving it empty would establish the proposed global value; no emptiness certificate is claimed.

The sin(pi/16) value is therefore a **verified global upper bound and verified sector optimum**, not the proved global optimum requested by the gate. The accepted strict positivity statement is not being presented as the answer.

## Original scope retained

- Fourier matrix F[j,k]=exp(-pi*i*j*k/4)/sqrt(8), with zero-based indices.
- Operator norm, unrestricted real 8-by-8 B, complex rank(E)<=1.
- Arbitrary diagonal unitary outer phases; arbitrary invertible monomial magnitudes remain covered by the accepted real-core absorption argument.
- The accepted fixed-phase reduction min_{P,Q} sigma_3(Im(PFQ)) is retained.
- No new group, size, conditioning condition, finite phase grid, Green realization, or broad-owner closure is substituted.

## Explicit upper construction

Let z=exp(i*pi/16), c=cos(pi/16), and

q=(1,z^2,1,z^10,1,z^2,1,z^10), Q=diag(q), P=zQ, V=PFQ.

a=(1,0,-1,0,-1,0,1,0)^T/2,
b=(0,1,0,1,0,1,0,1)^T/2.

Set

E=c(a+i b)(a+i b)^T,
B=Re(V)-c(aa^T-bb^T).

E has rank exactly one and B is real. Using outer phases P*=P^{-1} and Q*=Q^{-1}, the original external error is exactly sin(pi/16). The imaginary singular values of V are cos(pi/16) twice and sin(pi/16) six times.

The proof, sector lower bound, and careful distinction from the global problem are in `PROOF.md`. `WITNESS.json` contains every matrix entry in a precise exact cyclotomic coefficient encoding.

## Why the periodic-sector lower bound is new work within this attempt

Real paired-index transforms split all squared-four-periodic phases into four unitary 2-by-2 blocks. Their two imaginary singular values have the form |sin(theta_cd±phi_cd)|. Six small singular values force two opposite blocks to be small in both directions. The opposite-pair scalar phase relation has discrepancy pi/4; the allowed angular deviations can absorb at most 4*arcsin(sigma_3). Therefore sigma_3>=sin(pi/16).

The proof includes both choices of opposite good blocks and explicitly handles real-sign changes. Its block identities are checked symbolically for arbitrary phases. This statement makes no historical novelty claim.

## The exact missing global step

The unresolved inequality is

sigma_3(Im(PFQ)) >= sin(pi/16) for every arbitrary diagonal unitary P,Q.

The earlier exact-rank proof forced squared-four-periodicity using equality in the Frobenius energy bound. That equality does not follow at positive error. In fact, this new witness has squared imaginary Frobenius norm 2+4 sin^2(pi/16), strictly greater than 2. Reusing the zero-error periodicity argument would leave a genuine gap.

`GLOBAL_PHASE_GAP.md` supplies a complete equivalent counterexample system over a specified real algebraic field: 78 real variables, 36 equality constraints, six strict leading-principal-minor inequalities, and one strict nonperiodicity guard. No continuous phase branch or sign is omitted. No algebraic elimination was completed for that system.

## Exact checks and negative controls

Fresh `exact_checker.py` uses exact rational arithmetic in Q[z]/(z^16+1). It checks:

- Negative-sign normalized F8 unitarity.
- The explicit paired-index orthogonal block transforms.
- Exact spectral identities Y^2=s^2 I+(c^2-s^2)(aa^T+bb^T) and Y_0^2=s^2(I-aa^T-bb^T).
- All 64 original external-residual identities, B realness, rank-one nonzeroness, and all 784 two-by-two minors of E.
- The algebraic error polynomial and a rational isolating interval.
- The pinned accepted-source Git blob identity.

Four deliberate mutations are rejected: reversed Fourier sign, one incorrect phase exponent, conjugating the rank-one vector, and an incorrect normalization. Results are in `EXACT_CHECKS.json`.

Fresh `general_block_checks.py` independently checks the arbitrary four-periodic 64-entry block decomposition, the centered 2-by-2 trace and determinant identities, and the semialgebraic imaginary-entry formula. Results are in `GENERAL_BLOCK_CHECKS.json`.

Neither program imports or executes any historical research package. The checkers support the stated proofs; they do not prove the missing global inequality.

## Numerical exploration, expressly non-certifying

Two fresh exploratory scripts were run to identify the witness. A smooth continuation search used all 15 independent continuous phase angles, a fixed random seed, and 100 starts. Eighty runs ended near 0.1950903309 and twenty near 0.3826834324. The small offset of the first value from sin(pi/16) is consistent with the final nonzero smoothing temperature. These are numerical outcomes, not certified local minima, exhaustive coverage, or a lower proof.

The final witness was then recovered in exact phases and verified independently of floating-point search. The numeric scripts and raw outputs are retained solely as reproducible discovery controls. No numerical optimizer result is used in the sector lower proof or in the exact error calculation.

## Controlling source and provenance

Read the complete publication derivative of the accepted C8 review at the pinned commit:

https://github.com/AgentSlop-Si/research/blob/c8843f101dcb400195b9a79b30e3803f1805f541/math/reviewed_rounds/2026-10-12-reviewed-research/phase-defect-c8.md

- Git blob: 11b2f499b004f62686a8584488e57022e970ebf2.
- Exact fetched derivative SHA-256: 123d15d9258166bb530553eaf74e0492f7ca117acc4d9ffafff66351d71bcd52.
- Original review SHA-256 recorded in that derivative: 5e157faa626093f4af5a9e3c1c377a7fee87ea74a2aa8b9b644a6188463984e1. This is not the derivative's hash and is not misrepresented as the bytes fetched here.
- Local frozen copy: `SOURCE_ACCEPTED_C8.md`.

The full controlling task was read from the parent-supplied six-gate plan. All work remained in this unique local packet. No external writes, publication, table edits, or owner/census changes were made.

## Review request and stopping condition

Please review the exact witness and the full continuous periodic-sector theorem at their stated scope. The permissible stopping result for the original gate is the precisely identified unresolved global inequality/semialgebraic component. Do not mark the original C8 positive-error minimax or its broader research owner closed.
