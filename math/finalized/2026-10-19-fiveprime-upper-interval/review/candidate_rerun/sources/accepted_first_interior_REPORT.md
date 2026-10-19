# Order 5q: exclusion of the entire first interior for prime q >= 11

Date: 2026-10-19 UTC. Proof candidate requiring independent review. No historical-priority or novelty claim. All work is local; no external record or repository has been changed.

## Result and scope

Let q >= 11 be prime, N=5q, zeta any primitive N-th root, and R a binary N-by-N matrix. Define the original fixed-phase matrix D[r,c]=R[r,c] zeta^(rc). There is no such R satisfying both D*D=dI and DD*=dI at any integer degree

    q < d < 2q.

It suffices to assume either Gram identity because D is square and d>0. Both row and column degrees are d, and both are used below. This is a new scoped extension beyond the accepted N=3q classification. It does not classify N=5q: q=7 and the interval 2q <= d <= 4q remain outside this theorem. The already accepted low-degree and upper-degree statements are not counted as new results.

The new ingredient is a weighted incidence repair for five-coordinate fibers. Unlike the three-coordinate case, a split row group can contain a local triangle or four-row near-pencil without violating disjointness of its components. Those exceptions must be handled, not omitted. Section 9 retains an exact q=7 row-group control showing why the q>=11 restriction in the present reduction is substantive.

## 1. Original phases and classical cancellation

Set e_5=q(q^{-1} mod 5), e_q=5(5^{-1} mod q), modulo N. Relabel actual indices by r=a e_5+b e_q and c=u e_5+v e_q. Put alpha=zeta^(e_5), beta=zeta^(e_q). Exactly, not up to an altered pairing,

    zeta^(rc)=alpha^(au) beta^(bv).

Write G_a for the q rows with first coordinate a, F_v for the five columns with second coordinate v, and L_u for the q columns with first coordinate u.

Prime-order balance: an integral sum sum_v k_v beta^(hv)=0 with h nonzero modulo q forces all k_v equal. The analogous assertion holds at order five.

Primitive binary cancellation: a binary column subset whose sum vanishes against a character nontrivial in both CRT coordinates is a union of complete F_v fibers or a union of complete L_u lines. Indeed reduction in the rational basis alpha^i beta^j (0<=i<4, 0<=j<q-1) forces its coefficient array epsilon to satisfy

    epsilon_(i,j)-epsilon_(i,q-1)-epsilon_(4,j)+epsilon_(4,q-1)=0.

Thus epsilon_(u,v)=A_u+B_v with integer A,B. If both vary, the range of A+B on the Cartesian product has length at least two, impossible for a binary array. One coordinate is constant, proving the assertion. Nonzero coordinate multipliers simply permute the coordinates.

