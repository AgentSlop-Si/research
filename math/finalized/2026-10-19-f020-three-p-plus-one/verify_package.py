#!/usr/bin/env python3
"""Read-only public-tree integrity and administrative projection checks."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((ROOT/name).read_text())
m=read('MANIFEST.json');seal=read('SEAL.json');a=read('FINAL_ACCEPTANCE.json')
assert sha(ROOT/'MANIFEST.json')==seal['manifest_sha256']
expected={r['path'] for r in m['files']}|{'MANIFEST.json','SEAL.json'}
actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
assert actual==expected,{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for row in m['files']:
 p=ROOT/row['path'];assert not p.is_symlink();assert p.stat().st_size==row['bytes'];assert sha(p)==row['sha256'],row['path']
ledger=read('SOURCE_LEDGER.json')['files'];om=read('OMISSIONS.json')
assert len({(r['source_packet'],r['source_path']) for r in ledger})==len(ledger)
assert [r for r in ledger if r['mode']=='omitted']==om['omitted_frozen_entries']
assert om['accepted_final_mathematical_proof_checker_or_data_omitted'] is False
for row in ledger:
 if row['mode']=='omitted':assert row['export_path'] is None;continue
 p=ROOT/row['export_path'];assert sha(p)==row['exported']['sha256'];assert p.stat().st_size==row['exported']['bytes']
 if row['mode']=='exact':assert row['original']==row['exported']
 else:
  assert row['mode']=='admin_path_projection';assert row['projection']['scientific_text_changed'] is False
  assert row['original']!=row['exported'];assert 'original-source/' in p.read_text()
for ns,key in [('candidate','author_manifest'),('review','independent_manifest')]:
 assert sha(ROOT/ns/'MANIFEST.json')==a['originals'][key]['sha256']
 old=read(ns+'/MANIFEST.json')
 for r in old['files']:
  matches=[x for x in ledger if x['source_path']==r['path'] and (x.get('export_path','') or '').startswith(ns+'/')]
  if not matches:matches=[x for x in ledger if x['source_path']==r['path'] and x['mode']=='omitted' and ('successor_review' in x['source_packet'])==(ns=='review')]
  assert len(matches)==1,(ns,r['path']);assert matches[0]['original']=={'bytes':r['bytes'],'sha256':r['sha256']}
v=read('review/VERDICT.json')
assert v['verdict']=='PASS within exact scope'
assert v['candidate_report_sha256']==a['originals']['author_report']['sha256']
assert v['candidate_manifest_sha256']==a['originals']['author_manifest']['sha256']
assert sha(ROOT/'candidate/REPORT.md')==a['exported_author_report']['sha256']
assert sha(ROOT/'review/INDEPENDENT_REVIEW.md')==a['originals']['independent_review']['sha256']
assert sha(ROOT/'review/VERDICT.json')==a['exported_independent_verdict']['sha256']
scope=read('CLAIM_SCOPE.json');assert scope['combined_range']=='0<=b<=3p+1 AND b<p^s';assert scope['accepted_prior_range']=='0<=b<=3p AND b<p^s'
assert scope['new_degree']=='b=3p+1';assert scope['p_3']==v['prime_3'];assert scope['p_ge_5']==v['extra_claims_odd_primes_p_at_least_5']
owners=read('OWNER_DISPOSITIONS.json');assert owners['F020']['priority']==58 and owners['F020']['status']=='TO RESEARCH';assert owners['F023']=='alias of F020, not a new owner'
for p in ROOT.rglob('*'):
 if p.is_file():
  text=p.read_text()
  for token in ['docs.google.com'+'/spreadsheets','/'+'workspace'+'/','/'+'user_notes'+'/','/'+'agent_notes'+'/','dream'+'_notes']:
   assert token not in text,('private marker',str(p.relative_to(ROOT)))
print(json.dumps({'status':'PASS','public_files':len(actual),'source_rows':len(ledger),'explicit_omissions':len(om['omitted_frozen_entries']),'admin_projections':len(om['admin_projections']),'mathematical_replay':False,'external_writes':False}))
