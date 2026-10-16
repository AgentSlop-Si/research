# ALG-024 / ALG-027: source-specific sparse-Fourier comparison

Date: 16 October 2026. Mode: local proposal, no external writes. Repository baseline: `07455df33fd8243bc0e7facb92af6c6a5830ae2a`. Workbook: `1BHaGJHkXxf_UfZdyTKF2zrWNFzIP4IvhaqFMj-83BjU`.

## Disposition

The two selected, previously unfinished **NSW sparse-recovery comparison subgates** reach their recorded stop through a conditional norm mapping and explicit model/cost nonmatches. This is a candidate for independent acceptance, not blanket historical-priority clearance. Both parent records remain **TO RESEARCH**, priority **12**, with accepted mathematical scope and implementation obligations unchanged. There are zero record closures, zero new theorem identities and zero new implementation acceptances.

Selected owners: ALG-024, Catalogue row 162 / novelty row 201 / overview row 289; ALG-027, Catalogue row 163 / novelty row 202 / overview row 290. Their recorded action asks for exact error-norm/scale comparison with sparse recovery, sampling and rank barriers. Their stop explicitly permits a qualified nonmatch. The complete source rows, notes, historical material and accepted-scope columns were read. This report addresses that comparison, not a replacement algorithm or an easier mathematical parent.

## 1. Source boundary and prior work already completed

All seven owner-linked research bodies were read as inert documents. The independent reviewer fetched them at the pinned repository commit and verified the export identities. Source bindings are in `SOURCE_BINDINGS.json`. No supplied programs were imported or executed; no solver, package installation or external mutation was used.

ALG-024's Gaussian audit §8 already gives narrow descriptions of Nakos–Song–Wang (NSW) and Kapralov, expressly without a full theorem/model comparison. Its rough-padding proof already attributes Bertrand/prime-counting inputs. Those were not newly discovered here.

ALG-027's v2 and delta review already establish the Parseval support ceiling, the exact Alon perturbed-identity mapping, the calibrated energy-pruned graph comparison, and corrections for relative compressibility, stale plans and repeated full-input selection. The corrected derivation, planner README and independent review further bind the full-prefix planner and its numerical limitations. None is counted again as newly finished work. The newly supplied comparison is the NSW hypothesis/error/cost mapping below.

The historical delta source identity `f023fcf6…` denotes 5,972 original bytes. Its repository sanitized export is 5,908 bytes, SHA-256 `ab76c2274a20c52f23bf9e69e44bf5bde4a48c5fb8484e0830ec420ca1951b41`. They are not byte-identical; this report binds the published export and preserves the historical identity separately.

## 2. Primary comparator and its qualifications