This cancellation content is classical and is credited to de Bruijn and Lam–Leung, as in the accepted source packets. Lam and Leung’s [Theorem 3.3 and Corollary 3.4](https://arxiv.org/pdf/math/9511209) give the two-prime positive-sum structure and explicitly trace the result to de Bruijn, §3. See T. Y. Lam and K. H. Leung, On Vanishing Sums of Roots of Unity, Journal of Algebra 224 (2000), 91–109, [DOI 10.1006/jabr.1999.8089](https://doi.org/10.1006/jabr.1999.8089); N. G. de Bruijn, On the factorization of cyclic groups, Indagationes Mathematicae 15 (1953), 370–377. The basis proof is included for self-containment, not as a new vanishing-sum result. No general mixed-prime weighted-descent statement is assumed.

## 2. Clique components still follow for q<d<2q

For distinct r,s in one G_a, prime-order balance says the five-point fiber intersections |S_r intersect S_s intersect F_v| are a constant k. Since their whole intersection is at most d<2q, k is zero or one. Join r,s when k=1. Adjacent rows meet once in every fiber, while nonadjacent rows have disjoint full supports.

Every row has a fiber with at most one entry. A zero there makes it isolated; a singleton there makes all its neighbors contain the same coordinate and hence mutually adjacent. Every vertex has a clique neighborhood, so every connected component is a clique. There are at most four components: five components would supply five disjoint supports of size d>q in only 5q columns.

This concerns graphs inside the five residue row groups. It is not a full-square-block assumption about the entire mask support graph.

## 3. Exact local families on five coordinates

Consider the restrictions of the n rows of a nonsingleton clique component to a fiber. Their pairwise intersections are exactly one. Let k be their union size and I their incidence sum.

If they have a common point, it is unique, and all other used coordinates occur in exactly one row. Thus

    I=n+k-1.                                             (3.1)

Call this a star. For a singleton component the same identity holds with k its row weight, even when k=0.

If they have no common point, every row has size at least two. Their incidence matrix W satisfies

    W W^T = diag(w_i-1)+J,

which is positive definite. Hence n<=k. This is a rank argument, so it also covers repeated restrictions without any hidden distinctness assumption.

In a split G_a, every nonstar component has at most five rows. Since q>=11 and there are at most four components, at least one of its other components is nonsingleton. That other component occupies a coordinate in every fiber. Consequently k<=4. The only nonstar possibilities are:

- n=3, k=3 or 4, and I=k+3. The three pairwise meeting points must be distinct; each contributes one extra incidence beyond its union count. Any additional coordinate is private.
- n=4, k=4, and I=9. Here each used coordinate has multiplicity at most three and the total number of row pairs is six. The only possible multiplicities are (3,2,2,2). The other numerical possibility (3,3,1,1) would make two rows share both triple coordinates and is impossible. Thus this is the four-row near-pencil, for example {1,2},{1,3},{1,4},{2,3,4}.

There are no other nonstars in a split group. At most one occurs in a given fiber, since two would need at least six disjoint coordinates. Relative to (3.1), the triangle adds one incidence and the four-row near-pencil adds two.

For a single-clique group, q>5 and the rank argument force a star in every fiber. It has q baseline columns and at most four private extra incidences per fiber. Summing gives

    d <= q+4.                                             (3.2)

## 4. Weighted repair: split groups have d<=q+3

Write t=d-q, so every component of n rows has nt extra incidences relative to n baselines per fiber over the q fibers. This accounting permits the contribution k-1=-1 of an empty singleton restriction.

Suppose first that a split group has h>=3 components. Summing (3.1) and the possible nonstar defects in one fiber gives

    I_total <= q+5-h+2.

For h=4 this is q+3. For h=3 it is q+4, and equality requires a four-row nonstar, union size five in total, and no unused coordinate. The nonstar uses four coordinates. One other component is nonsingleton and needs the fifth coordinate; the final component must therefore be a singleton whose restriction is empty. Thus d=q+4 would require that same singleton row to be empty in every fiber, contradicting its positive degree. Hence d<=q+3 also for h=3. This also excludes d>q+4 directly.

Now suppose h=2. If neither component has size 3 or 4, both are stars in every fiber and (3.1) gives I_total<=q+3.

If the sizes are 3 and m=q-3>=8, write x=I_small-3 and y=I_large-m in a fiber. The large component is always a star. In the ordinary case x,y>=0 and x+y<=3. In the nonstar case the small component uses k=3 or 4 coordinates, giving x=k and y<=4-k. In every case

    2x+3y <= 9.

Summing over fibers, where sum x=3t and sum y=mt, gives

    t <= 3q/(q-1) < 4.

Integrality yields t<=3.

If the sizes are 4 and m=q-4>=7, the ordinary case again has x,y>=0, x+y<=3, now x=I_small-4. The only nonstar case has x=5,y=0. Therefore

    3x+5y <= 15,
    t <= 15q/(5q-8) < 4.

Again t<=3. These cases exhaust h=2 because q>=11 prevents both components from belonging to {3,4}. We have proved the claimed split-group bound.

Together with (3.2), every possible interior mask has d=q+1,q+2,q+3, or q+4; and d=q+4 forces every G_a to be a single clique.

## 5. Excluding d=q+4

At this degree, saturation of (3.2) makes every row contain its group's q baseline columns and four extras. In each fiber the group contributes multiplicities (q,1,1,1,1).

If h of the five groups use a particular column as a baseline, its full degree is

    hq+(5-h)=5+h(q-1)=q+4,

forcing h=1. The five group baselines are distinct in every fiber, hence disjoint as sets of columns.

Choose a row r and an extra column c. Its baseline belongs to another group G. Every row s in G meets r at c. Their common support lies in the union of their two four-element extra sets, so has size at most eight. For the q-1 partners with b_s != b_r, the character is primitive. Since eight<q, primitive binary cancellation and nonemptiness force their intersection to be exactly one full five-column fiber.

Row r can contain at most one full fiber, because it has only four extras. At that fiber, however, every off-baseline coordinate of G belongs to at most one row of G, so at most one row of G can contain the whole fiber. This contradicts q-1>1. Thus d=q+4 is impossible.

## 6. Below q+4 no row contains a full five-column fiber

It remains to consider d=q+t with 1<=t<=3.

If a row's own clique component has a different nonsingleton component in its group, that other component uses at least one coordinate in every fiber, disjoint from the row. So the row cannot contain a full fiber.

Otherwise all other components are singletons. The row's own component then has at least q-3>=8 rows, or the group is a single clique. The rank argument makes it a star in every fiber. Each row has q baseline entries and t<=3 extras, too few to complete any five-column fiber. This covers every row, including singleton rows: a singleton's group necessarily has another nonsingleton component when q>=11.

## 7. Column regularity forces a full q-line in every row

Suppose a row r contains no full L_u. It already contains no full F_v by Section 6. Primitive binary cancellation then forces its intersection with every row in another group having a different b coordinate to be empty.

For each c in S_r, each of the four other groups can therefore contribute at most one row to column c, its unique row with b=b_r. Since that column has total degree d, r's own group contributes at least

    d-4 >= q-3 >= 8.

A column of this multiplicity belongs to a component of at least q-3 rows. There is at most one such component, since 2(q-3)>q. Its size exceeds five, so it is a star in every fiber, and only its unique baseline coordinate in each fiber can have multiplicity greater than one. Thus at most q columns in the entire group can have multiplicity at least q-3.

But r uses d>q columns, all just forced to have that multiplicity. Contradiction. Every row contains a full q-line, necessarily unique because d<2q. Write

    S_r = L_(u(r)) union T_r,       |T_r|=t<=3.

## 8. Different baseline lines cannot meet; the degree contradiction

Take rows r,s with u(r)!=u(s). Their intersection has at most 2t<=6 entries.

- If a_r=a_s, their nonzero character has order q, and any nonempty zero overlap has at least q entries. Since six<q, the intersection is empty.
- If a_r!=a_s and b_r!=b_s, primitive cancellation and Section 6 forbid a five-fiber; the size bound forbids a q-line. Again the intersection is empty.
- If b_r=b_s, their character has order five. Its intersection counts in the five L_u lines must be equal. But r has entries on at most four of these lines: its baseline plus at most three others. One count is zero, so all are zero.

Hence rows with different baseline lines have disjoint supports. Let n_u be the number of rows whose baseline is L_u. If n_u>0, each column on L_u belongs to exactly these n_u rows. Column degree d gives n_u=d. Summing all row classes yields

    5q = h d,        1<=h<=5.

Since q is prime and q>5, q divides d. This is impossible for q<d<2q. The whole first interior is excluded.

## 9. Exact controls and the q=7 boundary

The checker enumerates all no-common-point exact-one-intersection families on five coordinates with 2<=n<=5, verifies the local classification and the displayed weighted inequalities with integer arithmetic, and checks the clique incidence bounds for every partition into at most four components at tested primes. It separately checks all original-phase CRT congruences and both full Gram orders for positive divisor masks and regular near-masks.

Negative mask controls at q=11,13 include:

- d=q+4 cross-shapes: R[(a,b),(u,v)]=1 exactly when u=a or v=b. Every row/column has degree q+4, every same-group row Gram vanishes, and order-five row Grams also vanish; primitive cross-group Grams fail.
- d=q+t, 1<=t<=3 all-split masks. In G_a the q-1 rows b!=0 use baseline L_a, and the singleton b=0 uses L_(a+1). Row (a,b) adds columns (a+j,b) for j=2,...,t+1, modulo five. They have both degree counts q+t and all same-group row Grams zero, but fail the complete original Grams. These isolate the global obstruction after the clique/line reductions.

A distinct q=7 row-group control consists of three rows A and four rows B, each of degree 11 across seven five-column fibers. In the first three fibers, A repeats singleton {4}, while B is the near-pencil on {0,1,2,3}, assigning its size-three row to three different B rows. In the remaining four fibers A is the triangle {0,1},{0,2},{1,2}; B repeats singleton {3}, except that its fourth row also uses {4} in the first of those four fibers. Every A row and B row has degree 11; within either component pairwise fiber intersections are one, and the components are disjoint. Its original order-35 row block has Gram 11 I_7. Thus the q>=11 split-group conclusion d<=q+3 is false at q=7 already at the exact row-group level. This is not a full square mask or a construction at (35,11), and it does not settle that degree.

The original inverse-model control uses the proper mask d=q at N=55, R[(a,b),(u,v)]=1 iff a=u. It reconstructs B_tilde=(H-D)*/(N-d), M_tilde=B_tilde^{-1}, and E=M_tilde-H in the exact original phase field. Its CRT product structure constructs the witness using only a five-by-five exact inverse. The checker then directly multiplies the full 55-by-55 matrices in the original index order, reducing integer polynomials modulo Phi_55 for every entry of both inverse products and both error Grams. Every inverse row and column has N-d=44 nonzeros and both error Grams are 11 I. Full coefficient data and completed check counts are retained, with no floating tolerance. The completed verifier passed 131,850 full square Gram entries, 6,050 inverse-product entries, 6,050 error-Gram entries, 49 rectangular boundary Gram entries, 29,529 local patterns, and 1,465,400 exact CRT congruences. RUN.stderr is empty. No full equality-mask census is claimed.

## 10. Original inverse-row consequence, credit, and limits

Using the separately accepted equality characterization and attainment result, the theorem yields

    Delta_(5q,5q-d) > sqrt(d/(5q))

for prime q>=11 and q<d<2q. Composing with the already accepted quantitative no-mask bound gives

    Delta_(5q,5q-d)^2 >= d/(5q) + 1/[50 q d^(4q-5)].

Here phi(5q)=4(q-1). This is an inherited nonsharp quantitative bound, not a new sharp optimum or rate.

The accepted N=3q classification, prime powers, N=2q, complementary-divisor constructions, and connected (8,4) countercontrol remain unchanged. No full-square-block geometry, general two-prime weighted descent, or complete 5q classification is claimed. In particular q=7 and the remaining middle interval at 5q need additional work. Classical cancellation credit remains with de Bruijn and Lam–Leung; the present report makes no historical-priority claim.

The frozen source files are bound in SOURCE_BINDINGS.json. Exact controls support but do not replace the symbolic proof. The owner remains M-SPARSE-DEFECT, TO RESEARCH, priority 42. No external write, status change, or self-acceptance has been performed.
