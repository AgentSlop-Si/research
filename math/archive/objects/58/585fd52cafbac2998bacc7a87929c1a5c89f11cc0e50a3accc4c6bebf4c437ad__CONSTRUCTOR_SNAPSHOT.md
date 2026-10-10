# A polynomial-size projective consistency gate for two-Green sums

## Result and scope

For any chosen collection of the cleared two-Green row-pair equations, there is an exact polynomial-size test for the existence of all shared row directions over an algebraic closure. It uses:

1. an invertible-transition spanning forest;
2. degree-at-most-two common-root tests within its components;
3. a 2-SAT instance for the rank-one transitions between components.

It keeps zero coefficients, projective infinity, singular transitions, repeated roots, and singular endpoint masks. It never fits Green weights. Rejection proves that the target has no two-Green realization with the specified support patterns, even after extending the coefficient field. Acceptance solves only this selected row-direction subsystem. Column directions, supported-entry scale equations, denominator guards, and the full matrix identity still remain.

The gate is not a faster Fourier algorithm and does not itself claim a new lower bound for every cycle pair. Its useful extension of the N=5 example is that global row consistency can be tested without enumerating projective branches exponentially.

## 1. Exact input equations

Let T0,T1 be two invertible proposed branches, Q0=T0^(-1), Q1=T1^(-1). Their sum equals a target B only if

    Q0 B Q1 = Q0 + Q1.                                      (1)

This orientation is important: Q0(T0+T1)Q1=Q1+Q0. It does not require B itself to be invertible.

For fixed diagonal/monomial-ended weighted-permutation Green plans, each Q has at most two structural entries per row. Write the two positions of row i of Q0 as r0(i),r1(i), with coefficients a_i,b_i. Write the two position permutations of Q1 as s0,s1. In column j of Q1 the two possible row positions are c0(j)=s0^(-1)(j), c1(j)=s1^(-1)(j), with a nonzero projective coefficient pair v_j when Q1 is invertible. Set u_i=(a_i,b_i)^T.

For each row i, positions outside {r0(i),r1(i),s0(i),s1(i)} have zero right side in (1). For two rows i,k and a column j outside both of those structural sets, define

    Mi=[[B[r0(i),c0(j)], B[r0(i),c1(j)]],
        [B[r1(i),c0(j)], B[r1(i),c1(j)]]],
    Mk=[[B[r0(k),c0(j)], B[r0(k),c1(j)]],
        [B[r1(k),c0(j)], B[r1(k),c1(j)]]].

Then u_i^T Mi v_j=u_k^T Mk v_j=0. Eliminating the nonzero v_j gives one homogeneous bilinear equation

    u_k^T L_e u_i=0.                                        (2)

Writing Mi=[[A,C],[B,D]], Mk=[[E,G],[F,H]], its coefficient matrix is

    L_e=[[AG-CE, BG-DE],
         [AH-CF, BH-DF]].

This derivation divides by no coefficient or minor. It retains zero edge weights and every singular 2×2 target block. Repeated row-pair/column choices give a multigraph of equations, not independent copies of a row variable.

Only eight target entries are needed for each selected triple (i,k,j). One need not extract all possible triples. When all triples are used there are at most N(N-1)N/2, hence O(N^3) extraction work, not a hidden linear-time gate.

## 2. Invertible and singular transitions

Put J=[[0,1],[-1,0]] and H_e=J L_e. Then

    H_e=[[AH-CF, BH-DF],[-AG+CE,-BG+DE]],
    det(H_e)=det(L_e)=det(Mi) det(Mk).                        (3)

Thus the equation induces an invertible Möbius transition exactly when both displayed target blocks are invertible. In that case,

    u_k is proportional to H_e u_i,                         (4)

and H_e u_i never vanishes. The reverse transition is H_e^(-1). This statement uses homogeneous vectors and is valid when an affine denominator is zero: infinity is an ordinary projective point, not an excluded branch.

