# Audit of the all length Taylor Fourier lift

10 October 2026. Source-based mathematical review with independently written finite controls.

## Decision

The dimension-free Taylor lift, its outer rounding ledger, the two stated asymptotic finite-word bounds, and the exact correction-rank formula are accepted at the scope below. No material gap was found in those mathematical arguments. This is a deterministic normwise approximation theorem on represented inputs in a specified word-RAM model. The supplied executable is an on-demand accuracy reference, not an implementation or benchmark of the eager-table asymptotic algorithm.

**Catalogue correction:** the accepted project record already has an all-integer-length normwise compiler under Q01, TH-01 and FUS-01, built on F132. Its final proof is identified below. The present source is an alternative Taylor construction and associated exact-rank diagnostic. It is not the first all-length extension in that combined record, and it does not improve the existing accuracy-dependent upper bound. The earlier theorem and its precision safeguards must remain in place. No discovery-count increment or historical-priority claim follows.

## Sources and review boundary

The inspected archive is `fft_all_length_norm_preserving_2026-10-10.zip`, 52,665 bytes, SHA-256:

`ccbbccc7f25be693d2f20ef69340882ae64f3512e5f68701a81f5e366736e28b`

Its principal text is `fft_all_length_norm_lift/THEORY.md`, SHA-256 `1716f38b2be430287973ea76856c3173770e873d102e4bf339d0084d4c994b77`. Its inherited dyadic proof is SHA-256 `a18a347674000c77f29ad86d5ffad2986b4f1091bcb25a3f9487905216a09f84`, identical to the dependency identified by the accepted earlier all-length proof. All 15 entries in the supplied archive manifest were rehashed successfully.

The source programs were read as text only. None was executed, imported, compiled or parsed into an executable representation. The author's recorded test totals are historical evidence, not tests repeated by this review. The fresh controls accompanying this audit are separate reviewer-authored programs.

The preceding accepted manuscript, *Deterministic normwise Fourier tabulation at every length*, second-pass corrected version, has SHA-256 `c8a775230a824872c23fc48b351e03d63878154bcfb314a8cca689842e31fc8d`. Its stable record is Q01 / TH-01 / FUS-01, with F132 as the dyadic antecedent. Sections 1, 9 and 10 make the precision domain, total quantizer, preparation cap and fallback explicit. Those distinctions are retained here.

## Computational contract

For every integer N, the target is the normalized transform

\[
(U_Nx)_k=N^{-1/2}\sum_{j=0}^{N-1}x_j e^{-2\pi i kj/N}.
\]

The accepted asymptotic statements are:

- For each fixed effectively specified accuracy 0 < ε ≤ 1/4, cold work is Oε(N log N / log log N).
- For an efficiently supplied inverse-polylogarithmic target ε = (log N)^−a, fixed a > 0, or a dyadic target within a constant factor, cold work is Oa(N log N / log log log N).
- Space is O(N) words in either regime. All N numeric outputs are written.

The input has finite binary representation and polynomial dynamic range. A concrete format is xj = (aj + i bj)2^−B, with integer magnitudes bounded by Nc and |B| = O(c log(N+2)), for fixed input-format constant c. Separate exponents in that range can be aligned. An arbitrary real oracle, unlimited exponent range or unlimited precision is not covered.

A machine word has Θ(log(N+2)) bits, with sufficiently large fixed constants in the eventual regime. Integer multiplication and division, addition, comparisons, shifts, bit operations, indexed random access and memory movement are charged word operations. This is an address-capable word RAM, not a unit-cost arbitrary-precision machine. A fixed number of words may implement a bounded-width intermediate. Output values may be explicit dyadic mantissa/exponent pairs or exact dyadic lattice values with a declared common scale. Their descriptions have O(log N) bits per coordinate in these regimes.

The guarantee is deterministic and pointwise for every represented input:

\[
\|\widetilde y-U_Nx\|_2\leq\varepsilon\|x\|_2.
\]

There is no failure probability or fresh-randomness quantifier. It is not a per-bin relative error guarantee, exact preservation of Euclidean norm, correct rounding, an exact-complex arithmetic count, a bit-complexity bound for integer multiplication or a fixed-binary64 asymptotic statement. The rounded backend is nonlinear. Operator norms below concern the analytic channel matrices; the executed backend has an all-input error contract.

