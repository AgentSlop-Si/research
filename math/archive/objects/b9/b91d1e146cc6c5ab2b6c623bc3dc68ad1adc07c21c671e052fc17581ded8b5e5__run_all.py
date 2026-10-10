#!/usr/bin/env python3
"""Strict v11+v12+v13 regression and exact modular checks."""
import subprocess,sys
from pathlib import Path

root=Path(__file__).resolve().parent
steps=[
    [sys.executable,'-m','unittest','-v','check_v13','test_centered','v11_test_checkpoint'],
    [sys.executable,'finite_field_audit.py'],
    [sys.executable,'precision_probe.py'],
    [sys.executable,'experiment_v13.py'],
]
for command in steps:
    print('>>>',' '.join(command),flush=True)
    subprocess.run(command,cwd=root,check=True)
print('v13 ALL PASSED: tests, finite-field entries, twiddle diagnostics, experiment',flush=True)
