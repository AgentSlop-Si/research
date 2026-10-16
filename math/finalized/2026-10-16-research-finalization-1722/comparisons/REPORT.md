# Three bounded research gates: Gaussian accuracy, normalized frontier, and Boolean orbit recovery

Date: 16 October 2026. Source cutoff: repository commit `0339a31eb6109f0b96074ab8321f8653641e7530`.

## Disposition

- **ALG-036:** the named HIKP sparse-recovery comparison is complete as a qualified norm/measurement/cost nonmatch. The accepted Gaussian posterior theorem is retained; no endpoint `alpha=1/2` theorem is claimed.
- **ALG-042:** the Ailon 2014 hypothesis comparison is complete as a qualified nonmatch to the rectangular/streaming interface. A bounded robust simultaneous-unitary obstruction is proved below. The faster selected-convolution/frontier constructor is still missing.
- **ALG-052:** the named Frobenius-FFT comparison is complete as an orbit-mechanism overlap and field/representation nonmatch. The existing deterministic quantization obstruction extends to randomized finite-message recovery, with all input-dependent metadata charged.

All three full parents remain **TO RESEARCH, priority 34**. None is a new canonical discovery or a historical-priority claim. The census stays **87 closed / 240 open / 327 views**. This report closes the specified comparison/lemma substages only. Exact source histories and earlier acceptances remain intact.

The pinned index has Git blob `08a174c549d5a696b8a156ad5ba4d860a8462646`. Eight actual source/review bodies were read, including the Gaussian probability audit, the normalized-frontier independent audit, and all four Boolean-family reports. `SOURCE_BINDINGS.json` binds their current bytes. Archive-name hashes are not silently equated to sanitized publication-export hashes. No inherited program was executed.

## 1. ALG-036: exact sparse-recovery comparison

### Retained theorem and why its guards matter

For original input `x~CN(0,I_N)`, an independent seed and a measurement-only transcript leave a Gaussian residual in a kernel of pathwise complex dimension at least `d0`. Arbitrary measurable decoders are allowed. Transcript-adaptive linear queries are also covered when the next row is a function solely of earlier responses and independent coins. The norm event is used by inclusion, never by conditioning the Gaussian posterior on a norm cutoff.

The source's density/volume calculation is

`P(success) <= min(1, (4 C^2 N^(2-2alpha))^d/d!) + exp(-(3-ln 4)N)`

conditional on the terminal rank, then averaged. With `d>=cN/log N` and fixed `alpha>1/2`, this is exponentially small for sufficiently large N. It excludes an every-fixed-input high-probability guarantee under that information interface. It neither proves a gate lower bound nor covers a state selected using uncharged input access.

The source also supplies a decisive rank-deficit control: randomly omit one input coordinate and compute the exact transform of the rest. Its all-bin error is `|x_J|/sqrt(N)`, so for each fixed input and `1/2<alpha<1`, failure is at most `C^-2 N^(2alpha-2)`. Thus a merely nonzero deficit is insufficient. The quantity and pathwise nature of the deficit cannot be dropped.

### Named primary theorem

