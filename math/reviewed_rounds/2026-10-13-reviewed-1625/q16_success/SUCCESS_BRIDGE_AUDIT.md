# Q16 sparse success contract bridge audit

13 October 2026 UTC

## Decision and scope

**The sparse success bridge is established on the explicitly promised input domain, using the pinned accepted numerical component contracts.** The universal arguments below establish the missing analytic link from the implemented supported-window buckets and fair-tape product law to simultaneous unwindowed unitary Fourier-coordinate accuracy. No unproved flat-window, isolation, total-energy, location-selection, median-conditioning or union-bound lemma remains within that link.

Precisely, the reviewed source-parameter route, on a fixed globally valid immutable normalized source and an independent uniform tape, satisfies

    Pr[ ||ztilde - U_M v||_infinity <= 4 M^(-beta) ||v||_2 ]
        >= 1 - M^(-3).

This is an implementation-to-existing-source-theorem bridge: it freshly audits and instantiates the recovered PROOF sections 2-7 for the pinned current implementation. It is not a new recovery construction, new mathematical Fourier theorem or new analytical exponent. The normalized coordinate error remains exactly 4 M^(-beta) ||v||_2 for the negative-sign unitary transform.

This result is restricted to the sparse branch and the mathematical finite-arithmetic source model. It inherits the numerical component contracts; it does not repeat every scalar-enclosure proof or certify the Python interpreter. It is not a new full all-length theorem review, complete E(beta) dense/sparse executable acceptance, full raw-input validator, physical entropy certificate, or outer-transfer implementation. The recovered edition acceptance was edition QA with inherited premises; its label was not used as a substitute for this proof.

The distinction between a promise-domain theorem and input validation is essential. Global source validity, normalization and independence are explicit theorem hypotheses. Their absence from a sublinear API's eager checks does not invalidate a theorem on inputs satisfying them. A new claim to accept arbitrary raw inputs and establish those promises would require a paid wrapper. Two counterexamples in section 10 demonstrate why the promises and parameter restrictions cannot simply be dropped.

## 1 Exact evidence and execution boundary

The inspected latest fair-tape acceptance archive has SHA-256

    7ce0c1074c2143bf03e33f664d4cadc58ebce62089a3d8b48b3d65d137c2ec47.

All six scientific modules in this audit were read directly from that archive and checked byte-for-byte against the inspected source. The files are copied under `sources/` for reproducible reference. `PROVENANCE.json` contains the member paths and full hashes.

- `PROOF.md`: 0bc9c71af3f084f465aeadd3a4c53122abb6b11673d25f5d5d87c43ca57a675b
- `ALGORITHM.txt`: 17240b411c59c51f579d5675f6ac80975ca86553714ad5d8296594bc71dc6cc1
- `compact_window.py`: e29741e71c276c156d708f1d9dce6d60ff9d3d2c34a6045b03630c46506dac59
- `buckets.py`: df3937a632217a8a1342545b803169ff8da062117b3837796386509b64f650d1
- `location_decode.py`: e3b592c40906d860d58c12cf7e21f17c6560cb8c95e7bcde4c161b0d52881c3a
- `phase_medians.py`: 45c0c6a59cac18912278dcda183fe8e5bea2a19398cb61fc1bf8ec97cac5a788
- `pipeline.py`: c3a2da5a11ceba2cfa0df7bbb346525013e740e7bc170b3d27dfadc3f2be4d3b
- `fair_tape.py`: 252d154e654d58bac4a9dddaaddcec939607801efc8ad6d9babd2c9cf8d260c4

The recovered edition and the actual window, bucket, location, phase/median, deterministic-pipeline and fair-tape acceptance reports were also inspected and copied. The edition report explicitly excludes a fresh full E(beta)/P05 audit. Every component's narrower scope is retained here.

No scientific production module, old program, producer test suite or historical reviewer program was executed in this audit. The only new execution was `controls/proof_controls.py`, an independent exact-integer/rational algebra, finite-geometry and source-hash control. Its finite results corroborate the universal proofs; they do not establish them by sampling.

## 2 Complete promise and parameter ledger

### Mathematical input hypotheses

