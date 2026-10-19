# Rank-two rigidity and the next Fourier rectangle-tiling domain

Date: 18 October 2026 UTC. Owner: M-RECTANGLE-TILING, priority 42.
Status: author-side extension; independent acceptance pending. No external writes.

## Result

For `N>=2` and the complex cyclic Fourier matrix `F_N[k,j]=omega^(-kj)`, partition all entries into disjoint nonempty Cartesian rectangles. A tile with side sizes a,b and actual complex rank r costs exactly `r(a+b)`. Put

`D_N = min_{d|N}(d+N/d)`.

**Theorem.** If `D_N^2 < 12N`, then the minimum total cost is exactly `N D_N`. Every optimal tile has rank one and is the full product of a subgroup coset and an annihilator coset, with side sizes attaining `D_N`. Every optimal tiling has exactly N tiles, each of area N.

This strictly extends the prior `D_N^2<8N` domain. Together with the accepted dominant-prime theorem, it settles every length `2<=N<=1000`, including the two previously uncovered cases:

- `N=343=7^3`: `D_N=7+49=56`, optimum **19,208**.
- `N=847=7*11^2`: `D_N=11+77=88`, optimum **74,536**.

There is also a structural result with no restriction on N: **a rank-two tile can never occur in an optimal disjoint tiling of any complex matrix whose entries all have modulus one**. It admits a strictly cheaper refinement into two rank-one rectangles.

The new argument is self-contained. It does not require a prime Fourier-minor theorem, a numerical-rank heuristic, or an exhaustive search over large tilings.

## 1. Scope and dependencies

The accepted starting points are the bounded-divisor result in `next_open_theorem_20261018_1043/REPORT.md`, its review in `rectangle_review_20261018_1053/REVIEW.md`, and the dominant-prime extension in `rectangle_triprime_20261018_1140/REPORT.md`, accepted in `dominant_prime_review_20261018_1143/REVIEW.md`.

The result here is over the complex numbers. The modulus-one geometry used below does not transfer to arbitrary finite fields. The cost and admissible objects remain precisely disjoint/no-sharing Cartesian tiles with rank-factor endpoint cost `sum r(a+b)`. Overlap with cancellation, shared intermediates, arbitrary basis changes, and general Fourier arithmetic circuits are outside the claim. Root supply, coefficient preparation, storage, and I/O remain separate. The inherited qualification about literal zero-initialized accumulation possibly adding N otherwise uncounted additions is unchanged.

This advances the existing owner; it does not create a new owner, alter its priority, establish worldwide novelty, or change the parent TO RESEARCH status.

## 2. Unit-modulus rank-two rigidity

Call two nonzero rows (or columns) *projectively equivalent* if one is a nonzero scalar multiple of the other.

**Lemma 1.** A complex rank-two matrix all of whose entries have modulus one has at most two projective row classes or at most two projective column classes.

**Proof.** Scale each column by the conjugate of its entry in the first row. This preserves ranks, unit moduli, and projective row/column equivalence, and makes the first row the all-ones vector. Choose another row z independent of it; all its coordinates lie on the unit circle, and it has at least two distinct coordinate values. Every remaining row has the form

`x_j = alpha + beta z_j`.

If z has only two distinct coordinate values, the entire normalized matrix has only two distinct columns: each column is determined by its value of z_j. Thus there are at most two projective column classes.

Otherwise z has at least three distinct coordinate values. The condition `|x_j|=1` gives

`|alpha|^2 + |beta|^2 + 2 Re(conj(alpha) beta z_j) = 1`.

If `conj(alpha) beta != 0`, this fixes a real affine line on which every z_j lies. A line meets the unit circle in at most two points, contradicting the three distinct values. Thus alpha or beta is zero. Every row is proportional to either the all-ones row or z, giving at most two projective row classes. QED.

This proof also covers two-row and two-column matrices. Since the rank is exactly two, the side identified by the lemma has exactly two, rather than one, projective classes.

