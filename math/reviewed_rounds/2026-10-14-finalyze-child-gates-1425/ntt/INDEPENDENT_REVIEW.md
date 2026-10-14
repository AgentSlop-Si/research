# Independent ACCEPT: complete frozen 288-vector NTT expected-output gate

14 October 2026. Decision: **ACCEPT_FULL_288_FROZEN_EXPECTED_OUTPUT_CORPUS**.

The finite expected-output obligation is complete and may be marked CLOSED at that exact child scope. No output-generation or output-acceptance task remains for the frozen corpus. The broader `ENGINEERING-NTT-BASELINE-20261012` parent remains open at its existing priority 43; 43 is not its stable ID.

## 1. Exactly what is accepted

The unchanged corpus contains 288 vectors at n=2,4,...,262144, sixteen cases per length. For p=998244353 and w=3^((p-1)/n), the accepted output is

    y[k] = sum_j x[j] w^(jk) mod p.

The exponent is positive, the transform is unnormalized, and output is in natural frequency order. Every value is a canonical residue, serialized as exactly four little-endian bytes without a header, in the original manifest order.

All **8,388,576 coordinates and 33,554,304 serialized bytes** were independently reconstructed and compared coordinate-by-coordinate and byte-for-byte. New accepted coverage is **128 vectors, 8,355,840 coordinates and 33,423,360 bytes** at n=2048 through 262144. The initial 160 vectors are byte-identical to the two previously accepted artifacts; their complete 130,944-byte prefix is preserved.

The complete expected-output SHA-256 is:

    ac4216d4a9d771723becee12765de9685a0b171e6785e9a047bc05a9fb1136d0

The accepted producer archive is `Paid_NTT_Full_288_Frozen_Corpus_Candidate_2026-10-14.zip`, 40,370,584 bytes, SHA-256:

    d05b25329a7e89637973eb74ab54f3535971ad31b84f0bcb6bdad096058f4a2d

Its thirty unique safe-path members pass CRC checks. Its twenty-nine-entry manifest covers every member other than itself, with exact size and SHA-256 checks. Every archived member is byte-identical to the actual candidate workspace inspected by this review. The archived proof and paid ledger are included in that verification, not assumed to match an earlier draft.

## 2. Independence and source binding

The reviewer implemented and sealed an iterative radix-2 **decimation-in-frequency** evaluator before reading the producer's recursive radix-4 **decimation-in-time** implementation. Only the reviewer's newly authored C++ and Python verification programs were executed during this review. No producer program, historical source, inherited generator, earlier checker or benchmark was executed, imported, evaluated or used as a library.

Both implementations use Cooley–Tukey mathematics. They are independently authored implementations with different splitting, traversal and output-order mechanisms; they are not unrelated mathematical algorithms. Agreement is supported by the exact recurrence proofs below, direct matrix controls, pinned roots and complete output comparison. It is not the only correctness argument.

Final reviewer C++ SHA-256:

    9f7763b2a6eebe719477491391717fea6ef310b044e3389f4d12bda307f7705d

Producer C++ SHA-256:

    5137ca0470688b54a4913ed30bfc0219ba753b57f47898e233e852a24bc0a8a9

The first reviewer design seal preceded two whitespace/indentation-warning repairs. The final executed source, launcher, binary and exact arguments are bound by `PREEXECUTION_SEAL.json`; that seal, not the earlier design digest, identifies the scientific run. The final compilation has no diagnostics.

The reviewer independently verifies the original corpus manifest, all 288 per-vector extents/hashes, original order, canonical values, all eight named deterministic input shapes and full corpus bytes. No dense-input generator is run. Corpus SHA-256 is:

    f07e9e1c550420ae431ee64a60e73449b1dcffce105bf452653972dbb7a7bba7

The original protocol SHA-256 is `e97f0f3da08ed17804169262fb8f31872032f53ab708091419af4b2eec28f3dd`; the corpus-manifest SHA-256 is `915115218da6f77a6386e5d65b27c8557ac69659538eb5eda0610617f5ee4639`. Input and prior-output bytes are hashed again after the scientific run. All remain unchanged. The producer's ten copied input bindings are also verified, together with its source seal and binary identity. `CANDIDATE_ARCHIVE_VERIFICATION.json` and `CANDIDATE_SOURCE_HASHES.json` bind this acceptance to the final archive.

