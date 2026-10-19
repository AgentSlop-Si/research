# Independent review: two-prime rank-three separation and N = 2873

Date: 19 October 2026 UTC. Candidate: `repeated_small_rank_three_20261019_1200`.

## Verdict

**ACCEPT the frozen report, including its explicit arithmetic-only closure correction. No further correction is needed.** Final source-byte identification is recorded in `SOURCES.json` and `SOURCE_VERIFICATION.json`.

Frozen candidate `REPORT.md` SHA-256:

    ef02706ac4265a67e5ff56f7f4d7bcfe41c987caf17e3cb0885f896d84bff1d5

All six manifested candidate artifacts and all eight pinned accepted dependencies were hash-verified after the completed independent controls and final proof read. This is a local source-binding check, not a fresh repository fetch.

For distinct primes p,q≥5, every rectangle of the complex cyclic Fourier matrix F_(p²q) having rank at most three satisfies

    min(|R|,|C|) ≤ max(6p,3q).

This is valid with either ordering of p and q. It does not rely on reversing the hypotheses of the older pq² theorem. The explicit four-minor certificate supplies the previously missing argument when the repeated prime is the smaller prime.

At N=2873=13²·17, the resulting side cutoff is 78 and the actual-rank-three density is at least 29/442, strictly above 186/2873 by 5/5746. The exact disjoint endpoint-incidence tiling optimum is **534378**. Every optimizer has exactly **2873 rank-one full mutually annihilating coset-product tiles**, with unordered side sizes **{17,169}**. The quantitative bound

    cost ≥ 534378 + (5/5746) A_(rank≥2)

is valid. Neither the side cutoff, the rank-three density floor, nor this penalty coefficient is asserted to be sharp.

The independently recomputed retained-domain census, extended only by the isolated target 2873, covers every N from 2 through 3756. Its next residual is **3757=13·17²**, at rank three. The general all-length problem remains open; owner status and priority are unchanged.

**Correction to the historical gate framing:** integer stable rank alone already settles the 2873 target. Its exact unrestricted rank-three scalar minimum is 62/957, uniquely at the unordered scalar shape {87,99}, which is strictly above 186/2873. The new structural theorem is independently valid and yields the substantially stronger 5/5746 area penalty, but it is not necessary just to prove the target optimum. The earlier dated description of 2873 as a residual of the retained domain union is preserved; treating that residual as requiring new rank-three structure was too strong and is corrected here.

## 1. Scope, dependencies, and independent approach

The objective is Σ r_t(a_t+b_t) over nonempty Cartesian rectangles that partition the N² entries, where each r_t is the actual complex rank. Row and column subsets are arbitrary. The proof does not permit overlaps, cancellation, or sharing between tiles.

The accepted rank-two report and review supply the rank-one equality theorem, the sharp rank-two density E₂(N)/N, and stable rank ab≤Nr. The mixed-prime report and acceptance contain the correct universal prime-power minor lemma and the short-support theorem at semiprime order. The sharp prime-cube report and review supply the previously accepted target 2197 and coverage through 2872. The dominant-prime source is used only in the arithmetic census.

The older mixed-prime theorem has p<q for its order pq² and cannot itself be invoked at 13²·17 by relabeling its primes. The candidate does not do so: it restates the elementary lemmas symmetrically and proves a new side cutoff. Neither the prime-cube four-fiber theorem nor a nonexistent blanket full-spark claim for composite Fourier matrices is used.

Before reading the candidate's final proof, this review independently obtained the three-row-basis argument that merges its old two- and three-residue cases. The final candidate sharpens this into an explicit four-by-four determinant, which was then checked independently, including all row and column phases. The mathematical acceptance rests on the universal argument below, not on a numerical rank test, a census, or a sampled determinant collection.

No historical author/reviewer code was imported or executed. No external writes, novelty claim, or status change was made. All paths in this package identify local review artifacts and are not publication claims.

## 2. Prime-power and semiprime lemmas

For the universal prime-power minor lemma, take distinct nonnegative row exponents e_i and write their alternant as Vandermonde times an integer polynomial S. The evaluation

    S(1,…,1) = ± ∏_(i<j)(e_j−e_i) / ∏_(i<j)(j−i)

