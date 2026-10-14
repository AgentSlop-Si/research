# Signed-bank extension and paid arithmetic audit

14 October 2026. Two independently reviewed results are preserved here, with their candidate work kept separately and labeled as such.

## Accepted N=13 scope

For N=13, q=16, the original legal signed-bank grammar, exactly one independently free effective alpha node in each cross-sign orientation, and arbitrary legal beta:

- 16 <= B(K) <= 24 for every field K of characteristic 53.
- 18 <= B(F53) <= 24.

The degree-six obstruction is a polynomial Bezout identity, valid over every extension; the degree-seven strengthening is a complete 2,756-polynomial base-field splitting census. The upper bound is a literal twenty-four-bank witness, independently checked through 312 inversions and all 169 target entries. No exact optimum, unrestricted-cross-support lower bound, different q/characteristic, extension-degree classification, characteristic-zero lift, novelty or FFT-speed result follows.

Read [the independent acceptance](n13_independent_acceptance/REVIEW.md) and [the candidate derivation](n13_candidate/REPORT.md). Candidate wording is retained as historical status; acceptance is supplied by the separate independent report. Prior N=11 minima and research scores are unchanged.

## Accepted arithmetic scope

The shared-phase diagonal-Toeplitz evaluator is accepted as a constructive upper bound with paid O(B M_K(N)+BN) setup and online cost for supplied legal banks, under the stated polynomial-multiplication model. For a certified sum targeting F, the outer transforms cancel algebraically. This does not prove that B convolution calls are necessary.

The classical odd-N DFT already uses one cyclic convolution plus at most 2N scalar multiplications. The N=11 thirteen-bank construction therefore establishes no asymptotic improvement, measured constant-factor advantage, or arithmetic novelty. Field-extension costs, coefficient generation and finding the decomposition remain separate charges. The independent checker passed 1,181 exact bank cases, including characteristic two, composite length, all signs, zero-diagonal rotations, and the literal N=11 certificate.

Read [the independent arithmetic review](arithmetic_independent_acceptance/REVIEW.md) and [the candidate arithmetic report](arithmetic_candidate/REPORT.md). The independent acceptance covers the evaluator and classical comparison; it does not grant blanket novelty or optimality to every discussion in the candidate report.

## Preservation boundary

This is an additive clean publication projection. ORIGINAL_PACKET_IDENTITIES.json binds four unchanged full original ZIPs. PUBLICATION_PROJECTION.json accounts for every original member, including duplicate cold-replay directories and the nested candidate ZIP retained in those originals. Every included mathematical JSON payload, raw certificate, review result and arithmetic count is byte-identical to its original. The top-level MANIFEST.json binds the actual publication files.

Source packet manifests are named ORIGINAL_MANIFEST.json and intentionally retain original hashes. A few selected source/report copies remove only non-mathematical execution-accounting labels or a local absolute path from a development error log. Each such projection has explicit original and publication hashes. No mathematical formula, numerical JSON, certificate coefficient, timing value in an included record, or original file was changed. The original candidate timing record containing unrelated accounting metadata is bound but omitted. Earlier text-source copies and duplicated cold replay files remain in the unchanged originals.

The N=13 independent checker uses its sibling sources/ numerical files; candidate source is inert provenance. Its numerical replay outputs remain reproducible from the included evidence, while a regenerated SOURCE_BINDINGS.json will reflect the explicitly projected inert source/report bytes and the omitted nested ZIP. Compare numerical outputs, not a projected package's provenance list, with the original replay receipt. The producer generator also expects the historical text inputs identified in n13_candidate/outputs/SOURCE_BINDINGS.json; those are retained in the original candidate archive. The certificate checker and both arithmetic checkers are included. No historical or scientific program was executed as part of this preservation step.

No spreadsheet snapshots, private spreadsheet identifiers, raw write requests, or coordination records are included. The existing research table is unchanged by this package.
