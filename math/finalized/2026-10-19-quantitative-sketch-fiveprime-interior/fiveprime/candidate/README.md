# Order-5q first-interior proof candidate

Result: no original binary Fourier equality mask at N=5q, q prime >=11, q<d<2q. This is not a complete 5q classification. Read REPORT.md for the symbolic proof and exact q=7 obstruction to the naive split-group extension.

Reproduce the completed exact controls with Python 3 and SymPy:

    python verify_fiveq.py > RUN.stdout 2> RUN.stderr

The verifier imports no historical research code. All Gram and inverse-model checks use exact integer/rational cyclotomic arithmetic. RESULTS.json records the completed successful run. POSITIVE_CONTROLS.json and NEGATIVE_CONTROLS.json retain complete original masks and every failed Gram residue. ORIGINAL_MODEL_CONTROL.json contains the complete proper N=55,d=11 inverse witness, in original index order. Q7_ROW_GROUP_COUNTERCONTROL.json is rectangular, not an equality-mask construction.

The optional exploratory development script requires SciPy and is not part of the verifier or proof. Source bytes, bibliography, manifest, and seal are retained. Independent review is required before acceptance. No external state was changed.
