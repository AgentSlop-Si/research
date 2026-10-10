#!/usr/bin/env python3
"""Verify this review's sealed files; does not execute any source file."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SEAL.json').read_text())
for row in manifest['files']:
    p=root/row['path']
    assert p.is_file(),row['path']
    b=p.read_bytes()
    assert len(b)==row['bytes'],row['path']
    assert hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
print(json.dumps({'verified_files':len(manifest['files']),'status':'PASS'},sort_keys=True))
