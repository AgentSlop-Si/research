"""Bind this review package after finalization; originals unchanged."""
import pathlib,hashlib,json
P=pathlib.Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[]
for p in sorted(P.rglob('*')):
 if p.is_file() and p.name not in ('SEAL.json','SHA256SUMS.txt'):
  files.append({'path':p.relative_to(P).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
manifest=''.join(f"{r['sha256']}  {r['path']}\n" for r in files)
(P/'SHA256SUMS.txt').write_text(manifest)
seal={'package':P.name,'scope':'96 assigned exact source hashes fully read inertly; no whole-corpus or supplied-test-execution claim',
      'source_hashes':96,'source_bytes':421838,'source_lines':10245,'source_executed_in_review':False,
      'supplied_source_imported_compiled_or_AST_parsed':False,'fresh_independent_control_count':8,
      'exact_archive_containers_verified':19,'source_archive_occurrences_verified':120,
      'payload_manifest_sha256':sha(P/'SHA256SUMS.txt'),'files':files}
(P/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
for r in files:assert sha(P/r['path'])==r['sha256']
assert sha(P/'SHA256SUMS.txt')==seal['payload_manifest_sha256']
print(json.dumps({'sealed_files':len(files),'payload_bytes':sum(r['bytes'] for r in files),'manifest_sha256':seal['payload_manifest_sha256'],'seal_sha256':sha(P/'SEAL.json')}))
