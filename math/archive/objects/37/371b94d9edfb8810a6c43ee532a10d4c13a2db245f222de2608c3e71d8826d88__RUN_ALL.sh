#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python test_gate.py
python test_twisted.py
python verify_certificates.py
