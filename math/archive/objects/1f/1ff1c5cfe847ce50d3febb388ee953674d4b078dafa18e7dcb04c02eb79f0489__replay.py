#!/usr/bin/env python3
from pathlib import Path
import tempfile,shutil,subprocess,hashlib,json,sys
base=Path(__file__).parent
with tempfile.TemporaryDirectory(prefix='review_n64_outer_') as t:
 p=Path(t)/'package';shutil.copytree(base,p,ignore=shutil.ignore_patterns('__pycache__'))
 outputs=['seed_audit/INDEPENDENT_CERTIFICATE.json','VERIFIED_RESULTS.json']
 before={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in outputs}
 commands=[['seed_audit/independent_verifier.py'],['independent_checks.py']]
 for cmd in commands:subprocess.run([sys.executable,*cmd],cwd=p,check=True)
 after={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in outputs}
 assert before==after
 print(json.dumps({'status':'PASS','isolated_directory':True,'byte_identical_outputs':after,'network_required':False,'dependencies':'Python standard library','constructor_programs_executed':False},indent=2,sort_keys=True))
