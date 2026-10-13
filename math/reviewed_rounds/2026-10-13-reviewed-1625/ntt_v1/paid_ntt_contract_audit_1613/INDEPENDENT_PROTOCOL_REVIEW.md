# Independent paid NTT protocol audit

Date: 2026-10-13. Review type: source text, file-byte checks, and fresh integer/counting calculations only.

## Decision

**ACCEPT the source-level arithmetic, finite-domain, recovered-file provenance, historical-benchmark limitations, and corpus-byte assertions. REPAIR a small set of protocol definitions before describing this as an execution-ready, fully frozen paid comparison.** The repairs concern measurement semantics and inference, not an observed NTT implementation failure.

No recovered C++ was imported, compiled, or run. No NTT reference was executed, no outputs were computed, and no new performance measurements were made. Existing CSV times are unreplicated historical values. This audit does not resolve the missing later ENGINEERING_NTT_REVIEW.md body or establish that these CPP/CSV files were that review's exact inputs.

Reviewed inputs:

- paid_ntt_contract_1546/PAID_NTT_CONTRACT.md, SHA-256 48a8b113c16df0c43981595068e0959c2efeaa165328a1c7b445f928ba84f377.
- paid_ntt_contract_1546/PROTOCOL.json, SHA-256 62bf456cd6c3514c0dc3bc2790cb1d25259974b02de22b7d0b9167632b53ebc9.
- fft_engine.cpp, 15,015 bytes, 400 lines, SHA-256 0bd324e62b302e4b2e6405c953cb513a93b8840b74137755bd7388b86cddafa7.
- benchmark_final_ntt.csv, 1,565 bytes, 37 lines, SHA-256 1cddc4cb6c8e90a45c367e1abd6e221851bd9922cd8f93fa098d70c9abefd616.
- All other files listed by the contract's FILES_SHA256.json, including corpus, generator, order, constants certificate, count table and checklist.

## 1. Independent checks completed

All 11 listed artifact lengths/hashes and both recovered-source lengths/hashes match. Fresh audit code reconstructed every one of the 288 serialized vectors without importing or running build_static_artifacts.py. Every coordinate is canonical; all per-vector hashes, offsets, lengths, ordering and the aggregate 33,554,304-byte corpus match. Its SHA-256 is f07e9e1c550420ae431ee64a60e73449b1dcffce105bf452653972dbb7a7bba7.

All 144 dense vectors match the stated SHA-256 counter/rejection construction. The correct rejection threshold is 3,992,977,412. There are exactly four accepted preimages of each residue in the accepted uint32 range. This removes modulo-mapping bias under a uniform-word model; it does not make a fixed deterministic corpus a random population sample. The historical mt19937 modulo mapping is different and biased. The contract correctly discloses that corpus change.

Fresh trial division verifies primality, factorization p-1=2^23*7*17, all three primitive-root checks, and all 23 length-root certificate entries. Independent schedule loop counts agree with the closed forms for every admitted exponent 1..23. All 92 STATIC_COUNTS rows and all 36 historical CSV field-count rows agree.

The paired-order file contains all 24 distinct permutations per session, each algorithm in each position six times per session, with the second session reversing the first. These are static schedule properties, not measurements of experimental independence.

Evidence: INDEPENDENT_STATIC_CHECKS.json and the independently authored independent_static_audit.py in this report's directory. The latter performs only byte/integer/counting checks; its own execution duration is not benchmark evidence.

## 2. Four schedule counts: ACCEPT

Let n=2^l, 1<=l<=23. All four have A(n)=nl calls to plusm/minusm together and M(n)=nl/2-n+1 calls to mulm for one forward transform. Multiplication by imag is counted, including j=0. These are source-call counts; they exclude planning, bounds/residue checks, memory traffic, allocation, sink work, inverse scaling and machine-instruction effects.

