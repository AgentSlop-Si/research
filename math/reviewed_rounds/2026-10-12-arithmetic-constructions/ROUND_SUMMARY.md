# Reviewed arithmetic constructions and exact obstructions

12 October 2026

This round advances five specific research obligations. Independent project reviews accepted the scoped results below. Earlier accepted results remain identified dependencies; these reviews are not external peer review or historical-priority determinations.

## Exact prefix optimization for one finite group

For all labeled element orderings of D8×C5×C7, with D8 of order eight, the sum, over nonempty prefixes, of (left-stabilizer size minus one) has maximum 884. Requiring the proper-prefix stabilizers to generate the whole group lowers the maximum to 814, a sharp deficit of 70. The full prefix contributes once and does not make the generation condition automatic. The unrestricted maximizers are exactly recursive maximal-subgroup right-coset block orders, with an exact labeled-count recurrence. Both maxima have verified attaining witnesses. Other prime pairs 5≤p<r and the complete classification/count of full-escape maximizers remain open. [Review](prefix-d8-c5-c7.md)

## Another pinned Fourier-target slice excluded

In the original pinned Phase42 N=8 chart, vary only stage-1 edge gains (8,9,12) by unit-complex multipliers. Keep every other phase and all tree-pinned gains fixed, both three-Green sums unweighted, the original cycle masks, product order S2S1, no interstage diagonal, and all six inverse guards nonzero. No point in this slice is equivalent to F8 under invertible complex row and column monomials. Accepted coverage is now 131 of 5,984 three-coordinate slices, leaving 5,853 unclassified. The full 34-phase target fiber remains open. [Review](q27-stage1-8912.md)

## Three base-field Green terms for the original five-dimensional block

For positive odd q, coprime to 5 and congruent to 1 modulo 241, the original five-dimensional principal block C_q of B_N, N=5q², has a three-term construction over Q(eta), where eta has order five. Each term is a diagonal-ended cycle resolvent L(I−W)⁻¹R in the original coordinates. The three structural cycles are distinct; zero edge weights are permitted. The third branch is a one-edge nilpotent resolvent containing both the necessary off-diagonal correction and the entire diagonal calibration. The new upper bound and inherited two-term lower bound give minimum three over the base field.

This completes only the original five-dimensional base-field upper alternative. Full growing B_N and negative-sign upper bounds remain open. The attribution review identifies classical weighted-cycle, state-space-correction and rank-one spectral-assignment ingredients; the arithmetic-family guard proof supplies the specific certified combination. Priority remains unresolved. [Mathematical review](q11-base-field-three.md) · [Attribution](q11-attribution.md)

## Rogers–Szegő overlap completed for b equals eleven

The new result proves the overlap discriminant nonzero for every integer size A≥1 and every primitive root of odd order 25≤d≤89. The normalized polynomial is J_(A+1)(x;τ)=x He_A(x)−Aτ He_(A−1)(x), with monic probabilists’ Hermite polynomials and τ fixed by the original b=11 Rogers–Szegő data. A residue-field argument handles d=25; complementary conjugate witnesses handle d=27; exact outer-annulus witnesses cover the remaining orders.

Together with the inherited lower strip and tail, this completes the b=11 overlap family for all odd d>11 in characteristic zero. Intermediate-overlap gaps remain for odd b≥13; ordinary-squarefreeness gaps remain for odd b≥27, except separately proved instances. The residue criterion is an explicit local-arithmetic consequence of classical quasi-Laguerre discriminant and Hermite congruence identities plus a unit argument. Historical priority remains unresolved. [Mathematical review](rs-b11-overlap.md) · [Attribution](rs-b11-attribution.md)

## Certified deterministic bucket arithmetic

The accepted finite-word stage covers n=2^m, B=2^b, 2≤b≤m, q≥10 and support width w=16Bq+1<n, using reflected signed taps h_t=a_|t|/2^p with p=q+ceil(log2 w)+6 and |h_t|<1/2, bounded rational samples, stable sample access, odd permutation multiplier and integer translation. Under the reviewed precision schedule, the error is simultaneously at most (15/64)2^−κ for all B outputs. The negative-DFT normalization is explicit: nU has unnormalized Fourier-convolution units; target error 2^−k in those units requires κ=k+m.

HIKP response guarantees require trusted accepted tap provenance: a caller-supplied self-hash does not establish it. Essential dimensions are recomputed from validated parameters; redundant JSON fields are ignored rather than authenticated. Prepared values are trusted, unmodified objects from the same process. Preparation, sample acquisition and actual JSON parsing memory remain charged. Ranking, support recovery, estimation, randomness, outer-loop success and the complete sparse engine remain open. [Review and interface clarifications](q16-bucket-arithmetic.md)

These results establish the stated constructions, exclusions and arithmetic guarantees. They do not establish a general FFT breakthrough, practical speed advantage, or worldwide-first claim.
