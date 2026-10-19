# Rank-optimal sketching, robust spectral tails, and an energy-adapted Green bridge

Independent synthesis, 9 October 2026. Exact arithmetic and explicitly stated probability models throughout. No general FFT lower bound or novelty claim is made.

## A. A rank-constrained minimax theorem, attained by v5

Let U be an N-by-N unitary matrix, and H a random complex linear operator independent of the input. Assume E H=U, rank(H)<=k almost surely, and a finite second moment. Then

    (1/N) sum_(j=1)^N E ||(H-U)e_j||₂² >= N/k-1,
    sup_(||x||₂=1) E ||(H-U)x||₂² >= N/k-1.            (A1)

Proof. Put A=U*H. The trace/nuclear-norm inequality and Cauchy-Schwarz on at most k nonzero singular values imply

    |tr A| <= ||A||_* <= sqrt(k)||A||_F.

Consequently E||H||_F² >= E|tr(U*H)|²/k >= |tr(U*E H)|²/k=N²/k. Unbiasedness gives

    E||H-U||_F²=E||H||_F²-N.

Dividing by N proves the first claim; the largest quadratic-form risk is at least its average diagonal. If the second moment is infinite, the lower bound is trivially true in the extended sense. Equivalently, a uniformly random unit input has average risk at least N/k-1. This does not assert the same lower bound for every fixed input for every estimator.

### Exact projection form of v5

For a fixed v5 seed, define C:C^N->C^K by

    (Cx)_r=sum_t conjugate(xi_t) exp(-2pi i r q_t/K) x_(rM+t).

Different rows of C have disjoint support and squared norm M, so

    CC*=M I_K.

The v5 decoder equals

    H=U C*C.                                            (A2)

To verify (A2), the reconstructed time sample (C*Cx)_(rM+t) is xi_t exp(2pi i r q_t/K)(Cx)_r. Transforming it and separating m=p+Kv gives exactly the supplied short-decoder formula. Thus P=C*C/M is an orthogonal projection of rank K and H=MU P.

Averaging phases gives E(C*C)=I even conditional on q. Since (C*C)²=M C*C,

    E[(H-U)*(H-U)] = (M-1) I,
    E||(H-U)x||₂² = (M-1)||x||₂².                       (A3)

Also, for every individual seed,

    tr(U*H)=N,  ||H||_F²=NM=N²/K.

Therefore v5 attains equality in (A1) at k=K, for every input direction. It is minimax-optimal in expected total squared error among unbiased random rank-at-most-K linear estimators. This is a precise class-specific optimality result, not optimality among biased estimators, nonlinear medians, larger measurement budgets, or infinity-norm accuracy objectives.

Balanced buckets with c columns per bucket have CC*=cI and k=N/c; they attain the corresponding lower bound c-1 as well.

For comparison, the arithmetic mean of R independent v5 rows has expected total error (M-1)||x||²/R and rank at most RK. It is generally not minimax-tight for the larger rank budget, whose lower bound is max(0,M/R-1). The rank argument must not be applied directly to the nonlinear median output.

## B. Why fewer than N retained linear measurements cannot be exact on arbitrary continuous inputs

### B1. Uniform-seed obstruction

Fix a seed omega and let L_omega:C^N->C^m be the retained linear measurement map, with rank below N. Any decoder g_omega depending only on L_omega x and the seed gives the same answer at x and x+v whenever 0!=v belongs to ker L_omega. Since U is invertible, it cannot be exact at both. This rules out a seed that works on every input. By itself it does not exchange the quantifiers and rule out high-probability success for every fixed input.

### B2. The stronger inputwise statement

Assume L_omega is input-independent and has rank below N almost surely. Assume the decoder and success event are measurable, and include any decoder randomness in omega. Then

    P_omega[g_omega(L_omega x)=Ux]=0                   (B1)

for Lebesgue-almost-every x in C^N, identified with R^(2N).

