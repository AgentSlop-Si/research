# Reproduction and execution boundaries

## Packaging only

From this publication directory, Python 3.8 or newer with only its standard library:

    python verify_package.py

This verifies the exact archive hash, complete inventory/CRCs, source-manifest
bindings, declared administrative omissions and readable exact copies. It does not
run any research program or verify the mathematical theorem anew.

## Optional exact controls

Extract evidence.zip into a new disposable directory, keeping candidate/ and review/
as siblings. The newly authored reviewer controls require only Python 3's standard
library (Python 3.12 was used for the recorded controls). From that extraction root:

    python review/independent_controls.py > review/controls.log
    python review/literal_bank_controls.py > review/literal_controls.log

The second script imports the first script's exact finite-field class; it does not
import or execute any historical research source. The programs write their control
JSON beside themselves, so retain the original ZIP and do not replay into the only
evidence copy. The exact field arithmetic and fixture representations are included
in the source; no external field library, network, private data or secret is needed.

The theorem and operation ledger are proofs and explicitly charged algorithms,
not a claim that the enormous deterministic coefficient search or splitting-field
construction was performed. The finite controls cover the stated fixtures and
negative controls in INDEPENDENT_REVIEW.md; they are not an exhaustive census and
cannot replace its all-field proof. In particular F_(Q^2) holds coefficients, not
necessarily all roots. Source documents are inert provenance and are not executed.
