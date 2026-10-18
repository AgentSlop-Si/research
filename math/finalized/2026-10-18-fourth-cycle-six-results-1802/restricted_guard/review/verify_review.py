from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parent
m=json.loads((r/'MANIFEST.json').read_text())
for f in m['files']:
 b=(r/f['path']).read_bytes()
 assert len(b)==f['bytes'],f['path']
 assert hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
c=r.parent/'candidate'
assert hashlib.sha256((c/'ORIGINAL_MANIFEST.json').read_bytes()).hexdigest()=='5eb8a2ca9cb85103d4da0833f63126b890820108823b07df673fae30a1f4f10b'
for f in json.loads((c/'MANIFEST.json').read_text())['files']:
 b=(c/f['path']).read_bytes()
 assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
assert json.loads((r/'INDEPENDENT_RESULTS.json').read_text())['status']=='PASS'
assert json.loads((r/'LIFT_RESULTS.json').read_text())['status']=='PASS'
result={'status':'PASS','payloads':len(m['files']),'manifest_sha256':hashlib.sha256((r/'MANIFEST.json').read_bytes()).hexdigest(),'review_sha256':hashlib.sha256((r/'REVIEW.md').read_bytes()).hexdigest()}
(r/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
