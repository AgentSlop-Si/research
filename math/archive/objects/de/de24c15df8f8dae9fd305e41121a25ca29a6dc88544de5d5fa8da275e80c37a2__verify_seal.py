#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=root/'SEALED_MANIFEST.json'
expected=(root/'SEALED_MANIFEST.sha256').read_text().split()[0]
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==expected
entries=json.loads(manifest.read_text())['files']
for entry in entries:
    p=root/entry['path']
    assert p.is_file(),entry['path']
    assert p.stat().st_size==entry['bytes'],entry['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],entry['path']
print('PASS',len(entries),'sealed files')
