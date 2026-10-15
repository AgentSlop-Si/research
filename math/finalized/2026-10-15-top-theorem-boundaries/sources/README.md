# FFT stable arc-signature research package

Contents:
- `THEOREM.md` — self-contained theorem and proof, precise model, explicit constant and novelty boundary.
- `verify.py` — independent numerical, combinatorial, graph-only and prime-field checks; requires NumPy.
- `results.json` — stored results from one deterministic run.
- `SOURCE_AUDIT.md` — relationship to the newest available research and external literature.

Run `python verify.py` with NumPy installed. Its outputs are deterministic for the saved random seeds. The mathematical theorem is the proof in `THEOREM.md`; numerical verification is supplementary.

**This is not an exact O(N) FFT algorithm, nor a claim of publication priority.**