1. M=2^m and beta is one fixed rational in (0,1/2). For the executable beta is an exact normalized Fraction, not a float. Fixed-parameter asymptotic constants may depend on beta; a uniform varying-beta encoding has a separately paid width h.
2. k=2^ceil(2 beta m), B=2^ceil((1/2+beta)m), T=M/B, r=2m+1, ell=8B, W=2r(ell-1)+1, q=512k, L=4m+1, P=16m+16, rho=2^-P, delta=M^-4.
3. Sparse eligibility requires B dividing M, B>=4, T>=4, B>=4096k and W<M. Since M,B are powers of two, g=T/4 and H=3T/4 are integers. In particular B<=M/4, k<=M and q<=B. This route rejects failures; it does not execute the proof's dense branch.
4. v is one fixed complex vector before the tape is chosen. Every Cartesian coordinate has magnitude at most one, and R=||v||_2>1/2. The full represented source is deeply immutable and globally valid. For the cost statement, each exponent value is at most F=O_d(m), not merely represented by O(m) exponent bits; numerator widths then are O_d(m). The recovered outer normalization supplies F<=dm. The numerical success proof itself does not need an asymptotic F restriction, but the stated cost does.
5. The tape is uniform on {0,1}^n, n=2L(2m-1), independent of v and all pre-tape data. The code accepts any concrete valid tape; fairness and independence are properties of its input law, not properties certified by examining its bits.
6. The accepted exact-dyadic numerical and finite-source-machine contracts hold for the pinned components. There is no adversarial monkeypatching, private-state forgery, concurrent mutation or host exhaustion inside that model.

### What the actual route establishes

`fair_tape.py` lines 178-189 derive k, q and the tape plan internally through `theorem_spec`; lines 228-239 offer the source sparse route. `compact_window.py` lines 251-325 establish the exact window geometry, source r/P/B relations and sparse guards. `fair_tape.py`'s fixed block decoder supplies exactly L location and L estimation pairs; its accepted product-bijection proof supplies mutual independence conditional on hypothesis 5. No supplied candidate, schedule or bucket can bypass the source route.

`pipeline.py` performs real preparation, actual BUCKETS calls and exact downstream forwarding. Its internal identity bindings link each bucket to the same source, spec, affine pair and role; estimation uses the actual canonical candidate object. Thus the analytic variables below describe executed data, not arbitrary well-shaped supplied rows.

The pipeline checks the source header; BUCKETS validates each queried sample. Neither claims to scan unsampled coordinates, infer R, normalize v or test physical independence. These are promised-input boundaries, not an additional probability failure term. Source storage is a represented length-M tuple; it is caller-owned and excluded from auxiliary cost. A caller constructing that tuple must pay O(M) fields.

The outer guards beta*m>=2 and t<M are deliberately not front-end hypotheses. The former is used to simplify the outer error constant, and the latter to define distinct interpolation incidences. Neither is needed for this sparse-coordinate theorem.

## 3 Exact supported window to flat response

This section freshly discharges PROOF section 2, equations (1)-(3), including all-frequency claims absent from finite fixtures.

Let U,U' be independent uniforms on {0,...,ell-1}; define F as the mass function of the sum of r copies of U-U'. Equivalently its coefficients are those of (1+...+X^(ell-1))^(2r), centered at r(ell-1), divided by ell^(2r). Symmetry of the uniform law verifies this equivalence. F is nonnegative, even, sums to one, and has W supported integer positions. W<M makes these positions distinct modulo M.

For omega=exp(2 pi i/M), the characteristic function is

    Phi_j = sum_t F_t omega^(-jt)
          = |ell^(-1) sum_(u=0)^(ell-1) omega^(-ju)|^(2r).

It is nonnegative, at most one and Phi_0=1. At circular distance d=|j|_M in [g,M/2], concavity of sine on [0,pi/2] gives |sin(pi j/M)|>=2d/M. The geometric sum therefore has normalized magnitude at most M/(2ell d)<=1/4 because ell*g=2M. Thus Phi_j<=16^-r outside the central arc, including its endpoints. At zero no sine division is used.

