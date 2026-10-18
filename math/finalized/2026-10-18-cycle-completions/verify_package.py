#!/usr/bin/env python3
"""Read-only preservation-integrity checks. No scientific module is imported."""
from pathlib import Path
import ast, hashlib, json, re
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'MANIFEST.json').read_text())['files']
allowed=json.loads((ROOT/'PRESERVATION_ALLOWLIST.json').read_text())['paths']
actual=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file())
assert actual==allowed, 'Exact public file set mismatch'
assert sorted(manifest)==[p for p in actual if p!='MANIFEST.json']
python_count=json_count=0
patterns=[r'/workspace/',r'/home/agent/',r'libfile_[A-Za-z0-9]+',r'sediment://',r'https://chatgpt\.com/c/',r'https://docs\.google\.com/spreadsheets/',r'codex://']
for name,entry in manifest.items():
    path=ROOT/name
    assert not path.is_symlink(),name
    body=path.read_bytes()
    assert len(body)==entry['bytes'] and hashlib.sha256(body).hexdigest()==entry['sha256'],name
    text=body.decode('utf-8')
    # The checker contains the banned-pattern literals so skip its own text scan.
    if name!='verify_package.py':
        assert not any(re.search(p,text) for p in patterns),name
    if path.suffix=='.py':ast.parse(text);python_count+=1
    if path.suffix=='.json':json.loads(text);json_count+=1
print(json.dumps({'status':'PASS','public_files':len(actual),'hashed_files':len(manifest),'python_sources_parsed':python_count,'json_files_parsed':json_count,'scientific_programs_executed':False,'external_writes':False},indent=2))
