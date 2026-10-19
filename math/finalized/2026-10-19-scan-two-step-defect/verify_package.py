#!/usr/bin/env python3
"""Verify this exact release inventory; optional isolated replay of fresh checks."""
from pathlib import Path
from hashlib import sha256
import argparse, json, os, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parent
TARGET='math/finalized/2026-10-19-scan-two-step-defect'

def digest(data):return sha256(data).hexdigest()
def read(name):return (ROOT/name).read_bytes()
def js(name):return json.loads(read(name))
def require(test,message):
    if not test:raise AssertionError(message)
def safe(name):
    p=Path(name)
    return not p.is_absolute() and '..' not in p.parts and str(p)==name

def verify():
    files=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file())
    require(not any(p.is_symlink() for p in ROOT.rglob('*')),'Symlinks are not allowed')
    allow=js('PRESERVATION_ALLOWLIST.json')
    require(allow['repository_prefix']==TARGET,'Wrong target prefix')
    require(all(safe(x) for x in allow['files']),'Unsafe allowlist path')
    require(files==allow['files'],'Unexpected/missing public file')
    manifest=js('MANIFEST.json');expected=[x for x in files if x not in ['MANIFEST.json','SEAL.json']]
    require(sorted(x['file'] for x in manifest['files'])==expected,'Manifest inventory mismatch')
    require(len(set(x['file'] for x in manifest['files']))==len(expected),'Duplicate manifest entry')
    for row in manifest['files']:
        data=read(row['file']);require(len(data)==row['bytes'] and digest(data)==row['sha256'],'Hash mismatch: '+row['file'])
    seal=js('SEAL.json')
    for name,hashvalue in seal['bindings'].items():require(digest(read(name))==hashvalue,'Seal mismatch: '+name)
    copies={r['public_file']:r for r in js('COPY_BINDINGS.json')}
    projected={r['file']:r for r in js('PROJECTION_DISCLOSURE.json')['files']}
    for name,row in copies.items():
        require(digest(read(name))==row['public_sha256'],'Copy binding public hash: '+name)
        if row['copy_mode']=='exact_complete_file':require(row['public_sha256']==row['source_sha256'],'Inexact purported exact copy: '+name)
        else:
            pr=projected[name]
            require(pr['original_sha256']==row['source_sha256'] and pr['projected_sha256']==row['public_sha256'],'Projection/copy mismatch: '+name)
    for name,pr in projected.items():
        data=read(name);require(digest(data)==pr['projected_sha256'] and len(data)==pr['projected_bytes'],'Projection public binding: '+name)
        shift=0
        for rep in sorted(pr.get('replacements',[]),key=lambda x:x['original_byte_offset']):
            offset=rep['original_byte_offset']+shift;replacement=rep['replacement'].encode()
            require(data[offset:offset+len(replacement)]==replacement,'Replacement location mismatch: '+name)
            shift+=len(replacement)-rep['original_token_bytes']
        if 'replacements' in pr:require(pr['original_bytes']+shift==pr['projected_bytes'],'Projection length mismatch: '+name)
    # Old manifest describes originals; declared projections bridge changed metadata only.
    for row in js('provenance/ORIGINAL_CANDIDATE_MANIFEST.json'):
        name='candidate/'+row['file'];binding=copies[name]
        require(row['sha256']==binding['source_sha256'],'Original candidate manifest mismatch: '+name)
    for row in js('review/MANIFEST.json'):
        name='review/'+row['file'];require(digest(read(name))==row['sha256'] and len(read(name))==row['bytes'],'Original review manifest mismatch: '+name)
    original_report=projected['candidate/REPORT.md']['original_sha256']
    require(original_report in read('review/REVIEW.md').decode(),'Review does not bind original candidate report')
    sources=js('SOURCE_PROVENANCE.json')
    sourcebindings=js('candidate/SOURCE_BINDINGS.json')
    for source,entry in zip(sources,sourcebindings):
        require(source['original_sha256']==entry['original_sha256'],'Original source hash mismatch')
        require(source['public_sha256']==entry['sha256']==digest(read(source['bundled_path'])),'Projected source hash mismatch')
    owner=js('OWNER_DISPOSITION.json')
    require(owner['owner_id']=='M-SCAN-DIMENSION' and owner['status']=='TO RESEARCH' and owner['priority']==34,'Owner/status/priority changed')
    require(not owner['all_dyadic_H_lemma_resolved'] and not owner['actual_H_annihilator_produced'],'Endpoint completion falsely asserted')
    require(all(owner[k]==0 for k in ['owner_closures','priority_changes','census_changes']),'Closure/count change')
    domains=js('DOMAIN_LEDGER.json')
    require('Every field' in domains['commutator_theorem']['domain'],'Missing all-field K domain')
    require('only when T is invertible' in domains['woodbury_and_two_channel_system']['domain'],'Missing inverse-domain restriction')
    require('characteristic not two' in domains['symmetric_skew_decomposition']['domain'],'Missing transpose-sector field restriction')
    # These restrictions are product/privacy checks, not mathematical-proof automation.
    forbidden=[b'/workspace/',b'/home/agent/',b'docs.google.com/spreadsheets/',b'BEGIN PRIVATE KEY',b'ghp_',b'sk-proj-']
    for name in files:
        if name=='verify_package.py':continue  # Contains the scanner's own literal patterns.
        data=read(name)
        require(not any(token in data for token in forbidden),'Forbidden private/source locator in '+name)
    return {'integrity':'PASS','public_file_count':len(files),'repository_prefix':TARGET,'endpoint_gate':'UNRESOLVED','status':'TO RESEARCH','priority':34,'scientific_code_executed':False}

def replay():
    jobs=[('review/checks.py','review/RESULTS.json'),('review/commutator_checks.py','review/COMMUTATOR_RESULTS.json'),('review/wedge_checks.py','review/WEDGE_RESULTS.json'),('review/woodbury_checks.py','review/WOODBURY_RESULTS.json')]
    receipts=[]
    with tempfile.TemporaryDirectory(prefix='scan-two-step-replay-') as tmp:
        copy=Path(tmp)/'packet';shutil.copytree(ROOT,copy)
        env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['OPENBLAS_NUM_THREADS']='1'
        result=subprocess.run([sys.executable,'-B','checks.py'],cwd=copy/'candidate',env=env,check=True,capture_output=True,text=True)
        require(json.loads(result.stdout)==js('candidate/RESULTS.json'),'Candidate replay result mismatch')
        require(json.loads((copy/'candidate/RESULTS.json').read_text())==js('candidate/RESULTS.json'),'Candidate written result mismatch')
        receipts.append({'script':'candidate/checks.py','result':'PASS'})
        for script,expected in jobs:
            result=subprocess.run([sys.executable,'-B',Path(script).name],cwd=copy/Path(script).parent,env=env,check=True,capture_output=True,text=True)
            require(json.loads(result.stdout)==js(expected),'Review replay result mismatch: '+script)
            receipts.append({'script':script,'result':'PASS'})
    # Assert that the published bytes were never overwritten.
    verify()
    return receipts

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true');args=parser.parse_args()
    result=verify()
    if args.replay:result['isolated_fresh_scientific_replay']=replay();result['scientific_code_executed']=True
    print(json.dumps(result,indent=2))
