# Independent audit of the all-length fused finite-precision lift, v11

9 October 2026. Scope: mathematical proof review, implementation-as-text audit, and independently authored finite controls. No uploaded program was executed or imported. This supplement does not modify the uploaded bundle or a master package.

## Verdict

The exact-arithmetic Clenshaw streaming, Neumann fusion identity, deterministic fusion bound, and shared-state covariance argument are sound in their stated dyadic/block regime. The production row paths genuinely avoid rank-times-full-length storage for fixed local halfwidth H. The rank-R decoder scans remain, so the claimed total O(RN) arithmetic order is unchanged.

The finite-precision conclusion is **conditional but under-specified for the fused program**. Its printed full-row contract does not by itself certify a decoder receiving separately formed, rounded summaries. A decoder-on-summaries contract, summable coefficient envelope, explicit summary/Clenshaw ledger, and charged coefficient generator repair the implication. These additions can preserve the leading precision and total arithmetic order; they do not certify the uploaded NumPy/SciPy/BLAS implementation.

Three useful extensions are established here:

1. For H=0, the total deterministic center error is at most (tau_R+Delta)||x||2, with Delta=pi(M-1)/Q. This removes the R factor from the fusion bias. Its variance bound can simultaneously retain (M/N)(1+tau_R)^2||x||2^2.
2. Negative local channels are redundant, leaving H+1 independent channels. Fixed L-row summary-only exact recovery requires L(H+1)>=M whenever a complete input block is present. Increasing expansion rank R does not relax that information barrier.
3. A frozen-block rational-Taylor variant obtains the same O(M/Q) bias with one unweighted channel and no Bessel oracle. It still requires R decoder scans and its own summary-interface precision contract.

All statements concern randomized approximation unless explicitly labelled exact algebra. None supplies an exact, all-output, arbitrary-input transform faster than N log N.

## 1. Sources and reproducibility boundary

Reviewed as inert text: RESEARCH.md, CHAIN_CHECKPOINT_2026-10-09_v11.md, prototype.py, unit_step_core.py, and saved result/manifest data. The prior all-length audit, charged rational-Taylor extension, and exact Fourier bridges were used as mathematical background.

`SOURCE_CHECKSUMS.json` independently hashes all 16 top-level source files, including the supplied manifest. `SOURCE_MANIFEST_VERIFICATION.json` checks the 15 listed manifest entries. `independent_v11_checks.py` is fresh code authored for this audit. Its dependencies are installed NumPy and mpmath; it neither imports source-bundle modules nor runs their tests, benchmarks, or entry points.

Classical identity references, checked against the official NIST DLMF:

- Neumann addition: https://dlmf.nist.gov/10.23.E2 . The nearby qualification explicitly removes the generic argument restriction for integer-order J.
- Bessel generating function/Jacobi–Anger expansions: https://dlmf.nist.gov/10.12 .
- Bessel integral representation: https://dlmf.nist.gov/10.9.E1 .

The proofs and bounds below are derived independently; the cited classical ingredients are not novelty claims.

## 2. Streaming, decoder, and storage

Write Q=KM, N<=Q<2N, M^2<=Q, with Q and M dyadic. For each output, exact integers give j_k=round(kQ/N) and theta_k=kQ/N-j_k in [-1/2,1/2]. The intended N=1 case is the identity and should be handled separately.

For coefficients a_r(k), the backward Clenshaw recurrence b_r=a_r+2(2theta_k)b_{r+1}-b_{r+2}, followed by a_0+(2theta_k)b_1-b_2, evaluates the desired Chebyshev sum. Two recurrence vectors persist between ranks; temporaries, current coefficients, and current decoder output add a constant number of vectors. This is O(N) storage, not literally a two-vector peak allocation.

The selected decoder retains a Q-sized cycle/phase plan and performs a Q-sized forcing/scan for each rank. Its returned N selected entries match the exact full decoder. Selection saves unneeded output construction; it does not remove the Q scan. Our independent closed-form recurrence was compared with direct U_Q C* for every odd a and every beta at (Q,M)=(8,2),(16,4),(32,4), totaling 672 states. Maximum discrepancy was 1.7592043482197232e-14.

Source inspection confirms that the production streamed and fused functions do not retain an R-by-N Chebyshev table. The separate v10-style reference deliberately still does. With H fixed, channel/factor arrays, the local phase/input matrix, decoder workspaces, and Clenshaw vectors total O(Q+(H+1)K+(H+1)M+N)=O(N). An unrestricted H cannot be dropped from this accounting. The algebra needs a constant number of passes; the phrase “consume the input once” describes channel formation, not all preceding phase/base allocation and input conversion.

