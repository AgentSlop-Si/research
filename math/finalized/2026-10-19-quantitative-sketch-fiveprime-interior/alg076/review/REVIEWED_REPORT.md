# ALG-076: quantitative retained-rank obstruction for nonlinear Fourier decoders

19 October 2026. Scoped mathematical continuation candidate. Independent review is required. Owner ALG-076 remains TO RESEARCH at priority 42.

## Result and precise delta

For arbitrary measurable nonlinear decoding of at most k input-independent complex linear measurements of a standard complex Gaussian N-vector, the maximal probability of absolute Euclidean error at most a is exactly the Gamma(N-k,1) distribution function at a². A direct consequence is that constant relative Euclidean accuracy epsilon, with a success probability bounded away from zero for every continuous input, asymptotically requires

    k/N >= 1-epsilon²-o(1).

This also applies to an all-output unitary-Fourier infinity-norm guarantee epsilon ||x||₂/sqrt(N). For the original unaugmented v6 retained-sketch interface k<=RK, N=KM, this requires R/M>=1-epsilon²-o(1). Thus fixed meaningful relative fidelity already restores the ordinary charged evaluator's order-N-log-N FFT work, under its explicitly retained schedule.

This is an elementary application of classical conditional-Gaussian and centered-ball facts, not a historical-novelty claim. The previously accepted exact-recovery, unbiased-linear minimax, spectral-tail and median-covariance results are retained. In particular FUSION_THEOREMS.md §B2 already proves the measurable almost-everywhere exact-recovery statement; this packet does not claim to discover or redo that gate. The new local scope is the quantitative approximate-recovery consequence for nonlinear decoders. The relative-error bound below is necessary, not sufficient or claimed sharp. Only the absolute Gaussian small-ball bound is sharp.

## 1. Model and normalization

Let U be any fixed unitary N-by-N complex matrix, including the unitary DFT. A random seed omega is independent of the input. Given omega, the retained measurement is L_omega x for a complex-linear map L_omega of rank r_omega<=k<N, where k is an integer. A noninteger rank budget is first replaced by its floor. The entire output has the form

    y(omega,x)=g(omega,L_omega x),

with a jointly measurable success event. All decoder randomness is included in omega. There is no linearity, unbiasedness, continuity or homogeneity requirement on g. Its only information about x is the retained measurement. Invert U to write h=U* g without changing the error norm.

For the average-case test input, X has independent CN(0,1) coordinates: density pi^(-N) exp(-||x||₂²), real and imaginary variances each 1/2, and E|X_j|²=1. X and omega are independent. This Gaussian is a proof device. A purported guarantee for every x, or Lebesgue-almost-every x, must hold under this Gaussian as well.

For d>=1 define

    G_d(t) = 1-exp(-t) sum_(j=0)^(d-1) t^j/j!,  t>=0.

This is the distribution function of the sum of d independent exponential random variables with mean one. Define G_0(t)=1 for t>=0. Rank is complex rank throughout; the analogous real theorem uses chi-square laws and real rank.

## 2. Sharp absolute-error theorem

For every a>=0,

    P_(X,omega)( ||y(omega,X)-UX||₂ <= a )
       <= E_omega G_(N-r_omega)(a²)
       <= G_(N-k)(a²).                                      (1)

For every fixed rank-k L, equality is attained for every a by

    g(Lx)=U L^dagger Lx.

Here L^dagger L is the orthogonal projector onto (ker L)^perp. The equality assertion is an information-theoretic attainment statement, not a cheap algorithm for a supplied L or a Fourier transform. No pseudoinverse or U application is free.

### Proof

Fix an admissible seed. Put P=L^dagger L and Q=I-P. A unitary change of coordinates gives

    X=PX+QX,

where PX and QX are independent circular Gaussians on orthogonal subspaces, and QX is standard in complex dimension d=N-r. The observed LX determines PX exactly; conversely PX determines LX. This follows directly by factoring the density into orthogonal coordinates, so no nonsingular covariance of the possibly redundant observation vector is needed.

Conditional on LX, write the proposed h=U*g as h_P+h_Q. If ||h-X||₂<=a, orthogonality implies ||h_Q-QX||₂<=a. The conditional probability is therefore at most the mass of a radius-a ball translated by h_Q under the standard d-dimensional complex Gaussian.

Among all translates, that mass is maximal at the origin. One elementary proof writes the radial Gaussian density by its superlevel sets (layer cake). Each superlevel set is a centered Euclidean ball B_R. For any translated radius-a ball B(c,a),

    vol(B(c,a) intersect B_R)
       <= min(vol(B_a),vol(B_R))
       = vol(B_a intersect B_R).

Integrate this inequality over the level parameter. This is the radial-ball specialization of the classical centered-translate/Anderson inequality; no general rearrangement theorem is needed for this proof.