**Uniformity qualification:** the source states asymptotic fixed-ε and fixed-a regimes, with finite-size fallbacks. Do not turn this into a stronger uniform claim for an arbitrarily long accuracy target on a fixed C log N-bit address space. A supplied dyadic exponent t = ceil(log2(1/ε)) should be charged, and the accepted older theorem's literal 2 ≤ t ≤ ceil(log2(N+1)) domain and separately charged high-precision fallback should be retained. For either regime reviewed here, q and the backend precision are eventually O(log log N), so this qualification does not change the claimed asymptotic bounds. It does distinguish a mathematical asymptotic theorem from a total production API accepting unrestricted precision.

## Analytic identity and norm bound

Let L be the least power of two at least 2N; hence 2N ≤ L < 4N. Set c = floor((N−1)/2),

\[
h_k=\left\lfloor\frac{2kL+N}{2N}\right\rfloor,
\quad\delta_k=kL/N-h_k,
\quad u_j=4(j-c)/L,
\quad v_k=2\delta_k.
\]

The selected indices hk are distinct and lie in [0,L−1]. Moreover |δk| ≤ 1/2, |uj| ≤ 1 and |vk| ≤ 1. Let Z zero-pad, S select the hk coordinates, α = √(L/N), and φk = exp(−2πicδk/L). Then

\[
U_N=\alpha D(\phi)\sum_{r\geq0}\frac{(-i\pi/4)^r}{r!}
 D(v^r)S U_L Z D(u^r).
\]

The entrywise phase is exp(−2πihkj/L) times exp(−2πiδkj/L), and α/√L = 1/√N. Thus the identity is exact. Because S has no repeated rows, Z, S, UL and each diagonal power mask have norm at most one. The series converges in operator norm. Its R-term truncation TR therefore satisfies, for R ≥ 2,

\[
\|U_N-T_R\|_2\leq\alpha\sum_{r\geq R}\frac{(\pi/4)^r}{r!}
\leq4/R!.
\]

This proof genuinely avoids a √N amplification. It does not infer a spectral bound solely from entrywise approximation. The unscaled channel norm sum is below 3. The title's “norm preserving” language should be understood as dimension-independent stability of the lift, rather than exact norm preservation by the rounded answer.

## Outer finite precision

Take R! ≥ 16/ε, δ = ε/128, q = ceil(log2(512R²/ε)) and t = 2^−q. The actual weighted input supplied to every dyadic call is covered by its pointwise error contract; linearity of the quantized call is unnecessary.

Updating each mask with its exact rational base and truncating toward zero gives bounded masks and error at most rt after r steps. Downward-rounded coefficient magnitudes satisfy 0 ≤ ĉr ≤ (π/4)^r/r! ≤ 1/r! and |ĉr−(π/4)^r/r!| ≤ 3rt. These inequalities include underflow.

The endpoint angle is in [−π/4,π/4]. A rational Machin enclosure for π, guarded integer Taylor recurrence, factorial remainder and final two-coordinate rounding give |φ̂k−φk| ≤ 3t. The normalized scale α̂ = 2^−q isqrt(floor(L2^(2q)/N)) is below α with error at most t. The square-root expression is exact integer arithmetic; it does not assume a real square-root oracle.

For ideal unscaled sum W and the computed sum Ŵ, the three errors give

\[
\|\widehat W-W\|_2
\leq[3\delta+(1.5R^2+6)t]\|x\|_2.
\]

Here the backend errors sum under ĉr ≤ 1/r!, the two mask errors under ∑r/r! < 3, and the scalar errors under ∑r < R²/2. The endpoint multiplier has norm at most 2(1+3t), and its difference from the ideal multiplier is at most 7t. Since ||W|| ≤ 3||x||, the source's conservative ledger follows:

\[
\frac{\|\widetilde y-U_Nx\|_2}{\|x\|_2}
\leq4/R!+12\delta+64R^2 2^{-q}<\varepsilon.
\]

Outer multiplication and accumulation can be exact on a common dyadic lattice: backend exponent ranges, input scaling and all outer denominators have O(log N) bits in the two regimes; summing R terms adds only O(log R) numerator bits. Separate input normalizations per channel do not multiply denominator lengths, because dyadic denominators align to their largest exponent. Thus no uncharged accumulation-rounding term is required in this mathematical algorithm.

## Cold work and memory audit

Write ℓ = log2 L. Backend mantissa precision is p = ceil(log2(1024(ℓ+1)/δ)). Its exponent range has O(ℓ+p) values, requiring O(log(ℓ+p)) exponent bits. One complex state therefore has b = O(p+log ℓ) bits, which is O(log ℓ) in both regimes here.

