# Fourier-8: an exact noncommuting coefficient chart and a bounded anchor test

Status: the eight anchor charts specified below are excluded by exact arithmetic over Q(zeta_8). The unrestricted two-layer problem remains open. No length-8 positive kernel is claimed. This work is separate from the nonlinear constructor's length-16, three-layer, eight-order coefficient problem.

## 1. Complete two-layer coefficient budget

Fix four Hamiltonian cycles pi_(l,t), l=1,2 and t=0,1, on eight coordinates. Their permutation matrices satisfy P_pi e_j=e_pi(j). A branch with nonsingular diagonal endpoints is equivalently the inverse of

    Q_(l,t)=diag(a_(l,t))+diag(b_(l,t)) P_pi(l,t).

There are exactly sixteen scalar coefficients per inverse branch and sixty-four for four branches. This representation retains arbitrary varying edge masks and both diagonal endpoints: if T=L(I-W)^(-1)R, then T^(-1)=R^(-1)(I-W)L^(-1) has this support. Conversely,

    Q^(-1)=(I-diag(w)P_pi)^(-1) diag(a^(-1)),
    w_i=-b_i/a_i.

The guards are, for every branch,

    all a_i != 0,
    delta=prod_i a_i - prod_i b_i != 0.                  (1)

The Green denominator guard is delta/(prod a). Requiring all edge masks nonzero additionally requires every b_i != 0. Allowing some zero masks enlarges the chart; the bounded rejections below allow them. Nonsingular diagonal endpoints remain required.

The desired full identity is

    F_8=(Q_(2,0)^(-1)+Q_(2,1)^(-1))
        (Q_(1,0)^(-1)+Q_(1,1)^(-1)).                    (2)

This is sixty-four rational coefficient equations with four determinant guards and thirty-two base-coordinate nonzero guards. A fraction-free equivalent lift introduces two 8 by 8 matrices X_1,X_2 and imposes

    Q_(l,0) X_l Q_(l,1)=Q_(l,0)+Q_(l,1), l=1,2,
    X_2 X_1=F_8.                                       (3)

There are 192 scalar variables including the 128 auxiliary entries and 192 scalar equations, with the same guards (1). The first identities uniquely determine X_l from guarded Q branches. The product then implies both X_l invertible. No generic dimension count decides solvability. An eight-parameter interstage diagonal gauge X_1 -> D X_1, X_2 -> X_2 D^(-1) preserves the support grammar; it is a gauge, not an evaluation algorithm.

Endpoint permutations other than the explicitly fixed support pattern are not included in a chart by implication. They require their own support tables. A supplied arbitrary factor or a dense solve for (3) is not charged as free setup.

## 2. Constructive scale completion after directions are known

For one specified target B, seek B=Q_0^(-1)+Q_1^(-1). Suppose U contains specified nonzero row directions for Q_0 and V contains specified nonzero column directions for Q_1, in the required two-permutation supports. Write

    Q_0=D_rho U,       Q_1=V D_tau,
    x_i=rho_i^(-1),    y_j=tau_j^(-1).

Then the full inverse-branch identity is equivalent to the linear scale system

    (U B V)_(i,j)=U_(i,j) y_j+V_(i,j) x_i.              (4)

Proof: substitute into Q_0 B Q_1=Q_0+Q_1 and multiply by D_rho^(-1) and D_tau^(-1).

Thus, once both families of directions are actually supplied, scale completion is a linear system in 2N variables, not another nonlinear fitting task. All x_i,y_j must be nonzero, U,V must be invertible, and every coefficient on the prescribed base permutation must be nonzero. These conditions recover legal Green branches through (1). A positive solution must still be checked in the full identity.

The column directions are not obtained for free from pairwise row tests: each must annihilate every applicable off-support row equation simultaneously. The projective gate only provides necessary consistency until that restoration is done. In the diagonal-base chart there are at most 3N supported scale equations, but all off-support entries must also vanish. With supplied target entries, a direct recovery/check can cost O(N^2) target-entry work and ordinary linear algebra for 2N unknowns; a generic O(N^3) scale solve is a safe charge. This is coefficient construction cost, not Fourier application cost. At a fixed N=8 it is constant-size work.

## 3. Two explicit legal radix-2 anchors

Let zeta=zeta_8 and F_8[i,j]=zeta^(ij). For each of the following pairings, let K act as [[1,1],[1,-1]] on every pair:

- Adjacent pairs: (0,1),(2,3),(4,5),(6,7).
- Half pairs: (0,4),(1,5),(2,6),(3,7).

Each K is one allowed paired-Green layer with nonzero masks. For pairs (a_i,b_i), use Hamiltonian orders

    b_0,a_0,b_1,a_1,... and a_0,b_0,a_1,b_1,... .

Keep only the matching edges b_i -> a_i in the first order and a_i -> b_i in the second. Their weights are respectively 1/2 and -1/3. All connecting edges are zero, so both denominator guards are 1. The left endpoints are 2I for the first branch and diag(-1 on a_i, -3 on b_i) for the second; right endpoints are I. Direct expansion gives K. There are four genuinely nonzero masks per branch and no singular endpoint.