Put C=sum_(j=-g)^g Phi_j, D_H(t)=sum_(u=-H)^H omega^(ut) and w_t=M F_t D_H(t)/C. Then 1<=C<=2g+1. Expanding D_H gives the exact normalized response

    G_j = M^(-1) sum_t w_t omega^(-jt)
        = C^(-1) sum_(u=-H)^H Phi_(j-u).

This algebra has the same factor M and signs as the implementation. All terms are nonnegative. There are 2H+1<M distinct residues in the last sum because B>=4 and T>=4.

If |j|_M<=T/2, choose a signed lift in [-T/2,T/2]. The interval [j-H,j+H] contains [-g,g], since H-T/2=g. Its central terms therefore contribute C. Every other residue contributes at most 16^-r. For an arbitrary j, the central terms contribute at most C. If |j|_M>T, circular reverse triangle inequality gives |j-u|_M>|j|_M-H>T-H=g for every |u|<=H. Consequently

    1 <= G_j <= 1+delta     for |j|_M<=T/2,
    0 <= G_j <= delta       for |j|_M>T,
    0 <= G_j <= 1+delta     for all j.

Here (2H+1)16^-r <= M16^-(2m+1)=2^(-7m-4)<=2^(-4m)=delta. No finite list of checked frequencies is used. Also |D_H(t)|<=2H+1 and sum F=1 imply sum_t |w_t|<=M(2H+1)<=M^2.

The accepted compact-window contract returns taps within rho of exactly these w_t. Rounded taps do not inherit exact nonnegativity or exact flatness. That is unnecessary: all flat-response analysis is for the ideal w/G, and the uniform numerical error bound below transfers it to the actual computed buckets. There is no extra, unbudgeted rounded-response leakage term.

## 4 Executed buckets and numerical constants

Write z=U_M v with the negative-sign unitary convention. The actual engine folds taps at t mod B, computes the negative-sign unnormalized B-point FFT and scales by 1/sqrt(M). Its ideal target is therefore

    b_j = M^(-1/2) sum_t w_t v_(sigma*t+tau) omega^(-jTt)
        = sum_i z_i omega^(tau*i) G_(jT-sigma*i).

The second equality follows by inserting the unitary inverse transform and the preceding response identity. Tau contributes a positive spectral phase; sigma multiplies the frequency. This matches `buckets.py` lines 178-207 and the accepted direct composition. There is no missing factor B or M.

Let b=log2 B and A=2M^2. The accepted bucket contract's exact general certificate, actually constructed in `buckets.py` lines 141-155, is

    E_B = (A+2W rho)(1+rho)^(b+1) - A + rho.

It follows from the l1 bound, per-tap error, one root path per FFT input/output pair, approximate scale and final complex rounding. This formula applies before invoking any successful-recovery event.

For source parameters, b<=m and (m+1)rho<=1/2. For integer n>=1 and n*rho<1, the binomial coefficients satisfy binom(n,j)<=n^j, so (1+rho)^n<=1/(1-n*rho). Hence (1+rho)^(b+1)<=1+2(b+1)rho<=2. Using W<M,

    E_B <= [4(m+1)M^2 + 4M + 1] rho
        <= 24(m+1)M^2 rho.

The code's generic certificate thus implies the source simplified bound universally, not only at tested precisions. The ideal bucket has magnitude <=A. The accepted phase code freshly certifies p_hat approximating p=omega^(-tau*i) with complex error <=rho, multiplies the actual bucket exactly and rounds once to the P grid. Therefore

    |e_tilde_i-e_i| <= (1+rho)E_B + A rho + rho
                   <= 64(m+1)M^2 rho =: eta,
    e_i = omega^(-tau*i) b_(h_sigma(i)).

The hash in `phase_medians.py` lines 147-151 is h_sigma(i)=floor(((sigma*i mod M)+T/2)/T) mod B. The estimator does not divide by G. Neither the code nor this argument assumes an ideal and computed sort order agree.

Set a=R/sqrt(k) for analysis only. Since rho=2^-16 M^-16,

    eta = (m+1)M^-14/1024 <= M^-13/1024 <= 1/(8 sqrt M) < a/4.

