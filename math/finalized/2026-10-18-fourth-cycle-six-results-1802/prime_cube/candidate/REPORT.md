# Sharp prime-cube rank-three separation settles N = 2197

Date: 18 October 2026 UTC. Owner: M-RECTANGLE-TILING, priority 42.
Status: author-side theorem; independent acceptance pending. No external writes.

## Result

For every prime p≥5, every rectangle of the complex cyclic Fourier matrix F_(p³) having rank at most three satisfies

    min(|R|,|C|) ≤ 3p.

For rectangles of actual rank three, the sharp density is consequently

    3(|R|+|C|)/(|R||C|) ≥ (p+3)/p².

Equality is attained by the p²×3p rectangle consisting of all rows divisible by p and three full column fibers modulo p². No classification of every rank-three equality case is asserted.

At **N=2197=13³**, the exact disjoint-rectangle endpoint-incidence optimum is **399,854 = N D_N**, with D_N=182. Every optimizer consists of exactly 2197 rank-one full subgroup-coset × annihilator-coset rectangles, each with unordered side sizes {13,169}. A valid, not-claimed-sharp quantitative bound is

    total cost ≥ 399854 + A_(rank≥2)/676.

Together with the precisely retained accepted-domain union, this settles every N from 2 through 2872. The next residual is **2873=13²·17**, again at rank three.

The new proof strengthens the accepted 4p bound using large fiber occupancies, a prime-square short-support lemma, and direct-sum separation. It does not need the unproved claim that every four-by-four minor injective modulo p² is nonsingular.

## 1. Exact model and retained dependencies

Write F_N[r,c]=ζ_N^(rc) with ζ_N a primitive N-th root. A tiling partitions all N² entries into disjoint, nonempty Cartesian rectangles R_t×C_t. A tile with side sizes a,b and actual complex rank r costs r(a+b). Higher-rank area A_(rank≥2) is the total number of entries in tiles having actual rank at least two.

Retain the accepted rank-one coset/density classification, sharp rank-two density, and stable-rank inequality ab≤Nr. The frozen local sources are rectangle_rank_two_20261018_1240 and rank_two_review_20261018_1248. The accepted prime-cube result and review, rank_three_prime_cube_20261018_1332 and prime_cube_rank_three_review_20261018_1340, supply these two facts:

1. **Universal prime-power minors.** If k≤p, k distinct rows of F_(p^m) are pairwise distinct modulo p, and k columns are distinct modulo p^m, then their minor is nonsingular. The transposed assertion also holds.
2. **Four-fiber occupancy bound.** If a rectangle of F_(p³) has rank at most three, at least one side occupies at most four distinct residues modulo p².

The second is the stronger occupancy form of the accepted 4p theorem, rather than an inference from its scalar consequence. Its complete proof selects four-point patterns from five residues and treats the mixed (3,1)–(2,2) case with two cyclotomic field extensions.

The argument below is also informed by the accepted mixed-prime direct-sum proof in mixed_prime_rank_three_20261018_1501 and its review mixed_prime_rank_three_review_20261018_1514. Here the required square-order support lemma and direct-sum statement are proved explicitly for p² and p³. No mixed-prime theorem is silently applied with equal primes.

All ranks, spans, and orthogonality are over C. The disjoint/no-sharing model is retained. Root supply and coefficient preparation, storage, and I/O remain separate; the inherited possible N extra additions for literal zero-initialized accumulation are unchanged. No claim is made about unrestricted Fourier circuits, arbitrary basis changes, overlap/cancellation between tiles, finite-field rigidity, production performance, or worldwide novelty. Parent TO RESEARCH status and priority 42 are unchanged. Source hashes are recorded in SOURCES.json.

## 2. Short-support zeros at prime-square order

**Lemma 1.** Let p be prime and 1≤k≤p. A nonzero linear combination of at most k distinct characters of Z_(p²) has at most (k−1)p zeros. In particular, if |A|>(k−1)p and T contains k distinct residues modulo p², then F_(p²)[A,T] has column rank k.

