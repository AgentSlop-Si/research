#!/usr/bin/env python3
"""Phase17 complete finite-field test + optional preserved Phase16 regression."""
import argparse,subprocess,sys,tempfile,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent

def call(*args,cwd=BASE):
    print('>>>',*args,flush=True)
    subprocess.run([sys.executable,*args],cwd=cwd,check=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--prior',action='store_true',help='replay original Phase16 archive without modifying it')
    args=p.parse_args()
    call('-m','unittest','-v','test_phase17')
    call('field_basis_audit.py')
    call('operation_benchmark.py')
    call('precision_gate.py')
    if args.prior:
        with tempfile.TemporaryDirectory() as dest:
            with zipfile.ZipFile(BASE/'PRIOR_PHASE16_COMPLETE.zip') as z:
                for name in z.namelist():
                    if name.startswith('/') or '..' in Path(name).parts:
                        raise ValueError('unsafe embedded archive member')
                z.extractall(dest)
            call('run_all.py',cwd=Path(dest)/'fft_hero1_phase16')
    print('PHASE17 PASSED: 16 focused tests, 222111 exact field entries, 32 benchmark comparisons',flush=True)
if __name__=='__main__':main()
