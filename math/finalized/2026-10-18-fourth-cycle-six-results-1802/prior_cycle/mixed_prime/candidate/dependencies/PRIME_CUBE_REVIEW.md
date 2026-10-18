# Independent acceptance: prime-cube rank-three separation and N = 1331

Date: 18 October 2026 UTC. Candidate: `rank_three_prime_cube_20261018_1332`.

## Verdict

**ACCEPT the frozen theorem and its stated N=1331 consequence within the complex, disjoint/no-sharing Fourier rectangle model.**

For every prime p≥5, a rectangle of F_(p³) with rank at most three has one side occupying at most four residue classes modulo p², and consequently min(a,b)≤4p. The proof of the selected four-by-four minors is complete, including the mixed (3,1)–(2,2) case. It does not extrapolate from the exploratory 22 million sampled minors.

At N=1331, the minimum total endpoint-incidence cost is **175,692**. Every optimum consists of exactly 1331 rank-one full subgroup-coset × annihilator-coset rectangles, each with unordered side sizes {11,121}. The stated, not-claimed-sharp higher-rank-area penalty **1/484** is valid. The union of the previously accepted domains and this new length covers every N from 2 through 1858, with 1859 the next residual.

One wording correction was requested before freezing and is present in the accepted packet: the residue-occupancy result is stronger than the side-cardinality corollary, rather than logically equivalent to it. No substantive mathematical correction was required.

Frozen candidate REPORT.md SHA-256:
`5ac20c944190b6d95699a4b689ba7827e1dd0dbc24631f2b1e99504b9b78a98a`.

All seven files in the candidate manifest and both pinned accepted dependencies were hash-verified. This review uses those local accepted dependencies and does not claim to have refetched the repository. The contextual universal-sampling paper is not a proof dependency. No external write, publication, archival-status change, priority change, or worldwide novelty claim is part of this review.

## 1. Model and dependency scope

The objective is exactly the sum of r(a+b) over nonempty Cartesian tiles partitioning all N² entries. Here r is the actual complex rank. The proof never permits sharing, overlapping or cancelling decompositions, and it never substitutes a finite-field rank for a complex rank.

The accepted rank-one coset classification, sharp rank-two density, and stable-rank inequality ab≤Nr are used at the final density step. They are pinned through the candidate's two accepted source records. The older dominant-prime domain is used only in the combined-domain census. None of these dependencies is silently strengthened.

The new theorem is more precise than its min(a,b)≤4p corollary: rank≤3 forces at least one side to occupy at most four residues modulo p². A set of size at most 4p can occupy many more than four residues, which is why the corrected wording matters.

## 2. Universal-minor lemma and selection

For k≤p row exponents distinct modulo p, the generalized Vandermonde determinant is an integer alternating polynomial divisible by the usual Vandermonde. Its quotient S at the all-ones point is, up to an irrelevant sign, the quotient of the two difference products stated in the report. All numerator and denominator factors are p-adic units. Since S(1) is an integer, it is nonzero modulo p.

In the prime-power cyclotomic integer ring, setting ζ=1 has residue field F_p because Φ_(p^m)(1)=p. Therefore S at the chosen powers of ζ cannot vanish. Distinct column indices modulo p^m make the ordinary Vandermonde nonzero. This proves the needed universal-minor result; no general Fourier-minor theorem is being assumed without proof.

Among five representatives distinct modulo p², the four patterns U, A=(4), B=(3,1), and C=(2,2) are exhaustive as selectable subpatterns. If four different residues modulo p occur, choose U. If at most three residues occur and a class has at least four elements, choose A. A class of exactly three gives B. Otherwise five elements distributed among at most three classes of size at most two force two double classes and give C. The unselected pattern (2,1,1) need not be handled.

A U side directly invokes the lemma at p³. An A side is translated to multiples of p and reduced to a p²-order minor whose row indices are distinct modulo p and whose column indices remain distinct modulo p². Thus that application also has all its hypotheses.

## 3. The three block cases

Write ζ=ζ_(p³), η=ζ^p, ω=ζ^(p²), K=Q(η), and L=Q(ω). Both tower degrees are p. Consequently the standard p powers of ζ form a K-basis, and those of η form an L-basis. If t and q are units modulo p, z=ζ^(tq) has degree p over K; multiplying its powers by K-elements does not alter independence of distinct residue classes of exponents modulo p.

