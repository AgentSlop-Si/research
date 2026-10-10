from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
b=(p/'SEALED_MANIFEST.json').read_bytes()
assert hashlib.sha256(b).hexdigest()==(p/'SEALED_MANIFEST.sha256').read_text().split()[0]
x=json.loads(b)
for r in x['files']:
    data=(p/r['path']).read_bytes()
    assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
print('PASS:',len(x['files']),'sealed files; read-only verification')
