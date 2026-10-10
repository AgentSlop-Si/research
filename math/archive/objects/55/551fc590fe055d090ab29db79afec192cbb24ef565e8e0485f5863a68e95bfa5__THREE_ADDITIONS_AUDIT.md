# Three new Fourier research additions: audited supplement

9 October 2026. This supplements the completed research corpus with the algebraic jet gate, global-chirp median v7, and Phase 15 folding checkpoint.

## Executive result

All three central developments survive independent audit, with their models kept distinct:

1. **Algebraic jet gate:** a valid 30-equation, 26-variable regular-patch feasibility reduction, and a separately certified pointwise second-order obstruction. Neither excludes Fourier from the whole architecture.
2. **Global-chirp median v7:** a valid approximate full-output transform theorem. It provides linear or sub-N-log-N arithmetic at a specified energy-relative error, for every fixed input with high probability. It is not an exact arbitrary-input transform or a floating-point accuracy guarantee.
3. **Phase 15:** an exact, reversible linear-work folding factor compresses residual execution. The complete constructed transform still uses exactly N log₂N/2 radix-2 butterflies.

No uploaded Python was executed or imported. Independent proofs, newly authored checks, source hash verification, and source-reported claims are distinguished throughout the detailed audits.

## 1. Algebraic feasibility and curvature

Read `algebraic/ALGEBRAIC_JET_INDEPENDENT_AUDIT.md` and `source_material/algebraic/PROOF_CERTIFICATE.md`.

The new F8 reduction eliminates the second stage on a specified regular chart. With det(PA), the normalization factors, and both reconstructed corner anchors nonzero, its 30 anchored minors are necessary and sufficient for the second stage to have the required global separated generators. The diagonal gauge leaves 26 first-stage coordinates. The system has not been solved or certified infeasible.

The local curvature certificate is exact: the Jacobian has characteristic-zero rank 60 and appending vec(E_(0,7)) raises rank to 61, certified by a 61-by-61 integer minor with determinant 6,913 modulo 12,289. All 20 gauge directions are independent and exhaust the kernel; the projected Hessian is independent of the choice of first-order lift. The obstruction concerns an ordinary parameter curve through that particular stored point, not all representations of Fourier.

The audit adds a concrete warning about exceptional patches: the invertible matrix I+E_(2,1)+E_(4,3) satisfies all the anchored equations with zero anchors but has no global lower-separated rank-one factorization. A polynomial infeasibility argument must handle saturation and missing patches explicitly.

Classical Cooley–Tukey controls have stage orders (1,1) at N=8 and N=16, but (4,1) at N=32. They clarify the difference between this finite separated-generator chart and the broader quasiseparable class. They use their own permutations and do not solve the fixed F8 chart problem.

Independent evidence includes exact reconstruction/mutation tests in two prime fields, the 6,913 minor, all 1,600 gauge-Hessian conormal pairings, and the CT entry identities.

## 2. Global-chirp median approximation

Read `chirp/V7_DIRECT_AUDIT.md` and `source_material/chirp/RESEARCH.md`.

For dyadic N=KM, M≥2, K≥2M, with independent uniform odd quadratic coefficient and uniform linear coefficient, one randomized row is unbiased and is decoded in O(N+K log K) scalar arithmetic. The per-output covariance norm is exactly 2M/N.

The audit sharpens the supplied bound to an exact spectral identity:

`Q_m=(2M/N)P_m`, where P_m is an orthogonal projector of rank K(M−1)/2.

All nonzero covariance eigenvalues therefore coincide. The large total one-row error, (M−1)||x||₂², is consistent with small variance at each individual output. It does not refute output-domain median amplification.

For R=2s−1 independent rows and C_s=binom(2s−1,s), the componentwise complex median satisfies, simultaneously over all outputs for each fixed seed-independent input x,

`||X̃−U_Nx||∞ ≤ 2(2NC_s/δ)^(1/(2s)) √(M/N)||x||₂`

with probability at least 1−δ, 0<δ<1. With dyadic M=Θ(log N), fixed s≥2, and fixed δ, this gives O(N) time/storage and error O(√log N · N^(−1/2+1/(2s))||x||₂). A sufficiently large R=Θ(log N/log log N) gives the claimed sub-N-log-N arithmetic regime with polylogarithmic loss over ||x||₂/√N.

The detailed audit supplies explicit nonvacuous parameters and qualifications:

- Use δ=min(1/2,N^(−a)), rather than δ=1 when a=0.
- State a sufficiently large row-count constant for a requested error exponent.
- Charge comparisons and use linear-time median selection, not sorting.
- The straightforward growing-row exact-median implementation stores O(RN) values.
- The input is fixed before the seeds. A single rank-deficient sketch is not promised to work uniformly for all later-chosen inputs.
- Exact scalar arithmetic, root preparation, and finite-precision stability are separate issues. No practical superiority or literature-wide priority is established.

Independent evidence includes 800 exhaustive seed states, 15 exact modular recurrence cases, seven complete covariance spectra through N=512, and 81,380 exact median-inequality cases, together with proofs of the general statements.

## 3. Phase 15 folding and the new entropy consequence

Read `phase15/PHASE15_INDEPENDENT_AUDIT.md` and `source_material/phase15/THEOREM.md`.

