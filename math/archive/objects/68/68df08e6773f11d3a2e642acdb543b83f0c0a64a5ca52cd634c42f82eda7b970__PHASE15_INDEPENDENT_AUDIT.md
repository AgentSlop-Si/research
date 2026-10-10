# Phase 15: independent audit and entropy saturation

9 October 2026. Scope: the supplied Phase 15 theorem and its delta from the already audited Phase 14 factorization. No uploaded executable was imported or run. The accompanying independently authored checker passed all cases reported below.

## Result

The exact residual-folding identities, inverse, scaled unitarity, butterfly conservation, and pure inverse-sparse product obstruction are correct in their stated models. Phase 15 supplies a real execution improvement for the residual compared with applying its sparse matrix directly. It does not improve the asymptotic complexity of the full transform.

A useful sharpening follows by combining Phase 15 with the earlier entropy audit: the normalized folding factor has exactly **N−B bits of matrix entropy** and uses exactly **(N−B)/2 balanced two-coordinate gates**. The complete three-bank circuit saturates the **N log₂N/2** entropy lower bound for arbitrary two-coordinate unitary gates. Therefore cross-bank fusion restricted to this gate model cannot lower the butterfly count at all. This is not a lower bound for unrestricted arithmetic circuits, nonunitary intermediate computations, or dense structured global gates charged by their own executors.

## Source and assumptions

Primary supplied text: `../source_material/phase15/THEOREM.md`, especially §§1–6. The prior audit is `../prior_audits/PHASE14_AUDIT_AND_FUSION.md`.

Throughout, N=BL, with N,B,L powers of two, 8≤B<N≤B², and F_N[k,j]=ζ_N^(kj) unnormalized with positive exponent. Thus L≤B. The finite-field checks use 998244353 and a primitive dyadic root. They confirm exact finite-field evaluations, while the mathematical argument establishes the complex identity. They do not establish floating-point performance, stability, or novelty relative to published literature. External publication claims in the supplied README were not needed or independently assessed.

## 1. Geometry and extraction

Because B² is divisible by N, (1+B)^t≡1+tB modulo N. A frequency k has orbit length d=L/gcd(k,L). Writing g=L/d, its least orbit representative k₀ lies in [0,Bg), so k₀=gu with 0≤u<B. When d>1, u is odd. This supplies the representative facts used in the new theorem.

For each orbit character e∈{0,…,d−1}, solve ua≡e modulo d with 0≤a<d, and set c=(ua−e)/d. The phase-14 residual row contributes exactly at j=a+dh. Its coefficient is ζ_B^(c+uh). Splitting h modulo B gives

`(Ax)[orbit,e] = ζ_B^c Y[d,a,u]`.

For d=1, a=0 and c=0; all B frequency coordinates at that level are selected. For each d>1, the B/2 odd u values and all d residues a occur exactly once. Consequently the extraction takes every odd-frequency coordinate at every nontrivial level and the complete final spectrum, without duplication. This is what makes the inverse valid.

## 2. Folding and inverse

Splitting the lower-level stream into even and odd h, then splitting the original summation index into its two halves, gives

`Y[d/2,a,q] = Y[d,a,2q] + ζ_B^q Y[d,a+d/2,2q]`,

`Y[d/2,a,q+B/2] = Y[d,a,2q] − ζ_B^q Y[d,a+d/2,2q]`.

The untouched odd-frequency coordinates become outputs at level d. The even-frequency pair is recovered by reversing this butterfly. Hence the folding map R is invertible with the same number of butterflies forward and backward:

`Σ_(d=L,L/2,…,2) dB/4 = (N−B)/2`.

The complete residual is A=R(I_L⊗F_B)P_in, so its execution costs O(N log B), plus O(N) folding, phases, and gathers. This replaces the sparse residual’s N[B+(B/2)log₂L] scalar nonzeros with shared computations. It does not replace the B-point Fourier bank.

## 3. Exact Gram and condition identities

Writing the phase-14 factorization as F_N=U_orbit Q A with unnormalized orbit DFT blocks, their Gram is diag(d_e). Therefore

`AA* = diag(N/d_e)` and `RR* = diag(L/d_e)`.

The normalized folding factor R̂=diag(√(d_e/L))R is unitary. Every row has g=L/d_e nonzeros of unit magnitude before normalization, so its nonzero probabilities after normalization are all 1/g.

