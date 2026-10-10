# Independent verification of the inverse defect refinements

Date: 10 October 2026

## Acceptance and boundary clarifications

All four refinements in the reviewed audit are correct: the local forbidden-block rank replacement; strict error greater than one below the parity threshold, with infimum one; attainment of the single-neighborhood spectral-quantile bound when its critical singular value is positive; and equivalence of the two scalar formulations for positive integer rank budgets.

The sharpness result has the following precise scope. It concerns one prescribed **allowed neighborhood**, meaning B[I,Jᶜ] = 0, with unrestricted remaining entries. It does not require the union of the nonzero supports to equal J, and does not establish sharpness of the uniform row-sparsity constant 4. For a nontrivial rank budget r < |I|, the class is nonempty exactly when d = |I|−r ≤ |J|. At a zero critical singular value the same lower bound is the exact infimum, but no invertible matrix attains it. These are clarifications and a completed boundary statement, not counterexamples to the reviewed claims.

The positive-sparsity scalar theorem is accepted for every flat unitary U, meaning U*U = UU* = I_N and |U[j,k]|² = 1/N, under the hypotheses that M is invertible, M⁻¹ = B+E, B is row-s-sparse, s ≥ 1 is an integer, and rank(E) ≤ r for an integer r ≥ 1:

‖M−U‖₂ ≥ √max{0, 1−4sr/N}.

No coefficient or conditioning hypothesis is needed. The r = 0 branch is ‖M−U‖₂ ≥ √max{0,1−s/N}. The scalar positive-rank formula is not valid at r = 0 or s = 0. If s = 0, invertibility forces rank(E) = N and the universal error lower bound is zero. Unitarity alone suffices for the spectral-quantile result; flatness is needed only to replace a submatrix Frobenius norm by |I||J|/N.

## Local rank theorem and classical reduction

Let U be any complex N×N unitary matrix, M invertible, and H = M⁻¹ = B+E. Choose index sets I,J with t = |I| > 0, m = |J|, and B[I,Jᶜ] = 0. Put

ρ = rank(E[I,Jᶜ]) = rank(H[I,Jᶜ]),   d = t−ρ.

Assume d > 0. Then d ≤ min(t,m), and

‖M−U‖₂² ≥ 1−σ_d(U[J,I])² ≥ max{0, 1−‖U[J,I]‖_F²/d}.

All singular values are in decreasing order, with zeros added when needed. To prove this without an inversion perturbation estimate, let V be the kernel of H[I,Jᶜ]*, of dimension d. Embed a ∈ V in the I coordinates and define h = H* a. Then h is supported in J, M*h = a is supported in I, and a ↦ h is injective. In fact its image is exactly

W = {h: h is supported in J and M*h is supported in I}.

Thus dim(W) = d. On this subspace, for ε = ‖M−U‖₂,

‖P_I U*h‖₂² = ‖h‖₂²−‖P_{Iᶜ}U*h‖₂² ≥ (1−ε²)‖h‖₂².

For ε < 1, singular-value minimax yields σ_d(U[J,I])² ≥ 1−ε²; for ε ≥ 1, the result is automatic. The trace inequality d σ_d² ≤ ‖U[J,I]‖_F² gives the second bound. Here P_K denotes the N×N orthogonal coordinate projection; vectors in coordinate subspaces are identified with their full-space embeddings.

The dimension of W is also m−rank(M[J,Iᶜ]). Therefore

rank(H[I,Jᶜ]) = rank(M[J,Iᶜ]) + t−m.

This is the classical inverse-submatrix nullity identity. It implies rank(M[J,Iᶜ]) = m−d. Set A = U[J,I] and C = U[J,Iᶜ]. Since AA*+CC* = I_m, their complementary eigenvalue lists give

σ_{m−d+1}(C)² = 1−σ_d(A)².

The classical spectral-norm low-rank approximation theorem now gives the same bound directly:

‖M−U‖₂ ≥ ‖M[J,Iᶜ]−C‖₂ ≥ σ_{m−d+1}(C).

The spectral lists here are padded to m entries. This includes empty complement blocks. If a global defect budget r satisfies rank(E) ≤ r < t, then ρ ≤ r and the local index t−ρ is at least t−r, so the local lower bound is at least as strong as the global one.