is an integer. If k≤ℓ and the row residues modulo ℓ are distinct, every numerator factor and every denominator factor is an ℓ-adic unit. Hence this integer is nonzero modulo ℓ. Reduction modulo 1−ζ_(ℓ^m) sends each selected root to one and gives residue field F_ℓ. Consequently S evaluated on the selected roots is nonzero. The ordinary Vandermonde is nonzero for distinct columns. Transposition is permitted. In particular, prime-order Fourier matrices have every square minor nonzero.

The short-support lemma at pq correctly uses u=min(p,q) and v=max(p,q). CRT changes the frequency indexing only by invertible units. For a nonzero combination with k′≤k≤u nonzero terms, let t be the number of v-frequency groups and k_j their positive sizes. Each corresponding u-character combination g_j is nonzero and has at most k_j−1 zeros. The number z₀ of u-coordinates killing every group therefore satisfies

    0 ≤ z₀ ≤ min_j(k_j−1) ≤ k′−t.

At every other u-coordinate, at most t active v-characters have at most t−1 zeros. Thus

    Z ≤ u(t−1)+(v−t+1)z₀
      ≤ u(t−1)+v(k′−t)
      ≤ v(k′−1) ≤ v(k−1).

All coefficients and inequality directions are valid for 1≤t≤k′≤u≤v. Allowing k′<k correctly handles zero coefficients in an alleged dependence. A dependence on more than (k−1)v distinct rows is impossible. This proves the exact semiprime rank statement used later without importing a general uncertainty theorem.

## 3. Explicit four-minor audit

Let N=p²q and suppose three rows are r_i=r₀+p²w_i, with distinct w_i modulo q. Let r_* be a fourth row outside r₀'s residue class modulo p. Suppose c₁,c₂,c₃ have distinct q-residues, while c₄≠c₁ and c₄≡c₁ modulo q.

Write Δ=c₄−c₁=qk, where k is nonzero modulo p², and set λ=ζ_N^(r₀Δ). Replacing column four by column four minus λ column one leaves its first three entries zero, since

    (r_i−r₀)Δ = p²q w_i k.

Its remaining entry is exactly

    ζ_N^(r_*c₁) λ [ζ_N^((r_*−r₀)Δ)−1].

The factor in brackets is nonzero. Otherwise p² would divide (r_*−r₀)k. The first factor is a unit modulo p² because r_* is not congruent to r₀ modulo p, while k is nonzero modulo p². Negative representatives or reducing the column difference modulo N do not affect the divisibility argument.

The remaining upper-left three-by-three minor has entries

    ζ_N^(r₀c_j) ζ_q^(w_i c_j),   ζ_q=ζ_N^(p²).

The first factor is a nonzero column scalar, and the second gives a prime-q Fourier minor with distinct row and column residues. That minor is nonsingular. Expanding along the modified fourth column proves the four-minor is nonzero. Its row/column ordering gives no hidden zero or sign issue.

Equivalently, the first three rows form a basis under a hypothetical rank-three assumption. Columns with the same q-residue would then be projectively equivalent on all rows. The fourth row, differing by a unit modulo p², rules out two distinct such columns. This independently derived basis interpretation agrees with the exact determinant identity and does not invoke a false general rank-three unit-modulus rigidity theorem.

## 4. Exhaustive occupancy cases

Put B=max(6p,3q) and suppose both a and b exceed B.

First each side occupies at most three residues modulo p. If C had four such residues, a>3q would place four rows in one q-residue class. Write them y+qu_i with distinct u_i modulo p². Removing the column phases ζ_N^(yc) leaves an F_(p²) minor with distinct row indices and four columns distinct modulo p. The transposed universal-minor lemma applies because 4≤p. This gives rank at least four. Transposition, using b>3q, gives the row-side occupancy restriction. This projection uses the actual cyclic Fourier phases, not a false CRT identification of Z_(p²) with Z_p×Z_p.

Let s and t be the nonzero counts of occupied p-residues on the row and column sides; both lie in {1,2,3}.

If s=1, write the rows y+pk. The k are distinct modulo pq. After column scaling, this is an order-pq Fourier restriction with column indices repeated by their residue modulo pq. Each such column fiber has at most p elements. Since b>B≥6p, at least four distinct fibers occur. Also B≥3max(p,q), so a>(4−1)max(p,q). The semiprime lemma with k=4≤min(p,q) yields rank four. This case is impossible.