**Corollary 2 (universal strict refinement).** A rank-two a-by-b tile with unit-modulus entries admits a disjoint rank-one refinement of strictly smaller endpoint cost.

If its rows have two projective classes of sizes a_1,a_2, split the row set accordingly and keep the whole column set. The new cost is

`(a_1+b)+(a_2+b)=a+2b < 2a+2b`.

The saving is exactly a. If instead its columns have two projective classes, splitting those columns costs `2a+b`, saving exactly b. Both refinements partition precisely the original tile and introduce no sharing or overlap. Thus no optimal disjoint tiling of a unit-modulus complex matrix contains a rank-two tile. QED.

This is stronger than an assertion limited to the two target lengths: it removes rank two from every unresolved complex Fourier length as well.

## 3. Exact divisor-sensitive rank-two density

For `N>=2`, define

`E_2(N) = min_{d|N, d<N} (2d+N/d)`.

**Theorem 3.** Among all actual rank-two rectangles in the complex Fourier matrix, the minimum endpoint-cost density is exactly

`min 2(a+b)/(ab) = E_2(N)/N`.

In particular `E_2(N)>D_N`, so every rank-two tile has strictly greater density than the rank-one optimum density, at every N.

**Proof of the lower bound.** First suppose the rectangle has two projective row classes. Fix `c_0 in C`. Let H be the subgroup of Z_N generated by all column differences `c-c_0`, and let `K=H^perp` be its annihilator. Write `|K|=d`, so `|H|=N/d` and `d|N`.

Two selected Fourier rows k,k' are projectively equivalent on C exactly when

`omega^(-(k-k')(c-c_0))=1 for every c in C`,

or equivalently `k-k' in K`. The selected row set is therefore contained in two K-cosets, and the selected column set is contained in the single coset `c_0+H`. Consequently

`a<=2d`, `b<=N/d`.

Because the tile has rank two, H is nontrivial and d<N. Hence

`2(a+b)/(ab) = 2/a+2/b >= 1/d+2d/N >= E_2(N)/N`.

If the two-class side consists of columns instead, transpose the rectangle and apply the same proof. Lemma 1 guarantees that one case applies.

**Attainment.** For any proper divisor d of N, let

`K={tN/d : 0<=t<d}`, `H={sd : 0<=s<N/d}`,

and take `R=K union (1+K)`, `C=H`. The two K-cosets are distinct. Within each row coset all Fourier rows agree on H; the two resulting rows are independent, as their restrictions to columns 0,d have determinant `omega^(-d)-1 != 0`. Thus this rectangle has actual complex rank two, side sizes `2d,N/d`, area `2N`, and density `(2d+N/d)/N`. Taking a minimizing divisor proves sharpness.

Finally, for every proper divisor d,

`2d+N/d = (d+N/d)+d >= D_N+d > D_N`.

Since the divisor set is finite, `E_2(N)>D_N`. QED.

Equality in the density theorem forces, up to transposition, two full cosets of a subgroup K of order d and one full coset of its annihilator, for a divisor d minimizing E_2. Conversely every such pair of distinct full row cosets and full annihilator column coset attains the corresponding density.

## 4. Global optimum when D_N^2<12N

For every Fourier rectangle of size a-by-b and rank r, complex stable rank gives

`ab <= Nr`.

Indeed its squared Frobenius norm is ab, while each singular value is at most sqrt(N), because the full unnormalized Fourier matrix satisfies `F_N^* F_N=N I` and coordinate restriction is contractive.

There are three rank cases.

1. **Rank one.** Fix a row and column. Vanishing 2-by-2 minors imply `N | (k-k_0)(j-j_0)` for all selected indices. If the row differences generate a subgroup K of order d, then `R subset k_0+K` and `C subset j_0+K^perp`; hence `a<=d`, `b<=N/d`. It follows that
   `1/a+1/b >= 1/d+d/N >= D_N/N`.
   Equality holds precisely when both cosets are full and `d+N/d=D_N`.