Proof. Take X to be a standard circular complex Gaussian independent of omega. For each fixed seed, decompose X into its components in (ker L)^perp and ker L. The first component is determined by LX; the second remains a nondegenerate continuous Gaussian in a positive-dimensional subspace. Conditional on LX, any proposed decoded vector determines at most one possible value of that second component. Its probability is zero. Thus success has probability zero over X for every admissible fixed seed. Tonelli/Fubini then gives

    0=P_(X,omega)(success)=integral P_omega(success at x) dGaussian(x).

The nonnegative integrand vanishes Gaussian-almost everywhere. Gaussian density is positive everywhere, so it also vanishes Lebesgue-almost everywhere.

### B3. Application and elementary finite-seed alternative

The v6 output depends only on R compressed length-K spectra and their input-independent seeds. Hence rank L_omega<=RK. If RK<N, (B1) applies: exact recovery has probability zero for almost every arbitrary continuous complex input. The v6 sparse exactness theorem is consistent because that structured class has ambient measure zero.

For this particular finite-seed median algorithm there is an elementary alternative. For a fixed seed, the real and imaginary coordinate medians divide input space into finitely many regions determined by linear comparisons. On each region the full output is real-linear and factors through a real measurement map of rank at most 2RK. Its agreement set with the invertible real DFT is contained in a proper real linear subspace when RK<N. There are finitely many regions and finitely many shift/phase seeds. Their union still has measure zero.

These claims, as stated with complex rank, concern arbitrary continuous complex inputs in C^N. For real inputs in R^N and complex-valued measurements, use the rank of the realified measurement map: one complex measurement can supply two independent real coordinates. For example x1+i x2 determines both real values through real/imaginary extraction. The real-input obstruction requires real rank below N; complex rank below N alone is insufficient. These claims also do not automatically apply to a finite binary or bounded-integer domain: an irrational linear measurement can be injective on such a finite set despite having real rank below N. They also do not cover schemes using extra input-dependent information, adaptive measurements without a separate analysis, or accessing the original input again during decoding.

A periodic mean head adds retained linear information. For a d-dimensional exact head plus RK residual measurements, the applicable rank budget is at most d+RK, not RK alone. Invertible exact Green filtering does not change the ambient dimension. Rounding is nonlinear and requires its own analysis if one changes the algorithm/model.

### B4. What the row-count gate implies about this evaluator's cost

For the unaugmented v6 measurement model, positive success for every continuous input requires RK>=N, hence R>=M. With the explicitly evaluated ordinary radix FFTs and full scans, the operation count has order

    R[N+K log K] + N log M.

At R>=M, its charged FFT stages alone contribute at least a constant multiple of

    N log K+N log M=N log N

for dyadic factors, and its input/gather scans also cost at least MN. This is a barrier for the described explicit evaluator and retained-measurement strategy. One cannot derive a universal arithmetic lower bound by treating its big-O upper bound as a lower bound. A different exact algorithm, circuit representation, discrete input model, or use of additional information is outside this conclusion.

## C. Spectral-tail-sensitive v6 recovery without changing the algorithm

Let A_t be the local column spectra. For an integer b>=0, split each spectrum into its b largest-magnitude entries H_t and the remaining tail T_t (break ties deterministically). Define

    E_tail = sum_t ||T_t||₂²,
    rho = min(1, (M-1)b/K).

This split is only for analysis; v6 need not find the heavy entries or compute E_tail. For a fixed target (p,t), let “heavy collision” mean that any other column's retained heavy entry lands at its queried shifted frequency. Its probability is at most rho by a union bound.

The tail contribution to the target error is

    W_t[p]=sum_(u!=t) xi_t conjugate(xi_u) T_u[p+q_u-q_t].

Its unconditional second moment is

    E|W_t[p]|²=(E_tail-||T_t||₂²)/K <= E_tail/K.

For any alpha>0, put a=sqrt(E_tail/(K alpha)). With probability at least 1-rho-alpha, there is no heavy collision and |W_t[p]|<=a. On that event the full local error is at most a. No independence between the collision event and tail noise has been assumed.