For B–B, all entries except the exceptional bottom-right entry lie in K. The coefficient of z is a three-by-three prime Fourier minor on distinct residues, hence nonzero. The determinant A+zB cannot vanish.

For C–C, only the lower-right block has the common z factor. The coefficient of z² is exactly, up to sign, the product of the upper-left two-by-two determinant and the phase-removed lower-right two-by-two determinant. The latter becomes a prime Fourier minor after nonzero row and column scalings. Both determinants are nonzero. Since 0,tq,2tq are distinct modulo p, the quadratic in z cannot vanish. This argument is valid for the stated p≥5.

### The mixed B–C case

This is the principal possible failure point, and it passes independent scrutiny.

The coefficient B of z in the determinant has precisely the displayed six-term expansion. To check the signs independently, let D_i be the unsigned two-by-two determinant deleting row i from the first pair of columns, with rows indexed from zero. Expansion along the remaining second-class column gives the coefficient (-1)^i D_i. The last-row cofactors then give

    sum_i (-1)^i D_i η^(u_i q)
      [η^(t w_2) ω^(u_i w_1) − η^(t w_1) ω^(u_i w_2)].

This agrees with the report's signed M_i convention. Every D_i is nonzero in L because both remaining u residues and both v residues are distinct modulo p.

The η exponents modulo p are the two translates of X={q u_1,q u_2,q u_3}. Each translate has three distinct elements; the translation difference t(w_2−w_1) is nonzero. If they coincided, X would be invariant under a nonzero translation of F_p. Such a translation generates the entire additive group, so a nonempty invariant subset must be all of F_p. This contradicts |X|=3<p.

A residue in their nonempty symmetric difference therefore appears in exactly one of the six summands. Upon reducing η exponents modulo p, its L-coefficient is one nonzero D_i multiplied by a root of unity. Higher base-p digits merely change those nonzero phase factors. There can be no cancellation with a term in another basis position. Hence B≠0 in K, and independence of 1 and z proves the determinant nonzero.

The use of primarity is essential to this proof: additive translation by a nonzero residue must be transitive, and the cyclotomic residue-field and tower arguments are prime-power statements. For example, {0,3,6} is a proper nonempty translation-invariant subset modulo 9. At p=3 the set X would be the whole field, so the proper-subset contradiction would disappear. These are proof-boundary controls, not asserted counterexamples to a broader theorem. The accepted statement remains p prime and p≥5.

## 4. From the minors to the side bound

If both selected sides occupy at least five residues modulo p², the selection gives a nonsingular four-by-four minor in every possible pattern pairing. The whole rectangle has rank at least four. Contraposition yields the claimed residue-occupancy restriction. Each residue class modulo p² contains exactly p indices in Z_(p³), so one side has cardinality at most 4p.

There is no unproved inference from sampled all-pattern minors, no assertion that every injective four-by-four minor is nonsingular, and no claim of the stronger 3p side bound. The exploratory sampler is correctly separated from the theorem.

## 5. N=1331 density, equality, and penalty

For an actual rank-three rectangle, transpose if necessary so a≤b. The new theorem gives a≤44 and stable rank gives b≤3993/a. Therefore

    3/a + 3/b ≥ 3/a + a/1331 ≥ 3/44 + 44/1331 = 49/484.

The monotonicity on 0<a≤44 follows because 44²<3·1331. Both the derivative argument and the report's displayed difference factorization have the correct sign. Since D/N=132/1331=12/121, the difference is exactly 1/484.

The rank-two floor is 143/1331=13/121, whose gap exceeds 1/484. The rank-at-least-four floor 4/√1331 also exceeds 49/484; the comparison can be squared because both sides are positive. Rank-one density is bounded below by 12/121.

All tile areas are positive and sum to N². Thus summing gives exactly

    cost ≥ 175692 + A_(rank≥2)/484.

A full subgroup/annihilator coset partition attains 175692. Strict slack excludes every higher-rank tile from an optimum. Equality of the remaining rank-one density inequalities forces full cosets with a minimizing divisor pair. At 11³ that pair is {11,121}; every tile has area 1331, and there are exactly 1331 tiles. This reasoning is tilewise and does not impose one common orientation on the entire tiling.

The penalty is valid without an attainment claim. The scalar corner used in the continuous estimate is nonintegral. Our independent integer search finds minimum relaxed rank-three density 67/660 at (44,90), with baseline gap 17/7260, but does not assert existence of a Fourier rank-three rectangle at that shape. The published conservative 1/484 coefficient requires no such existence claim.