Static limitations: N=1 is not handled by the actual end-to-end source path because choose_dyadic_block rejects Q=1; the mathematical fix is trivial. Int64 modular phase products and index storage are demonstration-size implementations, not arbitrary-size integer arithmetic. The core itself acknowledges moderate-size products. These do not invalidate the mathematical approximation theorem, but they limit the saved executable claim.

## 3. Neumann fusion and the original error bound

For n=bM+t, put z_b=pi b/K and delta_t=pi t/Q. Integer-order Neumann addition gives

    J_r(z_b+delta_t)=sum_{h in Z} J_{r-h}(z_b)J_h(delta_t).

Its absolute convergence follows directly from the factorial Bessel majorants on bounded real arguments. Thus retained channels

    G_h[b]=sum_t S[b,t]x[bM+t]J_h(delta_t)

produce the truncated weights exactly in exact arithmetic. Using |J_m(z)|<=1 and the tail A_H(Delta) printed in v11 gives per-order error <=A_H and combined Chebyshev-kernel error <=(2R-1)A_H. The denominator in that tail is positive in the theorem regime. Consequently the stated deterministic center bound is valid.

Let C_omega be block compression, P_omega=C_omega* C_omega, and A_omega=U_Q P_omega. For each final output k, all rank terms with the same omega combine into one weighted input x_n W_k(n). The lifted error is therefore one dyadic covariance problem, with variance at most

    (M/N) max_n |W_k(n)|^2 ||x||2^2.

This validates the source's shared-state argument. Different random states per expansion order would not justify this particular recombination. Correlations between different outputs do not obstruct the coordinatewise concentration plus union bound used later.

Our six exhaustive small-state covariance controls form full covariance matrices, rather than comparing only seeded empirical variances. Their maximum eigenvalue-to-bound ratio, using the actual kernel envelope, was 0.9999999999987084. These finite floating-point controls support the proof; they do not replace it.

## 4. Sharper H=0 theorem

Set w=2theta and

    p_R(z,w)=J_0(z)+2 sum_{r=1}^{R-1}(-i)^r J_r(z)T_r(w).

The one-channel kernel is exactly

    W_0(z,delta,w)=J_0(delta)p_R(z,w).

The Jacobi–Anger tail gives |p_R(z,w)-exp(-izw)|<=tau_R for 0<=z<=pi and |w|<=1. Also |J_0(delta)|<=1. The Bessel integral representation says J_0(delta) is the average of exp(i delta cos phi). Therefore

    |J_0(delta)-exp(-i delta w)|
      <= |delta| average_phi |cos phi+w|
      <= |delta|.

For the last inequality, the average is a convex function of w on [-1,1], and its value at either endpoint is 1. Combining these estimates yields the uniform bound

    |W_0(z,delta,w)-exp(-i(z+delta)w)|<=tau_R+|delta|.

Hence the stronger center theorem is

    ||Xbar^(0)-U_N x||infinity <= (tau_R+Delta)||x||2,
    Delta=pi(M-1)/Q.

For M=Theta(log N), the extra bias is O(log N/N), independent of R. This is negligible at every polynomial target N^-alpha with alpha<1, including the source's alpha<1/2 regime. The original bound remains valid but is needlessly rank-dependent.

Moreover |W_0|<=1+tau_R. Thus one can simultaneously use

    E|Xhat_k^(0)-Xbar_k^(0)|^2
       <= (M/N)(1+tau_R)^2||x||2^2.

Delta enters the deterministic bias; it need not inflate the statistical radius. For the source's robust aggregation convention, replace its total allowance by

    [tau_R+Delta+(5/sqrt(2))g(1+tau_R)sqrt(M/N)]||x||2,

with the same exact-arithmetic failure analysis. A numerical implementation must separately enlarge the radius for its proven rounding allowance and account for grid classifications.

The independent checks include 15 H=0 kernel cases; the largest actual-error/(tau_R+Delta) ratio was 0.9881921563344086. This near-one ratio also illustrates that an O(Delta) term is substantive; increasing R alone does not recover the missing within-block phase.

## 5. Remove redundant channels; clarify the exactness barrier

Integer-order parity gives J_-h(delta)=(-1)^h J_h(delta), so

    G_-h=(-1)^h G_h.

