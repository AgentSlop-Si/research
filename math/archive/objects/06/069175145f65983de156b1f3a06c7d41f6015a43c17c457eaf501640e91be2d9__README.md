# v26 reproduction

Requirements: Python 3.11+; standard library only.

```bash
python run_all.py
```

Individual commands:

```bash
python test_checkpoint.py
python independent_verifier.py
python generate_results.py
```

The package embeds the complete v25 ZIP as `PRIOR_v25_COMPLETE.zip` and checks its SHA-256 and CRC.
