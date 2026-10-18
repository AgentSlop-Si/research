# Centered bounded-variation originals

This packet extends the constant-only centered-source construction to recognized bounded-variation Gaussian-dyadic originals, with arbitrary constant-block endpoints and values. It retains the same centering, normalization, beta=1/4 approximation premise and accepted outer target. The explicit variation-to-energy factor C controls a supplied list of 2C*2^ceil(m/4)+1 approximate coefficients. All q-block formula costs, full dense recognition and source replay remain charged.

- PROOF.md: theorem, original grammar, tail and precision proofs, outer composition, full costs and limits.
- bounded_variation.py: new provider and semantic source replay.
- integrated_bv.py: source-bound accepted outer execution.
- run_example.py: genuine nonconstant 512-entry dense original, two full source passes, complete outer execution, independent exact direct-sum checks of all 512 outputs and all 2,048 centered coefficients.
- fresh_checks.py: 11 rejection controls, additional nonconstant/complex recognition and seven independently checked complex coefficients.
- SOURCE_BINDINGS.json: byte-identical accepted arithmetic/outer dependencies and independent oracle source.

The completed main run produced 49 sparse records, evaluated all 21,609 retained outer coefficients and wrote all 512 outputs. Exact direct-sum checks certify error at most 5.30% of the actual original L2 norm for this fixture. RESULTS.json, TARGET_CHECKS.json, PROVIDER_CHECKS.json and REPORT.md retain the final evidence; independent review remains pending.

Reproduce in a copy of this directory to preserve sealed bytes:

    python run_example.py
    python fresh_checks.py
    python check_plans.py
    python verify_packet.py --fresh

The existing completed result can be checked with python verify_packet.py. Standard-library Python 3.10 or later is sufficient. Independent oracles, export and packaging have separate harness costs; they are not included in production receipts.

This is a broader structured-family result and an execution witness. It is not arbitrary-original recovery, all-length executable coverage, a practical-fast-transform claim, or closure of ALG-034. No external write occurs in these programs.
