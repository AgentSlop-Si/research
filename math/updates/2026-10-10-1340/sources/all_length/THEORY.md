Public source-text preservation. This is the source author’s theory. The [accepted audit](../../reviews/02_all_length_taylor.md) controls its model and interpretation: the catalogue already contains a stronger all-length interpolation compiler, so this is an alternative Taylor proof. The original source’s project-wide missing-transfer and review-pending wording is historical. No historical priority or production eager-table implementation is certified. References to original programs describe the source package; those programs are excluded here. Preservation and hashing are not a new full proof review.

# Norm-preserving all-length Fourier lifting

**Date:** October 10, 2026  
**Status:** Self-contained project theorem and exact-dyadic reference implementation. Deterministic finite-word approximation, not a new exact arbitrary-complex FFT. External publication novelty and independent proof review are outstanding.

## Executive theorem

For every fixed 0 < epsilon <= 1/4, every integer length N >= 1, and every fresh complex dyadic input with O(log(N+2)) bits per coordinate and polynomial dynamic range, the construction produces all N normalized Fourier outputs with

    ||reported - U_N x||_2 <= epsilon ||x||_2

using O_epsilon(N log N / log log N) word-RAM operations and O(N) words, interpreted asymptotically and with ordinary bounded-size fallbacks. The word size is Theta(log(N+2)); table lookups, integer multiplication/division and bit operations are part of this model. Every preparation and input/output operation is charged. There is no sparsity or randomness assumption.

For effectively specified inverse-polylogarithmic epsilon = (log N)^(-a), a>0 fixed (or a dyadic value within a constant factor), the resulting all-length bound is

    O_a(N log N / log log log N) = o(N log N).

The new contribution relative to the inspected project norm-tabulation note is an all-length lift with a dimension-independent Euclidean operator bound, a complete outer fixed-point error ledger, and an exact rank boundary for the same correction kernel. Nearest-grid/Taylor NUFFT ideas and finite-state tabulation are established. This combination is not asserted to be historically new.

## 1. Computational contract and inherited constructive ingredient

U_N[k,j] = exp(-2*pi*i*k*j/N)/sqrt(N). Outputs are explicit numeric values, not queries or symbolic expressions. A concrete allowed input format is (a_j+i b_j)2^(-B), with integer magnitudes <= N^c and |B| <= c log_2(N+2), for fixed c. Per-coordinate dyadic exponents in an O(log N) range can be aligned with a constant-factor word-width increase. Arbitrary real oracles and unbounded exponents are excluded.

The inherited dyadic algorithm is specified in [INHERITED_DYADIC_THEORY.md](INHERITED_DYADIC_THEORY.md). Its original source code is excluded from this public export. Its short proof is restated in Section 6. For a dyadic L and local tolerance delta, denote its output map by A_{L,delta}; it need not be linear because of quantization. Its contract is pointwise for EVERY input:

    ||A_{L,delta}(v)-U_L v||_2 <= delta ||v||_2.

At fixed delta, its charged work is O_delta(L log L/log log L), with O(L) storage. The same order holds for delta=(log L)^(-a) for each fixed a. We use only these two regimes; we do not assert the older dyadic theorem's strongest variable-accuracy regimes survive an unbounded number of lift terms.

## 2. Exact all-length identity

Take L to be the least power of two with L >= 2N. Then

    2N <= L < 4N.

Set c=floor((N-1)/2), and for 0<=k<N let

    h_k = floor((2kL+N)/(2N)),
    b_k = kL-N h_k,
    delta_k = b_k/N,
    v_k = 2 delta_k.

The h_k are distinct indices in {0,...,L-1}; |delta_k|<=1/2. Define

    u_j = 4(j-c)/L,       |u_j|<=1,
    lambda=pi/4 < 1,
    phi_k=exp(-2*pi*i*c*delta_k/L),
    alpha=sqrt(L/N) < 2.

Let Z: C^N -> C^L be zero-padding and S: C^L -> C^N select indices h_k. Both have operator norm one, because the selector has no repeated indices. Let D(a) denote diagonal multiplication by a vector.

The exact identity is

    U_N = alpha D(phi) sum_{r>=0} [(-i lambda)^r/r!]
                         D(v^r) S U_L Z D(u^r).             (2.1)

Proof: each (k,j) entry on the right is

    (1/sqrt(N)) exp(-2*pi*i*h_k*j/L)
      exp(-2*pi*i*c*delta_k/L)
      exp(-i lambda*u_j*v_k)
  = (1/sqrt(N)) exp(-2*pi*i*k*j/N).

The power series converges absolutely in operator norm; all factors except alpha and the scalar coefficient have norm at most one. This is an exact analytic identity, not an exact finite arithmetic algorithm.

