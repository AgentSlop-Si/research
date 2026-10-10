# Phase41 × accepted F018: fixed-branch ceilings

Date: 2026-10-10. This note adds a separately reviewable corollary without editing either frozen manuscript. It uses the accepted F018 theorem in `research_cycle_0958/matrix/final_v1/CORE_THEOREMS_SECOND_AUDIT.md` §2, with full proof in `research_finalization_0923/matrix/FINAL_THEOREMS.md` Theorem2A.

## Exact contract and matching

For r≥1, let G_s=(I−W_s)^−1, where each W_s is an arbitrary weighted Hamiltonian-cycle successor matrix and every required inverse exists. Weights may have arbitrary nonzero complex amplitudes. Let E_s,H_s be independently chosen permutation-contained endpoints, which may include scalar coefficients and zero entries. Suppose

F_N = L P [sum_(s=1)^r E_s G_s H_s] Q R

with arbitrary invertible complex diagonal L,R and arbitrary permutations P,Q. Branch endpoints need not be unitary. The sum has one inverse per branch; products of sums are not being substituted for this model.

Set Q_s=I−W_s. Each Q_s is invertible and has at most two nonzero entries in every column. The accepted F018 theorem therefore supplies q=2 weighted half-separators for its symmetric bipartite support lift. This property concerns the actual Q_s support, rather than an unproved separator claim about the dense inverse. The endpoints

L_s=N^(−1/2) L P E_s, R_s=H_s Q R

still have permutation-contained support. Thus the normalized complex Fourier target U_N=N^(−1/2)F_N is exactly sum L_s Q_s^−1 R_s and satisfies every hypothesis of accepted F018.

## Corollary P41-S: fixed-r obstruction, including the amplitude route

Every such equality requires

N ≤ 2r·9^r + 2(3^r−1).

This is a direct application of the accepted theorem, not a newly asserted all-circuit lower bound. In particular:

- r=2: N≤340 for arbitrary admissible complex edge amplitudes and arbitrary independently routed complex endpoints.
- r=3: N≤4426 for that same general endpoint/amplitude model.
- For the narrower two-unit-gain family, Phase41 sharpens the r=2 cutoff from340 to8, including independently unitary monomial branch decorations and arbitrary external complex monomials.

Consequently the finite three-phase-cycle local Jacobian witnesses at N=8,16,32,64 do not imply that a fixed three-cycle sum can solve the full Fourier problem for arbitrarily large N. The entire r=3 one-inverse-per-branch route is already excluded for N>4426, even if phase-only gains are relaxed to arbitrary nonzero complex amplitudes and endpoints. Similarly, the two-amplitude dominance witnesses through N128 do not make that fixed-two-summand family an all-N route; it is excluded for N>340 by F018.

A uniform exact representation staying in this independently routed inverse-sum architecture must have r growing at least on the order of log N. This is a structural branch count, not by itself a general arithmetic-operation lower bound: coefficient generation, branch sharing, alternative circuit representations and evaluation costs must be analyzed separately. Products, deeper noncommuting circuits and dense preconditioners are not silently covered by this sum theorem.

If an additional free diagonal D is explicitly allowed, the separate accepted cutoff is

N ≤ 8r·9^r + 4(3^r−1) + 2.

It yields1330 for r=2 and17602 for r=3. Do not use the sharper no-D numbers for that different architecture. The Phase41 eight-value argument likewise has no free additive diagonal term.

## Supported implication and unresolved questions

This conjunction closes the claim that moving from two phase cycles to a **fixed three-cycle sum** supplies an unrestricted all-N escape. It does not reject actual full Fourier solutions at the smaller sizes permitted by the respective ceilings. Those exact target fibers remain open. No claim is made that340 or4426 is sharp, or that a fixed nonzero approximation tolerance forces logarithmically many branches.
