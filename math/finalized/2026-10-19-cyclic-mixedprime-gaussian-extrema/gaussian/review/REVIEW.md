# ALG-036 nondivisible Gaussian projector theorem: independent review

Date: 2026-10-19 UTC. Owner: ALG-036. Retained priority: 34.

## Disposition

**ACCEPTED at the candidate's stated scope. No mathematical correction remains.**

The frozen candidate is `/workspace/shared/alg036_nondivisible_extrema_20261019_1005`. Its REPORT.md SHA-256 is `269808ef8a379d7a9969655a6f6237f1ccc0aa29ecfcfffaf93eb8552b895edb`; its MANIFEST.sha256 SHA-256 is `02e0521e58cbea22ab9241efc945d2e487160a68b9ef419322ba96cb00113735`.

Accepted results are: complete equality classification in the refined leverage and ambient rank-only bounds at finite positive radius; attainment and a positive fixed-parameter nondivisible gap; centering for every projector; a large-radius counterexample to every orthogonal-line block candidate for every nondivisible dimension pair; two exact opposite-direction comparisons at N=3,d=2; and the exact compact-simplex integral reduction for that case.

This does not identify the exact nondivisible maximum, its maximizing projector, a computable positive gap, or a gap uniform along changing dimensions. It does not settle an arbitrary nondivisible critical-window law, unrestricted sphere-prior adaptivity, Fourier arithmetic complexity, every-input achievability, historical novelty, or all of ALG-036.

## 1. Inherited bound, normalization, and primary source

I read the controlling thin-deficit report and its accepted independent review, then independently checked the entire new argument. The inherited starting point is

    F_r(P,b) <= product_(p_j>0) (1-exp(-r^2/p_j))^p_j
             <= (1-exp(-N r^2/d))^d,

where P is a complex Hermitian orthogonal projector of rank d, p_j=P_jj, Z~CN(0,P), and F_r(P,b)=Pr(max_j |Z_j-b_j|<=r). The proper-complex convention has density pi^(-d)exp(-||g||^2) on C^d; the event uses complex moduli. Neither real Cartesian cubes nor arbitrary covariance matrices are substituted.

