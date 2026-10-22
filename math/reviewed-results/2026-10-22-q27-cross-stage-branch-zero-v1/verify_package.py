#!/usr/bin/env python3
"""Verify publication bytes and exact science closure, without executing research."""
from pathlib import Path
import hashlib, json, sys, zipfile, zlib

here=Path(__file__).resolve().parent
manifest=json.loads((here/'CONTENTS.json').read_text())
archive=here/manifest['archive']['path']
data=archive.read_bytes()
assert len(data)==manifest['archive']['bytes']
assert hashlib.sha256(data).hexdigest()==manifest['archive']['sha256']
with zipfile.ZipFile(archive) as z:
    expected={e['path']:e for e in manifest['members']}
    assert len(z.infolist())==len(expected)
    assert set(z.namelist())==set(expected)
    assert z.testzip() is None
    for name,e in expected.items():
        assert not name.startswith('/') and '..' not in Path(name).parts
        b=z.read(name)
        assert len(b)==e['bytes']
        assert hashlib.sha256(b).hexdigest()==e['sha256']
        assert f'{zlib.crc32(b)&0xffffffff:08x}'==e['crc32']
        assert z.getinfo(name).compress_size==e['compressed_bytes']
    projection=json.loads(z.read('PUBLIC_PROJECTION.json'))
    omitted={e['original_path']:e for e in projection['administrative_omissions']}
    for m in manifest['source_manifests']:
        raw=z.read(m['path'])
        assert hashlib.sha256(raw).hexdigest()==m['sha256']
        src=json.loads(raw)
        es=src.get('files',src.get('entries'))
        if es is None:es=[{'path':p,'sha256':h} for p,h in src.items()]
        parent=str(Path(m['path']).parent)
        for e in es:
            name=parent+'/'+e['path']
            if name in omitted:
                assert name not in expected
                assert omitted[name]['original_sha256']==e['sha256']
                if 'bytes' in e:assert omitted[name]['original_bytes']==e['bytes']
            else:
                assert name in expected,name
                assert expected[name]['sha256']==e['sha256'],name
                if 'bytes' in e:assert expected[name]['bytes']==e['bytes'],name
    for p in projection['administrative_omissions']:
        b=z.read(p['public_projection_path'])
        assert hashlib.sha256(b).hexdigest()==p['public_projection_sha256']
        assert len(b)==p['public_projection_bytes']
    for outside,member in manifest['readable_exact_copies'].items():
        assert (here/outside).read_bytes()==z.read(member)
    assert (here/'PUBLIC_PROJECTION.json').read_bytes()==z.read('PUBLIC_PROJECTION.json')
print('PASS: exact archive hash, inventory, CRC, unchanged science/manifest bindings, declared administrative omissions, and readable copies.')
print('No research program was executed. This check is packaging verification, not a fresh mathematical replay.')
