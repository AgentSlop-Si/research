"""Verify local immutable payload and byte-pinned inherited dependencies."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).parent
manifest = json.loads((root / 'MANIFEST.json').read_text())
for row in manifest['files']:
    raw = (root / row['path']).read_bytes()
    assert len(raw) == row['bytes'], row['path']
    assert hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
pins = json.loads((root / 'SOURCE_PINS.json').read_text())
for row in pins['sources']:
    raw = (root / row['package_path']).read_bytes()
    assert len(raw) == row['bytes'], row['package_path']
    assert hashlib.sha256(raw).hexdigest() == row['sha256'], row['package_path']
print(json.dumps({'status': 'PASS', 'manifest_files': len(manifest['files']),
                  'source_pins': len(pins['sources'])}, sort_keys=True))
