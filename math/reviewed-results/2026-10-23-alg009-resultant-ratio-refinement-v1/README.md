# ALG-009: nonzero-resultant selector guarantee refinement

Accepted scoped result, 23 October 2026: remove the specialized linear-gcd
condition from the named Phase20 selector, while retaining its nonzero padded
resultant T, supplied prime p > 55, N >= 8, supplied exact-order Nth root,
explicit raw r, nonzero alpha, 1 <= delta < N, exactly one or two relation
defects and at most one grid pole.

At most three nonzero-anchor raw-ratio proposals per retained shift give at
most 45 shifts and 135 proposals. The paid raw-r pre-fallback bound is
500,000 + 804N + 138 field operations, including failed certificates, pole
scans and full output. Original-input x requires separately paid and guarded
Green P/L stages. Eight direct Fourier probes are acquired, not a free transform.

This is a selector-level guarantee refinement. Raw-ratio recovery is inherited
from Phase19, and both N=8 and N=16 strict-selector witnesses already pass that
earlier ratio branch. There is no established net full-hybrid coverage increase,
new ratio method, runtime improvement, FFT speedup, novelty clearance, owner
closure or discovery-count increase. ALG-009 remains TO RESEARCH, priority 42.
T=0, inputs beyond the one-pole budget, the historical implementation/ledger
and the full-hybrid comparison remain outside this result.

## Read the result

- [Proof](PROOF.md), [operation ledger](OPERATION_LEDGER.md) and
  [independent review](INDEPENDENT_REVIEW.md): byte-exact scientific text.
- [Scoped result](SCOPED_RESULT.json): current accepted scope and evidence pins.
- [Complete bounded scientific evidence](evidence.zip): unchanged manifested
  proof/source/control/script/log/review bytes and both original manifests,
  with one explicitly disclosed administrative omission only.
- [Public inventory](CONTENTS.json), [projection disclosure](PUBLIC_PROJECTION.json),
  [source and runtime closure](SOURCE_CLOSURE.json) and [reproduction](REPRODUCE.md).

Run `python verify_package.py` here to verify all files listed in SHA256SUMS,
the complete ZIP and original scientific bindings. SHA256SUMS excludes itself;
it is an integrity reference, not an independent signature. Obtain it from the
verified immutable Git commit. It executes no research. Optional separate
new-control replay instructions are in REPRODUCE.md.

## Historical status and exact public projection

Author phrases such as "candidate", "pending independent review" and "not
published", and recorded no-external-write fields, describe when those immutable
files were written. The later independent review supplies the accepted scope.
They are preserved, not rewritten to suggest a new execution or table update.

This is not an exact copy of the complete private administrative bundle. One
private spreadsheet response is omitted; PUBLIC_PROJECTION.json gives its exact
old hash and size and identifies a public administrative derivative. That
derivative is not substituted into the original manifest chain. All other 36
manifested source entries and both original manifests are unchanged. CONTENTS.json
is the authoritative public archive membership inventory, not a claim that every
entry in the original private manifest is present.

Unmanifested caches, private coordination records and raw private captures are
excluded. Historical Library identifiers inside unchanged source-audit prose
are inert provenance labels, not credentials or required private dependencies.
The entire earlier archive corpus and external paper PDFs are not bundled; the
included source excerpts close the new theorem and control dependencies, not
historical implementation execution or global literature-priority research.
