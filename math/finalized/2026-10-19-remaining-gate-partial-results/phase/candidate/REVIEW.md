# Independent review of the local and coarse-global claims

Reviewed 19 October 2026 UTC. I inspected the newly authored exact checker and its output, the complete new `PROOF.md` and `GLOBAL_LEMMA.md`, and the accepted periodic-sector theorem as a prerequisite. I did not execute a historical research package. The derivations below independently check the analytic implications and constants. No flaw was found in either claim or in the remaining-lemma equivalences. The unrestricted sharp value remains unproved.

## 1. Strict local optimality

The coefficient formulas in `exact_local_checker.py` are correct. For a real phase-sum matrix D,

Y(h) = Y0 + X0 ∘ D − (Y0 ∘ D²)/2 + O(||h||³).

The checker's first derivative H1 and polarized quadratic coefficient H2 consequently agree with the expansion of Y(h)^T Y(h). Its mixed quadratic coefficients use the correct factors of 1/2. The resolvent correction also has the correct negative sign and denominator γ = c² − s².

At the witness, X0 and Y0 are real symmetric and commute: this follows from symmetry and unitarity of V0. Both commute with R and L because R = (Y0² − s²I)/γ. Thus the matrix G0 = L X0 Y0 L/(sc) and the displayed Ω are real symmetric. The certified identities G0² = L and tr(G0) = 2 give eigenvalues +1 four times and −1 twice on ran(L). Hence Ω has eigenvalues 1/8 four times and 1/4 twice there, is positive definite there, and has trace one. These symmetry/reality facts should appear in the proof, even though they are not separate named assertions in the checker.

The seven periodic directions and eight anti-periodic directions form a genuine local chart after removing the one-dimensional scalar phase-transfer gauge. The certified rank seven proves injectivity of α ↦ A(α) on the periodic directions. I also independently recomputed the displayed integer Gram determinant as 12288. The eight other first derivatives vanish. Since tr(Ω A(α)) = 0 and Ω is positive definite on ran(L), every nonzero A(α) has a positive eigenvalue. Compactness of the unit sphere in the seven-dimensional domain yields a uniform κ > 0 such that

λmax(A(α)|ran(L)) ≥ κ ||α||.

The isolated six-dimensional low spectral cluster admits a real-analytic orthonormal reduction to the fixed space ran(L). In the canonical graph frame its expansion is

G(h) = s² L + A(α) + L[H2(h) − H1(h) R H1(h)/γ]L + O(||h||³).

This is an operator on ran(L). The two remaining eigenvalues stay close to c², so σ3(Y(h))² = λmax(G(h)). The checker certifies that the Ω-weighted quadratic coefficient on the anti-periodic subspace is exactly

β ||ν||², where β = cos(π/8)/(4√2) > 0.

For completeness, a putative nonincrease λmax(G(h)) ≤ s² gives ||α|| = O(||h||²) by the preceding first-order bound and the uniform quadratic remainder. Therefore ||ν||² = ||h||² + O(||h||⁴), and

tr[Ω(G(h) − s²L)] = β ||ν||² + O(||α|| ||h||) + O(||h||³)
                         = β ||h||² + O(||h||³) > 0

for all sufficiently small nonzero h. This contradicts λmax(G(h)) ≤ s². Thus the stated strict local minimum, modulo scalar phase transfer, follows. Strictness is a local assertion and does not exclude other remote minimizers or lower remote points.

## 2. The coarse unrestricted lower bound

Let u = p², v = q², and let Π project onto four-periodic vectors. Put A = ||(I−Π)u||² and B = ||(I−Π)v||². For W[j,k] = exp(−πijk/2), one has W = ΠWΠ and W*W = 16Π. Consequently

E = ||Im(PFQ)||F² = 4 − Re(u^T Wv)/16
  ≥ 4 − √((8−A)(8−B))/4
  ≥ 2 + (A+B)/8.

The imaginary part of a unitary matrix is a contraction as a real matrix. With τ = σ3(Y), the first two squared singular values are at most one and the other six at most τ², so E ≤ 2 + 6τ². Hence A+B ≤ 48τ².

Independent real signs permit each phase pair to be represented by a common midpoint and deviations ±ρr or ±σr with absolute values at most π/4. These signs preserve the objective and the squared phases. Direct computation of the orthogonal projection gives

A+B = 2 Σr sin²(2ρr) + 2 Σr sin²(2σr).

Thus the claimed sum bound 24τ² is correct. Let u0 = max|ρr| and v0 = max|σr|. If τ < 1/√24, then sin²(2u0)+sin²(2v0)<1, which forces 2u0+2v0<π/2. The identity

sin²x + sin²y = 1 − cos(x+y)cos(x−y) ≥ 2 sin²((x+y)/2)

applies here with x=2u0 and y=2v0. It gives u0+v0 ≤ arcsin(√12 τ), including the stated constant.

### Elementary proof of the angular singular-value estimate

For a unit complex vector z, its angle to the real subspace R⁸, in the underlying real Euclidean space, is arcsin(||Im z||). A diagonal unitary D with arguments bounded by a ≤ π/2 moves every unit vector through an angle at most a, because Re(z*Dz) ≥ cos(a). Angular distance to R⁸ therefore increases by at most a.

Apply this pointwise on the real six-dimensional minimizing subspace in the singular-value min–max formula for σ3(Im V), using that V is unitary. It proves

arcsin σ3(Im(DV)) ≤ arcsin σ3(Im V) + a.

The same assertion for right multiplication follows by transposition, since V^T is unitary and singular values are unchanged by transposition. Applying the row and column bounds successively to remove the paired deviations gives the stated periodic-comparison estimate with a = u0+v0. No eigenphase-labeling assumption is needed.

The accepted periodic-sector theorem now gives

π/16 ≤ arcsin τ + arcsin(√12 τ)

when τ < 1/√24. The right side is strictly increasing. Its unique crossing is

t0 = sin(π/16)/√(13 + 4√3 cos(π/16))
   = 0.04384873791488374… .

Indeed sin(π/16 − arcsin t0) = √12 t0; the angles are in the principal arcsine range. The remaining branch τ ≥ 1/√24 already exceeds t0. Thus the lower bound is unrestricted and valid.

## 3. Remaining-lemma equivalences

The new `GLOBAL_LEMMA.md` correctly identifies the missing sharp result with the assertion that every open arc of length π/4 contains at most five eigenvalues of F₈ A F₈ B for arbitrary diagonal unitary A,B. Similarity by Q identifies this spectrum with that of VᵀV. Taking square roots of diagonal phases is surjective, and a scalar multiple of A rotates the whole spectrum, so the arbitrary-arc and arc-centered-at-one formulations are equivalent. The open-arc condition correctly corresponds to a strict counterexample below sin(π/16).

The cyclic-Hankel restatement is also valid: C=F₈AF₈ runs over precisely the symmetric unitary cyclic Hankel matrices; with D=B⁻¹, VᵀV−I=Q(C−D)Q. Thus σj(C−D)=2σj(Im V), with the same descending order. These equivalences are reformulations, not additional lower-bound proofs.

## Conclusion

The evidence supports both a strict full-phase local minimum at the displayed witness and the global interval t0 ≤ δ1 ≤ sin(π/16). It does not establish δ1 = sin(π/16). The global bound is conditional only on the accepted continuous periodic-sector theorem, not on a phase grid or an unproved phase-reduction assertion.
