# Independent acceptance: bounded H16 delete-two/insert-one exclusion

**Verdict: ACCEPT, for the exact bounded family below.** No substantive mathematical or implementation error found.

## Accepted claim and scope

The fixed chronological 32-call radix-two schedule on 16 registers has two distinct original calls deleted; the remaining 30 calls retain their order; one arbitrary unordered pair call is inserted at one of 31 cuts. The complete labeled family has C(32,2) × 31 × C(16,2) = **1,845,120 edit descriptions**, allowing duplicate circuits. Every member lacks at least one input-output path.

This excludes H16, including arbitrary nonzero endpoint row/column scalings and permutations, for arbitrary complex two-register linear maps on the tested pair schedule. Consequently it excludes the stipulated H2/diagonal specialization. It assumes precisely 16 independent inputs and no extra registers, initialized scratch, or discarded auxiliary outputs.

Internal permutations can be commuted to an endpoint while conjugating/relabeling each gate pair. Acceptance applies only when that resulting pair schedule belongs to the enumerated family. Adding arbitrary physical routing to one of the enumerated schedules can move its absorbed schedule outside the family and is **not excluded** by this census. This is not a general 31-call lower bound, a finite-win construction, or an asymptotic result.

## Logical audit

At each two-register linear gate, either new output depends only on the union of the two preceding dependency sets. This union is an upper bound valid even for singular maps and cancellations. A missing temporal path therefore forces an exactly zero matrix entry for every coefficient assignment. H16 is everywhere nonzero; multiplication on either side by an invertible monomial matrix preserves the existence of zero entries. Thus one missing path is sufficient to reject a schedule.

The prefix/suffix checker correctly evaluates Boolean S × G(a,b) × P: it starts with S × P and adds P[a] ∪ P[b] to every suffix row reaching a or b. Reversing the schedule transposes structural reachability because every two-wire structural gate is symmetric. Full reachability is therefore reversal-invariant.

The unneeded bottleneck/rank-cut stage in CONTRACT.md was not implemented or exercised; no survivor reaches it. Acceptance uses only the complete reachability rejection and makes no finding about that optional stage.

## Independent evidence

- Archive SHA-256: 8d13b99ba2e3d100b0bbe31ba6b7828b3eca1567f705e3255f7c70949e97ac5c.
- ZIP CRC test passed. All 11 archived files exactly match the candidate directory. All 10 content entries in its manifest match their hashes. The inherited context-only README hash also matches; this is an integrity check, not independent verification of historical activity claims.
- C++17 supplied enumerator replay: 1,845,120 configurations, zero forward survivors, zero reverse survivors, zero disagreements; exit 0.
- Supplied Python checker replay: all 1,845,120 configurations rejected; all recorded fields match the original except its expected runtime variation; exit 0. Its full integer ordinary 32-call operator control equals H16, and all 15,376 direct factorization comparisons pass.
- New independent audit checker, audit_traceback.cpp, imports no candidate source. It traces each final output backwards through the temporal graph, using a separately constructed baseline. It exhaustively reproduces zero survivors and the entire histogram. Its controls include identity on all 16 outputs, all 32 single-call deletions rejected, and all 32 restorations accepted.
- The independently emitted canonical missing-path stream has 1,845,120 bytes and SHA-256 **74bf2a26bec02505582bd10c52223b60ad5c80b34d6c6aaadecab387cc3be869**, exactly matching the candidate. It covers 90 distinct canonical absent input-output pairs. The 336 configurations with only one incomplete output still fail reachability.

## Reproduce independent test

Compile audit_traceback.cpp with a C++17 compiler and run the executable with the desired output directory as its sole argument. It writes traceback_results.json and traceback_witnesses.bin. Hash the latter using SHA-256 and compare with the value above. The archived candidate can independently be replayed using its documented commands; this audit used an isolated replay/ copy and did not alter the candidate.

## Timing, visibility, and errors

UTC review start: 2026-10-14T00:17:42Z. UTC substantive audit completion: 2026-10-14T00:19:33Z. Wall interval: 111 seconds, based on the clock tool. Packaging follows this completion time. Model input, output, reasoning, and total token counts are unavailable and remain unknown; tool output token metadata is not model-usage accounting.

No command, compiler, Python assertion, archive-integrity, authorization, or preview-limit error occurred. One initial overly broad directory listing was truncated. Exact warnings: “Warning: truncated output (original token count: 10164)” at the functions wrapper, and “Warning: truncated output (original token count: 13535)” within the exec-command result. This is output truncation, not evidence of a preview-limit rejection. Subsequent bounded reads and all computations completed successfully. The task involved local reads, local artifact creation, and execution only; no external writes.
