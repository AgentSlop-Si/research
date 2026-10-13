# Independent adversarial review: Q16 sparse success bridge

Date: 13 October 2026 UTC.

## Verdict

**ACCEPT, with the explicit promise-domain and source-model scope stated by the candidate. No required repair and no in-domain counterexample found.**

The reviewed artifact is `Q16_Sparse_Success_Contract_Bridge_Audit_2026-10-13.zip`, SHA-256 `55c074877d47b7c0f8d0d6f5f1394005b650ff29a428b9180e6de34d488d5f6f`, 117,351 bytes. The exact report is `q16_success_bridge_audit_20261013/SUCCESS_BRIDGE_AUDIT.md`, SHA-256 `5ad21fe8e2ff045026bc6152e943bdb134b8f81dff482650e2acd0e63e0cbacf`.

This independent review accepts the bridge from the six pinned accepted numerical components and the fair-tape product law to the following simultaneous statement. For each fixed, globally valid, deeply immutable source v, with every Cartesian component bounded by 1 and R=||v||₂>1/2, on the exact source sparse route with an independent uniform tape,

    Pr[||ztilde − U_M v||∞ ≤ 4 M^(−β) R] ≥ 1 − M^(−3).

U_M is the negative-sign unitary DFT. The coordinate target is the full unwindowed transform. The sparse output is interpreted as zero away from its returned indices. This is not a claim that ideal supported-window estimates equal the full transform pointwise, nor that arbitrary deterministic schedules have a recovery guarantee.

The every-tape work and cumulative auxiliary-storage claim is accepted in the inherited finite-arithmetic source model for fixed rational β∈(0,1/2), fixed d, and a declared exponent *value* bound F=O_d(m):

    O_(β,d)(M^(1/2+β) poly(m)),  M=2^m.

Caller-owned represented source storage, its construction and validation, tape construction and physical entropy, host runtime, I/O and archive serialization remain outside that auxiliary claim. The existing Python tuple interface does not acquire an implicit-source implementation merely from this theorem.

## 1. Independent scope and evidence discipline

The review read the complete recovered `PROOF.md`, `ALGORITHM.txt`, current audit, recovered edition and pinned component acceptance reports as text. It also read the actual six scientific source modules. No candidate scientific program, producer test, historical scientific program, historical reviewer program, or candidate proof-control program was imported or executed. The only executed numerical controls here are the newly written standard-library `reviewer/independent_checks.py`.

That program verifies the candidate ZIP hash and size, its complete manifest and member inventory, provenance hashes, all six scientific source bytes against the retained fair-tape acceptance ZIP, and all seven copied acceptance reports against their separate retained accepted-review ZIPs. Thus a filename, copied acceptance label, or mutable source directory is not the binding authority. The frozen candidate ZIP is included in `evidence/`.

The numerical scalar/window/FFT/phase contracts are inherited as explicitly permitted dependencies, not re-certified wholesale by this review. Their scopes are read rather than silently expanded. In particular the earlier recovered-edition acceptance is not used as proof of the present recovery bridge. Sections 2–9 below independently audit the missing universal arguments and their actual implementation connection.

Finite controls corroborate algebra, discontinuities and byte integrity. Their pass counts are not evidence that theorem-scale sparse recovery was executed, not an empirical estimate of its failure probability, and not a substitute for the universal arguments below.

## 2. Exact input domain and source dispatch

The parameters are exactly

    k=2^ceil(2βm), B=2^ceil((1/2+β)m), T=M/B,
    r=2m+1, ℓ=8B, W=2r(ℓ−1)+1,
    q=512k, L=4m+1, P=16m+16, ρ=2^(−P), δ=M^(−4).

The source route enforces B|M, B≥4, T≥4, B≥4096k and W<M. Consequently T is a multiple of four, g=T/4 and H=3T/4 are integers, q≤B, and k≤M. Exact normalized Fraction inputs and integer ceiling computations avoid floating-point dispatch discontinuities.

The source-only wrapper derives its own q and source WindowSpec. There is no accepted path by which reduced fixture parameters, supplied buckets, a supplied schedule, or a supplied candidate set can enter this source theorem. Failure of a sparse guard is an unsupported sparse call; the current code does not implement a dense fallback. This is consistent with the restricted claim.

