# Historical wording-only correction: v1 to accepted v2

This is a superseded attribution correction, not a change in the mathematical result. The historical v1 report is retained byte-identically as REPORT_V1_SUPERSEDED.md solely to preserve the revision trail. Its pending status and its unsupported attribution below must not be read as the current conclusion.

## Superseded v1 sentence, rejected by the reviewer

“The source's broader finite-field exact-evaluation contract alone does not provide complex order comparisons for coordinate medians.”

## Accepted v2 replacement

“A broader pure field-operation contract alone does not provide the complex order comparisons required for coordinate medians.”

The old wording incorrectly attributed a broader finite-field contract to the original source. The original DECODER.md states exact arithmetic over complex roots of unity. The accepted concentration theorem likewise uses complex roots and absolute values; its coordinate medians require ordered-real comparisons beyond pure field operations.

A byte comparison at packaging time confirmed that replacing precisely this one sentence transforms the full v1 REPORT bytes into the accepted v2 REPORT bytes. No other report byte changed. The earlier review recorded that only REPORT.md and the two author-manifest files changed across the workdir freezes; that is historical review evidence, not a claim that those full workdir inventories are included here.

The historical HOLD_CHECKPOINT_V1.json is retained verbatim, but its HOLD status was resolved by the accepted v2 review. The current acceptance is review/ACCEPTANCE.json, with only its candidate-root locator projected for public packaging. The current independent derivation preserves the correction discussion and accepted scope, with only the documented administrative locator substitutions.

Original and public hash bindings are in lineage/. No supplied research program or omitted control was executed during packaging. No fresh mathematical verification or performance claim is inferred from packaging checks.