The largest dyadic radix m with mb ≤ ℓ/4 is Θ(ℓ/log ℓ). For every occurring radix r ≤ m, the algorithm enumerates all 2^(br) padded keys. Invalid codes decode to zero; unreachable overflowing responses are clipped, so every address has a defined payload. Table coefficients have a certified operator error, and all keys are evaluated during preparation. Each payload has br bits and fits in a word, while each address is below L^(1/4). A leading-bit table is also included where needed.

Direct polynomial-time construction per key costs L^(1/4) poly(ℓ,p) in total, including the small family of radices. The complete phase grid has 2^(p+8) entries and costs 2^p poly(ℓ,p). Both preparation costs and storage are o(L) in the stated regimes. No nonuniform advice, free root table or prior-input cache is required.

Gathering, key assembly, lookup, unpacking and scattering cost O(r) per block, not O(1) for r outputs. There are O(ℓ/log m) macrolevels and O(L) work per macrolevel. Scale-dependent rounded twiddles are charged. The backend's unitary-stage recurrence and underflow budget give relative error δ; a first-overflow argument bounds reachable norms below the upper cutoff. Its total cold cost is O(L log L/log log L), with O(L) words.

The outer lift uses R such calls and O(NR) mask/collection work. Per-output certified phases use poly(q+log R) operations; shared π and scale preparation use polynomially many operations in log N + q. Streaming keeps two masks, one accumulator and one backend workspace, with sublinear tables and O(R) scalar coefficients. Thus

\[
T=O\!\left(R\frac{N\log N}{\log\log N}+NR+N\operatorname{poly}(q+\log R)+\operatorname{poly}(\log N+q)\right).
\]

At fixed ε, R and q are constants. At ε = (log N)^−a, R = Oa(log log N/log log log N) and q = Oa(log log N), yielding the two advertised bounds. The outer polynomial-in-log-log work is lower order than the displayed principal term. Input-independent tables may be reused among channels, but their construction is still charged to one fresh original transform. None of these calculations proves the supplied on-demand reference has that running time.

## Exact correction rank

For K[k,j] = exp(−2πiδk(j−c)/L), the residues kL modulo N take N/gcd(N,L) distinct values. The fixed nearest-integer convention maps these to the same number of distinct δ values. The corresponding complex nodes zδ = exp(−2πiδ/L) are distinct. After removing a nonzero row scalar, each row is (1,zδ,…,zδ^(N−1)). A Vandermonde minor gives

\[
\operatorname{rank}K=N/\gcd(N,L).
\]

Hence an exact separated representation K[k,j] = ∑_(r=1)^R ar(k)br(j) needs at least that many terms; at odd N, it needs N. This is a representation-specific rank statement. It is not a bound on the rank of the Fourier transform itself, on arithmetic complexity of a joint evaluator, or on every possible exact FFT. A numerical floating-point rank estimate is unsuitable evidence here because these Vandermonde matrices can be severely ill-conditioned; the proof and finite-field controls avoid that mistake.

## What is new in this source relative to the catalogue

The earlier accepted compiler uses one dyadic transform followed by stable oversampled interpolation, with a dimension-free interpolation norm, Schur tail bound, finite offset tables and explicit precision-domain safeguards. Its fixed-ε order is the same. For inverse-polylogarithmic ε, its refined bound is O(N log N/log log N), stronger than the present Taylor lift's O(N log N/log log log N). It also covers fixed stretched-log precision schedules and more general supplied sublinear precision exponents in its stated domain.

The present package supplies a simpler-to-state alternative channel identity and factorial tail, a separately spelled-out fixed-point outer wrapper, and an exact residual-kernel rank diagnostic. These are useful additional proof routes and source evidence. The source ledger's claim of supplying a missing project-wide all-length transfer is inaccurate relative to the now-inspected complete catalogue, although it is accurate relative to the dyadic-only note the source directly compared against. Preserve this distinction rather than replacing an accepted stronger result with a weaker one.

## Primary-source comparison

Anderson and Dahleh's publisher abstract expressly describes unrestricted lengths and nonequispaced points using local Taylor expansions and FFTs. This establishes direct mechanism precedent; the abstract alone does not settle equality of the complete finite-word error-and-cost contract. [Rapid Computation of the Discrete Fourier Transform](https://epubs.siam.org/doi/10.1137/0917059).

Ruiz-Antolín and Townsend write nearby-grid NUDFTs as sums of diagonally scaled Fourier matrices, discuss Taylor and Chebyshev constructions, and obtain a precision-dependent low-rank count. Their displayed approximation norm is entrywise maximum norm, and their planning work is discussed separately. Those details matter: their paper is strong precedent for the separated correction, but does not by itself supply this source's all-input relative-ℓ2 cold word-RAM theorem. Their Taylor-instability discussion does not negate a proof with explicitly bounded masks and charged guarded arithmetic; practical numerical validation remains separate. [Sections 2.1 and 2.3](https://arxiv.org/html/1701.04492v1).