If L_e has rank one, factor it as p q^T with p,q nonzero. Equation (2) is exactly

    (p^T u_k)(q^T u_i)=0.                                   (5)

It says u_i lies on the line ker(q^T), OR u_k lies on ker(p^T). The purported Möbius map is undefined on the first line; it must not be inverted or treated as a unique transition there. A factorization uses any explicitly nonzero pivot of L_e and records that pivot. If L_e=0, the equation is vacuous.

These three rank cases exhaust the strata. In particular, a zero transition determinant is not a rejection certificate.

## 3. Spanning-forest reduction and return maps

Make a graph containing every selected rank-two transition, with reversed edges supplied by its inverse. Choose a spanning forest. In each connected component C, choose a root, put T_root=I, and multiply oriented transition matrices along tree paths to obtain invertible T_i. Every compatible assignment has

    u_i proportional to T_i z_C,   z_C in P^1.              (6)

All tree propagation and inversion guards are explicit. For a rank-two non-tree edge i→k in one component, the root direction must be an eigenline of

    R_e=T_k^(-1) H_e T_i.                                   (7)

Equivalently, det(z_C,R_e z_C)=0. For a general internal edge, including rank one or zero, substitute (6) directly:

    q_e(z_C)=(T_k z_C)^T L_e (T_i z_C)=0.                    (8)

This is a homogeneous binary quadratic, possibly identically zero. For R=[[a,b],[c,d]], its eigenline polynomial is

    c x^2+(d-a)xy-b y^2.

A scalar return map gives the zero polynomial. No eigenvalue division is used. All selected internal equations must hold together; pairwise return-map compatibility alone is insufficient.

### Independent internal rejection certificates

A component has no algebraic-closure direction exactly when its internal homogeneous quadratics have no common projective zero. This can be checked with degree-at-most-two polynomial gcds and a separate infinity check, or with homogeneous gcds.

If rejected, at most three of its nonzero quadratics suffice. Proof: choose one nonzero quadratic. It has at most two distinct projective roots over an algebraic closure. For each root, select another constraint that does not vanish there. Those at most two extra constraints eliminate all its roots. Coincident roots require only one extra constraint. An independently checkable certificate can give those at most three coefficient triples and a gcd/Bézout computation in the affine chart, together with the infinity check. It need not supply numerical approximations to roots.

For two return maps, a nonzero determinant of their commutator is a particularly short sufficient rejection certificate: a common eigenvector would lie in the commutator kernel. This shortcut does not replace the complete quadratic test.

For example, over characteristic other than two,

    R1=[[1,0],[0,2]], R2=[[1,1],[0,2]], R3=[[2,0],[1,1]]

have eigenline polynomials xy, y(x-y), x(x-y). Every pair shares an eigenline and has zero commutator determinant, but all three have no common eigenline. The three-quadratic certificate detects this case.

## 4. Component domains and the rank-one edges

Let S_C be the common-zero set of the internal quadratics in P^1 over the chosen domain.

- If every internal quadratic is zero, S_C=P^1. There is no restriction.
- If at least one is nonzero, S_C has at most two distinct points over an algebraic closure. A repeated root counts once.
- An empty S_C rejects immediately.

Every edge between distinct forest components has rank at most one, because all rank-two edges were included in the forest graph. Discard rank-zero edges. For rank one, (5) becomes

    z_C = alpha_e  OR  z_D = beta_e,                        (9)

where alpha_e=ker(q^T T_i) and beta_e=ker(p^T T_k). Both are explicitly represented projective points over the base field. No algebraic root extraction is needed to compute these distinguished lines.

Create one Boolean equality indicator X[C,alpha] for each distinct distinguished line at that component. Equality is projective: proportional vectors are deduplicated, including infinity.

The clauses are:

