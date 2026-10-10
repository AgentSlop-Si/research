#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m unittest discover -s tests -v
python run_audit.py
python verify_matrix.py
python symbolic_complex_audit.py
