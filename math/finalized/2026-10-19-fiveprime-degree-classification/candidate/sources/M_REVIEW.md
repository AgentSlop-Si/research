# Independent review: order-5q middle open interval

Date: 2026-10-19 UTC. Independent symbolic audit and independently authored exact checks. This review concerns only the original binary fixed-phase model and the interval 2q<d<3q, for prime q>5.

## Verdict

PASS for the frozen packet, whose MANIFEST.json has SHA-256 bea917d6ee709f4c7ad1265dff18c4caa10a76776b4934ebb8fb2c3ddaacaa27. All 20 bound files and all seven source-copy bindings were checked. The exact verdict and source hashes are recorded in VERDICT.json. No proof repair is needed. This review does not assert any endpoint result, complete order-5q classification, general support-block geometry, novelty, historical priority, or FFT improvement. No external write was made.

The accepted statement is: for N=5q, R in {0,1}^{N by N}, and D[r,c]=R[r,c] zeta^(rc) with zeta any primitive Nth root, neither D*D=dI nor DD*=dI is possible when 2q<d<3q.

## Dependency-by-dependency challenge

1. **Square Gram implication and actual degrees.** Since d>0, either square Gram identity makes D invertible and implies the other. The two diagonal identities give both row and column degree d. The argument does not replace column regularity by an assumption about row blocks.

2. **CRT pairing is unchanged.** The actual indices are r=a e_5+b e_q and c=u e_5+v e_q. Orthogonal idempotents give rc=a u e_5+b v e_q modulo 5q. Thus the original root phase is exactly alpha^(au) beta^(bv); it is not an independently chosen tensor pairing. The products alpha^i beta^j for 0<=i<4 and 0<=j<q-1 are a rational basis: they span the cyclotomic field and their count is phi(5q)=4(q-1).

3. **Binary cancellation is correctly restricted.** Rational-basis reduction gives epsilon[i,j]-epsilon[i,q-1]-epsilon[4,j]+epsilon[4,q-1]=0. Hence epsilon=A+B with integral A,B. Two nonconstant integer arrays have combined range at least two and cannot produce a binary grid. Therefore a primitive zero overlap is a union of complete five-fibers or a union of complete q-lines. This is a binary statement, not an unproved general weighted descent. Character-coordinate multipliers are invertible and only permute these parallel families.

4. **Coverage counts the row itself.** There are exactly q+4 possible rows that agree with r in at least one CRT coordinate: q+5-1. Since d>=2q+1>q+4 for every prime q>5, each supported column of r has some supporting row differing in both coordinates. A full cycle through that entry lies inside the pair's overlap and hence inside r. Applying this argument entry by entry derives the row union of full cycles. It does not assume a common support, rectangular support, Cartesian support, uniform numbers of cycles, or any full-square-block geometry.

5. **Uniformity is proved in the correct order.** A row has at most two full q-lines because d<3q. If it had no full five-fiber, coverage would give degree at most 2q, so every B_r is nonempty. Two rows in the same a-group cannot share a full five-fiber: their prime-order balanced local intersection would be five everywhere, contradicting d<3q. Thus the q nonempty B_r are pairwise disjoint subsets of a q-element set. They must all be singletons. Only after this counting step is f_r=1 imposed. The exact union count gives d=5+ell_r(q-1), and the target interval forces ell_r=2 and d=2q+3 in every row.

6. **Within-group two-line sets are derived.** Distinct rows in one group have distinct singleton special fibers. Their common support contains exactly two points on each of those fibers and |A_r intersect A_s| on any of the other q-2 fibers. Prime balance forces intersection size two, hence equal two-element sets. The singleton fiber assignments are arbitrary bijections; no equality between their maps in different groups is needed.

7. **Column counting is exact.** For fixed u, if h_u groups have u in A_a, each such group contributes q rows to every column (u,v), and each of the other 5-h_u groups contributes exactly one, by its fiber bijection. Thus d=5+h_u(q-1), so h_u=2. The five baseline pairs cannot all coincide. This uses simultaneous row/column constraints and does not silently strengthen row orthogonality alone.

8. **Cross-group contradiction works with unrelated permutations.** Choose distinct baseline pairs. For any row in the first group, at most one second-group row has the same b coordinate, and at most one has the same special fiber. At most two exclusions leave an eligible row because q>5. Their character is primitive, but their overlap has two points in each of two special fibers and h<=1 points in every other fiber. It is not a union of full five-fibers, and its nonconstant fiber sizes prevent it from being a union of full q-lines. This contradicts the exact binary cancellation lemma.

9. **The q=7 boundary has no hidden gap.** Here q+4=11 and the target degrees are 15 through 20. Coverage is strict throughout. Disjointness forces the sole residual degree 17, the selection leaves at least five rows, and there are five other fibers for the final cardinality contradiction. Nothing from the exceptional first-interior q=7 row-group geometry is used.

10. **Inherited normalization and bound.** The normalized mask has Gram (d/N)I. The accepted equality/attainment source therefore yields Delta_(5q,5q-d)>sqrt(d/(5q)). Substitution into the separately accepted bound 1/[10 N d^(phi(N)-1)] gives exactly 1/[50 q d^(4q-5)]. These implications are inherited and do not newly prove their source theorems or sharpness.

## Independent exact evidence

The fresh standard-library program independent_check.py evaluates root sums in the original indices by integer polynomial remainder modulo Phi_(5q). It does not call the candidate checker or historical scripts, and does not use floating tolerance.

- It checks all original CRT phase products at q=7,11,13: 8,475 congruences.
- It tests every pair of two-element baseline sets and every pair of singleton fiber choices. At q=7 and q=11 it tests every primitive character; at q=13 it tests one primitive character. Total: 618,500 exact overlap checks. Zero is found exactly when either baseline sets agree and special fibers differ, or baseline sets are disjoint and special fibers agree. In particular every final-obstruction pair is nonzero.
- It constructs full-square negative masks with A_a={a,a+1} and group-dependent permutations f_a(b)=(a+1)b+a modulo q. This deliberately avoids a common fiber map. Every row and column has degree 2q+3, and all same-group row Grams vanish, but both complete Grams fail. Explicit original-index primitive witnesses are retained in RESULTS.json.
- It checks the positive divisor mask supported on u=a, including both complete Grams at q=7,11,13: 16,950 diagonal/off-diagonal Gram entries.

The candidate checker was also inspected and rerun in a separate copied directory. Its source, source bindings, five generated JSON result files, stdout, and empty stderr matched the frozen candidate byte-for-byte. Its 157,000 full Gram entries and 486,720 primitive-overlap tests passed.

These are exact finite corroborations of the symbolic proof, not a census of all square masks. The negative controls demonstrate why rectangular row-group conditions alone do not finish the problem. RUN.stderr is empty and RUN.stdout records PASS.

## Scope retained

Only 2q<d<3q is accepted here. Endpoints 2q and 3q, other order-5q intervals, complete semiprime classification, uniform divisibility, exact nonsharp optima, novelty, and FFT complexity remain outside this review. Owner M-SPARSE-DEFECT remains TO RESEARCH, priority 42.
