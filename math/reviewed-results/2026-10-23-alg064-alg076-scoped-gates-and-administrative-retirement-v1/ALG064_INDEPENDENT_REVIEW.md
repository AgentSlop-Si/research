# Independent mathematical review: ALG-064 noisy coefficient proposal

23 October 2026. Verdict: **SCOPED PASS**, with no requested author repair. ALG-064 remains **TO RESEARCH, priority 42**. This is a bounded certificate-producing exact-reference gate, not a new least-squares method, an improved general DFT algorithm, or a novelty determination.

## Exact accepted scope

For a raw complex dyadic vector of length N and declared span L in {1,2}, N>L, with rational absolute tolerance 0<epsilon<=1, accept the full-tail least-squares coefficient proposal when its lag matrix has full column rank. Accept its computed singular-value/condition certificate, the three stated conditioning-dependent perturbation inequalities, and its rounded full-tail residual certificate. Rank or residual refusal is not a nonmembership result. The proposed full DFT guarantee is a **mathematical composition with the previously accepted evaluator and paid node/fallback contracts**, not an executed or production-integrated backend.

Acceptance certifies the transform of the **observed** vector. The clean recurrence/noise-ball premise is external, is not inferred from a small residual, and may describe an empty class. The map-stability inequality itself needs no clean-model premise. No trajectory reconstruction, denoising, minimal-order identification, uniform condition bound, broad fixed noise floor, ordinary floating-point implementation, non-dyadic acquisition, normalized real-residual adapter, practical speed, or parent closure is accepted.

The candidate report is SHA-256 `12ce3f5754f8a39439d4a2bbd087e46d9253a07da79d249c98565309a6933f68`. Exact manifest and member/source bindings are recorded in `VERDICT.json` and `BINDINGS.json`. No candidate or historical research program was executed or imported for this review.

## Independent proof reconstruction

### Full-tail fit and measured conditioning

Writing A=A_x, b=b_x and c=-(A* A)^(-1)A*b, the residual r=b+Ac has A*r=0. Expanding the squared norm of r+A(d-c) proves the claimed Pythagorean identity and unique least-squares optimality. Both conjugations and every tail row are essential. L=2 with N<4 cannot have full column rank; rank refusal handles that case correctly.

For two positive Gram eigenvalues a<=b, ab/(a+b) lies in [a/2,a]. The exact dyadic bracket s^2<=gamma<4s^2 therefore implies A*A>=s^2 I, while trace(G) bounds the largest eigenvalue. The reported condition-squared upper bound trace(G)/s^2 follows. For L=1 the scalar Gram value is exact. Computing the bracket requires integer comparisons only. There is no hidden spectral-gap input, approximate eigenvalue test, or root extraction.

### All-size perturbation bounds

For x=y+e, each lag column is a truncation/shift of e, so ||A_x-A_y||_F<=sqrt(L)||e||_2 and the target difference has norm at most ||e||_2. If b_y+A_y c_star=0, applying A_x^+ to the observed normal-equation solution gives exactly

    c-c_star = -A_x^+[(b_x-b_y)+(A_x-A_y)c_star].

Its norm yields equation (1). Substituting ||c_star||<=||c||+||c-c_star|| and moving the last term to the left proves equation (2) under sqrt(L)eta/s<1. The reference's L eta/s<1 guard and componentwise l1 coefficient magnitudes are conservative rational replacements, not estimates of the unknown noise level.

For a second full-rank observation A'=A+DeltaA, b'=b+Deltab, put f=Deltab+DeltaA c. Then c'-c=-(A')^+(r+f). Orthogonality gives (A')*r=(DeltaA)*r. Thus the r term is at most ||DeltaA|| ||r||/(s')^2 and the f term at most ||f||/s', proving equation (3). Merely bounding (A')^+r by ||r||/s' would lose the useful perturbation factor; the report retains it correctly.

Least-squares optimality at the true coefficients gives ||r||_2<=eta(1+sqrt(L)||c_star||_2). Since the sum of real/imaginary absolute values is at most sqrt(2m)||r||_2, equations (5)-(6) follow. Weyl's lower singular-value bound supplies the separate sufficient observed-rank premise. At L=2 this sufficient noise class is only of order epsilon N^(-5/2) for bounded coefficients. This is explicitly not a macroscopic-noise recovery theorem.

The multiplier-2 example correctly shows that a single tiny defect can generate an exponentially larger terminal trajectory discrepancy. It prevents interpreting the residual certificate as a uniform reconstruction theorem.

### Rounded actual-data interface

Nearest rounding of each real/imaginary coefficient component to grid h changes its complex l1 magnitude by at most h. Submultiplicativity and summation of all shifted input magnitudes give

    R <= R0 + sum_i nu(Delta c_i) sum_(j=L)^(N-1) nu(x_(j-i))
      <= R0 + L h S <= R0 + epsilon tau/16.

