#!/usr/bin/env python3
"""Replay five exact original checkers in disposable copies, leaving evidence intact."""
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CASES=[('candidate','check_uniform.py','UNIFORM_CHECKS.json'),('candidate','check_exact.py','EXACT_CHECKS.json'),('review','check_recurrence.py','RECURRENCE_CHECKS.json'),('review','check_exceptional.py','P3_CHECKS.json'),('review','check_exact_identities.py','EXACT_CHECKS.json')]
def strip_timing(v):
 if isinstance(v,dict):return {k:strip_timing(x) for k,x in v.items() if k!='elapsed_seconds'}
 if isinstance(v,list):return [strip_timing(x) for x in v]
 return v
results=[]
with tempfile.TemporaryDirectory(prefix='f020-successor-replay-') as temp:
 for ns,script,output in CASES:
  work=Path(temp)/ns/script.removesuffix('.py');work.mkdir(parents=True)
  shutil.copyfile(ROOT/ns/script,work/script)
  run=subprocess.run([sys.executable,str(work/script)],text=True,capture_output=True,timeout=300)
  assert run.returncode==0,{'script':script,'stderr':run.stderr,'stdout':run.stdout}
  assert not run.stderr,{'script':script,'stderr':run.stderr}
  expected=json.loads((ROOT/ns/output).read_text());actual=json.loads((work/output).read_text())
  assert strip_timing(actual)==strip_timing(expected),{'script':script,'reason':'Scientific output changed'}
  results.append({'script':ns+'/'+script,'output':ns+'/'+output,'all_scientific_fields_match':True,'excluded_nondeterministic_fields':['elapsed_seconds']})
print(json.dumps({'status':'PASS','checks':results,'historical_dependency_programs_replayed':False,'frozen_evidence_modified':False,'external_writes':False},indent=2))
