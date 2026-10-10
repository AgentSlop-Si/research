# Claim proof and citation concordance

Companion to [the working manuscript](MANUSCRIPT.md), 10 October 2026. The assertions below distinguish the locally proved theorem, classical dependencies, saved review evidence, and unresolved priority comparison. Source identities and exact bytes are in `SOURCE_PINS.json`; local preserved bodies are in `evidence/`.

## B1 Mathematical claim map

| Claim | Manuscript proof location | Frozen proof source | Review evidence and limits |
|---|---|---|---|
| Complete raw-input prime-field contract; no supplied phase or frequencies | Sections 1–2; Appendix A1–A2 | P1 Sections 2–3 | R1 “Contract and exact correctness”; does not extend the shared theorem to every exact field |
| Canonical phase range of size \(N/\gcd(2,N)\) is complete | Section 1 | P1 Section 2 | R1 checks absorption of the even-length phase redundancy; uniqueness across phases is not asserted |
| Nonzero members have an allowed interior nonzero center | Section 3.1 | P2 Section 6; P4 Section 2; P1 Section 4.2 | R1 Vandermonde/no-consecutive-zeros argument; needs \(N\ge3r\) |
| \(E(0)=x_c^{r+1}\ne0\), \(\deg E\le\binom{r+2}{3}\), every leading minor has nonzero constant coefficient | Theorem 1; Section 3.2 | P2 Sections 1–2 | R1 determinant and rearrangement audit; equality of degree is not guaranteed |
| Every true phase is a root; at most \(C_*\) grid candidates | Section 3.3 | P1 Section 4.2; P4 Section 2 | R1 derives the separate row and column factors explicitly |
| Zero reduction modulo \(z^L-1\) retains all phases | Sections 3.3 and 6 | P1 Sections 4.3 and 10 | R1 checks both an accepting and rejecting zero-reduction control; root count always uses original nonzero \(E\) |
| Unit-safe ring recurrence and \(T(r)=r^2(D+1)^\kappa\) construction envelope | Section 4 | P2 Section 4 | R1 confirms nonsymmetric predictor invariants and cached scalar inverse; classical Toeplitz kernel C3 |
| Exact fixed-phase dyadic membership from BM, root scan, amplitudes, global synthesis | Section 5 | P3 Section S2; P1 Section 4.1 | R1 checks index negation, amplitude formula, and arbitrary-prefix rejection; classical C1–C2 recovery and C4 pruning |
| Complete dyadic attempt ledger, inversions, storage | Theorem 2; Section 6; Appendix A4 | P1 Section 4.3 | R1 “Hybrid bound and complete rejection ledger”; proof-level bound, not runtime measurement |
| All-length blocked scan and global recurrence verification | Theorem 3; Section 7; Appendix A5 | P4 Sections 3–6; P1 Section 4.2 | R1 accepts original B-envelope; no generic all-length FFT prerequisite |
| All-length Gauss row including \(a=0\), nonunit phases, even reduced lengths, and \(q=1\) | Section 8 | P1 Section 6 | R1 “Dense outputs fallback and operator applications”; 1,176 historical direct-row controls; current proof independent of D06 historical-byte identity |
| Sparse-first cost and equal/unequal-cap semantics | Section 9; Appendix A6 | P1 Section 5 | R1 checks the paid failed first attempt; no universal \(\min(A,B)\) conclusion |
| Sparse fresh-vector operator cost remains separate | Section 9 | P3 Section S2; P1 Section 8 | R1 checks the sign, factor \(N\), and odd-length one-chirp Fourier reduction; no application lower bound |
| Complete rejection differs from budget abort; paid backend | Section 10; Appendix A1, A3, A6 | P1 Section 7 | R1 accepts REJECT/UNKNOWN distinction; no DFT promised on REJECT |
| Word and bit-model conversions remain parameterized | Appendix A7 | P1 Section 9 | R1 requires paid inversion, certification, integer work, and input/output traffic |

## B2 Classical attribution map

| Ingredient | Citation and location | Use in this manuscript | What is not attributed to that source |
|---|---|---|---|
| Minimal recurrence synthesis | C1 Massey 1969, Section III, Theorems 2–3 and corollary | Berlekamp–Massey on a finite-field prefix, with nondecreasing minimal order | The common-phase eliminant, phase scan, or complete chirp decision ledger |
| Prony and Vandermonde reconstruction | C2 Peter–Plonka, Theorem 2.1 and Section 5 | Classical exponential-sum recovery; the manuscript supplies its finite-field factorization and full-input check | A claim that the cited complex-domain theorem directly states our exact finite-field decision interface |
| Nonsymmetric Toeplitz predictors | C3 Gutknecht–Hochbruck 1995, Section 2, equations (2.7)–(2.10), Algorithm 1, and (2.17)–(2.20) | Paired predictors, pivot/Schur-complement structure | The center-derived unit guarantee over a truncated finite-field polynomial ring; that algebraic specialization is proved in Section 4 |
| Fourier pruning | C4 FFTW official documentation | Classical \(O(N\log h)\)-type arithmetic saving for known support; the exact input-parity tree bound is proved in Section 5 | Practical speedup, optimized implementation, or a non-dyadic support-pruning theorem |
| Karatsuba and Newton arithmetic | P2 Section 4 supplies the recurrences and local cost derivation | The standard multiplication recurrence \(M(m)=3M(\lceil m/2\rceil)+O(m)\) and Newton residual squaring | An original polynomial-multiplication or series-inversion algorithm |
| Chirp convolution and overlap-add | P4 Sections 3–4 give the explicit integer-binomial identity and block accounting | Established convolution mechanisms with no field half or extra roots | A new general chirp-z transform, or a blanket all-length \(O(N\log N)\) backend |

