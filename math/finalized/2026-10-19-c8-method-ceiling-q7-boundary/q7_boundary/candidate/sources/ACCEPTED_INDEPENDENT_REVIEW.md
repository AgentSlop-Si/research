# Independent review: the order-5q first interior

Date: 2026-10-19 UTC.

## Verdict and exact binding

**PASS, with no required repair.** For every prime q >= 11 and every integer q < d < 2q, no binary 5q-by-5q matrix R makes the original fixed-phase matrix

    D[r,c] = R[r,c] zeta^(rc)

satisfy D*D = dI, where zeta is any primitive (5q)-th root. Equivalently, there is no mask satisfying both complete Gram identities D*D = DD* = dI. This verdict binds only the frozen candidate:

- Candidate directory: `/workspace/shared/sparse_fiveq_first_interior_20261019_1344`
- Candidate manifest SHA-256: `3764006c03cc895ea71d44764391867c17490957a2734007cb52a0b85b04650a`
- Candidate report SHA-256: `aa6c4507c215d7374e2e9aee1bb25a95b7275110178be5b549f4bc783c8cd6d6`
- All 23 manifest entries, its seal, and all seven source bindings match the local source originals. The complete integrity audit was repeated after the exact computations.

The proof is universally quantified by its symbolic argument. Finite controls independently corroborate it and are not a search proof. No candidate or historical program was imported or executed. The candidate files were not modified.

This is not a full 5q classification, a result for q=7, a support classification, or a general odd-semiprime theorem. The owner remains M-SPARSE-DEFECT, TO RESEARCH, priority 42. This local review changes no external record, repository, ownership, priority, or parent status.

## 1. Original phases, both Grams, and classical binary cancellation

The CRT idempotents e_5=q(q^(-1) mod 5) and e_q=5(5^(-1) mod q) satisfy e_5^2=e_5, e_q^2=e_q, e_5 e_q=0 and e_5+e_q=1 modulo 5q. Thus the candidate's identity

    rc = au e_5 + bv e_q modulo 5q

holds for actual indices r=a e_5+b e_q and c=u e_5+v e_q. It preserves the original phase zeta^(rc), rather than substituting a different pairing. It is a congruence, so every primitive choice of zeta is covered.

If the original square D obeys D*D=dI with d>0, then D is invertible with inverse D*/d, and DD*=dI follows. Consequently both row and column degrees are exactly d. All later column-regularity arguments are available under either original Gram hypothesis. No rectangular one-Gram relaxation is substituted.

Prime-order balance follows directly from the minimal polynomial 1+x+...+x^(q-1): if an integer coefficient vector of length q vanishes at a primitive q-th root, all its coefficients are equal. Multiplication of exponents by a nonzero residue only permutes the coefficients. The five-coordinate version is identical.

For primitive differences, the 4(q-1) products alpha^i beta^j, 0<=i<4 and 0<=j<q-1, span Q(zeta) and have exactly its degree, so they are a rational basis. Reducing a binary coefficient grid in this basis gives the displayed mixed-difference identities, hence epsilon_(u,v)=A_u+B_v with integer A,B. If both vary, the range of their Cartesian sum is at least two, impossible for values in {0,1}. One factor is constant. Therefore any primitive vanishing binary support is a union of complete five-point fibers or a union of complete q-lines. The empty support is included, and nonzero coordinate multipliers preserve the assertion.

This elementary proof is valid and self-contained. The candidate preserves classical credit to de Bruijn and Lam–Leung, including Lam–Leung Theorem 3.3 and Corollary 3.4, and makes no historical-priority claim. This review does not claim the classical cancellation lemma as a new result.

## 2. Clique reduction and exact five-point families

For two rows within G_a, the q fiber-intersection counts are equal to an integer k. Their whole intersection has size qk<=d<2q, so k is zero or one. Nonadjacent rows have disjoint full supports; adjacent rows meet in exactly one point in each fiber.

