# Independent audit of the stable Fourier inverse defect theorem

Date: 10 October 2026

## Verdict

The central subspace argument is valid. For the normalized complex DFT, an invertible matrix whose inverse is row-sparse plus low rank satisfies the claimed conditioning-independent error bound, provided the scalar corollary explicitly assumes **s ≥ 1**. The parity correction-rank threshold **N/4** is valid and is attained in the stated broad one-sided support class.

Two corrections are needed in the presentation:

1. The opening assumptions allow s = 0, but the scalar corollary silently uses s ≥ 1. With B = 0, E = U*, M = U and r = N, the displayed scalar bound incorrectly says 0 ≥ 1. Add s ≥ 1 to that corollary and its product-stage versions, or give a separate s = 0 branch.
2. For integer r ≥ 1, the integer optimization in equation (4) is **equivalent to**, rather than slightly stronger than, equation (5). No rounding loss is needed for the resulting positive-rank necessary condition.

These issues do not invalidate the main spectral-quantile theorem, the intended positive-sparsity bound, or the parity threshold. This is a restricted matrix-structure result. It supplies neither an O(N) FFT nor a lower bound against unrestricted FFT architectures. Publication-level novelty is not established.

## Evidence scope and lineage

The main spectral-quantile proof, scalar correction, and parity threshold were independently checked. Fresh controls were written without importing or executing submitted programs. The standalone theorem and archived theorem were byte-identical, with source hashes recorded in SOURCE_MANIFEST.json.

The inherited exact all-length inequality rank(F_N−B)≥floor(N/(s+1)) is preserved as inherited context and is excluded from new contribution accounting. Classical inverse-submatrix nullity and singular-value approximation already derive the graph certificate. Publication priority is unresolved.

The local-defect, strict-parity and single-neighborhood sharpness refinements received independent acceptance. The complete proof and the zero-critical-singular-value boundary are retained in notes/05_inverse_refinement_review.md. The sharpness constraint is one prescribed allowed neighborhood B[I,Jᶜ]=0, not an exact support-union constraint or a global row-sparsity sharpness theorem.

## Precise accepted statement

Let N ≥ 1 be an integer and let U be the normalized complex DFT,

U[j,k] = exp(−2πijk/N)/√N, with j,k in {0,…,N−1}.

Let M be invertible, H = M⁻¹ = B + E, and let r be a nonnegative integer with rank(E) ≤ r. For I of size t > r, put J = union of the supports of B's rows indexed by I and d = t−r. Singular values are ordered decreasingly and padded with zeros. Then

‖M−U‖₂² ≥ 1−σ_d(U[J,I])² ≥ max{0, 1−t|J|/[N(t−r)]}.

The first right-hand side is already nonnegative because a submatrix of a unitary matrix is a contraction. If every row of B has at most s nonzeros, with s an integer satisfying 1 ≤ s ≤ N, then:

- r = 0: ‖M−U‖₂ ≥ √(1−s/N)
- r ≥ 1: ‖M−U‖₂ ≥ √max{0, 1−4sr/N}

One may use any larger integer sparsity or rank budget; r > N is harmless but uninformative. For s = 0, invertibility forces rank(E) = N, and the correct universal error lower bound is only zero.

No bound on coefficients, ‖E‖, ‖H‖, or the condition number of B or M is an additional hypothesis. In particular, B need not be invertible. When an approximation already has error ε < 1, proximity to a unitary of course implies σ_min(M) ≥ 1−ε and ‖M‖ ≤ 1+ε; the proof does not need to assume these in advance.

## Independent proof

Write R_I for coordinate restriction. The nullspace of E[I,:]* contains a d-dimensional subspace V. Send a ∈ V to h = H[I,:]*a. Since H is invertible, this map is injective. Its image W therefore has dimension at least d. Every h ∈ W is supported on J and M*h is supported on I.

For a unit vector h ∈ W and ε = ‖M−U‖₂,

‖R_{Iᶜ}U*h‖₂ = ‖R_{Iᶜ}(U−M)*h‖₂ ≤ ε.

Unitarity gives ‖R_I U*h‖₂² ≥ 1−ε². Thus U[J,I]* has gain at least √(1−ε²) on a d-dimensional subspace when ε < 1. Singular-value minimax gives σ_d(U[J,I])² ≥ 1−ε². For ε ≥ 1, the claimed bound is automatic. Finally,

d σ_d(U[J,I])² ≤ ‖U[J,I]‖_F² = t|J|/N.

This proves the two graph bounds. For positive integer r with 2r ≤ N, choose t = 2r and use |J| ≤ st. If 2r > N and s ≥ 1, then 4sr/N > 1 and the scalar bound is vacuous. For r = 0 choose one row. No inversion perturbation estimate or limiting argument enters the proof.

