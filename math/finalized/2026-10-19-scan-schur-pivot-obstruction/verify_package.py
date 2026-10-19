#!/usr/bin/env python3
"""Read-only publication integrity check; never runs any research program."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def read(name): return json.loads((ROOT/name).read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check_entry(e):
    name=e.get('file',e.get('public_path'))
    assert name and not Path(name).is_absolute() and '..' not in Path(name).parts, name
    p=ROOT/name
    assert p.is_file() and not p.is_symlink(), name
    b=p.read_bytes()
    assert len(b)==e['bytes'], 'Length mismatch: '+name
    assert hashlib.sha256(b).hexdigest()==e['sha256'], 'SHA-256 mismatch: '+name
    if 'git_blob_sha1' in e:
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha1'], 'Git blob mismatch: '+name

allow=read('PRESERVATION_ALLOWLIST.json')
actual=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file())
assert not any(p.is_symlink() for p in ROOT.rglob('*')), 'No symlinks allowed.'
assert actual==allow['files'], 'Public inventory differs from allowlist.'
assert len(actual)==len(set(actual)), 'Duplicate paths.'
manifest=read('MANIFEST.json')
expected=sorted(set(actual)-{'MANIFEST.json','SEAL.json'})
assert [e['file'] for e in manifest['files']]==expected, 'Manifest inventory mismatch.'
for e in manifest['files']: check_entry(e)
seal=read('SEAL.json')
for file,key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('OWNER_DISPOSITION.json','owner_disposition_sha256'),('review/ACCEPTANCE.json','original_acceptance_sha256')]:
    assert sha(ROOT/file)==seal[key], 'Seal mismatch: '+file
assert seal['public_file_count']==len(actual)
for label in ['candidate','review']:
    for e in read(label+'/MANIFEST.json'):
        check_entry({**e,'file':label+'/'+e['file']})
copy=read('COPY_BINDINGS.json')['files']
for e in copy:
    assert e['transformation']=='EXACT_COPY'
    check_entry(e)
assert sha(ROOT/'candidate/REPORT.md')=='46968f362319f164f5eb01476d46899b34b9c1593f48a9cd412250f649c355ba'
assert sha(ROOT/'review/REVIEW.md')=='ec757a67f24113073b95771b2145384967501f4ef17a0ec9c689ec49921bdc81'
accept=read('review/ACCEPTANCE.json')
owner=read('OWNER_DISPOSITION.json')
assert accept['verdict']=='ACCEPT_SCOPED_STRUCTURAL_RESULTS_ONLY'
for field in ['all_dyadic_H_lemma_resolved','endpoint_anchor_disproved','generic_dominance_disproved','completion_gate_passed']:
    assert accept[field] is False and owner[field] is False
assert owner['owner_id']=='M-SCAN-DIMENSION' and owner['status']=='TO RESEARCH' and owner['priority']==34
assert owner['owner_closures']==owner['priority_changes']==owner['census_changes']==0
assert owner['new_owner'] is False and owner['historical_novelty_claim'] is False
assert 'N/4+log2(N)-1' in json.dumps(owner['accepted_new_scope'])
assert 'G=O/9' in json.dumps(owner['accepted_new_scope'])
assert 'h+q+1 for even q and h+q for odd q' in json.dumps(owner['accepted_new_scope'])
author_control=read('candidate/RESULTS.json')['positive_scope_control']
review_control=read('review/REVIEWER_RESULTS.json')['positive_control']
assert author_control['H_rank_mod5']==64 and author_control['odd_dressed_pivot_determinant_Q']=='-10/81'
assert author_control['odd_dressed_pivot_rank_mod5']==3 and author_control['does_not_imply_H_failure'] is True
assert review_control['N']==8 and review_control['ranks']=={'5':64,'12289':64}
checks=read('PACKAGING_CHECKS.json')
assert checks['scientific_programs_imported_or_executed']==0
assert checks['scientific_reruns_during_packaging'] is False and checks['external_writes'] is False
assert checks['privacy_projection_count']==0 and checks['privacy_pattern_matches']==[]
assert checks['prior_packets_or_index_modified'] is False and checks['fresh_native_read'] is False
assert checks['exact_source_copies']==len(copy)==17
print(json.dumps({'result':'PASS','verification_kind':'READ_ONLY_BYTES_AND_SCOPE','public_files':len(actual),'manifest_payload_entries':len(manifest['files']),'exact_source_copies':len(copy),'scientific_programs_executed':0,'owner':'M-SCAN-DIMENSION','owner_status':'TO RESEARCH','priority':34,'completion_gate_passed':False,'manifest_sha256':sha(ROOT/'MANIFEST.json'),'seal_sha256':sha(ROOT/'SEAL.json')},indent=2))
