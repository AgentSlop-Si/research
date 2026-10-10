#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python test_exact.py
python gf2_depth_certificate.py
