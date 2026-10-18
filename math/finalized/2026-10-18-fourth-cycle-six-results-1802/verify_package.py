#!/usr/bin/env python3
"""Publication integrity and syntax only. Never imports or runs scientific code."""
from pathlib import Path
import ast,hashlib,json
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def check(p,w):
 b=p.read_bytes();assert sha(b)==w['sha256'],str(p)
 if 'bytes' in w:assert len(b)==w['bytes'],str(p)
def rows(d):
 a=d.get('files',d.get('canonical_files',d)) if isinstance(d,dict) else d
 return [{'path':k,**(v if isinstance(v,dict) else {'sha256':v})} for k,v in a.items()] if isinstance(a,dict) else a
allow=read(R/'PRESERVATION_ALLOWLIST.json')['files']
actual=sorted(p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file())
assert sorted(allow)==actual and len(allow)==len(set(allow))
assert all(not p.is_symlink() for p in R.rglob('*'))
seal=read(R/'SEAL.json');assert seal['manifest_sha256']==sha((R/'MANIFEST.json').read_bytes());assert seal['allowlist_sha256']==sha((R/'PRESERVATION_ALLOWLIST.json').read_bytes())
m=read(R/'MANIFEST.json');assert sorted(e['path'] for e in m['files'])==sorted(set(allow)-{'MANIFEST.json','SEAL.json'})
for e in m['files']:check(R/e['path'],e)
status=read(R/'RELEASE_STATUS.json');g=read(R/'FINAL_ACCEPTANCES.json')
assert status['status']==seal['status']
if status['final_review_gate_passed']:
 assert g['all_six_final_gates_passed'] and len(g['acceptances'])==6 and status['accepted_results']==6
for e in g['acceptances']:
 check(R/e['public_candidate_report'],{'sha256':e['public_candidate_report_sha256']});check(R/e['public_review_report'],{'sha256':e['public_review_report_sha256']})
 assert e['acceptance_text'] in (R/e['public_review_report']).read_text()
 route=e['result']
 for role in ('candidate','review'):
  p=R/route/role/'MANIFEST.json'
  for v in rows(read(p)):check(p.parent/v['path'],v)
  s=p.parent/'SHA256SUMS'
  if s.exists():
   for line in s.read_text().splitlines():
    want,name=line.split(None,1);check(p.parent/name.lstrip('*'),{'sha256':want})
bindings=read(R/'COPY_BINDINGS.json')['files'];by={e['path']:e for e in bindings}
for e in bindings:
 p=R/e['path'];check(p,{'sha256':e['public_sha256'],'bytes':e['public_bytes']})
 if e['byte_identical']:assert e['public_sha256']==e['original_sha256'] and e['public_bytes']==e['original_bytes']
 else:assert e['adaptations'],e['path']
for e in read(R/'SOURCE_BINDINGS.json')['bindings']:check(R/e['path'],e)
checks=read(R/'PACKAGING_CHECKS.json')
for p in checks['byte_identical_required_payloads']:assert by[p]['byte_identical'],p
for p in checks['python_syntax_files']:ast.parse((R/p).read_text(),filename=p)
assert sum('/parity7_traces/' in p for p in allow)==30
for p in actual:
 s=(R/p).read_text()
 for token in ('/'+'workspace/','/'+'home/agent/','docs.google.com/'+'spreadsheets','library_'+'file_id','sediment'+':/'+'/','/'+'agent_notes/','dream'+'_notes'):
  assert token not in s,(p,token)
for e in g['acceptances']:
 route=e['result']
 for role in ('candidate','review'):
  for name,want in e[role+'_frozen_hashes'].items():
   key=route+'/'+role+'/'+name
   assert key in by and by[key]['original_sha256']==want,(key,'original frozen gate')
assert all(e['byte_identical'] for e in bindings if e['path'].startswith('prior_cycle/'))
assert not status['scientific_reruns_during_packaging'] and not status['external_writes'] and not status['general_fft_speedup_claim']
print(json.dumps({'status':'PASS','files':len(actual),'accepted_results':status['accepted_results'],'scientific_reruns':False,'external_writes':False,'privacy_locator_scan':'PASS'},indent=2))