**Proof.** Put η=ζ_(p²), ω=η^p. Use exactly k′≤k nonzero terms. Group the frequencies by their residue v modulo p, writing each as v+p u. Let V be the occurring residues, t=|V|, and k_v the number of terms in group v. Thus ∑_v k_v=k′. For x=y+p z, with 0≤y,z<p,

    f(y+p z) = ∑_(v∈V) η^(v y) ω^(v z) g_v(y),
    g_v(y) = ∑_u c_(v,u) ω^(u y).

Every g_v is nonzero and uses k_v distinct prime-order characters. Prime Fourier nonvanishing minors therefore give at most k_v−1 zeros. Let z₀ be the number of y at which all g_v vanish. Then

    z₀ ≤ min_v(k_v−1) ≤ k′−t.

For each other y, the function of z is a nonzero combination of at most t prime-order characters, so it has at most t−1 zeros. Hence the total number of zeros satisfies

    Z ≤ p z₀ + (p−z₀)(t−1)
      = p(t−1) + (p−t+1)z₀
      ≤ p(t−1) + p(k′−t)
      = p(k′−1) ≤ p(k−1).

The inequality uses z₀≥0, z₀≤k′−t, and 1≤t≤k′≤p. A column dependence on A would be a nonzero combination with at most k terms vanishing on more than (k−1)p points, a contradiction. This proves the rank statement. QED.

This is an explicit digit decomposition, rather than a Chinese-remainder identification of Z_(p²) with Z_p×Z_p.

## 3. Separating row-residue subspaces

**Lemma 2.** Let R occupy s residue classes y modulo p, with 1≤s≤p. For each such y set

    A_y = { (r−y)/p modulo p² : r∈R, r≡y modulo p }.

A column fiber means one residue v modulo p², whose members are v+p²w. Let T be a set of column fibers each containing at least s selected columns. Then

    rank F_(p³)[R,C] ≥ ∑_y rank F_(p²)[A_y,T].

**Proof.** Put ω=ζ_(p³)^(p²). On row r=y+p k, the column at v+p²w is the representative column at v multiplied by ω^(y w). For s selected lifts in one fiber, the s-by-s mixing matrix [ω^(y w)] is a nonsingular prime Fourier minor. Inverting it produces, inside the original column span, the representative column supported separately on each single row-residue class.

On the class y, the representative entries are

    ζ_(p³)^(yv) (ζ_(p³)^p)^(k v).

After removing the nonzero scalar for that representative and class, their matrix is F_(p²)[A_y,T]. Different row classes have disjoint supports. The supported spans thus add directly, proving the inequality. QED.

The lemma describes subspaces within one Fourier rectangle. It does not permit sharing, overlap, or cancellation between tiles.

We will also use the following consequence when s=3 and one selected fiber contains at least three columns. Those three columns are independent by the mixing matrix. If the whole rectangle has rank at most three, they span every column. On these three columns, rows in any one residue class modulo p are proportional. As these columns span, the same proportionality holds on the entire selected column set. There are at most three projective row classes.

Fix c₀∈C, let H be the subgroup generated by all c−c₀, and let K=H-perpendicular have order d. Two restricted Fourier rows are projectively equivalent exactly when their difference lies in K: their common row ratio can be evaluated at c₀, and equality of every remaining ratio is precisely annihilation of H. Therefore, in the situation just described,

    |R| ≤ 3d,    |C| ≤ p³/d,    d|p³.

## 4. Sharp 3p side theorem

**Theorem 3.** If p≥5 is prime and rank F_(p³)[R,C]≤3, then min(|R|,|C|)≤3p.

**Proof.** Suppose instead that a=|R|>3p and b=|C|>3p. The accepted four-fiber occupancy theorem permits transposing so that C occupies at most four residues modulo p². Since every such fiber has at most p points and b>3p, C occupies exactly four fibers.

