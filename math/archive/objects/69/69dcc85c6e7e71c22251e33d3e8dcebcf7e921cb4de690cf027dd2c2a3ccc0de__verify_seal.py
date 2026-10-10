import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SEALED_MANIFEST.json').read_text())
for name,expected in manifest['files'].items():
    if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected:
        raise SystemExit('HASH MISMATCH: '+name)
print('SEALED FILES PASS:',len(manifest['files']))