Consequently exact retained synthesis can be written with only H+1 channels:

    d_r=J_r(z)G_0
        +sum_{h=1}^H [J_{r-h}(z)+(-1)^h J_{r+h}(z)]G_h.

This halves the nonzero-h channel storage and input-side work constants. It does not alter the O(RN) total order. The source computes both signs independently and therefore does not exploit this redundancy.

More importantly, for any fixed random state, every rank's summaries and every decoded output factor through the same (H+1)K-dimensional channel map. On an occupied block containing n_b input coordinates, its rank is at most min(n_b,H+1). Thus the total row-map rank is at most

    sum_b min(n_b,H+1) <= (H+1)K,

independently of R. Our six numerical rank/factorization checks attain the occupancy-adjusted caps in the tested cases.

For L fixed states, a complete M-coordinate block is observed through at most L(H+1) scalar linear summaries. If L(H+1)<M, that block has a nonzero common kernel vector v. Inputs v and -v produce identical zero summaries and have equal norms, but their Fourier transforms differ. No decoder receiving only those summaries, the fixed states, and the exact input norm can be correct for every input. Therefore a necessary condition for uniform exact recovery is

    L(H+1)>=M,

whenever a full block is present. The weaker global condition L(H+1)K>=N also follows. Extra independent input information would need to be included in the information budget.

This is a fixed-seed, uniform-all-input obstruction. It does not assert that each fixed input fails under every random seed, and it does not contradict the randomized per-input approximation theorem. It is not an unrestricted Fourier complexity lower bound. Separately, the previous exact residual-kernel rank N/gcd(N,Q) still prevents simply declaring a short separated near-grid correction exact.

## 6. Finite precision: what is missing and how to repair it

`FP_CONTRACT_REVIEW.md` contains the detailed sufficient theorem and proof. The essential distinction is:

- Full-row contract: accuracy of a numerical composite compression-plus-decoder on supplied input y.
- Needed fused contract: accuracy of the decoder on every independently supplied, represented summary vector d.

In exact arithmetic C C*=M I and D=U_Q C*. A sufficient interface is

    ||Dhat(d)-D(d)||infinity <= epsilon_D||d||2,
    epsilon_D=C_D u log(Q)sqrt(Q).

It follows from an appropriate short-FFT error bound, certified phase/normalizer preparation, and balanced scans: the gauged forcing has l2 norm at most 2||d||2 and l1 norm at most 2sqrt(Q)||d||2. These hypotheses must be proved for an actual implementation.

The printed full-row bound alone does not isolate Dhat. If computed compression were exact, the minimal-norm lift C*d/M would transfer it. The actual rounded compression is not such a supplied exact lift. An input supported only at each block's t=0 position does give an exact simple lift for the source, but its norm is ||d||2 rather than ||d||2/sqrt(M). That argument gives only a weaker error bound with an extra sqrt(M), corresponding to another half log2(log N) mantissa bits when M=Theta(log N). The requested sharper coefficient needs the actual summary-interface analysis.

A second correction is the order of norms. A pointwise supremum of a sum of Bessel magnitudes cannot in general be moved outside a sum of l2 norms. The source's numerical constant can be justified by summing uniform factorial majorants instead. For H=0, define m_0=1 and m_r=exp(pi^2/8)(pi/2)^r/r! for r>=1. Then sum_r w_r m_r<27.17, with w_0=1 and w_r=2. For H>0, use the shifted convolution majorant given in the companion review; its bound remains independent of R for fixed H.

With certified channel errors, coefficient errors, synthesis rounding, in-range rounded Chebyshev nodes, final scaling, and a smallness condition uR^2<<1, the companion ledger proves

    eta_fp=O([u log Q sqrt(MQ)+uM(log M+R^2+1)]||x||2)

for fixed H. The first term dominates in the stated shrinking-error regime. Thus the advertised sufficient u=O(g/(N log N)) and leading mantissa-bit order can survive the repair. The conclusion is not established merely by evaluating the source's proposed bound function.

Source-specific gaps are material: matrix multiplication for channels does not prescribe pairwise reductions; summary synthesis uses a separate sum; coefficients/roots are not certified; summary dtype conversion needs a budget; the bound function has no H parameter; complex64 storage experiments still use higher-precision FFT/Bessel work; and exponent range, integer exactness, and robust-aggregation classifications need treatment. No fixed-binary32 or fixed-binary64 theorem is certified here.

