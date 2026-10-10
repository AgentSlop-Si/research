"""Fresh package-integrity verifier. It never executes/imports assigned sources."""
import hashlib, json
from pathlib import Path, PurePosixPath
root=Path(__file__).resolve().parent
manifest_path=root/'SEALED_MANIFEST.json'
expected=(root/'SEALED_MANIFEST.sha256').read_text().split()[0]
actual=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
if actual!=expected:raise RuntimeError('Manifest digest mismatch')
manifest=json.loads(manifest_path.read_text())
seen=set()
for item in manifest['files']:
    name=item['path'];relative=PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or name in seen:raise RuntimeError('Unsafe or duplicate manifest path')
    seen.add(name);path=root/name
    if path.is_symlink() or not path.is_file():raise RuntimeError('Missing or nonregular file: '+name)
    data=path.read_bytes()
    if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:raise RuntimeError('File mismatch: '+name)
actual_files={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
if actual_files!=seen|{'SEALED_MANIFEST.json','SEALED_MANIFEST.sha256'}:raise RuntimeError('Unexpected/missing package files')
review=json.loads((root/'SOURCE_REVIEW.json').read_text())
assignment=json.loads((root/'inputs/ASSIGNMENT.json').read_text())
assigned=set()
for name in assignment['batch_names']:
    assigned.update(r['sha256'] for r in json.loads((root/'inputs'/name).read_text())['rows'])
reviewed={r['sha256'] for r in review['rows']}
coverage=json.loads((root/'ADDITIVE_CODE_COVERAGE.json').read_text())
covered={r['sha256']for r in coverage['rows']}
if len(assigned)!=45 or assigned!=reviewed or assigned!=covered:raise RuntimeError('Assignment/review/coverage mismatch')
if len(review['rows'])!=45 or len(coverage['rows'])!=45:raise RuntimeError('Duplicate coverage rows')
evidence=hashlib.sha256((root/'SOURCE_REVIEW.json').read_bytes()).hexdigest()
for row in review['rows']:
    data=(root/row['snapshot_path']).read_bytes()
    if hashlib.sha256(data).hexdigest()!=row['sha256'] or len(data)!=row['size_bytes']:raise RuntimeError('Source snapshot mismatch')
    if row['reviewed_line_intervals']!=[[1,len(data.decode('utf-8').splitlines())]]:raise RuntimeError('Line coverage mismatch')
    if not row['full_static_inspection'] or any(row[k]for k in ['source_executed_in_review','source_imported_in_review','source_compiled_in_review','source_ast_parsed_in_review']):raise RuntimeError('Review scope mismatch')
for row in coverage['rows']:
    if row['evidence_sha256']!=evidence:raise RuntimeError('Evidence reference mismatch')
prior={r['sha256']for r in json.loads((root/'inputs/ADDITIVE_CODE_COVERAGE.json').read_text())['rows']}
if prior&assigned:raise RuntimeError('Unexpected baseline overlap')
print(json.dumps({'status':'PASS','manifest_sha256':actual,'sealed_files':len(seen),'reviewed_hashes':len(reviewed),'additive_hashes_against_snapshot':45,'source_review_sha256':evidence},indent=2))
