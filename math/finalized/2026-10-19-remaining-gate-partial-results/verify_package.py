#!/usr/bin/env python3
"""Verify documentary integrity only; never execute scientific programs."""
from pathlib import Path
import hashlib
import json
import re


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    get = lambda name: json.loads((root / name).read_text())
    allow = get('PRESERVATION_ALLOWLIST.json')
    paths = allow['files']
    assert len(paths) == len(set(paths))
    assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in paths)
    assert not any(p.is_symlink() for p in root.rglob('*'))
    assert sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()) == sorted(paths)
    manifest = get('MANIFEST.json')
    assert sorted(x['path'] for x in manifest['files']) == sorted(set(paths) - {'MANIFEST.json', 'SEAL.json'})
    for item in manifest['files']:
        p = root / item['path']
        assert p.stat().st_size == item['bytes'] and sha(p) == item['sha256'], item['path']
    seal = get('SEAL.json')
    for name, key in [('MANIFEST.json', 'manifest_sha256'), ('PRESERVATION_ALLOWLIST.json', 'allowlist_sha256'), ('FINAL_ACCEPTANCES.json', 'final_acceptances_sha256')]:
        assert sha(root / name) == seal[key], key
    assert seal['final_review_gate_passed'] is True
    assert seal['accepted_partial_result_packets'] == 2
    assert seal['owner_closures'] == 0
    assert seal['historical_novelty_claim'] is False
    assert seal['scientific_reruns_during_packaging'] is False
    assert seal['external_writes'] is False
    bindings = get('COPY_BINDINGS.json')['files']
    by_path = {x['public_path']: x for x in bindings}
    assert len(by_path) == len(bindings)
    for item in bindings:
        p = root / item['public_path']
        assert sha(p) == item['public_sha256'] and p.stat().st_size == item['public_bytes'], item['public_path']
        if item['transformation'] == 'EXACT_COPY':
            assert item['public_sha256'] == item['source_sha256']
            assert item['public_bytes'] == item['source_bytes']
    for directory in ['f020/candidate', 'f020/review', 'phase/candidate']:
        historical = get(directory + '/MANIFEST.json')
        declared = {directory + '/' + x['path'] for x in historical['files']} | {directory + '/MANIFEST.json'}
        copied = {p for p in by_path if p.startswith(directory + '/')}
        assert copied == declared, directory
        for item in historical['files']:
            bound = by_path[directory + '/' + item['path']]
            assert item['sha256'] == bound['source_sha256'] and item['bytes'] == bound['source_bytes']
    accept = get('FINAL_ACCEPTANCES.json')
    assert accept['accepted_partial_result_packets'] == 2
    assert accept['owner_closures'] == 0
    for result in accept['results']:
        assert sha(root / result['candidate_manifest_path']) == result['candidate_manifest_sha256']
        for artifact in result['review_artifacts']:
            bound = by_path[artifact['public_path']]
            assert artifact['reviewed_original_sha256'] == bound['source_sha256']
            assert artifact['public_sha256'] == bound['public_sha256']
    f = get('f020/review/VERDICT.json')
    assert f['verdict'] == 'ACCEPT_SCOPED' and f['blocking_corrections'] == []
    assert f['author_manifest_sha256'] == sha(root / 'f020/candidate/MANIFEST.json')
    assert f['automatic_owner_closure'] is False
    assert f['author_replay_assertions'] == 19 and f['independent_exact_and_source_assertions'] == 55
    assert f['author_report_sha256'] == by_path['f020/candidate/REPORT.md']['source_sha256']
    p = get('phase/candidate/VERDICT.json')
    assert p['status'] == 'ACCEPTED_PARTIAL_RESULTS_SHARP_GLOBAL_OPEN'
    assert p['global_lower_bound'] == 'sin(pi/16)/sqrt(13+4*sqrt(3)*cos(pi/16))'
    assert p['accepted_upper_bound'] == 'sin(pi/16)'
    assert p['sharp_global_value_proved'] is False and p['exact_counterexample_found'] is False
    assert get('phase/candidate/EXACT_LOCAL_CHECKS.json')['status'] == 'PASS'
    for item in get('f020/candidate/SOURCE_BINDINGS.json')['sources']:
        bound = by_path['f020/candidate/' + item['file']]
        assert item['sha256'] == bound['source_sha256'] and item['bytes'] == bound['source_bytes']
    for item in get('phase/candidate/PROVENANCE.json')['source_records']:
        bound = by_path['phase/candidate/' + item['frozen_path']]
        assert item['sha256'] == bound['source_sha256'] and item['bytes'] == bound['source_bytes']
    disclosure = get('PROJECTION_DISCLOSURE.json')
    assert len(disclosure['files']) == 1
    projected = disclosure['files'][0]
    assert projected['public_path'] == 'phase/candidate/PROVENANCE.json'
    assert projected['removed_field'] == 'independent_reviewer'
    assert 'independent_reviewer' not in get('phase/candidate/PROVENANCE.json')
    forbidden = [r'https?://docs[.]google[.]com/spreadsheets/d/', r'"spreadsheet_id"\s*:', r'sediment://', r'"download_url"\s*:', r'Bearer\s+[A-Za-z0-9]', r'/root/', r'dream_notes', r'cloud_threads']
    for file in root.rglob('*'):
        if not file.is_file():
            continue
        assert file.suffix.lower() in {'.json', '.md', '.py', '.log', '.txt'}, file.name
        if file.name == 'verify_package.py':
            continue
        text = file.read_text()
        assert not any(re.search(pattern, text) for pattern in forbidden), str(file)
    print(json.dumps({'status': 'PASS', 'files': len(paths), 'manifest_entries_verified': len(manifest['files']), 'copy_bindings_verified': len(bindings), 'accepted_partial_result_packets': 2, 'owner_closures': 0, 'scope_checks': 'PASS', 'privacy_scan': 'PASS', 'scientific_reruns': False}, indent=2))


if __name__ == '__main__':
    main()
