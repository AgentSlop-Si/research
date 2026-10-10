"""Fresh byte-only integrity and exact207-row coverage verifier."""
import json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
m=json.loads((p/'SEALED_MANIFEST.json').read_text())
for r in m['files']:
 b=(p/r['path']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
x=json.loads((p/'COVERAGE.json').read_text());q=json.loads((p/'SOURCE_QUEUE.json').read_text())['sources'];assert [r['queue_index'] for r in x['rows']]==list(range(207))
for r,s in zip(x['rows'],q):
 b=(p/r['source_snapshot']).read_bytes();assert len(b)==r['size_bytes']==s['size_bytes'];assert hashlib.sha256(b).hexdigest()==r['sha256']==s['sha256'];assert r['full_text_inspection']=='complete'
assert sum(r['size_bytes'] for r in x['rows'])==1230544
for r in x['bundles']:
 d=p/'reviews'/r['bundle'];assert hashlib.sha256((d/'SEALED_MANIFEST.json').read_bytes()).hexdigest()==r['manifest_sha256']
 for f in json.loads((d/'SEALED_MANIFEST.json').read_text())['files']:
  b=(d/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
print('PASS:207 source identities,1230544 bytes,three unchanged seals; no source executable run')
