# Independent review: HERO1 bounded counted RAM qualification

Date: 2026-10-12 UTC. Subject: HERO1 bounded cold-dispatch qualification.

## Decision

**ACCEPT BOUNDED NEGATIVE PROGRAM QUALIFICATION. KEEP THE GENERAL GATE OPEN.**

This review accepts the stated complete instruction/read/write counts of three newly authored, preinstalled finite RAM programs over N=32/F97. It does not certify complete historical-Python costs, an optimal RAM dispatcher, production performance, a multi-block implementation, a budgeted fallback, or a generic speedup.

Candidate archive: `HERO1_Bounded_Counted_RAM_CANDIDATE_2026-10-12.zip`.
SHA256: `27118a8b130e129a9e515426c896fd6a8c9830f908949aad59bf05e757763b61`.
The sealed archive contains 22 manifest-covered files; all hashes and its outer/inner seal bindings were independently checked.

## Findings

The retained witness independently gives:

| Program | Instructions/fetches | Data reads | Data writes | Initialized cells | Field work including validation |
|---|---:|---:|---:|---:|---:|
| Phase36-style | 1,552 | 1,882 | 1,320 | 847 | 113 |
| Phase37-style | 2,176 | 2,701 | 1,834 | 1,129 | 120 |
| Scalar-cold selector | 1,884 | 2,365 | 1,604 | 989 | 113 |

The corresponding field execution totals before validation remain 108, 115, and 108. The scalar-cold repair costs 332 additional unit instructions, 483 additional reads, and 284 additional writes relative to this exact Phase36-style program. These are distinct accounting coordinates; field instructions are already part of the instruction totals and must not be added again.

All 510 nonempty-support/principal-activity control classes cost 244–838 more instructions in each three-candidate program than in the two-candidate baseline. The two empty-support classes match across all programs, at 533 and 560 instructions. This is a finite statement about these programs and this unit-instruction objective, not an implementation-independent lower bound or a claim about all possible weights.

## Independent method and checks

`review_ram.py` does not import the author module, original source, or a previous checker. It parses the serialized instruction images and implements a separate interpreter using a fixed-size array, independent operand-read/write accounting, uninitialized-read checks, signed-word checks, and a forward-control-flow termination bound.

The independent fixture constructor first builds the complete 32-by-32 signed Haar matrix from coset formulas, then obtains its inverse using generic finite-field Gauss–Jordan elimination. The output oracle evaluates the full DFT by iterative powers. Neither reuses the author's inverse-Haar routine or DFT helper.

The independent suite passes:

- 3,072 complete-output and exact control-cost checks: all 256 supports, both principal states, all three programs, and two amplitude/root assignments per control class
- Exact equality of all three witness instruction traces, every section ledger, and all reported witness counters
- 768 basis/cancellation/dense-value checks covering all 16 primitive roots and all 14 allowed coordinates
- 291 checks of every canonical root candidate, including the zero-input guard
- 396 noncanonical input/root checks, at every one of 33 cells and values -2^31, -1, 97, and 2^31-1
- 5,184 paid refusal checks covering every nonzero F97 value in every one of the 18 forbidden detail coordinates, in all three programs

Each forbidden-detail check refuses after 317 instructions and returns no output. The admission guards have explicit paid paths; an invalid root may refuse after four or five squarings, while every accepted root pays five. No budget parameter or budget-exhaustion branch exists, and none is accepted as a delivered feature.

Four negative controls are detected: a kernel multiplication replaced by addition; root-refusal HALTs bypassed; one omitted write in the claimed ledger; and an altered serialized program fingerprint. These test arithmetic correctness, guard coverage, independent accounting, and byte integrity, respectively.

All 12 historical source bindings were checked against their actual files. Every available inert snapshot is byte-identical to its pinned source. Historical Python files were read as text only. The separately identified author-reproduction run executes only the fully inspected new `counted_ram.py`, in a fresh directory; it is corroboration rather than the independent oracle.

## Instruction, memory, and context audit

The complete charged execution begins with 32 canonical input words and one candidate root already placed in memory, and the fixed program already installed. All target operations are emitted instructions. Compilation, host parsing, input installation, operating-system allocation, simulator bookkeeping, and external delivery of outputs are outside this declared per-call boundary. The report discloses this limitation rather than calling it a production total.

