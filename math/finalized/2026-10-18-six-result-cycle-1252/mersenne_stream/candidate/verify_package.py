"""Verify the exact local candidate and read-only inherited report bindings."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
for entry in manifest['files']:
    path = ROOT / entry['path']
    data = path.read_bytes()
    assert len(data) == entry['bytes'], path
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], path
sources = json.loads((ROOT / 'SOURCE_PINS.json').read_text())
for entry in sources['sources']:
    path = ROOT / entry['path']
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry['sha256'], path
print(json.dumps({'status': 'PASS', 'candidate_files': len(manifest['files']),
                  'inherited_sources': len(sources['sources'])}))
