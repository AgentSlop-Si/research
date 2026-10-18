#!/usr/bin/env python3
"""Verify publication bytes and allowlist only; never execute scientific code."""
from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text())
a=json.loads((root/'PRESERVATION_ALLOWLIST.json').read_text())
actual=sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())
assert actual==a['files'], 'Unexpected or missing publication file'
for row in m['files']:
 data=(root/row['path']).read_bytes()
 assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
seal=json.loads((root/'SEAL.json').read_text())
assert hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()==seal['manifest_sha256']
print(json.dumps({'status':'PASS','allowlisted_files':len(actual),'manifest_bound_files':len(m['files']),'scientific_programs_executed':False}))
