# Claim and stored-evidence disposition

## Scope and provenance

This is new full inert source inspection of 33 exact hashes (246,583 bytes; 6,174 lines). The prior mathematical audit results are retained with their own exact bytes and hashes. No submitted, inherited or historical audit program was run, imported, compiled or parsed. Only newly authored metadata/document helpers were run. This worker made no writes to any original source or the central registry. The preservation receipt separately records initial and final metadata hashes and any authorized concurrent drift.

The strongest defects below were already documented in the preserved divisor and Phase14 audits. This review reconciles them with the complete exact source hashes; it does not claim a new mathematical discovery or a reproduced runtime failure.

## A. An actually false generic planner/executor certificate

Source 14 (`prototype.py`, SHA-256 8e8c5ac721bfab6aaa72ead610213cae50ffeee132551b4622a45be9da1edc80) uses `median_union_failure_bound` for all routes. Direct execution performs raw coordinate medians. Offset and fused-Bessel execution perform a quantized three-grid majority routine under a separately supplied `g` (default 3).

A legal offset candidate gives an exact counterexample without executing source:

- N=3; prime=2; Q=4; M=1; R=51; g=3; x=e_0; normalized tolerance 2
- M=1 makes every projected row the exact Fourier row. Each output is 1/sqrt(3), independent of the random state.
- tau=g*sqrt(M/N)*||x||=sqrt(3), and grid width is 7 tau.
- For both scalar inputs 0 and 1/sqrt(3)=tau/3, the three bin centers in units of tau are 7/2, -7/6 and 7/6. Odd repeated identical samples leave their respective bin as the Boyer–Moore candidate; the median center is 7 tau/6.
- Thus each returned complex output is (7 sqrt(3)/6)(1+i). Its squared error is (5 sqrt(3)/6)^2+(7 sqrt(3)/6)^2=37/6>4.
- Actual probability of exceeding tolerance 2 is one. Advertised bound is 2*3*2^51*(1/6)^26=67,108,864 / 847,288,609,443, approximately 0.000079204256.

This rejects the generic executed offset-candidate certificate. It does not reject direct coordinate-median theory, the one-row projected Fourier identity, or any saved empirical numerical row. It is a prior exact counterexample recorded in `additions/1954/divisor_audit/DIVISOR_SPECTRUM_AUDIT.md` and `CHECK_RESULTS.json`, both copied under `stored_evidence/` and identified in `EVIDENCE_IDENTITIES.json`.

## B. Saved planner rows: what is and is not contradicted

`additions/1954/divisor_audit/source_evidence/results.json` contains five selected plans:

- N=10,403: direct, R=9, M=101, K=103, failure_bound=1
- N=47,053: direct, R=9, M=211, K=223, failure_bound=1
- N=786,432: direct, R=9, M=768, K=1,024, failure_bound=1
- N=860,160: direct, R=9, M=896, K=960, failure_bound=1
- N=1,048,573: Bessel, R=9, Q=1,048,576, planned M=8, K=131,072, rank=8, deterministic_bias=0.0029297666508160333, failure_bound=0.0016252298067681939

The experiment driver records planner selection for these five lengths, not end-to-end execution of the five plans against the advertised tolerance. The four bounds equal to one are vacuous upper bounds, not small-failure guarantees or failed claims. The saved nontrivial Bessel bound is not established for the actual dispatcher method; there is no observed saved Bessel error-bound violation in this review.

If the stored Bessel plan is executed by the inspected dispatcher, the inherited executor chooses M=16 (log2(Q) block selection), while the planner used M=8 (natural-log block selection). It also fixes local fusion H=0 and uses g=3 unless overridden. Its error certificate must include

  epsilon = global_Bessel_tail(R) + (2R-1) * small_argument_Bessel_tail(pi*(M-1)/Q, H)

at the actual executed M. The standalone v11 code includes that term and uses variance factor (M/N)(1+epsilon)^2. The v13 planner omits the local term and uses a different M. The quantized aggregator requires its own radius and probability calculation. Missing terms and mismatched constants show an unsupported certificate; they do not prove the actual error equals an omitted conservative bound.

The preserved v13 stored direct checks remain finite numerical evidence: maximum materialized-projection discrepancy 3.14018491736755e-14, maximum covariance-formula entry discrepancy 3.3306690973927237e-16, maximum reported robust diagnostic ratio 0.20116924679879689. These were not rerun.

## C. Correct identities and their actual computational scope

