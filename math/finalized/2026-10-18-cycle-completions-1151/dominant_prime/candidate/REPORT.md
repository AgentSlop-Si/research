# Exact Fourier rectangle tilings with a dominant prime factor

Date: 18 October 2026. Owner: M-RECTANGLE-TILING, priority 42.
Status: author-side theorem; independent acceptance pending. No external writes.

## Result

Let `F_N[k,j] = omega^(-kj)` be the complex cyclic Fourier matrix, where omega has exact order N. Partition all its entries into disjoint nonempty Cartesian rectangles `R_t × C_t`. Write `a_t=|R_t|`, `b_t=|C_t|`, and let `r_t` be the actual matrix rank over the complex numbers. Charge precisely

`C = sum_t r_t(a_t+b_t)`.

**Theorem.** Suppose `N=mp`, where p is prime and `1 <= m < p`. Then `D_N = min_{d|N}(d+N/d) = m+p`, and

`min C = N(m+p) = N D_N`.

Every optimizer consists entirely of rank-one tiles. Each tile is the full product of a subgroup coset and an annihilator coset, with unordered side lengths `{m,p}`. Every optimizing tiling has exactly N tiles, each of area N. This is a tilewise classification; it does not impose one global orientation on all tiles.

In particular, the higher-rank problem is now solved for **every N=3p with p an odd prime**. The case p=3 is the previously accepted square case; every p>3 follows from the theorem. More broadly, the new theorem covers every length with a prime factor larger than its cofactor, including all nonsquare semiprimes, and arbitrarily large composite cofactors m.

The requested residual example is settled:

`N=57=3*19: min C = 57*(3+19) = 1254`.

The complete-family proof uses Fourier-specific prime-minor information, not the previously insufficient stable-rank relaxation. There is no actual Fourier counterexample to the conjectured optimum here.

## 1. Dependencies and scope

The starting point is the accepted bounded theorem in `next_open_theorem_20261018_1043/REPORT.md` and its independent acceptance in `rectangle_review_20261018_1053/REVIEW.md`. They settle `D_N^2<8N` and, separately, N=2p. Their pinned Phase7 source supplies the original objective, rank-one coset classification, and complex stable-rank inequality. This report advances the remaining family rather than recounting those accepted scopes as new.

The sole external mathematical ingredient is the characteristic-zero prime Fourier nonvanishing-minors theorem: Garcia, Karaali and Katz, *An improved uncertainty principle for functions with symmetry*, Section 1.1, Theorem 1.1, https://arxiv.org/html/1807.07648v4. The statement and Fourier normalization were freshly read for this report. Multiplying the entire matrix by a nonzero scalar and choosing a different primitive p-th root do not change the full-spark conclusion.

All ranks and norm arguments below are over C. There is no finite-field full-spark or singular-value claim. The model retains disjoint/no-sharing rectangles and the original rank-factor endpoint-incidence objective. It excludes overlapping/cancelling summands, shared intermediate computations, arbitrary invertible basis changes, and general Fourier arithmetic-circuit conclusions. Root supply, coefficient preparation, storage, and I/O remain separate. The inherited qualification that literal zero-initialized accumulation can add N otherwise uncounted additions is unchanged.

## 2. Fourier-specific prime-fiber rank lemma

**Lemma.** Let p be any prime divisor of N, put `m=N/p`, and let a Fourier rectangle have nonempty sides of sizes `a <= b` and actual rank r. Then

`r >= ceil(a/m)`.

This lemma itself does not require `m<p` or `gcd(m,p)=1`.

**Proof.** Among the m row residue classes modulo m, select a class containing at least `ceil(a/m)` rows. Write those rows as `k_0 + m u`, with distinct u modulo p.

Among the selected b columns, at least `ceil(b/m)` distinct residue classes modulo p occur, since each such class contains only m indices in Z_N. Choose one column representative from each occurring class. On these rows and columns, the matrix entries are

`omega^(-(k_0+m u)j) = omega^(-k_0 j) * (omega^m)^(-u j)`.

The first factor is a nonzero column scaling. The second is a submatrix of the prime-order Fourier matrix, with distinct row indices u and distinct column indices `j mod p`, and `omega^m` has exact order p. Chebotarev's nonvanishing-minors theorem gives full rank equal to the smaller selected side size. Since b>=a, both selected side sizes are at least `ceil(a/m)`. The rank of the whole rectangle is at least that of this submatrix. QED.

