# Independent acceptance: sharp prime-cube rank-three bound and N = 2197

Date: 18 October 2026 UTC. Candidate: `prime_cube_sharp_rank_three_20261018_1748`.

## Verdict

**ACCEPT the frozen report. No mathematical correction is required.**

For every prime p≥5, a rectangle of the complex cyclic Fourier matrix F_(p³) with rank at most three has

    min(a,b) ≤ 3p.

The exact minimum endpoint-cost density among actual rank-three rectangles is

    3(a+b)/(ab) = (p+3)/p².

Here equality is attained by the displayed p²-by-3p construction; acceptance does not assert a classification of all rank-three equality rectangles.

At N=2197=13³, the exact disjoint-rectangle optimum is **399854**. Every optimizer has exactly **2197 rank-one full subgroup-coset × annihilator-coset rectangles**, each with unordered side sizes **{13,169}**. The quantitative bound

    cost ≥ 399854 + A_(rank≥2)/676

is valid, without a sharpness claim for its penalty coefficient. The precisely retained accepted-domain union, extended by this target, covers every length from 2 through 2872; **2873=13²·17** is the next residual, with rank three the remaining gate there.

Frozen candidate REPORT.md SHA-256:

    92316a9c91dfcb8d0817bd16a534155020ca20fe09bdae24bb4e0eeb9debb729

All six candidate artifacts and all six pinned local dependencies were hash-verified before and after the independent controls. The checker neither imports nor executes any author or earlier reviewer checker. The review uses the accepted local source chain and does not claim a fresh repository fetch. No external writes or additional agents were used.

## 1. Model and dependency audit

The cost is exactly Σ_t r_t(a_t+b_t), with actual complex rank r_t. The nonempty Cartesian tiles partition all N² entries. Arbitrary row/column subsets are allowed; disjoint coverage and the absence of sharing are retained.

The rank-two accepted report and review supply the rank-one coset equality classification, the sharp rank-two density E₂(N)/N, and the stable-rank inequality ab≤Nr. The preceding prime-cube report and its acceptance explicitly supply the **four-fiber occupancy theorem**, not merely its weaker scalar min(a,b)≤4p consequence. This is the precise hypothesis required by the new proof.

The accepted occupancy proof selects one of U, A=(4), B=(3,1), or C=(2,2) from five distinct residues modulo p² and proves every selected pairing nonsingular. In the delicate B–C case, the two translated three-element subsets of F_p differ because 3<p. A uniquely occurring second-level cyclotomic basis exponent then has a nonzero coefficient. The pinned review explicitly accepts the occupancy statement and this mixed case. There is no reliance here on the unproved assertion that every arbitrary four-by-four minor injective modulo p² is nonsingular.

The universal prime-power-minor lemma is also correctly retained: for k≤p, one side distinct modulo p and the other distinct modulo p^m suffice. The alternating determinant divided by its ordinary Vandermonde has an integer all-ones value nonzero modulo p; reduction modulo 1−ζ preserves that nonvanishing. At m=1 this supplies every prime Fourier minor used in the new lemmas.

The mixed-prime accepted packet is background for the proof strategy and for the retained N=11q² domain. The new p² support lemma and p³ direct-sum proof are supplied afresh. No CRT identification of Z_(p²) with Z_p×Z_p, or substitution of equal primes into a distinct-prime theorem, occurs.

## 2. Prime-square short-support zeros

The digit calculation is exact. For a frequency v+pu and a point y+pz,

    η^((v+pu)(y+pz)) = η^(vy) ω^(vz) ω^(uy),

because the remaining exponent is a multiple of p². Thus the displayed decomposition into g_v(y) is valid for arbitrary complex coefficients and all higher digits.

Each nonzero group g_v uses k_v distinct prime-order characters. It is not the zero function, and a nonzero prime Fourier minor bounds its zeros by k_v−1. If z₀ values of y kill all groups, then z₀≤min_v(k_v−1)≤k′−t. At every other y, there are between one and t active prime-order characters, so at most t−1 zeros in z. Consequently

    Z ≤ p(t−1)+(p−t+1)z₀
      ≤ p(t−1)+p(k′−t)
      = p(k′−1).

All inequalities have their required signs: 1≤t≤k′≤k≤p and z₀≥0. Allowing k′<k handles zero coefficients in a putative dependence. A dependence among k selected columns on more than (k−1)p rows would contradict this zero count. Lemma 1 follows exactly as stated.

The strict threshold is meaningful: products of k−1 distinct linear factors in the p-order character have exactly (k−1)p zeros. The independent controls verify such boundary examples, as well as arbitrary sparse combinations. These examples do not supply the universal proof; the digit argument does.

## 3. Rich-fiber direct-sum separation

