#!/usr/bin/env python3
from pathlib import Path
import tempfile,shutil,subprocess,hashlib,json,sys
base=Path(__file__).parent
with tempfile.TemporaryDirectory(prefix='one_inner_sector_review_') as td:
 p=Path(td)/'package';shutil.copytree(base,p,ignore=shutil.ignore_patterns('__pycache__'))
 outputs=['seed_audit/INDEPENDENT_CERTIFICATE.json','FIXED_GUARD_RESULTS.json','SECTOR_RESULTS.json','MEMBERSHIP_RESULTS.json']
 old={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in outputs}
 for cmd in ['seed_audit/independent_verifier.py','check_fixed_guards.py','check_sectors.py','check_membership.py']:
  subprocess.run([sys.executable,cmd],cwd=p,check=True)
 new={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in outputs};assert old==new
 print(json.dumps({'status':'PASS','byte_identical_outputs':old,'isolated_temporary_directory':True,'network_required':False,'dependencies':'Python standard library','constructor_programs_executed':False},indent=2,sort_keys=True))