Since K^2=2I, fixing X_1=K forces the other target to be

    B=F_8 K/2.                                          (5)

This is a genuine specified-factor test. It does not apply the two-term projective gate directly to an unspecified two-layer product.

## 4. Four predeclared noncommuting order pairs

The second factor is tested only at these orders, written as cyclic visit lists:

    natural      = [0,1,2,3,4,5,6,7]
    bit_reverse  = [0,4,2,6,1,5,3,7]
    evens_odds   = [0,2,4,6,1,3,5,7]
    gray         = [0,1,3,2,6,7,5,4]

The four pairs are (natural,bit_reverse), (natural,gray), (evens_odds,gray), and (bit_reverse,gray). Their permutation matrices genuinely fail to commute, verified directly. The bounded test consists of these four pairs times the two fixed anchors: eight charts total. No edge-weight or endpoint parameter grid, numerical optimization, or broader permutation enumeration is used. Each remaining factor has its full thirty-two scalar inverse-branch coefficients unrestricted, including varying masks; these charts are not constant-coupling tests.

## 5. Exact rejection certificates

For row i of Q_0, the two positions are i and pi^(-1)(i); for column j of Q_1 they are j and sigma(j). If j lies outside the union of the two branch supports in rows i and k, the two off-support equations eliminate the column direction and give

    u_k^T L_(i,k,j) u_i=0.

Writing the corresponding target blocks as [[A,C],[B,D]] and [[E,G],[F,H]], put

    H_(i,k,j)=[[AH-CF, BH-DF],[-AG+CE, -BG+DE]].

When its determinant is nonzero, u_k is proportional to H_(i,k,j) u_i. The inverse-direction propagation uses its adjugate, so no unrecorded field division is needed. A spanning forest gives u_i proportional to T_i z. Internal equations then become homogeneous binary quadratics in z. Two return matrices whose commutator has nonzero determinant have no common eigenline, providing a short exact rejection certificate.

Results:

- Adjacent anchor, all four order pairs: exact nonzero commutator determinants reject the projective direction subsystem.
- Half anchor, (natural,gray): one internal equation forces the root to a coordinate axis and another excludes it. The two other mixed pairs, (evens_odds,gray) and (bit_reverse,gray), have simultaneous nonzero multiples of x^2 and y^2. These three direction subsystems are inconsistent.
- Half anchor, (natural,bit_reverse): the root must satisfy x y=0. Both coordinate axes satisfy the internal quadratics, but one makes every odd row's base coefficient zero and the other makes every even row's base coefficient zero. This violates the nonsingular diagonal-endpoint requirement before scale completion.

Accordingly all eight stipulated charts are excluded over Q(zeta_8) and every extension, including C. The last chart's rejection specifically uses nonsingular endpoints; the report does not assert the same conclusion for singular endpoint masks in that chart. The other seven rejections already exclude nonzero projective row directions.

Every integer coefficient is stored in the basis 1,zeta,zeta^2,zeta^3, with zeta^4=-1. This is exact characteristic-zero arithmetic, not a finite-field-only inference. The JSON records source triples, transition matrices and ranks, forest paths, internal quadratics, base-coordinate failures, and the commutator certificates. The verifier constructs its target entries directly from (5); it scales B by 2 only for the homogeneous off-support gate, which does not alter those equations.

Four additional positive controls use true sums of constant-mask Green operators, with weights 2 and 3 on each tested pair of Hamiltonian orders. Every extracted cleared equation vanishes on their genuine row direction (1,-2), and none is falsely rejected. Their guards are 1-2^8 and 1-3^8, both nonzero.

## 6. What remains open and what a positive kernel would cost

These failures do not exclude a free first layer in the sixty-four-coefficient system (2), other order pairs, nontrivial endpoint permutations, or other admissible charts. No conclusion follows from the parameter count alone. The previously sealed F_4 one-layer positive kernel and its field/guard qualifications are unchanged.

Applying four supplied length-8 Green branches costs O(8) arithmetic by guarded cyclic recurrences; discovering and representing their coefficients is a separate charge. A local length-8 cyclic construction would still need an explicit full-N Hamiltonian batch lift. A direct sum of 8-cycles does not satisfy a single Hamiltonian N-cycle requirement. Thus a local kernel alone would be a finite/constant-factor result, and it cannot yet be used as the N64 swapped-interface exterior.

## 7. Dependencies and files

The projective necessary equations and spanning-forest method come from the separately authored PROJECTIVE_CONSISTENCY_GATE.md in the projective_row_gate package. This report re-derives the needed formulas, runs a restricted exact shortcut plus axis tests, and does not claim to implement the full 2-SAT solver. The scale-completion identity (4) was independently checked by that constructor. No uploaded program was executed.

Companions: verify_fourier8_noncommuting_anchors.py, FOURIER8_NONCOMMUTING_ANCHOR_CONTROLS.json, and FOURIER8_NONCOMMUTING_ANCHOR_SHA256SUMS.txt.