## 3. Independent exact radix-2 DIF proof

Fresh trial division through floor(sqrt(p)) establishes primality. The exact factorization p-1=2^23*7*17, and nonunity of 3^((p-1)/q) for q in {2,7,17}, establish that 3 generates the multiplicative group. Each dyadic width therefore has the specified exact-order root. The code also checks w^n=1, w^(n/2)=-1 and the quarter-root square where applicable. Merely choosing any primitive root would be insufficient for the pinned sign/order contract.

At width n=2m, define for j<m

    s_j=x_j+x_(j+m),
    d_j=(x_j-x_(j+m)) w^j.

For even frequency 2r, the transform is sum_j s_j (w^2)^(jr). For odd frequency 2r+1, it is sum_j d_j (w^2)^(jr). This follows by pairing the two input halves and using w^m=-1. Thus each descending-width step creates the correct even- and odd-frequency subproblems. The stage root freshly generated from 3 agrees with the appropriate squared parent root. Induction to width two proves all leaves.

DIF orders those frequency choices from the low bit first. Scattering leaf index i to its exact fixed-width bit reversal therefore restores natural frequency order. The reviewer constructs that index directly from binary digits and does not read a producer or historical permutation table. Scalar roots are regenerated at each width; no uncharged cache or inherited root table is used.

The public reviewer routine rejects lengths below two, above 2^18, nonpowers of two and lengths not dividing p-1, and rejects every noncanonical input. It copies input into its work array and allocates a distinct natural-order output. Input byte integrity and value immutability are checked. Private control cases do not expand the accepted corpus scope.

## 4. Producer source review

The exact `fresh_radix4.cpp`, Python launcher, proof, declaration and source ledger were read as inert text after the reviewer evaluator was sealed.

For n=4m, splitting A(z)=sum_(s=0)^3 z^s E_s(z^4) gives four child transforms with root w^4. At a fixed child frequency k, let a,b,c,d be those values multiplied by 1,w^k,w^(2k),w^(3k), and let i=w^m. The four parent outputs are a+b+c+d, a+i b-c-i d, a-b+c-d and a-i b-c+i d, exactly as implemented. All four child values are read before their distinct slots are overwritten. Different k values use disjoint slots. Private size-one copying and size-two butterflies close the induction, including odd binary exponents.

The strided inputs enumerate distinct residues modulo four; their recursively reached addresses remain inside the original input, while child output blocks are disjoint. The declared maximum length bounds every stride, pointer index, allocation and recursion depth. The public length/divisibility/canonical checks precede output allocation. File input lengths come only from the bounded fixed loop; no unchecked user-supplied signed length is converted to an allocation size.

Both implementations require 8-bit bytes, 32-bit coefficients and 64-bit multiplication intermediates. Canonical additions are below 2p<2^31; products are below (p-1)^2<2^60. Promotion occurs before multiplication. Subtraction branches stay nonnegative and canonical. Codecs explicitly assemble/disassemble little-endian bytes; native endianness is not assumed.

The producer's source loop counts were independently recomputed for all eighteen lengths. Its recorded radix-4 merge, radix-2 base, child-root multiplication and addition/subtraction totals agree. These are abstract source-loop counts, not retired instructions, an optimized minimum or evidence of a speed advantage. Its candidate control logs were reviewed as records; their implementation was not rerun by this reviewer.

## 5. Completed independent checks

The independently executed evaluator and comparison establish:

- All 288 full vectors, 8,388,576 coordinates and 33,554,304 bytes equal the candidate. Full values were compared before confirming aggregate hashes.
- All 128 original small corpus vectors at n<=256 were also checked against the complete direct modular polynomial/Horner definition, covering 8,160 coordinates.
- Five independently selected direct rows were checked for each larger corpus vector: k=0,1,floor(n/3),n/2,n-1.
- Ninety exhaustive vectors over {0,1,p-1} at n=2 and n=4, plus an asymmetric length-eight anchor, were checked against the direct definition. Together with the corpus checks, there were 9,310 direct-coordinate checks.
- All 126 zero/constant/impulse/alternating full-output formulas agree, covering 3,670,002 coordinates.
- Full F_+ squared and inverse/reversal checks cover 16,777,152 further coordinates. These share the reviewer's transform routine and are supplemental consistency checks, not an independent substitute for the all-coordinate producer/reviewer comparison.
- DC, output-sum and input-immutability checks pass for every vector.
- 884 explicit negative controls reject bad lengths/residues, coordinate corruption, a balanced two-coordinate corruption, wrong sign, normalization, output order, extent, range and endianness. Three coordinate mutations per corpus vector include the endpoints and an interior point. These are declared controls, not a claim of exhaustive corruption testing at every coordinate.
- The reviewer recorded 37,284,055 assertions, 955 transform calls, 213,909,897 butterflies and 59,126 modular-power calls. Counters include supplemental and small control transforms. They must not be presented as the cost of computing one transform.

