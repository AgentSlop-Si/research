Publication derivative of an independently reviewed research report. Private tracking, file-service and delivery references are omitted where present. Mathematical scope and limitations remain those of the dated report. Later reports in this collection may extend an earlier report’s scope.

Original research-report SHA-256: 346b81c6729e5237bb46207ecf63a6925072afe61811f7f35bacc45cc14be7ee

---

# ALG-062 bounded raw dispatcher/reset: independent ACCEPT

Review date: 11 October 2026 UTC.

## Verdict

ACCEPT the exact sealed candidate as a newly authored, bounded reference API connecting raw-input Newton and optimal-reset recognition to all-coordinate exact finite-field DFT output. No blocking mathematical, membership, certificate-trust, status, or declared-ledger defect was found. The independent checks below and a cold authored-suite rerun passed.

This closes `ALG-062::bounded-dispatch` only in the explicit finite replacement scope. It does not migrate or repair the historical uploaded dispatcher, and does not establish physical-memory, physical-bit, wall-clock, production, floating-point, all-divisor, all-order, generic FFT, historical novelty, ALG-004, ALG-006, or ALG-079 closure.

## Exact frozen object reviewed

- Candidate: `ALG062_Bounded_Dispatch_Reset_CANDIDATE_2026-10-11.zip`
- Bytes: 80,844
- ZIP SHA256: `4769c9676a6f8f6821303bee45bb1a53c648e80ec701aa27612b18ee8297d75f`
- Manifest SHA256: `dacc6ead8e0356c4ae53587590dbc765916f8d1a8d4e602365cd95e5311ba1b3`
- Current implementation SHA256: `0d034d38b51c7d73df717dc8399d95af3a0d8a645a3e706b2cfa2643c093714c`
- Proof/contract SHA256: `e0b58ceae392bca522dcf09402f6a7b122070bd01ebfdbf7cb3b244baa1d0fc3`
- Authored tests SHA256: `c29b02c3f171bc583fcb71cb3347a2f6e52948cbc7e5316cc104fb804b09d274`
- Authored cold rerun results SHA256: `99b016aa364fd7a259d71a371499852309cad5674fe6618b55c83f2228ffc29f`

All 23 manifest payloads were verified from the ZIP; all nine historical source payloads matched their declared hashes and the separately available source files byte for byte. The candidate was extracted into a fresh review directory. Only the newly authored implementation and tests were executed. Historical supplied programs remained inert `.py.txt` data. No external service was changed.

## Accepted input and status contract

The public boundary is `raw_dispatch`, with canonical built-in list/tuple input samples and exact built-in metadata types. It enforces 1 <= N <= 256, prime N < p <= 65537, N dividing p-1, an explicitly verified primitive root of exact order N, at most 16 configuration tuples, d <= 4 and B <= 4. R <= 256 and the finite balance constants are also checked. The literal default list contains nine configurations. Custom lists select only their stated finite union.

Each eligible configuration is recognized from the validated raw snapshot. Ineligible configurations are paid skips; failed eligible configurations remain in the cumulative ledger. The first accepting configuration determines `SUPPORTED`. All eligible failures produce only `UNSUPPORTED_FOR_THIS_LIST`, unless the separately charged exact direct fallback is requested. Invalid field/root, canonical-residue, shape, or metadata errors cannot become a successful fallback. Budget exhaustion returns no output and no nonmembership claim.

Certificates are immutable, raw-bound canonical tuples. Supplied certificates do not control execution. The API first rederives a fresh certificate, then compares through exact built-in types and bounded canonical shape, then executes that fresh object. Hostile subclass equality/iteration hooks were not invoked in the independent tests. No public guarantee is assigned to calling implementation helpers outside the documented raw API and their internal preconditions.

## Mathematical review

### Sparse raw-row membership

The complete zero scan precedes sparse recovery and is charged, including R=0. Nonzero recovery uses geometrically increasing bounded Berlekamp-Massey trials, an exhaustive scan of the admissible grid nodes, quadratic Lagrange moment inversion, and reconstruction of every row sample. A low-order accidental recurrence cannot generate false success. A k-mode grid signal has a k-degree recurrence and distinct grid roots, so the sparse route is complete once its cap reaches k with M >= 3k. If the permitted sparse threshold is reached without recovery, the separately charged direct short transform supplies exact support membership; lengths 1 and 2 are explicit base cases.

The root polynomial orientation agrees with the positive-sign character expansion; recovered amplitudes are normalized. The direct short transform divides by M before producing event amplitudes. No caller support labels are trusted.

### Newton reconstruction

The d-th backward differences and the first d arbitrary raw anchors determine every row by the finite-difference recurrence. The code's anchor coefficients are the forward differences of unnormalized short spectra. The finite binomial-geometric kernel is correct at zero tail length, at z=1, and at other roots, where the batch inverse has no zero denominator. The factor M converting normalized event amplitudes to unnormalized short spectra appears once on every event. Each event updates its Q matching output bins, rather than an uncharged scan of all N bins. All N outputs are explicitly initialized and written.

### Optimal reset recognition and output

A reset suppresses exactly one fixed transition. Removing the largest B-1 costs therefore minimizes retained event count. The saturated R+1 marker is sufficient: any transition with true cost >R must be reset in every feasible representation. Before rejection, adding another nonnegative transition cannot decrease the sum outside the current largest B-1 costs. Thus early prefix rejection is sound; acceptance removes every marker and retains exact decompositions of total size <=R.

