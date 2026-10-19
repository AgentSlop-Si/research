# Independent review: order-35 first-interior exclusion

Date: 2026-10-19 UTC.

## Verdict

**PASS, scoped to the frozen candidate below.** The symbolic argument proves that no binary 35-by-35 original fixed-Fourier-phase mask has degree d in {8,9,10,11,12,13} and satisfies either Gram equality. Both Gram equalities follow from either one because the matrix is square and d>0. The proof uses column regularity essentially; it does not promote a rectangular row Gram to a square solution.

Reviewed candidate directory: `/workspace/shared/fiveprime_q7_boundary_20261019_1430`.

- Candidate manifest SHA-256: `5664318bea1b9be54d36b8dc99c3733c016f5e09a18375c581daa1505d0fc95c`
- Candidate report SHA-256: `84d43836ff591b5a667213f1c23475bd6b866fd4aa788db5a43bc9ec1a264b6d`
- Candidate checker SHA-256: `fffb2adbd326f4218080f22fb39cd183918187c3c52c3741f265cfc342f85c22`

All 19 manifest entries, the complete inventory, seal, and three historical source bindings were independently verified. The author's standard-library checker was rerun in a separate review copy. Its generated artifacts are byte-identical to the frozen manifest entries; the candidate and accepted historical files were not changed.

This closes only the q=7 exception to the already accepted first-interior theorem for N=5q, prime q>=11. It does not classify degrees at or above 14 for N=35, all degrees of N=5q, or general odd semiprimes. The earlier theorem remains an independently attributed accepted result. No historical-priority or novelty determination is made here.

## Symbolic proof audit

### 1. Original phases and character types

The idempotents 21 and 15 satisfy the correct CRT congruences, square to themselves modulo 35, have product zero modulo 35, and sum to one modulo 35. Thus the pairing is exactly the original r*c pairing after a bijective relabelling, not a replacement Fourier model.

For a difference confined to the seven-coordinate factor, the order-seven minimal polynomial forces all seven fiber intersection counts equal. Because the total overlap is at most d<14, the common count is zero or one. The corresponding order-five balance used later is also valid; it forces equal line counts, without an unwarranted individual 0/1 restriction on those counts.

For a difference nonzero in both coordinates, the 24 products alpha^i beta^j are a rational basis. Eliminating the last row and column of the binary coefficient array gives the stated additive form A_i+B_j. If both integer lists vary, their maxima-minus-minima sum is at least two, impossible for an array taking values only zero and one. Therefore a vanishing binary overlap is a union of whole five-fibers or a union of whole seven-lines. This is a symbolic completeness proof, not an inference from finitely tested subsets. Nonzero character multipliers merely permute the coordinate labels.

The report preserves the classical de Bruijn / Lam–Leung attribution. Its elementary derivation makes the application self-contained. This review does not relabel that cancellation lemma as a new contribution.

### 2. Clique structure and complete local incidence table

Every row has some fiber of weight at most one. An empty fiber makes the row isolated; a singleton makes all of its neighbors share that point and hence be pairwise adjacent. A graph in which every neighborhood is a clique has clique connected components. Distinct components have disjoint entire supports. Five representatives would have total disjoint support at least 5d>35, so there are at most four components.

For a nonstar restriction, a singleton row would be a common point for every row, so all row weights are at least two. The identity WW^T=diag(w_i-1)+J is positive definite, proving n<=k<=5. This also excludes hidden repeated non-singleton restrictions.

The listed nonstar cases are complete. For three rows, the three pair-meeting points are distinct. For four rows, pair-count six on at most five coordinates leaves the single-triple/three-double pattern, while two triples share two rows and are forbidden. For five rows, the three possible numerical multiplicity patterns listed in the candidate are exhaustive; the first two force repeated row-pair intersections, and the last is the near-pencil. Hence their incidence totals are exactly the stated values.