For r=y+pk and c=v+p²w, the lift-dependent factor is precisely ω^(yw), independent of k. Distinct selected lifts w and distinct occurring residues y give an invertible s-by-s prime Fourier matrix whenever s≤p.

Inversion therefore produces the representative column at v, supported on one chosen row-residue class and zero on every other class, as a linear combination of selected columns. The representative v itself need not belong to C. Its supported vector is still produced by the mixing inverse.

On a fixed row class, removing the nonzero scalar ζ_(p³)^(yv) from the supported representative leaves η^(kv). Scalars may depend on both y and v because the separate block ranks are computed independently. Hence the generated block span has dimension rank F_(p²)[A_y,T]. Different row classes have disjoint supports, so their spans form a direct sum inside the original column span. This proves Lemma 2 without any interaction or shared computation between different tiles.

For s=3, one fiber with three selected lifts already supplies three independent columns. Under rank≤3 these columns span the whole rectangle. Two rows from the same residue class have proportional restrictions to that basis, with a nonzero proportionality factor. Linear combinations of the basis columns preserve the same proportionality on all of C. The rectangle therefore has at most three projective row classes. This is a conditional basis argument, not the false general assertion that every unit-modulus rank-three matrix has three row directions.

For completeness, fixing c₀ and taking H generated by C−c₀ gives exact projective equivalence:

    rows r,r′ are proportional on C
      iff ζ^((r−r′)(c−c₀))=1 for all c∈C
      iff r−r′∈H-perpendicular.

With d=|H-perpendicular|, each class lies in one coset of size d, and C lies in one H-coset of size p³/d. Thus a≤3d and b≤p³/d, with d|p³. No extra completeness assumption about the selected row classes is needed.

## 4. Exhaustion of the side-bound proof

Assume a,b>3p. By the accepted occupancy theorem, transpose so C occupies at most four fibers modulo p². Each contains at most p indices, so there must be exactly four occupied fibers.

If R occupies at least four residues modulo p, four rows distinct modulo p and any four columns give a nonsingular minor at order p³. The condition 4≤p holds. Hence the row-residue count s is exactly one, two, or three.

- **s=1.** Removing column phases reduces to F_(p²) on more than 3p distinct rows and four distinct columns. Lemma 1 with k=4 forces rank at least four.
- **s=2.** At least three of the four column fibers contain two or more points. Otherwise b≤2p+2≤3p, a contradiction. For the two nonempty row classes, a₁+a₂>3p implies either max(a₁,a₂)>2p or both a_i>p. The first branch contributes block ranks at least 3+1 using three rich fibers. The second contributes at least 2+2 using two of those fibers. Lemma 2 adds the ranks. This is the complete dichotomy, including the strengthened branch needed at the 3p threshold.
- **s=3.** Some fiber contains at least three points, since otherwise b≤8<3p. The basis/projective argument gives a≤3d and b≤p³/d. Since a>3p, d>p. Among divisors of p³, only p² and p³ remain, forcing b≤p, a contradiction.

All cases contradict rank≤3. There is no gap at a=3p or b=3p: those values are explicitly allowed by the conclusion and occur in the sharp construction.

## 5. Sharp rank-three density

Order the sides a≤b. For actual rank three, the new theorem gives a≤3p, while stable rank gives b≤3p³/a. Therefore

    3/a+3/b ≥ 3/a+a/p³.

The candidate's exact difference identity is correct:

    [3/a+a/p³]−[1/p+3/p²]
      = (3p−a)(1/(pa)−1/p³).

For p≥5 and a≤3p<p² both factors are nonnegative. Thus the asserted density floor follows. In fact equality of these scalar steps forces a=3p and b=p², although this does not classify the underlying Fourier subsets.

For R=pZ_(p³) and C the union of the three full fibers v=0,1,2 modulo p², columns within each fiber coincide on R. Thus rank≤3. The rows 0,p,2p and columns 0,1,2 give the nonsingular order-p² three-minor, so actual rank is exactly three. The sides are p² and 3p, the area is 3p³, and the density equals (p+3)/p². Both the density bound and the side cutoff are attained.

## 6. Target optimum, equality, and penalty

At N=2197, the nearest divisor pair is uniquely {13,169}, so D=182 and D/N=14/169. The retained rank-two formula gives E₂=195 and density 15/169. The new sharp rank-three floor is 16/169.

For r≥4, stable rank and AM–GM give density at least 4/√2197. The target common higher-rank floor is 57/676, and the exact comparison is

    16/2197 > (57/676)²,

or equivalently 3328>3249 after clearing positive denominators. Both other higher-rank floors exceed 57/676 as well. Subtracting the baseline 56/676 leaves the claimed positive penalty 1/676.

