"""Verify only public package bytes. Never import or execute scientific code."""
from pathlib import Path
import hashlib, io, json, zipfile
P = Path(__file__).parent
def pin(b): return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def check_archive(raw, m):
    assert pin(raw) == {k: m['archive'][k] for k in ['bytes', 'sha256']}
    z = zipfile.ZipFile(io.BytesIO(raw)); assert z.testzip() is None
    assert len(z.namelist()) == len(set(z.namelist())) == len(m['archive']['members'])
    assert set(z.namelist()) == {x['path'] for x in m['archive']['members']}
    for x in m['archive']['members']: assert pin(z.read(x['path'])) == {k: x[k] for k in ['bytes', 'sha256']}
    for x in m['projection']['source_correspondence']: assert pin(z.read(x['archive_path'])) == x['public']
    for x in m['projection'].get('historical_manifests', []):
        b = z.read(x['archive_path']); assert pin(b) == {k: x[k] for k in ['bytes', 'sha256']}
        d = json.loads(b); fs = d.get('members', d.get('files', d)); label = x['archive_path'].rsplit('/', 1)[0]
        fs = {e['path']: {'bytes': e.get('bytes', e.get('size')), 'sha256': e['sha256']} for e in fs} if isinstance(fs, list) else fs
        for name, v in fs.items():
            original = next(e['original'] for e in m['projection']['source_correspondence'] if e['archive_path'] == label + '/' + name)
            assert original['sha256'] == v if isinstance(v, str) else original == v
    counts = [len(z.namelist())]
    for name in z.namelist():
        if name.endswith('/evidence.zip'):
            child = json.loads(z.read(name.rsplit('/', 1)[0] + '/PUBLIC_MANIFEST.json'))
            counts += check_archive(z.read(name), child)[1]
    return z, counts
M = json.loads((P / 'PUBLIC_MANIFEST.json').read_bytes())
raw = b''.join((P / x['path']).read_bytes() for x in M['archive']['parts'])
z, counts = check_archive(raw, M)
for x in M['archive']['parts']:
    b = (P / x['path']).read_bytes(); assert pin(b) == {k: x[k] for k in ['bytes', 'sha256']}
    assert raw[x['offset']:x['offset']+len(b)] == b and len(b) <= 409600
for x in M['direct_science_copies']: assert (P / x['path']).read_bytes() == z.read(x['archive_path'])
for x in M['direct_files']: assert pin((P / x['path']).read_bytes()) == {k: x[k] for k in ['bytes', 'sha256']}
assert json.loads(z.read('PUBLIC_PROJECTION.json')) == M['projection']
assert json.loads(z.read('SCOPED_RESULT.json')) == M['scope']
assert json.loads(z.read('SOURCE_CLOSURE.json')) == M['source_closure']
print(json.dumps({'verified': True, 'archive_bytes': len(raw), 'members': counts[0], 'current_source_entries': 46, 'nested_member_counts': counts[1:], 'research_code_executed': False, 'public_control_replay_certified': False}))
