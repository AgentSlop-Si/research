#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, pathlib

ROOT=pathlib.Path(__file__).resolve().parent
commands=[
    [sys.executable,'-m','unittest','-v','test_checkpoint'],
]
log=[]
for cmd in commands:
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    log.append({'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:
        (ROOT/'run_all.log').write_text(json.dumps(log,indent=2))
        raise SystemExit(p.returncode)
for script,out in [
    ('permutation_displacement.py','permutation_results.json'),
    ('measurement_transcript_gate.py','transcript_results.json'),
    ('moment_state_gate.py','moment_results.json'),
    ('reversal_split.py','reversal_results.json'),
]:
    p=subprocess.run([sys.executable,script],cwd=ROOT,text=True,capture_output=True)
    log.append({'command':[sys.executable,script],'returncode':p.returncode,'stderr':p.stderr})
    if p.returncode: raise SystemExit(p.returncode)
    (ROOT/out).write_text(p.stdout)
(ROOT/'run_all.log').write_text(json.dumps(log,indent=2))
print('v16 cold run passed')
