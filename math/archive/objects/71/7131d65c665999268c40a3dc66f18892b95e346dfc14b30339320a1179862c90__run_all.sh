#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m unittest -q test_phase30 test_phase27 test_phase28 test_phase29
python cyclotomic_rank_certificate.py --output fft_hero1_phase30_cyclic_replay.json
python abelian_rank_certificate.py
python linear_cse_probe.py
python full_cse_probe.py
sha256sum -c SOURCE_MANIFEST.sha256
printf '\nPhase 30 replay finished.\n'
