"""Fresh read-only metadata verification; never loads or runs source programs.

Inputs are the recovery ledger, hash snapshot, and preserved archives.  ZIP
members are read as bytes.  Hash equality is evidence of identity, not proof
validity or evidence that a recorded source test was run in this review.
"""
from pathlib import Path
import hashlib
import json
import collections
import zipfile
import argparse

BASE = Path('external_inventory_text_review_0225')
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=BASE / 'metadata_replay')
OUT = parser.parse_args().output
if (OUT / 'SEALED_MANIFEST.json').exists():
    raise SystemExit('Refusing to write into a sealed output directory')
OUT.mkdir(parents=True, exist_ok=True)
COVER = Path('coverage_audit_20261010')

def sha(b):
    return hashlib.sha256(b).hexdigest()

recovery_bytes = (COVER / 'EXTERNAL_INVENTORY_RECOVERY.json').read_bytes()
recovery = json.loads(recovery_bytes)
before = json.loads((BASE / 'INPUT_HASHES_BEFORE.json').read_text())
matches = json.loads((BASE / 'EXACT_LOCAL_SOURCE_MATCHES.json').read_text())
master = json.loads((COVER / 'master_file_hashes.json').read_text())
master_hashes = {x['sha256'] for x in master}
archive_cache = {}
rows = []
for i, item in enumerate(recovery):
    # Prefer the main master copy when available, without relying on its name
    # for identity. Every selected member is hashed below.
    possibilities = sorted(item['matches'], key=lambda x: (
        not x['source_archive'].startswith('fft_research_master_20261009/'),
        x['source_archive']))
    match = next(x for x in possibilities if Path(x['source_archive']).is_file())
    archive = Path(match['source_archive'])
    if str(archive) not in archive_cache:
        archive_cache[str(archive)] = {'sha256': sha(archive.read_bytes()), 'bytes': archive.stat().st_size}
    with zipfile.ZipFile(archive) as z:
        infos = [x for x in z.infolist() if x.filename == match['member']]
        assert len(infos) == 1, (i, 'duplicate or missing ZIP member')
        member = z.read(infos[0])
    local = Path(match['local_text']).read_bytes()
    assert len(member) == item['bytes'] == len(local)
    assert sha(member) == item['sha256'] == sha(local)
    assert member == local
    assert item['sha256'] not in master_hashes
    exact_paths = []
    for path in matches[str(i)]:
        assert sha(Path(path).read_bytes()) == item['sha256']
        exact_paths.append(path)
    # Decode the complete text without silently replacing invalid bytes.
    decoded = local.decode('utf-8')
    rows.append({
        'index': i, 'origin_name': item['origin'], 'source_member': match['member'],
        'bytes': len(member), 'sha256': sha(member),
        'selected_source_archive': str(archive),
        'source_archive_sha256': archive_cache[str(archive)]['sha256'],
        'source_archive_bytes': archive_cache[str(archive)]['bytes'],
        'recovered_text': match['local_text'], 'member_byte_equality': True,
        'unique_selected_member_name': True, 'valid_utf8': True,
        'line_count': len(decoded.splitlines()),
        'absent_from_standalone_master_hash_snapshot': True,
        'already_extracted_exact_local_matches': exact_paths,
    })

known = {
    'fft_green_research_phase25_2026-10-09(1).zip': '8b12d719315eb6dfddd11f6c153c40b39e476015e752bd1f3ffb862c4ca280c5',
    'fft_green_research_phase26_2026-10-10(1).zip': 'b3b03e9c84728cc4c9e9d258967fd8092f637d32f4a0aa6ecf27e1c6ea9c206e',
    'fft_green_research_phase33_2026-10-10(1).zip': '0ff572f21b9677bf40641e82805ffd358e283374b65a33910264c6b220ed2ce4',
    'fft_green_packet_separator_v19(1).zip': 'a6dd4cd48efc8233e1cc5829eae269242b4661f92ec7f22a05222e47d935f782',
    'fft_sparse_defect_green_gate_2026-10-10(1).zip': 'f0bcde62ec1a8fff9609a463c79025edc6ac150fd910f55ccc2cfd3cc56d885b',
    'fft_hero1_mixedradix_v13_20261010.zip': 'f9ccd6749ad214bc8038660cdb41bcc9e92cdba1232f75879c1a94064b3b7090',
}
for row in rows:
    if row['origin_name'] in known:
        assert row['source_archive_sha256'] == known[row['origin_name']], row['origin_name']
        row['matches_archive_hash_declared_in_prior_audit'] = True

after = [{'index': r['index'], 'path': r['recovered_text'], 'sha256': r['sha256']} for r in rows]
# The pre-review snapshot uses its original schema. Compare sets rather than
# serializations, so this does not require modifying that historical snapshot.
before_hashes = {x['sha256'] for x in before}
assert before_hashes == {x['sha256'] for x in after}
assert len(rows) == len(before) == len(before_hashes) == 70
assert sum(r['bytes'] for r in rows) == 191264
summary = {
    'items': len(rows), 'total_bytes': sum(r['bytes'] for r in rows),
    'extensions': dict(collections.Counter(Path(r['source_member']).suffix for r in rows)),
    'origin_names': len({r['origin_name'] for r in rows}),
    'selected_archive_paths': len(archive_cache),
    'selected_archive_hashes': len({x['sha256'] for x in archive_cache.values()}),
    'member_hash_checks_passed': len(rows),
    'already_extracted_exact_local_matches': sum(bool(r['already_extracted_exact_local_matches']) for r in rows),
    'no_match_in_targeted_existing_extraction_scan': sum(not r['already_extracted_exact_local_matches'] for r in rows),
    'standalone_master_hash_matches_in_snapshot': 0,
    'before_after_recovered_hash_sets_equal': True,
    'prior_audit_archive_hashes_matched': len(known),
    'source_software_executed': False,
    'new_theorem_tests_performed_by_this_script': False,
    'recovery_ledger_sha256': sha(recovery_bytes),
    'master_hash_snapshot_sha256': sha((COVER / 'master_file_hashes.json').read_bytes()),
}
for filename, obj in [('ARCHIVE_MEMBER_VERIFICATION.json', rows), ('METADATA_CHECK_RESULTS.json', summary), ('INPUT_HASHES_AFTER.json', after)]:
    (OUT / filename).write_text(json.dumps(obj, indent=2) + '\n')
print(json.dumps(summary, indent=2))
