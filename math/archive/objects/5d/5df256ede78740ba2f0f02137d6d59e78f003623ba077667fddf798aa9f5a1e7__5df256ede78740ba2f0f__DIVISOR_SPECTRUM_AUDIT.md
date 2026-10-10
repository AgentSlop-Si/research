# Independent audit: divisor-spectrum v13

Audit date: 9 October 2026. The uploaded package labels itself 10 October 2026. Source files and saved logs were read as data only. No uploaded Python file was imported, compiled, or executed. The checker in this directory was independently authored for this audit.

## Verdict

The direct composite covariance formula, its divisor-sum upper bound, and the least-prime-factor approximation theorem are mathematically sound in the stated ideal-arithmetic, fixed-input setting. The semiprime closed form needs a square-case correction.

The claimed improvement is not new relative to the supplied project history: the divisor sum already appears explicitly in the 19:16 composite audit, and the 16:28 mask-count certificate is strictly stronger. The balanced-semiprime approximation family already follows from that older certificate, with half v13's variance bound.

The adaptive planner's general execution certificate is **false as implemented**. Its offset and Bessel branches execute a quantized three-grid aggregator but advertise a coordinate-median guarantee. Section 5 gives an exact counterexample with failure probability one versus a claimed upper bound below 0.00008. The Bessel branch also omits an additional deterministic error term and sometimes certifies a different block size from the one it executes. These defects do not invalidate the standalone direct-composite theorem.

One bounded constructive extension is proved in Section 7: an exact least-prime covariance spectral reduction, including a sharp scaled-projector identity when the least prime occurs at least twice, and a further explicit rational improvement when it occurs once. This improves constants and identifies the exact small spectral problem. It does not change the asymptotic frontier.

## 1. Source, scope, and previous evidence

Source: `fft_divisor_spectrum_v13(1).zip`, Library identity `[private-id]`, 52,521 bytes. The source, archive, and previous reports are identified by SHA-256 in `SOURCE_PROVENANCE.json`. The source's own manifest is checked there independently. The audit changes no master or Library item.

Previous evidence read:

- `COMPOSITE_COVARIANCE_EXTENSION.md`, 16:28: exact masked Fourier-shell covariance, mask-count and logarithmic bounds.
- `COMPOSITE_GREEN_AUDIT.md`, 19:16: the same divisor sum as an intermediate inequality, the stronger previous certificate, sharper median tail, sampler and precision qualifications.

The main assumptions are N=KM, 2≤M≤K, a uniform unit a modulo N, an independent uniform β modulo N, and an input x fixed before the random states. A row returns U_N P_(a,β)x. It does not return U_Nx exactly in general. P²=MP; P is a scaled orthogonal projection and P/M is idempotent.

## 2. Direct covariance: proof and comparison

Let D_u={u−t:0≤t<M,t≠u}, where u=n mod M. For a nonzero signed displacement d, E_d is the diagonal indicator that d∈D_u. Let Π_g be the orthogonal Fourier projector onto the frequencies k with gcd(k,N)=g.

Expanding the error coefficient of one row and averaging β eliminates terms with different displacements. Indeed |d−d′|≤2M−2<N, so equality modulo N is actual equality. The odd-N parity twist then cancels. Averaging a maps a fixed d uniformly onto its gcd shell: reduction of units modulo N to units modulo N/g is onto with equal fibers, by the Chinese remainder theorem. This gives, up to a diagonal unitary modulation depending on the output frequency,

    Q = Σ_(0<|d|<M) E_d Π_g E_d / φ(N/g),    g=gcd(N,d).

The corresponding rational entries are

    Q[n,n′] = [1/(N φ(N))] Σ_(d∈D_u∩D_u′) c_N(d(n′−n)),

where c_N(t)=Σ_(r|gcd(N,t)) r μ(N/r). In particular tr Q=M−1 and Q is positive semidefinite.

Since each projector and each coordinate mask has norm at most one,

    ||Q|| ≤ V(N,M) = 2 Σ_(1≤d<M) 1/φ(N/gcd(N,d)).

Euler's product formula gives φ(N)/φ(N/g)≤g, and gcd(N,d)≤d, so

    V(N,M) ≤ M(M−1)/φ(N).

These steps are correct. They are precisely the intermediate argument already written in Section 3 of the 19:16 audit.

### The stronger existing certificate

For each g, put a_g=#{1≤d<M:gcd(N,d)=g} and

    c_g(u)=#{d∈D_u:gcd(N,d)=g}.
    C(N,M)=Σ_g max_u c_g(u)/φ(N/g).

