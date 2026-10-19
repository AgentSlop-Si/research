"""Verify the public projection without executing mathematical or historical code."""
from pathlib import Path
from hashlib import sha256
import json,sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent

def h(b):return sha256(b).hexdigest()
def read(rel):return json.loads((root/rel).read_text())
manifest=read('MANIFEST.json');seal=read('SEAL.json')
assert h((root/'MANIFEST.json').read_bytes())==seal['manifest_sha256'],'manifest seal'
paths=set()
for e in manifest['files']:
 f=root/e['path'];b=f.read_bytes();assert len(b)==e['bytes'] and h(b)==e['sha256'],e['path'];paths.add(e['path'])
actual={str(f.relative_to(root)) for f in root.rglob('*') if f.is_file()}
assert actual==paths|{'MANIFEST.json','SEAL.json'},'unlisted/missing public file'
ledger=read('SOURCE_LEDGER.json')['entries'];omitted=read('OMISSIONS.json')['omitted_frozen_entries'];covered=set()
for e in ledger:
 b=(root/e['public_path']).read_bytes();assert len(b)==e['public_bytes'] and h(b)==e['public_sha256'],e['public_path']
 if e['disposition']=='BYTE_IDENTICAL':assert e['source_bytes']==len(b) and e['source_sha256']==h(b)
 else:assert e['transformation'] and e['source_sha256']!=e['public_sha256']
 category=e['public_path'].split('/',1)[0];covered.add((category,e['source_path']))
for cat in ['candidate','review']:
 old=read(cat+'/MANIFEST.json')
 for e in old['files']:
  hits=[v for v in ledger if v['public_path']==cat+'/'+e['path']]
  if hits:
   assert len(hits)==1 and hits[0]['source_sha256']==e['sha256'] and hits[0]['source_bytes']==e['bytes']
  else:
   hits=[v for v in omitted if cat=='candidate' and v['path']==e['path']]
   assert len(hits)==1 and hits[0]['sha256']==e['sha256'] and hits[0]['bytes']==e['bytes']
assert {x['path'] for x in omitted}=={'SOURCE_INDEX.json','SOURCE_INDEX_RECORD.json'}
assert read('OMISSIONS.json')['proof_code_data_omissions'] is False
critical=['candidate/REPORT.md','candidate/check_boundary.py','candidate/check_p3_certificate.py','candidate/BOUNDARY_CHECKS.json','candidate/P3_CERTIFICATE.json','review/INDEPENDENT_REVIEW.md','review/VERDICT.json','review/check_uniform.py','review/check_exact_identities.py','review/check_p3.py','review/UNIFORM_CHECKS.json','review/EXACT_IDENTITY_CHECKS.json','review/P3_CHECKS.json']
for name in critical:
 entries=[e for e in ledger if e['public_path']==name];assert len(entries)==1 and entries[0]['disposition']=='BYTE_IDENTICAL',name
verdict=read('review/VERDICT.json');assert verdict['verdict']=='PASS'
assert h((root/'candidate/REPORT.md').read_bytes())==verdict['candidate_report_sha256']
assert h((root/'candidate/MANIFEST.json').read_bytes())==verdict['candidate_manifest_sha256']
assert h((root/'candidate/REPORT.md').read_bytes())=='90385545114303539d4c29e9cc6cde2383480d6ad94cad83899ecc4f1cab0762'
assert h((root/'review/INDEPENDENT_REVIEW.md').read_bytes())=='f0afdc63c6ae2ce6364a5872d97e5b985435ac9655a7b1ca3031cb3be8bfb503'
for e in read('candidate/SOURCE_BINDINGS.json'):
 b=(root/'candidate'/e['copy']).read_bytes();assert h(b)==e['sha256'] and len(b)==e['bytes']
scope=read('CLAIM_SCOPE.json');assert scope['priority']==58 and scope['status']=='TO RESEARCH' and scope['owner']=='F020' and scope['alias']=='F023'
assert scope['combined_range']=='0<=b<=3p AND b<p^s'
assert scope['explicit_truncations']['p=3,s=2']=='b<9; b=9 is not added'
assert not scope['owner_closure'] and not scope['score_changes']
# These fragments avoid embedding a forbidden service locator in this source.
bad=[('/'+'workspace'+'/').encode(),('/'+'home'+'/agent/').encode(),('docs.'+'google.com').encode(),('chatgpt.com'+'/c/').encode(),('codex'+':/').encode()]
for f in root.rglob('*'):
 if f.is_file():
  b=f.read_bytes()
  assert not any(x in b for x in bad),str(f.relative_to(root))+' privacy locator'
print(json.dumps({'verdict':'PASS','public_manifest_files':len(paths),'source_entries':len(ledger),'byte_identical':sum(e['disposition']=='BYTE_IDENTICAL' for e in ledger),'metadata_projections':sum(e['disposition']!='BYTE_IDENTICAL' for e in ledger),'explicit_omitted_frozen_entries':len(omitted),'mathematical_scripts_executed':False,'historical_source_programs_executed':False,'external_writes':False},indent=2))