2. **Rank two.** Theorem 3 gives density at least `E_2(N)/N>D_N/N`.
3. **Rank at least three.** AM-GM and stable rank give
   `r(a+b)/(ab) >= 2r/sqrt(ab) >= 2sqrt(r/N) >= sqrt(12N)/N`.
   This is strictly greater than `D_N/N` if `D_N^2<12N`.

Disjoint coverage gives `sum ab=N^2`, so summing proves `C>=N D_N`. For any minimizing divisor d, partition rows into cosets of the order-d subgroup and columns into cosets of its annihilator. The resulting N rank-one rectangles each cost `d+N/d=D_N`, attaining the bound.

Strictness for ranks two and above forces every optimal tile to have rank one. Equality in the rank-one bound forces full mutually annihilating cosets and a minimizing divisor pair. Each such tile has area N, so every optimal tiling has exactly N tiles. Tile orientations may vary; no common orientation is asserted. QED.

## 5. Universal lower bound and higher-rank-area penalty

The same three rank cases give, for **all** N>=2,

`N min(D_N,sqrt(12N)) <= min C <= N D_N`.

This sharpens the previous universal stable-rank threshold from 8N to 12N; the dominant-prime theorem can give more when this sandwich does not close.

Within `D_N^2<12N`, put

`delta_N = min(E_2(N)-D_N, sqrt(12N)-D_N)/N > 0`.

If `A_{>=2}` denotes total area in tiles of rank at least two, then

`C >= N D_N + delta_N A_{>=2}`.

Thus a tiling within E of the optimum has `A_{>=2}<=E/delta_N`. This bound concerns tile area in the stipulated model, not a general-circuit lower bound.

## 6. The two previously uncovered lengths

### N=343

The divisors are `1,7,49,343`. The nearest pair is `(7,49)`, so `D=56` and `D^2=3136<4116=12N`. The proper-divisor values of `2d+N/d` are `345,63,105`, so `E_2=63`. Since `63^2=3969<4116`, the rank-two branch determines the quantitative penalty:

`C >= 19,208 + A_{>=2}/49`.

The penalty is locally sharp: `R=K union (1+K)` for `K={0,49,...,294}`, and `C={0,7,...,336}` is a 14-by-49 rank-two tile with area 686 and cost 126. Its baseline at density `56/343` is 112, leaving excess 14 and density gap `1/49`. Merging the corresponding two tiles of an optimal coset partition gives a complete disjoint tiling of cost 19,222 with higher-rank area 686, so the penalty is globally sharp as well.

The scalar stable-rank relaxation formerly permits a 26-by-26 rank-two rectangle: `676<=686` and its putative density is below `56/343`. It cannot be an actual Fourier rank-two rectangle. Theorem 3's containment would require a divisor d with `26<=2d` and `26<=343/d`, i.e. `13<=d<=343/26`, and no divisor satisfies this. Thus every actual 26-by-26 Fourier rectangle has rank at least three. No claim of an attainable rank-three example is made.

### N=847

The divisors are `1,7,11,77,121,847`. The nearest pair is `(11,77)`, so `D=88` and `D^2=7744<10164=12N`. Proper-divisor values of `2d+N/d` are `849,135,99,165,249`; hence `E_2=99`. As `99^2=9801<10164`,

`C >= 74,536 + A_{>=2}/77`.

A sharp rank-two control has `K={0,77,...,770}`, `R=K union (1+K)`, `C={0,11,...,836}`. Its shape is 22-by-77, area 1694, and cost 198; its baseline is 176, giving excess 22 and density gap `1/77`. Merging the corresponding two optimum tiles yields a complete tiling of cost 74,558 with higher-rank area 1694, attaining the quantitative penalty exactly.

