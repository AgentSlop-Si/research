"""New reviewer-owned byte-only seal verifier. Does not import supplied programs."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
manifest=json.loads((R/'SEALED_MANIFEST.json').read_text())
fail=[]
for row in manifest['files']:
 p=R/row['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256'] or p.stat().st_size!=row['size_bytes']:fail.append(row['path'])
seal=json.loads((R/'SEAL.json').read_text())
if hashlib.sha256((R/'SEALED_MANIFEST.sha256').read_bytes()).hexdigest()!=seal['checksum_list_sha256']:fail.append('SEALED_MANIFEST.sha256')
for line in (R/'SEALED_MANIFEST.sha256').read_text().splitlines():
 h,rel=line.split('  ',1)
 if hashlib.sha256((R/rel).read_bytes()).hexdigest()!=h:fail.append(rel)
print(json.dumps({'files_verified':len(manifest['files']),'failures':fail,'source_execution':False},indent=2))
raise SystemExit(bool(fail))
