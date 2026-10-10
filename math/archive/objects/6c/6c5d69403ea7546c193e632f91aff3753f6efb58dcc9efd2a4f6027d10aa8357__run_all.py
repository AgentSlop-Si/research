"""Reproduce all new checks in isolated processes using the standard library."""
from pathlib import Path
import os
import subprocess
import sys

root = Path(__file__).resolve().parent
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
scripts = (
    root / 'fft_qweyl_boundary_research' / 'run_audit.py',
    root / 'fft_qweyl_cache_demo' / 'run_audit.py',
    root / 'fft_material_bridge_review' / 'material_checks.py',
)
for script in scripts:
    subprocess.run([sys.executable, str(script)], cwd=script.parent,
                   env=env, check=True)
print('PASS: all three continuation components')
