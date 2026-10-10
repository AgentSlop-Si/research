# Independent audit: the all-length Gaussian/Green approximation theorem

## Verdict

The Gaussian lifting and short-slack padding do support the stated **asymptotic randomized approximation** bound, under an explicit ideal supplied-coefficient arithmetic/RAM model and the exact Green decoder identity. I found no counterexample to LC4–LC8 or the Phase 4 interpolation/work argument. The number-theoretic step is unconditional: no unproved prime-gap or Jacobsthal estimate is needed.

This is not an exact FFT result, a binary64 correctness theorem, a bit-complexity result, a measured speedup, or a novelty determination. The guarantee is for each fixed input chosen independently of fresh random states; it is not a single sampled map working for all inputs at once. The submitted default deterministic PRNG seed does not itself instantiate that randomized quantifier.

Scope: independent review of `PROOF_AUDIT.md` §2 and §4, `LOCAL_CANCELLATION_PROOF.md` LC4–LC8, and the text of `gaussian_lift.py`, `coprime_pad.py`, and relevant decoder/sampler definitions. **No submitted source code was imported or executed.** The companion worker separately audits weighted covariance and the exact Green core. The calculations below rederive the Gaussian, padding, complexity, and model portions directly.

## 1. Exact Gaussian identity and safe bounds

Let the rounded frequency be ξ′=j+θ, with integer j and θ=(b+1/2)/H. The actual finite filter is

W(ξ′,t)=Σ_{d=−L}^L exp[−π(d−θ)²/σ²] exp[−2πi(j+d)t].

Poisson summation for the full integer sum gives

Σ_{ℓ∈Z} exp[−π(ℓ−ξ′)²/σ²] exp[−2πiℓt]
=σ Σ_{v∈Z} exp[−πσ²(t+v)²] exp[−2πiξ′(t+v)].

The v=0 term is exactly σ exp[−πσ²t²] exp[−2πiξ′t]=g(t)⁻¹ exp[−2πiξ′t]. For |t|≤τ′<1/2 and integers v≠0,

v²+2vt ≥ |v|(1−2τ′).

Dropping the additional factor exp[−πσ²t²]≤1 and summing a geometric series proves the submitted absolute alias bound σA, where

A=2 exp[−πσ²(1−2τ′)] / (1−exp[−πσ²(1−2τ′)]).

The omitted positive indices have |d−θ|≥L,L+1,…; the negative tail is no larger. Using (L+a)²≥L²+2La gives the submitted tail bound

T=2 exp[−πL²/σ²] / (1−exp[−2πL/σ²]).

Consequently |W−g⁻¹e^(−2πiξ′t)|≤σA+T. The asymmetry from θ∈(0,1) is covered. Frequency indices wrapping modulo Q cause no defect: t_i is an integer multiple of 1/Q, so exp(−2πiQt_i)=1.

The projected input Pz is supported only on blocks touching the centered input support. Each such block is within M/Q of an occupied point, so |t_i|≤τ′=τ+M/Q. For all sufficiently large N the relevant blocks are far from the representative discontinuity at ±1/2. Each block matrix has operator norm M (it is a rank-one matrix scaled by M, not an idempotent orthogonal projector). Hence

||Pz||₂ ≤ M ||z||₂ ≤ M exp(πσ²τ²)||x||₂/σ.

Cauchy–Schwarz, including the unitary N-output normalization, gives exactly

D_G ≤ √(Q/N) M exp(πσ²τ²)(A+T/σ)

in units of ||x||₂. This bound is uniform over the random state. It therefore can be added outside the random main-error analysis without an independence assumption.

## 2. Rounded-frequency target and exponents

The original target is ξ=kQ/N. The midpoint rounding has |ξ−ξ′|≤1/(2H). After Gaussian cancellation the ideal target row has coefficients exp(−2πiξt_i)/√N on the N original coordinates. The norm of its change under rounding is at most

(1/√N)(Σ_i (2πτ|ξ−ξ′|)²)^(1/2) ≤ πτ/H.

The final centering correction exp(−2πikc/N) is exact for the original DFT target and has modulus one. It introduces no additional amplification. Importantly, the phase-rounding bound is applied to the ideal target, rather than bounding the generally much larger norm of Pz.