1. Every cross edge supplies X[C,alpha] OR X[D,beta].
2. At most one different equality indicator in a component may be true. Pairwise clauses are NOT X[C,alpha] OR NOT X[C,beta].
3. A distinguished line outside S_C is forbidden by a unit negative clause.
4. If a restricted nonempty S_C is exhausted by its named permitted lines, add an at-least-one domain clause. It has one or two literals, never more, because |S_C|≤2.

For an unrestricted component, no large at-least-one clause is needed, even over a finite field when every projective point has a name. If no indicator is true, choose any point of P^1 afterward. This either changes no equality indicator, or turns just one false indicator true. Such a change cannot break a positive cross-edge clause or an at-most-one clause, because every other indicator in that component was false.

For a restricted component not exhausted by named lines, an all-false assignment is realized by an allowed unnamed point. These statements prove realizability of the equality flags, rather than merely treating them as independent Boolean variables.

### Exactness of the reduction

Any row-direction solution satisfies all the clauses by its equality indicators. Conversely, from a satisfying Boolean assignment choose the indicated point in each component if present. If none is indicated, use an allowed unnamed point, or the unrestricted repair just described. Every selected internal and cross-component equation then holds. Thus this 2-SAT problem is equivalent to the selected projective row subsystem over the stated domain, once the component domains are computed correctly.

It is still only a necessary gate for two-Green synthesis. In particular, the common column directions eliminated in Section1 have not been restored, and supported-entry equations have not been solved.

## 5. Algebraic closure versus finite fields

The strongest uncomplicated rejection test works over the algebraic closure of the base field. A rejection there excludes realizations over the base field and all extensions. An acceptance there does not imply that the required directions lie in the original finite field.

No square roots need be adjoined merely to construct this rejection test. In chart z=(1,t), take the gcd g(t) of the nonzero polynomials q_e(1,t); infinity is allowed exactly when all coefficients of y^2 vanish. A nonconstant gcd has a root in an algebraic closure. Each distinguished base-field point is tested simply by substitution. To decide whether all roots are named, test whether g divides the square of the product of the named finite-root linear factors, and separately check infinity. The exponent two handles multiplicity at most two. There can be at most two distinct permitted named points for a restricted component.

An exact base-field version needs, in addition, a certified base-field root test for degree-at-most-two g. Over a finite field this is a finite-field polynomial operation; its cost, and construction of roots if a witness is requested, must be counted separately. Enumeration of all field elements is unnecessary in the theorem. The small verification controls explicitly use enumeration only in fields of size5 or241 to compare against exact finite-domain ground truth.

For example, t^2-7 has algebraic-closure roots but no F241 root. A component with that sole finite-chart constraint and no infinity is accepted over the closure and rejected over F241. This is a domain distinction, not a numerical failure. Characteristic two and inseparable repeated-root cases remain valid because the algorithm uses exact polynomial gcd/divisibility and root tests, not a division by two or an unguarded quadratic formula.

## 6. Singular endpoint masks: why the same gate remains necessary

The inverse derivation starts with invertible endpoint matrices. Its necessary projective equations nevertheless extend to singular diagonal endpoint masks with fixed endpoint permutations and valid Green denominators.

Replace each zero endpoint scale by a formal epsilon, retaining every edge weight and denominator. The branches become invertible over E(epsilon), and their sum B(epsilon) specializes to B. Each row direction u_i(epsilon) is a nonzero rational pair. Multiply that pair by an appropriate power of epsilon and a scalar unit so both coordinates are regular and at least one has nonzero constant term. The bilinear equations are separately homogeneous in every row direction, so this independent normalization preserves them. Specializing epsilon=0 yields nonzero projective row directions satisfying every cleared target equation.

This proof does not assume that a transition determinant survives specialization. Rank drops are already handled by the rank-one/rank-zero clauses. It also does not divide by an edge weight, a target entry, or an affine coordinate. Thus a rejection by the full projective gate excludes the singular-endpoint boundary as well.

It does not extend to a branch whose Green denominator itself is singular: that branch is outside the stipulated inverse grammar. Nor does it authorize changing endpoint permutations after the support patterns have been fixed.