Let s be the number of row residues modulo p. If s≥4, choose four rows distinct modulo p and any four columns. The universal prime-power minor lemma, with k=4≤p, gives rank at least four. Thus 1≤s≤3. We treat all three cases.

### Case s=1

All rows have form y+p k. After removing column scalars, the matrix is an order-p² Fourier restriction on A_y, with columns repeated according to their residue modulo p². There are four distinct column fibers and |A_y|=a>3p. Lemma 1 with k=4 gives rank at least four. Contradiction.

### Case s=2

At least three of the four column fibers contain at least two points. Indeed, if at most two did, then

    b ≤ 2p+2 ≤ 3p,

contradicting b>3p. Select three rich fibers as T and apply Lemma 2.

Write the two row-class sizes as a₁,a₂, with a₁+a₂>3p. Either one size exceeds 2p, or both exceed p. To check exhaustion: if neither exceeds 2p and one is at most p, the sum is at most 3p.

- If one class exceeds 2p, Lemma 1 with k=3 gives rank three on that class for T; the other nonempty class has rank at least one. Lemma 2 gives total rank at least 3+1=4.
- If both classes exceed p, choose any two fibers from T. Lemma 1 with k=2 gives rank at least two on each class. Lemma 2 gives total rank at least 2+2=4.

Both possibilities contradict rank at most three. The 2+2 branch is what permits the threshold 3p in place of the earlier 4p argument.

### Case s=3

One of the four column fibers contains at least three points: otherwise b≤8, whereas b>3p≥15. By the consequence of Lemma 2, the rows have at most three projective classes, so

    a≤3d,    b≤p³/d,    d|p³.

Since a>3p, necessarily d>p. The only such divisors of p³ are p² and p³. Hence b≤p, contradicting b>3p.

Every possible s has led to a contradiction. QED.

The proof does not enumerate all four-point residue patterns, and its conclusion does not assert that every four-point pair injective modulo p² has nonzero determinant.

## 5. Sharp rank-three density for every p≥5

Let the rectangle have actual rank three, and transpose so a≤b. By Theorem 3, a≤3p. Stable rank gives ab≤3p³, so

    3/a + 3/b ≥ 3/a + a/p³.

For 0<a≤3p the last expression is at least its value at 3p. This follows directly from

    [3/a+a/p³] − [1/p+3/p²]
      = (3p−a)(1/(pa)−1/p³) ≥ 0,

because a≤3p≤p² for p≥5. Therefore

    3(a+b)/(ab) ≥ (p+3)/p².

This bound is sharp. Take

    R = {p k : 0≤k<p²},
    C = {v+p²w : v∈{0,1,2}, 0≤w<p}.

On R, all columns in any one of the three fibers coincide, so the rank is at most three. Rows 0,p,2p and columns 0,1,2 give a nonsingular three-by-three Fourier minor of order p², so the rank is exactly three. The side sizes are p² and 3p, area 3p³, and density (p+3)/p². Thus the side cutoff 3p itself is also attained.

## 6. Exact optimum and equality at N=2197

Set p=13, N=2197. The minimizing rank-one divisor pair is uniquely {13,169}, so D_N=182 and the rank-one density floor is

    D_N/N = 14/169 = 56/676.

For rank two, the retained proper-divisor formula gives E₂(N)=195 and density floor 15/169=60/676. Theorem 3 and Section 5 give the sharp rank-three density 16/169=64/676.

For rank r≥4, stable rank and AM–GM give density at least 2√(r/N)≥4/√2197. This exceeds 57/676: after squaring positive quantities and simplifying, the comparison is

    16·13 = 208 > (57/4)² = 3249/16.

Thus every tile of rank at least two has density at least

    57/676 = D_N/N + 1/676.