[NSW, arXiv:1909.11123v1](https://arxiv.org/pdf/1909.11123v1), Theorem 1.1, §1.5, Appendix A opening, Algorithm 3 and Theorem A.16: for normalized DFT X, the output is O(k)-sparse in frequency and satisfies ||X-z||∞ ≤ ||X_-k||₂/√k with polynomially high success probability. Samples: O(k log k log N). Explicit runtime: O(N log³N log k). One-dimensional arbitrary N is included. Appendix A assumes a supplied noise scale μ=||X_-k||₂/√k (a constant-factor approximation is discussed), a supplied polynomial bound R*≥||X||∞/μ, and time-coordinate access. §1.5 neglects FFT rounding error.

Important source inconsistency: v1 Theorem A.16 prints μ=||X_-k||₂/k, whereas §1.5, Appendix A's opening and Algorithm 3 use 1/√k. The informal theorem's R* wording also differs. We use the explicit algorithm convention conditionally, disclose the discrepancy, and do not certify an unambiguous full theorem contract or silently repair the paper. The output inequality itself agrees. Zero spectral tail (μ=0), unspecified noise-scale preparation and unbounded SNR are not automatically admitted. [Same version HTML](https://arxiv.org/html/1909.11123v1).

The parameter substitutions in the next sections are this report's algebraic comparison, not additional claims from NSW. All are conditional on the source assumptions above. Opposite Fourier signs amount to frequency reversal and preserve these norms, tails and sparse sizes. The runtime is the paper's stated ideal-arithmetic bound: Algorithm 3's random-shift repeat-until loop is bounded by its high-probability analysis event. This is not a deterministic capped executor or a random-bit/abort contract. The quoted polynomial-confidence result does not establish ALG-027's arbitrary requested δ or the Gaussian route's selected exponent c at identical constants/work; no such amplification is constructed or charged here.

## 3. ALG-024: rough padding is supporting preparation, not a recovery theorem

The accepted owner statement chooses prime M=Θ(log N), rough cofactor K and Q=MK=4N+N^o(1), with gcd(Q,d)=1 for 0<|d|<M. It proves φ(Q)/Q≥1−log Q/(M log M)=1−O(1/loglog N). Sieve and consecutive divisibility checks cost N^o(1) word work on O(log N)-bit integers; no exponential inclusion–exclusion table is constructed. This sharpens its companion Gaussian covariance to O(log N/N). It does not itself output a Fourier transform.

The companion source gives, for each fixed input independent of fresh random states and fixed 0<α<1/2, all-bin error O(N^-α)||x||₂ and O_{α,c}(N loglog N) ideal arithmetic work at polynomially high confidence, for sufficiently large N. It requires its exact Green identity, supplied base constants, correctly charged recurrence preparation, independent random-state generation and abort budget. Finite-word stability and concrete finite-size thresholds remain separate.

**Conditional norm overlap.** Write X=U_Nx and E_k=||X_-k||₂. Since E_k≤||x||₂, choose k=ceil(N^(2α)); for fixed α and sufficiently large N this lies between 2 and N−1. The comparator error is at most N^-α||x||₂. Thus this weak absolute all-bin scale is already within the sparse-recovery guarantee on its admitted input/interface domain. Zero-fill a sparse frequency result to expose all N bins, charging O(N) output work and storage.

**Cost and hypothesis nonmatch.** Substitution gives O(N^(2α) log²N) sample calls and an explicit O(N log⁴N) arithmetic upper bound. This does not supply the Gaussian O(N loglog N) bound, the rough-Q constructor, the covariance identity, exact exponential bases, or certified numerical evaluation. A smaller query count is not a complete end-to-end time comparison. Conversely, the Gaussian construction is not a source of the comparator's supplied spectral tail estimate. No universal speed order follows from comparing upper bounds in different access models.

**Error scale remains weak.** The Gaussian bound only implies ||error||₂/||x||₂ ≤ C N^(1/2−α); that implication does not force a vanishing relative-l₂ error. On an impulse input, all exact Fourier bins have magnitude ||x||₂/√N, so the zero output meets the coarse N^-α scale for α<1/2 while having relative-l₂ error 1. This is an illustration of the guarantee, not a claim that either algorithm returns zero.

NSW's theorem is therefore not the same rough-padding/covariance statement, and its conditional guarantee overlap does not settle originality of that supporting refinement. The named comparison is completed as a qualified nonmatch. F016's broader theorem, implementation, stability and priority work remain untouched.

## 4. ALG-027: time-sparse surrogate versus frequency-sparse recovery

Retain the owner's theorem. For x≠0, L=||x||₁, τ=L/(√N||x||₂)∈[N^-1/2,1]. The data-dependent law p_j=|x_j|/L is selected before fresh iid draws. With m≥4ε^-2 log(4N/δ) draws, the unitary full-output error is at most εL/√N=ετ||x||₂ with probability ≥1−δ. This is for each fixed input, not one sampled linear map for all inputs. The zero input is detected and N zeros are written in O(N).

For a predetermined exact head with residual mass ratio ρ_s, the existing real/imaginary Hoeffding and N-bin union argument is 4N exp(−m ε²/(4ρ_s²)). The deterministic branch ρ_s≤ε needs no draws; an exact-input bypass precedes RNG work. This is preserved accepted evidence, not a fresh sampling theorem.

**Exact comparator calibration.** Using only E_k≤||x||₂, the sufficient frequency-sparsity parameter is

    k₀=max{2, ceil(1/(ε²τ²))}.

When k₀<N and the supplied-noise/SNR conditions hold, E_k₀/√k₀≤ετ||x||₂. The formula ceil(ε^-2) only matches the weaker ε||x||₂ target, or τ=1. When k₀≥N, this coarse bound establishes no substitution inside the nonzero-tail comparator domain. It does not prove a transfer impossible: a particular spectral tail could be smaller. Any dense exact fallback is a separate charged computation.

The surrogate's m draws control **time-domain** support, while NSW's k controls **frequency-domain** support. Small time-domain tail mass ρ_s does not certify the spectral tail or μ. For example, an impulse is time-sparse but has a flat Fourier spectrum; a constant signal has a one-bin spectrum but a flat time-domain magnitude distribution. The constant signal's zero spectral tail also exposes the μ=0 caveat, so it is not cited as an admitted NSW execution.

**Full paid cost.** Preserve the corrected planner's O(N+H log(H+2)) preparation, O(N+m log(m+2)) construction, and O(N log(q+2)) classical dyadic transform of realized time support q, including roots, normalization and all N writes. The safe combined bound uses the chosen support upper bound B_selected, not q alone while discarding coalesced draws. Default H=O(log²N) gives linear asymptotic planner cost. NSW's sparse output additionally needs O(N) materialization for this task. Neither its sample count nor its reported runtime certifies the owner's floating planner, iid probability implementation, final transform roundoff or production speed.

**Rank and scale guards remain.** Existing Parseval reasoning gives ||U_N(y−x)||∞≥σ_q(x)₂/√N for q-sparse time surrogate y. Constant-magnitude inputs at tolerance η||x||₂/√N require q≥N(1−η²). The existing Alon realification argument restricts time-sparse surrogates, not arbitrary approximate-Fourier algorithms or frequency-sparse outputs. It therefore does not lower-bound NSW's runtime. Finally, ε_N→0 only forces the normalized multiplier to vanish; absolute error needs ε_N||x^(N)||₁/√N→0. On constant entries, polylogarithmic ε_N leaves a growing bound.

The named sparse-recovery comparison is completed as a qualified norm overlap with representation, advice, numerical and cost nonmatches. The accepted full-prefix result is preserved. Remaining numerical/all-length work and Q09's separate implementation obligations remain open at their recorded scopes.

## 5. Prior comparator checks retained without extra completion credit

[Kapralov, arXiv:1604.00845](https://arxiv.org/pdf/1604.00845), Introduction equation (1) and §2, targets l₂/l₂ sparse recovery on power-of-two side lengths, with polynomial precision/range, a supplied tail-scale bound and polynomial SNR. A bound C||X_-k||₂ does not alone imply N^-α||x||₂ or ετ||x||₂. It would need an additional spectral-tail inequality. Its source's norm, sampling and full-output distinctions remain; no generic arbitrary-length or exact-FFT transfer is inferred.

[Alon, Theorem 1.1](https://web.math.princeton.edu/~nalon/PDFS/identity1.pdf) is already explicitly mapped in the ALG-027 delta review: realification dimension 2N, diagonal at least 1−ε, off-diagonal at most ε, real rank at most 2q, with 1/(2√(2N))≤ε<1/4. It yields the recorded logarithmic support lower bound only for that sparse-surrogate construction. This report confirms its boundary rather than recounting the prior mapping as new work.

[FFTW authors, Pruned FFTs](https://fftw.org/pruned.html) explain the classical O(N log K) arithmetic behavior and warn that reduced arithmetic does not ensure wall-clock gains. This preserves the source credit for the transform backend, without certifying the separate arbitrary-support implementation or numerical guarantees.

## 6. Minimal table proposal and stopping condition

`NATIVE_CELL_PROPOSAL.json` proposes only leading current-action and pass/stop text: Catalogue AE/AF, overview P/Q, novelty Y/Z, plus overview F's current task overlay, seven cells per selected ID. The F update prevents the finished named comparison from remaining the leading pending task. Each carries its full original cell preimage and a prefix only. Apply only after independent acceptance and fresh exact-preimage checking. Append the original text unchanged as history; preserve notes, formatting, links, formulas, priorities and all other cells. The proposal changes neither status nor proof acceptance.

The recorded stop is met for these named primary comparisons by the explicit hypotheses, norm substitutions and nonmatches. No implementation is fabricated, no historical code is replayed, no probability of research success is assigned, and no worldwide-priority or unrestricted lower-bound claim is made. Further work requires a separately specified unmatched source, concrete implementation contract, or new mathematical question; the completed named comparison should not be rerun as pending.