Using Π_g≤I before summing its masks yields

    Σ_(d:gcd(N,d)=g) E_d Π_g E_d
       ≤ diag(c_g(n mod M)) ≤ (max_u c_g(u)) I.

Therefore ||Q||≤C(N,M). Since c_g(u)≤2a_g,

    C(N,M) ≤ V(N,M).

The inequality is actually strict whenever M≥2. Take g*=gcd(N,M−1). For no local coordinate can both signed displacements ±(M−1) be valid. Thus max_u c_g*(u)≤2a_g*−1, while the other groups have the preceding non-strict bound. Also c_g(0)=a_g, so V/2≤C<V. Neither statement asserts the unproved universal inequality ||Q||≤V/2.

The existing proof further gives

    c_g(u) ≤ floor((M−1)/g),
    C ≤ [(M−1)/φ(N)] #{g:g|N, g<M}.

The previous logarithmic alternative remains available. With L=ceil(log₂M), retain

    B(N,M)=min{C(N,M), 2(M−1)(L+1)²/φ(N), M−1}.

The triangle-mask proof for the logarithmic term was already supplied and is not displaced by v13. The general conjecture ||Q||≤M/φ(N) remains unresolved by this package and by this bounded audit.

## 3. Least-prime corollary and corrected family history

Let p be the least prime factor of composite N and choose M=p. Then p≤√N and all 1≤d<p are units modulo N. Thus

    V(N,p)=2(p−1)/φ(N),
    C(N,p)=(p−1)/φ(N)=V(N,p)/2.

The second equality follows because every local position has exactly p−1 valid displacements, all in the unit shell. It was already an immediate specialization of the 16:28 certificate.

The direct executor still costs O(N+(N/p)log(N/p)) scalar operations and O(N) storage. Consequently p→∞ gives o(N log N) row work; p=Ω(log N) gives O(N); and p=N^(γ+o(1)), for fixed 0<γ≤1/2, gives O(N) with variance N^(γ−1+o(1)). These assertions are correct.

An elementary sufficient totient estimate is φ(N)/N≥1/(1+ceil(log₂N)): if N has r distinct primes p_i in increasing order, p_i≥i+1 and the product Π_i(1−1/p_i) is at least Π_i i/(i+1)=1/(r+1). Thus the needed φ(N)=N^(1−o(1)) does not require an uncharged number-theory oracle. For polynomially growing least prime p, there are only O(1) prime factors and in fact φ(N)/N→1.

For a semiprime N=pq with prime p≤q, the correct cases are:

    p<q: V=2/(q−1), C=1/(q−1).
    p=q: V=2/p,     C=1/p.

Equation (4.3) in source `RESEARCH.md:206–220` silently uses p<q despite stating p≤q. The source's general formula and implementation return the correct square value; the displayed specialized formula is the error. Balanced semiprimes, including squares, retain variance N^(−1/2+o(1)) and the stated α<1/4 approximation regime. This is a valid family corollary, but is not an advance over the older project certificate.

## 4. Median theorem, with sharper finite constants

Let R=2r−1 and let B be a valid variance factor, preferably the older B(N,M). For each fixed input, output k, and threshold t||x||₂, Markov's inequality on the complex squared error gives bad-row probability at most p₀=min{1,B/t²}. If at least r rows are in the complex disk of radius t||x||₂ around the target, both real and imaginary medians are within t||x||₂, and their joint error is at most √2 t||x||₂. Therefore

    Pr(||median−U_Nx||∞>√2 t||x||₂)
      ≤ min{1, N binom(R,r) p₀^r}.

The exact binomial upper tail Σ_(j=r)^R binom(R,j)p₀^j(1−p₀)^(R−j) can replace the subset bound, since row indicators are independent and their individual probabilities are bounded by p₀. No independence between outputs is required. The source's larger bound 2N·2^R p₀^r is also valid for the direct coordinate-median aggregator.

For B=N^(−β+o(1)), t=N^(−α), a sufficient condition for failure to vanish is r(β−2α)>1. For β=1−γ this recovers every fixed α<(1−γ)/2; balanced semiprimes give α<1/4. R is a sufficiently large constant depending on the fixed exponent, not a universal small constant for all α. Work and stored rows are O(RN), hence O(N) for fixed R. Median comparisons belong to the operation model; the aggregator is nonlinear.

If a row sampler can abort with probability ε, add Rε to the unconditional abort-or-error bound. Uniformity conditional on acceptance is sufficient, provided states are independently sampled. The source omits this abort term from the advertised planner certificate.

This is a fixed-input probabilistic theorem, not one random seed guaranteeing every x simultaneously. A fixed public seed is a reproducibility device. For R<M, the common kernel of the R block projections has positive dimension and contains inputs on which every sampled row vanishes. Nothing here gives arbitrary exact DFT recovery or coefficientwise relative error.

