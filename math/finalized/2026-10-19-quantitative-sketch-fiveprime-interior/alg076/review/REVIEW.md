# ALG-076 independent probability-bound review

## Verdict: scoped PASS, no mathematical repair required

Reviewed on 19 October 2026. This verdict applies to candidate REPORT.md SHA-256 `aeb0c2129ea4edfd78db0a14e3b2746e88b0737d467ec5ca933556d81eb1216c` and candidate MANIFEST.json SHA-256 `35106552ca46ffa2684814a47aa79ef76a03182d20fd3470bdd4a7df637717ca`. All twelve manifest entries and the four local source bindings match their recorded hashes and byte lengths. The manifest contains every candidate file except itself.

The sharp absolute-error bound, its finite relative-error consequence, the necessary asymptotic rank density, and their stated application to the source-bound unaugmented v6 evaluator are correct within the stated information model. The candidate distinguishes inherited exact recovery from the quantitative approximate-recovery extension and explicitly disclaims historical novelty for the classical ingredients and standard consequences. Accept only this quantitative fixed-linear-retention subgate. ALG-076 remains TO RESEARCH, priority 42.

## Proof and quantifier audit

1. **Normalization.** The density pi^(-N) exp(-||x||^2) gives independent real and imaginary parts of variance 1/2. Therefore each squared complex coordinate is Exp(1), and the squared norm in complex deficiency d is Gamma(d,1). There is no missing factor of two. Complex rank must be used for arbitrary complex inputs; the separate realification warning is correct.

2. **Input independence and randomization.** Fixing a seed freezes both the measurement map and all decoder randomness. Independence from X preserves the same isotropic Gaussian input under this conditioning. Splitting into the row space and kernel makes PX and QX independent, and LX and PX determine each other. The argument needs no full-row-rank observation matrix. For random L, conditional identities in the fixed-seed proof are understood as conditional on the seed as well as the observation.

3. **Arbitrary measurable nonlinear output.** At fixed seed and observation, the proposed kernel component is a fixed center. Orthogonal projection of the error can only reduce its norm, so success is contained in a translated kernel-ball event. The layer-cake argument is valid: two concentric balls attain the smaller ball's volume as intersection, while every translated pair has at most that volume. Integrating radial density superlevel sets proves the required centered-ball inequality directly, without relying on an unread general theorem.

4. **Rank variation and sharpness.** For each seed the bound is G_(N-r)(a^2). Integrating over seeds gives the expected CDF. Adding independent positive exponentials makes G_d decrease with d, proving the rank-cap bound G_(N-k)(a^2). At fixed rank k, h=PX attains it. This is an information-theoretic achievement, with no free pseudoinverse or Fourier computation. The squared-error identity is likewise correct. Integer k and 0<=k<N are the relevant sharp-CDF parameters; d=0 is the stated trivial extension.

5. **Relative threshold.** The radius epsilon||X|| is dependent on X and generally on the residual. The candidate correctly avoids conditioning on this random radius: intersect success with ||X||^2<=s, use the absolute bound at epsilon sqrt(s), and add the upper energy tail. Thus (2) and its infimum consequence are valid without an independence assumption. Markov's inequality gives the stated population interpretation. Neither finite positive b nor a pointwise seedwise kernel argument produces an almost-everywhere zero statement for approximate recovery.

6. **Asymptotics.** Fix epsilon in (0,1) and a uniform success lower bound eta>0 independent of N, holding for Lebesgue-almost-every input at each N. Positive Gaussian density transfers that lower bound to the Gaussian average. If liminf(k_N/N)<1-epsilon^2, select a subsequence with k_N/N<=rho<1-epsilon^2 and a fixed 1<t<(1-rho)/epsilon^2. Both Chernoff rates are then bounded strictly away from zero on the subsequence, contradicting eta. This establishes the claimed liminf and equivalent o(1) lower bound. It asserts necessity only, and does not cover an epsilon approaching one or success tending to zero without a new rate analysis.

7. **Inherited exact-recovery endpoint.** At a=0 and deficient rank the CDF vanishes. Tonelli and positive Gaussian density give the already established almost-everywhere inputwise conclusion. Source FUSION_THEOREMS.md B2 already states and proves it. The candidate does not present this endpoint as new.

## Source-bound Fourier and evaluator audit

