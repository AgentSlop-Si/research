#!/usr/bin/env python3
"""Verify the sealed package and optionally rerun tests in disposable copies."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def verify():
    listed = {}
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,relative = line.split('  ',1)
        path = ROOT/relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise AssertionError('Hash verification failed: '+relative)
        listed[relative]=digest
    present = {str(p.relative_to(ROOT)).replace('\\','/') for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'SHA256SUMS' and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    if present!=set(listed):
        raise AssertionError('Manifest coverage mismatch: '+str(present.symmetric_difference(listed)))
    return len(listed)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify-only',action='store_true')
    args=parser.parse_args()
    report={'hashes_verified':verify(),'manifest_status':'pass'}
    if not args.verify_only:
        with tempfile.TemporaryDirectory(prefix='chirp_supplement_rerun_') as tmp:
            tmp=Path(tmp)
            for dirname,script in [('chirp_audit','independent_checker.py'),('eliminant_extension','test_eliminant_extension.py')]:
                dest=tmp/dirname
                shutil.copytree(ROOT/dirname,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
                print('Rerunning '+dirname+' in a disposable copy',flush=True)
                subprocess.run([sys.executable,str(dest/script)],cwd=str(dest),check=True)
            old=json.loads((ROOT/'chirp_audit/independent_results.json').read_text())
            new=json.loads((tmp/'chirp_audit/independent_results.json').read_text())
            old.pop('elapsed_seconds',None);new.pop('elapsed_seconds',None)
            if old!=new:raise AssertionError('Original independent audit deterministic results differ')
            old_ext=json.loads((ROOT/'eliminant_extension/test_results.json').read_text())
            new_ext=json.loads((tmp/'eliminant_extension/test_results.json').read_text())
            if old_ext!=new_ext:raise AssertionError('Extension deterministic results differ')
            report.update({'original_audit_rerun':'pass','original_audit_deterministic_results_match':True,'extension_rerun':'pass','extension_deterministic_results_match':True,'original_audit_exhaustive_vectors':sum(x['vectors'] for x in new['exhaustive_membership']),'extension_test_groups':new_ext['test_groups_run'],'extension_toeplitz_bareiss_comparisons':new_ext['toeplitz_bareiss_comparisons'],'sealed_files_unchanged':verify()==report['hashes_verified']})
    print('PACKAGE_VALIDATION_JSON='+json.dumps(report,sort_keys=True),flush=True)


if __name__=='__main__':main()
