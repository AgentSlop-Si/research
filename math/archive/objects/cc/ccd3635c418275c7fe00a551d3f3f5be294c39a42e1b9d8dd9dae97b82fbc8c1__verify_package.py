"""Independent read-only integrity checker; never imports supplied source code."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    payloads = 0
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        rel = PurePosixPath(name)
        assert not rel.is_absolute() and '..' not in rel.parts
        assert sha((ROOT / name).read_bytes()) == expected, name
        payloads += 1
    provenance = json.loads((ROOT / 'PROVENANCE.json').read_text())
    total_members = 0
    for record in provenance:
        archive = ROOT / record['package_archive_path']
        assert sha(archive.read_bytes()) == record['archive_sha256'], archive.name
        expected_names = set()
        with zipfile.ZipFile(archive) as z:
            for entry in z.infolist():
                q = PurePosixPath(entry.filename)
                assert not q.is_absolute() and '..' not in q.parts
                assert not stat.S_ISLNK(entry.external_attr >> 16)
            for entry in record['files']:
                # Extraction used one branch directory before the actual ZIP name.
                member = str(PurePosixPath(entry['path']).relative_to(PurePosixPath(entry['path']).parts[0]))
                expected_names.add(member)
                data = z.read(member)
                assert len(data) == entry['size'], member
                assert sha(data) == entry['sha256'], member
                total_members += 1
            actual_names = {i.filename for i in z.infolist() if not i.is_dir()}
            assert actual_names == expected_names, archive.name
            assert len(actual_names) == sum(not i.is_dir() for i in z.infolist()), 'duplicate archive members'
        print('PASS archive and members:', archive.name)
    hero = next(r for r in provenance if 'hero17_phase_union' in r['package_archive_path'])
    note = next(x for x in hero['files'] if x['path'].endswith('/RESEARCH.md'))
    assert note['sha256'] == '503cf095980e7114f8d9bff39d7e33fe600a7747bfbb8756cd5c7729cf63c2b9'
    print(f'PASS: {payloads} payload files; {len(provenance)} original archives; {total_members} preserved members.')
    print('No supplied code was imported, executed, compiled, or extracted by this checker.')

if __name__ == '__main__':
    main()