Consequently R0<=epsilon tau/16 is sufficient, while the actual gate R<=epsilon tau/8 is sound and may accept more inputs. The implementation recomputes R over the whole tail. The additional coefficient Euclidean error is at most sqrt(L)h.

Direct coefficient comparison proves C(T)X(T)=P(T)+E(T)+T^N B(T), with A_boundary=P+B. This remains valid when the rounded degree r is less than the declared span L, including r=0. At an Nth root it is the precise inherited identity C X=A_boundary+E. The conservative tau=(2N)^(-L) is no larger than the degree-r threshold, so the accepted suspect-bin argument still gives at most r suspect bins. The retained span, original raw dyadics, boundary coefficients, entire residual, actual coefficient/boundary magnitudes, and p>=2b_c supply the predecessor's stated finite-word interface. No denominator lower bound is assumed independently of its certified classifier. Output remains the unnormalized positive-exponent DFT.

## Bit and setup ledger

After raw-grid alignment, integer Gram and right-hand-side entries have O(B+log(N+1)) bits, up to fixed factors from products. Since L<=2, determinant and adjugate numerators have the same asymptotic width. The common raw denominator cancels from the coefficients, but not from the conditioning certificate; the report correctly includes b in later widths. A tiny nonzero determinant costs its actual bit length, not a free inverse.

All coefficient denominators divide a fixed determinant-derived denominator of O(H) bits. Full residual summation therefore stays on a common denominator of O(H+b) bits; it does not introduce an uncharged product of N unrelated denominators. Fixed L likewise bounds the boundary-construction width. Rounding, exact square comparisons, tolerance representation, dyadic bracketing and grid selection fit the stated conservative W. Each elementary rational reduction/division/comparison is included in A(W), and loop counts W+b_c are charged. The resulting discovery cost O(E+(N+b_c+W)A(W)) and O(NW) materialized storage are valid conservative upper bounds.

A successful mathematical composition must add the predecessor's rational-node construction, its actual H_root operand width, all precision inequalities, O(N) fixed-L evaluator arithmetic at its own width, exact classification/division and all output writes. A failed proposal retains its discovery invoice before a paid certified fallback. Neither O(N) arithmetic for fixed L nor an O(N log N) fallback kernel means linear or quasilinear **total bit time** here. The new program stops at the coefficient/certificate interface and does not implement that integration.

## Fresh independent controls and implementation inspection

`control.py` is newly written reviewer code using only the standard library. It forms a real 2L-dimensional normal system and performs rational elimination, independently of the candidate's explicit complex 2-by-2 inverse. No candidate or historical scientific code is imported or executed. The new candidate source was inspected for conjugation, lag indexing, inverse signs, rounding, boundary formation and status semantics; those agree with the reconstructed mathematics. The reviewer controls are not a claim to have executed the candidate implementation or a DFT backend.

Normal and Python -O runs are byte-identical: **2,655 active checks over 180 fixtures**. There are 90 accepted coefficient packets, including 58 nonzero-residual packets; 73 residual refusals; 17 rank refusals; 87 clean-model and observable-conditional checks; and 54 proposal-map perturbation checks. Coverage includes N=2,3,4,5,9,17,32, both spans, complex data, repeated-root recurrence fixtures, dyadic noise, 300-bit near-rank-one inputs, full polynomial convolution identities and exact rational unit-node interfaces. Mutations reject prefix-only fitting, missing conjugation, coarse rounding and a false conditioning bound. A rank-deficient exact recurrence and a degree-zero connection at declared span two guard against incorrect refusal and span interpretations. The unstable trajectory countercontrol is explicit. The finite tests support transcription; the all-size guarantees come from the proof above.

All 11 public/source manifest members were hash/length checked, and all six source captures have matching SHA-256 and recorded Git blob identities. This is a selected dependency binding, not a broad repository/history audit.

## Baseline and attribution boundary

The new delta is the all-tail noisy-data proposal, computed conditioning certificate and its conditional stability/rounded-residual interface. The residual-aware evaluator (`source_1.md`, Sections 2-6), exact-data coefficient/node bridge (`source_2.md`, Sections 3-6), certified FFT fallback (`source_3.md` plus its independent review), and original Phase23/audit scopes were read as selected pinned dependencies. Their completed claims are inherited, not recounted as new work.

The primary LAPACK Users' Guide's [linear least-squares page](https://netlib.org/lapack/lug/node27.html), independently read on 23 October, confirms the classical full-rank QR/LQ and rank-deficient orthogonal-factorization/SVD context. The present normal-equation identities and perturbation proof do not establish a floating-point QR, SVD or normal-equation implementation. No broad attribution clearance was attempted.

**Disposition:** accept this bounded exact-reference gate and preserve all explicit open production, broad-noise, acquisition, integration, architecture and novelty obligations. Do not redispatch this exact certificate proposal as an unfilled oracle; do not close ALG-064.