The last strict inequality uses R>1/2 and k<=M. No norm query is required. In particular E_B< a/4, as needed for robust location. The error budget depends on normalization; it is not scale invariant for arbitrary tiny inputs.

## 5 Hash displacement and total energy

For nonzero d modulo M, write d=2^s u with u odd and Q=M/2^s. A uniform odd sigma modulo M induces a uniform odd sigma*u modulo Q; each odd residue has the same 2^s lifts. For 0<=c<=M/2, the event |sigma*d|_M<=c is empty if c<2^s. Otherwise the number of odd residues in the symmetric arc of radius c/2^s is at most 2c/2^s. There are Q/2 odd residues. Thus

    Pr_sigma[|sigma*d|_M<=c] <= 4c/M.

This bound does not assume d is invertible. It remains valid at endpoints and when Q=2. The center of the target bucket depends on sigma, so it must not be treated as an independent random center.

For fixed sigma, h=h_sigma(i) obeys |hT-sigma*i|_M<=T/2. If |hT-sigma*l|_M<=T then |sigma(i-l)|_M<=3T/2. Since B>=4, 3T/2<=M/2 and the preceding displacement bound gives probability <=6/B. This is the exact isolation substitute needed here; no stronger pairwise-uniform hash assertion is used.

Conditional on fixed sigma, tau remains uniform and independent. For l!=i the characters omega^(tau(l-i)) have zero mean, and distinct l have zero cross inner product. Expanding the squared error gives

    E_tau |e_i-z_i|^2
       = |G_(hT-sigma*i)-1|^2 |z_i|^2
         + sum_(l!=i) |z_l|^2 G_(hT-sigma*l)^2.

The self term is bounded by delta^2|z_i|^2. Each other response is at most 1+delta<=2 inside distance T and at most delta outside. Averaging the near event and using Parseval sum_i |z_i|^2=R^2 yields the conservative source inequality

    E_(sigma,tau) |e_i-z_i|^2 <= (24/B+2delta^2) R^2.

Markov then implies

    Pr[|e_i-z_i|>a] <=24k/B+2kM^-8
                     <=24/4096+2M^-7 <1/128.

The last comparison already follows for M>=4: 24/4096=48/8192, and 2*4^-7=1/8192, giving 49/8192<64/8192. Actual source guards are much stronger.

For location we additionally need a count of competitive buckets. Orthogonality in tau gives, for every sigma,

    E_tau sum_j |b_j|^2 = sum_i |z_i|^2 sum_j G_(jT-sigma*i)^2.

At most three of the equally spaced bucket centers lie within circular distance T of a fixed residue. Endpoint equality can attain three, so replacing this count by two would be unsound. The remaining B centers have response <=delta. Thus the energy is at most (12+Bdelta^2)R^2<=13R^2. If K={j:|b_j|>=2a}, then 4a^2 |K|<=sum_j |b_j|^2, whence

    E|K| <=13k/4,
    Pr[|K|>512k] <=13/2048 <1/128.

No spectral-tail optimality, known support, heavy gap or separate isolation promise is required. This is a total-energy argument, so it applies to arbitrary spectra in the stated time-source domain.

## 6 Robust location and exact decoding

Fix i with |z_i|>=4a. On |e_i-z_i|<=a, its ideal bucket has magnitude at least 3a. Uniform bucket error E_B<a/4 implies its computed magnitude is at least 11a/4. Every bucket ranked at least as high has ideal magnitude at least 11a/4-a/4=5a/2>2a, hence belongs to K.

If |K|<=q, the target bucket cannot be omitted from the q largest computed buckets: omission would give q other competitive buckets in K, in addition to the target itself. This covers computed ties, lower-index tie priority, exact |z_i|=4a, and changed numerical rankings. The decoder performs exact integer squared-magnitude ordering, so it realizes the order used in this argument.

The two preceding probability bounds need not be independent. A union bound gives a one-round heavy-location miss probability <1/64, which is certainly <=1/16.

