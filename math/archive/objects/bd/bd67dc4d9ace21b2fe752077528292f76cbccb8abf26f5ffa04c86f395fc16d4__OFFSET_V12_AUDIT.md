# Offset-class v12: independent mathematical and provenance audit

Audit date: 9 October 2026. This report concerns **fft_offset_class_joint_v12(1).zip**, the offset-class archive. It does not concern the differently named centered-v12 archive or any later composite-Green construction.

## Verdict

The central positive result is sound in exact arithmetic with an explicit half-up rounding convention and the inherited legal prime-power block regime: an unbiased, exact-center, full-output randomized row with per-output variance at most `(M/N)||x||₂²`, using `L=N/gcd(N,Q)` modulated prime-power evaluations. Fixed-cofactor families admit linear-arithmetic-work rows when `M=Θ(log Q)`.

This is an approximation theorem, not an exact FFT. The high-probability accuracy and row count must be stated together. The restricted scan-state rank argument is valid after specifying post-cut queries and a linear-state/no-reread model; it proves neither an `Ω(RN)` Fourier lower bound nor a barrier to analytic pre-materialization fusion.

There are two important implementation/provenance qualifications:

1. The literal prototype repeatedly calls sorted uniqueness validation; its claimed linear fresh-input row cost is not established for all allowed NumPy implementations. A deterministic linear-time structural plan is supplied below and independently checked.
2. The archive's claim that the preceding v11 archive omitted `unit_step_core.py` is **not true of the exact preceding v11 artifact in this chain**. That earlier ZIP contains a byte-identical core. A different omitted-core export remains possible but unverified.

No uploaded Python file was executed or imported. The supplied 27-test log and benchmarks are archived claims, not rerun results. Only the reviewer-owned independent checker in this supplement was executed.

## 1. Artifact identity and lineage

Reviewed Library source: `[private-id]`.

- Original offset-class ZIP: 42,700 bytes; SHA-256 `89b05db6afc7e0e868cf647a08aaae18dc0baab6b3ed10ed28bf30e91cc82978`.
- All 17 entries in its embedded `MANIFEST.sha256` match extracted bytes.
- Included `unit_step_core.py`: SHA-256 `6a95e865e6489abd11d312d0b46336e7b2a21320ffff054ada74f145a5130182`.
- This exactly matches `fft_unit_step_chirp_v9/prototype.py` in the earlier v9 ZIP, SHA-256 `4fb1574ed84c3beb1a3a4f33f116b139952ba9452495815cf47573d79a2aa5e4`.
- It also exactly matches `fft_all_length_fused_fp_v11/unit_step_core.py` in the supplied prior v11 ZIP, SHA-256 `cea5b07e13545b38db58655e68cca1617e2f172ce9ba20b88d33c37963544e31`.
- Included `v11_fused_reference.py`: SHA-256 `25590a19d0fb466e27a89da776a0abcd1dd3c0cd5fbf51183875426f14d58d8c`, exactly matching that prior v11 ZIP's `prototype.py`.

Thus the mathematical dependency is identifiable and byte-stable. The specific alleged standalone failure cannot be reproduced as a missing member of this chain's v11 ZIP. Source files remain unchanged; this audit records the discrepancy separately.

Provenance context supplied with the audit request: the saved conversation “Broken chain,” assistant message `[private-id]`, [conversation]([private source omitted]), explicitly retracts an earlier standalone-v11 claim and reports a missing-core cold run. That is an admission concerning some export, not evidence that this exact earlier ZIP lacks the member. The conversation-generated v12 Library artifact `[private-id]` has not been byte-compared with the uploaded offset-class source reviewed here. This footnote records supplied source context; it does not conflate the artifacts.

## 2. Correct exact-grid theorem

Let `Q≥N≥1`, and define

    j_k = floor(kQ/N + 1/2),    r_k = kQ - N j_k,    θ_k = r_k/N.

This fixes ties towards the larger integer, so `θ_k ∈ [-1/2,1/2)`. Merely writing “round” is insufficient. With ties-to-even, `N=6,Q=9` produces residuals `0,-1/2,0,+1/2,0,-1/2`: three classes although `N/gcd(N,Q)=2`. The source's integer formula implements the correct half-up convention.

