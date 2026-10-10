#!/usr/bin/env python3
"""Phase15 standalone verification with optional complete Phase14 replay."""
import argparse,subprocess,sys,tempfile,zipfile
from pathlib import Path

root=Path(__file__).resolve().parent

def call(*args,cwd=root):
    print('>>>',*args,flush=True)
    subprocess.run([sys.executable,*args],cwd=cwd,check=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--full-lineage',action='store_true',help='Re-extract Phase14 intact and rerun its full suite')
    args=parser.parse_args()
    call('-m','unittest','-v','test_phase15')
    call('conditioning.py')
    call('slope_tradeoff.py')
    call('field_joint_audit.py')
    call('field_slope_audit.py')
    if args.full_lineage:
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            with zipfile.ZipFile(root/'PRIOR_PHASE14_COMPLETE.zip') as archive:
                names=archive.namelist()
                if any(x.startswith('/') or '..' in Path(x).parts for x in names):
                    raise RuntimeError('Unsafe archive entries in lineage bundle')
                archive.extractall(base)
            call('run_all.py',cwd=base/'fft_hero1_phase14')
    print('PHASE15 PASSED: 8 new unittest cases, analytic condition/rank tests, exact finite-field joint and slope gates',flush=True)

if __name__=='__main__':main()
