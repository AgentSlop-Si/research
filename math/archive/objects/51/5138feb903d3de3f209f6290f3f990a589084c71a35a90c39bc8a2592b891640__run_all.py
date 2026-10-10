from __future__ import annotations
import hashlib, json, subprocess, sys, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def run(args):
    cp=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
    print(cp.stdout,end='');print(cp.stderr,end='',file=sys.stderr)
    if cp.returncode:raise SystemExit(cp.returncode)

run([sys.executable,'-m','unittest','-v','test_checkpoint'])
run([sys.executable,'independent_verifier.py'])
run([sys.executable,'generate_results.py'])
print('cold run passed')