Write `d=gcd(N,Q)`, `N=dL`, `Q=dq`, so `gcd(L,q)=1`. The residues `kq mod L` exhaust the `L` possibilities, and the half-open centering map is injective on those residues. Hence there are exactly `L` classes.

Stronger constructive form:

    θ_(k+L) = θ_k,    j_(k+L) = j_k + q.

The classes are exactly the index sets `{r, r+L, r+2L, ...}` for `0≤r<L`; each contains `d` targets. This needs no sorting or hashing.

The right-endpoint wrapping branch in `exact_nearest_grid_map` is unreachable. Indeed `k≤N-1` gives `kQ/N≤Q-Q/N≤Q-1`, so `j_k≤Q-1`; `j_k≥0` is immediate. This includes `N=1`. Adjacent indices differ by at least one because `Q/N≥1`, proving injectivity directly. Neither wrapping nor repeated centering loops are required under the declared domain.

The grid helper accepts `N=1`, but `next_prime_power(1,p)=1` is rejected by the v9 prime-power core; the adaptive planner also passes tolerance one to a routine requiring tolerance below one. An explicit identity fast path is required for an all-positive-length executable interface. This is an edge-case implementation defect, not a failure of the mathematical identity.

## 3. Exact modulation and shared-state variance

For a class value `θ`, let `yθ[n]=x[n] exp(-2πinθ/Q)` for `0≤n<N`, padded by zeros to length `Q`. Since `(j_k+θ_k)/Q=k/N`,

    sqrt(Q/N) (U_Q yθ)[j_k] = (U_N x)[k].

The scale factor is essential because both transforms are unitary. Also `||yθ||₂=||x||₂`.

Let `A_s` be the exact prime-power random row for state `s=(a,β)`, with `a` uniform among units modulo `Q` and `β` uniform modulo `Q`, independently. If `E A_s=U_Q` and the one-output error covariance has operator norm `M/Q`, then

    E Xhat_k = (U_N x)[k],
    E |Xhat_k-(U_N x)[k]|² ≤ (M/N)||x||₂².

The argument uses only the marginal distribution of the state assigned to a class. Reusing the same state across every class is valid; it generally correlates different output errors. Independence is needed between repeated complete rows when using the binomial/majority tail bound, not between classes within one row.

“Exact center” means exact expectation of the ideal randomized estimator. It does not mean the realized row is an exact Fourier transform, or that floating-point code is exactly unbiased.

## 4. Independent derivation of the inherited sharp covariance

The legal regime is `Q=p^E`, `M=p^m`, `K=Q/M`, `K≥M`, with `Q≥2` and `M≥1`. Merely writing `M|Q` omits `M²≤Q`, which the actual core enforces.

Within block `r`, local phase `S[r,t]` has modulus one. The sketch forms the rank-one block operator `P_s[r]=conj(S_r) S_rᵀ`; the complete row is `U_Q P_s x`. Uniform `β` kills every off-diagonal within-block phase, so `E P_s=I` and the row is unbiased. The odd-modulus half-step twist is deterministic and does not change the covariance.

For input position `i=rM+u`, put `D_u={u-t:0≤t<M,t≠u}`. Averaging first over `β`, then over units `a`, gives the zero-frequency error covariance

    C[i,j] = (1/Q) sum_(d in D_(i mod M) ∩ D_(j mod M)) c_Q(d(j-i)),

where `c_Q(t)=E_(a unit) exp(2πiat/Q)` is the normalized Ramanujan sum. Other output frequencies conjugate `C` by a unitary diagonal, preserving its spectrum.

For prime powers, `c_Q(t)` is `1` if `Q|t`, `-1/(p-1)` if `Q/p|t` but `Q∤t`, and `0` otherwise. Each nonzero displacement has p-adic valuation below `m`. Since `E≥2m`, a nonzero covariance entry must have `i≡j mod M`. For each fixed `u`, the remaining `K×K` block is circulant.

Fourier-diagonalize in the block index. For mode `ℓ mod K`, its eigenvalue is

    λ_ℓ = (1/M) sum_(d in D_u) Pr_(a unit mod K)[a d ≡ ℓ mod K].

