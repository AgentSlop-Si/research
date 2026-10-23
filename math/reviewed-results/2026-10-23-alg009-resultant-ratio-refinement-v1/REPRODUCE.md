# Reproduction and execution boundaries

## Packaging only

From this publication directory, using Python 3.8+ and only its standard library:

    python verify_package.py

This checks all files listed in SHA256SUMS, complete ZIP inventory/CRCs, exact original
manifest bindings for included files, the declared administrative omission,
readable copies and all declared source/runtime/data dependencies. It does not
import or execute a scientific program, rerun a proof, or publish anything.
SHA256SUMS lists every other top-level public file and excludes itself. It is
an integrity reference, not an independent signature; obtain it from the verified
immutable Git commit. Compare the archive hash against that commit and the
externally reviewed publication manifest when available.

## Optional new-control replay, separate from packaging

Extract evidence.zip into a fresh disposable directory with candidate/ and
review/ as siblings. Preserve the original ZIP and original extracted evidence:
these programs overwrite result files beside themselves. No private data,
network access, historical archive lookup or nonstandard Python package is
required. Python 3.12 is the closest recorded runtime. Python 3.8+ provides the
modular-inverse language feature used here.

From the disposable extraction root, author replay:

    python candidate/run_executor_controls.py > candidate/CONTROLS.log

This executes only candidate/paid_executor.py, candidate/exact_controls.py and
the newly authored runner. It writes EXECUTOR_RESULTS.json, CONTROL_SUMMARY.json
and STRICT_EXTENSION_WITNESS_N16.json. Compare 88 controls, 1,632 complete output
coordinates, 48 fast acceptances, 40 exact fallbacks, three invalid-root
rejections, both Green lifts and the exact field outputs with preserved evidence.
The initial control-input preparation failure and its correction remain recorded
in candidate/CONTROL_RUN_HISTORY.json; they are not silently discarded.

Independent replay, from that same disposable extraction root:

    python review/independent_controls.py candidate > review/CONTROLS.log

The explicit candidate argument is required for this layout: the script's
historical default sibling name differs. This script reads only the two witness
JSON files, uses independently authored algebra and does not import candidate
or historical programs. It writes review/INDEPENDENT_CONTROLS.json. Compare
29,344 anchor triples, 2,360 qualifying descriptions, 664 noncoprime descriptions,
296 sparse-padded-zero checks, 92 resultant evaluations and both exact witnesses.

Do not execute anything under sources/. Historical .py and *_static.txt files
are inert provenance. The new core's optional direct fallback is O(N^2); the
historical Green wrapper, full hybrid, extra-root FFT fallback and their literal
meters have not been executed or certified by this publication. Original-x
Green lifts are exact dense control computations, not charged wrapper executions.
The finite controls supplement the universal proof; they do not extend its field,
length, pole or nonzero-resultant hypotheses.