Set σ²=L=max(12,ceil(κ ln N)), κ=2α/π, and τ≤1/8. Since M/Q=o(1), the preweight-adjusted alias exponent is

πκ(1−2/8−1/64)=47α/32,

and the tail exponent is πκ(1−1/64)=63α/32. Both strictly exceed α. The factor M=Θ(log N), the bounded √(Q/N), and denominators tending to constants do not eliminate this positive exponent margin. Thus D_G=o(N^−α) and D_phase≤(π/8)N^−α.

There is a minor wording issue in LC6–LC7: the Gaussian remainder compares to the rounded-frequency row; the phase term then compares that row to the original target. The stated combined bound is nevertheless correct.

## 3. Padding and prime selection

Put t=ceil(log₂(4N)) and choose the first prime M≥t. Bertrand's theorem bounds M by 2t for t>1, so the submitted sieve range is sufficient. Then M=Θ(log N).

Let B=π(M−1), P=∏_{p<M}p, and K₀=ceil(4N/M). In any interval of T consecutive integers, inclusion–exclusion yields

#{a in interval: gcd(a,P)=1}=T∏_{p<M}(1−1/p)+E, with |E|≤2^B.

Each factor is at least 1/2, so T=2^(2B)+1 makes the count strictly positive. The standard bound π(u)=O(u/log u) gives

K−K₀ ≤ exp[O(log N/loglog N)]=N^o(1).

Therefore Q=MK=4N+r with 0≤r≤M(K−K₀+1)=N^o(1), Q/N→4, and M divides Q. Every prime factor of Q is at least M, so gcd(Q,d)=1 for 1≤|d|<M.

There is no need to construct the enormous inclusion–exclusion table in the algorithm. It proves a termination bound for testing consecutive K candidates against the primes below M. A simple sieve up to O(log N) and at most B divisibility tests per candidate take N^o(1) word operations. The intermediate integers require O(log N) bits, up to constant factors. This is a RAM-operation statement, not a unit-cost arbitrary-integer bit statement.

Primary references checked:

