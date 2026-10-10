"""From a clean extraction: verify the new research tests and the nested prior checkpoint.
Use: python verify_checkpoint.py
"""
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

root=Path(__file__).resolve().parent

def run(args,cwd):
    result=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
    print(result.stdout,end='')
    print(result.stderr,end='',file=sys.stderr)
    if result.returncode:
        raise SystemExit(f'Failed: {args}, rc={result.returncode}')

print('New research verifier:')
run([sys.executable,'-m','unittest','-v','test_twisted_gate'],root)

with tempfile.TemporaryDirectory(prefix='fft_prior_clean_') as temp:
    path=Path(temp)
    with zipfile.ZipFile(root/'prior_checkpoint_full.zip') as z:
        for member in z.namelist():
            destination=(path/member).resolve()
            if not destination.is_relative_to(path.resolve()):
                raise RuntimeError('Unsafe prior ZIP path')
        z.extractall(path)
    print('Previous sparse-defect checkpoint:')
    run([sys.executable,'run_all.py'],path/'fft_sparse_defect_gate_2026-10-10')
print('PASS: 11 new test groups and 7+3 previous checkpoint groups')