This is stronger in scope than restricting both sides to the same kind of residue classes: it remains valid when p divides m. The main optimum theorem uses it only in the dominant-prime range m<p.

## 3. A local density inequality with strict higher-rank gap

For any nonempty Fourier rectangle, the accepted stable-rank bound gives

`ab <= Nr`.

Indeed, every entry has modulus one, the Frobenius norm squared is ab, and every singular value is at most sqrt(N), because the full Fourier matrix satisfies `F_N^*F_N=N I`.

Set `rho = r(a+b)/(ab)` and transpose the rectangle if necessary so that `a<=b`. The prime-fiber lemma gives `a<=mr`. Stable rank implies

`rho = r/a+r/b >= r/a+a/(mp)`.

There are two exhaustive cases.

### Case I: mr <= p

Because `a<=mr<=p`, the exact identity

`[r/a+a/(mp)] - [1/m+r/p] = (mr-a)(p-a)/(m a p)`

is nonnegative. Hence

`rho >= 1/m+r/p >= 1/m+1/p`.

For r>=2 its excess above the target is at least `1/p`.

### Case II: mr >= p

AM-GM and stable rank give

`rho >= 2r/sqrt(ab) >= 2sqrt(r/(mp)) >= 2/m`.

Since m<p,

`2/m > 1/m+1/p`.

At the common boundary mr=p either case is valid. Thus every rank-at-least-two rectangle has **strictly** larger density than `(m+p)/(mp)`.

More quantitatively, with

`delta = min(1/p, (p-m)/(mp)) > 0`,

every rank-at-least-two tile satisfies

`r(a+b) >= [(m+p)/(mp) + delta] ab`.

Every rank-one tile satisfies the same inequality without delta. In fact the local argument already proves this, without needing to import the rank-one lower bound separately.

## 4. Exact global optimum and complete equality conditions

First, m is the largest divisor of N not exceeding sqrt(N). Since `m < sqrt(mp) < p`, any divisor d at most sqrt(N) cannot contain the prime p, and therefore divides m. Thus d<=m. The minimizing divisor pair is uniquely `(m,p)` up to interchange, and `D_N=m+p`.

Disjoint coverage gives `sum_t a_t b_t=N^2`. Summing the local density bounds proves

`C >= N(m+p) + delta A_{>=2}`,

where `A_{>=2}` is the total area of higher-rank tiles. In particular every optimizer at the lower endpoint has only rank-one tiles.

For r=1, necessarily Case I applies, because m<p. Equality in its identity forces `a=m`: the alternative `a=p` is impossible with `a<=m<p`. Equality in the use of stable rank then forces `b=p`. Thus equality requires r=1 and unordered side lengths `{m,p}`.

For completeness, rank one gives the full set structure, not merely these cardinalities. Choose `k_0 in R`, `j_0 in C`. Every 2-by-2 minor vanishes exactly when

`N divides (k-k_0)(j-j_0)` for every k in R and j in C.

Let H be generated by the row differences. Then `R subset k_0+H` and `C subset j_0+H^perp`. Their ambient coset sizes multiply to N. Since the actual side sizes also multiply to N, both inclusions are equalities. This is the claimed full-coset classification.

For attainment, use row classes

`R_u = {u+p k: 0<=k<m}`, for `0<=u<p`,

and column classes

`C_v = {v+m ell: 0<=ell<p}`, for `0<=v<m`.

Their N Cartesian products partition the full matrix. Their row/column difference products are multiples of N, so they have rank one. Every tile costs m+p, giving `C=N(m+p)`. Each equality tile has area N, so exactly N tiles are necessary in every optimizer. QED.

## 5. Quantitative consequences and actual Fourier controls at N=57

If a tiling costs at most `N(m+p)+E`, then

`A_{>=2} <= E/delta`.

When `p>=2m`, delta simplifies to `1/p`. In particular, for `N=3p`, p>=7,

`C >= 3p(p+3) + A_{>=2}/p`.

At N=57 this is `C>=1254+A_{>=2}/19`.

The local coefficient `1/p` is sharp in the regime `p>=2m`. Take two distinct complete row cosets of the subgroup of order m and the full annihilator column subgroup of size p. This gives a `2m × p` rectangle of rank 2: after removing repeated rows, its two distinct rows are independent prime-Fourier rows. Its density is exactly `1/m+2/p`, whose excess is `1/p`. More generally, for `mr<=p`, taking r such row cosets gives a `mr × p` rectangle of rank r and attains the Case I density `1/m+r/p`.