For any odd sigma, multiplication by sigma is a permutation modulo M. The half-open intervals jT-T/2,...,jT+T/2-1 partition the residues, with exactly T in each cell. `location_decode.py` lines 194-207 enumerates precisely the inverse-sigma images of the selected cells, without a tau translation. Thus each selected target bucket gives the correct i membership, and every location round produces qT distinct memberships.

`aggregate_memberships` lines 225-269 counts exact occurrences and retains ceil(L/2)=2m+1 votes. Its successful output has K_cand<=floor(LqT/ceil(L/2))<=2qT on every tape. With B>=4096k, K_cand<=1024kM/B<=M/4. No success event is used for this cap.

## 7 Conditioning and simultaneous probability

The fair-tape product bijection supplies mutually independent affine pairs across all 2L rounds, and independent sigma/tau within each pair. The first L rounds are location; the second L are estimation. Deterministic shared preparation does not introduce random dependence.

For a fixed heavy i, missing a strict location majority requires at least h=ceil(L/2) bad rounds. For independent bad events of probability at most 1/16, a union bound over h-element subsets gives

    Pr[at least h bad rounds] <= binom(L,h)(1/16)^h
                               <=2^L(1/16)^(L/2)=2^-L.

There is no need for equal success probabilities or a Chernoff approximation. A union bound over at most M heavy indices gives failure <=M2^-L.

Define the ideal estimation values for all M indices as mathematical functions of the same L estimation affine pairs, although only the actual candidates are computed. For each fixed i the ideal bad probability is <1/128<=1/16. The same majority argument and union bound give probability <=M2^-L that any coordinate lacks a strict majority within a. Coordinate events may be arbitrarily dependent; the union bound does not require their independence.

This hypothetical-all-indices method does not condition on a favorable candidate set or charge unexecuted computations. Alternatively, condition on the complete location transcript, which fixes I'; the fresh estimation tape remains independent, and union over |I'|<=M gives the same bound. Conditioning a shared estimation tape on a selection event it helped create would require a different proof; that is not the accepted schedule.

On the joint good event, all heavy indices are included. For each included coordinate, more than half of its ideal estimates lie within complex radius a of z_i, and every actual estimate is within eta of its ideal value. Therefore a strict majority of both real and imaginary values lies within a+eta of the respective component. The exact Cartesian median cannot leave either interval, so its complex error is at most sqrt(2)(a+eta)<2a. The good majority may differ across coordinates; no common majority of rows is assumed.

Every omitted coordinate has |z_i|<4a. Returned zeros remain allowed. Consequently

    ||ztilde-z||_infinity <=4a <=4M^-beta R,
    Pr[failure] <=2M2^-L = M^-3 <=1/M.

This is one simultaneous event over all coordinates for each fixed input. It is neither one tape good for all inputs nor merely a pointwise estimate handed to an outer transform without a union bound.

## 8 All tape magnitude widths and source model cost

The accepted numerical bounds imply |b_j|<=2M^2 and |e_tilde_i|<=2M^2+eta<3M^2 on every tape. Each Cartesian median is one of the represented coordinate estimates, so each output Cartesian magnitude is <3M^2. At exponent P the numerator is smaller than 2^(P+2m+2), exactly the all-tape magnitude premise used by the recovered outer accumulator argument. The numerical output contains only indices and P-grid numerators; polynomial-width diagnostics are separate.

All work is paid independently of recovery success. The actual source contains:

- O(r^2 ell) exact coefficient cells; each coefficient has O(r log ell)=O(m^2) bits.
- O(T) normalizer terms and W=O(Bm) supported taps, with predetermined polynomial-bit scalar calculations. T<=M^(1/2-beta)<=B in the source regime.
- O(B) prepared roots and 2L actual bucket runs, including W source reads and O(B log B) FFT work each.
- L exact bucket sorts; L inversions with O(m) Euclidean steps; LqT explicit memberships and their exact sorts, including per-round validation.
- L estimation runs on K_cand<=2qT actual candidates, each with a fresh paid inverse phase, then exact per-coordinate medians.
- All retained bucket, membership, candidate and estimate traces and the fixed-tape decoder/adapter. The source stores these traces rather than claiming an unimplemented streaming peak.

