# ALG-036 thin-deficit projector theorem: independent review

Review date: 2026-10-19 UTC. Owner: ALG-036. Priority remains 34.

## Disposition

**ACCEPTED at the stated thin-deficit scope. No unresolved mathematical correction remains.** The acceptance applies to the frozen candidate identified below, after full proof review, primary-source verification, independent exact controls, and an inspected byte-identical replay of its newly authored checker.

The result under review is the proper-complex Gaussian inequality

    Pr(||Z-b||_infinity <= r)
      <= product_(j:p_j>0) (1-exp(-r^2/p_j))^p_j
      <= (1-exp(-N r^2/d))^d,

for an orthogonal rank-d complex projector covariance P, p_j=P_jj, arbitrary translation b, and positive radius. Positive-rank radius zero has probability zero. The rank-only bound is exactly attained when d divides N. Its extension to transcript-only adaptive measurements gives a sharp thin-deficit Gaussian-average transition, including the corrected critical location and window on the stated attaining dimensions.

Acceptance is scoped. It does not identify the exact nondivisible extremum, prove a theorem for every arbitrary adaptive sphere-prior algorithm, provide a positive every-fixed-input randomized guarantee, prove a Fourier arithmetic lower bound, change owner or priority, establish historical novelty, or close the full ALG-036 owner.

## 1. Source and primary-theorem verification

I read the complete baseline report, its independent acceptance, the new proposal, and all eleven sections of the new report. The baseline supplied the exact information model and previously accepted posterior argument; the new proof has nevertheless been checked directly below. The new mathematical strengthening is not inferred from the old coarsened constant-fraction estimate.

The primary source was opened independently at the author-hosted URL:

