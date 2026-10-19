"""Restore only scientific/support source files into a new directory. No science runs."""
from pathlib import Path
import hashlib
import json
import runpy
import sys

ROOT=Path(__file__).resolve().parent
if len(sys.argv)!=2:
    raise SystemExit('Usage: python restore_sources.py NEW_EMPTY_DIRECTORY')
output=Path(sys.argv[1]).resolve()
if output.exists():
    raise SystemExit('Destination must not already exist; choose a new directory.')
ns=runpy.run_path(str(ROOT/'verify_package.py'))
receipt=ns['verify']()
copies=json.loads((ROOT/'COPY_BINDINGS.json').read_text())['files']
payload=[]
for item in copies:
    name=item.get('logical_path',item['public_path'])
    relative=Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Unsafe restored source path')
    data=ns['source_data'](name)
    if len(data)!=item['source_bytes'] or hashlib.sha256(data).hexdigest()!=item['source_sha256']:
        raise ValueError('Restoration integrity failure: '+name)
    payload.append((relative,data))
output.mkdir(parents=True,exist_ok=False)
for relative,data in payload:
    p=output/relative
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(data)
    if p.read_bytes()!=data:raise ValueError('Restored write failed: '+str(relative))
print(json.dumps({'verdict':'PASS','restored_source_files':len(payload),'restored_bytes':sum(len(d) for _,d in payload),'output':str(output),'scientific_programs_executed':False},indent=2))