With F=O_d(m), source-aligned FFT numerators and denominator exponents are O_d(m^2). Coefficient and scalar powering intermediates are polynomial in m; sort indices and loop counters have O(m+log m) bits. The generic error certificate has exponent P(b+2)=O(m^2). The decoder's conservative O(m^2)-bit Euclidean bound remains polynomial. Hence the complete accepted ledger has event count (B+T+qT)poly(m), polynomial observed width, and work/cumulative auxiliary storage

    (B+T+qT) poly_d(m+h) + poly(m+h).

Here h denotes actual beta-field width. For fixed beta, k<2M^(2beta), B<2M^(1/2+beta), qT=512kM/B<=1024M^(1/2+beta), so this is

    O_(beta,d)(M^(1/2+beta) poly(m)).

The schedule alone contributes O(m^4) work and O(m^3) cumulative auxiliary storage and is absorbed. Fixed-width diagnostics have fixed field counts, not fixed integer bit lengths. This bound includes deterministic failures of recovery, but not invalid-input rejection outside the promised domain, externally constructed source/tape storage, physical entropy acquisition, Python VM allocations, I/O or archive serialization. Arbitrary F or variable beta encoding cannot be hidden in the fixed-parameter statement.

An original raw-input wrapper can pay its O(M)=O(N) source construction where M is between 4N and 8N. That would preserve the outer asymptotic envelope, but it is additional executed work, and the current concrete tuple interface is not the recovered edition's implicit centered-source callback. This distinction is an engineering conformance issue, not a defect in the promised-source success proof.

## 9 Relation to the claimed outer coordinate error

The result just established is the exact simultaneous E_M=4M^-beta error and failure <=1/M required by recovered edition section 4. It also supplies its stated on-all-tapes support and <3M^2 Cartesian magnitude bounds. No new analytical exponent follows.

The subsequent outer result remains conditional on its separate P05 interpolation and finite-coefficient contracts. With N>=1, 0<alpha<beta<1/2, fixed c>0, integer d>=1, integer D>alpha+4, M=2^ceil(log2(4N)), t=32Dm+4, s=Dm, eta_C=2^(-(D+3)m), b_out=ceil((beta+2)m), and the outer guards t<M and beta*m>=2, that inherited transfer gives

    |y'_ell-(U_N x')_ell|
      <= [3t E_M+t eta_C(1+E_M)+12*4^-s+2^(1-b_out)] R.

The first term uses the simultaneous source event; the coefficient term uses the per-row t bound; the interpolation tail applies to exact z, not an uncontrolled failed approximation. The normalization lambda rescales this inequality exactly to ||x||_2. For E_M<=1 the bracket is bounded by (448Dm+70)M^-beta. The strict gap beta-alpha absorbs the logarithm into N^-alpha.

With r_amp=floor(c)+2 and J=2r_amp-1 independent complete front-end tapes, the outer Cartesian medians incur another sqrt(2), and failure is at most 2^(2r_amp-1)M^-r_amp<=N^-c. An outer repetition needs J disjoint fresh complete tape blocks; the current single-call scheduler does not itself implement that wrapper. No extra union over N coordinates is needed because each front-end event is already simultaneous.

This paragraph identifies the interface and algebraic consequence, not a fresh audit of P05, its active coefficient generator, retained-index scatter or its dense exceptional branch. Full all-length claims remain at their separate inherited mathematical/engineering boundaries. The error is for the unitary transform; the corresponding unnormalized error has an additional sqrt(N). Relative-l2 recovery, exact DFT and practical speed are not implied.

## 10 Explicit excluded-domain counterexamples

### A supported reduced window need not have source leakage

Use the accepted reduced geometry M=64, B=4, T=16, r=1, ell=32, W=63<M, g=4, H=12. Any allowed reduced P suffices. At j=32, the sum defining G_32 ranges over Phi_d for d=20,...,44. Exactly twelve of these d are odd. For odd d, |sin(pi ell d/M)|=1 and |sin(pi d/M)|<=1, so Phi_d>=1/32^2. Since C<=2g+1=9,

    G_32 >=12/(1024*9)=1/768 >64^-4.