If s is two or three, at most sp≤3p row fibers occur modulo p². If every fiber had at most two rows then a≤6p, contrary to a>B. Hence there are three rows in one p²-fiber, and the existence of another p-residue supplies r_*.

The columns must occupy at least three q-residues. With at most two, the t≤3 p-residues and at most two q-residues give at most six CRT classes modulo pq. Each class has precisely p lifts modulo p²q, so b≤6p. This contradicts b>B. Moreover b>B≥3q>q ensures a repeated q-residue. A pair c₁,c₄ in that class and columns c₂,c₃ from two other classes meet every hypothesis of the explicit four-minor lemma. This gives rank four again.

These two branches exhaust every occupancy case, for either prime ordering. Every strict inequality used in a pigeonhole step follows from a,b>B. There is no missing case with fewer occupied fibers, no assumption that all allowed fibers occur, and no unwarranted conclusion about arbitrary four-minors.

For comparison with the initial, longer candidate route, its two-residue direct-sum argument is also valid at 13²·17. A column fiber modulo 221 has 13 possible lifts; at most three mod13 column residues allow at most 51 such fibers. If at most two fibers were rich, b≤2·13+(51−2)=75. With b>78 there are three rich fibers. For r=y+13k and c=v+221w, the exact lift factor is ζ_13^(yw); a two-by-two prime minor separates the two supported row blocks. The larger row block has at least 40>34=2·17 rows, hence rank three on the three representative columns, and the other block has rank at least one. Disjoint coordinate supports make the sum of their dimensions at least four. This confirms the old threshold-75 route, but the frozen proof does not need it.

## 5. Density, exact optimum, and equality

### 5.1 Arithmetic-only closure of the target

The side cutoff is unnecessary for merely establishing strict rank-three slack at this particular N. Suppose a,b are arbitrary positive integers with ab≤3N=8619, and put s=a+b.

- If s≤185, then ab≤s²/4 gives density 3s/(ab)≥12/s≥12/185>62/957.
- If s≥187, then ab≤3N gives density 3s/(ab)≥s/N≥187/2873>62/957.
- If s=186, the difference d=b−a is even and ab=(186²−d²)/4. The stable-rank bound forces d²≥120, so the even integer |d| is at least 12. Hence ab≤8613 and density≥558/8613=62/957. Equality forces the unordered pair {87,99}, which meets the scalar constraints.

Thus the exact unrestricted integer scalar minimum is 62/957=186/2871. It exceeds the rank-one baseline by 124/2749461. The argument is independent of the new side theorem and already yields the same global optimum and equality conclusion, with a weaker valid higher-rank-area penalty. No actual rank-three Fourier rectangle at the scalar minimizer is asserted; indeed the new structural theorem rules it out.

The former domain census was arithmetically correct for the explicitly named union. The implication that its first residual required a new structural theorem was not justified. This review preserves that statement as dated history and explicitly corrects the present interpretation.

### 5.2 Stronger density from the new theorem

At p=13,q=17, B=78. For an actual-rank-three rectangle, order the sides a≤b. Stable rank ab≤3N gives

    3/a+3/b ≥ 3/a+a/N.

For 0<a≤78,

    [3/a+a/N]−[3/78+78/N]
      = (78−a)[3/(78a)−1/N] ≥ 0,

since 78a≤6084<8619=3N. Thus the density is at least 29/442=377/5746. The baseline is 186/2873=372/5746, giving precisely 5/5746 of positive excess.

The six divisors 1,13,17,169,221,2873 give unique unordered rank-one minimizing pair {17,169} and D_N=186. The proper-divisor expression 2d+N/d has minimum 203 at d=17, so rank-two density is strictly above 377/(2N). For r≥4, density is at least 4/√N, also strictly above 377/(2N), because 64N=183872>142129=377².

Summing density times area over the disjoint tiling, with total area N², proves the stated cost and higher-rank-area penalty. Strictly positive excess excludes every higher-rank tile from an optimizer. Equality in the accepted rank-one theorem forces full mutually annihilating cosets with the unique unordered side pair {17,169}. Each such tile has area N; hence exactly N=2873 tiles are required. This is tilewise: a common orientation across all tiles is not asserted.

For attainment, K={169i:0≤i<17} and H={17j:0≤j<169} annihilate each other. All 169 row K-cosets crossed with all 17 column H-cosets partition the matrix. Every tile is rank one, has area N, and costs 186. Their total cost is 2873·186=534378. This establishes a sharp global tiling value without claiming the intermediate rank-three bounds are sharp.

