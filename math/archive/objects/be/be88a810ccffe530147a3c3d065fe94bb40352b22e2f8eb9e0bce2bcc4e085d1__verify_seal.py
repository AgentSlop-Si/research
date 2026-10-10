#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parent
manifest = root / 'SEALED_MANIFEST.json'
expected = (root / 'SEALED_MANIFEST.sha256').read_text().split()[0]
assert hashlib.sha256(manifest.read_bytes()).hexdigest() == expected
entries = json.loads(manifest.read_text())['files']
for name, digest in entries.items():
    path = root / name
    assert path.is_file(), ('missing', name)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, ('changed', name)
actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()
          and '__pycache__' not in p.parts and p.name not in {'SEALED_MANIFEST.json', 'SEALED_MANIFEST.sha256'}}
assert actual == set(entries), ('unlisted', sorted(actual - set(entries)), 'missing', sorted(set(entries) - actual))
print(json.dumps({'status': 'PASS', 'sealed_files': len(entries)}, sort_keys=True))
