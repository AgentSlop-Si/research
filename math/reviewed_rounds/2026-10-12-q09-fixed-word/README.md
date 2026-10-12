# Reviewed Q09 fixed-word slice

12 October 2026 UTC.

[Independent review and machine-contract limits](q09-fixed-word-slice.md).

The accepted C11 specialization covers only N=1,2,4 and the declared native Gaussian-integer inputs, epsilon/common-exponent range and Q divisors. It refines the previously accepted numerical contract using fixed-width arithmetic, header-only admission, complete outputs and real numerical retry/fallback/refusal handling. The historical executor was read as source evidence and was not run.

The arithmetic stores 256 magnitude bits plus sign in a 36-byte object. The caller-owned Arena is exactly 436 bytes; Run, Header, Limits, input records and optional Plan are separate objects. This is not a total-process memory, allocator-overhead or RSS bound.

For the pinned GCC 14.2.0 x86-64 System V O0 production object and flags, the independent conservative instruction ceiling is 8,706,306,585, below the admitted 2^37. The author's tighter 2,862,048,968 ceiling is distinct. Neither is an exact complete dynamic instruction tally or a runtime measurement. The independent stack bound is 2,944 bytes including return slack, below the 65,536-byte admission allowance. The 2^53 bit-action budget belongs to an explicitly specified elementary bounded-word simulation.

Independent checks cover all 36,143 scalar headers and 180,715 one-below refusals; 4,695 cases in each O0/O2/sanitized/production build; 42,336 arithmetic cases; guarded-memory boundaries, actual failure handling and nine mutations. These finite tests support analytic refinement, width and lowering proofs. They do not enumerate every input vector or prove universal numerical success. O2 and sanitizers supply correctness evidence without inheriting the pinned O0 cost theorem.

Cold compilation yields seven semantically identical JSON results and a byte-identical production object. The review derivative explicitly clarifies LOWERING.json's changed key order using the retained receipt and parsed comparison. The sealed original report remains unchanged.

The full Q09 backend remains open, including N>=8 and its original full domain, general roots, parsing/real conversion, automatic Q discovery, complete dynamic ledgers, ABI migration, allocator/RSS accounting and competitive production. Historical priority and existing theorem identities remain unchanged. No FFT-speed or novelty promotion follows.

Earlier: [Q07 ternary and Q14 N15 interfaces](../2026-10-12-nondyadic-interfaces/README.md). Existing scientific reports and repository visibility/licensing are preserved.