Global validity, R>1/2, deep immutability, and input/tape independence are premises. The source header check and sample-by-sample validation are not purported to establish unsampled global validity or normalization. A theorem on the promised input domain does not need to scan that entire domain at runtime. Conversely the theorem gives no permission to label arbitrary unvalidated sources normalized.

For cost, F is a bound on the numeric dyadic exponent, not its binary encoding width. A source with exponent 2^m can have only O(m) exponent-field bits yet require enormous alignment integers. The candidate explicitly excludes that cost regime. Its F=O_d(m) hypothesis is therefore substantive and correctly stated.

Outer predicates βm≥2 and t<M do not enter the front-end proof. Their absence from this front-end dispatch is intentional and causes no missing premise here.

## 3. Compact window: support, normalization and every frequency

Let U,U′ be independent uniform integers in {0,…,ℓ−1}. Reflecting U′ shows that the sum of r differences has exactly the centered coefficients of (1+X+…+X^(ℓ−1))^(2r)/ℓ^(2r). Thus F is even, nonnegative, sums to one, and has support from −r(ℓ−1) through r(ℓ−1). W<M ensures no time-support aliasing. No numerical experiment is required for this identity.

Its characteristic function is

    Φ_j = |ℓ^(−1) Σ_(u=0)^(ℓ−1) ω^(−ju)|^(2r), ω=e^(2πi/M).

It is real and lies in [0,1], including Φ_0=1. For d=|j|_M∈[g,M/2], sine concavity gives |sin(πj/M)|≥2d/M; the numerator sine has modulus at most 1. Since ℓg=2M, the normalized ratio is at most 1/4 and Φ_j≤16^(−r). The zero-frequency case is handled by its exact limit, with no division by zero.

For C=Σ_(j=−g)^g Φ_j and D_H(t)=Σ_(u=−H)^H ω^(ut), the implemented ideal window is w_t=M F_t D_H(t)/C. Direct finite rearrangement gives

    M^(−1) Σ_t w_t ω^(−jt) = C^(−1) Σ_(u=−H)^H Φ_(j−u) = G_j.

This independently checks the factor M, both signs and the normalizer. Omitting M would be a real defect; it is present in the source and report.

There are 2H+1 distinct residues in the shifted interval, because 2H+1<M. For |j|_M≤T/2, a signed lift of [j−H,j+H] contains [−g,g], so its central contribution is exactly C. For general j the central contribution is at most C. Any noncentral term is at circular distance greater than g and has size at most 16^(−r). For |j|_M>T, circular reverse triangle inequality gives |j−u|_M>T−H=g, so every term is small. This handles wrapped intervals and the exact passband and stopband endpoints.

The excess is bounded by

    (2H+1)16^(−r) ≤ M16^(−2m−1) = 2^(−7m−4) ≤ M^(−4).

Therefore 1≤G≤1+δ on |j|_M≤T/2; 0≤G≤δ on |j|_M>T; and 0≤G≤1+δ everywhere. These are all-frequency bounds, not extrapolations from finite fixtures. Also Σ|w_t|≤M(2H+1)≤M².

The rounded taps need not have an exactly nonnegative or flat Fourier response. The proof correctly uses the exact w and G, then transfers through the numerical bucket error. It neither assumes exact properties of rounded taps nor adds the same tap perturbation twice.

## 4. Actual bucket and phase errors

Folding by t mod B and applying the negative-sign unnormalized B-DFT followed by 1/√M gives the ideal bucket

    b_j=M^(−1/2)Σ_t w_t v_(σt+τ) ω^(−jTt)
       =Σ_i z_i ω^(τi) G_(jT−σi), z=U_Mv.

The second identity follows by inserting the unitary inverse transform. In particular τ creates a positive spectral phase, canceled by the estimator's negative inverse phase. There is no omitted B normalization, M normalization or frequency translation by τ.

For A=2M², b=log₂B and ρ=2^(−P), the pinned BUCKETS constructor literally builds

    E_B=(A+2Wρ)(1+ρ)^(b+1)−A+ρ.