Likewise the relaxed 41-by-41 rank-two shape has area 1681<=1694 but cannot occur: the containment would require `41/2<=d<=847/41`, containing no divisor of 847. Every actual rectangle of this square shape has rank at least three.

## 7. Remaining domain and next structural gate

Combining the new balanced-divisor theorem with the accepted dominant-prime domain covers all lengths from 2 through 1000. The first uncovered length is now

`N=1331=11^3`, `D_N=11+121=132`, `D_N^2=17424>15972=12N`.

For it the universal bounds supplied here are

`1331 sqrt(15972) <= min C <= 175,692`.

At N=1331, rank two is nevertheless completely excluded from optimal tilings by Corollary 2. The first unresolved obstruction has rank three. Rank at least four already has strictly larger local density than D_N/N because `16N=21296>D_N^2`. A rank-three structural/refinement theorem, or a Fourier-specific rank-three density bound, is a concrete next gate.

The rank-two circle proof does not automatically extend to rank three. In fact the naive generalization is false for arbitrary unit-modulus matrices: the matrix

`[[1,-1,i,-i],[-i,1,-1,i],[i,-i,1,-1],[-1,i,-i,1]]`

has four projective row classes and four projective column classes, but rank three. Every row sums to zero, and its upper-left 3-by-3 minor is `2-2i`, so its rank is exactly three. This is a limit on a general unit-modulus rigidity analogy, **not** a Fourier rectangle counterexample and not a failure of a possible rank-three cost-refinement theorem. No rank-three extension is asserted here.

## 8. Verification and source record

`check_rank_two.py` is a fresh checker. It does not import or execute the previous author or reviewer scripts. Its finite tests supplement the complete proofs above and do not establish them by enumeration.

The checker records:

- Exact characteristic-zero ranks of exhaustive small Fourier rectangles, checking the projective two-class conclusion and strict refinement whenever rank is two.
- Exhaustive normalized small root-of-unity matrices, independently exercising the geometric lemma beyond Fourier matrices.
- Exact integer divisor-containment and stable-rank shape inequalities, together with exact census of old and new domains.
- Exact group-theoretic rank certificates for the large target rank-two examples, without using floating-point numerical rank.
- Explicit disjoint rank-one partitions and full entry coverage at both target lengths.
- A finite-field negative control showing why the complex modulus hypothesis matters.

All checks completed successfully:

- 21,342 exact Fourier rectangles at every length from 2 through 7.
- 5,706 normalized non-Fourier root-of-unity matrices.
- 910,468 rank-two divisor-envelope shapes through N=400.
- 11,781,870 rank-at-least-three scalar shapes over 300 eligible lengths through N=500.
- 1,190 target-optimal tiles covering 835,058 entries exactly once at N=343 and N=847, plus exact globally sharp higher-rank-penalty constructions.
- Exact finite-field and naive-rank-three negative controls.
- Through N=1000: exactly the two requested lengths are newly covered, with no remaining residual. Through N=10000: 44 lengths are newly covered and 25 remain outside the combined domains, beginning at 1331.

Completed counts and examples are in `RESULTS.json`; source identities and hashes are in `SOURCES.json`; final artifact hashes are in `MANIFEST.json`. No publication or repository write was performed.

## Proposed next-gate wording

The higher-rank complex disjoint-tile optimum N D_N, with rank-one-only full-coset equality, is now proved whenever D_N^2<12N, in addition to the accepted dominant-prime domain. The new self-contained rank-two unit-modulus lemma permits a strictly cheaper two-piece rank-one refinement at every N and yields the sharp local density E_2(N)/N, where E_2(N)=min_{d|N,d<N}(2d+N/d)>D_N. The union settles every length through 1000, including N=343 at 19,208 and N=847 at 74,536, with respective higher-rank-area penalties 1/49 and 1/77. The next uncovered length is 1331; rank-three structure is the new obstruction there. Preserve complex/disjoint/no-sharing qualifications, preparation/storage/I/O exclusions, priority 42, and parent TO RESEARCH status.
