#!/usr/bin/env python3
"""Verify publication integrity only. No scientific or historical-code execution."""
from pathlib import Path
import csv
import hashlib
import json
import re


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    get = lambda name: json.loads((root / name).read_text())
    allow = get('PRESERVATION_ALLOWLIST.json')
    listed = allow['files']
    assert len(listed) == len(set(listed))
    assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in listed)
    assert not any(p.is_symlink() for p in root.rglob('*'))
    actual = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
    assert actual == sorted(listed), 'Public files do not equal the exact allowlist'
    manifest = get('MANIFEST.json')
    assert sorted(x['path'] for x in manifest['files']) == sorted(set(listed) - {'MANIFEST.json', 'SEAL.json'})
    for entry in manifest['files']:
        p = root / entry['path']
        assert p.stat().st_size == entry['bytes'], entry['path']
        assert digest(p) == entry['sha256'], entry['path']
    seal = get('SEAL.json')
    for name, key in [('MANIFEST.json', 'manifest_sha256'), ('PRESERVATION_ALLOWLIST.json', 'allowlist_sha256'), ('FINAL_ACCEPTANCES.json', 'final_acceptances_sha256')]:
        assert digest(root / name) == seal[key], key
    assert seal['final_review_gate_passed'] is True
    assert seal['external_writes'] is False
    bindings = get('COPY_BINDINGS.json')['files']
    by_path = {item['public_path']: item for item in bindings}
    for entry in bindings:
        p = root / entry['public_path']
        assert digest(p) == entry['public_sha256']
        assert p.stat().st_size == entry['public_bytes']
        if entry['transformation'] == 'EXACT_COPY':
            assert entry['source_sha256'] == entry['public_sha256']
            assert entry['source_bytes'] == entry['public_bytes']
    for family in ['c02', 'rs_families']:
        historical = get(f'{family}/candidate/MANIFEST.json')
        for entry in historical['files']:
            binding = by_path[f'{family}/candidate/{entry["path"]}']
            assert entry['sha256'] == binding['source_sha256']
            assert entry['bytes'] == binding['source_bytes']
    acceptances = get('FINAL_ACCEPTANCES.json')
    assert acceptances['accepted_dispositions'] == 2
    for result in acceptances['results']:
        assert digest(root / result['candidate_manifest_path']) == result['candidate_manifest_sha256']
        for artifact in result['review_artifacts']:
            binding = by_path[artifact['public_path']]
            assert binding['source_sha256'] == artifact['reviewed_original_sha256']
    c02_review = get('c02/review/REVIEW_CHECKS.json')
    assert c02_review['verdict'] == 'ACCEPT'
    for name, entry in c02_review['reviewed_files'].items():
        public_path = ('c02/candidate/' + name[len('public/'):]) if name.startswith('public/') else 'provenance/C02_SOURCE_MANIFEST.json'
        assert by_path[public_path]['source_sha256'] == entry['sha256']
        assert by_path[public_path]['source_bytes'] == entry['bytes']
    c02_owners = get('c02/candidate/OWNER_DISPOSITIONS.json')
    assert c02_owners['recommended_status_cell_changes'] == []
    assert c02_owners['census_change'] == 0
    assert {x['stable_id'] for x in c02_owners['owners']} == {'C02', 'NEW-05', 'Q05', 'TH-05'}
    assert all(x['recommended_status'] == 'TO RESEARCH' and x['priority'] == 52 for x in c02_owners['owners'])
    with (root / 'c02/candidate/COMPARISON_MATRIX.csv').open(newline='') as stream:
        assert list(csv.DictReader(stream)) == get('c02/candidate/COMPARISON_MATRIX.json')
    rs_stop = get('rs_families/candidate/ORIGINAL_STOP_CRITERION.json')
    assert rs_stop['owner']['stable_id'] == 'ALG-RS-FAMILIES'
    assert rs_stop['owner']['priority'] == 42
    assert rs_stop['accepted_original_scope']['separated_bases'] == [5, 9, 13, 17, 21, 25]
    assert rs_stop['accepted_original_scope']['overlap_bases'] == [3, 7, 11, 15, 19]
    assert rs_stop['separate_augmented_scope']['merged_into_historical_eleven'] is False
    assert 'F020/F022' in rs_stop['scope_exclusions']
    forbidden = [r'https?://docs[.]google[.]com/spreadsheets/d/', r'"spreadsheet_id"\s*:', r'sediment://', r'"download_url"\s*:', r'Bearer\s+[A-Za-z0-9]', r'/workspace/(?:shared|scratch)/']
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        assert p.suffix.lower() in {'.json', '.md', '.csv', '.py'}, p.name
        # The verifier contains its own generic detection patterns, not private values.
        if p.name == 'verify_package.py':
            continue
        body = p.read_text()
        assert not any(re.search(pattern, body) for pattern in forbidden), str(p)
    print(json.dumps({'status': 'PASS', 'files': len(listed), 'manifest_entries_verified': len(manifest['files']), 'copy_bindings_verified': len(bindings), 'accepted_dispositions': 2, 'scope_checks': 'PASS', 'privacy_scan': 'PASS', 'scientific_reruns': False}, indent=2))


if __name__ == '__main__':
    main()