This also follows directly from an exact input ℓ₁ envelope A, tap perturbation 2Wρ, at most b approximate root factors on each FFT input/output path, the approximate scale, and one final Cartesian-grid rounding with complex error at most ρ. It does not depend on successful recovery.

For n=b+1≤m+1, nρ≤1/2. The binomial/geometric estimate (1+ρ)^n≤1/(1−nρ)≤1+2nρ gives

    E_B≤[4(m+1)M²+4M+1]ρ≤24(m+1)M²ρ.

Each actual phase estimate approximates e_i=ω^(−τi)b_(hσ(i)) with error at most (1+ρ)E_B+Aρ+ρ, hence at most η=64(m+1)M²ρ. The phase root is freshly certified for its actual τ and i, multiplication is exact, and final rounding is performed once. The report does not introduce division by G.

Since ρ=2^(−16)M^(−16), η=(m+1)M^(−14)/1024≤M^(−13)/1024<1/(8√M). With a=R/√k, R>1/2 and k≤M imply 1/(8√M)<a/4. In particular E_B<a/4. This is the normalization-dependent uniform margin used below; arbitrary tiny inputs do not have it.

## 5. Odd-slope collision and second moment

For nonzero d mod M, write d=2^s u with u odd and Q=M/2^s. A uniform odd σ mod M gives a uniform odd residue σu mod Q, because every odd residue has exactly 2^s odd lifts. This remains true for Q=2. Thus no invertibility of d is assumed.

For 0≤c≤M/2, if c<2^s the small-displacement event is empty. Otherwise the symmetric circular arc contains at most 2c/2^s odd residues among Q/2. If the two endpoints identify at Q/2, counting them twice is only an upper bound. Hence

    Prσ[|σd|_M≤c]≤4c/M.

The exact half-open hash obeys |hσ(i)T−σi|_M≤T/2, including equality. If another frequency ℓ lies within T of that target-dependent center, then |σ(i−ℓ)|_M≤3T/2. B≥4 gives 3T/2≤M/2, so its probability is at most 6/B. The bucket center was never treated as independent of σ.

Conditional on σ, uniform independent τ makes distinct Fourier characters orthogonal. Expanding the squared error and averaging τ eliminates both the cross terms with the self bias and all cross terms between different interfering indices:

    Eτ|e_i−z_i|² = |G_self−1|²|z_i|² + Σ_(ℓ≠i)|z_ℓ|²G_other².

Use self bias δ, near response at most 2, distant response δ, the near-event bound 6/B, and Parseval. This proves the reported conservative bound (24/B+2δ²)R². Markov at a=R/√k yields

    Pr[|e_i−z_i|>a]≤24k/B+2kM^(−8)
                     ≤24/4096+2M^(−7)<1/128.

The last strict inequality already holds for M≥4, far below actual sparse eligibility. Boundary equality in the good event is allowed.

## 6. Energy, top-q ties and exact unknown-location enumeration

Again using τ orthogonality, conditional on any σ,

    Eτ Σ_j|b_j|² = Σ_i|z_i|² Σ_j G_(jT−σi)².

At most three equally spaced centers can lie within distance T of a fixed residue. Three is necessary at endpoints: an index exactly at a center is also distance T from its two neighbors. The remaining centers contribute at most δ² each. The energy is therefore at most (12+Bδ²)R²≤13R².

For K={j:|b_j|≥2a}, E|K|≤13k/4 and Pr[|K|>q]≤13/2048<1/128. This is a total-energy bound for arbitrary spectra, not a heavy-gap, spectral-tail or known-support assumption.

Fix |z_i|≥4a. On |e_i−z_i|≤a, its ideal bucket has modulus at least 3a and its computed bucket at least 11a/4. Every computed bucket ranking at least as high has ideal modulus at least 5a/2>2a. If |K|≤q, omission would require q distinct other K buckets in addition to the target. That is impossible.

This argument is stable to changed numerical sort order, all computed ties and |z_i|=4a. It requires no comparison between the *ideal* and computed sort permutations. Exact squared integer magnitudes and the source's lower-index tie rule implement the required computed order. Combining the two bad events gives per-round heavy-location failure <1/64, so the weaker bound 1/16 used in amplification is safe.