Distinct components have disjoint coordinate unions in a fiber. Summing all permitted local types reproduces every one of the eleven partition maxima. No assumption of full square support blocks occurs. The independent checker additionally enumerated valid local multisets through component size seven, rather than relying computationally on the rank reduction for six and seven; it agrees exactly with the symbolic list.

### 3. Degrees 12 and 13, and the preliminary degree-11 reduction

The incidence ceiling twelve in every fiber implies d<=12. At degree twelve every fiber must attain its partition ceiling. The only possibilities are 3+4 with component incidence (3,9), or 1+1+5 with (0,0,12). They force the three-clique rows to degree seven, or the two singleton rows to degree zero, respectively. Both contradict the proposed common degree.

For d=11 the only remaining partition maxima are 7, 3+4, 1+1+5, and 1+2+4. Saturation for 1+2+4 forces the singleton empty in every fiber. For 1+1+5 the valid inequality is 4 I_5+7 I_s<=48 per fiber. Across seven fibers its left-hand side is 4(5d)+7(2d)=34d, so 34d<=336 and integer d<=9. The coefficients and direction are correct. This leaves only seven-cliques and 3+4 splits.

### 4. Multiplicity and full-line lemmas

Two multiplicity-at-least-four coordinates cannot lie in different components of seven rows. Within a star, only the center repeats. Within a nonstar, n<=5, so two sets of at least four row incidences would share at least three rows, contradicting pairwise intersection one. Thus there is at most one high-multiplicity coordinate in each fiber.

Every row has at most one full seven-line because d<14. If two clique rows have the same full line, their exact-one fiber intersections exhaust their overlap. A third row on another full line cannot be singleton in any fiber: its singleton would force the first two rows to share a second point there. Its degree would therefore be at least fourteen. This proves the dichotomy that all line labels in a clique are equal or all are distinct. In the distinct case at most one row can be singleton in a fiber, yielding nd>=7(2n-1). The claimed thresholds d>=12 for n=3 and d>=13 for n=4 are correctly rounded.

### 5. Degrees 8, 9, and 10

A nonsingleton component meets every fiber, so a full fiber would force degree at least eleven. A singleton component has another nonsingleton component in its group (seven rows and at most four components); disjointness from that component prevents a full fiber as well.

A row without a full line or full fiber has zero intersection with every primitive partner. At any column it supports, each of the other four groups supplies at most its one row having the same seven-coordinate label. Column degree d therefore forces at least d-4>=4 incidences inside its own group. The high-multiplicity lemma allows at most seven such columns, contradicting its degree greater than seven. This establishes full-line existence without assuming it.

For two rows on different baseline lines, their intersection is contained in the union of their t=d-7 extra entries, hence has size at most 2t<=6. Same-group, primitive, and order-five differences are all addressed separately. In the order-five case a row occupies at most four line labels, providing a zero count and therefore zero in every line. The distinct baseline classes consequently have disjoint supports. Each occupied line has exactly the number n_u of rows in its class, giving n_u=d and 35=hd. None of 8,9,10 divides 35. The argument does not assume that extra entries are absent.

### 6. Degree eleven: split groups

A 3+4 row group cannot contain a full fiber in any row because the other component occupies a disjoint point in every fiber. A row lacking a full line would then need own-group column multiplicity at least 11-4=7, whereas a split group's multiplicity is at most four. Thus every row has a full line.

The line lemma forces each component to have one common line, since distinct labels in sizes three and four already require degree at least twelve and thirteen. Each fiber is then a pair of disjoint stars, whose combined incidence is 7+(k_1+k_2)-2<=10. Its average would have to be eleven, a contradiction. This eliminates all 3+4 groups regardless of what types other groups initially had.

### 7. Degree eleven: all groups single seven-cliques

After split elimination every group is a seven-clique. Rank excludes nonstars, and average incidence eleven saturates every fiber's star ceiling. Consequently each group covers all five coordinates in each fiber, with one multiplicity-seven center and four multiplicity-one private coordinates. A column that is a center for h groups has degree 7h+(5-h)=5+6h. Degree eleven forces h=1, so the five baseline sets are disjoint and partition all columns.

