"""Integrity and inert syntax checks only; no scientific imports or executions."""
from pathlib import Path
import ast, hashlib, json, re
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(n):return json.loads((ROOT/n).read_text())
def check_entry(root,e):
 p=root/e.get('path',e.get('file'));b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],str(p)
 if 'git_blob_sha1' in e:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha1'],str(p)
def rows(d):
 if isinstance(d,list):return d
 out=d.get('files',d.get('canonical_files',[]))
 return [{'path':k,**v} for k,v in out.items()] if isinstance(out,dict) else out
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
expected=set(load('PRESERVATION_ALLOWLIST.json')['files']);assert actual==expected,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
assert not any(p.is_symlink() for p in ROOT.rglob('*'))
manifest=load('MANIFEST.json');assert {e['path'] for e in manifest['files']}==actual-{'MANIFEST.json','SEAL.json'}
for e in manifest['files']:check_entry(ROOT,e)
seal=load('SEAL.json');assert seal['status']=='SEALED_LOCAL_PUBLICATION_PACKET' and seal['final_review_gate_passed']
for key,name in [('manifest_sha256','MANIFEST.json'),('allowlist_sha256','PRESERVATION_ALLOWLIST.json'),('final_acceptances_sha256','FINAL_ACCEPTANCES.json')]:assert seal[key]==sha((ROOT/name).read_bytes())
bind={e['path']:e for e in load('COPY_BINDINGS.json')['files']}
for path,e in bind.items():
 b=(ROOT/path).read_bytes();assert len(b)==e['public_bytes'] and sha(b)==e['public_sha256'],path
 assert e['byte_identical']==(e['original_sha256']==e['public_sha256'] and e['original_bytes']==e['public_bytes'])
 assert e['byte_identical'] or e['adaptations'],path
for p in ROOT.rglob('MANIFEST.json'):
 if p==ROOT/'MANIFEST.json' or 'provenance' in p.parts:continue
 for e in rows(json.loads(p.read_text())):check_entry(p.parent,e)
for p in ROOT.rglob('DELIVERABLE_HASHES.json'):
 if 'provenance' not in p.parts:
  for e in rows(json.loads(p.read_text())):check_entry(p.parent,e)
accept=load('FINAL_ACCEPTANCES.json');assert accept['all_six_final_gates_passed'] and len(accept['acceptances'])==6
assert len({g['result'] for g in accept['acceptances']})==6
for g in accept['acceptances']:
 assert g['verdict'].startswith(('ACCEPT','PASS'))
 for key,pathkey in [('original_candidate_manifest_sha256','original_candidate_integrity'),('original_review_integrity_sha256','original_review_integrity'),('public_candidate_report_sha256','public_candidate_report'),('public_review_report_sha256','public_review_report'),('public_verdict_sha256','public_verdict')]:assert sha((ROOT/g[pathkey]).read_bytes())==g[key],(g['result'],key)
 for role in ('candidate','review'):
  path=g['public_'+role+'_report'];assert bind[path]['original_sha256']==g['original_'+role+'_report_sha256']
 assert bind[g['public_verdict']]['original_sha256']==g['original_verdict_sha256']
 # Each frozen original manifest row agrees with the original identity in COPY_BINDINGS.
 for pathkey,route in [('original_candidate_integrity',g['result']+'/candidate'),('original_review_integrity',g['result']+'/review')]:
  for e in rows(load(g[pathkey])):
   path=route+'/'+e.get('path',e.get('file'));assert bind[path]['original_sha256']==e['sha256'],path
checks=load('PACKAGING_CHECKS.json');assert checks['status']=='PASS' and not checks['scientific_reruns'] and not checks['external_writes']
for path in checks['required_byte_identical_payloads']:assert bind[path]['byte_identical'],path
private_tokens=['docs.google.com/spreadsheets','library_file_id','sediment://','/agent_notes/','dream_notes']
# The verifier's pattern literals are not payload findings.
for p in ROOT.rglob('*'):
 if not p.is_file():continue
 try:s=p.read_text()
 except UnicodeDecodeError:continue
 if p.name!='verify_package.py':assert not any(x in s for x in private_tokens),p
 if p.suffix=='.py':ast.parse(s,filename=str(p.relative_to(ROOT)))
print(json.dumps({'status':'PASS','files':len(actual),'accepted_scoped_results':6,'scientific_reruns':False,'external_writes':False,'manifest_sha256':sha((ROOT/'MANIFEST.json').read_bytes())},indent=2))