## 5. Adaptive planner: exact failure and further mismatches

### 5.1 Wrong aggregation theorem for offset and Bessel execution

`prototype.py:262–319` uses `median_union_failure_bound` for all three route types. The direct route executes real/imaginary coordinate medians (`169–187`). In contrast, `execute_candidate:359–365` calls the inherited streaming three-grid majority routines for offset and Bessel. Their bin width is 7τ, their final values are medians of three bin centers, and τ is set using the caller's g (default 3). The requested tolerance is never passed to these execution routines.

Their inherited guaranteed complex radius is (5/√2)g√V||x||₂, plus applicable deterministic bias. A coordinate-median certificate at an independently requested tolerance cannot certify these returned bin centers.

**Exact counterexample.** Take an offset candidate with N=3, p=2, Q=4, M=1, R=51, g=3, input x=e₀, and normalized tolerance 2. Since M=1, each projected row is exact. The modulation of e₀ is trivial, so every retained output of every row is exactly 1/√3. The row variance is actually zero (the planner conservatively uses V=1/3).

Here τ=√3. For either a constant scalar value 0 or 1/√3=τ/3, the three grid bin centers, in units of τ, are 7/2, −7/6, and 7/6. The final scalar median is 7τ/6. Therefore the returned complex value at every output is

    (7√3/6)(1+i),

whose squared error from 1/√3 is

    (5√3/6)²+(7√3/6)² = 37/6 > 2².

Failure at tolerance 2 has probability one, for every collection of states. Yet the planner's formula returns

    2·3·2^51·(1/6)^26
      = 67,108,864 / 847,288,609,443
      ≈ 0.000079204256.

This refutes the advertised executed offset-candidate certificate in exact arithmetic. It is not a floating-point artifact, and no uploaded executable was needed to establish it. Using the available p=3,Q=3,M=1 candidate gives the same example; it is also the least-work offset option for this tiny length.

### 5.2 Bessel-specific omissions

There are two further independent defects:

- `bessel_candidate` records only the global Jacobi–Anger truncation tail. Execution calls `fused_addition_bessel_chirp_row` with halfwidth H=0, which also approximates local Bessel addition. The inherited code itself includes `addition_kernel_error_bound`, and uses its sum with the tail for bias and variance inflation. The v13 planner omits this positive term whenever M>1.
- The planner obtains M from `offset_core.choose_prime_power_block`, whose target is log Q. Execution obtains M independently from `v11_fused_reference.choose_dyadic_block`, whose target is log₂Q. At N=129,Q=256, the recorded block is 4 and the executed block is 8. Thus the planner's stochastic coefficient, forcing dimensions, and work proxy can describe a different plan from the one run. The disagreement occurs before considering the missing addition error or the wrong aggregator.

These facts are static source findings, with exact small rule checks. This audit does not claim the omitted conservative addition bound equals the actual error in every case; its omission means the claimed certificate is unsupported, and the offset example already disproves the generic certification mechanism.

### 5.3 Required repair contract

Keep the uploaded files unchanged. A repaired dispatcher should:

1. Store and execute exactly one set of N,Q,M,rank,H,row-count,aggregation parameters.
2. Either use actual coordinate medians for all branches, or certify the three-grid radius and choose its τ/g from the target tolerance. These alternatives have different constants and should not share the present certificate blindly.
3. For the fused Bessel branch, use ε=global tail+addition error (plus any certified numerical term), and stochastic factor (M/N)(1+ε)² at the actual M. Reject or increase the rank/H if the deterministic budget fails.
4. Use the stronger direct bound, account for state-sampling aborts, and return an explicit certified/uncertified status against a nontrivial requested failure target.
5. Use exact or outward-rounded computations for formal finite probability certificates. Converting Fraction to float and evaluating products can round downward or underflow; a decimal zero is not a rigorous zero failure probability.

`failure_target=1.0` is the default, so every probability-clipped candidate is declared feasible. Saved choices under that default demonstrate a cost ranking, not necessarily a useful high-probability guarantee. Four of the five saved selected plans have failure_bound=1.0. The fifth, a Bessel plan at N=1,048,573, records approximately 0.00162523; it is subject to the Bessel execution mismatches above and is not a verified executed guarantee.

## 6. Setup, runtime, and precision

### Direct row algebra and short FFT

The inherited one-cycle chirp identity applies to composite N without a prime-power condition. The gauge closure is −1, including odd N with its parity twist, and the forcing uses only one length-K FFT. Compression, phases, cycle forcing, balanced reduction, scan, and scattering have O(N) scalar work. The sole execution FFT call is at `composite_cycle_core.py:147`; the full N-FFT at line 166 belongs to a separate reference oracle.

