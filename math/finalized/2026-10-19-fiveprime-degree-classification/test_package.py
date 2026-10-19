"""Read-only source plus isolated mutation controls for the package verifier."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import tempfile,shutil,json,hashlib
from verify_package import verify
ROOT=Path(__file__).resolve().parent

def rehash(r):
 m=json.loads((r/'MANIFEST.json').read_text())
 for e in m['files']:
  p=r/e['path'];e['bytes']=p.stat().st_size;e['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
 (r/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
 s=json.loads((r/'SEAL.json').read_text());s['manifest_sha256']=hashlib.sha256((r/'MANIFEST.json').read_bytes()).hexdigest()
 (r/'SEAL.json').write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
def change_json(r,name,change):
 p=r/name;x=json.loads(p.read_text());change(x);p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');rehash(r)
def main():
 before=verify(ROOT);results=[]
 def run(name,mutation):
  with tempfile.TemporaryDirectory(prefix='fiveq_package_negative_') as t:
   r=Path(t)/'copy';shutil.copytree(ROOT,r,ignore=shutil.ignore_patterns('__pycache__'))
   mutation(r)
   try:verify(r)
   except (AssertionError,FileNotFoundError,KeyError,ValueError):results.append({'control':name,'result':'REJECTED'})
   else:raise AssertionError('Accepted malformed package: '+name)
 run('changed_exact_scientific_report',lambda r:(r/'candidate/REPORT.md').write_text((r/'candidate/REPORT.md').read_text()+'\nchanged'))
 run('missing_logical_dependency',lambda r:(r/'candidate/sources/P_candidate_REPORT.md').unlink())
 run('unlisted_file',lambda r:(r/'unlisted.txt').write_text('unlisted'))
 run('unlisted_symlink',lambda r:(r/'unlisted_link').symlink_to('candidate/REPORT.md'))
 run('broadened_arbitrary_semiprime_scope_despite_reseal',lambda r:change_json(r,'CLAIM_SCOPE.json',lambda x:x.update(arbitrary_semiprime_classification=True)))
 run('full_owner_closure_despite_reseal',lambda r:change_json(r,'OWNER_DISPOSITIONS.json',lambda x:x.update(status='CLOSED',full_owner_closure=True)))
 run('broken_acceptance_despite_reseal',lambda r:change_json(r,'FINAL_ACCEPTANCE.json',lambda x:x.update(verdict='PENDING')))
 run('changed_projection_mode_despite_reseal',lambda r:change_json(r,'SOURCE_LEDGER.json',lambda x:next(e for e in x['entries'] if e['mode']=='administrative_projection').update(mode='exact')))
 assert verify(ROOT)==before
 print(json.dumps({'verdict':'PASS','negative_controls':results,'frozen_public_evidence_unchanged':True,'external_writes':False},indent=2,sort_keys=True))
if __name__=='__main__':main()
