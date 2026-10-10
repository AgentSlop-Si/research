"""Verify this archive as data; never import or execute its research programs."""
from pathlib import Path
import gzip
import hashlib
import json

root = Path(__file__).resolve().parent
h = lambda b: hashlib.sha256(b).hexdigest()
allow = json.loads((root / 'ALLOWLIST.json').read_text())['members']
actual = sorted(p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file())
assert actual == sorted(allow), 'Unexpected or missing member'
for line in (root / 'SHA256SUMS').read_text().splitlines():
    digest, relative = line.split('  ', 1)
    assert h((root / relative).read_bytes()) == digest, relative
manifest = json.loads((root / 'EXPORT_MANIFEST.json').read_text())
for row in manifest['members']:
    data = (root / row['path']).read_bytes()
    assert len(data) == row['bytes'] and h(data) == row['sha256'], row['path']
for row in json.loads((root / 'COMPRESSED_CERTIFICATES.json').read_text()):
    compressed = (root / row['archive_path']).read_bytes()
    raw = gzip.decompress(compressed)
    assert h(compressed) == row['sha256'], row['archive_path']
    assert len(raw) == row['reconstructed_bytes'], row['reconstructed_path']
    assert h(raw) == row['reconstructed_sha256'], row['reconstructed_path']
print('PASS:', len(actual), 'members; all shipped hashes and both gzip reconstructions verified.')