In the Phase 14 single-mask regime N=BL≤B², the residual factors as

`A=R(I_L⊗F_B)P_in`.

The folding map R and its inverse use exactly (N−B)/2 radix-2 butterflies plus O(N) gathers and phases. This supplies an O(N log B) residual executor, improving on naive sparse multiplication. Its row Gram is diag(L/d_e), so the row-normalized R̂ is unitary. Its sparse matrix has N+(N/2)log₂L nonzeros despite its O(N) shared-computation executor.

The complete network conserves classical work:

`C_base+C_fold+C_orbit=N log₂N/2`.

Combining Phase 15 with the earlier entropy audit gives a sharper model-qualified statement. The three normalized factors have entropies

- Base Fourier bank: N log₂B bits
- Folding: N−B bits
- Orbit Fourier bank: N log₂L−N+B bits

Each is exactly twice its constructed butterfly count. A two-coordinate unitary gate can increase matrix entropy by at most two bits; the complete circuit therefore saturates the N log₂N/2 lower bound in that gate model. Cross-bank fusion that remains entirely in two-coordinate unitary gates cannot reduce the count. This is not a general arithmetic-circuit lower bound.

The separate pure inverse-sparse obstruction also holds: if inverse stages have respective row sparsities s_j, separated by arbitrary monomial factors, then ∏s_j≥N. Dense inverses or sums of resolvents are outside this hypothesis. Sparse inverse matrices do not by themselves guarantee cheap solves.

Independent evidence includes exact modular full factorization and inverse through N=4096, direct residual comparisons through N=1024, and complex Gram/support/entropy checks through N=256.

## 4. What is actually new in the files

Recursive inspection found 417 archive-member occurrences containing 245 distinct byte contents. Against the completed canonical sources, archive-member catalog, Library-level archive hashes, and prior fusion files, 367 occurrences were already known. There are **50 new unique file contents**:

- Algebraic jet archive: 25 new files, 85 inherited occurrences
- Global-chirp v7 archive: 6 new files
- Phase 15 archive and embedded history: 19 new files, 282 inherited occurrences

These counts include code, data, documentation, and manifests. They are not counts of new theorems. Repeated ancestry is not independent corroboration. All 135 entries in the three supplied top-level checksum manifests matched the bytes.

Original archive SHA-256 values:

- fft_algebraic_jet_gate_2026-10-09(1).zip: 4c7e1817b85a0c0d99bfff9c82763803943c81ce979ce3033b248af77a6841bf
- fft_global_chirp_median_v7(1).zip: 48a0d1f29660dfe017557e81325ba28d6457ad1512d36376499116b7237afdec
- fft_green_research_phase15_2026-10-09(1).zip: 027854e8133c6f8aeb256ecf51306bb2a63eb1fbadad42cd723b07fb9c6dfbff

## 5. Decisive next gates

- **Exact algebraic route:** solve the saturated F8 patch system exactly, or prove that patch infeasible and then cover the exceptional patches. Equation counts and optimizer failures are insufficient.
- **Approximate chirp route:** establish finite-precision stability and a full precision/phase-preparation budget. Improving robust aggregation memory is a separate algorithmic opportunity.
- **Exact folding route:** a cross-bank construction must jointly replace the expensive Fourier banks and explicitly leave whichever restricted gate/Green model caused the lower bound. Reducing the already-linear folding factor cannot establish the desired asymptotic improvement.

## 6. Additional synthesis: linear-space robust aggregation

Read `chirp_audit/STREAMING_ROBUST_SYNTHESIS.md`. A new, self-contained five-representative streaming selector replaces the exact median with a different robust output estimator. It uses only arithmetic, comparisons, and indexed access, with constant storage per real output coordinate.

The deterministic lemma is: if fewer than R/4 samples lie outside [μ−B,μ+B], the largest surviving counter represents a value within 3B of μ. The proof explicitly handles nontransitive near-matching; a naive one-counter replacement fails on a supplied seven-value counterexample.

With R=4s−1 independent chirp rows, A_s=binom(4s−1,s), and a certified variance threshold, the simultaneous complex error is

`||X_stream−U_Nx||∞ ≤ 6(2NA_s/δ)^(1/(2s)) √(M/N)||x||₂`.

The displayed constant 6 uses the ideal threshold; its arithmetic-only power-of-two rounding gives constant at most 12. The selector uses O(N) registers even in the growing-row regime, while retaining O(R[N+K log K]) work. Its error exponents and strict sub-N-log-N time regime match v7 up to constants. Root-power tables and a comparison-only threshold schedule are explicitly charged; no floor oracle or exact real-power primitive is hidden.

Independent exact-integer checks cover 597,870 exhaustive short words, 720 designed permutations, 48,000 randomized order/tie cases, and 360 bad-first/bad-last constructions. The proof, not those finite checks, establishes the general bound. No end-to-end streaming chirp implementation, floating-point stability result, or literature-wide novelty claim is supplied.

This closes the straightforward median implementation’s O(RN) storage gap for a modified estimator. It does not make the underlying approximate transform exact: the growing-row measurement count is still deficient for generic exact recovery of arbitrary complex inputs, even when the norm scalar used by the selector is provided.

The three branches and this synthesis are compatible advances, but their combination does not currently give an exact faster-than-N-log-N Fourier algorithm.
