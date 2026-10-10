# Charged rational-Taylor lift and conditional finite-precision theorem

9 October 2026. Independent extension of the v10 all-length construction. This proves a specified rational-Taylor implementation variant, conditional on the stated v9 row contract. It does not certify the uploaded Bessel/NumPy implementation. No uploaded source was executed or imported.

## Result and scope

The all-length lift does not need an exact Bessel-value oracle. Replace its residual-phase approximation by a bounded-phase Taylor polynomial with a certified rational approximation to pi. The coefficient setup is explicitly charged, the same-state covariance proof survives unchanged, and the numerical-error contribution has an explicit deterministic ledger.

For fixed target error the arithmetic cost remains O_epsilon(N); for polynomially shrinking error it remains O(N log N / log log N), with O(N) arithmetic storage and a fixed number of random rows. These are randomized, energy-relative approximation statements, not exact FFT or fixed-binary64 theorems. Root preparation, input representation, bit complexity, aggregation classification, and range handling remain part of the contract below.

## 1. Charged rational approximation to pi

For m >= 1 define exact rational sums

    A_m(q) = sum_{j=0}^{m-1} (-1)^j / [(2j+1) q^(2j+1)],
    rho_m = 16 A_m(5) - 4 A_m(239),
    eta_m = 16 / [(2m+1) 5^(2m+1)]
            + 4 / [(2m+1) 239^(2m+1)].

The alternating-series estimate and Machin's identity give

    |rho_m - pi| <= eta_m.

For completeness, if A=arctan(1/5), B=arctan(1/239), then tan(2A)=5/12, tan(4A)=120/119, and tan(4A-B)=1; the angle lies in (0,pi/2), so 4A-B=pi/4. Thus no transcendental evaluation is hidden in this preparation.

Generate each signed power by multiplication by -1/q^2, divide by the next odd integer, and accumulate. Compute the displayed error bound by rational recurrences too. There are O(m) exact rational arithmetic operations, and m=O(1+log(1/eta)) suffices for requested eta. The rational intervals themselves certify rho and its error; using m>=1 keeps 0<rho<4. This is an arithmetic-operation bound. Exact rational numerators/denominators grow, and their bit costs are not unit costs.

## 2. Lift, tail, and deterministic error

For N>=2, set Q=2^ceil(log2 N), so N<=Q<2N. The N=1 transform can be returned directly. Use exact integer nearest-grid indexing, for example ties upward:

    j_k = floor((2kQ+N)/(2N)),
    d_k = kQ-j_k N,
    theta_k = d_k/N,               |theta_k|<=1/2,
    s_n = n/Q,                    0<=s_n<1.

The j_k are distinct and lie in 0,...,Q-1. Let rho be the rational number above, with |rho-pi|<=eta, and set q=|rho|. Define

    b_r(theta)=(-2 i rho theta)^r/r!,
    p_R(s,theta)=sum_{r=0}^{R-1} b_r(theta) s^r,
    E_R=sum_{r=0}^{R-1} q^r/r! <= exp(q),
    tau_R=eta+q^R/R!.

Then, uniformly on this domain,

    |exp(-2 pi i s theta)-p_R(s,theta)| <= tau_R,
    |p_R(s,theta)| <= 1+tau_R.                         (1)

Indeed the pi-to-rho replacement costs at most 2 eta s |theta|<=eta. For real a=2 rho s theta, the integral Taylor remainder for exp(-ia) is

    (-ia)^R/(R-1)! integral_0^1 (1-t)^(R-1) exp(-ita) dt.

Its modulus is at most |a|^R/R!<=q^R/R!. Thus the initially proposed, looser tail eta+exp(q)q^R/R! is also valid, but unnecessary. The sharper bound uses rho real. General complex arguments would require an exponential factor.

Set y^(r)_n=x_n s_n^r for n<N, zero-padded to Q. The deterministic lift is

    Xbar_k = sqrt(Q/N) sum_{r<R} b_r(theta_k) [U_Q y^(r)]_{j_k}.

The exact Fourier kernel identity then gives

    ||Xbar-U_N x||_infinity <= tau_R ||x||_2.           (2)

This follows from a rowwise kernel error at most tau_R/sqrt(N) and Cauchy-Schwarz. For tau_R<=N^(-alpha), alpha>0 fixed, select eta<=N^(-alpha)/2 and q^R/R!<=N^(-alpha)/2. Stirling's formula yields an admissible R=(alpha+o(1))log N/log log N. The certified rank can be selected by the rational recurrence q^R/R! and rational comparison; no Lambert-W or logarithm oracle is needed.

## 3. Same-state covariance and charged arithmetic work

