# Applied mathematical-value archival disposition

Applied on **16 October 2026** and independently verified in the native research table. Q16, STR-Q1, FUS-09 and ENGINEERING-NTT-BASELINE-20261012 are **CLOSED: archived for low identified mathematical novelty/value in their current continuations**. These are four existing views across two continuation families. Accepted mathematics, all evidence and unfinished engineering remain preserved; there is no new proof or implementation-completion claim.

The verified census is **79 closed/archived and 248 open views, 327 total**. All numeric priorities, stable IDs, row positions, proof verdicts and other overview statuses are unchanged. Retained priority scores are historical/inactive for the four archived views.

See [the applied-disposition receipt](APPLICATION_COMPLETE.md), [independent native acceptance](ROOT_ARCHIVAL_POSTWRITE_ACCEPTANCE.json), and [independent index acceptance](ROOT_INDEX_ACCEPTANCE.json). The [current open-record index](../2026-10-15-rebuilt-open-record-index/README.md) excludes the four archived views.

The original pre-application rationale follows verbatim as dated history. Its proposal wording describes the stage before the verified application above; `ARCHIVAL_DISPOSITIONS.json` is likewise preserved as the exact accepted proposal, with actual application recorded separately.

---

# Proposed archival disposition: Q16 continuation and fixed-modulus NTT baseline

16 October 2026 UTC. **Proposal, not an application receipt.** This document does not claim that repository or research-table statuses have already changed.

## Decision and scope

Four existing records belong to two continuation families recommended for archival from active mathematical research:

| Stable ID | Current named continuation | Retained priority |
|---|---|---:|
| Q16 | Weak-error all-length approximation: remaining integrated implementation | 60 |
| STR-Q1 | Sparse-transfer numerical certification | 60 |
| FUS-09 | Sparse HIKP output and all-length interpolation: remaining implementation | 60 |
| ENGINEERING-NTT-BASELINE-20261012 | Fixed-modulus NTT implementation and benchmark qualification | 43 |

The proposed disposition is **CLOSED: archived for low mathematical novelty/value in the current named continuation**. It is not a new proof verdict or engineering-completion claim. Accepted mathematics, previous evidence, failed attempts, source files, saved measurements, and unresolved implementation obligations remain preserved. Any numeric priority retained after archival is historical and does not assign active work.

This decision does not imply that a theorem is false, that implementation is complete, or that no future mathematical contribution could exist. It concerns the current continuation: no distinct substantive mathematical target has been identified beyond the existing analytical foundation, while the remaining tasks concern implementation or validation.

No F016, FUS-01, Q32, or other sibling status changes are included. Similar names, shared dependencies, and shared executors are not grounds to close a separately owned scope.

## Mathematical-value criterion

Continued mathematical research should target a concrete addition to knowledge: a nontrivial theorem, construction, classification, sharp bound, counterexample, or useful proof/connection in a motivated model, with an identifiable difference from prior work. Negative results can meet this criterion.

Source pinning, evidence recovery, additional benchmark cases, serialization, conformance, and repeated comparison of unchanged statements do not alone provide that difference. Conversely, missing sources or an unproved novelty claim do not establish that a result is valueless. The proposals below rely on known analytical foundations and the actual remaining work, rather than an unsuccessful search for prior art.

## Q16, STR-Q1, and FUS-09

The accepted finite-word existence theorem remains intact. Its guarantee is weak simultaneous coordinatewise approximation of the unitary Fourier transform for the stated finite input family and growing-word model. Its preserved limitations include the distinction from exact DFT, relative-l2 recovery, the alpha=1/2 endpoint, practical speed, and a new analytical exponent.

The reviewed owner edition is `FINAL_THEOREM_AND_PROOF.md`, SHA-256 `0a7733e2ac1d1c32cf70609ba0db151a13a73765107907aec44045daaf0a58f5`. Sections 10–11 distinguish its prior analytical foundation from unfinished integrated-executable work. The immutable v1 theorem has SHA-256 `4bc3e876a680cfb031d4e7d2363f81dfc713c45ef680b3a34eedb167a536d408`. The recovered edition carries forward historical mathematical acceptance with inherited premises; it is not a fresh full proof replay or a certificate for a production implementation.