An O(K log K) arbitrary-length short transform can be instantiated with a padded Bluestein convolution and dyadic FFTs, charging O(K)-scale chirp preparation. The declared arithmetic model must include root/phase generation or a sufficient-precision implementation. NumPy exp/FFT calls do not establish an exact-complex or bit-complexity theorem.

### Planner setup really is more than one trial factorization

The source factors N, enumerates all divisors M≤√N, loops through d<M for each, computes gcd(N,d), and trial-refactors N/g for each newly encountered g within that candidate. The cache is per candidate, not global. The proxy adds only isqrt(N), so it is not a literal charge for these operations or for generating the alternatives.

This omission does **not** force a superlinear asymptotic setup theorem. Put D=τ(N), the total divisor count. There are at most D candidates, at most √N D displacement visits, and at most D² separate totient calculations, each using at most O(√N) trial divisions. An upper bound in a word-arithmetic model is

    O(√N D² + √N D log N + D log D),

with comparable logarithmic factors if charging gcd/Fraction arithmetic more conservatively. Every denominator φ(N/g) divides φ(N), so the rational sums have O(log N)-bit numerators and denominators in this regime. For every fixed ε>0, τ(N)≤C_εN^ε: large primes obey a+1≤2^a≤p^(εa), while the finitely many small primes contribute bounded constants sup_a (a+1)/p^(εa). Thus the displayed setup is N^(1/2+o(1)) and is O(N). Full factorization once, globally cached divisor totients, and the older count certificate give an easier efficient implementation.

This is a completed setup argument under the stated model, not a defense of the precise proxy values or an empirical speed claim. It does not make exact arbitrary complex inputs a bit-linear transform. Rank/tolerance-dependent Bessel planning must be charged separately when those parameters grow.

### Randomness and finite precision

The direct sampler caps unit-candidate calls at max{64,8 ceil(log₂N)²}. It returns the uniform unit/β distribution conditional on success, but a cap on calls to `rng.integers` does not cap their internal rejection bits. The older 19:16 report's bounded fair-bit repair is available: b=ceil(log₂N), at most T=max{64,8b³} independent pairs of b-bit words A,B, accepting exactly A<N, gcd(A,N)=1, B<N. Success per trial is at least 1/[4(b+1)], abort probability at most exp(−b²), and random-bit/GCD setup is O(log⁴N). This is not implemented in the source.

The inherited offset/Bessel sampler has an uncapped rejection loop. The nearest-grid setup still calls `np.unique` unnecessarily and does not establish deterministic linear setup through that library call. Arithmetic-progression classes k≡r mod N/gcd(N,Q) avoid sorting/grouping ambiguities. These were already identified in the previous audit.

The executors use int64 products before modular reduction, with no overflow guard. They use float64 phases, complex128 FFTs, a fixed default seed, and no outward error accounting. Passing a wider dtype does not upgrade phases and FFTs that are explicitly computed as complex128. Thus the saved numerical tests certify neither fixed-binary64 asymptotic accuracy nor a rigorously computed finite failure upper bound.

Source `exhaustive_covariance_matrix` also forms the coefficient row for the conjugated projection rather than the same labeled P used by the direct executor: it uses conjugate(S) times the sum of output_row·S. The covariance distribution is nevertheless unchanged, because conjugating S corresponds to the bijection (a,β)↦(−a,−β−h) modulo N. Its full-state mean and covariance checks remain legitimate distribution checks, but are not a same-state coefficient identity test.

## 7. Bounded extension: exact least-prime spectrum

This section is an independent derivation from the accepted covariance, not a literature priority claim.

Let p be the least prime factor of composite N, M=p, K=N/p, and define the real symmetric p×p matrix

    W_p[u,v]=p−1−|u−v|,    0≤u,v<p.

All nonzero local displacements are units, and their common-validity count is W_p[u,v]. Therefore

    Q = (1/φ(N)) (W_periodic ∘ Π_1),

where ∘ is entrywise product and W_periodic repeats W_p in the local coordinates.

### Block-Fourier reduction

Fourier transform the K block coordinates. At block frequency ℓ, the associated global frequencies are ℓ+sK, 0≤s<p. After a diagonal unitary gauge, the reduced unit-shell projector is

    Π_ℓ[u,v]=(1/p) Σ_(s:gcd(ℓ+sK,N)=1) exp(2πi s(u−v)/p).

The covariance block is (W_p∘Π_ℓ)/φ(N). There are no unit frequencies when gcd(ℓ,K)>1.

