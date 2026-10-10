#!/usr/bin/env python3
"""Standalone Phase14 + prior-lineage verifier; no outside downloads."""
import subprocess
import sys
from pathlib import Path

root=Path(__file__).resolve().parent
steps=[
    [sys.executable,'-m','unittest','-v','test_phase14','test_stationary','check_v13','test_centered','v11_test_checkpoint'],
    [sys.executable,'finite_field_audit.py'],
    [sys.executable,'precision_probe.py'],
    [sys.executable,'field_gram_audit.py'],
    [sys.executable,'field_stationary_audit.py'],
    [sys.executable,'green_forcing_gate.py'],
    [sys.executable,'leverage_gate.py'],
    [sys.executable,'orbit_collision_gate.py'],
    [sys.executable,'experiment_phase14.py'],
]
for args in steps:
    print('>>>',' '.join(args),flush=True)
    subprocess.run(args,cwd=root,check=True)
print('PHASE14 ALL PASSED: 63 tests, prior and new exact fields, precision probes, Green forcing, leverage, diagnostics',flush=True)
