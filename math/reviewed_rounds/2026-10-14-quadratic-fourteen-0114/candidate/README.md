# Pinned quadratic-field fourteen-bank candidate

Read REPORT.md for the theorem, proof dependency and scope. The exact raw witness is outputs/RAW_WITNESS.json and its readable pair expansion is WITNESS_TABLE.md.

Run `python fresh_gate.py --out replay` to reconstruct all 529 factorizations, derive the witness, and check its full literal arithmetic. Only Python standard-library modules are used. Supplied scientific code is never executed.

A cold run reproduced all ten deterministic output files byte for byte; see REPLAY_VERIFICATION.json. The packet is a candidate awaiting independent review.
