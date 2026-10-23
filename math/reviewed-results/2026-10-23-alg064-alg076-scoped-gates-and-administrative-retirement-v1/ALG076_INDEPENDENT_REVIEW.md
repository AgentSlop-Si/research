# Independent review: ALG-076 adaptive Gaussian information gate

Review date: 23 October 2026 UTC. Verdict: **SCOPED_PASS**. No mathematical repair is required within the exact scope below. This review neither edits external records nor closes the owner.

## 1. Frozen object and independent evidence

The reviewed candidate is `alg076_adaptive_information_20261023_v1/REPORT.md`, SHA-256 `ad5f4907b6da9824a1cac1a590986cb74cc539d579a9f81c6628a3f4d5a02a10`. All ten entries in the candidate's SHA256SUMS were independently recomputed and matched. No candidate or historical scientific script was imported, compiled, or executed. The candidate's reported 72-transcript experiment is not the basis of this verdict.

The reviewer independently fetched the following exact files at repository commit `ea78d5c259d99c2907bc822fcc4b33f2a405593d` and compared their returned UTF-8 bytes against the candidate's copies:

- [Original FUSION_THEOREMS.md](https://github.com/AgentSlop-Si/research/blob/ea78d5c259d99c2907bc822fcc4b33f2a405593d/math/finalized/2026-10-19-quantitative-sketch-fiveprime-interior/alg076/candidate/sources/FUSION_THEOREMS.md), SHA-256 `0e029e7ee61acd4b2ec9404259face106eb660e166338c286cf72296b2c9e2ed`, exact match. Sections B2-B4 were read, together with the other source sections for normalization and the retained-information boundary.
- [Accepted fixed-linear predecessor report](https://github.com/AgentSlop-Si/research/blob/ea78d5c259d99c2907bc822fcc4b33f2a405593d/math/finalized/2026-10-19-quantitative-sketch-fiveprime-interior/alg076/candidate/REPORT.md), SHA-256 `aeb0c2129ea4edfd78db0a14e3b2746e88b0737d467ec5ca933556d81eb1216c`, exact match; the full report was read.

A fresh native Sheets metadata read verified the visible `Research overview` tab, sheetId 1731260011, 337 rows by 17 columns. A subsequent bounded read of [A67:Q67]([private native worksheet locator omitted; not a scientific source]) independently confirmed owner ALG-076, status TO RESEARCH, priority 42, the previously accepted fixed-linear result, and the still-open adaptive-information obligation. Exact read responses are preserved under `sources/`. The earlier exact-recovery statement in FUSION B2 is inherited, not newly discovered here.

## 2. Precisely accepted information model

The input is a standard proper complex Gaussian X in C^N, with density pi^(-N) exp(-||x||^2); each complex coordinate has second moment one, not two. The target U is fixed unitary. A standard-Borel seed W independent of X includes all random choices. Every finite query vector a_j must be measurable from W and preceding answers. An answer is exactly a_j^*X, and the terminal output is a measurable function of the stopped transcript alone. The stopping rule is a stopping time, finite almost surely. The integer hard rank budget k<N bounds the complex span of **all acquired** query vectors, not expected rank, final storage, or the number of nominal sketch objects. A noninteger stated budget is interpreted as its floor; table text should use an integer rank budget explicitly.

This permits nonorthogonal adaptive vectors, arbitrary finite redundant/zero queries, randomized strategies, nonlinear/discontinuous/biased decoders, T=0, unbounded finite T, and infinite expected running time. It excludes raw-input-dependent directions or stop events, unobserved input norms/support or other side channels, input rereads by the decoder, general nonlinear measurements, noise, non-Gaussian priors, and nontermination with positive probability.

## 3. Independent mathematical verification

### Conditional law, including degenerate queries

At time zero independence gives the conditional kernel CN(0,I) even after the complete independent seed is revealed. Suppose the current kernel is CN(m,Q), with Q the projector onto the common nullspace of the observed row equations. Conditional on the actual previous transcript, a is a fixed vector, not an independent random final matrix. Write v=Qa and lambda=a^*Qa=||v||^2.

When lambda=0, a lies in the old observed span and the new answer equals a^*m almost surely. Thus this answer cannot refine the conditional distribution. When lambda>0, let eta=a^*(X-m) and R=(X-m)-v eta/lambda. The joint vector (R,eta) is proper complex Gaussian. Its cross covariance is v-v lambda/lambda=0 and its cross pseudo-covariance is also zero by properness; therefore R and eta are conditionally independent. The conditional mean after observing eta is m+v eta/lambda and covariance is Q-vv^*/lambda.

Because Q is a projector, the latter matrix is a Hermitian projector deleting one direction from its range. It annihilates all old rows and the new row, has rank reduced by one, and produces m=(I-Q)X with Qm=0. These facts establish the induction at every deterministic finite step. The zero branch is measurable and prevents a division-by-zero hole. Gaussian regular conditional kernels on the stated standard-Borel transcript supply the needed measurable versions. The proof does not illegitimately condition on the final adaptive matrix as though it were input independent.

### Stopping does not inspect the residual

For any event A in the stopped sigma-field, A intersect {T=j} belongs to F_j. Apply the deterministic-step conditional kernel identity to that event, then sum over j. Absolute convergence holds for bounded test functions, since {T=j} are disjoint and cover the probability space up to the null nontermination set. The resulting kernel is CN(m_T,Q_T). This uses no optional-stopping integrability theorem. Finite expected T is not needed.

A concrete stress case is N>=2, first query X_1, then only zero rows, with T=1+ceil(exp(|X_1|^2)). This is finite almost surely but has infinite expectation because |X_1|^2 is exponential with mean one. Its stopped transcript contains exactly the same input information as X_1. The untouched N-1 coordinates remain standard independent Gaussians, consistent with the theorem. Stopping on an unobserved coordinate would instead be an inadmissible information leak.

### Sharp probability and squared error

Conditioned on the stopped transcript, the unknown residual has d=N-r_T standard complex coordinates on the known residual subspace. Passing from Y to U^*Y preserves Euclidean distance. Displacement outside the residual space spends radius without improving success. Within that space, radial layer-cake integration shows that no translated ball has greater Gaussian mass than the concentric ball: at each density level, overlap is bounded by the smaller of the two ball volumes, achieved concentrically. Thus conditional success at radius a is at most G_d(a^2), where the residual energy is Gamma(d,1). For d=0 the posterior is a point and G_0=1 is correct, including at a=0.

The single decoder Y=Um_T attains the first bound for every radius simultaneously. Integrating yields P(success)<=E G_(N-r_T)(a^2). Since G_d decreases with integer d, the hard rank condition gives the further ceiling G_(N-k)(a^2), attained by a fixed rank-k orthogonal observation scheme. This is information-theoretic optimality, not a cost-free algorithm for producing m_T or applying U.

The conditional squared-error expectation is d+||U^*Y-m_T||^2. Integration gives exactly the candidate's extended-expectation identity and MSE lower bound. Finite-valued measurable decoders need not be globally square integrable; conditioning first avoids an unjustified infinity-minus-infinity expansion. Also ||m_T||<=||X|| pathwise, so the stated conditional mean itself is integrable.

### Hard rank, expected rank, and storage are different

The N=3 independent coin mixture between rank zero and rank two has mean rank one and success 1-(7/4)e^(-1) at a^2=1. This exceeds G_2(1)=1-2e^(-1) by e^(-1)/4. The candidate's counterexample is exact. Expected rank is valid in the MSE identity but cannot replace k in the probability ceiling.

Similarly, reading every coordinate and retaining only a small final representation still acquires rank N. Directions chosen from the raw unknown vector can encode it: for x nonzero, a=x/||x|| and z=a^*x imply za=x. That construction violates predictability and is not a rank-one counterexample within the accepted model. Independent seed is also essential: a seed containing X would already disclose everything at T=0.

### Relative error is a necessary consequence, not a sharp optimum

For deterministic s>0, relative success on {||X||^2<=s} implies absolute success at epsilon sqrt(s). The other event has probability 1-G_N(s). The union bound proves the displayed finite relative ceiling, without independence between reconstruction error and input energy. Gamma Chernoff bounds then give the candidate's exponents. If k_N/N were below 1-epsilon^2 by a fixed gap along a subsequence, choosing one fixed t>1 inside that gap would force exponentially vanishing success along that subsequence, contradicting a positive N-independent lower bound for almost every continuous input. Integrating such an inputwise guarantee against the everywhere-positive Gaussian density justifies the implication.

The all-bin unitary-DFT bound at scale epsilon||x||/sqrt(N) implies the Euclidean relative event by the norm inequality. This does not address finite or sparse input classes, a growing error scale, or nonunitary normalization without rescaling.

There is a simple independent reason not to advertise posterior-mean relative optimality. Take N=1, no observations, epsilon=1/2. The posterior-mean output 0 has relative success probability zero. The fixed output 1 succeeds whenever |1-X|<=|X|/2, equivalently |X-4/3|<=2/3, a disk with strictly positive Gaussian mass. Absolute-error optimality therefore does not transfer to input-relative radii. The candidate correctly declines that transfer.

## 4. Full charged-cost audit and its limitation

For the restricted adaptive row interface, each row returns K complex-linear answers, and a separately counted d_head-dimensional linear head contributes to the bound r_T<=min(N,d_head+RK). Discarded/failed rows still count. Without a head, N=KM and the rank-density necessity imply R/M>=1-epsilon^2-o(1) for a hard cap R compatible with the requested uniform fidelity.

That necessary cap is not itself an execution lower bound. The reviewed report expressly adds the condition that the changed method actually executes R ordinary K-point dyadic transforms and K ordinary M-point output transforms. Only under that condition is the butterfly occurrence count

    (RK/2) log2 K + (N/2) log2 M
    = (N/2)[(R/M) log2 K + log2 M].

For a fixed executed R with R/M>=c>0 eventually, this is at least min(c,1)N log2(N)/2. The unit-size K=1 or M=1 endpoints are valid. Full scans/gathers, any head formation, query selection, posterior update and final output formation are additional paid work, not free primitives. This is a schedule count, not a claim that every butterfly performs a nontrivial multiplication and not a universal Fourier-circuit lower bound.

The cap/execution distinction is substantive: with K=M=16 and cap R=16, the capped formula is 1,024 butterflies, but a path executing one row and the stipulated output transforms uses 544. The cap cannot prove the larger execution count. The independent controls check this witness and the report already warns against precisely this substitution. Variable-row expected/pathwise runtime needs its own analysis; no such general lower bound is accepted here.

The abstract linear-observation interface must also remain explicit when attaching physical full scans to it. If raw coordinate values or scan intermediates are available to the adaptive controller or decoder, they are additional acquired information, potentially rank N, and the deficient-rank hypothesis fails. A scan implementing an encapsulated linear query is not permission to use its internal raw values as uncharged adaptive side information. This is a scope condition, not an assertion that the theorem covers every low-storage implementation.

## 5. Fresh independent controls

The reviewer authored `independent_controls.py` from scratch, using only Python standard-library exact fractions. It neither imports nor reads the candidate's verifier. Its separate Gaussian-rational arithmetic checks adaptive recursive posterior updates against independently eliminated row rank and direct identities on 324 finite rational transcripts in dimensions one through six:

- 3,350 queries, including 604 positive innovations and 2,746 redundant/zero innovations;
- 30 time-zero stops and 92 history-dependent early stops;
- 28 full-rank boundary controls for the update and point-posterior case, not claims that k=N belongs to the k<N deficiency theorem;
- Hermitian symmetry, projector idempotence, trace/rank, all row equations, residual orthogonality, and exact reconstruction;
- 32 exact gamma derivative polynomial identities and the expected-rank counterexample;
- 400 exact dyadic butterfly identities and the cap-versus-execution witness.

The inherited N=1024,k=496,epsilon=1/2 certificate was independently checked without the author's exponential enclosure. A degree-48 rational Taylor enclosure of e gives an exact rational upper bound for exp(208)(20/33)^528 + exp(-256)(5/4)^1024 that is strictly below 12/10^13. Its decimal display is approximately 1.138848497124288e-12; the strict comparison is rational, not floating-point evidence.

These controls validate algebra and finite certificates. They do not prove conditional laws, all-N quantifiers, or arbitrary stopping by experimentation; the separate argument in section 3 is the reason those statements are accepted.

## 6. Attribution: verified abstracts, not full-paper theorem reads

The reviewer independently opened the [University of Kentucky record for Wasilkowski (1986)](https://scholars.uky.edu/en/publications/optimal-algorithms-for-linear-problems-with-gaussian-measures/). Its bibliographic record and abstract support classical Gaussian adaptive/nonadaptive antecedence in average and probabilistic settings. The DOI target was not accessible through the available retrieval tool.

The reviewer independently opened the [University of Kentucky record for Kadane, Wasilkowski and Wozniakowski (1988)](https://scholars.uky.edu/en/publications/on-adaption-with-noisy-information/). Its abstract describes noiseless Gaussian nonadaptivity as known and discusses additional noisy and fixed-sample variants. The publisher article request returned HTTP 403. No full paper body, exact theorem hypothesis, stopping-time formulation or cost-interface equivalence was verified from either article.

These are adequate antecedent acknowledgments for the candidate's explicit refusal to claim a new mechanism. They are not a complete primary-source theorem comparison or historical-priority audit. The self-contained proof is independently sufficient for this narrow mathematical acceptance; broader attribution obligations remain open. No third-party paper body is redistributed.

## 7. Disposition and safe table wording

Accept only the transcript-adaptive noiseless complex-linear information subgate with independent seed, almost-sure finite transcript stopping and a hard bound on all acquired complex rank. Preserve ALG-076 **TO RESEARCH / priority 42** and its old evidence/history.

Suggested concise result text: "The sharp absolute Gaussian bound P(||Y-UX||_2<=a)<=E G_(N-r_T)(a^2)<=G_(N-k)(a^2) extends to transcript-predictable noiseless complex-linear queries, independent seed, and a.s.-finite transcript stopping under a hard total acquired-rank budget k<N. Posterior mean attains the first bound; relative-error and stipulated-executed-schedule consequences remain necessary and qualified."

Do not close sharper covariance/robust/norm-adapted aggregation, genuinely other information models, finite-word/numerical stability and production implementation, complete primary theorem mapping, or historical priority. Do not present the fixed-linear exact-recovery endpoint as new research. Do not convert a query cap into actual executed work, a storage limit into acquired rank, an expected rank into the hard probability bound, or absolute sharpness into finite-relative sharpness. Zero new-mechanism claims and zero owner retirements are authorized by this review.
