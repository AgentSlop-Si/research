# Hero #0 phase 2: independent composite Green audit

9 October 2026. Source received at 19:16 UTC. Uploaded code was **read only**, never imported, compiled, or executed. The fresh numerical and exact-rational checker is `independent_checks.py`.

## Verdict

The central mathematics is valid with the stated restricted lengths, fixed-input randomness, and ideal arithmetic contract:

- For N=KM, 2≤M≤K, every unit-step state has an exact one-K-FFT-plus-linear-scan executor for U_N P x.
- E[P]=I and the source covariance bound M(M−1)/φ(N) are correct.
- A sufficiently large constant odd number of independent rows gives all-output additive error √2 N^(−α)||x||₂, with probability tending to one, for each fixed α<1/2, along families with M=Θ(log N).

This **does not newly establish the composite extension**: the master already contained the same executor extension and a strictly stronger covariance certificate. The previous v9 audit also contained a fixed-row binomial tail. Preserve the older result as the primary bound; treat this package as a useful alternative implementation and consolidation. It establishes neither exact arbitrary-input DFT recovery nor an all-length linear-time theorem, fixed-binary64 stability, an integer-multiplication improvement, or mathematical priority.

Two implementation qualifications matter for a fully charged claim. The composite sampler caps unit candidates, not the internal work of bounded-integer random draws. The offset fallback contains uncapped sampling and unnecessary uniqueness/sorting work. Both admit straightforward repairs described below, but those repairs are not already present in the uploaded program.

## 1. Provenance and source integrity

- Original archive: `fft_hero0_phase2_composite_green_2026-10-09.zip`, 45,877 bytes.
- Original SHA-256: `41d56b89d6020334cbb7504919dcbece69aeb4ce95726e2d6a6ebf0b995a0555`.
- Supplied Library identity: `[private-id]`.
- `original_source.zip` preserves that archive. `source/` preserves its 24 extracted regular files, unchanged. All 23 entries in the source's own manifest verified.
- `prior/COMPOSITE_COVARIANCE_EXTENSION.md` is the stronger, previously accepted 16:28 independent result. `prior/V9_INDEPENDENT_AUDIT.md`, Section 3, already gives the fixed-row binomial argument.
- `SOURCE_PROVENANCE.json` and `SHA256SUMS.txt` identify the files and copied evidence. This audit made no changes to the master or Library.

## 2. Exact cycle: accepted, with corrected projection terminology

Write ζ=exp(2πi/N), η=exp(πi/N), h=N mod 2, and

S[b,t]=ζ^(a t(t−1)/2+(aMb+β)t) η^(ht).

d[b]=Σ_t S[b,t]x[bM+t], and the block output is conjugate(S[b,t])d[b]. Thus each block of P is conjugate(S) outer S. Consequently

P*=P, diag(P)=1, rank(P)=K, and P²=MP.

P is a **scaled orthogonal projection**, not an idempotent orthogonal projection when M>1. P/M is the orthogonal projection. The distinction does not affect E[P]=I: uniform β kills each within-block off-diagonal term.

For D[ell]=Σ_b d[b]exp(−2πi ell b/K), put

A(k)=ζ^(k+β)η^h,

B(k)=ζ^(−M(k+β)−aM(M−1)/2)η^(−hM),

F(k)=[D[k mod K]−B(k)D[(k+aM) mod K]]/√N.

A direct shift of the local chirp sum gives

Y[k+a]=A(k)(Y[k]−F(k)).

The unit a gives one cycle. Its cumulative gauge at step j is

G_j=ζ^(a j(j−1)/2+βj)η^(hj).

G_N=(−1)^(a(N−1)+h)=−1 for every N: an even N has odd a; an odd N has even N−1 and h=1. Cycle closure therefore gives

Y[0]=(1/2)Σ_(j=0)^(N−1) F(aj mod N)/G_j,

Y[aj mod N]=G_j(Y[0]−Σ_(ell<j) F(a ell mod N)/G_ell).

No prime-power condition occurs here. Compression, phases, forcing, reduction, scan, and output scattering each require O(N) scalar operations and O(N) words. The single short transform requires O(K log K). For arbitrary K this can be instantiated by an ordinary zero-padded Bluestein convolution and a dyadic FFT, with all O(K)-size chirp/root preparation charged. As in the inherited model, exact roots and their generation must be part of the declared primitive/constant-preparation contract; the uploaded calls to floating-point exp and NumPy FFT do not certify that exact contract or a bit bound.

