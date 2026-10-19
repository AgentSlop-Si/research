# Order 5q: exclusion of the upper interior interval 3q<d<4q

Date: 2026-10-19 UTC. Owner M-SPARSE-DEFECT; retain TO RESEARCH and priority 42. Frozen proof candidate pending independent review. All work is local. Historical novelty remains unresolved. No endpoint, complete order-5q classification, support-block theorem, or Fourier/FFT improvement is claimed.

## 1. Precise theorem and preserved scope

Let q>5 be prime, N=5q, and zeta any primitive Nth root of unity. For a binary N-by-N matrix R, put

    D[r,c] = R[r,c] zeta^(rc),       0 <= r,c < N.

There is no such R satisfying either square Gram identity D*D=dI or DD*=dI at any integer degree

    3q < d < 4q.

Since d>0 and D is square, either Gram identity implies the other. Their diagonal entries give degree d for every row and every column of R. Equivalently, the entrywise binary mask of the normalized Fourier matrix cannot have Gram (d/N)I in this open interval.

This packet proves exactly the indicated interval. It does not decide d=3q, d=4q, or 4q<d<5q, nor claim a full semiprime classification or uniform divisibility. The previously accepted first interior q<d<2q, its q=7 boundary work, and middle interior 2q<d<3q are preserved. Those earlier exclusions are not used as black boxes to infer the new result. Frozen prior reports and the accepted middle verdict are bound in SOURCE_BINDINGS.json to fix the model, provenance, and prior scope. No historical script is executed.

## 2. Literal CRT phase and cancellation lemmas

Choose the orthogonal CRT idempotents modulo N

    e_5 = q (q^(-1) mod 5),       e_q = 5 (5^(-1) mod q).

Write actual row and column indices as

    r = a e_5 + b e_q,       c = u e_5 + v e_q,
    a,u in Z/5,              b,v in Z/q.

With alpha=zeta^(e_5) and beta=zeta^(e_q), the original fixed phase is exactly

    zeta^(rc) = alpha^(au) beta^(bv).

This is a relabeling of the given Fourier matrix, not permission to choose new entry phases. Let G_a consist of the q rows with first coordinate a; let F_v be the five columns whose second coordinate is v; and let L_u be the q columns whose first coordinate is u. Write S_r for the support of row r.

For two distinct rows r,s in G_a, their character difference has order q. Therefore row orthogonality says that

    |S_r intersect S_s intersect F_v| = k(r,s)

is independent of v. Indeed the integer coefficients of a polynomial of degree at most q-1 vanishing at a primitive qth root are all equal, by its minimal polynomial 1+x+...+x^(q-1). Here q k(r,s)<=d<4q, so k(r,s)<=3.

For a pair of rows with both CRT coordinates different, their difference character has primitive order 5q. A binary subset of the column grid with zero sum against this character is either a union of complete F_v fibers or a union of complete L_u lines. For completeness, nonzero character multipliers first permute the two coordinates. The products alpha^i beta^j, 0<=i<4 and 0<=j<q-1, form a rational basis: they span the cyclotomic field and their count equals its degree phi(5q)=4(q-1). Reducing a binary coefficient array epsilon in this basis gives

    epsilon[i,j] - epsilon[i,q-1] - epsilon[4,j] + epsilon[4,q-1] = 0.

Thus epsilon[u,v]=A[u]+B[v] for integer-valued arrays A and B. If both varied, their respective ranges would have positive integer length, so the range of their sum on the full Cartesian grid would be at least two. A binary array has range at most one. Hence one array is constant, giving exactly one of the two parallel-cycle alternatives. The empty subset is allowed. This binary two-prime cancellation is classical; the present argument is included to make the proof self-contained, with no novelty claim for the lemma.

## 3. Column-degree coverage derives the complete row geometry

Fix a supported entry (r,c), with r=(a,b). Exactly q+4 rows agree with r in at least one of its two coordinates: the q rows of G_a and four additional rows having second coordinate b. This count includes r.

Column c has d supporting rows, and

    d >= 3q+1 > q+4.

Consequently there is a second supporting row s differing from r in both coordinates. Its overlap with r has zero primitive character sum and contains c. The cancellation lemma supplies a full fiber F_v or full line L_u through c, lying entirely inside S_r.

Do this separately for every supported entry of r. If A_r denotes all u such that L_u is fully contained in S_r, and B_r denotes all v such that F_v is fully contained in S_r, then

    S_r = (A_r x Z/q) union (Z/5 x B_r).                 (3.1)

Put ell_r=|A_r| and f_r=|B_r|. Both sets are maximal full-cycle sets, not arbitrary pieces of a convenient representation. The exact support size is

    d = ell_r q + (5-ell_r) f_r.                         (3.2)

Because d<4q, ell_r<=3. Because d>3q, f_r cannot be zero. Up to this point ell_r and f_r may vary between rows, and mixed line/fiber shapes have not been discarded.

This derives a union of cycles for each individual support. It does not assume Cartesian-product row supports, a common fiber assignment, or a decomposition of the square mask into full square blocks.

## 4. Disjoint fiber packing removes all mixed-count alternatives

For distinct rows r,s in one G_a, B_r and B_s are disjoint. Otherwise a common v would give all five points in their overlap on F_v. Prime-order balance from Section 2 would force k(r,s)=5 in every fiber, impossible because k(r,s)<=3.

There are q rows in G_a and exactly q available fibers. Their q pairwise disjoint nonempty B_r must therefore each have size one. This argument does not assume the f_r were equal. Write

    B_(a,b) = { f_a(b) },

