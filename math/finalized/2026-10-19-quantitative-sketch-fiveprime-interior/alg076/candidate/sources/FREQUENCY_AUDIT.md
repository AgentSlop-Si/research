# Independent audit of the frequency-shift and predecode-median sketches

9 October 2026. No uploaded Python was imported or run. All executed checks in this directory were independently authored.

## Bottom line

The v5 algebra and variance identity are correct. The v6 change in median placement is real: its repeated work no longer includes the short transforms, and its stated arbitrary-input, all-output, polylogarithmic energy-scale approximation follows in the algebraic arithmetic model. Its locally Fourier-sparse exact-recovery theorem is also correct. These statements do not give exact arbitrary-input FFTs, a bounded-word implementation, floating-point stability, or a practical timing win.

The useful additions established here are:

1. The v5 row is an unbiased scaled orthogonal projection followed by the DFT. It exactly attains a universal rank-constrained linear-estimator minimax MSE bound.
2. If the retained measurements have rank below N, arbitrary measurable nonlinear postprocessing cannot yield positive exact-recovery probability on almost every continuous complex input. This rigorously closes a quantifier gap left by a seedwise kernel argument.
3. Least-squares periodic means, rather than the earlier L1-optimal periodic medians, give the right cheap residual head for an L2 guarantee. The same head composes with the residual-certified Green bridge, paying its source and target errors explicitly.
4. The same v6 algorithm has a spectral-tail-sensitive theorem interpolating between its dense approximation and sparse exactness cases; no additional top-entry computation is required by the algorithm.
5. Nonlinear local medians do not have diagonal cross-column covariance. An exhaustive exact counterexample prevents an unjustified independence-based removal of the short-decoder loss.

See FUSION_THEOREMS.md for the proofs and exact scope.

## 1. Algebra and moments checked

Write N=KM, use the unitary negative-sign DFT U, and let A be the K-point column transforms. The column modulation gives

    Z[s] = sum_u conjugate(xi_u) A_u[s+q_u],
    Ahat_t[p] = xi_t Z[p-q_t].

The target term is exactly A_t[p]. Fourth-root orthogonality gives unbiasedness, including conditional on all shifts. The local variance is

    E |Ahat_t[p]-A_t[p]|² = (||x||²-E_t)/K.

For the v5 decoded row, the only surviving ordered-pair phase product in its complex squared error is the identical pair. The reversed pair vanishes because E xi²=0. Uniform differences q_u-q_t then give

    E |Xhat_m-(Ux)_m|² = (M-1)||x||²/N

for every m. Summing yields total MSE (M-1)||x||². For balanced buckets with c columns per bucket, the same argument replaces M-1 by c-1. Its rank is N/c. At c=1 it is the ordinary exact factorization.

In v6 the short decoder runs once after local medians. Its infinity-norm bound is the triangle inequality for the unitary M-point row, followed by

    sum_t sqrt(E-E_t) <= sqrt(M(M-1)E).

This is where the additional sqrt(M) relative to v5 enters. No independence of the median errors is assumed or available in general.

## 2. Median theorem and constants verified against a primary source

Larsen, Pagh, and Tětek, “CountSketches, Feature Hashing and the Median of Three,” Theorem 5, states the general tq-th moment bound with binomial coefficient C_t=binom(2t-1,t). Taking q=2 gives exactly the theorem invoked by both checkpoints. The theorem is about error from the one-row mean, not the median's mean, and does not require an unbiased median. Primary source: https://arxiv.org/pdf/2102.02193, Theorem 5 on PDF pages 4 and 6.

Here is a self-contained proof of the needed case. For real z_1,...,z_(2s-1) and their median m, at least s values have absolute value at least |m| on the appropriate side of zero. Consequently

    |m|^(2s) <= sum_{S: |S|=s} product_{j in S} |z_j|².

Center the samples at their common mean and take expectations. Independence makes each product equal to the s-th power of the second moment. Thus

    E |median(Y)-E Y_1|^(2s) <= binom(2s-1,s) Var(Y_1)^s.

The checkpoints' separate real/imaginary Markov bounds and union over 2N components are therefore valid with their displayed constants. The exact v6 factor is

    beta = sqrt(2) (2N binom(2s-1,s)/delta)^(1/(2s)) sqrt(M(M-1)/N).

With probability at least 1-delta, the output error is at most beta ||x||₂. The T_h tail theorem below uses a shared complex-good event and can avoid the extra factor 2 inside the failure count.

## 3. Heavy-tail obstruction checked

For one nonzero local Fourier atom and p equal to its frequency, each other column collides independently with probability 1/K. Conditional on the source's fourth-root phase, the remaining phases are independent proper unit-modulus variables; deterministic output twiddles do not change the relevant second and fourth moments. The common source phase also leaves this distribution unchanged.

For C collisions,

    E |sum_(j=1)^C zeta_j|⁴ = 2C²-C.

Averaging C~Bin(M-1,1/K) gives exactly

    E |error|² = (M-1)/(MK),
    E |error|⁴ = [(M-1)/K+2(M-1)(M-2)/K²]/M²,
    kurtosis = K/(M-1)+2-2/(M-1).

Thus no universal one-row subgaussian estimate at the variance scale is possible. This rules out that specific route; it is not a lower bound against other estimators or robust aggregation.

## 4. Cost and parameter audit

For v6, with R=2s-1,

    T = O(R[N+(N/M) log(N/M)] + N log M),
    S = O(N+R[N/M+M]).

The retained random spectra require RK entries, and shifts/phases require RM entries. Per-coordinate median selection takes O(R); a p-slice uses O(RM) temporary entries. A comparison-sort implementation would incur an additional log R and must not be substituted silently for linear selection. All N outputs and RN gathers are charged.

