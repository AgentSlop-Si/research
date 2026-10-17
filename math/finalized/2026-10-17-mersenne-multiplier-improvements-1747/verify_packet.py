from pathlib import Path
import hashlib, json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PUBLICATION_MANIFEST.json').read_text())
expected={e['path'] for e in manifest['files']}
actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert actual==expected|{'PUBLICATION_MANIFEST.json'}, 'Missing or extra publication files'
for e in manifest['files']:
 p=root/e['path']; assert not p.is_symlink()
 data=p.read_bytes()
 assert len(data)==e['bytes'] and hashlib.sha256(data).hexdigest()==e['sha256'], e['path']
print(f"PASS: {len(expected)} files match the current publication manifest.")
