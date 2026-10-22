# Reproduction and execution boundaries

## Packaging only

Use Python 3.8 or newer with its standard library, from this publication directory:

    python verify_package.py

This validates SHA-256, the complete ZIP inventory, every CRC, exact original
manifest bindings for included members, declared administrative omissions and
the readable byte-exact proof/review copies and scoped-result summary. It executes no research.

## Optional mathematical replay

Extract evidence.zip into a new disposable directory. Keep candidate/ and review/
as siblings. Preserve the original ZIP as evidence: the replay scripts write
result JSON files in their own directories and can overwrite extracted results.

The recorded research environment used Python 3.12, NumPy 2.3.5 and SymPy 1.14.0.
Only Python's standard library plus NumPy and SymPy are required. Provision those
packages through your normal trusted environment/package workflow. No network,
repository checkout, historical program, external private file or secret is needed.
The chart and both complete recorded certificate files are included.

Author replay, from the disposable candidate/ directory:

    python check_cross_stage.py --all --output CERTIFICATES_PRIMARY.json > PRIMARY.log
    python check_cross_stage.py --all --imag 65281 --output CERTIFICATES_CONJUGATE.json > CONJUGATE.log
    python exact_controls.py > EXACT_CONTROLS.log

The frozen candidate/REPRODUCE.md contains the original author instructions and
deterministic data conventions. Logs include elapsed time and are not byte-stable.

Independent replay, from the disposable extraction root:

    python review/independent_review.py > review/INDEPENDENT.log
    python review/additional_controls.py > review/ADDITIONAL.log
    python review/exact_rational_control.py > review/EXACT_RATIONAL.log

The independent main replay reconstructs all 512 label/embedding instances and
uses the fixed recorded row minors, not replacement selections. Additional controls
import only the newly authored independent_review.py; no producer or historical
program is imported by the independent replay. The exact rational control uses
SymPy's Gaussian-rational domain. All source/model inputs are relative paths inside
the ZIP. Timed logs may differ; compare the certificate hashes, determinant residues,
instance counts, exact controls and the substantive assertions described in REVIEW.md.

Neither packaging nor these replay commands publish files or edit a research table.
Finite controls do not replace the universal symbolic support and adjugate argument.
