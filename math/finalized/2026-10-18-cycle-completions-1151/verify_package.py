#!/usr/bin/env python3
"""Check publication bytes and exact allowlist; never execute scientific code."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
allow=json.loads((root/'PRESERVATION_ALLOWLIST.json').read_text())
actual=sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())
assert not any(p.is_symlink() for p in root.rglob('*')), 'Symlinks forbidden'
assert actual==allow['files'], 'Unexpected or missing publication file'
for row in manifest['files']:
 p=root/row['path'];b=p.read_bytes()
 assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
status=json.loads((root/'RELEASE_STATUS.json').read_text())
if status['final_review_gate_passed']:
 seal=json.loads((root/'SEAL.json').read_text())
 assert seal['final_review_gate_passed'] is True
 assert hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest()==seal['manifest_sha256']
else:
 assert not (root/'SEAL.json').exists(),'Draft must not have a release seal'
print(json.dumps({'status':'PASS','release_final':status['final_review_gate_passed'],'allowlisted_files':len(actual),'manifest_bound_files':len(manifest['files']),'scientific_programs_executed':False}))