For even T, the half-open cells [jT−T/2,jT+T/2−1] partition the residues. The literal hash sends a midpoint to the upper bucket and wraps the final midpoint to bucket zero. Odd σ is invertible, and the decoder enumerates precisely σ^(−1) times those residues. τ is correctly absent from this frequency inverse. Every selected bucket gives T distinct preimages and each round gives exactly qT memberships.

With L=4m+1, the vote threshold ceil(L/2)=2m+1 is a strict majority. If C candidates survive, C ceil(L/2)≤LqT. Thus C≤2qT≤M/4 on every tape, including complete statistical failures. Aggregation and exact medians operate on the canonical actual candidates produced by the executed bucket/location stages.

## 7. Fairness, fresh estimation, Cartesian medians and simultaneous probability

Each fixed-width tape block is decoded as σ=2A+1 from m−1 bits and τ from m bits. This is a bijection from {0,1}^(2m−1) to all odd-slope/shift pairs. The 2L disjoint blocks give a product bijection. Under the specified independent uniform tape law, all pairs and their two coordinates have exactly the required independence. No rejection sampler, selected successful tape, deterministic PRNG guarantee or physical entropy claim is hidden here.

For each heavy i, missing the strict location majority requires at least h=ceil(L/2) bad independent rounds. With per-round bad probability ≤1/16, union over h-element subsets gives

    Pr[location majority fails at i]≤binom(L,h)16^(−h)≤2^(−L).

Union over at most M heavy indices costs M2^(−L). For estimation, define the ideal e_i for all M indices as mathematical functions of the fresh L estimation pairs. They need not be computed. The same bound and a union over all indices cost another M2^(−L). Dependence across frequency indices is irrelevant to that union bound.

Equivalently one may condition on the complete location transcript: it fixes the actual candidate set, while estimation pairs remain fresh and independent. One may not condition on a selection event produced by shared estimation randomness; the source uses disjoint roles, so that prohibited conditioning is absent.

On the joint good event, every included coordinate has a strict majority of ideal complex estimates within a of its true value; actual estimates are within η of their ideal values. Therefore more than half of both Cartesian estimates lie in their respective intervals of radius a+η. The exact odd-length Cartesian medians cannot leave those intervals. Their complex error is ≤√2(a+η)<2a. The good subset may depend on the coordinate; a universal good row set is unnecessary.

All heavy coordinates were included. Every omitted coefficient has magnitude <4a, so assigning it zero is valid. Since k≥M^(2β), 4a≤4M^(−β)R. Finally

    2M2^(−L)=2·2^m·2^(−4m−1)=M^(−3).

This is one event controlling all Fourier coordinates for every fixed permitted input. It is not one fixed tape that works for every input. Neither an additional N-coordinate union bound downstream nor an extra rounded-window leakage term is needed.

## 8. Every-tape magnitudes and resource regimes

On all tapes |b_j|≤A and actual estimates have complex magnitude ≤A+η<3M². Each returned Cartesian median is one represented Cartesian estimate. Thus its Cartesian magnitude is <3M² and its P-grid numerator is <2^(P+2m+2), exactly the needed outer accumulator input envelope. The complex norm of a Cartesian median need not equal a single estimate's norm; the report only uses the correct Cartesian bound.

The paid window has O(r²ℓ) coefficient cells with O(r logℓ)=O(m²) bits. Normalizer construction has O(T) terms on a common dyadic grid. Supported taps number W=O(Bm); roots number O(B). The source performs 2L real bucket runs, each with W source reads and B log B exact FFT operations. Location sorts, bounded modular inversions, explicit memberships and candidate aggregation are paid. Estimation prepares phases for the actual candidates, and exact median sorts are paid. Retained diagnostic arrays and tuple/reference allocations are included rather than described as an unimplemented streaming scheme.

With exponent values F=O_d(m), source alignment and each exact FFT layer produce O_d(m²)-bit numerators/exponents. A source coordinate has numerator ≤2^e and e≤F, so there is no extra unbounded numerator promise missing. Scalar intermediate widths are polynomial in m, dyadic additions align to common exponents, and the constructed general E_B certificate has exponent P(b+2)=O(m²). Fixed-size diagnostic dictionaries have fixed field counts, not constant integer widths; their variable widths are retained by the ledger.

