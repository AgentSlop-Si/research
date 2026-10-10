# Standalone reproducibility audit

## Failure found in v11

A cold invocation of the v11 tests failed before test collection completed:

```text
ModuleNotFoundError: No module named 'unit_step_core'
```

The v11 archive imported the v9 unit-step implementation but did not include that file. The prior archive therefore was not standalone, even though its tests had passed in an environment where the dependency already existed.

## Repair in v12

This package includes:

- `unit_step_core.py` — the v9 unit-step chirp core;
- `v11_fused_reference.py` — the v11 reference implementation;
- `test_v11_repaired.py` — the v11 regression suite importing the included reference;
- `prototype.py`, `test_checkpoint.py` — v12 implementation and tests.

The final ZIP excludes caches and bytecode. Reproduction:

```bash
python -m pip install -r requirements.txt
pytest -q
python prototype.py --output results.json
python benchmark.py
```

The SHA-256 manifest and ZIP CRC test are included in the release process.