where every f_a is a permutation of Z/q. Equation (3.2) now becomes

    d = 5 + ell_r (q-1),       ell_r in {0,1,2,3}.       (4.1)

The values for ell_r=0,1,2 are 5, q+4, and 2q+3, all below 3q for prime q>5. Hence every row has ell_r=3, and the only degree still possible is

    d = 3q+2.                                          (4.2)

This is the essential mixed-count gate. In particular the degree equation alone would not force three lines. For q=7, at the residual degree d=23, its individual row solutions are (ell,f)=(1,4), (2,3), and (3,1). The first would require at least 4+6=10 disjoint fibers in its seven-row group; the second at least 3+6=9; only seven are available. Both are eliminated by the group packing argument before (4.1) is used.

Now take two distinct rows r,s of G_a. Their special fibers v and w differ. On F_v and F_w their overlap has three points; on every other fiber it has |A_r intersect A_s| points. Since q>2 there is another fiber. Prime balance implies |A_r intersect A_s|=3, so A_r=A_s. Thus there is one three-element set A_a per row group, and every remaining candidate has the derived form

    R[(a,b),(u,v)] = 1 iff u in A_a or v=f_a(b),
    |A_a|=3,       f_a a permutation of Z/q.            (4.3)

No relation between f_a and f_(a') is imposed.

## 5. Column saturation forces distinct baseline triples

For fixed u, let h_u be the number of row groups a with u in A_a. Every such group supplies all q of its rows to any column (u,v). Each remaining group supplies exactly one row, because its special-fiber map is a permutation. The column degree is therefore

    h_u q + (5-h_u) = 5+h_u(q-1).

Equating this with d=3q+2 gives h_u=3 for every u. In particular the five sets A_a cannot all be identical: identical triples would give column multiplicities five or zero, rather than three.

Choose a!=a' with A_a!=A_(a'). Since both are triples inside a five-element set,

    1 <= h=|A_a intersect A_(a')| <= 2.                 (5.1)

## 6. Primitive cross-group obstruction

Fix any row r=(a,b), whose special fiber is v=f_a(b). In the second group G_(a'), at most one row has second coordinate b, and at most one has special fiber v. Excluding those at most two rows leaves at least q-2>0 choices. Choose s=(a',b') among them and write w=f_(a')(b'). Then a!=a', b!=b', and v!=w.

The overlap S_r intersect S_s has exactly three points in F_v and F_w, and h points in every other F_t, where h<=2 by (5.1). It is not a union of full five-fibers, since the special fibers have three points. It is not a union of full q-lines, since its fiber counts are nonconstant and at least one other fiber exists. Both primitive-cancellation alternatives fail. But r and s differ in both coordinates and must have zero primitive overlap sum. This contradiction excludes d=3q+2 and finishes the entire interval.

For q=7 specifically, the target degrees are 22 through 27, coverage compares d>=22 with q+4=11, the singleton reduction leaves only 23, and the partner choice leaves at least five rows and five ordinary fibers. Thus no small-prime exception is hidden in any strict inequality or selection step. The exceptional geometry from the earlier first interval is not assumed to transfer to this interval.

## 7. Fresh exact controls

Run `python verify_upper.py` from this directory. The program uses only the Python standard library, exact integer arithmetic, and original row/column indices. Root sums are reduced in the explicit rational basis from Section 2, with no floating tolerance. It neither executes nor imports any historical checker.

The completed run verifies:

- 37,950 original-index CRT phase products at q=7,11,13,17,19,23.
- 188,400 complete Gram entries, including diagonal entries and both orientations. Positive controls have divisor degrees 1,5,q,5q at q=7,11,13,17. Deliberately invalid regular near-masks have degree 3q+2 and cyclic triples A_a={a,a+1,a+2}; one family uses f_a(b)=b and another uses unrelated affine maps f_a(b)=(a+1)b+a mod q. Their same-group row Grams vanish, but both full Grams fail. Original-index witnesses and literal q=7 masks are retained.
- 56,524 canonical mixed-cycle row supports at q=7,11. For every support it checks actual maximal full lines and full fibers, the union-size formula, every pre-packing degree possibility, and the unique singleton reduction. The q=7 mixed shapes described above are preserved explicitly rather than excluded from the enumeration.
- 135,200 exact same-group overlap sums and 601,600 primitive overlap sums for all baseline triples and all fiber pairs at q=7,11. The exact primitive zero condition is A=C and v!=w. In particular every different-triple/different-fiber obstruction is nonzero, including both possible intersection sizes h=1,2.
- 260,270 partner selections, including all 5,040 permutations of seven fibers and all affine permutations of eleven fibers. The mathematical proof permits every permutation at every prime; these finite tests corroborate its at-most-two-exclusions count.
- 90 coverage exception-set counts, 16 interval-degree reductions, 16 mixed-fiber packing obstructions, and all five frozen source-copy hashes.

RESULTS.json reports PASS. RUN.stderr is empty. These controls supplement the symbolic theorem; they are not an exhaustive square-mask census, optimizer certificate, or numerical extrapolation. The negative near-masks are not equality constructions. Their role is to show why exact rectangular same-group Gram conditions and regularity alone do not finish the global problem.

## 8. Administrative and dependency limits

The new mathematical result is only the stated open-interval exclusion. Earlier equality/attainment and quantitative defect-gap results may be composed with it by the parent project, but this packet does not re-prove those results or claim a sharp defect optimum. The classical cancellation lemma is not newly attributed to this work. Historical novelty remains unresolved.

Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42. No external repository or catalogue write, owner closure, score change, independent self-acceptance, endpoint conclusion, or complete classification is performed.