[Bennett–Carbery–Christ–Tao, The Brascamp–Lieb inequalities: finiteness, structure and extremals](https://math.berkeley.edu/~mchrist/Papers/bcct11.pdf).

Definition 1.1, printed pages 1–2, sets real Euclidean spaces with Lebesgue measure, surjective maps with trivial common kernel, nonnegative exponents, and measurable nonnegative inputs. Example 1.6, page 3, states the geometric constant-one result for subspace projections. Definition 2.1 and Remark 2.2, page 9, explicitly give the equivalent coisometry formulation: B_j B_j*=I and sum p_j B_j*B_j=I. Those identities imply nondegeneracy. Proposition 2.8, page 12, proves that the full Brascamp–Lieb constant is one. These hypotheses cover the candidate's real rank-two maps and Gaussian-restricted disk inputs; no rank-one-only theorem or unverified higher-rank rearrangement principle is being substituted.

The complex-Gaussian application is a derivation in the candidate and this review, not a theorem attributed verbatim to that source. The report also gives a valid direct proof of the precise constant-one input case it needs.

## 2. Direct heat-flow supplement

The supplementary proof is correct. For positive time, each heat convolution is smooth and positive. Compact support of a nonzero nonnegative input gives Gaussian tails and log derivatives of at most polynomial growth; the weighted identity combines these into integrable decay in every domain direction. Thus differentiation and integration by parts on a compact positive-time interval are justified.

Writing v_j for the target-space log-gradient, the derivative is the integral of the product times

    sum p_j |v_j|^2 - |sum p_j B_j* v_j|^2.

The linear map from the direct sum with coordinates sqrt(p_j)v_j to sum p_j B_j*v_j has norm one, since its product with its adjoint is sum p_jB_j*B_j=I. The displayed quantity is nonnegative. Taking traces gives sum p_j dim(H_j)=dim(H). With x=sqrt(t)z, the large-time Gaussian has the correct total integral one; compact support gives an integrable dominating Gaussian. At time zero, the disk-boundary exceptional sets and their surjective linear preimages have measure zero. Fatou's lemma supplies the required lower endpoint. The argument does not incorrectly require that discontinuous disk indicators be smooth initially.

## 3. Complex normalization, translations, and zero leverage

Let P=VV* with V*V=I_d and row v_j. The real matrix of the unnormalized complex row a+ib is

    T_j = [a, -b; b, a].

Direct multiplication gives T_j T_j^T=p_j I_2, while realification of V*V gives sum T_j^T T_j=I_(2d). Therefore B_j=T_j/sqrt(p_j) is a rank-two coisometry and sum p_j B_j^T B_j=I_(2d). Trace gives sum p_j=d, not 2d. The dimension is 2d, but each target dimension is two, so the scaling relation is 2 sum p_j=2d. This resolves the potentially dangerous factor-of-two issue.

For f_j(y)=pi^(-1) exp(-|y|^2) times the shifted radius-r/sqrt(p_j) disk indicator, the product of f_j(B_jg)^p_j is exactly pi^(-d) exp(-||g||^2) times the full coordinate event. Positive indicator powers leave the indicator unchanged. Thus the geometric inequality applies to the actual CN(0,I_d) density, whose real variances are 1/2, with no omitted normalization constant.

The one-dimensional mass is that of CN(0,p_j) in the disk centered at b_j. Layer cake bounds each intersection of a radial-density superlevel disk with a translated disk by its concentric maximum. Its centered mass is exactly 1-exp(-r^2/p_j). Arbitrary shifts are therefore valid; no singular-covariance coordinate independence is assumed.

A zero-leverage coordinate is deterministic zero. An incompatible translated constraint makes the event empty; otherwise the coordinate is omitted before the geometric datum is built. At positive rank and radius zero, any nonzero row is nonatomic, so the event has probability zero. Rank zero is separately deterministic and is not put into a formula dividing by d or p_j.

## 4. Concavity, ambient dimension, and equality

For a>0, h(p)=p log(1-exp(-a/p)) has

    h''(p)=-(a/p)^2 exp(a/p) / [p(exp(a/p)-1)^2] < 0.

Its continuous extension h(0)=0 is concave, including at the endpoint. Jensen over all N leverage values therefore gives the displayed rank-only upper bound; excluding zero values would instead give the stronger bound with the positive-leverage support size. The direction is correct. The derivative h'(p)=log(1-exp(-a/p))-(a/p)/(exp(a/p)-1) is negative, which also proves the needed monotonicity in residual rank.

For d disjoint blocks of sizes n_l, each normalized block indicator gives one independent complex residual coordinate g_l, copied at scale 1/sqrt(n_l). The actual event is the intersection of d independent disks |g_l|<=sqrt(n_l)r. Its exact probability is product_l(1-exp(-n_l r^2)). The refined leverage product has exactly the same value because each block's n_l exponents sum to one. Equal blocks give all p_j=d/N and attain the ambient bound when d|N. The report does not mistake equal diagonal leverage alone for a sufficient extremizer characterization.

## 5. Adaptive posterior and stopping

The seed is independent of x and all random choices can be included in that seed. Conditional on the prior transcript, the next query row is a fixed measurable vector. For v=a*Pa>0, the Gaussian innovation decomposition gives mean increment Pa(y-a*m)/v and covariance P-Paa*P/v. The removed direction is a unit vector in range(P), so the covariance is exactly the orthogonal projector onto the updated query kernel. If v=0, the answer is already determined and the posterior does not change.

An almost-sure finite stopping event {T=t} belongs to the deterministic-time transcript sigma field. Testing the conditional-kernel identity separately on each event and summing proves the stopped posterior. The stopping decision does not introduce an unobserved condition. With a limiting infinite transcript, the finite-dimensional nested subspace can lose rank at most N times and is eventually constant pathwise; the conditional means converge by the L2 martingale theorem. The conditional characteristic function has the correct exponent -h*Ph/4. A countable dense family followed by continuity identifies the limiting conditional Gaussian. No hidden deterministic bound on the query count is needed.

After a fixed target unitary, covariance remains an orthogonal projector. The estimate minus the posterior mean is an arbitrary fixed shift under transcript conditioning, exactly the allowed shift in the small-ball theorem. Average that conditional bound, then use the negative derivative in residual rank when the pathwise deficit is at least d. An exceptional rank event can be split off at its probability cost; an expected rank deficit cannot be substituted.

## 6. Norm envelopes and the critical window

For S=||x||^2, the moment generating function is (1-lambda)^(-N). Optimizing at lambda=epsilon/(1+epsilon) and lambda=-epsilon/(1-epsilon) gives the upper and lower tails in the report with the correct signs. The proof uses event inclusions only: relative success and S<=N(1+epsilon) imply fixed-radius success; fixed-radius block success and S>=N(1-epsilon) imply relative success. It never conditions a Gaussian posterior on either norm event and never assumes residual/norm independence.

The complement-query construction is admissible for each fixed unitary U: query q_l*Ux for an orthonormal basis of the orthogonal complement of the output residual subspace, and decode its orthogonal projection. Its information cost is exactly N-d complex measurements. No claim about inexpensive dense arithmetic is made.

Set w=NC^2/d-log d and lambda=d exp(-NC^2/d)=exp(-w). For finite w->s and d->infinity, d log(1-exp(-w)/d)->-exp(-s). The elementary upper exponential bound gives zero success when w->-infinity; Bernoulli's inequality gives probability tending to one for the attaining construction when w->+infinity. With epsilon_N=N^(-1/4) in the critical d comparable to N/log N regime, both norm tails vanish and epsilon_N NC^2/d->0, so the same window survives relative normalization. The report correctly gives a universal limsup bound, not a claim that every decoder attains the bound.

The center d_c log d_c=NC^2 gives d_c=NC^2/W(NC^2), hence denominator log N-log log N+log C^2+o(1). The derivative of w at that center is -(log d_c+1)/d_c, establishing width d_c/(log d_c+1), of order N/log^2 N, with the sign w->-h for a positive scaled rank increment h. Thus the attaining success limit is exp(-exp(h)). The integer/divisor-lattice qualification is indispensable and is present.

The first-order threshold constant is C^2. For deficit coefficient a>C^2 all admissible schemes have vanishing success; for a<C^2 nearly equal blocks give high Gaussian-average success on all dimensions. The statement also handles d=o(N/log N) and d much larger than N/log N. In particular d=floor(C^2N/log N) lies on the high-success side: its w grows like log log N-log C^2. Merely specifying ratio d/(N/log N)->C^2 does not select a limit.

## 7. Nondivisible dimensions

Let N/d=m+theta. The nearly equal-block exceedance intensity is the universal intensity times

    A(theta,C)=(1-theta)exp(theta C^2)
                 + theta exp(-(1-theta)C^2).

This factor is at least one by convexity and can remain above one. Therefore the nearly equal-block critical limit is exp(-A(theta_0,C) exp(-s)) when theta converges, not automatically the universal Gumbel upper envelope. The formula and its relative-norm transfer are correct. It is not evidence that no better projector exists; the candidate leaves the nondivisible exact extremum open.

## 8. Sphere and deterministic-input distinctions

For the block linear decoder, positive radial scaling gives an exact samplewise equivalence between Gaussian relative-error success and fixed-radius success on the sphere of radius sqrt(N). Its Dirichlet proportions yield the finite inclusion-exclusion expression in the report. The special N=1 boundary and positive-rank C=0 case are explicitly separated. At N=2,d=1,C=1 the sphere probability is one, while the fixed-radius Gaussian probability is 1-exp(-2); this is a useful control against conflating those two laws.

The universal sphere upper bound is restricted to algorithms whose query rows and stopping choices are unchanged by positive scaling of answers and whose decoder scales accordingly. Under precisely those assumptions, the same admissible algorithm runs on both points of a ray, so the success-event identity and deficit transfer are justified. The report expressly declines to apply the Gaussian posterior to a general sphere prior. A sphere posterior is generally a translated residual sphere, not a Gaussian, and centered disks need not maximize its mass. No uncharged norm observation is introduced.

For an every-fixed-input guarantee on the full input space, averaging over Gaussian x immediately contradicts a uniformly high success promise whenever the average upper bound tends to zero. The bad input can be fixed before an independent seed is drawn. Conversely a high Gaussian-average success construction gives no every-input positive guarantee. The candidate maintains this distinction and does not promote average-case sharpness to worst-case achievability.

## 9. Block-local consequence and exclusions

The retained pathwise accounting gives D>=B(M-s). If M/log N->kappa and M-s=q is fixed, this lower bound has coefficient q/kappa at scale N/log N, so q/kappa>C^2 lies in the universal vanishing-success regime. At equality its actual sequence w must be used. The attaining unrestricted query construction need not be implementable in that original block-local architecture, especially for a prescribed output unitary. No such positive architectural claim is accepted.

Properness of the complex Gaussian, the complex modulus infinity norm, the independent seed, transcript-only information, and pathwise complex rank remain required. Nonproper Gaussians, arbitrary covariance matrices, raw-input algorithms, uncharged nonlinear statistics, every-input achievability, arithmetic complexity, and blanket owner closure remain outside the result.

## 10. Independent controls and frozen-byte audit

The frozen candidate is `/workspace/shared/alg036_thin_deficit_20261019_0125`.

- REPORT.md SHA-256: `ae348fde6e14b20f3bb7227a7c56c37d979136a5eed1540de933bf940e97b851`
- MANIFEST.sha256 SHA-256: `829f407ab9681470de0838856ee64eb9611e56214d6f893a2f1bc63e6f4776b5`
- All ten candidate payload entries verify, with no missing or unlisted payload file.
- All three copied controlling local sources are byte-identical to their declared originals, with matching lengths and SHA-256 values.
- The accepted baseline's nine manifest entries and its earlier independent review's seven manifest entries verify without executing any historical code.

`controls/audit_sources.json` records this full integrity audit and the independently checked primary-source locations. `CANDIDATE_MANIFEST.sha256` is a byte copy of the candidate seal. No local PDF body or PDF hash is claimed: the primary theorem was independently read in the author-hosted PDF through the web tool.

My separately authored `controls/independent_checks.py` passed:

- 84 exact rational complex frame/projector data, constructed using complex Householder transformations rather than the author's plane rotations
- 363 positive rank-two row identities and 57 zero-leverage row checks; full weighted identity decompositions and leverage sums verified exactly
- 159 positive-innovation projector updates and nine redundant-query identities
- Exact symbolic first/second derivative identities and 42 equal-block exponent controls
- 1,740 high-precision rank-envelope/monotonicity diagnostics and 15 critical-window/norm-envelope diagnostics

The separately authored `controls/window_sphere_checks.py` also passed:

- Twelve rational-radius cases covering 24 direct N=2 simplex-interval identities
- 24 exact integrations of Dirichlet marginal densities over an untruncated cube
- Ten exact integrations over a truncated two-coordinate simplex domain
- Exact critical-width and Chernoff-optimizer identities
- Twelve high-precision critical-width diagnostics and nine nondivisible rounding diagnostics

These sphere controls integrate the marginal density directly, independently of the author's inclusion-exclusion evaluator and simulation. The checker outputs record all diagnostics; finite algebra and numerical checks support transcription and edge cases, while the all-dimensional proof establishes the theorem.

I read the author's entire newly authored checker before replay and rechecked the final edits. It was copied into `controls/author_replay/` and run there, so its self-written RESULTS.json did not overwrite the frozen candidate. The replay passed and reproduced the candidate RESULTS.json byte-for-byte (SHA-256 `c701b9c13ecb8b37263d4bf899227fed8eb8a75b651acea62faf22b043c1ef45`). This covers its 19 exact projectors, 100 rank-two identities, 840 equal-block and 5,400 unequal-block checks, 35 adaptive updates across ten paths, 45 critical-window rows, and its other scalar, sphere and Gaussian diagnostics. The final candidate report and manifest hashes were checked again after replay and are unchanged.

## 11. Corrections during review

Two small presentation issues were identified in the draft and corrected by the author before freeze: the summary now specifies the shrinking epsilon choice used for its critical limit, and the primary-source introductory page range now begins at printed page 1. A floating-point stability issue in the author's fresh diagnostic helper was also identified and corrected before freeze: log(1-exp(-t)) uses the appropriate log1p/expm1 branch. These were not counterexamples to any mathematical claim.

No historical program was executed, no candidate source was modified by this reviewer, and no external write or publication was performed.

**Final disposition: accept the sharp projector/leverage bound, divisible-dimension attainment, adaptive Gaussian endpoint, and precisely qualified thin-deficit and sphere consequences. The selected new gate has no remaining proof gap.**