## 7. Charge every coefficient and precision operation

The source requests (2H+1)M local Bessel values and (2H+1)RK block Bessel values per row. The displayed O(Q+RK) input-side count is a count of applications/traversals with prepared coefficients or unit-cost special-function calls. It is not a complete arbitrary-precision setup count.

A constructive repair uses

    J_m(z)=(z/2)^m/m! sum_{j>=0}(-z^2/4)^j m!/[j!(m+j)!].

For bounded |z|<=4, a relative-to-factorial tail is bounded by exp(4)4^L/(L!)^2. Thus L=O((b+1)/log(b+2)) terms suffice at b-bit target accuracy, with explicitly charged leading factors, argument preparation, recurrence, sums, and guard precision. A rational pi approximation can be prepared by the prior Machin-series construction. Working with guard bits and adequate exponent range is part of this variant; ordinary library calls do not establish it.

For b=Theta(log N), R=Theta(log N/log log N), and K=Theta(N/log N), the charged block series work is

    O(RKL)=O(N log N/(log log N)^2)=o(RN).

A stored R-by-K coefficient table occupies O(RK)=O(N) in this regime. Alternatively, recomputing leading factors while streaming costs the same asymptotic order because R and L have comparable order. Therefore total O(RN) arithmetic work remains achievable after coefficient charging, but the narrower O(Q+RK) claim does not include that construction's coefficient preparation. All R short transforms and Q scans remain charged as well.

These are arithmetic-operation bounds with precision specified. Exact integer/rational operations, b-bit multiplication, input/output representation, root construction, and guard precision cannot be treated as unit-cost in a bit-complexity theorem. No improved exact or bit-complexity exponent follows.

## 8. Simpler one-channel frozen-block Taylor variant

The Bessel machinery is unnecessary if the aim is only one local input pass with O(M/Q) deterministic bias. For n=bM+t, approximate the residual exp(-2pi i theta n/Q) by exp(-2pi i theta b/K). Their difference is at most Delta. Form one unweighted channel

    G[b]=sum_t S[b,t]x[bM+t].

Let rho be a certified rational approximation to pi, |rho-pi|<=eta, and use

    p_R(b/K,theta)=sum_{r=0}^{R-1}(-2i rho theta)^r (b/K)^r/r!.

The real-phase Taylor remainder and pi replacement give

    |p_R-exp(-2pi i theta b/K)|<=tau,
    tau=eta+|rho|^R/R!.

The required rank-r summaries are simply d_r[b]=(b/K)^r G[b]. Thus one pass costs O(Q), their streamed preparation O(RK), and the R decoder/output passes still O(RN). Rational coefficient/pi setup is charged as in the previous extension. The deterministic error is at most (Delta+tau)||x||2; since |p_R|<=1+tau, the same-state variance is at most (M/N)(1+tau)^2||x||2^2. Fixed-row aggregation and O(N) storage follow in the usual regime.

This is an exact-arithmetic/conditional-precision variant, not a production implementation or a claim that the old full-row numerical contract automatically covers it. It shares the same one-channel information-rank barrier and R-decoder bottleneck. Four independent numerical controls verify its displayed kernel inequalities.

## 9. Independent checks and final boundary

The saved run passes:

- bounded-argument Bessel reconstruction against 70-digit mpmath: maximum absolute error 1.1102230246251565e-16;
- exact nearest-grid identities at 513 lengths;
- 672 exhaustive selected-decoder states: maximum discrepancy 1.7592043482197232e-14;
- Clenshaw versus direct cosine-definition summation: maximum discrepancy 4.167405171867302e-15;
- 45 Neumann/truncated/true-kernel cases, including 15 sharper H=0 checks;
- 6 exhaustive fused covariance cases, with full eigenvalue tests;
- 6 reduced-channel rank/factorization cases;
- 4 frozen-block/Taylor controls.

`CHECK_RESULTS.json` contains the complete numerical results; `CHECK_RUN.log` is the actual run output; `SHA256SUMS.txt` seals the deliverables. Rerun from this directory with `OPENBLAS_NUM_THREADS=1 python independent_v11_checks.py`. Dependencies are listed in `requirements.txt`.

The useful conclusion is a better-qualified approximation theorem, a sharper H=0 bias/variance statement, a smaller independent-channel count, and an explicit interface/setup repair. The work does not certify the uploaded full floating-point implementation, remove the rank-R scans, establish novelty, or solve the exact arbitrary-input all-output Fourier goal.
