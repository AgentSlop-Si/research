# Global chirp v7: comparison, scope, and a linear-space robust replacement

Independent synthesis, 9 October 2026. Uploaded code was inspected only as text; no uploaded code was imported or executed. This note supplies new self-contained arguments, not a novelty or practical-speed claim. The separate direct v7 audit verifies its decoder and covariance identities.

## Result in brief

The v7 global Nth-root chirp and output-domain aggregation legitimately avoid the v6 short-decoder loss. Its growing-row storage gap can also be removed without a floor oracle: replace the exact coordinate median with a five-representative streaming robust selector. It uses only arithmetic, comparisons and indexed access; with a constant-factor increase in rows it gives the same asymptotic error and time with O(N) real/complex registers. This is a modified estimator, not an O(N)-space implementation of the exact median.

All conclusions remain approximate, dyadic, and exact-arithmetic statements. End-to-end numerical stability and finite-word complexity are unresolved.

## 1. Comparison with v5/v6

For one v7 seed, let C be the K-by-N block-summary matrix. Each row is supported on one length-M block and has M unit-modulus entries. Thus CC*=M I_K, P=C*C/M is a rank-K orthogonal projection, and the decoded estimator is H=U_N C*C=M U_N P. Uniform beta gives E C*C=I. Consequently

    E[(H-U_N)*(H-U_N)] = (M-1) I,
    E||(H-U_N)x||_2^2 = (M-1)||x||_2^2.

Exactly as for v5, this attains the universal worst-direction total-MSE lower bound N/K-1 for unbiased input-independent rank-at-most-K random linear estimators. That optimality statement is about total MSE, not per-output covariance, nonlinear aggregation, or runtime.

The differences are decisive:

- v5 has exactly isotropic per-output covariance ((M-1)/N)I, but repeats the conventional final short decoder.
- v6 robustifies local coordinates before a single short decoder. Its proved all-output bound pays an additional factor of order sqrt(M); cross-coordinate median covariances are not generally zero.
- v7 decodes each row through its exact two-cycle recurrence in O(N+K log K). It can robustify after decoding while retaining cheap rows. Its per-output covariance has sharp norm 2M/N. There is no illicit removal of the v6 covariance terms: the estimator and location of aggregation changed.

The v7 covariance can in fact be written Q_m=(2M/N)P_m with P_m an orthogonal projection, as the direct audit observes. For every u and valuation v, the count c[u,v] is exactly M/2^(v+1), not merely at most that number. The total projection rank is K(M-1)/2, consistent with tr Q_m=M-1. This anisotropy explains why its sharp worst-input constant is approximately twice v5's isotropic variance while total MSE is unchanged.

## 2. A comparison-only streaming robust selector

### Deterministic lemma

Let z_1,...,z_R be real values, mu a target and B>0. Suppose b of the samples satisfy |z_j-mu|>B. Maintain at most five pairs (representative c,count h), with positive integer counts:

1. If some representative satisfies |z-c|<=2B, increment one matching count. Any fixed tie rule is allowed.
2. Otherwise, if fewer than five representatives are occupied, insert (z,1).
3. Otherwise decrement all five counts by one, remove zero counts, and discard the incoming value.

At the end return a representative with largest count. If b<R/4, the returned value is within 3B of mu.

Proof. Stored representatives remain pairwise farther than 2B apart: new representatives are inserted only when no old one matches, and representatives never move. Call a representative near if |c-mu|<=3B and far otherwise. An interval of length 6B cannot contain four points pairwise farther than 2B, so at most three stored representatives are near. Every good input either increments/inserts a near representative or is discarded in step 3. No good value can increment a far representative, by the triangle inequality.

Let D be the total number of step-3 events. Each such event decrements at least two far counts, since all five slots are occupied and at most three are near. All increments/inserts into far counts come from bad inputs, at most b in total. Counts remain nonnegative, so 2D<=b.

Among the R-b good inputs, at most D are discarded on arrival. Near counters lose at most three counts per step-3 event. Their final total is therefore at least R-b-4D. Let F be the final total of all far counters. Both these surviving units and the at least 2D consumed far units arose from distinct bad arrivals, so F+2D<=b. At most three near counters exist, and consequently

    max_near - max_far
       >= (R-b-4D)/3 - (b-2D)
        = (R-4b+2D)/3 > 0,

whenever b<R/4. A largest counter is necessarily near; a nonempty near counter exists because R-b-4D>=R-3b>0. This proof allows representatives to be created or deleted at arbitrary times; their near/far classification never changes during their lifetime. QED.

The condition B>0 is harmless for Fourier use: zero input is detected and returned exactly. Squared-distance comparisons (z-c)^2<=4B^2 avoid computing square roots. Unlike fixed-grid binning, no floor, exact logarithm or logarithmic-time bin search is required.

A one-counter approximate Boyer-Moore replacement is not valid. At mu=0,B=1 the sequence (-2,-1,-1,1,1,1,10) has five good samples out of seven. A single candidate matching at distance 2B finishes with candidate 10. Nontransitive matching can cancel two good values through an off-center candidate. The five-counter proof explicitly pays for this phenomenon.

