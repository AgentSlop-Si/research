# Q16 next executable gate after sparse success acceptance

13 October 2026 UTC. Source-bound gap analysis and bounded interface lemma. No new acceptance verdict.

## Conclusion

The accepted sparse success contract supplies the E(beta) mathematical interface used by the recovered all-length existence theorem, on the latter's normalized input domain. It is stronger in probability than that interface requires. There is no additional missing general sparse-recovery theorem identified here. The remaining separation is between accepted mathematical existence and an accepted source-pinned all-length executable.

The smallest standalone implementation gate is an exact paid constructor from the theorem's common-exponent raw input x to the literal pinned DyadicSource type, with complete validation, zero handling, max normalization, centered indexing and immutable copies. This is an arbitrary-length exact-input task, distinct from the already accepted bounded ALG034 producer-output adapter.

An implicit source is optional for the outer O(N) theorem. Since 4N <= M < 8N, a fully paid M-entry source costs O(N) growing words. It can feed the currently accepted tuple-only sparse code without changing that code. This is a representation variant of the recovered edition, whose Section 2 explicitly chooses to store only N entries. One must disclose that variant rather than claim the current code implements an implicit source.

The accompanying lemma resolves this representation/applicability question with an explicit finite construction. It does not claim that a new production wrapper has been implemented or independently accepted. No scientific program was imported or executed in this analysis.

## Evidence bindings

The full local paths, SHA-256 values and sizes are recorded in EVIDENCE.json. The following abbreviations identify the inspected bytes.

- S: q16_success_independent_1633/INDEPENDENT_REVIEW.md, SHA-256 2baf544af1fe8670728ea0ed300b7dcea6069ca5fc3c26823df3262f26b24e97. Byte-equal to its member in the independent acceptance ZIP, SHA-256 4ebd428764c96ec2c233db76604fc47b3705fa3489850ab0b2a468c7a3f17333.
- E: q16_success_bridge_audit_20261013/sources/RECOVERED_EDITION.md, SHA-256 0a7733e2ac1d1c32cf70609ba0db151a13a73765107907aec44045daaf0a58f5.
- B, P, T: the same sources directory's buckets.py, pipeline.py and fair_tape.py. Their full hashes are in EVIDENCE.json and match the frozen sparse-bridge evidence ZIP.
- H: q16_conformance_20261013/src/q16.py, SHA-256 710a49f6a0c6a0f709f3acd35cb10f4f499dd57b6204d4aaf77b8662dc5ef65d, with its README.
- A: paid_source_adapter_independent_1618/REVIEW.txt, SHA-256 b481803172638f847edf296cd5d32272bc4a73e730e979cb5ca15cffb3f7b4c7.
- P05: q16_recovered_from_context_20261013/reconstructed/P05_ACCEPTED.md, SHA-256 02ec40df49f0585c57f98d3af7cbb9867216773f98a2998db9d51237fd69b787.
- Transfer: the same reconstructed directory's UNIFORM_TRANSFER_LEMMA.md, SHA-256 fed947dce547463d3829aadfe9f6e23410fb70a0b139a3b8da64d399a4cc8a9d.

E and the inspected six-component interface sources are byte-equal to the corresponding members of the frozen sparse-bridge candidate ZIP, SHA-256 55c074877d47b7c0f8d0d6f5f1394005b650ff29a428b9180e6de34d488d5f6f. The recovered-edition review, SHA-256 579f7f4515c2e744a12821c217bdb696801b76b5a3eb0ce8db156ba8190de34d, accepts edition fidelity and preserved historical mathematical status; it is not an integrated executable acceptance.

## Actual theorem and target

E Section 1 fixes 0 < alpha < beta < 1/2, rational beta, c > 0, integer d >= 1 and integer D > alpha+4. For every integer N >= 1, M=2^ceil(log2(4N)) and x_j=(a_j+i b_j)/2^e with |a_j|,|b_j| <= 2^(dm), 0 <= e <= dm and m=log2 M. The input is in declared bounded binary fields.