Attribution: the nullity identity is classical; see Vandebril and Van Barel, *A short note on the nullity theorem*, Section 3, Corollary 1, which recounts its earlier lineage. Lang, *The Inverse of a Nearly-banded Matrix*, Theorem 2.1 and equation (3.2), explicitly states the nullity and spectral low-rank approximation facts used here; the latter is the Eckart–Young singular-value characterization. The proof above spells out their application to this setting. No publication-priority or novelty claim is made.

- https://www.cs.kuleuven.be/publicaties/rapporten/tw/TW397.pdf
- https://arxiv.org/pdf/0812.0172

## Complete sharpness theorem for one allowed neighborhood

Fix U,I,J and an integer 0 ≤ r < t. Write d = t−r and define

C(I,J,r) = {M invertible: rank(M⁻¹[I,Jᶜ]) ≤ r}.

This is exactly the set of invertible matrices admitting some decomposition M⁻¹ = B+E with B[I,Jᶜ] = 0 and rank(E) ≤ r: one direction is immediate, and the other follows by taking E to be the forbidden block of M⁻¹ and zero elsewhere.

If d > m, this class is empty, by the nullity identity. If 1 ≤ d ≤ min(t,m), it is nonempty and

inf over M ∈ C(I,J,r) of ‖M−U‖₂ = √(1−σ_d(U[J,I])²).

The infimum is attained if and only if σ_d(U[J,I]) > 0. This includes the zero-error case σ_d = 1.

### Positive critical singular value

Let Q_J contain orthonormal leading d left singular vectors of A = U[J,I], and embed it as Q ∈ C^{N×d}, supported in J. Write the corresponding squared singular values as λ₁ ≥ ⋯ ≥ λ_d > 0. Define

M₀ = U−QQ*U P_{Iᶜ}.

Because Q is an isometry,

‖M₀−U‖₂² = ‖Q*U P_{Iᶜ}‖₂²
             = λ_max(I_d−Q*U P_I U*Q)
             = 1−λ_d.

This error is strictly less than one. Therefore M₀ is invertible: U*M₀ differs from the identity in norm by less than one. Equivalently, the determinant identity gives

det(M₀)/det(U) = det(Q*U P_I U*Q) = λ₁⋯λ_d > 0.

Moreover Q*M₀ P_{Iᶜ} = 0. Restricting to J yields

M₀[J,Iᶜ] = (I_m−Q_J Q_J*)U[J,Iᶜ],

whose rank is at most m−d. The inverse-submatrix identity then gives

rank(M₀⁻¹[I,Jᶜ]) ≤ t−d = r.

With E equal to this forbidden inverse block and B = M₀⁻¹−E, all claimed structural conditions hold. The lower bound already proved shows that the achieved error is exactly the optimum. The construction need not use the entire allowed defect-rank budget.

### Zero critical singular value

Suppose σ_d(A) = 0. For every M in the class, its subspace W above has dimension at least d. Since rank(A) < d, W contains a nonzero h with P_I U*h = 0. Normalize h to unit norm. Then U*h is supported in Iᶜ with norm one, whereas M*h is a nonzero vector supported in I. Orthogonality gives

‖(M−U)*h‖₂² = 1+‖M*h‖₂² > 1.

Hence every feasible invertible M has error strictly greater than one, so equality is impossible.

To prove that the infimum is nevertheless one, choose any permutation matrix H₀ assigning at least d of the rows in I to distinct columns of J. Such a permutation exists because d ≤ min(t,m): choose d distinct row-column pairs and extend the partial matching to a full permutation. At most t−d rows of the forbidden block H₀[I,Jᶜ] can be nonzero, so its rank is at most r. For any δ > 0 put M_δ = δH₀⁻¹. Its inverse forbidden-block rank is unchanged. Since H₀⁻¹ is unitary,

|‖M_δ−U‖₂−1| ≤ δ.

Thus feasible errors approach one. Together with strictness, this proves the unattained infimum statement.

If r ≥ t, the forbidden-block constraint is automatic and U itself is feasible, giving minimum zero; no σ₀ notation is appropriate. Empty J with r < t gives an empty class. If I or J is the full index set, the same formulas and zero padding apply; there is no additional exceptional case once feasibility is imposed.