The candidate's per-vector output hashes, extents, labels and coordinate counts all agree with the fresh reconstruction. Both previous accepted artifacts match complete prefix bytes. No earlier result was overwritten or reinterpreted.

## 6. Resource admission and paid work

The independent scientific process completed with hard limits of 180 CPU seconds, 512 MiB address space, 64 MiB per output file and zero core-file size. The child invocation's observed wall time was approximately 1.670 seconds; user/system CPU were approximately 1.569/0.081 seconds. Recorded maximum RSS was 94,400 KiB. Because the Python launcher forks before exec, that process high-water figure can include pre-exec launcher memory; it is not an isolated C++ workspace measurement.

These are verifier resource receipts on this environment, **not transform benchmark results**, throughput evidence, a competitor comparison, or a speedup claim. `EXECUTION_RECEIPT.json` records exact observations and limits. Compilation, corpus hashing, Python all-coordinate comparison, source review, artifact creation and sealing are additional paid work. CPU caps are per process, not a combined 180-second budget for all producer and reviewer work.

The producer independently declares 180 CPU seconds and 512 MiB address space per process, with a 128 MiB single-file cap. This reviewer inspected those controls and source/log consistency, but did not execute the producer or independently witness its original invocation. Its stored outputs are nevertheless fully independently reconstructed here.

All root construction, index generation, scans, input/output copies, full writes, direct controls, inverse controls, hashing, comparison, allocation and setup are charged as work. No numerical oracle, fixture or prior setup is assumed free.

## 7. Terminal scope and open parent gates

**CLOSED / COMPLETE:** availability and exactness of independent expected outputs for the entire fixed 288-vector corpus under `paid-ntt-v2-20261013`. The earlier missing-128-output gate and its proposed 2048/4096-only intermediate step are superseded by this full finite completion. Keep their historical text and files.

**Still OPEN:** source-bound adapters and reviewed source-to-adapter diffs; guarded requests/allocations; schedule-owned paid plans; fixture ownership/lifetimes; full-output sinks; diagnostic and release binary identities; type-width/resource/sanitizer evidence for the inherited schedules; every inherited schedule's full-corpus correctness; session pre/postflight checks; and any separately authorized timing. The historical later-review-body hash `32b9e8e7c33b69633e1616188b59e0f9ad643677680bbb5b6175ee5900ddf4d8` remains missing. Matching C++/CSV or producing this reference corpus does not recover it.

There is no acceptance here of a production NTT, benchmark readiness, a faster transform, arbitrary-length/Bluestein behavior, integer/CRT reconstruction, an all-size scientific claim, novelty or parent closure. The accepted finite corpus is a correctness oracle for later work, not a substitute for validating the actual schedules against it.

## 8. Deliverable and reproduction

`ALL_COORDINATE_COMPARISON.json` records every vector's exact output hash and compared coordinate count. `RESULTS.json`, `RUN_STDOUT.json`, `PER_VECTOR.tsv`, `INPUT_BINDINGS.json`, the preexecution seal and resource receipt preserve the fresh independent run. The original candidate archive contains the complete corpus and accepted output artifact. The review archive need not duplicate those large bytes; it binds their exact identities above.

For fresh reproduction, compile only `independent_dif.cpp` with a C++17 compiler, then invoke the resulting program with three paths: the candidate's `inputs/corpus_inputs.bin`, a new output file, and a new per-vector TSV file. Enforce the declared resource limits before invoking it. The independently generated full output must have the SHA-256 above and equal the candidate's full output byte-for-byte. The workspace launcher and comparison scripts automate the same flow when the preserved sibling directories are present. No code from the candidate archive needs to be executed.

No Sheet, GitHub or other external service was written during this review.