Static inspection finds only one FFT call in `decode_balanced_scan` (`source/composite_cycle_core.py:147`), on K summaries. The full N-FFT at line 166 is in the separate testing oracle and is not called by `one_row_estimate`.

## 3. Covariance: valid new proof, weaker than the existing result

The displacement difference satisfies |d−d′|≤2M−2<N in the stated range, so the β average leaves only equal displacements. The parity phase cancels. If E_d is the displacement-validity mask, g=gcd(N,d), and Π_g is the orthogonal Fourier projection onto frequencies with gcd(k,N)=g, then, up to output-dependent diagonal unitary conjugation,

Q=Σ_(0<|d|<M) E_d Π_g E_d / φ(N/g).

The reduction map on units is onto with equal fibers. This is what makes multiplication of a uniform unit by d uniform on that Fourier shell. Taking norms and using φ(N)/φ(N/g)≤g≤|d| gives

||Q||≤Σ_(0<|d|<M)1/φ(N/gcd(N,d))≤M(M−1)/φ(N).

This source proof is sound. It must not replace the stronger prior bound. Let

D(N,M)=#{g:g divides N, 1≤g<M}, L=ceil(log₂ M),

c_g(u)=#{d:u−M+1≤d≤u, d≠0, gcd(N,d)=g},

C(N,M)=Σ_g max_u c_g(u)/φ(N/g).

The accepted prior certificate is

B(N,M)=min{C(N,M), 2(M−1)(L+1)²/φ(N), M−1},

with the simpler valid bound

B_simple(N,M)=[(M−1)/φ(N)]min{D(N,M), 2(L+1)²}.

The direct divisor argument is elementary: Σ_(d:gcd(N,d)=g) E_dΠ_gE_d≤diag(c_g), max_u c_g(u)≤floor((M−1)/g), and φ(N)/φ(N/g)≤g. The prior note separately proves the logarithmic triangular-mask bound. Since D(N,M)≤M−1,

B_simple≤(M−1)²/φ(N)<M(M−1)/φ(N).

Thus the source's advertised variance certificate is always dominated in the nontrivial range. For N=49, M=7, for example, the new bound is 1 while the prior divisor bound and the actual norm are 1/7. The sharper universal conjecture ||Q||≤M/φ(N) remains unproved; this upload does not close it.

## 4. Consolidated constant-row theorem, with a sharper finite bound

Let x be fixed before all row randomness. Take an odd number s of independent accepted states, q=(s+1)/2, and the medians of real and imaginary output coordinates. Let B be any valid per-output variance coefficient, preferably the prior bound above. Put t=N^(−α)||x||₂ and p=min{1, B N^(2α)}.

For a fixed output k, Markov gives Pr(|Y_k−(U_Nx)_k|>t)≤p. If at least q rows are within the complex disk of radius t, both scalar medians are within t and their combined complex error is at most √2 t. Therefore failure requires at least q bad complex rows. A union bound over choices of q rows and over N outputs gives

Pr(||median−U_Nx||∞>√2 N^(−α)||x||₂)
    ≤ min{1, N binom(s,q) p^q}.

This removes the unnecessary extra scalar-coordinate factor 2 and replaces 2^s by binom(s,q). No independence between output coordinates is needed. If each attempted row can abort with probability at most ε, the unconditional abort-or-error probability is at most

min{1, sε + N binom(s,q) p^q}.

Conditioning on every row's success preserves the product uniform state distribution when their randomness is independent. The abort term must not be omitted when claiming an unconditional implemented guarantee.

For M=Θ(log N), either the source bound or the stronger prior bound is N^(−1+o(1)). Hence the output-error contribution is N^(1−q(1−2α)+o(1)), which tends to zero precisely under the sufficient condition

q(1−2α)>1.

At α=1/3, s=7 already suffices with exponent −1/3+o(1); the source's s=9 gives its stated −2/3+o(1). For fixed α and fixed s, the median storage O(sN) and work O(sN) are O(N). This work count includes exact real comparisons for median selection; it is not a complex-arithmetic-only linear circuit. The per-state projected transform is linear, whereas the median aggregator is nonlinear. Letting α approach 1/2 with N is a different regime and does not preserve the fixed-row conclusion automatically.

