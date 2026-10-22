# Original signed banks in all admissible characteristics

Accepted scope, 22 October 2026: for odd N, d >= 4, N >= 8d-10 and m=N-d,
over a field with a supplied primitive Nth root and characteristic not dividing N,
the original signed-bank construction uses at most 2m+2 banks over a genuine
splitting field. Choosing d=floor((N+10)/8) inherits the existing 7N/4+O(1)
bound for odd N >= 23. The bounded extension is its validity in every admissible
positive characteristic, including characteristic two; the bank constant is not new.

For q in F_Q, polynomial coefficients can be chosen in F_(Q^2). This does not
mean the roots split there. The true splitting-field degree is at most m! over
the coefficient field and at most 2m! over F_Q. Explicit, potentially enormous
preparation and root recovery are charged in the operation ledger.

For B=2m+2 physical banks, the stated conservative warm cost is 2BN^2
multiplications and 2BN^2-BN-N additions, including all outputs and accumulation.
It is cubic, not an FFT improvement, and uses extension-field arithmetic.

No base-field attainment, optimality, smaller bank constant, polynomial extension
degree, historical novelty, full support classification, new N13 claim, or broader
owner closure follows. The original N13 extension-degree question remains an
inherited completed predecessor, not new work in this publication.

## Read and reproduce

- [Theorem](THEOREM.md) and [operation ledger](OPERATION_LEDGER.md), byte-exact.
- [Independent review](INDEPENDENT_REVIEW.md), byte-exact.
- [Scoped result](SCOPED_RESULT.json), public summary with exact evidence bindings.
- [Complete scientific evidence ZIP](evidence.zip), containing the author/reviewer
  scientific files, all manifest-pinned borrowed mathematical sources, exact new
  controls and logs, source manifests and the public scoped-result summary.
- [Public inventory](CONTENTS.json), [projection disclosure](PUBLIC_PROJECTION.json),
  and [reproduction instructions](REPRODUCE.md).

Run `python verify_package.py` here for packaging-only verification. The huge
deterministic construction is a priced mathematical algorithm, not a reported
executed computation. Small exact controls corroborate, not replace, the proof.

## Borrowed inputs

The characteristic-zero upper bound, whole-left completion and classical
polynomial/Vandermonde methods are inherited. All six source files pinned by the
author and all six pinned by the reviewer are bundled unchanged; duplicate sources
retain their original paths and bytes. SOURCE_PINS.json and SOURCE_FETCHES.json
identify their immutable GitHub origins. Historical source programs are neither
bundled nor needed by the new controls. The later completed N13 classification is
scope provenance, not a premise or fresh computational claim in this theorem.

## Status and provenance

The author files and source manifests are immutable historical bytes. Their phrases
"candidate", "pending independent review", and "not published" describe the time
they were written, not the present scoped mathematical disposition. The later
independent review supplies that disposition; SCOPED_RESULT.json is a reader-facing summary
of its accepted scope and evidence bindings. No-publication/no-table-write wording
in preserved historical author/reviewer text is a point-in-time record, not a
claim that downloading this directory updates a research table.

This is an explicit public projection, not an exact copy of the complete private
administrative bundle. All scientific proof, operation-ledger, source-chart,
certificate, control, log and review bytes are unchanged. Original
manifests are also unchanged, including hashes of the omitted administrative
captures. PUBLIC_PROJECTION.json lists every omission and its public derivative.
The derivatives remove only private locator fields and are not substituted into
the original manifest chain. CONTENTS.json is the authoritative public membership
inventory. No omitted capture is a runtime or mathematical input to these proofs.

Only files named in the source manifests, the source manifests themselves, the
public scoped-result summary and explicitly identified publication metadata are included.
Unmanifested bytecode/cache files, exploratory work and private captures are not
published. No historical research program was imported, run or compiled in
preparing this publication. Packaging verification is not a new proof replay.