FUSION_THEOREMS.md B3 explicitly states that the unaugmented v6 output uses only R retained length-K compressed spectra and input-independent seeds. Their concatenated linear map has rank at most RK; arbitrary nonlinear medians cannot increase retained information. FREQUENCY_AUDIT.md sections 1 and 4 agree with this interface, including the single final short-transform stage and the charged RN gathers. The original mapping is therefore supported by the retained controlling sources. This review does not claim to replay historical implementation code or timing experiments.

The all-output infinity error alpha||x||/sqrt(N) implies Euclidean error at most alpha||x||, so fixed alpha<1 is exactly within the quantitative obstruction. The source's growing polylogarithmic coefficient is outside that fixed-fidelity hypothesis, and its accepted approximate and sparse results are not contradicted.

With N=KM, the necessary rank density implies R/M>=1-epsilon^2-o(1) when RK<N; if RK>=N, this row-ratio conclusion is already automatic. The displayed radix-2 butterfly count equals (N/2)[(R/M)log2 K+log2 M]. An eventual R/M>=c>0 implies at least min(c,1)N log2 N/2 executed butterflies. This is a lower count for the stipulated ordinary transforms, not an inference from a big-O upper bound and not an unrestricted FFT or circuit lower bound. Degenerate factors K=1 and M=1 cause no problem. Any retained head or other input-dependent side information requires a different counted rank budget, as the candidate states.

## Independently executed exact controls

The reviewer wrote and ran independent_controls.py without reading, importing, or executing the candidate checks.py. It uses only Python standard-library integer and rational arithmetic. No Monte Carlo or floating special functions certify the result.

- A degree-40 Taylor enclosure of e, with an explicit positive geometric remainder, gives the candidate Chernoff expression in the strict rational enclosure:
  - lower: 0.0000000000011388484971242879556794902059
  - upper: 0.0000000000011388484971242879556794902060
- Its upper endpoint is strictly below 0.0000000000012.
- An independent direct integer-shape Gamma/Poisson-tail calculation at the same s=1280 gives the stronger union-bound enclosure:
  - lower: 0.0000000000000557338491251927817922005605
  - upper: 0.0000000000000557338491251927817922005606
- The controls also check Gamma polynomial identities through degree 64; exact realification and projector identities for the genuinely complex map L=[1,i]; and 345 dyadic butterfly-count instances through N=2^14.
- Negative model controls verify that a nonzero constant estimate can beat the conditional mean for a relative-error event even at rank zero, and that a single scalar can encode a finite binary input domain injectively. These substantiate the candidate's limitations, rather than expanding its theorem.

The direct-Gamma improvement is optional supporting arithmetic, not a requested change to the conservative certified headline. Finite checks support the all-N proof audit; they do not replace it.

## Classical attribution and access limits

The classical centered-translate attribution to Anderson (1955) is appropriate. The original AMS PDF and DOI were not accessible in this review's web route. Its journal issue record supports the bibliographic attribution; this review does not claim to have read the original article.

Dereich and Lifshits, Annals of Probability 33(4), 1397-1421 (2005), author-deposited reprint https://arxiv.org/pdf/math/0402220, was accessible. Remark 2.2 on PDF page 4 explicitly invokes Anderson's inequality for the centered-versus-shifted Gaussian-ball comparison; the same comparison is displayed again in the page-6 proof. This supports the stated ingredient, not a matched finite-rank Fourier complexity theorem or priority clearance.

Tropp's author-hosted Fall 2024 notes at https://tropp.caltech.edu/notes/Tro24-Probability-Theory-LN.pdf were accessible. Corollary 21.40, Example 21.45, and Theorem 21.47 verify Gaussian independence and the conditional-mean formula with a pseudoinverse for singular observation covariance. The theorem is on printed page 324 / PDF page 339. These are correctly described as expository notes rather than the historical origin of Gaussian conditioning.

The packet appropriately characterizes its contribution as a source-specific mapping of classical consequences. Broader literature priority, adaptive information, numerical stability, word complexity, unrestricted runtime, and full owner closure remain unproved.

## Final disposition

SCOPED PASS. No required repairs. Preserve every model and novelty limitation above. Candidate source files were not modified, no external state was changed, and no delegated work was spawned. CANDIDATE_HASH_CHECK.json binds the exact reviewed packet; REVIEW_MANIFEST.json binds this review and its independent controls.