Disjoint coverage gives Σab=N², so summing the tilewise inequalities yields

    cost ≥ N D + A_(rank≥2)/676 = 399854 + A_(rank≥2)/676.

A full subgroup/annihilator coset partition attains ND. The independent control uses the transposed orientation: 13 row cosets of size 169 and 169 column cosets of size 13. It verifies every entry exactly once and every rank-one phase condition.

Any higher-rank tile has positive area and strictly positive density slack, so no optimizer contains one. The remaining rank-one inequalities must all be equalities. The accepted equality theorem then forces full mutually annihilating coset products with the unique unordered minimizing sizes {13,169}. Every such tile has area N, so every optimum has exactly N tiles. Tile orientations need not be common. No sharp penalty or unrestricted-circuit conclusion is inferred.

## 7. Fresh exact controls

`independent_controls.py` uses a subset dynamic program for determinant polynomials, followed by literal monic long division by Φ_(p^m). It does not reuse the author's signed-permutation implementation or fiber-coefficient reducer. These are characteristic-zero computations. Separately implemented SymPy remainders cross-check the reducer, including zero determinants.

All controls passed in 16.053 seconds:

1. All **7,641** threshold row-set/column-support pairs at order nine for k=1,2,3, and all **12,650** four-column supports at order 25 against a concentrated 16-row boundary set.
2. **560** sparse complex-coefficient polynomials and **56** sharp zero-bound examples across six primes, including the p=3 boundary of Lemma 1 independently of the p≥5 theorem.
3. **1,960** fresh rich-fiber examples across both 3+1 and 2+2 branches for p=5,7,11,13,17,23,29. The selected fibers deliberately omit their zero-lift representatives.
4. **216** general direct-sum full-rank square minors, including s=3 and s=4 and ranks as high as six. These test the direct-sum lemma beyond the theorem's contradiction cases.
5. All **400** retained target certificates recomputed independently, with exact equality of their nonzero cyclotomic remainders.
6. Every ordered four-fiber occupancy and every relevant two-class size split for seven tested primes, plus **9,800** exact projective-equivalence comparisons using the subgroup generated by the actual column differences.
7. Sharp-family nonzero three-minors, vanishing four-minors, and rational density identities for **166 primes** from 5 through 997.
8. All **21,784** target scalar shapes under the new cutoff, with minimum 16/169 attained only at unordered sizes {39,169}; the **12** previous scalar obstructions are all excluded by the new side bound.
9. The full **2197-tile** transposed target partition, covering all **4,826,809 entries** exactly once and costing **399854**.
10. An independent prime-sieve/divisor census through **10000**, and **84** independent symbolic remainder cross-checks.

The exact-minor counters total **133,398**: **128,680** at prime-square order and **4,718** at prime-cube order. Counts, results, source hashes, and output are retained in the review packet. Finite controls supplement the universal proofs and do not establish them by sampling.

## 8. Exact remaining boundary

The retained union is D_N²<12N, the dominant-prime domain, the isolated accepted N=1331, and N=11q² for prime q>11. Adding exactly N=2197 removes its first residual and leaves **2873=13²·17** next. The independent census agrees with the entire reported residual list through 10000.

At 2873, D=186 and

    12N=34476 < D²=34596 < 16N=45968.

Rank two is excluded by the accepted result, and all ranks at least four have strict stable-rank density slack. Rank three remains unresolved. The repeated prime 13 is smaller than the other prime 17, so the accepted p<q theorem for N=pq² does not apply with p=17,q=13. The new prime-cube theorem also does not apply to this mixed-prime length.

## Accepted next-gate wording

Accept the sharp prime-cube theorem for every prime p≥5: rank-at-most-three rectangles in F_(p³) have min(a,b)≤3p, and the exact minimum actual rank-three density is (p+3)/p². The proof uses the accepted four-fiber occupancy theorem, a proved prime-square short-support zero bound, and direct-sum separation, including both 3+1 and 2+2 branches in the two-residue case. At N=2197 accept optimum 399854, rank-one-only full-coset equality with exactly 2197 tiles of unordered sizes {13,169}, and the valid higher-rank-area penalty 1/676. The exact retained-domain union covers every length through 2872; the next residual is 2873=13²·17 at rank three.

Preserve actual complex ranks, disjoint/no-sharing endpoint-incidence cost, separate root/coefficient preparation, storage and I/O, and the inherited possible N extra additions for literal zero-initialized accumulation. Do not infer a full rank-three equality classification, an optimal penalty coefficient, arbitrary basis-change or finite-field rigidity results, unrestricted Fourier-circuit lower bounds, production performance, or worldwide novelty. Owner M-RECTANGLE-TILING remains TO RESEARCH, priority 42; the general nonsquare-composite problem remains open.
