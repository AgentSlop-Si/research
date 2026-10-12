# ALG-074 stacked word and copied-center interface: independent HOLD

Date: 2026-10-12 UTC. This review accepts the documented source blocker and diagnostic separation only. It does not accept the actual stacked program, copied-center stream implementation, or whole emitted-witness contract. Whole ALG-074 remains unreviewed at the full-program level; the global contract remains OPEN. No external write or historical program execution was performed.

This review binds the final candidate ZIP, 116,711 bytes, SHA-256 42c87707ecc26a973d6205bc4cc5022195d826853cdbc7fd50df255e20e9295f. The earlier 107,188-byte candidate is superseded.

## Finding first

The currently available source metadata names exact original h=23 and h=25 serialized word hashes, but those original word bytes have not been supplied. The source captures were independently byte-bound. The reviewer checked the fixed listed archive inventory and found none of its four named artifacts. This corroborates only the declared inventory and filename/member-name scope. It does not establish nonexistence, search renamed/base64 contents, or recursively decompress nested archives. Prior denied network routes were neither retried nor bypassed.

The source's scalar replay builds its word from `ops` and `scatter`. Separately, its profile-preparation function inserts two copied-center entries into a transition counter. That function writes a transition histogram/record, not a transformed copy/read/park/erase instruction stream. Therefore scalar replay plus the modified profile ledger does not establish that the same physical program realizes the claimed copied-center transformation. This is a missing binding, not a counterexample to the historical source's conditional proposition.

The seven captures are pinned to CrocSwap/integer-mult-bounds commit 56b66d58297deca1d7dd130247d720e960f77a37. SOURCE_BINDINGS and INDEPENDENT_RESULTS record every SHA-256, byte length, Git blob hash and URL. The fresh reviewer never imports or runs those captures, candidate code, or any historical program.

## Exact original word pins

- h=23 gzip: 4629d45d5074f87706db46be3aa3cd369071cd215bc6560d641115aadcce54a0
- h=23 expanded: bd0cbf73756f2e4f8d3879ec6c7a194990eb9ec40aaf3580bdded6994798d920
- h=25 gzip: 1094276c9ee901e4e5c23062775aad2f50bb5a85a67e64e685d79babcf5b8ecb
- h=25 expanded: 634d3cc0fa8e4f592b1924c141bc953524ea08bf683059e18d8ad0c2f26785ec

These hashes are obligations identifying the absent artifacts; they are not evidence of successful retrieval or replay. A newly generated program would require its own declared identity and scope and could not silently stand in for these historical bytes.

## Independent interface requirements

A valid binding must supply the concrete transformed schedule and show all of the following.

1. Every original read-only center use receives exactly the original transformed value at the same logical output address. Prove this as an operator on all relevant inputs and dirty coordinates, rather than by matching rank or number of reads.
2. The center's cleanup endpoint equals the old cleanup endpoint; every caller-visible dirty role and spectator returns exactly to its required value. A copy destination must have an explicit precondition: arbitrary dirty, or established clean. Fresh clean work-tape copies are permitted, but allocation, copying, retention and erasure must be explained and charged.
3. The full stream record, including address/control/spectator fields required by the compiler interface, has a specified layout and order. An abstract coordinate permutation or payload-only XOR is insufficient to identify this physical operation.
4. Both forward and reverse-complement invocations have complete source/output/temporary maps. Reversing scalar transvections alone does not verify reversed address frames or transformed read timing.
5. The actual event ordering supplies legal frame inclusions, terminal ownership and reclaimed-role lifecycle; every reclaimed role is cleared with paid operations before its next incompatible use.
6. The exact program-derived transitions, copied-center children and their rational profiles are bound to the same schedule. This must include setup, record widths, tapes, routing/head motion, copy/erase costs, parked ancestors and all recursive interfaces for any larger complexity claim.

Equality of all formal basis images proves a complete finite map only when the parsed operations are linear in that declared field, use fixed legal addresses, and expose every relevant coordinate. The F2 payload calculation does not identify rational address projectors or Gaussian payload operations.

## Fresh independent counterexamples and controls

`check_independent.py` is newly authored for this review and interprets only its own explicit lists of elementary XORs.

With coordinates (center x, destination y, temporary z), the naive schedule z ^= x; y ^= z; z ^= x maps (x,y,z) to (x,y+x+z,z). Thus it succeeds when z=0 and restores z even when dirty, yet fails the required shear on the dirty-basis input (0,0,1): the actual output is (0,1,1), not (0,0,1). This control assumes the copy destination itself is arbitrary dirty scratch. It does not refute a construction that explicitly establishes a clean temporary and pays for its lifecycle.

The four-XOR echo y ^= z; z ^= x; y ^= z; z ^= x realizes (x,y+x,z) on every formal coordinate; its reversed transposed word gives the opposite shear. Removing the final erasure changes the scratch row. Reordering the same four instructions to put the two y ^= z operations together and the two z ^= x operations together gives the identity. It has exactly the same instruction count and operand-pair multiset as the valid echo. Counts and unordered event ledgers cannot establish chronological program identity.

A separate explicit 5-row, 7-bit-per-record extension with five untouched spectator coordinates passes all 110 formal coordinates. Omitting one record-bit echo is rejected. This is a finite diagnostic example only; it is not a replacement for the missing h=23/25 stream program or a proof of tape cost, all widths, or recursion.

## Preserved scope

The earlier accepted plain finite words and the complete explicit 47x47 retained family for all 4,073,300 pairs remain accepted at their original scopes. This review neither repeats nor enlarges them. The actual 575-dimensional tensor/controlled-permutation embedding and width-481 child remain open, as do original stacked-word replay, copied-center/endpoint stream binding, complete-record/fixed-tape recursion, setup, storage/routing, precision/recovery and an effective common all-size threshold. No complexity theorem, FFT/exact-complex transfer, novelty, priority or count promotion follows.

Derivative note: private inventory counts and record-status wording are omitted or expressed as scientific review scope. The missing-artifact identities, source distinction, conditional interface requirements, exact synthetic diagnostics and preserved limitations are unchanged. Original report SHA-256: `d73edf82cf754780e215ae5c674c64006db077beb31afe266b7fe05d72058c9e`.