## Parity threshold including strictness

Let N = 4q and U be the normalized DFT. Take I = J to be the 2q even indices. After ordering the repeated indices, its even-even block equals

(1/2) [ U_q  U_q ; U_q  U_q ].

It has q singular values equal to one and q equal to zero. If B's even rows vanish on odd columns and rank(E) < q, the local forbidden-block rank is also less than q, so d = 2q−ρ > q. The zero-critical-value proof above yields ‖M−U‖₂ > 1.

Nevertheless M_δ = δI_N, B_δ = δ⁻¹I_N and E_δ = 0 obey the support constraint, and their error tends to one. Thus one is the exact unattained infimum for any defect-rank budget below q.

At budget q, take M = U, H = U*, E equal to its even-row/odd-column block, and B = H−E. The forbidden block differs from the conjugated even-even block only by unit-modulus row factors, so rank(E) = q. Exact error zero is possible. This is a cutoff in the broad one-sided support class; no small uniform row-sparsity condition is imposed on the unrestricted rows.

## Integer optimization with all boundaries stated

For s ≥ 1, 0 ≤ ε < 1 and α = N(1−ε²)/s, one has 0 < α ≤ N. Define

F_N(α) = max over integer 1 ≤ t ≤ N of (t−t²/α).

For every integer r ≥ 1,

r ≥ F_N(α)  if and only if  α ≤ 4r.

If α ≤ 4r, completing the square gives t−t²/α ≤ α/4 ≤ r for every real t. Conversely, if α > 4r, then t = 2r is an allowed integer because 2r < α/2 ≤ N/2. At this t, 2r−4r²/α > r. This proves equivalence, including the equality boundary α = 4r, with no rounding loss.

For r = 0, the equivalence is instead F_N(α) ≤ 0 if and only if α ≤ 1: check t = 1 for necessity, and t ≥ 1 ≥ α for sufficiency. At ε = 1, α is zero and the displayed rational optimization is undefined; only the original vacuous nonnegative error bound remains. At s = 0 the definition of α is likewise unavailable.

Consequently, for positive integer rank budgets, equations (4) and (5) in the source have exactly the same strength. An error target 0 ≤ ε₀ < 1 forces

r ≥ ceil(N(1−ε₀²)/(4s)),

subject to the explicit r ≥ 1 hypothesis. This is a necessary condition, not a general sufficiency assertion for globally row-sparse inverses.

## Independent controls and provenance

No supplied source code or earlier audit-control code was run or imported. A separate script, independent_refinement_controls.py, generated 264 positive-critical-value attainment cases for DFT and general unitaries, including 146 strictly intermediate bounds. It checked 264 complementary-rank identities, 4 zero-critical-value boundary examples, 6 parity threshold examples, 18 parity infimum examples, 164 empty-class rank obstructions, and 43,400 exact rational integer-envelope cases. Every check passed. The maximum squared-attainment residual was 1.56×10⁻¹⁵; the maximum inverse identity residual was 3.29×10⁻¹⁵. Numerical rank checks are supplementary controls, not exact rank proofs.

Reviewed inputs:

- STABLE_INVERSE_DEFECT_AUDIT.md: SHA-256 07756e7de788a7b4f04dcb0b988e2057f49c193e8be170a57a826d913d0a8022
- THEOREM.md and THEOREM(20261010-121059).md: SHA-256 db0052f2a206111170c3aeab03a9584659c0fc3978f387261982260730d2cefc
- FFT_STABLE_INVERSE_DIMENSION_THEORY_2026-10-10.zip: SHA-256 5953c67b6651224ddd935db2b6d7bc3341bbe755c2f78ad8ef96377dc3524414

The source ZIP was hashed, not executed. This refinement review does not repeat the earlier archive inventory or certify its historical test claims. Result details are in certificates/stable_inverse/INDEPENDENT_REFINEMENT_RESULTS.json; public exported-file hashes are in SOURCE_MANIFEST.json and SHA256SUMS. The accepted mathematics is a restricted matrix-structure statement, not an FFT implementation or an unrestricted complexity lower bound.
