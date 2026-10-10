# Q25 independent review and operator-gap sharpening

10 October 2026. Source reviewed as inert mathematical text: `novelty_catalogue_0825/library_delta_extracted/fft_hero0_phase17_two_sided_gauge_2026-10-10/fft_hero0_phase17_two_sided_gauge/THEOREMS.md`. No source program was executed or imported.

## Accepted scope

The paired monomial Fourier classification (17.1), the exact arbitrary-invertible-diagonal obstruction for even s>=4 (17.2), the rank-four phase-ratio spectrum (17.3), the metric floor for unitary diagonal endpoints (17.4), the fixed-gauge Frobenius projection (17.5), and the uniform rank/edit bound (17.6) are accepted. The s=2 exception and the unitary restriction for numerical gaps are essential.

The generic full-rank statement in section 5 initially depended on the earlier identity-gauge full-rank theorem. This dependency is now closed by independently reading and checking the complete all-size polyphase proof in `intake_audit/PROOFS_AND_DISPOSITIONS.md` Section2.1: a fixed-point-free monomial W has W² equal to +i or -i and W⁴=-I, with all four primitive eighth roots equally represented. Thus the Fourier commutator has full rank at every even s, and the rational-function genericity deduction follows. Fresh floating-point controls supplement this proof but are not its basis.

## Independent spectral derivation

Set n=N/2 and rho=2/(s sin(pi/s)). Write the phase-ratio matrix as H=n A B^T, indexed by the four sign pairs (e,f). After diagonal rephasing its two Gram matrices are I+rho X and I+rho Y, where

X=[[0,1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,-1,0]],
Y=[[0,0,1,0],[0,0,0,-1],[1,0,0,0],[0,-1,0,0]].

Direct multiplication gives X²=Y²=I and XY=YX. Moreover tr X=tr Y=tr XY=0. The four joint (+,+),(+,-),(-,+),(-,-) eigenspaces each have dimension one, by the projectors (I±X)(I±Y)/4. Thus the Gram product eigenvalues are (1+rho)², 1-rho², 1-rho², (1-rho)², proving the claimed singular values without a supplied symbolic certificate. The geometric-sum overlap has modulus rho; its sign reverses between the two half-grid classes. Because s>=4, 0<rho<1.

If Q,R are the two diagonal-unitary conjugates of the involution and U is unitary Fourier, the source computes E=UQ-RU and proves

||E||_F² >= N(1-rho),   ||E||_2 <= 2.

Both follow directly from the rank-four norm and the triangle inequality. If T=T_g+Delta with T_g Q=R T_g and rank Delta<=k, then Z=Delta Q-R Delta has rank <=2k. Eckart–Young therefore gives

||E-Z||_F² >= max(0,N(1-rho)-8k).

Since E-Z=(U-T)Q-R(U-T), its Frobenius norm is at most 2||U-T||_F. Division by 4N proves the source's Frobenius and operator floors. This applies to arbitrary Delta; no bound on its entries or condition number was assumed.

## New small sharpening for operator norm

For 0<=2k<N, there are N-2k singular values in the tail after the first 2k. Their squared sum is at least N(1-rho)-8k, since each removed squared singular value is at most four. Consequently

sigma_(2k+1)(E)² >= max(0,[N(1-rho)-8k]/[N-2k]).

Every rank-at-most-2k approximation Z has operator error at least sigma_(2k+1)(E), while ||E-Z||_2<=2||U-T||_2. Thus the valid strengthened floor is

||U-T||_2 >= (1/2) sqrt(max(0,[N(1-rho)-8k]/[N-2k])).

For 2k>=N, use zero as the bound. The Frobenius lower bound remains the source expression. The exact equality threshold k>=ceil(N(1-rho)/8) is unchanged. This is an elementary refinement of the same singular-value argument, not a claimed novel principle.

## Edits and bridge interpretation

For a diagonal bridge B, changing one entry in each asymmetric involution pair gives an invertible commuting B0 and rank(B-B0)<=k. Multiplication by surrounding factors cannot increase rank. For an occurrence-wise resolvent perturbation, the resolvent identity proves rank of the difference <=rank of the changed weighted entry, provided both endpoint inverses exist. A multilinear sum/product circuit can be telescoped occurrence by occurrence. All intermediate inverse instances used in that interpretation must remain legal; singular intermediate inverses cannot be silently traversed.

These are restricted representation and approximation barriers. Theta(N) symmetry-breaking edits can still have O(N) representation/application cost. No unrestricted Fourier circuit lower bound follows.

## Fresh controls

`fresh_two_sided_gauge_control.py` was written independently in this review. It checks the rank-four spectrum and random unitary-gauge/rank-perturbation metric floors at seven sizes including the s=2 degeneracy. All 21 metric controls passed; maximum error in the four singular values was below 2.2e-14. This is floating-point falsification evidence only, not an all-size proof or source-code replay.
