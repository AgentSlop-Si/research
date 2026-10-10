# Reproduce the fresh controls

Use Python 3.10 or newer. The bridge and inverse-defect controls use NumPy; the sparse-defect, modal projection and projected-comparator controls use only the standard library. These are dependency descriptions, not installation commands. No submitted source program or original source ZIP is required or executed.

Run from this packet root, keeping the distributed evidence unchanged:

```sh
work=$(mktemp -d)
cp -R programs/. "$work/"
python "$work/bridge/fresh_phase22_verifier.py"
python "$work/stable_inverse/fresh_controls.py"
python "$work/stable_inverse/independent_refinement_controls.py"
python "$work/sparse_defect/independent_controls.py"
python "$work/projected_fourier/independent_controls.py"
python "$work/projected_comparator/fresh_controls.py"
```

Each verifier writes a result JSON beside itself. Compare it with the corresponding directory under certificates. Public source-file and exported-file hashes are distinguished in SOURCE_MANIFEST.json. The bridge and sparse-defect verifiers are portable derivatives: original-archive integrity checks have been removed, selected comparison data have been retained, and the mathematics is unchanged. Their portable outputs were independently rerun and compared to the distributed mathematical results. Other verifier files are byte-identical to the frozen fresh controls.

## Expected controls

- Bridge: eight pinned modular minors at N=9,16,64,256, both orientations; six exact rational-cyclotomic coefficient vectors; all-block ranks; reachable zero-bridge controls; exact sine-rank proofs accompanied by numerical diagnostics. First-minor values are 65/44, 46990/5754, 8970/35649 and 24394/34918. Explicit integer arrays are distributed as data.
- Stable inverse base: 120 constructed unitary/DFT attainments, 120 complementary-rank identities, 72 scalar checks, 102 graph checks, 549 coset-spectrum cases, exact modular parity ranks and explicit s=0 counterexamples.
- Stable inverse refinement: 264 positive-critical-value attainments, 264 complementary-rank identities, 4 zero-critical-value examples, 6 threshold and 18 infimum cases, 164 infeasible-class checks, and 43,400 exact rational envelope comparisons. Floating-point attainment checks supplement the included universal proofs.
- Sparse q-defect: 2,736 direct kernel bins, 61,378 sparse transform bins, all 343 raw F7^3 inputs, seven complete chart comparisons through N=6,561, 420 directly checked chart rows, a dense-forcing boundary case and all seven operation-count rows. The deliberately dense recurrence check can take longer than a fast algorithm call; it is verification work, not part of the complexity claim.
- Phase33 source scope: 56 modular projected cases, 3,076 dense output entries, 12,744 basis-entry comparisons, 12 complete modal matrices, 15 exact rational-cyclotomic complex checks and all logged cost formula rows.
- Projected comparator independent review: 100 basis-parameter cases, 3,012 basis vectors and 213,220 entries per reconstruction; 219 dense vectors; 36,408 exact characteristic-zero coefficient entries; 18 vectors over base fields lacking the full Nth root. It also tests optional C=0 and N=1 extensions separately from the accepted theorem's 1≤C≤t, t≥1 contract.

Exact field/rational assertions and floating-point diagnostics are labeled in the notes and result files. Finite checks corroborate the proofs; they do not establish global program correctness, numerical stability, bit complexity or historical novelty.

The frozen comparator note retains its historical pending-review label. Its subsequently accepted scope is supplied by notes/07_projected_comparator_review.txt and certificates/projected_comparator/REVIEW_RECEIPT.json. Their original receipt filenames identify source bytes; SOURCE_MANIFEST.json maps those bytes to this packet's organized paths.