### Probabilistic lemma

Assume independently sampled real estimators have common mean mu and variance at most sigma^2. Use R=4s-1 rows, s>=1. A sample is bad at tolerance B with probability at most p=sigma^2/B^2. If at most s-1 samples are bad, then b<R/4. A union bound over s-subsets gives

    P[streamed estimate differs from mu by more than 3B]
        <= binom(4s-1,s) (sigma^2/B^2)^s.

Identical distributions are unnecessary; independence and the individual variance/mean bounds suffice. Values in different output coordinates need not be independent.

## 3. Apply it to the global chirp decoder

For fixed x and every real or imaginary output coordinate, the v7 unbiased row has variance at most

    sigma^2 = (2M/N)||x||_2^2.

Let A_s=binom(4s-1,s), delta in (0,1), and choose B so that

    B^2 >= sigma^2 (2N A_s/delta)^(1/s).

Run the five-counter selector separately on the real and imaginary parts at each of the N output locations. The N outputs of a row may arrive in any order, including the row's two chirp cycles; use their output index to access the corresponding two lists, each of at most five pairs. After R=4s-1 independent rows, with probability at least 1-delta,

    ||X_stream-U_N x||_infty
       <= 3 sqrt(2) B
       = 6 (2N A_s/delta)^(1/(2s)) sqrt(M/N)||x||_2

for equality in the threshold choice.

This is directly comparable to v7's exact-median bound with prefactor 2 and binom(2s-1,s), using 2s-1 rows. Our selector sacrifices constants, not asymptotic exponents.

### Arithmetic and storage

Each emitted complex value updates two lists of at most five entries, using O(1) arithmetic/comparisons. One row needs O(N+K log K) work and O(N) memory. Processing rows sequentially and releasing row temporaries gives

    T = O(R[N+K log K]+N),
    S = O(N).

A primitive Nth root zeta and the normalization scalar 1/sqrt(N) are supplied, as in the exact-arithmetic DFT model. Prepare the complete table of N root powers by successive multiplication in O(N) work and O(N) storage, shared by every row. Every chirp and recurrence coefficient is then obtained by modular index arithmetic and table access. The K-FFT uses the compatible root zeta^M. This removes any hidden per-entry transcendental evaluation, but does not claim that arbitrary Nth roots or normalization constants can be constructed from N by field operations alone. Uniform odd-a and beta sampling and ordinary integer index operations follow the original model; random-bit/bit-operation costs are separate.

The O(N) memory includes the input, per-output representatives/counts, root or row workspace, and final output. No R-by-N table is retained. This is an O(N)-register statement; counts and indices cost O(log N+log R) bits each, while numerical registers are still ideal exact real/complex values.

Compute E=sum_j((Re x_j)^2+(Im x_j)^2) once in O(N) arithmetic. No modulus or square root is needed in the algorithm. An exact field/comparison implementation can use T=B^2 as its threshold and compare squared distances to 4T.

Nor is the displayed real 1/s power essential. Choose a power of two A such that A^(2s)>=2N A_s/delta and use T=(2M/N)E A^2. The smallest such A is at most twice the ideal amplification. Compute A_s by its s-factor multiplicative formula in O(s) field operations. Set Q=2N A_s/delta, start A=V=1, and repeatedly replace A by 2A and V by 2^(2s)V until V>=Q. The multiplier 2^(2s) is prepared by O(s) doublings; throughout, V=A^(2s). This costs O(s+1+log(N/delta)/s) arithmetic/comparisons because log A_s=O(s), and is O(N) in the stated fixed-s or polylogarithmic-s, polynomial-confidence regimes. It changes the ideal amplification by at most a factor two, so the implemented bound has prefactor at most 12 instead of the ideal 6. No new real-power or floor primitive is being hidden.

### Consequences

1. Fixed s and delta, M=Theta(log N): O(N) time, O(N) registers, and error O(sqrt(log N) N^(-1/2+1/(2s))||x||_2).
2. Let L=log N, 1<=f=o(log log N), M=Theta(L/f), delta=min(1/2,N^(-a)), with fixed a>=0 and fixed epsilon>0. Choose explicitly

       s = max(1, ceil(log(2N/delta)/(2 epsilon log L)))

   for sufficiently large N (natural logarithms). Since A_s<= (4e)^s, amplification is O(L^epsilon). With R=4s-1,

       T = O(((1+a)/epsilon) [f/log log N] N log N)
           = o(N log N),
       S = O(N),
       error = O((log N)^(1/2+epsilon)/sqrt(f)
                 * ||x||_2/sqrt(N)).

Thus the growing-row theorem no longer needs O(RN) storage if this different robust estimator is acceptable. As in the original theorem, choose sufficiently large dyadic N so K>=2M. Exact arithmetic is assumed throughout. This does not certify floating recurrence errors or comparison decisions near thresholds.