- The fixed field F97 and primitive modular field operations are part of the chosen machine. No primality certification or root search is silently advertised.
- PC increments, instruction decoding, direct addressing, and specified arithmetic are included in a unit instruction. An indirect root request executes its address addition and a LOAD whose two data reads are separately counted.
- Every target data read and write is recounted from opcode semantics, including repeated reads of one address. SET has one write; binary operations have two reads and one write; conditions read one cell; LOAD reads an address cell and its target.
- Static scratch reservation is disclosed, not presented as dynamic allocation. Unwritten scratch has no usable initial value. Every actual initialization, copy, mask write, root store, and output store is explicit.
- All branch targets are forward and in range. Thus no hidden loop or recursion remains at runtime, and execution cannot exceed the serialized program length.
- The full principal scan is six NE tests and an OR reduction; all detail positions are scanned. There is no uncharged `any(A)` or support-list construction in the target.
- Both baseline candidate records and all three global-selector records are built explicitly. Candidate masks, cost recurrences, five-bit population counts, comparisons, tie selection, copies, and discarded candidate attempts are paid.
- Both root preparation paths are emitted. Their table initializations, binary powers, selected-bit scans, conditional multiplications, lookups, and every destination write appear in the trace.
- Every output cell is initialized and receives its final value. The index-zero final assignment is in `synthesis`; the remaining 31 final assignments are in `output_write`. There are 64 output-cell writes in all accepted runs.

Static program sizes are 4,572/5,669/5,669 instructions, reserving 1,852/2,344/2,344 data cells. Admitted test executions use at most 1,051/1,364/1,364 initialized cells and 1,861/2,699/2,699 instructions. The largest raw field intermediate observed is 9,216. Static addresses and control targets fit easily within the declared signed 32-bit convention; field operands stay within 0–96 and planner quantities are bounded by the fixed masks and dimensions.

## Coverage beyond tested amplitudes

All accepted roots follow the same successful guard path. After admission, branching depends only on eight support bits, the principal-active bit, or integer values derived from them. Kernel arithmetic cancellations do not drive branches. Therefore the 512 support/activity classes exhaust accepted instruction-count paths; varying amplitudes and roots changes field values but not costs within a class.

Functional correctness also follows structurally. The full Haar analysis is an invertible linear transform. The sparse kernel generates the exact twisted columns by geometric progression. The full/pruned radix-2 kernel implements the same twisted matrix, including paid odd-only negation and zero-child copying. Root construction gives the requested powers exactly. The emitted Haar synthesis reconstructs all 32 positive-root DFT outputs. These identities apply to arbitrary allowed values; finite tests corroborate the lowering rather than exhaust F97^14 values.

## Essential translation boundary and remaining work

The eager construction of two full root-cost records in the Phase36-style baseline is a new, disclosed implementation choice. Historical Phase36 did not necessarily perform that work. Both comparisons are therefore restricted to the actual serialized programs, even where their scalar selection semantics agree with the source. Removing unnecessary baseline planning could strengthen this particular negative comparison, but no optimized-baseline result is claimed here.

The word “cold” means kernel-plus-root-preparation field minimization. It does not mean total RAM instruction minimization. The permitted family has only one potential active detail block, so the program does not establish multi-block shared-root planning. There is no free enumeration hidden in these finite programs, and no general efficient enumeration result follows from them.

The broader question remains open. Preserve the original online theorem, accepted 115-versus-108 counterexample, scalar global objective, supplied-root boundary, and existing I-dependent hybrid formulas. The next meaningful task is a genuinely economical source-pinned planner or an explicitly larger bounded contract with the same complete cost boundary and matched-program comparison.

No repository, table, service, or historical file was changed by this independent review.

## Reproduction

Run `python3 review_ram.py sealed_candidate final_cold_replay` from this review directory to interpret and validate only the serialized sealed programs. The independent run creates `INDEPENDENT_RESULTS.json` at the requested output directory. `SEALED_ARCHIVE_CHECK.json`, `SOURCE_BINDING_CHECK.json`, and `FINAL_COLD_REPLAY_RECEIPT.json` bind the archive, sources, final independent run, and byte-for-byte regeneration result.

Public derivative note: private tracking locations and administrative instructions are omitted; all counted-program boundaries and remaining limits are retained. Original report SHA-256: `7bde285d390420d00b0e70fe448e5574c633ff93dd1c386f4193b013e6348af4`.
