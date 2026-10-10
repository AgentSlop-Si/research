#!/usr/bin/env python3
"""Run only independently authored auditors, never uploaded source programs."""
from pathlib import Path
import json, os, subprocess, sys
BASE=Path(__file__).resolve().parent
TASKS=[
 'audit_provenance.py',
 'phase22_audit/independent_checks.py',
 'bilateral_audit/independent_symbolic_audit.py',
 'bilateral_audit/independent_modular_audit.py',
 'tail_screen_extension/independent_checks.py',
]
results=[]
for rel in TASKS:
 print('Running independent audit:',rel,flush=True)
 p=subprocess.run([sys.executable,str(BASE/rel)],cwd=BASE,text=True,capture_output=True,env={**os.environ,"OPENBLAS_NUM_THREADS":"1"})
 print(p.stdout,end='',flush=True)
 if p.stderr: print(p.stderr,file=sys.stderr,end='',flush=True)
 results.append({'script':rel,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 if p.returncode:
  (BASE/'INDEPENDENT_RERUN.json').write_text(json.dumps({'passed':False,'checks':results},indent=2)+'\n')
  sys.exit(p.returncode)
(BASE/'INDEPENDENT_RERUN.json').write_text(json.dumps({'passed':True,'uploaded_programs_executed':False,'checks':results},indent=2)+'\n')
print('All independent audit programs passed.',flush=True)