The present pass reopened the primary C1, C2, C3, and C4 sources and inspected the relevant passages. C5 and C6 were also reopened as versioned primary PDFs. This activity checks cited source locations; it does not turn the incomplete C7–C9 comparison into a completed literature survey.

## B3 Input interface comparison

| Work | Data and domain supported by inspected evidence | Shared unknown parameter and conclusion | Comparison depth and remaining work |
|---|---|---|---|
| This manuscript | Every complete raw \(x\in\mathbb F_p^N\); supplied prime and exact-order root; variable cap | Unknown grid quadratic phase; exact all-input membership and full verification; DFT on acceptance; paid rejection | Complete scoped proofs and the preserved local independent review |
| C5 Agostini–Améndola–Ranestad | Ordinary moments of homoscedastic Gaussian mixtures | Trial common variance in a deconvolved Hankel determinant; atomic recovery once variance is chosen | Primary Section 4.3 inspected; v2 equations (90)–(92), published (79)–(81). Establishes conceptual elimination antecedent, not a matched raw-vector decision theorem |
| C6 Wu–Yang | Empirical moments from statistical samples | Shared-variance root procedure and quadrature with statistical/almost-sure qualifications | Primary v2 Section 4.2, Algorithm 3, Lemmas 6–7; footnote 6 gives an exceptional empirical configuration. Numerical root-finding work is not an exact finite-field root/rejection ledger |
| C7 Derin 1987 | Abstract describes Gaussian-mixture estimation and moment equations | Equal-variance or equal-mean component estimation using Prony’s method | Abstract and metadata only. Obtain and inspect pp. 142–148 before attributing unknown-common-variance assumptions, determinant equations, or universal guarantees |
| C8 Applebaum et al. 2009 | Inspected passages use complex-valued chirps on prime-length grids | Decoder based on delay products, Fourier peaks, dechirping, and residual stopping; a separate sparse-minimizer uniqueness theorem | Indexed primary passages only; full PDF inspection pending. Distinguish uniqueness of the \(\ell_0\) minimizer from every-input correctness of the peak decoder |
| C9 Lindsay 1989 | Moment-matrix setting known through C5’s discussion | Theorem 5B is cited by C5 for selecting a variance root | Original theorem not independently read. Obtain its statement, hypotheses, and surrounding argument before claiming exact correspondence or exclusion |

Observed random samples, ordinary moments, equispaced density ordinates, characteristic-function ordinates, complex chirps, and \(\mathbb F_p\)-valued arrays are different input interfaces. Their relation may motivate a comparison; it cannot substitute for one. In particular, a shared quadratic-exponential factor in Gaussian ordinate formulas is a reason to examine older methods carefully, not a reason to assert that an uninspected paper either contains or excludes this theorem.

The C7/C8/C9 gaps are priority/comparison gaps. They are not missing lemmas in the current finite-field proof. No source has been marked cleared merely because access failed.

## B4 Identity and historical evidence qualifications

- The current proof source P1 has SHA-256 `670fc97d4969b0130ba7b99661de1092c6989272c717d3c8dade17771eb4a11c` and 28,692 bytes. Its historical header says independent review was pending. The later R1 acceptance applies to those exact bytes; this packet preserves the historical header rather than silently rewriting it.
- R1 has SHA-256 `5caac961c8ef5120c55fa024063080e0d87b67e8cc5847387f239221cb6d3cbb` and 15,374 bytes. Its receipt binds the reviewed report, checker, and saved result. Packet verification checks these identities without rerunning inherited research code.
- The available D06 repository variant has 13,619 bytes and actual SHA-256 `8bb0ccc144506e968df1a9999300e3e42d060dc055b9e7f6a1049e1b36753b0f`. It is 28 bytes shorter than the historical record and does not match historical SHA-256 `e871250b94c9a5823adacee7da26bb6d4477af0758c684aa8c8ff9e34be21f89`. The mismatch remains explicit. Manuscript Section 8 uses P1’s self-contained, subsequently reviewed Gauss proof.
- R1’s saved controls include 1,043 hybrid decisions, 1,250 sparse decisions, 240 accepted-certificate and dense-output checks, 204 pruned transforms, 150 Toeplitz/permutation comparisons, and 1,176 Gauss rows. These are historical reviewer results. They are not fresh runs for this manuscript, optimized implementation evidence, or all-parameter proof substitutes.
- The reviewer used schoolbook polynomial arithmetic for controls. The asymptotic claim derives from the mathematical recurrence and cost proof, not timings of that checker.
- The new packet’s integrity checks establish byte identities, receipt links, and local document links. They do not constitute independent mathematical peer review of this editorial consolidation. No submission, outreach, repository mutation, or new fusion is performed by this packet’s authoring workflow.

## B5 Remaining work before stronger claims

1. Obtain authorized readable original bodies for Derin and Lindsay and complete the Applebaum journal-body inspection. Make theorem-level comparisons of assumptions, data interfaces, uniform nonvanishing, candidate completeness, and worst-case rejection costs.
2. Obtain a fresh review of this assembled manuscript if it is to be circulated as a formally finalized paper. Its underlying theorem is already locally reviewed; the manuscript is a new editorial object.
3. If claiming practical speed or an optimized implementation, implement and benchmark the specified kernels under a declared machine model. This is not required for the mathematical working draft.
4. Resolve historical D06 bytes only if historical source identity itself is needed. The currently proved output theorem does not depend on resolving that provenance discrepancy.

No additional theorem extension, rank census, generic FFT experiment, or fusion is required to state the present scoped result. Worldwide novelty remains unclaimed.