[Hassanieh–Indyk–Katabi–Price, arXiv:1201.2501v2](https://arxiv.org/html/1201.2501v2), Theorem 4.9, gives probability 2/3 of unitary-spectrum error at most `(1+epsilon) sigma_k(y)_2 + delta ||y||_2`, in `O((k/epsilon) log(N/k) log(N/delta))` time. Section 2 restricts lengths to powers of two and discusses precision. Theorem 6.1 instead lower-bounds adaptive samples from a flat orthonormal matrix for a constant-factor best-k-term l2 contract. Its proof uses a separated support family and noisy-information accounting. It is not a kernel-deficit theorem for arbitrary block linear observations.

### Exact norm and model map

Set `y=Ux`, so `||y||2=||x||2`. A sufficient transfer of that l2 certificate into the ALG-036 all-bin scale is

`(1+epsilon) sigma_k(y)_2/||y||2 + delta <= C N^-alpha`.        (1)

This is an explicit additional spectral-tail hypothesis, absent from the arbitrary-input Gaussian barrier. For flat spectrum `y=(1,...,1)`, `sigma_k(y)_2=sqrt(N-k)`. Even ignoring the nonnegative delta term, (1) requires

`N-k <= (C/(1+epsilon))^2 N^(1-2alpha)`.                    (2)

For fixed `alpha>1/2`, eventually no integer `k<N` satisfies (2). This says the displayed l2-to-linfinity certificate cannot establish the strong all-input target; it is not an impossibility theorem for all conceivable adaptations of sparse recovery. More directly, a genuinely sublinear-support reported spectrum misses a unit-sized coordinate of this flat spectrum and cannot meet a tolerance tending to zero.

For `alpha<1/2`, the converse direction is equally invalid: reporting zero for flat y has all-bin error 1 and relative l2 error 1, while its allowed all-bin tolerance `C N^(1/2-alpha)` grows. Consequently the accepted weak-scale positive approximation does not promise vanishing relative l2 error.

The primary sampling lower bound cannot simply be substituted either: it concerns a different recovery norm and a restricted class of sampled rows; the Gaussian theorem allows arbitrary linear queries but requires a pathwise retained-information deficit. Both distinguish every-fixed-input success from a single random map correct simultaneously on every input. Nonlinear sparse decoding is permitted and should not be confused with a fixed linear estimator.

If the output interface requires all N explicit entries, sparse-list materialization costs at least N writes. Filter preparation, sample access and amplification remain paid; a sample bound is not a gate bound. No model-matched runtime improvement follows from this comparison.

**Stop:** the named HIKP comparison is complete. Retain the Gaussian theorem, its quantitative deficit and measurability conditions, the unresolved endpoint/other information-model obligations, and the separate alpha<1/2 positive theorem. No broader survey is silently certified.

## 2. ALG-042: robust simultaneous-unitary realization

### What was already complete

The normalized source and its independent audit already establish an orthonormal antichain frontier W with m rows, `m>=N/4096`, each flat on `2^h` original-input coordinates with `h>=n-L`, where `N=2^n`. The complete marker hypotheses include `b>=7`, `L=2^(b-1)`, and `L+2b<=n`; asymptotically `L=Theta(n/ln n)`.

The accepted `O(NL)` conversion to selected Fourier outputs, the sharpened fixed-graph bound `N(n-2b-1)`, the triangular-chirp identity and the exact simultaneous-unitary bound are historical results. They are not counted as fresh work here.

[Ailon 2013, Theorem 2.1](https://arxiv.org/html/1305.4745v1) supplies the classical matrix-entropy method: a physical two-register unitary operation changes total row entropy by at most two bits. This report uses that method for a coefficient-error extension; it does not claim a new lower-bound technique.

### Robust lemma, full formal-input coefficient contract

Let a circuit begin at the identity on D physical registers, apply g two-register unitary gates, and finish with m distinct registers whose full coefficient rows `v_i` satisfy

`||v_i-w_i||2 <= eta < 1/2`,

where each desired normalized frontier row `w_i` is extended by zeros to the D formal inputs. Then, writing `h2` for binary entropy,

`g >= (1/2) sum_i [(1-eta) h_i - h2(eta)]`

`  >= (m/2) [(1-eta)(n-L) - h2(eta)].`                    (3)

A negative right side is merely a vacuous bound. Fixed eta below one-half leaves an `Omega(N log N)` obstruction under the marker hypotheses.

**Proof.** Fix one row, with desired support S of size `s=2^h`. Both v and w have norm one. Their squared-magnitude probability vectors p and q obey

`(1/2) sum_j | |v_j|^2-|w_j|^2 | <= ||v-w||2`,

by Cauchy–Schwarz applied to `||v|-|w||` and `|v|+|w|`. Coarsen every coordinate outside S into one symbol. The resulting probability vectors have alphabet size `s+1`, total variation delta no larger than eta, and q is uniform on S with zero outside mass.

For completeness, couple random variables P and Q with these laws and mismatch probability delta: match their common coordinate masses, then pair the remaining disjoint masses. Conditional on P, the mismatch indicator costs at most `h2(delta)` bits and, on mismatch, Q has at most s possibilities. Thus

`H(q) <= H(p_coarse) + h2(delta) + delta log2 s`.

Coarsening does not increase entropy, `H(q)=h`, and both `h2(t)` and `t h` are increasing for `0<=t<=eta<1/2`. Therefore the original row entropy is at least `(1-eta)h-h2(eta)`. Sum over the m requested final rows. Other rows have nonnegative entropy. The initial total entropy is zero. For one two-register gate, each column's mass in the two changed rows is fixed, its possible entropy variation is at most that mass, and these masses sum to two. Hence total entropy is at most 2g. This proves (3).

### Zero-initialized ancillas and an original-input-only promise

If ancillas are zero and the actual promise is only `||v_original-w||2<=epsilon`, the full coefficient row is still unit norm but its ancillary coefficients need not vanish. Nevertheless

`||v-(w,0)||2^2 = 2-2 Re<v_original,w> <= 2epsilon`,

because `|<v_original-w,w>|<=epsilon`. For `epsilon<1/8`, take `eta=sqrt(2epsilon)<1/2` in (3). This explicitly pays the weaker lifting. One may not silently substitute epsilon itself when ancillary coefficient mass is unbounded by that stronger promise.

These are deterministic, simultaneous physical-register statements. A per-input randomized guarantee, free copies to a historical output tape, an arbitrary nonunitary circuit or a packed-word primitive is outside (3). The proof is over complex magnitudes; no finite-field entropy lower bound follows.

### Named well-conditioned comparison and exact gap

[Ailon 2014 v1, Definition 2.1 and Theorem 3.1](https://arxiv.org/html/1403.1307v1) treats a square invertible layered state, two-register rotations/one-register scaling, and bounds both the state and inverse norms at every prefix. Its terminal target is the full normalized transform; its potential uses entries of the inverse transpose. A rectangular W has no inverse. A cheap nonunitary selected-output program supplies neither a permitted square completion nor a bound on the needed final potential. Zero-input ancillas, discarded state and a historical output tape do not automatically repair these missing premises. Thus this is a qualified nonmatch, not a stronger lower bound for the present general interface.

**Stop:** the named comparison and bounded robust unitary lemma are complete at their stated scope. The live constructive task remains a fully charged `T_E(N)=o(N log N)` selected-chirp or frontier algorithm. A constant-size affine cover, early-time outputs, causal inverse/full recovery and numerical/bit qualification remain separate gaps. The proved `O(L)` cover does not solve them.

## 3. ALG-052: finite messages, randomization and orbit representation

### Historical scopes retained

The four source bodies distinguish quadratic Boolean rigidity, finite cubic controls, exact conductor-orbit injectivity, one-scalar holomorphic recovery degree, and joint measurement-only stability. None licenses an all-degree arithmetic lower bound. Exact integer/cyclotomic coefficient access can preserve information discarded by a few rounded complex coordinates. High degree alone does not imply exponential circuit size.

### A stronger separation constant and randomized counting lemma

Let `N=2m=2^t`, `t>=3`, and use the complementary binary family

`x(u)=(u,1-u)`, `u in {0,1}^m`.

Let X(u) be its unnormalized length-N Fourier spectrum. All even bins are fixed. If u and v differ in H coordinates, then `||x(u)-x(v)||2^2=2H`. Parseval and the fact that only m odd outputs differ give

`sum_(k odd) |X(u)[k]-X(v)[k]|^2 = 4mH`.

Therefore `||X(u)-X(v)||infinity >= 2 sqrt(H) >= 2`.      (4)

The source used the weaker all-output separation `sqrt(2)`; (4) is an elementary support-aware refinement, not a change to its original valid bound.

**Finite-message theorem.** Suppose the entire information exposed to a decoder about u is a message in an alphabet of at most Q possibilities per independent public seed. Arbitrary randomized encoders and decoders are allowed, with independent private coins and no other input side channel. For any `rho<1`, average success over uniform u in producing all outputs within max-coordinate error rho is at most

`min(1, Q/2^m)`.                                         (5)

Consequently every-input success at least `1-delta` requires

`Q >= (1-delta) 2^m`.                                    (6)

**Proof.** By (4), the radius-rho output balls are disjoint. Fix a public seed. For each message a, let `D_a(B_u)` be the probability that its randomized decoding lands in u's success ball. Disjointness gives `sum_u D_a(B_u)<=1`. With encoding probabilities `E(a|u)<=1`,

`sum_u P(success|u) = sum_a sum_u E(a|u) D_a(B_u) <= Q`.

Average over 2^m inputs and then over independent public seeds. Shared input-independent randomness may be included in the public seed. This proves (5)–(6) without continuity, linearity or a deterministic decoder.

For r fixed or publicly chosen complex odd bins quantized on the source's fixed uniform grid with b fractional bits, its bounded range yields

`Q <= (N 2^b + 2)^(2r)`.

Hence a necessary condition is

`(N 2^b + 2)^(2r) >= (1-delta)2^(N/2)`,                    (7)

and, for `0<=delta<1`,

`b >= N/(4r) + log2(1-delta)/(2r) - log2(N+2)`.             (8)

The strict approximation radius is rho<1 for unnormalized outputs, rho<1/sqrt(N) for unitary normalization, or rho<1/N for normalization by N. Equations (7)–(8) require every input-dependent bin choice, routing field, branch identifier and adaptivity transcript to be included in the message budget. If these choices are not determined by the already counted transcript and independent seed, their additional alphabet size must multiply Q. An arbitrary hidden raw-input read invalidates this interface.

This completes a bounded randomized/approximate-output extension of the finite-precision gate. It does not establish that the necessary precision is sufficient or that generating the measurements is cheap. It does not obstruct an unbounded-precision exact scalar.

### Named primary comparison: Frobenius FFT

[Van der Hoeven–Larrieu, The Frobenius FFT (2017)](https://www.texmacs.org/joris/ffft/ffft.pdf), sections 2 and 4, works over finite-field extensions with base-field inputs, and explicitly charges bit arithmetic, Frobenius operations and representation changes. Its orbit representatives are stored in native subfields: equation (4.1) says their base-field dimensions sum to n. Theorem 6.2 includes field-arithmetic and conversion costs. Orbit reuse is therefore established antecedent machinery; the source is not a theorem extracting all complex conjugates from a rounded numerical scalar. Characteristic, encoding, native-subfield dimension and full-output expansion differ. A normal-basis permutation is not an uncharged complex Galois operation. This is mechanism overlap and a qualified model nonmatch, not worldwide novelty clearance.

**Stop:** the named comparison and finite-message lemma are complete. The original charged shared evaluator with original-input access, higher-degree/rational completion and all explicit outputs remains unconstructed. Its separate singular-denominator, arithmetic, representation, preparation and numerical obligations remain open.

## 4. Verification and application boundary

`checks.py` is newly authored and imports no research code. It checks exact rational entropy inputs and coefficient/ancilla norm identities, exact finite cyclotomic Parseval/separation identities, the randomized-message inequality on rational stochastic matrices, and integer quantization thresholds. Floating entropy evaluations are diagnostics only; proofs above establish all-size claims. Negative controls test dropped message metadata, an erroneously unrestricted approximation radius, a missing odd-support factor, and a false l2-to-linfinity implication.

`PROPOSED_PREFIXES.json` specifies only new leading blocks in current action/pass-stop fields and source-link supplementation. The publisher must recover fresh rich-cell preimages and preserve the full previous cell body, formatting, notes and historical links behind the established history marker. No status, priority, stable-ID, historical proof or novelty-classification edits are proposed.
