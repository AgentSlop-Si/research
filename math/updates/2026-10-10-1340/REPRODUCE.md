# Reproduce the independent controls

Use Python 3. Work in a disposable copy of this packet: the scripts write their own result JSON beside themselves. No original research-source directory belongs on the import path. Each program is independent reviewer-authored code; original uploaded or predecessor executables are neither needed nor included.

From the packet root:

    python controls/schur/fresh_controls.py
    OPENBLAS_NUM_THREADS=1 python controls/all_length/fresh_controls.py
    OPENBLAS_NUM_THREADS=1 python controls/all_length/fresh_outer_controls.py
    OPENBLAS_NUM_THREADS=1 python controls/phase_cone/fresh_controls.py
    python controls/jordan/verify_jets.py
    python controls/jordan_second/second_review_controls.py

Schur and both Jordan controls use the Python standard library. Taylor controls also require NumPy and mpmath; the reviewed environment used NumPy 2.3.5 and mpmath 1.3.0. Phase-cone controls require NumPy and SymPy. Do not install dependencies or run code outside your own trusted verification environment without reviewing them.

## Meaning of the outputs

- Schur: exact finite-field rank/path, tiny support minima, Beneš and finite-field non-converse controls. The general mathematical proof is in the review.
- Taylor: exact geometry, rational rounding schedules and modular ranks, plus floating-point operator falsification and high-precision scalar comparisons. Numerical controls are not certified spectral bounds or an eager-table implementation benchmark.
- Phase cone: exact modular potentials, exhaustive circular-width cases, rational-interval decisions and a complete small rejection certificate; numerical gauge and multimask controls are separately labelled.
- Jordan first review: exact finite-field full/interval jets, reconstructed bins and confluent-Hankel controls.
- Jordan second review: independently recovered recurrence, factor/amplitude reconstruction, full verification, spoof/off-grid negatives and the concrete greedy-segmentation rejection case.

The saved JSON results are included in each matching directory. Floating-point output last digits may depend on the numerical environment; mathematical proof acceptance does not rest on their byte identity. For immutable input identity, compare [SHA256SUMS](SHA256SUMS) before running. Generated outputs may change these checksums, which is why a disposable copy is required.

The inert source ordinary-N benchmark ledger in sources/jordan is not an independent control result and was not rerun. No source-reported end-to-end performance ledger is promoted to independently reproduced evidence here.