Choose an extra column of a row r, and the other group G whose baseline contains it. All seven G rows meet r at that column; exactly six have a different seven-coordinate label and hence a primitive difference. Their overlaps are contained in the two four-element extra sets because the baseline sets are disjoint, so have size at most eight.

If r had no full seven-line, each of these six nonempty primitive overlaps would be exactly one five-fiber. A row has only four extras beyond its one-point-per-fiber baseline, so it can contain at most one full fiber. All six G rows would therefore contain that same fiber. But every off-baseline coordinate in G has multiplicity one, so at most one G row can contain the full fiber. This contradiction proves every row contains a full line.

Seven rows and only five line labels give a repeated label. The line lemma forces the entire clique to share it. The common intersection of its seven rows is exactly its baseline, making that baseline the full line. Different groups get different full lines. Repeating the extra-column argument, two such rows cannot share a full line because their unique full lines differ. Each primitive overlap must again be the same full fiber of r, producing the same six-versus-one contradiction. There is no circular invocation of full-line existence or baseline linearity.

## Exact retained rectangular control

The historical binary block is unchanged. Its actual row indices are 0,15,30,10,25,5,20. Independent original-phase evaluation verifies all 49 row Gram entries: DD*=11 I_7. Its column Gram is not 11 I_35; the column degrees are nonconstant, and column 5 has diagonal entry two.

Direct support inspection confirms that six rows contain neither a full five-fiber nor a full seven-line. Original row 5 alone contains L_3; no row contains a full fiber. Original row 0 contains original column 5, and the retained block has exactly two incidences in that column.

In a square extension, any row in one of the other four groups whose seven-coordinate label differs from row 0 is a primitive partner. Such a row must be disjoint from row 0, since a nonempty overlap would supply a whole fiber or line inside row 0. Only one row from each other group can contribute to column 5. Therefore its completed degree is at most 2+4=6, strictly below eleven. This is an exact extension obstruction for the particular retained block, independent of the general degree-eleven exclusion. It is neither a failed extension search nor a square existence control.

## Independent exact controls and reproducibility

Run `python independent_check.py` in this review directory. The checker uses integer arithmetic and the Python standard library. It does not import or call the candidate's proof checker.

Unlike the candidate's univariate Phi_35 remainder basis, this checker uses the tensor basis alpha^i beta^j, reducing alpha^4 and beta^6 separately. It:

- Enumerates all valid five-coordinate local multisets through component size seven, including repeated singleton restrictions and empty singleton components.
- Recomputes all eleven partition maxima and the weighted 1+1+5 certificate.
- Verifies all 1,225 original CRT pairing congruences.
- Evaluates both complete Grams of four divisor-positive masks and six fresh regular cyclic negative masks, degrees 8 through 13: 24,500 exact Gram entries.
- Independently recomputes both Grams of all eight submitted masks: 19,600 more entries. It checks every reported failure residue by transforming the candidate's univariate residue into the independent tensor basis, and checks the complete pass/fail counts by character order.
- Verifies 3,792 primitive full-fiber/full-line union controls, 840 primitive singleton negatives, and nonprimitive equal-count and single-imbalance controls.
- Recomputes the retained rectangular row Gram, its column degrees, each row's full-line/full-fiber status, and the 6<11 obstruction.

All passed. These controls corroborate the exact local claims and phase implementation. They are not an exhaustive search over binary square masks and do not establish the theorem without the symbolic audit above.

The candidate's two exploratory SciPy scripts are segregated under `development/`; their optimization output is not used as mathematical evidence. No numerical infeasibility or floating-point tolerance is needed in the accepted proof. No substantive proof gap or required correction was found. The historical source is retained with its original scope and attribution, and this review makes no external writes or repository changes.
