# Mixed-prime rank-three separation: N = 11q² and the 1859 gate

Date: 18 October 2026 UTC. Owner: M-RECTANGLE-TILING, priority 42.
Status: author-side theorem; independent acceptance pending. No external writes.

## Result

For every prime q>11, the complex cyclic Fourier matrix at N=11q² has exact disjoint-rectangle endpoint-incidence optimum

    N D_N = 132q³,    D_N = 12q.

Every optimizer consists of exactly N rank-one full subgroup-coset × annihilator-coset rectangles, each with unordered side lengths {q,11q}. A valid, not-claimed-sharp quantitative bound is

    cost ≥ 132q³ + A_(rank≥2)/(44q).

In particular, **N=1859=11·13² has optimum 290,004 and higher-rank-area penalty 1/572**. Adding this infinite family to the accepted domains settles every length through 2196. The next residual is 2197=13³, still at rank three.

The new structural theorem, proved below for all distinct primes 5≤p<q, is

    rank(F_(pq²)[R,C])≤3  ⇒  min(a,b)≤4q OR max(a,b)≤B(p,q),
    B(p,q)=max(6p, 3p+2q−2, 3q).

At (p,q)=(11,13), this reads min(a,b)≤52 or max(a,b)≤66. It is a dichotomy, not a claim that every such rectangle has a side of size at most 52.

The proof is complete and does not extrapolate from the exact finite controls. Its main new step separates column spans across two or three residue classes. The short-support bound on F_(pq) used within that argument is an elementary consequence of prime Fourier nonvanishing minors and is also a specialization of Meshulam's established uncertainty inequality.

## 1. Model, retained dependencies, and exclusions

Let F_N[r,c]=ζ_N^(rc), where ζ_N is a primitive N-th root. Changing the sign convention does not alter any assertion. A tiling partitions all N² entries into disjoint nonempty Cartesian rectangles R_t×C_t. A rectangle with side sizes a,b and actual complex rank r costs r(a+b). A_(rank≥2) is the total entry area of tiles of rank at least two.

We retain the accepted rank-one coset/density classification, sharp rank-two density E_2(N)/N, and stable-rank bound ab≤Nr from rectangle_rank_two_20261018_1240 and its independent review rank_two_review_20261018_1248. We retain the accepted prime-power universal-minor lemma from rank_three_prime_cube_20261018_1332 and its review prime_cube_rank_three_review_20261018_1340. Source hashes are recorded in SOURCES.json. The latter theorem had settled N=1331 and the old domain union through 1858; it did not apply directly at mixed-prime length 1859.

All ranks and spans here are over C. No sharing, overlap, or cancellation between tiles is allowed. Root supply and coefficient preparation, storage, and I/O remain separate. The inherited possible N extra additions for literal zero-initialized accumulation are unchanged. There is no conclusion about unrestricted Fourier circuits, arbitrary basis changes, finite-field rigidity, production performance, or worldwide novelty. Parent TO RESEARCH status and priority 42 remain unchanged.

## 2. Two elementary Fourier facts

### 2.1 Prime-power universal minors

If ℓ is prime, k≤ℓ, and k rows are distinct modulo ℓ, then every k-column minor with distinct columns in F_(ℓ^m) is nonsingular. The transposed statement holds.

For completeness, the determinant det[x_j^(e_i)] is the usual Vandermonde times an integer polynomial S. At x_1=…=x_k=1 its quotient is, up to sign,

    S(1,…,1)=∏_(i<j)(e_j−e_i) / ∏_(i<j)(j−i).

This is an integer not divisible by ℓ because every numerator and denominator factor is an ℓ-adic unit. In Z[ζ_(ℓ^m)], reduction modulo (1−ζ_(ℓ^m)) has residue field F_ℓ, so S at the chosen roots is nonzero. Distinct columns give a nonzero Vandermonde factor. This proves the lemma. At m=1 it gives all prime Fourier minors.

### 2.2 A short-support zero bound on F_(pq)

Let p<q be primes and 1≤k≤p. Any nonzero linear combination of at most k distinct characters of Z_(pq) vanishes at at most (k−1)q points. Consequently, if |A|>(k−1)q and T contains k distinct indices modulo pq, then F_(pq)[A,T] has column rank k.

