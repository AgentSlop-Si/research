# Independent acceptance: rank-two rigidity and the 12N Fourier tiling domain

Date: 18 October 2026 UTC. Candidate: `rectangle_rank_two_20261018_1240`.

## Verdict

**ACCEPT within the stated complex, disjoint/no-sharing rectangle model. No mathematical correction is required.**

The new rank-two rigidity lemma and its strict two-piece rank-one refinement are correct for every finite complex matrix whose entries have modulus one. For the complex cyclic Fourier matrix, the sharp minimum rank-two endpoint-cost density is `E_2(N)/N`, with `E_2(N)=min_{d|N,d<N}(2d+N/d)>D_N`. The exact disjoint-tiling optimum is `N D_N` whenever `D_N^2<12N`, with the complete stated rank-one-only, full-coset equality characterization.

In particular, `N=343` has optimum **19,208**, and `N=847` has optimum **74,536**. Their respective higher-rank-area penalties `1/49` and `1/77` are attained by actual complete tilings. The union with the accepted dominant-prime domain covers every length from 2 through 1000. Its first uncovered length is 1331, where only rank three remains an unresolved higher-rank obstruction to this method.

The owner remains **M-RECTANGLE-TILING, TO RESEARCH, priority 42**. This bounded extension does not close the general nonsquare composite problem. No external writes, publication, score, archival-status change, or worldwide novelty claim were made by this review.

Frozen candidate `REPORT.md` SHA-256:
`7aacb964f32e3061d1f1c0d7d1d554e281a3d5d219b53dc11948c7bc83971cdf`.

## 1. Model and accepted baseline

The objective remains exactly `sum_t r_t(a_t+b_t)`, where each tile is a nonempty Cartesian product of arbitrary row and column subsets, and `r_t` is its actual complex rank. Tiles partition all entries, with no overlap or sharing. In particular, splitting a row subset into its projective classes produces admissible rectangles; contiguity of indices is not part of this model.

The retained Phase7 audit explicitly supplies the rank-one subgroup/annihilator classification, rank-one optimum, complex stable-rank bound, and independent endpoint-incidence interpretation. The retained open-gate record requires this same higher-rank objective and preserves the general nonsquare-composite gate. I read those baseline records and both prior accepted reports/reviews. The candidate's four pinned dependency hashes and complete five-file manifest are checked before and after the fresh controls. This review uses the retained, pinned source chain; it does not claim to have fetched the repository again.

The dominant-prime result remains an accepted dependency only for the combined-domain census: if `N=mp`, p is prime, and `1<=m<p`, then the optimum is `N(m+p)`. The new rank-two lemma and 12N theorem themselves require no prime-minor result or other new external mathematical input.

## 2. Rank-two unit-modulus rigidity

The normalization is legitimate: multiplying column j by the conjugate of its first-row entry preserves all entry moduli, rank, and projective row/column equivalence. The first row becomes one. A second independent row z spans the row space together with that first row, and each coordinate of z lies on the unit circle.

Every row is therefore `alpha + beta z`. If z assumes only two values, every normalized column is determined by its z-coordinate. There are exactly two column directions because the matrix has rank two.

If z assumes at least three values, requiring every coordinate of the new row to have modulus one gives

`2 Re(conj(alpha) beta z_j) = 1-|alpha|^2-|beta|^2`.

For nonzero `conj(alpha) beta`, this is a genuine affine line in the complex plane, which cannot contain three distinct points of the unit circle. Thus `alpha beta=0`; every row is proportional to the first or second chosen row. Again the rank forces exactly two projective classes rather than one. This argument includes matrices with only two rows or only two columns.

Splitting those two row classes yields rank-one pieces with total cost `a+2b`, strictly less than `2a+2b` by exactly a. The column version costs `2a+b`, saving exactly b. Both pieces are nonempty and partition the original Cartesian tile. Replacing that tile leaves every other tile unchanged, proving that **no optimal disjoint tiling of any finite unit-modulus complex matrix contains a rank-two tile**. This is an actual cost-refinement theorem, stronger than a local Fourier-density inequality.

## 3. Sharp Fourier rank-two density and equality

Assume the row side has two projective classes. Generate H from the selected column differences, and put `K=H^perp`, `d=|K|`. Two Fourier rows restricted to these columns are proportional exactly when their difference belongs to K. Consequently the rows lie in two K-cosets and the columns in one H-coset:

`a<=2d`, `b<=N/d`, with `d|N` and `d<N`.

