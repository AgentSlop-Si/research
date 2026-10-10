# Independent block-jet certificate

Read `INDEPENDENT_AUDIT.md` for the result, exact map, proof, scope, and limitations.

Reproduce from this directory:

```sh
OPENBLAS_NUM_THREADS=1 python3 fresh_block_jet_audit.py
OPENBLAS_NUM_THREADS=1 python3 fresh_boundary_and_cost_controls.py
```

Requirements: Python 3, NumPy, and a C++17 compiler named `g++`. The first command compiles this audit's own `modular_elimination.cpp`. Run commands sequentially because the eliminator uses a common temporary file. Expected final statuses are `ALL_INDEPENDENT_CHECKS_PASSED` and `ALL_BOUNDARY_AND_COST_CONTROLS_PASSED`.

The original supplied programs are never executed or imported. `source_data/` contains unchanged JSON inputs only. The fresh independent checker and its compiled binary are not part of the mathematical candidate or a claimed Fourier implementation. Reproduction may change runtime fields and log contents; mathematical results and canonical matrix digests should agree.

The export contains no executable binary, caches, or temporary matrix. `MANIFEST.sha256` covers every exported file except itself and can be checked with `sha256sum -c MANIFEST.sha256`.