If `v_p(ℓ)=v<m`, the number of `d∈D_u` with valuation `v` is `(p-1)p^(m-v-1)`, because `D_u` represents every nonzero residue modulo `M` once. The probability for each such displacement is `1/φ(p^(E-m-v))`. Therefore `λ_ℓ=1/K=M/Q`. If `M|ℓ`, it is zero. There are `K/M` zero modes for each of the `M` values of `u`, giving total nullity `K` and active rank `Q-K`.

Consequently

    C²=(M/Q) C,     spectrum(C) ⊂ {0,M/Q},

which proves the sharp operator bound independently of the supplied tests. For `M=1`, the covariance is identically zero and the row reduces to an ordinary full-length FFT; the upper bound is then non-sharp.

## 5. Charged complexity and a bounded constructive repair

A theorem-level implementation can charge:

- prime/lift/block selection and exact grid/class preparation;
- state sampling and state-dependent phase/index/gauge preparation;
- `L` input modulation/padding passes;
- `L` block-summary passes;
- `L` length-`K` FFTs;
- `L` length-`Q` balanced scans;
- selection of all `N` outputs.

With constant-cost field arithmetic, root evaluation and word-sized exact index arithmetic, this is

    O(N + Q + L[Q + K log K]) = O(L[Q + K log K]),
    workspace O(N+Q),

with one class alive at a time. Materializing all classes instead uses `O(LQ)` workspace. The library FFT is a charged kernel, not a removed computation. Random state sampling is expected constant attempts for a fixed prime; a deterministic bounded-time claim would need an explicitly specified sampler. Integer bit complexity, random-bit generation and precision-dependent root generation are separate from unit-cost arithmetic.

For fixed `p`, the next prime power has `Q<pN` for `N>1`. The largest legal p-power block below `log Q` is `Θ(log Q)` for sufficiently large `Q` and automatically satisfies `M²≤Q`; finitely many smaller cases are covered by constants. Thus each class costs `O(Q)`. If `N=c p^e` with fixed `c,p` and `gcd(c,p)=1`, then `L=c` and one fresh-input row costs `O(N)` arithmetic operations and `O(N)` words.

### Literal source versus theorem

The source builds the nearest-grid map twice in each row, once directly and once inside `offset_classes`. Each call invokes `np.unique(j)` merely to validate a mathematically guaranteed injection. NumPy's API returns sorted unique values; no linear-time guarantee follows from that call. Depending on NumPy version/implementation it can introduce a sorting cost. Therefore the literal prototype should not be presented as having proved worst-case linear fresh-input runtime solely from the displayed proxy. [NumPy unique documentation](https://numpy.org/doc/stable/reference/generated/numpy.unique.html).

The reviewer-owned `constructive_classes` function in the independent checker replaces this with the exact congruence classes `k mod L`, generates a total of `N` targets, and uses deterministic `O(N+L)` index work. Its correctness was checked against 3,230 exact integer grids. Removing the redundant uniqueness validation and using this structural plan restores the intended arithmetic bound without changing the estimator. This is an audit-side constructive repair; the uploaded source has not been altered.

The work proxies are planning heuristics, not measured instruction counts. `choose_adaptive_plan` returns plan metadata; the archive does not implement a single complete adaptive dispatcher. The Bessel branch has its inherited deterministic truncation and numerical requirements, while the class branch has no Bessel truncation. A cost-based choice must retain the branch-specific error guarantee. Candidate primes are a fixed small set, not an uncharged global factorization search.

## 6. Probability, accuracy, and row count

For `g>sqrt(2)`, define `τ=g sqrt(M/N)||x||₂`. Each real/imaginary coordinate is bad with probability at most `1/g²`. With independent complete rows, the stated three-grid majority theorem gives

    Pr[||Xtilde-U_N x||∞ > (5/sqrt(2))g sqrt(M/N)||x||₂]
      ≤ 2N exp(-R0 D(1/2 || 1/g²)).

The class-sharing correlations do not obstruct this bound: independence is across rows, and the final union bound does not require independence across outputs.

At **constant g** and a specified uniform failure probability `δ`, the displayed sufficient row count is

    R0 ≥ log(2N/δ) / D(1/2 || 1/g²),