For powers of two, let 1<=h(N)=o(log log N), M a power of two within a constant factor of log N/h, and

    delta = min(1/2, N^(-a)), a>=0,
    s = max(1, ceil(log(2N/delta)/(2 epsilon log log N))).

For sufficiently large N, the amplification factor is at most 2(log N)^epsilon because binom(2s-1,s)<=2^(2s-1). This concrete choice, unlike an unspecified Theta constant, guarantees the advertised exponent. It yields

    error = O((log N)^(1+epsilon)/h * ||x||₂/sqrt(N)),
    time = O(((1+a)/epsilon)(h/log log N)N log N + N log log N)
         = o(N log N),
    storage = O(N).

Corrections/clarifications to the supplied text:

- v6 sets delta=N^(-a) for a>=0. At a=0 that is delta=1 and the claimed success probability is vacuous. The min(1/2,N^(-a)) choice above fixes the endpoint without changing asymptotics.
- A stated s=Theta(...) needs a sufficiently large hidden constant for the precise exponent epsilon; the explicit schedule above resolves this.
- The v6 sparse corollary's expression “Mq” appears to use q as an undefined substitute for h_0. Its underlying formula and conclusion are correct.
- v5's condition t>1+a alone only implies polynomial decay if M grows sufficiently slowly; in the intended sub-FFT regimes M=N^{o(1)}, it is valid. For unrestricted M=N^b, one instead needs t>(1+a)/(1-b), with b<1.
- v5 contains a harmless corrupted closing delimiter in its displayed slower-runtime formula.
- The FFT costs assume compatible fast transforms for the selected factors and available exact roots. The clean dyadic corollaries satisfy that condition. The work does not establish bit complexity, random-bit charging, numerical stability, or optimized wall-clock performance.

## 5. Sparse exactness and its scope

If each local spectrum has at most h_0 nonzeros, a target is collision-free with probability at least 1-rho, rho=(M-1)h_0/K. A majority of collision-free rows forces both component medians to equal the target. Thus

    P[any output differs algebraically] <= N binom(2s-1,s) rho^s.

This is valid even when the written bound exceeds one (then it is only uninformative). Equality observed up to numerical roundoff in a floating-point test is evidence about the implementation, not a literal exact-arithmetic certificate.

The class can be larger than constant h_0. If M=Theta(log N), h_0<=N^b/(log N)^2 for fixed b<1, and s>(a+1)/(1-b) is a fixed integer, the failure is at most N^(-a) eventually. The arithmetic runtime is O(N log log N). This is a direct corollary, not a novelty claim and not a result for arbitrary dense spectra.

## 6. Independent execution results

Run `python independent_tests.py` and `python covariance_probe.py` from this directory. The latter now includes both the simple M=3 example and a dyadic M=4 example.

- Four exhaustive one-row seed enumerations: (K,M)=(2,2),(2,3),(3,3),(2,4), totaling 728 gauge-reduced states.
- The largest direct-factorization / fast-sketch discrepancy was 1.36e-14.
- Per-output variance discrepancies were below 4.5e-15; local variance discrepancies below 1.1e-14.
- The unbiased operator, projection identity, trace identity, Frobenius norm, and scalar risk matrix (M-1)I were checked independently.
- Exact rational enumeration checked three tone fourth moments; kurtoses were 2, 4, and 35/2.
- Exact finite-distribution enumeration checked the median-moment inequality for 1,3,5,7 samples.
- The new spectral-tail row bound was exhaustively checked at (K,M)=(8,2),(16,2), retaining the top one entry per column and alpha=1/8. Over 32 and 64 reduced seeds, maximum bad-row fractions were 0.125 and 0.0625, below bounds 0.25 and 0.1875; tail-variance identities agreed within 1.4e-15.
- A 12-by-32 stacked measurement map had rank 12 and a nonzero null vector with measurement norm 3.4e-16 and Fourier norm 1. Its role is only to illustrate the exact proof, not prove it numerically.
- Periodic projection orthogonality, Pythagorean optimality, and removal of local p=0 were independently checked.
- An N=32 Green-fusion example had target infinity norm 3.31045, below 73/18; observed error 5.38809 was below its conservative proved bound 85.11421. This arbitrary example is not evidence of a universal Green improvement.
- In 12 local-sparse trials at K=64,M=4,R=5,h_0=1, 9 recovered to roundoff and 3 did not. The per-trial theoretical failure upper bound is 0.263672. These small tests are not used as proof or as a speed benchmark.

The separate standard-library-only `python exact_covariance_witness.py` verifies the covariance counterexample entirely with integer pairs and rational output: K=1,M=3,R=3,A=(1,2,3), reduced to 16 equally likely phase states per row and 4096 ordered triples. Each median error has mean zero, but

    E[e_0 conjugate(e_1)] = 45/512.

At the dyadic point K=1,M=4,R=3,A=(1,2,3,4), 262144 ordered triples give a largest off-diagonal covariance 0.223480224609375. Nonzero covariance also occurs for K=2,M=3. These invalidate a general diagonal-covariance assertion without claiming that no sharper decoder analysis is possible.

## 7. Prior-art and provenance boundary

The CountSketch ingredients and median theorem are established prior work. The factorization-compatible compressed measurement and schedule are the supplied project's candidate contribution. This audit checks correctness and derives consequences; it does not establish research novelty. The new lemmas here are elementary linear algebra/probability consequences, and should likewise not be advertised as novel without a literature review.

Inputs reviewed: v5 RESEARCH.md, v6 RESEARCH.md, the earlier periodic median baseline, and the residual-certified Green bridge PROOF.md. The Green bridge's independent constants and source/target residual-certificate machinery are taken as previously audited ingredients; this directory rechecks their composition with the new energy-based decoder rather than re-proving every finite-word implementation bound.