- Radix2, CPP 57-65: each level has n additions/subtractions. A length-L level uses (n/L)(L/2-1) multiplications. Summing gives nl/2-(n-1).
- Fused4, CPP 74-103: the optional initial radix2 layer costs n additions and zero multiplications. Each 4m block costs 8m additions and m+3(m-1)=4m-3 multiplications. Summing its layers gives the same formula, for both exponent parities.
- DIF4, CPP 111-129: each length-L block costs 2L additions and L-3 multiplications; an odd exponent adds a terminal radix2 layer with n additions. Reverse layer direction and the different permutation do not change these counts.
- Splitradix, CPP 133-154: A(n)=3n/2+A(n/2)+2A(n/4), M(n)=3n/4-2+M(n/2)+2M(n/4), with (A(1),M(1))=(0,0), (A(2),M(2))=(2,0). The stated closed forms solve these recurrences exactly.

The root-table preparation count is also correct. The powm exponent is 119*2^(23-l), with bit length 30-l and popcount 6. The source powm executes 36-l multiplication calls, including its final square. The table recurrence adds n-1, totaling n+35-l. At n=8192 that is 8,214 root-preparation multiplications, in addition to 106,496 transform add/subtract calls and 45,057 transform multiplication calls. At n=262144 the transform counts are 4,718,592 and 2,097,153.

No arithmetic-operation saving over this particular radix2 baseline is established. Equal field-call counts neither imply equal machine time nor disprove a possible constant-factor timing difference.

## 3. Source Plan, timer and correctness findings: ACCEPT

CPP 29-42 allocate both index families, produce the mixed-radix map (including an initial allocation later replaced), produce rev, generate roots, and set imag. benchfair creates one such Plan at CPP 344 and reprints that same ptime for every schedule at CPP 364. That is neither a schedule-owned setup measurement nor a cold setup-plus-transform measurement. The proposed equally applied minimal-plan pruning is a legitimate new variant if its exact diff is reviewed and disclosed; it is not a byte-identical rerun of the historical program.

benchfair timestamps before run_algo at CPP 353 and after its return at CPP 355. The returned vector v remains alive through checksum use and is destroyed at the inner loop's end, after the stop timestamp. By contrast, the local work vector in dif_radix4 and splitradix is destroyed before those functions finish returning their separately allocated outputs. The contract's source-lifetime assertion is correct. It is not evidence of a quantified time penalty, and no guessed deallocation cost should be subtracted.

benchfair contains no full-output comparison. Its sampled checksum cannot establish correctness. The existence of selftest/testheavy is not evidence that either mode passed for the historical measured binary. The old bench makes an algorithm-equality comparison but has only three contenders and its radix2 value is not an independent exact oracle. The old header's per-input labels are wrong for its printed unnormalized count totals; the recovered CSV's adds/muls labels avoid that particular error.

The nominal dedicated-plan and buffer memory ledgers are reasonable lower ledgers for the described 4-byte representation. They exclude allocator overhead, capacity, vector headers, recursive/map temporaries, stacks, and the eight-input pool and must not be called measured resident memory. The transform-call diagnostic still includes internal scratch cleanup that precedes return; only caller-owned input/returned-output destruction is excluded from that diagnostic.

## 4. Domain, guards and correctness oracle: ACCEPT with explicit implementation gates

For prime p=998244353, generator g=3 and n a power of two in [2,2^23], omega^n=1 and omega^(n/2)!=1 establish exact order n. For n>=4, imag=omega^(n/4) squares to -1. No imag multiplication is needed at n=2. On canonical inputs, 2(p-1)=1,996,488,704 fits uint32 and (p-1)^2=996,491,786,299,899,904 fits uint64. A 32-bit signed index is sufficient for all source indices and the terminating loop increment at n=2^23, but the build must enforce its index/byte-size assumptions. Record CHAR_BIT as well as widths; for the specified 4-byte wire/ledger representation require 8-bit bytes and 4-byte coefficients/indices.

The inherited CLI/transform entrypoints are not safe substitutes for the specified adapter guards: run_stdin allocates from n before the Plan guard, normalizes inputs, and the Plan transform methods do not check vector size/canonical range. Bounds, representability, shift and byte-size checks must be in the new adapter; the negative tests are appropriate. p and g are compile-time constants in the source; if the harness exposes configurable versions, wrong p/g must also be rejected.

