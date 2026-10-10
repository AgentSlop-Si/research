# Complete two-Green synthesis for fixed projective directions

## Result and boundary

For a specified target B and fixed jointly compatible projective row and column directions, two invertible Green branches exist exactly when an explicit sparse linear scale system has a solution satisfying the stated nonzero, structural and cyclic-inverse guards. The resulting Green plans are recovered directly, including endpoint permutations.

This completes the fixed-direction problem. It does not select unrestricted continuous directions, prove that a passing row gate has a column completion, or decide the singular-endpoint boundary.

## 1. Fixed support patterns and directions

Work over a field E. For a permutation r, P_r is the row-action matrix (P_r x)_i=x_{r(i)}. Fix four position permutations r0,r1,s0,s1. These are fixed structural permutations even on zero-weight edges, not replaceable upper support bounds. In row i of the first inverse branch, the base and edge positions are r0(i),r1(i). In column j of the second inverse branch, they are c0(j)=s0^(-1)(j), c1(j)=s1^(-1)(j). Assume the two positions are distinct; for Hamiltonian cycles this holds at N>1.

Choose a matrix U supported on r0,r1, specifying its nonzero projective row directions, and a matrix V supported on s0,s1, specifying its nonzero projective column directions. Their individual entries may be zero, subject to the base-coordinate guards below. All directions are part of the supplied data, not unknowns solved by the scale theorem.

The unknown inverse branches have the form

    Q0=D_rho U,     Q1=V D_tau,

where every rho_i,tau_j is nonzero. Set x_i=rho_i^(-1), y_j=tau_j^(-1). The target equation is

    Q0 B Q1=Q0+Q1,

which is equivalent to

    K=UBV=U D_y+D_x V,
    K_ij=U_ij y_j+V_ij x_i.                                (S)

No factors have been commuted. Multiplication by D_x on the left and D_y on the right proves (S); multiplying back proves its converse.

If Q0,Q1 are invertible, the inverse identity is also equivalent to

    B=Q0^(-1)+Q1^(-1).

The target B need not itself be invertible for this sum theorem. An application requiring invertible B, such as the forced chirp construction, must check that additional application guard separately.

## 2. Both directional subsystems must hold

Let Z_i={r0(i),r1(i),s0(i),s1(i)}. For j outside Z_i, (S) requires K_ij=0. In terms of the selected directions, this is the joint equation

    u_i^T M_ij v_j=0,

with the two-by-two target block M_ij defined in the projective-gate report.

A projective row-gate pass only eliminates v_j pairwise from some of these equations. It is not a substitute for their joint check. Given U, recover or validate a proposed v_j by forming the two-column matrix with rows

    ((UB)_[i,c0(j)], (UB)_[i,c1(j)])

for all i with j outside Z_i. Its rank must be at most one, and v_j must lie in its common nullspace. Rank two rejects; rank one determines one projective column direction; rank zero leaves that direction free. A determined column direction with zero base coordinate fails the invertible-endpoint guard.

Symmetrically, for fixed columns v_j, each row direction must annihilate every M_ij v_j on its off-support positions. The full check K_ij=0 outside Z_i checks the supplied row and column directions together. Neither subsystem is silently dropped.

Any unresolved rank-zero column choice remains a direction-selection obligation. The scale theorem applies only after those choices have actually been specified.

## 3. Structural and inverse guards; explicit Green recovery

Define

    a_i=U_[i,r0(i)],       b_i=U_[i,r1(i)],
    d_j=V_[c0(j),j],       e_j=V_[c1(j),j].

Every a_i and d_j must be nonzero for invertible diagonal/monomial endpoints in this fixed base/edge convention. Invertibility of U or V alone does not imply this base-coordinate condition.

Set

    W0=-D_(b/a) P_r1 P_r0^(-1),
    W1=-P_s0^(-1) P_s1 D_(e/d).

Then, exactly,

    U=D_a (I-W0) P_r0,
    V=P_s0 (I-W1) D_d.                                     (G)

The relative permutation underlying W0 is r0^(-1) composed with r1; that underlying W1 is s1 composed with s0^(-1). Their cycle types must belong to the permitted grammar. For the paired Hamiltonian-cycle grammar, each must be one N-cycle. The displayed outer permutations are a canonical realization of the fixed inverse-support patterns. If the original left and right endpoint permutations are separately prescribed, use the additional compatibility check and reconstruction below; merely changing them is not permitted.