## 3. A dimension-free remainder bound

Let T_R be (2.1) truncated to 0<=r<R, R>=2. Since Z, S, U_L and both diagonal masks are contractions,

    ||U_N-T_R||_2 <= alpha sum_{r>=R} lambda^r/r!
                  <= 2 sum_{r>=R} 1/r!
                  <= 4/R!.                                 (3.1)

Also, the norm sum of the unscaled channels is at most e^lambda < 3.

This avoids the sqrt(N) loss that would arise from an entrywise error bound converted through the Frobenius norm. It controls every dense input, including worst singular directions; sampled-vector accuracy is not the theorem's justification.

Select the smallest R>=2 with

    R! >= 16/epsilon.

Then the truncation error is <= epsilon/4. For fixed epsilon, R is a constant independent of N. In general,

    R=O(1+log(1/epsilon)/log(2+log(1/epsilon))).

This bound follows, for example, from R! >= (R/2)^(R/2). Each channel is generally full-rank as an N-dimensional map; a short separable correction is NOT a projection of the input into R dimensions.

## 4. Concrete fixed-point implementation and error ledger

Set

    delta=epsilon/128,
    q=ceil(log_2(512 R^2/epsilon)),  t=2^(-q).

Use integer numerators with common denominator 2^q for the outer masks and scalar coefficients.

### 4.1 Power masks

Start both input and output power masks at one. Update with the exact rational u_j and v_k, truncating the result toward zero to q fractional bits after each step. Since |u_j|,|v_k|<=1, after r steps:

    |u_hat_{r,j}|, |v_hat_{r,k}| <=1,
    |u_hat_{r,j}-u_j^r| <= r t,
    |v_hat_{r,k}-v_k^r| <= r t.                           (4.1)

Each update uses one bounded-word integer multiplication and division/shift. The intermediate integer widths are O(log N+q), not r log N. Only the current masks are stored.

### 4.2 Scalar coefficients

Use a certified rational lower bound for pi, round lambda=pi/4 downward to q fractional bits, and generate nonnegative magnitudes c_hat_r by downward rounding the recurrence c_{r+1}=lambda*c_r/(r+1). Attach the exact four-cycle phase (-i)^r. Then

    0<=c_hat_r<=lambda^r/r!<=1/r!,
    |c_hat_r-lambda^r/r!| <=3r t.                         (4.2)

The second bound follows from lambda-lambda_hat<=2t and an elementary one-step induction. Underflow to zero is included in this absolute bound.

### 4.3 Endpoint phase and normalization

All required endpoint phases have argument magnitude <=pi/4: |c delta_k/L|<=1/8. phase_fixed() evaluates them using integer fixed-point Taylor recurrences and certified Machin intervals for pi. It returns phi_hat with

    |phi_hat_k-phi_k| <=3t.

For detail, take degree D with 1/(D+1)! <= 2^(-q-12), and working precision q+ceil(log_2(4096(D+1)^2))+1. The real argument approximation contributes at most two working units, the recurrence roundings at most O(D^2) working units, and final two-coordinate rounding at most 2t. The program emits a rational certificate <=3t for each phase. Neither an N-step root multiplication nor an exact-transcendental oracle is used.

Compute alpha_hat = floor(2^q sqrt(L/N))/2^q using integer square root. Then 0<alpha_hat<=alpha and alpha-alpha_hat<=t. The one square root and shared pi preparation have elementary polylogarithmic cost; the small fixed-point phase recurrences cost O_epsilon(1) per output for fixed epsilon, or poly(log log N) in the inverse-polylogarithmic tolerance regime.

### 4.4 Stream the channels

For each r, call the dyadic backend on Z D(u_hat_r)x, select the h_k outputs, multiply by c_hat_r(-i)^r and v_hat_r, and add to a single N-vector accumulator. Finally multiply by alpha_hat phi_hat.

The reference program passes Gaussian integers multiplied by the integer mask numerators to its dyadic backend and restores the mask denominator on collection. This is exactly the same operation by homogeneity of the desired transform; the backend error contract applies to the actual supplied vector, irrespective of its normalization choices.

Dyadic outputs, outer constants and masks all have polynomial dynamic range and O(log N) bits in the two stated regimes. Products and aligned sums can therefore be retained exactly in a constant number of RAM words; accumulation need not add an uncharged rounding error. A common binary input scale is restored at the end. For N=1 the identity is returned; a zero vector returns zeros.

### 4.5 Error derivation

Let W be the unscaled, unphased ideal R-channel sum and W_hat the computed sum. Using (4.1), (4.2), sum 1/r!<3 and sum r/r!<3 gives

    ||W_hat-W||_2 <= [3 delta + (1.5 R^2+6)t] ||x||_2.