The proper-divisor restriction follows because trivial H would make all selected columns equal as indices and give rank one. Positive side sizes give

`2/a+2/b >= 1/d+2d/N >= E_2(N)/N`.

The other projective-class case is the transpose. There is no gap between the circle lemma and the subgroup envelope.

For every proper divisor d, `K union (1+K)` and `H=K^perp` produce the announced shape `2d` by `N/d`. The two K-cosets are disjoint since `N/d>=2`. On H, rows within either coset agree, and the two resulting characters are independent: the columns 0 and d give determinant `omega^(-d)-1`, which is nonzero by primitive order. Hence the actual complex rank is exactly two and the area is 2N. This attains `(2d+N/d)/N`.

Equality in both reciprocal bounds forces both side sets to fill their containing cosets and d to minimize E_2. Conversely, two arbitrary distinct full K-cosets and any full H-coset have rank two: translation changes only nonzero row/column factors, and distinct K-cosets restrict to distinct characters on H. Thus the stated equality characterization is complete, up to transposition. It does not mistakenly restrict the attaining cosets to the particular representatives 0 and 1.

Finally `2d+N/d=(d+N/d)+d>=D_N+d>D_N`. Minimizing over the finite nonempty proper-divisor set preserves strictness, including N=2.

## 4. Global theorem, equality, and quantitative gap

The unnormalized complex Fourier matrix has operator norm sqrt(N). Row/column restriction is contractive, so a rectangle has `ab<=Nr`. For `r>=3`,

`r(a+b)/(ab) >= 2r/sqrt(ab) >= 2sqrt(r/N) >= sqrt(12N)/N`.

The normalization, inequality directions, and rank threshold are correct. When `D_N^2<12N`, this density is strictly above `D_N/N`. Rank two has the separate strict bound from Section 3.

Rank one has density at least `D_N/N` by the inherited subgroup envelope. Equality requires both cosets to be full and their divisor pair to minimize `d+N/d`. Since the nonnegative tile areas sum to N², summing yields the global lower bound `N D_N`, and no positive local slack can cancel. Full subgroup/annihilator coset partitions attain it. Therefore every optimum has only rank-one tiles, every tile has area N, and every optimum has exactly N tiles. The classification is tilewise and does not require one common orientation throughout a tiling.

For arbitrary N, taking the minimum of the three valid rank-case constants gives the claimed sandwich

`N min(D_N,sqrt(12N)) <= min C <= N D_N`.

Within the strict domain, subtracting the rank-one baseline and summing gives the exact stated quantitative inequality with

`delta_N=min(E_2(N)-D_N,sqrt(12N)-D_N)/N`.

This applies to the total area of higher-rank tiles. It is neither a tile-count estimate nor a lower bound for a circuit that can share intermediates.

## 5. The target lengths and remaining obstruction

At 343, `(D,E_2)=(56,63)` and `D^2<E_2^2<12N`. Thus `delta=7/343=1/49`, and the optimum is `343*56=19,208`. The 14-by-49 rank-two rectangle is the union of two adjacent row-coset tiles over one annihilator column coset. Replacing those two rank-one tiles costs 14 extra, yielding a complete tiling of cost **19,222** with higher-rank area 686. It attains the area penalty exactly.

At 847, `(D,E_2)=(88,99)` and again `D^2<E_2^2<12N`. Thus `delta=11/847=1/77`, the optimum is **74,536**, and the analogous 22-by-77 merge gives a complete tiling of cost **74,558** with higher-rank area 1694. Its penalty is also exact globally, not merely on one isolated rectangle.

The square scalar shapes 26-by-26 at 343 and 41-by-41 at 847 satisfy stable-rank rank-two constraints but fail every rank-two divisor envelope. The report correctly concludes rank at least three for actual rectangles of those shapes without claiming rank three is attainable.

The census independently reproduces the transition: 343 and 847 are precisely the additional covered lengths through 1000, with none remaining in that interval. Through 10000 there are 44 new lengths and 25 residual lengths, starting at 1331. These are exact finite domain counts, not a claim that no other theorem could settle a residual length.

At 1331, `D=132`, `E_2=143`, and `12N=15972<D^2=17424<16N=21296`. Rank two is excluded by strict refinement, and every rank at least four has density strictly above D/N. Rank three is the remaining structural gate. The scalar tuple `(a,b,r)=(63,63,3)` satisfies `ab<=3N` while having density below D/N, illustrating why stable rank alone does not close this gate; this is not an asserted Fourier rectangle. The accepted bounds remain `1331 sqrt(15972) <= optimum <= 175692`.

