# ALG-071 heterogeneous pair matching: bounded recovery packet

The one-epoch homogeneous matching theorem extends to arbitrary endpoint costs and arbitrary bin sets under the exact contract in `MODEL_AND_PROOF.md`.

- Every pair cost must dominate either endpoint's solo cost.
- A pair serves only its declared endpoints; undeclared containment service is excluded.
- Every feasible active set can be pruned to a no-more-expensive matching.
- For a common per-bin charge, edge saving is intersection refresh saving minus paid activation.
- Feasibility and peak memory remain explicit. A binding memory budget gives constrained matching, not automatically ordinary weighted matching.

Fresh exact-integer controls passed 59,808 exhaustive abstract instances, 600 ordinary bin-set instances, 200 weighted-bin instances, 250 additive-budget instances, and 250 shared-atom-budget instances. They checked 1,530,136 edge sets, 2,703,054 individual deletions, and 1,499,593 full pruning sequences. Exact counts and negative controls are in `FRESH_RESULTS.json`.

The test program was newly written for this packet. Run `python fresh_verify.py` to reproduce the mathematical checks. No historical supplied code was executed. Rerunning replaces `FRESH_RESULTS.json` and changes its timing field, so it also invalidates the original byte-level manifest until regenerated.

`SOURCE_BINDINGS.json` binds the accepted prior theorem and primary weighted-matching source. `DISPOSITION.json` preserves the recorded owner boundaries. `MANIFEST.json` binds the public mathematical packet. The separate `private/` directory is local recovery provenance, excluded from this packet's publication manifest.

No external write or source-cell change was made. This is a bounded reduction result, not a new matching algorithm, historical novelty claim, general stateful optimizer, production qualification, or whole-owner closure.