The old relaxed tuple `(N,a,b,r)=(57,10,11,2)` is decisively excluded as an actual Fourier rectangle by the new lemma: every 10-by-11 rectangle has rank at least `ceil(10/3)=4`.

The lower rank 4 is attainable for these side sizes. Use

`R = {0,3,6,9,12,15,18,21,24,27}`,

`C = {0,19,38,1,20,39,2,21,40,3,22}`.

The ten rows lie in one residue class modulo 3; the eleven columns occupy exactly four classes modulo 19. Removing repeated columns leaves a 10-by-4 prime Fourier submatrix. Its exact complex rank is 4. Its objective density is strictly above the optimum density. This is an actual Fourier rank example, **not** a competing tiling or a counterexample to the theorem.

An additional sharp-gap control uses

`R = {0,19,38,1,20,39}` and `C={0,3,6,...,54}`.

This 6-by-19 rectangle has exact rank 2, area 114, cost 50, and target-baseline cost 44, so its excess density is exactly `1/19`.

## 6. What remains open

This result strictly extends the accepted domains but does not settle all nonsquare composite N. For example, `N=343=7^3` has closest divisor pair `(7,49)`, with `D_N=56` and `D_N^2=3136>2744=8N`. Its largest prime factor 7 is smaller than its cofactor 49, so the present theorem does not apply. The accepted universal sandwich remains

`686 sqrt(686) <= min C <= 19208`.

Likewise N=847=7*11^2 has closest divisor pair `(11,77)` and is outside both domains. An exact finite census through N=1000 finds 238 lengths newly covered beyond the prior accepted domains; 343 and 847 are the only remaining lengths in that finite interval. This census is a domain illustration, not an infinite-family proof or a status change.

The parent owner remains TO RESEARCH at priority 42. No score, novelty, archival, publication, or census-record change is made here. No worldwide novelty conclusion is claimed for the mathematical argument.

## 7. Fresh checks and source records

`check_dominant_prime.py` is newly written for this extension. It does not import or execute the previous source or review checkers. It tests scalar shapes with exact integers, actual Fourier ranks with exact cyclotomic arithmetic, explicit coset partitions, the formerly obstructive N=57 shape, sharpness examples, and the domain boundary. These controls supplement the all-length proof; finite enumeration does not replace it.

All checks completed successfully:

- 7,455,712 feasible scalar shapes over all 279 dominant-prime lengths through N=400; 7,399,663 higher-rank shapes satisfy the quantitative strict gap. The only scalar equality shape at each length is `(a,b,r)=(m,p,1)`.
- 4,988 exact characteristic-zero Fourier rectangles exhaustively checked at N=2,3,5,6.
- 56 additional exact characteristic-zero rectangles, including N=57 and 116, the attaining 10-by-11 rank-4 example, full-coset equality cases, sharp rank-2 gaps, and prime-fiber controls at N=9,27,49 where p divides m.
- 137 full coset partitions through N=200, with 13,829 tiles covering 1,832,293 entries, checked for exact coverage, rank-one plaquettes, and objective.
- The separate finite-field negative control at N=11 has rank 2 over F_23 and rank 3 over Q(zeta_11), confirming that characteristic-zero full spark must not be replaced by a finite-field assertion.
- The exact finite domain census through N=1000 confirms 238 additional lengths and residual set `{343,847}`.

`RESULTS.json` records completed counts and exact examples. `SOURCES.json` records source hashes and the primary theorem citation. `MANIFEST.json` records final artifact hashes after the checks complete.

## Proposed accepted next-gate wording

The higher-rank disjoint-tile optimum N D_N, with rank-one-only full-coset equality, is proved whenever N=mp with p prime and 1<=m<p, in addition to the previously accepted balanced-divisor domain D_N^2<8N. This settles every N=3p and every semiprime length, including the former N=57 obstruction at exact optimum 1254. The proof combines the new prime-fiber rank bound r>=ceil(min(a,b)/m) with the complex stable-rank bound. A quantitative higher-rank-area penalty is available, and the N=57 10-by-11 rank lower bound is 4, attained by an explicit Fourier submatrix. General nonsquare composites outside the union remain open, starting with 343 and 847 through N=1000. Preserve the original disjoint/no-sharing cost model, characteristic-zero prime-minor dependency, field and preparation/storage/I/O qualifications, and parent TO RESEARCH status.
