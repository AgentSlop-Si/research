# Independent ACCEPT: Q09 fixed-word bounded slice

Review date: 12 October 2026 (UTC). Verdict: **ACCEPT, limited to N in {1,2,4} and the pinned implementation/ABI.** No candidate source repair was needed. The broader Q09::primitive-bit-reservations gate remains open. This does not retire the full-domain backend obligation or change a theorem, attribution, novelty, priority, or FFT-speed claim.

## Sealed subject

- Candidate archive: Q09_Fixed_Word_Slice_CANDIDATE_2026-10-12.zip
- Candidate archive SHA256: 365dd7c3177b568fac10d229dc6abc0492f384e29ce619c05e80d2d70efefd4c
- Candidate q09_fixed.c SHA256: 63e5c15e3c5197c26668a23d3e059c1620ba082d0d956a509c4c1b34f08f1684
- All 38 candidate manifest members and the four predecessor-source bindings were checked independently. Archive extraction rejected unsafe paths. The accepted reference was read as text only; no historical executor was run.
- The independent production rebuild has SHA256 2ef175604a4c7d999c60850d001ae125be3d23e0bd1904fc0d9581187397f648 and is byte-identical to the sealed candidate production object. A further cold rebuild in a new temporary directory reproduced those exact bytes.

## Accepted claim and limits

The new C11 entry point admits N=1,2,4, Q absent or a power-of-two divisor, the inherited bounded epsilon/common-exponent ranges, and native int32_t Gaussian-integer input records with each component magnitude below 2^(4 max(1,log2 N)). Budget fields are uint64_t. This is a numerical specialization of the accepted source contract, not a compatibility claim about its complete Python API.

Eight uint32_t magnitude limbs plus an int32_t sign occupy 36 bytes. The capacity is **256 magnitude bits plus sign**, rather than a 32-byte two's-complement signed integer. The core has no heap call or undefined external symbol. Its exact caller-owned Arena size is 436 bytes. Run (112 bytes), Header (20), Limits (40), and at most 32 input bytes are distinct caller objects outside that Arena. Standalone Plan is 56 bytes when the caller separately requests one. Valid extents, alignment, lifetime, nonoverlap, and no concurrent mutation are preconditions.

The production resource proof is pinned to GCC 14.2.0 on x86-64 System V, with -std=c11 -O0 -fno-inline -fno-optimize-sibling-calls -fno-stack-protector -mno-red-zone -fstack-usage and Q09_NO_MAIN. O2 and sanitizer builds are correctness evidence, not a transfer of the pinned cost theorem to those binaries.

The inclusive admissions reserve 2^17 metered helper dispatches, 2^37 own-code word/instruction actions, 2^53 actions in the stated elementary bit-simulation model, a 436-byte Arena, and 65,536 bytes of stack allowance. Header and budget refusal precede input reads and Arena writes. Fixed Run/header administration necessarily occurs before admission; a zero budget does not make the entry prelude free. Stack allowance is a checked contract backed by a frame bound, not an operating-system stack reservation or available-memory probe.

The 436-byte claim means object layout and the demonstration allocation request. It excludes allocator metadata/usable size, pages, RSS, total process memory, and OS availability. Instruction counts are not cycles, wall time, hardware micro-operations, or silicon bit-operation counts.

## Numerical and width review

For L=1,2,4 the frozen reference constructs exact Gaussian-unit point roots. All pre-normalization butterfly operations consequently remain exact grid points. Its linear transform is the same negative-sign Fourier map as the new direct specialization. A fresh symbolic-basis check verifies 14 real/imaginary basis vectors across the three lengths, establishing equality of these integer-linear maps for all Gaussian-integer vectors.

Both sources use floor(S/sqrt(N)) = isqrt(floor(S^2/N)), the same one-step enclosing upper endpoint, signed endpoint ordering, floor midpoint, squared radius, periodic gate, precision schedule, target comparison, and dense frequency placement. The descending periodic scatter does not overwrite an unread source. Zero, general, periodic, and failed-gate fallback semantics agree. The reference's historical bookkeeping dictionaries are intentionally not reproduced. This bridge is a source/refinement proof plus a fresh independent oracle; it is not a claim that the historical implementation was empirically executed.

Input/group/Fourier partial components have magnitude <=1020. Energy is below 2^19, group energy below 2^21, and scalar gate products fit uint64_t. Precision is at most 44 initially and 76 on retry. The candidate's non-probe intermediate bound of fewer than 191 magnitude bits is conservative. Greedy square-root trial values are below 2^128, so their squares fit all 256 magnitude bits exactly. Schoolbook limb accumulators are bounded by (2^32-1)^2 + 2(2^32-1) = 2^64-1. Shift widths, subtraction borrow, overflow detection, negative floor-halving, and input INT32_MIN rejection were checked. magbits only sees already bounded magnitudes. No signed-overflow assumption is used.

Every accepted API call initializes its own meter and Arena, so no prior contents or earlier failure can affect the next result. Invalid data stops at the first bad pair. A forced comparison rejection occurs after real numerical work, with one rejection exercising successful retry and two exercising terminal refusal. Terminal refusal scrubs output, leaves certified=0, and keeps the entire reservation. The production build ignores the hook. These controls establish failure-path handling, not existence of a naturally failing legal input or a universal-success claim.

## Actual primitive and physical-storage audit