Zero edge weights are allowed. For every cycle gamma in either weighted permutation, let omega_gamma be the product of its row edge weights. The exact inverse guard is

    1-omega_gamma != 0.

For one Hamiltonian cycle there is one such guard per branch. These guards are equivalent to invertibility of I-W0 and I-W1. They, and therefore invertibility of U,V, are independent of the unknown x,y. A singular direction matrix cannot be repaired by nonzero row or column scaling.

Given a solution of (S) with all x_i,y_j nonzero, the two plans are

    T0=P_r0^(-1) (I-W0)^(-1) D_(x/a),
    T1=D_(y/d) (I-W1)^(-1) P_s0^(-1).                     (R)

Their inverses are Q0=D_(1/x)U and Q1=V D_(1/y), so (S) proves B=T0+T1. Conversely, any realization with the supplied directions and fixed inverse patterns supplies x,y satisfying (S) and all guards. Equations (S), (G), (R), nonzero base coordinates/scales, the allowed relative cycle types and the cyclic inverse guards are thus necessary and sufficient for this fixed-direction invertible-endpoint problem.

If a branch's original endpoint permutations P_L,P_R and cycle P_pi are individually prescribed, first check its base and edge support matrices equal

    P_R^(-1) P_L^(-1),    P_R^(-1) P_pi P_L^(-1).

After Q has been recovered, form Qprime=P_R Q P_L. Its support is exactly the diagonal plus the prescribed cycle. Write Qprime=D_g(I-D_w P_pi), using its nonzero diagonal base coefficients g and edge/base ratios. Then

    Q^(-1)=P_L (I-D_w P_pi)^(-1) D_(1/g) P_R.

This realizes the same operator with the original endpoint permutations and the original cycle order, not just an equivalent cycle type. It is valid because endpoint diagonals and edge weights remain free variables in this task. If those diagonal scales or edge weights are themselves prescribed, their equality is an additional guard. The verifier explicitly checks this reconstruction as well as the canonical plans (R).

Projective rescaling does not change the result. Replacing U by D_lambda U and V by V D_mu replaces a,d,x,y by lambda*a,mu*d,lambda*x,mu*y. The recovered plans remain the same.

Singular endpoint masks have no inverse Q representation in general. The earlier rejection gate extends to that boundary by projective limits, but the sufficiency theorem here makes no converse claim for such limits. A singular-mask construction requires its forward Green identity to be supplied separately.

## 4. The scale solve is an affine graph problem

The union of supports of U and V has at most 4N positions. Once all off-support entries K_ij=0 have been checked, each remaining equation is

    A x_i+B y_j=k,
    A=V_ij, B=U_ij, k=K_ij.

- If A and B are nonzero, it gives the invertible affine transition y_j=-(A/B)x_i+k/B. The reverse transition is equally valid.
- If only A is nonzero, it fixes x_i=k/A.
- If only B is nonzero, it fixes y_j=k/B.
- If both are zero, consistency requires k=0.

Make a bipartite graph on the 2N scale variables, using only two-nonzero-coefficient equations as edges. A spanning forest expresses every variable in a component as

    z_v=alpha_v t+beta_v,    alpha_v != 0.

Every remaining edge or unary equation reduces to one linear equation in t. It is either an identity, a contradiction, or a prescribed value of t. Conflicting prescribed values reject. Thus no multivariate nonlinear fitting or exponential scale search is required.

If t is fixed, directly check all variables are nonzero. If t is free, the nonzero guard forbids at most one value -beta_v/alpha_v per variable. Over an infinite field a permissible value exists. Over a finite field it exists exactly when the distinct forbidden values do not cover the field. In particular, |E| greater than the component's number of variables suffices, but that inequality must not be assumed in small fields. A returned parameter value is independently certified by substitution and the nonzero tests.

Constructing or enumerating field elements must use the supplied field representation. No root-generation or arbitrary field-element oracle is hidden in this statement. Over characteristic zero, a parameter can be found among a sufficiently long explicit list of distinct integers. Over a specified finite field, exact field-element generation and membership costs are additional implementation details. They do not require searching directions.

## 5. Cost and short certificates