The accepted existence claim is a finite-word randomized algorithm returning all N coordinates y, with

    Pr[||y-U_N x||_infinity <= C_(alpha,beta,D) N^(-alpha) ||x||_2] >= 1-N^(-c),

and O_(alpha,beta,c,d,D)(N) growing-word work and storage on every tape. U_N is the negative-sign unitary DFT. It is neither exact Fourier evaluation nor relative-l2 recovery, an O(N)-bit claim, or a new analytical exponent.

S accepts, for each fixed globally valid deeply immutable v with Cartesian amplitudes <=1, R=||v||_2>1/2, numeric exponent-value bound F=O_d(m), exact source sparse guards and fresh independent fair tape,

    Pr[||zhat-U_M v||_infinity <= 4 M^(-beta) R] >= 1-M^(-3).

Its output grid is P=16m+16; support is at most 2qT; every returned Cartesian magnitude is <3M^2. Its every-tape auxiliary finite-arithmetic cost is O_(beta,d)(M^(1/2+beta) poly(m)). These are precisely the front-end data required by E Sections 4 and 6, with stronger failure probability. They do not themselves produce the outer N-dimensional transform.

## Gap ledger

### 1 Global source validity and exact normalization

Status: proved in the outer mathematical specification, not performed by the accepted sparse source wrapper.

Evidence: E lines 62-79; S lines 11-21, 43-49 and 185-187. B lines 19-29 and 168-181 accept an already represented source, checking only reached samples. P lines 103-116 and 188-197 retain caller duties. H lines 134-150 contain a normalization fixture but do not construct the accepted DyadicSource.

Smallest completion evidence: a fresh source-pinned exact-input constructor, complete validation/zero handling before randomness, correct k0 at exact powers of two, a copied immutable centered source and paid source construction. Do not infer global validity from sample checks. Do not reuse the ALG034 requantization/floor assumptions for exact x.

### 2 Source storage versus random access

Status: exact tuple-only current source interface; implicit callback implementation absent. This does not obstruct the outer O(N) resource bound.

Evidence: B lines 168-181 require type(source) is DyadicSource, type(source.values) is tuple, length exactly M, and literal source.values[index]. P lines 111-116 has the same type/length gate. E line 75 instead describes an N-entry implicit source. H lines 118-131 gives a mutable Normalized record with a callback returning numerator pairs, not the accepted source type or its full dyadic cell schema.

Completion alternatives: (a) paid full centered M-tuple construction and a declared O(N)-equivalent representation variant; or (b) modify the accepted sparse source reader and independently recertify that change to support an N-entry adapter. Alternative (a) preserves accepted numerical source bytes and is the smaller gate. Caller source storage remains outside the standalone sparse auxiliary claim and must be included explicitly in the outer total.

### 3 Existing bounded ALG034 adapter

Status: accepted, but for a different bounded conditional problem. Not a substitute for gate 1.

Evidence: A Sections 2, 4, 5 and 8. It accepts only 4<=M<=4096, dyadic lengths, bounded producer-output fields and a genuine external ALG034 producer contract. It normalizes/requantizes Yhat and retains the guard Delta/alpha<=rho. Its ideal second Fourier target remains R P x/alpha, not U_N x. The small M=4/8 cases do not imply sparse-window eligibility. The accepted independent controls and copy charges do not extend this deployment domain.

Required distinction: the exact-input outer adapter has N arbitrary, M between 4N and 8N, no producer approximation Delta, no projection P, no projected-signal floor and no requantization. Its proof uses max normalization directly. The accompanying lemma does not replace or generalize A.

### 4 Exact all-length dispatch and dense fallback

Status: mathematically specified and historically accepted; current sparse executable is not an all-length dispatcher. Existing dense conformance is bounded.

Evidence: E Sections 3 and 8. Sparse requires B|M, B>=4, T>=4, B>=4096k, W<M, plus outer t<M and beta*m>=2. T lines 192-196 and 228-239 rejects failed sparse guards, without fallback. H lines 242-244 caps the nonzero dense path at N<=32; lines 261-273 reject the sparse path. Its README disclaims a universal scalar-loop proof and complete growing-word accounting.

