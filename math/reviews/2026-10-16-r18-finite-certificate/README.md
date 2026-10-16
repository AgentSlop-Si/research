# R18 finite certificate: portable independent audit

This package preserves a separately implemented finite exact-arithmetic
cross-check of the R18 four-stage F16 existence certificate. Read AUDIT.md
for hypotheses, findings, evidence level and limits. The evidence is a static
mathematical review plus a fresh computational check, not formal or independent
human verification. No novelty, general-size FFT improvement or new catalogue
closure is asserted.

## Contents

- AUDIT.md: reviewed statement, methodology, limits and original source hashes
- independent_check.py: independently authored checker; no supplied code imports
- independent_result.json: preserved exact rational result from the original audit
- data/root_candidate.json: original finite root witness (JSON data only)
- data/inverse_witness.npy: original numeric dyadic preconditioner
- source_text/PROOF.md and source_text/REPORT.md: unchanged, clean source text
- ENVIRONMENT.json and requirements.txt: tested environment and dependency version
- PROVENANCE.json: original/export SHA-256 bindings and export modifications
- ALLOWLIST.json: complete intended publication file list

The original ZIP, supplied executables, original search results and original
validation suite are excluded. The source proof/report refer to files from
the full original package; those references do not imply inclusion here.
Private conversation links and local workspace paths are excluded.

## Reproduce

The tested environment is Python 3.12.14 with NumPy 2.3.5. Use an existing
compatible environment, or install the single pinned dependency in your own
preferred virtual environment. Run from this directory, without -O or -OO:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 independent_check.py

No network or credentials are used at runtime. The checker uses paths relative
to its own location, verifies SHA-256 hashes of both data inputs before either
is decoded, and loads the numeric array with allow_pickle=False. It refuses
optimized Python modes because assertions are part of the audit checks.

The checker writes independent_result_reproduced.json, leaving the preserved
independent_result.json unchanged. It compares every result field with the
reference except elapsed seconds. The exact rational numerators/denominators,
input hashes, booleans, method and displayed values must all match. Expect
runtime to vary with the machine; the original run including all 256 exact
derivative perturbations took approximately 17 seconds. The reproduced output
is a local run product and is intentionally outside the publication allowlist.

All accepting mathematical comparisons use integers/Fraction. Decimal display
fields are illustrative. The Jacobian truncation error is explicitly bounded;
it is not discarded. The Fourier target is enclosed by exact integer square
root bounds for its known radicals, not evaluated by floating trigonometry.

## Interpretation

The saved dyadic center is not the exact Fourier circuit. The contraction
certificate identifies an algebraic root within radius 2^-100 in a fixed
256-coordinate affine chart. It establishes the full F16 matrix identity at
that root. No runtime for arithmetic in its algebraic coefficient field is
provided. C09 already supplied a different exact F16 seed; R18 does not
contradict R17's frozen-prefix exclusion. Its literal 320 multiplications and
496 additions/subtractions lose to the stated FFT reference count 48 and 64.
The original supplied checks/searches were not rerun by this audit.
