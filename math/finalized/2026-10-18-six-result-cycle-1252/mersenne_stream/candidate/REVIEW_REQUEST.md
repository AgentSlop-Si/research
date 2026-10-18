# Independent review request

Please independently check the new candidate at the scope stated in REPORT.md. No external write is authorized.

The central proposed advance is an exact common-denominator rewrite K_i=2^popcount(i) U/u_i, followed by limb-streamed narrow-kernel convolution and two explicitly evaluated output modular divisions. This removes the same-scale product from complete conversion in very-wide supplied parameter families. The full multiplier, matrix transform, correlated point-product and prime-selection gates remain open.

Please prioritize:

1. The common-denominator identity, sign twisting, correlation orientation and unchanged H+g reconstruction guards.
2. Exact construction of u_i and U/u_i without hidden long divisions; all kernel widths and three short-factor passes; the single microinverse and reverse table.
3. Every-prefix inter-slab carry invariant, partial top limbs, no inter-slot carries, and exact q packed-call count/capacity.
4. The exact 5nq local diagonal count, separately charged preparation, bounded multiplication arguments and no hidden W-bit inverse.
5. The complete general cost ledger and simplification to O(nW [n² log(n+1)]^(log₂3−1)) under W≥t.
6. The p/p^d composition and the little-o claim for L=O((log N)^(4/5)), with actual-width group handling and inherited carries distinguished from fresh implementations.
7. The array-model qualification, optional explicit-address supplement and unimplemented elementary dispatcher; avoid interpreting arithmetic bounds as Python timings.
8. The narrow scope of the slab-size optimization statement, and all remaining open parent gates.

Read-only source bindings are in SOURCE_PINS.json. Verify MANIFEST.json and source bindings with `python verify_package.py`. Run the candidate controls only in a review copy if preservation of candidate outputs is required. Please write fresh independent controls rather than relying solely on the author harness.
