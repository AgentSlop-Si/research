#!/usr/bin/env python3
"""Offline public identity/status checks only; never executes research code."""
import argparse
import hashlib
import json
import re
from pathlib import Path

PAYLOAD = {
    'README.md', 'REPORT.md', 'UNPRICED_LEDGER.json', 'VERDICT.json',
    'COVERAGE.md', 'SOURCE_IDENTITIES.json', 'EXPORT_MAP.json',
    'BUILD_RECEIPT.json', 'evidence/INDEPENDENT_REVIEW.md',
    'evidence/FROZEN_PACKET_RESULTS.json', 'verify_packet.py',
    'verification/test_controls.py', 'verification/CONTROL_RESULTS.json',
}
EXCLUDED = {'MANIFEST.json', 'SEAL.json'}
DIRECTORIES = {'evidence', 'verification'}
WIDTHS = [2, 3, 4, 5, 8, 16, 17, 32]
STABLE_ID = 'BORROWED-FOURIER-COMPILER-20261012'
CANDIDATE = '81713639a3d227b3981e9b2baf7b2bdb4da3025db4457fc6412dec709e5536f4'
REVIEW = '640b9dab68d2fed744b42f18612a92573ed7e4f34d5eabd97d5ed9caa2e125df'
ORIGINAL_REPORT = 'f3fac36a41302dcbb1f354efc9d1ef6c781c2a5a3dfa75c909d86b60b5d38828'
FROZEN = {
    'REPORT.md': '037c46ab785936d4cc19020090eb790f723c736a33f6cf9f6993b7c9d4c3f06c',
    'UNPRICED_LEDGER.json': '3705d106f3179f57c9407c4291456e1dcbe0eb5ee55b8c22e9d10625d486e654',
    'VERDICT.json': '538298de0e6f0c96d54126213eb6af17fe7edcfd2921007beae3e96b5af65687',
    'evidence/INDEPENDENT_REVIEW.md': '26bc159f8c943b9dc9b84ca2cb486fb5d1428440cc7f4445adb325bbf4bf0edf',
    'evidence/FROZEN_PACKET_RESULTS.json': '7579c29993a3b0cc0c936bac429c948ca861aa1245e12d3dea95e1544b170e89',
    'SOURCE_IDENTITIES.json': '5b697d2979546dd6bef4b832a9b214a78bd857097704ea29dcbd678fbd91cf37',
    'EXPORT_MAP.json': '0713fb21df35d6f1d55eb754ddec248cd698976af796c2682d7a334334b4cdfb',
    'BUILD_RECEIPT.json': '8a66edb95f3a9dcb60441048d4ca9d040fa0b70701fe324becb6bedac46b2080',
    'COVERAGE.md': 'df19f1841c18cfe814092b2133680c59d076ee1ad631ee3aea2dec414b7ca95e',
}

class Invalid(ValueError):
    pass

def need(condition, message):
    if not condition:
        raise Invalid(message)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def strict_object(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key: ' + key)
        out[key] = value
    return out

def reject_constant(value):
    raise Invalid('nonstandard JSON numeric constant: ' + value)

def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'),
                      object_pairs_hook=strict_object, parse_constant=reject_constant)

