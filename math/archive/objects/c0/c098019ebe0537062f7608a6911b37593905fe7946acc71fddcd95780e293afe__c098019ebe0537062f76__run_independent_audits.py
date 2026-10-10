#!/usr/bin/env python3
"""Run only independently authored auditors; never submitted source programs."""
from pathlib import Path
import subprocess,sys

ROOT=Path(__file__).resolve().parent
SCRIPTS=[
    'audit_provenance.py',
    'rank_audit/independent_rank_checks.py',
    'woodbury_audit/independent_checks.py',
    'prior_window_audit/independent_checks.py',
]

if __name__=='__main__':
    for name in SCRIPTS:
        print('Running independent auditor:',name,flush=True)
        subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,check=True)
    print('PASS: every independent auditor completed.',flush=True)
