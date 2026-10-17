# Independent review: fixed-pencil primary comparison

Date: 2026-10-17. Claim: ALG-FIXED-PENCIL-CERTS.

## Verdict

**Accept the bounded comparison in the author files bound by AUTHOR_BINDINGS.json.** The required primary-source hypothesis/formula/cost mappings and qualified whole-theorem nonmatches are supplied. The existing finite-certificate comparison activity can be archived as completed supporting evidence. No independent public status change or external write is made by this review.

This acceptance retains the previously accepted exclusion at N = 4, 8, 16, 32, 64, 128. It does not reopen that proof, rerun its programs, reconstruct its certificate arrays, add discovery credit, establish worldwide novelty, or authorize a standalone promotion.

The two gates must remain distinct:

- The **bounded comparison gate is complete**. Its permitted qualified-nonmatch outcome has been reached with specific, accessible primary sources.
- A **new reusable theorem increment sufficient for standalone novelty promotion is not established**. That conditional threshold is respected because no such promotion is proposed. It must not be marked as passed.

The author's COMPARISON.json makes this distinction explicitly: bounded_gate_exhausted is true and promotion_gate_passed is false.

## 1. Cyclic-resolvent and cost comparison

Huhtanen–Perämäki, Theorem 2.9 (manuscript p. 6), gives the inverse of I + DS. With D = −αI and W = QSQ⁻¹, its scalar specialization is

(I − αW)⁻¹ = Q(Σ[k=0,…,N−1] αᵏSᵏ)Q⁻¹/(1 − αᴺ).

The hypothesis is exactly αᴺ ≠ 1. Proposition 2.5 (p. 4) gives linear factorization/storage for a nonsingular sum of two scaled permutations. Sparse triangular solves then supply linear application cost. The n-term inverse expansion by itself is not a linear-time application argument. The author correctly locates the cost in the sparse primitive and the accepted recurrence. [Primary manuscript](https://math.aalto.fi/~mhuhtane/manu.pdf).

Theorem 4.3 (p. 10) uses n−1 factors S − Dⱼ and a final diagonal, with freely selected diagonals, on an open dense, full-measure set of matrices. It is generic expressivity, not a theorem for every particular matrix or a fixed-depth one-scalar grammar. Neither Fourier membership nor nonmembership in the fixed six-resolvent pencil follows. A direct supplied-factor schedule is O(n²), not a constant-stage O(n) construction. The author preserves these distinctions.

For the retained circuit, the inherited corrected schedule is six Green solves, two masks, and **three** branch sums. Its O(N) field-arithmetic application cost assumes the fixed lists and parameters are supplied. Certificate generation/checking, parameter generation, coefficient bit growth, and numerical stability are different questions.

## 2. Rational Haagerup ratio

Ikuta–Munemasa explicitly use arbitrary nonsingular complex diagonal scalings and independent permutations in their equivalence definition (pp. 1–2). Their §5 (p. 18) gives the rational invariant WₐᵦW𝚌𝚍/(Wₐ𝚍W𝚌ᵦ). This directly supports the author's ratio and gauge-group comparison, not merely the unit-modulus conjugate formula. [Primary manuscript](https://arxiv.org/pdf/1411.0057v3).

The target implication can also be checked directly. With M_ij = a_i b_j omega^(r_i c_j), each ratio cancels a and b and becomes an Nth root of unity. Thus the two displayed fⱼ are necessary equations independent of the unknown outer permutations. Their vanishing is not a sufficient Fourier-recognition criterion. Zero-entry matrices cannot be equivalent to Fourier through invertible outer scalings. The target does not need to assume every member of the pencil is type-II.

The author's citation supports a classical mechanism. It does not attribute the particular two-plaquette, six-size exclusion to this paper or claim that the 1997 Haagerup chapter was read.

## 3. Modular GCD and characteristic-zero lifting

Van Hoeij–Monagan, Theorem 1 (p. 5), bounds characteristic-zero gcd degree by the successful modular gcd degree under its stated reduction hypotheses. Algorithm step 4 (p. 7) terminates at gcd one. Section 2 defines the full residue algebra, which for Q(i) is Fₚ[z]/(z²+1). This is not the target's selected component i ↦ j in Fₚ. The author correctly treats this as related classical machinery and supplies a separate determinant-specialization bridge. [Primary manuscript](https://www.cecm.sfu.ca/CAG/papers/hoeijmon.pdf).

The bridge is sound, with all of these guards:

1. The polynomials lie in a coefficient localization A = Z[i,S⁻¹]. All inverted rational and Green denominators have nonzero images under φ:A→Fₚ, and the chosen image j satisfies j² = −1. There is no homomorphism of fields Q(i)→Fₚ.
2. Both polynomial degrees are preserved, here exactly 2N. Thus the fixed-size Sylvester determinant specializes to the resultant of the actual reduced polynomials.
3. The complete modular identity uφ(f₁)+vφ(f₂)=1 proves coprimality over Fₚ and therefore absence of common roots over its algebraic closure.
4. Consequently the reduced resultant is nonzero. The original resultant in A, hence Q(i), is nonzero and the original polynomials have no common complex root.

This shows why **one** valid component and prime suffice. The second prime is corroboration. No characteristic-zero Bézout arrays are reconstructed by this reasoning.

The degree guard is substantive: f = g = pλ + 1 has a common characteristic-zero root, while both reductions are constants with gcd one. Merely searching λ in Fₚ is also insufficient. The author's final report makes neither mistake.

Collins' publisher abstract confirms an earlier exact modular-resultant algorithm. The author uses it only as abstract-level historical context, and I independently checked that limited support. It is not a substitute for the explicit bridge. [Publisher abstract](https://doi.org/10.1145/800204.806289).

## 4. Specific content and residual scope

The classical ingredients are cyclic sparse inversion, diagonal/permutation ratio cancellation, polynomial elimination, and guarded modular coprimality. The retained instance-specific content consists of the fixed six traversal orders, Gaussian-rational parameters and masks, two selected plaquettes, and twelve successful certificates across six sizes. The inspected primary statements do not supply those particular outcomes. This is a bounded qualified nonmatch, not evidence that no earlier equivalent result exists.

The accepted claim allows every complex value of the single middle scalar λ and arbitrary invertible external diagonal gauges/permutations. It does not allow variable internal masks, α values, branch weights, seeds, cycle orders, arbitrary Green sums, or unbounded N. The adjacent primitive-holonomy single-Green curvature theorem is a different statement and receives no new priority assessment here.

Broader tunable-mask and noncommuting-weight constructions, uniform parameter generation, and a fully costed Fourier algorithm remain unresolved. They are not silently declared solved, transferred, or made prerequisites for retaining the existing finite negative result. Any future standalone promotion requires an explicitly new reusable increment and a fresh bounded comparison appropriate to that increment.

## 5. Review coverage and reproducibility

I read all four final author files, checked the declared manifest against actual bytes, and independently read the relevant primary statements. Accepted theorem/review hashes are recorded separately. The review's byte bindings include the author's manifest itself, so changing any author artifact invalidates this acceptance until rebound.

No historical program was executed; no full original-certificate replay is claimed. No external write, status mutation, exhaustive bibliography census, production claim, new proof acceptance, or worldwide novelty assertion was performed. No blocking mathematical or attribution issue remains for this bounded comparison.