This is not a guarantee simultaneously for every x under one revealed state set. In fact, if M>s, the common kernel of s sampled P operators has dimension at least N−sK. Some unit vector in it has a Fourier coordinate at least √(1−s/M), by projecting the Fourier basis onto that kernel and averaging the squared projection norms. All sampled estimates and their median vanish on that vector. This also explains why the hardcoded reproducibility seed in `composite_lift.py:48–50` cannot itself provide a fresh-randomness theorem against arbitrary inputs chosen with knowledge of that seed.

The older v9 audit already proved a fixed-row tail of this type for its three-grid robust decoder. The new direct-median presentation improves simple constants and makes the restricted-length corollary explicit; it is not a new asymptotic frontier or priority claim.

## 5. Fully charged setup and actual source limitations

### Divisor selection

`CompositePlan.build` (`source/composite_lift.py:29–39`) scans an interval from floor(0.5 log₂N), bounded below by 2, through ceil(2 log₂N), bounded above by √N. This costs O(log N) integer remainder tests. Full factorization and φ(N) are not needed for execution. The diagnostic totient routine uses trial division in O(√N) word divisions, still within O(N), but is not on the estimator path.

The actual default planner supports that particular window. An abstract family admitting a divisor c log N for some other fixed constant c need not be accepted by the default settings; the window must cover the known family or M must be supplied. When the window is empty the implementation raises `ValueError`. The handoff's sentence that prime N “necessarily chooses M=1” is not the behavior of this planner. Manually using M=1 in the core is exact but pays for the full N-FFT.

### Capped composite state selection

The uploaded code samples a uniformly from {1,…,N−1} and accepts units. Therefore its exact candidate success probability, in the ideal uniform-integer model, is φ(N)/(N−1), not φ(N)/N. The displayed failure upper bound (1−φ(N)/N)^T is conservative and valid. First acceptance before a fixed cap is uniform on the units; independently drawn β is uniform.

T=max{64,8 ceil(log₂N)²}. GCD by Euclid adds O(log N) word divisions per candidate, so the capped outer loop costs O(log³N) word operations, asymptotically O(N). With the standard totient lower bound, its stated superpolynomially small outer failure bound is correct. However, a cap on calls to `rng.integers` does not establish a bound on the internal bounded-integer sampler or supply an ideal independent random-bit oracle. Thus “deterministic charged runtime” for that exact Python program needs an explicit random-draw cost contract, or the repair below.

### A completely bounded fair-bit repair

This repair avoids reliance on a sharper analytic totient estimate. Put b=ceil(log₂N), T=max{64,8b³}. On each of at most T trials, draw two independent b-bit words A,B. Accept exactly when A<N, gcd(A,N)=1, and B<N; return (A,B). Abort after T failures. Every unit/β pair has one equally likely raw preimage, so the accepted output is exactly uniform on (Z/NZ)^××Z/NZ, including conditional on success.

If N has r distinct prime factors p_1<…<p_r, then p_i≥i+1 and r≤b, giving

φ(N)/N=Π_i(1−1/p_i)≥Π_i i/(i+1)=1/(r+1)≥1/(b+1).

Since 2^b<2N, each trial succeeds with probability φ(N)N/2^(2b)≥1/[4(b+1)]. Hence

ε≤exp(−T/[4(b+1)])≤exp(−b²).

This is superpolynomially small, using only an elementary bound. At most 2bT=O(log⁴N) fair bits are requested, and the trial GCDs cost O(log⁴N) word divisions in total, still O(N). This addresses random-state setup only; it does not turn arbitrary exact complex arithmetic, input reading, or the full transform into a bit-linear algorithm.

### Numerical and practical contract

The source uses int64 intermediates such as a*j and j*(j−1) before reduction, with no overflow guard. It uses complex128 phases and FFTs. The default seed fixes the run. Consequently the prototype is a reproducible numerical implementation, not a certified unlimited-size exact-arithmetic or fixed-binary64 theorem. Existing dyadic finite-precision results cannot simply be declared to certify this arbitrary-composite NumPy implementation.

The saved speed ratios compare a single composite row with a different, 15-order approximate procedure at unmatched accuracy. The source itself shows native NumPy FFT faster. Those saved timing measurements were not rerun here and establish neither matched-error superiority nor an asymptotic runtime proof.

## 6. Offset-class branch: algebra accepted, scope and code cost corrected

With Q=p^L≥N, nearest index j_k=round(kQ/N) using ties up, and θ_k=kQ/N−j_k, the exact class count is h=N/gcd(N,Q). Modulating x by exp(−2πiθ_k n/Q) and padding to Q gives