A row has some fiber with at most one point because its average fiber weight is below two. A zero makes it isolated. A singleton forces every neighbor to use that point and therefore makes its neighborhood a clique. A graph with every vertex simplicial is a disjoint union of cliques: otherwise a shortest path between two nonadjacent connected vertices supplies a vertex whose neighbors on the path are nonadjacent. Five components would give five pairwise disjoint supports of size d>q in 5q columns. Thus there are at most four components.

In a nonsingleton local family whose pairwise intersections are one, a common point is unique. Every other coordinate has multiplicity one, giving incidence I=n+k-1. For a singleton, the same numerical identity holds for every weight k, including k=0. The accounting therefore does not accidentally exclude an empty singleton fiber.

If there is no common point, each row has weight at least two. The exact matrix identity WW^T=diag(w_i-1)+J is positive definite, so n<=rank(W)<=k. This covers repeated restrictions too. A repeated non-singleton restriction cannot have pairwise intersection one; repeated singleton restrictions are stars and are correctly retained.

In a split group, a nonstar initially has n<=5. Its other at most three components contain at least q-5>=6 rows, so one is nonsingleton and occupies a point in every fiber. Disjointness reduces the nonstar union to k<=4. The remaining possibilities are exactly:

- n=3, k=3 or 4. The three pair-meeting points are distinct, each has multiplicity two, and any remaining point is private. Hence I=k+3, one above the star formula.
- n=4, k=4. Pair counting gives multiplicity pattern (3,2,2,2), so I=9, two above the star formula. The other numerical pattern (3,3,1,1) is impossible because two 3-subsets of four rows meet in at least two rows, producing an intersection of at least two points for those rows.

Two nonstars in one fiber would occupy at least six disjoint coordinates. Thus there is at most one. For a single clique, q>5 makes every local family a star, and its incidence is at most q+4. Summing over q fibers yields d<=q+4.

These steps genuinely address the five-coordinate triangle and near-pencil exceptions. They do not copy the order-3q incidence bound, where the smaller fiber excluded these exceptions by itself.

## 3. The weighted split-group repair is complete

Let t=d-q. With h components, summing the star formulas and the possible nonstar defect gives local incidence at most q+5-h+2. Empty singleton contributions k-1=-1 remain present.

For h=4 this is q+3. For h=3 it is q+4, with equality requiring the size-four nonstar, all five coordinates used, and defect two. The nonstar occupies four points; a different nonsingleton uses the fifth. The last component must be a singleton with empty restriction. More explicitly, the component sizes must be (1,4,q-5), and for q>=11 the singleton is unique and fixed across fibers. If d=q+4, every fiber must attain its upper bound, so that same singleton row would be empty everywhere. This contradicts its degree d>0. Integers then give d<=q+3. There is no possibility of varying which singleton is empty from fiber to fiber.

For h=2, if neither component has size three or four, both are stars and total incidence is at most q+3. This includes a singleton component; the total formula remains valid even when that singleton is empty.

For sizes 3 and m=q-3>=8, the large component is always a star. In a star fiber, x,y>=0 and x+y<=3, so 2x+3y<=9. In a nonstar fiber, (x,y) has x=k in {3,4}, y<=4-k, giving respectively at most 9 or 8. Summing over fibers gives

    (2*3 + 3m)t <= 9q,
    t <= 3q/(q-1) < 4.

For sizes 4 and m=q-4>=7, star fibers satisfy 3x+5y<=15, and the near-pencil has (x,y)=(5,0), also giving 15. Thus

    (3*4 + 5m)t <= 15q,
    t <= 15q/(5q-8) < 4.

These are symbolic inequalities for every allowed q, not estimates inferred from tested primes. Integrality gives t<=3. Because q>=11, both components cannot simultaneously have size in {3,4}. The cases exhaust every split group.

Thus every hypothetical first-interior mask has d=q+1, q+2, q+3, or q+4; the last degree forces every G_a to be one clique.

## 4. The q+4 branch is excluded without straightening its baselines

At d=q+4, equality in the local q+4 incidence bound holds in every fiber of every group. Each fiber has one baseline column of multiplicity q and four private columns of multiplicity one. A row has one baseline entry per fiber and four extras in total. These baselines may initially depend on the fiber; the proof does not assume they are straight q-lines.