**Proof.** Under the Chinese remainder identification, the characters are α^(ux)β^(vz), where α and β have orders p and q. Absorbing the harmless CRT units into u,v is a permutation of frequencies. Write a nonzero combination with exactly k'≤k terms as

    f(x,z)=∑_(v∈V) β^(vz) g_v(x),
    g_v(x)=∑_(u∈U_v) c_(u,v) α^(ux).

Put t=|V| and k_v=|U_v|, so ∑k_v=k'. Every g_v is nonzero. Prime nonvanishing minors imply that g_v has at most k_v−1 zeros. Let z_0 be the number of x for which all g_v vanish. Then z_0≤min_v(k_v−1)≤k'−t.

At each other x there are at most t active q-characters, so the function of z has at most t−1 zeros. Thus the total number Z of zeros satisfies

    Z≤z_0 q+(p−z_0)(t−1)
      =p(t−1)+(q−t+1)z_0
      ≤p(t−1)+q(k'−t)
      ≤q(k'−1)≤q(k−1).

Here t≤k'≤p<q, so all inequalities have the stated direction. A dependence among the specified k columns would be such a nonzero combination vanishing on A, contradicting |A|>(k−1)q. QED.

This bound is also the d_1=1,d_2=p case of Roy Meshulam, *An uncertainty inequality for finite abelian groups*, European Journal of Combinatorics 27 (2006), 63–67; preprint https://arxiv.org/abs/math/0312407. The primary abstract was freshly checked. The argument above proves precisely the needed special case without importing the general theorem.

## 3. A direct-sum separation lemma

Put N=pq² and let R occupy s distinct residue classes y modulo q, with 1≤s≤q. Partition R as R_y. For a column residue v modulo pq, call its fiber the columns c=v+pq w; each fiber has q possible elements.

Suppose a selected fiber contains at least s columns. Choose s distinct w. On rows in class y, these columns differ from the column at v by the scalar ζ_q^(yw). The s-by-s matrix [ζ_q^(yw)] on the occurring y and selected w is a nonzero prime Fourier minor. Inverting that scalar matrix shows that their column span contains, separately for every y, the vector equal to the column at v on R_y and zero on all other row classes.

Let T be any collection of column fibers each containing at least s columns. Summing these supported subspaces over fibers gives the exact lower bound

    rank F_N[R,C] ≥ ∑_y rank F_(pq)[A_y,T],
    A_y={ (r−y)/q mod pq : r∈R_y }.

Indeed, for r=y+qk, the restriction of the representative column c to R_y is

    ζ_N^(yc) (ζ_N^q)^(kc).

Removing its nonzero column scalar leaves a Fourier column of order pq, and the representatives c modulo pq are distinct. The supported spaces for different y have disjoint coordinates, so their sum is direct. This is a statement about subspaces inside one rectangle. It does not permit sharing or cancellation between tiles in the cost model.

## 4. Complete mixed-prime rank-three theorem

**Theorem.** Let 5≤p<q be distinct primes, N=pq², and B=max(6p,3p+2q−2,3q). If a rectangle has rank at most three, then

    min(a,b)≤4q or max(a,b)≤B.

**Proof.** It suffices to prove that a>4q and b>B are incompatible with rank≤3. We do not initially assume a≤b. Let s=|R mod q| and t=|C mod q|.

First s,t≤3. To see t≤3, suppose C occupies at least four classes modulo q. Since a>4q>3p, four rows lie in one residue class modulo p. Write these rows as r_0+p u_i; the u_i are distinct modulo q². Removing column phases leaves an F_(q²) minor whose selected columns are distinct modulo q. The transposed universal-minor lemma in Section 2.1 makes it nonsingular. This contradicts rank≤3. The argument with rows and columns reversed proves s≤3, because b>B≥6p>3p.

There are three exhaustive possibilities for s.

### Case s=1

All rows are in one residue class y modulo q. After column scaling, the rectangle is F_(pq)[A_y,T] with possibly repeated columns, where T is the set of occurring column classes modulo pq. Since each such fiber contains at most q columns and b>B≥3q, there are at least four distinct elements of T. Also |A_y|=a>4q>3q. Section 2.2 with k=4 gives rank at least four, a contradiction.

### Case s=2

Because t≤3, C occupies at most 3p fibers modulo pq. A fiber is now called rich if it contains at least two columns. If there were at most two rich fibers, the total number of columns would be at most

    2q+(3p−2)=3p+2q−2≤B,

contradicting b>B. Thus there are at least three rich fibers. Select any three as T and apply the direct-sum lemma with s=2.

One of the two row classes has at least a/2>2q elements. By Section 2.2 with k=3, its F_(pq)[A_y,T] rank is three. The other row class is nonempty and its rank is at least one. Their supported subspaces therefore have total dimension at least four. Contradiction.

### Case s=3

Again C occupies at most 3p fibers modulo pq. If every fiber had at most two columns, then b≤6p≤B. Thus one fiber contains three columns. By the separation argument, these columns have rank three, and their span is the entire column space of the rank-at-most-three rectangle.

Within each row class modulo q, the entries in these three columns are a fixed nonzero row phase times a vector depending only on that class. Since all other columns lie in their span, all rows in any one class are projectively equivalent on the entire C. There are therefore at most three projective row classes.

To make the resulting size restriction explicit, fix c_0∈C. Let H be the subgroup generated by c−c_0 for c∈C, and let K=H^perp have order d. Two Fourier rows are projectively equivalent on C exactly when their difference lies in K. Thus

    a≤3d,    b≤N/d,    d|N.

Since a>4q, necessarily d>4q/3>q. The only divisors of pq² exceeding q are pq,q²,pq², so b≤q. This contradicts b>B≥3q. The last case is impossible.

We have proved that a>4q implies b≤B. Transposing proves that b>4q implies a≤B. Equivalently, if min(a,b)>4q then max(a,b)≤B. This is the claimed dichotomy. QED.

The proof remains valid when B<4q; in that situation the second branch cannot occur if both sides exceed 4q. No sharpness of either numerical cutoff is asserted.

## 5. Density and exact tilings for every N=11q², q>11 prime

Now fix p=11 and q≥13 prime. Since the divisors are 1,11,q,11q,q²,11q² and q is the largest divisor below sqrt(N),

    D_N=q+11q=12q.

### Rank three

Transpose so a≤b. Stable rank gives ab≤3N. If a≤4q, then

    3/a+3/b≥3/a+a/N≥3/(4q)+4q/N=49/(44q).

The second inequality holds because 4q<sqrt(3N)=sqrt(33)q and f(a)=3/a+a/N decreases on that interval. An entirely rational check is

    f(a)−f(4q)=(4q−a)(3/(4qa)−1/N)≥0.

In the other branch of the theorem, a,b≤B=max(66,31+2q,3q), so the density is at least 6/B. For every q≥13,

    49·66≤264q,
    49(31+2q)≤264q,
    49·3q≤264q.

The first two inequalities hold at q=13 and only improve thereafter. Thus 49B≤264q and 6/B≥49/(44q). Every rank-three tile consequently has density at least

    49/(44q) = D_N/N + 1/(44q).

### Other ranks and equality

The accepted rank-two theorem gives density E_2(N)/N. Here E_2(N)=13q: the proper divisor q attains 2q+11q, while the other divisor values are larger for q≥13. Hence rank-two density is 13/(11q)>49/(44q).

For rank r≥4, stable rank and AM-GM give density at least 4/sqrt(N)=4/(sqrt(11)q)>49/(44q). Squaring the positive constants verifies the last strict inequality: 16·1936=30976>26411=11·2401.

Rank-one density is at least D_N/N, with equality precisely at full mutually annihilating subgroup-coset products of sizes {q,11q}. Summing the tilewise bounds using disjoint coverage ∑ab=N² gives

    cost≥ND_N+A_(rank≥2)/(44q)=132q³+A_(rank≥2)/(44q).

Partition rows into cosets of the subgroup of order q and columns into cosets of its annihilator, of order 11q. Their N Cartesian products are rank one and attain ND_N. Strict higher-rank slack forces every optimal tile to be rank one. Rank-one equality forces each product to be full and of the stated sizes. Each has area N, so every optimizer has exactly N tiles. Tile orientations may vary; no common orientation is asserted.

At q=13 this gives N=1859, D_N=156, optimum 290004, rank-three floor 49/572, baseline 48/572, and penalty 1/572. The relaxed scalar side bound does not assert an attainable rank-three rectangle at its continuous endpoint.

## 6. Exact limitation of the direct prime-cube analogy

The accepted prime-cube residue-occupancy theorem cannot simply replace p³ by pq² and count classes modulo pq. In F_(pq²), take

    R={j q²:0≤j<p},    C={j p:0≤j<q²}.

Every row-column product is divisible by N, so this is a rank-one rectangle. Nevertheless R occupies p distinct classes modulo pq and C occupies q distinct classes modulo pq. At (p,q)=(11,13), both occupancies exceed four. This exactly disproves that proposed mixed-prime occupancy extension.

It does not disprove the present size dichotomy: the smaller side is p=11. Our proof explicitly handles the alternative prime factor and does not assume a one-prime residue hierarchy.

## 7. Exact controls and the next residual

The fresh checker check_mixed_prime.py imports no previous checker. It uses integer signed permutation sums and exact cyclotomic reduction for every determinant certificate; it does not substitute floating-point or finite-field ranks for complex rank. Finite controls supplement the complete proof above. RESULTS.json and controls.stdout.txt contain the completed counts.

The controls cover prime-square universal minors, short-support rank bounds including structured near-boundary sets, exact four-minor extraction in the two-residue direct-sum case, genuine rank-three examples, the invalid mixed occupancy extension, all target scalar shapes in both dichotomy branches, the full target coset tiling, and a fresh accepted-domain census through 10000. Separately, SymPy polynomial division cross-checks the mixed cyclotomic determinant evaluator.

Completed controls (all passed):

- 7,200 exact prime-square universal minors across q=5,7,11,13,17,19.
- Every two-, three-, and four-column set in F_35 against the fixed near-boundary row sets of sizes 8,15,22: 595,6,545,52,360 cases, respectively, totaling 59,500.
- 3,600 additional exact semiprime short-support rank controls, including arbitrary and structured boundary row sets, across six prime pairs.
- 1,800 explicit four-minor certificates for the two-residue direct-sum step; 2,400 vanishing four-minors in six independently certified genuine rank-three coset rectangles.
- 1,504 exact target four-minor certificates: every one of the 94 formerly obstructive scalar shapes, with every pair of row/column residue-occupancy counts in {1,2,3,4}. All five selection branches are exercised. The selected four rows and columns are retained in TARGET_MINOR_CERTIFICATES.json. These structured samples are certificates for those chosen rectangles, not an exhaustive enumeration of all rectangles of each shape.
- The complete 1,859-tile target partition, covering all 3,455,881 entries exactly once at cost 290,004.
- Exact integer/rational density and divisor controls, the full census through 10,000, and 36 separate SymPy polynomial-remainder cross-checks.
- In total, 262,502 mixed-prime and 7,200 prime-power exact determinant evaluations; the checker completed in 6.642 seconds in this run.

The new family removes the five former residuals 1859,3179,3971,5819,9251 through 10000. The remaining first residual is 2197=13³, with D=182 and 12N<D²<16N. The earlier prime-cube side bound 4p=52 does not close that case: at its continuous endpoint 3/52+52/2197=55/676 is below D/N=56/676. An exact integer scalar example is a=52,b=126, with ab=6552≤6591 and density 89/1092<14/169=D/N. This is a limitation of the currently proved scalar bounds, not an actual rank-three Fourier rectangle or counterexample.

## Proposed next-gate wording

Accept, after independent review, the mixed-prime rank-three dichotomy for N=pq² with distinct primes 5≤p<q: a rank-at-most-three rectangle has min(a,b)≤4q or max(a,b)≤max(6p,3p+2q−2,3q). Its proof uses prime-square minor restrictions, a short-support rank bound at order pq, and direct-sum separation across residue classes. Consequently every N=11q², q>11 prime, has exact disjoint-tile optimum 132q³, rank-one-only full-coset equality, exactly N tiles, and valid higher-rank-area penalty 1/(44q). At N=1859 accept optimum 290004 and penalty 1/572. The accepted-domain union then covers every N≤2196; 2197 is the next residual at rank three. Preserve all complex/disjoint/no-sharing, preparation/storage/I/O qualifications, parent TO RESEARCH status, and priority 42.