- Composite row: N=KM, K>=M, unit a, beta modulo N. P^2=MP; a row is U_N P x. Parity twist gives monodromy -1 and one K FFT plus O(N) scan/compression. This is not exact U_N x for a generic row when M>1.
- Offset classes: h=N/gcd(N,Q); classwise modulation yields exact expectation, with all h class costs charged. The literal implementations call sorting-based `np.unique`; ideal linear map/grouping alternatives are not already implemented by those calls.
- Prime-power covariance: M/N projector eigenvalue with rank N-K; M=1 is the zero-covariance boundary. Full-state checks using conjugated chirp rows remain valid distribution checks via (a,beta)->(-a,-beta-h), not same-labeled-state coefficient checks.
- Phase26: exact strict pigeonhole witnesses, nonsingular weighted cycles, dyadic balanced character cuts, Hamiltonian no-two-cycle condition, affine interstage conjugations and finite modular rank examples are retained. Character cuts are not all balanced cuts, and modular rank is not a complex norm certificate. The saved strict-witness repair belongs to the historical audit.
- Sparse repair: exact rational/field checks support the separated support witness and rank lower bound for row-q-sparse baselines, with characteristic/denominator exceptions retained. Dense verifier and support enumeration costs are not fast-transform runtimes.
- Phase14: orthogonal bank and Gram-union outputs are Fourier transforms of input projections. q=M stationary frame gives exact arbitrary-input Fourier algebra, with actual O(NM+N log(G/M)+N log(m+1)) work. Bounded-q linear work concerns a prescribed proper subspace. Generic Gram storage contains Kq^2 (and phase tensors), while the stationary evaluator can stay O(N) for supported parameters.

## D. Actual implementation accounting discrepancies, without false failure claims

1. The v13 planner proxy charges one sqrt(N) factorization but actually enumerates all divisor candidates and repeats totient work. A fuller divisor-count argument still supports O(N) word-arithmetic setup, so omission from the literal proxy does not refute the asymptotic direct-family claim.
2. `stationary_eval` refactors the shared Gram once per odd column through separate `np.linalg.solve` calls; it does not literally retain one factorization globally. Extra mq^3 is absorbed by mKq^2 since q<=K.
3. Adaptive bank proxy suppresses root-table setup after `analyze_banks` has built it. A fresh end-to-end charge needs the O(G) term; asymptotic results are unchanged.
4. Source 14's introductory “strictly improves” comparison with M(M-1)/phi(N) is not strict at M=2, where the bounds coincide. The non-strict inequality and saved numerical values remain sound. The stronger preceding mask-count certificate was already available.

## E. Hypothetical input gaps that do not invalidate stored supported cases

- `stationary_states` and `construction` accept direct helper parameters G=32,M=3,q=3 without enforcing M|G. The extra iKMr u term need not vanish. Public `stationary_eval` invokes the correct inherited validator, so supported saved evaluator instances remain valid.
- `offset_class_core.choose_prime_power_block` lacks a q>0 guard (q=0 can loop), and N=1 can yield unsupported Q=1. Listed saved routes use supported positive larger parameters.
- Several internal matrix helpers trust compatible shape/permutation/prime inputs; some zip-based routines truncate bad shapes. Driver inputs are legal.
- Some numerical comparisons can fail open on NaN, and int64 modular products can overflow for sufficiently large unsupported sizes. No NaN/overflow is established in the saved finite datasets.
- Historical archive scripts rely on fixed paths and additional inventory fields. Actual stored inventory contains both `master_archive_member_matches` and `master_recursive_archive_matches`; a missing-key defect in a hypothetical clean pipeline does not contradict the saved successful metadata.

## F. Evidence acceptance boundary

All numerical timings, PASS strings, assertion counters, test counts and “source_code_executed=false” declarations inside old artifacts remain attributed historical claims. They are not new runs. The sparse independent record embeds this exact checker SHA-256; that identity was reconciled, not treated as proof every assertion executed. Manifest/CRC/syntax checks and seal writers establish byte/provenance facts, not whole-source correctness. Source 21 hardcodes an all-checks-PASS seal without checking result status; source 31 hardcodes the test-count success caption. Both require their underlying records for evidentiary weight.

The complete 33 source reads receive new static-coverage credit. Eight additional source dependency hashes are preserved hash-only with zero credit. No global research completion, dependency-closure completion, unrestricted exact faster Fourier construction, universal FFT lower bound, or literature-priority claim is made.
