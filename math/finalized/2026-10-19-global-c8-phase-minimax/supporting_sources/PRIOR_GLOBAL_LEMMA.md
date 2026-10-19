# The remaining global spectral anti-concentration lemma

This is an exact unresolved lemma, not a theorem established by this packet.

## Lemma that would finish the sharp minimax

For all diagonal unitary A and B of order 8, every open arc of angular length π/4 on the unit circle contains at most five eigenvalues, counted with multiplicity, of

    M=F₈ A F₈ B.

A proof would combine with the accepted upper witness to give δ=sin(π/16). An exact pair A,B whose M has six eigenvalues in such an arc would refute that proposed value. The accepted witness has six eigenvalues on the endpoints of a closed arc of width π/4, so the open/closed distinction matters.

## Exact equivalence

For V=PF₈Q and W=VᵀV,

    W=QF₈P²F₈Q,
    Q⁻¹ W Q=F₈P²F₈Q²=M,
    (Im V)ᵀ Im V=(I−Re W)/2.

W is symmetric unitary. Its real and imaginary parts commute and are simultaneously real-orthogonally diagonalizable. Therefore its eigenvalues e^{iθ_j} correspond to imaginary singular values |sin(θ_j/2)|.

Thus σ₃(Im V)<sin(π/16) holds exactly when at least six eigenvalues of M lie in the open arc |arg λ|<π/8. The map (P,Q)↦(A=P²,B=Q²) is surjective onto all diagonal unitary pairs. Multiplying A by a scalar unitary rotates all eigenvalues and centers any proposed arc. The lemma is consequently equivalent to the missing sharp global bound, without restricting phase components or using a phase grid.

## Equivalent diagonal approximation of a unitary Hankel matrix

Let C=F₈AF₈, so

    C[j,k]=(1/8) Σ_{l=0}^7 a_l exp(−π i (j+k)l/4).

C is a symmetric unitary cyclic Hankel matrix. Conversely every such unitary cyclic Hankel matrix has this representation. Set D=B⁻¹. Then

    W−I=Q(C−D)Q,
    σ_j(C−D)=2 σ_j(Im V).

The same missing assertion is

    σ₃(C−D) ≥ 2 sin(π/16)

for every symmetric unitary cyclic Hankel C of order 8 and every diagonal unitary D. This exposes the global structured low-rank approximation obstruction: no unitary Hankel matrix in this family can approach a diagonal unitary by a rank-two correction with operator error below 2 sin(π/16).

## Status after the new mechanism

The positive dual-weight second-variation certificate in `PROOF.md` excludes all sufficiently small unrestricted perturbations of the accepted witness. The quantitative energy plus angular-perturbation argument gives a uniform explicit lower bound about 0.04385 everywhere on the torus. Neither statement controls the entire spectral anti-concentration family above. In particular, local stability is not a reduction of all global minimizers to the periodic sector.

No global spectral-arc theorem, invariant forcing all minimizers into the periodic sector, exact counterexample, CAD/quantifier elimination, or Positivstellensatz emptiness certificate was completed. The sharp unrestricted minimax remains open.
