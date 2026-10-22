# C13: prescribed one-sided zero-mask forward constructor

22 October 2026 UTC. **Accepted for the exact fixed-skeleton prescribed one-sided zero-mask forward-construction child gate.** C13-FIXED-DIRECTIONS remains **TO RESEARCH, priority 34**.

For every admitted `N>=2`, supplied legal invertible direction skeletons `U,V`, and prescribed zero/nonzero masks, the construction decides and constructs exactly the grammar

    B = U^(-1) D_x + D_y V^(-1),
    equivalently U B V = U D_y + D_x V.

Only the skeletons are inverted, never a singular endpoint mask. The solver returns actual-field scales and executable forward plans, or a checkable failure certificate for this skeleton and these masks. Applying the plans costs O(N) field/index operations per vector; full target validation and dense reconstruction costs are separately charged. The theorem treats effective fields with explicit representation/generation assumptions; the reference Python program implements Q and prime fields only.

Read the unchanged [result and proof](candidate/RESULT.md), [reference constructor](candidate/constructor.py), [author checker](candidate/check.py), [recorded author results](candidate/CHECK_RESULTS.json), [independent review](review/REVIEW.md), and [scoped verdict](review/VERDICT.json). Field, target-oracle, exact-scalar, cycle, denominator, support and untampered-preparation guards are part of the contract.

This is not unrestricted singular completion. The first branch allows a singular right endpoint and the second a singular left endpoint. Arbitrary two-sided singular endpoints, general direction discovery, other original-endpoint restrictions, target invertibility, application-specific Fourier integration, and attribution remain open. A concrete two-sided counterexample in the proof demonstrates the strict boundary. No historical novelty or whole-owner closure is asserted.

## Reproduction and evidence

From `candidate/`, run `python3 -B check.py` to reproduce the fresh author's bounded controls. From `review/`, run `python3 -B independent_check.py` to reproduce the independently authored controls. Both use only the Python standard library and write their result JSON beside the script. The independent reviewer did not execute or import the candidate or historical programs: candidate CHECK_RESULTS.json is author-reported, whereas review/INDEPENDENT_RESULTS.json records independently implemented controls. Neither finite experiment substitutes for the all-size proof. A separate [publication validation](PUBLICATION_VALIDATION.json) subsequently replayed both fresh programs from isolated copies and matched their recorded output bytes; that does not change what the original independent reviewer executed.

Scientific source copies are unchanged under candidate/sources/, with immutable GitHub URLs and source hashes in candidate/SOURCE_BINDINGS.json. The copies named sources/prior_RESULT.md and sources/prior_review.md by the historical review manifest correspond byte-for-byte to candidate/sources/inherited_entry_oracle_result.md and candidate/sources/c13_review.md; those duplicate source bodies are intentionally not copied a second time. Relative locators inside historical source copies retain their original repository-relative meaning; use their immutable original URLs for any dependencies not republished here.

## Publication identities and status

The mathematical result, code, recorded controls, original candidate manifest and independent review artifacts are byte-preserved. The sole metadata projection removes the private worksheet-reference object from candidate/SOURCE_BINDINGS.json. [PROJECTION.json](PROJECTION.json) documents the exact transformation and original/published hashes. Original candidate and review manifests still identify reviewed original bytes; their SOURCE_BINDINGS hash is intentionally not the projected hash. Root [SHA256SUMS](SHA256SUMS) binds all actual files in this bundle except itself.

Candidate-at-creation labels and no-external-write statements remain historical. The independent accepted verdict supersedes only the matching candidate's pending-review status at the stated scope. This package records accepted mathematics, not a native table edit, overall owner completion, or execution of any historical program.
