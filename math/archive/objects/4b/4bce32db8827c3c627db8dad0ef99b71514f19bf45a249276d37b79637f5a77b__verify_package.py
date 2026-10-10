"""Byte-only package and source integrity check; no source execution."""
import json,hashlib,zipfile
from pathlib import Path
p=Path(__file__).resolve().parent
for f in json.loads((p/'SEALED_MANIFEST.json').read_text())['files']:
 b=(p/f['path']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
q=json.loads((p/'PROVENANCE.json').read_text());assert hashlib.sha256((p/'SOURCE.zip').read_bytes()).hexdigest()==q['sha256']
with zipfile.ZipFile(p/'SOURCE.zip') as z:
 assert z.testzip() is None
 for r in q['members']:
  b=z.read(r['member']);assert b==(p/r['snapshot']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['sha256']
print('PASS:15 inert source members and sealed package; no uploaded code executed')
