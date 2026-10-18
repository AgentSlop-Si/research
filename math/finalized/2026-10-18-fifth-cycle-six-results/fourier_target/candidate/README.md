# Unrestricted F8 task packet

Status: target undecided. Read REPORT.md first.

- ORIGINAL_IDEAL.json / ORIGINAL_IDEAL.sing: all original equations, no nonzero gauge assumption.
- RELAXED_QUADRICS.json / RELAXED_IDEAL.sing: necessary inverse system retaining every original zero component.
- build_exact_systems.py: reproducible exact system emission.
- verify_exact.py: independent evaluation, inverse identities, and zero-boundary controls.
- CHECKS.json and VERIFY.log: successful exact encoding checks.
- exact_elimination_attempt.py and associated logs/status: bounded characteristic-zero attempt.
- discover.py, numeric_*.npz, NUMERIC_DISCOVERY.json: numerical discovery only, no nonexistence inference.
- matroid_probe.py / MATROID* files: unused exploratory tangent probe.

Run `python3 build_exact_systems.py` and `python3 verify_exact.py` for standard-library exact checks. No external write or historical package execution is required. Do not interpret numerical residuals or unsuccessful elimination as a certificate.