Alman proves finite-field lookup-table transform savings and explicitly distinguishes bit, arithmetic and word-RAM costs, including permutation costs in Section 5. This is precedent for the acceleration mechanism, not an exact cyclic complex Fourier primitive. The present proof pays O(r) to gather and scatter r separately stored states; it must not borrow a stronger packed-data movement claim. [Theorem 1.1 and Section 5](https://arxiv.org/html/2211.04643v1).

Reif's 1999 result is an important earlier approximate-algorithm comparator. The publisher states an exact-arithmetic model and absolute evaluation error, with k = log(|P|/η), where |P| sums coefficient magnitudes. Its O(log² k) amortized cost requires at least n log n/log² k evaluation points. Setting k = O(log n) does not meet that threshold for a single n-output DFT. The stated O(n log k) Fourier-related corollary instead restricts root order to n′ ≥ Ω(n²/k), or restricts the coefficients to a descending-magnitude class. These are concrete scope differences, not evidence that the present combined contract is novel. The full article was not reviewed here; the publisher statement was. [Approximate Complex Polynomial Evaluation in Near Constant Work Per Point](https://epubs.siam.org/doi/10.1137/S0097539797324291).

Chan, Jin, Vassilevska Williams and Xu give a more direct word-RAM packing comparator: Lemma 2.2 computes length-n convolution over Fp deterministically in O(n log p) time for polynomially bounded prime p. Appendix B uses bit tricks and precomputed small DFTs, and identifies and repairs an incomplete earlier packed-convolution argument. This establishes substantial prior finite-word Fourier machinery. Its exact modular output does not automatically provide complex relative-ℓ2 Fourier outputs or the required precision conversion. [Lemma 2.2 and Appendix B](https://arxiv.org/html/2310.13174).

The SWIFFT implementation also explicitly stores several initial FFT iterations in tables for binary inputs, alongside SIMD processing. Its finite-field hashing input/output contract is different, but it is direct FFT-specific evidence against presenting the lookup principle as new. [Section 3](https://people.csail.mit.edu/cpeikert/pubs/fft_impl.pdf).

These comparisons do not establish worldwide novelty or complete subsumption of the exact combined contract. The bounded search found no theorem-matched subsumption proof, which is not a positive originality finding. Publication ranking should remain unresolved pending a broader model-matched comparison. No exact-complex result is imported into this audit.

## Fresh controls and reproducibility

Two independently authored programs produced the accompanying JSON results:

- Exact integer geometry and residual counts for 2,048 lengths; 99 exact rational precision schedules; 32,724 exact rational mask checks.
- 276 full operator comparisons through N = 127. Maximum measured tail-bound ratio 0.131812; maximum entry-construction operator discrepancy 6.34×10^−14. These are floating-point falsification controls, not rigorous interval spectral certificates.
- 63 exact finite-field rank cases through N = 64. Each field root's order is verified before modular elimination.
- 40 adversarial backend-error cases obeying the pointwise δ contract, without assuming backend linearity.
- 33 independently reconstructed rounded-outer-operator cases, 489 guarded phase checks against 100-digit values, and 264 scalar-coefficient checks. The maximum rounded-outer error/bound ratio is 0.008199.
- Eight negative controls reject uncorrected padding or omission of the endpoint phase at N = 3, 7, 17, 31. For example, the uncorrected N = 31 operator error is about 1.06008.

Run the fresh control files with Python 3, NumPy and mpmath; no package-source directory belongs on the import path. The recorded environment used NumPy 2.3.5 and mpmath 1.3.0. The reproduction instructions give the exact commands and output hashes. The controls replace the dyadic engine with mathematical matrix evaluation where appropriate, so they do not certify a production eager-table executor or reproduce the author's end-to-end reference run.

## Catalogue disposition

Attach this audited alternative construction and the exact-rank diagnostic to Q01 / TH-01 / FUS-01, retaining F132 as an inherited dependency. Keep the existing stronger precision theorem, implementation-pending flag and unresolved external priority. A source-specific supplemental claim identifier may distinguish the Taylor proof from the interpolation proof; it must not be counted as a new project-wide arbitrary-length breakthrough. The accompanying local delta records that bounded change. No remote catalogue or repository was modified during this review.
