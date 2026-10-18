# Independent review: dominant-prime Fourier rectangle optimum

Date: 18 October 2026 UTC. Candidate: `rectangle_triprime_20261018_1140`.

## Verdict

**ACCEPT within the stated domain and model. All fresh controls passed.** No mathematical correction was needed. An inherited citation-role label was corrected by the author before the final frozen manifest was supplied.

For the complex cyclic Fourier matrix, disjoint nonempty Cartesian tilings, and exactly the objective `sum_t r_t(a_t+b_t)`, the optimum is `N(m+p)` whenever `N=mp`, p is prime, and `1<=m<p`. All optimizing tiles have rank one and are full products of subgroup and annihilator cosets, with unordered side sizes `{m,p}`. Every optimum therefore has N tiles of area N.

The quantitative bound is also correct:

`C >= N(m+p) + delta A_{>=2}`, where `delta=min(1/p,(p-m)/(mp))`.

The result settles the prior residual example N=57 at optimum 1254. It strictly extends the prior balanced-divisor/twice-prime acceptance but does not settle every nonsquare composite length. Parent status remains TO RESEARCH at priority 42. This review performed no external writes and establishes no worldwide novelty, score, or archival-status claim.

Frozen candidate `REPORT.md` SHA-256: `14f1a590aa06866649bd406a4846860dfa770c9c521c92d1a96921ae67aad4fc`.

Frozen author `MANIFEST.json` SHA-256: `4f3a59c92ab20a77b14d061da3bc5fa429d573f8a15550ed895519eb71400e98`.

## 1. Prime-fiber rank lemma

The lemma is valid in its stronger stated form: for any prime divisor p of N, put m=N/p. A Fourier rectangle of side sizes a<=b and complex rank r satisfies `r>=ceil(a/m)`. No coprimality assumption is needed.

There are m row classes modulo m, so one has at least `ceil(a/m)` selected rows. In that class write `k=k0+m u`; the u values are distinct modulo p because a residue class modulo m in Z_N has precisely p members. Each column class modulo p has m members, so the b selected columns occupy at least `ceil(b/m)` distinct classes. Select one representative of each.

On this submatrix the entry factors as `omega^(-k0 j) (omega^m)^(-u j)`. The first factor is a nonzero column scaling. The second is an exact prime-order Fourier submatrix indexed by distinct u and distinct `j mod p`; `omega^m` has order p, including when p divides m. Chebotarev makes its rank the smaller selected side size. Both side sizes are at least `ceil(a/m)`, and submatrix rank cannot exceed the original rank.

