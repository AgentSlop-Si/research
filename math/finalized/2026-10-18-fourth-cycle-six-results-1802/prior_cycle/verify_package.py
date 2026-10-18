#!/usr/bin/env python3
"""Verify publication integrity and syntax only. No scientific imports or execution."""
from pathlib import Path
import ast,hashlib,json
R=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def load(p):return json.loads((R/p).read_text())
def safe(rel):
 p=(R/rel).resolve();assert p.is_relative_to(R) and p.is_file(),rel;return p

def verify_manifest(path):
 p=safe(path);d=json.loads(p.read_text());rows=d.get('files',d.get('canonical_files',d))
 if isinstance(rows,dict):rows=[{'path':k,**(v if isinstance(v,dict) else {'sha256':v})} for k,v in rows.items()]
 for e in rows:
  f=(p.parent/e['path']).resolve();assert f.is_relative_to(R) and f.is_file(),e['path']
  assert sha(f)==e['sha256'],str(f)
  if 'bytes' in e:assert f.stat().st_size==e['bytes'],str(f)
 return len(rows)

actual=sorted(p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file())
assert actual==load('PRESERVATION_ALLOWLIST.json')['files'],'Missing or unexpected file'
assert not any(p.is_symlink() for p in R.rglob('*')),'Symlink forbidden'
count=verify_manifest('MANIFEST.json');seal=load('SEAL.json');status=load('RELEASE_STATUS.json')
assert seal['manifest_sha256']==sha(R/'MANIFEST.json')
assert seal['allowlist_sha256']==sha(R/'PRESERVATION_ALLOWLIST.json')
assert seal['final_review_gate_passed']==status['final_review_gate_passed']
for route in status['included_routes']:
 verify_manifest(route+'/MANIFEST.json')
 s=R/route/'SEAL.json'
 if s.exists():
  d=json.loads(s.read_text());assert d['manifest_sha256']==sha(R/route/'MANIFEST.json'),route
  if 'review_manifest_sha256' in d:assert d['review_manifest_sha256']==sha(R/route/'MANIFEST.json'),route
 s=R/route/'SHA256SUMS'
 if s.exists():
  for line in s.read_text().splitlines():
   want,rel=line.split(None,1);p=(s.parent/rel.lstrip('*')).resolve();assert p.is_relative_to(R) and p.is_file() and sha(p)==want,rel
copied={e['path']:e for e in load('COPY_BINDINGS.json')['files']}
for e in copied.values():
 p=safe(e['path']);assert p.stat().st_size==e['public_bytes'] and sha(p)==e['public_sha256'],e['path']
 if e['byte_identical']:assert e['original_bytes']==e['public_bytes'] and e['original_sha256']==e['public_sha256'],e['path']
 else:assert e['adaptations'],e['path']
for e in load('SOURCE_BINDINGS.json')['bindings']:
 p=safe(e['path']);assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],e['path']
for e in load('SOURCE_NORMALIZATION.json')['sources']:
 p=safe(e['path']);b=p.read_bytes();assert b.endswith(b'\n') and len(b)==e['retained_bytes'] and sha(p)==e['retained_sha256']
 assert blob(b)==e['retained_git_blob'] and blob(b[:-1])==e['upstream_git_blob']
 assert hashlib.sha256(b[:-1]).hexdigest()==e['upstream_sha256'] and len(b)-1==e['upstream_bytes']
for p in R.rglob('*.py'):ast.parse(p.read_text(),filename=p.relative_to(R).as_posix())
for rel in load('PACKAGING_CHECKS.json')['byte_identical_required_payloads']:assert copied[rel]['byte_identical'],rel
for rel,e in copied.items():
 if '/candidate/' in rel and rel.endswith(('.py','.cpp','.h')):assert e['byte_identical'],rel
for p in R.rglob('*'):
 if not p.is_file():continue
 s=p.read_text()
 for token in ('/'+'workspace/','/'+'home/agent/','docs.google.com/'+'spreadsheets','library_'+'file_id','sediment'+':/'+'/','/'+'agent_notes/','dream'+'_notes'):assert token not in s,(p.name,token)
if status['final_review_gate_passed']:
 a=load('FINAL_ACCEPTANCES.json');assert a['all_six_final_gates_passed'] and len(a['acceptances'])==6
 assert status['accepted_results']==seal['accepted_results']==6 and a['mandatory_summary_qualification_satisfied']
 for e in a['acceptances']:
  assert sha(safe(e['public_review_report']))==e['public_review_report_sha256']
  assert sha(safe(e['public_candidate_report']))==e['public_candidate_report_sha256']
  for role in ('candidate','review'):
   for rel,want in e['original_frozen_hashes'][role].items():
    key=e['result']+'/'+role+'/'+rel
    if key in copied:assert copied[key]['original_sha256']==want,key
   name=e['original_'+role+'_integrity_file'];p=safe(e['result']+'/'+role+'/ORIGINAL_'+name)
   assert sha(p)==e['original_'+role+'_integrity_sha256'],e['result']
 wording='canonical-factor sharpness proved here only for sufficiently large H'
 for name in ('README.md','REQUIRED_CLARIFICATIONS.md','correlated_precision/README.md'):assert wording in safe(name).read_text(),name
 assert copied['correlated_precision/candidate/README.md']['byte_identical']
 assert copied['correlated_precision/review/SMALL_WIDTH_SCOPE_COUNTERCONTROL.json']['byte_identical']
print(json.dumps({'status':'PASS','publication_status':status['status'],'final_review_gates':6 if status['final_review_gate_passed'] else 'PENDING','allowlisted_files':len(actual),'manifest_bound_files':count,'scientific_programs_executed':False,'external_writes':False}))
