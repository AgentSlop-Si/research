#!/usr/bin/env python3
"""Verify publication integrity and syntax only; do not import scientific code."""
from pathlib import Path
import ast,hashlib,json
R=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads((R/p).read_text())
def safe(rel):
 p=(R/rel).resolve();assert p.is_relative_to(R) and p.is_file(),rel;return p

def verify_manifest(path):
 p=safe(path);d=json.loads(p.read_text());rows=d.get('files',d.get('canonical_files'))
 if rows is None:rows=[{'path':k,'sha256':v} for k,v in d.items()]
 for e in rows:
  f=(p.parent/e['path']).resolve();assert f.is_relative_to(R) and f.is_file(),e['path']
  assert sha(f)==e['sha256'],str(f)
  if 'bytes' in e:assert f.stat().st_size==e['bytes'],str(f)
 return len(rows)

actual=sorted(p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file())
assert actual==load('PRESERVATION_ALLOWLIST.json')['files'],'Missing or unexpected file'
assert not any(p.is_symlink() for p in R.rglob('*')),'Symlink forbidden'
count=verify_manifest('MANIFEST.json');seal=load('SEAL.json');status=load('RELEASE_STATUS.json')
assert seal['manifest_sha256']==sha(R/'MANIFEST.json')
assert seal['allowlist_sha256']==sha(R/'PRESERVATION_ALLOWLIST.json')
assert seal['final_review_gate_passed']==status['final_review_gate_passed']
for route in status['included_routes']:
 verify_manifest(route+'/MANIFEST.json')
 route_seal=R/route/'SEAL.json'
 if route_seal.exists():assert json.loads(route_seal.read_text())['manifest_sha256']==sha(R/route/'MANIFEST.json'),route
for e in load('COPY_BINDINGS.json')['files']:
 p=safe(e['path']);assert p.stat().st_size==e['public_bytes'] and sha(p)==e['public_sha256'],e['path']
 if e['byte_identical']:assert e['original_bytes']==e['public_bytes'] and e['original_sha256']==e['public_sha256'],e['path']
for e in load('SOURCE_BINDINGS.json')['bindings']:
 p=safe(e['path']);assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],e['path']
for p in R.rglob('*.py'):ast.parse(p.read_text(),filename=p.relative_to(R).as_posix())
for rel in load('PACKAGING_CHECKS.json')['byte_identical_required_payloads']:
 e=next(e for e in load('COPY_BINDINGS.json')['files'] if e['path']==rel);assert e['byte_identical'],rel
if status['final_review_gate_passed']:
 a=load('FINAL_ACCEPTANCES.json');assert a['all_six_final_gates_passed'] and len(a['acceptances'])==6
 assert status['accepted_results']==seal['accepted_results']==6
 for e in a['acceptances']:
  assert sha(safe(e['public_review_report']))==e['public_review_report_sha256']
  assert sha(safe(e['public_candidate_report']))==e['public_candidate_report_sha256']
print(json.dumps({'status':'PASS','publication_status':status['status'],'final_review_gates':6 if status['final_review_gate_passed'] else 'PENDING','allowlisted_files':len(actual),'manifest_bound_files':count,'scientific_programs_executed':False,'external_writes':False}))
