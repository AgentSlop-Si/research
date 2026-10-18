#!/usr/bin/env python3
"""Verify the frozen public packet. Standard library only; no scientific code runs."""
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def get(name):
    return json.loads((root / name).read_text(encoding='utf-8'))

allow = get('PRESERVATION_ALLOWLIST.json')
manifest = get('MANIFEST.json')
seal = get('SEAL.json')
actual = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
assert actual == sorted(allow['files']), 'Exact allowlist mismatch'
assert len(actual) == len(set(actual)), 'Duplicate allowlist entry'
assert not any(p.is_symlink() for p in root.rglob('*')), 'Symlinks forbidden'
assert set(x['path'] for x in manifest['files']) == set(actual) - {'MANIFEST.json', 'SEAL.json'}
for rec in manifest['files']:
    path = root / rec['path']
    assert path.resolve().is_relative_to(root), rec['path']
    assert path.stat().st_size == rec['bytes'], rec['path']
    assert digest(path) == rec['sha256'], rec['path']
assert digest(root / 'MANIFEST.json') == seal['manifest_sha256']
assert digest(root / 'PRESERVATION_ALLOWLIST.json') == seal['allowlist_sha256']
assert digest(root / 'FINAL_ACCEPTANCES.json') == seal['final_acceptances_sha256']
assert seal['final_review_gate_passed'] is True
assert seal['scientific_reruns_during_packaging'] is False
assert seal['external_writes'] is False
for rec in get('COPY_BINDINGS.json')['files']:
    assert digest(root / rec['public_path']) == rec['public_sha256'], rec['public_path']
    if rec['mode'] == 'BYTE_EXACT':
        assert rec['original_sha256'] == rec['public_sha256'], rec['public_path']
    if rec['mode'] == 'EXTRACTED_SOURCE_BODY':
        assert rec['extracted_body_sha256'] == rec['public_sha256'], rec['public_path']
for name in actual:
    path = root / name
    assert path.suffix.lower() not in {'.pdf','.png','.jpg','.jpeg','.webp','.gif','.zip','.gz','.pyc'}, name
    data = path.read_text(encoding='utf-8')
    # Detect literal private register locators and common secret formats, without storing them.
    assert not re.search(r'https?://docs[.]google[.]com/(?:spreadsheets|document)/d/', data), name
    assert not re.search(r'"spreadsheet(?:_id|Id)"\s*:\s*"(?!WITHHELD)[^"]+"', data), name
    assert not re.search(r'(?:github_pat_|ghp_|gho_)[A-Za-z0-9_]{20,}', data), name
    assert not re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', data), name
    if path.suffix == '.json':
        json.loads(data)
verdicts = get('FINAL_ACCEPTANCES.json')
assert verdicts['original_scope_owner_closure_recommendations'] == ['M-FCUT','M-HARPER','ALG-FINITE-CHIRP-1001']
assert verdicts['F015_broader_owner_remains_open'] is True
assert verdicts['successors_unchanged'] == {'Q14':37,'STR-Q5':37}
assert verdicts['finite_chirp_range'] == {'first_odd':3,'last_odd':1001,'odd_sizes':500,'parent_owner':'F021','broader_parent_closed':False}
assert len(get('fcut/candidate/CLOSURE_MATRIX.json')['clauses']) == 14
assert len(get('harper/candidate/CLAUSE_DISPOSITION_MATRIX.json')) == 19
assert get('f015/candidate/DISPOSITION.json')['whole_owner_closure_recommended'] is False
assert get('finite_chirp/candidate/VERDICT.json')['finite_range']['odd_sizes'] == 500
print(json.dumps({'status':'PASS','verified_files':len(actual),'manifest_sha256':digest(root/'MANIFEST.json'),'seal_sha256':digest(root/'SEAL.json'),'privacy_pattern_screen':'PASS','scientific_programs_executed':False,'external_writes':False}, indent=2))