The candidate helper meter counts tick calls exactly. It is not a complete dynamic instruction counter. The independent audit instead inventories the newly compiled production object, resolves every direct call, rejects unresolved external/indirect calls and recursion, and applies source-checked loop visit ceilings.

Using deliberately looser ceilings than the author's audit gives a conservative upper bound of **8,706,306,585 executed own-code instructions**, below 137,438,953,472 = 2^37. The differing author figure (2,862,048,968) reflects tighter conservative visit ceilings, not an empirical timing disagreement. Loads, stores, control flow, stack setup, returns, and scalar administration are included. No repeat-string or floating-point arithmetic instruction is used.

An additional independent partition checks the actual charging mechanism. Each metered helper pays for its own instructions and reachable unmetered helpers; descendant metered calls pay themselves. The largest local bound is 34,464 instructions, below the 2^20 charge. Separately paid outer, attempt, and direct-Fourier administrative blocks are bounded by 322,025, 12,688, and 2,848 instructions, also below 2^20 each. Thus full admitted executions, including failed work, are covered by the conservative charges rather than counting only arithmetic results.

The specified bit expansion assigns at most 2^16 elementary actions per bounded <=64-bit arithmetic/control instruction or <=128-bit transfer. This is an explicit bounded-word simulation with RAM access semantics, not a physical CPU assertion. Multiplication/division are expanded by schoolbook/restoring algorithms. The resulting full 2^53 reservation is sufficient within that model.

The independent nonrecursive stack audit obtains 2,880 bytes of summed compiler frames, maximum depth eight, and **2,944 bytes** after an extra eight-byte return-address allowance per level. This fits the admitted 65,536. Compiler-generated temporaries and arithmetic scratch arrays are part of those frames. Source/compiler/ABI/flag changes require a fresh audit. The new Arena/frame accounting is not a reinterpretation of the predecessor's logical-slot ledger.

## Fresh evidence

Independent suites, written separately from the author tests, report:

- Exhaustive admission checks for all 36,143 legal scalar headers (including every epsilon numerator and common exponent), with 180,715 one-field-below refusals through execute using null input/Arena pointers. Source W/P compatibility fields are independently checked.
- 4,695 cases each in O0, O2, and ASan/UBSan verification builds. Each has 3,826 numerical matches, 786 forced terminal refusals, 15 one-unit-below budget refusals, 56 malformed-prefix cases, and 12 bad headers. Exact-budget equality is used throughout normal calls. All four numerical branches occur. Outputs, precision, error ticks, exponents, certification, and attempts are checked against an explicit Fourier-matrix/integer-square-root oracle. O0/O2/sanitized digests agree.
- The same 4,695 cases in hook-free production yield 4,612 numerical matches and the same 83 input/admission refusals, with forced-failure requests correctly having no effect.
- 42,336 arithmetic cases: boundary and seeded-random signed addition, multiplication, shifts, floor-halving, and integer square root. All 8,668 expected overflows were detected; truncated values and widths were also checked. Address/undefined sanitizers reproduce the result. Leak checking was not run or accepted.
- Protected inaccessible pages verify no pre-admission input/Arena access. A bad record placed immediately before an inaccessible page proves prefix refusal does not read the next record. Read-only input, exact arena end boundaries, pre-Arena sentinels, repeated poisoned-Arena calls, and retry-to-zero reuse all pass (11,327 assertions, including individual sentinel bytes).
- Nine deliberate source mutations are detected: DFT sign, negative midpoint truncation, strict versus inclusive gate, missing upper normalization enclosure, wrong dense scatter, removed retry, unsanitized terminal output, admission equality rejection, and off-by-one input magnitude acceptance. Mutation builds are explicitly test-only derivatives.
- Fresh cold compilation reproduces seven semantically identical independent JSON results and a byte-identical production object. LOWERING.json has a different object-key order; complete parsed equality and the cold-output receipt hash are verified.
- The author's inspected rebuild script was separately replayed from the sealed source. Its 9,046-case O0/O2/production/sanitized suites, 18,414 arithmetic cases, and guard/resource audit pass. These remain author-suite replays, separately labeled from independent evidence.

Observed maxima are 1,226 helper tick calls and 1,289,748,480 charged word actions in the independent verification controls. Finite tests corroborate the analytic proof; they are not an exhaustive enumeration of all input vectors. Sanitizers support, but do not replace, the C/object-validity and width review.

## Gate disposition

The accepted bounded scope is:

> Independently accepted C11 fixed-word specialization for N=1,2,4, with exact numerical refinement, header-only admission, both real attempts/fallback/refusal, 256 magnitude-bit arithmetic, 436-byte caller Arena, and pinned GCC/x86-64 instruction and stack bounds. Full-domain production lowering remains open.

The broader backend obligation remains open. N>=8 and the original N<=2^20 domain, general roots, arbitrary parsing/real conversion, automatic Q discovery, exact complete dynamic instruction ledgers, ABI migration, allocator/RSS accounting, wall time, and competitive production performance remain unclosed. Preserve prior source-semantic acceptance and keep historical timings tied to their original source. No external service, repository, or spreadsheet was changed by this review.

Derivative note: private integration instructions are removed. The instruction figure is explicitly labeled as a conservative ceiling. The cold-replay sentence is clarified against the sealed receipt: seven JSON results are semantically identical, while the production object is byte-identical; LOWERING.json differs in key order. No proof, source bytes, cost bound or accepted domain is changed. Original report SHA-256: `dce86cd2ebc3714c9018d03d3f6a77c69c134813e411aecdddde524a3131b1d5`.