The implementation retains decompositions for current exact top-cost rows, allowing a later larger cost to displace one into the retained set. Ties are deterministic; zero-cost reset candidates are omitted. Independent subset enumeration confirmed feasibility and exact top-cost tie behavior when all costs are known. On acceptance, every saturated marker is removed, and every unknown true marker cost exceeds every unsaturated cost. The remaining reset positions are the largest exact costs. Thus saturation preserves the optimal retained total even though removed marker costs need not be recovered.

Each reset starts an arbitrary raw anchor and terminates the previous interval's event tails. The interval kernel and frequency-label mapping produce the same negative-sign, unnormalized DFT as the independent matrix oracle.

## Resource and trust boundaries

The accepted meter is a declared logical field/scalar-inverse/word model. It includes exact instrumented algebraic operations and conservative prepaid semantic word-administration envelopes. It is not a measurement of Python bytecode, allocator behavior, garbage collection, RSS, CPU instructions, integer-bit operations, serialization bytes, or elapsed time. Caller-owned input memory and result/diagnostic physical storage do not become bounded by `work_limit`. Malformed huge Python integers are rejected by value/type rules; the physical cost of inspecting their representation is not promoted into a bounded-bit guarantee.

The reservations cover validation, root preparation, each full eligible recognition attempt, certificate comparison, accepted execution, and fallback preparation. Explicit arithmetic/read/write counters may conservatively double-charge administrative work. Source inspection confirms the semantic loop families underlying the envelopes: geometric sparse caps, quadratic moment recovery, short direct transforms, bounded top-cost maintenance, anchor transforms, output/event loops, and bounded certificate shape. The finite caps and source-bound contract matter; this review does not silently interpret the chosen constants as a physical resource theorem.

Every failed sparse trial and every rejected earlier configuration remains charged. Newton recognition can charge its final failed row to remaining R; reset recognition can charge up to B discarded/current rows to BM² and retained modes to MR. Root preparation and prime/root validation are paid. Primality's bounded trial-division work is separate from the inherited supplied-prime asymptotic theorem.

The direct fallback reuses the already paid root table, pays its own preparation, then pays exactly N² products, N² additions (including addition to the initial zero), and N output writes. Its complete cost is the sum of earlier attempts plus fallback, never their minimum. Insufficient budget never triggers an unbudgeted fallback, and an abort at the final output-write charge returns no output.

## Rebuilt saved controls

1. N=16, p=17, omega=3, x=[1,2,3,4,2,2,2,2,3,3,3,3,4,4,4,4]. Public list accepts index 2: Q=4, d=2, R=0. All 16 outputs match both the independent DFT and the historical saved output. This establishes reachability in the fresh API; the unchanged legacy failure remains historically true.
2. N=12, p=13, omega=2, x=[9,4,3,5,11,2,7,6,2,7,10,0]. Q=3 has transition supports [4,4] and is paid then rejected; Q=2 has support [2] and public index 1 accepts. No implicit all-divisor search is inferred.
3. N=16, p=17, omega=3, x=[0,4,5,6,0,0,1,2,0,0,1,2,0,0,1,2]. Transition costs are [4,1,1]. Public index 3 accepts with reset at t=1 and two retained events. This realizes the prior optimal-reset repair on raw data.

## Verification results

Cold authored suite: 11,224 raw membership cases; 9,894 output vectors and 169,364 exact output bins; 9,475 exhaustive realized reset cases; 4,582 exhaustive short-row budget cases; 1,965 generated sparse-row cases; malformed-input/certificate and fee-boundary controls. The newly produced `TEST_RESULTS.json` is byte-identical to its sealed candidate version.

Independently authored review suite:

- 14,397 raw membership calls
- 12,280 complete output vectors and 126,591 exact output coordinates
- 8,424 exhaustive small raw/configuration cases
- 800 random raw/configuration lists
- 314 constructed Newton boundary cases and 4,856 constructed reset boundary cases
- 9,277 brute reset-subset optimality comparisons
- 99 malformed/hostile typed-input cases
- 138 adversarial certificate cases and 16 changed-raw certificate-binding cases
- 1,027 separately selected budget-boundary cases across recognition, certificates, reset saturation, repeated failures and fallback
- A 16-failed-attempt additive fallback control
- 5,928 independent finite-sum kernel identities
- 1,011 sparse-row membership/cap boundaries through M=256 and 14 exact zero-scan controls

All passed. Finite checks corroborate the source and algebraic review; they are not an exhaustive enumeration of every input in the bounded domain or a proof of unrelated asymptotic or production claims.

## Reproduction

From this review folder, run `python independent_checks.py` and `python kernel_identity_checks.py`. They import only `cold/alg062_dispatch/bounded_dispatch.py` from the verified candidate extraction. The embedded candidate ZIP is also preserved. To rerun its authored suite, extract it into a fresh directory and run `python test_dispatch.py` inside `alg062_dispatch`. Verify the candidate and review manifest hashes before relying on relocated bytes.

## Scope and remaining work

ALG-004 and ALG-006 may receive optional narrow cross-references only. Their tensor/fiber and shear/orbit/confluent recognizers were neither integrated nor recertified. ALG-079 receives no status change from this review.  Closing this bounded implementation gate does not close broader migration, stable numerical computation, unbounded resource analysis, or unrestricted FFT objectives.
