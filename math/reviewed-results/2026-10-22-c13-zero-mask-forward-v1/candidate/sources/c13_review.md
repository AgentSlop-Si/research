# Independent review: fixed-direction two-Green completion

10 October 2026 UTC. Verdict: accepted as a necessary-and-sufficient completion theorem for supplied projective row and column directions, fixed structural permutations, free endpoint diagonals/edge weights, and invertible branches. It does not solve unrestricted direction selection or establish a converse for singular endpoint limits.

## Scale identity and obligations

With Q0=D_(1/x)U and Q1=V D_(1/y), multiplication of Q0 B Q1=Q0+Q1 on the left by D_x and right by D_y gives exactly

    UBV=U D_y+D_x V.

All x_i,y_j must be nonzero. Conversely that equation and invertibility of Q0,Q1 give B=Q0^(-1)+Q1^(-1). B itself need not be invertible for this sum theorem. Invertibility of a forced feedback target is a separate application guard.

The row-pair gate only eliminated column directions. Given row directions, every column must still have a common null direction for all off-support equations; rank two rejects, rank one fixes that direction, and rank zero leaves a choice. A fixed-direction completion certificate must supply the actual choice. Computing every entry of UBV and checking every off-support zero jointly validates those choices. Neither a row-gate pass nor a collection of independent pairwise nullspaces replaces this test.

The union of the two inverse supports has at most4N entries. Each UBV entry uses at most four target entries. Thus the complete unstructured verification costs O(N^2) target queries/field work, after target setup; only the subsequent supported scale system is sparse. The source correctly charges this full off-support stage.

## Relative permutations and exact Green recovery

Let a_i=U[i,r0(i)], b_i=U[i,r1(i)], d_j=V[s0^(-1)(j),j], e_j=V[s1^(-1)(j),j]. All a_i,d_j must be nonzero. An invertible direction matrix alone does not ensure those base coordinates are nonzero.

With row-action permutation matrices, the two denominator factorizations are

    U=D_a(I-W0)P_r0,
    W0=-D_(b/a)P_r1 P_r0^(-1),
    V=P_s0(I-W1)D_d,
    W1=-P_s0^(-1)P_s1 D_(e/d).

The relative permutations are r0^(-1) composed with r1, and s1 composed with s0^(-1), respectively. The different orders and placement of the diagonal in W1 are necessary. For every permitted cycle, its row-weight product must differ from one. These guards, and the invertibility of U,V, do not depend on x,y. Nonzero scaling cannot repair a singular direction matrix.

The recovered plans are

    T0=P_r0^(-1)(I-W0)^(-1)D_(x/a),
    T1=D_(y/d)(I-W1)^(-1)P_s0^(-1).

Their inverses are the required Q0,Q1. Thus the full scale identity, nonzero scales/base coordinates, cycle-type restrictions and denominator guards are sufficient as well as necessary in this fixed-data problem. Zero edge weights are allowed.

The structural permutations are fixed even at zero-weight entries, as clarified in the reviewed final snapshot. If instead they were merely replaceable upper support bounds, a zero-weight edge could admit a different Hamiltonian completion; the stated cycle-type guard would then not be a necessary matrix-membership test. That is a different search problem.

## Prescribed original endpoints

If the original endpoint permutations P_L,P_R and cycle P_pi are separately fixed, first check the base and edge support matrices P_R^(-1)P_L^(-1) and P_R^(-1)P_pi P_L^(-1). Given recovered Q, form Qprime=P_R Q P_L. Its diagonal base g must be nonzero, and its edge/base ratios determine W on the prescribed cycle. Then

    Q^(-1)=P_L(I-W)^(-1)D_(1/g)P_R.

This realizes the original permutations and order, rather than replacing them by merely conjugate patterns. It is valid because the endpoint diagonals and edge weights remain free; if those values are also prescribed, equality to them is an additional condition. Independent projective rescaling U->D_lambda U and V->V D_mu changes x,y by the corresponding factors and leaves the recovered plans unchanged.

The entire inverse representation assumes invertible branches/endpoints. The earlier projective gate may reject a singular-endpoint boundary through homogeneous limits, but its passing limit directions do not satisfy a converse construction theorem here. A singular-mask positive construction must supply its forward identity separately.

## Affine graph solver and finite fields

Each supported equation has the form A x_i+B y_j=k. Two nonzero coefficients give an invertible affine transition. One nonzero coefficient pins a variable; two zero coefficients require k=0. A spanning forest writes every variable in a connected component as alpha_v t+beta_v with alpha_v!=0. Remaining equations become identities, contradictions or one forced parameter value, with conflicting values rejected. This uses O(N) field operations for the supported system.

If the parameter is fixed, test every variable for nonzero. If free, exclude each value -beta_v/alpha_v. An infinite field always has an allowed choice. In a finite field there is a choice exactly when these distinct forbidden values do not cover the field; ordinary linear consistency alone is insufficient. Field-element generation, membership and deduplication require the supplied representation. A conservative O(N^2) comparison budget is explicitly retained, and no field-size or root-generation shortcut is hidden.

The source's F2 example is valid: x+y=1 has linear solutions but none with both variables nonzero. Over F4, t and t+1 are a nonzero solution; our control also gives the separate F3 solution(2,2). This distinction is checked rather than treating the original field and its extensions as interchangeable.

## Nonvacuous direction-pass/scale-failure certificate

For the specified N5 cycles, U=I-2P,V=I-3Q and K=U+V+E00 give B=U^(-1)K V^(-1). Independent exact determinant evaluation gives det U=-31, det V=-242, det K=-1625; all are nonzero over C and modulo241. UBV has no forbidden off-support entries, all nine eliminated row relations pass, and each of the five column nullspace tests has rank one.

Nevertheless the supported equations force x0=1 from(0,2), y0=1 from(4,0), and x0+y0=3 from(0,0), giving0=1. This excludes only those supplied directions, not every representation of the diagnostic B. A separate one-entry target perturbation produces a nonzero off-support residual, demonstrating why that complete check cannot be omitted.

## Independent controls

Twelve newly generated noncommuting targets at N5,8,9 recover all680 matrix entries and88 complete basis outputs using reviewer-authored cyclic scans. Six have nontrivial endpoint permutations and six have zero edge weights. Every case verifies canonical recovery, the original endpoint permutations/cycle orders, and projective gauge invariance. Additional controls retain an invertible zero-base direction, a singular cyclic denominator, the nonvacuous N5 contradiction, an off-support failure and finite-field exhaustion. The affine solver matches exhaustive nonzero assignments for144 bounded systems over fields2,3,5.

No uploaded or constructor program was imported or executed. The clarified source snapshot, deterministic results, standalone standard-library checker, isolated replay and immutable manifest are included. Earlier seals remain unchanged.
