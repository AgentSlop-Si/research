# FFT joint-block & second-order gate — October 10, 2026

This is a research checkpoint continuing the original four-stage 256-point affine FFT scan candidate. Its central **proved** result is that the leading 28×28 matrix entries have no universal polynomial identity in the separated-generator four-stage family. A separate second-order theorem explains why pointwise Jacobian rank defects do not immediately yield global algebraic incompatibilities.

**Run:** `OPENBLAS_NUM_THREADS=1 python verify_joint_gate.py` (NumPy, Python 3, and g++).

`PROOF_CERTIFICATE.md` separates proofs from observations. `witness28.json` supplies the exact selected Jacobian columns; `GENERATOR_POINT_*.json` saves the full integer parameter witnesses, so the code does not rely on reproducing a pseudorandom number generator. `AFFINE_LAYOUT.json` is copied from the preceding checkpoint; `prior_checkpoint_full.zip` preserves all earlier research.

No `O(N)` FFT, new asymptotic upper bound, or general FFT lower bound is claimed.