I freshly checked the primary exposition [Garcia–Karaali–Katz, Section 1.1, Theorem 1.1](https://arxiv.org/html/1807.07648v4). It states the prime complex Fourier nonvanishing-minors result with the Fourier normalization explicitly defined. Scalar normalization and changing the primitive root leave ranks unchanged. The review uses that established result; neither a new proof of it nor a finite-field analogue is asserted.

## 2. Stable rank and density arithmetic

For the unnormalized complex Fourier matrix, `F*F=N I`. Restricting rows and columns cannot increase its spectral norm, so every singular value of an a-by-b rectangle is at most sqrt(N). All entries have modulus one, giving squared Frobenius norm ab. Consequently `ab<=Nr`. The normalization and inequality directions are correct.

The prime-fiber lemma gives `a<=mr`. From stable rank,

`rho=r/a+r/b >= r/a+a/(mp)`.

The candidate's two cases cover every positive integer r:

- If `mr<=p`, then `a<=mr<=p`, and
  `r/a+a/(mp)-1/m-r/p = (mr-a)(p-a)/(map) >= 0`.
  The identity is exact, and every denominator is positive. Thus `rho>=1/m+r/p`; if r>=2 the excess over `1/m+1/p` is at least `1/p`.
- If `mr>=p`, then AM-GM and stable rank give
  `rho>=2r/sqrt(ab)>=2sqrt(r/(mp))>=2/m`.
  Its excess over the target is at least `(p-m)/(mp)>0`. The two cases are consistent at the common boundary.

It follows that the stated delta is positive and valid uniformly for every higher-rank tile. The argument even establishes the weak target density for rank one without separately importing its old classification.

The near-optimality consequence `A_{>=2}<=E/delta` follows directly whenever the objective is at most `N(m+p)+E`. Its interpretation is the total area of higher-rank tiles, not their count and not a circuit lower bound with shared computation.

## 3. Nearest divisors, global optimum, and equality

Because p is prime and m<p, p does not divide m and occurs to exponent one in N. Also `m<sqrt(N)<p`. Any divisor of N below sqrt(N) cannot contain p and hence divides m. Therefore m is the largest such divisor. The function `d+N/d` is strictly decreasing up to sqrt(N), so the only minimizing divisor pair is `(m,p)`, up to exchange. This verifies the exact assertion `D_N=m+p`, including m=1 and p=2.

Disjoint coverage gives total tile area N². Summing the local inequalities yields the objective lower bound and the higher-rank-area penalty. As delta is strictly positive, a tiling achieving the endpoint cannot contain any higher-rank tile. There can be no cancellation of local slack.

For r=1 the first density case applies because m<p, and `a<=m`. Equality in the displayed identity forces a=m: its other scalar zero a=p is excluded by a<=m<p. Equality in stable rank then gives b=p. Thus every equality tile has precisely those unordered side sizes.

For its set structure, rank one is equivalent to `N | (k-k0)(j-j0)` for all selected row and column indices. If H is generated by row differences, the rows lie in a coset of H and the columns in a coset of its annihilator. Their ambient sizes multiply to N. The actual sizes also multiply to N, so both inclusions must be equalities. This argument handles both tile orientations and does not assume a common orientation throughout a tiling.

The explicit row residue classes modulo p and column residue classes modulo m give N disjoint rank-one Cartesian products, cover every matrix entry once, and cost m+p per tile. They attain the lower bound. Since each equality tile has area N, every optimal tiling has exactly N tiles. These conditions are necessary and sufficient within the stipulated disjoint tiling model.

## 4. Sharpness and the former N=57 obstruction

The proposed sharp-gap example is valid. Choose r distinct complete row cosets of the order-m subgroup and all columns in its annihilator subgroup of size p. Repeated rows collapse to r distinct prime-Fourier rows, so the rank is exactly r. The rectangle has shape `mr × p` and density `1/m+r/p`. For r=2 when p>=2m, it realizes the stated delta `1/p`. No claim is made that the other branch of delta is sharp.

At N=57, the old relaxed shape `(a,b,r)=(10,11,2)` violates the new Fourier-specific rank lower bound because `ceil(10/3)=4`. This resolves the limitation of the old scalar relaxation rather than turning that relaxed tuple into a real Fourier counterexample.

The candidate's explicit ten rows in one modulo-3 class and eleven columns in exactly four modulo-19 classes do attain rank 4. After removal of repeated columns they form a 10-by-4 prime Fourier submatrix. The stated 6-by-19 rank-2 example has cost 50 and area 114, whereas its baseline target cost is 44; its density excess is exactly 1/19.

## 5. Independent finite controls and source integrity

The new `independent_controls.py` imports no author or predecessor checker. All actual ranks are computed over exact cyclotomic number fields with an independently selected algebraic primitive root, rather than using numerical singular-value thresholds or modular ranks. The full fresh run passed in approximately 103 seconds, with the following independently reproduced controls:

1. **21,342** nonempty subset rectangles exhaustively checked at N=2 through 7. For each, the exact rank, stable-rank inequality, every prime-divisor fiber bound, fiber-gauge exponent identity, rank-one plaquette equivalence, and applicable density/equality conditions were checked.
2. **208** additional exact rectangles at N=8,9,10,12,15,18,20,21,25,27,33,35,39,55,57,77. These include repeated-prime cases where p divides its cofactor, random subsets, and full-column rank controls. All obey the generalized fiber lemma.
3. Both explicit **N=57 examples**, independently computed over Q(zeta_57), have their claimed exact ranks 4 and 2 and their claimed cost/area values.
4. **3,194,432** higher-rank scalar shapes across all **210** dominant-prime lengths through N=300 satisfy the quantitative delta inequality. The minimum integer rank allowed by stable rank, the fiber bound, and rank>=2 was checked, which suffices for every larger rank. A further **60,175** rank-one scalar shapes have nonnegative slack and equality only at `(a,b)=(m,p)`.
5. **103** explicit disjoint coset tilings through N=150, comprising **7,915** tiles, have exact coverage, rank-one structure, and objective N(m+p). Separately, **56** exact rank-2 rectangles through N=100 attain the 1/p local gap in its stated regime.
6. The independent finite census through N=1000 confirms **238** newly covered lengths and precisely **343,847** outside the combined domains. Nearest-divisor pairs are independently enumerated, rather than inferred from the desired theorem statement.

The computations are supplementary controls. The infinite-domain theorem and complete equality characterization rest on the proof above.

The author and prior acceptance manifests are verified before testing. The author manifest is verified again after testing to detect any change to frozen inputs. The stdout log is supplemental and is deliberately outside the author's four-file core manifest.

The previous acceptance's retained Phase7 source supplies the inherited objective and qualifications. This review verifies the local accepted chain and freshly reads the primary full-spark source; it does not pretend to have newly fetched the GitHub dependency again.

## 6. Remaining scope and accepted wording

N=343 has nearest divisor pair `(7,49)`, `D=56`, and `D²=3136>8N=2744`. Its largest prime 7 is smaller than cofactor 49. Thus neither the prior balanced-divisor theorem nor this dominant-prime theorem applies. The universal sandwich is correctly `686 sqrt(686) <= optimum <= 19208`.

N=847=7*11² similarly has nearest pair `(11,77)` with D=88 and lies outside both domains. The finite census through N=1000 counts 238 newly covered lengths and leaves precisely 343 and 847 outside the union. This is a finite census of these theorem domains, not an assertion that no other theorem might apply or an infinite-domain proof.

The combined accepted domain covers every N=3p for prime p: p>3 follows here, p=3 is the old square case, and p=2 is already balanced. It also covers all semiprimes: distinct prime factors satisfy the present hypothesis, while equal factors give an already-settled square.

Recommended accepted next-gate statement:

> Accept the exact rank-weighted disjoint Fourier tile optimum `N D_N` and full-coset, rank-one-only equality characterization for every `N=mp` with p prime and `1<=m<p`, together with the stated positive higher-rank-area penalty. This extends the prior balanced-divisor domain, settles N=57 at 1254, and excludes its relaxed rank-2 shape by a sharp actual rank-4 bound. General nonsquare composites outside the combined domains remain open. Preserve the complex-field dependency, disjoint/no-sharing objective, preparation/storage/I/O qualifications, and parent TO RESEARCH status and priority 42.

No claim extends to overlapping or cancelling rectangle decompositions, shared intermediate computations, general invertible endpoint basis changes, unrestricted Fourier arithmetic circuits, finite-field full spark, or production/cold-cost performance. The inherited extra-N-additions qualification for literal zero-initialized accumulation remains unchanged.