Smallest completion evidence: a total dispatcher that handles zero and N=1 exactly, evaluates the exact rational guards, and routes every other failed-guard input to a universally certified dense root/scale and accumulation path. A finite exceptional set proves asymptotic absorbability, not that the current N<=32 harness covers it.

### 5 Outer interpolation and active coefficient preparation

Status: inherited mathematical P05 identity/tail premises; no source-pinned full coefficient/scatter realization established by the current acceptance.

Evidence: E Section 5; P05 S6; S lines 177-179. With centered embedding, U_N x'=D_phase B_full U_M v. Each retained row has t=32Dm+4 entries, |C_lk|<3, and omitted-tail operator norm <=12*4^(-Dm). Only active incidences may receive poly(m)-cost root, ratio, power and phase evaluation.

Smallest completion evidence: exact wrapped incidence enumeration with no missed/duplicated row contributions; source-pinned coefficient generation at complex absolute error eta=2^(-(D+3)m); exact zero limits; denominator lower bound 2/(NM); fixed scalar budgets and a charge O(S t poly(m)). Preparing one transcendental phase for every dense output would introduce an unabsorbed N poly(m) pass.

### 6 Accumulation, final rounding and exact scale back

Status: source output supplies the required every-tape envelope; full outer arithmetic composition is not accepted. H's injected row fixtures are not active generated-coefficient execution.

Evidence: S lines 159-167; E Section 6; H fixture_row_sum after line 340. Given p=(D+3)m+g and w=P+2m+2, signed allocation p+w+4+ceil(log2 t) bits suffices per Cartesian accumulator. Final row rounding is once to b=ceil((beta+2)m), followed by exact power-of-two scale back.

Smallest completion evidence: bind actual accepted sparse outputs to actual generated coefficients and exact row incidences; pay N accumulator initialization and output/rounding; exercise failed-tape maximum magnitudes, cancellation, empty support and all signed rounding/scale boundaries. A fixture accepting supplied coefficients does not certify coefficient generation.

### 7 Independent J-call amplification

Status: proven algebra and accepted single-call fair-tape decoding; complete outer J-call orchestration remains unimplemented in the pinned sparse wrapper.

Evidence: E Section 7; S lines 139-157 and 177-179. J=2 floor(c)+3 is fixed. Each complete run needs a separate block of 2(4m+1)(2m-1) fair bits; J output vectors feed exact Cartesian medians. Probability is already simultaneous, so no additional N-coordinate union bound is needed. The sqrt(2) median loss remains.

Smallest completion evidence: actual disjoint role/run blocks, complete-call binding, exact J medians, paid dense arrays and all-tape accounting. Tape uniformity and input independence remain declared probability assumptions; a parser cannot prove physical entropy.

### 8 Full path conformance and machine boundary

Status: open. Neither accepted individual components nor the mathematical theorem imply a source-pinned complete program or a practical crossover.

Evidence: S Sections 8-10; E Section 11; the bounded harness README and ledger.

Completion evidence: pinned composition source and dependencies, universal code-to-proof bounds, complete input/output and copy accounting in the declared growing-word model, independent finite controls against certified reference enclosures, and honest limits on host/interpreter/allocator certification. Do not demand a physical theorem-scale test as a replacement for the universal argument, or use reduced fixtures as such a test.

## Recommended next task and stopping condition

Implement and independently review only the exact common-exponent x-to-DyadicSource constructor described in MATERIALIZATION_LEMMA.md, preserving accepted sparse source bytes. Pin its binary or explicitly built-in finite-record input grammar and complete output copy/cost ledger. Its output should contain the exact source, M, k0, symbolic lambda exponent k0-e, and a separate zero result. No FFT execution is needed for this gate.

Stop when that adapter is accepted on its declared all-size finite-input/source model, or when an exact interface/cost counterexample is found. Then address the active outer coefficient/scatter path and all-length dense fallback as independent next components. Do not report the all-length executable complete merely because the adapter passes.

No Sheet, GitHub, existing scientific source, or accepted record was changed. No general FFT claim follows.
