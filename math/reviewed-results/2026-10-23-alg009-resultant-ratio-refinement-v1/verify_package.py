#!/usr/bin/env python3
"""Packaging integrity only. Never import or execute a research program."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile
import zlib

HERE = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe(path):
    p = PurePosixPath(path)
    assert not p.is_absolute() and '..' not in p.parts and str(p) == path
    return path

def main():
    checks = {}
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        safe(name)
        assert name not in checks
        checks[name] = digest
    assert set(checks) == {p.name for p in HERE.iterdir() if p.is_file()} - {'SHA256SUMS'}
    for name, digest in checks.items():
        assert sha((HERE / name).read_bytes()) == digest, name
    inventory = json.loads((HERE / 'CONTENTS.json').read_text())
    data = (HERE / inventory['archive']['path']).read_bytes()
    assert len(data) == inventory['archive']['bytes']
    assert sha(data) == inventory['archive']['sha256']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == inventory['archive']['git_blob_sha1']
    with zipfile.ZipFile(HERE / inventory['archive']['path']) as archive:
        expected = {e['path']: e for e in inventory['members']}
        assert len(expected) == len(inventory['members']) == len(archive.infolist())
        assert set(expected) == set(archive.namelist())
        assert archive.testzip() is None
        for name, entry in expected.items():
            safe(name)
            b = archive.read(name)
            assert len(b) == entry['bytes'] and sha(b) == entry['sha256'], name
            assert f'{zlib.crc32(b) & 0xffffffff:08x}' == entry['crc32']
            assert archive.getinfo(name).compress_size == entry['compressed_bytes']
        projection = json.loads(archive.read('PUBLIC_PROJECTION.json'))
        omitted = {e['original_path']: e for e in projection['administrative_omissions']}
        assert len(omitted) == len(projection['administrative_omissions'])
        observed_omissions = set()
        covered = set()
        for item in inventory['source_manifests']:
            raw = archive.read(item['path'])
            assert sha(raw) == item['sha256'] and len(raw) == item['bytes']
            source = json.loads(raw)
            prefix = str(PurePosixPath(item['path']).parent)
            assert len({e['path'] for e in source['files']}) == len(source['files'])
            covered.add(item['path'])
            for entry in source['files']:
                name = prefix + '/' + safe(entry['path'])
                if name in omitted:
                    assert name not in expected
                    omission = omitted[name]
                    assert omission['original_sha256'] == entry['sha256']
                    assert omission['original_bytes'] == entry['bytes']
                    observed_omissions.add(name)
                else:
                    assert name in expected, name
                    assert expected[name]['sha256'] == entry['sha256'], name
                    assert expected[name]['bytes'] == entry['bytes'], name
                    covered.add(name)
        assert observed_omissions == set(omitted)
        for item in projection['administrative_omissions']:
            b = archive.read(item['public_projection_path'])
            assert sha(b) == item['public_projection_sha256']
            assert len(b) == item['public_projection_bytes']
        assert set(expected) == covered | set(inventory['publication_metadata_members'])
        for name, member in inventory['readable_exact_copies'].items():
            assert (HERE / name).read_bytes() == archive.read(member), name
        closure = json.loads(archive.read('SOURCE_CLOSURE.json'))
        for entry in closure['new_research_programs']:
            assert entry['path'] in expected
            assert expected[entry['path']]['sha256'] == entry['sha256']
            for dependency in entry['bundled_program_dependencies'] + entry['data_inputs']:
                assert dependency in expected, dependency
        for entry in closure['inert_historical_sources']:
            assert expected[entry['path']]['sha256'] == entry['sha256']
        result = json.loads(archive.read('SCOPED_RESULT.json'))
        for entry in result['evidence_bindings']:
            assert expected[entry['path']]['sha256'] == entry['sha256']
    print('PASS: all files listed in SHA256SUMS; exact ZIP bytes, inventory, hashes and CRCs; original manifest bindings; declared administrative projection; source/runtime/data closure; readable copies.')
    print('No research program was executed. This is packaging verification, not a mathematical replay or a historical implementation audit.')

if __name__ == '__main__':
    main()