The singular values of R are √(L/d_e). Both d=1 and d=L occur; therefore its exact 2-norm condition number is √L. A has the same condition number. The diagonal normalization removes this conditioning in R̂; exact unitarity alone is not a complete floating-point error analysis of a particular program.

The support count is

`nnz(R)=N+(N/2)log₂L`.

This is a precise example of graph sharing: a matrix with Θ(N log L) nonzeros has an O(N)-work exact executor. It is a wavelet-like factor, not the full Fourier matrix.

## 4. New fusion consequence: exact entropy saturation

For a unitary matrix T define the base-two matrix entropy

`Φ(T)=−Σ_ij |T_ij|² log₂ |T_ij|²`.

Let h=log₂L. The orbit histogram consists of B fixed points and B/2 cycles of every length 2^t, 1≤t≤h. Hence

`Φ(R̂) = Bh + (B/2)Σ_(t=1)^h 2^t(h−t) = N−B`.

The other normalized banks have

`Φ(I_L⊗F̂_B)=N log₂B`,

`Φ(Û_orbit)=N(log₂L−1)+B`.

These three numbers sum to N log₂N, exactly the entropy of F̂_N. The already audited normalized residual has entropy N log₂B+N−B, consistent with the same decomposition. Entropy is not generally additive under matrix multiplication; these are explicit identities proved from the support distributions of these particular factors.

Their constructed gate counts are exactly half of the corresponding entropy values:

- Base bank: (N/2)log₂B
- Folding: (N−B)/2
- Orbit bank: (N/2)(log₂L−1)+B/2

To see the lower bound, a two-coordinate unitary mixing changes the probabilities in two rows while preserving their per-column sum. For each column, the binary entropy contribution can change by at most that sum; summing the two row masses gives at most 2 bits. Starting from identity entropy zero, at least N log₂N/2 such gates are necessary to reach Fourier entropy N log₂N. Permutations and unit-modulus coordinate phases contribute no entropy and do not weaken the bound.

Thus the constructed circuit is already gate-optimal in the two-coordinate unitary model, including with arbitrary intermediate monomial factors. Cross-bank fusion must leave this gate model to deliver an asymptotic saving. This does not prohibit fast global structured stages: their dense action must be charged by an explicit executor, and the entropy-per-two-coordinate-gate argument cannot simply be assigned to a whole global stage.

## 5. Pure inverse-sparse product obstruction

For factors G_j=B_j^−1 whose inverses have at most s_j nonzeros per row, interspersed with monomial matrices, the inverse product has at most ∏_j s_j nonzeros per row. Since every inverse Fourier entry is nonzero,

`∏_j s_j ≥ N`.

The supplied constant-s statement s^t≥N is the special case. For s≥2, t≥ceil(log_sN). If s=1 and N>1, the factorization is impossible at every depth. Cancellation can only reduce support, so it cannot defeat the inequality. The result is independent of conditioning and coefficient sizes.

This is a necessary structural stage-count bound. Bounded row sparsity of B_j alone does not guarantee a cheap algorithm for applying B_j^−1, so it must not be converted into a universal runtime lower bound by presuming every solve costs Θ(N). Sums of inverses and stages with dense inverses are outside the hypothesis.

The one-stage complex support uncertainty corollary st≥N is also valid for F_N=B^−1A with respective row-support bounds s,t. It does not cover a dense but fast structured preprocessing A.

## 6. Independent verification

Run `python3 independent_phase15.py` in this directory. Results are saved to `independent_phase15_results.json`.

- Exact modular full factorization and forward/inverse round trips at (N,B)=(16,8),(32,8),(64,8),(128,16),(256,16),(256,128),(512,32),(1024,32),(2048,64),(4096,64).
- Direct phase-14 residual sums compared independently with folded residuals for every listed N≤1024.
- Exact orbit histograms and butterfly counts for all ten cases.
- Independently constructed complex R matrices at N=16,32,64,128,256 verify scaled unitarity, exact support counts, and Φ(R̂)=N−B. Maximum Gram-entry error: 4.45×10^−16.
- No imported source checker, source executor, or source test suite was run. Source regression claims remain separately source-reported.

## Bottom line

Keep Phase 15 as an exact structural advance and a calibrated positive control. It closes the direct-sparse-residual bottleneck but conserves the complete classical radix-2 work. A useful next construction must jointly handle the two expensive Fourier banks and explain how it avoids both the two-coordinate unitary gate restriction and, if applicable, the pure inverse-sparse support restriction. Neither obstruction is a general Fourier arithmetic lower bound.