If a majority of the R=2s-1 rows meet this complex-good condition, both component medians lie within a of their respective target components. The complex median error is at most sqrt(2)a. Independence across rows, then a union bound over N targets, gives

    P[any local median error > sqrt(2E_tail/(K alpha))]
       <= N binom(2s-1,s) (rho+alpha)^s.                (C1)

The final unitary M-point decoder therefore satisfies, on the same event,

    ||Xtilde-Ux||∞ <= sqrt(2M E_tail/(K alpha))
                    = M sqrt(2E_tail/(N alpha)).       (C2)

The proof is informative when rho+alpha is small enough; the trivial failure bound 1 can always be taken. For a desired delta, set

    p=(delta/[N binom(2s-1,s)])^(1/s),
    alpha=p-rho>0.                                    (C3)

Then (C2) holds with probability at least 1-delta. Using 2N in (C1)/(C3) is a valid looser version, but the same majority of complex-good rows controls both component medians, so it is unnecessary.

If E_tail=0, avoid the division/threshold argument: a majority of collision-free rows is exactly correct, and

    P[Xtilde != Ux] <= N binom(2s-1,s) rho^s.           (C4)

This recovers the supplied locally Fourier-sparse theorem. At b=0, (C1)-(C3) give an arbitrary-input energy bound with the same scaling as v6 and slightly sharper union-bound constants.

An E_tail-based guarantee is analytical/oracle information unless the tails are known or separately certified. Computing all exact local spectra just to evaluate this bound would undo the intended speedup. No such computation is part of the proposed algorithm.

## D. The correct cheap head for an energy-based decoder

Let d divide N and P_d be the orthogonal projection onto d-periodic vectors:

    (P_d x)_(j)=a_(j mod d),
    a_s=(d/N) sum_(j mod d=s) x_j.

Then

    ||x-P_d x||₂ = min_(d-periodic h) ||x-h||₂,
    ||x-g||₂² = ||x-P_d x||₂²+||P_d x-g||₂²

for every d-periodic g. This follows independently on each residue class by the least-squares mean identity. In particular, it is no worse in L2 than the earlier componentwise periodic median or zero head. The median remains the appropriate exact optimizer for the older componentwise L1 mass; there is no contradiction or universal preference between the objectives.

The head transform is supported only at m=lN/d, where

    (U_N P_d x)_(lN/d) = sqrt(N/d) (U_d a)_l.

Thus fitting, residual formation, and all output writes cost O(N), with an additional O(d log d) short transform in this algebraic model. For constant d or d=O(polylog N), this fits comfortably in the v6 budget.

If D_v6(r) has failure delta and error beta||r||₂, then

    Xhat=U_N P_d x+D_v6((I-P_d)x)

has the same failure and error

    ||Xhat-U_N x||∞ <= beta ||(I-P_d)x||₂.              (D1)

For d=M, the fitted mean is precisely each interleaved column's time average. Consequently every residual local p=0 value vanishes, and all M global bins m=Kv can be set exactly from the head. This is an O(N)-fit adaptation to the actual factorization. It does not require computing the other local spectra. The remaining v6 bound is unchanged or improved because the residual energy is smaller.

## E. Residual-certified Green composition in the energy norm

Let T=tridiag(-1,3,-1), S=T^(-1)+(T+I)^(-1), G=U S U*, and B=G^(-1). The previously audited Green bridge supplies

    ||B||∞ <= L=73/18.

For exact filtering, put u=Sx, h=P_d u, r=u-h. Then

    y=B[U h+D_v6(r)]

satisfies, with the v6 success probability,

    ||y-Ux||∞ <= L beta ||(I-P_d)Sx||₂.                (E1)

All added source filtering, fitting and target application take O(N) arithmetic using the earlier tridiagonal/rank-two formulas. The error advantage is data-dependent: there is no claim that L||(I-P_d)Sx||₂ always beats ||(I-P_d)x||₂.

### Paying rounded source and target errors

Let z3,z4 be any approximate source solves, u=z3+z4, and exact residuals

    r3=x-Tz3,  r4=x-(T+I)z4.