rounded up to an allowed odd integer. Thus the advertised near-variance-scale all-output guarantee uses `Θ(log(N/δ))` rows. A fixed-cofactor linear row then yields `O(N log(N/δ))` work at this accuracy. This is what follows from this bound, not a lower bound ruling out all other algorithms or analyses.

There is an important different regime. For any fixed `α<1/2`, one may target the weaker but still shrinking error `ε N^(-α)||x||₂` by choosing

    g = (sqrt(2)/5) ε N^(1/2-α) / sqrt(M).

Then one-row bad probability is `O(M N^(-(1-2α)))`. For `R0=2s-1`, a direct binomial union bound is at most a constant (depending on `R0,ε`) times

    N M^s N^(-s(1-2α)).

For `M=Θ(log N)`, any fixed `s` satisfying `s(1-2α)>1+c` gives failure `o(N^(-c))`. Consequently **a constant number of linear-work rows does suffice for fixed-cofactor all-output high-probability approximation at any fixed power scale N^(-α), α<1/2**. This positive qualification must not be lost by discussing only constant `g`.

The particular saved checks with nine rows and `g=3` demonstrate selected sample errors, not an asymptotic probability theorem or failure-rate estimate. A successful seeded run cannot certify the tail bound.

## 7. Restricted scan-state rank gate

For `R` independent black-box forcing channels, restrict the input to first forcing values `z_r`, with all later forcing zero. The exact cyclic scan has a nonzero common gauge factor times `z_r` at every later position. At a later query with offset `θ_i`, the combined output is, up to nonzero row and column factors,

    sum_(r=0)^(R-1) T_r(2θ_i) z_r.

For `R` distinct such offsets, the Chebyshev evaluation matrix is nonsingular: its degree sequence is `0,...,R-1`, with nonzero leading coefficients, hence it differs from the ordinary Vandermonde matrix by an invertible triangular basis change. Any exact linear state map `S: C^R→C^d` through which all these future queries factor has `d≥R` (complex scalar coordinates).

The model must forbid rereading the discarded channel inputs or writing equivalent information to an uncharged side store. It must count any retained seed/global-summary state. This is an information-transfer cut argument, not an arithmetic lower bound.

### Post-cut qualification

The saved certificate selects the first `R` distinct residuals, including the zero-frequency target at scan position zero. If the cut is after position zero, that first target is not a future query. The numerical rank of the saved matrix is correct, but the certificate should choose `R` distinct **later** query offsets to instantiate the stated cut literally. In the three supplied examples, doing so is immediate: choosing residual numerators `1,...,R` gives exact ranks `8,10,12` for `(N,Q)=(127,128),(255,256),(511,512)`. These corrected post-cut certificates are included in the independent results.

In general, the relevant bound is `min(R,L_after)` where `L_after` counts distinct offsets queried after the cut; it cannot automatically be replaced by the total class count including already-emitted outputs. With an arbitrary gauge depending jointly on channel and query, a diagonal-scaling argument would need additional justification; the inherited shared-state decoder uses the common gauge required here.

This gate does not exclude approximate state compression, nonlinear representations with a different model, low-dimensional structure among actual Bessel channels, or a direct estimator. Its `R`-state requirement alone is much weaker than an `Ω(RN)` time theorem.

## 8. Finite precision and integer range

The exact integer grid formula removes floating-point nearest-grid misclassification only while its stored integer results fit the selected type. The source uses Python integers for some grid products but writes into `int64` arrays. The core uses `int64` products such as `a*j`, `j*(j-1)`, and phase products before reduction; these can overflow at large lengths. The core itself limits its comments to moderate validation sizes. Production code needs checked ranges or exact modular multiplication.

The source's `dtype` argument is not a uniform mantissa parameter: modulation and phase generation and the FFT input are explicitly `complex128`, while casts change portions of decoder storage. NumPy also documents promotion of single-precision FFT inputs to double precision. [NumPy FFT documentation](https://numpy.org/doc/2.2/reference/routines.fft.html). Neither switching `dtype` nor the saved tests certifies an arbitrary-precision implementation or a whole-pipeline binary64 stability theorem.

A useful conditional extension is available. Suppose the inherited complete Q-row contract is

    ||Ahat_s(y)-A_s(y)||∞ ≤ C u log(Q) sqrt(MQ)||y||₂,

