#!/usr/bin/env python3
"""Verify this publication package with the Python standard library only."""
import hashlib, json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'FILE_MANIFEST.json').read_text(encoding='utf-8'))
entries=manifest['files']
expected={e['path'] for e in entries}
assert len(expected)==len(entries),'Duplicate manifest path'
for e in entries:
    p=root/e['path']
    assert p.is_file() and not p.is_symlink(),f'Missing/unsafe file: {e["path"]}'
    assert root in p.resolve().parents,f'Escaping path: {e["path"]}'
    b=p.read_bytes()
    assert len(b)==e['bytes'],f'Byte count mismatch: {e["path"]}'
    assert hashlib.sha256(b).hexdigest()==e['sha256'],f'Hash mismatch: {e["path"]}'
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==expected|{'FILE_MANIFEST.json','SHA256SUMS'},'Unexpected or unlisted file'
checksums={}
for line in (root/'SHA256SUMS').read_text().splitlines():
    h,name=line.split('  ',1)
    assert name not in checksums,'Duplicate checksum path'
    checksums[name]=h
assert set(checksums)==expected|{'FILE_MANIFEST.json'},'Checksum set mismatch'
for name,h in checksums.items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==h,f'Checksum mismatch: {name}'
print(json.dumps({'status':'PASS','payload_files':len(entries),'manifest_verified':True,'external_state_verified':False},indent=2))