If p|K, every s is allowed whenever gcd(ℓ,K)=1. Thus Π_ℓ=I, and every active covariance block is ((p−1)/φ(N))I. There are φ(K) active blocks. Consequently

    p²|N  ⇒  ||Q||=(p−1)/φ(N),
               Q²=((p−1)/φ(N))Q,
               rank Q=p φ(K).

This includes non-prime-power examples such as N=12,p=2 and N=45,p=3. It does not assert that general composite covariance is a scaled projector at arbitrary M.

If p∤K, exactly one residue s=s₀ is excluded in each active block. Hence Π_ℓ=I−vv*/p for a vector v with unit-modulus entries. With D=diag(v),

    W_p∘Π_ℓ = (p−1)I − D W_p D*/p.

Every active block has the same spectrum. Therefore the exact norm is

    p²∤N  ⇒  ||Q|| = [(p−1)−λ_min(W_p)/p]/φ(N).

Each eigenvalue of the displayed p×p block occurs φ(K) times; the other blocks are zero. This is an exact structural theorem. A floating-point eigensolver is optional and is not needed for the following rational bound.

### A direct rational improvement

For any complex vector z=(z₀,…,z_(p−1)), let T=Σ_i z_i and s_j=Σ_(i≤j) z_i for 0≤j≤p−2. Counting the prefix and suffix masks gives

    z*W_p z = Σ_(j=0)^(p−2) (|s_j|²+|T−s_j|²).

Put y_j=s_j−T/2, y_(-1)=−T/2, y_(p−1)=T/2. Since z_j=y_j−y_(j−1),

    ||z||² ≤ 4Σ_(j=0)^(p−2)|y_j|²+|T|²
            ≤ 4Σ_(j=0)^(p−2)|y_j|²+(p−1)|T|²
            = 2 z*W_p z.

Thus W_p≥I/2, giving the explicit valid certificate

    p²∤N  ⇒  ||Q|| ≤ [(p−1)−1/(2p)]/φ(N)
                       < (p−1)/φ(N)=V(N,p)/2.

For p=2, W_2=I, so the exact value when N=2K with K odd is 1/(2φ(N)), an additional factor two below C. For p≥3 the stated general rational improvement is small but unconditional. It requires no spectral computation and no factorization beyond knowing p and whether p² divides N.

For distinct-prime N=pq, the exact coefficient is

    [1−λ_min(W_p)/(p(p−1))]/(q−1),

and the rational upper bound replaces λ_min(W_p) by 1/2. For squares N=p², the exact coefficient is 1/p. All retain the same α<1/4 balanced-semiprime exponent. This bounded result neither solves the general sharp-covariance conjecture nor extends the exact/sublinear FFT frontier.

## 8. Fresh verification and reproducibility

Run only the fresh checker:

    OPENBLAS_NUM_THREADS=1 python independent_checks.py

The completed run is preserved in `CHECK_RUN.log`, with structured results in `CHECK_RESULTS.json` and static call evidence in `STATIC_CALLS.json`.

- Exact Fraction count/divisor comparisons for all 9,275 admissible pairs through N=3,000. C<V in every case; all 2,569 least-prime choices satisfy C=V/2.
- 32,895 exact integer/Fraction Ramanujan identity checks, for 2≤N≤256 and every residue.
- Exact rational LDL positivity checks of W_m−I/2 for every 2≤m≤49. The universal proof above is independent of this finite check.
- Seventeen least-prime spectrum examples through N=121. In p²|N cases, the full rational covariance satisfies the projector polynomial exactly; in the other cases, the first four full-matrix spectral moments match the reduced formula exactly as integers. Separately, full floating spectra match the predicted spectra with maximum discrepancy below 5.0×10⁻16.
- The aggregation counterexample is checked entirely with Fractions, including its squared error 37/6 and false advertised probability bound.
- Static AST checks confirm the mismatched executor calls, omitted Bessel addition-bound call, and differing block selection. Parsing syntax trees did not execute the imported source.

These checks supplement proofs; the exact moment checks alone would not prove full-spectrum equality, and floating eigenvalues alone would not certify a spectral bound. No saved source benchmark or source test suite was rerun. Historical timing and outside literature novelty were not independently established.

## Incorporation recommendation

Retain the older composite certificate as primary. Add the least-prime family as an explicit corollary with corrected provenance and square handling. Add the bounded spectrum theorem if useful. Mark the v13 dispatcher uncertified until its aggregator, block parameters, deterministic error, randomness, and rounding contracts agree with execution. Preserve all exact-FFT, all-length, practical-speed, and fixed-precision limitations.