Let A_omega=U_Q P_omega be the exact v9 row, with the valid dyadic block size M, and reuse the same omega for every r in one lifted row. For fixed k,

    Xhat_k = sqrt(Q/N) [A_omega z^(k)]_{j_k},
    z^(k)_n=x_n p_R(s_n,theta_k).

Assuming the already established dyadic v9 covariance theorem,

    E Xhat_k = Xbar_k,
    E |Xhat_k-Xbar_k|^2
        <= (M/N)(1+tau_R)^2 ||x||_2^2.                (3)

No triangle inequality across R random errors, and no R factor in the variance, is needed. Independent states for the different expansion terms would invalidate this particular recombination proof.

Initialize a_n=1 and b_k=1. At each rank use y_n=x_n a_n, evaluate the row, gather at j_k, and accumulate b_k times the gathered result. Then update

    a_n <- a_n (n/Q),
    b_k <- b_k (-2 i rho theta_k)/(r+1).

The recurrence indices are adjusted after the r-th term so the next term has degree r+1. These are O(N) operations per rank; all weights, coefficient updates, row calls, gathers, and additions are charged. They store O(N) working values. Thus L independent lifted rows cost

    O(L R N + log(1/eta)) arithmetic operations,
    O(N) arithmetic storage for fixed-row aggregation,

plus the already charged v9 roots/normalizers and whatever bit cost their implementation model imposes. Recomputing the streamed weights for each row costs O(LRN), not additional storage. The three-grid majority acts on the final arbitrary-length outputs, not separately on each expansion term.

For fixed epsilon, choose eta<=epsilon/4 and a constant R with q^R/R!<=epsilon/4. The v10 three-row argument gives O_epsilon(N) arithmetic work and failure O((log N)^2/(epsilon^4 N)). For fixed a>=0, integer s>1+a, and L=2s-1, the v10 choice of g gives error O(sqrt(log N)N^[-1/2+(1+a)/(2s)]||x||_2), failure <=N^(-a), and O(N log N/log log N) work. The constant L dependence is explicit in the displayed work above. For nontrivial confidence at the endpoint a=0, use failure target c N^(-a), with fixed 0<c<1, and choose g=[2N binom(2s-1,s)/(c N^(-a))]^(1/(2s)). This changes only the g-dependent constant and gives success at least 1-c at a=0; the literal target N^0=1 would give only the vacuous success lower bound zero.

## 4. General deterministic numerical-error ledger

Write X=||x||_2, C=sqrt(Q/N), and B_r=q^r/r!. All comparisons below are to the same ideal shared-state row. For every r,k, assume:

1. Represented weighted inputs ytilde^(r) satisfy

       ||ytilde^(r)-y^(r)||_2 <= delta X,
       ||ytilde^(r)||_2 <= (1+delta) X.

   It suffices to have componentwise relative error <=delta in the complete product x_n s_n^r. Exact zeros are handled explicitly.

2. Represented output coefficients satisfy

       |btilde_(k,r)-b_r(theta_k)| <= delta B_r.

3. The row evaluator, on its represented input y, satisfies

       |Ftilde_j-[A_omega y]_j| <= epsilon_0 ||y||_2

   for every state, input, and output, and ||A_omega||_2<=M. This last norm is exact: each unnormalized rank-one block of P_omega has eigenvalues M and 0, and U_Q is unitary.

4. Lift multiplication residuals have magnitude <=t|v||w|, and addition residuals <=t(|v|+|w|). The R-term sum obeys

       |computed sum - exact sum of supplied terms|
          <= gamma_R sum |supplied terms|.

   Sequential summation permits gamma_R=(1+t)^(R-1)-1, including gamma_1=0. An appropriately arranged balanced sum can replace R-1 by its maximum addition depth, but a streaming implementation need not claim that improvement.

5. The computed normalizer has relative error <=delta_C. One rounded coefficient/output multiplication per term and one final normalizer multiplication are included.

Define

    H=(1+delta_C)(1+t)^2(1+gamma_R)(1+delta)^2.

Then every final computed lifted row obeys the explicit bound

    ||Xhat_computed-Xhat_ideal||_infinity
       <= C E_R [H epsilon_0+M(H-1)] X.              (4)

In particular, for small errors this is

    O(exp(q)[epsilon_0+M(delta+delta_C+t+gamma_R)]) X.

Proof: Before product/summation/scaling rounding, input, coefficient, and row errors contribute at most

    E_R [(1+delta)^2 epsilon_0
         +M((1+delta)^2-1)] X.

The sum of absolute represented terms is at most

    E_R (1+delta)^2 (M+epsilon_0) X.

Product, summation, normalizer, and final multiplication introduce an additional factor

    (1+delta_C)(1+t)^2(1+gamma_R)-1