The resulting shape is (B+T+qT)poly_d(m+h)+poly(m+h), where h is the exact β-field width. For fixed β, h is constant. Since B<2M^(1/2+β), T≤M^(1/2−β)≤B and qT≤1024M^(1/2+β), the stated fixed-parameter bound follows. The fair-tape decoder's O(m⁴) work and O(m³) cumulative auxiliary storage are absorbed. No recovery-success premise is used to bound storage, loops or widths.

Actual source sparse eligibility can begin at enormous M. Reduced fixtures are not source-parameter executions. For fixed β<1/2 the guards eventually hold because B/k grows polynomially and W/M→0; this asymptotic fact neither supplies a physical large-scale run nor makes the unimplemented exceptional branch part of this acceptance.

## 9. Excluded-domain witnesses and outer algebra

The reduced-window witness is correct. For M=64, B=4, r=1, ℓ=32 and j=32, the Dirichlet convolution contains twelve odd residues in {20,…,44}. Each has Φ≥1/1024 and C≤9, so G_32≥1/768>64^(−4). A compact certified window with arbitrary reduced r does not inherit source leakage. Source r=2m+1 is essential; this is not an in-domain counterexample.

The tiny-source witness is also correct. At m=46, β=1/4, B=2^35, k=2^23, P=752 and F=849, constant v_t=2^(−849) meets the source sparse guards and has linear exponent value, but R=2^(−826)<1/2. Before bucket rounding, linearity and the accepted ℓ₁/root/scale bounds give modulus <4M²2^(−849)=ρ/8. Every bucket, phase estimate and median therefore rounds to zero on every tape. Since 4M^(−β)<1, this violates a falsely extended scale-free guarantee. It validates the necessity of the normalization premise rather than refuting the accepted theorem.

The outer-interface algebra in the audit is consistent with the recovered edition. Given the separate interpolation premises and βm≥2, the error bracket is bounded by (14t+14)M^(−β)=(448Dm+70)M^(−β), and the strict gap β−α absorbs m. J=2r_amp−1 fresh full calls, r_amp=floor(c)+2, incur the extra Cartesian √2 and failure ≤2^(2r_amp−1)M^(−r_amp)≤(1/2)N^(−r_amp)≤N^(−c), since M≥4N. This uses the conservative 1/M front-end failure, even though M^(−3) is available.

These elementary interface consequences are checked here. P05 interpolation, active coefficient generation, outer incidence/scatter implementation, complete accumulator implementation, dense dispatch and J-call wrapper are not re-certified by that algebra. No broader acceptance is implied.

## 10. Remaining gates and claim language

Closed by this review, conditional on pinned numerical contracts: all-frequency exact window bounds; support-to-unwindowed-transform identity; source-parameter numerical margin; odd-slope collision law; shift orthogonality; total energy; robust top-q selection including ties; complete inverse fibers and votes; fresh estimation conditioning; Cartesian medians; simultaneous M^(−3) probability; every-tape support/magnitude envelopes and fixed-parameter source-model cost.

Continuing hypotheses: fixed globally valid immutable normalized source; bounded Cartesian amplitudes; numeric F=O_d(m) and fixed β for cost; independent uniform tape; trusted finite-arithmetic numerical component contracts. These are explicit assumptions rather than undisclosed missing internal recovery lemmas.

For an expanded executable claim, still required: paid full raw parser/global validator, zero/max-normalization and a compatible centered source adapter; exact all-length dispatch and certified dense fallback; active interpolation coefficients and scatter; finite accumulators, final rounding and exact scale-back; independent J-call amplification; source-pinned full-path conformance and complete input/output accounting. Separately accepted components do not establish their composition automatically.

Outside this acceptance: physical entropy, arbitrary seeded-randomness security, Python/interpreter/allocator certification, host exhaustion, practical speed or crossover, missing historical archives, worldwide novelty, full all-length integrated execution, exact DFT, relative-ℓ₂ recovery and a general FFT improvement. The result is an implementation bridge for an existing weak unitary-coordinate theorem, with unchanged analytical exponent.

No production source, accepted dependency, Sheet, GitHub repository, publication or sharing permission was modified. The new review packet is private.