## 6. Original exact controls

The new `independent_controls.py` evaluates signed determinant sums as integer polynomials modulo the ordinary cyclotomic polynomial Φ_N, in characteristic zero. Its monomial recurrence uses exact integer arithmetic. Sixty separate SymPy matrix determinants followed by polynomial division cross-check that implementation. No numerical singular-value cutoff, finite-field substitute, or historical checker is used.

The completed controls pass across twelve ordered prime pairs, including both repeated-smaller and repeated-larger primes:

- 1,200 actual mixed-order projection identities, including their nonzero Fourier phase factors, plus the corresponding prime-square minors.
- 2,160 semiprime short-support rank controls for k=2,3,4, with random and residue-concentrated sets at the strict zero-count threshold, and 264 zero-envelope composition checks.
- 150 target one-residue rectangles with 79 rows and 79 columns, each supplying an exact nonzero four-minor.
- 1,800 explicit four-minor factorizations, with equality of exact cyclotomic remainders as well as nonvanishing. The 150 target certificates are retained in `TARGET_EXACT_CERTIFICATES.json`.
- 150 independent target two-residue direct-sum certificates, despite this lemma being unnecessary to the simplified proof.
- 48 structurally genuine rank-three coset-union examples, with independent nonzero three-minors and 720 exact zero four-minors.
- All nine allowed occupancy-count pairs and all 32,357 target scalar shapes satisfying the proved side cutoff and stable-rank envelope. Their minimum relaxed density is 47/715 at (78,110), above the convenient bound 29/442. No Fourier attainability is inferred from this scalar minimum.
- Every entry of the explicit 2873-tile partition: all 8,254,129 entries occur exactly once, and the rank-one difference identity is checked throughout every tile. Cost is exactly 534378.

The run makes 10,666 calls to the exact determinant evaluator; its 60 direct SymPy matrix-determinant cross-checks are recorded separately as cross-checks. `RESULTS.json` contains counts and elapsed time. The finite controls supplement the proof and do not establish an infinite result by extrapolation.

The separate original `check_domain.py` reconstructs exactly the named domain union through 10000. It verifies that adding only 2873 leaves first residual 3757. It also exhausts the unrestricted integer stable-rank shapes at 2873 without imposing the new side cutoff, verifies zero scalar obstructions, and reproduces the unique scalar minimum 62/957 at (87,99). Its initial one-character syntax error was corrected before the successful run; it did not affect the mathematical checker or any result artifact. The final script and successful `DOMAIN_RESULTS.json` are retained.

## 7. Retained boundary and accepted next-gate wording

The census retains D_N²<12N, the dominant-prime domain, isolated accepted lengths 1331 and 2197, and N=11q² for prime q>11. It adds only the newly proved target 2873, without silently treating the new side theorem as a complete tiling theorem at every p²q.

At 3757=13·17², D_N=238 and 12N=45084<D_N²=56644<16N=60112. The new side cutoff is 102. The integer scalar shape (102,110) has area at most 3N and density below D_N/N, so the available scalar envelope does not close that gate. This is an insufficiency witness for these bounds, not an actual rank-three Fourier rectangle or a counterexample.

Accept the universal side theorem min(a,b)≤max(6p,3q) for distinct primes p,q≥5 at order p²q. Accept at N=2873 the exact optimum 534378, rank-one-only full-coset equality with exactly 2873 tiles of unordered sizes {17,169}, and valid higher-rank-area penalty 5/5746. The retained union covers every N≤3756; 3757 remains the next rank-three residual.

Record the correction that the target optimum itself already follows from integer stable rank, whose exact unrestricted scalar minimum is 62/957 above the baseline. The structural theorem supplies an additional general result and a stronger target penalty; it is not represented as indispensable to the target closure.

Preserve actual complex rank, arbitrary Cartesian subsets, the disjoint/no-sharing endpoint-incidence model, separate root/coefficient preparation, storage and I/O, and the inherited possible N extra additions for literal zero-initialized accumulation. No unrestricted Fourier-circuit, basis-change, overlapping/cancelling decomposition, finite-field rigidity, production-performance, sharp-penalty, or worldwide-priority conclusion follows. Parent TO RESEARCH status and priority 42 remain unchanged.