The centered Gaussian mass is G_d(a²), because each |Z_j|² is exponential with mean one, as follows by two-real-dimensional polar integration. The sum has gamma density t^(d-1)e^(-t)/(d-1)!, and integration gives the displayed formula for G_d. Thus the conditional bound is independent of LX. Integrating over LX and then omega proves the first inequality. Since increasing d adds an independent nonnegative exponential variable, G_d decreases in d; d>=N-k proves the second. The choice h=PX has error -QX and attains equality at fixed rank k. This proves (1).

The accompanying conditional squared-error identity is

    E[||h-X||₂² | LX] = (N-r)+||h-PX||₂²,

interpreted in the extended sense if the decoder is not square-integrable. Hence E||y-UX||₂² >= N-E r>=N-k. This is classical Gaussian estimation, not the earlier unbiased-random-linear N/k-1 minimax theorem; their estimator classes and normalizations differ.

At a=0, (1) yields the already accepted exact-recovery probability zero when k<N. Tonelli and the positive Gaussian density give the earlier Lebesgue-almost-every-input conclusion. This endpoint is inherited, not the new contribution.

## 3. A finite relative-error obstruction

Let 0<epsilon<1 and d=N-k. For every s>0,

    P_(X,omega)(||y-UX||₂ <= epsilon ||X||₂)
       <= min(1, G_d(epsilon² s)+1-G_N(s)).                  (2)

Indeed, on ||X||₂²<=s the relative-success event implies absolute error at most epsilon sqrt(s); the complement has probability 1-G_N(s). Equation (1) and the union bound prove (2). One may take the infimum over s. No independence of the error and ||X||₂ is assumed.

Consequently any guarantee

    P_omega(||y(omega,x)-Ux||₂ <= epsilon||x||₂) >= 1-delta

for Lebesgue-almost-every x necessarily satisfies

    1-delta <= inf_(s>0) min(1,G_d(epsilon²s)+1-G_N(s)).      (3)

There is also a useful population interpretation. Write p(x) for the seedwise relative-success probability. If the right side of (2), for one chosen s, is b, then for every eta>0,

    P_X(p(X)>=eta) <= b/eta.                               (4)

This is Markov's inequality for the nonnegative function p. It does not claim that every input is hard, nor that a finite nonzero b gives a Lebesgue-null exceptional set.

### Explicit exponential version

For Z_m~Gamma(m,1), its moment generating function is (1-lambda)^(-m), lambda<1. Exponential Markov gives

    P(Z_d<=a) <= exp(lambda a)/(1+lambda)^d, lambda>0;
    P(Z_N>=s) <= exp(-mu s)/(1-mu)^N, 0<mu<1.              (5)

Set h(u)=u-1-log u. If epsilon² Nt<d and t>1, optimize these scalar choices to obtain

    P(relative success)
      <= exp[-d h(epsilon² Nt/d)] + exp[-N h(t)].           (6)

The first term uses lambda=d/(epsilon²Nt)-1, the second mu=1-1/t. Both exponents are strictly negative because h(u)>0 for u!=1.

If k/N<=rho<1-epsilon², select any fixed 1<t<(1-rho)/epsilon². Then d/N>=1-rho. The first rate is uniformly positive: writing a=epsilon²t, d h(aN/d)=N[theta log(theta/a)-theta+a], theta=d/N, and the bracket increases for theta>a. Both terms decay exponentially in N. Thus for any sequence with success bounded below by a fixed positive number for almost every input,

    liminf_(N->infty) k_N/N >= 1-epsilon².                 (7)

Equivalently k_N/N>=1-epsilon²-o(1). This is a necessary asymptotic rank density. Neither a sharp finite relative-error minimax law nor sufficiency follows. In particular, the conditional mean need not maximize a relative-error success event whose radius itself depends on the unknown X; the sharpness of (1) must not be transferred to (2).

## 4. Fourier/sketch application and paid work

An all-bin guarantee

    ||y-Ux||_infinity <= alpha ||x||₂/sqrt(N)

implies relative Euclidean error <=alpha because ||v||₂<=sqrt(N)||v||_infinity. For fixed 0<alpha<1, (2)-(7) apply with epsilon=alpha. A per-bin coefficient alpha that grows with N or exceeds one does not give this meaningful relative guarantee; the accepted v6 polylogarithmic energy-scale bound is therefore not contradicted.

For the unaugmented v6 interface, the source FUSION_THEOREMS.md §B3 binds the output to R compressed K-spectra with input-independent seeds and N=KM. Thus k<=RK, including arbitrary nonlinear component medians. A uniform relative guarantee with fixed epsilon<1 and nonvanishing success requires

    R/M >= 1-epsilon²-o(1).                               (8)

If an independent d_head-dimensional exact linear head is also retained, replace the rank budget by min(N,d_head+RK). All data-dependent side information must be counted or the theorem is inapplicable. An invertible prefilter alone does not create information; its combined retained linear map still has to be the actual one.

For the specific dyadic evaluator in the preserved source, each row explicitly executes an ordinary K-point radix-2 transform, and the final decoding explicitly executes K ordinary M-point transforms. Its butterfly occurrences are

    (RK/2) log2 K + (N/2) log2 M
      = (N/2)[(R/M) log2 K+log2 M].                       (9)