The exact owner comparison is `PRIOR_COMPARISON_REPORT.md`, SHA-256 `d2b6b8f1a0ad74626f3d10f00bf1ebf7fe9bd25e23448f2c2a710aae2c88d0ef`. Its decisive primary matches were reopened for this disposition:

- [Hassanieh–Indyk–Katabi–Price, Simple and Practical Algorithm for Sparse Fourier Transform](https://people.csail.mit.edu/haitham/Papers/sFFT.pdf), Theorem 4.4 and preceding support/runtime argument, PDF page 9. With sparsity proportional to M^(2beta) and suitable polynomial leakage, its infinity-error theorem supplies the owner's analytical sparse-front target. The success-independent support-count mechanism is also present. The owner's report provides the normalization and parameter map.
- [Kapralov, Sparse Fourier Transform in Any Constant Dimension](https://theory.epfl.ch/kapralov/papers/ft-sublinear-loglogn.pdf), section 8.1, Algorithm 4 and Lemma 8.1, printed pages 36–37. The paid total-energy envelope in the owner comparison yields a faster sparse-front arithmetic bound under the paper's numerical abstraction. This is not a claim that its text is a drop-in finite-dyadic executable certificate.

The finite-word refinement can be useful without making the remaining continuation a new mathematical advance. Current tasks are source-pinned execution, certified routines, parsing and serialization, sparse-output binding, outer transfer, dispatch, randomness, resource accounting, reproducible builds, and conformance. Those remain unfinished and would be archived as such.

The record-specific boundaries are:

- **Q16:** archive the present operational continuation; retain accepted finite-word mathematical existence and all inherited premises.
- **STR-Q1:** archive the named sparse-transfer numerical-certification continuation; retain all bounded acceptances and the incomplete production/all-length/outer boundary.
- **FUS-09:** archive the named implementation continuation of the accepted HIKP/interpolation composition; preserve its existing proof-closed verdict.

The owner's edition review explicitly distinguishes **F016's separate Gaussian/Green mechanism**, which retains its own accepted ideal O(N log log N) scope. No disposition of F016 or FUS-01 follows here.

## Fixed-modulus NTT baseline

The source is a conventional positive-exponent modular DFT over modulus 998244353, with stated dyadic and Bluestein length guards. The [exact repository review](https://github.com/AgentSlop-Si/research/blob/77b086e3827d2af2ede09e8dcf88b54836d5b5f7/math/reviewed_rounds/2026-10-12-submitted-source-assessments/ENGINEERING_NTT_REVIEW.md) was fetched at the pinned snapshot and its SHA-256 was independently checked as `32b9e8e7c33b69633e1616188b59e0f9ad643677680bbb5b6175ee5900ddf4d8`.

The reviewed paid protocol is `PAID_NTT_CONTRACT.md`, SHA-256 `0cefd28b3548a2368ca87b6429b4775aff7e8e16d28913dfaaf4c2a324ca2301`. Sections 7–9 establish the scope of the arithmetic counts and remaining experiment. For each of the four pinned schedules at n=2^l, the source counts are

- A(n)=n log2(n) modular additions/subtractions
- M(n)=(n/2)log2(n)−n+1 modular multiplications

These exclude other explicitly paid work. Equal field-operation counts do not establish equal runtime; they also provide no arithmetic-count improvement for the candidate. The remaining build, adapter, allocation/lifetime, sanitizer, replay, and timing tasks are engineering qualification. No new asymptotic rate, mathematical construction, universal speed advantage, or production-readiness claim is supplied.

Archive **ENGINEERING-NTT-BASELINE-20261012** from active mathematical research. Preserve its source archive, original implementation, saved timings, protocol, accepted expected-output corpus, and all unfinished engineering qualifications. The accepted 288-vector expected-output obligation stays accepted. Historical speed observations remain unreplicated. Q32's different API and comparator remain unchanged.

## Preservation and reopening

No files are to be deleted or replaced by this disposition. Old claims and evidence remain available with their original qualifications. Unfinished implementation remains unfinished, even if the research activity is marked CLOSED.

A new explicit mathematical target with a substantive identified difference can justify reopening. A separately requested engineering task can reactivate implementation for its own practical purpose. Neither requires rewriting the historical evidence.

`ARCHIVAL_DISPOSITIONS.json` supplies the four proposed record-specific texts. A later application receipt must identify any actual status changes and their verification separately; this proposal does not supply that receipt.