times this latter bound, followed by the exact C. Adding gives (4). This argument allows cancellation in both the Fourier outputs and the R-term sum. It does not assume that numerical errors are independent or mean zero, or that the computed random row remains unbiased.

## 5. Concrete multiplicative recurrences: delta=O(Ru)

Suppose binary real operations have unit roundoff u, and sufficient exponent range; exact integer indices and nearest-grid residual numerators d_k are used. Round each nonzero rational seed s_n, theta_k, rho with relative error <=u. Compute s_n=n/Q exactly when the chosen mantissa permits it; the following bound allows one rounding anyway. The integer r+1 is exact, and rational seed conversion is certified. Use exact sign/swap operations for powers of -i, so coefficient generation involves real multiplies/divisions rather than cancellation-prone complex formulas.

Power recurrence: a_0=1; ahat_(r+1)=fl(ahat_r shat_n). Then

    |ahat_r/s_n^r-1| <= (1+u)^(2r)-1.

Multiplication of each component of represented x_n by the real ahat_r adds one operation, so complete weighted inputs have relative error at most (1+u)^(2r+1)-1.

Coefficient recurrence: let v_k=2 rho theta_k and vhat_k=fl(2 rhohat thetahat_k), with binary doubling exact. The three seed/product factors give relative error at most (1+u)^3-1 in vhat. Generate real d_0=1 and

    dhat_(r+1)=fl(fl(dhat_r vhat_k)/(r+1)),
    btilde_(k,r)=(-i)^r dhat_r.

There are at most 5r small multiplicative errors relative to v_k^r/r!, hence coefficient relative error <=(1+u)^(5r)-1 and absolute error <=that quantity times B_r. If s_n=0 or theta_k=0, initialize the positive-degree terms to exact zero; never divide by a zero exact term in this reasoning.

A single convenient bound for all r<R is therefore

    delta=(1+u)^(5R+1)-1.                            (5)

Certified relative seed error is important. Computing theta_k as floating-point kQ/N-j_k can suffer cancellation and is not the prescribed method; calculate d_k as an exact signed integer first and round d_k/N. Ordinary unverified rounding of integer indices or modular phase indices is also outside this theorem.

Set t=delta_C=u for the lift and use sequential summation. Equations (4)-(5) give

    H <= (1+u)^(11R+4).

If (11R+4)u<=0.01, then H<=1.02 and H-1<=16Ru. Consequently

    ||Xhat_computed-Xhat_ideal||_infinity
       <= C exp(q) [1.02 epsilon_0+16MRu] X.         (6)

The coefficient recurrence and its error bound are constructive. The separate v9 row evaluator still needs its own certified roots, short FFT, balanced scan, and range contracts.

## 6. Transfer of the v9 precision extension and robust aggregation

Use the previously proved dyadic v9 implementation variant, now at Q. It supplies

    epsilon_0=800 sqrt(QM) log2(Q) u,
    8u log2(Q)<=0.01,                               (7)

provided its certified root/normalizer, operation, pairwise summary, normalized short-FFT, and balanced total/prefix scan conditions hold. This is the bound in the prior V9_PRECISION_EXTENSION.md, not a guarantee for an arbitrary FFT library or the uploaded source.

Together with (6), a sufficient numerical-row bound is

    epsilon_lift
      = C exp(q) [816 sqrt(QM) log2(Q)+16MR]u.        (8)

It multiplies X. To avoid a transcendental bound evaluation, exp(q) may be replaced by a certified rational upper bound; q<4 and exp(4)<55, for example. The finite sum E_R itself is exact rational and sharper in (4).

Let B>=X be a certified norm envelope and choose a common represented radius r satisfying

    r >= g(1+tau_R)sqrt(M/N) B + epsilon_lift B,
    g>sqrt(2).

For L independent random states, exact three-grid classification and the prior verified majority argument give

    Pr[||Xtilde-U_Nx||_infinity
         > tau_R X+(5/sqrt(2))r+eta_out]
      <= 2N exp[-L D(1/2 || g^(-2))].               (9)

For L=2s-1 the bound 2N binom(2s-1,s)g^(-2s) also applies. Here eta_out is a separately certified final output-conversion allowance. The statistical statement is about the independent ideal rows; computed rows may be biased or correlated through deterministic tables.

For a chosen numerical fraction vartheta>0, it is sufficient to take

    u <= vartheta g(1+tau_R)
         / {exp(q)[816 Q log2(Q)+16R sqrt(QM)]},     (10)

as well as the two smallness conditions above, to ensure epsilon_lift<=vartheta g(1+tau_R)sqrt(M/N). The actual choice may use the rational upper bound 55 instead of exp(q). In both all-length asymptotic regimes, O(log N) mantissa bits suffice under bounded-input and sufficient-range assumptions. Fixed binary64 is not an asymptotic substitute for this choice.