The singular-value statement holds for **every unitary U**, not only the DFT. Fourier flatness is used only in the Frobenius calculation. More generally, if max|U[j,k]| ≤ μ/√N, replace t|J|/N by μ²t|J|/N.

## Integer optimization correction

Assume s ≥ 1 and ε < 1, and put α = N(1−ε²)/s, so 0 < α ≤ N. Equation (4) says

r ≥ max over integers 1 ≤ t ≤ N of {t−t²/α}.

For integer r ≥ 1 this holds exactly when α ≤ 4r:

- If α ≤ 4r, the maximum even over all real t is α/4 ≤ r.
- If α > 4r, t = 2r is an allowed integer and 2r−4r²/α > r, a contradiction.

For r = 0, the condition instead reduces to α ≤ 1, recovering the one-row bound. Hence the integer envelope adds no extra positive-rank strength to equation (5). If r ≥ 1 and ‖M−U‖₂ ≤ ε₀ < 1, the exact necessary condition is

r ≥ ceil((1−ε₀²)N/(4s)).

The source's weaker O(1)-loss statement is true with suitable interpretation, but the suggested extra finite-N strength is not present. The graph-specific quantile bound can still be much stronger than either scalar formulation.

## Parity threshold and its boundary

Assume 4 divides N and B's even rows vanish on odd columns. For I = J₀ = the N/2 even indices, U[J₀,I] has rank N/4 and its nonzero singular values are all one. This follows directly by rewriting the block as repeated characters of order N/4.

If rank(E) < N/4, then d = N/2−rank(E) exceeds the rank of this block. The graph certificate yields error at least one. In fact, invertibility strengthens this to **error strictly greater than one**: W contains a nonzero h with R_I U*h = 0, whereas M*h is nonzero and supported on I. These two images are orthogonal, so for a unit such h,

‖(M−U)*h‖₂² = 1 + ‖M*h‖₂² > 1.

The value one is still the infimum in this class: M = δI, B = δ⁻¹I, E = 0 has error tending to one as δ decreases to zero.

At rank(E) = N/4, exact equality M = U is possible. Set H = U*, let E contain precisely H's even-row/odd-column block, and set B = H−E. That block has rank N/4 and B has the required one-sided support. This establishes the exact correction-rank cutoff. The construction permits dense unrestricted rows and does not attain the cutoff under an additional small uniform row-sparsity constraint.

## Other source corollaries

The general residue-coset spectrum is correct. For divisor steps d_I,d_J, put t = N/d_I, m = N/d_J and h = N/gcd(N,d_I d_J). Removing offset phases leaves the character matrix exp(−2πi d_I d_J ab/N)/√N. Its character has order h, and h divides both t and m. The h nonzero singular values are therefore √(tm/(Nh)); the remaining values vanish. This value is at most one because gcd(N,d_I d_J) ≤ d_I d_J. Restricting the row set from the containing coset J₀ to J cannot increase any singular value. The source's two cases follow when t > r. No additional arithmetic restriction on N beyond the specified divisors is needed.

The product-stage claim is also correct under its stated structural model, with the same positive-sparsity qualification for the scalar bound. Write H = A₁⋯A_k, A_j = B_j+E_j. The difference H−B₁⋯B_k has the telescoping expansion

Σ_j (A₁⋯A_{j−1}) E_j (B_{j+1}⋯B_k).

Each term has rank at most rank(E_j), so the defect rank is at most R = Σ_j r_j. Products of row-s_j-sparse matrices have row degree at most S = ∏_j s_j. Consequently the scalar bound applies for S ≥ 1 and R ≥ 1. R = 0 uses the separate sparse-inverse bound. If a stage's sparse part is zero, its inverse-stage matrix must instead have full-rank defect for invertibility; that degenerate case cannot use a scalar expression with S = 0. The advertised S ≤ 2^k application presupposes an actual two-sparse inverse representation for each Green stage. It does not extend to products of sums merely by counting individual Green denominators.

## Classical connection and local-defect refinement

The graph certificate has a particularly direct classical derivation that should be cited. The inverse-submatrix nullity theorem gives

rank(H[I,Jᶜ]) = rank(M[J,Iᶜ]) + t−|J|.

Because H[I,Jᶜ] = E[I,Jᶜ], its rank is at most r. Consequently rank(M[J,Iᶜ]) ≤ |J|−d. Low-rank approximation by singular values gives

ε ≥ σ_{|J|−d+1}(U[J,Iᶜ]) = √(1−σ_d(U[J,I])²).