Here the three contributions are backend errors, both mask errors, and scalar-coefficient errors. Linearity of the rounded backend is NOT assumed.

Since ||W||_2 <=3||x||_2, alpha_hat<=2 and |phi_hat|<=1+3t, a conservative final bound is

    ||computed-T_R x||_2 <= [12 delta+64 R^2 t] ||x||_2.     (4.3)

For example, before simplifying it is bounded by

    {2(1+3t)[3 delta+(1.5R^2+6)t]+21t}||x||_2,

which is less than (4.3) for R>=2 and t<=1/12. Our parameter schedule is much smaller than that threshold.

Combining (3.1) and (4.3),

    ||computed-U_N x||_2 / ||x||_2
       <=4/R!+12 delta+64 R^2 2^(-q) < epsilon.             (4.4)

LiftPlan.error_certificate() evaluates this upper bound using exact fractions. This proof is deterministic and independent of numerical tests.

## 5. Cost theorem, memory, and shrinking accuracy

Let W_D(L,delta) be the dyadic backend work, including its input-independent preparation. Reuse its input-independent tables across the R channels, but charge their construction even for one original input. The total is bounded by

    O(R W_D(L,delta) + N R + N poly(q+log(R+2))
      + poly(log N+q)).                                    (5.1)

The term N poly(q+log R) permits an elementary independently rounded phase routine for every output; no dense phase transform is precomputed. Only R scalar coefficients, two N-sized masks, one N-sized accumulator and one L-sized backend workspace are retained. The dyadic tables occupy o(N) words. Total memory is O(N) in both stated regimes.

At fixed epsilon, R and q are constants; delta is fixed and L<4N. Thus (5.1) gives

    O_epsilon(N log N/log log N).

At epsilon=(log N)^(-a), fixed a>0, R=O_a(log log N/log log log N), q=O_a(log log N), and delta has the same inverse-polylogarithmic scale. The dyadic finite alphabet still has O_a(log log N) bits per complex symbol, and its word-RAM bound is O_a(N log N/log log N). Hence

    T=O_a(N log N/log log log N).

All N poly(log log N) outer work is lower order asymptotically. These bounds use growing Theta(log N)-bit RAM words, not a fixed 64-bit machine as N tends to infinity. Small sizes use finite fallbacks. The constants and table crossover can be astronomical.

The inverse normalized transform follows by conjugating the input, running the forward algorithm, and conjugating the output, at the same cost and error. No exact integer-convolution, coefficientwise-relative-error, or correct-rounding consequence is claimed.

## 6. Restated dyadic tabulation lemma (why the backend is not a free macro)

For L=2^ell and tolerance delta, choose p=ceil(log_2(1024(ell+1)/delta)) mantissa fraction bits. Use an exponent range of O(ell+log(1/delta)) values, not that many exponent bits. With input power-of-two normalization, a sufficiently low underflow threshold tau<=delta/[1024 L(ell+1)] and an upper cutoff above 16L, one complex symbol uses

    b=O(log ell+log(1/delta))

bits in the fixed/inverse-polylogarithmic regimes. A rounded coordinate satisfies the vector bound

    ||quantize(v)-v||_2 <=2^(-p)||v||_2+sqrt(2L)tau.

Take a dyadic radix m with mb <= ell/4. For every padded input key, explicitly store the rounded complete m-point normalized Fourier result using dyadic coefficients of operator error <=2^(-p)/8. There are at most L^(1/4) keys per occurring radix. Construction and storage cost L^(1/4)poly(ell,p)=o(L); packed output also fits in a word. Gathering and scattering m separate values still cost O(m), fully charged.

A separately prepared phase grid of size 2^(p+8), with rounded unit-circle coefficients, handles all scale-dependent twiddles. Its preparation is polylog(L) in the stated regimes. It avoids N-fold accumulation of root errors. Integer address arithmetic is included.

The classical mixed-radix decomposition then has O(ell/log m) macro levels, each of O(L) word work. For fixed or inverse-polylogarithmic delta, m=Theta(ell/log ell) and log m=Theta(log ell), giving the claimed backend bound.

Every intended stage is unitary. At most 2ell+1 stage errors obey

    e_{j+1}<=(1+3u)e_j+3u||x_normalized||_2+sqrt(2L)tau.

The choices above make the resulting relative error <delta. A first-overflow contradiction shows no reachable state saturates: before the supposed first overflow, its norm stays below a constant times sqrt(L), whereas the cutoff is above 16L. The inherited manuscript contains the detailed finite constants. This is a rounded nonlinear word-table algorithm, not an exact bounded-coefficient linear circuit.

## 7. Exact residual rank: why truncation cannot become exact cheaply in this representation

Let

    K[k,j]=exp(-2*pi*i*delta_k*(j-c)/L).

