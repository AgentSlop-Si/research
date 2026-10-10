#!/usr/bin/env python3
"""Verify the immutable-by-convention review snapshot; no source imports."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=root/'SEALED_MANIFEST.json'
expected=(root/'SEALED_MANIFEST.sha256').read_text().split()[0]
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected,'Manifest hash mismatch'
data=json.loads(manifest.read_text())
known=set()
for item in data['files']:
    name=item['path'];known.add(name);p=root/name
    assert p.is_file(),name
    b=p.read_bytes()
    assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],name
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==known|{'SEALED_MANIFEST.json','SEALED_MANIFEST.sha256'},'Unexpected/missing files'
print('PASS: '+str(len(known))+' files; manifest '+expected)