The last identity follows from U[J,I]U[J,I]* + U[J,Iᶜ]U[J,Iᶜ]* = I_|J|. This is an independent derivation of exactly the source's certificate, not merely an analogy. The classical nullity relation and its proof are available in Vandebril and Van Barel, Section 3; Lang, Theorem 2.1 and equation (3.2), states the inverse-nullity and singular-value approximation facts together. [Vandebril and Van Barel](https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf), [Lang](https://arxiv.org/pdf/0812.0172)

This derivation also permits the smaller **local** defect rank ρ = rank(E[I,Jᶜ]) in place of the global bound r, whenever t > ρ. The original theorem remains valid; it simply leaves this refinement unused.

### Single-neighborhood sharpness refinement

There is an explicit attaining construction for the general unitary certificate when d ≤ min(t,|J|) and σ_d(U[J,I]) > 0. Let Q be an N×d orthonormal matrix supported on J whose columns are the leading d left singular vectors of U[J,I], embedded in the full coordinate space. Put

M = U−QQ*U P_{Iᶜ}.

Then ‖M−U‖₂ = √(1−σ_d(U[J,I])²). To see invertibility, if Mx = 0 then Ux = Qa; substituting x = U*Qa gives

Q*U P_I U*Q a = 0.

The coefficient matrix has eigenvalues σ₁²,…,σ_d², all positive, so a = x = 0. Also Q*M vanishes on Iᶜ, hence rank(M[J,Iᶜ]) ≤ |J|−d. The nullity identity yields rank(H[I,Jᶜ]) ≤ t−d. Take E to be exactly that forbidden block of H, with zeros elsewhere, and B = H−E. This gives rank(E) ≤ t−d and B[I,Jᶜ] = 0.

Thus the quantile certificate is optimal for a **single prescribed neighborhood constraint** with unrestricted remaining rows. This audit-derived observation is not a claim of first publication and does not prove sharpness of the global uniform-sparsity 4sr/N constant.

## Relation to uncertainty and rigidity

Candès and Romberg's quantitative uncertainty theorem concerns random time/frequency support sets and controls concentration through Fourier submatrix norms. The source uses the same type of concentration operator, but its deterministic d-dimensional conclusion follows here from minimax and trace. Their random-support theorem should not be described as the identical result. [Candès and Romberg, Section 3](https://arxiv.org/html/math/0411273)

Dvir and Liu define regular rigidity using a bound on changed entries in both each row and each column, and prove quasipolynomial non-rigidity of complex DFT matrices. The source imposes a row-only sparse-plus-low-rank structure on an inverse, and measures approximation error on the forward operator. These are different conditions; the present lower bound does not contradict their result or restore a general FFT circuit lower bound. [Dvir and Liu, Definition 1.2 and Theorem 1.10](https://arxiv.org/html/1902.07334)

Chandrasekaran and coauthors study identifiability and convex recovery of sparse-plus-low-rank decompositions. This is relevant background for the decomposition model, not a proved priority match for this inverse-approximation statement. [Chandrasekaran et al.](https://arxiv.org/abs/0906.2220)

The checked sources make the classical nullity and approximation lineage especially important. A useful project refinement has been established mathematically; a new theorem in the literature has not been established by this limited search.

## Fresh controls and limitations

The independently written fresh_controls.py and its output FRESH_CONTROL_RESULTS.json are included under programs/stable_inverse and certificates/stable_inverse; see REPRODUCE.md. With seed 741803 and NumPy 2.3.5, all controls passed:

- 60 constructed DFT and 60 constructed general-unitary quantile attainment cases; 75 have a strictly intermediate bound between zero and one
- 120 complementary-rank identity checks
- 72 positive-sparsity scalar checks and 102 random graph-quantile checks
- 549 coset-spectrum checks, covering every divisor pair for N from 1 through 32 with nonzero offsets where available
- 6 exact prime-field parity rank checks, for N = 4, 8, 12, 20, 28, 36
- 5 exact-Fourier parity threshold constructions and 15 controls approaching the lower-error infimum
- 3 deliberate s = 0 counterexamples to the unqualified scalar statement

The largest squared-error residual in the 120 attainment cases was 2.67×10⁻¹⁵. Near an exactly zero bound, taking a square root magnifies roundoff to about 5.2×10⁻⁸; intermediate-bound attainment residuals were at most 3.2×10⁻¹⁵. The largest coset-spectrum residual was 5.0×10⁻¹⁵. These are finite checks, not proofs, and modular rank calculations say nothing about an operator norm over a finite field.

## Recommended disposition

Accept the main theorem and parity application after making s ≥ 1 explicit in scalar corollaries and correcting the integer-optimization comparison. Cite the inverse-submatrix nullity theorem. Preserve inherited exact-rigidity attribution. Retain the restricted-model and no-complexity-conclusion limitations. The local-rank, strict-parity and single-neighborhood sharpness statements are retained separately; their independent review status is recorded in PROOF_STATUS.json. Worldwide priority remains unresolved.