## 6. Negative control and next gate

For R=C={0,p²,2p²,1}, the three-by-three leading block is all ones, so the full four-by-four matrix has rank at most three by the stated three supported rank-one pieces. The minor on {0,p²,1} is exactly −(ω−1)² and is nonzero. Because both selected sets contain 0 and 1, distinct indices give distinct projective rows and columns. The proposed three-class extension of rank-two rigidity therefore genuinely fails within cyclic Fourier matrices.

The counterexample has three repeated residues modulo p², so it does not challenge the accepted separation theorem. The three-piece refinement costs 6+4+5=15 rather than 24. No universal rank-three refinement theorem follows from this example.

The independent census reproduces the previous 25 residual lengths through 10000. Removing 1331 leaves 1859 first. At 1859=11·13², D=156 and 12N<D²<16N, so the retained rank-two and rank≥4 arguments leave rank three as the relevant unresolved obstruction. The new prime-cube lemma does not apply to this mixed-prime length. The parent general nonsquare-composite problem remains open.

## 7. Fresh exact controls

`independent_controls.py` imports no author checker and no earlier checker. Signed permutation sums are reduced exactly by the prime-power cyclotomic polynomial: a polynomial of degree below p^m vanishes at ζ_(p^m) exactly when its coefficients are constant on each fiber separated by p^(m−1). These are characteristic-zero tests. A separate SymPy polynomial-division cross-check verifies that criterion on 24 additional examples.

All fresh controls pass:

1. **44,400** exhaustive canonical first-two-digit B–B, B–C and C–C four-minor cases at p=5: 400, 4,000 and 40,000 respectively.
2. **25,300** additional exact U/A minors, covering every four-element column subset modulo 25 against each of the two fixed applicable row patterns.
3. **21,000** arbitrary-high-digit B–B, B–C and C–C minors across p=5,7,11,13,17,19,23. These controls are samples, while the proof handles all higher digits.
4. **11,000** independent coefficient identities for the mixed case, comparing the six-term formula directly against the z-coefficient extracted from the full permutation determinant. Each extracted coefficient is separately checked nonzero over Q(η).
5. **72,616** exhaustive three-subset/nonzero-translation cases over those seven primes, each with nonempty symmetric difference; and **144,507** five-element residue-multiplicity selection cases. Separate composite-9 and p=3 controls verify the exact limits of the additive-translation step.
6. **2,800** exact universal-minor checks of orders two through five at several prime-power roots, plus the **24** independent symbolic remainder cross-checks.
7. **Six** exact Fourier rank-three/four-projective-direction negative controls at p=3,5,7,11,13,17, each with its nonzero three-minor checked against the explicit polynomial −(ω−1)².
8. All **10,506** feasible integer scalar shapes with 3≤a≤44, a≤b≤1331 and ab≤3993 satisfy the published rank-three density floor. Exact rational arithmetic also verifies both other higher-rank branches.
9. The explicit **1331-tile** target coset partition covers all **1,771,561 entries exactly once**, has rank-one phase certificates and total cost **175,692**.
10. An independent divisor/prime census through **10,000** reproduces the retained old-domain residual list and the new first residual **1859**.

The completed counts and elapsed time are recorded in `RESULTS.json` and `controls.stdout.txt`. All tests supplement the proof, rather than supplying an unproved extrapolation. Frozen candidate and dependency hashes were checked again after the controls.

## Accepted next-gate wording

Accept prime-cube rank-three separation for p≥5 prime: rank≤3 rectangles in F_(p³) have one side occupying at most four residue classes modulo p² and hence min(a,b)≤4p. Its four-minor proof includes a complete mixed (3,1)–(2,2) cyclotomic coefficient argument. At N=1331, accept the exact disjoint-tile optimum 175692, rank-one-only full-coset equality, and the valid higher-rank-area penalty 1/484. The accepted-domain union now covers every length through 1858; 1859 is the next residual, still at rank three. The general nonsquare-composite problem remains open.

Preserve actual complex ranks, arbitrary Cartesian row/column subsets, disjoint/no-sharing endpoint-incidence cost, separate root/coefficient preparation, storage and I/O, and the inherited possible N extra additions for literal zero-initialized accumulation. No unrestricted Fourier-circuit, finite-field rigidity, general basis-change, sharp-penalty, production-performance, or worldwide-priority conclusion follows. Owner M-RECTANGLE-TILING remains TO RESEARCH, priority 42.