If h groups use a given column as baseline, its column degree is hq+(5-h)=q+4. Hence h=1, so the five group baseline sets are disjoint and cover the columns.

Choose an extra of row r, on the baseline of a different group G. Every row s in G meets r at that extra. The intersection lies in the union of their two four-element extra sets, so has size at most eight. Among G's rows are q-1 primitive partners (different b), and eight<q holds already at q=11. Binary cancellation therefore forces each nonempty primitive intersection to be exactly one full five-point fiber.

Row r can contain at most one such fiber, since completing one consumes all four extras. Consequently all q-1 primitive partners must contain that same fiber. In G, each off-baseline point belongs to at most one row, so at most one G-row can contain the whole fiber. This contradicts q-1>1. No extra geometric assumption enters this exclusion.

## 5. No full five-fiber and the full-q-line forcing step

For t=1,2,3, a row whose component has another nonsingleton component cannot fill a five-fiber: the other component uses a disjoint point in every fiber. Otherwise all other components are singletons, so the row's component has at least q-3>5 rows and is a star in every fiber. Its row then has q baseline points and only t<=3 extras, too few to complete a five-fiber. Singleton rows are covered by the first case, since q>=11 and at most four components ensure another nonsingleton component exists.

Suppose a row r has neither a full q-line nor a full five-fiber. Its intersection with every primitive partner must be empty by binary cancellation. At each supported column, each of the four other row groups can contribute at most its unique row with b=b_r. Column regularity therefore forces at least d-4>=q-3>=8 contributions from r's own group.

All rows sharing a column belong to a single clique component, so this high multiplicity requires a component of at least q-3 rows. There can be at most one such component because 2(q-3)>q. Its size exceeds five, so it is a star in every fiber. Only its one baseline coordinate per fiber can have multiplicity above one; all other components are disjoint from it. Thus at most q columns have multiplicity at least q-3 in that group. Row r would need d>q such columns, a contradiction.

Every row consequently contains a full q-line. It is unique because distinct q-lines are disjoint and d<2q. Only at this point may the row be written as L_(u(r)) union T_r with |T_r|=t<=3. The argument does not prematurely identify local star baselines with these full lines.

## 6. All character orders and the final divisibility contradiction

For rows on different baseline lines, the intersection is contained in their two extra sets, so has size at most 2t<=6. All row-difference orders are explicitly covered:

1. Same a, different b: order q. A nonempty integral vanishing overlap has at least q entries, contradicting 6<q.
2. Different a and b: order 5q. Primitive binary cancellation would require a complete five-fiber or q-line; the first is forbidden in either row, and the second is too large.
3. Same b, different a: order five. The five q-line intersection counts must all be equal. A row occupies at most its baseline plus t<=3 other q-lines, so at least one count is zero. All counts are zero.

Hence different baseline classes have disjoint supports. For any occupied baseline line L_u, each column on that line belongs to all n_u rows in its class. No row from another class can use such a column, because it would meet that class. Column degree forces n_u=d. The baseline classes partition all 5q rows, so

    5q = h d, with 1<=h<=5.

Since q is prime and q>5>=h, q does not divide h and must divide d. No integer in (q,2q) is a multiple of q. This closes the entire claimed interior. It does not assume all five lines are occupied; the argument allows every h from one through five.

## 7. Exact q=7 countercontrol and what it does not establish

The review independently reconstructed the seven-row, 35-column block described by the candidate. The first component has three rows; the second has four. Its first three fibers use a repeated singleton for the former and a near-pencil for the latter, with the size-three row rotating among three of its four rows. The last four fibers use a triangle for the first component and repeated singleton restrictions for the second, with one additional private point on its fourth row in one fiber.

Every row has degree 11. Pair intersections within either component equal one in every fiber, and the components are disjoint. The actual order-35 row indices are 0,15,30,10,25,5,20. All 49 original row Gram entries reduce exactly to 11 I_7. The retained block and residues match the independent reconstruction.

