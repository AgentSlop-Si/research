#!/usr/bin/env python3
"""Run only the three independently authored auditors, never source programs."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
for relative in ('audit_provenance.py','window_audit/independent_checks.py','phase23_audit/independent_checks.py'):
    script=ROOT/relative
    print('Running independent audit:',relative,flush=True)
    subprocess.run([sys.executable,str(script)],cwd=script.parent,check=True)
print('All independent auditors passed.',flush=True)
