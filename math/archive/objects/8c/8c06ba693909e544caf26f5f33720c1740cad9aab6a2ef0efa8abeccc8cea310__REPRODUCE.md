# Portable reproduction

Python 3.9 or later; standard library only. No network dependency.

    python independent_checks.py feedback-review-replay.json
    python -c 'import json; from pathlib import Path; assert json.loads(Path("feedback-review-replay.json").read_text()) == json.loads(Path("INDEPENDENT_RESULTS.json").read_text()); print("EXACT REPLAY PASS")'
    python verify_seal.py

No uploaded or constructor code is imported or executed. The optional first argument is the output path. No absolute workspace path is required.