This refutes an extension of the split-group bound d<=q+3 to q=7 at the row-group level: 11=7+4. It is expressly a 7-by-35 rectangular block. Its column degrees are nonconstant and below 11, and it cannot satisfy a 35-by-35 column Gram 11I. It neither constructs a square equality mask at (N,d)=(35,11) nor decides whether that degree is possible.

## 8. Fresh independent controls and retained-data audit

`independent_checks.py` uses integer polynomial arithmetic. For prime q!=5 it constructs Phi_(5q)(x)=Phi_5(x^q)/Phi_5(x) by exact monic division, independently of the candidate's SymPy implementation. Every original Gram is reduced modulo this polynomial, with opposite exponent signs for row and column orders. No floating tolerance is used.

The completed run has empty standard error and passed:

- 376,960 multisets of two through five nonempty five-coordinate restrictions, allowing repeated restrictions. All exact-one-intersection families satisfy the stated star formula or independently recovered nonstar list.
- 25,483 local partition patterns at q=11,12,13,17,19,23,47,53, including empty singleton fibers. The composite value 12 is only an incidence control; the theorem remains restricted to prime q. Every saturated three-component pattern has the same forced empty singleton structure.
- All 131,850 retained square Gram entries, including all twelve divisor controls, all eight regular negative masks, and the proper N=55,d=11 original-model mask. Every retained failure residue and every zero-by-character-order count match, rather than merely trusting success flags.
- 520,000 fresh square Gram entries from sixteen newly constructed controls at q=17,19, each evaluated for two primitive-root choices. Divisor masks pass both complete Grams. Cross-shape and all-split near-masks have the required regular degrees and same-group row orthogonality but fail both complete Grams.
- All 49 rectangular q=7 row Gram entries.
- All 6,050 entries across both full inverse products and all 6,050 entries across both full error Grams of the retained proper N=55,d=11 original-model witness. The audit checks B=(H-D)*/(N-d), E=M-H, exact denominators, both inverse row/column budgets 44, MB=BM=I, and EE*=E*E=11I. Its matrices are checked in the original index order, not just in the reduced five-dimensional factor.
- 37,950 exact original-index CRT congruences for q=7,11,13,17,19,23. The congruence proves primitive-root invariance; the two-root Gram controls independently exercise it.
- Candidate manifest, all 23 entries, seal, and seven source bindings both before and after the audit.

The local computations are independent controls, not a complete mask census. Universal correctness rests on Sections 1–6 of this review. The original inverse-model control at d=q is a proper positive witness; the d=N examples are only mask controls and are not misrepresented as admissible s=0 inverse models.

## 9. Inherited consequence, attribution, and scope

The supplied accepted equality criterion and attainment argument imply

    Delta_(5q,5q-d) > sqrt(d/(5q))

for the excluded first-interior degrees. This is strict separation of the infimum, not just absence of an attaining mask. The accepted general quantitative theorem is

    Delta_(N,N-d)^2 >= d/N + 1/[10 N d^(phi(N)-1)].

Because phi(5q)=4(q-1), substitution gives exactly

    Delta_(5q,5q-d)^2 >= d/(5q) + 1/[50 q d^(4q-5)].

This is an inherited nonsharp lower bound. It does not provide the exact optimum or an optimal rate.

Classical cancellation remains credited to N. G. de Bruijn, On the factorization of cyclic groups, Indagationes Mathematicae 15 (1953), 370–377; and T. Y. Lam and K. H. Leung, On Vanishing Sums of Roots of Unity, Journal of Algebra 224 (2000), 91–109, DOI 10.1006/jabr.1999.8089, as retained in the candidate bibliography. The present review confirms the self-contained argument and preserves those attributions without making a historical-priority claim.

The existing order-3q classification, prime powers, order-2q statements, complementary-divisor constructions, and connected order-eight control are unchanged. The q=7 square problem, remaining middle interval 2q<=d<=4q at order 5q, and general odd-semiprime classification remain outside this acceptance. M-SPARSE-DEFECT remains TO RESEARCH, priority 42. No external write, repository action, owner change, or service-limit retry was performed.
