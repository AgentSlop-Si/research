"""Portable integrity reconciliation for data copies, no source execution."""
from pathlib import Path
import hashlib,json
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=Path(__file__).resolve().parent
c=json.loads((r/'COVERAGE.json').read_text());q=json.loads((r/'SOURCE_QUEUE.json').read_text())
assert H(r/'SOURCE_QUEUE.json')==c['source_queue_sha256']
assert len(c['rows'])==q['count']==200
seen=[];hashes=[];size=0;members=0
for p in c['packages']:
 d=r/p['path'];m=d/'SEALED_MANIFEST.json';assert H(m)==p['manifest_sha256']
 f=json.loads(m.read_text())['files'];fs=f.items() if isinstance(f,dict) else ((x['path'],x['sha256']) for x in f)
 n=0
 for name,sha in fs:assert H(d/name)==sha;n+=1
 assert n==p['verified_manifest_members'];members+=n
 rows=json.loads((d/'COVERAGE.json').read_text())['rows']
 assert sorted(x['queue_index'] for x in rows)==p['rows']
 assert sum(x['size_bytes'] for x in rows)==p['source_bytes']
 for x in rows:
  i=x['queue_index'];a=c['rows'][i];b=q['sources'][i]
  assert a['queue_index']==i and x['sha256']==a['sha256']==b['sha256']
  assert x['canonical_path']==a['canonical_path']==b['canonical_path']
  assert x['inspection']=='complete_text_read'
  raw=d/x['local_inert_snapshot'];assert H(raw)==x['sha256'] and raw.stat().st_size==x['size_bytes']
  seen.append(i);hashes.append(x['sha256']);size+=x['size_bytes']
assert sorted(seen)==list(range(200)) and len(set(seen))==200 and len(set(hashes))==200
assert size==c['completed_source_bytes']==q['bytes']==1230558
out={'status':'PASS','full_text_inspection_records':200,'unique_sha256':200,'source_bytes':size,'packages_verified':6,'package_manifest_members_verified':members,'gaps':[],'overlaps':[],'uploaded_programs_executed_by_this_reconciliation':0,'scope':'Verifies evidence identity and coverage, not mathematical truth or actual source execution.'}
(r/'INTEGRITY_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