## 4. Which recovered barriers transfer, and which do not

### Old polynomial-slope collision does not transfer

The recovered collision theorem uses Mth-root local phases eta^(a_r t^2+c_r t), eta=exp(2pi i/M). Pairing t and t+M/2 gives the block-constant ratio (-1)^c_r, so odd polynomial slope parity annihilates the indicated block-flat input. That root/phase identity is essential; it is not a theorem about all quadratic chirps.

V7 instead uses Nth roots and c_r=2aMr+beta. The same half-block shift has a factor exp(2pi i a t/K), which depends on t in the stated regime. The pair cancellation is gone. For an exact concrete negative control take N=32,M=4,K=8,a=1,beta=1. On block zero of the old witness the v7 summary is 1+zeta^2+zeta^6+zeta^12. It is nonzero: its nonzero polynomial has degree 12, below the degree-16 minimal polynomial z^16+1 of a primitive 32nd root. Thus odd beta does not reproduce the old half-probability collision.

The separate old prime-M raw-median obstruction and Mth-root Gauss-sum arithmetic-mean bound likewise do not directly apply to this changed phase law and accuracy contract. A new obstruction would need to be proved for the new estimator.

### Linear strong-scale rank theorem does not exclude nonlinear aggregation

The recovered theorem requiring nearly full expected rank assumes an input-independent random linear final estimator with a uniform epsilon||x||_1/sqrt(N) contract. One v7 row is linear; the coordinate median and the streaming selector are nonlinear. Moreover the coefficient-energy guarantee carries a factor alpha_N growing polylogarithmically:

    error <= alpha_N ||x||_2/sqrt(N).

For effective support d_eff=(||x||_1/||x||_2)^2, this is the old L1 scale with multiplier alpha_N/sqrt(d_eff). It gives a fixed epsilon L1-scale result only when d_eff >= (alpha_N/epsilon)^2. Near-spike dense inputs need not satisfy this. Do not claim the arbitrary-input strong L1-scale contract solely from v7's theorem.

### Continuous exact-recovery obstruction does transfer

All R v7 rows retain at most RK complex linear measurements with input-independent seeds. If RK<N, any measurable decoder using only those measurements and the seed has exact-recovery probability zero for Lebesgue-almost-every x in C^N. Condition a standard circular Gaussian input on its measured projection; the remaining component is a non-atomic Gaussian in the nonzero kernel. Any exact decoded answer selects only one point of that conditional distribution. Fubini exchanges the input/seed quantifiers.

The streaming selector also uses E=||x||_2^2. The same exact-recovery conclusion still holds: conditional on the measured projection and total norm, the remaining complex kernel component is uniform on a sphere of real dimension at least one, hence non-atomic almost surely. Supplying this one scalar does not make generic exact recovery possible. This argument is about continuous complex inputs; discrete and real-only domains need their own rank/injectivity analysis.

In the growing-row schedule, R/M=Theta(f/log log N)->0, so RK<N eventually. The result cannot be promoted to exact arbitrary complex FFTs, even though its real/complex arithmetic is exact.

## 5. Cheap fitted heads remain compatible

The earlier periodic least-squares head transfers unchanged. If P_d is the orthogonal projection onto vectors with period d dividing N, fitting costs O(N); its full spectrum costs O(N+d log d), including explicit zeros. Apply v7 or the streaming replacement only to r=(I-P_d)x, and add U_N P_d x exactly. The failure probability is unchanged and every displayed error bound uses ||r||_2 instead of ||x||_2.

This is a data-dependent improvement to a rigorous residual bound, not a universal gain. The prior residual-certified Green composition can also substitute the new chirp bound for beta, retaining all source/target/rounding certificates and the Fourier sign convention. The new decoder does not inherit a bounded-word or stable end-to-end implementation merely by composing with a certified Green executor.

## Source paths

- New checkpoint: ../source_material/chirp/RESEARCH.md
- Previous audit and proofs: ../prior_audits/FREQUENCY_AUDIT.md and ../prior_audits/FUSION_THEOREMS.md
- Recovered map: ../prior_context/RECOVERED_RESEARCH.md
- Exact old collision: ../prior_context/c20b8706ae4214b3__README.md
- Old repetition/resonance: ../prior_context/0554f98e8eb0cdca__REPETITION.md and ../prior_context/504e7f01540b55df__AFFINE_RESONANCE.md


## Independent check results

The standalone `independent_streaming_checks.py` uses exact integer samples and no uploaded modules. It passes 597,870 exhaustive short words, 720 designed permutations, 48,000 randomized order/tie cases (43,764 inside the proved below-quarter bad-fraction regime), and 360 bad-first/bad-last constructions. It exercises 7,218 full-decrement cases and all five slots. Every prefix checks separation, near occupancy, far-mass accounting, near-mass accounting and total mass R-6D. It also checks the false one-counter shortcut's explicit counterexample. `streaming_check_results.json` contains the reproducible counts. Finite tests support the proof; they do not replace it or establish floating-point robustness.