The 4-by-4 unit-modulus counterexample to a naive rank-three projective-class extension is valid: it has exact rank three, four directions on each side, zero row sums, and the specified nonzero 3-by-3 minor `2-2i`. It is not asserted to be a cyclic Fourier submatrix or a counterexample to a possible higher-rank refinement theorem.

## 6. Fresh exact controls

The new `independent_controls.py` imports no author or earlier reviewer checker. It selects an exact algebraic root of each cyclotomic polynomial and computes characteristic-zero ranks over that number field. Actual projective classes are computed from exact entry ratios, and the rank-one pieces in each asserted refinement are separately rank-checked. No numerical singular-value threshold or finite-field rank substitutes for complex rank.

All controls passed in 33.089 seconds on SymPy 1.14.0:

1. **21,342** exhaustive nonempty Fourier subset rectangles at N=2 through 7, including **6,624** actual rank-two rectangles. The controls check exact ranks, both projective-class possibilities, exact ranks of every refinement piece, strict cost savings, the divisor envelope derived from actual selected differences, sharp density, and full-coset equality. Each length attains the predicted minimum rank-two density.
2. Fresh exact-cover dynamic programming over all disjoint tilings at **N=2,3,4** gives costs **6,12,16**, respectively, with **2,2,1** optimal tilings and no higher-rank optimum. This is a small global optimization control, independent of the density summation proof.
3. **625** normalized 3-by-3 matrices with entries drawn from five exact unit-modulus phases in Q(i), including the non-root-of-unity values `(3+4i)/5` and `(5+12i)/13`. Their ranks are 1,2,3 in counts 1,108,516; all rank-two cases pass the strict refinement test. Another **32** rectangular constructions test two through five distinct projective classes on one side and exactly two on the other.
4. **151** additional exact Fourier rectangles at N=8,9,10,12,15,16,18,20,24,25,27,35,49, including **83** actual rank-two examples and full-coset attaining constructions.
5. **1,108,027** divisor-envelope rank-two scalar shapes through N=500, including their equality restrictions; and **11,781,870** feasible rank-at-least-three scalar shapes across **300** eligible lengths through N=500. All inequalities use exact integers, including a squared check of the irrational stable-rank density branch. Scalar feasibility is not mislabeled as actual Fourier existence.
6. Both target optimal partitions and both target merged partitions have explicit once-only coverage of every entry. The four constructions cover **1,670,116** entries in total across their separate matrices, with **2,378** tiles in total. Their actual ranks, costs, higher-rank areas, and exact penalty equalities agree with the report. The two relaxed square rank-two shapes are excluded by independent divisor enumeration.
7. The finite-field negative control has rank two over F_23 but rank three over the exact characteristic-zero eleventh cyclotomic field, and three projective classes on each side. The separate rank-three unit-modulus counterexample has the claimed rank, projective classes, and nonzero minor.
8. An independent sieve-based census through **10,000** reproduces **44** newly covered lengths and **25** residual lengths; through 1000 it reproduces exactly the newly covered pair **343,847** and no residual lengths. The boundary data at 1331 and its scalar rank-three obstruction are checked exactly.

Detailed results are in `RESULTS.json`; the successful run is recorded in `controls.stdout.txt`. Source identities and the frozen input chain are in `SOURCES.json`.

All enumerations supplement the mathematical proofs; none is used to extrapolate an infinite-domain conclusion. Exact hashes are verified again after testing to detect changes to the frozen candidate.

## Accepted next-gate wording

Accept the universal strict two-piece rank-one refinement of every rank-two complex unit-modulus tile, the sharp Fourier rank-two density `E_2(N)/N>D_N/N`, and the exact disjoint-tile optimum `N D_N` whenever `D_N^2<12N`, with rank-one-only full-coset equality and the stated higher-rank-area penalty. Together with the accepted dominant-prime theorem this settles all lengths through 1000, including 343 and 847 at 19,208 and 74,536. The next uncovered length is 1331; rank-three Fourier structure is the next obstruction. General nonsquare composite lengths outside the combined domains remain open.

Preserve complex coefficients, disjoint/no-sharing Cartesian tiles, actual ranks, the exact endpoint-incidence objective, separate root/coefficient preparation, storage and I/O, and the inherited possible N extra additions for literal zero-initialized accumulation. No overlapping/cancelling decomposition, unrestricted Fourier circuit, general basis-change, finite-field rigidity, cold-cost, production-performance, or worldwide-priority conclusion follows. Parent status and priority remain unchanged.