Aggregation retains the earlier exact signed-integer floor classification, certified dyadic radius, certified norm envelope, and output-conversion budget. Approximate division followed by an unverified floor is not covered. Input conversion x to x' adds ||x-x'||_2 to the normalized DFT error.

## 7. Setup, roots, representation, and bit costs

The Taylor construction closes the special-function coefficient-generation gap only for this replacement variant. It does not turn all exact arithmetic into bounded-word computation.

- Machin preparation uses O(log(1/eta)) rational operations. A straightforward reduced-rational implementation has polynomial bit cost in log(1/eta), including fraction reduction. Exact intermediate rational sizes and rank-selection products must be charged; they are not automatically fixed-width words.
- After certified conversion of rho, the power and coefficient recurrences use O(LRN) working-precision operations and O(N) values. Exact modular/grid indices need O(log N)-bit integers. The normalizer sqrt(Q/N) is prepared with certified relative error, not treated as free.
- The v9 guard-precision root preparation remains necessary. A working-precision product chain of Q roots can accumulate O(Qu) error. The inherited constructive approach uses guard roundoff of order u/Q, a certified primitive root, O(Q) guard products, and final rounding, with O(log N) guard mantissa bits in these regimes.
- Inputs need a declared representation/range. The inherited common-exponent bounded-integer input model supplies a certified norm envelope with charged work; arbitrary real data of unlimited significant precision does not.
- Relative-error recurrences fail on destructive underflow or overflow. Either provide sufficient exponent range, exact zero handling, and charged scaling, or account for every dropped tiny term through a separate absolute-error budget. The checks below use unbounded exponent range and do not certify binary64 range behavior.
- With C_arith(w) the bit cost of a working-precision arithmetic operation and w_g the guard precision, a conservative accounting is

      O(L R N C_arith(w) + Q C_arith(w_g)
        + polynomial(log(1/eta)+w_g+log N)
        + input/output bit costs).

  Storage is O(Nw) bits plus exponent, input, setup-rational, and counter storage. For fixed L, counters are constant sized; variable L requires O(log L) bits. The bounded-word arithmetic count and the bit-cost statement must not be conflated.

## 8. Fresh independent checks

The included check_charged_taylor.py was written for this extension from the displayed mathematics. It does not import or execute any uploaded code. Its full records are check_results.json and check_run.log.

All checks passed:

- Seven Machin truncations, m=1,2,4,8,16,32,64, compared at high precision against pi and their rational certificates.
- 2,200 sampled real-phase Taylor kernels, ranks 1 through 64, including endpoint s=1, theta=1/2: maximum observed error/tau_R = 0.9980321353.
- 6,240 exact-rational finite-recurrence checks using nearest-even binary rounding at 12, 24, and 53 mantissa bits: maximum relative-error/bound = 0.3096076301. These checks certify the simulated recurrence arithmetic exactly, with unbounded exponents, rather than relying on host float rounding.
- 24 independent lifted-DFT/shared-state/covariance cases at N=3,5,7,10,15,17,23,31 and R=2,5,10. Every (odd a,beta) state of the dyadic v9 row was enumerated. Maximum shared-state identity residual was 6.57e-15; maximum variance/proved-bound ratio was 0.8671237132.
- 600 independently generated bounded-perturbation tests of the general composition ledger: maximum observed error/bound = 0.9996414723.

The Fourier, covariance, high-precision transcendental, and generic-perturbation checks are numerical corroboration, not proofs or end-to-end implementation certification. The exact-rational recurrence tests have the stronger, precisely limited status described above. No practical runtime comparison was made.

## 9. Prior-art and novelty boundary

Ruiz-Antolin and Townsend, *A nonuniform fast Fourier transform based on low rank approximation*, explicitly derive diagonally scaled DFT decompositions and discuss a Taylor construction, its numerical difficulties, and a Chebyshev alternative in Sections 2.1.1-2.1.2. Their discussion also identifies a planning-stage coefficient-construction cost. This extension neither claims a new Taylor/NUFFT principle nor refutes those practical stability observations. Its contribution here is a fully charged bounded-phase rational-Taylor replacement and an absolute energy-relative error transfer to this specific shared-state randomized v9 row.

Primary source: https://arxiv.org/abs/1701.04492 ; full text: https://arxiv.org/html/1701.04492v1 .

The assumptions supporting this absolute-error bound do not imply coefficientwise relative accuracy, equal-precision superiority to Chebyshev/Bessel methods, a practical speedup over FFTW/FINUFFT, an exact sub-N-log-N Fourier transform, or established novelty.
