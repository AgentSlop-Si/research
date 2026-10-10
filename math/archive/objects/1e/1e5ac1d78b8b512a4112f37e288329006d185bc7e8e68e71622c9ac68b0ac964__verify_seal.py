from pathlib import Path
import json,hashlib
p=Path(__file__).parent
manifest=p/'SEALED_MANIFEST.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==(p/'SEALED_MANIFEST.sha256').read_text().split()[0]
for name,h in json.loads(manifest.read_text())['files'].items():
 assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h,name
print('SEALED MANIFEST VERIFIED')