The numbers delta_k comprise exactly N/gcd(N,L) distinct values. To see this, kL mod N has that many values; the chosen nearest-integer convention maps those residues injectively into [-N/2,N/2). The sign at a half tie changes neither count nor distinctness.

For each distinct delta, set z_delta=exp(-2*pi*i*delta/L). These nodes are distinct, because the delta values lie in an interval of length one and L>=2. Removing the nonzero row factor z_delta^(-c), the corresponding rows are

    (1,z_delta,...,z_delta^(N-1)).

The Vandermonde determinant therefore gives the exact complex rank

    rank K = N/gcd(N,L).                                   (7.1)

Any EXACT separated expansion K[k,j]=sum_{r=1}^R a_r(k)b_r(j) needs R at least this large. For odd N and dyadic L, R>=N. This is a restriction on the exact separated phase-correction representation; it is not an arithmetic lower bound for arbitrary Fourier algorithms or a prohibition on sharing a large expansion.

Thus this specific bounded-term near-grid mechanism cannot be relabeled an exact all-length FFT. Taking epsilon=N^(-a) also makes the dyadic symbol width Theta(log N) and destroys the growing-radix advantage. The new exact arbitrary-complex target remains unresolved.

## 8. Executed evidence

Eight groups pass in verify.py:

- 2,048 exact integer geometry and rational error schedules.
- 200 independently checked phase approximations, 4,862 rational mask checks, 99 scalar-coefficient checks.
- 95 full operator-norm comparisons through N=65, covering 73,215 matrix entries. The maximum numerical error/proved-bound ratio is about 0.114439; these are numerical corroboration, not proofs.
- 240 end-to-end cases through N=33, with 3,216 outputs and 1,310 dyadic reference calls. Tolerances 1/64 and 10^-6; zero, impulse, constant, alternating, random dense integer and large-dynamic-range inputs. Maximum relative-error/tolerance ratio about 0.000361336.
- 54 complete small basis inputs, 384 basis outputs and 18 same-length fresh-signal checks.
- 47 exact finite-field residual-rank tests, N=2,...,48, with primitive roots checked in suitable prime fields.
- Eight invalid contracts and twelve deliberately wrong transform cases rejected.
- Twelve symbolic-only cost schedules. No transforms of those huge sizes are run.

The accuracy executor uses on-demand high-precision block evaluation and forced small radices. It does NOT demonstrate the eager-table asymptotic runtime or practical FFT speed. StreamingDyadicReference removes persistent input-dependent block-entry caching; the original code's numerical blocks are reused as arithmetic definitions, not as expected-output oracles. NumPy and mpmath are used only by independent tests. A second complete execution is recorded separately.

## 9. Prior art and originality boundary

Anderson and Dahleh (1996), Rapid Computation of the Discrete Fourier Transform, DOI 10.1137/0917059, already combine local Taylor expansions with FFTs for unrestricted lengths and nonuniform locations.

Ruiz-Antolin and Townsend (2018), A Nonuniform Fast Fourier Transform Based on Low Rank Approximation, DOI 10.1137/17M1134822; arXiv:1701.04492, express NUDFT matrices by sums of diagonally scaled nearby-grid Fourier matrices and analyze precision-dependent rank. That general method is not new here.

Alman (SOSA 2023), Faster Walsh-Hadamard Transform and Matrix Multiplication over Finite Fields using Lookup Tables, DOI 10.1137/1.9781611977585.ch13; arXiv:2211.04643, supplies established adjacent finite-alphabet transform speedups. This manuscript uses the user's rounded complex dyadic backend, not that paper as an exact cyclic Fourier primitive.

The inspected abstract of Liu, Li, Chan and Lam (1998), A Novel Approach to Fast Discrete Fourier Transform, DOI 10.1006/jpdc.1998.1472, also discusses Taylor/moment reductions and a sub-N-log-N multiplication count/systolic execution measure. Its full model and error guarantees were not audited here. It reinforces the need not to claim historical priority from a familiar asymptotic expression alone.

The official OpenAI Math documentation for family 130 separately reports a uniform exact-complex result O(N(log N)^(1-10^-13)) with supplied chosen roots and unrestricted coefficients. Its model differs. Its construction is not used, independently certified, or improved here.

The contribution of this pass relative to the inspected project notes is the dimension-free all-length norm transfer and its finite-word composition, not a new general NUFFT principle. A focused search did not establish priority for the full combined contract. Independent mathematical and literature review remain necessary.

**Bottom line:** a complete all-length normwise approximation construction in the stated word model, with exact coefficient/rank diagnostics and a tested reference executor. Not the requested new exact arbitrary-complex FFT, not a practical speed benchmark, and not novelty-cleared.