The source certificate from the earlier bridge is

    E1=M_box(r3)+(1/2)M_box(r4),
    M_box(u-Sx)<=E1,

where M_box(z)=sum_j(|Re z_j|+|Im z_j|). An optional Euclidean certificate is

    E2=||r3||₂+(1/2)||r4||₂,
    ||u-Sx||₂<=E2,

because the positive tridiagonal inverse operator norms are at most 1 and 1/2. Thus

    ||U(u-Sx)||∞ <= epsilon_src := min(E1/sqrt(N), E2).

Choose h=P_d u, r=u-h. Let v be the computed U h+D_v6(r), with any additional head/decoder/output rounding bounded by epsilon_num in infinity norm. If the target executor has a certified error ||y-Bv||∞<=tau, then

    ||y-Ux||∞ <= L[beta||r||₂+epsilon_src+epsilon_num]+tau.  (E2)

The earlier bridge writes its formulas for a positive-sign unnormalized DFT, whereas this document uses a negative-sign unitary DFT. Use the conjugated Fourier-conjugated operators and root table here: equivalently set q=exp(-2pi i/N) in those formulas, and conjugate the approximate roots consistently. The tridiagonal S is real, so the operators are complex conjugates and all displayed norm bounds are identical. After this sign adjustment, the prior target certificate applies with the same constants to the unitary-scale vector v:

    tau=2 rho_root m_infty(v)
        +(11/36)[m_infty(rhat)+4 rho_root m_infty(zt)],

with rhat=v-(Htilde+I/2)zt and m_infty(z)=max_j(|Re z_j|+|Im z_j|), as defined in the earlier bridge. For an implementation maintained in unnormalized Fourier units, multiply the decoder term by sqrt(N), apply the prior unnormalized certificate, and divide the final bound by sqrt(N). Normalization must not silently be treated as exact finite-word arithmetic.

A zero fitted residual does not erase epsilon_src, epsilon_num, or tau. Rounded Green filtering therefore cannot be used to claim exact original outputs solely because its fitted residual is zero.

The earlier bridge has bounded-word source/target certificates. The new v6 decoder presently has only an algebraic arithmetic guarantee. Composing them gives (E2) and an algebraic cost theorem; it does not, without a new v6 rounding/phase analysis, inherit the old end-to-end word-RAM claim.

### No-worse selection

The direct mean-residual route and Green route can both be run with failure budgets delta/2. Select the output with the smaller complete applicable bound, including all rounding/source/target terms. On the joint success event the selected output satisfies that smaller bound. Two calls preserve the same big-O complexity. If one selects before running from deterministic exact-arithmetic residual bounds, only the selected call is needed; no adaptive selection from an unproved empirical error is allowed.

## F. Why the simplest covariance improvement fails

For each target, the local noise is centrally symmetric by flipping that target's fourth-root phase. Across independent rows, coordinatewise median is odd under a simultaneous sign flip of their errors, so its marginal mean is zero. This fact does not make distinct target errors uncorrelated.

For K=1, M=3, R=3, and A=(1,2,3), fix the irrelevant common phase in each row so xi_0=1. The other two phases independently have four choices, giving 16 equiprobable row states and 4096 ordered triples. The standard-library-only exact_covariance_witness.py enumerates all 4096 triples using integer pairs, and gives

    E e=0,
    E[e e*] = [[6.61328125, 45/512,     3/64],
                [45/512,    5.30078125, 3/256],
                [3/64,      3/256,     2.59765625]].

For example, the p=0/v=0 short-decoder sum consequently has larger variance than would be predicted from only these diagonal entries. The dyadic M=4 example in covariance_results.json confirms this is not an artifact of choosing a non-power-of-two short length.

This does not prove that the full worst-case sqrt(M) decoder factor is necessary. It only rules out the attractive but false claim that local median errors always have zero off-diagonal covariance. Sharper covariance, higher-moment, vector-robust, or norm-adapted aggregation analysis remains an open route.