- Paul Erdős, *Beweis eines Satzes von Tschebyschef* (1932), especially pp. 197–198: [original paper](https://users.renyi.hu/~p_erdos/1932-01.pdf).
- J. B. Rosser and L. Schoenfeld, *Approximate formulas for some functions of prime numbers* (1962), Corollary 1, equation (3.6), states π(x)<1.25506x/log x for x>1: [DOI](https://doi.org/10.1215/ijm/1255631807), [scanned paper inspected](https://denisevellachemla.eu/Rosser-Schoenfeld-1962.pdf).

No sophisticated bound on the Jacobsthal function is invoked. The exact inclusion–exclusion estimate above is already enough.

### A useful strengthening specific to this padding

Write w=ω(Q). Since every prime factor is ≥M, w≤log Q/log M. The elementary product inequality gives

φ(Q)/Q=∏_{p|Q}(1−1/p) ≥1−Σ_{p|Q}1/p ≥1−log Q/(M log M)
=1−O(1/loglog N).

Thus Q/φ(Q)=1+o(1). The general totient lower bound cited in the submission is valid but unnecessary for this rough branch. Together with the independently audited Phase 4 covariance bound, this sharpens the variance to O(log N/N), rather than O(log N loglog N/N).

## 4. The convolution charge really is near-linear

For k=0,…,N−1, write kQ/N=4k+f_k+θ_k where f_k=floor(kr/N). On a segment with fixed f_k and bucket b_k, the integer filter centers increase by exactly 4, and the filter taps are identical.

If r>0, f_k has at most r+1 distinct consecutive sweeps. Within each sweep, θ_k increases monotonically and meets at most H buckets. When r=0 there is one segment. Hence in all cases

S≤(r+1)H.

The submitted loop discovers these segments in O(N) integer work. No sorting or quadratic scan is hidden here.

Take a chunk of B₀=2L output positions in one segment. Its gathered input window has length W=4(B₀−1)+2L+1. Convolving with the reversed 2L+1-tap filter requires linear-convolution length

W+(2L+1)−1=4(B₀−1)+4L+1.

The submitted power-of-two FFT size is at least this quantity and is O(L). Reading entries 2L+4j, 0≤j<B₀, gives exactly the intended FIR values; reversing the kernel is the correct orientation. The final partial chunk may gather unused entries, but still pays only O(L).

The number of chunks is Σ_segments ceil(segment_length/B₀) ≤ N/B₀+S. Two short FFTs per chunk, pointwise products, gathers, and output writes therefore cost

O((N/L+S)L log L)=O(N log L+(r+1)HL log L).

Preparing and caching at most H kernel FFTs costs O(HL log L) and O(HL) memory. Since r=N^o(1), H=N^α and L=Θ(log N), the overhead is N^(α+o(1))=o(N), for fixed α<1/2 (indeed α<1 would suffice for this complexity step). The explicit N output writes are already charged.

The long K-point transform costs O(K log K)=O(N) since K=Q/M=Θ(N/log N). For arbitrary K this can be implemented by the standard Bluestein reduction and a power-of-two FFT; it does not require a faster full-Q FFT oracle. The exact Green scan and compression cost O(Q)=O(N), assuming their separately audited identities. A fixed number of repetitions preserves O_α(N loglog N) work and O_α(N) memory.

## 5. Precise coefficient/access model that suffices

A vague unlimited coefficient oracle is avoidable. One precise sufficient ideal model supplies exact length-dependent base constants, supports exact complex arithmetic, and uses O(log N)-bit integer RAM addresses/arithmetic plus independent uniform random words.

For preweights, let a=exp(πL/Q²). Then g_n=a^((n−c)²)/√L. Its multiplicative ratio is a^(2(n−c)+1), and the ratio itself changes by multiplication by a². O(log N) initialization by integer exponentiation and O(N) multiplications generate all weights.

For the actual midpoint buckets, let b=exp[−π/(4LH²)]. Then

w_{d,h}=b^((2Hd−2h−1)²), for −L≤d≤L and 0≤h<H.

The square exponent has constant second differences in each index. Nested multiplicative-ratio recurrences generate all O(HL) taps from a constant number of starting powers of b. Those starting integer powers take O(log N) arithmetic initialization; no per-tap transcendental function oracle is necessary. The factor 4 and the odd integer 2h+1 matter because the implementation uses bucket midpoints, not h/H.

A constant number of supplied phase/root bases covers the Q-chirp table, N-centering phases, the K-point Bluestein chirp, and the power-of-two FFT twiddles, along with the required square-root normalizers. Tables can be generated in O(N+HL) arithmetic and accessed with O(1) RAM operations. Thus coefficient access does not force a missing N log N term in this ideal model.

This does **not** prove that the exact exponential bases can be constructed from rational inputs using field operations. Nor does it prove stability of long recurrences, accurate phase reduction, bounded mantissas, integer-overflow safety, or a particular precision budget. Those must be specified and analyzed separately for a finite-precision or bit-complexity theorem. The supplied NumPy implementation uses exp, fixed-width integer products, and complex128 and explicitly has different numerical limits.

## 6. Randomness, medians, and exact output guarantee

For each fixed x independent of the random states, take s=2h−1 independent states, with h>1/(1−2α). The sharp rough-Q covariance gives B²=O(log N/N). With u=N^−α, Chebyshev gives

p_N≤C log N · N^(−(1−2α)).

For each real or imaginary coordinate, an error beyond D+u in the median requires at least h bad main errors. The union bound over at most 2N real coordinates gives

Pr[||Xhat−U_Nx||∞ > √2(D+u)||x||₂]
≤O_α((log N)^h N^(1−h(1−2α))).

Here D=πτ/H+D_G=O(N^−α). Thus this proves the submitted P4.2 exponent, with a slightly more explicit logarithmic factor. For any prescribed fixed c>0, choosing h>(1+c)/(1−2α) makes the failure bound at most N^−c for all sufficiently large N, since the strict exponent margin absorbs the logarithmic factor and constants. The number of rows then depends on both α and c, giving O_{α,c}(N loglog N) work. Dependence among bins is harmless: only row independence is required. The √2 for combining real/imaginary medians is absorbed into the error constant.

The actual unit sampler caps its calls to rng.integers, not necessarily the internal work needed for each bounded-integer draw. Under an explicit unit-cost exact uniform-integer draw contract, its accepted slope is uniform among units; the rough-Q acceptance probability tends to 1, and the submitted Θ(log²Q) call cap gives all-row abort probability exp[−Ω(log²N)] or smaller. This abort probability must be added to the theorem. The call cap alone does not establish a worst-case bound in a fair-bit model, and the prototype PRNG is not a proof of exact randomness. Alternatively, unbounded rejection gives an expected-work algorithm under an appropriate randomness contract. These distinctions must remain explicit.

A fully bounded fair-bit repair is straightforward. Put ℓ=ceil(log₂Q). At each trial draw two independent ℓ-bit integers A and B; accept the pair only if 1≤A<Q, gcd(A,Q)=1, and 0≤B<Q. Conditional on acceptance the pair is exactly uniform on the product of the unit group and Z/QZ, so a=A and β=B have the required independent distributions. The pair-acceptance probability is Qφ(Q)/2^(2ℓ)>φ(Q)/(4Q), bounded below by a positive constant for all sufficiently large rough Q. Cap the total pair trials at Θ(log²Q), counting every bit trial including those rejected for being ≥Q. Then each row has deterministically O(log³Q) generated fair bits, polylogarithmic integer/gcd work, and abort probability exp[−Ω(log²Q)]. Separate independent bit streams give independent rows; conditional on success the truncated first-acceptance distribution is still exactly uniform. Adding all-row abort to the bound above preserves the stated polynomial-failure guarantees. This is a theoretical repair, not a claim that the submitted sampler already implements it.

The implementation's fixed default seed is useful for reproducibility but cannot be treated as independent fresh randomness for arbitrary adversarial inputs. The theorem must describe genuine independent sampling (or separately prove an appropriate pseudorandomness property). The approximation error is absolute relative to the total input norm; it is not relative accuracy for every Fourier bin. For α<1/2, an N^−α||x||₂ tolerance is larger than the typical ||x||₂/√N scale of many dense spectra, so this is a materially weaker task than exact or uniformly high-relative-accuracy FFT evaluation.

## 7. Independent tiny checks

`independent_checks.py` was authored for this audit. It imports only standard math/json and NumPy; it does not import, execute, or dynamically load submitted modules. `independent_check_results.json` records the successful run.

- Five independently constructed rough-padding plans, N=67,127,257,509,1009: FFT-chunk FIR agrees with direct FIR within 1.85e−15 maximum absolute difference. All segment and chunk counts satisfy the derived upper bounds.
- Twelve Gaussian-width/fractional-phase cases comparing direct integer-frequency sums to independent Poisson-dual sums: maximum difference 4.79e−16.
- At four lengths, five frequencies and three independently built chirp states each, direct Gaussian-remainder input-row norms satisfy LC5; maximum observed bound ratio 0.0132. The corresponding phase-rounding operator norm ratio is at most 0.586. The local pointwise LC4 bound also holds in these checks.

These are tiny floating-point sanity checks, not substitutes for the analytic proof and not numerical error certification. Some extremely small remainders are near floating cancellation error.

## 8. Narrow prior-art/model comparison

[Nakos, Song and Wang (2019)](https://arxiv.org/abs/1909.11123) explicitly advertise an ℓ∞/ℓ₂ sparse-Fourier guarantee for any universe size, with O(k log k log n) samples and running time comparable to the FFT. This confirms that the error norm and arbitrary-length setting must be compared with sparse-Fourier literature before any novelty claim.

[Kapralov (2016)](https://arxiv.org/abs/1604.00845) gives a k-sparse Fourier approximation with an ℓ₂/ℓ₂ guarantee, O_d(k log N loglog N) samples, and O_d(k log^(d+3)N) time. An ℓ₂/ℓ₂ approximation does not by itself imply the N^−α||x||₂ all-bin tolerance for arbitrary dense signals. Conversely, returning all N explicitly materialized outputs already costs Ω(N), even when a sparse result could be produced more cheaply. These differences require checking full theorem assumptions rather than comparing headlines.

Only these narrow primary-source descriptions were checked. This audit makes no broad novelty verdict. Regardless of prior art, the exact O(N loglog N) FFT objective remains unsolved by the constant-row approximation construction.