The independent arbitrary-precision direct definition at n<=256 and independently indexed exact radix2 reference for larger n form a suitable empirical all-coordinate oracle for this fixed corpus. Direct small-length validation, analytic vectors, a separately implemented inverse and summation identities improve independence. They do not turn finite tests into a proof for every input or n>2^18. Expected output bytes and oracle source hashes remain unproduced requirements. The release binary used for timing, not just the sanitizer build, must pass the exact gates; explicitly check input immutability as well as output length, range and values.

The pilot currently inherits the full preflight correctness corpus through n=2^18, even though timing is only n=8192. Retain that distinction in its execution manifest. The separate non-power-of-two/Bluestein caveats in the contract are accurate and remain outside this comparison.

## 5. Required protocol repairs before execution-ready acceptance

### R1. Freeze warm-up input order and sink lifecycle

Contract 95 specifies four "designated" warm-ups, but no artifact unambiguously names them. Contract 109 freezes every measured batch's useful sequence; it does not explicitly settle the discarded warm-up sequence and accumulator state across the enclosing paid-warm and conditional-warm windows.

Minimal repair: set the four warm-up cases to dense_0, dense_1, dense_2, dense_3, in that order, using the same allocation, checks, sink and destruction lifecycle as useful requests. Warm-up sink starts at the fixed seed. Immediately before the useful interval reset the accumulator to the fixed seed, and restart useful input at dense_0. Specify whether each reset and volatile publication is inside each applicable timer; use the identical boundary for all contenders. Publish warm-up and useful accumulators separately if retained. Add these fields to PROTOCOL.json and the expanded trial manifest.

### R2. Resolve validation, fixture and directly measured paid-total boundaries

The request charge list does not explicitly place required per-request input guards in or out of service time. Contract 87 includes "corpus verification" in T_fixture but also calls "Verification/reference generation" separately measured audit overhead. Its workflow permits several fixture provenance/reuse models while contract 9 says only execution-environment configuration remains unbound. These choices affect a paid result.

Minimal repair:

1. State that ordinary runtime request size/canonical checks are inside the paid checked-request lifecycle for every method, and length/overflow checks inside a fresh plan's lifetime are included in paid planning. Independently verifying fixed mathematical constants and oracle correctness is audit work outside primary service timing. If runtime root checks are repeated per plan, include them in plan time and label their operation counts separately from the source's root-generation count.
2. Choose and freeze the workflow fixture route. For a pre-generated corpus, creation of that historical corpus and reference outputs is audit/preparation history; the measured workflow may include necessary file read, deserialization, allocation and integrity/range verification. State whether integrity checks are a required API feature or benchmark audit and count them in exactly one category.
3. Name the fixture lifetime and H explicitly. Do not silently amortize one shared pool over competing algorithms or all benchmark trials and call that the cost of one method serving K requests. A service with a historically caller-owned pool is an appropriate separate resident-fixture metric. A workflow result requires a concretely defined workflow and its own enclosing interval or clearly labeled accounting estimate.
4. Define primary paid-warm batch as one directly measured plan-construction-through-plan-destruction interval, divided by K. Record the conditional useful interval inside that trial; do not make the primary total depend solely on summing stage timers. Stage-diagnostic timing overhead and any separately instrumented runs must be disclosed. Apply the same principle to workflow enclosing intervals; stage sums are reconciliation, not a substitute for a direct total.

This repair preserves the intended cold versus conditional-warm versus paid-warm distinction. It closes ambiguity rather than asserting that the current source has been timed incorrectly anew.

### R3. Qualify the bootstrap's statistical assumptions

The arithmetic definitions are reproducible: medians, nearest-rank IQR indices 11/35 for 48 observations, SHA-256 rejection sampling of block IDs, and percentile ranks 249/9749 are internally consistent. Whole-block pairing is the right granularity; K transforms are not K independent samples.

However, resampling all 48 whole blocks as exchangeable observations does not automatically give a calibrated 95% confidence interval when those blocks are serial and split between only two sessions. Exact order-position balance removes one obvious order imbalance, not thermal drift, autocorrelation, interference or session-by-method interaction. "Conditional on environment and workload" does not state these additional assumptions.