(U_Nx)[k]=√(Q/N)(U_Q z_(θ_k))[j_k].

Norm preservation plus the inherited prime-power variance gives the stated per-output coefficient M/N. Reusing a state across classes does not hurt that per-output argument or a union bound; independence is needed between repeated rows. Work is O(hN), under the same short-transform and phase-generation contract, for fixed p and M=Θ(log N).

This does not enlarge the asymptotic near-log-divisor family when N=c p^a with fixed c,p: choose p^r≤log N<p^(r+1). For all sufficiently large a, r≤a, so M=p^r divides N and lies between (log N)/p and log N; also M≤√N. Such a family already satisfies the direct composite theorem. The offset method remains an alternative, may improve a finite-size choice or constant, and does not help general rough/prime lengths when h grows like N.

The packaged offset implementation is not a complete deterministic linear-time realization of this mathematical alternative:

- `OffsetPlan.build` checks `np.unique(indices).size==N`, and `classes()` also calls `np.unique`. Unique/sorting routines do not come with the required worst-case linear-work contract. In the installed NumPy 2.3.5, the integer unique path builds a hash table then sorts its unique result by default; the all-distinct index check sorts N values unnecessarily. No conclusion here depends on asserting a tight lower bound for every library version.
- `classes()` scans all N numerators per class, consistent with O(hN), but the preliminary uniqueness operations are unnecessary.
- The fallback imports the old `unit_step_core.draw_state`, whose rejection loop is uncapped.

An exact linear grouping repair is immediate: θ_(k+h)=θ_k, because hQ/N is integral. The h first values are distinct, so class r is exactly k≡r mod h. Construct the classes by these arithmetic progressions, compute indices once, and prove/check strict increase directly instead of sorting. Combine this with the bounded fair-bit state sampler. These repairs are independently verified structurally but have not been applied to the preserved uploaded source.

## 7. Fresh checks and their limitations

All results are in `CHECK_RESULTS.json`; `CHECK_RUN.log` is the actual independent run.

- 1,389 cycle/oracle comparisons: **every** one of the 1,384 factor pairs 4≤N≤600, 2≤M≤√N, M|N, plus five larger cases through N=20,736. Maximum discrepancy 7.3612×10^−14. There were 303 odd-length cases including the extra tests. The source's saved 1,018-case fuzzer selected at most three block divisors per N; it was not an exhaustive sweep over every factor pair.
- 4,926 full-state enumerations across seven (N,M,k) cases, including odd composite and prime-power controls. These use the actual U_NP row coefficients. Maximum covariance entry discrepancy versus the independent rational Ramanujan formula was 2.6368×10^−16. First moments, trace M−1, PSD tolerance, P²=MP, and diag(P)=1 passed.
- Exact rational divisor/count inequalities for 5,781 admissible pairs through N=2,000, totaling 19,787 gcd-group certificates. The new bound was strictly weaker for every pair. The largest ratio against the simple prior divisor bound in this sweep was 43 at (N,M)=(1849,43).
- 210 exact binomial-tail comparisons and 81,375 median-geometry configurations checked the aggregation certificate.
- Exact accepted-state counts and the elementary fully bounded sampler inequalities checked for every N from 2 through 256.
- 36 exact-offset-class/direct Fourier comparisons across radices 2,3,5 and 12 lengths; largest numerical discrepancy 7.6915×10^−14. Exact class count and rational offset identities were checked with integers.
- Static AST inspection confirmed the separate K-FFT execution call and N-FFT reference call. AST parsing does not execute uploaded code.

These checks supplement the proofs. Floating eigenvalues and finite-size comparisons do not prove an infinite-family theorem, uniform numerical stability, or the conjectural sharper covariance bound. Historical performance and external literature/priority claims were not independently established by this audit.

## 8. Reproduction and incorporation

From this directory, with Python 3 and NumPy installed:

    OPENBLAS_NUM_THREADS=1 python independent_checks.py

This invokes only the fresh checker. It reads source bytes for hashes and AST inspection; it never executes or imports any uploaded module. The original archive and its reproduction commands are preserved for provenance, not run by this audit.

Recommended incorporation: retain the older composite bound and fixed-row history; add the direct-median consolidation, correct scaled-projection terminology, record the sampler/setup qualifications, and retain the exact-DFT frontier as unresolved. Do not promote the looser covariance certificate or fixed-cofactor fallback to new asymptotic advances.
