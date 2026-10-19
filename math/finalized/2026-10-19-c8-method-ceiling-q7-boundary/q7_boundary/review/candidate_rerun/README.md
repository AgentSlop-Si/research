# Order-35 first-interior proof candidate

Result: no original binary Fourier mask at N=35 and d in {8,9,10,11,12,13}.

- `REPORT.md`: complete symbolic proof and scope.
- `THEOREM.json`: machine-readable claim and review status.
- `verify_q7.py`: standard-library exact corroboration, reproducible with `python verify_q7.py`.
- `RESULTS.json`, `RUN.stdout`, `RUN.stderr`: completed run; stderr is empty.
- `LOCAL_FAMILIES.json`, `PARTITION_CERTIFICATES.json`, `SPLIT_LINE_CERTIFICATES.json`: exact local certificates.
- `ORIGINAL_PHASE_CONTROLS.json`: both complete Grams for original-order positive and negative controls.
- `RECTANGULAR_EXTENSION_OBSTRUCTION.json`: exact no-extension certificate for the retained degree-eleven block.
- `SOURCE_BINDINGS.json`, `sources/`: frozen inputs from the accepted first-interior work.
- `MANIFEST.json`, `SEAL.sha256`: content binding.

This is a finished candidate requiring independent review, not a self-acceptance. It does not classify other order-35 degrees or claim an exhaustive square-mask search. No external writes were performed.