The coefficient 1/676 is convenient and valid; it is not claimed sharp. Summing tile density times tile area, and using disjoint coverage ∑ab=N², gives

    total cost ≥ N D_N + A_(rank≥2)/676
               = 399854 + A_(rank≥2)/676.

For attainment, partition rows into the 169 cosets of the subgroup of order 13, and columns into the 13 cosets of its annihilator of order 169. Their 2197 products are rank-one rectangles, each costing 13+169=182. The total cost is 399854.

Strict positive slack for all higher-rank tiles excludes them from every optimizer. Equality in the retained rank-one density theorem forces every tile to be a full mutually annihilating coset product with unordered sizes {13,169}. Every such tile has area N, so every optimizer has exactly N=2197 tiles. Orientations can vary between tiles; a single common orientation is not claimed.

## 7. Exact controls and remaining boundary

The fresh checker check_sharp_prime_cube.py imports or executes no accepted author or review checker. Exact determinant tests use signed permutation sums of integer monomials reduced modulo Φ_(p^m), in characteristic zero. Separately implemented SymPy polynomial divisions cross-check that evaluator. All finite controls supplement the universal proofs; no sampling is promoted to a theorem.

All controls passed in 2.706 seconds in the recorded run. There were 106,467 exact determinant evaluations (80,031 at prime-square order and 26,436 at prime-cube order), plus 108 independent SymPy polynomial-remainder cross-checks. RESULTS.json and controls.stdout.txt record the completed counts, including:

- All 15,275 column sets of sizes one through four at order 25 against a specified row set just beyond the short-support zero threshold.
- 3,600 prime-square short-support examples over p=5,7,11,13,17,19, with arbitrary higher digits and concentrated as well as random row sets.
- 2,400 examples across both strengthened two-residue branches, with exact four-minor certificates; all 400 target-p=13 certificates are retained in TARGET_MINOR_CERTIFICATES.json.
- Every ordered four-fiber occupancy above 3p and every two-class size split above 3p for those six primes, checking the complete combinatorial case split.
- Genuine rank-three, three-projective-class rectangles at both possible annihilator scales, including exact nonzero three-minors and vanishing four-minors.
- The sharp family density and construction for 166 primes from 5 through 997, all 21,784 target scalar shapes under the new cutoff, all 12 former scalar obstructions, and explicit entry-by-entry coverage of all 4,826,809 entries in the complete 2197-tile partition.
- A fresh accepted-domain census through 10000 and independent direct cyclotomic polynomial-division cross-checks.

The exact accepted-domain union being extended is D_N²<12N, dominant-prime lengths, the isolated accepted length 1331, and the accepted family N=11q² for primes q>11. Adding 2197 leaves first residual 2873=13²·17, with D_N=186 and

    12·2873 = 34476 < 186² = 34596 < 16·2873 = 45968.

Rank two is already excluded there and ranks at least four have strict stable-rank density slack. Rank three is again the next gate. The repeated prime 13 is the smaller prime in 13²·17, so this length lies outside the earlier mixed-prime theorem's p<q hypothesis for N=pq². No result here settles that length or the general nonsquare-composite problem.

## Proposed next-gate wording

Accept, after independent review, the sharp prime-cube rank-three theorem: for every prime p≥5, rank-at-most-three Fourier rectangles in F_(p³) have a side of size at most 3p, and the exact rank-three density minimum is (p+3)/p². The proof combines the accepted four-fiber occupancy theorem with prime-square short-support zeros and direct-sum separation; the critical two-class case includes both 3+1 and 2+2 rank contributions. At N=2197 accept optimum 399854, rank-one-only full-coset equality with exactly 2197 tiles of unordered sizes {13,169}, and the valid higher-rank-area penalty 1/676. The retained-domain union covers all N≤2872; the next residual is 2873=13²·17 at rank three. Preserve all complex/disjoint/no-sharing, preparation/storage/I/O qualifications, parent TO RESEARCH status, and priority 42.
