#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
python -m unittest discover -s tests -v
python exact_audit.py > exact_results.json
python numerical_audit.py > numerical_results.json
python expander_audit.py > expander_results.json
python spectral_certificate.py > spectral_certificates_small.json
python -m compileall -q .
