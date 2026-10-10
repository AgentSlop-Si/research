from pathlib import Path
import shutil,tempfile,subprocess,hashlib,json
base=Path(__file__).parent
with tempfile.TemporaryDirectory(prefix='review_common_poles_') as td:
 p=Path(td)/'review';shutil.copytree(base,p,ignore=shutil.ignore_patterns('__pycache__','SEALED_MANIFEST*','portable_replay.log','PORTABLE_REPLAY.json'))
 r=subprocess.run(['python3','independent_checks.py'],cwd=p,capture_output=True,text=True)
 (base/'portable_replay.log').write_text(r.stdout+r.stderr);assert r.returncode==0
 a=(base/'VERIFIED_RESULTS.json').read_bytes();b=(p/'VERIFIED_RESULTS.json').read_bytes();assert a==b
 out={'status':'PASS','isolated_temporary_directory':True,'command':'python3 independent_checks.py','byte_identical':True,'result_sha256':hashlib.sha256(b).hexdigest(),'source_programs_executed':False,'dependencies':'Python standard library','network_required':False}
 (base/'PORTABLE_REPLAY.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
