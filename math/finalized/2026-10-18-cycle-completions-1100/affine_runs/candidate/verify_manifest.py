#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
manifest = json.loads((root/'MANIFEST.json').read_text())
for item in manifest['files']:
    p = root/item['path']
    blob = p.read_bytes()
    assert len(blob) == item['bytes'], item['path']
    assert hashlib.sha256(blob).hexdigest() == item['sha256'], item['path']
print(json.dumps({'status':'pass','verified_files':len(manifest['files'])}))
