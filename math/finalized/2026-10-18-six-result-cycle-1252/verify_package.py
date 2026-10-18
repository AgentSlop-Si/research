#!/usr/bin/env python3
"""Check exact public preservation, paths and syntax; never run scientific code."""
from pathlib import Path
import ast,hashlib,json
R=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
allow=json.loads((R/'PRESERVATION_ALLOWLIST.json').read_text())['files']
actual=sorted(p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file())
assert actual==allow,'Missing or unexpected public file'
assert not any(p.is_symlink() for p in R.rglob('*')),'Symlink forbidden'
manifest=json.loads((R/'MANIFEST.json').read_text())
for e in manifest['files']:
 p=R/e['path'];assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],e['path']
status=json.loads((R/'RELEASE_STATUS.json').read_text())
assert status['final_review_gate_passed'] and status['accepted_results']==6
seal=json.loads((R/'SEAL.json').read_text());assert seal['manifest_sha256']==sha(R/'MANIFEST.json') and seal['final_review_gate_passed']
accept=json.loads((R/'FINAL_ACCEPTANCES.json').read_text());assert accept['all_six_final_gates_passed'] and len(accept['acceptances'])==6
for route in status['included_routes']:
 p=R/route/'MANIFEST.json'
 for e in json.loads(p.read_text())['files']:
  f=p.parent/e['path'];assert f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],str(f.relative_to(R))
for route,filename,key,field in [
 ('degree17/candidate','SOURCE_PINS.json',None,'local_path'),
 ('mersenne_stream/candidate','SOURCE_PINS.json','sources','path'),
 ('mersenne_stream/review','SOURCE_BINDINGS.json','sources','review_copy'),
 ('centered_integration/candidate','SOURCE_BINDINGS.json','local_sources','snapshot_path'),
 ('rank_two/candidate','SOURCES.json','accepted_local_dependencies','path'),
 ('sparse_masks/candidate','SOURCE_BINDINGS.json','copied_sources','copy')]:
 d=json.loads((R/route/filename).read_text());rows=d[key] if key else d
 if isinstance(rows,dict):rows=rows.values()
 for e in rows:
  p=(R/route/e[field]).resolve();assert p.is_relative_to(R.resolve()) and p.is_file()
  assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],str(p)
for p in R.rglob('*.py'):ast.parse(p.read_text(),filename=p.relative_to(R).as_posix())
for e in json.loads((R/'COPY_BINDINGS.json').read_text())['files']:
 p=R/e['path'];assert p.stat().st_size==e['public_bytes'] and sha(p)==e['public_sha256'],e['path']
 if e['byte_identical']:assert e['original_sha256']==e['public_sha256'] and e['original_bytes']==e['public_bytes']
print(json.dumps({'status':'PASS','final_review_gates':6,'allowlisted_files':len(actual),'manifest_bound_files':len(manifest['files']),'scientific_programs_executed':False,'external_writes':False}))