Each entry of UBV uses at most four target entries because U has two entries per row and V has two per column. An unstructured complete verification therefore uses O(N^2) target-entry queries and O(N^2) field operations. The full off-support check is included in that count. A sparse representation alone does not make this verification linear time.

Given that check, the supported scale system has O(N) equations and variables. Its affine-graph elimination uses O(N) field operations, with all nonzero division guards recorded. Checking the relative permutation cycle types and constructing the two Green plans also costs O(N). Distinct forbidden-value handling can conservatively use O(N^2) comparisons; a more efficient dictionary or field-specific representation may improve it. Count any target setup, field generation and cyclic closure inversions separately.

Once recovered, each Green branch applies to arbitrary input in O(N) operations by cyclic scans, plus O(N) diagonal/permutation work. This is a useful application statement for an actually completed target. It does not supply fixed directions for a large Fourier matrix for free.

A positive certificate consists of the four support permutations, U,V, x,y, the allowed-cycle decomposition, all nonzero base/scale/closure guards, and the exact identity (S). A verifier can recover both plans from these data and check every entry or a complete algebraic identity.

A negative fixed-direction certificate may be a nonzero off-support entry; a forbidden base coefficient or cyclic guard; a cycle/unary contradiction in the affine graph; or a finite-field forbidden-parameter set covering the field. In particular, a linear inconsistency can also be supplied as a short linear combination of equations with zero left side and nonzero right side.

## 6. A nonvacuous direction pass with scale failure

Take N=5 over C or F241. Let P have row permutation [1,2,3,4,0], and Q have row permutation [2,0,3,4,1]. They are noncommuting Hamiltonian cycles. Put

    U=I-2P, V=I-3Q,
    K=U+V+E00,
    B=U^(-1) K V^(-1).

The Green guards 1-2^5 and 1-3^5 are nonzero in both stated fields. In characteristic zero det(U)=-31, det(V)=-242 and det(K)=-1625; their reductions modulo241 are nonzero as well, so this diagnostic target B is invertible. By construction UBV=K has support inside the union of U and V. Therefore the supplied row directions and supplied column directions satisfy every joint off-support equation, and every eliminated row gate passes. The fresh F241 check finds nine cleared row relations and a rank-one column nullspace in each of the five columns, so this direction pass is nonvacuous.

Nevertheless three supported equations force

    (0,2): -3 x0=-3,   hence x0=1,
    (4,0): -2 y0=-2,   hence y0=1,
    (0,0): x0+y0=3.

They are inconsistent. Subtract the first two normalized equations from the third to obtain 0=1. This is a fixed-direction failure after both directional subsystems pass, not a statement that B lacks every possible two-Green representation with different directions.

## 7. Constructed positive recovery and guard controls

The fresh verifier constructs positive targets from known valid Green plans, forgets their scales, and recovers them using only the fixed directions and scale equations. It checks the recovered plans entrywise and applies their cyclic-scan implementations to every basis vector. The controls include noncommuting cycles, monomial endpoints and zero edges. These are deliberately constructed targets, not claimed Fourier factorizations or a search for unrestricted parameters.

It also tests the preceding N5 direction-pass/scale-failure example; base-coordinate and singular-direction guards; and finite-field exclusion of all free-parameter values. For example, over F2, U=V=I and B=I give x_i+y_i=1, but the only nonzero choices x_i=y_i=1 violate the equation. The linear system alone is consistent; the nonzero-scale requirement is decisive. Over an extension with more than two elements that particular obstruction disappears.

The 12 constructed positive targets are at N=5,8,9, all with noncommuting cycles; six have monomial endpoints and six have zero edges. Recovery verifies 680 target entries and 88 complete basis-vector outputs by the actual Green scans. Each case also checks projective gauge invariance and exact reconstruction retaining individually prescribed endpoint permutations and cycle orders. Exact instance data, recovered scales and failure certificates are in FIXED_DIRECTION_RESULTS.json.

Provenance: the projective consistency predecessor is PROJECTIVE_CONSISTENCY_GATE.md. The initial scale identity was communicated by construct_bank_interface_certificate and independently derived here with its permutations and structural guards. This is a bounded construction extension, not an independent review of that agent's F8 factor targets. No uploaded program is executed and no unrestricted direction-search claim is made.