uniformly in the state, under exact modular indices, accurate roots, stable short FFT, balanced reductions, adequate exponent range and small `u log Q`. Because each retained output uses only one class, scaling transfers its contribution to

    C u log(Q) Q sqrt(M/N)||x||₂.

There is **no leading L factor** in this per-output error budget. Input-modulation errors and the final normalizer must also be charged. A conservative perturbation bound uses `||A_s||₂→∞≤||A_s||₂→₂=M`; thus a modulation perturbation of norm `η||x||₂` contributes at most `sqrt(Q/N) M η||x||₂`. Sharper row-norm estimates can improve this, but are not needed for a sufficient contract.

For fixed `Q/N` and `M=Θ(log N)`, keeping the inherited decoder contribution below `ε N^(-α)||x||₂` requires, sufficiently,

    u = O(ε N^(-(α+1/2)) (log N)^(-3/2)),

or `(α+1/2)log₂N + (3/2)log₂log N + log₂(1/ε) + O(1)` mantissa bits, assuming the stated root/FFT contracts. This is a conditional arithmetic-precision statement, not a certificate for the fixed NumPy implementation. Bit cost must multiply the arithmetic work by the selected arithmetic/root-generation costs.

Robust aggregation of computed rows also needs to accommodate the deterministic numerical allowance. For example, enlarge the working success radius and bin widths consistently. The code's exact-theorem radius cannot simply be reused without a numerical perturbation argument.

## 9. Independent checks and saved-claim reconciliation

Executed checker: `audit/independent_offset_checks.py`, which imports only the Python standard library and NumPy, never the supplied modules.

Results:

- 3,230 exact integer grid cases: class count, half-open residual range, injection, unreachable wrap, congruence-class construction and exact rational modulation frequencies all pass.
- Ties-to-even counterexample `N=6,Q=9` confirms three classes instead of two.
- Exact Fraction covariance checks for `(Q,M)=(4,2),(8,2),(9,3),(16,4),(25,5),(27,3),(32,4),(81,9)` certify `C²=(M/Q)C` and rank `Q-Q/M`.
- Exact post-cut Chebyshev certificates have ranks `8,10,12` after excluding position-zero output.
- Numerical **all-state, all-input-operator** lifted checks for `(N,Q,M)=(6,9,3),(7,8,2),(12,16,4),(18,27,3),(20,25,5)` verify mean operator, exact-center modulation and covariance eigenvalue bound. Maximum mean entry discrepancy is `6.83e-15`; maximum bound ratio is `1+9.6e-15`, consistent with floating arithmetic. These check an independently assembled dense block operator rather than testing one random signal or importing the source scan.

Exact Fraction identities are exact finite certificates. Dense complex-root calculations are numerical cross-checks, not exact symbolic certificates or a replacement for the general proof above.

The supplied `RESULT_SUMMARY.json` matches the supplied scalar results. Its performance ranges match `benchmark_results.csv`, but the prose in `RESEARCH.md` is stale: recorded stream/Bessel ratios run from `0.869` to `1.493`, and stream/NumPy FFT ratios from `96.59` to `157.34`, rather than the narrower prose ranges. These are archived benchmark measurements; no performance benchmark was independently rerun. They support no practical FFT speed claim.

## 10. Recommended next bounded steps

1. Replace ambiguous “round” with the exact half-up formula and state `Q≥2`, `M²≤Q`, plus the `N=1` identity fast path.
2. Use the exact congruence-class plan to remove sorted uniqueness validation; cache input-independent grid structure without hiding its one-time cost.
3. Keep exact-center class and biased/truncated Bessel branch error guarantees explicit in any adaptive dispatcher.
4. Parameterize the accuracy and failure probability together when discussing linear-time high-probability approximation.
5. Correct the post-cut rank certificate and avoid presenting the rank gate as a time lower bound.
6. Correct or identify the separate v11 export underlying the missing-core claim; retain byte-exact provenance.
7. If pursuing numerical implementation, specify and certify the modular-integer, roots, FFT and aggregation interfaces before claiming fixed-precision stability.

This audit provides no novelty verdict. The source itself treats the rational-grid identities as elementary and disclaims a novelty proof; that remains the appropriate boundary.