def sha(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None

def integer(value, expected=None):
    return type(value) is int and (expected is None or value == expected)

def validate_ledger(x):
    need(type(x) is dict, 'ledger must be an object')
    need(x.get('stable_id') == STABLE_ID, 'wrong stable ID')
    need(x.get('disposition') == 'EXACT_UNPRICED_OBLIGATION', 'wrong disposition')
    need(x.get('pilot_completed') is False, 'pilot must remain incomplete boolean false')
    need(x.get('parent_status_unchanged') == 'TO RESEARCH', 'parent status must remain open')
    need(integer(x.get('priority_unchanged'), 32), 'priority must be integer 32')
    need(x.get('original_archive_recovered') is True, 'archive recovery flag must be true')
    need(x.get('library_matched_archive_is_pre_correction') is True, 'old archive must remain pre-correction')
    rows = x.get('widths')
    need(type(rows) is list and len(rows) == len(WIDTHS), 'eight width rows required')
    for row, n in zip(rows, WIDTHS):
        need(type(row) is dict and set(row) == {'width','complete_program_cost','status','reason_ids'}, 'bad width row schema')
        need(integer(row['width'], n), 'width must have its fixed integer value')
        need(row['complete_program_cost'] is None, 'complete costs must be null, not zero or false')
        need(row['status'] == 'UNPRICED_COMPLETE_PAIRED_PROGRAM', 'wrong width status')
        need(row['reason_ids'] == ['paired_complete_program','complete_preparation','movement_storage'], 'missing cost obligations')
    reasons = x.get('unpriced_obligations')
    need(type(reasons) is list, 'obligations must be a list')
    need([r.get('id') for r in reasons] == ['accepted_revision_binding','paired_complete_program','complete_preparation','movement_storage','characteristic_zero_coverage','bit_model'], 'obligation inventory changed')
    need(reasons[4]['widths'] == [3,5,17] and all(type(n) is int for n in reasons[4]['widths']), 'odd-root coverage widths changed')


def verify(root, expected_manifest=None):
    root = Path(root).resolve()
    entries = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in entries), 'symlink is forbidden')
    actual_files = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    actual_dirs = {p.relative_to(root).as_posix() for p in entries if p.is_dir()}
    need(actual_dirs == DIRECTORIES, 'directory inventory mismatch')
    need(actual_files == PAYLOAD | EXCLUDED, 'exact file inventory mismatch')
    need(len(entries) == len(actual_files) + len(actual_dirs), 'nonregular filesystem entry')
    parsed = {name: load_json(root/name) for name in actual_files if name.endswith('.json')}
    manifest = parsed['MANIFEST.json']
    seal = parsed['SEAL.json']
    need(type(manifest) is list, 'manifest must be a list')
    listed = []
    for r in manifest:
        need(type(r) is dict and set(r) == {'path','bytes','sha256'}, 'manifest entry schema')
        need(type(r['path']) is str and r['path'] in PAYLOAD, 'manifest path not allowlisted')
        need(integer(r['bytes']) and r['bytes'] >= 0, 'manifest byte length must be integer')
        need(sha(r['sha256']), 'manifest hash format')
        listed.append(r['path'])
        b = (root/r['path']).read_bytes()
        need(len(b) == r['bytes'] and digest(b) == r['sha256'], 'payload bytes changed: ' + r['path'])
    need(len(listed) == len(set(listed)) and set(listed) == PAYLOAD, 'duplicate or missing manifest entry')
    need(listed == sorted(listed), 'manifest ordering must be canonical')
    need(type(seal) is dict and set(seal) == {'schema_version','stable_id','scope','files','manifest_sha256','report_sha256','candidate_manifest_sha256','independent_review_manifest_sha256','pilot_completed','parent_status','priority','excluded_exact_root_paths'}, 'seal schema')
    need(integer(seal['schema_version'],1) and integer(seal['files'],len(PAYLOAD)), 'seal integer fields')
    need(seal['stable_id']==STABLE_ID and seal['scope']=='BOUNDED_PUBLIC_IDENTITY_AND_STATUS_CHECKS_ONLY','seal scope')
    mb = (root/'MANIFEST.json').read_bytes()
    need(sha(seal['manifest_sha256']) and digest(mb)==seal['manifest_sha256'], 'seal manifest hash')
    if expected_manifest is not None:
        need(sha(expected_manifest) and digest(mb)==expected_manifest, 'external manifest anchor mismatch')
    need(seal['report_sha256']==FROZEN['REPORT.md'], 'report seal anchor')
    need(seal['candidate_manifest_sha256']==CANDIDATE and seal['independent_review_manifest_sha256']==REVIEW, 'source seal anchors')
    need(seal['pilot_completed'] is False and seal['parent_status']=='TO RESEARCH' and integer(seal['priority'],32), 'seal status')
    need(seal['excluded_exact_root_paths']==sorted(EXCLUDED), 'only exact root exclusions allowed')
    validate_ledger(parsed['UNPRICED_LEDGER.json'])
    for name, expected in FROZEN.items():
        need(digest((root/name).read_bytes())==expected, 'frozen export anchor mismatch: '+name)
    identities = parsed['SOURCE_IDENTITIES.json']
    need(integer(identities['schema_version'],1), 'identity version type')
    roles={x['role']:x for x in identities['selected_sources']}
    need(len(roles)==19 and roles['accepted_candidate_v2_manifest']['sha256']==CANDIDATE and roles['independent_review_manifest']['sha256']==REVIEW and roles['accepted_scientific_report_original']['sha256']==ORIGINAL_REPORT, 'source anchor inventory')
    for row in identities['selected_sources']:
        need(integer(row['bytes']) and row['bytes']>=0 and sha(row['sha256']), 'source identity strict types')
        if row['included_path'] is not None:
            need(row['included_path'] in PAYLOAD, 'included source path')
            b=(root/row['included_path']).read_bytes()
            need(len(b)==row['bytes'] and digest(b)==row['sha256'], 'included source identity mismatch')
    old=roles['earlier_pre_correction_matched_manifest']['sha256']
    newer=identities['unrecovered_accepted_bodies']
    need(old=='d42781f8737b83c1e886eb70560128169ae39aa057da7f43325d12bfb868d060' and [x['sha256'] for x in newer]==['4e5e75b8e1fd946a3224900231e732f2768180285696c9e09cd06faba618b9f3','937b256ad983a6a23ddc024d7d2bd8f11a6d1d7b3e0ccdbd83dddb35dfd16a32'], 'old/new identity gap changed')
    need(all(x['bytes'] is None and x['included_path'] is None and x['state']=='NOT_RECOVERED_IN_BOUNDED_SEARCH' for x in newer), 'unrecovered bodies cannot be asserted present')
    mapping=parsed['EXPORT_MAP.json']
    need(mapping['report_scientific_text_unchanged'] is True and len(mapping['exports'])==5 and len(mapping['report_changes'])==4, 'projection map scope')
    for row in mapping['exports']:
        need(integer(row['original_bytes']) and integer(row['export_bytes']) and sha(row['original_sha256']) and sha(row['export_sha256']), 'export map types')
        b=(root/row['export_path']).read_bytes()
        need(len(b)==row['export_bytes'] and digest(b)==row['export_sha256'], 'export-map byte binding')
        if row['transformation']=='byte_identical':
            need(row['original_bytes']==row['export_bytes'] and row['original_sha256']==row['export_sha256'], 'unchanged source mismatched')
    controls=parsed['verification/CONTROL_RESULTS.json']
    need(set(controls)=={'schema_version','scope','baseline_passed','all_controls_detected','control_count','controls'}, 'control receipt schema')
    need(integer(controls['schema_version'],1) and controls['scope']=='PUBLIC_PACKET_CHECKS_ONLY' and controls['baseline_passed'] is True and controls['all_controls_detected'] is True, 'control receipt flags')
    need(type(controls['controls']) is list and integer(controls['control_count'],len(controls['controls'])) and controls['control_count']>=20, 'control receipt count')
    need(all(type(c) is dict and set(c)=={'mutation','resealed','detected'} and type(c['mutation']) is str and type(c['resealed']) is bool and c['detected'] is True for c in controls['controls']), 'control result strict schema')
    # Narrow marker screen in public prose/JSON, not a universal privacy proof.
    blocked=['docs.google.com/spreadsheets/','/work'+'space/','library_file'+'_id','cloud_browser'+'_handoff','sediment'+':/','codex'+':/','elicitation_request'+'_id']
    for name in sorted(actual_files):
        if name.endswith(('.json','.md')):
            t=(root/name).read_text(encoding='utf-8')
            need(not any(s in t for s in blocked), 'private locator marker in '+name)
    return {'all_checks_passed':True,'scope':'BOUNDED_PUBLIC_IDENTITY_AND_STATUS_CHECKS_ONLY','manifest_sha256':digest(mb),'payload_files':len(PAYLOAD),'total_files':len(actual_files),'selected_source_identities':len(roles),'widths':WIDTHS,'complete_program_costs':[None]*8,'pilot_completed':False,'parent_status':'TO RESEARCH','priority':32,'original_programs_executed':False,'full_source_replay':False,'mathematical_replay':False}

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    p.add_argument('--expected-manifest')
    a=p.parse_args()
    try:
        result=verify(a.root,a.expected_manifest)
    except (Invalid,ValueError,KeyError,TypeError,OSError) as e:
        print(json.dumps({'all_checks_passed':False,'error':str(e)},indent=2))
        raise SystemExit(1)
    print(json.dumps(result,indent=2))