Minimal repair preserving the already frozen resampling scheme: call this a nominal, exploratory 95% percentile bootstrap interval under exchangeability of paired block log-ratios; explicitly say coverage is unestablished under serial/session dependence. Require session-specific paired estimates and plots/tabulation against block order, retain all slow samples, and report material disagreement/dependence as inconclusive for a stable speed ordering. Do not advertise statistical significance from the pooled interval alone. A later confirmatory design can freeze additional independent sessions and a justified stratified/cluster/time-series analysis before collecting data; do not select the uncertainty procedure after seeing a desired winner.

### R4. Scope K=1 and the single-size conclusion precisely

Because every useful batch restarts at dense_0, every K=1 timing uses only dense_0. K=64 uses each of the eight dense cases eight times. Both are interpretable fixed workloads, but the K=1 estimate is not an eight-case average. State this in the summary and PROTOCOL.json. If an eight-case K=1 workload is desired instead, preregister a balanced case allocation and regenerate the expanded manifest before timing; do not retrofit after measurements.

Call 8192 the first tested power of two above forward_auto's n<=4096 cutoff, not an independently established optimal dispatch boundary. The pilot cannot determine a crossover, validate the threshold, or confirm the entire historical ordering curve.

### R5. Correct a minor ordering description

PAIRED_ORDER.json follows itertools.permutations in the explicitly supplied algorithm order [radix2,fused4,splitradix,dif4]. That is lexicographic by those algorithm indices, not by the algorithm-name strings (whose lexical first order starts dif4). The file itself is exact and balanced. Change "lexicographic" to "permutations in the frozen algorithm-index order" in the human description and generator description; no permutation bytes need change.

## 6. Pilot interpretability and required machine binding

With the repairs, the proposed pilot is a useful narrow experiment: one fixed positive-exponent 8192-point forward NTT, four directly called schedules, separately owned pruned plans, matched lifecycle and output consumption, K=1 and K=64, with cold finite-use and deliberately prewarmed service costs separated. It tests whether the historical apparent warm ordering persists under a new, paid API and corpus. It is not strict replication because plans, corpus, buffer lifetimes and sink differ. Raw transform-call diagnostics can help connect the two boundaries but do not restore the missing historical environment.

The frozen design contains 768 primary batches (48 blocks * 2 K values * 2 independently executed cold/warm modes * 4 algorithms), 24,960 useful transform calls, and 1,536 discarded warm-up calls, excluding oracle/correctness/diagnostic runs. Paid-warm totals and conditional-warm totals should come from the same 384 warm trials rather than being treated as independent extra observations. K=1 covers one timed case; K=64 covers all eight evenly. A single n cannot establish scaling or a crossover.

Before compilation/timing, bind the manifest fields already listed: physical CPU/model/stepping, architecture, cache sizes, RAM and NUMA placement, actual core/affinity, single-thread policy and sibling activity, OS/kernel, governor/turbo and observed frequency/thermals, allocator/runtime, compiler version and standard library, standard and exact uniform release flags, separate correctness/sanitizer flags, and source/adapter/sink/binary hashes. Add VM/container status and any CPU quota or shared-host limitation when known; mark unavailable physical/frequency fields unknown instead of inventing them. Record monotonic clock resolution/overhead and process/filesystem-cache conditions. The current cloud machine's existence does not bind the future experiment to that machine.

The resolution gate should apply to positive primary batch durations, with clock overhead quantified separately. If a revised common repetition scheme is necessary, repeat complete cold lifecycles rather than making a reusable plan free; version and freeze the revision before rerunning. Do not call a clock-resolution check a bound on all measurement noise.

## Completion status

This review is complete as a source-only audit. Benchmark execution remains unperformed and requires its own authorization. To move the contract to execution-ready acceptance: resolve R1-R4 explicitly, correct R5, refresh affected hashes, review the resulting adapter/oracle and manifest, and enforce the existing correctness/resource gates. No Sheet or GitHub write was made.