I independently opened [Valdimarsson's author-hosted paper](https://uni.hi.is/siv/files/2017/07/optimisers.pdf) and checked Definitions 8–9 on printed page 10, Theorem 12 on page 12, and removal of the Schwartz restriction on pages 15–16. For geometric projection data, its equality structure separates independent intersections from a dependent Gaussian part. On a wholly dependent output space the nonzero equality input is Gaussian; shared independent components use proportional factors. The result applies to nonnegative integrable inputs. The author's [research page](https://uni.hi.is/siv/research/) also identifies the publication and DOI.

Consequently the discontinuous disk-restricted Gaussian functions are covered. The proof does not accidentally use a theorem restricted to strictly positive inputs, to smooth functions, or to real rank-one outputs. No local PDF copy or PDF hash is claimed.

## 2. Equality in the leverage product

### Shift and zero-leverage cases

If p_j=0, the jth coordinate is deterministically zero. Its constraint is redundant for |b_j|<=r, including equality at the boundary, and makes the event empty for |b_j|>r. The positive-rank leverage product is strictly positive at every finite r>0; hence the latter case cannot be an equality case.

For p_j>0 the relevant one-coordinate input is the Gaussian density truncated to the disk of radius r/sqrt(p_j) and center b_j/sqrt(p_j). Every such disk has positive mass. A strictly radially decreasing Gaussian gives strictly more mass to the centered disk whenever b_j is nonzero: at the density level whose superlevel disk has the same radius as the test disk, two distinct disks have strictly smaller intersection area than the centered pair. Continuity preserves this loss for a positive interval of density levels. Layer cake therefore proves strictness, not merely nonincrease. Positive leverage exponents prevent any loss from being hidden in the product. Thus equality with the centered leverage product forces b_j=0 at every positive-leverage coordinate.

### Geometric datum and complex structure

Write P=VV* with V*V=I_d. For a nonzero row v_j, B_j=v_j/sqrt(p_j) is a real rank-two coisometry. Let E_j=range(B_j*). Identifying the target C with E_j by B_j* is an isometry, preserves two-dimensional Lebesgue measure, and converts B_j into orthogonal projection onto E_j. Hence the required datum is exactly

    sum_j p_j Pi_(E_j) = I_(C^d).

The E_j are complex lines and span the domain. Each centered input on E_j is pi^(-1)exp(-||x||^2) restricted to ||x||<=r/sqrt(p_j).

The possible real-plane/complex-line mismatch is resolved as follows. Every E_j and E_j-perp is invariant under the same complex structure J. Every independent intersection is therefore J-invariant. A nonzero such intersection cannot choose every E_j-perp, since the common kernel is zero. It lies in some E_j, and a nonzero complex subspace of a complex line is the whole line. Thus all independent components here are complete complex lines, never arbitrary real one-dimensional factors.

For an independent line K and any row line E_j, the defining intersection puts K either inside E_j or inside E_j-perp. The first alternative gives K=E_j; the second gives orthogonality. It follows that every row line not itself an independent component lies wholly in the dependent complement. If that complement were nonzero, at least one row line would be there, because the row lines span the domain. Its equality input would then be a nonzero Gaussian on the whole real plane. This has positive density everywhere and cannot equal a density with bounded disk support. Any further real critical decomposition within the dependent component does not change this conclusion: its Gaussian factors remain positive on their entire factors and together span that output space.

The dependent complement is therefore zero. There are precisely d distinct row lines, and they are pairwise orthogonal.

### Magnitudes and phases

Within a shared line, the input functions must be proportional almost everywhere. Distinct cutoff radii would produce an annulus of positive area where one function is positive and another zero, so all p_j in that line class are equal. The geometric identity restricted to the line says their sum is one. A class of n_l rows therefore has p_j=1/n_l.

Choosing the orthonormal basis given by the d distinct lines, each row has one nonzero entry zeta_j/sqrt(n_l), with |zeta_j|=1. This is exactly the phase-block projector stated in the candidate. Conversely independent standard complex coefficients on those d lines give success product_l(1-exp(-n_l r^2)), equal to the refined leverage product. Zero rows and their allowed translated coordinates do not change this event. Necessity and sufficiency are both established.

## 3. Equality in the rank-only bound

For a=r^2>0 the inherited scalar function h_a(p)=p log(1-exp(-a/p)), with h_a(0)=0, has the displayed strictly negative second derivative on p>0. Strictness also extends across zero: for q>0 and 0<t<1, h_a(tq)>t h_a(q), directly because a/(tq)>a/q. Thus ambient Jensen equality requires all N leverages to be d/N, including the exclusion of zero rows.

If F equals the rank envelope U, both F<=L and L<=U must be equalities. The first gives phase blocks and centering, and the second gives 1/n_l=d/N on every block. Thus all block sizes equal the integer N/d, and d divides N. Conversely equal-size phase blocks attain U. This proves the complete ambient equality classification. Equal diagonal alone is necessary but insufficient.

The finite positive-radius condition is essential. At r=0 all positive-rank probabilities and the envelope are zero for every projector and shift, so the equality classification would be false. At an infinite radius the probabilities become one. Rank zero is deterministic and lies outside the stated theorem. The edge cases d=1 and d=N are divisible and are correctly included.

## 4. Centering, compactness, and the strict gap

The candidate's centering argument correctly invokes classical Brunn–Minkowski as a standard auxiliary theorem; it does not claim to prove that theorem. For C_b(R)={g:||Vg-b||_infinity<=r, ||g||<=R}, compactness and convexity hold, C_-b(R)=-C_b(R), and the midpoint of a point in each set belongs to C_0(R). This last inclusion remains valid when b is outside range(V). Equal volumes plus Brunn–Minkowski yield vol(C_b(R))<=vol(C_0(R)); zero-volume or empty cases are immediate. Integrating the Gaussian's radial superlevel balls gives F_r(P,b)<=F_r(P,0). No nonsingular ambient density for the possibly singular Z is assumed.

The rank-d projector set is compact: it is closed by its Hermitian, idempotent, and trace equations and bounded in operator norm by one. In the common coupling Z=PG with G~CN(0,I_N), P_kG tends pointwise to PG. For centered events at r>0 every positive-variance coordinate has zero probability of lying on the boundary circle; a zero-variance coordinate is zero and strictly inside. Dominated convergence therefore proves centered continuity. Hence the centered maximum is attained, and centering makes it the maximum over all translations too.

Nondivisibility excludes equality at that actual maximizer, yielding delta_(N,d)(r)>0. Joint centered continuity in (P,r) for r>0, compactness, and the usual subsequence maximum argument give continuity of M and delta in r. Consequently delta has a positive minimum on a fixed compact radius interval away from zero and infinity. These are nonquantitative statements with N,d fixed.

### Independent alternate compactness proof

The strict-gap conclusion does not even require the centering lemma. For ||b||_infinity>r choose a coordinate attaining that norm. Since p_j<=1, the reverse triangle inequality and its scalar Gaussian tail give

    F_r(P,b) <= exp[-(||b||_infinity-r)^2],

with the zero-variance case equal to zero. An explicit block construction supplies some positive lower value L. Choosing R=r+sqrt(log(2/L)) confines every maximizer to ||b||_infinity<=R, since outside that set probability is at most L/2.

The function F is jointly upper semicontinuous in (P,b): under the common PG coupling the event is closed, so its indicators satisfy the pointwise limsup inequality, and reverse Fatou applies. Upper semicontinuity on the compact projector/translation product gives an actual maximizer. The equality classification again yields the strict gap.

It is important here to say upper semicontinuous, not continuous. For P=diag(1,0), b=(0,r), the probability is 1-exp(-r^2), whereas b=(0,r+epsilon) gives zero. This exact zero-row boundary control is included in the independent results.

## 5. General large-radius obstruction to block optimality

Selecting d orthonormal Fourier columns gives a rank-d projector with diagonal d/N. The union bound yields success at least 1-N exp(-Nr^2/d), without coordinate independence.

In any orthogonal-line block projector, a line class of size n_l has leverage sum one and maximum leverage at least 1/n_l. Its centered success is exactly 1-exp(-r^2/max p_j), at most 1-exp(-n_l r^2). Different line classes are independent. Since at most N coordinates are used, some class has size at most m=floor(N/d), so the whole success is at most 1-exp(-mr^2). Centering shows that a translation cannot improve that family bound.

For nondivisible N,d, theta=N/d-m is positive. The stated sufficient condition r^2>log(N)/theta makes the first construction's lower bound strictly exceed the entire block family's upper bound. The threshold and direction are correct. It is sufficient, not asserted necessary. Nearly equal sizes are optimal within the constant-magnitude block family by discrete balancing and strict concavity in block size.

This large-radius result does not establish any critical-window separation when r stays fixed and N grows: the displayed sufficient threshold generally grows with log N. Nor does fixed-dimensional strictness itself produce a uniform asymptotic gap.

## 6. Exact N=3,d=2 comparisons and reduction

At r^2=log16, the projector I-11*/3 has variance 2/3 per coordinate, so each marginal failure is 1/64. Its success is at least 61/64=3904/4096. The size-(2,1) block projector has exact success (15/16)(255/256)=3825/4096. The certified improvement is 79/4096. The rank envelope is 3969/4096, and its strictness for the global maximum is justified by the theorem, not by finite computation. The chain of rational bounds in the candidate is correct.

For the reverse comparison, the parameterization z=(x,y,-x-y) has complex Gram determinant 3 and therefore induced real four-volume factor 3. The unit-disk lens integral evaluates to pi/2-3sqrt(3)/8, giving normalized section coefficient C=3-9sqrt(3)/(4pi), approximately 1.7595099853. Bounding the Gaussian density by its value at zero gives success at most C a^2. On the size-(2,1) block product the density is at least exp(-3a), giving success at least 2a^2 exp(-3a)>=2a^2(1-3a). At a=1/100 the lower coefficient 97/50 exceeds 9/5>C. This proves the stated two-projector comparison and does not imply global block optimality at small radius.

Finally every rank-two complex projector in C^3 is I-uu*. Diagonal unitary conjugation removes the phases for this modulus event, so q_j=|u_j|^2 parametrizes the problem. Relabeling so q_3=max q_j gives q_3>=1/3. The graph matrix with third row (-sqrt(q_1/q_3),-sqrt(q_2/q_3)) has Gram determinant 1/q_3 and image u-perp. Its induced Gaussian density is exactly the integral in Section 8, including when q_1 or q_2 vanishes. The phase/permutation invariance, Jacobian, exponential, integration domain, and prefactor all check out. The restricted simplex is compact and contains a representative of every projector class.

The candidate correctly leaves maximization of that integral unresolved. No claim that two q_j must coincide, that only two candidate shapes compete, or that a particular crossover radius is optimal is accepted or needed.

## 7. Original controls and frozen integrity

The review's two programs were written independently for this audit and executed locally. They do not load or execute historical or candidate programs and make no network requests.

`controls/independent_checks.py` passed:

- symbolic Hessian and zero-limit identities;
- exact rational N=3 projector and counterexample identities;
- seven exact phased-block data, including zero rows, with 28 scalar comparisons;
- 4,755 rank-one probability/leverage equality and strictness cases;
- 27 direct translated-disk quadratures;
- five uniform-translation truncation cutoffs;
- the exact zero-row discontinuity example distinguishing continuity from upper semicontinuity.

`controls/section_geometry_checks.py` passed:

- three symbolic Gram/projector/real-Jacobian identities;
- 83 exact rational simplex-plane cases;
- four exact section-integral and small-radius relations;
- two direct boundary-simplex integral identities;
- 354 high-precision nondivisible threshold diagnostics;
- 2,049 balanced-block partition controls.

These finite controls support algebra, normalization, and edge cases. They do not replace the equality theorem or establish a global maximizer. The author's fresh checker was read but not replayed; only this review's original programs were run.

The integrity audit independently verifies every candidate payload hash, detects unlisted payload files, and checks the four inherited source records against their current bytes. `controls/audit_sources.json` records the results. The candidate manifest is copied as `CANDIDATE_MANIFEST.sha256`. No inherited file or candidate file was modified, no historical code was executed, and no external write or publication was performed.

**Final disposition: accept the frozen packet's scoped equality, strict-gap, counterexample, and simplex-reduction results. Keep the exact nondivisible optimization and asymptotic gates open.**
