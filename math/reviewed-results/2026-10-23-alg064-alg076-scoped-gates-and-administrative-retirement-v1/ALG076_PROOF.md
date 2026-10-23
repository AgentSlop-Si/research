# ALG-076: transcript-adaptive Gaussian information gate

23 October 2026 UTC. Candidate for independent review. No external writes, table edits, owner closure, novelty claim, or historical-code execution.

## 1. Exact source and the one obligation resolved

At repository main `ea78d5c259d99c2907bc822fcc4b33f2a405593d`, the accepted predecessor is:

- [19 October quantitative fixed-linear report](https://github.com/AgentSlop-Si/research/blob/ea78d5c259d99c2907bc822fcc4b33f2a405593d/math/finalized/2026-10-19-quantitative-sketch-fiveprime-interior/alg076/candidate/REPORT.md), especially sections 1, 3, 4 and 7.
- [Original FUSION_THEOREMS.md](https://github.com/AgentSlop-Si/research/blob/ea78d5c259d99c2907bc822fcc4b33f2a405593d/math/finalized/2026-10-19-quantitative-sketch-fiveprime-interior/alg076/candidate/sources/FUSION_THEOREMS.md), B2-B4. B2 already proves fixed-linear almost-everywhere exact-recovery failure and is not a new result here.
- Fresh read on 23 October of [Research overview row 67]([private native worksheet locator omitted; not a scientific source]): ALG-076 is TO RESEARCH, priority 42. P explicitly retains changed/adaptive information models with all side information counted. Q restricts the predecessor to fixed linear retention.

The selected stopping condition is a rigorous extension or counterexample for sequential, transcript-adaptive, noiseless complex-linear queries, an independent seed, a hard total queried-rank budget, and an almost surely finite transcript-based stopping rule. This report supplies the extension, including the zero-innovation and adaptive-stopping cases. It does not solve every changed-information model or the other ALG-076 obligations.

## 2. Model: information acquired, not final storage width

Fix N>=1 and a unitary U on C^N. Let X~CN(0,I_N): its density is pi^(-N) exp(-||x||_2^2), and E|X_i|^2=1. All random bits used for query selection, stopping and decoding are included in a seed W independent of X, valued in a standard Borel space. All maps below are Borel measurable. These assumptions supply ordinary regular conditional probability kernels; arbitrary nonmeasurable encodings are not admitted.

Start with F_0=sigma(W). Before query j choose a finite vector a_j in C^N as an F_(j-1)-measurable function of the seed and earlier observations. Receive the exact scalar

    Z_j = a_j^* X,       F_j = sigma(W,Z_1,...,Z_j).

Thus the query vectors, any chosen query indices, intermediate comparisons and other bookkeeping are already measurable from F_j. There is no raw-input-dependent choice of a_j, no separately observed input norm, and no input-dependent side channel outside these queries. An affine offset known from the transcript can be subtracted and adds no information.

A stopping time T taking values in {0,1,...} is almost surely finite and satisfies {T=j} in F_j. The stopped transcript is (W,T,Z_1,...,Z_T), with its stopped sigma-field F_T. Stopping decisions must be functions of the seed and data already observed. Algorithms that never terminate on a set of positive Gaussian-seed measure are outside this terminal-output statement. One may define zero queries after stopping, purely for the proof.

Let

    r_j = dim_C span{a_1,...,a_j},       r_T<=k<N a.s.

The last inequality is a HARD pathwise bound on all input information acquired, not an expected rank, a nominal number of sketches, or the rank of what happens to remain stored at the end. Arbitrarily many redundant queries are allowed if T is finite a.s.; they do not increase r. A k-query cap implies this rank cap but is not required. The output Y is any F_T-measurable C^N-valued vector. Nonlinear, biased, discontinuous and randomized decoders are allowed. No additional access to X during decoding is allowed.

## 3. Main theorem

For d>=1 and t>=0 put

    G_d(t) = 1-exp(-t) sum_(l=0)^(d-1) t^l/l!,
    G_0(t) = 1.

For every a>=0,

    P(||Y-UX||_2<=a)
       <= E G_(N-r_T)(a^2)
       <= G_(N-k)(a^2).                                  (1)

For EACH admissible measurement/stopping strategy, the first bound is attained simultaneously for all a by the posterior-mean output

    Y = U m_T,      m_T=E[X|F_T].                         (2)

Consequently adaptive queries do not improve the optimal absolute-error success probability under a hard rank-k budget: a fixed rank-k orthogonal measurement and (2) already attain G_(N-k)(a^2). Attainment is information-theoretic; forming m_T and applying U are not free computational primitives.

Also, in the extended-expectation sense,

    E||Y-UX||_2^2 = N-E r_T + E||U^*Y-m_T||_2^2
                  >= N-E r_T >= N-k.                     (3)

The hard-rank probability bound in (1) cannot in general replace k by E r_T. Section 7 supplies an exact counterexample.

### 3.1 Predictable conditional-Gaussian induction

Define m_0=0 and Q_0=I. Inductively, given F_(j-1), put

    v=Q_(j-1)a_j,       lambda=a_j^*Q_(j-1)a_j=||v||_2^2.

If lambda>0 set

    m_j=m_(j-1)+v[Z_j-a_j^*m_(j-1)]/lambda,
    Q_j=Q_(j-1)-vv^*/lambda.                             (4)

If lambda=0 set m_j=m_(j-1), Q_j=Q_(j-1). Formula (4) is measurable, with the zero branch explicitly defined. For every j, almost surely,

    Law(X|F_j) = CN(m_j,Q_j),                            (5)
    Q_j is the orthogonal projector onto span(a_1,...,a_j)^perp,
    rank Q_j=N-r_j,       m_j=(I-Q_j)X,       Q_j m_j=0.   (6)

Here the expression (I-Q_j)X in (6) is an identity, not a new input read: (4) constructs m_j from the transcript.

Proof. The statement holds at j=0 because W is independent of X. Conditional on a previous history where (5) holds, the chosen a_j is fixed. Write X=m+E, with E a centered proper complex Gaussian of covariance Q. The innovation eta=a_j^*E has variance lambda.

If lambda=0, eta=0 almost surely, so Z_j=a_j^*m is already determined. The query adds no information; its row lies in the existing row span because Q is its orthogonal-complement projector.

If lambda>0, the pair eta and E-v eta/lambda is jointly proper complex Gaussian. Their cross covariance is zero, since E[E conjugate(eta)]=Qa_j=v. Hence they are independent, and the latter has covariance Q-vv^*/lambda. Conditioning on eta gives (4)-(5). The projector update removes exactly the unit direction v/sqrt(lambda) from the old residual space, proving the row-span and rank assertions. Because Z_j=a_j^*X, induction in (4) gives m_j=(I-Q_j)X and Q_jm_j=0. This also proves that all already observed row equations remain satisfied.

This argument uses the regular Gaussian kernel at the ACTUAL history. It does not condition on a random final measurement matrix as if that matrix had been chosen independently of X. Averaging over adaptive matrix choices first and using a fixed-matrix independence assertion would not justify (5).

### 3.2 Why stopping adds no hidden constraint

For each finite j, (5) holds outside a null set. Their countable union is still null. For any bounded Borel test function phi and any A in F_T,

    E[1_A phi(X)]
      = sum_(j>=0) E[1_(A intersect {T=j}) phi(X)]
      = sum_(j>=0) E[1_(A intersect {T=j}) K_j(phi)],

where K_j is the Gaussian kernel CN(m_j,Q_j). The second equality is valid because A intersect {T=j} is in F_j. Since T<infinity a.s., the sum is E[1_A K_T(phi)]. Thus

    Law(X|F_T)=CN(m_T,Q_T).                              (7)

Any stop event depending on an unobserved part of X would violate the stopping-time hypothesis; the argument does not apply to it. Arbitrary unbounded but a.s.-finite running time introduces no optional-stopping integrability premise here: this is a countable conditional-kernel identity for bounded test functions, not an optional-stopping martingale theorem.

### 3.3 Conditional success and sharpness

Condition on F_T. Its residual space has dimension d=N-r_T, and (7) says X=m_T+E, where E is standard proper complex Gaussian on that space. Put h=U^*Y and split h-m_T into components parallel and orthogonal to that residual space. A nonzero component outside the residual space only consumes part of the error radius. Inside the residual space, the probability of a radius-a ball centered at an arbitrary displacement is no greater than the probability of the centered ball.

For completeness, this last radial-ball fact needs no unread external theorem: write the Gaussian density as an integral of indicators of centered balls. At each level, the intersection of a translated radius-a ball with a centered radius-R ball has volume at most min(vol B_a,vol B_R), attained by concentric balls. Integration proves the claim. The centered squared residual norm is a sum of d independent mean-one exponentials, hence has CDF G_d. For d=0 the posterior is a point and the same upper bound G_0=1 holds. Therefore the conditional success probability is at most G_d(a^2); h=m_T attains it. Integrate and use that G_d decreases in integer d to prove (1)-(2). The same posterior decomposition gives (3) by conditional expectation, with no square-integrability assumption on the decoder needed for the lower bound.

## 4. Relative-error consequences, separately identified

For 0<epsilon<1 and every deterministic s>0, the exact new adaptive theorem implies

    P(||Y-UX||_2<=epsilon||X||_2)
      <= min(1, G_(N-k)(epsilon^2 s)+1-G_N(s)).          (8)

Indeed on ||X||_2^2<=s, relative success implies absolute error at most epsilon sqrt(s); apply (1), then add the probability of the complement. No independence between error and input norm is assumed. Taking the infimum over s is valid. This is the SAME necessary finite relative bound as the predecessor, now justified for this larger information model. It is not a sharp finite relative-error law and is not claimed sufficient; posterior-mean optimality for absolute error does not imply posterior-mean optimality for a random, input-relative radius.

For d=N-k, t>1 and epsilon^2 Nt<d, the usual gamma Chernoff bounds give

    P(relative success)
      <= exp[-d h(epsilon^2 Nt/d)]+exp[-N h(t)],
    h(u)=u-1-log u.                                      (9)

If k/N<=rho<1-epsilon^2, choose fixed 1<t<(1-rho)/epsilon^2. Both terms decay exponentially in N. Consequently a sequence of these algorithms with success bounded below by a positive N-independent constant for Lebesgue-almost-every continuous input necessarily has

    liminf k_N/N >= 1-epsilon^2.                         (10)

Integrating an inputwise guarantee against the strictly positive Gaussian density justifies this application. The analogous all-bin unitary-DFT guarantee ||Y-Ux||_infinity<=epsilon||x||_2/sqrt(N) implies the Euclidean one and obeys the same necessary bound. This is not a finite-domain or sparse-class impossibility.

The predecessor's N=1024,k=496,epsilon=1/2 certificate <1.2e-12 applies unchanged to the present HARD-rank model via (8). It is an inherited exact numerical certificate, not a new experiment or a claimed replay here.

## 5. Precisely what transfers to adaptive v6-style rows

Suppose a changed v6-style procedure chooses each row seed solely from W and previous compressed-row observations, each row supplies K complex-linear observations, and it uses at most R rows on every path. An additional d_head-dimensional exact linear head is also counted. Then

    r_T <= min(N,d_head+RK).

This is an upper bound on actual total queried rank, including failed/discarded queries and all information used for adaptive selection. It is not enough that only RK scalars remain stored. The theorem requires a lower bound on this budget if uniform meaningful relative fidelity is requested.

With no head and N=KM, (10) again gives R/M>=1-epsilon^2-o(1). If, ADDITIONALLY, the changed procedure really executes the same R ordinary K-point dyadic FFT stages and K ordinary M-point output FFTs as the source, its stipulated butterfly occurrence count is

    (RK/2)log2 K+(N/2)log2 M
      = (N/2)[(R/M)log2 K+log2 M].                       (11)

This is Omega(N log N) for fixed epsilon<1; the explicit scans/gathers are also paid. Formula (11) counts that fixed executed schedule only. If R is merely an upper cap and the actual number of rows varies, (11) with the cap R is NOT an execution lower bound; a separate pathwise/average cost analysis is required. The theorem supplies no universal computational lower bound, no restriction on an unrestricted Fourier circuit that has read all N coordinates, and no no-adaptivity theorem for every information model.

## 6. Classical antecedents and limited attribution

This is a source-bound specialization of classical Gaussian information-based complexity, not a new mechanism or a historical novelty claim.

- G. W. Wasilkowski, *Optimal algorithms for linear problems with Gaussian measures*, Rocky Mountain Journal of Mathematics 16(4), 727-749 (1986), DOI [10.1216/rmj-1986-16-4-727](https://doi.org/10.1216/rmj-1986-16-4-727), is an identified direct predecessor on adaptive versus nonadaptive Gaussian linear information in average/probabilistic settings. The [author-institution publication record and abstract](https://scholars.uky.edu/en/publications/optimal-algorithms-for-linear-problems-with-gaussian-measures/) were checked and explicitly describe the adaptive/nonadaptive conclusion in both settings; the primary publisher full text was inaccessible in this pass. No exact theorem-number, full-hypothesis or cost-interface equivalence is certified here from an unverified reproduction.
- J. B. Kadane, G. W. Wasilkowski and H. Wozniakowski, *On adaption with noisy information*, Journal of Complexity 4(4), 257-276 (1988), DOI [10.1016/0885-064X(88)90010-6](https://www.sciencedirect.com/science/article/pii/0885064X88900106). The publisher's indexed abstract expressly identifies noiseless Gaussian nonadaptivity as known and states related noisy/orthogonal results. That abstract is also available in the [author-institution record](https://scholars.uky.edu/en/publications/on-adaption-with-noisy-information/). Only abstract-level attribution was verified; the full article request returned HTTP 403. Its noise and sample-size variants are not silently imported.
- The predecessor already credits Anderson's centered-translate inequality. Its elementary radial-ball specialization is proved in section 3.3 above. The additional substantive step here is the predictable conditional-kernel induction and stopping rule, also given in full rather than outsourced to an inaccessible source.

These records are enough to avoid any original-mechanism claim. They do not supply a complete worldwide-priority audit. No third-party paper body is redistributed in this packet.

## 7. Sharp model boundaries and exact counterexamples

### Expected rank is not a hard rank budget

Take N=3. An independent fair bit chooses either no observations (r=0) or the first two coordinates (r=2); use the posterior mean. Then E r=1, but at a^2=1 the success probability is

    (G_3(1)+G_1(1))/2 = 1-(7/4)e^(-1),

whereas substituting E r into the hard-budget formula gives

    G_2(1)=1-2e^(-1).

The true probability is greater by e^(-1)/4>0. The exact correct mixture formula (1) holds, and the actual hard bound is k=2. Thus (3)'s expectation-of-rank MSE identity cannot be substituted into (1)'s probability bound. The rational coefficient identity is checked by the new verifier.

### Raw-input-dependent query directions can encode the whole vector

For N>=2 and x!=0 choose a(x)=x/||x||_2, receive z=a(x)^*x=||x||_2, and retain both the chosen vector and scalar. Then za(x)=x exactly after a nominal single query. At x=0 choose any fixed unit direction. This violates transcript predictability at the first query because a(x) reads the unknown x. The direction carries uncounted input information. It is not a counterexample to (1); it proves why an arbitrary data-dependent final matrix of rank one cannot replace the stated sequential model.

### Other exclusions

- Every direct coordinate read is a linear query; a decoder that rereads the entire input has acquired rank N, even if it keeps little memory.
- An energy oracle, support oracle or raw-input-derived stopping event needs a separate information model. Calling it one scalar is not permission to treat it as one complex-linear measurement.
- Complex-linear observations of a complex Gaussian use complex rank. Arbitrary real-linear observations require realification and the corresponding chi-square residual law; one must not reuse k unchanged for real inputs.
- Noisy observations, changed priors, finite/discrete domains, lower-dimensional signal classes, nonterminating protocols and arbitrary nonlinear measurements are not covered.
- Postprocessing the full admissible transcript by rounding cannot improve the information-theoretic ceiling. But finite-word arithmetic that introduces additional raw-input-dependent reads or branching must itself be modeled; no roundoff or bit-complexity guarantee is supplied.
- No exact finite relative-error optimum, robust-aggregation theorem, practical executor, fast preparation, source migration, historical-priority clearance, or parent-owner closure follows.

## 8. Validation and disposition

The new standard-library-only `verify_adaptive_updates.py` uses exact Gaussian-rational arithmetic. It checks (4)-(6) on deliberately adaptive finite rational transcripts, including nonorthogonal complex directions, zero queries, repeated rows, more queries than rank, and history-based stopping. It independently checks Hermitian idempotence, residual dimension, all observed row equations, orthogonality and exact reconstruction. These finite algebra controls support the update transcription; the conditional law, stopping and all-N theorem are proved above, not inferred from finite tests or Gaussian samples.

All 72 adaptive rational transcripts passed, comprising 1,071 queries, 252 positive innovations and 819 zero innovations. Every transcript has more queries than acquired rank.

The verifier also checks the exact expected-rank counterexample and explicitly demonstrates the forbidden raw-input-direction encoding. No historical research program is imported, executed or compiled. Source text is inert evidence only.

Recommended after separate independent acceptance: mark ONLY the transcript-adaptive noiseless complex-linear hard-total-rank subgate complete. Do not redispatch this same Gaussian adaptive-information argument as new original research. Preserve ALG-076 TO RESEARCH/42 and all source/proof histories. Remaining sharper covariance/robust or norm-adapted aggregation, genuinely different information models, numerical/bit implementation, production and broader primary-source attribution retain their original scope. This is a classical-method gate closure, zero claimed new mechanisms, zero owner retirements.
