"""Verify this frozen checkpoint's bytes, archive members and review bindings.

Run: python verify_package.py
No third-party dependencies are needed. This is an integrity check, not a
fresh execution of the historical mathematical proofs or a live table audit.
"""
from pathlib import Path, PurePosixPath
import csv
import hashlib
import io
import json
import zipfile

ROOT = Path(__file__).resolve().parent


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    manifest = json.loads((ROOT / 'PACKAGE_MANIFEST.json').read_text())
    for row in manifest['files']:
        path = ROOT / row['path']
        data = path.read_bytes()
        assert len(data) == row['bytes'], row['path']
        assert sha256(data) == row['sha256'], row['path']
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == row['git_blob_sha'], row['path']
    science = json.loads((ROOT / 'SCIENCE_ARCHIVES.json').read_text())
    table = json.loads((ROOT / 'TABLE_ARCHIVE.json').read_text())
    contents = {}
    for archive in science['archives'] + [table]:
        raw = (ROOT / archive['path']).read_bytes()
        assert len(raw) == archive['bytes'] and sha256(raw) == archive['sha256']
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names = z.namelist()
            assert len(names) == len(set(names))
            assert set(names) == {f['path'] for f in archive['files']}
            assert z.testzip() is None
            for row in archive['files']:
                name = row['path']
                path = PurePosixPath(name)
                assert not path.is_absolute() and '..' not in path.parts
                assert ((z.getinfo(name).external_attr >> 16) & 0o170000) != 0o120000
                data = z.read(name)
                assert len(data) == row['bytes'] and sha256(data) == row['sha256'], name
                if name in contents:
                    assert contents[name] == data
                contents[name] = data
    index = json.loads((ROOT / 'SCIENTIFIC_ACCEPTANCE_INDEX.json').read_text())
    for record in index['records']:
        assert sha256(contents[record['review_path']]) == record['review_sha256']
    seals = json.loads((ROOT / 'COMPLETED_SCIENTIFIC_SEALS_CHECK.json').read_text())
    assert not seals['bad']
    assert len(seals['checks']) == seals['checked'] == 588
    for row in seals['checks']:
        assert row['pass'] and sha256(contents[row['path']]) == row['sha256']
    rankings = list(csv.DictReader((ROOT / 'CURRENT_PRIORITIES_331.csv').open()))
    assert len(rankings) == len({r['record_id'] for r in rankings}) == 331
    assert sum(r['canonical_counted'].lower() == 'true' for r in rankings) == 178
    assert len(science['archives']) == 7 and len(index['records']) == 7
    assert sum(len(a['files']) for a in science['archives']) == 656
    assert len(table['files']) == 45 and len(contents) == 701
    print(json.dumps({'status': 'PASS', 'manifested_files': len(manifest['files']),
                      'archives': 8, 'archived_files': 701, 'seal_bindings': 588,
                      'review_bindings': 7, 'ranking_ids': 331, 'canonical_claims': 178}))


if __name__ == '__main__':
    main()