Thus compact support, certified taps and deterministic pipeline acceptance alone do not give delta=M^-4. The exact source r=2m+1 is indispensable. This reduced case is explicitly excluded by `run_source_tape`; it is not a counterexample to the theorem above.

### Removing the norm promise causes an all tape rounding failure

Take source-eligible m=46, beta=1/4, M=2^46, B=2^35, k=2^23, r=93, P=752. Define the valid constant dyadic source v_t=epsilon=2^-F for all t with F=P+2m+5=849. It has Cartesian magnitude <=1 and F=O(m), but R=sqrt(M)epsilon=2^-826<1/2.

Before final bucket rounding, the exact implemented arithmetic is linear in v. Tap magnitudes sum to at most M^2+W rho; every approximate root-path and scale factor has absolute magnitude bounded by (1+rho)^(b+1)<=2. Thus every pre-round bucket has complex magnitude at most

    epsilon*(M^2+W rho)*(1+rho)^(b+1)
        <4M^2 epsilon =rho/8 <rho/2.

Each Cartesian bucket therefore rounds exactly to zero on every affine pair. Every phase estimate and median is zero for every tape. But z_0=R, and 4M^-beta<1 because 16<M^(2beta)=2^23. The required relative coordinate inequality fails at zero with probability one.

This is a concrete reason an arbitrary valid `DyadicSource` cannot be promoted to the normalized success contract. It does not weaken the promise-domain theorem: that input violates its explicit norm hypothesis, and the recovered outer max-normalization would rescale it before calling the front end. The counterexample is proved analytically; no enormous source was allocated or executed.

## 11 Remaining gates classified by purpose

### Discharged within this sparse promise theorem

Exact source parameters and guards; fixed-tape product law conditional on fair input bits; executed-data provenance; ideal supported-window normalization and all-frequency flat response; odd-slope displacement and circular counts; shift orthogonality; total-energy estimate and competitive-bucket count; robust sorting under numerical perturbation; inverse fibers and votes; fresh estimation conditioning; Cartesian median error; simultaneous M^-3 failure; all-tape numerical widths/support; stated source-model auxiliary cost.

### Continuing theorem hypotheses rather than missing internal lemmas

The input is fixed, globally valid, deeply immutable, normalized with R>1/2 and bounded components; the cost additionally assumes F=O_d(m) and fixed beta; the tape is independently uniform; the pinned accepted numerical contracts and stated machine model apply. A theorem may legitimately retain these promises. No runtime scan is necessary merely to state or prove it.

### Required only for an expanded raw input or all length implementation claim

A paid raw-field parser/global validator and max-normalizer; zero handling and centered adapter compatible with the concrete source interface; exceptional dense branch; exact outer branch dispatch; active interpolation coefficient construction and scatter; finite accumulator, final rounding and scale-back implementation; J-call independent amplification; complete input/output accounting and source-bound integration evidence. The presence of any separately accepted component does not alone establish their joint executable conformance.

### Outside both mathematical claims

Physical fair-bit generation or a declared alternative randomness assumption; host-memory/exhaustion guarantees; Python runtime/allocator certification; end-to-end physical I/O and serialization performance; practical crossover; historical archive recovery; novelty or general FFT improvement.

## 12 Primary source context and fresh control receipt

[Hassanieh, Indyk, Katabi and Price, SODA 2012](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf), section 4.2, Lemma 4.3 and Theorem 4.4, give the earlier location/vote/Cartesian-median architecture and a simultaneous infinity-norm guarantee for their algorithm under its own window and parameter assumptions. The paper assumes power-of-two length. Those statements were checked in the primary PDF. This audit does not substitute that algorithm for the code under review or import its constants; sections 3-7 supply the required direct argument for Q16's undivided, total-energy estimator.

`CONTROL_RESULTS.json` records fresh exact source-hash checks, odd-slope counts, circular geometry, exact generic-to-source error comparisons, exact binomial tails, rational parameter cases and the two analytic witness predicates. These controls import only standard-library arithmetic and file utilities. Their counts are evidence about these new controls alone. None is described as theorem-scale recovery execution or a universal proof inferred from fixtures.

No production source, accepted dependency, shared Sheet, GitHub repository, publication or access permission was modified.