## 7. Work and certificate costs

Let M be the number of selected row-pair/column equations, and suppose the needed target entries can be obtained at cost E_B per entry after setup S_B.

- Reading all chosen equations and forming their 2×2 matrices: O(M E_B) target-entry work and O(M) field operations, after support/inverse-permutation tables have been built in O(N).
- All 2×2 rank tests, the forest, propagation, and conversion to internal quadratics/cross-edge labels: O(N+M) field operations and graph work, with explicitly guarded scalar inversions.
- Degree-at-most-two gcds and line/domain tests over the algebraic closure: O(N+M) field operations. Naive projective-label deduplication adds O(M^2) comparisons; canonical labels plus a suitable exact dictionary may improve that, but is not assumed.
- The direct pairwise at-most-one encoding has O(M^2) clauses in the worst case. Its implication graph and strongly connected components have polynomial size. A linear-size sequential at-most-one encoding is possible, but is not needed for the stated bound.
- Exact finite-field root availability, if demanded, has an additional degree-two root-test cost per restricted component. A successful direction witness over an extension also needs its coefficients represented and accounted for.

A conservative overall bound is S_B+O(N+M E_B+M^2) work in the field-operation model, plus any finite-field root-test/representation costs. This is a verification bound, not a Fourier-application bound. In the odd-chirp target, supplied roots and the chirp/Gauss recurrence give O(N) setup and O(1) arithmetic per selected B entry, but evaluating B on an arbitrary vector is still a separate obligation.

Useful independently checkable rejection certificates are:

- one component's at-most-three incompatible binary quadratics, with the tree transforms and exact source entries;
- a pair of return maps with a nonzero commutator determinant;
- a 2-SAT contradiction, supplied as implication paths from a literal to its negation and back, with each clause traced to a rank-one relation, domain restriction, or at-most-one requirement.

A verifier checks scalar guards, matrix products, the small polynomial identities, and the displayed paths. It need not search endpoint values. A full gate pass is never reported as a complete synthesis certificate.

## 8. Exact controls and provenance

The newly authored verifier passes 32 genuine two-Green controls at N=3,5,7,9. Sixteen each include zero edges, singular endpoint masks, and fixed monomial endpoints. Their 1552 extracted equations comprise 397 rank-zero, 164 rank-one and 991 rank-two transitions; 12 controls exercise nontrivial Boolean consistency. It checks the epsilon-limit directions directly for every masked control.

Fifteen abstract controls include infinity, repeated roots, identity cycles, rank-zero constraints, the rank-one free branch, a true 2-SAT contradiction with implication paths, the three-quadratic counterexample to pairwise compatibility, a fully named unrestricted finite domain, characteristic-two cases and closure/base-field disagreement. Twelve F5 controls and two F2 controls are compared to bounded exhaustive direction checks (528 possible assignments in total), solely to validate the solver rather than search Fourier parameters.

The existing N3 positive construction passes the new gate vacuously because that tiny support geometry supplies no eligible cleared triple. Its full constructive certificate is the separate predecessor, not a consequence of the vacuous gate. The N5 example is nonvacuously rejected by the general routine: after its forest reduction, two internal quadratics have coefficient triples (113,40,220) and (207,140,92) modulo241, no common finite root, and no root at infinity. The results include an exact affine Bezout identity. Actual controls and certificates are in PROJECTIVE_GATE_RESULTS.json.

Predecessors: FOUR_BY_FOUR_COEFFICIENT_GATE.md and SMALL_GATE_SURVIVORS.md, the latter independently accepted by reviewer_bank_interface_certificate. The original motivating ACFF upload is Library [private-id], ZIP SHA-256 490d919ee261f13bdb22dd5136f065b9ca8d099833ce32bb787bfa1650dbfcf9. This report is a newly derived extension. No uploaded program was executed, and no novelty claim is made.