For fixed epsilon<1, (8) implies R/M>=c>0 eventually. Consequently (9)>=min(c,1) N log2(N)/2, using KM=N. This remains true for K=1 or M=1 with the zero logarithm interpreted literally. Its actual full row scans/gathers cost Omega(RN) as well. These are counts of the stipulated evaluator's executed stages, not a lower bound inferred from an O-expression, not a proof that every butterfly multiplication is nontrivial, and not a lower bound for unrestricted Fourier circuits. Shared/fused schedules, other information models, input classes, or changed evaluators need their own analysis.

## 5. Exact finite certificate

Take N=1024, K=16, M=64, R=31. Then k=496, d=528. At epsilon=1/2 choose s=1280. In (5), use lambda=13/20 and mu=1/5. This gives

    b <= exp(208)/(33/20)^528 + exp(-256)*(5/4)^1024
      < 12/10^13 = 1.2e-12.                              (10)

The final strict inequality is checked with exact rational arithmetic in checks.py. Taylor partial sums with a geometric remainder bound enclose each exponential; neither floating Gaussian samples nor a numerical gamma library certifies it. In particular, every such decoder has Gaussian-average relative-half-error success below 1.2e-12; a 99% guarantee for all continuous inputs is impossible in this retained-information model. Equation (4) also bounds the Gaussian measure of inputs enjoying seedwise success at least 99% by b/(99/100).

The script additionally verifies projector identities for rational measurement matrices, gamma-polynomial derivative and monotonicity identities, finite examples, and model-boundary controls. These support the finite arithmetic and transcription only. The all-N statements are proved above.

## 6. Source and prior-art attribution

The exact local source bytes and hashes are in SOURCE_BINDINGS.json. FUSION_THEOREMS.md §§A-B supplies the existing theorem/model boundary; FREQUENCY_AUDIT.md corroborates its v5/v6 formula and cost mapping. They are user-supplied research source material, not a new replay of their historical experiments.

The centered-translate mechanism is classical: T. W. Anderson, *The integral of a symmetric unimodal function over a symmetric convex set and some probability inequalities*, Proceedings of the AMS 6(2), 170-176 (1955), DOI https://doi.org/10.1090/S0002-9939-1955-0069229-1. The original AMS PDF request returned HTTP 403 in this pass, so this packet does not claim to have reread that original article. Its bibliographic attribution is supported by the checked record; the radial-ball special case needed here is proved in full above. No broad missing-source recovery was undertaken.

An accessible primary research article was also checked: S. Dereich and M. A. Lifshits, *Probabilities of randomly centered small balls and quantization in Banach spaces*, Annals of Probability 33(4), 1397-1421 (2005), DOI 10.1214/009117905000000161, author-deposited reprint https://arxiv.org/pdf/math/0402220#page=4. Its Remark 2.2 explicitly uses Anderson's inequality to bound shifted Gaussian-ball mass by centered-ball mass. This directly credits the classical centered-ball ingredient; its infinite-dimensional quantization theorem is not asserted to be a model-matched Fourier evaluator or the exact finite-rank statement here.

For an accessible author-hosted statement of the Gaussian conditioning mechanism, Joel Tropp's *Probability Theory & Computational Mathematics* (Caltech CMS/ACM 117, Fall 2024, typeset January 23, 2025), Corollary 21.40, Example 21.45 and Theorem 21.47, gives independence and conditional expectation including a pseudoinverse for singular observation covariance: https://tropp.caltech.edu/notes/Tro24-Probability-Theory-LN.pdf#page=339. These are expository primary-author notes, not a historical-priority source. The complete source-independent derivation above avoids reliance on either unread passages or an external implementation.

The combined bound is recorded as a standard probability consequence newly mapped to this catalogue interface. No claim is made that its formula, method or corollaries are historically new. Broader owner-level prior-art comparison remains open.

## 7. Boundaries and disposition

- Input-independent fixed linear sketches with independent seed randomness only. Input-dependent/adaptive measurements, uncounted side information, or original-input access during decoding are not covered.
- Continuous complex ambient input. A finite or bounded-integer domain can be injectively encoded by a rank-one map, so no finite-domain impossibility follows.
- Complex rank and real rank differ. For real inputs the realified map is the relevant map; one complex scalar can encode two real coordinates.
- No bit-cost or roundoff theorem. A measurable rounding/postprocessing of the same exact measurements cannot beat (1); a finite-word implementation whose intermediate rounding is not a function of the stipulated exact retained map needs a new information model. No stable implementation is certified.
- No contradiction to exact recovery on lower-dimensional sparse classes, to loose per-bin energy-scale approximation, or to the original v5/v6 variance and tail theorems.
- No universal FFT lower bound, novel discovery, numerical production result, or full owner closure.

Recommendation: after independent acceptance, mark only ALG-076's quantitative fixed-linear-retention/relative-fidelity subgate complete, append this evidence, and retain TO RESEARCH/42. Preserve the original source comparison, sharper median covariance, changed information models, numerical/bit implementation and historical-priority questions. Do not redispatch the already proved almost-everywhere exact-recovery gate as new.
