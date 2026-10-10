"""Auditor-authored byte-only package verifier. Never executes source files."""
import json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
m=json.loads((p/'SEALED_MANIFEST.json').read_text())
for r in m['files']:
 b=(p/r['path']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],r['path']
c=json.loads((p/'COVERAGE.json').read_text());assert len(c['rows'])==136
for r in c['rows']:
 b=(p/r['source_snapshot']).read_bytes();assert len(b)==r['size_bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
print('PASS: package hashes and136 exact source identities; no source executable run')
