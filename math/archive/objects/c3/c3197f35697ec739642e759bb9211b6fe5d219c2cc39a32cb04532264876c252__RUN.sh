#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1
cd fft_green_phase41_unit_holonomy
python -m unittest -v tests_phase41
python phase41_exact_jacobian.py
python phase41_three_exact.py
python phase41_arbitrary_amplitude.py
python phase41_full_audit.py
cd ..
sha256sum -c SHA256SUMS.txt
python - <<'PY'
import zipfile
p='fft_green_phase41_unit_holonomy/previous_full_phase40_checkpoint.zip'
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
print('Prior Phase 40 archive integrity: OK')
PY
